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
    mocq__mawx = []
    pgsiz__wzqr = []
    una__dptc = []
    for eew__nzg, fqov__epo in enumerate(json_node.out_vars):
        if fqov__epo.name in lives:
            mocq__mawx.append(json_node.df_colnames[eew__nzg])
            pgsiz__wzqr.append(json_node.out_vars[eew__nzg])
            una__dptc.append(json_node.out_types[eew__nzg])
    json_node.df_colnames = mocq__mawx
    json_node.out_vars = pgsiz__wzqr
    json_node.out_types = una__dptc
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        ffd__ldy = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        qjgbm__iou = json_node.loc.strformat()
        ftb__aremd = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', ffd__ldy,
            qjgbm__iou, ftb__aremd)
        ual__xmqp = [kfgb__fvm for eew__nzg, kfgb__fvm in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            eew__nzg], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if ual__xmqp:
            lawj__siw = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', lawj__siw,
                qjgbm__iou, ual__xmqp)
    parallel = False
    if array_dists is not None:
        parallel = True
        for atdjy__snm in json_node.out_vars:
            if array_dists[atdjy__snm.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                atdjy__snm.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    msuzq__luaa = len(json_node.out_vars)
    kvoli__azzs = ', '.join('arr' + str(eew__nzg) for eew__nzg in range(
        msuzq__luaa))
    rjzw__umkwd = 'def json_impl(fname):\n'
    rjzw__umkwd += '    ({},) = _json_reader_py(fname)\n'.format(kvoli__azzs)
    qmbg__noa = {}
    exec(rjzw__umkwd, {}, qmbg__noa)
    oks__brg = qmbg__noa['json_impl']
    iri__byvl = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    coia__rgt = compile_to_numba_ir(oks__brg, {'_json_reader_py': iri__byvl
        }, typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
        ), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(coia__rgt, [json_node.file_name])
    wtt__hvlhx = coia__rgt.body[:-3]
    for eew__nzg in range(len(json_node.out_vars)):
        wtt__hvlhx[-len(json_node.out_vars) + eew__nzg
            ].target = json_node.out_vars[eew__nzg]
    return wtt__hvlhx


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
    zlg__pusj = [sanitize_varname(kfgb__fvm) for kfgb__fvm in col_names]
    wldv__jiniz = ', '.join(str(eew__nzg) for eew__nzg, ldu__ufx in
        enumerate(col_typs) if ldu__ufx.dtype == types.NPDatetime('ns'))
    tyq__aikze = ', '.join(["{}='{}'".format(rzw__krl, bodo.ir.csv_ext.
        _get_dtype_str(ldu__ufx)) for rzw__krl, ldu__ufx in zip(zlg__pusj,
        col_typs)])
    eychg__erunz = ', '.join(["'{}':{}".format(xtfzo__vujcy, bodo.ir.
        csv_ext._get_pd_dtype_str(ldu__ufx)) for xtfzo__vujcy, ldu__ufx in
        zip(col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    rjzw__umkwd = 'def json_reader_py(fname):\n'
    rjzw__umkwd += '  df_typeref_2 = df_typeref\n'
    rjzw__umkwd += '  check_java_installation(fname)\n'
    rjzw__umkwd += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    rjzw__umkwd += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    rjzw__umkwd += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    rjzw__umkwd += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    rjzw__umkwd += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    rjzw__umkwd += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    rjzw__umkwd += "      raise FileNotFoundError('File does not exist')\n"
    rjzw__umkwd += f'  with objmode({tyq__aikze}):\n'
    rjzw__umkwd += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    rjzw__umkwd += f'       convert_dates = {convert_dates}, \n'
    rjzw__umkwd += f'       precise_float={precise_float}, \n'
    rjzw__umkwd += f'       lines={lines}, \n'
    rjzw__umkwd += '       dtype={{{}}},\n'.format(eychg__erunz)
    rjzw__umkwd += '       )\n'
    rjzw__umkwd += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for rzw__krl, xtfzo__vujcy in zip(zlg__pusj, col_names):
        rjzw__umkwd += '    if len(df) > 0:\n'
        rjzw__umkwd += "        {} = df['{}'].values\n".format(rzw__krl,
            xtfzo__vujcy)
        rjzw__umkwd += '    else:\n'
        rjzw__umkwd += '        {} = np.array([])\n'.format(rzw__krl)
    rjzw__umkwd += '  return ({},)\n'.format(', '.join(puhwz__bql for
        puhwz__bql in zlg__pusj))
    eewz__ospe = globals()
    eewz__ospe.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    qmbg__noa = {}
    exec(rjzw__umkwd, eewz__ospe, qmbg__noa)
    iri__byvl = qmbg__noa['json_reader_py']
    jnv__yfrf = numba.njit(iri__byvl)
    compiled_funcs.append(jnv__yfrf)
    return jnv__yfrf
