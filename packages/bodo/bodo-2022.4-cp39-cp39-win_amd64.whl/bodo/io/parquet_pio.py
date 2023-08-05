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
        except OSError as pssve__dub:
            if 'non-file path' in str(pssve__dub):
                raise FileNotFoundError(str(pssve__dub))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        xtel__rojmb = lhs.scope
        ifo__fwhp = lhs.loc
        ivhp__aevv = None
        if lhs.name in self.locals:
            ivhp__aevv = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        zkrit__iqh = {}
        if lhs.name + ':convert' in self.locals:
            zkrit__iqh = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if ivhp__aevv is None:
            araw__uhga = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/file_io.html#non-constant-filepaths'
                )
            gidey__bqr = get_const_value(file_name, self.func_ir,
                araw__uhga, arg_types=self.args, file_info=ParquetFileInfo(
                columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols))
            uwh__bil = False
            aop__jhny = guard(get_definition, self.func_ir, file_name)
            if isinstance(aop__jhny, ir.Arg):
                typ = self.args[aop__jhny.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, voui__hryrd, vwlj__hek, col_indices,
                        partition_names, twlmb__bxd, fbo__fph) = typ.schema
                    uwh__bil = True
            if not uwh__bil:
                (col_names, voui__hryrd, vwlj__hek, col_indices,
                    partition_names, twlmb__bxd, fbo__fph) = (
                    parquet_file_schema(gidey__bqr, columns,
                    storage_options=storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            gzakj__pby = list(ivhp__aevv.keys())
            olcwj__zamas = {c: rkx__olxj for rkx__olxj, c in enumerate(
                gzakj__pby)}
            tsg__zcz = [gehjz__ybcse for gehjz__ybcse in ivhp__aevv.values()]
            vwlj__hek = 'index' if 'index' in olcwj__zamas else None
            if columns is None:
                selected_columns = gzakj__pby
            else:
                selected_columns = columns
            col_indices = [olcwj__zamas[c] for c in selected_columns]
            voui__hryrd = [tsg__zcz[olcwj__zamas[c]] for c in selected_columns]
            col_names = selected_columns
            vwlj__hek = vwlj__hek if vwlj__hek in col_names else None
            partition_names = []
            twlmb__bxd = []
            fbo__fph = []
        vyrxq__rwi = None if isinstance(vwlj__hek, dict
            ) or vwlj__hek is None else vwlj__hek
        index_column_index = None
        index_column_type = types.none
        if vyrxq__rwi:
            xxqgk__gttx = col_names.index(vyrxq__rwi)
            index_column_index = col_indices.pop(xxqgk__gttx)
            index_column_type = voui__hryrd.pop(xxqgk__gttx)
            col_names.pop(xxqgk__gttx)
        for rkx__olxj, c in enumerate(col_names):
            if c in zkrit__iqh:
                voui__hryrd[rkx__olxj] = zkrit__iqh[c]
        mqu__vvlok = [ir.Var(xtel__rojmb, mk_unique_var('pq_table'),
            ifo__fwhp), ir.Var(xtel__rojmb, mk_unique_var('pq_index'),
            ifo__fwhp)]
        jqju__sjnvn = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.
            name, col_names, col_indices, voui__hryrd, mqu__vvlok,
            ifo__fwhp, partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, twlmb__bxd, fbo__fph)]
        return (col_names, mqu__vvlok, vwlj__hek, jqju__sjnvn, voui__hryrd,
            index_column_type)


def determine_filter_cast(pq_node, typemap, filter_val, orig_colname_map):
    vnko__moz = filter_val[0]
    cci__sqd = pq_node.original_out_types[orig_colname_map[vnko__moz]]
    yryr__ygbne = bodo.utils.typing.element_type(cci__sqd)
    if vnko__moz in pq_node.partition_names:
        if yryr__ygbne == types.unicode_type:
            atlmu__dukct = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(yryr__ygbne, types.Integer):
            atlmu__dukct = f'.cast(pyarrow.{yryr__ygbne.name}(), safe=False)'
        else:
            atlmu__dukct = ''
    else:
        atlmu__dukct = ''
    jdgqu__yvbrc = typemap[filter_val[2].name]
    if isinstance(jdgqu__yvbrc, (types.List, types.Set)):
        nfaw__bkn = jdgqu__yvbrc.dtype
    else:
        nfaw__bkn = jdgqu__yvbrc
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(yryr__ygbne,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(nfaw__bkn,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([yryr__ygbne, nfaw__bkn]):
        if not bodo.utils.typing.is_safe_arrow_cast(yryr__ygbne, nfaw__bkn):
            raise BodoError(
                f'Unsupported Arrow cast from {yryr__ygbne} to {nfaw__bkn} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if yryr__ygbne == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif yryr__ygbne in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(jdgqu__yvbrc, (types.List, types.Set)):
                yfv__xefoh = 'list' if isinstance(jdgqu__yvbrc, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {yfv__xefoh} values with isin filter pushdown.'
                    )
            return atlmu__dukct, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return atlmu__dukct, ''


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    wpqlg__rsyf = len(pq_node.out_vars)
    extra_args = ''
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    wlozl__seaxm, svy__cpf = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    if pq_node.filters:
        qjoqf__egko = []
        oie__kqj = []
        vtilv__pkky = False
        agbfg__gbu = None
        orig_colname_map = {c: rkx__olxj for rkx__olxj, c in enumerate(
            pq_node.original_df_colnames)}
        for kyrw__xti in pq_node.filters:
            hja__zftob = []
            kndf__tpjxp = []
            evsp__jvvm = set()
            for jlty__gdsm in kyrw__xti:
                if isinstance(jlty__gdsm[2], ir.Var):
                    urj__sits, zio__ecdf = determine_filter_cast(pq_node,
                        typemap, jlty__gdsm, orig_colname_map)
                    if jlty__gdsm[1] == 'in':
                        kndf__tpjxp.append(
                            f"(ds.field('{jlty__gdsm[0]}').isin({wlozl__seaxm[jlty__gdsm[2].name]}))"
                            )
                    else:
                        kndf__tpjxp.append(
                            f"(ds.field('{jlty__gdsm[0]}'){urj__sits} {jlty__gdsm[1]} ds.scalar({wlozl__seaxm[jlty__gdsm[2].name]}){zio__ecdf})"
                            )
                else:
                    assert jlty__gdsm[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if jlty__gdsm[1] == 'is not':
                        prefix = '~'
                    else:
                        prefix = ''
                    kndf__tpjxp.append(
                        f"({prefix}ds.field('{jlty__gdsm[0]}').is_null())")
                if jlty__gdsm[0] in pq_node.partition_names and isinstance(
                    jlty__gdsm[2], ir.Var):
                    aqgrs__ozz = (
                        f"('{jlty__gdsm[0]}', '{jlty__gdsm[1]}', {wlozl__seaxm[jlty__gdsm[2].name]})"
                        )
                    hja__zftob.append(aqgrs__ozz)
                    evsp__jvvm.add(aqgrs__ozz)
                else:
                    vtilv__pkky = True
            if agbfg__gbu is None:
                agbfg__gbu = evsp__jvvm
            else:
                agbfg__gbu.intersection_update(evsp__jvvm)
            sez__wdvub = ', '.join(hja__zftob)
            grabk__itv = ' & '.join(kndf__tpjxp)
            if sez__wdvub:
                qjoqf__egko.append(f'[{sez__wdvub}]')
            oie__kqj.append(f'({grabk__itv})')
        zkn__cwa = ', '.join(qjoqf__egko)
        cpzw__ymfb = ' | '.join(oie__kqj)
        if vtilv__pkky:
            if agbfg__gbu:
                dit__tpza = sorted(agbfg__gbu)
                dnf_filter_str = f"[[{', '.join(dit__tpza)}]]"
        elif zkn__cwa:
            dnf_filter_str = f'[{zkn__cwa}]'
        expr_filter_str = f'({cpzw__ymfb})'
        extra_args = ', '.join(wlozl__seaxm.values())
    hefyn__swu = ', '.join(f'out{rkx__olxj}' for rkx__olxj in range(
        wpqlg__rsyf))
    ztfp__utsbg = f'def pq_impl(fname, {extra_args}):\n'
    ztfp__utsbg += (
        f'    (total_rows, {hefyn__swu},) = _pq_reader_py(fname, {extra_args})\n'
        )
    tfrj__drc = {}
    exec(ztfp__utsbg, {}, tfrj__drc)
    hms__brff = tfrj__drc['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        zso__lpnsl = pq_node.loc.strformat()
        jrsd__mlb = []
        tty__hfa = []
        for rkx__olxj in pq_node.type_usecol_offset:
            vnko__moz = pq_node.df_colnames[rkx__olxj]
            jrsd__mlb.append(vnko__moz)
            if isinstance(pq_node.out_types[rkx__olxj], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                tty__hfa.append(vnko__moz)
        imv__yhbh = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', imv__yhbh,
            zso__lpnsl, jrsd__mlb)
        if tty__hfa:
            vlt__fgl = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', vlt__fgl,
                zso__lpnsl, tty__hfa)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        gyb__qjk = set(pq_node.type_usecol_offset)
        pzft__ojr = set(pq_node.unsupported_columns)
        ume__jcu = gyb__qjk & pzft__ojr
        if ume__jcu:
            npsp__hic = sorted(ume__jcu)
            jfqk__pblvv = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            ewt__msxpq = 0
            for ldfpk__gzc in npsp__hic:
                while pq_node.unsupported_columns[ewt__msxpq] != ldfpk__gzc:
                    ewt__msxpq += 1
                jfqk__pblvv.append(
                    f"Column '{pq_node.df_colnames[ldfpk__gzc]}' with unsupported arrow type {pq_node.unsupported_arrow_types[ewt__msxpq]}"
                    )
                ewt__msxpq += 1
            vihj__qpt = '\n'.join(jfqk__pblvv)
            raise BodoError(vihj__qpt, loc=pq_node.loc)
    gwv__fqe = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.type_usecol_offset, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    zarku__cqmd = typemap[pq_node.file_name.name]
    lmg__rfq = (zarku__cqmd,) + tuple(typemap[jlty__gdsm.name] for
        jlty__gdsm in svy__cpf)
    cwb__qrubg = compile_to_numba_ir(hms__brff, {'_pq_reader_py': gwv__fqe},
        typingctx=typingctx, targetctx=targetctx, arg_typs=lmg__rfq,
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(cwb__qrubg, [pq_node.file_name] + svy__cpf)
    jqju__sjnvn = cwb__qrubg.body[:-3]
    if meta_head_only_info:
        jqju__sjnvn[-1 - wpqlg__rsyf].target = meta_head_only_info[1]
    jqju__sjnvn[-2].target = pq_node.out_vars[0]
    jqju__sjnvn[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        jqju__sjnvn.pop(-1)
    elif not pq_node.type_usecol_offset:
        jqju__sjnvn.pop(-2)
    return jqju__sjnvn


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    iwkgd__uovd = get_overload_const_str(dnf_filter_str)
    zepsk__yjh = get_overload_const_str(expr_filter_str)
    jqjib__pqvu = ', '.join(f'f{rkx__olxj}' for rkx__olxj in range(len(
        var_tup)))
    ztfp__utsbg = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        ztfp__utsbg += f'  {jqjib__pqvu}, = var_tup\n'
    ztfp__utsbg += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    ztfp__utsbg += f'    dnf_filters_py = {iwkgd__uovd}\n'
    ztfp__utsbg += f'    expr_filters_py = {zepsk__yjh}\n'
    ztfp__utsbg += '  return (dnf_filters_py, expr_filters_py)\n'
    tfrj__drc = {}
    exec(ztfp__utsbg, globals(), tfrj__drc)
    return tfrj__drc['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    jlqef__doja = next_label()
    gjpk__fvsrv = ',' if extra_args else ''
    ztfp__utsbg = f'def pq_reader_py(fname,{extra_args}):\n'
    ztfp__utsbg += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    ztfp__utsbg += f"    ev.add_attribute('g_fname', fname)\n"
    ztfp__utsbg += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    ztfp__utsbg += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{gjpk__fvsrv}))
"""
    ztfp__utsbg += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    ztfp__utsbg += f"""    storage_options_py = get_storage_options_pyobject({str(storage_options)})
"""
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    yollb__hkhqb = not type_usecol_offset
    stc__mbg = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    czfg__iaft = {c: rkx__olxj for rkx__olxj, c in enumerate(col_indices)}
    xgvge__uete = {c: rkx__olxj for rkx__olxj, c in enumerate(stc__mbg)}
    petqh__haq = []
    ifbaq__xxp = set()
    kak__muax = partition_names + [input_file_name_col]
    for rkx__olxj in type_usecol_offset:
        if stc__mbg[rkx__olxj] not in kak__muax:
            petqh__haq.append(col_indices[rkx__olxj])
        elif not input_file_name_col or stc__mbg[rkx__olxj
            ] != input_file_name_col:
            ifbaq__xxp.add(col_indices[rkx__olxj])
    if index_column_index is not None:
        petqh__haq.append(index_column_index)
    petqh__haq = sorted(petqh__haq)
    rgjhd__hfc = {c: rkx__olxj for rkx__olxj, c in enumerate(petqh__haq)}

    def is_nullable(typ):
        return bodo.utils.utils.is_array_typ(typ, False) and (not
            isinstance(typ, types.Array) and not isinstance(typ, bodo.
            DatetimeArrayType))
    vgw__cyk = [(int(is_nullable(out_types[czfg__iaft[jzydc__lcws]])) if 
        jzydc__lcws != index_column_index else int(is_nullable(
        index_column_type))) for jzydc__lcws in petqh__haq]
    str_as_dict_cols = []
    for jzydc__lcws in petqh__haq:
        if jzydc__lcws == index_column_index:
            gehjz__ybcse = index_column_type
        else:
            gehjz__ybcse = out_types[czfg__iaft[jzydc__lcws]]
        if gehjz__ybcse == dict_str_arr_type:
            str_as_dict_cols.append(jzydc__lcws)
    atcb__amyzh = []
    gll__uwf = {}
    bjd__evim = []
    kyth__nto = []
    for rkx__olxj, imma__hxuwo in enumerate(partition_names):
        try:
            kom__zhu = xgvge__uete[imma__hxuwo]
            if col_indices[kom__zhu] not in ifbaq__xxp:
                continue
        except (KeyError, ValueError) as qchoe__qlz:
            continue
        gll__uwf[imma__hxuwo] = len(atcb__amyzh)
        atcb__amyzh.append(imma__hxuwo)
        bjd__evim.append(rkx__olxj)
        sova__fpfol = out_types[kom__zhu].dtype
        lruxp__kpum = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            sova__fpfol)
        kyth__nto.append(numba_to_c_type(lruxp__kpum))
    ztfp__utsbg += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    ztfp__utsbg += f'    out_table = pq_read(\n'
    ztfp__utsbg += f'        fname_py, {is_parallel},\n'
    ztfp__utsbg += f'        unicode_to_utf8(bucket_region),\n'
    ztfp__utsbg += f'        dnf_filters, expr_filters,\n'
    ztfp__utsbg += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{jlqef__doja}.ctypes,
"""
    ztfp__utsbg += f'        {len(petqh__haq)},\n'
    ztfp__utsbg += f'        nullable_cols_arr_{jlqef__doja}.ctypes,\n'
    if len(bjd__evim) > 0:
        ztfp__utsbg += (
            f'        np.array({bjd__evim}, dtype=np.int32).ctypes,\n')
        ztfp__utsbg += (
            f'        np.array({kyth__nto}, dtype=np.int32).ctypes,\n')
        ztfp__utsbg += f'        {len(bjd__evim)},\n'
    else:
        ztfp__utsbg += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        ztfp__utsbg += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        ztfp__utsbg += f'        0, 0,\n'
    ztfp__utsbg += f'        total_rows_np.ctypes,\n'
    ztfp__utsbg += f'        {input_file_name_col is not None},\n'
    ztfp__utsbg += f'    )\n'
    ztfp__utsbg += f'    check_and_propagate_cpp_exception()\n'
    xtl__pokfp = 'None'
    hucdd__wqtt = index_column_type
    nbui__awfmn = TableType(tuple(out_types))
    if yollb__hkhqb:
        nbui__awfmn = types.none
    if index_column_index is not None:
        krru__xfhs = rgjhd__hfc[index_column_index]
        xtl__pokfp = (
            f'info_to_array(info_from_table(out_table, {krru__xfhs}), index_arr_type)'
            )
    ztfp__utsbg += f'    index_arr = {xtl__pokfp}\n'
    if yollb__hkhqb:
        pgrpy__ugq = None
    else:
        pgrpy__ugq = []
        oyjvc__bxqr = 0
        tabur__sukoo = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for rkx__olxj, ldfpk__gzc in enumerate(col_indices):
            if oyjvc__bxqr < len(type_usecol_offset
                ) and rkx__olxj == type_usecol_offset[oyjvc__bxqr]:
                jgozb__beiz = col_indices[rkx__olxj]
                if tabur__sukoo and jgozb__beiz == tabur__sukoo:
                    pgrpy__ugq.append(len(petqh__haq) + len(atcb__amyzh))
                elif jgozb__beiz in ifbaq__xxp:
                    egfp__fzxf = stc__mbg[rkx__olxj]
                    pgrpy__ugq.append(len(petqh__haq) + gll__uwf[egfp__fzxf])
                else:
                    pgrpy__ugq.append(rgjhd__hfc[ldfpk__gzc])
                oyjvc__bxqr += 1
            else:
                pgrpy__ugq.append(-1)
        pgrpy__ugq = np.array(pgrpy__ugq, dtype=np.int64)
    if yollb__hkhqb:
        ztfp__utsbg += '    T = None\n'
    else:
        ztfp__utsbg += f"""    T = cpp_table_to_py_table(out_table, table_idx_{jlqef__doja}, py_table_type_{jlqef__doja})
"""
    ztfp__utsbg += f'    delete_table(out_table)\n'
    ztfp__utsbg += f'    total_rows = total_rows_np[0]\n'
    ztfp__utsbg += f'    ev.finalize()\n'
    ztfp__utsbg += f'    return (total_rows, T, index_arr)\n'
    tfrj__drc = {}
    uux__icocl = {f'py_table_type_{jlqef__doja}': nbui__awfmn,
        f'table_idx_{jlqef__doja}': pgrpy__ugq,
        f'selected_cols_arr_{jlqef__doja}': np.array(petqh__haq, np.int32),
        f'nullable_cols_arr_{jlqef__doja}': np.array(vgw__cyk, np.int32),
        'index_arr_type': hucdd__wqtt, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(ztfp__utsbg, uux__icocl, tfrj__drc)
    gwv__fqe = tfrj__drc['pq_reader_py']
    nffgy__ogy = numba.njit(gwv__fqe, no_cpython_wrapper=True)
    return nffgy__ogy


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    zbb__tmstx = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in zbb__tmstx:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        rvh__avv = pa_ts_typ.to_pandas_dtype().tz
        rtdkn__xvjxx = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            rvh__avv)
        return bodo.DatetimeArrayType(rtdkn__xvjxx), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        ndiv__cyqlp, akf__vwy = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(ndiv__cyqlp), akf__vwy
    if isinstance(pa_typ.type, pa.StructType):
        dar__qxp = []
        xhfvx__fgdh = []
        akf__vwy = True
        for zqebk__exqyw in pa_typ.flatten():
            xhfvx__fgdh.append(zqebk__exqyw.name.split('.')[-1])
            pktgq__qzba, rzz__uukc = _get_numba_typ_from_pa_typ(zqebk__exqyw,
                is_index, nullable_from_metadata, category_info)
            dar__qxp.append(pktgq__qzba)
            akf__vwy = akf__vwy and rzz__uukc
        return StructArrayType(tuple(dar__qxp), tuple(xhfvx__fgdh)), akf__vwy
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
        mtzfu__utij = _pa_numba_typ_map[pa_typ.type.index_type]
        lztf__pydh = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=mtzfu__utij)
        return CategoricalArrayType(lztf__pydh), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        jadqa__xoxwz = _pa_numba_typ_map[pa_typ.type]
        akf__vwy = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if jadqa__xoxwz == datetime_date_type:
        return datetime_date_array_type, akf__vwy
    if jadqa__xoxwz == bytes_type:
        return binary_array_type, akf__vwy
    ndiv__cyqlp = (string_array_type if jadqa__xoxwz == string_type else
        types.Array(jadqa__xoxwz, 1, 'C'))
    if jadqa__xoxwz == types.bool_:
        ndiv__cyqlp = boolean_array
    if nullable_from_metadata is not None:
        pzo__jin = nullable_from_metadata
    else:
        pzo__jin = use_nullable_int_arr
    if pzo__jin and not is_index and isinstance(jadqa__xoxwz, types.Integer
        ) and pa_typ.nullable:
        ndiv__cyqlp = IntegerArrayType(jadqa__xoxwz)
    return ndiv__cyqlp, akf__vwy


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None):
    if get_row_counts:
        rgiht__rhxu = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    ywp__uaco = MPI.COMM_WORLD
    if isinstance(fpath, list):
        vakwp__fvt = urlparse(fpath[0])
        protocol = vakwp__fvt.scheme
        pbfj__gms = vakwp__fvt.netloc
        for rkx__olxj in range(len(fpath)):
            wjbzm__chys = fpath[rkx__olxj]
            ayer__xnjk = urlparse(wjbzm__chys)
            if ayer__xnjk.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if ayer__xnjk.netloc != pbfj__gms:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[rkx__olxj] = wjbzm__chys.rstrip('/')
    else:
        vakwp__fvt = urlparse(fpath)
        protocol = vakwp__fvt.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as qchoe__qlz:
            wxz__oows = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(wxz__oows)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as qchoe__qlz:
            wxz__oows = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            wqrr__kyalo = gcsfs.GCSFileSystem(token=None)
            fs.append(wqrr__kyalo)
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
                prefix = f'{protocol}://{vakwp__fvt.netloc}'
                path = path[len(prefix):]
            qljp__dvna = fs.glob(path)
            if protocol == 's3':
                qljp__dvna = [('s3://' + wjbzm__chys) for wjbzm__chys in
                    qljp__dvna if not wjbzm__chys.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                qljp__dvna = [(prefix + wjbzm__chys) for wjbzm__chys in
                    qljp__dvna]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(qljp__dvna) == 0:
            raise BodoError('No files found matching glob pattern')
        return qljp__dvna
    uin__zfro = False
    if get_row_counts:
        hjib__oyfx = getfs(parallel=True)
        uin__zfro = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        xwp__smlj = 1
        lzu__pjtt = os.cpu_count()
        if lzu__pjtt is not None and lzu__pjtt > 1:
            xwp__smlj = lzu__pjtt // 2
        try:
            if get_row_counts:
                oslh__kndyv = tracing.Event('pq.ParquetDataset',
                    is_parallel=False)
                if tracing.is_tracing():
                    oslh__kndyv.add_attribute('g_dnf_filter', str(dnf_filters))
            pocs__xscmt = pa.io_thread_count()
            pa.set_io_thread_count(xwp__smlj)
            if isinstance(fpath, list):
                ekvvw__rfa = []
                for lkoau__okfns in fpath:
                    if has_magic(lkoau__okfns):
                        ekvvw__rfa += glob(protocol, getfs(), lkoau__okfns)
                    else:
                        ekvvw__rfa.append(lkoau__okfns)
                fpath = ekvvw__rfa
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{vakwp__fvt.netloc}'
                if isinstance(fpath, list):
                    ndr__fupj = [wjbzm__chys[len(prefix):] for wjbzm__chys in
                        fpath]
                else:
                    ndr__fupj = fpath[len(prefix):]
            else:
                ndr__fupj = fpath
            ofw__ktt = pq.ParquetDataset(ndr__fupj, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=xwp__smlj)
            pa.set_io_thread_count(pocs__xscmt)
            emhr__zxqo = bodo.io.pa_parquet.get_dataset_schema(ofw__ktt)
            if dnf_filters:
                if get_row_counts:
                    oslh__kndyv.add_attribute('num_pieces_before_filter',
                        len(ofw__ktt.pieces))
                ssv__dow = time.time()
                ofw__ktt._filter(dnf_filters)
                if get_row_counts:
                    oslh__kndyv.add_attribute('dnf_filter_time', time.time(
                        ) - ssv__dow)
                    oslh__kndyv.add_attribute('num_pieces_after_filter',
                        len(ofw__ktt.pieces))
            if get_row_counts:
                oslh__kndyv.finalize()
            ofw__ktt._metadata.fs = None
        except Exception as pssve__dub:
            if isinstance(fpath, list) and isinstance(pssve__dub, (OSError,
                FileNotFoundError)):
                pssve__dub = BodoError(str(pssve__dub) +
                    list_of_files_error_msg)
            else:
                pssve__dub = BodoError(
                    f"""error from pyarrow: {type(pssve__dub).__name__}: {str(pssve__dub)}
"""
                    )
            ywp__uaco.bcast(pssve__dub)
            raise pssve__dub
        if get_row_counts:
            ueph__uyev = tracing.Event('bcast dataset')
        ywp__uaco.bcast(ofw__ktt)
        ywp__uaco.bcast(emhr__zxqo)
    else:
        if get_row_counts:
            ueph__uyev = tracing.Event('bcast dataset')
        ofw__ktt = ywp__uaco.bcast(None)
        if isinstance(ofw__ktt, Exception):
            qlyn__vtj = ofw__ktt
            raise qlyn__vtj
        emhr__zxqo = ywp__uaco.bcast(None)
    if get_row_counts:
        xgmfm__tem = getfs()
    else:
        xgmfm__tem = get_legacy_fs()
    ofw__ktt._metadata.fs = xgmfm__tem
    if get_row_counts:
        ueph__uyev.finalize()
    ofw__ktt._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = uin__zfro = False
        for lkoau__okfns in ofw__ktt.pieces:
            lkoau__okfns._bodo_num_rows = 0
    if get_row_counts or uin__zfro:
        if get_row_counts and tracing.is_tracing():
            cdnx__wluol = tracing.Event('get_row_counts')
            cdnx__wluol.add_attribute('g_num_pieces', len(ofw__ktt.pieces))
            cdnx__wluol.add_attribute('g_expr_filters', str(expr_filters))
        xvez__ggb = 0.0
        num_pieces = len(ofw__ktt.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        rdkd__fhuw = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        vgfb__tede = 0
        izjxi__fst = 0
        mvron__ikj = 0
        ktw__yfucd = True
        if expr_filters is not None:
            import random
            random.seed(37)
            hrkmt__dmy = random.sample(ofw__ktt.pieces, k=len(ofw__ktt.pieces))
        else:
            hrkmt__dmy = ofw__ktt.pieces
        for lkoau__okfns in hrkmt__dmy:
            lkoau__okfns._bodo_num_rows = 0
        fpaths = [lkoau__okfns.path for lkoau__okfns in hrkmt__dmy[start:
            rdkd__fhuw]]
        if protocol == 's3':
            pbfj__gms = vakwp__fvt.netloc
            prefix = 's3://' + pbfj__gms + '/'
            fpaths = [wjbzm__chys[len(prefix):] for wjbzm__chys in fpaths]
            xgmfm__tem = get_s3_subtree_fs(pbfj__gms, region=getfs().region,
                storage_options=storage_options)
        else:
            xgmfm__tem = getfs()
        xwp__smlj = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(xwp__smlj)
        pa.set_cpu_count(xwp__smlj)
        qlyn__vtj = None
        try:
            xix__shm = ds.dataset(fpaths, filesystem=xgmfm__tem,
                partitioning=ds.partitioning(flavor='hive'))
            for jmprd__oqvgn, xytcy__npxyb in zip(hrkmt__dmy[start:
                rdkd__fhuw], xix__shm.get_fragments()):
                ssv__dow = time.time()
                eud__wfu = xytcy__npxyb.scanner(schema=xix__shm.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                xvez__ggb += time.time() - ssv__dow
                jmprd__oqvgn._bodo_num_rows = eud__wfu
                vgfb__tede += eud__wfu
                izjxi__fst += xytcy__npxyb.num_row_groups
                mvron__ikj += sum(epm__xwikg.total_byte_size for epm__xwikg in
                    xytcy__npxyb.row_groups)
                if uin__zfro:
                    ord__qhbzt = xytcy__npxyb.metadata.schema.to_arrow_schema()
                    if emhr__zxqo != ord__qhbzt:
                        print(
                            'Schema in {!s} was different. \n{!s}\n\nvs\n\n{!s}'
                            .format(jmprd__oqvgn, ord__qhbzt, emhr__zxqo))
                        ktw__yfucd = False
                        break
        except Exception as pssve__dub:
            qlyn__vtj = pssve__dub
        if ywp__uaco.allreduce(qlyn__vtj is not None, op=MPI.LOR):
            for qlyn__vtj in ywp__uaco.allgather(qlyn__vtj):
                if qlyn__vtj:
                    if isinstance(fpath, list) and isinstance(qlyn__vtj, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(qlyn__vtj) +
                            list_of_files_error_msg)
                    raise qlyn__vtj
        if uin__zfro:
            ktw__yfucd = ywp__uaco.allreduce(ktw__yfucd, op=MPI.LAND)
            if not ktw__yfucd:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            ofw__ktt._bodo_total_rows = ywp__uaco.allreduce(vgfb__tede, op=
                MPI.SUM)
            quo__xdxi = ywp__uaco.allreduce(izjxi__fst, op=MPI.SUM)
            pxp__tzy = ywp__uaco.allreduce(mvron__ikj, op=MPI.SUM)
            fuijj__eiw = np.array([lkoau__okfns._bodo_num_rows for
                lkoau__okfns in ofw__ktt.pieces])
            fuijj__eiw = ywp__uaco.allreduce(fuijj__eiw, op=MPI.SUM)
            for lkoau__okfns, xyv__iuip in zip(ofw__ktt.pieces, fuijj__eiw):
                lkoau__okfns._bodo_num_rows = xyv__iuip
            if is_parallel and bodo.get_rank(
                ) == 0 and quo__xdxi < bodo.get_size() and quo__xdxi != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({quo__xdxi}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()})
"""
                    ))
            if quo__xdxi == 0:
                fqsm__jqsol = 0
            else:
                fqsm__jqsol = pxp__tzy // quo__xdxi
            if (bodo.get_rank() == 0 and pxp__tzy >= 20 * 1048576 and 
                fqsm__jqsol < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({fqsm__jqsol} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                cdnx__wluol.add_attribute('g_total_num_row_groups', quo__xdxi)
                cdnx__wluol.add_attribute('total_scan_time', xvez__ggb)
                use__bqqgu = np.array([lkoau__okfns._bodo_num_rows for
                    lkoau__okfns in ofw__ktt.pieces])
                ihhv__fkwco = np.percentile(use__bqqgu, [25, 50, 75])
                cdnx__wluol.add_attribute('g_row_counts_min', use__bqqgu.min())
                cdnx__wluol.add_attribute('g_row_counts_Q1', ihhv__fkwco[0])
                cdnx__wluol.add_attribute('g_row_counts_median', ihhv__fkwco[1]
                    )
                cdnx__wluol.add_attribute('g_row_counts_Q3', ihhv__fkwco[2])
                cdnx__wluol.add_attribute('g_row_counts_max', use__bqqgu.max())
                cdnx__wluol.add_attribute('g_row_counts_mean', use__bqqgu.
                    mean())
                cdnx__wluol.add_attribute('g_row_counts_std', use__bqqgu.std())
                cdnx__wluol.add_attribute('g_row_counts_sum', use__bqqgu.sum())
                cdnx__wluol.finalize()
    ofw__ktt._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{vakwp__fvt.netloc}'
        if len(ofw__ktt.pieces) > 0:
            jmprd__oqvgn = ofw__ktt.pieces[0]
            if not jmprd__oqvgn.path.startswith(prefix):
                ofw__ktt._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(ofw__ktt)
    if get_row_counts:
        rgiht__rhxu.finalize()
    return ofw__ktt


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read):
    import pyarrow as pa
    lzu__pjtt = os.cpu_count()
    if lzu__pjtt is None or lzu__pjtt == 0:
        lzu__pjtt = 2
    hfy__ogep = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), lzu__pjtt)
    snncg__qbku = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), lzu__pjtt
        )
    if is_parallel and len(fpaths) > snncg__qbku and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(snncg__qbku)
        pa.set_cpu_count(snncg__qbku)
    else:
        pa.set_io_thread_count(hfy__ogep)
        pa.set_cpu_count(hfy__ogep)
    if fpaths[0].startswith('s3://'):
        pbfj__gms = urlparse(fpaths[0]).netloc
        prefix = 's3://' + pbfj__gms + '/'
        fpaths = [wjbzm__chys[len(prefix):] for wjbzm__chys in fpaths]
        xgmfm__tem = get_s3_subtree_fs(pbfj__gms, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        xgmfm__tem = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        xgmfm__tem = gcsfs.GCSFileSystem(token=None)
    else:
        xgmfm__tem = None
    brgn__gjm = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    ofw__ktt = ds.dataset(fpaths, filesystem=xgmfm__tem, partitioning=ds.
        partitioning(flavor='hive'), format=brgn__gjm)
    col_names = ofw__ktt.schema.names
    ivb__jjl = [col_names[yys__jgr] for yys__jgr in selected_fields]
    mcomf__mzxp = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if mcomf__mzxp and expr_filters is None:
        mxh__uzac = []
        bsd__rszrc = 0
        fjeu__swyk = 0
        for xytcy__npxyb in ofw__ktt.get_fragments():
            mmx__hxwu = []
            for epm__xwikg in xytcy__npxyb.row_groups:
                vqt__xlupu = epm__xwikg.num_rows
                if start_offset < bsd__rszrc + vqt__xlupu:
                    if fjeu__swyk == 0:
                        frnbe__hxbua = start_offset - bsd__rszrc
                        qvr__dcof = min(vqt__xlupu - frnbe__hxbua, rows_to_read
                            )
                    else:
                        qvr__dcof = min(vqt__xlupu, rows_to_read - fjeu__swyk)
                    fjeu__swyk += qvr__dcof
                    mmx__hxwu.append(epm__xwikg.id)
                bsd__rszrc += vqt__xlupu
                if fjeu__swyk == rows_to_read:
                    break
            mxh__uzac.append(xytcy__npxyb.subset(row_group_ids=mmx__hxwu))
            if fjeu__swyk == rows_to_read:
                break
        ofw__ktt = ds.FileSystemDataset(mxh__uzac, ofw__ktt.schema,
            brgn__gjm, filesystem=ofw__ktt.filesystem)
        start_offset = frnbe__hxbua
    tmg__gkos = ofw__ktt.scanner(columns=ivb__jjl, filter=expr_filters,
        use_threads=True).to_reader()
    return ofw__ktt, tmg__gkos, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    aqvtz__tnlr = [c for c in pa_schema.names if isinstance(pa_schema.field
        (c).type, pa.DictionaryType)]
    if len(aqvtz__tnlr) == 0:
        pq_dataset._category_info = {}
        return
    ywp__uaco = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            byl__smj = pq_dataset.pieces[0].open()
            epm__xwikg = byl__smj.read_row_group(0, aqvtz__tnlr)
            category_info = {c: tuple(epm__xwikg.column(c).chunk(0).
                dictionary.to_pylist()) for c in aqvtz__tnlr}
            del byl__smj, epm__xwikg
        except Exception as pssve__dub:
            ywp__uaco.bcast(pssve__dub)
            raise pssve__dub
        ywp__uaco.bcast(category_info)
    else:
        category_info = ywp__uaco.bcast(None)
        if isinstance(category_info, Exception):
            qlyn__vtj = category_info
            raise qlyn__vtj
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    vwlj__hek = None
    nullable_from_metadata = defaultdict(lambda : None)
    ggss__wpn = b'pandas'
    if schema.metadata is not None and ggss__wpn in schema.metadata:
        import json
        uoslf__hkia = json.loads(schema.metadata[ggss__wpn].decode('utf8'))
        enan__lcwt = len(uoslf__hkia['index_columns'])
        if enan__lcwt > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        vwlj__hek = uoslf__hkia['index_columns'][0] if enan__lcwt else None
        if not isinstance(vwlj__hek, str) and (not isinstance(vwlj__hek,
            dict) or num_pieces != 1):
            vwlj__hek = None
        for jcwv__yrub in uoslf__hkia['columns']:
            qey__womdn = jcwv__yrub['name']
            if jcwv__yrub['pandas_type'].startswith('int'
                ) and qey__womdn is not None:
                if jcwv__yrub['numpy_type'].startswith('Int'):
                    nullable_from_metadata[qey__womdn] = True
                else:
                    nullable_from_metadata[qey__womdn] = False
    return vwlj__hek, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for qey__womdn in pa_schema.names:
        zqebk__exqyw = pa_schema.field(qey__womdn)
        if zqebk__exqyw.type == pa.string():
            str_columns.append(qey__womdn)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    ywp__uaco = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        hrkmt__dmy = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        hrkmt__dmy = pq_dataset.pieces
    wwtk__smh = np.zeros(len(str_columns), dtype=np.int64)
    ofi__hpb = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(hrkmt__dmy):
        jmprd__oqvgn = hrkmt__dmy[bodo.get_rank()]
        try:
            zlps__gkn = jmprd__oqvgn.get_metadata()
            for rkx__olxj in range(zlps__gkn.num_row_groups):
                for oyjvc__bxqr, qey__womdn in enumerate(str_columns):
                    ewt__msxpq = pa_schema.get_field_index(qey__womdn)
                    wwtk__smh[oyjvc__bxqr] += zlps__gkn.row_group(rkx__olxj
                        ).column(ewt__msxpq).total_uncompressed_size
            lvfjn__mrw = zlps__gkn.num_rows
        except Exception as pssve__dub:
            if isinstance(pssve__dub, (OSError, FileNotFoundError)):
                lvfjn__mrw = 0
            else:
                raise
    else:
        lvfjn__mrw = 0
    eqse__viao = ywp__uaco.allreduce(lvfjn__mrw, op=MPI.SUM)
    if eqse__viao == 0:
        return set()
    ywp__uaco.Allreduce(wwtk__smh, ofi__hpb, op=MPI.SUM)
    hwlz__myn = ofi__hpb / eqse__viao
    str_as_dict = set()
    for rkx__olxj, xsr__fgrx in enumerate(hwlz__myn):
        if xsr__fgrx < READ_STR_AS_DICT_THRESHOLD:
            qey__womdn = str_columns[rkx__olxj][0]
            str_as_dict.add(qey__womdn)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    voui__hryrd = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[rkx__olxj].name for rkx__olxj in range(len(
        pq_dataset.partitions.partition_names))]
    pa_schema = pq_dataset.schema.to_arrow_schema()
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    bzngz__rgpov = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    azqrz__cqi = read_as_dict_cols - bzngz__rgpov
    if len(azqrz__cqi) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {azqrz__cqi}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(bzngz__rgpov)
    bzngz__rgpov = bzngz__rgpov - read_as_dict_cols
    str_columns = [zvuil__tcvvj for zvuil__tcvvj in str_columns if 
        zvuil__tcvvj in bzngz__rgpov]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    vwlj__hek, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    tsg__zcz = []
    ljy__dgmn = []
    tjr__pgqm = []
    for rkx__olxj, c in enumerate(col_names):
        zqebk__exqyw = pa_schema.field(c)
        jadqa__xoxwz, akf__vwy = _get_numba_typ_from_pa_typ(zqebk__exqyw, c ==
            vwlj__hek, nullable_from_metadata[c], pq_dataset._category_info,
            str_as_dict=c in str_as_dict)
        tsg__zcz.append(jadqa__xoxwz)
        ljy__dgmn.append(akf__vwy)
        tjr__pgqm.append(zqebk__exqyw.type)
    if partition_names:
        col_names += partition_names
        tsg__zcz += [_get_partition_cat_dtype(pq_dataset.partitions.levels[
            rkx__olxj]) for rkx__olxj in range(len(partition_names))]
        ljy__dgmn.extend([True] * len(partition_names))
        tjr__pgqm.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        tsg__zcz += [dict_str_arr_type]
        ljy__dgmn.append(True)
        tjr__pgqm.append(None)
    fcj__jpfjh = {c: rkx__olxj for rkx__olxj, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in fcj__jpfjh:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if vwlj__hek and not isinstance(vwlj__hek, dict
        ) and vwlj__hek not in selected_columns:
        selected_columns.append(vwlj__hek)
    col_names = selected_columns
    col_indices = []
    voui__hryrd = []
    twlmb__bxd = []
    fbo__fph = []
    for rkx__olxj, c in enumerate(col_names):
        jgozb__beiz = fcj__jpfjh[c]
        col_indices.append(jgozb__beiz)
        voui__hryrd.append(tsg__zcz[jgozb__beiz])
        if not ljy__dgmn[jgozb__beiz]:
            twlmb__bxd.append(rkx__olxj)
            fbo__fph.append(tjr__pgqm[jgozb__beiz])
    return (col_names, voui__hryrd, vwlj__hek, col_indices, partition_names,
        twlmb__bxd, fbo__fph)


def _get_partition_cat_dtype(part_set):
    qzubd__szg = part_set.dictionary.to_pandas()
    rru__waa = bodo.typeof(qzubd__szg).dtype
    lztf__pydh = PDCategoricalDtype(tuple(qzubd__szg), rru__waa, False)
    return CategoricalArrayType(lztf__pydh)


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
        gcb__sluc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        vaa__oqo = cgutils.get_or_insert_function(builder.module, gcb__sluc,
            name='pq_write')
        builder.call(vaa__oqo, args)
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
        gcb__sluc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        vaa__oqo = cgutils.get_or_insert_function(builder.module, gcb__sluc,
            name='pq_write_partitioned')
        builder.call(vaa__oqo, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
