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
    jedc__wcd = []
    nvym__nhs = []
    oza__cbt = []
    for jbw__glce, sep__pwfxk in enumerate(json_node.out_vars):
        if sep__pwfxk.name in lives:
            jedc__wcd.append(json_node.df_colnames[jbw__glce])
            nvym__nhs.append(json_node.out_vars[jbw__glce])
            oza__cbt.append(json_node.out_types[jbw__glce])
    json_node.df_colnames = jedc__wcd
    json_node.out_vars = nvym__nhs
    json_node.out_types = oza__cbt
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        ygkc__xyfno = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        jqs__mhh = json_node.loc.strformat()
        vuzue__rfy = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', ygkc__xyfno,
            jqs__mhh, vuzue__rfy)
        fcana__mis = [pcunj__afro for jbw__glce, pcunj__afro in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            jbw__glce], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if fcana__mis:
            xhcc__hfeah = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                xhcc__hfeah, jqs__mhh, fcana__mis)
    parallel = False
    if array_dists is not None:
        parallel = True
        for pach__oej in json_node.out_vars:
            if array_dists[pach__oej.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                pach__oej.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    jdd__gqfy = len(json_node.out_vars)
    rka__pkkyf = ', '.join('arr' + str(jbw__glce) for jbw__glce in range(
        jdd__gqfy))
    qyebd__fwpt = 'def json_impl(fname):\n'
    qyebd__fwpt += '    ({},) = _json_reader_py(fname)\n'.format(rka__pkkyf)
    khx__csb = {}
    exec(qyebd__fwpt, {}, khx__csb)
    efq__cal = khx__csb['json_impl']
    vfk__bnyrm = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    dvuvx__qowo = compile_to_numba_ir(efq__cal, {'_json_reader_py':
        vfk__bnyrm}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(dvuvx__qowo, [json_node.file_name])
    dqqjd__mta = dvuvx__qowo.body[:-3]
    for jbw__glce in range(len(json_node.out_vars)):
        dqqjd__mta[-len(json_node.out_vars) + jbw__glce
            ].target = json_node.out_vars[jbw__glce]
    return dqqjd__mta


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
    arm__qwbh = [sanitize_varname(pcunj__afro) for pcunj__afro in col_names]
    hts__waxz = ', '.join(str(jbw__glce) for jbw__glce, rgf__lxfs in
        enumerate(col_typs) if rgf__lxfs.dtype == types.NPDatetime('ns'))
    ecd__dny = ', '.join(["{}='{}'".format(ifik__npl, bodo.ir.csv_ext.
        _get_dtype_str(rgf__lxfs)) for ifik__npl, rgf__lxfs in zip(
        arm__qwbh, col_typs)])
    nomfk__skisd = ', '.join(["'{}':{}".format(azp__uzj, bodo.ir.csv_ext.
        _get_pd_dtype_str(rgf__lxfs)) for azp__uzj, rgf__lxfs in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    qyebd__fwpt = 'def json_reader_py(fname):\n'
    qyebd__fwpt += '  df_typeref_2 = df_typeref\n'
    qyebd__fwpt += '  check_java_installation(fname)\n'
    qyebd__fwpt += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    qyebd__fwpt += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    qyebd__fwpt += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    qyebd__fwpt += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    qyebd__fwpt += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    qyebd__fwpt += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    qyebd__fwpt += "      raise FileNotFoundError('File does not exist')\n"
    qyebd__fwpt += f'  with objmode({ecd__dny}):\n'
    qyebd__fwpt += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    qyebd__fwpt += f'       convert_dates = {convert_dates}, \n'
    qyebd__fwpt += f'       precise_float={precise_float}, \n'
    qyebd__fwpt += f'       lines={lines}, \n'
    qyebd__fwpt += '       dtype={{{}}},\n'.format(nomfk__skisd)
    qyebd__fwpt += '       )\n'
    qyebd__fwpt += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for ifik__npl, azp__uzj in zip(arm__qwbh, col_names):
        qyebd__fwpt += '    if len(df) > 0:\n'
        qyebd__fwpt += "        {} = df['{}'].values\n".format(ifik__npl,
            azp__uzj)
        qyebd__fwpt += '    else:\n'
        qyebd__fwpt += '        {} = np.array([])\n'.format(ifik__npl)
    qyebd__fwpt += '  return ({},)\n'.format(', '.join(pqzok__dhgsp for
        pqzok__dhgsp in arm__qwbh))
    knunj__kkz = globals()
    knunj__kkz.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    khx__csb = {}
    exec(qyebd__fwpt, knunj__kkz, khx__csb)
    vfk__bnyrm = khx__csb['json_reader_py']
    qtdl__uuo = numba.njit(vfk__bnyrm)
    compiled_funcs.append(qtdl__uuo)
    return qtdl__uuo
