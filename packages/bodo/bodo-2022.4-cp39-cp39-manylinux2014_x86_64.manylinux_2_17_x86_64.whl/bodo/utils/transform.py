"""
Helper functions for transformations.
"""
import itertools
import math
import operator
import types as pytypes
from collections import namedtuple
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.ir_utils import GuardException, build_definitions, compile_to_numba_ir, compute_cfg_from_blocks, find_callname, find_const, get_definition, guard, is_setitem, mk_unique_var, replace_arg_nodes, require
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import fold_arguments
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoConstUpdatedError, BodoError, can_literalize_type, get_literal_value, get_overload_const_bool, get_overload_const_list, is_literal_type, is_overload_constant_bool
from bodo.utils.utils import is_array_typ, is_assign, is_call, is_expr
ReplaceFunc = namedtuple('ReplaceFunc', ['func', 'arg_types', 'args',
    'glbls', 'inline_bodo_calls', 'run_full_pipeline', 'pre_nodes'])
bodo_types_with_params = {'ArrayItemArrayType', 'CSRMatrixType',
    'CategoricalArrayType', 'CategoricalIndexType', 'DataFrameType',
    'DatetimeIndexType', 'Decimal128Type', 'DecimalArrayType',
    'IntegerArrayType', 'IntervalArrayType', 'IntervalIndexType', 'List',
    'MapArrayType', 'NumericIndexType', 'PDCategoricalDtype',
    'PeriodIndexType', 'RangeIndexType', 'SeriesType', 'StringIndexType',
    'BinaryIndexType', 'StructArrayType', 'TimedeltaIndexType',
    'TupleArrayType'}
container_update_method_names = ('clear', 'pop', 'popitem', 'update', 'add',
    'difference_update', 'discard', 'intersection_update', 'remove',
    'symmetric_difference_update', 'append', 'extend', 'insert', 'reverse',
    'sort')
no_side_effect_call_tuples = {(int,), (list,), (set,), (dict,), (min,), (
    max,), (abs,), (len,), (bool,), (str,), ('ceil', math), ('init_series',
    'pd_series_ext', 'hiframes', bodo), ('get_series_data', 'pd_series_ext',
    'hiframes', bodo), ('get_series_index', 'pd_series_ext', 'hiframes',
    bodo), ('get_series_name', 'pd_series_ext', 'hiframes', bodo), (
    'get_index_data', 'pd_index_ext', 'hiframes', bodo), ('get_index_name',
    'pd_index_ext', 'hiframes', bodo), ('init_binary_str_index',
    'pd_index_ext', 'hiframes', bodo), ('init_numeric_index',
    'pd_index_ext', 'hiframes', bodo), ('init_categorical_index',
    'pd_index_ext', 'hiframes', bodo), ('_dti_val_finalize', 'pd_index_ext',
    'hiframes', bodo), ('init_datetime_index', 'pd_index_ext', 'hiframes',
    bodo), ('init_timedelta_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_range_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_heter_index', 'pd_index_ext', 'hiframes', bodo), (
    'get_int_arr_data', 'int_arr_ext', 'libs', bodo), ('get_int_arr_bitmap',
    'int_arr_ext', 'libs', bodo), ('init_integer_array', 'int_arr_ext',
    'libs', bodo), ('alloc_int_array', 'int_arr_ext', 'libs', bodo), (
    'inplace_eq', 'str_arr_ext', 'libs', bodo), ('get_bool_arr_data',
    'bool_arr_ext', 'libs', bodo), ('get_bool_arr_bitmap', 'bool_arr_ext',
    'libs', bodo), ('init_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'alloc_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'datetime_date_arr_to_dt64_arr', 'pd_timestamp_ext', 'hiframes', bodo),
    (bodo.libs.bool_arr_ext.compute_or_body,), (bodo.libs.bool_arr_ext.
    compute_and_body,), ('alloc_datetime_date_array', 'datetime_date_ext',
    'hiframes', bodo), ('alloc_datetime_timedelta_array',
    'datetime_timedelta_ext', 'hiframes', bodo), ('cat_replace',
    'pd_categorical_ext', 'hiframes', bodo), ('init_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('alloc_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('get_categorical_arr_codes',
    'pd_categorical_ext', 'hiframes', bodo), ('_sum_handle_nan',
    'series_kernels', 'hiframes', bodo), ('_box_cat_val', 'series_kernels',
    'hiframes', bodo), ('_mean_handle_nan', 'series_kernels', 'hiframes',
    bodo), ('_var_handle_mincount', 'series_kernels', 'hiframes', bodo), (
    '_compute_var_nan_count_ddof', 'series_kernels', 'hiframes', bodo), (
    '_sem_handle_nan', 'series_kernels', 'hiframes', bodo), ('dist_return',
    'distributed_api', 'libs', bodo), ('rep_return', 'distributed_api',
    'libs', bodo), ('init_dataframe', 'pd_dataframe_ext', 'hiframes', bodo),
    ('get_dataframe_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_table', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_column_names', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_table_data', 'table', 'hiframes', bodo), ('get_dataframe_index',
    'pd_dataframe_ext', 'hiframes', bodo), ('init_rolling',
    'pd_rolling_ext', 'hiframes', bodo), ('init_groupby', 'pd_groupby_ext',
    'hiframes', bodo), ('calc_nitems', 'array_kernels', 'libs', bodo), (
    'concat', 'array_kernels', 'libs', bodo), ('unique', 'array_kernels',
    'libs', bodo), ('nunique', 'array_kernels', 'libs', bodo), ('quantile',
    'array_kernels', 'libs', bodo), ('explode', 'array_kernels', 'libs',
    bodo), ('explode_no_index', 'array_kernels', 'libs', bodo), (
    'get_arr_lens', 'array_kernels', 'libs', bodo), (
    'str_arr_from_sequence', 'str_arr_ext', 'libs', bodo), (
    'get_str_arr_str_length', 'str_arr_ext', 'libs', bodo), (
    'parse_datetime_str', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_dt64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'dt64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'timedelta64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_timedelta64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'npy_datetimestruct_to_datetime', 'pd_timestamp_ext', 'hiframes', bodo),
    ('isna', 'array_kernels', 'libs', bodo), ('copy',), (
    'from_iterable_impl', 'typing', 'utils', bodo), ('chain', itertools), (
    'groupby',), ('rolling',), (pd.CategoricalDtype,), (bodo.hiframes.
    pd_categorical_ext.get_code_for_value,), ('asarray', np), ('int32', np),
    ('int64', np), ('float64', np), ('float32', np), ('bool_', np), ('full',
    np), ('round', np), ('isnan', np), ('isnat', np), ('arange', np), (
    'internal_prange', 'parfor', numba), ('internal_prange', 'parfor',
    'parfors', numba), ('empty_inferred', 'ndarray', 'unsafe', numba), (
    '_slice_span', 'unicode', numba), ('_normalize_slice', 'unicode', numba
    ), ('init_session_builder', 'pyspark_ext', 'libs', bodo), (
    'init_session', 'pyspark_ext', 'libs', bodo), ('init_spark_df',
    'pyspark_ext', 'libs', bodo), ('h5size', 'h5_api', 'io', bodo), (
    'pre_alloc_struct_array', 'struct_arr_ext', 'libs', bodo), (bodo.libs.
    struct_arr_ext.pre_alloc_struct_array,), ('pre_alloc_tuple_array',
    'tuple_arr_ext', 'libs', bodo), (bodo.libs.tuple_arr_ext.
    pre_alloc_tuple_array,), ('pre_alloc_array_item_array',
    'array_item_arr_ext', 'libs', bodo), (bodo.libs.array_item_arr_ext.
    pre_alloc_array_item_array,), ('dist_reduce', 'distributed_api', 'libs',
    bodo), (bodo.libs.distributed_api.dist_reduce,), (
    'pre_alloc_string_array', 'str_arr_ext', 'libs', bodo), (bodo.libs.
    str_arr_ext.pre_alloc_string_array,), ('pre_alloc_binary_array',
    'binary_arr_ext', 'libs', bodo), (bodo.libs.binary_arr_ext.
    pre_alloc_binary_array,), ('pre_alloc_map_array', 'map_arr_ext', 'libs',
    bodo), (bodo.libs.map_arr_ext.pre_alloc_map_array,), (
    'convert_dict_arr_to_int', 'dict_arr_ext', 'libs', bodo), (
    'cat_dict_str', 'dict_arr_ext', 'libs', bodo), ('str_replace',
    'dict_arr_ext', 'libs', bodo), ('dict_arr_eq', 'dict_arr_ext', 'libs',
    bodo), ('dict_arr_ne', 'dict_arr_ext', 'libs', bodo), ('str_startswith',
    'dict_arr_ext', 'libs', bodo), ('str_endswith', 'dict_arr_ext', 'libs',
    bodo), ('str_contains_non_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_series_contains_regex', 'dict_arr_ext', 'libs', bodo), ('prange',
    bodo), (bodo.prange,), ('objmode', bodo), (bodo.objmode,), (
    'get_label_dict_from_categories', 'pd_categorial_ext', 'hiframes', bodo
    ), ('get_label_dict_from_categories_no_duplicates', 'pd_categorial_ext',
    'hiframes', bodo), ('build_nullable_tuple', 'nullable_tuple_ext',
    'libs', bodo), ('generate_mappable_table_func', 'table_utils', 'utils',
    bodo)}


def remove_hiframes(rhs, lives, call_list):
    mhliz__vxz = tuple(call_list)
    if mhliz__vxz in no_side_effect_call_tuples:
        return True
    if len(call_list) == 4 and call_list[1:] == ['conversion', 'utils', bodo]:
        return True
    if isinstance(call_list[-1], pytypes.ModuleType) and call_list[-1
        ].__name__ == 'bodosql':
        return True
    if len(call_list) == 2 and call_list[0] == 'copy':
        return True
    if call_list == ['h5read', 'h5_api', 'io', bodo] and rhs.args[5
        ].name not in lives:
        return True
    if call_list == ['move_str_binary_arr_payload', 'str_arr_ext', 'libs', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list == ['setna', 'array_kernels', 'libs', bodo] and rhs.args[0
        ].name not in lives:
        return True
    if call_list == ['set_table_data', 'table', 'hiframes', bodo] and rhs.args[
        0].name not in lives:
        return True
    if call_list == ['ensure_column_unboxed', 'table', 'hiframes', bodo
        ] and rhs.args[0].name not in lives and rhs.args[1].name not in lives:
        return True
    if call_list == ['generate_table_nbytes', 'table_utils', 'utils', bodo
        ] and rhs.args[1].name not in lives:
        return True
    if len(mhliz__vxz) == 1 and tuple in getattr(mhliz__vxz[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    ohpwg__xvk = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math':
        math}
    if extra_globals is not None:
        ohpwg__xvk.update(extra_globals)
    if not replace_globals:
        ohpwg__xvk = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, ohpwg__xvk, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[fdq__rnbf.name] for fdq__rnbf in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, ohpwg__xvk)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        htwzt__jzer = tuple(typing_info.typemap[fdq__rnbf.name] for
            fdq__rnbf in args)
        sbjhn__mrdnx = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, htwzt__jzer, {}, {}, flags)
        sbjhn__mrdnx.run()
    ylzvg__ivr = f_ir.blocks.popitem()[1]
    replace_arg_nodes(ylzvg__ivr, args)
    mes__qmagt = ylzvg__ivr.body[:-2]
    update_locs(mes__qmagt[len(args):], loc)
    for stmt in mes__qmagt[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        yusi__ygsvy = ylzvg__ivr.body[-2]
        assert is_assign(yusi__ygsvy) and is_expr(yusi__ygsvy.value, 'cast')
        qwzop__ocwf = yusi__ygsvy.value.value
        mes__qmagt.append(ir.Assign(qwzop__ocwf, ret_var, loc))
    return mes__qmagt


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for eukjp__tyoy in stmt.list_vars():
            eukjp__tyoy.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        laf__byg = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        pygi__zdm, rffei__rayw = laf__byg(stmt)
        return rffei__rayw
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        uuuw__nqbff = get_const_value_inner(func_ir, var, arg_types,
            typemap, file_info=file_info)
        if isinstance(uuuw__nqbff, ir.UndefinedType):
            fghes__rlcig = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{fghes__rlcig}' is not defined", loc=loc)
    except GuardException as vjbx__tehwu:
        raise BodoError(err_msg, loc=loc)
    return uuuw__nqbff


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    ktxv__jnik = get_definition(func_ir, var)
    vtcjy__mnjrk = None
    if typemap is not None:
        vtcjy__mnjrk = typemap.get(var.name, None)
    if isinstance(ktxv__jnik, ir.Arg) and arg_types is not None:
        vtcjy__mnjrk = arg_types[ktxv__jnik.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(vtcjy__mnjrk):
        return get_literal_value(vtcjy__mnjrk)
    if isinstance(ktxv__jnik, (ir.Const, ir.Global, ir.FreeVar)):
        uuuw__nqbff = ktxv__jnik.value
        return uuuw__nqbff
    if literalize_args and isinstance(ktxv__jnik, ir.Arg
        ) and can_literalize_type(vtcjy__mnjrk, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({ktxv__jnik.index}, loc=var
            .loc, file_infos={ktxv__jnik.index: file_info} if file_info is not
            None else None)
    if is_expr(ktxv__jnik, 'binop'):
        if file_info and ktxv__jnik.fn == operator.add:
            try:
                wwq__umud = get_const_value_inner(func_ir, ktxv__jnik.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(wwq__umud, True)
                cqzzg__dtknp = get_const_value_inner(func_ir, ktxv__jnik.
                    rhs, arg_types, typemap, updated_containers, file_info)
                return ktxv__jnik.fn(wwq__umud, cqzzg__dtknp)
            except (GuardException, BodoConstUpdatedError) as vjbx__tehwu:
                pass
            try:
                cqzzg__dtknp = get_const_value_inner(func_ir, ktxv__jnik.
                    rhs, arg_types, typemap, updated_containers,
                    literalize_args=False)
                file_info.set_concat(cqzzg__dtknp, False)
                wwq__umud = get_const_value_inner(func_ir, ktxv__jnik.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return ktxv__jnik.fn(wwq__umud, cqzzg__dtknp)
            except (GuardException, BodoConstUpdatedError) as vjbx__tehwu:
                pass
        wwq__umud = get_const_value_inner(func_ir, ktxv__jnik.lhs,
            arg_types, typemap, updated_containers)
        cqzzg__dtknp = get_const_value_inner(func_ir, ktxv__jnik.rhs,
            arg_types, typemap, updated_containers)
        return ktxv__jnik.fn(wwq__umud, cqzzg__dtknp)
    if is_expr(ktxv__jnik, 'unary'):
        uuuw__nqbff = get_const_value_inner(func_ir, ktxv__jnik.value,
            arg_types, typemap, updated_containers)
        return ktxv__jnik.fn(uuuw__nqbff)
    if is_expr(ktxv__jnik, 'getattr') and typemap:
        douw__pdf = typemap.get(ktxv__jnik.value.name, None)
        if isinstance(douw__pdf, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and ktxv__jnik.attr == 'columns':
            return pd.Index(douw__pdf.columns)
        if isinstance(douw__pdf, types.SliceType):
            ftykg__ivw = get_definition(func_ir, ktxv__jnik.value)
            require(is_call(ftykg__ivw))
            kbcxe__jhl = find_callname(func_ir, ftykg__ivw)
            pbqtn__lhkd = False
            if kbcxe__jhl == ('_normalize_slice', 'numba.cpython.unicode'):
                require(ktxv__jnik.attr in ('start', 'step'))
                ftykg__ivw = get_definition(func_ir, ftykg__ivw.args[0])
                pbqtn__lhkd = True
            require(find_callname(func_ir, ftykg__ivw) == ('slice', 'builtins')
                )
            if len(ftykg__ivw.args) == 1:
                if ktxv__jnik.attr == 'start':
                    return 0
                if ktxv__jnik.attr == 'step':
                    return 1
                require(ktxv__jnik.attr == 'stop')
                return get_const_value_inner(func_ir, ftykg__ivw.args[0],
                    arg_types, typemap, updated_containers)
            if ktxv__jnik.attr == 'start':
                uuuw__nqbff = get_const_value_inner(func_ir, ftykg__ivw.
                    args[0], arg_types, typemap, updated_containers)
                if uuuw__nqbff is None:
                    uuuw__nqbff = 0
                if pbqtn__lhkd:
                    require(uuuw__nqbff == 0)
                return uuuw__nqbff
            if ktxv__jnik.attr == 'stop':
                assert not pbqtn__lhkd
                return get_const_value_inner(func_ir, ftykg__ivw.args[1],
                    arg_types, typemap, updated_containers)
            require(ktxv__jnik.attr == 'step')
            if len(ftykg__ivw.args) == 2:
                return 1
            else:
                uuuw__nqbff = get_const_value_inner(func_ir, ftykg__ivw.
                    args[2], arg_types, typemap, updated_containers)
                if uuuw__nqbff is None:
                    uuuw__nqbff = 1
                if pbqtn__lhkd:
                    require(uuuw__nqbff == 1)
                return uuuw__nqbff
    if is_expr(ktxv__jnik, 'getattr'):
        return getattr(get_const_value_inner(func_ir, ktxv__jnik.value,
            arg_types, typemap, updated_containers), ktxv__jnik.attr)
    if is_expr(ktxv__jnik, 'getitem'):
        value = get_const_value_inner(func_ir, ktxv__jnik.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, ktxv__jnik.index, arg_types,
            typemap, updated_containers)
        return value[index]
    wrfog__hoa = guard(find_callname, func_ir, ktxv__jnik, typemap)
    if wrfog__hoa is not None and len(wrfog__hoa) == 2 and wrfog__hoa[0
        ] == 'keys' and isinstance(wrfog__hoa[1], ir.Var):
        xfp__djds = ktxv__jnik.func
        ktxv__jnik = get_definition(func_ir, wrfog__hoa[1])
        pytao__mbiqn = wrfog__hoa[1].name
        if updated_containers and pytao__mbiqn in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                pytao__mbiqn, updated_containers[pytao__mbiqn]))
        require(is_expr(ktxv__jnik, 'build_map'))
        vals = [eukjp__tyoy[0] for eukjp__tyoy in ktxv__jnik.items]
        uflwn__kjtz = guard(get_definition, func_ir, xfp__djds)
        assert isinstance(uflwn__kjtz, ir.Expr) and uflwn__kjtz.attr == 'keys'
        uflwn__kjtz.attr = 'copy'
        return [get_const_value_inner(func_ir, eukjp__tyoy, arg_types,
            typemap, updated_containers) for eukjp__tyoy in vals]
    if is_expr(ktxv__jnik, 'build_map'):
        return {get_const_value_inner(func_ir, eukjp__tyoy[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            eukjp__tyoy[1], arg_types, typemap, updated_containers) for
            eukjp__tyoy in ktxv__jnik.items}
    if is_expr(ktxv__jnik, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, eukjp__tyoy, arg_types,
            typemap, updated_containers) for eukjp__tyoy in ktxv__jnik.items)
    if is_expr(ktxv__jnik, 'build_list'):
        return [get_const_value_inner(func_ir, eukjp__tyoy, arg_types,
            typemap, updated_containers) for eukjp__tyoy in ktxv__jnik.items]
    if is_expr(ktxv__jnik, 'build_set'):
        return {get_const_value_inner(func_ir, eukjp__tyoy, arg_types,
            typemap, updated_containers) for eukjp__tyoy in ktxv__jnik.items}
    if wrfog__hoa == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if wrfog__hoa == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers))
    if wrfog__hoa == ('range', 'builtins') and len(ktxv__jnik.args) == 1:
        return range(get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers))
    if wrfog__hoa == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, eukjp__tyoy,
            arg_types, typemap, updated_containers) for eukjp__tyoy in
            ktxv__jnik.args))
    if wrfog__hoa == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers))
    if wrfog__hoa == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers))
    if wrfog__hoa == ('format', 'builtins'):
        fdq__rnbf = get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers)
        ppylw__audtt = get_const_value_inner(func_ir, ktxv__jnik.args[1],
            arg_types, typemap, updated_containers) if len(ktxv__jnik.args
            ) > 1 else ''
        return format(fdq__rnbf, ppylw__audtt)
    if wrfog__hoa in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers))
    if wrfog__hoa == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers))
    if wrfog__hoa == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, ktxv__jnik.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, ktxv__jnik.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            ktxv__jnik.args[2], arg_types, typemap, updated_containers))
    if wrfog__hoa == ('len', 'builtins') and typemap and isinstance(typemap
        .get(ktxv__jnik.args[0].name, None), types.BaseTuple):
        return len(typemap[ktxv__jnik.args[0].name])
    if wrfog__hoa == ('len', 'builtins'):
        mmaar__nptsm = guard(get_definition, func_ir, ktxv__jnik.args[0])
        if isinstance(mmaar__nptsm, ir.Expr) and mmaar__nptsm.op in (
            'build_tuple', 'build_list', 'build_set', 'build_map'):
            return len(mmaar__nptsm.items)
        return len(get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers))
    if wrfog__hoa == ('CategoricalDtype', 'pandas'):
        kws = dict(ktxv__jnik.kws)
        tovd__xuwch = get_call_expr_arg('CategoricalDtype', ktxv__jnik.args,
            kws, 0, 'categories', '')
        axdzc__bzfzo = get_call_expr_arg('CategoricalDtype', ktxv__jnik.
            args, kws, 1, 'ordered', False)
        if axdzc__bzfzo is not False:
            axdzc__bzfzo = get_const_value_inner(func_ir, axdzc__bzfzo,
                arg_types, typemap, updated_containers)
        if tovd__xuwch == '':
            tovd__xuwch = None
        else:
            tovd__xuwch = get_const_value_inner(func_ir, tovd__xuwch,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(tovd__xuwch, axdzc__bzfzo)
    if wrfog__hoa == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, ktxv__jnik.args[0],
            arg_types, typemap, updated_containers))
    if wrfog__hoa is not None and len(wrfog__hoa) == 2 and wrfog__hoa[1
        ] == 'pandas' and wrfog__hoa[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, wrfog__hoa[0])()
    if wrfog__hoa is not None and len(wrfog__hoa) == 2 and isinstance(
        wrfog__hoa[1], ir.Var):
        uuuw__nqbff = get_const_value_inner(func_ir, wrfog__hoa[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, eukjp__tyoy, arg_types,
            typemap, updated_containers) for eukjp__tyoy in ktxv__jnik.args]
        kws = {jzc__unqrc[0]: get_const_value_inner(func_ir, jzc__unqrc[1],
            arg_types, typemap, updated_containers) for jzc__unqrc in
            ktxv__jnik.kws}
        return getattr(uuuw__nqbff, wrfog__hoa[0])(*args, **kws)
    if wrfog__hoa is not None and len(wrfog__hoa) == 2 and wrfog__hoa[1
        ] == 'bodo' and wrfog__hoa[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, eukjp__tyoy, arg_types,
            typemap, updated_containers) for eukjp__tyoy in ktxv__jnik.args)
        kwargs = {fghes__rlcig: get_const_value_inner(func_ir, eukjp__tyoy,
            arg_types, typemap, updated_containers) for fghes__rlcig,
            eukjp__tyoy in dict(ktxv__jnik.kws).items()}
        return getattr(bodo, wrfog__hoa[0])(*args, **kwargs)
    if is_call(ktxv__jnik) and typemap and isinstance(typemap.get(
        ktxv__jnik.func.name, None), types.Dispatcher):
        py_func = typemap[ktxv__jnik.func.name].dispatcher.py_func
        require(ktxv__jnik.vararg is None)
        args = tuple(get_const_value_inner(func_ir, eukjp__tyoy, arg_types,
            typemap, updated_containers) for eukjp__tyoy in ktxv__jnik.args)
        kwargs = {fghes__rlcig: get_const_value_inner(func_ir, eukjp__tyoy,
            arg_types, typemap, updated_containers) for fghes__rlcig,
            eukjp__tyoy in dict(ktxv__jnik.kws).items()}
        arg_types = tuple(bodo.typeof(eukjp__tyoy) for eukjp__tyoy in args)
        kw_types = {gddj__zuon: bodo.typeof(eukjp__tyoy) for gddj__zuon,
            eukjp__tyoy in kwargs.items()}
        require(_func_is_pure(py_func, arg_types, kw_types))
        return py_func(*args, **kwargs)
    raise GuardException('Constant value not found')


def _func_is_pure(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.ir.csv_ext import CsvReader
    from bodo.ir.json_ext import JsonReader
    from bodo.ir.parquet_ext import ParquetReader
    from bodo.ir.sql_ext import SqlReader
    f_ir, typemap, nwmxt__knkg, nwmxt__knkg = bodo.compiler.get_func_type_info(
        py_func, arg_types, kw_types)
    for block in f_ir.blocks.values():
        for stmt in block.body:
            if isinstance(stmt, ir.Print):
                return False
            if isinstance(stmt, (CsvReader, JsonReader, ParquetReader,
                SqlReader)):
                return False
            if is_setitem(stmt) and isinstance(guard(get_definition, f_ir,
                stmt.target), ir.Arg):
                return False
            if is_assign(stmt):
                rhs = stmt.value
                if isinstance(rhs, ir.Yield):
                    return False
                if is_call(rhs):
                    xqbo__qtovw = guard(get_definition, f_ir, rhs.func)
                    if isinstance(xqbo__qtovw, ir.Const) and isinstance(
                        xqbo__qtovw.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    lpuh__molv = guard(find_callname, f_ir, rhs)
                    if lpuh__molv is None:
                        return False
                    func_name, iiqoa__nvs = lpuh__molv
                    if iiqoa__nvs == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if lpuh__molv in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if lpuh__molv == ('File', 'h5py'):
                        return False
                    if isinstance(iiqoa__nvs, ir.Var):
                        vtcjy__mnjrk = typemap[iiqoa__nvs.name]
                        if isinstance(vtcjy__mnjrk, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(vtcjy__mnjrk, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(vtcjy__mnjrk, bodo.LoggingLoggerType):
                            return False
                        if str(vtcjy__mnjrk).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            iiqoa__nvs), ir.Arg)):
                            return False
                    if iiqoa__nvs in ('numpy.random', 'time', 'logging',
                        'matplotlib.pyplot'):
                        return False
    return True


def fold_argument_types(pysig, args, kws):

    def normal_handler(index, param, value):
        return value

    def default_handler(index, param, default):
        return types.Omitted(default)

    def stararg_handler(index, param, values):
        return types.StarArgTuple(values)
    args = fold_arguments(pysig, args, kws, normal_handler, default_handler,
        stararg_handler)
    return args


def get_const_func_output_type(func, arg_types, kw_types, typing_context,
    target_context, is_udf=True):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    py_func = None
    if isinstance(func, types.MakeFunctionLiteral):
        owa__iho = func.literal_value.code
        pvpv__ruw = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            pvpv__ruw = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(pvpv__ruw, owa__iho)
        fix_struct_return(f_ir)
        typemap, demih__nnzys, gqfg__jlsc, nwmxt__knkg = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, gqfg__jlsc, demih__nnzys = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, gqfg__jlsc, demih__nnzys = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, gqfg__jlsc, demih__nnzys = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(demih__nnzys, types.DictType):
        phx__gev = guard(get_struct_keynames, f_ir, typemap)
        if phx__gev is not None:
            demih__nnzys = StructType((demih__nnzys.value_type,) * len(
                phx__gev), phx__gev)
    if is_udf and isinstance(demih__nnzys, (SeriesType,
        HeterogeneousSeriesType)):
        zynf__bpvnm = numba.core.registry.cpu_target.typing_context
        sqjbe__kno = numba.core.registry.cpu_target.target_context
        hkgak__bspu = bodo.transforms.series_pass.SeriesPass(f_ir,
            zynf__bpvnm, sqjbe__kno, typemap, gqfg__jlsc, {})
        hkgak__bspu.run()
        hkgak__bspu.run()
        hkgak__bspu.run()
        iuvn__bhh = compute_cfg_from_blocks(f_ir.blocks)
        fgkes__exofl = [guard(_get_const_series_info, f_ir.blocks[qgt__evq],
            f_ir, typemap) for qgt__evq in iuvn__bhh.exit_points() if
            isinstance(f_ir.blocks[qgt__evq].body[-1], ir.Return)]
        if None in fgkes__exofl or len(pd.Series(fgkes__exofl).unique()) != 1:
            demih__nnzys.const_info = None
        else:
            demih__nnzys.const_info = fgkes__exofl[0]
    return demih__nnzys


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    dxrjp__cvnd = block.body[-1].value
    fpjx__lxxo = get_definition(f_ir, dxrjp__cvnd)
    require(is_expr(fpjx__lxxo, 'cast'))
    fpjx__lxxo = get_definition(f_ir, fpjx__lxxo.value)
    require(is_call(fpjx__lxxo) and find_callname(f_ir, fpjx__lxxo) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    gaovj__rmbwr = fpjx__lxxo.args[1]
    ysmyx__jrt = tuple(get_const_value_inner(f_ir, gaovj__rmbwr, typemap=
        typemap))
    if isinstance(typemap[dxrjp__cvnd.name], HeterogeneousSeriesType):
        return len(typemap[dxrjp__cvnd.name].data), ysmyx__jrt
    eexef__uop = fpjx__lxxo.args[0]
    bhl__dbkh = get_definition(f_ir, eexef__uop)
    func_name, hpxr__bsyav = find_callname(f_ir, bhl__dbkh)
    if is_call(bhl__dbkh) and bodo.utils.utils.is_alloc_callname(func_name,
        hpxr__bsyav):
        lyqs__cgqz = bhl__dbkh.args[0]
        pldm__beu = get_const_value_inner(f_ir, lyqs__cgqz, typemap=typemap)
        return pldm__beu, ysmyx__jrt
    if is_call(bhl__dbkh) and find_callname(f_ir, bhl__dbkh) in [('asarray',
        'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'), (
        'build_nullable_tuple', 'bodo.libs.nullable_tuple_ext')]:
        eexef__uop = bhl__dbkh.args[0]
        bhl__dbkh = get_definition(f_ir, eexef__uop)
    require(is_expr(bhl__dbkh, 'build_tuple') or is_expr(bhl__dbkh,
        'build_list'))
    return len(bhl__dbkh.items), ysmyx__jrt


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    hfl__zidjg = []
    ceot__tmya = []
    values = []
    for gddj__zuon, eukjp__tyoy in build_map.items:
        pcsdu__jbch = find_const(f_ir, gddj__zuon)
        require(isinstance(pcsdu__jbch, str))
        ceot__tmya.append(pcsdu__jbch)
        hfl__zidjg.append(gddj__zuon)
        values.append(eukjp__tyoy)
    eodgd__zrgp = ir.Var(scope, mk_unique_var('val_tup'), loc)
    hzezl__casgi = ir.Assign(ir.Expr.build_tuple(values, loc), eodgd__zrgp, loc
        )
    f_ir._definitions[eodgd__zrgp.name] = [hzezl__casgi.value]
    wgqnj__vaot = ir.Var(scope, mk_unique_var('key_tup'), loc)
    mfo__hgdqb = ir.Assign(ir.Expr.build_tuple(hfl__zidjg, loc),
        wgqnj__vaot, loc)
    f_ir._definitions[wgqnj__vaot.name] = [mfo__hgdqb.value]
    if typemap is not None:
        typemap[eodgd__zrgp.name] = types.Tuple([typemap[eukjp__tyoy.name] for
            eukjp__tyoy in values])
        typemap[wgqnj__vaot.name] = types.Tuple([typemap[eukjp__tyoy.name] for
            eukjp__tyoy in hfl__zidjg])
    return ceot__tmya, eodgd__zrgp, hzezl__casgi, wgqnj__vaot, mfo__hgdqb


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    mbrn__adze = block.body[-1].value
    amnmj__bqmx = guard(get_definition, f_ir, mbrn__adze)
    require(is_expr(amnmj__bqmx, 'cast'))
    fpjx__lxxo = guard(get_definition, f_ir, amnmj__bqmx.value)
    require(is_expr(fpjx__lxxo, 'build_map'))
    require(len(fpjx__lxxo.items) > 0)
    loc = block.loc
    scope = block.scope
    ceot__tmya, eodgd__zrgp, hzezl__casgi, wgqnj__vaot, mfo__hgdqb = (
        extract_keyvals_from_struct_map(f_ir, fpjx__lxxo, loc, scope))
    unrq__udd = ir.Var(scope, mk_unique_var('conv_call'), loc)
    xcwvg__tmrug = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), unrq__udd, loc)
    f_ir._definitions[unrq__udd.name] = [xcwvg__tmrug.value]
    mtj__scqzb = ir.Var(scope, mk_unique_var('struct_val'), loc)
    ifmpm__psoh = ir.Assign(ir.Expr.call(unrq__udd, [eodgd__zrgp,
        wgqnj__vaot], {}, loc), mtj__scqzb, loc)
    f_ir._definitions[mtj__scqzb.name] = [ifmpm__psoh.value]
    amnmj__bqmx.value = mtj__scqzb
    fpjx__lxxo.items = [(gddj__zuon, gddj__zuon) for gddj__zuon,
        nwmxt__knkg in fpjx__lxxo.items]
    block.body = block.body[:-2] + [hzezl__casgi, mfo__hgdqb, xcwvg__tmrug,
        ifmpm__psoh] + block.body[-2:]
    return tuple(ceot__tmya)


def get_struct_keynames(f_ir, typemap):
    iuvn__bhh = compute_cfg_from_blocks(f_ir.blocks)
    xyzoy__ghagu = list(iuvn__bhh.exit_points())[0]
    block = f_ir.blocks[xyzoy__ghagu]
    require(isinstance(block.body[-1], ir.Return))
    mbrn__adze = block.body[-1].value
    amnmj__bqmx = guard(get_definition, f_ir, mbrn__adze)
    require(is_expr(amnmj__bqmx, 'cast'))
    fpjx__lxxo = guard(get_definition, f_ir, amnmj__bqmx.value)
    require(is_call(fpjx__lxxo) and find_callname(f_ir, fpjx__lxxo) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[fpjx__lxxo.args[1].name])


def fix_struct_return(f_ir):
    fld__yvba = None
    iuvn__bhh = compute_cfg_from_blocks(f_ir.blocks)
    for xyzoy__ghagu in iuvn__bhh.exit_points():
        fld__yvba = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            xyzoy__ghagu], xyzoy__ghagu)
    return fld__yvba


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    pvtct__xpza = ir.Block(ir.Scope(None, loc), loc)
    pvtct__xpza.body = node_list
    build_definitions({(0): pvtct__xpza}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(eukjp__tyoy) for eukjp__tyoy in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    lytxf__vzumo = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(lytxf__vzumo, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for eojiq__vdmi in range(len(vals) - 1, -1, -1):
        eukjp__tyoy = vals[eojiq__vdmi]
        if isinstance(eukjp__tyoy, str) and eukjp__tyoy.startswith(
            NESTED_TUP_SENTINEL):
            flp__kgc = int(eukjp__tyoy[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:eojiq__vdmi]) + (
                tuple(vals[eojiq__vdmi + 1:eojiq__vdmi + flp__kgc + 1]),) +
                tuple(vals[eojiq__vdmi + flp__kgc + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    fdq__rnbf = None
    if len(args) > arg_no and arg_no >= 0:
        fdq__rnbf = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        fdq__rnbf = kws[arg_name]
    if fdq__rnbf is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return fdq__rnbf


def set_call_expr_arg(var, args, kws, arg_no, arg_name, add_if_missing=False):
    if len(args) > arg_no:
        args[arg_no] = var
    elif add_if_missing or arg_name in kws:
        kws[arg_name] = var
    else:
        raise BodoError('cannot set call argument since does not exist')


def avoid_udf_inline(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    f_ir = numba.core.compiler.run_frontend(py_func, inline_closures=True)
    if '_bodo_inline' in kw_types and is_overload_constant_bool(kw_types[
        '_bodo_inline']):
        return not get_overload_const_bool(kw_types['_bodo_inline'])
    if any(isinstance(t, DataFrameType) for t in arg_types + tuple(kw_types
        .values())):
        return True
    for block in f_ir.blocks.values():
        if isinstance(block.body[-1], (ir.Raise, ir.StaticRaise)):
            return True
        for stmt in block.body:
            if isinstance(stmt, ir.EnterWith):
                return True
    return False


def replace_func(pass_info, func, args, const=False, pre_nodes=None,
    extra_globals=None, pysig=None, kws=None, inline_bodo_calls=False,
    run_full_pipeline=False):
    ohpwg__xvk = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        ohpwg__xvk.update(extra_globals)
    func.__globals__.update(ohpwg__xvk)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            vbjy__nyiiw = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[vbjy__nyiiw.name] = types.literal(default)
            except:
                pass_info.typemap[vbjy__nyiiw.name] = numba.typeof(default)
            cfno__xgj = ir.Assign(ir.Const(default, loc), vbjy__nyiiw, loc)
            pre_nodes.append(cfno__xgj)
            return vbjy__nyiiw
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    htwzt__jzer = tuple(pass_info.typemap[eukjp__tyoy.name] for eukjp__tyoy in
        args)
    if const:
        akdeo__tnd = []
        for eojiq__vdmi, fdq__rnbf in enumerate(args):
            uuuw__nqbff = guard(find_const, pass_info.func_ir, fdq__rnbf)
            if uuuw__nqbff:
                akdeo__tnd.append(types.literal(uuuw__nqbff))
            else:
                akdeo__tnd.append(htwzt__jzer[eojiq__vdmi])
        htwzt__jzer = tuple(akdeo__tnd)
    return ReplaceFunc(func, htwzt__jzer, args, ohpwg__xvk,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(qcny__zqw) for qcny__zqw in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        okqwp__who = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {okqwp__who} = 0\n', (okqwp__who,)
    if isinstance(t, ArrayItemArrayType):
        ilzct__eghq, wahf__ecld = gen_init_varsize_alloc_sizes(t.dtype)
        okqwp__who = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {okqwp__who} = 0\n' + ilzct__eghq, (okqwp__who,
            ) + wahf__ecld
    return '', ()


def gen_varsize_item_sizes(t, item, var_names):
    if t == string_array_type:
        return '    {} += bodo.libs.str_arr_ext.get_utf8_size({})\n'.format(
            var_names[0], item)
    if isinstance(t, ArrayItemArrayType):
        return '    {} += len({})\n'.format(var_names[0], item
            ) + gen_varsize_array_counts(t.dtype, item, var_names[1:])
    return ''


def gen_varsize_array_counts(t, item, var_names):
    if t == string_array_type:
        return ('    {} += bodo.libs.str_arr_ext.get_num_total_chars({})\n'
            .format(var_names[0], item))
    return ''


def get_type_alloc_counts(t):
    if isinstance(t, (StructArrayType, TupleArrayType)):
        return 1 + sum(get_type_alloc_counts(qcny__zqw.dtype) for qcny__zqw in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(qcny__zqw) for qcny__zqw in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(qcny__zqw) for qcny__zqw in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    xxosq__enkv = typing_context.resolve_getattr(obj_dtype, func_name)
    if xxosq__enkv is None:
        wgt__vtiw = types.misc.Module(np)
        try:
            xxosq__enkv = typing_context.resolve_getattr(wgt__vtiw, func_name)
        except AttributeError as vjbx__tehwu:
            xxosq__enkv = None
        if xxosq__enkv is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return xxosq__enkv


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    xxosq__enkv = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(xxosq__enkv, types.BoundFunction):
        if axis is not None:
            cjj__jkyaw = xxosq__enkv.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            cjj__jkyaw = xxosq__enkv.get_call_type(typing_context, (), {})
        return cjj__jkyaw.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(xxosq__enkv):
            cjj__jkyaw = xxosq__enkv.get_call_type(typing_context, (
                obj_dtype,), {})
            return cjj__jkyaw.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    xxosq__enkv = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(xxosq__enkv, types.BoundFunction):
        crny__ewdv = xxosq__enkv.template
        if axis is not None:
            return crny__ewdv._overload_func(obj_dtype, axis=axis)
        else:
            return crny__ewdv._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    ojgm__loxwa = get_definition(func_ir, dict_var)
    require(isinstance(ojgm__loxwa, ir.Expr))
    require(ojgm__loxwa.op == 'build_map')
    gpx__hmcrw = ojgm__loxwa.items
    hfl__zidjg = []
    values = []
    kfpvv__ktej = False
    for eojiq__vdmi in range(len(gpx__hmcrw)):
        dvgl__ztg, value = gpx__hmcrw[eojiq__vdmi]
        try:
            xhyic__efsx = get_const_value_inner(func_ir, dvgl__ztg,
                arg_types, typemap, updated_containers)
            hfl__zidjg.append(xhyic__efsx)
            values.append(value)
        except GuardException as vjbx__tehwu:
            require_const_map[dvgl__ztg] = label
            kfpvv__ktej = True
    if kfpvv__ktej:
        raise GuardException
    return hfl__zidjg, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        hfl__zidjg = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as vjbx__tehwu:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in hfl__zidjg):
        raise BodoError(err_msg, loc)
    return hfl__zidjg


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    hfl__zidjg = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    jui__nay = []
    rvkta__mtz = [bodo.transforms.typing_pass._create_const_var(gddj__zuon,
        'dict_key', scope, loc, jui__nay) for gddj__zuon in hfl__zidjg]
    veb__sjucc = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        ealah__hyrog = ir.Var(scope, mk_unique_var('sentinel'), loc)
        blzv__nst = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        jui__nay.append(ir.Assign(ir.Const('__bodo_tup', loc), ealah__hyrog,
            loc))
        ebzk__ojqzd = [ealah__hyrog] + rvkta__mtz + veb__sjucc
        jui__nay.append(ir.Assign(ir.Expr.build_tuple(ebzk__ojqzd, loc),
            blzv__nst, loc))
        return (blzv__nst,), jui__nay
    else:
        irmwt__cwt = ir.Var(scope, mk_unique_var('values_tup'), loc)
        rjohc__rfk = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        jui__nay.append(ir.Assign(ir.Expr.build_tuple(veb__sjucc, loc),
            irmwt__cwt, loc))
        jui__nay.append(ir.Assign(ir.Expr.build_tuple(rvkta__mtz, loc),
            rjohc__rfk, loc))
        return (irmwt__cwt, rjohc__rfk), jui__nay
