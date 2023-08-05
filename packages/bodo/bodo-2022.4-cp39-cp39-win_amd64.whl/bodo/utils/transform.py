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
    hfh__ylmlc = tuple(call_list)
    if hfh__ylmlc in no_side_effect_call_tuples:
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
    if len(hfh__ylmlc) == 1 and tuple in getattr(hfh__ylmlc[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    ysp__qls = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math': math}
    if extra_globals is not None:
        ysp__qls.update(extra_globals)
    if not replace_globals:
        ysp__qls = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, ysp__qls, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[vkkh__hglt.name] for vkkh__hglt in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, ysp__qls)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        eluw__jvytj = tuple(typing_info.typemap[vkkh__hglt.name] for
            vkkh__hglt in args)
        iajvr__zht = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, eluw__jvytj, {}, {}, flags)
        iajvr__zht.run()
    ncu__vhjx = f_ir.blocks.popitem()[1]
    replace_arg_nodes(ncu__vhjx, args)
    vyhj__fcrl = ncu__vhjx.body[:-2]
    update_locs(vyhj__fcrl[len(args):], loc)
    for stmt in vyhj__fcrl[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        lqbjm__zbsol = ncu__vhjx.body[-2]
        assert is_assign(lqbjm__zbsol) and is_expr(lqbjm__zbsol.value, 'cast')
        vroe__xaybo = lqbjm__zbsol.value.value
        vyhj__fcrl.append(ir.Assign(vroe__xaybo, ret_var, loc))
    return vyhj__fcrl


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for vvgv__fub in stmt.list_vars():
            vvgv__fub.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        cxa__gzhqi = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        eyy__gyoa, lbr__sra = cxa__gzhqi(stmt)
        return lbr__sra
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        smo__bdrx = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(smo__bdrx, ir.UndefinedType):
            vqho__njmg = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{vqho__njmg}' is not defined", loc=loc)
    except GuardException as xjo__cmosm:
        raise BodoError(err_msg, loc=loc)
    return smo__bdrx


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    leul__kas = get_definition(func_ir, var)
    bfm__jkqn = None
    if typemap is not None:
        bfm__jkqn = typemap.get(var.name, None)
    if isinstance(leul__kas, ir.Arg) and arg_types is not None:
        bfm__jkqn = arg_types[leul__kas.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(bfm__jkqn):
        return get_literal_value(bfm__jkqn)
    if isinstance(leul__kas, (ir.Const, ir.Global, ir.FreeVar)):
        smo__bdrx = leul__kas.value
        return smo__bdrx
    if literalize_args and isinstance(leul__kas, ir.Arg
        ) and can_literalize_type(bfm__jkqn, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({leul__kas.index}, loc=var.
            loc, file_infos={leul__kas.index: file_info} if file_info is not
            None else None)
    if is_expr(leul__kas, 'binop'):
        if file_info and leul__kas.fn == operator.add:
            try:
                uiw__ehna = get_const_value_inner(func_ir, leul__kas.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(uiw__ehna, True)
                dnfa__sxb = get_const_value_inner(func_ir, leul__kas.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return leul__kas.fn(uiw__ehna, dnfa__sxb)
            except (GuardException, BodoConstUpdatedError) as xjo__cmosm:
                pass
            try:
                dnfa__sxb = get_const_value_inner(func_ir, leul__kas.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(dnfa__sxb, False)
                uiw__ehna = get_const_value_inner(func_ir, leul__kas.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return leul__kas.fn(uiw__ehna, dnfa__sxb)
            except (GuardException, BodoConstUpdatedError) as xjo__cmosm:
                pass
        uiw__ehna = get_const_value_inner(func_ir, leul__kas.lhs, arg_types,
            typemap, updated_containers)
        dnfa__sxb = get_const_value_inner(func_ir, leul__kas.rhs, arg_types,
            typemap, updated_containers)
        return leul__kas.fn(uiw__ehna, dnfa__sxb)
    if is_expr(leul__kas, 'unary'):
        smo__bdrx = get_const_value_inner(func_ir, leul__kas.value,
            arg_types, typemap, updated_containers)
        return leul__kas.fn(smo__bdrx)
    if is_expr(leul__kas, 'getattr') and typemap:
        fgx__qgn = typemap.get(leul__kas.value.name, None)
        if isinstance(fgx__qgn, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and leul__kas.attr == 'columns':
            return pd.Index(fgx__qgn.columns)
        if isinstance(fgx__qgn, types.SliceType):
            pktck__zalw = get_definition(func_ir, leul__kas.value)
            require(is_call(pktck__zalw))
            klt__fkcv = find_callname(func_ir, pktck__zalw)
            qgcpv__wwxbv = False
            if klt__fkcv == ('_normalize_slice', 'numba.cpython.unicode'):
                require(leul__kas.attr in ('start', 'step'))
                pktck__zalw = get_definition(func_ir, pktck__zalw.args[0])
                qgcpv__wwxbv = True
            require(find_callname(func_ir, pktck__zalw) == ('slice',
                'builtins'))
            if len(pktck__zalw.args) == 1:
                if leul__kas.attr == 'start':
                    return 0
                if leul__kas.attr == 'step':
                    return 1
                require(leul__kas.attr == 'stop')
                return get_const_value_inner(func_ir, pktck__zalw.args[0],
                    arg_types, typemap, updated_containers)
            if leul__kas.attr == 'start':
                smo__bdrx = get_const_value_inner(func_ir, pktck__zalw.args
                    [0], arg_types, typemap, updated_containers)
                if smo__bdrx is None:
                    smo__bdrx = 0
                if qgcpv__wwxbv:
                    require(smo__bdrx == 0)
                return smo__bdrx
            if leul__kas.attr == 'stop':
                assert not qgcpv__wwxbv
                return get_const_value_inner(func_ir, pktck__zalw.args[1],
                    arg_types, typemap, updated_containers)
            require(leul__kas.attr == 'step')
            if len(pktck__zalw.args) == 2:
                return 1
            else:
                smo__bdrx = get_const_value_inner(func_ir, pktck__zalw.args
                    [2], arg_types, typemap, updated_containers)
                if smo__bdrx is None:
                    smo__bdrx = 1
                if qgcpv__wwxbv:
                    require(smo__bdrx == 1)
                return smo__bdrx
    if is_expr(leul__kas, 'getattr'):
        return getattr(get_const_value_inner(func_ir, leul__kas.value,
            arg_types, typemap, updated_containers), leul__kas.attr)
    if is_expr(leul__kas, 'getitem'):
        value = get_const_value_inner(func_ir, leul__kas.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, leul__kas.index, arg_types,
            typemap, updated_containers)
        return value[index]
    ywauf__rws = guard(find_callname, func_ir, leul__kas, typemap)
    if ywauf__rws is not None and len(ywauf__rws) == 2 and ywauf__rws[0
        ] == 'keys' and isinstance(ywauf__rws[1], ir.Var):
        zuh__eck = leul__kas.func
        leul__kas = get_definition(func_ir, ywauf__rws[1])
        jmu__swxgn = ywauf__rws[1].name
        if updated_containers and jmu__swxgn in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                jmu__swxgn, updated_containers[jmu__swxgn]))
        require(is_expr(leul__kas, 'build_map'))
        vals = [vvgv__fub[0] for vvgv__fub in leul__kas.items]
        oul__vep = guard(get_definition, func_ir, zuh__eck)
        assert isinstance(oul__vep, ir.Expr) and oul__vep.attr == 'keys'
        oul__vep.attr = 'copy'
        return [get_const_value_inner(func_ir, vvgv__fub, arg_types,
            typemap, updated_containers) for vvgv__fub in vals]
    if is_expr(leul__kas, 'build_map'):
        return {get_const_value_inner(func_ir, vvgv__fub[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            vvgv__fub[1], arg_types, typemap, updated_containers) for
            vvgv__fub in leul__kas.items}
    if is_expr(leul__kas, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, vvgv__fub, arg_types,
            typemap, updated_containers) for vvgv__fub in leul__kas.items)
    if is_expr(leul__kas, 'build_list'):
        return [get_const_value_inner(func_ir, vvgv__fub, arg_types,
            typemap, updated_containers) for vvgv__fub in leul__kas.items]
    if is_expr(leul__kas, 'build_set'):
        return {get_const_value_inner(func_ir, vvgv__fub, arg_types,
            typemap, updated_containers) for vvgv__fub in leul__kas.items}
    if ywauf__rws == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if ywauf__rws == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers))
    if ywauf__rws == ('range', 'builtins') and len(leul__kas.args) == 1:
        return range(get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers))
    if ywauf__rws == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, vvgv__fub,
            arg_types, typemap, updated_containers) for vvgv__fub in
            leul__kas.args))
    if ywauf__rws == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers))
    if ywauf__rws == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers))
    if ywauf__rws == ('format', 'builtins'):
        vkkh__hglt = get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers)
        fnqzj__bqi = get_const_value_inner(func_ir, leul__kas.args[1],
            arg_types, typemap, updated_containers) if len(leul__kas.args
            ) > 1 else ''
        return format(vkkh__hglt, fnqzj__bqi)
    if ywauf__rws in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers))
    if ywauf__rws == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers))
    if ywauf__rws == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, leul__kas.args[
            0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, leul__kas.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            leul__kas.args[2], arg_types, typemap, updated_containers))
    if ywauf__rws == ('len', 'builtins') and typemap and isinstance(typemap
        .get(leul__kas.args[0].name, None), types.BaseTuple):
        return len(typemap[leul__kas.args[0].name])
    if ywauf__rws == ('len', 'builtins'):
        uab__hraw = guard(get_definition, func_ir, leul__kas.args[0])
        if isinstance(uab__hraw, ir.Expr) and uab__hraw.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(uab__hraw.items)
        return len(get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers))
    if ywauf__rws == ('CategoricalDtype', 'pandas'):
        kws = dict(leul__kas.kws)
        jona__vfxu = get_call_expr_arg('CategoricalDtype', leul__kas.args,
            kws, 0, 'categories', '')
        qen__zekn = get_call_expr_arg('CategoricalDtype', leul__kas.args,
            kws, 1, 'ordered', False)
        if qen__zekn is not False:
            qen__zekn = get_const_value_inner(func_ir, qen__zekn, arg_types,
                typemap, updated_containers)
        if jona__vfxu == '':
            jona__vfxu = None
        else:
            jona__vfxu = get_const_value_inner(func_ir, jona__vfxu,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(jona__vfxu, qen__zekn)
    if ywauf__rws == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, leul__kas.args[0],
            arg_types, typemap, updated_containers))
    if ywauf__rws is not None and len(ywauf__rws) == 2 and ywauf__rws[1
        ] == 'pandas' and ywauf__rws[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, ywauf__rws[0])()
    if ywauf__rws is not None and len(ywauf__rws) == 2 and isinstance(
        ywauf__rws[1], ir.Var):
        smo__bdrx = get_const_value_inner(func_ir, ywauf__rws[1], arg_types,
            typemap, updated_containers)
        args = [get_const_value_inner(func_ir, vvgv__fub, arg_types,
            typemap, updated_containers) for vvgv__fub in leul__kas.args]
        kws = {kkmgx__vfldt[0]: get_const_value_inner(func_ir, kkmgx__vfldt
            [1], arg_types, typemap, updated_containers) for kkmgx__vfldt in
            leul__kas.kws}
        return getattr(smo__bdrx, ywauf__rws[0])(*args, **kws)
    if ywauf__rws is not None and len(ywauf__rws) == 2 and ywauf__rws[1
        ] == 'bodo' and ywauf__rws[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, vvgv__fub, arg_types,
            typemap, updated_containers) for vvgv__fub in leul__kas.args)
        kwargs = {vqho__njmg: get_const_value_inner(func_ir, vvgv__fub,
            arg_types, typemap, updated_containers) for vqho__njmg,
            vvgv__fub in dict(leul__kas.kws).items()}
        return getattr(bodo, ywauf__rws[0])(*args, **kwargs)
    if is_call(leul__kas) and typemap and isinstance(typemap.get(leul__kas.
        func.name, None), types.Dispatcher):
        py_func = typemap[leul__kas.func.name].dispatcher.py_func
        require(leul__kas.vararg is None)
        args = tuple(get_const_value_inner(func_ir, vvgv__fub, arg_types,
            typemap, updated_containers) for vvgv__fub in leul__kas.args)
        kwargs = {vqho__njmg: get_const_value_inner(func_ir, vvgv__fub,
            arg_types, typemap, updated_containers) for vqho__njmg,
            vvgv__fub in dict(leul__kas.kws).items()}
        arg_types = tuple(bodo.typeof(vvgv__fub) for vvgv__fub in args)
        kw_types = {smbie__njd: bodo.typeof(vvgv__fub) for smbie__njd,
            vvgv__fub in kwargs.items()}
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
    f_ir, typemap, ilgui__nja, ilgui__nja = bodo.compiler.get_func_type_info(
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
                    emqm__bdg = guard(get_definition, f_ir, rhs.func)
                    if isinstance(emqm__bdg, ir.Const) and isinstance(emqm__bdg
                        .value, numba.core.dispatcher.ObjModeLiftedWith):
                        return False
                    nvamu__ckvq = guard(find_callname, f_ir, rhs)
                    if nvamu__ckvq is None:
                        return False
                    func_name, lgzfm__xmlpl = nvamu__ckvq
                    if lgzfm__xmlpl == 'pandas' and func_name.startswith(
                        'read_'):
                        return False
                    if nvamu__ckvq in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if nvamu__ckvq == ('File', 'h5py'):
                        return False
                    if isinstance(lgzfm__xmlpl, ir.Var):
                        bfm__jkqn = typemap[lgzfm__xmlpl.name]
                        if isinstance(bfm__jkqn, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(bfm__jkqn, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(bfm__jkqn, bodo.LoggingLoggerType):
                            return False
                        if str(bfm__jkqn).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            lgzfm__xmlpl), ir.Arg)):
                            return False
                    if lgzfm__xmlpl in ('numpy.random', 'time', 'logging',
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
        dvl__bbkx = func.literal_value.code
        wdtvs__jtxf = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            wdtvs__jtxf = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(wdtvs__jtxf, dvl__bbkx)
        fix_struct_return(f_ir)
        typemap, ojpip__bwcmy, nuv__zge, ilgui__nja = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, nuv__zge, ojpip__bwcmy = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, nuv__zge, ojpip__bwcmy = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, nuv__zge, ojpip__bwcmy = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(ojpip__bwcmy, types.DictType):
        dhi__dqp = guard(get_struct_keynames, f_ir, typemap)
        if dhi__dqp is not None:
            ojpip__bwcmy = StructType((ojpip__bwcmy.value_type,) * len(
                dhi__dqp), dhi__dqp)
    if is_udf and isinstance(ojpip__bwcmy, (SeriesType,
        HeterogeneousSeriesType)):
        gmk__xseo = numba.core.registry.cpu_target.typing_context
        qmt__mrqok = numba.core.registry.cpu_target.target_context
        rjcs__fxo = bodo.transforms.series_pass.SeriesPass(f_ir, gmk__xseo,
            qmt__mrqok, typemap, nuv__zge, {})
        rjcs__fxo.run()
        rjcs__fxo.run()
        rjcs__fxo.run()
        dvq__gufr = compute_cfg_from_blocks(f_ir.blocks)
        lzvb__duwte = [guard(_get_const_series_info, f_ir.blocks[jbnzg__wec
            ], f_ir, typemap) for jbnzg__wec in dvq__gufr.exit_points() if
            isinstance(f_ir.blocks[jbnzg__wec].body[-1], ir.Return)]
        if None in lzvb__duwte or len(pd.Series(lzvb__duwte).unique()) != 1:
            ojpip__bwcmy.const_info = None
        else:
            ojpip__bwcmy.const_info = lzvb__duwte[0]
    return ojpip__bwcmy


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    ftga__acd = block.body[-1].value
    emk__dmw = get_definition(f_ir, ftga__acd)
    require(is_expr(emk__dmw, 'cast'))
    emk__dmw = get_definition(f_ir, emk__dmw.value)
    require(is_call(emk__dmw) and find_callname(f_ir, emk__dmw) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    cqsv__yjqim = emk__dmw.args[1]
    pwlbm__gdqpd = tuple(get_const_value_inner(f_ir, cqsv__yjqim, typemap=
        typemap))
    if isinstance(typemap[ftga__acd.name], HeterogeneousSeriesType):
        return len(typemap[ftga__acd.name].data), pwlbm__gdqpd
    jzlq__dzwb = emk__dmw.args[0]
    hggl__yfxs = get_definition(f_ir, jzlq__dzwb)
    func_name, szt__rgx = find_callname(f_ir, hggl__yfxs)
    if is_call(hggl__yfxs) and bodo.utils.utils.is_alloc_callname(func_name,
        szt__rgx):
        svrrn__jxd = hggl__yfxs.args[0]
        ufz__vtaw = get_const_value_inner(f_ir, svrrn__jxd, typemap=typemap)
        return ufz__vtaw, pwlbm__gdqpd
    if is_call(hggl__yfxs) and find_callname(f_ir, hggl__yfxs) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        jzlq__dzwb = hggl__yfxs.args[0]
        hggl__yfxs = get_definition(f_ir, jzlq__dzwb)
    require(is_expr(hggl__yfxs, 'build_tuple') or is_expr(hggl__yfxs,
        'build_list'))
    return len(hggl__yfxs.items), pwlbm__gdqpd


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    xqz__cjny = []
    iry__lxz = []
    values = []
    for smbie__njd, vvgv__fub in build_map.items:
        udsh__ljldo = find_const(f_ir, smbie__njd)
        require(isinstance(udsh__ljldo, str))
        iry__lxz.append(udsh__ljldo)
        xqz__cjny.append(smbie__njd)
        values.append(vvgv__fub)
    cxt__bzesn = ir.Var(scope, mk_unique_var('val_tup'), loc)
    lkw__asvg = ir.Assign(ir.Expr.build_tuple(values, loc), cxt__bzesn, loc)
    f_ir._definitions[cxt__bzesn.name] = [lkw__asvg.value]
    ayvk__fbtlz = ir.Var(scope, mk_unique_var('key_tup'), loc)
    vwwp__flef = ir.Assign(ir.Expr.build_tuple(xqz__cjny, loc), ayvk__fbtlz,
        loc)
    f_ir._definitions[ayvk__fbtlz.name] = [vwwp__flef.value]
    if typemap is not None:
        typemap[cxt__bzesn.name] = types.Tuple([typemap[vvgv__fub.name] for
            vvgv__fub in values])
        typemap[ayvk__fbtlz.name] = types.Tuple([typemap[vvgv__fub.name] for
            vvgv__fub in xqz__cjny])
    return iry__lxz, cxt__bzesn, lkw__asvg, ayvk__fbtlz, vwwp__flef


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    vcn__bhfh = block.body[-1].value
    mdh__qac = guard(get_definition, f_ir, vcn__bhfh)
    require(is_expr(mdh__qac, 'cast'))
    emk__dmw = guard(get_definition, f_ir, mdh__qac.value)
    require(is_expr(emk__dmw, 'build_map'))
    require(len(emk__dmw.items) > 0)
    loc = block.loc
    scope = block.scope
    iry__lxz, cxt__bzesn, lkw__asvg, ayvk__fbtlz, vwwp__flef = (
        extract_keyvals_from_struct_map(f_ir, emk__dmw, loc, scope))
    bauwf__acpf = ir.Var(scope, mk_unique_var('conv_call'), loc)
    swk__xob = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), bauwf__acpf, loc)
    f_ir._definitions[bauwf__acpf.name] = [swk__xob.value]
    hjfjd__euhhx = ir.Var(scope, mk_unique_var('struct_val'), loc)
    vdgut__gquwz = ir.Assign(ir.Expr.call(bauwf__acpf, [cxt__bzesn,
        ayvk__fbtlz], {}, loc), hjfjd__euhhx, loc)
    f_ir._definitions[hjfjd__euhhx.name] = [vdgut__gquwz.value]
    mdh__qac.value = hjfjd__euhhx
    emk__dmw.items = [(smbie__njd, smbie__njd) for smbie__njd, ilgui__nja in
        emk__dmw.items]
    block.body = block.body[:-2] + [lkw__asvg, vwwp__flef, swk__xob,
        vdgut__gquwz] + block.body[-2:]
    return tuple(iry__lxz)


def get_struct_keynames(f_ir, typemap):
    dvq__gufr = compute_cfg_from_blocks(f_ir.blocks)
    porqm__chroj = list(dvq__gufr.exit_points())[0]
    block = f_ir.blocks[porqm__chroj]
    require(isinstance(block.body[-1], ir.Return))
    vcn__bhfh = block.body[-1].value
    mdh__qac = guard(get_definition, f_ir, vcn__bhfh)
    require(is_expr(mdh__qac, 'cast'))
    emk__dmw = guard(get_definition, f_ir, mdh__qac.value)
    require(is_call(emk__dmw) and find_callname(f_ir, emk__dmw) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[emk__dmw.args[1].name])


def fix_struct_return(f_ir):
    gjnjh__vwwcw = None
    dvq__gufr = compute_cfg_from_blocks(f_ir.blocks)
    for porqm__chroj in dvq__gufr.exit_points():
        gjnjh__vwwcw = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            porqm__chroj], porqm__chroj)
    return gjnjh__vwwcw


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    ycdey__riqdr = ir.Block(ir.Scope(None, loc), loc)
    ycdey__riqdr.body = node_list
    build_definitions({(0): ycdey__riqdr}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(vvgv__fub) for vvgv__fub in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    rxwj__ekbl = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(rxwj__ekbl, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for rmjs__vyppx in range(len(vals) - 1, -1, -1):
        vvgv__fub = vals[rmjs__vyppx]
        if isinstance(vvgv__fub, str) and vvgv__fub.startswith(
            NESTED_TUP_SENTINEL):
            lel__hhy = int(vvgv__fub[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:rmjs__vyppx]) + (
                tuple(vals[rmjs__vyppx + 1:rmjs__vyppx + lel__hhy + 1]),) +
                tuple(vals[rmjs__vyppx + lel__hhy + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    vkkh__hglt = None
    if len(args) > arg_no and arg_no >= 0:
        vkkh__hglt = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        vkkh__hglt = kws[arg_name]
    if vkkh__hglt is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return vkkh__hglt


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
    ysp__qls = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        ysp__qls.update(extra_globals)
    func.__globals__.update(ysp__qls)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            bpkq__dmfnq = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[bpkq__dmfnq.name] = types.literal(default)
            except:
                pass_info.typemap[bpkq__dmfnq.name] = numba.typeof(default)
            ahszt__rmwc = ir.Assign(ir.Const(default, loc), bpkq__dmfnq, loc)
            pre_nodes.append(ahszt__rmwc)
            return bpkq__dmfnq
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    eluw__jvytj = tuple(pass_info.typemap[vvgv__fub.name] for vvgv__fub in args
        )
    if const:
        xtz__pdwqn = []
        for rmjs__vyppx, vkkh__hglt in enumerate(args):
            smo__bdrx = guard(find_const, pass_info.func_ir, vkkh__hglt)
            if smo__bdrx:
                xtz__pdwqn.append(types.literal(smo__bdrx))
            else:
                xtz__pdwqn.append(eluw__jvytj[rmjs__vyppx])
        eluw__jvytj = tuple(xtz__pdwqn)
    return ReplaceFunc(func, eluw__jvytj, args, ysp__qls, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(tcz__lmgz) for tcz__lmgz in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        qwz__tyuoj = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {qwz__tyuoj} = 0\n', (qwz__tyuoj,)
    if isinstance(t, ArrayItemArrayType):
        afc__rtyl, lfqcy__rhg = gen_init_varsize_alloc_sizes(t.dtype)
        qwz__tyuoj = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {qwz__tyuoj} = 0\n' + afc__rtyl, (qwz__tyuoj,) + lfqcy__rhg
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
        return 1 + sum(get_type_alloc_counts(tcz__lmgz.dtype) for tcz__lmgz in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(tcz__lmgz) for tcz__lmgz in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(tcz__lmgz) for tcz__lmgz in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    nmw__pbwr = typing_context.resolve_getattr(obj_dtype, func_name)
    if nmw__pbwr is None:
        nlycm__wdket = types.misc.Module(np)
        try:
            nmw__pbwr = typing_context.resolve_getattr(nlycm__wdket, func_name)
        except AttributeError as xjo__cmosm:
            nmw__pbwr = None
        if nmw__pbwr is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return nmw__pbwr


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    nmw__pbwr = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(nmw__pbwr, types.BoundFunction):
        if axis is not None:
            kvr__vwms = nmw__pbwr.get_call_type(typing_context, (), {'axis':
                axis})
        else:
            kvr__vwms = nmw__pbwr.get_call_type(typing_context, (), {})
        return kvr__vwms.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(nmw__pbwr):
            kvr__vwms = nmw__pbwr.get_call_type(typing_context, (obj_dtype,
                ), {})
            return kvr__vwms.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    nmw__pbwr = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(nmw__pbwr, types.BoundFunction):
        qrpp__fon = nmw__pbwr.template
        if axis is not None:
            return qrpp__fon._overload_func(obj_dtype, axis=axis)
        else:
            return qrpp__fon._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    ufw__zxbg = get_definition(func_ir, dict_var)
    require(isinstance(ufw__zxbg, ir.Expr))
    require(ufw__zxbg.op == 'build_map')
    ttc__psrn = ufw__zxbg.items
    xqz__cjny = []
    values = []
    crd__fezun = False
    for rmjs__vyppx in range(len(ttc__psrn)):
        spawy__szpkz, value = ttc__psrn[rmjs__vyppx]
        try:
            wfrhy__xjnm = get_const_value_inner(func_ir, spawy__szpkz,
                arg_types, typemap, updated_containers)
            xqz__cjny.append(wfrhy__xjnm)
            values.append(value)
        except GuardException as xjo__cmosm:
            require_const_map[spawy__szpkz] = label
            crd__fezun = True
    if crd__fezun:
        raise GuardException
    return xqz__cjny, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        xqz__cjny = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as xjo__cmosm:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in xqz__cjny):
        raise BodoError(err_msg, loc)
    return xqz__cjny


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    xqz__cjny = _get_const_keys_from_dict(args, func_ir, build_map, err_msg,
        loc)
    ckg__wva = []
    smpw__fseuz = [bodo.transforms.typing_pass._create_const_var(smbie__njd,
        'dict_key', scope, loc, ckg__wva) for smbie__njd in xqz__cjny]
    kulj__qgul = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        nobf__obz = ir.Var(scope, mk_unique_var('sentinel'), loc)
        dzof__ovu = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        ckg__wva.append(ir.Assign(ir.Const('__bodo_tup', loc), nobf__obz, loc))
        omsc__bonqs = [nobf__obz] + smpw__fseuz + kulj__qgul
        ckg__wva.append(ir.Assign(ir.Expr.build_tuple(omsc__bonqs, loc),
            dzof__ovu, loc))
        return (dzof__ovu,), ckg__wva
    else:
        ycpl__vvzo = ir.Var(scope, mk_unique_var('values_tup'), loc)
        zjo__jon = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        ckg__wva.append(ir.Assign(ir.Expr.build_tuple(kulj__qgul, loc),
            ycpl__vvzo, loc))
        ckg__wva.append(ir.Assign(ir.Expr.build_tuple(smpw__fseuz, loc),
            zjo__jon, loc))
        return (ycpl__vvzo, zjo__jon), ckg__wva
