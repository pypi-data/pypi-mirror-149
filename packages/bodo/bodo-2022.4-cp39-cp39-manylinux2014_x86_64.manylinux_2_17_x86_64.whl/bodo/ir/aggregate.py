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
            aoq__yrou = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            qiae__xcfi = cgutils.get_or_insert_function(builder.module,
                aoq__yrou, sym._literal_value)
            builder.call(qiae__xcfi, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            aoq__yrou = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            qiae__xcfi = cgutils.get_or_insert_function(builder.module,
                aoq__yrou, sym._literal_value)
            builder.call(qiae__xcfi, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            aoq__yrou = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            qiae__xcfi = cgutils.get_or_insert_function(builder.module,
                aoq__yrou, sym._literal_value)
            builder.call(qiae__xcfi, [context.get_constant_null(sig.args[0]
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
        aika__pkm = True
        wqrki__vxb = 1
        msj__ruf = -1
        if isinstance(rhs, ir.Expr):
            for gyohy__mueej in rhs.kws:
                if func_name in list_cumulative:
                    if gyohy__mueej[0] == 'skipna':
                        aika__pkm = guard(find_const, func_ir, gyohy__mueej[1])
                        if not isinstance(aika__pkm, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if gyohy__mueej[0] == 'dropna':
                        aika__pkm = guard(find_const, func_ir, gyohy__mueej[1])
                        if not isinstance(aika__pkm, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            wqrki__vxb = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', wqrki__vxb)
            wqrki__vxb = guard(find_const, func_ir, wqrki__vxb)
        if func_name == 'head':
            msj__ruf = get_call_expr_arg('head', rhs.args, dict(rhs.kws), 0,
                'n', 5)
            if not isinstance(msj__ruf, int):
                msj__ruf = guard(find_const, func_ir, msj__ruf)
            if msj__ruf < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = aika__pkm
        func.periods = wqrki__vxb
        func.head_n = msj__ruf
        if func_name == 'transform':
            kws = dict(rhs.kws)
            eoht__xgjvy = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            ytp__uree = typemap[eoht__xgjvy.name]
            ltyb__izvf = None
            if isinstance(ytp__uree, str):
                ltyb__izvf = ytp__uree
            elif is_overload_constant_str(ytp__uree):
                ltyb__izvf = get_overload_const_str(ytp__uree)
            elif bodo.utils.typing.is_builtin_function(ytp__uree):
                ltyb__izvf = bodo.utils.typing.get_builtin_function_name(
                    ytp__uree)
            if ltyb__izvf not in bodo.ir.aggregate.supported_transform_funcs[:
                ]:
                raise BodoError(f'unsupported transform function {ltyb__izvf}')
            func.transform_func = supported_agg_funcs.index(ltyb__izvf)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    eoht__xgjvy = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if eoht__xgjvy == '':
        ytp__uree = types.none
    else:
        ytp__uree = typemap[eoht__xgjvy.name]
    if is_overload_constant_dict(ytp__uree):
        izhxa__lcszu = get_overload_constant_dict(ytp__uree)
        vfmjt__dzki = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in izhxa__lcszu.values()]
        return vfmjt__dzki
    if ytp__uree == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(ytp__uree, types.BaseTuple):
        vfmjt__dzki = []
        vkjg__fele = 0
        for t in ytp__uree.types:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                vfmjt__dzki.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>':
                    func.fname = '<lambda_' + str(vkjg__fele) + '>'
                    vkjg__fele += 1
                vfmjt__dzki.append(func)
        return [vfmjt__dzki]
    if is_overload_constant_str(ytp__uree):
        func_name = get_overload_const_str(ytp__uree)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(ytp__uree):
        func_name = bodo.utils.typing.get_builtin_function_name(ytp__uree)
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
        vkjg__fele = 0
        ozkq__kxlgp = []
        for bxt__chl in f_val:
            func = get_agg_func_udf(func_ir, bxt__chl, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{vkjg__fele}>'
                vkjg__fele += 1
            ozkq__kxlgp.append(func)
        return ozkq__kxlgp
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
    ltyb__izvf = code.co_name
    return ltyb__izvf


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
            jpiv__hwshg = types.DType(args[0])
            return signature(jpiv__hwshg, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    uincl__nukp = nobs_a + nobs_b
    wtxv__lxu = (nobs_a * mean_a + nobs_b * mean_b) / uincl__nukp
    teo__tuew = mean_b - mean_a
    heyal__jenf = (ssqdm_a + ssqdm_b + teo__tuew * teo__tuew * nobs_a *
        nobs_b / uincl__nukp)
    return heyal__jenf, wtxv__lxu, uincl__nukp


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
        yrker__igbf = ''
        for dgu__iydar, lbd__niacr in self.df_out_vars.items():
            yrker__igbf += "'{}':{}, ".format(dgu__iydar, lbd__niacr.name)
        ouu__xih = '{}{{{}}}'.format(self.df_out, yrker__igbf)
        uucvz__ael = ''
        for dgu__iydar, lbd__niacr in self.df_in_vars.items():
            uucvz__ael += "'{}':{}, ".format(dgu__iydar, lbd__niacr.name)
        ifgo__sskc = '{}{{{}}}'.format(self.df_in, uucvz__ael)
        adlyh__lxjwb = 'pivot {}:{}'.format(self.pivot_arr.name, self.
            pivot_values) if self.pivot_arr is not None else ''
        key_names = ','.join(self.key_names)
        leefw__pmn = ','.join([lbd__niacr.name for lbd__niacr in self.key_arrs]
            )
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(ouu__xih,
            ifgo__sskc, key_names, leefw__pmn, adlyh__lxjwb)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        hplx__kaw, zaxq__zrul = self.gb_info_out.pop(out_col_name)
        if hplx__kaw is None and not self.is_crosstab:
            return
        bxr__sonsp = self.gb_info_in[hplx__kaw]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for otykx__bjftt, (func, yrker__igbf) in enumerate(bxr__sonsp):
                try:
                    yrker__igbf.remove(out_col_name)
                    if len(yrker__igbf) == 0:
                        bxr__sonsp.pop(otykx__bjftt)
                        break
                except ValueError as rcqh__olrl:
                    continue
        else:
            for otykx__bjftt, (func, yvzlg__pqwj) in enumerate(bxr__sonsp):
                if yvzlg__pqwj == out_col_name:
                    bxr__sonsp.pop(otykx__bjftt)
                    break
        if len(bxr__sonsp) == 0:
            self.gb_info_in.pop(hplx__kaw)
            self.df_in_vars.pop(hplx__kaw)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({lbd__niacr.name for lbd__niacr in aggregate_node.key_arrs})
    use_set.update({lbd__niacr.name for lbd__niacr in aggregate_node.
        df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({lbd__niacr.name for lbd__niacr in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({lbd__niacr.name for lbd__niacr in aggregate_node.
            out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    mgnq__shaki = [jwb__iviue for jwb__iviue, wuak__ffigs in aggregate_node
        .df_out_vars.items() if wuak__ffigs.name not in lives]
    for nkckg__pqpr in mgnq__shaki:
        aggregate_node.remove_out_col(nkckg__pqpr)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(lbd__niacr.name not in lives for
        lbd__niacr in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    gfc__jzpoy = set(lbd__niacr.name for lbd__niacr in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        gfc__jzpoy.update({lbd__niacr.name for lbd__niacr in aggregate_node
            .out_key_vars})
    return set(), gfc__jzpoy


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for otykx__bjftt in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[otykx__bjftt] = replace_vars_inner(
            aggregate_node.key_arrs[otykx__bjftt], var_dict)
    for jwb__iviue in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[jwb__iviue] = replace_vars_inner(
            aggregate_node.df_in_vars[jwb__iviue], var_dict)
    for jwb__iviue in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[jwb__iviue] = replace_vars_inner(
            aggregate_node.df_out_vars[jwb__iviue], var_dict)
    if aggregate_node.out_key_vars is not None:
        for otykx__bjftt in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[otykx__bjftt] = replace_vars_inner(
                aggregate_node.out_key_vars[otykx__bjftt], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for otykx__bjftt in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[otykx__bjftt] = visit_vars_inner(aggregate_node
            .key_arrs[otykx__bjftt], callback, cbdata)
    for jwb__iviue in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[jwb__iviue] = visit_vars_inner(aggregate_node
            .df_in_vars[jwb__iviue], callback, cbdata)
    for jwb__iviue in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[jwb__iviue] = visit_vars_inner(
            aggregate_node.df_out_vars[jwb__iviue], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for otykx__bjftt in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[otykx__bjftt] = visit_vars_inner(
                aggregate_node.out_key_vars[otykx__bjftt], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    lwsm__lmho = []
    for uonq__xwbu in aggregate_node.key_arrs:
        zbtb__ihwt = equiv_set.get_shape(uonq__xwbu)
        if zbtb__ihwt:
            lwsm__lmho.append(zbtb__ihwt[0])
    if aggregate_node.pivot_arr is not None:
        zbtb__ihwt = equiv_set.get_shape(aggregate_node.pivot_arr)
        if zbtb__ihwt:
            lwsm__lmho.append(zbtb__ihwt[0])
    for wuak__ffigs in aggregate_node.df_in_vars.values():
        zbtb__ihwt = equiv_set.get_shape(wuak__ffigs)
        if zbtb__ihwt:
            lwsm__lmho.append(zbtb__ihwt[0])
    if len(lwsm__lmho) > 1:
        equiv_set.insert_equiv(*lwsm__lmho)
    bzhs__bvvmk = []
    lwsm__lmho = []
    bqo__djcnz = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        bqo__djcnz.extend(aggregate_node.out_key_vars)
    for wuak__ffigs in bqo__djcnz:
        mkwxs__lrb = typemap[wuak__ffigs.name]
        ybii__evjr = array_analysis._gen_shape_call(equiv_set, wuak__ffigs,
            mkwxs__lrb.ndim, None, bzhs__bvvmk)
        equiv_set.insert_equiv(wuak__ffigs, ybii__evjr)
        lwsm__lmho.append(ybii__evjr[0])
        equiv_set.define(wuak__ffigs, set())
    if len(lwsm__lmho) > 1:
        equiv_set.insert_equiv(*lwsm__lmho)
    return [], bzhs__bvvmk


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    cth__cjk = Distribution.OneD
    for wuak__ffigs in aggregate_node.df_in_vars.values():
        cth__cjk = Distribution(min(cth__cjk.value, array_dists[wuak__ffigs
            .name].value))
    for uonq__xwbu in aggregate_node.key_arrs:
        cth__cjk = Distribution(min(cth__cjk.value, array_dists[uonq__xwbu.
            name].value))
    if aggregate_node.pivot_arr is not None:
        cth__cjk = Distribution(min(cth__cjk.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = cth__cjk
    for wuak__ffigs in aggregate_node.df_in_vars.values():
        array_dists[wuak__ffigs.name] = cth__cjk
    for uonq__xwbu in aggregate_node.key_arrs:
        array_dists[uonq__xwbu.name] = cth__cjk
    tsj__bhsxi = Distribution.OneD_Var
    for wuak__ffigs in aggregate_node.df_out_vars.values():
        if wuak__ffigs.name in array_dists:
            tsj__bhsxi = Distribution(min(tsj__bhsxi.value, array_dists[
                wuak__ffigs.name].value))
    if aggregate_node.out_key_vars is not None:
        for wuak__ffigs in aggregate_node.out_key_vars:
            if wuak__ffigs.name in array_dists:
                tsj__bhsxi = Distribution(min(tsj__bhsxi.value, array_dists
                    [wuak__ffigs.name].value))
    tsj__bhsxi = Distribution(min(tsj__bhsxi.value, cth__cjk.value))
    for wuak__ffigs in aggregate_node.df_out_vars.values():
        array_dists[wuak__ffigs.name] = tsj__bhsxi
    if aggregate_node.out_key_vars is not None:
        for tfrn__oocd in aggregate_node.out_key_vars:
            array_dists[tfrn__oocd.name] = tsj__bhsxi
    if tsj__bhsxi != Distribution.OneD_Var:
        for uonq__xwbu in aggregate_node.key_arrs:
            array_dists[uonq__xwbu.name] = tsj__bhsxi
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = tsj__bhsxi
        for wuak__ffigs in aggregate_node.df_in_vars.values():
            array_dists[wuak__ffigs.name] = tsj__bhsxi


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for wuak__ffigs in agg_node.df_out_vars.values():
        definitions[wuak__ffigs.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for tfrn__oocd in agg_node.out_key_vars:
            definitions[tfrn__oocd.name].append(agg_node)
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
        for lbd__niacr in (list(agg_node.df_in_vars.values()) + list(
            agg_node.df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[lbd__niacr.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                lbd__niacr.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    vyqd__drr = tuple(typemap[lbd__niacr.name] for lbd__niacr in agg_node.
        key_arrs)
    dvdj__ulut = [lbd__niacr for pzwy__pkobi, lbd__niacr in agg_node.
        df_in_vars.items()]
    hpuq__elo = [lbd__niacr for pzwy__pkobi, lbd__niacr in agg_node.
        df_out_vars.items()]
    in_col_typs = []
    vfmjt__dzki = []
    if agg_node.pivot_arr is not None:
        for hplx__kaw, bxr__sonsp in agg_node.gb_info_in.items():
            for func, zaxq__zrul in bxr__sonsp:
                if hplx__kaw is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[
                        hplx__kaw].name])
                vfmjt__dzki.append(func)
    else:
        for hplx__kaw, func in agg_node.gb_info_out.values():
            if hplx__kaw is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[hplx__kaw].name]
                    )
            vfmjt__dzki.append(func)
    out_col_typs = tuple(typemap[lbd__niacr.name] for lbd__niacr in hpuq__elo)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(vyqd__drr + tuple(typemap[lbd__niacr.name] for
        lbd__niacr in dvdj__ulut) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    wxs__vtv = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for otykx__bjftt, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            wxs__vtv.update({f'in_cat_dtype_{otykx__bjftt}': in_col_typ})
    for otykx__bjftt, wyvoy__bhanr in enumerate(out_col_typs):
        if isinstance(wyvoy__bhanr, bodo.CategoricalArrayType):
            wxs__vtv.update({f'out_cat_dtype_{otykx__bjftt}': wyvoy__bhanr})
    udf_func_struct = get_udf_func_struct(vfmjt__dzki, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    aeafl__ydxff = gen_top_level_agg_func(agg_node, in_col_typs,
        out_col_typs, parallel, udf_func_struct)
    wxs__vtv.update({'pd': pd, 'pre_alloc_string_array':
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
            wxs__vtv.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            wxs__vtv.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    wwcd__ydnvq = compile_to_numba_ir(aeafl__ydxff, wxs__vtv, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    fpye__yho = []
    if agg_node.pivot_arr is None:
        vrrfc__whcn = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        rtex__lnbrt = ir.Var(vrrfc__whcn, mk_unique_var('dummy_none'), loc)
        typemap[rtex__lnbrt.name] = types.none
        fpye__yho.append(ir.Assign(ir.Const(None, loc), rtex__lnbrt, loc))
        dvdj__ulut.append(rtex__lnbrt)
    else:
        dvdj__ulut.append(agg_node.pivot_arr)
    replace_arg_nodes(wwcd__ydnvq, agg_node.key_arrs + dvdj__ulut)
    eoznx__txmt = wwcd__ydnvq.body[-3]
    assert is_assign(eoznx__txmt) and isinstance(eoznx__txmt.value, ir.Expr
        ) and eoznx__txmt.value.op == 'build_tuple'
    fpye__yho += wwcd__ydnvq.body[:-3]
    bqo__djcnz = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        bqo__djcnz += agg_node.out_key_vars
    for otykx__bjftt, wanas__himyq in enumerate(bqo__djcnz):
        rgl__ewvl = eoznx__txmt.value.items[otykx__bjftt]
        fpye__yho.append(ir.Assign(rgl__ewvl, wanas__himyq, wanas__himyq.loc))
    return fpye__yho


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        xdyys__svuhb = args[0]
        dtype = types.Tuple([t.dtype for t in xdyys__svuhb.types]
            ) if isinstance(xdyys__svuhb, types.BaseTuple
            ) else xdyys__svuhb.dtype
        if isinstance(xdyys__svuhb, types.BaseTuple) and len(xdyys__svuhb.types
            ) == 1:
            dtype = xdyys__svuhb.types[0].dtype
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
        obh__uajh = args[0]
        if obh__uajh == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    kssry__kbwr = context.compile_internal(builder, lambda a: False, sig, args)
    return kssry__kbwr


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        qrqi__eqjx = IntDtype(t.dtype).name
        assert qrqi__eqjx.endswith('Dtype()')
        qrqi__eqjx = qrqi__eqjx[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{qrqi__eqjx}'))"
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
        szz__wfh = 'in' if is_input else 'out'
        return f'bodo.utils.utils.alloc_type(1, {szz__wfh}_cat_dtype_{colnum})'
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
    bapa__xaho = udf_func_struct.var_typs
    dxyp__niqon = len(bapa__xaho)
    nnuh__vkrj = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    nnuh__vkrj += '    if is_null_pointer(in_table):\n'
    nnuh__vkrj += '        return\n'
    nnuh__vkrj += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in bapa__xaho]), 
        ',' if len(bapa__xaho) == 1 else '')
    xucc__iowgx = n_keys
    upkvb__ruy = []
    redvar_offsets = []
    ktmzs__kgxlh = []
    if do_combine:
        for otykx__bjftt, bxt__chl in enumerate(allfuncs):
            if bxt__chl.ftype != 'udf':
                xucc__iowgx += bxt__chl.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(xucc__iowgx, xucc__iowgx +
                    bxt__chl.n_redvars))
                xucc__iowgx += bxt__chl.n_redvars
                ktmzs__kgxlh.append(data_in_typs_[func_idx_to_in_col[
                    otykx__bjftt]])
                upkvb__ruy.append(func_idx_to_in_col[otykx__bjftt] + n_keys)
    else:
        for otykx__bjftt, bxt__chl in enumerate(allfuncs):
            if bxt__chl.ftype != 'udf':
                xucc__iowgx += bxt__chl.ncols_post_shuffle
            else:
                redvar_offsets += list(range(xucc__iowgx + 1, xucc__iowgx +
                    1 + bxt__chl.n_redvars))
                xucc__iowgx += bxt__chl.n_redvars + 1
                ktmzs__kgxlh.append(data_in_typs_[func_idx_to_in_col[
                    otykx__bjftt]])
                upkvb__ruy.append(func_idx_to_in_col[otykx__bjftt] + n_keys)
    assert len(redvar_offsets) == dxyp__niqon
    mne__kffl = len(ktmzs__kgxlh)
    ylob__grk = []
    for otykx__bjftt, t in enumerate(ktmzs__kgxlh):
        ylob__grk.append(_gen_dummy_alloc(t, otykx__bjftt, True))
    nnuh__vkrj += '    data_in_dummy = ({}{})\n'.format(','.join(ylob__grk),
        ',' if len(ktmzs__kgxlh) == 1 else '')
    nnuh__vkrj += """
    # initialize redvar cols
"""
    nnuh__vkrj += '    init_vals = __init_func()\n'
    for otykx__bjftt in range(dxyp__niqon):
        nnuh__vkrj += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(otykx__bjftt, redvar_offsets[otykx__bjftt], otykx__bjftt))
        nnuh__vkrj += '    incref(redvar_arr_{})\n'.format(otykx__bjftt)
        nnuh__vkrj += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            otykx__bjftt, otykx__bjftt)
    nnuh__vkrj += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(otykx__bjftt) for otykx__bjftt in range(dxyp__niqon)]), ',' if
        dxyp__niqon == 1 else '')
    nnuh__vkrj += '\n'
    for otykx__bjftt in range(mne__kffl):
        nnuh__vkrj += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(otykx__bjftt, upkvb__ruy[otykx__bjftt], otykx__bjftt))
        nnuh__vkrj += '    incref(data_in_{})\n'.format(otykx__bjftt)
    nnuh__vkrj += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(otykx__bjftt) for otykx__bjftt in range(mne__kffl)]), ',' if
        mne__kffl == 1 else '')
    nnuh__vkrj += '\n'
    nnuh__vkrj += '    for i in range(len(data_in_0)):\n'
    nnuh__vkrj += '        w_ind = row_to_group[i]\n'
    nnuh__vkrj += '        if w_ind != -1:\n'
    nnuh__vkrj += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    fvr__irwk = {}
    exec(nnuh__vkrj, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, fvr__irwk)
    return fvr__irwk['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    bapa__xaho = udf_func_struct.var_typs
    dxyp__niqon = len(bapa__xaho)
    nnuh__vkrj = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    nnuh__vkrj += '    if is_null_pointer(in_table):\n'
    nnuh__vkrj += '        return\n'
    nnuh__vkrj += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in bapa__xaho]), 
        ',' if len(bapa__xaho) == 1 else '')
    izbj__hszd = n_keys
    iitlt__wxd = n_keys
    lru__urf = []
    jwnat__qusz = []
    for bxt__chl in allfuncs:
        if bxt__chl.ftype != 'udf':
            izbj__hszd += bxt__chl.ncols_pre_shuffle
            iitlt__wxd += bxt__chl.ncols_post_shuffle
        else:
            lru__urf += list(range(izbj__hszd, izbj__hszd + bxt__chl.n_redvars)
                )
            jwnat__qusz += list(range(iitlt__wxd + 1, iitlt__wxd + 1 +
                bxt__chl.n_redvars))
            izbj__hszd += bxt__chl.n_redvars
            iitlt__wxd += 1 + bxt__chl.n_redvars
    assert len(lru__urf) == dxyp__niqon
    nnuh__vkrj += """
    # initialize redvar cols
"""
    nnuh__vkrj += '    init_vals = __init_func()\n'
    for otykx__bjftt in range(dxyp__niqon):
        nnuh__vkrj += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(otykx__bjftt, jwnat__qusz[otykx__bjftt], otykx__bjftt))
        nnuh__vkrj += '    incref(redvar_arr_{})\n'.format(otykx__bjftt)
        nnuh__vkrj += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            otykx__bjftt, otykx__bjftt)
    nnuh__vkrj += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(otykx__bjftt) for otykx__bjftt in range(dxyp__niqon)]), ',' if
        dxyp__niqon == 1 else '')
    nnuh__vkrj += '\n'
    for otykx__bjftt in range(dxyp__niqon):
        nnuh__vkrj += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(otykx__bjftt, lru__urf[otykx__bjftt], otykx__bjftt))
        nnuh__vkrj += '    incref(recv_redvar_arr_{})\n'.format(otykx__bjftt)
    nnuh__vkrj += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(otykx__bjftt) for otykx__bjftt in range
        (dxyp__niqon)]), ',' if dxyp__niqon == 1 else '')
    nnuh__vkrj += '\n'
    if dxyp__niqon:
        nnuh__vkrj += '    for i in range(len(recv_redvar_arr_0)):\n'
        nnuh__vkrj += '        w_ind = row_to_group[i]\n'
        nnuh__vkrj += """        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)
"""
    fvr__irwk = {}
    exec(nnuh__vkrj, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, fvr__irwk)
    return fvr__irwk['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    bapa__xaho = udf_func_struct.var_typs
    dxyp__niqon = len(bapa__xaho)
    xucc__iowgx = n_keys
    redvar_offsets = []
    rvv__omf = []
    out_data_typs = []
    for otykx__bjftt, bxt__chl in enumerate(allfuncs):
        if bxt__chl.ftype != 'udf':
            xucc__iowgx += bxt__chl.ncols_post_shuffle
        else:
            rvv__omf.append(xucc__iowgx)
            redvar_offsets += list(range(xucc__iowgx + 1, xucc__iowgx + 1 +
                bxt__chl.n_redvars))
            xucc__iowgx += 1 + bxt__chl.n_redvars
            out_data_typs.append(out_data_typs_[otykx__bjftt])
    assert len(redvar_offsets) == dxyp__niqon
    mne__kffl = len(out_data_typs)
    nnuh__vkrj = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    nnuh__vkrj += '    if is_null_pointer(table):\n'
    nnuh__vkrj += '        return\n'
    nnuh__vkrj += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in bapa__xaho]), 
        ',' if len(bapa__xaho) == 1 else '')
    nnuh__vkrj += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for otykx__bjftt in range(dxyp__niqon):
        nnuh__vkrj += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(otykx__bjftt, redvar_offsets[otykx__bjftt], otykx__bjftt))
        nnuh__vkrj += '    incref(redvar_arr_{})\n'.format(otykx__bjftt)
    nnuh__vkrj += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(otykx__bjftt) for otykx__bjftt in range(dxyp__niqon)]), ',' if
        dxyp__niqon == 1 else '')
    nnuh__vkrj += '\n'
    for otykx__bjftt in range(mne__kffl):
        nnuh__vkrj += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(otykx__bjftt, rvv__omf[otykx__bjftt], otykx__bjftt))
        nnuh__vkrj += '    incref(data_out_{})\n'.format(otykx__bjftt)
    nnuh__vkrj += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(otykx__bjftt) for otykx__bjftt in range(mne__kffl)]), ',' if
        mne__kffl == 1 else '')
    nnuh__vkrj += '\n'
    nnuh__vkrj += '    for i in range(len(data_out_0)):\n'
    nnuh__vkrj += '        __eval_res(redvars, data_out, i)\n'
    fvr__irwk = {}
    exec(nnuh__vkrj, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, fvr__irwk)
    return fvr__irwk['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    xucc__iowgx = n_keys
    nnlj__irncg = []
    for otykx__bjftt, bxt__chl in enumerate(allfuncs):
        if bxt__chl.ftype == 'gen_udf':
            nnlj__irncg.append(xucc__iowgx)
            xucc__iowgx += 1
        elif bxt__chl.ftype != 'udf':
            xucc__iowgx += bxt__chl.ncols_post_shuffle
        else:
            xucc__iowgx += bxt__chl.n_redvars + 1
    nnuh__vkrj = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    nnuh__vkrj += '    if num_groups == 0:\n'
    nnuh__vkrj += '        return\n'
    for otykx__bjftt, func in enumerate(udf_func_struct.general_udf_funcs):
        nnuh__vkrj += '    # col {}\n'.format(otykx__bjftt)
        nnuh__vkrj += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(nnlj__irncg[otykx__bjftt], otykx__bjftt))
        nnuh__vkrj += '    incref(out_col)\n'
        nnuh__vkrj += '    for j in range(num_groups):\n'
        nnuh__vkrj += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(otykx__bjftt, otykx__bjftt))
        nnuh__vkrj += '        incref(in_col)\n'
        nnuh__vkrj += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(otykx__bjftt))
    wxs__vtv = {'pd': pd, 'info_to_array': info_to_array, 'info_from_table':
        info_from_table, 'incref': incref}
    rwba__vcy = 0
    for otykx__bjftt, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[rwba__vcy]
        wxs__vtv['func_{}'.format(rwba__vcy)] = func
        wxs__vtv['in_col_{}_typ'.format(rwba__vcy)] = in_col_typs[
            func_idx_to_in_col[otykx__bjftt]]
        wxs__vtv['out_col_{}_typ'.format(rwba__vcy)] = out_col_typs[
            otykx__bjftt]
        rwba__vcy += 1
    fvr__irwk = {}
    exec(nnuh__vkrj, wxs__vtv, fvr__irwk)
    bxt__chl = fvr__irwk['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    ejmvv__atr = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(ejmvv__atr, nopython=True)(bxt__chl)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    nlej__wpbqb = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        ygn__pgm = 1
    else:
        ygn__pgm = len(agg_node.pivot_values)
    vow__trvhe = tuple('key_' + sanitize_varname(dgu__iydar) for dgu__iydar in
        agg_node.key_names)
    rob__horp = {dgu__iydar: 'in_{}'.format(sanitize_varname(dgu__iydar)) for
        dgu__iydar in agg_node.gb_info_in.keys() if dgu__iydar is not None}
    smov__tkn = {dgu__iydar: ('out_' + sanitize_varname(dgu__iydar)) for
        dgu__iydar in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    baa__dfn = ', '.join(vow__trvhe)
    csyy__qst = ', '.join(rob__horp.values())
    if csyy__qst != '':
        csyy__qst = ', ' + csyy__qst
    nnuh__vkrj = 'def agg_top({}{}{}, pivot_arr):\n'.format(baa__dfn,
        csyy__qst, ', index_arg' if agg_node.input_has_index else '')
    for a in (vow__trvhe + tuple(rob__horp.values())):
        nnuh__vkrj += f'    {a} = decode_if_dict_array({a})\n'
    if nlej__wpbqb:
        nnuh__vkrj += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        pkabo__imzc = []
        for hplx__kaw, bxr__sonsp in agg_node.gb_info_in.items():
            if hplx__kaw is not None:
                for func, zaxq__zrul in bxr__sonsp:
                    pkabo__imzc.append(rob__horp[hplx__kaw])
    else:
        pkabo__imzc = tuple(rob__horp[hplx__kaw] for hplx__kaw, zaxq__zrul in
            agg_node.gb_info_out.values() if hplx__kaw is not None)
    vdjm__rxcxw = vow__trvhe + tuple(pkabo__imzc)
    nnuh__vkrj += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in vdjm__rxcxw), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    nnuh__vkrj += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    odli__vmytq = []
    func_idx_to_in_col = []
    cwnz__rzf = []
    aika__pkm = False
    vmwog__tfkc = 1
    msj__ruf = -1
    pkyr__hblps = 0
    xbc__flenm = 0
    if not nlej__wpbqb:
        vfmjt__dzki = [func for zaxq__zrul, func in agg_node.gb_info_out.
            values()]
    else:
        vfmjt__dzki = [func for func, zaxq__zrul in bxr__sonsp for
            bxr__sonsp in agg_node.gb_info_in.values()]
    for qcp__jtbio, func in enumerate(vfmjt__dzki):
        odli__vmytq.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            pkyr__hblps += 1
        if hasattr(func, 'skipdropna'):
            aika__pkm = func.skipdropna
        if func.ftype == 'shift':
            vmwog__tfkc = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            xbc__flenm = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            msj__ruf = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(qcp__jtbio)
        if func.ftype == 'udf':
            cwnz__rzf.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            cwnz__rzf.append(0)
            do_combine = False
    odli__vmytq.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == ygn__pgm, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * ygn__pgm, 'invalid number of groupby outputs'
    if pkyr__hblps > 0:
        if pkyr__hblps != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for otykx__bjftt, dgu__iydar in enumerate(agg_node.gb_info_out.keys()):
        brwsh__pmijk = smov__tkn[dgu__iydar] + '_dummy'
        wyvoy__bhanr = out_col_typs[otykx__bjftt]
        hplx__kaw, func = agg_node.gb_info_out[dgu__iydar]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(wyvoy__bhanr, bodo.
            CategoricalArrayType):
            nnuh__vkrj += '    {} = {}\n'.format(brwsh__pmijk, rob__horp[
                hplx__kaw])
        elif udf_func_struct is not None:
            nnuh__vkrj += '    {} = {}\n'.format(brwsh__pmijk,
                _gen_dummy_alloc(wyvoy__bhanr, otykx__bjftt, False))
    if udf_func_struct is not None:
        ujxiv__kef = next_label()
        if udf_func_struct.regular_udfs:
            ejmvv__atr = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            qih__taph = numba.cfunc(ejmvv__atr, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, ujxiv__kef))
            nalcu__rxa = numba.cfunc(ejmvv__atr, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, ujxiv__kef))
            mjsb__koklj = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                ujxiv__kef))
            udf_func_struct.set_regular_cfuncs(qih__taph, nalcu__rxa,
                mjsb__koklj)
            for lta__bqmf in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[lta__bqmf.native_name] = lta__bqmf
                gb_agg_cfunc_addr[lta__bqmf.native_name] = lta__bqmf.address
        if udf_func_struct.general_udfs:
            qecmu__cjtvq = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                ujxiv__kef)
            udf_func_struct.set_general_cfunc(qecmu__cjtvq)
        yxgfw__aaks = []
        hxa__oicx = 0
        otykx__bjftt = 0
        for brwsh__pmijk, bxt__chl in zip(smov__tkn.values(), allfuncs):
            if bxt__chl.ftype in ('udf', 'gen_udf'):
                yxgfw__aaks.append(brwsh__pmijk + '_dummy')
                for cmf__oskse in range(hxa__oicx, hxa__oicx + cwnz__rzf[
                    otykx__bjftt]):
                    yxgfw__aaks.append('data_redvar_dummy_' + str(cmf__oskse))
                hxa__oicx += cwnz__rzf[otykx__bjftt]
                otykx__bjftt += 1
        if udf_func_struct.regular_udfs:
            bapa__xaho = udf_func_struct.var_typs
            for otykx__bjftt, t in enumerate(bapa__xaho):
                nnuh__vkrj += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(otykx__bjftt, _get_np_dtype(t)))
        nnuh__vkrj += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in yxgfw__aaks))
        nnuh__vkrj += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            nnuh__vkrj += ("    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".
                format(qih__taph.native_name))
            nnuh__vkrj += ("    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".
                format(nalcu__rxa.native_name))
            nnuh__vkrj += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                mjsb__koklj.native_name)
            nnuh__vkrj += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(qih__taph.native_name))
            nnuh__vkrj += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(nalcu__rxa.native_name))
            nnuh__vkrj += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n"
                .format(mjsb__koklj.native_name))
        else:
            nnuh__vkrj += '    cpp_cb_update_addr = 0\n'
            nnuh__vkrj += '    cpp_cb_combine_addr = 0\n'
            nnuh__vkrj += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            lta__bqmf = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[lta__bqmf.native_name] = lta__bqmf
            gb_agg_cfunc_addr[lta__bqmf.native_name] = lta__bqmf.address
            nnuh__vkrj += ("    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".
                format(lta__bqmf.native_name))
            nnuh__vkrj += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(lta__bqmf.native_name))
        else:
            nnuh__vkrj += '    cpp_cb_general_addr = 0\n'
    else:
        nnuh__vkrj += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        nnuh__vkrj += '    cpp_cb_update_addr = 0\n'
        nnuh__vkrj += '    cpp_cb_combine_addr = 0\n'
        nnuh__vkrj += '    cpp_cb_eval_addr = 0\n'
        nnuh__vkrj += '    cpp_cb_general_addr = 0\n'
    nnuh__vkrj += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(bxt__chl.ftype)) for
        bxt__chl in allfuncs] + ['0']))
    nnuh__vkrj += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(
        str(odli__vmytq))
    if len(cwnz__rzf) > 0:
        nnuh__vkrj += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(
            str(cwnz__rzf))
    else:
        nnuh__vkrj += '    udf_ncols = np.array([0], np.int32)\n'
    if nlej__wpbqb:
        nnuh__vkrj += '    arr_type = coerce_to_array({})\n'.format(agg_node
            .pivot_values)
        nnuh__vkrj += '    arr_info = array_to_info(arr_type)\n'
        nnuh__vkrj += (
            '    dispatch_table = arr_info_list_to_table([arr_info])\n')
        nnuh__vkrj += '    pivot_info = array_to_info(pivot_arr)\n'
        nnuh__vkrj += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        nnuh__vkrj += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, aika__pkm, agg_node.return_key, agg_node.same_index))
        nnuh__vkrj += '    delete_info_decref_array(pivot_info)\n'
        nnuh__vkrj += '    delete_info_decref_array(arr_info)\n'
    else:
        nnuh__vkrj += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, aika__pkm,
            vmwog__tfkc, xbc__flenm, msj__ruf, agg_node.return_key,
            agg_node.same_index, agg_node.dropna))
    sisyq__avk = 0
    if agg_node.return_key:
        for otykx__bjftt, najv__tmzi in enumerate(vow__trvhe):
            nnuh__vkrj += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(najv__tmzi, sisyq__avk, najv__tmzi))
            sisyq__avk += 1
    for otykx__bjftt, brwsh__pmijk in enumerate(smov__tkn.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(wyvoy__bhanr, bodo.
            CategoricalArrayType):
            nnuh__vkrj += f"""    {brwsh__pmijk} = info_to_array(info_from_table(out_table, {sisyq__avk}), {brwsh__pmijk + '_dummy'})
"""
        else:
            nnuh__vkrj += f"""    {brwsh__pmijk} = info_to_array(info_from_table(out_table, {sisyq__avk}), out_typs[{otykx__bjftt}])
"""
        sisyq__avk += 1
    if agg_node.same_index:
        nnuh__vkrj += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(sisyq__avk))
        sisyq__avk += 1
    nnuh__vkrj += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    nnuh__vkrj += '    delete_table_decref_arrays(table)\n'
    nnuh__vkrj += '    delete_table_decref_arrays(udf_table_dummy)\n'
    nnuh__vkrj += '    delete_table(out_table)\n'
    nnuh__vkrj += f'    ev_clean.finalize()\n'
    eudq__oip = tuple(smov__tkn.values())
    if agg_node.return_key:
        eudq__oip += tuple(vow__trvhe)
    nnuh__vkrj += '    return ({},{})\n'.format(', '.join(eudq__oip), 
        ' out_index_arg,' if agg_node.same_index else '')
    fvr__irwk = {}
    exec(nnuh__vkrj, {'out_typs': out_col_typs}, fvr__irwk)
    poq__dywp = fvr__irwk['agg_top']
    return poq__dywp


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for kvam__ccu in block.body:
            if is_call_assign(kvam__ccu) and find_callname(f_ir, kvam__ccu.
                value) == ('len', 'builtins') and kvam__ccu.value.args[0
                ].name == f_ir.arg_names[0]:
                ywj__fmjch = get_definition(f_ir, kvam__ccu.value.func)
                ywj__fmjch.name = 'dummy_agg_count'
                ywj__fmjch.value = dummy_agg_count
    rlxn__jyrjm = get_name_var_table(f_ir.blocks)
    cwet__vcu = {}
    for name, zaxq__zrul in rlxn__jyrjm.items():
        cwet__vcu[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, cwet__vcu)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    zyaus__xte = numba.core.compiler.Flags()
    zyaus__xte.nrt = True
    haptt__naa = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, zyaus__xte)
    haptt__naa.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, bpchi__ddg, calltypes, zaxq__zrul = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    vzij__vtru = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    fztb__dtxa = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    pbm__hjfgl = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    kvc__xor = pbm__hjfgl(typemap, calltypes)
    pm = fztb__dtxa(typingctx, targetctx, None, f_ir, typemap, bpchi__ddg,
        calltypes, kvc__xor, {}, zyaus__xte, None)
    nsy__gzbgn = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = fztb__dtxa(typingctx, targetctx, None, f_ir, typemap, bpchi__ddg,
        calltypes, kvc__xor, {}, zyaus__xte, nsy__gzbgn)
    lyo__savr = numba.core.typed_passes.InlineOverloads()
    lyo__savr.run_pass(pm)
    npqq__frq = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    npqq__frq.run()
    for block in f_ir.blocks.values():
        for kvam__ccu in block.body:
            if is_assign(kvam__ccu) and isinstance(kvam__ccu.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[kvam__ccu.target.name],
                SeriesType):
                mkwxs__lrb = typemap.pop(kvam__ccu.target.name)
                typemap[kvam__ccu.target.name] = mkwxs__lrb.data
            if is_call_assign(kvam__ccu) and find_callname(f_ir, kvam__ccu.
                value) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[kvam__ccu.target.name].remove(kvam__ccu.value
                    )
                kvam__ccu.value = kvam__ccu.value.args[0]
                f_ir._definitions[kvam__ccu.target.name].append(kvam__ccu.value
                    )
            if is_call_assign(kvam__ccu) and find_callname(f_ir, kvam__ccu.
                value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[kvam__ccu.target.name].remove(kvam__ccu.value
                    )
                kvam__ccu.value = ir.Const(False, kvam__ccu.loc)
                f_ir._definitions[kvam__ccu.target.name].append(kvam__ccu.value
                    )
            if is_call_assign(kvam__ccu) and find_callname(f_ir, kvam__ccu.
                value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[kvam__ccu.target.name].remove(kvam__ccu.value
                    )
                kvam__ccu.value = ir.Const(False, kvam__ccu.loc)
                f_ir._definitions[kvam__ccu.target.name].append(kvam__ccu.value
                    )
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    uyz__krci = numba.parfors.parfor.PreParforPass(f_ir, typemap, calltypes,
        typingctx, targetctx, vzij__vtru)
    uyz__krci.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    dsri__gcea = numba.core.compiler.StateDict()
    dsri__gcea.func_ir = f_ir
    dsri__gcea.typemap = typemap
    dsri__gcea.calltypes = calltypes
    dsri__gcea.typingctx = typingctx
    dsri__gcea.targetctx = targetctx
    dsri__gcea.return_type = bpchi__ddg
    numba.core.rewrites.rewrite_registry.apply('after-inference', dsri__gcea)
    hnqv__bnyoa = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        bpchi__ddg, typingctx, targetctx, vzij__vtru, zyaus__xte, {})
    hnqv__bnyoa.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            xfu__zwmj = ctypes.pythonapi.PyCell_Get
            xfu__zwmj.restype = ctypes.py_object
            xfu__zwmj.argtypes = ctypes.py_object,
            izhxa__lcszu = tuple(xfu__zwmj(sqp__hox) for sqp__hox in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            izhxa__lcszu = closure.items
        assert len(code.co_freevars) == len(izhxa__lcszu)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks,
            izhxa__lcszu)


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
        ktyz__befb = SeriesType(in_col_typ.dtype, in_col_typ, None, string_type
            )
        f_ir, pm = compile_to_optimized_ir(func, (ktyz__befb,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        afde__vkzyi, arr_var = _rm_arg_agg_block(block, pm.typemap)
        hjly__jdgi = -1
        for otykx__bjftt, kvam__ccu in enumerate(afde__vkzyi):
            if isinstance(kvam__ccu, numba.parfors.parfor.Parfor):
                assert hjly__jdgi == -1, 'only one parfor for aggregation function'
                hjly__jdgi = otykx__bjftt
        parfor = None
        if hjly__jdgi != -1:
            parfor = afde__vkzyi[hjly__jdgi]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = afde__vkzyi[:hjly__jdgi] + parfor.init_block.body
        eval_nodes = afde__vkzyi[hjly__jdgi + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for kvam__ccu in init_nodes:
            if is_assign(kvam__ccu) and kvam__ccu.target.name in redvars:
                ind = redvars.index(kvam__ccu.target.name)
                reduce_vars[ind] = kvam__ccu.target
        var_types = [pm.typemap[lbd__niacr] for lbd__niacr in redvars]
        nhggp__ovtf = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        ueqn__gyp = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        dazo__ahhn = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(dazo__ahhn)
        self.all_update_funcs.append(ueqn__gyp)
        self.all_combine_funcs.append(nhggp__ovtf)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        joau__gyfo = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        ytwp__snc = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        euepj__xzpx = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        ntke__ikzw = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return (self.all_vartypes, joau__gyfo, ytwp__snc, euepj__xzpx,
            ntke__ikzw)


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
    comd__jgle = []
    for t, bxt__chl in zip(in_col_types, agg_func):
        comd__jgle.append((t, bxt__chl))
    agu__hurxg = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    lahwx__nev = GeneralUDFGenerator()
    for in_col_typ, func in comd__jgle:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            agu__hurxg.add_udf(in_col_typ, func)
        except:
            lahwx__nev.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = agu__hurxg.gen_all_func()
    general_udf_funcs = lahwx__nev.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    ogqzu__bwv = compute_use_defs(parfor.loop_body)
    xkhd__zmy = set()
    for bjvnd__wpzkf in ogqzu__bwv.usemap.values():
        xkhd__zmy |= bjvnd__wpzkf
    uavpi__etbg = set()
    for bjvnd__wpzkf in ogqzu__bwv.defmap.values():
        uavpi__etbg |= bjvnd__wpzkf
    qbl__vwem = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    qbl__vwem.body = eval_nodes
    qlz__tvdt = compute_use_defs({(0): qbl__vwem})
    yqlnx__zzegx = qlz__tvdt.usemap[0]
    kgbya__sdjz = set()
    srfhx__ogjo = []
    tcoi__tyws = []
    for kvam__ccu in reversed(init_nodes):
        vrk__vnqe = {lbd__niacr.name for lbd__niacr in kvam__ccu.list_vars()}
        if is_assign(kvam__ccu):
            lbd__niacr = kvam__ccu.target.name
            vrk__vnqe.remove(lbd__niacr)
            if (lbd__niacr in xkhd__zmy and lbd__niacr not in kgbya__sdjz and
                lbd__niacr not in yqlnx__zzegx and lbd__niacr not in
                uavpi__etbg):
                tcoi__tyws.append(kvam__ccu)
                xkhd__zmy |= vrk__vnqe
                uavpi__etbg.add(lbd__niacr)
                continue
        kgbya__sdjz |= vrk__vnqe
        srfhx__ogjo.append(kvam__ccu)
    tcoi__tyws.reverse()
    srfhx__ogjo.reverse()
    erp__pjf = min(parfor.loop_body.keys())
    usig__anq = parfor.loop_body[erp__pjf]
    usig__anq.body = tcoi__tyws + usig__anq.body
    return srfhx__ogjo


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    edkwz__mprr = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    nll__hmu = set()
    pnb__yvo = []
    for kvam__ccu in init_nodes:
        if is_assign(kvam__ccu) and isinstance(kvam__ccu.value, ir.Global
            ) and isinstance(kvam__ccu.value.value, pytypes.FunctionType
            ) and kvam__ccu.value.value in edkwz__mprr:
            nll__hmu.add(kvam__ccu.target.name)
        elif is_call_assign(kvam__ccu
            ) and kvam__ccu.value.func.name in nll__hmu:
            pass
        else:
            pnb__yvo.append(kvam__ccu)
    init_nodes = pnb__yvo
    omf__jlcev = types.Tuple(var_types)
    qigz__exh = lambda : None
    f_ir = compile_to_numba_ir(qigz__exh, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    xvqh__puow = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    fwb__kqb = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc), xvqh__puow, loc
        )
    block.body = block.body[-2:]
    block.body = init_nodes + [fwb__kqb] + block.body
    block.body[-2].value.value = xvqh__puow
    lohd__slz = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        omf__jlcev, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rhor__sliwl = numba.core.target_extension.dispatcher_registry[cpu_target](
        qigz__exh)
    rhor__sliwl.add_overload(lohd__slz)
    return rhor__sliwl


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    cmog__wdz = len(update_funcs)
    zvxyt__zvv = len(in_col_types)
    if pivot_values is not None:
        assert zvxyt__zvv == 1
    nnuh__vkrj = (
        'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        lkwz__wxn = redvar_offsets[zvxyt__zvv]
        nnuh__vkrj += '  pv = pivot_arr[i]\n'
        for cmf__oskse, ikmt__ldude in enumerate(pivot_values):
            etkz__bwd = 'el' if cmf__oskse != 0 else ''
            nnuh__vkrj += "  {}if pv == '{}':\n".format(etkz__bwd, ikmt__ldude)
            ytzth__wla = lkwz__wxn * cmf__oskse
            jsu__ueeqb = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                otykx__bjftt) for otykx__bjftt in range(ytzth__wla +
                redvar_offsets[0], ytzth__wla + redvar_offsets[1])])
            wco__xbbd = 'data_in[0][i]'
            if is_crosstab:
                wco__xbbd = '0'
            nnuh__vkrj += '    {} = update_vars_0({}, {})\n'.format(jsu__ueeqb,
                jsu__ueeqb, wco__xbbd)
    else:
        for cmf__oskse in range(cmog__wdz):
            jsu__ueeqb = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                otykx__bjftt) for otykx__bjftt in range(redvar_offsets[
                cmf__oskse], redvar_offsets[cmf__oskse + 1])])
            if jsu__ueeqb:
                nnuh__vkrj += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(jsu__ueeqb, cmf__oskse, jsu__ueeqb, 0 if 
                    zvxyt__zvv == 1 else cmf__oskse))
    nnuh__vkrj += '  return\n'
    wxs__vtv = {}
    for otykx__bjftt, bxt__chl in enumerate(update_funcs):
        wxs__vtv['update_vars_{}'.format(otykx__bjftt)] = bxt__chl
    fvr__irwk = {}
    exec(nnuh__vkrj, wxs__vtv, fvr__irwk)
    rkt__deef = fvr__irwk['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(rkt__deef)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    zteh__ujbsi = types.Tuple([types.Array(t, 1, 'C') for t in
        reduce_var_types])
    arg_typs = zteh__ujbsi, zteh__ujbsi, types.intp, types.intp, pivot_typ
    xlzc__god = len(redvar_offsets) - 1
    lkwz__wxn = redvar_offsets[xlzc__god]
    nnuh__vkrj = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert xlzc__god == 1
        for cgqrf__iogju in range(len(pivot_values)):
            ytzth__wla = lkwz__wxn * cgqrf__iogju
            jsu__ueeqb = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                otykx__bjftt) for otykx__bjftt in range(ytzth__wla +
                redvar_offsets[0], ytzth__wla + redvar_offsets[1])])
            apycf__qpftl = ', '.join(['recv_arrs[{}][i]'.format(
                otykx__bjftt) for otykx__bjftt in range(ytzth__wla +
                redvar_offsets[0], ytzth__wla + redvar_offsets[1])])
            nnuh__vkrj += '  {} = combine_vars_0({}, {})\n'.format(jsu__ueeqb,
                jsu__ueeqb, apycf__qpftl)
    else:
        for cmf__oskse in range(xlzc__god):
            jsu__ueeqb = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                otykx__bjftt) for otykx__bjftt in range(redvar_offsets[
                cmf__oskse], redvar_offsets[cmf__oskse + 1])])
            apycf__qpftl = ', '.join(['recv_arrs[{}][i]'.format(
                otykx__bjftt) for otykx__bjftt in range(redvar_offsets[
                cmf__oskse], redvar_offsets[cmf__oskse + 1])])
            if apycf__qpftl:
                nnuh__vkrj += '  {} = combine_vars_{}({}, {})\n'.format(
                    jsu__ueeqb, cmf__oskse, jsu__ueeqb, apycf__qpftl)
    nnuh__vkrj += '  return\n'
    wxs__vtv = {}
    for otykx__bjftt, bxt__chl in enumerate(combine_funcs):
        wxs__vtv['combine_vars_{}'.format(otykx__bjftt)] = bxt__chl
    fvr__irwk = {}
    exec(nnuh__vkrj, wxs__vtv, fvr__irwk)
    kgwnb__lls = fvr__irwk['combine_all_f']
    f_ir = compile_to_numba_ir(kgwnb__lls, wxs__vtv)
    euepj__xzpx = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rhor__sliwl = numba.core.target_extension.dispatcher_registry[cpu_target](
        kgwnb__lls)
    rhor__sliwl.add_overload(euepj__xzpx)
    return rhor__sliwl


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    zteh__ujbsi = types.Tuple([types.Array(t, 1, 'C') for t in
        reduce_var_types])
    out_col_typs = types.Tuple(out_col_typs)
    xlzc__god = len(redvar_offsets) - 1
    lkwz__wxn = redvar_offsets[xlzc__god]
    nnuh__vkrj = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert xlzc__god == 1
        for cmf__oskse in range(len(pivot_values)):
            ytzth__wla = lkwz__wxn * cmf__oskse
            jsu__ueeqb = ', '.join(['redvar_arrs[{}][j]'.format(
                otykx__bjftt) for otykx__bjftt in range(ytzth__wla +
                redvar_offsets[0], ytzth__wla + redvar_offsets[1])])
            nnuh__vkrj += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                cmf__oskse, jsu__ueeqb)
    else:
        for cmf__oskse in range(xlzc__god):
            jsu__ueeqb = ', '.join(['redvar_arrs[{}][j]'.format(
                otykx__bjftt) for otykx__bjftt in range(redvar_offsets[
                cmf__oskse], redvar_offsets[cmf__oskse + 1])])
            nnuh__vkrj += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                cmf__oskse, cmf__oskse, jsu__ueeqb)
    nnuh__vkrj += '  return\n'
    wxs__vtv = {}
    for otykx__bjftt, bxt__chl in enumerate(eval_funcs):
        wxs__vtv['eval_vars_{}'.format(otykx__bjftt)] = bxt__chl
    fvr__irwk = {}
    exec(nnuh__vkrj, wxs__vtv, fvr__irwk)
    cnz__seffo = fvr__irwk['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(cnz__seffo)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    zvz__hrpy = len(var_types)
    mzjz__rveo = [f'in{otykx__bjftt}' for otykx__bjftt in range(zvz__hrpy)]
    omf__jlcev = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    bnnkc__thng = omf__jlcev(0)
    nnuh__vkrj = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        mzjz__rveo))
    fvr__irwk = {}
    exec(nnuh__vkrj, {'_zero': bnnkc__thng}, fvr__irwk)
    omp__keat = fvr__irwk['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(omp__keat, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': bnnkc__thng}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    edd__bux = []
    for otykx__bjftt, lbd__niacr in enumerate(reduce_vars):
        edd__bux.append(ir.Assign(block.body[otykx__bjftt].target,
            lbd__niacr, lbd__niacr.loc))
        for yno__wpizb in lbd__niacr.versioned_names:
            edd__bux.append(ir.Assign(lbd__niacr, ir.Var(lbd__niacr.scope,
                yno__wpizb, lbd__niacr.loc), lbd__niacr.loc))
    block.body = block.body[:zvz__hrpy] + edd__bux + eval_nodes
    dazo__ahhn = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        omf__jlcev, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rhor__sliwl = numba.core.target_extension.dispatcher_registry[cpu_target](
        omp__keat)
    rhor__sliwl.add_overload(dazo__ahhn)
    return rhor__sliwl


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    zvz__hrpy = len(redvars)
    hlntk__vos = [f'v{otykx__bjftt}' for otykx__bjftt in range(zvz__hrpy)]
    mzjz__rveo = [f'in{otykx__bjftt}' for otykx__bjftt in range(zvz__hrpy)]
    nnuh__vkrj = 'def agg_combine({}):\n'.format(', '.join(hlntk__vos +
        mzjz__rveo))
    fnwgd__lvmgh = wrap_parfor_blocks(parfor)
    wrv__mphne = find_topo_order(fnwgd__lvmgh)
    wrv__mphne = wrv__mphne[1:]
    unwrap_parfor_blocks(parfor)
    kata__pyxt = {}
    uvh__ppl = []
    for tcila__thmcg in wrv__mphne:
        vvye__vemw = parfor.loop_body[tcila__thmcg]
        for kvam__ccu in vvye__vemw.body:
            if is_call_assign(kvam__ccu) and guard(find_callname, f_ir,
                kvam__ccu.value) == ('__special_combine', 'bodo.ir.aggregate'):
                args = kvam__ccu.value.args
                ofsto__kbhw = []
                yyp__cryzs = []
                for lbd__niacr in args[:-1]:
                    ind = redvars.index(lbd__niacr.name)
                    uvh__ppl.append(ind)
                    ofsto__kbhw.append('v{}'.format(ind))
                    yyp__cryzs.append('in{}'.format(ind))
                yzrn__uzen = '__special_combine__{}'.format(len(kata__pyxt))
                nnuh__vkrj += '    ({},) = {}({})\n'.format(', '.join(
                    ofsto__kbhw), yzrn__uzen, ', '.join(ofsto__kbhw +
                    yyp__cryzs))
                vls__orb = ir.Expr.call(args[-1], [], (), vvye__vemw.loc)
                riflr__uxup = guard(find_callname, f_ir, vls__orb)
                assert riflr__uxup == ('_var_combine', 'bodo.ir.aggregate')
                riflr__uxup = bodo.ir.aggregate._var_combine
                kata__pyxt[yzrn__uzen] = riflr__uxup
            if is_assign(kvam__ccu) and kvam__ccu.target.name in redvars:
                iezxt__yhkyg = kvam__ccu.target.name
                ind = redvars.index(iezxt__yhkyg)
                if ind in uvh__ppl:
                    continue
                if len(f_ir._definitions[iezxt__yhkyg]) == 2:
                    var_def = f_ir._definitions[iezxt__yhkyg][0]
                    nnuh__vkrj += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[iezxt__yhkyg][1]
                    nnuh__vkrj += _match_reduce_def(var_def, f_ir, ind)
    nnuh__vkrj += '    return {}'.format(', '.join(['v{}'.format(
        otykx__bjftt) for otykx__bjftt in range(zvz__hrpy)]))
    fvr__irwk = {}
    exec(nnuh__vkrj, {}, fvr__irwk)
    jutr__mhtz = fvr__irwk['agg_combine']
    arg_typs = tuple(2 * var_types)
    wxs__vtv = {'numba': numba, 'bodo': bodo, 'np': np}
    wxs__vtv.update(kata__pyxt)
    f_ir = compile_to_numba_ir(jutr__mhtz, wxs__vtv, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    omf__jlcev = pm.typemap[block.body[-1].value.name]
    nhggp__ovtf = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        omf__jlcev, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rhor__sliwl = numba.core.target_extension.dispatcher_registry[cpu_target](
        jutr__mhtz)
    rhor__sliwl.add_overload(nhggp__ovtf)
    return rhor__sliwl


def _match_reduce_def(var_def, f_ir, ind):
    nnuh__vkrj = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        nnuh__vkrj = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        ayapp__ptdbv = guard(find_callname, f_ir, var_def)
        if ayapp__ptdbv == ('min', 'builtins'):
            nnuh__vkrj = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if ayapp__ptdbv == ('max', 'builtins'):
            nnuh__vkrj = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return nnuh__vkrj


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    zvz__hrpy = len(redvars)
    bwyp__ujqk = 1
    pjdcn__ruz = []
    for otykx__bjftt in range(bwyp__ujqk):
        guhsj__rcc = ir.Var(arr_var.scope, f'$input{otykx__bjftt}', arr_var.loc
            )
        pjdcn__ruz.append(guhsj__rcc)
    ihfs__qaid = parfor.loop_nests[0].index_variable
    eeifm__skiod = [0] * zvz__hrpy
    for vvye__vemw in parfor.loop_body.values():
        iwxrr__urbg = []
        for kvam__ccu in vvye__vemw.body:
            if is_var_assign(kvam__ccu
                ) and kvam__ccu.value.name == ihfs__qaid.name:
                continue
            if is_getitem(kvam__ccu
                ) and kvam__ccu.value.value.name == arr_var.name:
                kvam__ccu.value = pjdcn__ruz[0]
            if is_call_assign(kvam__ccu) and guard(find_callname, pm.
                func_ir, kvam__ccu.value) == ('isna', 'bodo.libs.array_kernels'
                ) and kvam__ccu.value.args[0].name == arr_var.name:
                kvam__ccu.value = ir.Const(False, kvam__ccu.target.loc)
            if is_assign(kvam__ccu) and kvam__ccu.target.name in redvars:
                ind = redvars.index(kvam__ccu.target.name)
                eeifm__skiod[ind] = kvam__ccu.target
            iwxrr__urbg.append(kvam__ccu)
        vvye__vemw.body = iwxrr__urbg
    hlntk__vos = ['v{}'.format(otykx__bjftt) for otykx__bjftt in range(
        zvz__hrpy)]
    mzjz__rveo = ['in{}'.format(otykx__bjftt) for otykx__bjftt in range(
        bwyp__ujqk)]
    nnuh__vkrj = 'def agg_update({}):\n'.format(', '.join(hlntk__vos +
        mzjz__rveo))
    nnuh__vkrj += '    __update_redvars()\n'
    nnuh__vkrj += '    return {}'.format(', '.join(['v{}'.format(
        otykx__bjftt) for otykx__bjftt in range(zvz__hrpy)]))
    fvr__irwk = {}
    exec(nnuh__vkrj, {}, fvr__irwk)
    uwbhn__lrqo = fvr__irwk['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * bwyp__ujqk)
    f_ir = compile_to_numba_ir(uwbhn__lrqo, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    urzl__vwn = f_ir.blocks.popitem()[1].body
    omf__jlcev = pm.typemap[urzl__vwn[-1].value.name]
    fnwgd__lvmgh = wrap_parfor_blocks(parfor)
    wrv__mphne = find_topo_order(fnwgd__lvmgh)
    wrv__mphne = wrv__mphne[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    usig__anq = f_ir.blocks[wrv__mphne[0]]
    qkao__pvqpq = f_ir.blocks[wrv__mphne[-1]]
    dfo__zkx = urzl__vwn[:zvz__hrpy + bwyp__ujqk]
    if zvz__hrpy > 1:
        bxqga__ensnp = urzl__vwn[-3:]
        assert is_assign(bxqga__ensnp[0]) and isinstance(bxqga__ensnp[0].
            value, ir.Expr) and bxqga__ensnp[0].value.op == 'build_tuple'
    else:
        bxqga__ensnp = urzl__vwn[-2:]
    for otykx__bjftt in range(zvz__hrpy):
        lmthv__oql = urzl__vwn[otykx__bjftt].target
        ggmv__qfb = ir.Assign(lmthv__oql, eeifm__skiod[otykx__bjftt],
            lmthv__oql.loc)
        dfo__zkx.append(ggmv__qfb)
    for otykx__bjftt in range(zvz__hrpy, zvz__hrpy + bwyp__ujqk):
        lmthv__oql = urzl__vwn[otykx__bjftt].target
        ggmv__qfb = ir.Assign(lmthv__oql, pjdcn__ruz[otykx__bjftt -
            zvz__hrpy], lmthv__oql.loc)
        dfo__zkx.append(ggmv__qfb)
    usig__anq.body = dfo__zkx + usig__anq.body
    vmk__tuhjj = []
    for otykx__bjftt in range(zvz__hrpy):
        lmthv__oql = urzl__vwn[otykx__bjftt].target
        ggmv__qfb = ir.Assign(eeifm__skiod[otykx__bjftt], lmthv__oql,
            lmthv__oql.loc)
        vmk__tuhjj.append(ggmv__qfb)
    qkao__pvqpq.body += vmk__tuhjj + bxqga__ensnp
    nffs__jckg = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        omf__jlcev, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    rhor__sliwl = numba.core.target_extension.dispatcher_registry[cpu_target](
        uwbhn__lrqo)
    rhor__sliwl.add_overload(nffs__jckg)
    return rhor__sliwl


def _rm_arg_agg_block(block, typemap):
    afde__vkzyi = []
    arr_var = None
    for otykx__bjftt, kvam__ccu in enumerate(block.body):
        if is_assign(kvam__ccu) and isinstance(kvam__ccu.value, ir.Arg):
            arr_var = kvam__ccu.target
            qmlfp__fvm = typemap[arr_var.name]
            if not isinstance(qmlfp__fvm, types.ArrayCompatible):
                afde__vkzyi += block.body[otykx__bjftt + 1:]
                break
            dsna__exgs = block.body[otykx__bjftt + 1]
            assert is_assign(dsna__exgs) and isinstance(dsna__exgs.value,
                ir.Expr
                ) and dsna__exgs.value.op == 'getattr' and dsna__exgs.value.attr == 'shape' and dsna__exgs.value.value.name == arr_var.name
            yon__lglmy = dsna__exgs.target
            qnfl__aiw = block.body[otykx__bjftt + 2]
            assert is_assign(qnfl__aiw) and isinstance(qnfl__aiw.value, ir.Expr
                ) and qnfl__aiw.value.op == 'static_getitem' and qnfl__aiw.value.value.name == yon__lglmy.name
            afde__vkzyi += block.body[otykx__bjftt + 3:]
            break
        afde__vkzyi.append(kvam__ccu)
    return afde__vkzyi, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    fnwgd__lvmgh = wrap_parfor_blocks(parfor)
    wrv__mphne = find_topo_order(fnwgd__lvmgh)
    wrv__mphne = wrv__mphne[1:]
    unwrap_parfor_blocks(parfor)
    for tcila__thmcg in reversed(wrv__mphne):
        for kvam__ccu in reversed(parfor.loop_body[tcila__thmcg].body):
            if isinstance(kvam__ccu, ir.Assign) and (kvam__ccu.target.name in
                parfor_params or kvam__ccu.target.name in var_to_param):
                kbp__jas = kvam__ccu.target.name
                rhs = kvam__ccu.value
                okzr__avb = (kbp__jas if kbp__jas in parfor_params else
                    var_to_param[kbp__jas])
                huqj__lsc = []
                if isinstance(rhs, ir.Var):
                    huqj__lsc = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    huqj__lsc = [lbd__niacr.name for lbd__niacr in
                        kvam__ccu.value.list_vars()]
                param_uses[okzr__avb].extend(huqj__lsc)
                for lbd__niacr in huqj__lsc:
                    var_to_param[lbd__niacr] = okzr__avb
            if isinstance(kvam__ccu, Parfor):
                get_parfor_reductions(kvam__ccu, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for joiq__mrtz, huqj__lsc in param_uses.items():
        if joiq__mrtz in huqj__lsc and joiq__mrtz not in reduce_varnames:
            reduce_varnames.append(joiq__mrtz)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
