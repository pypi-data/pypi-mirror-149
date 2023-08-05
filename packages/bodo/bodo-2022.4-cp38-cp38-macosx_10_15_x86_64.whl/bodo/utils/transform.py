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
    xrkfu__srts = tuple(call_list)
    if xrkfu__srts in no_side_effect_call_tuples:
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
    if len(xrkfu__srts) == 1 and tuple in getattr(xrkfu__srts[0], '__mro__', ()
        ):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    ycvm__ngyxd = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math':
        math}
    if extra_globals is not None:
        ycvm__ngyxd.update(extra_globals)
    if not replace_globals:
        ycvm__ngyxd = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, ycvm__ngyxd, typingctx=typing_info
            .typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[qun__ieaq.name] for qun__ieaq in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, ycvm__ngyxd)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        xdg__tbs = tuple(typing_info.typemap[qun__ieaq.name] for qun__ieaq in
            args)
        ucj__njr = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, xdg__tbs, {}, {}, flags)
        ucj__njr.run()
    iteh__zod = f_ir.blocks.popitem()[1]
    replace_arg_nodes(iteh__zod, args)
    ouk__wnlx = iteh__zod.body[:-2]
    update_locs(ouk__wnlx[len(args):], loc)
    for stmt in ouk__wnlx[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        wnowt__xor = iteh__zod.body[-2]
        assert is_assign(wnowt__xor) and is_expr(wnowt__xor.value, 'cast')
        jns__lna = wnowt__xor.value.value
        ouk__wnlx.append(ir.Assign(jns__lna, ret_var, loc))
    return ouk__wnlx


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for dxer__vufy in stmt.list_vars():
            dxer__vufy.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        brc__unjk = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        seqg__rrbw, ccln__cpq = brc__unjk(stmt)
        return ccln__cpq
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        tnpf__xvb = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(tnpf__xvb, ir.UndefinedType):
            tklnl__tlo = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{tklnl__tlo}' is not defined", loc=loc)
    except GuardException as bvtt__xdn:
        raise BodoError(err_msg, loc=loc)
    return tnpf__xvb


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    ubvq__biej = get_definition(func_ir, var)
    ejwt__gqy = None
    if typemap is not None:
        ejwt__gqy = typemap.get(var.name, None)
    if isinstance(ubvq__biej, ir.Arg) and arg_types is not None:
        ejwt__gqy = arg_types[ubvq__biej.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(ejwt__gqy):
        return get_literal_value(ejwt__gqy)
    if isinstance(ubvq__biej, (ir.Const, ir.Global, ir.FreeVar)):
        tnpf__xvb = ubvq__biej.value
        return tnpf__xvb
    if literalize_args and isinstance(ubvq__biej, ir.Arg
        ) and can_literalize_type(ejwt__gqy, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({ubvq__biej.index}, loc=var
            .loc, file_infos={ubvq__biej.index: file_info} if file_info is not
            None else None)
    if is_expr(ubvq__biej, 'binop'):
        if file_info and ubvq__biej.fn == operator.add:
            try:
                bco__xraq = get_const_value_inner(func_ir, ubvq__biej.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(bco__xraq, True)
                xso__lwxkz = get_const_value_inner(func_ir, ubvq__biej.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return ubvq__biej.fn(bco__xraq, xso__lwxkz)
            except (GuardException, BodoConstUpdatedError) as bvtt__xdn:
                pass
            try:
                xso__lwxkz = get_const_value_inner(func_ir, ubvq__biej.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(xso__lwxkz, False)
                bco__xraq = get_const_value_inner(func_ir, ubvq__biej.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return ubvq__biej.fn(bco__xraq, xso__lwxkz)
            except (GuardException, BodoConstUpdatedError) as bvtt__xdn:
                pass
        bco__xraq = get_const_value_inner(func_ir, ubvq__biej.lhs,
            arg_types, typemap, updated_containers)
        xso__lwxkz = get_const_value_inner(func_ir, ubvq__biej.rhs,
            arg_types, typemap, updated_containers)
        return ubvq__biej.fn(bco__xraq, xso__lwxkz)
    if is_expr(ubvq__biej, 'unary'):
        tnpf__xvb = get_const_value_inner(func_ir, ubvq__biej.value,
            arg_types, typemap, updated_containers)
        return ubvq__biej.fn(tnpf__xvb)
    if is_expr(ubvq__biej, 'getattr') and typemap:
        eylob__icz = typemap.get(ubvq__biej.value.name, None)
        if isinstance(eylob__icz, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and ubvq__biej.attr == 'columns':
            return pd.Index(eylob__icz.columns)
        if isinstance(eylob__icz, types.SliceType):
            ttvv__ikt = get_definition(func_ir, ubvq__biej.value)
            require(is_call(ttvv__ikt))
            kkkz__yzkif = find_callname(func_ir, ttvv__ikt)
            cbfh__qkz = False
            if kkkz__yzkif == ('_normalize_slice', 'numba.cpython.unicode'):
                require(ubvq__biej.attr in ('start', 'step'))
                ttvv__ikt = get_definition(func_ir, ttvv__ikt.args[0])
                cbfh__qkz = True
            require(find_callname(func_ir, ttvv__ikt) == ('slice', 'builtins'))
            if len(ttvv__ikt.args) == 1:
                if ubvq__biej.attr == 'start':
                    return 0
                if ubvq__biej.attr == 'step':
                    return 1
                require(ubvq__biej.attr == 'stop')
                return get_const_value_inner(func_ir, ttvv__ikt.args[0],
                    arg_types, typemap, updated_containers)
            if ubvq__biej.attr == 'start':
                tnpf__xvb = get_const_value_inner(func_ir, ttvv__ikt.args[0
                    ], arg_types, typemap, updated_containers)
                if tnpf__xvb is None:
                    tnpf__xvb = 0
                if cbfh__qkz:
                    require(tnpf__xvb == 0)
                return tnpf__xvb
            if ubvq__biej.attr == 'stop':
                assert not cbfh__qkz
                return get_const_value_inner(func_ir, ttvv__ikt.args[1],
                    arg_types, typemap, updated_containers)
            require(ubvq__biej.attr == 'step')
            if len(ttvv__ikt.args) == 2:
                return 1
            else:
                tnpf__xvb = get_const_value_inner(func_ir, ttvv__ikt.args[2
                    ], arg_types, typemap, updated_containers)
                if tnpf__xvb is None:
                    tnpf__xvb = 1
                if cbfh__qkz:
                    require(tnpf__xvb == 1)
                return tnpf__xvb
    if is_expr(ubvq__biej, 'getattr'):
        return getattr(get_const_value_inner(func_ir, ubvq__biej.value,
            arg_types, typemap, updated_containers), ubvq__biej.attr)
    if is_expr(ubvq__biej, 'getitem'):
        value = get_const_value_inner(func_ir, ubvq__biej.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, ubvq__biej.index, arg_types,
            typemap, updated_containers)
        return value[index]
    nixk__evgeb = guard(find_callname, func_ir, ubvq__biej, typemap)
    if nixk__evgeb is not None and len(nixk__evgeb) == 2 and nixk__evgeb[0
        ] == 'keys' and isinstance(nixk__evgeb[1], ir.Var):
        ujun__wpmfe = ubvq__biej.func
        ubvq__biej = get_definition(func_ir, nixk__evgeb[1])
        cwrto__doznp = nixk__evgeb[1].name
        if updated_containers and cwrto__doznp in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                cwrto__doznp, updated_containers[cwrto__doznp]))
        require(is_expr(ubvq__biej, 'build_map'))
        vals = [dxer__vufy[0] for dxer__vufy in ubvq__biej.items]
        kjut__srxx = guard(get_definition, func_ir, ujun__wpmfe)
        assert isinstance(kjut__srxx, ir.Expr) and kjut__srxx.attr == 'keys'
        kjut__srxx.attr = 'copy'
        return [get_const_value_inner(func_ir, dxer__vufy, arg_types,
            typemap, updated_containers) for dxer__vufy in vals]
    if is_expr(ubvq__biej, 'build_map'):
        return {get_const_value_inner(func_ir, dxer__vufy[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            dxer__vufy[1], arg_types, typemap, updated_containers) for
            dxer__vufy in ubvq__biej.items}
    if is_expr(ubvq__biej, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, dxer__vufy, arg_types,
            typemap, updated_containers) for dxer__vufy in ubvq__biej.items)
    if is_expr(ubvq__biej, 'build_list'):
        return [get_const_value_inner(func_ir, dxer__vufy, arg_types,
            typemap, updated_containers) for dxer__vufy in ubvq__biej.items]
    if is_expr(ubvq__biej, 'build_set'):
        return {get_const_value_inner(func_ir, dxer__vufy, arg_types,
            typemap, updated_containers) for dxer__vufy in ubvq__biej.items}
    if nixk__evgeb == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if nixk__evgeb == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers))
    if nixk__evgeb == ('range', 'builtins') and len(ubvq__biej.args) == 1:
        return range(get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers))
    if nixk__evgeb == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, dxer__vufy,
            arg_types, typemap, updated_containers) for dxer__vufy in
            ubvq__biej.args))
    if nixk__evgeb == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers))
    if nixk__evgeb == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers))
    if nixk__evgeb == ('format', 'builtins'):
        qun__ieaq = get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers)
        fvufp__affqk = get_const_value_inner(func_ir, ubvq__biej.args[1],
            arg_types, typemap, updated_containers) if len(ubvq__biej.args
            ) > 1 else ''
        return format(qun__ieaq, fvufp__affqk)
    if nixk__evgeb in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers))
    if nixk__evgeb == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers))
    if nixk__evgeb == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, ubvq__biej.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, ubvq__biej.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            ubvq__biej.args[2], arg_types, typemap, updated_containers))
    if nixk__evgeb == ('len', 'builtins') and typemap and isinstance(typemap
        .get(ubvq__biej.args[0].name, None), types.BaseTuple):
        return len(typemap[ubvq__biej.args[0].name])
    if nixk__evgeb == ('len', 'builtins'):
        bbhpu__lnhsw = guard(get_definition, func_ir, ubvq__biej.args[0])
        if isinstance(bbhpu__lnhsw, ir.Expr) and bbhpu__lnhsw.op in (
            'build_tuple', 'build_list', 'build_set', 'build_map'):
            return len(bbhpu__lnhsw.items)
        return len(get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers))
    if nixk__evgeb == ('CategoricalDtype', 'pandas'):
        kws = dict(ubvq__biej.kws)
        gox__cnaku = get_call_expr_arg('CategoricalDtype', ubvq__biej.args,
            kws, 0, 'categories', '')
        sscbb__aqtnz = get_call_expr_arg('CategoricalDtype', ubvq__biej.
            args, kws, 1, 'ordered', False)
        if sscbb__aqtnz is not False:
            sscbb__aqtnz = get_const_value_inner(func_ir, sscbb__aqtnz,
                arg_types, typemap, updated_containers)
        if gox__cnaku == '':
            gox__cnaku = None
        else:
            gox__cnaku = get_const_value_inner(func_ir, gox__cnaku,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(gox__cnaku, sscbb__aqtnz)
    if nixk__evgeb == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, ubvq__biej.args[0],
            arg_types, typemap, updated_containers))
    if nixk__evgeb is not None and len(nixk__evgeb) == 2 and nixk__evgeb[1
        ] == 'pandas' and nixk__evgeb[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, nixk__evgeb[0])()
    if nixk__evgeb is not None and len(nixk__evgeb) == 2 and isinstance(
        nixk__evgeb[1], ir.Var):
        tnpf__xvb = get_const_value_inner(func_ir, nixk__evgeb[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, dxer__vufy, arg_types,
            typemap, updated_containers) for dxer__vufy in ubvq__biej.args]
        kws = {rxdwf__eve[0]: get_const_value_inner(func_ir, rxdwf__eve[1],
            arg_types, typemap, updated_containers) for rxdwf__eve in
            ubvq__biej.kws}
        return getattr(tnpf__xvb, nixk__evgeb[0])(*args, **kws)
    if nixk__evgeb is not None and len(nixk__evgeb) == 2 and nixk__evgeb[1
        ] == 'bodo' and nixk__evgeb[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, dxer__vufy, arg_types,
            typemap, updated_containers) for dxer__vufy in ubvq__biej.args)
        kwargs = {tklnl__tlo: get_const_value_inner(func_ir, dxer__vufy,
            arg_types, typemap, updated_containers) for tklnl__tlo,
            dxer__vufy in dict(ubvq__biej.kws).items()}
        return getattr(bodo, nixk__evgeb[0])(*args, **kwargs)
    if is_call(ubvq__biej) and typemap and isinstance(typemap.get(
        ubvq__biej.func.name, None), types.Dispatcher):
        py_func = typemap[ubvq__biej.func.name].dispatcher.py_func
        require(ubvq__biej.vararg is None)
        args = tuple(get_const_value_inner(func_ir, dxer__vufy, arg_types,
            typemap, updated_containers) for dxer__vufy in ubvq__biej.args)
        kwargs = {tklnl__tlo: get_const_value_inner(func_ir, dxer__vufy,
            arg_types, typemap, updated_containers) for tklnl__tlo,
            dxer__vufy in dict(ubvq__biej.kws).items()}
        arg_types = tuple(bodo.typeof(dxer__vufy) for dxer__vufy in args)
        kw_types = {ekx__ubkok: bodo.typeof(dxer__vufy) for ekx__ubkok,
            dxer__vufy in kwargs.items()}
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
    f_ir, typemap, cya__ewes, cya__ewes = bodo.compiler.get_func_type_info(
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
                    rcq__yjcp = guard(get_definition, f_ir, rhs.func)
                    if isinstance(rcq__yjcp, ir.Const) and isinstance(rcq__yjcp
                        .value, numba.core.dispatcher.ObjModeLiftedWith):
                        return False
                    egace__gqf = guard(find_callname, f_ir, rhs)
                    if egace__gqf is None:
                        return False
                    func_name, zrt__btk = egace__gqf
                    if zrt__btk == 'pandas' and func_name.startswith('read_'):
                        return False
                    if egace__gqf in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if egace__gqf == ('File', 'h5py'):
                        return False
                    if isinstance(zrt__btk, ir.Var):
                        ejwt__gqy = typemap[zrt__btk.name]
                        if isinstance(ejwt__gqy, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(ejwt__gqy, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(ejwt__gqy, bodo.LoggingLoggerType):
                            return False
                        if str(ejwt__gqy).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir, zrt__btk
                            ), ir.Arg)):
                            return False
                    if zrt__btk in ('numpy.random', 'time', 'logging',
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
        scmg__rxodi = func.literal_value.code
        dsbc__abmof = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            dsbc__abmof = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(dsbc__abmof, scmg__rxodi)
        fix_struct_return(f_ir)
        typemap, kpwj__zyc, nbki__suvw, cya__ewes = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, nbki__suvw, kpwj__zyc = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, nbki__suvw, kpwj__zyc = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, nbki__suvw, kpwj__zyc = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(kpwj__zyc, types.DictType):
        skezf__auz = guard(get_struct_keynames, f_ir, typemap)
        if skezf__auz is not None:
            kpwj__zyc = StructType((kpwj__zyc.value_type,) * len(skezf__auz
                ), skezf__auz)
    if is_udf and isinstance(kpwj__zyc, (SeriesType, HeterogeneousSeriesType)):
        baoua__vmxyr = numba.core.registry.cpu_target.typing_context
        gkgaa__tui = numba.core.registry.cpu_target.target_context
        gsc__hyzm = bodo.transforms.series_pass.SeriesPass(f_ir,
            baoua__vmxyr, gkgaa__tui, typemap, nbki__suvw, {})
        gsc__hyzm.run()
        gsc__hyzm.run()
        gsc__hyzm.run()
        yafj__rbza = compute_cfg_from_blocks(f_ir.blocks)
        wqi__idjs = [guard(_get_const_series_info, f_ir.blocks[bjr__wjmr],
            f_ir, typemap) for bjr__wjmr in yafj__rbza.exit_points() if
            isinstance(f_ir.blocks[bjr__wjmr].body[-1], ir.Return)]
        if None in wqi__idjs or len(pd.Series(wqi__idjs).unique()) != 1:
            kpwj__zyc.const_info = None
        else:
            kpwj__zyc.const_info = wqi__idjs[0]
    return kpwj__zyc


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    engsx__pjiky = block.body[-1].value
    aoj__tsqtv = get_definition(f_ir, engsx__pjiky)
    require(is_expr(aoj__tsqtv, 'cast'))
    aoj__tsqtv = get_definition(f_ir, aoj__tsqtv.value)
    require(is_call(aoj__tsqtv) and find_callname(f_ir, aoj__tsqtv) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    oueiq__dmk = aoj__tsqtv.args[1]
    ezuw__zenb = tuple(get_const_value_inner(f_ir, oueiq__dmk, typemap=typemap)
        )
    if isinstance(typemap[engsx__pjiky.name], HeterogeneousSeriesType):
        return len(typemap[engsx__pjiky.name].data), ezuw__zenb
    rdi__ybg = aoj__tsqtv.args[0]
    kgxc__benoc = get_definition(f_ir, rdi__ybg)
    func_name, uwg__lmyfg = find_callname(f_ir, kgxc__benoc)
    if is_call(kgxc__benoc) and bodo.utils.utils.is_alloc_callname(func_name,
        uwg__lmyfg):
        swf__hytvj = kgxc__benoc.args[0]
        cfrdq__asfc = get_const_value_inner(f_ir, swf__hytvj, typemap=typemap)
        return cfrdq__asfc, ezuw__zenb
    if is_call(kgxc__benoc) and find_callname(f_ir, kgxc__benoc) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        rdi__ybg = kgxc__benoc.args[0]
        kgxc__benoc = get_definition(f_ir, rdi__ybg)
    require(is_expr(kgxc__benoc, 'build_tuple') or is_expr(kgxc__benoc,
        'build_list'))
    return len(kgxc__benoc.items), ezuw__zenb


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    coaf__nnmvh = []
    sgrcv__gcoi = []
    values = []
    for ekx__ubkok, dxer__vufy in build_map.items:
        bwd__uda = find_const(f_ir, ekx__ubkok)
        require(isinstance(bwd__uda, str))
        sgrcv__gcoi.append(bwd__uda)
        coaf__nnmvh.append(ekx__ubkok)
        values.append(dxer__vufy)
    oie__xlopa = ir.Var(scope, mk_unique_var('val_tup'), loc)
    lbjd__raup = ir.Assign(ir.Expr.build_tuple(values, loc), oie__xlopa, loc)
    f_ir._definitions[oie__xlopa.name] = [lbjd__raup.value]
    yvfu__ijkv = ir.Var(scope, mk_unique_var('key_tup'), loc)
    kjaqf__rkqxw = ir.Assign(ir.Expr.build_tuple(coaf__nnmvh, loc),
        yvfu__ijkv, loc)
    f_ir._definitions[yvfu__ijkv.name] = [kjaqf__rkqxw.value]
    if typemap is not None:
        typemap[oie__xlopa.name] = types.Tuple([typemap[dxer__vufy.name] for
            dxer__vufy in values])
        typemap[yvfu__ijkv.name] = types.Tuple([typemap[dxer__vufy.name] for
            dxer__vufy in coaf__nnmvh])
    return sgrcv__gcoi, oie__xlopa, lbjd__raup, yvfu__ijkv, kjaqf__rkqxw


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    qccnz__tsuzu = block.body[-1].value
    ogizb__jfvf = guard(get_definition, f_ir, qccnz__tsuzu)
    require(is_expr(ogizb__jfvf, 'cast'))
    aoj__tsqtv = guard(get_definition, f_ir, ogizb__jfvf.value)
    require(is_expr(aoj__tsqtv, 'build_map'))
    require(len(aoj__tsqtv.items) > 0)
    loc = block.loc
    scope = block.scope
    sgrcv__gcoi, oie__xlopa, lbjd__raup, yvfu__ijkv, kjaqf__rkqxw = (
        extract_keyvals_from_struct_map(f_ir, aoj__tsqtv, loc, scope))
    wed__khf = ir.Var(scope, mk_unique_var('conv_call'), loc)
    xmd__xdz = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), wed__khf, loc)
    f_ir._definitions[wed__khf.name] = [xmd__xdz.value]
    yln__ggipy = ir.Var(scope, mk_unique_var('struct_val'), loc)
    hkqy__tud = ir.Assign(ir.Expr.call(wed__khf, [oie__xlopa, yvfu__ijkv],
        {}, loc), yln__ggipy, loc)
    f_ir._definitions[yln__ggipy.name] = [hkqy__tud.value]
    ogizb__jfvf.value = yln__ggipy
    aoj__tsqtv.items = [(ekx__ubkok, ekx__ubkok) for ekx__ubkok, cya__ewes in
        aoj__tsqtv.items]
    block.body = block.body[:-2] + [lbjd__raup, kjaqf__rkqxw, xmd__xdz,
        hkqy__tud] + block.body[-2:]
    return tuple(sgrcv__gcoi)


def get_struct_keynames(f_ir, typemap):
    yafj__rbza = compute_cfg_from_blocks(f_ir.blocks)
    ogx__ueth = list(yafj__rbza.exit_points())[0]
    block = f_ir.blocks[ogx__ueth]
    require(isinstance(block.body[-1], ir.Return))
    qccnz__tsuzu = block.body[-1].value
    ogizb__jfvf = guard(get_definition, f_ir, qccnz__tsuzu)
    require(is_expr(ogizb__jfvf, 'cast'))
    aoj__tsqtv = guard(get_definition, f_ir, ogizb__jfvf.value)
    require(is_call(aoj__tsqtv) and find_callname(f_ir, aoj__tsqtv) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[aoj__tsqtv.args[1].name])


def fix_struct_return(f_ir):
    zdmjf__scml = None
    yafj__rbza = compute_cfg_from_blocks(f_ir.blocks)
    for ogx__ueth in yafj__rbza.exit_points():
        zdmjf__scml = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            ogx__ueth], ogx__ueth)
    return zdmjf__scml


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    okzv__yyv = ir.Block(ir.Scope(None, loc), loc)
    okzv__yyv.body = node_list
    build_definitions({(0): okzv__yyv}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(dxer__vufy) for dxer__vufy in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    ayb__pool = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(ayb__pool, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for shf__qlj in range(len(vals) - 1, -1, -1):
        dxer__vufy = vals[shf__qlj]
        if isinstance(dxer__vufy, str) and dxer__vufy.startswith(
            NESTED_TUP_SENTINEL):
            ynf__evw = int(dxer__vufy[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:shf__qlj]) + (
                tuple(vals[shf__qlj + 1:shf__qlj + ynf__evw + 1]),) + tuple
                (vals[shf__qlj + ynf__evw + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    qun__ieaq = None
    if len(args) > arg_no and arg_no >= 0:
        qun__ieaq = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        qun__ieaq = kws[arg_name]
    if qun__ieaq is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return qun__ieaq


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
    ycvm__ngyxd = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        ycvm__ngyxd.update(extra_globals)
    func.__globals__.update(ycvm__ngyxd)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            csvn__ftwk = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[csvn__ftwk.name] = types.literal(default)
            except:
                pass_info.typemap[csvn__ftwk.name] = numba.typeof(default)
            sezud__qfk = ir.Assign(ir.Const(default, loc), csvn__ftwk, loc)
            pre_nodes.append(sezud__qfk)
            return csvn__ftwk
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    xdg__tbs = tuple(pass_info.typemap[dxer__vufy.name] for dxer__vufy in args)
    if const:
        lsv__dsw = []
        for shf__qlj, qun__ieaq in enumerate(args):
            tnpf__xvb = guard(find_const, pass_info.func_ir, qun__ieaq)
            if tnpf__xvb:
                lsv__dsw.append(types.literal(tnpf__xvb))
            else:
                lsv__dsw.append(xdg__tbs[shf__qlj])
        xdg__tbs = tuple(lsv__dsw)
    return ReplaceFunc(func, xdg__tbs, args, ycvm__ngyxd, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(uwe__mcip) for uwe__mcip in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        zeipy__vneqb = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {zeipy__vneqb} = 0\n', (zeipy__vneqb,)
    if isinstance(t, ArrayItemArrayType):
        zqd__caxk, mrb__vii = gen_init_varsize_alloc_sizes(t.dtype)
        zeipy__vneqb = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {zeipy__vneqb} = 0\n' + zqd__caxk, (zeipy__vneqb,
            ) + mrb__vii
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
        return 1 + sum(get_type_alloc_counts(uwe__mcip.dtype) for uwe__mcip in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(uwe__mcip) for uwe__mcip in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(uwe__mcip) for uwe__mcip in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    gkrmt__auhi = typing_context.resolve_getattr(obj_dtype, func_name)
    if gkrmt__auhi is None:
        sjo__fxnl = types.misc.Module(np)
        try:
            gkrmt__auhi = typing_context.resolve_getattr(sjo__fxnl, func_name)
        except AttributeError as bvtt__xdn:
            gkrmt__auhi = None
        if gkrmt__auhi is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return gkrmt__auhi


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    gkrmt__auhi = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(gkrmt__auhi, types.BoundFunction):
        if axis is not None:
            ylg__ppjlc = gkrmt__auhi.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            ylg__ppjlc = gkrmt__auhi.get_call_type(typing_context, (), {})
        return ylg__ppjlc.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(gkrmt__auhi):
            ylg__ppjlc = gkrmt__auhi.get_call_type(typing_context, (
                obj_dtype,), {})
            return ylg__ppjlc.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    gkrmt__auhi = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(gkrmt__auhi, types.BoundFunction):
        ucd__trofx = gkrmt__auhi.template
        if axis is not None:
            return ucd__trofx._overload_func(obj_dtype, axis=axis)
        else:
            return ucd__trofx._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    gof__ggk = get_definition(func_ir, dict_var)
    require(isinstance(gof__ggk, ir.Expr))
    require(gof__ggk.op == 'build_map')
    sspnp__hvx = gof__ggk.items
    coaf__nnmvh = []
    values = []
    jzqiy__mgjil = False
    for shf__qlj in range(len(sspnp__hvx)):
        coryq__ipu, value = sspnp__hvx[shf__qlj]
        try:
            zxi__eybvs = get_const_value_inner(func_ir, coryq__ipu,
                arg_types, typemap, updated_containers)
            coaf__nnmvh.append(zxi__eybvs)
            values.append(value)
        except GuardException as bvtt__xdn:
            require_const_map[coryq__ipu] = label
            jzqiy__mgjil = True
    if jzqiy__mgjil:
        raise GuardException
    return coaf__nnmvh, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        coaf__nnmvh = tuple(get_const_value_inner(func_ir, t[0], args) for
            t in build_map.items)
    except GuardException as bvtt__xdn:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in coaf__nnmvh):
        raise BodoError(err_msg, loc)
    return coaf__nnmvh


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    coaf__nnmvh = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    nup__dclzq = []
    rnou__awkkc = [bodo.transforms.typing_pass._create_const_var(ekx__ubkok,
        'dict_key', scope, loc, nup__dclzq) for ekx__ubkok in coaf__nnmvh]
    lhtzp__rvm = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        rfys__sbh = ir.Var(scope, mk_unique_var('sentinel'), loc)
        ttla__gpdvq = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        nup__dclzq.append(ir.Assign(ir.Const('__bodo_tup', loc), rfys__sbh,
            loc))
        keyn__npjk = [rfys__sbh] + rnou__awkkc + lhtzp__rvm
        nup__dclzq.append(ir.Assign(ir.Expr.build_tuple(keyn__npjk, loc),
            ttla__gpdvq, loc))
        return (ttla__gpdvq,), nup__dclzq
    else:
        wan__nmc = ir.Var(scope, mk_unique_var('values_tup'), loc)
        ymf__ften = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        nup__dclzq.append(ir.Assign(ir.Expr.build_tuple(lhtzp__rvm, loc),
            wan__nmc, loc))
        nup__dclzq.append(ir.Assign(ir.Expr.build_tuple(rnou__awkkc, loc),
            ymf__ften, loc))
        return (wan__nmc, ymf__ften), nup__dclzq
