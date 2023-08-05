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
    jbo__cgeae = typemap[node.file_name.name]
    if types.unliteral(jbo__cgeae) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {jbo__cgeae}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        zjp__zacdy = typemap[node.skiprows.name]
        if isinstance(zjp__zacdy, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(zjp__zacdy, types.Integer) and not (isinstance(
            zjp__zacdy, (types.List, types.Tuple)) and isinstance(
            zjp__zacdy.dtype, types.Integer)) and not isinstance(zjp__zacdy,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {zjp__zacdy}."
                , loc=node.skiprows.loc)
        elif isinstance(zjp__zacdy, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        dnmum__btny = typemap[node.nrows.name]
        if not isinstance(dnmum__btny, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {dnmum__btny}."
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
        jygk__tvb = csv_node.out_vars[0]
        if jygk__tvb.name not in lives:
            return None
    else:
        ptdnw__tbkxf = csv_node.out_vars[0]
        clfw__wgkr = csv_node.out_vars[1]
        if ptdnw__tbkxf.name not in lives and clfw__wgkr.name not in lives:
            return None
        elif clfw__wgkr.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif ptdnw__tbkxf.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    zjp__zacdy = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            fqpvk__lqp = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            ihp__rdia = csv_node.loc.strformat()
            rdys__mvc = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', fqpvk__lqp,
                ihp__rdia, rdys__mvc)
            dhw__swj = csv_node.out_types[0].yield_type.data
            qbg__rfq = [voi__upnnk for fesno__cxfua, voi__upnnk in
                enumerate(csv_node.df_colnames) if isinstance(dhw__swj[
                fesno__cxfua], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if qbg__rfq:
                dsz__nlyn = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    dsz__nlyn, ihp__rdia, qbg__rfq)
        if array_dists is not None:
            ibl__ixpv = csv_node.out_vars[0].name
            parallel = array_dists[ibl__ixpv] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        kkcej__mjhfb = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        kkcej__mjhfb += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        kkcej__mjhfb += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        bbubr__pdg = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(kkcej__mjhfb, {}, bbubr__pdg)
        omq__qthbz = bbubr__pdg['csv_iterator_impl']
        wkj__xbj = 'def csv_reader_init(fname, nrows, skiprows):\n'
        wkj__xbj += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        wkj__xbj += '  return f_reader\n'
        exec(wkj__xbj, globals(), bbubr__pdg)
        yrr__bpyz = bbubr__pdg['csv_reader_init']
        spfhg__xqvf = numba.njit(yrr__bpyz)
        compiled_funcs.append(spfhg__xqvf)
        qnz__saya = compile_to_numba_ir(omq__qthbz, {'_csv_reader_init':
            spfhg__xqvf, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, zjp__zacdy), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(qnz__saya, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        zdld__hat = qnz__saya.body[:-3]
        zdld__hat[-1].target = csv_node.out_vars[0]
        return zdld__hat
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    kkcej__mjhfb = 'def csv_impl(fname, nrows, skiprows):\n'
    kkcej__mjhfb += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    bbubr__pdg = {}
    exec(kkcej__mjhfb, {}, bbubr__pdg)
    lmuxi__rtjf = bbubr__pdg['csv_impl']
    ddtuv__ldt = csv_node.usecols
    if ddtuv__ldt:
        ddtuv__ldt = [csv_node.usecols[fesno__cxfua] for fesno__cxfua in
            csv_node.type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        fqpvk__lqp = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        ihp__rdia = csv_node.loc.strformat()
        rdys__mvc = []
        qbg__rfq = []
        if ddtuv__ldt:
            for fesno__cxfua in ddtuv__ldt:
                ayj__weaf = csv_node.df_colnames[fesno__cxfua]
                rdys__mvc.append(ayj__weaf)
                if isinstance(csv_node.out_types[fesno__cxfua], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    qbg__rfq.append(ayj__weaf)
        bodo.user_logging.log_message('Column Pruning', fqpvk__lqp,
            ihp__rdia, rdys__mvc)
        if qbg__rfq:
            dsz__nlyn = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', dsz__nlyn,
                ihp__rdia, qbg__rfq)
    qntxt__zmdvv = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, ddtuv__ldt, csv_node.type_usecol_offset, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    qnz__saya = compile_to_numba_ir(lmuxi__rtjf, {'_csv_reader_py':
        qntxt__zmdvv}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, zjp__zacdy), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(qnz__saya, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    zdld__hat = qnz__saya.body[:-3]
    zdld__hat[-1].target = csv_node.out_vars[1]
    zdld__hat[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not ddtuv__ldt
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        zdld__hat.pop(-1)
    elif not ddtuv__ldt:
        zdld__hat.pop(-2)
    return zdld__hat


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
    gjyuq__gyhcd = t.dtype
    if isinstance(gjyuq__gyhcd, PDCategoricalDtype):
        adqs__uzxzi = CategoricalArrayType(gjyuq__gyhcd)
        omxsg__afdyl = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, omxsg__afdyl, adqs__uzxzi)
        return omxsg__afdyl
    if gjyuq__gyhcd == types.NPDatetime('ns'):
        gjyuq__gyhcd = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        llrkx__plpmp = 'int_arr_{}'.format(gjyuq__gyhcd)
        setattr(types, llrkx__plpmp, t)
        return llrkx__plpmp
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if gjyuq__gyhcd == types.bool_:
        gjyuq__gyhcd = 'bool_'
    if gjyuq__gyhcd == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(gjyuq__gyhcd, (
        StringArrayType, ArrayItemArrayType)):
        firpj__zxr = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, firpj__zxr, t)
        return firpj__zxr
    return '{}[::1]'.format(gjyuq__gyhcd)


def _get_pd_dtype_str(t):
    gjyuq__gyhcd = t.dtype
    if isinstance(gjyuq__gyhcd, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(gjyuq__gyhcd.categories)
    if gjyuq__gyhcd == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if gjyuq__gyhcd.signed else 'U',
            gjyuq__gyhcd.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(gjyuq__gyhcd, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(gjyuq__gyhcd)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    yzupy__zqmph = ''
    from collections import defaultdict
    umtqt__ooea = defaultdict(list)
    for tsgd__plze, mly__hkn in typemap.items():
        umtqt__ooea[mly__hkn].append(tsgd__plze)
    cqm__fytl = df.columns.to_list()
    sjdm__vgj = []
    for mly__hkn, jvzdp__dbbdc in umtqt__ooea.items():
        try:
            sjdm__vgj.append(df.loc[:, jvzdp__dbbdc].astype(mly__hkn, copy=
                False))
            df = df.drop(jvzdp__dbbdc, axis=1)
        except (ValueError, TypeError) as hzc__ddgb:
            yzupy__zqmph = (
                f"Caught the runtime error '{hzc__ddgb}' on columns {jvzdp__dbbdc}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    gaao__txyt = bool(yzupy__zqmph)
    if parallel:
        aqvhz__cyvyn = MPI.COMM_WORLD
        gaao__txyt = aqvhz__cyvyn.allreduce(gaao__txyt, op=MPI.LOR)
    if gaao__txyt:
        mea__adcx = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if yzupy__zqmph:
            raise TypeError(f'{mea__adcx}\n{yzupy__zqmph}')
        else:
            raise TypeError(
                f'{mea__adcx}\nPlease refer to errors on other ranks.')
    df = pd.concat(sjdm__vgj + [df], axis=1)
    wxthd__htom = df.loc[:, cqm__fytl]
    return wxthd__htom


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    inwb__flvg = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        kkcej__mjhfb = '  skiprows = sorted(set(skiprows))\n'
    else:
        kkcej__mjhfb = '  skiprows = [skiprows]\n'
    kkcej__mjhfb += '  skiprows_list_len = len(skiprows)\n'
    kkcej__mjhfb += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    kkcej__mjhfb += '  check_java_installation(fname)\n'
    kkcej__mjhfb += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    kkcej__mjhfb += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    kkcej__mjhfb += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    kkcej__mjhfb += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, inwb__flvg, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    kkcej__mjhfb += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    kkcej__mjhfb += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    kkcej__mjhfb += "      raise FileNotFoundError('File does not exist')\n"
    return kkcej__mjhfb


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    aem__tjy = [str(fesno__cxfua) for fesno__cxfua, svfi__zzl in enumerate(
        usecols) if col_typs[type_usecol_offset[fesno__cxfua]].dtype ==
        types.NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        aem__tjy.append(str(idx_col_index))
    vntke__jjcjs = ', '.join(aem__tjy)
    kceis__apux = _gen_parallel_flag_name(sanitized_cnames)
    mbv__nbnrm = f"{kceis__apux}='bool_'" if check_parallel_runtime else ''
    vbrj__mwmc = [_get_pd_dtype_str(col_typs[type_usecol_offset[
        fesno__cxfua]]) for fesno__cxfua in range(len(usecols))]
    mke__ptdy = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    izxwo__nqc = [svfi__zzl for fesno__cxfua, svfi__zzl in enumerate(
        usecols) if vbrj__mwmc[fesno__cxfua] == 'str']
    if idx_col_index is not None and mke__ptdy == 'str':
        izxwo__nqc.append(idx_col_index)
    nrpi__tob = np.array(izxwo__nqc, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = nrpi__tob
    kkcej__mjhfb = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    vpar__yivym = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = vpar__yivym
    kkcej__mjhfb += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    oevos__ftzl = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = oevos__ftzl
        kkcej__mjhfb += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    lfvl__hlflc = defaultdict(list)
    for fesno__cxfua, svfi__zzl in enumerate(usecols):
        if vbrj__mwmc[fesno__cxfua] == 'str':
            continue
        lfvl__hlflc[vbrj__mwmc[fesno__cxfua]].append(svfi__zzl)
    if idx_col_index is not None and mke__ptdy != 'str':
        lfvl__hlflc[mke__ptdy].append(idx_col_index)
    for fesno__cxfua, gztjj__pyj in enumerate(lfvl__hlflc.values()):
        glbs[f't_arr_{fesno__cxfua}_{call_id}'] = np.asarray(gztjj__pyj)
        kkcej__mjhfb += (
            f'  t_arr_{fesno__cxfua}_{call_id}_2 = t_arr_{fesno__cxfua}_{call_id}\n'
            )
    if idx_col_index != None:
        kkcej__mjhfb += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {mbv__nbnrm}):
"""
    else:
        kkcej__mjhfb += (
            f'  with objmode(T=table_type_{call_id}, {mbv__nbnrm}):\n')
    kkcej__mjhfb += f'    typemap = {{}}\n'
    for fesno__cxfua, mvjtx__ekgn in enumerate(lfvl__hlflc.keys()):
        kkcej__mjhfb += f"""    typemap.update({{i:{mvjtx__ekgn} for i in t_arr_{fesno__cxfua}_{call_id}_2}})
"""
    kkcej__mjhfb += '    if f_reader.get_chunk_size() == 0:\n'
    kkcej__mjhfb += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    kkcej__mjhfb += '    else:\n'
    kkcej__mjhfb += '      df = pd.read_csv(f_reader,\n'
    kkcej__mjhfb += '        header=None,\n'
    kkcej__mjhfb += '        parse_dates=[{}],\n'.format(vntke__jjcjs)
    kkcej__mjhfb += (
        f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n')
    kkcej__mjhfb += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        kkcej__mjhfb += f'    {kceis__apux} = f_reader.is_parallel()\n'
    else:
        kkcej__mjhfb += f'    {kceis__apux} = {parallel}\n'
    kkcej__mjhfb += f'    df = astype(df, typemap, {kceis__apux})\n'
    if idx_col_index != None:
        oovy__mjg = sorted(vpar__yivym).index(idx_col_index)
        kkcej__mjhfb += f'    idx_arr = df.iloc[:, {oovy__mjg}].values\n'
        kkcej__mjhfb += (
            f'    df.drop(columns=df.columns[{oovy__mjg}], inplace=True)\n')
    if len(usecols) == 0:
        kkcej__mjhfb += f'    T = None\n'
    else:
        kkcej__mjhfb += f'    arrs = []\n'
        kkcej__mjhfb += f'    for i in range(df.shape[1]):\n'
        kkcej__mjhfb += f'      arrs.append(df.iloc[:, i].values)\n'
        kkcej__mjhfb += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return kkcej__mjhfb


def _gen_parallel_flag_name(sanitized_cnames):
    kceis__apux = '_parallel_value'
    while kceis__apux in sanitized_cnames:
        kceis__apux = '_' + kceis__apux
    return kceis__apux


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(voi__upnnk) for voi__upnnk in
        col_names]
    kkcej__mjhfb = 'def csv_reader_py(fname, nrows, skiprows):\n'
    kkcej__mjhfb += _gen_csv_file_reader_init(parallel, header, compression,
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    mbgr__pkx = globals()
    if idx_col_typ != types.none:
        mbgr__pkx[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        mbgr__pkx[f'table_type_{call_id}'] = types.none
    else:
        mbgr__pkx[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    kkcej__mjhfb += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, type_usecol_offset, sep, escapechar,
        storage_options, call_id, mbgr__pkx, parallel=parallel,
        check_parallel_runtime=False, idx_col_index=idx_col_index,
        idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        kkcej__mjhfb += '  return (T, idx_arr)\n'
    else:
        kkcej__mjhfb += '  return (T, None)\n'
    bbubr__pdg = {}
    mbgr__pkx['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(kkcej__mjhfb, mbgr__pkx, bbubr__pdg)
    qntxt__zmdvv = bbubr__pdg['csv_reader_py']
    spfhg__xqvf = numba.njit(qntxt__zmdvv)
    compiled_funcs.append(spfhg__xqvf)
    return spfhg__xqvf
