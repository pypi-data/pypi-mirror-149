import os
import warnings
from collections import defaultdict
from glob import has_magic
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow
import pyarrow.dataset as ds
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, get_definition, guard, mk_unique_var, next_label, replace_arg_nodes
from numba.extending import NativeValue, intrinsic, models, overload, register_model, unbox
from pyarrow import null
import bodo
import bodo.ir.parquet_ext
import bodo.utils.tracing as tracing
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import TableType
from bodo.io.fs_io import get_hdfs_fs, get_s3_fs_from_path, get_s3_subtree_fs, get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import get_end, get_start
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.transforms import distributed_pass
from bodo.utils.transform import get_const_value
from bodo.utils.typing import BodoError, BodoWarning, FileInfo, get_overload_const_str
from bodo.utils.utils import check_and_propagate_cpp_exception, numba_to_c_type, sanitize_varname
use_nullable_int_arr = True
from urllib.parse import urlparse
import bodo.io.pa_parquet
REMOTE_FILESYSTEMS = {'s3', 'gcs', 'gs', 'http', 'hdfs', 'abfs', 'abfss'}
READ_STR_AS_DICT_THRESHOLD = 1.0
list_of_files_error_msg = (
    '. Make sure the list/glob passed to read_parquet() only contains paths to files (no directories)'
    )


class ParquetPredicateType(types.Type):

    def __init__(self):
        super(ParquetPredicateType, self).__init__(name=
            'ParquetPredicateType()')


parquet_predicate_type = ParquetPredicateType()
types.parquet_predicate_type = parquet_predicate_type
register_model(ParquetPredicateType)(models.OpaqueModel)


@unbox(ParquetPredicateType)
def unbox_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ReadParquetFilepathType(types.Opaque):

    def __init__(self):
        super(ReadParquetFilepathType, self).__init__(name=
            'ReadParquetFilepathType')


read_parquet_fpath_type = ReadParquetFilepathType()
types.read_parquet_fpath_type = read_parquet_fpath_type
register_model(ReadParquetFilepathType)(models.OpaqueModel)


@unbox(ReadParquetFilepathType)
def unbox_read_parquet_fpath_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ParquetFileInfo(FileInfo):

    def __init__(self, columns, storage_options=None, input_file_name_col=
        None, read_as_dict_cols=None):
        self.columns = columns
        self.storage_options = storage_options
        self.input_file_name_col = input_file_name_col
        self.read_as_dict_cols = read_as_dict_cols
        super().__init__()

    def _get_schema(self, fname):
        try:
            return parquet_file_schema(fname, selected_columns=self.columns,
                storage_options=self.storage_options, input_file_name_col=
                self.input_file_name_col, read_as_dict_cols=self.
                read_as_dict_cols)
        except OSError as lcfu__vpnbn:
            if 'non-file path' in str(lcfu__vpnbn):
                raise FileNotFoundError(str(lcfu__vpnbn))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        dcm__ziml = lhs.scope
        vfae__scw = lhs.loc
        rztp__kplcu = None
        if lhs.name in self.locals:
            rztp__kplcu = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        gwopr__nnko = {}
        if lhs.name + ':convert' in self.locals:
            gwopr__nnko = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if rztp__kplcu is None:
            smcta__bzogb = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/file_io.html#non-constant-filepaths'
                )
            qqn__swzl = get_const_value(file_name, self.func_ir,
                smcta__bzogb, arg_types=self.args, file_info=
                ParquetFileInfo(columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols))
            qnoc__tlyrj = False
            fjtxv__usbk = guard(get_definition, self.func_ir, file_name)
            if isinstance(fjtxv__usbk, ir.Arg):
                typ = self.args[fjtxv__usbk.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, ehwd__msipr, zur__okz, col_indices,
                        partition_names, fel__hchjf, qcdj__xar) = typ.schema
                    qnoc__tlyrj = True
            if not qnoc__tlyrj:
                (col_names, ehwd__msipr, zur__okz, col_indices,
                    partition_names, fel__hchjf, qcdj__xar) = (
                    parquet_file_schema(qqn__swzl, columns, storage_options
                    =storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            fae__tal = list(rztp__kplcu.keys())
            featq__tbov = {c: alvj__hgdd for alvj__hgdd, c in enumerate(
                fae__tal)}
            zvhi__cohii = [ulun__ywe for ulun__ywe in rztp__kplcu.values()]
            zur__okz = 'index' if 'index' in featq__tbov else None
            if columns is None:
                selected_columns = fae__tal
            else:
                selected_columns = columns
            col_indices = [featq__tbov[c] for c in selected_columns]
            ehwd__msipr = [zvhi__cohii[featq__tbov[c]] for c in
                selected_columns]
            col_names = selected_columns
            zur__okz = zur__okz if zur__okz in col_names else None
            partition_names = []
            fel__hchjf = []
            qcdj__xar = []
        asidr__nbd = None if isinstance(zur__okz, dict
            ) or zur__okz is None else zur__okz
        index_column_index = None
        index_column_type = types.none
        if asidr__nbd:
            yqi__mjr = col_names.index(asidr__nbd)
            index_column_index = col_indices.pop(yqi__mjr)
            index_column_type = ehwd__msipr.pop(yqi__mjr)
            col_names.pop(yqi__mjr)
        for alvj__hgdd, c in enumerate(col_names):
            if c in gwopr__nnko:
                ehwd__msipr[alvj__hgdd] = gwopr__nnko[c]
        vqav__eczgi = [ir.Var(dcm__ziml, mk_unique_var('pq_table'),
            vfae__scw), ir.Var(dcm__ziml, mk_unique_var('pq_index'), vfae__scw)
            ]
        idae__nyh = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, ehwd__msipr, vqav__eczgi, vfae__scw,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, fel__hchjf, qcdj__xar)]
        return (col_names, vqav__eczgi, zur__okz, idae__nyh, ehwd__msipr,
            index_column_type)


def determine_filter_cast(pq_node, typemap, filter_val, orig_colname_map):
    klx__nrayi = filter_val[0]
    dxdfi__dln = pq_node.original_out_types[orig_colname_map[klx__nrayi]]
    qap__scnfh = bodo.utils.typing.element_type(dxdfi__dln)
    if klx__nrayi in pq_node.partition_names:
        if qap__scnfh == types.unicode_type:
            xslw__xseo = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(qap__scnfh, types.Integer):
            xslw__xseo = f'.cast(pyarrow.{qap__scnfh.name}(), safe=False)'
        else:
            xslw__xseo = ''
    else:
        xslw__xseo = ''
    pkz__stkq = typemap[filter_val[2].name]
    if isinstance(pkz__stkq, (types.List, types.Set)):
        zdyzb__tchn = pkz__stkq.dtype
    else:
        zdyzb__tchn = pkz__stkq
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(qap__scnfh,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(zdyzb__tchn,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([qap__scnfh, zdyzb__tchn]):
        if not bodo.utils.typing.is_safe_arrow_cast(qap__scnfh, zdyzb__tchn):
            raise BodoError(
                f'Unsupported Arrow cast from {qap__scnfh} to {zdyzb__tchn} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if qap__scnfh == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif qap__scnfh in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(pkz__stkq, (types.List, types.Set)):
                lfiz__eoms = 'list' if isinstance(pkz__stkq, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {lfiz__eoms} values with isin filter pushdown.'
                    )
            return xslw__xseo, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return xslw__xseo, ''


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    xur__tdpqa = len(pq_node.out_vars)
    extra_args = ''
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    bha__cvix, wtlq__hka = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    if pq_node.filters:
        ojqos__xhtm = []
        xtg__vzgw = []
        uieh__oobmu = False
        esz__egbc = None
        orig_colname_map = {c: alvj__hgdd for alvj__hgdd, c in enumerate(
            pq_node.original_df_colnames)}
        for fjyv__smox in pq_node.filters:
            gnqru__jhi = []
            gfnn__acwoa = []
            tirb__egdk = set()
            for uhico__lfpf in fjyv__smox:
                if isinstance(uhico__lfpf[2], ir.Var):
                    psp__ytkpu, txx__imjeu = determine_filter_cast(pq_node,
                        typemap, uhico__lfpf, orig_colname_map)
                    if uhico__lfpf[1] == 'in':
                        gfnn__acwoa.append(
                            f"(ds.field('{uhico__lfpf[0]}').isin({bha__cvix[uhico__lfpf[2].name]}))"
                            )
                    else:
                        gfnn__acwoa.append(
                            f"(ds.field('{uhico__lfpf[0]}'){psp__ytkpu} {uhico__lfpf[1]} ds.scalar({bha__cvix[uhico__lfpf[2].name]}){txx__imjeu})"
                            )
                else:
                    assert uhico__lfpf[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if uhico__lfpf[1] == 'is not':
                        prefix = '~'
                    else:
                        prefix = ''
                    gfnn__acwoa.append(
                        f"({prefix}ds.field('{uhico__lfpf[0]}').is_null())")
                if uhico__lfpf[0] in pq_node.partition_names and isinstance(
                    uhico__lfpf[2], ir.Var):
                    zgcqs__exm = (
                        f"('{uhico__lfpf[0]}', '{uhico__lfpf[1]}', {bha__cvix[uhico__lfpf[2].name]})"
                        )
                    gnqru__jhi.append(zgcqs__exm)
                    tirb__egdk.add(zgcqs__exm)
                else:
                    uieh__oobmu = True
            if esz__egbc is None:
                esz__egbc = tirb__egdk
            else:
                esz__egbc.intersection_update(tirb__egdk)
            hto__falr = ', '.join(gnqru__jhi)
            rdh__dmks = ' & '.join(gfnn__acwoa)
            if hto__falr:
                ojqos__xhtm.append(f'[{hto__falr}]')
            xtg__vzgw.append(f'({rdh__dmks})')
        uxal__rmbpc = ', '.join(ojqos__xhtm)
        dosvc__sdr = ' | '.join(xtg__vzgw)
        if uieh__oobmu:
            if esz__egbc:
                xipw__fdaf = sorted(esz__egbc)
                dnf_filter_str = f"[[{', '.join(xipw__fdaf)}]]"
        elif uxal__rmbpc:
            dnf_filter_str = f'[{uxal__rmbpc}]'
        expr_filter_str = f'({dosvc__sdr})'
        extra_args = ', '.join(bha__cvix.values())
    nsiak__akkm = ', '.join(f'out{alvj__hgdd}' for alvj__hgdd in range(
        xur__tdpqa))
    mwjhs__kxxly = f'def pq_impl(fname, {extra_args}):\n'
    mwjhs__kxxly += (
        f'    (total_rows, {nsiak__akkm},) = _pq_reader_py(fname, {extra_args})\n'
        )
    dxujf__rpp = {}
    exec(mwjhs__kxxly, {}, dxujf__rpp)
    bcbcr__llncc = dxujf__rpp['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        adtez__epa = pq_node.loc.strformat()
        sjnqd__iznc = []
        jcjv__zwfv = []
        for alvj__hgdd in pq_node.type_usecol_offset:
            klx__nrayi = pq_node.df_colnames[alvj__hgdd]
            sjnqd__iznc.append(klx__nrayi)
            if isinstance(pq_node.out_types[alvj__hgdd], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                jcjv__zwfv.append(klx__nrayi)
        hdjy__tnv = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', hdjy__tnv,
            adtez__epa, sjnqd__iznc)
        if jcjv__zwfv:
            ipy__jlnmr = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', ipy__jlnmr,
                adtez__epa, jcjv__zwfv)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        ammuz__hctf = set(pq_node.type_usecol_offset)
        gmidk__wkp = set(pq_node.unsupported_columns)
        pzzgr__enq = ammuz__hctf & gmidk__wkp
        if pzzgr__enq:
            ivb__qvjor = sorted(pzzgr__enq)
            dep__tukf = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            puzuc__ojjr = 0
            for iwkvq__dklwr in ivb__qvjor:
                while pq_node.unsupported_columns[puzuc__ojjr] != iwkvq__dklwr:
                    puzuc__ojjr += 1
                dep__tukf.append(
                    f"Column '{pq_node.df_colnames[iwkvq__dklwr]}' with unsupported arrow type {pq_node.unsupported_arrow_types[puzuc__ojjr]}"
                    )
                puzuc__ojjr += 1
            gtm__bzfaq = '\n'.join(dep__tukf)
            raise BodoError(gtm__bzfaq, loc=pq_node.loc)
    mhzg__mgcsi = _gen_pq_reader_py(pq_node.df_colnames, pq_node.
        col_indices, pq_node.type_usecol_offset, pq_node.out_types, pq_node
        .storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    czbop__skhno = typemap[pq_node.file_name.name]
    kdwy__pjp = (czbop__skhno,) + tuple(typemap[uhico__lfpf.name] for
        uhico__lfpf in wtlq__hka)
    olizp__lpkio = compile_to_numba_ir(bcbcr__llncc, {'_pq_reader_py':
        mhzg__mgcsi}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        kdwy__pjp, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(olizp__lpkio, [pq_node.file_name] + wtlq__hka)
    idae__nyh = olizp__lpkio.body[:-3]
    if meta_head_only_info:
        idae__nyh[-1 - xur__tdpqa].target = meta_head_only_info[1]
    idae__nyh[-2].target = pq_node.out_vars[0]
    idae__nyh[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        idae__nyh.pop(-1)
    elif not pq_node.type_usecol_offset:
        idae__nyh.pop(-2)
    return idae__nyh


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    bfeer__sqqnz = get_overload_const_str(dnf_filter_str)
    micvm__wumgf = get_overload_const_str(expr_filter_str)
    evf__gpfj = ', '.join(f'f{alvj__hgdd}' for alvj__hgdd in range(len(
        var_tup)))
    mwjhs__kxxly = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        mwjhs__kxxly += f'  {evf__gpfj}, = var_tup\n'
    mwjhs__kxxly += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    mwjhs__kxxly += f'    dnf_filters_py = {bfeer__sqqnz}\n'
    mwjhs__kxxly += f'    expr_filters_py = {micvm__wumgf}\n'
    mwjhs__kxxly += '  return (dnf_filters_py, expr_filters_py)\n'
    dxujf__rpp = {}
    exec(mwjhs__kxxly, globals(), dxujf__rpp)
    return dxujf__rpp['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    jrz__qxt = next_label()
    boy__ozwp = ',' if extra_args else ''
    mwjhs__kxxly = f'def pq_reader_py(fname,{extra_args}):\n'
    mwjhs__kxxly += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    mwjhs__kxxly += f"    ev.add_attribute('g_fname', fname)\n"
    mwjhs__kxxly += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    mwjhs__kxxly += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{boy__ozwp}))
"""
    mwjhs__kxxly += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    mwjhs__kxxly += f"""    storage_options_py = get_storage_options_pyobject({str(storage_options)})
"""
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    foe__uxjal = not type_usecol_offset
    pyi__izs = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    cstr__wyk = {c: alvj__hgdd for alvj__hgdd, c in enumerate(col_indices)}
    ljuvw__fzx = {c: alvj__hgdd for alvj__hgdd, c in enumerate(pyi__izs)}
    yusv__zqf = []
    wnjo__vcgc = set()
    pddxz__kbovp = partition_names + [input_file_name_col]
    for alvj__hgdd in type_usecol_offset:
        if pyi__izs[alvj__hgdd] not in pddxz__kbovp:
            yusv__zqf.append(col_indices[alvj__hgdd])
        elif not input_file_name_col or pyi__izs[alvj__hgdd
            ] != input_file_name_col:
            wnjo__vcgc.add(col_indices[alvj__hgdd])
    if index_column_index is not None:
        yusv__zqf.append(index_column_index)
    yusv__zqf = sorted(yusv__zqf)
    ulupt__jpk = {c: alvj__hgdd for alvj__hgdd, c in enumerate(yusv__zqf)}

    def is_nullable(typ):
        return bodo.utils.utils.is_array_typ(typ, False) and (not
            isinstance(typ, types.Array) and not isinstance(typ, bodo.
            DatetimeArrayType))
    ksgw__ilv = [(int(is_nullable(out_types[cstr__wyk[asnp__sdbr]])) if 
        asnp__sdbr != index_column_index else int(is_nullable(
        index_column_type))) for asnp__sdbr in yusv__zqf]
    str_as_dict_cols = []
    for asnp__sdbr in yusv__zqf:
        if asnp__sdbr == index_column_index:
            ulun__ywe = index_column_type
        else:
            ulun__ywe = out_types[cstr__wyk[asnp__sdbr]]
        if ulun__ywe == dict_str_arr_type:
            str_as_dict_cols.append(asnp__sdbr)
    wqp__qybfz = []
    lardg__rklit = {}
    xvdly__pmlxl = []
    jwq__mgm = []
    for alvj__hgdd, oso__asd in enumerate(partition_names):
        try:
            rxlzu__sqj = ljuvw__fzx[oso__asd]
            if col_indices[rxlzu__sqj] not in wnjo__vcgc:
                continue
        except (KeyError, ValueError) as bifny__jabv:
            continue
        lardg__rklit[oso__asd] = len(wqp__qybfz)
        wqp__qybfz.append(oso__asd)
        xvdly__pmlxl.append(alvj__hgdd)
        kpi__mhygu = out_types[rxlzu__sqj].dtype
        miam__pdtfg = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            kpi__mhygu)
        jwq__mgm.append(numba_to_c_type(miam__pdtfg))
    mwjhs__kxxly += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    mwjhs__kxxly += f'    out_table = pq_read(\n'
    mwjhs__kxxly += f'        fname_py, {is_parallel},\n'
    mwjhs__kxxly += f'        unicode_to_utf8(bucket_region),\n'
    mwjhs__kxxly += f'        dnf_filters, expr_filters,\n'
    mwjhs__kxxly += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{jrz__qxt}.ctypes,
"""
    mwjhs__kxxly += f'        {len(yusv__zqf)},\n'
    mwjhs__kxxly += f'        nullable_cols_arr_{jrz__qxt}.ctypes,\n'
    if len(xvdly__pmlxl) > 0:
        mwjhs__kxxly += (
            f'        np.array({xvdly__pmlxl}, dtype=np.int32).ctypes,\n')
        mwjhs__kxxly += (
            f'        np.array({jwq__mgm}, dtype=np.int32).ctypes,\n')
        mwjhs__kxxly += f'        {len(xvdly__pmlxl)},\n'
    else:
        mwjhs__kxxly += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        mwjhs__kxxly += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        mwjhs__kxxly += f'        0, 0,\n'
    mwjhs__kxxly += f'        total_rows_np.ctypes,\n'
    mwjhs__kxxly += f'        {input_file_name_col is not None},\n'
    mwjhs__kxxly += f'    )\n'
    mwjhs__kxxly += f'    check_and_propagate_cpp_exception()\n'
    ktvt__gxv = 'None'
    mmf__ihthu = index_column_type
    fzxa__bvky = TableType(tuple(out_types))
    if foe__uxjal:
        fzxa__bvky = types.none
    if index_column_index is not None:
        fvek__jdnq = ulupt__jpk[index_column_index]
        ktvt__gxv = (
            f'info_to_array(info_from_table(out_table, {fvek__jdnq}), index_arr_type)'
            )
    mwjhs__kxxly += f'    index_arr = {ktvt__gxv}\n'
    if foe__uxjal:
        cxhtr__vgc = None
    else:
        cxhtr__vgc = []
        vzog__hqk = 0
        ypmxo__bgk = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for alvj__hgdd, iwkvq__dklwr in enumerate(col_indices):
            if vzog__hqk < len(type_usecol_offset
                ) and alvj__hgdd == type_usecol_offset[vzog__hqk]:
                uozug__nbf = col_indices[alvj__hgdd]
                if ypmxo__bgk and uozug__nbf == ypmxo__bgk:
                    cxhtr__vgc.append(len(yusv__zqf) + len(wqp__qybfz))
                elif uozug__nbf in wnjo__vcgc:
                    cyb__cnq = pyi__izs[alvj__hgdd]
                    cxhtr__vgc.append(len(yusv__zqf) + lardg__rklit[cyb__cnq])
                else:
                    cxhtr__vgc.append(ulupt__jpk[iwkvq__dklwr])
                vzog__hqk += 1
            else:
                cxhtr__vgc.append(-1)
        cxhtr__vgc = np.array(cxhtr__vgc, dtype=np.int64)
    if foe__uxjal:
        mwjhs__kxxly += '    T = None\n'
    else:
        mwjhs__kxxly += f"""    T = cpp_table_to_py_table(out_table, table_idx_{jrz__qxt}, py_table_type_{jrz__qxt})
"""
    mwjhs__kxxly += f'    delete_table(out_table)\n'
    mwjhs__kxxly += f'    total_rows = total_rows_np[0]\n'
    mwjhs__kxxly += f'    ev.finalize()\n'
    mwjhs__kxxly += f'    return (total_rows, T, index_arr)\n'
    dxujf__rpp = {}
    anlic__fokvh = {f'py_table_type_{jrz__qxt}': fzxa__bvky,
        f'table_idx_{jrz__qxt}': cxhtr__vgc,
        f'selected_cols_arr_{jrz__qxt}': np.array(yusv__zqf, np.int32),
        f'nullable_cols_arr_{jrz__qxt}': np.array(ksgw__ilv, np.int32),
        'index_arr_type': mmf__ihthu, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(mwjhs__kxxly, anlic__fokvh, dxujf__rpp)
    mhzg__mgcsi = dxujf__rpp['pq_reader_py']
    xacus__zpcn = numba.njit(mhzg__mgcsi, no_cpython_wrapper=True)
    return xacus__zpcn


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    waq__cydf = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in waq__cydf:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        xvde__lctqo = pa_ts_typ.to_pandas_dtype().tz
        quzma__jxbes = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            xvde__lctqo)
        return bodo.DatetimeArrayType(quzma__jxbes), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        afn__lpif, secxn__jbcp = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(afn__lpif), secxn__jbcp
    if isinstance(pa_typ.type, pa.StructType):
        xtsn__zuves = []
        iehb__mara = []
        secxn__jbcp = True
        for mbng__adj in pa_typ.flatten():
            iehb__mara.append(mbng__adj.name.split('.')[-1])
            bpfy__bpq, hin__shnf = _get_numba_typ_from_pa_typ(mbng__adj,
                is_index, nullable_from_metadata, category_info)
            xtsn__zuves.append(bpfy__bpq)
            secxn__jbcp = secxn__jbcp and hin__shnf
        return StructArrayType(tuple(xtsn__zuves), tuple(iehb__mara)
            ), secxn__jbcp
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale), True
    if str_as_dict:
        if pa_typ.type != pa.string():
            raise BodoError(
                f'Read as dictionary used for non-string column {pa_typ}')
        return dict_str_arr_type, True
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        qxwl__kfer = _pa_numba_typ_map[pa_typ.type.index_type]
        ehivw__paj = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=qxwl__kfer)
        return CategoricalArrayType(ehivw__paj), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        nzuw__oyuhu = _pa_numba_typ_map[pa_typ.type]
        secxn__jbcp = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if nzuw__oyuhu == datetime_date_type:
        return datetime_date_array_type, secxn__jbcp
    if nzuw__oyuhu == bytes_type:
        return binary_array_type, secxn__jbcp
    afn__lpif = (string_array_type if nzuw__oyuhu == string_type else types
        .Array(nzuw__oyuhu, 1, 'C'))
    if nzuw__oyuhu == types.bool_:
        afn__lpif = boolean_array
    if nullable_from_metadata is not None:
        hxxub__znhql = nullable_from_metadata
    else:
        hxxub__znhql = use_nullable_int_arr
    if hxxub__znhql and not is_index and isinstance(nzuw__oyuhu, types.Integer
        ) and pa_typ.nullable:
        afn__lpif = IntegerArrayType(nzuw__oyuhu)
    return afn__lpif, secxn__jbcp


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None):
    if get_row_counts:
        stfhc__jlbi = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    msj__kwzng = MPI.COMM_WORLD
    if isinstance(fpath, list):
        pcaz__cwoln = urlparse(fpath[0])
        protocol = pcaz__cwoln.scheme
        elh__evny = pcaz__cwoln.netloc
        for alvj__hgdd in range(len(fpath)):
            audd__dtm = fpath[alvj__hgdd]
            nzgki__hwzc = urlparse(audd__dtm)
            if nzgki__hwzc.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if nzgki__hwzc.netloc != elh__evny:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[alvj__hgdd] = audd__dtm.rstrip('/')
    else:
        pcaz__cwoln = urlparse(fpath)
        protocol = pcaz__cwoln.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as bifny__jabv:
            iettr__nah = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(iettr__nah)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as bifny__jabv:
            iettr__nah = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
"""
    fs = []

    def getfs(parallel=False):
        if len(fs) == 1:
            return fs[0]
        if protocol == 's3':
            fs.append(get_s3_fs_from_path(fpath, parallel=parallel,
                storage_options=storage_options) if not isinstance(fpath,
                list) else get_s3_fs_from_path(fpath[0], parallel=parallel,
                storage_options=storage_options))
        elif protocol in {'gcs', 'gs'}:
            dcw__vtwj = gcsfs.GCSFileSystem(token=None)
            fs.append(dcw__vtwj)
        elif protocol == 'http':
            fs.append(fsspec.filesystem('http'))
        elif protocol in {'hdfs', 'abfs', 'abfss'}:
            fs.append(get_hdfs_fs(fpath) if not isinstance(fpath, list) else
                get_hdfs_fs(fpath[0]))
        else:
            fs.append(None)
        return fs[0]

    def get_legacy_fs():
        if protocol in {'s3', 'hdfs', 'abfs', 'abfss'}:
            from fsspec.implementations.arrow import ArrowFSWrapper
            return ArrowFSWrapper(getfs())
        else:
            return getfs()

    def glob(protocol, fs, path):
        if not protocol and fs is None:
            from fsspec.implementations.local import LocalFileSystem
            fs = LocalFileSystem()
        if isinstance(fs, pyarrow.fs.FileSystem):
            from fsspec.implementations.arrow import ArrowFSWrapper
            fs = ArrowFSWrapper(fs)
        try:
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{pcaz__cwoln.netloc}'
                path = path[len(prefix):]
            ider__bnbk = fs.glob(path)
            if protocol == 's3':
                ider__bnbk = [('s3://' + audd__dtm) for audd__dtm in
                    ider__bnbk if not audd__dtm.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                ider__bnbk = [(prefix + audd__dtm) for audd__dtm in ider__bnbk]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(ider__bnbk) == 0:
            raise BodoError('No files found matching glob pattern')
        return ider__bnbk
    vxng__jgfb = False
    if get_row_counts:
        ymymd__pjb = getfs(parallel=True)
        vxng__jgfb = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        rou__xjf = 1
        hbng__vnlj = os.cpu_count()
        if hbng__vnlj is not None and hbng__vnlj > 1:
            rou__xjf = hbng__vnlj // 2
        try:
            if get_row_counts:
                rxwv__dqpsv = tracing.Event('pq.ParquetDataset',
                    is_parallel=False)
                if tracing.is_tracing():
                    rxwv__dqpsv.add_attribute('g_dnf_filter', str(dnf_filters))
            mizja__vpzm = pa.io_thread_count()
            pa.set_io_thread_count(rou__xjf)
            if isinstance(fpath, list):
                vdrs__nxv = []
                for ycua__xgdw in fpath:
                    if has_magic(ycua__xgdw):
                        vdrs__nxv += glob(protocol, getfs(), ycua__xgdw)
                    else:
                        vdrs__nxv.append(ycua__xgdw)
                fpath = vdrs__nxv
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{pcaz__cwoln.netloc}'
                if isinstance(fpath, list):
                    dsezp__xswju = [audd__dtm[len(prefix):] for audd__dtm in
                        fpath]
                else:
                    dsezp__xswju = fpath[len(prefix):]
            else:
                dsezp__xswju = fpath
            mlw__stse = pq.ParquetDataset(dsezp__xswju, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=rou__xjf)
            pa.set_io_thread_count(mizja__vpzm)
            naqjb__gaef = bodo.io.pa_parquet.get_dataset_schema(mlw__stse)
            if dnf_filters:
                if get_row_counts:
                    rxwv__dqpsv.add_attribute('num_pieces_before_filter',
                        len(mlw__stse.pieces))
                dscq__apmil = time.time()
                mlw__stse._filter(dnf_filters)
                if get_row_counts:
                    rxwv__dqpsv.add_attribute('dnf_filter_time', time.time(
                        ) - dscq__apmil)
                    rxwv__dqpsv.add_attribute('num_pieces_after_filter',
                        len(mlw__stse.pieces))
            if get_row_counts:
                rxwv__dqpsv.finalize()
            mlw__stse._metadata.fs = None
        except Exception as lcfu__vpnbn:
            if isinstance(fpath, list) and isinstance(lcfu__vpnbn, (OSError,
                FileNotFoundError)):
                lcfu__vpnbn = BodoError(str(lcfu__vpnbn) +
                    list_of_files_error_msg)
            else:
                lcfu__vpnbn = BodoError(
                    f"""error from pyarrow: {type(lcfu__vpnbn).__name__}: {str(lcfu__vpnbn)}
"""
                    )
            msj__kwzng.bcast(lcfu__vpnbn)
            raise lcfu__vpnbn
        if get_row_counts:
            bdfm__fmzm = tracing.Event('bcast dataset')
        msj__kwzng.bcast(mlw__stse)
        msj__kwzng.bcast(naqjb__gaef)
    else:
        if get_row_counts:
            bdfm__fmzm = tracing.Event('bcast dataset')
        mlw__stse = msj__kwzng.bcast(None)
        if isinstance(mlw__stse, Exception):
            iyukz__maw = mlw__stse
            raise iyukz__maw
        naqjb__gaef = msj__kwzng.bcast(None)
    if get_row_counts:
        zhpa__exl = getfs()
    else:
        zhpa__exl = get_legacy_fs()
    mlw__stse._metadata.fs = zhpa__exl
    if get_row_counts:
        bdfm__fmzm.finalize()
    mlw__stse._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = vxng__jgfb = False
        for ycua__xgdw in mlw__stse.pieces:
            ycua__xgdw._bodo_num_rows = 0
    if get_row_counts or vxng__jgfb:
        if get_row_counts and tracing.is_tracing():
            gih__navjs = tracing.Event('get_row_counts')
            gih__navjs.add_attribute('g_num_pieces', len(mlw__stse.pieces))
            gih__navjs.add_attribute('g_expr_filters', str(expr_filters))
        mtb__bal = 0.0
        num_pieces = len(mlw__stse.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        sbw__tigdl = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        yhcs__bveo = 0
        itnow__cilll = 0
        uhpii__gyma = 0
        kur__band = True
        if expr_filters is not None:
            import random
            random.seed(37)
            nxb__hzzzx = random.sample(mlw__stse.pieces, k=len(mlw__stse.
                pieces))
        else:
            nxb__hzzzx = mlw__stse.pieces
        for ycua__xgdw in nxb__hzzzx:
            ycua__xgdw._bodo_num_rows = 0
        fpaths = [ycua__xgdw.path for ycua__xgdw in nxb__hzzzx[start:
            sbw__tigdl]]
        if protocol == 's3':
            elh__evny = pcaz__cwoln.netloc
            prefix = 's3://' + elh__evny + '/'
            fpaths = [audd__dtm[len(prefix):] for audd__dtm in fpaths]
            zhpa__exl = get_s3_subtree_fs(elh__evny, region=getfs().region,
                storage_options=storage_options)
        else:
            zhpa__exl = getfs()
        rou__xjf = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(rou__xjf)
        pa.set_cpu_count(rou__xjf)
        iyukz__maw = None
        try:
            sypav__ojvn = ds.dataset(fpaths, filesystem=zhpa__exl,
                partitioning=ds.partitioning(flavor='hive'))
            for fqqev__thnw, ufd__kwzmf in zip(nxb__hzzzx[start:sbw__tigdl],
                sypav__ojvn.get_fragments()):
                dscq__apmil = time.time()
                abp__iyd = ufd__kwzmf.scanner(schema=sypav__ojvn.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                mtb__bal += time.time() - dscq__apmil
                fqqev__thnw._bodo_num_rows = abp__iyd
                yhcs__bveo += abp__iyd
                itnow__cilll += ufd__kwzmf.num_row_groups
                uhpii__gyma += sum(glu__yyrx.total_byte_size for glu__yyrx in
                    ufd__kwzmf.row_groups)
                if vxng__jgfb:
                    ypj__ndmy = ufd__kwzmf.metadata.schema.to_arrow_schema()
                    if naqjb__gaef != ypj__ndmy:
                        print(
                            'Schema in {!s} was different. \n{!s}\n\nvs\n\n{!s}'
                            .format(fqqev__thnw, ypj__ndmy, naqjb__gaef))
                        kur__band = False
                        break
        except Exception as lcfu__vpnbn:
            iyukz__maw = lcfu__vpnbn
        if msj__kwzng.allreduce(iyukz__maw is not None, op=MPI.LOR):
            for iyukz__maw in msj__kwzng.allgather(iyukz__maw):
                if iyukz__maw:
                    if isinstance(fpath, list) and isinstance(iyukz__maw, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(iyukz__maw) +
                            list_of_files_error_msg)
                    raise iyukz__maw
        if vxng__jgfb:
            kur__band = msj__kwzng.allreduce(kur__band, op=MPI.LAND)
            if not kur__band:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            mlw__stse._bodo_total_rows = msj__kwzng.allreduce(yhcs__bveo,
                op=MPI.SUM)
            xtff__lhqpu = msj__kwzng.allreduce(itnow__cilll, op=MPI.SUM)
            mchj__osi = msj__kwzng.allreduce(uhpii__gyma, op=MPI.SUM)
            nkpo__hbz = np.array([ycua__xgdw._bodo_num_rows for ycua__xgdw in
                mlw__stse.pieces])
            nkpo__hbz = msj__kwzng.allreduce(nkpo__hbz, op=MPI.SUM)
            for ycua__xgdw, uaby__pkk in zip(mlw__stse.pieces, nkpo__hbz):
                ycua__xgdw._bodo_num_rows = uaby__pkk
            if is_parallel and bodo.get_rank(
                ) == 0 and xtff__lhqpu < bodo.get_size() and xtff__lhqpu != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({xtff__lhqpu}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()})
"""
                    ))
            if xtff__lhqpu == 0:
                muyj__ukd = 0
            else:
                muyj__ukd = mchj__osi // xtff__lhqpu
            if (bodo.get_rank() == 0 and mchj__osi >= 20 * 1048576 and 
                muyj__ukd < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({muyj__ukd} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                gih__navjs.add_attribute('g_total_num_row_groups', xtff__lhqpu)
                gih__navjs.add_attribute('total_scan_time', mtb__bal)
                ejfo__hqdju = np.array([ycua__xgdw._bodo_num_rows for
                    ycua__xgdw in mlw__stse.pieces])
                bfsx__fnv = np.percentile(ejfo__hqdju, [25, 50, 75])
                gih__navjs.add_attribute('g_row_counts_min', ejfo__hqdju.min())
                gih__navjs.add_attribute('g_row_counts_Q1', bfsx__fnv[0])
                gih__navjs.add_attribute('g_row_counts_median', bfsx__fnv[1])
                gih__navjs.add_attribute('g_row_counts_Q3', bfsx__fnv[2])
                gih__navjs.add_attribute('g_row_counts_max', ejfo__hqdju.max())
                gih__navjs.add_attribute('g_row_counts_mean', ejfo__hqdju.
                    mean())
                gih__navjs.add_attribute('g_row_counts_std', ejfo__hqdju.std())
                gih__navjs.add_attribute('g_row_counts_sum', ejfo__hqdju.sum())
                gih__navjs.finalize()
    mlw__stse._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{pcaz__cwoln.netloc}'
        if len(mlw__stse.pieces) > 0:
            fqqev__thnw = mlw__stse.pieces[0]
            if not fqqev__thnw.path.startswith(prefix):
                mlw__stse._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(mlw__stse)
    if get_row_counts:
        stfhc__jlbi.finalize()
    return mlw__stse


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read):
    import pyarrow as pa
    hbng__vnlj = os.cpu_count()
    if hbng__vnlj is None or hbng__vnlj == 0:
        hbng__vnlj = 2
    amrgv__psrr = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), hbng__vnlj
        )
    nirr__pkpw = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), hbng__vnlj
        )
    if is_parallel and len(fpaths) > nirr__pkpw and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(nirr__pkpw)
        pa.set_cpu_count(nirr__pkpw)
    else:
        pa.set_io_thread_count(amrgv__psrr)
        pa.set_cpu_count(amrgv__psrr)
    if fpaths[0].startswith('s3://'):
        elh__evny = urlparse(fpaths[0]).netloc
        prefix = 's3://' + elh__evny + '/'
        fpaths = [audd__dtm[len(prefix):] for audd__dtm in fpaths]
        zhpa__exl = get_s3_subtree_fs(elh__evny, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        zhpa__exl = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        zhpa__exl = gcsfs.GCSFileSystem(token=None)
    else:
        zhpa__exl = None
    mgm__xgb = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    mlw__stse = ds.dataset(fpaths, filesystem=zhpa__exl, partitioning=ds.
        partitioning(flavor='hive'), format=mgm__xgb)
    col_names = mlw__stse.schema.names
    ibkg__fnjbn = [col_names[kanhx__lvsi] for kanhx__lvsi in selected_fields]
    gfqa__inm = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if gfqa__inm and expr_filters is None:
        gsfb__gymg = []
        hmhcu__sxs = 0
        ygvs__whpc = 0
        for ufd__kwzmf in mlw__stse.get_fragments():
            djrhm__wnain = []
            for glu__yyrx in ufd__kwzmf.row_groups:
                xzb__mfbk = glu__yyrx.num_rows
                if start_offset < hmhcu__sxs + xzb__mfbk:
                    if ygvs__whpc == 0:
                        sbzj__ppxa = start_offset - hmhcu__sxs
                        uzmy__llke = min(xzb__mfbk - sbzj__ppxa, rows_to_read)
                    else:
                        uzmy__llke = min(xzb__mfbk, rows_to_read - ygvs__whpc)
                    ygvs__whpc += uzmy__llke
                    djrhm__wnain.append(glu__yyrx.id)
                hmhcu__sxs += xzb__mfbk
                if ygvs__whpc == rows_to_read:
                    break
            gsfb__gymg.append(ufd__kwzmf.subset(row_group_ids=djrhm__wnain))
            if ygvs__whpc == rows_to_read:
                break
        mlw__stse = ds.FileSystemDataset(gsfb__gymg, mlw__stse.schema,
            mgm__xgb, filesystem=mlw__stse.filesystem)
        start_offset = sbzj__ppxa
    rzu__epfbq = mlw__stse.scanner(columns=ibkg__fnjbn, filter=expr_filters,
        use_threads=True).to_reader()
    return mlw__stse, rzu__epfbq, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    qnf__ezib = [c for c in pa_schema.names if isinstance(pa_schema.field(c
        ).type, pa.DictionaryType)]
    if len(qnf__ezib) == 0:
        pq_dataset._category_info = {}
        return
    msj__kwzng = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            drn__fsq = pq_dataset.pieces[0].open()
            glu__yyrx = drn__fsq.read_row_group(0, qnf__ezib)
            category_info = {c: tuple(glu__yyrx.column(c).chunk(0).
                dictionary.to_pylist()) for c in qnf__ezib}
            del drn__fsq, glu__yyrx
        except Exception as lcfu__vpnbn:
            msj__kwzng.bcast(lcfu__vpnbn)
            raise lcfu__vpnbn
        msj__kwzng.bcast(category_info)
    else:
        category_info = msj__kwzng.bcast(None)
        if isinstance(category_info, Exception):
            iyukz__maw = category_info
            raise iyukz__maw
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    zur__okz = None
    nullable_from_metadata = defaultdict(lambda : None)
    kbju__ndjfe = b'pandas'
    if schema.metadata is not None and kbju__ndjfe in schema.metadata:
        import json
        mgyy__ltiyx = json.loads(schema.metadata[kbju__ndjfe].decode('utf8'))
        tpmr__xfr = len(mgyy__ltiyx['index_columns'])
        if tpmr__xfr > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        zur__okz = mgyy__ltiyx['index_columns'][0] if tpmr__xfr else None
        if not isinstance(zur__okz, str) and (not isinstance(zur__okz, dict
            ) or num_pieces != 1):
            zur__okz = None
        for wwxx__pbeo in mgyy__ltiyx['columns']:
            qsyv__ndc = wwxx__pbeo['name']
            if wwxx__pbeo['pandas_type'].startswith('int'
                ) and qsyv__ndc is not None:
                if wwxx__pbeo['numpy_type'].startswith('Int'):
                    nullable_from_metadata[qsyv__ndc] = True
                else:
                    nullable_from_metadata[qsyv__ndc] = False
    return zur__okz, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for qsyv__ndc in pa_schema.names:
        mbng__adj = pa_schema.field(qsyv__ndc)
        if mbng__adj.type == pa.string():
            str_columns.append(qsyv__ndc)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    msj__kwzng = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        nxb__hzzzx = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        nxb__hzzzx = pq_dataset.pieces
    pmdb__pyqu = np.zeros(len(str_columns), dtype=np.int64)
    ceklj__pwxhw = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(nxb__hzzzx):
        fqqev__thnw = nxb__hzzzx[bodo.get_rank()]
        try:
            vwmy__txmrs = fqqev__thnw.get_metadata()
            for alvj__hgdd in range(vwmy__txmrs.num_row_groups):
                for vzog__hqk, qsyv__ndc in enumerate(str_columns):
                    puzuc__ojjr = pa_schema.get_field_index(qsyv__ndc)
                    pmdb__pyqu[vzog__hqk] += vwmy__txmrs.row_group(alvj__hgdd
                        ).column(puzuc__ojjr).total_uncompressed_size
            cchu__nvqkv = vwmy__txmrs.num_rows
        except Exception as lcfu__vpnbn:
            if isinstance(lcfu__vpnbn, (OSError, FileNotFoundError)):
                cchu__nvqkv = 0
            else:
                raise
    else:
        cchu__nvqkv = 0
    djt__yuu = msj__kwzng.allreduce(cchu__nvqkv, op=MPI.SUM)
    if djt__yuu == 0:
        return set()
    msj__kwzng.Allreduce(pmdb__pyqu, ceklj__pwxhw, op=MPI.SUM)
    lxv__ljg = ceklj__pwxhw / djt__yuu
    str_as_dict = set()
    for alvj__hgdd, ghvwa__sxu in enumerate(lxv__ljg):
        if ghvwa__sxu < READ_STR_AS_DICT_THRESHOLD:
            qsyv__ndc = str_columns[alvj__hgdd][0]
            str_as_dict.add(qsyv__ndc)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    ehwd__msipr = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[alvj__hgdd].name for alvj__hgdd in range(len(
        pq_dataset.partitions.partition_names))]
    pa_schema = pq_dataset.schema.to_arrow_schema()
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    stkxl__tvapu = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    xqhov__lfo = read_as_dict_cols - stkxl__tvapu
    if len(xqhov__lfo) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {xqhov__lfo}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(stkxl__tvapu)
    stkxl__tvapu = stkxl__tvapu - read_as_dict_cols
    str_columns = [jnv__gkx for jnv__gkx in str_columns if jnv__gkx in
        stkxl__tvapu]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    zur__okz, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    zvhi__cohii = []
    bov__fijch = []
    voa__gjbt = []
    for alvj__hgdd, c in enumerate(col_names):
        mbng__adj = pa_schema.field(c)
        nzuw__oyuhu, secxn__jbcp = _get_numba_typ_from_pa_typ(mbng__adj, c ==
            zur__okz, nullable_from_metadata[c], pq_dataset._category_info,
            str_as_dict=c in str_as_dict)
        zvhi__cohii.append(nzuw__oyuhu)
        bov__fijch.append(secxn__jbcp)
        voa__gjbt.append(mbng__adj.type)
    if partition_names:
        col_names += partition_names
        zvhi__cohii += [_get_partition_cat_dtype(pq_dataset.partitions.
            levels[alvj__hgdd]) for alvj__hgdd in range(len(partition_names))]
        bov__fijch.extend([True] * len(partition_names))
        voa__gjbt.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        zvhi__cohii += [dict_str_arr_type]
        bov__fijch.append(True)
        voa__gjbt.append(None)
    pmcrl__kvab = {c: alvj__hgdd for alvj__hgdd, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in pmcrl__kvab:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if zur__okz and not isinstance(zur__okz, dict
        ) and zur__okz not in selected_columns:
        selected_columns.append(zur__okz)
    col_names = selected_columns
    col_indices = []
    ehwd__msipr = []
    fel__hchjf = []
    qcdj__xar = []
    for alvj__hgdd, c in enumerate(col_names):
        uozug__nbf = pmcrl__kvab[c]
        col_indices.append(uozug__nbf)
        ehwd__msipr.append(zvhi__cohii[uozug__nbf])
        if not bov__fijch[uozug__nbf]:
            fel__hchjf.append(alvj__hgdd)
            qcdj__xar.append(voa__gjbt[uozug__nbf])
    return (col_names, ehwd__msipr, zur__okz, col_indices, partition_names,
        fel__hchjf, qcdj__xar)


def _get_partition_cat_dtype(part_set):
    yfzp__cyed = part_set.dictionary.to_pandas()
    pcdyl__atg = bodo.typeof(yfzp__cyed).dtype
    ehivw__paj = PDCategoricalDtype(tuple(yfzp__cyed), pcdyl__atg, False)
    return CategoricalArrayType(ehivw__paj)


_pq_read = types.ExternalFunction('pq_read', table_type(
    read_parquet_fpath_type, types.boolean, types.voidptr,
    parquet_predicate_type, parquet_predicate_type,
    storage_options_dict_type, types.int64, types.voidptr, types.int32,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.voidptr,
    types.int32, types.voidptr, types.boolean))
from llvmlite import ir as lir
from numba.core import cgutils
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_read', arrow_cpp.pq_read)
    ll.add_symbol('pq_write', arrow_cpp.pq_write)
    ll.add_symbol('pq_write_partitioned', arrow_cpp.pq_write_partitioned)


@intrinsic
def parquet_write_table_cpp(typingctx, filename_t, table_t, col_names_t,
    index_t, write_index, metadata_t, compression_t, is_parallel_t,
    write_range_index, start, stop, step, name, bucket_region, row_group_size):

    def codegen(context, builder, sig, args):
        edza__qawe = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        fgpy__wecnk = cgutils.get_or_insert_function(builder.module,
            edza__qawe, name='pq_write')
        builder.call(fgpy__wecnk, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, table_t, col_names_t, index_t, types.
        boolean, types.voidptr, types.voidptr, types.boolean, types.boolean,
        types.int32, types.int32, types.int32, types.voidptr, types.voidptr,
        types.int64), codegen


@intrinsic
def parquet_write_table_partitioned_cpp(typingctx, filename_t, data_table_t,
    col_names_t, col_names_no_partitions_t, cat_table_t, part_col_idxs_t,
    num_part_col_t, compression_t, is_parallel_t, bucket_region, row_group_size
    ):

    def codegen(context, builder, sig, args):
        edza__qawe = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        fgpy__wecnk = cgutils.get_or_insert_function(builder.module,
            edza__qawe, name='pq_write_partitioned')
        builder.call(fgpy__wecnk, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
