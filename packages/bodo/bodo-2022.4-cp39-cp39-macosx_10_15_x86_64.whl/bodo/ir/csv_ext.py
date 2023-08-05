from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from mpi4py import MPI
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname


class CsvReader(ir.Stmt):

    def __init__(self, file_name, df_out, sep, df_colnames, out_vars,
        out_types, usecols, loc, header, compression, nrows, skiprows,
        chunksize, is_skiprows_list, low_memory, escapechar,
        storage_options=None, index_column_index=None, index_column_typ=
        types.none):
        self.connector_typ = 'csv'
        self.file_name = file_name
        self.df_out = df_out
        self.sep = sep
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.usecols = usecols
        self.loc = loc
        self.skiprows = skiprows
        self.nrows = nrows
        self.header = header
        self.compression = compression
        self.chunksize = chunksize
        self.is_skiprows_list = is_skiprows_list
        self.pd_low_memory = low_memory
        self.escapechar = escapechar
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_typ = index_column_typ
        self.type_usecol_offset = list(range(len(usecols)))

    def __repr__(self):
        return (
            '{} = ReadCsv(file={}, col_names={}, types={}, vars={}, nrows={}, skiprows={}, chunksize={}, is_skiprows_list={}, pd_low_memory={}, escapechar={}, storage_options={}, index_column_index={}, index_colum_typ = {}, type_usecol_offsets={})'
            .format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars, self.nrows, self.skiprows, self.
            chunksize, self.is_skiprows_list, self.pd_low_memory, self.
            escapechar, self.storage_options, self.index_column_index, self
            .index_column_typ, self.type_usecol_offset))


def check_node_typing(node, typemap):
    arnw__ekarz = typemap[node.file_name.name]
    if types.unliteral(arnw__ekarz) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {arnw__ekarz}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        wseb__owho = typemap[node.skiprows.name]
        if isinstance(wseb__owho, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(wseb__owho, types.Integer) and not (isinstance(
            wseb__owho, (types.List, types.Tuple)) and isinstance(
            wseb__owho.dtype, types.Integer)) and not isinstance(wseb__owho,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {wseb__owho}."
                , loc=node.skiprows.loc)
        elif isinstance(wseb__owho, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        rqpnr__ftee = typemap[node.nrows.name]
        if not isinstance(rqpnr__ftee, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {rqpnr__ftee}."
                , loc=node.nrows.loc)


import llvmlite.binding as ll
from bodo.io import csv_cpp
ll.add_symbol('csv_file_chunk_reader', csv_cpp.csv_file_chunk_reader)
csv_file_chunk_reader = types.ExternalFunction('csv_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
    storage_options_dict_type, types.int64, types.bool_, types.int64, types
    .bool_))


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        ucbmm__zhivt = csv_node.out_vars[0]
        if ucbmm__zhivt.name not in lives:
            return None
    else:
        wghvu__cezmz = csv_node.out_vars[0]
        yfrfh__jxz = csv_node.out_vars[1]
        if wghvu__cezmz.name not in lives and yfrfh__jxz.name not in lives:
            return None
        elif yfrfh__jxz.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif wghvu__cezmz.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    wseb__owho = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            lcllg__uwgly = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            zhe__mtw = csv_node.loc.strformat()
            qimsr__qemxe = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', lcllg__uwgly,
                zhe__mtw, qimsr__qemxe)
            aeyat__cbct = csv_node.out_types[0].yield_type.data
            eflop__ssf = [mnyp__tzzyn for eki__hoial, mnyp__tzzyn in
                enumerate(csv_node.df_colnames) if isinstance(aeyat__cbct[
                eki__hoial], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if eflop__ssf:
                azj__eahmq = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    azj__eahmq, zhe__mtw, eflop__ssf)
        if array_dists is not None:
            xej__tnjp = csv_node.out_vars[0].name
            parallel = array_dists[xej__tnjp] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        wij__ucu = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        wij__ucu += f'    reader = _csv_reader_init(fname, nrows, skiprows)\n'
        wij__ucu += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        gwrjj__gihud = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(wij__ucu, {}, gwrjj__gihud)
        poz__jgmk = gwrjj__gihud['csv_iterator_impl']
        ydl__wnwq = 'def csv_reader_init(fname, nrows, skiprows):\n'
        ydl__wnwq += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        ydl__wnwq += '  return f_reader\n'
        exec(ydl__wnwq, globals(), gwrjj__gihud)
        rwvlc__jmoch = gwrjj__gihud['csv_reader_init']
        xrqd__zwhrt = numba.njit(rwvlc__jmoch)
        compiled_funcs.append(xrqd__zwhrt)
        zuzls__tlv = compile_to_numba_ir(poz__jgmk, {'_csv_reader_init':
            xrqd__zwhrt, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, wseb__owho), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(zuzls__tlv, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        gza__awyi = zuzls__tlv.body[:-3]
        gza__awyi[-1].target = csv_node.out_vars[0]
        return gza__awyi
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    wij__ucu = 'def csv_impl(fname, nrows, skiprows):\n'
    wij__ucu += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    gwrjj__gihud = {}
    exec(wij__ucu, {}, gwrjj__gihud)
    gvf__jwzw = gwrjj__gihud['csv_impl']
    ftn__wseug = csv_node.usecols
    if ftn__wseug:
        ftn__wseug = [csv_node.usecols[eki__hoial] for eki__hoial in
            csv_node.type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        lcllg__uwgly = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        zhe__mtw = csv_node.loc.strformat()
        qimsr__qemxe = []
        eflop__ssf = []
        if ftn__wseug:
            for eki__hoial in ftn__wseug:
                whi__ntdf = csv_node.df_colnames[eki__hoial]
                qimsr__qemxe.append(whi__ntdf)
                if isinstance(csv_node.out_types[eki__hoial], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    eflop__ssf.append(whi__ntdf)
        bodo.user_logging.log_message('Column Pruning', lcllg__uwgly,
            zhe__mtw, qimsr__qemxe)
        if eflop__ssf:
            azj__eahmq = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', azj__eahmq,
                zhe__mtw, eflop__ssf)
    dyx__moi = _gen_csv_reader_py(csv_node.df_colnames, csv_node.out_types,
        ftn__wseug, csv_node.type_usecol_offset, csv_node.sep, parallel,
        csv_node.header, csv_node.compression, csv_node.is_skiprows_list,
        csv_node.pd_low_memory, csv_node.escapechar, csv_node.
        storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    zuzls__tlv = compile_to_numba_ir(gvf__jwzw, {'_csv_reader_py': dyx__moi
        }, typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
        types.int64, wseb__owho), typemap=typemap, calltypes=calltypes
        ).blocks.popitem()[1]
    replace_arg_nodes(zuzls__tlv, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    gza__awyi = zuzls__tlv.body[:-3]
    gza__awyi[-1].target = csv_node.out_vars[1]
    gza__awyi[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not ftn__wseug
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        gza__awyi.pop(-1)
    elif not ftn__wseug:
        gza__awyi.pop(-2)
    return gza__awyi


def csv_remove_dead_column(csv_node, column_live_map, equiv_vars, typemap):
    if csv_node.chunksize is not None:
        return False
    return bodo.ir.connector.base_connector_remove_dead_columns(csv_node,
        column_live_map, equiv_vars, typemap, 'CSVReader', csv_node.usecols)


numba.parfors.array_analysis.array_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[CsvReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[CsvReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[CsvReader] = remove_dead_csv
numba.core.analysis.ir_extension_usedefs[CsvReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[CsvReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[CsvReader] = csv_distributed_run
remove_dead_column_extensions[CsvReader] = csv_remove_dead_column
ir_extension_table_column_use[CsvReader
    ] = bodo.ir.connector.connector_table_column_use


def _get_dtype_str(t):
    ubrtc__orktg = t.dtype
    if isinstance(ubrtc__orktg, PDCategoricalDtype):
        tca__jvpbp = CategoricalArrayType(ubrtc__orktg)
        hmcm__romq = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, hmcm__romq, tca__jvpbp)
        return hmcm__romq
    if ubrtc__orktg == types.NPDatetime('ns'):
        ubrtc__orktg = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        epph__jyoxu = 'int_arr_{}'.format(ubrtc__orktg)
        setattr(types, epph__jyoxu, t)
        return epph__jyoxu
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if ubrtc__orktg == types.bool_:
        ubrtc__orktg = 'bool_'
    if ubrtc__orktg == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(ubrtc__orktg, (
        StringArrayType, ArrayItemArrayType)):
        xfyu__hjg = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, xfyu__hjg, t)
        return xfyu__hjg
    return '{}[::1]'.format(ubrtc__orktg)


def _get_pd_dtype_str(t):
    ubrtc__orktg = t.dtype
    if isinstance(ubrtc__orktg, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(ubrtc__orktg.categories)
    if ubrtc__orktg == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if ubrtc__orktg.signed else 'U',
            ubrtc__orktg.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(ubrtc__orktg, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(ubrtc__orktg)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    kbjsg__yqjm = ''
    from collections import defaultdict
    xwzpu__rrv = defaultdict(list)
    for izh__qnfqb, pez__glwa in typemap.items():
        xwzpu__rrv[pez__glwa].append(izh__qnfqb)
    imjy__rrzx = df.columns.to_list()
    icro__blvm = []
    for pez__glwa, mfz__ctx in xwzpu__rrv.items():
        try:
            icro__blvm.append(df.loc[:, mfz__ctx].astype(pez__glwa, copy=False)
                )
            df = df.drop(mfz__ctx, axis=1)
        except (ValueError, TypeError) as imzo__fsc:
            kbjsg__yqjm = (
                f"Caught the runtime error '{imzo__fsc}' on columns {mfz__ctx}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    aqz__gunal = bool(kbjsg__yqjm)
    if parallel:
        vrigq__awcqa = MPI.COMM_WORLD
        aqz__gunal = vrigq__awcqa.allreduce(aqz__gunal, op=MPI.LOR)
    if aqz__gunal:
        cndwa__dcxn = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if kbjsg__yqjm:
            raise TypeError(f'{cndwa__dcxn}\n{kbjsg__yqjm}')
        else:
            raise TypeError(
                f'{cndwa__dcxn}\nPlease refer to errors on other ranks.')
    df = pd.concat(icro__blvm + [df], axis=1)
    tlk__esumr = df.loc[:, imjy__rrzx]
    return tlk__esumr


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    ervpi__taprv = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        wij__ucu = '  skiprows = sorted(set(skiprows))\n'
    else:
        wij__ucu = '  skiprows = [skiprows]\n'
    wij__ucu += '  skiprows_list_len = len(skiprows)\n'
    wij__ucu += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    wij__ucu += '  check_java_installation(fname)\n'
    wij__ucu += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    wij__ucu += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    wij__ucu += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    wij__ucu += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, ervpi__taprv, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    wij__ucu += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    wij__ucu += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    wij__ucu += "      raise FileNotFoundError('File does not exist')\n"
    return wij__ucu


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    pyct__tdjhl = [str(eki__hoial) for eki__hoial, pkdyw__wgu in enumerate(
        usecols) if col_typs[type_usecol_offset[eki__hoial]].dtype == types
        .NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        pyct__tdjhl.append(str(idx_col_index))
    nlu__knq = ', '.join(pyct__tdjhl)
    tip__tlhk = _gen_parallel_flag_name(sanitized_cnames)
    rdq__rqac = f"{tip__tlhk}='bool_'" if check_parallel_runtime else ''
    ffb__tmwmo = [_get_pd_dtype_str(col_typs[type_usecol_offset[eki__hoial]
        ]) for eki__hoial in range(len(usecols))]
    tkwne__rog = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    omj__vuecu = [pkdyw__wgu for eki__hoial, pkdyw__wgu in enumerate(
        usecols) if ffb__tmwmo[eki__hoial] == 'str']
    if idx_col_index is not None and tkwne__rog == 'str':
        omj__vuecu.append(idx_col_index)
    yubn__oyzhu = np.array(omj__vuecu, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = yubn__oyzhu
    wij__ucu = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    scbx__qgf = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = scbx__qgf
    wij__ucu += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    xap__ios = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = xap__ios
        wij__ucu += (
            f'  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}\n'
            )
    glsux__slf = defaultdict(list)
    for eki__hoial, pkdyw__wgu in enumerate(usecols):
        if ffb__tmwmo[eki__hoial] == 'str':
            continue
        glsux__slf[ffb__tmwmo[eki__hoial]].append(pkdyw__wgu)
    if idx_col_index is not None and tkwne__rog != 'str':
        glsux__slf[tkwne__rog].append(idx_col_index)
    for eki__hoial, kmi__qcymd in enumerate(glsux__slf.values()):
        glbs[f't_arr_{eki__hoial}_{call_id}'] = np.asarray(kmi__qcymd)
        wij__ucu += (
            f'  t_arr_{eki__hoial}_{call_id}_2 = t_arr_{eki__hoial}_{call_id}\n'
            )
    if idx_col_index != None:
        wij__ucu += (
            f'  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {rdq__rqac}):\n'
            )
    else:
        wij__ucu += f'  with objmode(T=table_type_{call_id}, {rdq__rqac}):\n'
    wij__ucu += f'    typemap = {{}}\n'
    for eki__hoial, ons__atuc in enumerate(glsux__slf.keys()):
        wij__ucu += f"""    typemap.update({{i:{ons__atuc} for i in t_arr_{eki__hoial}_{call_id}_2}})
"""
    wij__ucu += '    if f_reader.get_chunk_size() == 0:\n'
    wij__ucu += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    wij__ucu += '    else:\n'
    wij__ucu += '      df = pd.read_csv(f_reader,\n'
    wij__ucu += '        header=None,\n'
    wij__ucu += '        parse_dates=[{}],\n'.format(nlu__knq)
    wij__ucu += f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n'
    wij__ucu += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        wij__ucu += f'    {tip__tlhk} = f_reader.is_parallel()\n'
    else:
        wij__ucu += f'    {tip__tlhk} = {parallel}\n'
    wij__ucu += f'    df = astype(df, typemap, {tip__tlhk})\n'
    if idx_col_index != None:
        tgmf__jdnwt = sorted(scbx__qgf).index(idx_col_index)
        wij__ucu += f'    idx_arr = df.iloc[:, {tgmf__jdnwt}].values\n'
        wij__ucu += (
            f'    df.drop(columns=df.columns[{tgmf__jdnwt}], inplace=True)\n')
    if len(usecols) == 0:
        wij__ucu += f'    T = None\n'
    else:
        wij__ucu += f'    arrs = []\n'
        wij__ucu += f'    for i in range(df.shape[1]):\n'
        wij__ucu += f'      arrs.append(df.iloc[:, i].values)\n'
        wij__ucu += (
            f'    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})\n'
            )
    return wij__ucu


def _gen_parallel_flag_name(sanitized_cnames):
    tip__tlhk = '_parallel_value'
    while tip__tlhk in sanitized_cnames:
        tip__tlhk = '_' + tip__tlhk
    return tip__tlhk


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(mnyp__tzzyn) for mnyp__tzzyn in
        col_names]
    wij__ucu = 'def csv_reader_py(fname, nrows, skiprows):\n'
    wij__ucu += _gen_csv_file_reader_init(parallel, header, compression, -1,
        is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    mnagu__bau = globals()
    if idx_col_typ != types.none:
        mnagu__bau[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        mnagu__bau[f'table_type_{call_id}'] = types.none
    else:
        mnagu__bau[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    wij__ucu += _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs,
        usecols, type_usecol_offset, sep, escapechar, storage_options,
        call_id, mnagu__bau, parallel=parallel, check_parallel_runtime=
        False, idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        wij__ucu += '  return (T, idx_arr)\n'
    else:
        wij__ucu += '  return (T, None)\n'
    gwrjj__gihud = {}
    mnagu__bau['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(wij__ucu, mnagu__bau, gwrjj__gihud)
    dyx__moi = gwrjj__gihud['csv_reader_py']
    xrqd__zwhrt = numba.njit(dyx__moi)
    compiled_funcs.append(xrqd__zwhrt)
    return xrqd__zwhrt
