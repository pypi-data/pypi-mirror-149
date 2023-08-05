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
    givc__lsl = typemap[node.file_name.name]
    if types.unliteral(givc__lsl) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {givc__lsl}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        qxewx__krbt = typemap[node.skiprows.name]
        if isinstance(qxewx__krbt, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(qxewx__krbt, types.Integer) and not (isinstance
            (qxewx__krbt, (types.List, types.Tuple)) and isinstance(
            qxewx__krbt.dtype, types.Integer)) and not isinstance(qxewx__krbt,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {qxewx__krbt}."
                , loc=node.skiprows.loc)
        elif isinstance(qxewx__krbt, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        oyo__jcyeu = typemap[node.nrows.name]
        if not isinstance(oyo__jcyeu, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {oyo__jcyeu}."
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
        ohdlj__qwwj = csv_node.out_vars[0]
        if ohdlj__qwwj.name not in lives:
            return None
    else:
        cxjxz__rivy = csv_node.out_vars[0]
        zfogx__qpbe = csv_node.out_vars[1]
        if cxjxz__rivy.name not in lives and zfogx__qpbe.name not in lives:
            return None
        elif zfogx__qpbe.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif cxjxz__rivy.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    qxewx__krbt = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            sxd__vlipk = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            vpqm__zlnp = csv_node.loc.strformat()
            gakf__dxbwe = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', sxd__vlipk,
                vpqm__zlnp, gakf__dxbwe)
            krw__hsp = csv_node.out_types[0].yield_type.data
            lni__vxnxj = [ywo__zzau for vqm__fefk, ywo__zzau in enumerate(
                csv_node.df_colnames) if isinstance(krw__hsp[vqm__fefk],
                bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if lni__vxnxj:
                zbn__myasf = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    zbn__myasf, vpqm__zlnp, lni__vxnxj)
        if array_dists is not None:
            xrlwd__pkkf = csv_node.out_vars[0].name
            parallel = array_dists[xrlwd__pkkf] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        wqh__wci = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        wqh__wci += f'    reader = _csv_reader_init(fname, nrows, skiprows)\n'
        wqh__wci += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        gcuv__omn = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(wqh__wci, {}, gcuv__omn)
        ifl__edu = gcuv__omn['csv_iterator_impl']
        tqz__slv = 'def csv_reader_init(fname, nrows, skiprows):\n'
        tqz__slv += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        tqz__slv += '  return f_reader\n'
        exec(tqz__slv, globals(), gcuv__omn)
        vyd__uzqeu = gcuv__omn['csv_reader_init']
        nrizm__wakr = numba.njit(vyd__uzqeu)
        compiled_funcs.append(nrizm__wakr)
        sry__anchi = compile_to_numba_ir(ifl__edu, {'_csv_reader_init':
            nrizm__wakr, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, qxewx__krbt), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(sry__anchi, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        gdk__opo = sry__anchi.body[:-3]
        gdk__opo[-1].target = csv_node.out_vars[0]
        return gdk__opo
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    wqh__wci = 'def csv_impl(fname, nrows, skiprows):\n'
    wqh__wci += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    gcuv__omn = {}
    exec(wqh__wci, {}, gcuv__omn)
    mhc__djl = gcuv__omn['csv_impl']
    pcbv__msnj = csv_node.usecols
    if pcbv__msnj:
        pcbv__msnj = [csv_node.usecols[vqm__fefk] for vqm__fefk in csv_node
            .type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        sxd__vlipk = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        vpqm__zlnp = csv_node.loc.strformat()
        gakf__dxbwe = []
        lni__vxnxj = []
        if pcbv__msnj:
            for vqm__fefk in pcbv__msnj:
                ddwco__vphtk = csv_node.df_colnames[vqm__fefk]
                gakf__dxbwe.append(ddwco__vphtk)
                if isinstance(csv_node.out_types[vqm__fefk], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    lni__vxnxj.append(ddwco__vphtk)
        bodo.user_logging.log_message('Column Pruning', sxd__vlipk,
            vpqm__zlnp, gakf__dxbwe)
        if lni__vxnxj:
            zbn__myasf = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', zbn__myasf,
                vpqm__zlnp, lni__vxnxj)
    hcdz__druo = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, pcbv__msnj, csv_node.type_usecol_offset, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    sry__anchi = compile_to_numba_ir(mhc__djl, {'_csv_reader_py':
        hcdz__druo}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, qxewx__krbt), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(sry__anchi, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    gdk__opo = sry__anchi.body[:-3]
    gdk__opo[-1].target = csv_node.out_vars[1]
    gdk__opo[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not pcbv__msnj
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        gdk__opo.pop(-1)
    elif not pcbv__msnj:
        gdk__opo.pop(-2)
    return gdk__opo


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
    zrr__aqr = t.dtype
    if isinstance(zrr__aqr, PDCategoricalDtype):
        nhla__hzc = CategoricalArrayType(zrr__aqr)
        vsqm__ome = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, vsqm__ome, nhla__hzc)
        return vsqm__ome
    if zrr__aqr == types.NPDatetime('ns'):
        zrr__aqr = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        lgmv__ejzu = 'int_arr_{}'.format(zrr__aqr)
        setattr(types, lgmv__ejzu, t)
        return lgmv__ejzu
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if zrr__aqr == types.bool_:
        zrr__aqr = 'bool_'
    if zrr__aqr == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(zrr__aqr, (
        StringArrayType, ArrayItemArrayType)):
        kvqgh__rgape = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, kvqgh__rgape, t)
        return kvqgh__rgape
    return '{}[::1]'.format(zrr__aqr)


def _get_pd_dtype_str(t):
    zrr__aqr = t.dtype
    if isinstance(zrr__aqr, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(zrr__aqr.categories)
    if zrr__aqr == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if zrr__aqr.signed else 'U', zrr__aqr.
            bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(zrr__aqr, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(zrr__aqr)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    aankb__tnyps = ''
    from collections import defaultdict
    qco__sac = defaultdict(list)
    for ygi__llm, txts__gzz in typemap.items():
        qco__sac[txts__gzz].append(ygi__llm)
    fcuf__epey = df.columns.to_list()
    msuu__llpg = []
    for txts__gzz, nolc__ezo in qco__sac.items():
        try:
            msuu__llpg.append(df.loc[:, nolc__ezo].astype(txts__gzz, copy=
                False))
            df = df.drop(nolc__ezo, axis=1)
        except (ValueError, TypeError) as wtsbi__gcy:
            aankb__tnyps = (
                f"Caught the runtime error '{wtsbi__gcy}' on columns {nolc__ezo}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    kfkba__eyo = bool(aankb__tnyps)
    if parallel:
        gwsp__zukoe = MPI.COMM_WORLD
        kfkba__eyo = gwsp__zukoe.allreduce(kfkba__eyo, op=MPI.LOR)
    if kfkba__eyo:
        akg__gwzp = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if aankb__tnyps:
            raise TypeError(f'{akg__gwzp}\n{aankb__tnyps}')
        else:
            raise TypeError(
                f'{akg__gwzp}\nPlease refer to errors on other ranks.')
    df = pd.concat(msuu__llpg + [df], axis=1)
    jqz__ajen = df.loc[:, fcuf__epey]
    return jqz__ajen


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    xxoy__jbl = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        wqh__wci = '  skiprows = sorted(set(skiprows))\n'
    else:
        wqh__wci = '  skiprows = [skiprows]\n'
    wqh__wci += '  skiprows_list_len = len(skiprows)\n'
    wqh__wci += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    wqh__wci += '  check_java_installation(fname)\n'
    wqh__wci += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    wqh__wci += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    wqh__wci += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    wqh__wci += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, xxoy__jbl, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    wqh__wci += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    wqh__wci += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    wqh__wci += "      raise FileNotFoundError('File does not exist')\n"
    return wqh__wci


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    vvv__pga = [str(vqm__fefk) for vqm__fefk, hnkem__qcnzn in enumerate(
        usecols) if col_typs[type_usecol_offset[vqm__fefk]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        vvv__pga.append(str(idx_col_index))
    ygdet__jcp = ', '.join(vvv__pga)
    mag__nwn = _gen_parallel_flag_name(sanitized_cnames)
    ghx__stgzm = f"{mag__nwn}='bool_'" if check_parallel_runtime else ''
    ibq__ruw = [_get_pd_dtype_str(col_typs[type_usecol_offset[vqm__fefk]]) for
        vqm__fefk in range(len(usecols))]
    vhl__famz = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    dnbk__owxn = [hnkem__qcnzn for vqm__fefk, hnkem__qcnzn in enumerate(
        usecols) if ibq__ruw[vqm__fefk] == 'str']
    if idx_col_index is not None and vhl__famz == 'str':
        dnbk__owxn.append(idx_col_index)
    gat__jghzo = np.array(dnbk__owxn, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = gat__jghzo
    wqh__wci = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    yhv__enle = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = yhv__enle
    wqh__wci += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    xjglp__ysi = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = xjglp__ysi
        wqh__wci += (
            f'  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}\n'
            )
    kbc__jpcdl = defaultdict(list)
    for vqm__fefk, hnkem__qcnzn in enumerate(usecols):
        if ibq__ruw[vqm__fefk] == 'str':
            continue
        kbc__jpcdl[ibq__ruw[vqm__fefk]].append(hnkem__qcnzn)
    if idx_col_index is not None and vhl__famz != 'str':
        kbc__jpcdl[vhl__famz].append(idx_col_index)
    for vqm__fefk, jhidg__gho in enumerate(kbc__jpcdl.values()):
        glbs[f't_arr_{vqm__fefk}_{call_id}'] = np.asarray(jhidg__gho)
        wqh__wci += (
            f'  t_arr_{vqm__fefk}_{call_id}_2 = t_arr_{vqm__fefk}_{call_id}\n')
    if idx_col_index != None:
        wqh__wci += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {ghx__stgzm}):
"""
    else:
        wqh__wci += f'  with objmode(T=table_type_{call_id}, {ghx__stgzm}):\n'
    wqh__wci += f'    typemap = {{}}\n'
    for vqm__fefk, icn__wdmz in enumerate(kbc__jpcdl.keys()):
        wqh__wci += f"""    typemap.update({{i:{icn__wdmz} for i in t_arr_{vqm__fefk}_{call_id}_2}})
"""
    wqh__wci += '    if f_reader.get_chunk_size() == 0:\n'
    wqh__wci += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    wqh__wci += '    else:\n'
    wqh__wci += '      df = pd.read_csv(f_reader,\n'
    wqh__wci += '        header=None,\n'
    wqh__wci += '        parse_dates=[{}],\n'.format(ygdet__jcp)
    wqh__wci += f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n'
    wqh__wci += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        wqh__wci += f'    {mag__nwn} = f_reader.is_parallel()\n'
    else:
        wqh__wci += f'    {mag__nwn} = {parallel}\n'
    wqh__wci += f'    df = astype(df, typemap, {mag__nwn})\n'
    if idx_col_index != None:
        wxaqd__xuc = sorted(yhv__enle).index(idx_col_index)
        wqh__wci += f'    idx_arr = df.iloc[:, {wxaqd__xuc}].values\n'
        wqh__wci += (
            f'    df.drop(columns=df.columns[{wxaqd__xuc}], inplace=True)\n')
    if len(usecols) == 0:
        wqh__wci += f'    T = None\n'
    else:
        wqh__wci += f'    arrs = []\n'
        wqh__wci += f'    for i in range(df.shape[1]):\n'
        wqh__wci += f'      arrs.append(df.iloc[:, i].values)\n'
        wqh__wci += (
            f'    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})\n'
            )
    return wqh__wci


def _gen_parallel_flag_name(sanitized_cnames):
    mag__nwn = '_parallel_value'
    while mag__nwn in sanitized_cnames:
        mag__nwn = '_' + mag__nwn
    return mag__nwn


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(ywo__zzau) for ywo__zzau in col_names]
    wqh__wci = 'def csv_reader_py(fname, nrows, skiprows):\n'
    wqh__wci += _gen_csv_file_reader_init(parallel, header, compression, -1,
        is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    kxeji__ujc = globals()
    if idx_col_typ != types.none:
        kxeji__ujc[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        kxeji__ujc[f'table_type_{call_id}'] = types.none
    else:
        kxeji__ujc[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    wqh__wci += _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs,
        usecols, type_usecol_offset, sep, escapechar, storage_options,
        call_id, kxeji__ujc, parallel=parallel, check_parallel_runtime=
        False, idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        wqh__wci += '  return (T, idx_arr)\n'
    else:
        wqh__wci += '  return (T, None)\n'
    gcuv__omn = {}
    kxeji__ujc['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(wqh__wci, kxeji__ujc, gcuv__omn)
    hcdz__druo = gcuv__omn['csv_reader_py']
    nrizm__wakr = numba.njit(hcdz__druo)
    compiled_funcs.append(nrizm__wakr)
    return nrizm__wakr
