import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.utils import check_java_installation, sanitize_varname


class JsonReader(ir.Stmt):

    def __init__(self, df_out, loc, out_vars, out_types, file_name,
        df_colnames, orient, convert_dates, precise_float, lines,
        compression, storage_options):
        self.connector_typ = 'json'
        self.df_out = df_out
        self.loc = loc
        self.out_vars = out_vars
        self.out_types = out_types
        self.file_name = file_name
        self.df_colnames = df_colnames
        self.orient = orient
        self.convert_dates = convert_dates
        self.precise_float = precise_float
        self.lines = lines
        self.compression = compression
        self.storage_options = storage_options

    def __repr__(self):
        return ('{} = ReadJson(file={}, col_names={}, types={}, vars={})'.
            format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars))


import llvmlite.binding as ll
from bodo.io import json_cpp
ll.add_symbol('json_file_chunk_reader', json_cpp.json_file_chunk_reader)
json_file_chunk_reader = types.ExternalFunction('json_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    bool_, types.int64, types.voidptr, types.voidptr,
    storage_options_dict_type))


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    zdfnw__kuc = []
    ouszk__acdd = []
    dioa__xltmx = []
    for lowc__rag, sznpg__nhac in enumerate(json_node.out_vars):
        if sznpg__nhac.name in lives:
            zdfnw__kuc.append(json_node.df_colnames[lowc__rag])
            ouszk__acdd.append(json_node.out_vars[lowc__rag])
            dioa__xltmx.append(json_node.out_types[lowc__rag])
    json_node.df_colnames = zdfnw__kuc
    json_node.out_vars = ouszk__acdd
    json_node.out_types = dioa__xltmx
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        axez__qwehq = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        ezpyk__sis = json_node.loc.strformat()
        nyziv__lpuve = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', axez__qwehq,
            ezpyk__sis, nyziv__lpuve)
        eovw__czf = [kliox__kcse for lowc__rag, kliox__kcse in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            lowc__rag], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if eovw__czf:
            gwxn__hzzpz = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                gwxn__hzzpz, ezpyk__sis, eovw__czf)
    parallel = False
    if array_dists is not None:
        parallel = True
        for npui__cki in json_node.out_vars:
            if array_dists[npui__cki.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                npui__cki.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    zmk__kvcd = len(json_node.out_vars)
    dlv__hxwg = ', '.join('arr' + str(lowc__rag) for lowc__rag in range(
        zmk__kvcd))
    rwc__hkjs = 'def json_impl(fname):\n'
    rwc__hkjs += '    ({},) = _json_reader_py(fname)\n'.format(dlv__hxwg)
    httel__vhup = {}
    exec(rwc__hkjs, {}, httel__vhup)
    jlvb__vdtct = httel__vhup['json_impl']
    gng__gpq = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    xdavn__yokj = compile_to_numba_ir(jlvb__vdtct, {'_json_reader_py':
        gng__gpq}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(xdavn__yokj, [json_node.file_name])
    hmjd__myr = xdavn__yokj.body[:-3]
    for lowc__rag in range(len(json_node.out_vars)):
        hmjd__myr[-len(json_node.out_vars) + lowc__rag
            ].target = json_node.out_vars[lowc__rag]
    return hmjd__myr


numba.parfors.array_analysis.array_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[JsonReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[JsonReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[JsonReader] = remove_dead_json
numba.core.analysis.ir_extension_usedefs[JsonReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[JsonReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[JsonReader] = json_distributed_run
compiled_funcs = []


def _gen_json_reader_py(col_names, col_typs, typingctx, targetctx, parallel,
    orient, convert_dates, precise_float, lines, compression, storage_options):
    yuu__cpei = [sanitize_varname(kliox__kcse) for kliox__kcse in col_names]
    rzgeo__fclw = ', '.join(str(lowc__rag) for lowc__rag, prjwe__ojyr in
        enumerate(col_typs) if prjwe__ojyr.dtype == types.NPDatetime('ns'))
    dbhoj__gvwpi = ', '.join(["{}='{}'".format(hcg__sfu, bodo.ir.csv_ext.
        _get_dtype_str(prjwe__ojyr)) for hcg__sfu, prjwe__ojyr in zip(
        yuu__cpei, col_typs)])
    ylwj__odke = ', '.join(["'{}':{}".format(axaq__pif, bodo.ir.csv_ext.
        _get_pd_dtype_str(prjwe__ojyr)) for axaq__pif, prjwe__ojyr in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    rwc__hkjs = 'def json_reader_py(fname):\n'
    rwc__hkjs += '  df_typeref_2 = df_typeref\n'
    rwc__hkjs += '  check_java_installation(fname)\n'
    rwc__hkjs += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    rwc__hkjs += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    rwc__hkjs += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    rwc__hkjs += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    rwc__hkjs += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    rwc__hkjs += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    rwc__hkjs += "      raise FileNotFoundError('File does not exist')\n"
    rwc__hkjs += f'  with objmode({dbhoj__gvwpi}):\n'
    rwc__hkjs += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    rwc__hkjs += f'       convert_dates = {convert_dates}, \n'
    rwc__hkjs += f'       precise_float={precise_float}, \n'
    rwc__hkjs += f'       lines={lines}, \n'
    rwc__hkjs += '       dtype={{{}}},\n'.format(ylwj__odke)
    rwc__hkjs += '       )\n'
    rwc__hkjs += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for hcg__sfu, axaq__pif in zip(yuu__cpei, col_names):
        rwc__hkjs += '    if len(df) > 0:\n'
        rwc__hkjs += "        {} = df['{}'].values\n".format(hcg__sfu,
            axaq__pif)
        rwc__hkjs += '    else:\n'
        rwc__hkjs += '        {} = np.array([])\n'.format(hcg__sfu)
    rwc__hkjs += '  return ({},)\n'.format(', '.join(cacgl__uhwp for
        cacgl__uhwp in yuu__cpei))
    gdhlc__hopkh = globals()
    gdhlc__hopkh.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode':
        objmode, 'check_java_installation': check_java_installation,
        'df_typeref': bodo.DataFrameType(tuple(col_typs), bodo.
        RangeIndexType(None), tuple(col_names)),
        'get_storage_options_pyobject': get_storage_options_pyobject})
    httel__vhup = {}
    exec(rwc__hkjs, gdhlc__hopkh, httel__vhup)
    gng__gpq = httel__vhup['json_reader_py']
    hfsq__txf = numba.njit(gng__gpq)
    compiled_funcs.append(hfsq__txf)
    return hfsq__txf
