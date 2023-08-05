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
            ggn__lnxx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            pvc__dkq = cgutils.get_or_insert_function(builder.module,
                ggn__lnxx, sym._literal_value)
            builder.call(pvc__dkq, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            ggn__lnxx = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            pvc__dkq = cgutils.get_or_insert_function(builder.module,
                ggn__lnxx, sym._literal_value)
            builder.call(pvc__dkq, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            ggn__lnxx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            pvc__dkq = cgutils.get_or_insert_function(builder.module,
                ggn__lnxx, sym._literal_value)
            builder.call(pvc__dkq, [context.get_constant_null(sig.args[0]),
                context.get_constant_null(sig.args[1]), context.
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
        eqfyf__copfq = True
        rdcnq__eiw = 1
        tab__onkx = -1
        if isinstance(rhs, ir.Expr):
            for oxmly__xyvu in rhs.kws:
                if func_name in list_cumulative:
                    if oxmly__xyvu[0] == 'skipna':
                        eqfyf__copfq = guard(find_const, func_ir,
                            oxmly__xyvu[1])
                        if not isinstance(eqfyf__copfq, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if oxmly__xyvu[0] == 'dropna':
                        eqfyf__copfq = guard(find_const, func_ir,
                            oxmly__xyvu[1])
                        if not isinstance(eqfyf__copfq, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            rdcnq__eiw = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', rdcnq__eiw)
            rdcnq__eiw = guard(find_const, func_ir, rdcnq__eiw)
        if func_name == 'head':
            tab__onkx = get_call_expr_arg('head', rhs.args, dict(rhs.kws), 
                0, 'n', 5)
            if not isinstance(tab__onkx, int):
                tab__onkx = guard(find_const, func_ir, tab__onkx)
            if tab__onkx < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = eqfyf__copfq
        func.periods = rdcnq__eiw
        func.head_n = tab__onkx
        if func_name == 'transform':
            kws = dict(rhs.kws)
            jqf__kcpwn = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            qrhq__jtk = typemap[jqf__kcpwn.name]
            dbjvt__xjf = None
            if isinstance(qrhq__jtk, str):
                dbjvt__xjf = qrhq__jtk
            elif is_overload_constant_str(qrhq__jtk):
                dbjvt__xjf = get_overload_const_str(qrhq__jtk)
            elif bodo.utils.typing.is_builtin_function(qrhq__jtk):
                dbjvt__xjf = bodo.utils.typing.get_builtin_function_name(
                    qrhq__jtk)
            if dbjvt__xjf not in bodo.ir.aggregate.supported_transform_funcs[:
                ]:
                raise BodoError(f'unsupported transform function {dbjvt__xjf}')
            func.transform_func = supported_agg_funcs.index(dbjvt__xjf)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    jqf__kcpwn = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if jqf__kcpwn == '':
        qrhq__jtk = types.none
    else:
        qrhq__jtk = typemap[jqf__kcpwn.name]
    if is_overload_constant_dict(qrhq__jtk):
        mlx__izeed = get_overload_constant_dict(qrhq__jtk)
        aqe__yda = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in mlx__izeed.values()]
        return aqe__yda
    if qrhq__jtk == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(qrhq__jtk, types.BaseTuple):
        aqe__yda = []
        qgkys__ujgn = 0
        for t in qrhq__jtk.types:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                aqe__yda.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>':
                    func.fname = '<lambda_' + str(qgkys__ujgn) + '>'
                    qgkys__ujgn += 1
                aqe__yda.append(func)
        return [aqe__yda]
    if is_overload_constant_str(qrhq__jtk):
        func_name = get_overload_const_str(qrhq__jtk)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(qrhq__jtk):
        func_name = bodo.utils.typing.get_builtin_function_name(qrhq__jtk)
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
        qgkys__ujgn = 0
        ngo__fvm = []
        for izb__jrp in f_val:
            func = get_agg_func_udf(func_ir, izb__jrp, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{qgkys__ujgn}>'
                qgkys__ujgn += 1
            ngo__fvm.append(func)
        return ngo__fvm
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
    dbjvt__xjf = code.co_name
    return dbjvt__xjf


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
            zee__xku = types.DType(args[0])
            return signature(zee__xku, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    kxioo__rxvt = nobs_a + nobs_b
    ura__bip = (nobs_a * mean_a + nobs_b * mean_b) / kxioo__rxvt
    melg__craj = mean_b - mean_a
    dopr__sdebj = (ssqdm_a + ssqdm_b + melg__craj * melg__craj * nobs_a *
        nobs_b / kxioo__rxvt)
    return dopr__sdebj, ura__bip, kxioo__rxvt


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
        nyrtg__bpsr = ''
        for xvjd__wowx, dwn__pii in self.df_out_vars.items():
            nyrtg__bpsr += "'{}':{}, ".format(xvjd__wowx, dwn__pii.name)
        rup__zijl = '{}{{{}}}'.format(self.df_out, nyrtg__bpsr)
        vowt__thcuk = ''
        for xvjd__wowx, dwn__pii in self.df_in_vars.items():
            vowt__thcuk += "'{}':{}, ".format(xvjd__wowx, dwn__pii.name)
        ybtm__jce = '{}{{{}}}'.format(self.df_in, vowt__thcuk)
        iqev__hos = 'pivot {}:{}'.format(self.pivot_arr.name, self.pivot_values
            ) if self.pivot_arr is not None else ''
        key_names = ','.join(self.key_names)
        bkwj__idn = ','.join([dwn__pii.name for dwn__pii in self.key_arrs])
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(rup__zijl,
            ybtm__jce, key_names, bkwj__idn, iqev__hos)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        dkk__hrs, zrim__gpqxx = self.gb_info_out.pop(out_col_name)
        if dkk__hrs is None and not self.is_crosstab:
            return
        qlzlx__mgrt = self.gb_info_in[dkk__hrs]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for afc__ehrdq, (func, nyrtg__bpsr) in enumerate(qlzlx__mgrt):
                try:
                    nyrtg__bpsr.remove(out_col_name)
                    if len(nyrtg__bpsr) == 0:
                        qlzlx__mgrt.pop(afc__ehrdq)
                        break
                except ValueError as wgxrl__cus:
                    continue
        else:
            for afc__ehrdq, (func, gtld__nvri) in enumerate(qlzlx__mgrt):
                if gtld__nvri == out_col_name:
                    qlzlx__mgrt.pop(afc__ehrdq)
                    break
        if len(qlzlx__mgrt) == 0:
            self.gb_info_in.pop(dkk__hrs)
            self.df_in_vars.pop(dkk__hrs)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({dwn__pii.name for dwn__pii in aggregate_node.key_arrs})
    use_set.update({dwn__pii.name for dwn__pii in aggregate_node.df_in_vars
        .values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({dwn__pii.name for dwn__pii in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({dwn__pii.name for dwn__pii in aggregate_node.
            out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    cey__qwbs = [hzunu__msiu for hzunu__msiu, nov__hyb in aggregate_node.
        df_out_vars.items() if nov__hyb.name not in lives]
    for gsqp__bszpo in cey__qwbs:
        aggregate_node.remove_out_col(gsqp__bszpo)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(dwn__pii.name not in lives for
        dwn__pii in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    zle__frlom = set(dwn__pii.name for dwn__pii in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        zle__frlom.update({dwn__pii.name for dwn__pii in aggregate_node.
            out_key_vars})
    return set(), zle__frlom


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for afc__ehrdq in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[afc__ehrdq] = replace_vars_inner(aggregate_node
            .key_arrs[afc__ehrdq], var_dict)
    for hzunu__msiu in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[hzunu__msiu] = replace_vars_inner(
            aggregate_node.df_in_vars[hzunu__msiu], var_dict)
    for hzunu__msiu in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[hzunu__msiu] = replace_vars_inner(
            aggregate_node.df_out_vars[hzunu__msiu], var_dict)
    if aggregate_node.out_key_vars is not None:
        for afc__ehrdq in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[afc__ehrdq] = replace_vars_inner(
                aggregate_node.out_key_vars[afc__ehrdq], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for afc__ehrdq in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[afc__ehrdq] = visit_vars_inner(aggregate_node
            .key_arrs[afc__ehrdq], callback, cbdata)
    for hzunu__msiu in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[hzunu__msiu] = visit_vars_inner(
            aggregate_node.df_in_vars[hzunu__msiu], callback, cbdata)
    for hzunu__msiu in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[hzunu__msiu] = visit_vars_inner(
            aggregate_node.df_out_vars[hzunu__msiu], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for afc__ehrdq in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[afc__ehrdq] = visit_vars_inner(
                aggregate_node.out_key_vars[afc__ehrdq], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    wka__qfgu = []
    for qwao__msx in aggregate_node.key_arrs:
        vcc__gkn = equiv_set.get_shape(qwao__msx)
        if vcc__gkn:
            wka__qfgu.append(vcc__gkn[0])
    if aggregate_node.pivot_arr is not None:
        vcc__gkn = equiv_set.get_shape(aggregate_node.pivot_arr)
        if vcc__gkn:
            wka__qfgu.append(vcc__gkn[0])
    for nov__hyb in aggregate_node.df_in_vars.values():
        vcc__gkn = equiv_set.get_shape(nov__hyb)
        if vcc__gkn:
            wka__qfgu.append(vcc__gkn[0])
    if len(wka__qfgu) > 1:
        equiv_set.insert_equiv(*wka__qfgu)
    ggav__fartm = []
    wka__qfgu = []
    tygk__umyft = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        tygk__umyft.extend(aggregate_node.out_key_vars)
    for nov__hyb in tygk__umyft:
        swrx__rjng = typemap[nov__hyb.name]
        ilx__saw = array_analysis._gen_shape_call(equiv_set, nov__hyb,
            swrx__rjng.ndim, None, ggav__fartm)
        equiv_set.insert_equiv(nov__hyb, ilx__saw)
        wka__qfgu.append(ilx__saw[0])
        equiv_set.define(nov__hyb, set())
    if len(wka__qfgu) > 1:
        equiv_set.insert_equiv(*wka__qfgu)
    return [], ggav__fartm


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    oxvit__qnw = Distribution.OneD
    for nov__hyb in aggregate_node.df_in_vars.values():
        oxvit__qnw = Distribution(min(oxvit__qnw.value, array_dists[
            nov__hyb.name].value))
    for qwao__msx in aggregate_node.key_arrs:
        oxvit__qnw = Distribution(min(oxvit__qnw.value, array_dists[
            qwao__msx.name].value))
    if aggregate_node.pivot_arr is not None:
        oxvit__qnw = Distribution(min(oxvit__qnw.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = oxvit__qnw
    for nov__hyb in aggregate_node.df_in_vars.values():
        array_dists[nov__hyb.name] = oxvit__qnw
    for qwao__msx in aggregate_node.key_arrs:
        array_dists[qwao__msx.name] = oxvit__qnw
    kdfw__pxlz = Distribution.OneD_Var
    for nov__hyb in aggregate_node.df_out_vars.values():
        if nov__hyb.name in array_dists:
            kdfw__pxlz = Distribution(min(kdfw__pxlz.value, array_dists[
                nov__hyb.name].value))
    if aggregate_node.out_key_vars is not None:
        for nov__hyb in aggregate_node.out_key_vars:
            if nov__hyb.name in array_dists:
                kdfw__pxlz = Distribution(min(kdfw__pxlz.value, array_dists
                    [nov__hyb.name].value))
    kdfw__pxlz = Distribution(min(kdfw__pxlz.value, oxvit__qnw.value))
    for nov__hyb in aggregate_node.df_out_vars.values():
        array_dists[nov__hyb.name] = kdfw__pxlz
    if aggregate_node.out_key_vars is not None:
        for yezls__mop in aggregate_node.out_key_vars:
            array_dists[yezls__mop.name] = kdfw__pxlz
    if kdfw__pxlz != Distribution.OneD_Var:
        for qwao__msx in aggregate_node.key_arrs:
            array_dists[qwao__msx.name] = kdfw__pxlz
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = kdfw__pxlz
        for nov__hyb in aggregate_node.df_in_vars.values():
            array_dists[nov__hyb.name] = kdfw__pxlz


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for nov__hyb in agg_node.df_out_vars.values():
        definitions[nov__hyb.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for yezls__mop in agg_node.out_key_vars:
            definitions[yezls__mop.name].append(agg_node)
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
        for dwn__pii in (list(agg_node.df_in_vars.values()) + list(agg_node
            .df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[dwn__pii.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                dwn__pii.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    xuy__dwklt = tuple(typemap[dwn__pii.name] for dwn__pii in agg_node.key_arrs
        )
    zffjd__dzyr = [dwn__pii for gsyj__dpg, dwn__pii in agg_node.df_in_vars.
        items()]
    nuj__htxl = [dwn__pii for gsyj__dpg, dwn__pii in agg_node.df_out_vars.
        items()]
    in_col_typs = []
    aqe__yda = []
    if agg_node.pivot_arr is not None:
        for dkk__hrs, qlzlx__mgrt in agg_node.gb_info_in.items():
            for func, zrim__gpqxx in qlzlx__mgrt:
                if dkk__hrs is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[dkk__hrs
                        ].name])
                aqe__yda.append(func)
    else:
        for dkk__hrs, func in agg_node.gb_info_out.values():
            if dkk__hrs is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[dkk__hrs].name])
            aqe__yda.append(func)
    out_col_typs = tuple(typemap[dwn__pii.name] for dwn__pii in nuj__htxl)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(xuy__dwklt + tuple(typemap[dwn__pii.name] for dwn__pii in
        zffjd__dzyr) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    yyr__qwaxj = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for afc__ehrdq, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            yyr__qwaxj.update({f'in_cat_dtype_{afc__ehrdq}': in_col_typ})
    for afc__ehrdq, ctdwr__sshi in enumerate(out_col_typs):
        if isinstance(ctdwr__sshi, bodo.CategoricalArrayType):
            yyr__qwaxj.update({f'out_cat_dtype_{afc__ehrdq}': ctdwr__sshi})
    udf_func_struct = get_udf_func_struct(aqe__yda, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    kzd__jed = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    yyr__qwaxj.update({'pd': pd, 'pre_alloc_string_array':
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
            yyr__qwaxj.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            yyr__qwaxj.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    jdj__bip = compile_to_numba_ir(kzd__jed, yyr__qwaxj, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    vfzo__xbnr = []
    if agg_node.pivot_arr is None:
        ouv__vhta = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        trca__mvhvg = ir.Var(ouv__vhta, mk_unique_var('dummy_none'), loc)
        typemap[trca__mvhvg.name] = types.none
        vfzo__xbnr.append(ir.Assign(ir.Const(None, loc), trca__mvhvg, loc))
        zffjd__dzyr.append(trca__mvhvg)
    else:
        zffjd__dzyr.append(agg_node.pivot_arr)
    replace_arg_nodes(jdj__bip, agg_node.key_arrs + zffjd__dzyr)
    zjjef__yms = jdj__bip.body[-3]
    assert is_assign(zjjef__yms) and isinstance(zjjef__yms.value, ir.Expr
        ) and zjjef__yms.value.op == 'build_tuple'
    vfzo__xbnr += jdj__bip.body[:-3]
    tygk__umyft = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        tygk__umyft += agg_node.out_key_vars
    for afc__ehrdq, avmow__tiug in enumerate(tygk__umyft):
        aruu__bubhf = zjjef__yms.value.items[afc__ehrdq]
        vfzo__xbnr.append(ir.Assign(aruu__bubhf, avmow__tiug, avmow__tiug.loc))
    return vfzo__xbnr


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        jmz__miqtt = args[0]
        dtype = types.Tuple([t.dtype for t in jmz__miqtt.types]) if isinstance(
            jmz__miqtt, types.BaseTuple) else jmz__miqtt.dtype
        if isinstance(jmz__miqtt, types.BaseTuple) and len(jmz__miqtt.types
            ) == 1:
            dtype = jmz__miqtt.types[0].dtype
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
        wcga__qtcok = args[0]
        if wcga__qtcok == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    xag__peudn = context.compile_internal(builder, lambda a: False, sig, args)
    return xag__peudn


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        otriz__bbt = IntDtype(t.dtype).name
        assert otriz__bbt.endswith('Dtype()')
        otriz__bbt = otriz__bbt[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{otriz__bbt}'))"
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
        rwhf__keaas = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {rwhf__keaas}_cat_dtype_{colnum})'
            )
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
    essq__lhnlg = udf_func_struct.var_typs
    zpemq__ymu = len(essq__lhnlg)
    fnqu__gowi = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    fnqu__gowi += '    if is_null_pointer(in_table):\n'
    fnqu__gowi += '        return\n'
    fnqu__gowi += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in essq__lhnlg]), 
        ',' if len(essq__lhnlg) == 1 else '')
    cgkl__foffq = n_keys
    inr__yluf = []
    redvar_offsets = []
    uny__jbhpw = []
    if do_combine:
        for afc__ehrdq, izb__jrp in enumerate(allfuncs):
            if izb__jrp.ftype != 'udf':
                cgkl__foffq += izb__jrp.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(cgkl__foffq, cgkl__foffq +
                    izb__jrp.n_redvars))
                cgkl__foffq += izb__jrp.n_redvars
                uny__jbhpw.append(data_in_typs_[func_idx_to_in_col[afc__ehrdq]]
                    )
                inr__yluf.append(func_idx_to_in_col[afc__ehrdq] + n_keys)
    else:
        for afc__ehrdq, izb__jrp in enumerate(allfuncs):
            if izb__jrp.ftype != 'udf':
                cgkl__foffq += izb__jrp.ncols_post_shuffle
            else:
                redvar_offsets += list(range(cgkl__foffq + 1, cgkl__foffq +
                    1 + izb__jrp.n_redvars))
                cgkl__foffq += izb__jrp.n_redvars + 1
                uny__jbhpw.append(data_in_typs_[func_idx_to_in_col[afc__ehrdq]]
                    )
                inr__yluf.append(func_idx_to_in_col[afc__ehrdq] + n_keys)
    assert len(redvar_offsets) == zpemq__ymu
    nvo__kogjm = len(uny__jbhpw)
    yxj__hsfli = []
    for afc__ehrdq, t in enumerate(uny__jbhpw):
        yxj__hsfli.append(_gen_dummy_alloc(t, afc__ehrdq, True))
    fnqu__gowi += '    data_in_dummy = ({}{})\n'.format(','.join(yxj__hsfli
        ), ',' if len(uny__jbhpw) == 1 else '')
    fnqu__gowi += """
    # initialize redvar cols
"""
    fnqu__gowi += '    init_vals = __init_func()\n'
    for afc__ehrdq in range(zpemq__ymu):
        fnqu__gowi += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(afc__ehrdq, redvar_offsets[afc__ehrdq], afc__ehrdq))
        fnqu__gowi += '    incref(redvar_arr_{})\n'.format(afc__ehrdq)
        fnqu__gowi += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            afc__ehrdq, afc__ehrdq)
    fnqu__gowi += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(afc__ehrdq) for afc__ehrdq in range(zpemq__ymu)]), ',' if 
        zpemq__ymu == 1 else '')
    fnqu__gowi += '\n'
    for afc__ehrdq in range(nvo__kogjm):
        fnqu__gowi += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(afc__ehrdq, inr__yluf[afc__ehrdq], afc__ehrdq))
        fnqu__gowi += '    incref(data_in_{})\n'.format(afc__ehrdq)
    fnqu__gowi += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(afc__ehrdq) for afc__ehrdq in range(nvo__kogjm)]), ',' if 
        nvo__kogjm == 1 else '')
    fnqu__gowi += '\n'
    fnqu__gowi += '    for i in range(len(data_in_0)):\n'
    fnqu__gowi += '        w_ind = row_to_group[i]\n'
    fnqu__gowi += '        if w_ind != -1:\n'
    fnqu__gowi += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    yjz__pseix = {}
    exec(fnqu__gowi, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yjz__pseix)
    return yjz__pseix['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    essq__lhnlg = udf_func_struct.var_typs
    zpemq__ymu = len(essq__lhnlg)
    fnqu__gowi = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    fnqu__gowi += '    if is_null_pointer(in_table):\n'
    fnqu__gowi += '        return\n'
    fnqu__gowi += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in essq__lhnlg]), 
        ',' if len(essq__lhnlg) == 1 else '')
    rfti__cvsy = n_keys
    kojm__hivzl = n_keys
    wuibp__wtxk = []
    ruju__bqrm = []
    for izb__jrp in allfuncs:
        if izb__jrp.ftype != 'udf':
            rfti__cvsy += izb__jrp.ncols_pre_shuffle
            kojm__hivzl += izb__jrp.ncols_post_shuffle
        else:
            wuibp__wtxk += list(range(rfti__cvsy, rfti__cvsy + izb__jrp.
                n_redvars))
            ruju__bqrm += list(range(kojm__hivzl + 1, kojm__hivzl + 1 +
                izb__jrp.n_redvars))
            rfti__cvsy += izb__jrp.n_redvars
            kojm__hivzl += 1 + izb__jrp.n_redvars
    assert len(wuibp__wtxk) == zpemq__ymu
    fnqu__gowi += """
    # initialize redvar cols
"""
    fnqu__gowi += '    init_vals = __init_func()\n'
    for afc__ehrdq in range(zpemq__ymu):
        fnqu__gowi += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(afc__ehrdq, ruju__bqrm[afc__ehrdq], afc__ehrdq))
        fnqu__gowi += '    incref(redvar_arr_{})\n'.format(afc__ehrdq)
        fnqu__gowi += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            afc__ehrdq, afc__ehrdq)
    fnqu__gowi += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(afc__ehrdq) for afc__ehrdq in range(zpemq__ymu)]), ',' if 
        zpemq__ymu == 1 else '')
    fnqu__gowi += '\n'
    for afc__ehrdq in range(zpemq__ymu):
        fnqu__gowi += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(afc__ehrdq, wuibp__wtxk[afc__ehrdq], afc__ehrdq))
        fnqu__gowi += '    incref(recv_redvar_arr_{})\n'.format(afc__ehrdq)
    fnqu__gowi += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(afc__ehrdq) for afc__ehrdq in range(
        zpemq__ymu)]), ',' if zpemq__ymu == 1 else '')
    fnqu__gowi += '\n'
    if zpemq__ymu:
        fnqu__gowi += '    for i in range(len(recv_redvar_arr_0)):\n'
        fnqu__gowi += '        w_ind = row_to_group[i]\n'
        fnqu__gowi += """        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)
"""
    yjz__pseix = {}
    exec(fnqu__gowi, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yjz__pseix)
    return yjz__pseix['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    essq__lhnlg = udf_func_struct.var_typs
    zpemq__ymu = len(essq__lhnlg)
    cgkl__foffq = n_keys
    redvar_offsets = []
    uod__vbrx = []
    out_data_typs = []
    for afc__ehrdq, izb__jrp in enumerate(allfuncs):
        if izb__jrp.ftype != 'udf':
            cgkl__foffq += izb__jrp.ncols_post_shuffle
        else:
            uod__vbrx.append(cgkl__foffq)
            redvar_offsets += list(range(cgkl__foffq + 1, cgkl__foffq + 1 +
                izb__jrp.n_redvars))
            cgkl__foffq += 1 + izb__jrp.n_redvars
            out_data_typs.append(out_data_typs_[afc__ehrdq])
    assert len(redvar_offsets) == zpemq__ymu
    nvo__kogjm = len(out_data_typs)
    fnqu__gowi = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    fnqu__gowi += '    if is_null_pointer(table):\n'
    fnqu__gowi += '        return\n'
    fnqu__gowi += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in essq__lhnlg]), 
        ',' if len(essq__lhnlg) == 1 else '')
    fnqu__gowi += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for afc__ehrdq in range(zpemq__ymu):
        fnqu__gowi += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(afc__ehrdq, redvar_offsets[afc__ehrdq], afc__ehrdq))
        fnqu__gowi += '    incref(redvar_arr_{})\n'.format(afc__ehrdq)
    fnqu__gowi += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(afc__ehrdq) for afc__ehrdq in range(zpemq__ymu)]), ',' if 
        zpemq__ymu == 1 else '')
    fnqu__gowi += '\n'
    for afc__ehrdq in range(nvo__kogjm):
        fnqu__gowi += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(afc__ehrdq, uod__vbrx[afc__ehrdq], afc__ehrdq))
        fnqu__gowi += '    incref(data_out_{})\n'.format(afc__ehrdq)
    fnqu__gowi += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(afc__ehrdq) for afc__ehrdq in range(nvo__kogjm)]), ',' if 
        nvo__kogjm == 1 else '')
    fnqu__gowi += '\n'
    fnqu__gowi += '    for i in range(len(data_out_0)):\n'
    fnqu__gowi += '        __eval_res(redvars, data_out, i)\n'
    yjz__pseix = {}
    exec(fnqu__gowi, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yjz__pseix)
    return yjz__pseix['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    cgkl__foffq = n_keys
    mzl__czajk = []
    for afc__ehrdq, izb__jrp in enumerate(allfuncs):
        if izb__jrp.ftype == 'gen_udf':
            mzl__czajk.append(cgkl__foffq)
            cgkl__foffq += 1
        elif izb__jrp.ftype != 'udf':
            cgkl__foffq += izb__jrp.ncols_post_shuffle
        else:
            cgkl__foffq += izb__jrp.n_redvars + 1
    fnqu__gowi = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    fnqu__gowi += '    if num_groups == 0:\n'
    fnqu__gowi += '        return\n'
    for afc__ehrdq, func in enumerate(udf_func_struct.general_udf_funcs):
        fnqu__gowi += '    # col {}\n'.format(afc__ehrdq)
        fnqu__gowi += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(mzl__czajk[afc__ehrdq], afc__ehrdq))
        fnqu__gowi += '    incref(out_col)\n'
        fnqu__gowi += '    for j in range(num_groups):\n'
        fnqu__gowi += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(afc__ehrdq, afc__ehrdq))
        fnqu__gowi += '        incref(in_col)\n'
        fnqu__gowi += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(afc__ehrdq))
    yyr__qwaxj = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    myj__eki = 0
    for afc__ehrdq, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[myj__eki]
        yyr__qwaxj['func_{}'.format(myj__eki)] = func
        yyr__qwaxj['in_col_{}_typ'.format(myj__eki)] = in_col_typs[
            func_idx_to_in_col[afc__ehrdq]]
        yyr__qwaxj['out_col_{}_typ'.format(myj__eki)] = out_col_typs[afc__ehrdq
            ]
        myj__eki += 1
    yjz__pseix = {}
    exec(fnqu__gowi, yyr__qwaxj, yjz__pseix)
    izb__jrp = yjz__pseix['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    fnnzt__shhu = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(fnnzt__shhu, nopython=True)(izb__jrp)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    ysphb__old = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        xrkr__yvm = 1
    else:
        xrkr__yvm = len(agg_node.pivot_values)
    swrtp__eyv = tuple('key_' + sanitize_varname(xvjd__wowx) for xvjd__wowx in
        agg_node.key_names)
    bhyg__vtavb = {xvjd__wowx: 'in_{}'.format(sanitize_varname(xvjd__wowx)) for
        xvjd__wowx in agg_node.gb_info_in.keys() if xvjd__wowx is not None}
    exlop__smej = {xvjd__wowx: ('out_' + sanitize_varname(xvjd__wowx)) for
        xvjd__wowx in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    yjgco__ifo = ', '.join(swrtp__eyv)
    gdwvm__lmnuj = ', '.join(bhyg__vtavb.values())
    if gdwvm__lmnuj != '':
        gdwvm__lmnuj = ', ' + gdwvm__lmnuj
    fnqu__gowi = 'def agg_top({}{}{}, pivot_arr):\n'.format(yjgco__ifo,
        gdwvm__lmnuj, ', index_arg' if agg_node.input_has_index else '')
    for a in (swrtp__eyv + tuple(bhyg__vtavb.values())):
        fnqu__gowi += f'    {a} = decode_if_dict_array({a})\n'
    if ysphb__old:
        fnqu__gowi += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        ctgjj__ofio = []
        for dkk__hrs, qlzlx__mgrt in agg_node.gb_info_in.items():
            if dkk__hrs is not None:
                for func, zrim__gpqxx in qlzlx__mgrt:
                    ctgjj__ofio.append(bhyg__vtavb[dkk__hrs])
    else:
        ctgjj__ofio = tuple(bhyg__vtavb[dkk__hrs] for dkk__hrs, zrim__gpqxx in
            agg_node.gb_info_out.values() if dkk__hrs is not None)
    oahk__vhuns = swrtp__eyv + tuple(ctgjj__ofio)
    fnqu__gowi += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in oahk__vhuns), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    fnqu__gowi += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    mfmw__dgb = []
    func_idx_to_in_col = []
    zgkfc__gfphr = []
    eqfyf__copfq = False
    xxf__esx = 1
    tab__onkx = -1
    hji__lrs = 0
    ibiwz__yxs = 0
    if not ysphb__old:
        aqe__yda = [func for zrim__gpqxx, func in agg_node.gb_info_out.values()
            ]
    else:
        aqe__yda = [func for func, zrim__gpqxx in qlzlx__mgrt for
            qlzlx__mgrt in agg_node.gb_info_in.values()]
    for rehg__mqn, func in enumerate(aqe__yda):
        mfmw__dgb.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            hji__lrs += 1
        if hasattr(func, 'skipdropna'):
            eqfyf__copfq = func.skipdropna
        if func.ftype == 'shift':
            xxf__esx = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            ibiwz__yxs = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            tab__onkx = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(rehg__mqn)
        if func.ftype == 'udf':
            zgkfc__gfphr.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            zgkfc__gfphr.append(0)
            do_combine = False
    mfmw__dgb.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == xrkr__yvm, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * xrkr__yvm, 'invalid number of groupby outputs'
    if hji__lrs > 0:
        if hji__lrs != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for afc__ehrdq, xvjd__wowx in enumerate(agg_node.gb_info_out.keys()):
        xsoce__zzm = exlop__smej[xvjd__wowx] + '_dummy'
        ctdwr__sshi = out_col_typs[afc__ehrdq]
        dkk__hrs, func = agg_node.gb_info_out[xvjd__wowx]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(ctdwr__sshi, bodo.
            CategoricalArrayType):
            fnqu__gowi += '    {} = {}\n'.format(xsoce__zzm, bhyg__vtavb[
                dkk__hrs])
        elif udf_func_struct is not None:
            fnqu__gowi += '    {} = {}\n'.format(xsoce__zzm,
                _gen_dummy_alloc(ctdwr__sshi, afc__ehrdq, False))
    if udf_func_struct is not None:
        nhqxk__rza = next_label()
        if udf_func_struct.regular_udfs:
            fnnzt__shhu = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            wuoea__exw = numba.cfunc(fnnzt__shhu, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, nhqxk__rza))
            wyokz__udoju = numba.cfunc(fnnzt__shhu, nopython=True)(
                gen_combine_cb(udf_func_struct, allfuncs, n_keys,
                out_col_typs, nhqxk__rza))
            grtq__bchw = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                nhqxk__rza))
            udf_func_struct.set_regular_cfuncs(wuoea__exw, wyokz__udoju,
                grtq__bchw)
            for gftk__yrhun in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[gftk__yrhun.native_name] = gftk__yrhun
                gb_agg_cfunc_addr[gftk__yrhun.native_name
                    ] = gftk__yrhun.address
        if udf_func_struct.general_udfs:
            ysz__fzrx = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                nhqxk__rza)
            udf_func_struct.set_general_cfunc(ysz__fzrx)
        okjv__qaxov = []
        oympf__yiavp = 0
        afc__ehrdq = 0
        for xsoce__zzm, izb__jrp in zip(exlop__smej.values(), allfuncs):
            if izb__jrp.ftype in ('udf', 'gen_udf'):
                okjv__qaxov.append(xsoce__zzm + '_dummy')
                for dmiow__snqgi in range(oympf__yiavp, oympf__yiavp +
                    zgkfc__gfphr[afc__ehrdq]):
                    okjv__qaxov.append('data_redvar_dummy_' + str(dmiow__snqgi)
                        )
                oympf__yiavp += zgkfc__gfphr[afc__ehrdq]
                afc__ehrdq += 1
        if udf_func_struct.regular_udfs:
            essq__lhnlg = udf_func_struct.var_typs
            for afc__ehrdq, t in enumerate(essq__lhnlg):
                fnqu__gowi += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(afc__ehrdq, _get_np_dtype(t)))
        fnqu__gowi += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in okjv__qaxov))
        fnqu__gowi += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            fnqu__gowi += ("    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".
                format(wuoea__exw.native_name))
            fnqu__gowi += ("    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".
                format(wyokz__udoju.native_name))
            fnqu__gowi += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                grtq__bchw.native_name)
            fnqu__gowi += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(wuoea__exw.native_name))
            fnqu__gowi += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(wyokz__udoju.native_name))
            fnqu__gowi += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n"
                .format(grtq__bchw.native_name))
        else:
            fnqu__gowi += '    cpp_cb_update_addr = 0\n'
            fnqu__gowi += '    cpp_cb_combine_addr = 0\n'
            fnqu__gowi += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            gftk__yrhun = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[gftk__yrhun.native_name] = gftk__yrhun
            gb_agg_cfunc_addr[gftk__yrhun.native_name] = gftk__yrhun.address
            fnqu__gowi += ("    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".
                format(gftk__yrhun.native_name))
            fnqu__gowi += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(gftk__yrhun.native_name))
        else:
            fnqu__gowi += '    cpp_cb_general_addr = 0\n'
    else:
        fnqu__gowi += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        fnqu__gowi += '    cpp_cb_update_addr = 0\n'
        fnqu__gowi += '    cpp_cb_combine_addr = 0\n'
        fnqu__gowi += '    cpp_cb_eval_addr = 0\n'
        fnqu__gowi += '    cpp_cb_general_addr = 0\n'
    fnqu__gowi += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(izb__jrp.ftype)) for
        izb__jrp in allfuncs] + ['0']))
    fnqu__gowi += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(
        str(mfmw__dgb))
    if len(zgkfc__gfphr) > 0:
        fnqu__gowi += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(
            str(zgkfc__gfphr))
    else:
        fnqu__gowi += '    udf_ncols = np.array([0], np.int32)\n'
    if ysphb__old:
        fnqu__gowi += '    arr_type = coerce_to_array({})\n'.format(agg_node
            .pivot_values)
        fnqu__gowi += '    arr_info = array_to_info(arr_type)\n'
        fnqu__gowi += (
            '    dispatch_table = arr_info_list_to_table([arr_info])\n')
        fnqu__gowi += '    pivot_info = array_to_info(pivot_arr)\n'
        fnqu__gowi += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        fnqu__gowi += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, eqfyf__copfq, agg_node.return_key, agg_node.
            same_index))
        fnqu__gowi += '    delete_info_decref_array(pivot_info)\n'
        fnqu__gowi += '    delete_info_decref_array(arr_info)\n'
    else:
        fnqu__gowi += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel,
            eqfyf__copfq, xxf__esx, ibiwz__yxs, tab__onkx, agg_node.
            return_key, agg_node.same_index, agg_node.dropna))
    wnn__kebg = 0
    if agg_node.return_key:
        for afc__ehrdq, xjb__vfeta in enumerate(swrtp__eyv):
            fnqu__gowi += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(xjb__vfeta, wnn__kebg, xjb__vfeta))
            wnn__kebg += 1
    for afc__ehrdq, xsoce__zzm in enumerate(exlop__smej.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(ctdwr__sshi, bodo.
            CategoricalArrayType):
            fnqu__gowi += f"""    {xsoce__zzm} = info_to_array(info_from_table(out_table, {wnn__kebg}), {xsoce__zzm + '_dummy'})
"""
        else:
            fnqu__gowi += f"""    {xsoce__zzm} = info_to_array(info_from_table(out_table, {wnn__kebg}), out_typs[{afc__ehrdq}])
"""
        wnn__kebg += 1
    if agg_node.same_index:
        fnqu__gowi += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(wnn__kebg))
        wnn__kebg += 1
    fnqu__gowi += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    fnqu__gowi += '    delete_table_decref_arrays(table)\n'
    fnqu__gowi += '    delete_table_decref_arrays(udf_table_dummy)\n'
    fnqu__gowi += '    delete_table(out_table)\n'
    fnqu__gowi += f'    ev_clean.finalize()\n'
    zav__tnc = tuple(exlop__smej.values())
    if agg_node.return_key:
        zav__tnc += tuple(swrtp__eyv)
    fnqu__gowi += '    return ({},{})\n'.format(', '.join(zav__tnc), 
        ' out_index_arg,' if agg_node.same_index else '')
    yjz__pseix = {}
    exec(fnqu__gowi, {'out_typs': out_col_typs}, yjz__pseix)
    jlgao__oeag = yjz__pseix['agg_top']
    return jlgao__oeag


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for inzks__vgbv in block.body:
            if is_call_assign(inzks__vgbv) and find_callname(f_ir,
                inzks__vgbv.value) == ('len', 'builtins'
                ) and inzks__vgbv.value.args[0].name == f_ir.arg_names[0]:
                nwq__sokf = get_definition(f_ir, inzks__vgbv.value.func)
                nwq__sokf.name = 'dummy_agg_count'
                nwq__sokf.value = dummy_agg_count
    dkr__nothr = get_name_var_table(f_ir.blocks)
    vmjb__xfpn = {}
    for name, zrim__gpqxx in dkr__nothr.items():
        vmjb__xfpn[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, vmjb__xfpn)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    kfwa__dot = numba.core.compiler.Flags()
    kfwa__dot.nrt = True
    kqds__vrfz = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, kfwa__dot)
    kqds__vrfz.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, yagd__ctmd, calltypes, zrim__gpqxx = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    kmr__iwqhk = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    sja__hdtl = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    vokdf__rbtbg = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    dwha__qvygc = vokdf__rbtbg(typemap, calltypes)
    pm = sja__hdtl(typingctx, targetctx, None, f_ir, typemap, yagd__ctmd,
        calltypes, dwha__qvygc, {}, kfwa__dot, None)
    whday__lav = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = sja__hdtl(typingctx, targetctx, None, f_ir, typemap, yagd__ctmd,
        calltypes, dwha__qvygc, {}, kfwa__dot, whday__lav)
    gqfix__uymv = numba.core.typed_passes.InlineOverloads()
    gqfix__uymv.run_pass(pm)
    cwqf__vxzkb = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    cwqf__vxzkb.run()
    for block in f_ir.blocks.values():
        for inzks__vgbv in block.body:
            if is_assign(inzks__vgbv) and isinstance(inzks__vgbv.value, (ir
                .Arg, ir.Var)) and isinstance(typemap[inzks__vgbv.target.
                name], SeriesType):
                swrx__rjng = typemap.pop(inzks__vgbv.target.name)
                typemap[inzks__vgbv.target.name] = swrx__rjng.data
            if is_call_assign(inzks__vgbv) and find_callname(f_ir,
                inzks__vgbv.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[inzks__vgbv.target.name].remove(inzks__vgbv
                    .value)
                inzks__vgbv.value = inzks__vgbv.value.args[0]
                f_ir._definitions[inzks__vgbv.target.name].append(inzks__vgbv
                    .value)
            if is_call_assign(inzks__vgbv) and find_callname(f_ir,
                inzks__vgbv.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[inzks__vgbv.target.name].remove(inzks__vgbv
                    .value)
                inzks__vgbv.value = ir.Const(False, inzks__vgbv.loc)
                f_ir._definitions[inzks__vgbv.target.name].append(inzks__vgbv
                    .value)
            if is_call_assign(inzks__vgbv) and find_callname(f_ir,
                inzks__vgbv.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[inzks__vgbv.target.name].remove(inzks__vgbv
                    .value)
                inzks__vgbv.value = ir.Const(False, inzks__vgbv.loc)
                f_ir._definitions[inzks__vgbv.target.name].append(inzks__vgbv
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    xsch__ckqi = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, kmr__iwqhk)
    xsch__ckqi.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    ytw__vfn = numba.core.compiler.StateDict()
    ytw__vfn.func_ir = f_ir
    ytw__vfn.typemap = typemap
    ytw__vfn.calltypes = calltypes
    ytw__vfn.typingctx = typingctx
    ytw__vfn.targetctx = targetctx
    ytw__vfn.return_type = yagd__ctmd
    numba.core.rewrites.rewrite_registry.apply('after-inference', ytw__vfn)
    kwpwk__jhg = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        yagd__ctmd, typingctx, targetctx, kmr__iwqhk, kfwa__dot, {})
    kwpwk__jhg.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            bnlx__zxfwr = ctypes.pythonapi.PyCell_Get
            bnlx__zxfwr.restype = ctypes.py_object
            bnlx__zxfwr.argtypes = ctypes.py_object,
            mlx__izeed = tuple(bnlx__zxfwr(jbx__qxs) for jbx__qxs in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            mlx__izeed = closure.items
        assert len(code.co_freevars) == len(mlx__izeed)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, mlx__izeed
            )


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
        gxb__rele = SeriesType(in_col_typ.dtype, in_col_typ, None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (gxb__rele,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        glxn__ufop, arr_var = _rm_arg_agg_block(block, pm.typemap)
        otc__oki = -1
        for afc__ehrdq, inzks__vgbv in enumerate(glxn__ufop):
            if isinstance(inzks__vgbv, numba.parfors.parfor.Parfor):
                assert otc__oki == -1, 'only one parfor for aggregation function'
                otc__oki = afc__ehrdq
        parfor = None
        if otc__oki != -1:
            parfor = glxn__ufop[otc__oki]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = glxn__ufop[:otc__oki] + parfor.init_block.body
        eval_nodes = glxn__ufop[otc__oki + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for inzks__vgbv in init_nodes:
            if is_assign(inzks__vgbv) and inzks__vgbv.target.name in redvars:
                ind = redvars.index(inzks__vgbv.target.name)
                reduce_vars[ind] = inzks__vgbv.target
        var_types = [pm.typemap[dwn__pii] for dwn__pii in redvars]
        ejssx__bec = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        lyqp__grek = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        mlg__dppc = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(mlg__dppc)
        self.all_update_funcs.append(lyqp__grek)
        self.all_combine_funcs.append(ejssx__bec)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        vlbiu__rqfk = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        gqg__veft = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        nrnru__kbjo = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        bwvo__gsjie = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return (self.all_vartypes, vlbiu__rqfk, gqg__veft, nrnru__kbjo,
            bwvo__gsjie)


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
    ekag__gcfe = []
    for t, izb__jrp in zip(in_col_types, agg_func):
        ekag__gcfe.append((t, izb__jrp))
    dgi__cdrk = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    reap__zvl = GeneralUDFGenerator()
    for in_col_typ, func in ekag__gcfe:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            dgi__cdrk.add_udf(in_col_typ, func)
        except:
            reap__zvl.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = dgi__cdrk.gen_all_func()
    general_udf_funcs = reap__zvl.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    cetzq__phxq = compute_use_defs(parfor.loop_body)
    loq__jccrn = set()
    for pdj__wmk in cetzq__phxq.usemap.values():
        loq__jccrn |= pdj__wmk
    lhy__rjik = set()
    for pdj__wmk in cetzq__phxq.defmap.values():
        lhy__rjik |= pdj__wmk
    hziv__igama = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    hziv__igama.body = eval_nodes
    jja__quqs = compute_use_defs({(0): hziv__igama})
    fcbvu__srsb = jja__quqs.usemap[0]
    wnrxg__yzxjy = set()
    ged__cwp = []
    czol__pth = []
    for inzks__vgbv in reversed(init_nodes):
        yxq__elhbi = {dwn__pii.name for dwn__pii in inzks__vgbv.list_vars()}
        if is_assign(inzks__vgbv):
            dwn__pii = inzks__vgbv.target.name
            yxq__elhbi.remove(dwn__pii)
            if (dwn__pii in loq__jccrn and dwn__pii not in wnrxg__yzxjy and
                dwn__pii not in fcbvu__srsb and dwn__pii not in lhy__rjik):
                czol__pth.append(inzks__vgbv)
                loq__jccrn |= yxq__elhbi
                lhy__rjik.add(dwn__pii)
                continue
        wnrxg__yzxjy |= yxq__elhbi
        ged__cwp.append(inzks__vgbv)
    czol__pth.reverse()
    ged__cwp.reverse()
    qddru__oudv = min(parfor.loop_body.keys())
    tog__uwus = parfor.loop_body[qddru__oudv]
    tog__uwus.body = czol__pth + tog__uwus.body
    return ged__cwp


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    gdsot__ares = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    ebzfl__ogu = set()
    iag__jhb = []
    for inzks__vgbv in init_nodes:
        if is_assign(inzks__vgbv) and isinstance(inzks__vgbv.value, ir.Global
            ) and isinstance(inzks__vgbv.value.value, pytypes.FunctionType
            ) and inzks__vgbv.value.value in gdsot__ares:
            ebzfl__ogu.add(inzks__vgbv.target.name)
        elif is_call_assign(inzks__vgbv
            ) and inzks__vgbv.value.func.name in ebzfl__ogu:
            pass
        else:
            iag__jhb.append(inzks__vgbv)
    init_nodes = iag__jhb
    omuhe__zuh = types.Tuple(var_types)
    ofi__tlzuf = lambda : None
    f_ir = compile_to_numba_ir(ofi__tlzuf, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    zgkl__qkv = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    xzx__ixn = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc), zgkl__qkv, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [xzx__ixn] + block.body
    block.body[-2].value.value = zgkl__qkv
    sgsq__exfiy = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        omuhe__zuh, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cmuix__edp = numba.core.target_extension.dispatcher_registry[cpu_target](
        ofi__tlzuf)
    cmuix__edp.add_overload(sgsq__exfiy)
    return cmuix__edp


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    rytj__fujr = len(update_funcs)
    izbcq__riog = len(in_col_types)
    if pivot_values is not None:
        assert izbcq__riog == 1
    fnqu__gowi = (
        'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        dax__ldf = redvar_offsets[izbcq__riog]
        fnqu__gowi += '  pv = pivot_arr[i]\n'
        for dmiow__snqgi, scfs__zey in enumerate(pivot_values):
            hps__xcnnv = 'el' if dmiow__snqgi != 0 else ''
            fnqu__gowi += "  {}if pv == '{}':\n".format(hps__xcnnv, scfs__zey)
            gfrw__tblbw = dax__ldf * dmiow__snqgi
            nou__htw = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                afc__ehrdq) for afc__ehrdq in range(gfrw__tblbw +
                redvar_offsets[0], gfrw__tblbw + redvar_offsets[1])])
            gqng__ozlct = 'data_in[0][i]'
            if is_crosstab:
                gqng__ozlct = '0'
            fnqu__gowi += '    {} = update_vars_0({}, {})\n'.format(nou__htw,
                nou__htw, gqng__ozlct)
    else:
        for dmiow__snqgi in range(rytj__fujr):
            nou__htw = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                afc__ehrdq) for afc__ehrdq in range(redvar_offsets[
                dmiow__snqgi], redvar_offsets[dmiow__snqgi + 1])])
            if nou__htw:
                fnqu__gowi += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(nou__htw, dmiow__snqgi, nou__htw, 0 if 
                    izbcq__riog == 1 else dmiow__snqgi))
    fnqu__gowi += '  return\n'
    yyr__qwaxj = {}
    for afc__ehrdq, izb__jrp in enumerate(update_funcs):
        yyr__qwaxj['update_vars_{}'.format(afc__ehrdq)] = izb__jrp
    yjz__pseix = {}
    exec(fnqu__gowi, yyr__qwaxj, yjz__pseix)
    qrk__jaugi = yjz__pseix['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(qrk__jaugi)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    xgb__ncsqf = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = xgb__ncsqf, xgb__ncsqf, types.intp, types.intp, pivot_typ
    wprgq__fqv = len(redvar_offsets) - 1
    dax__ldf = redvar_offsets[wprgq__fqv]
    fnqu__gowi = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert wprgq__fqv == 1
        for zosn__eawsp in range(len(pivot_values)):
            gfrw__tblbw = dax__ldf * zosn__eawsp
            nou__htw = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                afc__ehrdq) for afc__ehrdq in range(gfrw__tblbw +
                redvar_offsets[0], gfrw__tblbw + redvar_offsets[1])])
            umn__ylmsz = ', '.join(['recv_arrs[{}][i]'.format(afc__ehrdq) for
                afc__ehrdq in range(gfrw__tblbw + redvar_offsets[0], 
                gfrw__tblbw + redvar_offsets[1])])
            fnqu__gowi += '  {} = combine_vars_0({}, {})\n'.format(nou__htw,
                nou__htw, umn__ylmsz)
    else:
        for dmiow__snqgi in range(wprgq__fqv):
            nou__htw = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                afc__ehrdq) for afc__ehrdq in range(redvar_offsets[
                dmiow__snqgi], redvar_offsets[dmiow__snqgi + 1])])
            umn__ylmsz = ', '.join(['recv_arrs[{}][i]'.format(afc__ehrdq) for
                afc__ehrdq in range(redvar_offsets[dmiow__snqgi],
                redvar_offsets[dmiow__snqgi + 1])])
            if umn__ylmsz:
                fnqu__gowi += '  {} = combine_vars_{}({}, {})\n'.format(
                    nou__htw, dmiow__snqgi, nou__htw, umn__ylmsz)
    fnqu__gowi += '  return\n'
    yyr__qwaxj = {}
    for afc__ehrdq, izb__jrp in enumerate(combine_funcs):
        yyr__qwaxj['combine_vars_{}'.format(afc__ehrdq)] = izb__jrp
    yjz__pseix = {}
    exec(fnqu__gowi, yyr__qwaxj, yjz__pseix)
    uur__cfz = yjz__pseix['combine_all_f']
    f_ir = compile_to_numba_ir(uur__cfz, yyr__qwaxj)
    nrnru__kbjo = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cmuix__edp = numba.core.target_extension.dispatcher_registry[cpu_target](
        uur__cfz)
    cmuix__edp.add_overload(nrnru__kbjo)
    return cmuix__edp


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    xgb__ncsqf = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    out_col_typs = types.Tuple(out_col_typs)
    wprgq__fqv = len(redvar_offsets) - 1
    dax__ldf = redvar_offsets[wprgq__fqv]
    fnqu__gowi = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert wprgq__fqv == 1
        for dmiow__snqgi in range(len(pivot_values)):
            gfrw__tblbw = dax__ldf * dmiow__snqgi
            nou__htw = ', '.join(['redvar_arrs[{}][j]'.format(afc__ehrdq) for
                afc__ehrdq in range(gfrw__tblbw + redvar_offsets[0], 
                gfrw__tblbw + redvar_offsets[1])])
            fnqu__gowi += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                dmiow__snqgi, nou__htw)
    else:
        for dmiow__snqgi in range(wprgq__fqv):
            nou__htw = ', '.join(['redvar_arrs[{}][j]'.format(afc__ehrdq) for
                afc__ehrdq in range(redvar_offsets[dmiow__snqgi],
                redvar_offsets[dmiow__snqgi + 1])])
            fnqu__gowi += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                dmiow__snqgi, dmiow__snqgi, nou__htw)
    fnqu__gowi += '  return\n'
    yyr__qwaxj = {}
    for afc__ehrdq, izb__jrp in enumerate(eval_funcs):
        yyr__qwaxj['eval_vars_{}'.format(afc__ehrdq)] = izb__jrp
    yjz__pseix = {}
    exec(fnqu__gowi, yyr__qwaxj, yjz__pseix)
    fqb__hxat = yjz__pseix['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(fqb__hxat)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    ckoue__trbp = len(var_types)
    jwc__rkckf = [f'in{afc__ehrdq}' for afc__ehrdq in range(ckoue__trbp)]
    omuhe__zuh = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    jhmn__ouitr = omuhe__zuh(0)
    fnqu__gowi = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        jwc__rkckf))
    yjz__pseix = {}
    exec(fnqu__gowi, {'_zero': jhmn__ouitr}, yjz__pseix)
    devp__pxuyr = yjz__pseix['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(devp__pxuyr, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': jhmn__ouitr}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    mlmad__bgn = []
    for afc__ehrdq, dwn__pii in enumerate(reduce_vars):
        mlmad__bgn.append(ir.Assign(block.body[afc__ehrdq].target, dwn__pii,
            dwn__pii.loc))
        for brv__nsnyj in dwn__pii.versioned_names:
            mlmad__bgn.append(ir.Assign(dwn__pii, ir.Var(dwn__pii.scope,
                brv__nsnyj, dwn__pii.loc), dwn__pii.loc))
    block.body = block.body[:ckoue__trbp] + mlmad__bgn + eval_nodes
    mlg__dppc = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        omuhe__zuh, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cmuix__edp = numba.core.target_extension.dispatcher_registry[cpu_target](
        devp__pxuyr)
    cmuix__edp.add_overload(mlg__dppc)
    return cmuix__edp


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    ckoue__trbp = len(redvars)
    vdof__cktos = [f'v{afc__ehrdq}' for afc__ehrdq in range(ckoue__trbp)]
    jwc__rkckf = [f'in{afc__ehrdq}' for afc__ehrdq in range(ckoue__trbp)]
    fnqu__gowi = 'def agg_combine({}):\n'.format(', '.join(vdof__cktos +
        jwc__rkckf))
    mvph__fiu = wrap_parfor_blocks(parfor)
    aqbt__qtl = find_topo_order(mvph__fiu)
    aqbt__qtl = aqbt__qtl[1:]
    unwrap_parfor_blocks(parfor)
    ucs__wdvi = {}
    fcl__urilm = []
    for bfxlz__uunjw in aqbt__qtl:
        etxli__vxcn = parfor.loop_body[bfxlz__uunjw]
        for inzks__vgbv in etxli__vxcn.body:
            if is_call_assign(inzks__vgbv) and guard(find_callname, f_ir,
                inzks__vgbv.value) == ('__special_combine', 'bodo.ir.aggregate'
                ):
                args = inzks__vgbv.value.args
                wizp__szih = []
                qbf__eqlp = []
                for dwn__pii in args[:-1]:
                    ind = redvars.index(dwn__pii.name)
                    fcl__urilm.append(ind)
                    wizp__szih.append('v{}'.format(ind))
                    qbf__eqlp.append('in{}'.format(ind))
                fpjg__mic = '__special_combine__{}'.format(len(ucs__wdvi))
                fnqu__gowi += '    ({},) = {}({})\n'.format(', '.join(
                    wizp__szih), fpjg__mic, ', '.join(wizp__szih + qbf__eqlp))
                grzw__flfv = ir.Expr.call(args[-1], [], (), etxli__vxcn.loc)
                uqg__vzm = guard(find_callname, f_ir, grzw__flfv)
                assert uqg__vzm == ('_var_combine', 'bodo.ir.aggregate')
                uqg__vzm = bodo.ir.aggregate._var_combine
                ucs__wdvi[fpjg__mic] = uqg__vzm
            if is_assign(inzks__vgbv) and inzks__vgbv.target.name in redvars:
                yjynm__oni = inzks__vgbv.target.name
                ind = redvars.index(yjynm__oni)
                if ind in fcl__urilm:
                    continue
                if len(f_ir._definitions[yjynm__oni]) == 2:
                    var_def = f_ir._definitions[yjynm__oni][0]
                    fnqu__gowi += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[yjynm__oni][1]
                    fnqu__gowi += _match_reduce_def(var_def, f_ir, ind)
    fnqu__gowi += '    return {}'.format(', '.join(['v{}'.format(afc__ehrdq
        ) for afc__ehrdq in range(ckoue__trbp)]))
    yjz__pseix = {}
    exec(fnqu__gowi, {}, yjz__pseix)
    bfvu__sov = yjz__pseix['agg_combine']
    arg_typs = tuple(2 * var_types)
    yyr__qwaxj = {'numba': numba, 'bodo': bodo, 'np': np}
    yyr__qwaxj.update(ucs__wdvi)
    f_ir = compile_to_numba_ir(bfvu__sov, yyr__qwaxj, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    omuhe__zuh = pm.typemap[block.body[-1].value.name]
    ejssx__bec = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        omuhe__zuh, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cmuix__edp = numba.core.target_extension.dispatcher_registry[cpu_target](
        bfvu__sov)
    cmuix__edp.add_overload(ejssx__bec)
    return cmuix__edp


def _match_reduce_def(var_def, f_ir, ind):
    fnqu__gowi = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        fnqu__gowi = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        msya__kgi = guard(find_callname, f_ir, var_def)
        if msya__kgi == ('min', 'builtins'):
            fnqu__gowi = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if msya__kgi == ('max', 'builtins'):
            fnqu__gowi = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return fnqu__gowi


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    ckoue__trbp = len(redvars)
    gdhjb__egbcj = 1
    ndo__ezuu = []
    for afc__ehrdq in range(gdhjb__egbcj):
        mubrg__thkll = ir.Var(arr_var.scope, f'$input{afc__ehrdq}', arr_var.loc
            )
        ndo__ezuu.append(mubrg__thkll)
    scrrm__vqd = parfor.loop_nests[0].index_variable
    sfnfs__ivk = [0] * ckoue__trbp
    for etxli__vxcn in parfor.loop_body.values():
        ymbti__dsnf = []
        for inzks__vgbv in etxli__vxcn.body:
            if is_var_assign(inzks__vgbv
                ) and inzks__vgbv.value.name == scrrm__vqd.name:
                continue
            if is_getitem(inzks__vgbv
                ) and inzks__vgbv.value.value.name == arr_var.name:
                inzks__vgbv.value = ndo__ezuu[0]
            if is_call_assign(inzks__vgbv) and guard(find_callname, pm.
                func_ir, inzks__vgbv.value) == ('isna',
                'bodo.libs.array_kernels') and inzks__vgbv.value.args[0
                ].name == arr_var.name:
                inzks__vgbv.value = ir.Const(False, inzks__vgbv.target.loc)
            if is_assign(inzks__vgbv) and inzks__vgbv.target.name in redvars:
                ind = redvars.index(inzks__vgbv.target.name)
                sfnfs__ivk[ind] = inzks__vgbv.target
            ymbti__dsnf.append(inzks__vgbv)
        etxli__vxcn.body = ymbti__dsnf
    vdof__cktos = ['v{}'.format(afc__ehrdq) for afc__ehrdq in range(
        ckoue__trbp)]
    jwc__rkckf = ['in{}'.format(afc__ehrdq) for afc__ehrdq in range(
        gdhjb__egbcj)]
    fnqu__gowi = 'def agg_update({}):\n'.format(', '.join(vdof__cktos +
        jwc__rkckf))
    fnqu__gowi += '    __update_redvars()\n'
    fnqu__gowi += '    return {}'.format(', '.join(['v{}'.format(afc__ehrdq
        ) for afc__ehrdq in range(ckoue__trbp)]))
    yjz__pseix = {}
    exec(fnqu__gowi, {}, yjz__pseix)
    riq__nzti = yjz__pseix['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * gdhjb__egbcj)
    f_ir = compile_to_numba_ir(riq__nzti, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    qpd__goew = f_ir.blocks.popitem()[1].body
    omuhe__zuh = pm.typemap[qpd__goew[-1].value.name]
    mvph__fiu = wrap_parfor_blocks(parfor)
    aqbt__qtl = find_topo_order(mvph__fiu)
    aqbt__qtl = aqbt__qtl[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    tog__uwus = f_ir.blocks[aqbt__qtl[0]]
    xeu__pavrj = f_ir.blocks[aqbt__qtl[-1]]
    ghsa__iduec = qpd__goew[:ckoue__trbp + gdhjb__egbcj]
    if ckoue__trbp > 1:
        urix__hcdg = qpd__goew[-3:]
        assert is_assign(urix__hcdg[0]) and isinstance(urix__hcdg[0].value,
            ir.Expr) and urix__hcdg[0].value.op == 'build_tuple'
    else:
        urix__hcdg = qpd__goew[-2:]
    for afc__ehrdq in range(ckoue__trbp):
        pqsdo__zns = qpd__goew[afc__ehrdq].target
        swmvy__qmjpe = ir.Assign(pqsdo__zns, sfnfs__ivk[afc__ehrdq],
            pqsdo__zns.loc)
        ghsa__iduec.append(swmvy__qmjpe)
    for afc__ehrdq in range(ckoue__trbp, ckoue__trbp + gdhjb__egbcj):
        pqsdo__zns = qpd__goew[afc__ehrdq].target
        swmvy__qmjpe = ir.Assign(pqsdo__zns, ndo__ezuu[afc__ehrdq -
            ckoue__trbp], pqsdo__zns.loc)
        ghsa__iduec.append(swmvy__qmjpe)
    tog__uwus.body = ghsa__iduec + tog__uwus.body
    kse__yne = []
    for afc__ehrdq in range(ckoue__trbp):
        pqsdo__zns = qpd__goew[afc__ehrdq].target
        swmvy__qmjpe = ir.Assign(sfnfs__ivk[afc__ehrdq], pqsdo__zns,
            pqsdo__zns.loc)
        kse__yne.append(swmvy__qmjpe)
    xeu__pavrj.body += kse__yne + urix__hcdg
    jjm__lwb = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        omuhe__zuh, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cmuix__edp = numba.core.target_extension.dispatcher_registry[cpu_target](
        riq__nzti)
    cmuix__edp.add_overload(jjm__lwb)
    return cmuix__edp


def _rm_arg_agg_block(block, typemap):
    glxn__ufop = []
    arr_var = None
    for afc__ehrdq, inzks__vgbv in enumerate(block.body):
        if is_assign(inzks__vgbv) and isinstance(inzks__vgbv.value, ir.Arg):
            arr_var = inzks__vgbv.target
            ijve__lvay = typemap[arr_var.name]
            if not isinstance(ijve__lvay, types.ArrayCompatible):
                glxn__ufop += block.body[afc__ehrdq + 1:]
                break
            qlkqw__vwl = block.body[afc__ehrdq + 1]
            assert is_assign(qlkqw__vwl) and isinstance(qlkqw__vwl.value,
                ir.Expr
                ) and qlkqw__vwl.value.op == 'getattr' and qlkqw__vwl.value.attr == 'shape' and qlkqw__vwl.value.value.name == arr_var.name
            aepi__tax = qlkqw__vwl.target
            nzk__bif = block.body[afc__ehrdq + 2]
            assert is_assign(nzk__bif) and isinstance(nzk__bif.value, ir.Expr
                ) and nzk__bif.value.op == 'static_getitem' and nzk__bif.value.value.name == aepi__tax.name
            glxn__ufop += block.body[afc__ehrdq + 3:]
            break
        glxn__ufop.append(inzks__vgbv)
    return glxn__ufop, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    mvph__fiu = wrap_parfor_blocks(parfor)
    aqbt__qtl = find_topo_order(mvph__fiu)
    aqbt__qtl = aqbt__qtl[1:]
    unwrap_parfor_blocks(parfor)
    for bfxlz__uunjw in reversed(aqbt__qtl):
        for inzks__vgbv in reversed(parfor.loop_body[bfxlz__uunjw].body):
            if isinstance(inzks__vgbv, ir.Assign) and (inzks__vgbv.target.
                name in parfor_params or inzks__vgbv.target.name in
                var_to_param):
                elucj__brml = inzks__vgbv.target.name
                rhs = inzks__vgbv.value
                xbi__jnnmc = (elucj__brml if elucj__brml in parfor_params else
                    var_to_param[elucj__brml])
                jsty__glkqe = []
                if isinstance(rhs, ir.Var):
                    jsty__glkqe = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    jsty__glkqe = [dwn__pii.name for dwn__pii in
                        inzks__vgbv.value.list_vars()]
                param_uses[xbi__jnnmc].extend(jsty__glkqe)
                for dwn__pii in jsty__glkqe:
                    var_to_param[dwn__pii] = xbi__jnnmc
            if isinstance(inzks__vgbv, Parfor):
                get_parfor_reductions(inzks__vgbv, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for pwoyv__akkk, jsty__glkqe in param_uses.items():
        if pwoyv__akkk in jsty__glkqe and pwoyv__akkk not in reduce_varnames:
            reduce_varnames.append(pwoyv__akkk)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
