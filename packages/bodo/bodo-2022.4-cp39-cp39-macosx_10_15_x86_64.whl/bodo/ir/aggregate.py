"""IR node for the groupby, pivot and cross_tabulation"""
import ctypes
import operator
import types as pytypes
from collections import defaultdict, namedtuple
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, compiler, ir, ir_utils, types
from numba.core.analysis import compute_use_defs
from numba.core.ir_utils import build_definitions, compile_to_numba_ir, find_callname, find_const, find_topo_order, get_definition, get_ir_of_code, get_name_var_table, guard, is_getitem, mk_unique_var, next_label, remove_dels, replace_arg_nodes, replace_var_names, replace_vars_inner, visit_vars_inner
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin
from numba.parfors.parfor import Parfor, unwrap_parfor_blocks, wrap_parfor_blocks
import bodo
from bodo.hiframes.datetime_date_ext import DatetimeDateArrayType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, groupby_and_aggregate, info_from_table, info_to_array, pivot_groupby_and_aggregate
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, pre_alloc_array_item_array
from bodo.libs.binary_arr_ext import BinaryArrayType, pre_alloc_binary_array
from bodo.libs.bool_arr_ext import BooleanArrayType
from bodo.libs.decimal_arr_ext import DecimalArrayType, alloc_decimal_array
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.transform import get_call_expr_arg
from bodo.utils.typing import BodoError, decode_if_dict_array, get_literal_value, get_overload_const_func, get_overload_const_str, get_overload_constant_dict, is_overload_constant_dict, is_overload_constant_str, list_cumulative, to_str_arr_if_dict_array
from bodo.utils.utils import debug_prints, incref, is_assign, is_call_assign, is_expr, is_null_pointer, is_var_assign, sanitize_varname, unliteral_all
gb_agg_cfunc = {}
gb_agg_cfunc_addr = {}


@intrinsic
def add_agg_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        sig = func.signature
        if sig == types.none(types.voidptr):
            xud__jjmg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            tqan__ztys = cgutils.get_or_insert_function(builder.module,
                xud__jjmg, sym._literal_value)
            builder.call(tqan__ztys, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            xud__jjmg = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            tqan__ztys = cgutils.get_or_insert_function(builder.module,
                xud__jjmg, sym._literal_value)
            builder.call(tqan__ztys, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            xud__jjmg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            tqan__ztys = cgutils.get_or_insert_function(builder.module,
                xud__jjmg, sym._literal_value)
            builder.call(tqan__ztys, [context.get_constant_null(sig.args[0]
                ), context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        context.add_linking_libs([gb_agg_cfunc[sym._literal_value]._library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_agg_udf_addr(name):
    with numba.objmode(addr='int64'):
        addr = gb_agg_cfunc_addr[name]
    return addr


class AggUDFStruct(object):

    def __init__(self, regular_udf_funcs=None, general_udf_funcs=None):
        assert regular_udf_funcs is not None or general_udf_funcs is not None
        self.regular_udfs = False
        self.general_udfs = False
        self.regular_udf_cfuncs = None
        self.general_udf_cfunc = None
        if regular_udf_funcs is not None:
            (self.var_typs, self.init_func, self.update_all_func, self.
                combine_all_func, self.eval_all_func) = regular_udf_funcs
            self.regular_udfs = True
        if general_udf_funcs is not None:
            self.general_udf_funcs = general_udf_funcs
            self.general_udfs = True

    def set_regular_cfuncs(self, update_cb, combine_cb, eval_cb):
        assert self.regular_udfs and self.regular_udf_cfuncs is None
        self.regular_udf_cfuncs = [update_cb, combine_cb, eval_cb]

    def set_general_cfunc(self, general_udf_cb):
        assert self.general_udfs and self.general_udf_cfunc is None
        self.general_udf_cfunc = general_udf_cb


AggFuncStruct = namedtuple('AggFuncStruct', ['func', 'ftype'])
supported_agg_funcs = ['no_op', 'head', 'transform', 'size', 'shift', 'sum',
    'count', 'nunique', 'median', 'cumsum', 'cumprod', 'cummin', 'cummax',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'idxmin', 'idxmax',
    'var', 'std', 'udf', 'gen_udf']
supported_transform_funcs = ['no_op', 'sum', 'count', 'nunique', 'median',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'var', 'std']


def get_agg_func(func_ir, func_name, rhs, series_type=None, typemap=None):
    if func_name == 'no_op':
        raise BodoError('Unknown aggregation function used in groupby.')
    if series_type is None:
        series_type = SeriesType(types.float64)
    if func_name in {'var', 'std'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 3
        func.ncols_post_shuffle = 4
        return func
    if func_name in {'first', 'last'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        return func
    if func_name in {'idxmin', 'idxmax'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 2
        func.ncols_post_shuffle = 2
        return func
    if func_name in supported_agg_funcs[:-8]:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        xoifx__ethj = True
        maxfb__tjzgc = 1
        yknmh__efzs = -1
        if isinstance(rhs, ir.Expr):
            for dcb__gcyj in rhs.kws:
                if func_name in list_cumulative:
                    if dcb__gcyj[0] == 'skipna':
                        xoifx__ethj = guard(find_const, func_ir, dcb__gcyj[1])
                        if not isinstance(xoifx__ethj, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if dcb__gcyj[0] == 'dropna':
                        xoifx__ethj = guard(find_const, func_ir, dcb__gcyj[1])
                        if not isinstance(xoifx__ethj, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            maxfb__tjzgc = get_call_expr_arg('shift', rhs.args, dict(rhs.
                kws), 0, 'periods', maxfb__tjzgc)
            maxfb__tjzgc = guard(find_const, func_ir, maxfb__tjzgc)
        if func_name == 'head':
            yknmh__efzs = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(yknmh__efzs, int):
                yknmh__efzs = guard(find_const, func_ir, yknmh__efzs)
            if yknmh__efzs < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = xoifx__ethj
        func.periods = maxfb__tjzgc
        func.head_n = yknmh__efzs
        if func_name == 'transform':
            kws = dict(rhs.kws)
            qkbf__mvk = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            clpd__ofhbp = typemap[qkbf__mvk.name]
            pbrr__nfu = None
            if isinstance(clpd__ofhbp, str):
                pbrr__nfu = clpd__ofhbp
            elif is_overload_constant_str(clpd__ofhbp):
                pbrr__nfu = get_overload_const_str(clpd__ofhbp)
            elif bodo.utils.typing.is_builtin_function(clpd__ofhbp):
                pbrr__nfu = bodo.utils.typing.get_builtin_function_name(
                    clpd__ofhbp)
            if pbrr__nfu not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {pbrr__nfu}')
            func.transform_func = supported_agg_funcs.index(pbrr__nfu)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    qkbf__mvk = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if qkbf__mvk == '':
        clpd__ofhbp = types.none
    else:
        clpd__ofhbp = typemap[qkbf__mvk.name]
    if is_overload_constant_dict(clpd__ofhbp):
        jeh__vuij = get_overload_constant_dict(clpd__ofhbp)
        taad__akaz = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in jeh__vuij.values()]
        return taad__akaz
    if clpd__ofhbp == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(clpd__ofhbp, types.BaseTuple):
        taad__akaz = []
        hwpwe__rxo = 0
        for t in clpd__ofhbp.types:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                taad__akaz.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>':
                    func.fname = '<lambda_' + str(hwpwe__rxo) + '>'
                    hwpwe__rxo += 1
                taad__akaz.append(func)
        return [taad__akaz]
    if is_overload_constant_str(clpd__ofhbp):
        func_name = get_overload_const_str(clpd__ofhbp)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(clpd__ofhbp):
        func_name = bodo.utils.typing.get_builtin_function_name(clpd__ofhbp)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    assert typemap is not None, 'typemap is required for agg UDF handling'
    func = _get_const_agg_func(typemap[rhs.args[0].name], func_ir)
    func.ftype = 'udf'
    func.fname = _get_udf_name(func)
    return func


def get_agg_func_udf(func_ir, f_val, rhs, series_type, typemap):
    if isinstance(f_val, str):
        return get_agg_func(func_ir, f_val, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(f_val):
        func_name = bodo.utils.typing.get_builtin_function_name(f_val)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if isinstance(f_val, (tuple, list)):
        hwpwe__rxo = 0
        lyd__llvh = []
        for omprp__sbzb in f_val:
            func = get_agg_func_udf(func_ir, omprp__sbzb, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{hwpwe__rxo}>'
                hwpwe__rxo += 1
            lyd__llvh.append(func)
        return lyd__llvh
    else:
        assert is_expr(f_val, 'make_function') or isinstance(f_val, (numba.
            core.registry.CPUDispatcher, types.Dispatcher))
        assert typemap is not None, 'typemap is required for agg UDF handling'
        func = _get_const_agg_func(f_val, func_ir)
        func.ftype = 'udf'
        func.fname = _get_udf_name(func)
        return func


def _get_udf_name(func):
    code = func.code if hasattr(func, 'code') else func.__code__
    pbrr__nfu = code.co_name
    return pbrr__nfu


def _get_const_agg_func(func_typ, func_ir):
    agg_func = get_overload_const_func(func_typ, func_ir)
    if is_expr(agg_func, 'make_function'):

        def agg_func_wrapper(A):
            return A
        agg_func_wrapper.__code__ = agg_func.code
        agg_func = agg_func_wrapper
        return agg_func
    return agg_func


@infer_global(type)
class TypeDt64(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if len(args) == 1 and isinstance(args[0], (types.NPDatetime, types.
            NPTimedelta)):
            drlqx__lxigv = types.DType(args[0])
            return signature(drlqx__lxigv, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    tmm__yvxg = nobs_a + nobs_b
    gmtqx__njncs = (nobs_a * mean_a + nobs_b * mean_b) / tmm__yvxg
    zysf__pjrd = mean_b - mean_a
    jvnwk__pzms = (ssqdm_a + ssqdm_b + zysf__pjrd * zysf__pjrd * nobs_a *
        nobs_b / tmm__yvxg)
    return jvnwk__pzms, gmtqx__njncs, tmm__yvxg


def __special_combine(*args):
    return


@infer_global(__special_combine)
class SpecialCombineTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *unliteral_all(args))


@lower_builtin(__special_combine, types.VarArg(types.Any))
def lower_special_combine(context, builder, sig, args):
    return context.get_dummy_value()


class Aggregate(ir.Stmt):

    def __init__(self, df_out, df_in, key_names, gb_info_in, gb_info_out,
        out_key_vars, df_out_vars, df_in_vars, key_arrs, input_has_index,
        same_index, return_key, loc, func_name, dropna=True, pivot_arr=None,
        pivot_values=None, is_crosstab=False):
        self.df_out = df_out
        self.df_in = df_in
        self.key_names = key_names
        self.gb_info_in = gb_info_in
        self.gb_info_out = gb_info_out
        self.out_key_vars = out_key_vars
        self.df_out_vars = df_out_vars
        self.df_in_vars = df_in_vars
        self.key_arrs = key_arrs
        self.input_has_index = input_has_index
        self.same_index = same_index
        self.return_key = return_key
        self.loc = loc
        self.func_name = func_name
        self.dropna = dropna
        self.pivot_arr = pivot_arr
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab

    def __repr__(self):
        nchr__uuanm = ''
        for lpjwo__ublnd, brxni__qzbdc in self.df_out_vars.items():
            nchr__uuanm += "'{}':{}, ".format(lpjwo__ublnd, brxni__qzbdc.name)
        pxyv__xwqi = '{}{{{}}}'.format(self.df_out, nchr__uuanm)
        optl__bctzs = ''
        for lpjwo__ublnd, brxni__qzbdc in self.df_in_vars.items():
            optl__bctzs += "'{}':{}, ".format(lpjwo__ublnd, brxni__qzbdc.name)
        aqevb__fxw = '{}{{{}}}'.format(self.df_in, optl__bctzs)
        gwsw__oze = 'pivot {}:{}'.format(self.pivot_arr.name, self.pivot_values
            ) if self.pivot_arr is not None else ''
        key_names = ','.join(self.key_names)
        ijjf__newh = ','.join([brxni__qzbdc.name for brxni__qzbdc in self.
            key_arrs])
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(pxyv__xwqi,
            aqevb__fxw, key_names, ijjf__newh, gwsw__oze)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        fxfno__nyp, ruu__uko = self.gb_info_out.pop(out_col_name)
        if fxfno__nyp is None and not self.is_crosstab:
            return
        ztefm__dzzj = self.gb_info_in[fxfno__nyp]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for nwkj__idpa, (func, nchr__uuanm) in enumerate(ztefm__dzzj):
                try:
                    nchr__uuanm.remove(out_col_name)
                    if len(nchr__uuanm) == 0:
                        ztefm__dzzj.pop(nwkj__idpa)
                        break
                except ValueError as nmes__hgpwf:
                    continue
        else:
            for nwkj__idpa, (func, ugo__not) in enumerate(ztefm__dzzj):
                if ugo__not == out_col_name:
                    ztefm__dzzj.pop(nwkj__idpa)
                    break
        if len(ztefm__dzzj) == 0:
            self.gb_info_in.pop(fxfno__nyp)
            self.df_in_vars.pop(fxfno__nyp)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({brxni__qzbdc.name for brxni__qzbdc in aggregate_node.
        key_arrs})
    use_set.update({brxni__qzbdc.name for brxni__qzbdc in aggregate_node.
        df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({brxni__qzbdc.name for brxni__qzbdc in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({brxni__qzbdc.name for brxni__qzbdc in
            aggregate_node.out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    yzu__szhi = [hmpgf__npeq for hmpgf__npeq, txmd__jxfif in aggregate_node
        .df_out_vars.items() if txmd__jxfif.name not in lives]
    for ere__cfx in yzu__szhi:
        aggregate_node.remove_out_col(ere__cfx)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(brxni__qzbdc.name not in lives for
        brxni__qzbdc in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    she__dzd = set(brxni__qzbdc.name for brxni__qzbdc in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        she__dzd.update({brxni__qzbdc.name for brxni__qzbdc in
            aggregate_node.out_key_vars})
    return set(), she__dzd


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for nwkj__idpa in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[nwkj__idpa] = replace_vars_inner(aggregate_node
            .key_arrs[nwkj__idpa], var_dict)
    for hmpgf__npeq in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[hmpgf__npeq] = replace_vars_inner(
            aggregate_node.df_in_vars[hmpgf__npeq], var_dict)
    for hmpgf__npeq in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[hmpgf__npeq] = replace_vars_inner(
            aggregate_node.df_out_vars[hmpgf__npeq], var_dict)
    if aggregate_node.out_key_vars is not None:
        for nwkj__idpa in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[nwkj__idpa] = replace_vars_inner(
                aggregate_node.out_key_vars[nwkj__idpa], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for nwkj__idpa in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[nwkj__idpa] = visit_vars_inner(aggregate_node
            .key_arrs[nwkj__idpa], callback, cbdata)
    for hmpgf__npeq in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[hmpgf__npeq] = visit_vars_inner(
            aggregate_node.df_in_vars[hmpgf__npeq], callback, cbdata)
    for hmpgf__npeq in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[hmpgf__npeq] = visit_vars_inner(
            aggregate_node.df_out_vars[hmpgf__npeq], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for nwkj__idpa in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[nwkj__idpa] = visit_vars_inner(
                aggregate_node.out_key_vars[nwkj__idpa], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    iff__uii = []
    for fdp__qgs in aggregate_node.key_arrs:
        jile__bfb = equiv_set.get_shape(fdp__qgs)
        if jile__bfb:
            iff__uii.append(jile__bfb[0])
    if aggregate_node.pivot_arr is not None:
        jile__bfb = equiv_set.get_shape(aggregate_node.pivot_arr)
        if jile__bfb:
            iff__uii.append(jile__bfb[0])
    for txmd__jxfif in aggregate_node.df_in_vars.values():
        jile__bfb = equiv_set.get_shape(txmd__jxfif)
        if jile__bfb:
            iff__uii.append(jile__bfb[0])
    if len(iff__uii) > 1:
        equiv_set.insert_equiv(*iff__uii)
    voq__xuc = []
    iff__uii = []
    fqg__qhgf = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        fqg__qhgf.extend(aggregate_node.out_key_vars)
    for txmd__jxfif in fqg__qhgf:
        rahoj__tahnv = typemap[txmd__jxfif.name]
        ililt__hrno = array_analysis._gen_shape_call(equiv_set, txmd__jxfif,
            rahoj__tahnv.ndim, None, voq__xuc)
        equiv_set.insert_equiv(txmd__jxfif, ililt__hrno)
        iff__uii.append(ililt__hrno[0])
        equiv_set.define(txmd__jxfif, set())
    if len(iff__uii) > 1:
        equiv_set.insert_equiv(*iff__uii)
    return [], voq__xuc


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    thaws__emswz = Distribution.OneD
    for txmd__jxfif in aggregate_node.df_in_vars.values():
        thaws__emswz = Distribution(min(thaws__emswz.value, array_dists[
            txmd__jxfif.name].value))
    for fdp__qgs in aggregate_node.key_arrs:
        thaws__emswz = Distribution(min(thaws__emswz.value, array_dists[
            fdp__qgs.name].value))
    if aggregate_node.pivot_arr is not None:
        thaws__emswz = Distribution(min(thaws__emswz.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = thaws__emswz
    for txmd__jxfif in aggregate_node.df_in_vars.values():
        array_dists[txmd__jxfif.name] = thaws__emswz
    for fdp__qgs in aggregate_node.key_arrs:
        array_dists[fdp__qgs.name] = thaws__emswz
    adyb__naxcf = Distribution.OneD_Var
    for txmd__jxfif in aggregate_node.df_out_vars.values():
        if txmd__jxfif.name in array_dists:
            adyb__naxcf = Distribution(min(adyb__naxcf.value, array_dists[
                txmd__jxfif.name].value))
    if aggregate_node.out_key_vars is not None:
        for txmd__jxfif in aggregate_node.out_key_vars:
            if txmd__jxfif.name in array_dists:
                adyb__naxcf = Distribution(min(adyb__naxcf.value,
                    array_dists[txmd__jxfif.name].value))
    adyb__naxcf = Distribution(min(adyb__naxcf.value, thaws__emswz.value))
    for txmd__jxfif in aggregate_node.df_out_vars.values():
        array_dists[txmd__jxfif.name] = adyb__naxcf
    if aggregate_node.out_key_vars is not None:
        for vahb__mst in aggregate_node.out_key_vars:
            array_dists[vahb__mst.name] = adyb__naxcf
    if adyb__naxcf != Distribution.OneD_Var:
        for fdp__qgs in aggregate_node.key_arrs:
            array_dists[fdp__qgs.name] = adyb__naxcf
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = adyb__naxcf
        for txmd__jxfif in aggregate_node.df_in_vars.values():
            array_dists[txmd__jxfif.name] = adyb__naxcf


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for txmd__jxfif in agg_node.df_out_vars.values():
        definitions[txmd__jxfif.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for vahb__mst in agg_node.out_key_vars:
            definitions[vahb__mst.name].append(agg_node)
    return definitions


ir_utils.build_defs_extensions[Aggregate] = build_agg_definitions


def __update_redvars():
    pass


@infer_global(__update_redvars)
class UpdateDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __combine_redvars():
    pass


@infer_global(__combine_redvars)
class CombineDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __eval_res():
    pass


@infer_global(__eval_res)
class EvalDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(args[0].dtype, *args)


def agg_distributed_run(agg_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    if array_dists is not None:
        parallel = True
        for brxni__qzbdc in (list(agg_node.df_in_vars.values()) + list(
            agg_node.df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[brxni__qzbdc.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                brxni__qzbdc.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    fjuiu__qfz = tuple(typemap[brxni__qzbdc.name] for brxni__qzbdc in
        agg_node.key_arrs)
    vbwwu__gviy = [brxni__qzbdc for ynh__mgkuo, brxni__qzbdc in agg_node.
        df_in_vars.items()]
    phn__fzfp = [brxni__qzbdc for ynh__mgkuo, brxni__qzbdc in agg_node.
        df_out_vars.items()]
    in_col_typs = []
    taad__akaz = []
    if agg_node.pivot_arr is not None:
        for fxfno__nyp, ztefm__dzzj in agg_node.gb_info_in.items():
            for func, ruu__uko in ztefm__dzzj:
                if fxfno__nyp is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[
                        fxfno__nyp].name])
                taad__akaz.append(func)
    else:
        for fxfno__nyp, func in agg_node.gb_info_out.values():
            if fxfno__nyp is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[fxfno__nyp].
                    name])
            taad__akaz.append(func)
    out_col_typs = tuple(typemap[brxni__qzbdc.name] for brxni__qzbdc in
        phn__fzfp)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(fjuiu__qfz + tuple(typemap[brxni__qzbdc.name] for
        brxni__qzbdc in vbwwu__gviy) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    jzaji__yjt = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for nwkj__idpa, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            jzaji__yjt.update({f'in_cat_dtype_{nwkj__idpa}': in_col_typ})
    for nwkj__idpa, rzvl__bbab in enumerate(out_col_typs):
        if isinstance(rzvl__bbab, bodo.CategoricalArrayType):
            jzaji__yjt.update({f'out_cat_dtype_{nwkj__idpa}': rzvl__bbab})
    udf_func_struct = get_udf_func_struct(taad__akaz, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    jxkh__dhdm = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    jzaji__yjt.update({'pd': pd, 'pre_alloc_string_array':
        pre_alloc_string_array, 'pre_alloc_binary_array':
        pre_alloc_binary_array, 'pre_alloc_array_item_array':
        pre_alloc_array_item_array, 'string_array_type': string_array_type,
        'alloc_decimal_array': alloc_decimal_array, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'coerce_to_array': bodo.utils.conversion.coerce_to_array,
        'groupby_and_aggregate': groupby_and_aggregate,
        'pivot_groupby_and_aggregate': pivot_groupby_and_aggregate,
        'info_from_table': info_from_table, 'info_to_array': info_to_array,
        'delete_info_decref_array': delete_info_decref_array,
        'delete_table': delete_table, 'add_agg_cfunc_sym':
        add_agg_cfunc_sym, 'get_agg_udf_addr': get_agg_udf_addr,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'decode_if_dict_array': decode_if_dict_array, 'out_typs': out_col_typs}
        )
    if udf_func_struct is not None:
        if udf_func_struct.regular_udfs:
            jzaji__yjt.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            jzaji__yjt.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    wudg__ofpc = compile_to_numba_ir(jxkh__dhdm, jzaji__yjt, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    tjv__fxa = []
    if agg_node.pivot_arr is None:
        rwjr__ohc = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        feqq__jge = ir.Var(rwjr__ohc, mk_unique_var('dummy_none'), loc)
        typemap[feqq__jge.name] = types.none
        tjv__fxa.append(ir.Assign(ir.Const(None, loc), feqq__jge, loc))
        vbwwu__gviy.append(feqq__jge)
    else:
        vbwwu__gviy.append(agg_node.pivot_arr)
    replace_arg_nodes(wudg__ofpc, agg_node.key_arrs + vbwwu__gviy)
    llero__ovnfu = wudg__ofpc.body[-3]
    assert is_assign(llero__ovnfu) and isinstance(llero__ovnfu.value, ir.Expr
        ) and llero__ovnfu.value.op == 'build_tuple'
    tjv__fxa += wudg__ofpc.body[:-3]
    fqg__qhgf = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        fqg__qhgf += agg_node.out_key_vars
    for nwkj__idpa, lca__yxcg in enumerate(fqg__qhgf):
        myf__rdqxa = llero__ovnfu.value.items[nwkj__idpa]
        tjv__fxa.append(ir.Assign(myf__rdqxa, lca__yxcg, lca__yxcg.loc))
    return tjv__fxa


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        wxwxm__cas = args[0]
        dtype = types.Tuple([t.dtype for t in wxwxm__cas.types]) if isinstance(
            wxwxm__cas, types.BaseTuple) else wxwxm__cas.dtype
        if isinstance(wxwxm__cas, types.BaseTuple) and len(wxwxm__cas.types
            ) == 1:
            dtype = wxwxm__cas.types[0].dtype
        return signature(types.Set(dtype), *args)


@lower_builtin(get_numba_set, types.Any)
def lower_get_numba_set(context, builder, sig, args):
    return numba.cpython.setobj.set_empty_constructor(context, builder, sig,
        args)


@infer_global(bool)
class BoolNoneTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        bhehc__oeuu = args[0]
        if bhehc__oeuu == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    tkhq__xofux = context.compile_internal(builder, lambda a: False, sig, args)
    return tkhq__xofux


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        wlr__sjpu = IntDtype(t.dtype).name
        assert wlr__sjpu.endswith('Dtype()')
        wlr__sjpu = wlr__sjpu[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{wlr__sjpu}'))"
            )
    elif isinstance(t, BooleanArrayType):
        return (
            'bodo.libs.bool_arr_ext.init_bool_array(np.empty(0, np.bool_), np.empty(0, np.uint8))'
            )
    elif isinstance(t, StringArrayType):
        return 'pre_alloc_string_array(1, 1)'
    elif isinstance(t, BinaryArrayType):
        return 'pre_alloc_binary_array(1, 1)'
    elif t == ArrayItemArrayType(string_array_type):
        return 'pre_alloc_array_item_array(1, (1, 1), string_array_type)'
    elif isinstance(t, DecimalArrayType):
        return 'alloc_decimal_array(1, {}, {})'.format(t.precision, t.scale)
    elif isinstance(t, DatetimeDateArrayType):
        return (
            'bodo.hiframes.datetime_date_ext.init_datetime_date_array(np.empty(1, np.int64), np.empty(1, np.uint8))'
            )
    elif isinstance(t, bodo.CategoricalArrayType):
        if t.dtype.categories is None:
            raise BodoError(
                'Groupby agg operations on Categorical types require constant categories'
                )
        qqwp__yoc = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {qqwp__yoc}_cat_dtype_{colnum})')
    else:
        return 'np.empty(1, {})'.format(_get_np_dtype(t.dtype))


def _get_np_dtype(t):
    if t == types.bool_:
        return 'np.bool_'
    if t == types.NPDatetime('ns'):
        return 'dt64_dtype'
    if t == types.NPTimedelta('ns'):
        return 'td64_dtype'
    return 'np.{}'.format(t)


def gen_update_cb(udf_func_struct, allfuncs, n_keys, data_in_typs_,
    out_data_typs, do_combine, func_idx_to_in_col, label_suffix):
    sdlxq__egeh = udf_func_struct.var_typs
    uptr__ljd = len(sdlxq__egeh)
    aan__jma = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    aan__jma += '    if is_null_pointer(in_table):\n'
    aan__jma += '        return\n'
    aan__jma += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in sdlxq__egeh]), 
        ',' if len(sdlxq__egeh) == 1 else '')
    zzor__aaw = n_keys
    eae__ifhb = []
    redvar_offsets = []
    knn__jgbwi = []
    if do_combine:
        for nwkj__idpa, omprp__sbzb in enumerate(allfuncs):
            if omprp__sbzb.ftype != 'udf':
                zzor__aaw += omprp__sbzb.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(zzor__aaw, zzor__aaw +
                    omprp__sbzb.n_redvars))
                zzor__aaw += omprp__sbzb.n_redvars
                knn__jgbwi.append(data_in_typs_[func_idx_to_in_col[nwkj__idpa]]
                    )
                eae__ifhb.append(func_idx_to_in_col[nwkj__idpa] + n_keys)
    else:
        for nwkj__idpa, omprp__sbzb in enumerate(allfuncs):
            if omprp__sbzb.ftype != 'udf':
                zzor__aaw += omprp__sbzb.ncols_post_shuffle
            else:
                redvar_offsets += list(range(zzor__aaw + 1, zzor__aaw + 1 +
                    omprp__sbzb.n_redvars))
                zzor__aaw += omprp__sbzb.n_redvars + 1
                knn__jgbwi.append(data_in_typs_[func_idx_to_in_col[nwkj__idpa]]
                    )
                eae__ifhb.append(func_idx_to_in_col[nwkj__idpa] + n_keys)
    assert len(redvar_offsets) == uptr__ljd
    lwf__fxkv = len(knn__jgbwi)
    ibyce__bjwvj = []
    for nwkj__idpa, t in enumerate(knn__jgbwi):
        ibyce__bjwvj.append(_gen_dummy_alloc(t, nwkj__idpa, True))
    aan__jma += '    data_in_dummy = ({}{})\n'.format(','.join(ibyce__bjwvj
        ), ',' if len(knn__jgbwi) == 1 else '')
    aan__jma += """
    # initialize redvar cols
"""
    aan__jma += '    init_vals = __init_func()\n'
    for nwkj__idpa in range(uptr__ljd):
        aan__jma += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(nwkj__idpa, redvar_offsets[nwkj__idpa], nwkj__idpa))
        aan__jma += '    incref(redvar_arr_{})\n'.format(nwkj__idpa)
        aan__jma += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(nwkj__idpa
            , nwkj__idpa)
    aan__jma += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(nwkj__idpa) for nwkj__idpa in range(uptr__ljd)]), ',' if 
        uptr__ljd == 1 else '')
    aan__jma += '\n'
    for nwkj__idpa in range(lwf__fxkv):
        aan__jma += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(nwkj__idpa, eae__ifhb[nwkj__idpa], nwkj__idpa))
        aan__jma += '    incref(data_in_{})\n'.format(nwkj__idpa)
    aan__jma += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(nwkj__idpa) for nwkj__idpa in range(lwf__fxkv)]), ',' if 
        lwf__fxkv == 1 else '')
    aan__jma += '\n'
    aan__jma += '    for i in range(len(data_in_0)):\n'
    aan__jma += '        w_ind = row_to_group[i]\n'
    aan__jma += '        if w_ind != -1:\n'
    aan__jma += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    nvoe__fyo = {}
    exec(aan__jma, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, nvoe__fyo)
    return nvoe__fyo['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    sdlxq__egeh = udf_func_struct.var_typs
    uptr__ljd = len(sdlxq__egeh)
    aan__jma = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    aan__jma += '    if is_null_pointer(in_table):\n'
    aan__jma += '        return\n'
    aan__jma += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in sdlxq__egeh]), 
        ',' if len(sdlxq__egeh) == 1 else '')
    labv__rwdtx = n_keys
    sky__udtwj = n_keys
    chcm__lovb = []
    jlz__hfz = []
    for omprp__sbzb in allfuncs:
        if omprp__sbzb.ftype != 'udf':
            labv__rwdtx += omprp__sbzb.ncols_pre_shuffle
            sky__udtwj += omprp__sbzb.ncols_post_shuffle
        else:
            chcm__lovb += list(range(labv__rwdtx, labv__rwdtx + omprp__sbzb
                .n_redvars))
            jlz__hfz += list(range(sky__udtwj + 1, sky__udtwj + 1 +
                omprp__sbzb.n_redvars))
            labv__rwdtx += omprp__sbzb.n_redvars
            sky__udtwj += 1 + omprp__sbzb.n_redvars
    assert len(chcm__lovb) == uptr__ljd
    aan__jma += """
    # initialize redvar cols
"""
    aan__jma += '    init_vals = __init_func()\n'
    for nwkj__idpa in range(uptr__ljd):
        aan__jma += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(nwkj__idpa, jlz__hfz[nwkj__idpa], nwkj__idpa))
        aan__jma += '    incref(redvar_arr_{})\n'.format(nwkj__idpa)
        aan__jma += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(nwkj__idpa
            , nwkj__idpa)
    aan__jma += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(nwkj__idpa) for nwkj__idpa in range(uptr__ljd)]), ',' if 
        uptr__ljd == 1 else '')
    aan__jma += '\n'
    for nwkj__idpa in range(uptr__ljd):
        aan__jma += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(nwkj__idpa, chcm__lovb[nwkj__idpa], nwkj__idpa))
        aan__jma += '    incref(recv_redvar_arr_{})\n'.format(nwkj__idpa)
    aan__jma += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(nwkj__idpa) for nwkj__idpa in range(
        uptr__ljd)]), ',' if uptr__ljd == 1 else '')
    aan__jma += '\n'
    if uptr__ljd:
        aan__jma += '    for i in range(len(recv_redvar_arr_0)):\n'
        aan__jma += '        w_ind = row_to_group[i]\n'
        aan__jma += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)\n'
            )
    nvoe__fyo = {}
    exec(aan__jma, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, nvoe__fyo)
    return nvoe__fyo['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    sdlxq__egeh = udf_func_struct.var_typs
    uptr__ljd = len(sdlxq__egeh)
    zzor__aaw = n_keys
    redvar_offsets = []
    ingh__fvu = []
    out_data_typs = []
    for nwkj__idpa, omprp__sbzb in enumerate(allfuncs):
        if omprp__sbzb.ftype != 'udf':
            zzor__aaw += omprp__sbzb.ncols_post_shuffle
        else:
            ingh__fvu.append(zzor__aaw)
            redvar_offsets += list(range(zzor__aaw + 1, zzor__aaw + 1 +
                omprp__sbzb.n_redvars))
            zzor__aaw += 1 + omprp__sbzb.n_redvars
            out_data_typs.append(out_data_typs_[nwkj__idpa])
    assert len(redvar_offsets) == uptr__ljd
    lwf__fxkv = len(out_data_typs)
    aan__jma = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    aan__jma += '    if is_null_pointer(table):\n'
    aan__jma += '        return\n'
    aan__jma += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in sdlxq__egeh]), 
        ',' if len(sdlxq__egeh) == 1 else '')
    aan__jma += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for nwkj__idpa in range(uptr__ljd):
        aan__jma += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(nwkj__idpa, redvar_offsets[nwkj__idpa], nwkj__idpa))
        aan__jma += '    incref(redvar_arr_{})\n'.format(nwkj__idpa)
    aan__jma += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(nwkj__idpa) for nwkj__idpa in range(uptr__ljd)]), ',' if 
        uptr__ljd == 1 else '')
    aan__jma += '\n'
    for nwkj__idpa in range(lwf__fxkv):
        aan__jma += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(nwkj__idpa, ingh__fvu[nwkj__idpa], nwkj__idpa))
        aan__jma += '    incref(data_out_{})\n'.format(nwkj__idpa)
    aan__jma += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(nwkj__idpa) for nwkj__idpa in range(lwf__fxkv)]), ',' if 
        lwf__fxkv == 1 else '')
    aan__jma += '\n'
    aan__jma += '    for i in range(len(data_out_0)):\n'
    aan__jma += '        __eval_res(redvars, data_out, i)\n'
    nvoe__fyo = {}
    exec(aan__jma, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, nvoe__fyo)
    return nvoe__fyo['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    zzor__aaw = n_keys
    enn__dgk = []
    for nwkj__idpa, omprp__sbzb in enumerate(allfuncs):
        if omprp__sbzb.ftype == 'gen_udf':
            enn__dgk.append(zzor__aaw)
            zzor__aaw += 1
        elif omprp__sbzb.ftype != 'udf':
            zzor__aaw += omprp__sbzb.ncols_post_shuffle
        else:
            zzor__aaw += omprp__sbzb.n_redvars + 1
    aan__jma = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    aan__jma += '    if num_groups == 0:\n'
    aan__jma += '        return\n'
    for nwkj__idpa, func in enumerate(udf_func_struct.general_udf_funcs):
        aan__jma += '    # col {}\n'.format(nwkj__idpa)
        aan__jma += (
            '    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)\n'
            .format(enn__dgk[nwkj__idpa], nwkj__idpa))
        aan__jma += '    incref(out_col)\n'
        aan__jma += '    for j in range(num_groups):\n'
        aan__jma += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(nwkj__idpa, nwkj__idpa))
        aan__jma += '        incref(in_col)\n'
        aan__jma += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(nwkj__idpa))
    jzaji__yjt = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    tsgj__otorx = 0
    for nwkj__idpa, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[tsgj__otorx]
        jzaji__yjt['func_{}'.format(tsgj__otorx)] = func
        jzaji__yjt['in_col_{}_typ'.format(tsgj__otorx)] = in_col_typs[
            func_idx_to_in_col[nwkj__idpa]]
        jzaji__yjt['out_col_{}_typ'.format(tsgj__otorx)] = out_col_typs[
            nwkj__idpa]
        tsgj__otorx += 1
    nvoe__fyo = {}
    exec(aan__jma, jzaji__yjt, nvoe__fyo)
    omprp__sbzb = nvoe__fyo['bodo_gb_apply_general_udfs{}'.format(label_suffix)
        ]
    wjfi__klf = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(wjfi__klf, nopython=True)(omprp__sbzb)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    kpvkj__elxt = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        zucvo__eyawi = 1
    else:
        zucvo__eyawi = len(agg_node.pivot_values)
    vwty__xig = tuple('key_' + sanitize_varname(lpjwo__ublnd) for
        lpjwo__ublnd in agg_node.key_names)
    akb__zqkf = {lpjwo__ublnd: 'in_{}'.format(sanitize_varname(lpjwo__ublnd
        )) for lpjwo__ublnd in agg_node.gb_info_in.keys() if lpjwo__ublnd
         is not None}
    kms__ucgbw = {lpjwo__ublnd: ('out_' + sanitize_varname(lpjwo__ublnd)) for
        lpjwo__ublnd in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    cbfu__mmw = ', '.join(vwty__xig)
    bza__nbb = ', '.join(akb__zqkf.values())
    if bza__nbb != '':
        bza__nbb = ', ' + bza__nbb
    aan__jma = 'def agg_top({}{}{}, pivot_arr):\n'.format(cbfu__mmw,
        bza__nbb, ', index_arg' if agg_node.input_has_index else '')
    for a in (vwty__xig + tuple(akb__zqkf.values())):
        aan__jma += f'    {a} = decode_if_dict_array({a})\n'
    if kpvkj__elxt:
        aan__jma += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        bpsr__fzwve = []
        for fxfno__nyp, ztefm__dzzj in agg_node.gb_info_in.items():
            if fxfno__nyp is not None:
                for func, ruu__uko in ztefm__dzzj:
                    bpsr__fzwve.append(akb__zqkf[fxfno__nyp])
    else:
        bpsr__fzwve = tuple(akb__zqkf[fxfno__nyp] for fxfno__nyp, ruu__uko in
            agg_node.gb_info_out.values() if fxfno__nyp is not None)
    nyl__rcomj = vwty__xig + tuple(bpsr__fzwve)
    aan__jma += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in nyl__rcomj), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    aan__jma += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    sptxr__hsdo = []
    func_idx_to_in_col = []
    hlz__ktije = []
    xoifx__ethj = False
    dvav__gyxdp = 1
    yknmh__efzs = -1
    sgw__pzqen = 0
    tgttk__hbybd = 0
    if not kpvkj__elxt:
        taad__akaz = [func for ruu__uko, func in agg_node.gb_info_out.values()]
    else:
        taad__akaz = [func for func, ruu__uko in ztefm__dzzj for
            ztefm__dzzj in agg_node.gb_info_in.values()]
    for nap__eogp, func in enumerate(taad__akaz):
        sptxr__hsdo.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            sgw__pzqen += 1
        if hasattr(func, 'skipdropna'):
            xoifx__ethj = func.skipdropna
        if func.ftype == 'shift':
            dvav__gyxdp = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            tgttk__hbybd = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            yknmh__efzs = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(nap__eogp)
        if func.ftype == 'udf':
            hlz__ktije.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            hlz__ktije.append(0)
            do_combine = False
    sptxr__hsdo.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == zucvo__eyawi, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * zucvo__eyawi, 'invalid number of groupby outputs'
    if sgw__pzqen > 0:
        if sgw__pzqen != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for nwkj__idpa, lpjwo__ublnd in enumerate(agg_node.gb_info_out.keys()):
        hvrzz__aict = kms__ucgbw[lpjwo__ublnd] + '_dummy'
        rzvl__bbab = out_col_typs[nwkj__idpa]
        fxfno__nyp, func = agg_node.gb_info_out[lpjwo__ublnd]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(rzvl__bbab, bodo.
            CategoricalArrayType):
            aan__jma += '    {} = {}\n'.format(hvrzz__aict, akb__zqkf[
                fxfno__nyp])
        elif udf_func_struct is not None:
            aan__jma += '    {} = {}\n'.format(hvrzz__aict,
                _gen_dummy_alloc(rzvl__bbab, nwkj__idpa, False))
    if udf_func_struct is not None:
        yeh__eyeuz = next_label()
        if udf_func_struct.regular_udfs:
            wjfi__klf = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            jgv__etiyz = numba.cfunc(wjfi__klf, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, yeh__eyeuz))
            cielj__rgkfi = numba.cfunc(wjfi__klf, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, yeh__eyeuz))
            fnrh__hpdd = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                yeh__eyeuz))
            udf_func_struct.set_regular_cfuncs(jgv__etiyz, cielj__rgkfi,
                fnrh__hpdd)
            for ihopa__iwnc in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[ihopa__iwnc.native_name] = ihopa__iwnc
                gb_agg_cfunc_addr[ihopa__iwnc.native_name
                    ] = ihopa__iwnc.address
        if udf_func_struct.general_udfs:
            tkqod__uzs = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                yeh__eyeuz)
            udf_func_struct.set_general_cfunc(tkqod__uzs)
        tumb__hnhx = []
        nja__cwe = 0
        nwkj__idpa = 0
        for hvrzz__aict, omprp__sbzb in zip(kms__ucgbw.values(), allfuncs):
            if omprp__sbzb.ftype in ('udf', 'gen_udf'):
                tumb__hnhx.append(hvrzz__aict + '_dummy')
                for mecb__wotyl in range(nja__cwe, nja__cwe + hlz__ktije[
                    nwkj__idpa]):
                    tumb__hnhx.append('data_redvar_dummy_' + str(mecb__wotyl))
                nja__cwe += hlz__ktije[nwkj__idpa]
                nwkj__idpa += 1
        if udf_func_struct.regular_udfs:
            sdlxq__egeh = udf_func_struct.var_typs
            for nwkj__idpa, t in enumerate(sdlxq__egeh):
                aan__jma += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(nwkj__idpa, _get_np_dtype(t)))
        aan__jma += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in tumb__hnhx))
        aan__jma += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            aan__jma += "    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".format(
                jgv__etiyz.native_name)
            aan__jma += "    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".format(
                cielj__rgkfi.native_name)
            aan__jma += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                fnrh__hpdd.native_name)
            aan__jma += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(jgv__etiyz.native_name))
            aan__jma += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(cielj__rgkfi.native_name))
            aan__jma += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n".
                format(fnrh__hpdd.native_name))
        else:
            aan__jma += '    cpp_cb_update_addr = 0\n'
            aan__jma += '    cpp_cb_combine_addr = 0\n'
            aan__jma += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            ihopa__iwnc = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[ihopa__iwnc.native_name] = ihopa__iwnc
            gb_agg_cfunc_addr[ihopa__iwnc.native_name] = ihopa__iwnc.address
            aan__jma += "    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".format(
                ihopa__iwnc.native_name)
            aan__jma += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(ihopa__iwnc.native_name))
        else:
            aan__jma += '    cpp_cb_general_addr = 0\n'
    else:
        aan__jma += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        aan__jma += '    cpp_cb_update_addr = 0\n'
        aan__jma += '    cpp_cb_combine_addr = 0\n'
        aan__jma += '    cpp_cb_eval_addr = 0\n'
        aan__jma += '    cpp_cb_general_addr = 0\n'
    aan__jma += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(omprp__sbzb.ftype)) for
        omprp__sbzb in allfuncs] + ['0']))
    aan__jma += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(str
        (sptxr__hsdo))
    if len(hlz__ktije) > 0:
        aan__jma += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(str
            (hlz__ktije))
    else:
        aan__jma += '    udf_ncols = np.array([0], np.int32)\n'
    if kpvkj__elxt:
        aan__jma += '    arr_type = coerce_to_array({})\n'.format(agg_node.
            pivot_values)
        aan__jma += '    arr_info = array_to_info(arr_type)\n'
        aan__jma += '    dispatch_table = arr_info_list_to_table([arr_info])\n'
        aan__jma += '    pivot_info = array_to_info(pivot_arr)\n'
        aan__jma += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        aan__jma += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, xoifx__ethj, agg_node.return_key, agg_node.same_index)
            )
        aan__jma += '    delete_info_decref_array(pivot_info)\n'
        aan__jma += '    delete_info_decref_array(arr_info)\n'
    else:
        aan__jma += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, xoifx__ethj,
            dvav__gyxdp, tgttk__hbybd, yknmh__efzs, agg_node.return_key,
            agg_node.same_index, agg_node.dropna))
    tvd__pcukl = 0
    if agg_node.return_key:
        for nwkj__idpa, eyf__bttet in enumerate(vwty__xig):
            aan__jma += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(eyf__bttet, tvd__pcukl, eyf__bttet))
            tvd__pcukl += 1
    for nwkj__idpa, hvrzz__aict in enumerate(kms__ucgbw.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(rzvl__bbab, bodo.
            CategoricalArrayType):
            aan__jma += f"""    {hvrzz__aict} = info_to_array(info_from_table(out_table, {tvd__pcukl}), {hvrzz__aict + '_dummy'})
"""
        else:
            aan__jma += f"""    {hvrzz__aict} = info_to_array(info_from_table(out_table, {tvd__pcukl}), out_typs[{nwkj__idpa}])
"""
        tvd__pcukl += 1
    if agg_node.same_index:
        aan__jma += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(tvd__pcukl))
        tvd__pcukl += 1
    aan__jma += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    aan__jma += '    delete_table_decref_arrays(table)\n'
    aan__jma += '    delete_table_decref_arrays(udf_table_dummy)\n'
    aan__jma += '    delete_table(out_table)\n'
    aan__jma += f'    ev_clean.finalize()\n'
    guh__tel = tuple(kms__ucgbw.values())
    if agg_node.return_key:
        guh__tel += tuple(vwty__xig)
    aan__jma += '    return ({},{})\n'.format(', '.join(guh__tel), 
        ' out_index_arg,' if agg_node.same_index else '')
    nvoe__fyo = {}
    exec(aan__jma, {'out_typs': out_col_typs}, nvoe__fyo)
    otshs__quru = nvoe__fyo['agg_top']
    return otshs__quru


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for boi__uhlx in block.body:
            if is_call_assign(boi__uhlx) and find_callname(f_ir, boi__uhlx.
                value) == ('len', 'builtins') and boi__uhlx.value.args[0
                ].name == f_ir.arg_names[0]:
                ldjgg__nuagy = get_definition(f_ir, boi__uhlx.value.func)
                ldjgg__nuagy.name = 'dummy_agg_count'
                ldjgg__nuagy.value = dummy_agg_count
    dzwho__cukv = get_name_var_table(f_ir.blocks)
    vfh__yme = {}
    for name, ruu__uko in dzwho__cukv.items():
        vfh__yme[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, vfh__yme)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    khzj__ysei = numba.core.compiler.Flags()
    khzj__ysei.nrt = True
    ucdvz__emne = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, khzj__ysei)
    ucdvz__emne.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, lxocf__cjp, calltypes, ruu__uko = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    nuig__vaqdy = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    iinpi__sxeu = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    mbsn__wiuwu = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    bgi__cebpb = mbsn__wiuwu(typemap, calltypes)
    pm = iinpi__sxeu(typingctx, targetctx, None, f_ir, typemap, lxocf__cjp,
        calltypes, bgi__cebpb, {}, khzj__ysei, None)
    ufyaw__xpf = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = iinpi__sxeu(typingctx, targetctx, None, f_ir, typemap, lxocf__cjp,
        calltypes, bgi__cebpb, {}, khzj__ysei, ufyaw__xpf)
    gpf__ibosv = numba.core.typed_passes.InlineOverloads()
    gpf__ibosv.run_pass(pm)
    bdyg__wfqm = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    bdyg__wfqm.run()
    for block in f_ir.blocks.values():
        for boi__uhlx in block.body:
            if is_assign(boi__uhlx) and isinstance(boi__uhlx.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[boi__uhlx.target.name],
                SeriesType):
                rahoj__tahnv = typemap.pop(boi__uhlx.target.name)
                typemap[boi__uhlx.target.name] = rahoj__tahnv.data
            if is_call_assign(boi__uhlx) and find_callname(f_ir, boi__uhlx.
                value) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[boi__uhlx.target.name].remove(boi__uhlx.value
                    )
                boi__uhlx.value = boi__uhlx.value.args[0]
                f_ir._definitions[boi__uhlx.target.name].append(boi__uhlx.value
                    )
            if is_call_assign(boi__uhlx) and find_callname(f_ir, boi__uhlx.
                value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[boi__uhlx.target.name].remove(boi__uhlx.value
                    )
                boi__uhlx.value = ir.Const(False, boi__uhlx.loc)
                f_ir._definitions[boi__uhlx.target.name].append(boi__uhlx.value
                    )
            if is_call_assign(boi__uhlx) and find_callname(f_ir, boi__uhlx.
                value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[boi__uhlx.target.name].remove(boi__uhlx.value
                    )
                boi__uhlx.value = ir.Const(False, boi__uhlx.loc)
                f_ir._definitions[boi__uhlx.target.name].append(boi__uhlx.value
                    )
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    nmwzq__jvog = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, nuig__vaqdy)
    nmwzq__jvog.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    vnx__umm = numba.core.compiler.StateDict()
    vnx__umm.func_ir = f_ir
    vnx__umm.typemap = typemap
    vnx__umm.calltypes = calltypes
    vnx__umm.typingctx = typingctx
    vnx__umm.targetctx = targetctx
    vnx__umm.return_type = lxocf__cjp
    numba.core.rewrites.rewrite_registry.apply('after-inference', vnx__umm)
    fjoyr__kguml = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        lxocf__cjp, typingctx, targetctx, nuig__vaqdy, khzj__ysei, {})
    fjoyr__kguml.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            mzfzd__nxrt = ctypes.pythonapi.PyCell_Get
            mzfzd__nxrt.restype = ctypes.py_object
            mzfzd__nxrt.argtypes = ctypes.py_object,
            jeh__vuij = tuple(mzfzd__nxrt(amy__con) for amy__con in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            jeh__vuij = closure.items
        assert len(code.co_freevars) == len(jeh__vuij)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, jeh__vuij)


class RegularUDFGenerator(object):

    def __init__(self, in_col_types, out_col_types, pivot_typ, pivot_values,
        is_crosstab, typingctx, targetctx):
        self.in_col_types = in_col_types
        self.out_col_types = out_col_types
        self.pivot_typ = pivot_typ
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab
        self.typingctx = typingctx
        self.targetctx = targetctx
        self.all_reduce_vars = []
        self.all_vartypes = []
        self.all_init_nodes = []
        self.all_eval_funcs = []
        self.all_update_funcs = []
        self.all_combine_funcs = []
        self.curr_offset = 0
        self.redvar_offsets = [0]

    def add_udf(self, in_col_typ, func):
        ogf__jixo = SeriesType(in_col_typ.dtype, in_col_typ, None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (ogf__jixo,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        lug__kxmc, arr_var = _rm_arg_agg_block(block, pm.typemap)
        bpaxs__obmhs = -1
        for nwkj__idpa, boi__uhlx in enumerate(lug__kxmc):
            if isinstance(boi__uhlx, numba.parfors.parfor.Parfor):
                assert bpaxs__obmhs == -1, 'only one parfor for aggregation function'
                bpaxs__obmhs = nwkj__idpa
        parfor = None
        if bpaxs__obmhs != -1:
            parfor = lug__kxmc[bpaxs__obmhs]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = lug__kxmc[:bpaxs__obmhs] + parfor.init_block.body
        eval_nodes = lug__kxmc[bpaxs__obmhs + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for boi__uhlx in init_nodes:
            if is_assign(boi__uhlx) and boi__uhlx.target.name in redvars:
                ind = redvars.index(boi__uhlx.target.name)
                reduce_vars[ind] = boi__uhlx.target
        var_types = [pm.typemap[brxni__qzbdc] for brxni__qzbdc in redvars]
        fumzl__lowmu = gen_combine_func(f_ir, parfor, redvars,
            var_to_redvar, var_types, arr_var, pm, self.typingctx, self.
            targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        ett__qmed = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        aad__tiu = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(aad__tiu)
        self.all_update_funcs.append(ett__qmed)
        self.all_combine_funcs.append(fumzl__lowmu)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        ikcd__jbeyc = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        zvsm__dvssi = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        psovv__qba = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        ntrhy__ljjjq = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return (self.all_vartypes, ikcd__jbeyc, zvsm__dvssi, psovv__qba,
            ntrhy__ljjjq)


class GeneralUDFGenerator(object):

    def __init__(self):
        self.funcs = []

    def add_udf(self, func):
        self.funcs.append(bodo.jit(distributed=False)(func))
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        func.n_redvars = 0

    def gen_all_func(self):
        if len(self.funcs) > 0:
            return self.funcs
        else:
            return None


def get_udf_func_struct(agg_func, input_has_index, in_col_types,
    out_col_types, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab):
    if is_crosstab and len(in_col_types) == 0:
        in_col_types = [types.Array(types.intp, 1, 'C')]
    royq__levzs = []
    for t, omprp__sbzb in zip(in_col_types, agg_func):
        royq__levzs.append((t, omprp__sbzb))
    sdy__gsagk = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    orpoh__bimx = GeneralUDFGenerator()
    for in_col_typ, func in royq__levzs:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            sdy__gsagk.add_udf(in_col_typ, func)
        except:
            orpoh__bimx.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = sdy__gsagk.gen_all_func()
    general_udf_funcs = orpoh__bimx.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    psd__tbj = compute_use_defs(parfor.loop_body)
    fyhsh__ivahp = set()
    for fhps__sldav in psd__tbj.usemap.values():
        fyhsh__ivahp |= fhps__sldav
    xka__fzb = set()
    for fhps__sldav in psd__tbj.defmap.values():
        xka__fzb |= fhps__sldav
    ocvr__erngr = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    ocvr__erngr.body = eval_nodes
    gmrg__lma = compute_use_defs({(0): ocvr__erngr})
    bjf__jjrg = gmrg__lma.usemap[0]
    gcb__wrxbv = set()
    brrg__qump = []
    ngy__liwe = []
    for boi__uhlx in reversed(init_nodes):
        zuw__suz = {brxni__qzbdc.name for brxni__qzbdc in boi__uhlx.list_vars()
            }
        if is_assign(boi__uhlx):
            brxni__qzbdc = boi__uhlx.target.name
            zuw__suz.remove(brxni__qzbdc)
            if (brxni__qzbdc in fyhsh__ivahp and brxni__qzbdc not in
                gcb__wrxbv and brxni__qzbdc not in bjf__jjrg and 
                brxni__qzbdc not in xka__fzb):
                ngy__liwe.append(boi__uhlx)
                fyhsh__ivahp |= zuw__suz
                xka__fzb.add(brxni__qzbdc)
                continue
        gcb__wrxbv |= zuw__suz
        brrg__qump.append(boi__uhlx)
    ngy__liwe.reverse()
    brrg__qump.reverse()
    ynhbi__drbf = min(parfor.loop_body.keys())
    tzk__qdbwf = parfor.loop_body[ynhbi__drbf]
    tzk__qdbwf.body = ngy__liwe + tzk__qdbwf.body
    return brrg__qump


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    tes__plall = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    jac__mtgf = set()
    lanlg__xwihe = []
    for boi__uhlx in init_nodes:
        if is_assign(boi__uhlx) and isinstance(boi__uhlx.value, ir.Global
            ) and isinstance(boi__uhlx.value.value, pytypes.FunctionType
            ) and boi__uhlx.value.value in tes__plall:
            jac__mtgf.add(boi__uhlx.target.name)
        elif is_call_assign(boi__uhlx
            ) and boi__uhlx.value.func.name in jac__mtgf:
            pass
        else:
            lanlg__xwihe.append(boi__uhlx)
    init_nodes = lanlg__xwihe
    qrr__zkqv = types.Tuple(var_types)
    sgcbm__nmzzo = lambda : None
    f_ir = compile_to_numba_ir(sgcbm__nmzzo, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    cel__twrew = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    bsvac__yxpq = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        cel__twrew, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [bsvac__yxpq] + block.body
    block.body[-2].value.value = cel__twrew
    zfvd__zyerc = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        qrr__zkqv, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    hzrtc__pzpx = numba.core.target_extension.dispatcher_registry[cpu_target](
        sgcbm__nmzzo)
    hzrtc__pzpx.add_overload(zfvd__zyerc)
    return hzrtc__pzpx


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    zkjcz__nea = len(update_funcs)
    zhicr__fvu = len(in_col_types)
    if pivot_values is not None:
        assert zhicr__fvu == 1
    aan__jma = 'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n'
    if pivot_values is not None:
        ywsoq__bgk = redvar_offsets[zhicr__fvu]
        aan__jma += '  pv = pivot_arr[i]\n'
        for mecb__wotyl, gbz__ztg in enumerate(pivot_values):
            kdlk__hprh = 'el' if mecb__wotyl != 0 else ''
            aan__jma += "  {}if pv == '{}':\n".format(kdlk__hprh, gbz__ztg)
            epst__esn = ywsoq__bgk * mecb__wotyl
            lrss__qgx = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                nwkj__idpa) for nwkj__idpa in range(epst__esn +
                redvar_offsets[0], epst__esn + redvar_offsets[1])])
            hlga__ilin = 'data_in[0][i]'
            if is_crosstab:
                hlga__ilin = '0'
            aan__jma += '    {} = update_vars_0({}, {})\n'.format(lrss__qgx,
                lrss__qgx, hlga__ilin)
    else:
        for mecb__wotyl in range(zkjcz__nea):
            lrss__qgx = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                nwkj__idpa) for nwkj__idpa in range(redvar_offsets[
                mecb__wotyl], redvar_offsets[mecb__wotyl + 1])])
            if lrss__qgx:
                aan__jma += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(lrss__qgx, mecb__wotyl, lrss__qgx, 0 if 
                    zhicr__fvu == 1 else mecb__wotyl))
    aan__jma += '  return\n'
    jzaji__yjt = {}
    for nwkj__idpa, omprp__sbzb in enumerate(update_funcs):
        jzaji__yjt['update_vars_{}'.format(nwkj__idpa)] = omprp__sbzb
    nvoe__fyo = {}
    exec(aan__jma, jzaji__yjt, nvoe__fyo)
    mwqrb__jdho = nvoe__fyo['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(mwqrb__jdho)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    sui__bna = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types])
    arg_typs = sui__bna, sui__bna, types.intp, types.intp, pivot_typ
    roknh__nzqio = len(redvar_offsets) - 1
    ywsoq__bgk = redvar_offsets[roknh__nzqio]
    aan__jma = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert roknh__nzqio == 1
        for egs__hnwqa in range(len(pivot_values)):
            epst__esn = ywsoq__bgk * egs__hnwqa
            lrss__qgx = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                nwkj__idpa) for nwkj__idpa in range(epst__esn +
                redvar_offsets[0], epst__esn + redvar_offsets[1])])
            mtn__pprng = ', '.join(['recv_arrs[{}][i]'.format(nwkj__idpa) for
                nwkj__idpa in range(epst__esn + redvar_offsets[0], 
                epst__esn + redvar_offsets[1])])
            aan__jma += '  {} = combine_vars_0({}, {})\n'.format(lrss__qgx,
                lrss__qgx, mtn__pprng)
    else:
        for mecb__wotyl in range(roknh__nzqio):
            lrss__qgx = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                nwkj__idpa) for nwkj__idpa in range(redvar_offsets[
                mecb__wotyl], redvar_offsets[mecb__wotyl + 1])])
            mtn__pprng = ', '.join(['recv_arrs[{}][i]'.format(nwkj__idpa) for
                nwkj__idpa in range(redvar_offsets[mecb__wotyl],
                redvar_offsets[mecb__wotyl + 1])])
            if mtn__pprng:
                aan__jma += '  {} = combine_vars_{}({}, {})\n'.format(lrss__qgx
                    , mecb__wotyl, lrss__qgx, mtn__pprng)
    aan__jma += '  return\n'
    jzaji__yjt = {}
    for nwkj__idpa, omprp__sbzb in enumerate(combine_funcs):
        jzaji__yjt['combine_vars_{}'.format(nwkj__idpa)] = omprp__sbzb
    nvoe__fyo = {}
    exec(aan__jma, jzaji__yjt, nvoe__fyo)
    jrgbj__kqaog = nvoe__fyo['combine_all_f']
    f_ir = compile_to_numba_ir(jrgbj__kqaog, jzaji__yjt)
    psovv__qba = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    hzrtc__pzpx = numba.core.target_extension.dispatcher_registry[cpu_target](
        jrgbj__kqaog)
    hzrtc__pzpx.add_overload(psovv__qba)
    return hzrtc__pzpx


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    sui__bna = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types])
    out_col_typs = types.Tuple(out_col_typs)
    roknh__nzqio = len(redvar_offsets) - 1
    ywsoq__bgk = redvar_offsets[roknh__nzqio]
    aan__jma = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert roknh__nzqio == 1
        for mecb__wotyl in range(len(pivot_values)):
            epst__esn = ywsoq__bgk * mecb__wotyl
            lrss__qgx = ', '.join(['redvar_arrs[{}][j]'.format(nwkj__idpa) for
                nwkj__idpa in range(epst__esn + redvar_offsets[0], 
                epst__esn + redvar_offsets[1])])
            aan__jma += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                mecb__wotyl, lrss__qgx)
    else:
        for mecb__wotyl in range(roknh__nzqio):
            lrss__qgx = ', '.join(['redvar_arrs[{}][j]'.format(nwkj__idpa) for
                nwkj__idpa in range(redvar_offsets[mecb__wotyl],
                redvar_offsets[mecb__wotyl + 1])])
            aan__jma += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                mecb__wotyl, mecb__wotyl, lrss__qgx)
    aan__jma += '  return\n'
    jzaji__yjt = {}
    for nwkj__idpa, omprp__sbzb in enumerate(eval_funcs):
        jzaji__yjt['eval_vars_{}'.format(nwkj__idpa)] = omprp__sbzb
    nvoe__fyo = {}
    exec(aan__jma, jzaji__yjt, nvoe__fyo)
    jqdi__akudh = nvoe__fyo['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(jqdi__akudh)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    qkz__mjqx = len(var_types)
    bvdc__poefk = [f'in{nwkj__idpa}' for nwkj__idpa in range(qkz__mjqx)]
    qrr__zkqv = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    zoy__inu = qrr__zkqv(0)
    aan__jma = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        bvdc__poefk))
    nvoe__fyo = {}
    exec(aan__jma, {'_zero': zoy__inu}, nvoe__fyo)
    rfotc__vgy = nvoe__fyo['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(rfotc__vgy, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': zoy__inu}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    rnau__larz = []
    for nwkj__idpa, brxni__qzbdc in enumerate(reduce_vars):
        rnau__larz.append(ir.Assign(block.body[nwkj__idpa].target,
            brxni__qzbdc, brxni__qzbdc.loc))
        for ihlm__kibks in brxni__qzbdc.versioned_names:
            rnau__larz.append(ir.Assign(brxni__qzbdc, ir.Var(brxni__qzbdc.
                scope, ihlm__kibks, brxni__qzbdc.loc), brxni__qzbdc.loc))
    block.body = block.body[:qkz__mjqx] + rnau__larz + eval_nodes
    aad__tiu = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        qrr__zkqv, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    hzrtc__pzpx = numba.core.target_extension.dispatcher_registry[cpu_target](
        rfotc__vgy)
    hzrtc__pzpx.add_overload(aad__tiu)
    return hzrtc__pzpx


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    qkz__mjqx = len(redvars)
    zcwx__drm = [f'v{nwkj__idpa}' for nwkj__idpa in range(qkz__mjqx)]
    bvdc__poefk = [f'in{nwkj__idpa}' for nwkj__idpa in range(qkz__mjqx)]
    aan__jma = 'def agg_combine({}):\n'.format(', '.join(zcwx__drm +
        bvdc__poefk))
    hsjt__ctub = wrap_parfor_blocks(parfor)
    jvdaz__siobl = find_topo_order(hsjt__ctub)
    jvdaz__siobl = jvdaz__siobl[1:]
    unwrap_parfor_blocks(parfor)
    gqvmr__dlgi = {}
    pxg__syvjz = []
    for cffw__livxz in jvdaz__siobl:
        nhfv__kcp = parfor.loop_body[cffw__livxz]
        for boi__uhlx in nhfv__kcp.body:
            if is_call_assign(boi__uhlx) and guard(find_callname, f_ir,
                boi__uhlx.value) == ('__special_combine', 'bodo.ir.aggregate'):
                args = boi__uhlx.value.args
                kqava__cuo = []
                ptmr__fqetm = []
                for brxni__qzbdc in args[:-1]:
                    ind = redvars.index(brxni__qzbdc.name)
                    pxg__syvjz.append(ind)
                    kqava__cuo.append('v{}'.format(ind))
                    ptmr__fqetm.append('in{}'.format(ind))
                mui__ymko = '__special_combine__{}'.format(len(gqvmr__dlgi))
                aan__jma += '    ({},) = {}({})\n'.format(', '.join(
                    kqava__cuo), mui__ymko, ', '.join(kqava__cuo + ptmr__fqetm)
                    )
                jwkwq__lkl = ir.Expr.call(args[-1], [], (), nhfv__kcp.loc)
                fbins__fyktt = guard(find_callname, f_ir, jwkwq__lkl)
                assert fbins__fyktt == ('_var_combine', 'bodo.ir.aggregate')
                fbins__fyktt = bodo.ir.aggregate._var_combine
                gqvmr__dlgi[mui__ymko] = fbins__fyktt
            if is_assign(boi__uhlx) and boi__uhlx.target.name in redvars:
                etf__wvhs = boi__uhlx.target.name
                ind = redvars.index(etf__wvhs)
                if ind in pxg__syvjz:
                    continue
                if len(f_ir._definitions[etf__wvhs]) == 2:
                    var_def = f_ir._definitions[etf__wvhs][0]
                    aan__jma += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[etf__wvhs][1]
                    aan__jma += _match_reduce_def(var_def, f_ir, ind)
    aan__jma += '    return {}'.format(', '.join(['v{}'.format(nwkj__idpa) for
        nwkj__idpa in range(qkz__mjqx)]))
    nvoe__fyo = {}
    exec(aan__jma, {}, nvoe__fyo)
    zrpf__wcye = nvoe__fyo['agg_combine']
    arg_typs = tuple(2 * var_types)
    jzaji__yjt = {'numba': numba, 'bodo': bodo, 'np': np}
    jzaji__yjt.update(gqvmr__dlgi)
    f_ir = compile_to_numba_ir(zrpf__wcye, jzaji__yjt, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    qrr__zkqv = pm.typemap[block.body[-1].value.name]
    fumzl__lowmu = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        qrr__zkqv, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    hzrtc__pzpx = numba.core.target_extension.dispatcher_registry[cpu_target](
        zrpf__wcye)
    hzrtc__pzpx.add_overload(fumzl__lowmu)
    return hzrtc__pzpx


def _match_reduce_def(var_def, f_ir, ind):
    aan__jma = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        aan__jma = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        dzgoa__ire = guard(find_callname, f_ir, var_def)
        if dzgoa__ire == ('min', 'builtins'):
            aan__jma = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if dzgoa__ire == ('max', 'builtins'):
            aan__jma = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return aan__jma


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    qkz__mjqx = len(redvars)
    zivkp__ffoeg = 1
    wymb__eohaj = []
    for nwkj__idpa in range(zivkp__ffoeg):
        tdgkm__vsqlx = ir.Var(arr_var.scope, f'$input{nwkj__idpa}', arr_var.loc
            )
        wymb__eohaj.append(tdgkm__vsqlx)
    nfqfr__fnkrn = parfor.loop_nests[0].index_variable
    nbjph__vndr = [0] * qkz__mjqx
    for nhfv__kcp in parfor.loop_body.values():
        buyq__ybiv = []
        for boi__uhlx in nhfv__kcp.body:
            if is_var_assign(boi__uhlx
                ) and boi__uhlx.value.name == nfqfr__fnkrn.name:
                continue
            if is_getitem(boi__uhlx
                ) and boi__uhlx.value.value.name == arr_var.name:
                boi__uhlx.value = wymb__eohaj[0]
            if is_call_assign(boi__uhlx) and guard(find_callname, pm.
                func_ir, boi__uhlx.value) == ('isna', 'bodo.libs.array_kernels'
                ) and boi__uhlx.value.args[0].name == arr_var.name:
                boi__uhlx.value = ir.Const(False, boi__uhlx.target.loc)
            if is_assign(boi__uhlx) and boi__uhlx.target.name in redvars:
                ind = redvars.index(boi__uhlx.target.name)
                nbjph__vndr[ind] = boi__uhlx.target
            buyq__ybiv.append(boi__uhlx)
        nhfv__kcp.body = buyq__ybiv
    zcwx__drm = ['v{}'.format(nwkj__idpa) for nwkj__idpa in range(qkz__mjqx)]
    bvdc__poefk = ['in{}'.format(nwkj__idpa) for nwkj__idpa in range(
        zivkp__ffoeg)]
    aan__jma = 'def agg_update({}):\n'.format(', '.join(zcwx__drm +
        bvdc__poefk))
    aan__jma += '    __update_redvars()\n'
    aan__jma += '    return {}'.format(', '.join(['v{}'.format(nwkj__idpa) for
        nwkj__idpa in range(qkz__mjqx)]))
    nvoe__fyo = {}
    exec(aan__jma, {}, nvoe__fyo)
    ntz__bsv = nvoe__fyo['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * zivkp__ffoeg)
    f_ir = compile_to_numba_ir(ntz__bsv, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    jbwf__yppoo = f_ir.blocks.popitem()[1].body
    qrr__zkqv = pm.typemap[jbwf__yppoo[-1].value.name]
    hsjt__ctub = wrap_parfor_blocks(parfor)
    jvdaz__siobl = find_topo_order(hsjt__ctub)
    jvdaz__siobl = jvdaz__siobl[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    tzk__qdbwf = f_ir.blocks[jvdaz__siobl[0]]
    jdgid__rxdk = f_ir.blocks[jvdaz__siobl[-1]]
    ihgm__vkn = jbwf__yppoo[:qkz__mjqx + zivkp__ffoeg]
    if qkz__mjqx > 1:
        cbd__fpds = jbwf__yppoo[-3:]
        assert is_assign(cbd__fpds[0]) and isinstance(cbd__fpds[0].value,
            ir.Expr) and cbd__fpds[0].value.op == 'build_tuple'
    else:
        cbd__fpds = jbwf__yppoo[-2:]
    for nwkj__idpa in range(qkz__mjqx):
        yue__hnai = jbwf__yppoo[nwkj__idpa].target
        atao__ufy = ir.Assign(yue__hnai, nbjph__vndr[nwkj__idpa], yue__hnai.loc
            )
        ihgm__vkn.append(atao__ufy)
    for nwkj__idpa in range(qkz__mjqx, qkz__mjqx + zivkp__ffoeg):
        yue__hnai = jbwf__yppoo[nwkj__idpa].target
        atao__ufy = ir.Assign(yue__hnai, wymb__eohaj[nwkj__idpa - qkz__mjqx
            ], yue__hnai.loc)
        ihgm__vkn.append(atao__ufy)
    tzk__qdbwf.body = ihgm__vkn + tzk__qdbwf.body
    azrse__nic = []
    for nwkj__idpa in range(qkz__mjqx):
        yue__hnai = jbwf__yppoo[nwkj__idpa].target
        atao__ufy = ir.Assign(nbjph__vndr[nwkj__idpa], yue__hnai, yue__hnai.loc
            )
        azrse__nic.append(atao__ufy)
    jdgid__rxdk.body += azrse__nic + cbd__fpds
    phw__rpmgm = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        qrr__zkqv, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    hzrtc__pzpx = numba.core.target_extension.dispatcher_registry[cpu_target](
        ntz__bsv)
    hzrtc__pzpx.add_overload(phw__rpmgm)
    return hzrtc__pzpx


def _rm_arg_agg_block(block, typemap):
    lug__kxmc = []
    arr_var = None
    for nwkj__idpa, boi__uhlx in enumerate(block.body):
        if is_assign(boi__uhlx) and isinstance(boi__uhlx.value, ir.Arg):
            arr_var = boi__uhlx.target
            fuo__fxkt = typemap[arr_var.name]
            if not isinstance(fuo__fxkt, types.ArrayCompatible):
                lug__kxmc += block.body[nwkj__idpa + 1:]
                break
            fasen__rigj = block.body[nwkj__idpa + 1]
            assert is_assign(fasen__rigj) and isinstance(fasen__rigj.value,
                ir.Expr
                ) and fasen__rigj.value.op == 'getattr' and fasen__rigj.value.attr == 'shape' and fasen__rigj.value.value.name == arr_var.name
            unn__muha = fasen__rigj.target
            dnh__bspm = block.body[nwkj__idpa + 2]
            assert is_assign(dnh__bspm) and isinstance(dnh__bspm.value, ir.Expr
                ) and dnh__bspm.value.op == 'static_getitem' and dnh__bspm.value.value.name == unn__muha.name
            lug__kxmc += block.body[nwkj__idpa + 3:]
            break
        lug__kxmc.append(boi__uhlx)
    return lug__kxmc, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    hsjt__ctub = wrap_parfor_blocks(parfor)
    jvdaz__siobl = find_topo_order(hsjt__ctub)
    jvdaz__siobl = jvdaz__siobl[1:]
    unwrap_parfor_blocks(parfor)
    for cffw__livxz in reversed(jvdaz__siobl):
        for boi__uhlx in reversed(parfor.loop_body[cffw__livxz].body):
            if isinstance(boi__uhlx, ir.Assign) and (boi__uhlx.target.name in
                parfor_params or boi__uhlx.target.name in var_to_param):
                zqomb__hgch = boi__uhlx.target.name
                rhs = boi__uhlx.value
                naycg__kyer = (zqomb__hgch if zqomb__hgch in parfor_params else
                    var_to_param[zqomb__hgch])
                wqf__yfw = []
                if isinstance(rhs, ir.Var):
                    wqf__yfw = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    wqf__yfw = [brxni__qzbdc.name for brxni__qzbdc in
                        boi__uhlx.value.list_vars()]
                param_uses[naycg__kyer].extend(wqf__yfw)
                for brxni__qzbdc in wqf__yfw:
                    var_to_param[brxni__qzbdc] = naycg__kyer
            if isinstance(boi__uhlx, Parfor):
                get_parfor_reductions(boi__uhlx, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for pzulx__ool, wqf__yfw in param_uses.items():
        if pzulx__ool in wqf__yfw and pzulx__ool not in reduce_varnames:
            reduce_varnames.append(pzulx__ool)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
