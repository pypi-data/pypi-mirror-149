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
        except OSError as mal__pbudo:
            if 'non-file path' in str(mal__pbudo):
                raise FileNotFoundError(str(mal__pbudo))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        oyp__gnscf = lhs.scope
        svbio__cxsc = lhs.loc
        jrm__mbso = None
        if lhs.name in self.locals:
            jrm__mbso = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        oophw__hurg = {}
        if lhs.name + ':convert' in self.locals:
            oophw__hurg = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if jrm__mbso is None:
            omwo__bfa = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/file_io.html#non-constant-filepaths'
                )
            btzz__ghas = get_const_value(file_name, self.func_ir, omwo__bfa,
                arg_types=self.args, file_info=ParquetFileInfo(columns,
                storage_options=storage_options, input_file_name_col=
                input_file_name_col, read_as_dict_cols=read_as_dict_cols))
            hhfh__lgk = False
            nkzc__ppgfq = guard(get_definition, self.func_ir, file_name)
            if isinstance(nkzc__ppgfq, ir.Arg):
                typ = self.args[nkzc__ppgfq.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, fpcwj__qcg, phoo__owg, col_indices,
                        partition_names, ztsah__saye, povgt__naow) = typ.schema
                    hhfh__lgk = True
            if not hhfh__lgk:
                (col_names, fpcwj__qcg, phoo__owg, col_indices,
                    partition_names, ztsah__saye, povgt__naow) = (
                    parquet_file_schema(btzz__ghas, columns,
                    storage_options=storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            wvze__qujv = list(jrm__mbso.keys())
            xcu__sgsl = {c: bvi__fpba for bvi__fpba, c in enumerate(wvze__qujv)
                }
            gqjsn__rgd = [xlht__teu for xlht__teu in jrm__mbso.values()]
            phoo__owg = 'index' if 'index' in xcu__sgsl else None
            if columns is None:
                selected_columns = wvze__qujv
            else:
                selected_columns = columns
            col_indices = [xcu__sgsl[c] for c in selected_columns]
            fpcwj__qcg = [gqjsn__rgd[xcu__sgsl[c]] for c in selected_columns]
            col_names = selected_columns
            phoo__owg = phoo__owg if phoo__owg in col_names else None
            partition_names = []
            ztsah__saye = []
            povgt__naow = []
        hjp__vqcqi = None if isinstance(phoo__owg, dict
            ) or phoo__owg is None else phoo__owg
        index_column_index = None
        index_column_type = types.none
        if hjp__vqcqi:
            myyra__aihfi = col_names.index(hjp__vqcqi)
            index_column_index = col_indices.pop(myyra__aihfi)
            index_column_type = fpcwj__qcg.pop(myyra__aihfi)
            col_names.pop(myyra__aihfi)
        for bvi__fpba, c in enumerate(col_names):
            if c in oophw__hurg:
                fpcwj__qcg[bvi__fpba] = oophw__hurg[c]
        boshp__dyyge = [ir.Var(oyp__gnscf, mk_unique_var('pq_table'),
            svbio__cxsc), ir.Var(oyp__gnscf, mk_unique_var('pq_index'),
            svbio__cxsc)]
        mmrnj__ydwx = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.
            name, col_names, col_indices, fpcwj__qcg, boshp__dyyge,
            svbio__cxsc, partition_names, storage_options,
            index_column_index, index_column_type, input_file_name_col,
            ztsah__saye, povgt__naow)]
        return (col_names, boshp__dyyge, phoo__owg, mmrnj__ydwx, fpcwj__qcg,
            index_column_type)


def determine_filter_cast(pq_node, typemap, filter_val, orig_colname_map):
    aey__noawi = filter_val[0]
    lpl__znrg = pq_node.original_out_types[orig_colname_map[aey__noawi]]
    pxv__upz = bodo.utils.typing.element_type(lpl__znrg)
    if aey__noawi in pq_node.partition_names:
        if pxv__upz == types.unicode_type:
            fxb__xvs = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(pxv__upz, types.Integer):
            fxb__xvs = f'.cast(pyarrow.{pxv__upz.name}(), safe=False)'
        else:
            fxb__xvs = ''
    else:
        fxb__xvs = ''
    ghr__xogbt = typemap[filter_val[2].name]
    if isinstance(ghr__xogbt, (types.List, types.Set)):
        xll__dbne = ghr__xogbt.dtype
    else:
        xll__dbne = ghr__xogbt
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(pxv__upz,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(xll__dbne,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([pxv__upz, xll__dbne]):
        if not bodo.utils.typing.is_safe_arrow_cast(pxv__upz, xll__dbne):
            raise BodoError(
                f'Unsupported Arrow cast from {pxv__upz} to {xll__dbne} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if pxv__upz == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif pxv__upz in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(ghr__xogbt, (types.List, types.Set)):
                liyd__vxfuw = 'list' if isinstance(ghr__xogbt, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {liyd__vxfuw} values with isin filter pushdown.'
                    )
            return fxb__xvs, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return fxb__xvs, ''


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    ufk__tpjls = len(pq_node.out_vars)
    extra_args = ''
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    rmx__notxn, roegt__asely = bodo.ir.connector.generate_filter_map(pq_node
        .filters)
    if pq_node.filters:
        klkox__ltrvz = []
        mnqm__auqec = []
        wodnu__tceq = False
        eff__ium = None
        orig_colname_map = {c: bvi__fpba for bvi__fpba, c in enumerate(
            pq_node.original_df_colnames)}
        for kgqnp__lnit in pq_node.filters:
            qdca__clzl = []
            ieyvr__wlal = []
            zhso__nkny = set()
            for uffj__kvxbn in kgqnp__lnit:
                if isinstance(uffj__kvxbn[2], ir.Var):
                    pkjth__rqnq, oduwt__hlr = determine_filter_cast(pq_node,
                        typemap, uffj__kvxbn, orig_colname_map)
                    if uffj__kvxbn[1] == 'in':
                        ieyvr__wlal.append(
                            f"(ds.field('{uffj__kvxbn[0]}').isin({rmx__notxn[uffj__kvxbn[2].name]}))"
                            )
                    else:
                        ieyvr__wlal.append(
                            f"(ds.field('{uffj__kvxbn[0]}'){pkjth__rqnq} {uffj__kvxbn[1]} ds.scalar({rmx__notxn[uffj__kvxbn[2].name]}){oduwt__hlr})"
                            )
                else:
                    assert uffj__kvxbn[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if uffj__kvxbn[1] == 'is not':
                        prefix = '~'
                    else:
                        prefix = ''
                    ieyvr__wlal.append(
                        f"({prefix}ds.field('{uffj__kvxbn[0]}').is_null())")
                if uffj__kvxbn[0] in pq_node.partition_names and isinstance(
                    uffj__kvxbn[2], ir.Var):
                    lttel__qsnh = (
                        f"('{uffj__kvxbn[0]}', '{uffj__kvxbn[1]}', {rmx__notxn[uffj__kvxbn[2].name]})"
                        )
                    qdca__clzl.append(lttel__qsnh)
                    zhso__nkny.add(lttel__qsnh)
                else:
                    wodnu__tceq = True
            if eff__ium is None:
                eff__ium = zhso__nkny
            else:
                eff__ium.intersection_update(zhso__nkny)
            ozis__tnnw = ', '.join(qdca__clzl)
            bvacx__gqz = ' & '.join(ieyvr__wlal)
            if ozis__tnnw:
                klkox__ltrvz.append(f'[{ozis__tnnw}]')
            mnqm__auqec.append(f'({bvacx__gqz})')
        def__txkm = ', '.join(klkox__ltrvz)
        yge__tbua = ' | '.join(mnqm__auqec)
        if wodnu__tceq:
            if eff__ium:
                gym__vwx = sorted(eff__ium)
                dnf_filter_str = f"[[{', '.join(gym__vwx)}]]"
        elif def__txkm:
            dnf_filter_str = f'[{def__txkm}]'
        expr_filter_str = f'({yge__tbua})'
        extra_args = ', '.join(rmx__notxn.values())
    khx__vvtvk = ', '.join(f'out{bvi__fpba}' for bvi__fpba in range(ufk__tpjls)
        )
    ovqb__jjrfd = f'def pq_impl(fname, {extra_args}):\n'
    ovqb__jjrfd += (
        f'    (total_rows, {khx__vvtvk},) = _pq_reader_py(fname, {extra_args})\n'
        )
    cneaw__wog = {}
    exec(ovqb__jjrfd, {}, cneaw__wog)
    oow__xqchj = cneaw__wog['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        jwvwp__omorq = pq_node.loc.strformat()
        anlp__zsnmj = []
        kbz__wjou = []
        for bvi__fpba in pq_node.type_usecol_offset:
            aey__noawi = pq_node.df_colnames[bvi__fpba]
            anlp__zsnmj.append(aey__noawi)
            if isinstance(pq_node.out_types[bvi__fpba], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                kbz__wjou.append(aey__noawi)
        thft__jvyu = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', thft__jvyu,
            jwvwp__omorq, anlp__zsnmj)
        if kbz__wjou:
            rkd__iau = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', rkd__iau,
                jwvwp__omorq, kbz__wjou)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        cfz__rufn = set(pq_node.type_usecol_offset)
        kyfjx__dvnt = set(pq_node.unsupported_columns)
        vjax__usn = cfz__rufn & kyfjx__dvnt
        if vjax__usn:
            pem__dvzcm = sorted(vjax__usn)
            tvtb__yylo = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            pmawz__vbpf = 0
            for fapx__mwk in pem__dvzcm:
                while pq_node.unsupported_columns[pmawz__vbpf] != fapx__mwk:
                    pmawz__vbpf += 1
                tvtb__yylo.append(
                    f"Column '{pq_node.df_colnames[fapx__mwk]}' with unsupported arrow type {pq_node.unsupported_arrow_types[pmawz__vbpf]}"
                    )
                pmawz__vbpf += 1
            ctms__vlt = '\n'.join(tvtb__yylo)
            raise BodoError(ctms__vlt, loc=pq_node.loc)
    rbpfu__fgflt = _gen_pq_reader_py(pq_node.df_colnames, pq_node.
        col_indices, pq_node.type_usecol_offset, pq_node.out_types, pq_node
        .storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    nbz__lciht = typemap[pq_node.file_name.name]
    gnql__nem = (nbz__lciht,) + tuple(typemap[uffj__kvxbn.name] for
        uffj__kvxbn in roegt__asely)
    argqo__cpjk = compile_to_numba_ir(oow__xqchj, {'_pq_reader_py':
        rbpfu__fgflt}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        gnql__nem, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(argqo__cpjk, [pq_node.file_name] + roegt__asely)
    mmrnj__ydwx = argqo__cpjk.body[:-3]
    if meta_head_only_info:
        mmrnj__ydwx[-1 - ufk__tpjls].target = meta_head_only_info[1]
    mmrnj__ydwx[-2].target = pq_node.out_vars[0]
    mmrnj__ydwx[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        mmrnj__ydwx.pop(-1)
    elif not pq_node.type_usecol_offset:
        mmrnj__ydwx.pop(-2)
    return mmrnj__ydwx


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    apeo__pqept = get_overload_const_str(dnf_filter_str)
    tilz__djgde = get_overload_const_str(expr_filter_str)
    nbimy__kxwv = ', '.join(f'f{bvi__fpba}' for bvi__fpba in range(len(
        var_tup)))
    ovqb__jjrfd = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        ovqb__jjrfd += f'  {nbimy__kxwv}, = var_tup\n'
    ovqb__jjrfd += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    ovqb__jjrfd += f'    dnf_filters_py = {apeo__pqept}\n'
    ovqb__jjrfd += f'    expr_filters_py = {tilz__djgde}\n'
    ovqb__jjrfd += '  return (dnf_filters_py, expr_filters_py)\n'
    cneaw__wog = {}
    exec(ovqb__jjrfd, globals(), cneaw__wog)
    return cneaw__wog['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    hnegf__pvmxz = next_label()
    ymm__ntwqm = ',' if extra_args else ''
    ovqb__jjrfd = f'def pq_reader_py(fname,{extra_args}):\n'
    ovqb__jjrfd += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    ovqb__jjrfd += f"    ev.add_attribute('g_fname', fname)\n"
    ovqb__jjrfd += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    ovqb__jjrfd += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{ymm__ntwqm}))
"""
    ovqb__jjrfd += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    ovqb__jjrfd += f"""    storage_options_py = get_storage_options_pyobject({str(storage_options)})
"""
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    hufbd__oyzmz = not type_usecol_offset
    wwpq__fem = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    qmt__gwnb = {c: bvi__fpba for bvi__fpba, c in enumerate(col_indices)}
    duqzf__dlukm = {c: bvi__fpba for bvi__fpba, c in enumerate(wwpq__fem)}
    yuyfw__pcrf = []
    dbs__gthk = set()
    lammv__wrq = partition_names + [input_file_name_col]
    for bvi__fpba in type_usecol_offset:
        if wwpq__fem[bvi__fpba] not in lammv__wrq:
            yuyfw__pcrf.append(col_indices[bvi__fpba])
        elif not input_file_name_col or wwpq__fem[bvi__fpba
            ] != input_file_name_col:
            dbs__gthk.add(col_indices[bvi__fpba])
    if index_column_index is not None:
        yuyfw__pcrf.append(index_column_index)
    yuyfw__pcrf = sorted(yuyfw__pcrf)
    nsbrk__ogm = {c: bvi__fpba for bvi__fpba, c in enumerate(yuyfw__pcrf)}

    def is_nullable(typ):
        return bodo.utils.utils.is_array_typ(typ, False) and (not
            isinstance(typ, types.Array) and not isinstance(typ, bodo.
            DatetimeArrayType))
    fzmwo__rlhzg = [(int(is_nullable(out_types[qmt__gwnb[srfft__sxqgo]])) if
        srfft__sxqgo != index_column_index else int(is_nullable(
        index_column_type))) for srfft__sxqgo in yuyfw__pcrf]
    str_as_dict_cols = []
    for srfft__sxqgo in yuyfw__pcrf:
        if srfft__sxqgo == index_column_index:
            xlht__teu = index_column_type
        else:
            xlht__teu = out_types[qmt__gwnb[srfft__sxqgo]]
        if xlht__teu == dict_str_arr_type:
            str_as_dict_cols.append(srfft__sxqgo)
    zfomu__ple = []
    asws__dqjy = {}
    uwm__nlah = []
    kzez__cnvn = []
    for bvi__fpba, eer__qrdd in enumerate(partition_names):
        try:
            pnxu__scifl = duqzf__dlukm[eer__qrdd]
            if col_indices[pnxu__scifl] not in dbs__gthk:
                continue
        except (KeyError, ValueError) as abuj__rgcau:
            continue
        asws__dqjy[eer__qrdd] = len(zfomu__ple)
        zfomu__ple.append(eer__qrdd)
        uwm__nlah.append(bvi__fpba)
        zcv__hfw = out_types[pnxu__scifl].dtype
        kjzi__rdqyl = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            zcv__hfw)
        kzez__cnvn.append(numba_to_c_type(kjzi__rdqyl))
    ovqb__jjrfd += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    ovqb__jjrfd += f'    out_table = pq_read(\n'
    ovqb__jjrfd += f'        fname_py, {is_parallel},\n'
    ovqb__jjrfd += f'        unicode_to_utf8(bucket_region),\n'
    ovqb__jjrfd += f'        dnf_filters, expr_filters,\n'
    ovqb__jjrfd += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{hnegf__pvmxz}.ctypes,
"""
    ovqb__jjrfd += f'        {len(yuyfw__pcrf)},\n'
    ovqb__jjrfd += f'        nullable_cols_arr_{hnegf__pvmxz}.ctypes,\n'
    if len(uwm__nlah) > 0:
        ovqb__jjrfd += (
            f'        np.array({uwm__nlah}, dtype=np.int32).ctypes,\n')
        ovqb__jjrfd += (
            f'        np.array({kzez__cnvn}, dtype=np.int32).ctypes,\n')
        ovqb__jjrfd += f'        {len(uwm__nlah)},\n'
    else:
        ovqb__jjrfd += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        ovqb__jjrfd += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        ovqb__jjrfd += f'        0, 0,\n'
    ovqb__jjrfd += f'        total_rows_np.ctypes,\n'
    ovqb__jjrfd += f'        {input_file_name_col is not None},\n'
    ovqb__jjrfd += f'    )\n'
    ovqb__jjrfd += f'    check_and_propagate_cpp_exception()\n'
    ptrg__rjawr = 'None'
    qqyf__cffio = index_column_type
    nvtqy__arywm = TableType(tuple(out_types))
    if hufbd__oyzmz:
        nvtqy__arywm = types.none
    if index_column_index is not None:
        hczmt__pgbag = nsbrk__ogm[index_column_index]
        ptrg__rjawr = (
            f'info_to_array(info_from_table(out_table, {hczmt__pgbag}), index_arr_type)'
            )
    ovqb__jjrfd += f'    index_arr = {ptrg__rjawr}\n'
    if hufbd__oyzmz:
        smf__wjww = None
    else:
        smf__wjww = []
        bbube__bvqa = 0
        bpmip__gzdj = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for bvi__fpba, fapx__mwk in enumerate(col_indices):
            if bbube__bvqa < len(type_usecol_offset
                ) and bvi__fpba == type_usecol_offset[bbube__bvqa]:
                benia__qhrzq = col_indices[bvi__fpba]
                if bpmip__gzdj and benia__qhrzq == bpmip__gzdj:
                    smf__wjww.append(len(yuyfw__pcrf) + len(zfomu__ple))
                elif benia__qhrzq in dbs__gthk:
                    houu__tqmkk = wwpq__fem[bvi__fpba]
                    smf__wjww.append(len(yuyfw__pcrf) + asws__dqjy[houu__tqmkk]
                        )
                else:
                    smf__wjww.append(nsbrk__ogm[fapx__mwk])
                bbube__bvqa += 1
            else:
                smf__wjww.append(-1)
        smf__wjww = np.array(smf__wjww, dtype=np.int64)
    if hufbd__oyzmz:
        ovqb__jjrfd += '    T = None\n'
    else:
        ovqb__jjrfd += f"""    T = cpp_table_to_py_table(out_table, table_idx_{hnegf__pvmxz}, py_table_type_{hnegf__pvmxz})
"""
    ovqb__jjrfd += f'    delete_table(out_table)\n'
    ovqb__jjrfd += f'    total_rows = total_rows_np[0]\n'
    ovqb__jjrfd += f'    ev.finalize()\n'
    ovqb__jjrfd += f'    return (total_rows, T, index_arr)\n'
    cneaw__wog = {}
    wyt__qndp = {f'py_table_type_{hnegf__pvmxz}': nvtqy__arywm,
        f'table_idx_{hnegf__pvmxz}': smf__wjww,
        f'selected_cols_arr_{hnegf__pvmxz}': np.array(yuyfw__pcrf, np.int32
        ), f'nullable_cols_arr_{hnegf__pvmxz}': np.array(fzmwo__rlhzg, np.
        int32), 'index_arr_type': qqyf__cffio, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(ovqb__jjrfd, wyt__qndp, cneaw__wog)
    rbpfu__fgflt = cneaw__wog['pq_reader_py']
    umg__jcwjo = numba.njit(rbpfu__fgflt, no_cpython_wrapper=True)
    return umg__jcwjo


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    hvkjc__yzcz = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in hvkjc__yzcz:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        ocscc__bbtot = pa_ts_typ.to_pandas_dtype().tz
        yvjsb__sji = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            ocscc__bbtot)
        return bodo.DatetimeArrayType(yvjsb__sji), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        nwtm__zej, blw__gnc = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(nwtm__zej), blw__gnc
    if isinstance(pa_typ.type, pa.StructType):
        hgv__wwl = []
        wrpbk__alii = []
        blw__gnc = True
        for pvlt__nrqxv in pa_typ.flatten():
            wrpbk__alii.append(pvlt__nrqxv.name.split('.')[-1])
            nnvzn__upnc, sne__hpdjj = _get_numba_typ_from_pa_typ(pvlt__nrqxv,
                is_index, nullable_from_metadata, category_info)
            hgv__wwl.append(nnvzn__upnc)
            blw__gnc = blw__gnc and sne__hpdjj
        return StructArrayType(tuple(hgv__wwl), tuple(wrpbk__alii)), blw__gnc
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
        qkypl__gwwfi = _pa_numba_typ_map[pa_typ.type.index_type]
        izwzf__nots = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=qkypl__gwwfi)
        return CategoricalArrayType(izwzf__nots), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        fidui__hmkfs = _pa_numba_typ_map[pa_typ.type]
        blw__gnc = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if fidui__hmkfs == datetime_date_type:
        return datetime_date_array_type, blw__gnc
    if fidui__hmkfs == bytes_type:
        return binary_array_type, blw__gnc
    nwtm__zej = (string_array_type if fidui__hmkfs == string_type else
        types.Array(fidui__hmkfs, 1, 'C'))
    if fidui__hmkfs == types.bool_:
        nwtm__zej = boolean_array
    if nullable_from_metadata is not None:
        thscl__dhnsp = nullable_from_metadata
    else:
        thscl__dhnsp = use_nullable_int_arr
    if thscl__dhnsp and not is_index and isinstance(fidui__hmkfs, types.Integer
        ) and pa_typ.nullable:
        nwtm__zej = IntegerArrayType(fidui__hmkfs)
    return nwtm__zej, blw__gnc


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None):
    if get_row_counts:
        xiq__dovfb = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    nta__iyueg = MPI.COMM_WORLD
    if isinstance(fpath, list):
        ezdz__rpnq = urlparse(fpath[0])
        protocol = ezdz__rpnq.scheme
        tes__ycmne = ezdz__rpnq.netloc
        for bvi__fpba in range(len(fpath)):
            olbj__diqi = fpath[bvi__fpba]
            xjqwp__nvyxg = urlparse(olbj__diqi)
            if xjqwp__nvyxg.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if xjqwp__nvyxg.netloc != tes__ycmne:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[bvi__fpba] = olbj__diqi.rstrip('/')
    else:
        ezdz__rpnq = urlparse(fpath)
        protocol = ezdz__rpnq.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as abuj__rgcau:
            tyrr__lhc = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(tyrr__lhc)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as abuj__rgcau:
            tyrr__lhc = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            reja__meriz = gcsfs.GCSFileSystem(token=None)
            fs.append(reja__meriz)
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
                prefix = f'{protocol}://{ezdz__rpnq.netloc}'
                path = path[len(prefix):]
            xutg__bvdf = fs.glob(path)
            if protocol == 's3':
                xutg__bvdf = [('s3://' + olbj__diqi) for olbj__diqi in
                    xutg__bvdf if not olbj__diqi.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                xutg__bvdf = [(prefix + olbj__diqi) for olbj__diqi in
                    xutg__bvdf]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(xutg__bvdf) == 0:
            raise BodoError('No files found matching glob pattern')
        return xutg__bvdf
    zfdxd__pelts = False
    if get_row_counts:
        qgq__aucdc = getfs(parallel=True)
        zfdxd__pelts = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        asx__srvi = 1
        obdv__hcr = os.cpu_count()
        if obdv__hcr is not None and obdv__hcr > 1:
            asx__srvi = obdv__hcr // 2
        try:
            if get_row_counts:
                mzt__wtv = tracing.Event('pq.ParquetDataset', is_parallel=False
                    )
                if tracing.is_tracing():
                    mzt__wtv.add_attribute('g_dnf_filter', str(dnf_filters))
            idni__bryy = pa.io_thread_count()
            pa.set_io_thread_count(asx__srvi)
            if isinstance(fpath, list):
                csigy__gbfhs = []
                for xrmy__qswdy in fpath:
                    if has_magic(xrmy__qswdy):
                        csigy__gbfhs += glob(protocol, getfs(), xrmy__qswdy)
                    else:
                        csigy__gbfhs.append(xrmy__qswdy)
                fpath = csigy__gbfhs
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{ezdz__rpnq.netloc}'
                if isinstance(fpath, list):
                    jygzn__vgct = [olbj__diqi[len(prefix):] for olbj__diqi in
                        fpath]
                else:
                    jygzn__vgct = fpath[len(prefix):]
            else:
                jygzn__vgct = fpath
            wpvid__hyey = pq.ParquetDataset(jygzn__vgct, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=asx__srvi)
            pa.set_io_thread_count(idni__bryy)
            tpp__bqio = bodo.io.pa_parquet.get_dataset_schema(wpvid__hyey)
            if dnf_filters:
                if get_row_counts:
                    mzt__wtv.add_attribute('num_pieces_before_filter', len(
                        wpvid__hyey.pieces))
                gzc__cizmn = time.time()
                wpvid__hyey._filter(dnf_filters)
                if get_row_counts:
                    mzt__wtv.add_attribute('dnf_filter_time', time.time() -
                        gzc__cizmn)
                    mzt__wtv.add_attribute('num_pieces_after_filter', len(
                        wpvid__hyey.pieces))
            if get_row_counts:
                mzt__wtv.finalize()
            wpvid__hyey._metadata.fs = None
        except Exception as mal__pbudo:
            if isinstance(fpath, list) and isinstance(mal__pbudo, (OSError,
                FileNotFoundError)):
                mal__pbudo = BodoError(str(mal__pbudo) +
                    list_of_files_error_msg)
            else:
                mal__pbudo = BodoError(
                    f"""error from pyarrow: {type(mal__pbudo).__name__}: {str(mal__pbudo)}
"""
                    )
            nta__iyueg.bcast(mal__pbudo)
            raise mal__pbudo
        if get_row_counts:
            pbx__kzmxs = tracing.Event('bcast dataset')
        nta__iyueg.bcast(wpvid__hyey)
        nta__iyueg.bcast(tpp__bqio)
    else:
        if get_row_counts:
            pbx__kzmxs = tracing.Event('bcast dataset')
        wpvid__hyey = nta__iyueg.bcast(None)
        if isinstance(wpvid__hyey, Exception):
            ersl__uoah = wpvid__hyey
            raise ersl__uoah
        tpp__bqio = nta__iyueg.bcast(None)
    if get_row_counts:
        fnm__bep = getfs()
    else:
        fnm__bep = get_legacy_fs()
    wpvid__hyey._metadata.fs = fnm__bep
    if get_row_counts:
        pbx__kzmxs.finalize()
    wpvid__hyey._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = zfdxd__pelts = False
        for xrmy__qswdy in wpvid__hyey.pieces:
            xrmy__qswdy._bodo_num_rows = 0
    if get_row_counts or zfdxd__pelts:
        if get_row_counts and tracing.is_tracing():
            soww__xyha = tracing.Event('get_row_counts')
            soww__xyha.add_attribute('g_num_pieces', len(wpvid__hyey.pieces))
            soww__xyha.add_attribute('g_expr_filters', str(expr_filters))
        crm__ivmk = 0.0
        num_pieces = len(wpvid__hyey.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        cyw__aqbug = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        rbjju__oih = 0
        sckv__lsdm = 0
        lrkk__otcrx = 0
        bnz__qpg = True
        if expr_filters is not None:
            import random
            random.seed(37)
            json__vnasq = random.sample(wpvid__hyey.pieces, k=len(
                wpvid__hyey.pieces))
        else:
            json__vnasq = wpvid__hyey.pieces
        for xrmy__qswdy in json__vnasq:
            xrmy__qswdy._bodo_num_rows = 0
        fpaths = [xrmy__qswdy.path for xrmy__qswdy in json__vnasq[start:
            cyw__aqbug]]
        if protocol == 's3':
            tes__ycmne = ezdz__rpnq.netloc
            prefix = 's3://' + tes__ycmne + '/'
            fpaths = [olbj__diqi[len(prefix):] for olbj__diqi in fpaths]
            fnm__bep = get_s3_subtree_fs(tes__ycmne, region=getfs().region,
                storage_options=storage_options)
        else:
            fnm__bep = getfs()
        asx__srvi = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(asx__srvi)
        pa.set_cpu_count(asx__srvi)
        ersl__uoah = None
        try:
            rekch__zee = ds.dataset(fpaths, filesystem=fnm__bep,
                partitioning=ds.partitioning(flavor='hive'))
            for zku__lvcv, pjtyf__inl in zip(json__vnasq[start:cyw__aqbug],
                rekch__zee.get_fragments()):
                gzc__cizmn = time.time()
                ylwqg__kxaok = pjtyf__inl.scanner(schema=rekch__zee.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                crm__ivmk += time.time() - gzc__cizmn
                zku__lvcv._bodo_num_rows = ylwqg__kxaok
                rbjju__oih += ylwqg__kxaok
                sckv__lsdm += pjtyf__inl.num_row_groups
                lrkk__otcrx += sum(xfw__abqum.total_byte_size for
                    xfw__abqum in pjtyf__inl.row_groups)
                if zfdxd__pelts:
                    ffsu__pwwk = pjtyf__inl.metadata.schema.to_arrow_schema()
                    if tpp__bqio != ffsu__pwwk:
                        print(
                            'Schema in {!s} was different. \n{!s}\n\nvs\n\n{!s}'
                            .format(zku__lvcv, ffsu__pwwk, tpp__bqio))
                        bnz__qpg = False
                        break
        except Exception as mal__pbudo:
            ersl__uoah = mal__pbudo
        if nta__iyueg.allreduce(ersl__uoah is not None, op=MPI.LOR):
            for ersl__uoah in nta__iyueg.allgather(ersl__uoah):
                if ersl__uoah:
                    if isinstance(fpath, list) and isinstance(ersl__uoah, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(ersl__uoah) +
                            list_of_files_error_msg)
                    raise ersl__uoah
        if zfdxd__pelts:
            bnz__qpg = nta__iyueg.allreduce(bnz__qpg, op=MPI.LAND)
            if not bnz__qpg:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            wpvid__hyey._bodo_total_rows = nta__iyueg.allreduce(rbjju__oih,
                op=MPI.SUM)
            cwro__dybd = nta__iyueg.allreduce(sckv__lsdm, op=MPI.SUM)
            fflk__uyvj = nta__iyueg.allreduce(lrkk__otcrx, op=MPI.SUM)
            bnpr__ieni = np.array([xrmy__qswdy._bodo_num_rows for
                xrmy__qswdy in wpvid__hyey.pieces])
            bnpr__ieni = nta__iyueg.allreduce(bnpr__ieni, op=MPI.SUM)
            for xrmy__qswdy, woej__sbre in zip(wpvid__hyey.pieces, bnpr__ieni):
                xrmy__qswdy._bodo_num_rows = woej__sbre
            if is_parallel and bodo.get_rank(
                ) == 0 and cwro__dybd < bodo.get_size() and cwro__dybd != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({cwro__dybd}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()})
"""
                    ))
            if cwro__dybd == 0:
                omza__ufmhe = 0
            else:
                omza__ufmhe = fflk__uyvj // cwro__dybd
            if (bodo.get_rank() == 0 and fflk__uyvj >= 20 * 1048576 and 
                omza__ufmhe < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({omza__ufmhe} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                soww__xyha.add_attribute('g_total_num_row_groups', cwro__dybd)
                soww__xyha.add_attribute('total_scan_time', crm__ivmk)
                qcdaz__vuh = np.array([xrmy__qswdy._bodo_num_rows for
                    xrmy__qswdy in wpvid__hyey.pieces])
                mhq__pva = np.percentile(qcdaz__vuh, [25, 50, 75])
                soww__xyha.add_attribute('g_row_counts_min', qcdaz__vuh.min())
                soww__xyha.add_attribute('g_row_counts_Q1', mhq__pva[0])
                soww__xyha.add_attribute('g_row_counts_median', mhq__pva[1])
                soww__xyha.add_attribute('g_row_counts_Q3', mhq__pva[2])
                soww__xyha.add_attribute('g_row_counts_max', qcdaz__vuh.max())
                soww__xyha.add_attribute('g_row_counts_mean', qcdaz__vuh.mean()
                    )
                soww__xyha.add_attribute('g_row_counts_std', qcdaz__vuh.std())
                soww__xyha.add_attribute('g_row_counts_sum', qcdaz__vuh.sum())
                soww__xyha.finalize()
    wpvid__hyey._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{ezdz__rpnq.netloc}'
        if len(wpvid__hyey.pieces) > 0:
            zku__lvcv = wpvid__hyey.pieces[0]
            if not zku__lvcv.path.startswith(prefix):
                wpvid__hyey._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(wpvid__hyey)
    if get_row_counts:
        xiq__dovfb.finalize()
    return wpvid__hyey


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read):
    import pyarrow as pa
    obdv__hcr = os.cpu_count()
    if obdv__hcr is None or obdv__hcr == 0:
        obdv__hcr = 2
    tokcy__sie = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), obdv__hcr)
    rfcn__ucdka = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), obdv__hcr
        )
    if is_parallel and len(fpaths) > rfcn__ucdka and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(rfcn__ucdka)
        pa.set_cpu_count(rfcn__ucdka)
    else:
        pa.set_io_thread_count(tokcy__sie)
        pa.set_cpu_count(tokcy__sie)
    if fpaths[0].startswith('s3://'):
        tes__ycmne = urlparse(fpaths[0]).netloc
        prefix = 's3://' + tes__ycmne + '/'
        fpaths = [olbj__diqi[len(prefix):] for olbj__diqi in fpaths]
        fnm__bep = get_s3_subtree_fs(tes__ycmne, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        fnm__bep = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        fnm__bep = gcsfs.GCSFileSystem(token=None)
    else:
        fnm__bep = None
    ymwgf__uqfw = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    wpvid__hyey = ds.dataset(fpaths, filesystem=fnm__bep, partitioning=ds.
        partitioning(flavor='hive'), format=ymwgf__uqfw)
    col_names = wpvid__hyey.schema.names
    smn__aowva = [col_names[xlc__qnm] for xlc__qnm in selected_fields]
    vtzf__hvdli = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if vtzf__hvdli and expr_filters is None:
        vib__czr = []
        blaz__kyxoc = 0
        pftb__lts = 0
        for pjtyf__inl in wpvid__hyey.get_fragments():
            uvsa__jchu = []
            for xfw__abqum in pjtyf__inl.row_groups:
                tlp__obokv = xfw__abqum.num_rows
                if start_offset < blaz__kyxoc + tlp__obokv:
                    if pftb__lts == 0:
                        hhfy__udr = start_offset - blaz__kyxoc
                        gux__kqgk = min(tlp__obokv - hhfy__udr, rows_to_read)
                    else:
                        gux__kqgk = min(tlp__obokv, rows_to_read - pftb__lts)
                    pftb__lts += gux__kqgk
                    uvsa__jchu.append(xfw__abqum.id)
                blaz__kyxoc += tlp__obokv
                if pftb__lts == rows_to_read:
                    break
            vib__czr.append(pjtyf__inl.subset(row_group_ids=uvsa__jchu))
            if pftb__lts == rows_to_read:
                break
        wpvid__hyey = ds.FileSystemDataset(vib__czr, wpvid__hyey.schema,
            ymwgf__uqfw, filesystem=wpvid__hyey.filesystem)
        start_offset = hhfy__udr
    rhh__tvu = wpvid__hyey.scanner(columns=smn__aowva, filter=expr_filters,
        use_threads=True).to_reader()
    return wpvid__hyey, rhh__tvu, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    qotlf__fvq = [c for c in pa_schema.names if isinstance(pa_schema.field(
        c).type, pa.DictionaryType)]
    if len(qotlf__fvq) == 0:
        pq_dataset._category_info = {}
        return
    nta__iyueg = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            lloee__wrksy = pq_dataset.pieces[0].open()
            xfw__abqum = lloee__wrksy.read_row_group(0, qotlf__fvq)
            category_info = {c: tuple(xfw__abqum.column(c).chunk(0).
                dictionary.to_pylist()) for c in qotlf__fvq}
            del lloee__wrksy, xfw__abqum
        except Exception as mal__pbudo:
            nta__iyueg.bcast(mal__pbudo)
            raise mal__pbudo
        nta__iyueg.bcast(category_info)
    else:
        category_info = nta__iyueg.bcast(None)
        if isinstance(category_info, Exception):
            ersl__uoah = category_info
            raise ersl__uoah
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    phoo__owg = None
    nullable_from_metadata = defaultdict(lambda : None)
    yiuok__doyjp = b'pandas'
    if schema.metadata is not None and yiuok__doyjp in schema.metadata:
        import json
        nvv__nks = json.loads(schema.metadata[yiuok__doyjp].decode('utf8'))
        usmgd__mjegx = len(nvv__nks['index_columns'])
        if usmgd__mjegx > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        phoo__owg = nvv__nks['index_columns'][0] if usmgd__mjegx else None
        if not isinstance(phoo__owg, str) and (not isinstance(phoo__owg,
            dict) or num_pieces != 1):
            phoo__owg = None
        for pykt__blb in nvv__nks['columns']:
            eoeca__sjdyn = pykt__blb['name']
            if pykt__blb['pandas_type'].startswith('int'
                ) and eoeca__sjdyn is not None:
                if pykt__blb['numpy_type'].startswith('Int'):
                    nullable_from_metadata[eoeca__sjdyn] = True
                else:
                    nullable_from_metadata[eoeca__sjdyn] = False
    return phoo__owg, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for eoeca__sjdyn in pa_schema.names:
        pvlt__nrqxv = pa_schema.field(eoeca__sjdyn)
        if pvlt__nrqxv.type == pa.string():
            str_columns.append(eoeca__sjdyn)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    nta__iyueg = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        json__vnasq = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        json__vnasq = pq_dataset.pieces
    jagg__ymw = np.zeros(len(str_columns), dtype=np.int64)
    abp__hpi = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(json__vnasq):
        zku__lvcv = json__vnasq[bodo.get_rank()]
        try:
            smnd__ixpf = zku__lvcv.get_metadata()
            for bvi__fpba in range(smnd__ixpf.num_row_groups):
                for bbube__bvqa, eoeca__sjdyn in enumerate(str_columns):
                    pmawz__vbpf = pa_schema.get_field_index(eoeca__sjdyn)
                    jagg__ymw[bbube__bvqa] += smnd__ixpf.row_group(bvi__fpba
                        ).column(pmawz__vbpf).total_uncompressed_size
            rnh__grbr = smnd__ixpf.num_rows
        except Exception as mal__pbudo:
            if isinstance(mal__pbudo, (OSError, FileNotFoundError)):
                rnh__grbr = 0
            else:
                raise
    else:
        rnh__grbr = 0
    ldz__cpcnn = nta__iyueg.allreduce(rnh__grbr, op=MPI.SUM)
    if ldz__cpcnn == 0:
        return set()
    nta__iyueg.Allreduce(jagg__ymw, abp__hpi, op=MPI.SUM)
    hbgl__kflp = abp__hpi / ldz__cpcnn
    str_as_dict = set()
    for bvi__fpba, nmr__aghy in enumerate(hbgl__kflp):
        if nmr__aghy < READ_STR_AS_DICT_THRESHOLD:
            eoeca__sjdyn = str_columns[bvi__fpba][0]
            str_as_dict.add(eoeca__sjdyn)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    fpcwj__qcg = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[bvi__fpba].name for bvi__fpba in range(len(
        pq_dataset.partitions.partition_names))]
    pa_schema = pq_dataset.schema.to_arrow_schema()
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    majru__iel = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    nfzm__adgdp = read_as_dict_cols - majru__iel
    if len(nfzm__adgdp) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {nfzm__adgdp}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(majru__iel)
    majru__iel = majru__iel - read_as_dict_cols
    str_columns = [puu__imi for puu__imi in str_columns if puu__imi in
        majru__iel]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    phoo__owg, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    gqjsn__rgd = []
    prjz__nzvfp = []
    dzq__reutv = []
    for bvi__fpba, c in enumerate(col_names):
        pvlt__nrqxv = pa_schema.field(c)
        fidui__hmkfs, blw__gnc = _get_numba_typ_from_pa_typ(pvlt__nrqxv, c ==
            phoo__owg, nullable_from_metadata[c], pq_dataset._category_info,
            str_as_dict=c in str_as_dict)
        gqjsn__rgd.append(fidui__hmkfs)
        prjz__nzvfp.append(blw__gnc)
        dzq__reutv.append(pvlt__nrqxv.type)
    if partition_names:
        col_names += partition_names
        gqjsn__rgd += [_get_partition_cat_dtype(pq_dataset.partitions.
            levels[bvi__fpba]) for bvi__fpba in range(len(partition_names))]
        prjz__nzvfp.extend([True] * len(partition_names))
        dzq__reutv.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        gqjsn__rgd += [dict_str_arr_type]
        prjz__nzvfp.append(True)
        dzq__reutv.append(None)
    fev__yfctn = {c: bvi__fpba for bvi__fpba, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in fev__yfctn:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if phoo__owg and not isinstance(phoo__owg, dict
        ) and phoo__owg not in selected_columns:
        selected_columns.append(phoo__owg)
    col_names = selected_columns
    col_indices = []
    fpcwj__qcg = []
    ztsah__saye = []
    povgt__naow = []
    for bvi__fpba, c in enumerate(col_names):
        benia__qhrzq = fev__yfctn[c]
        col_indices.append(benia__qhrzq)
        fpcwj__qcg.append(gqjsn__rgd[benia__qhrzq])
        if not prjz__nzvfp[benia__qhrzq]:
            ztsah__saye.append(bvi__fpba)
            povgt__naow.append(dzq__reutv[benia__qhrzq])
    return (col_names, fpcwj__qcg, phoo__owg, col_indices, partition_names,
        ztsah__saye, povgt__naow)


def _get_partition_cat_dtype(part_set):
    jqsl__wht = part_set.dictionary.to_pandas()
    judww__wnx = bodo.typeof(jqsl__wht).dtype
    izwzf__nots = PDCategoricalDtype(tuple(jqsl__wht), judww__wnx, False)
    return CategoricalArrayType(izwzf__nots)


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
        kkis__kros = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        lfwrb__elpbe = cgutils.get_or_insert_function(builder.module,
            kkis__kros, name='pq_write')
        builder.call(lfwrb__elpbe, args)
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
        kkis__kros = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        lfwrb__elpbe = cgutils.get_or_insert_function(builder.module,
            kkis__kros, name='pq_write_partitioned')
        builder.call(lfwrb__elpbe, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
