"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
from typing import Tuple
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_getattr, models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import _no_input, datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import DatetimeIndexType, RangeIndexType, StringIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array, boolean_dtype
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_index_data_arr_types, get_index_names, get_literal_value, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, parse_dtype, raise_bodo_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names: Tuple):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        evti__mpgr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({evti__mpgr})\n'
            )
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    vnm__tref = 'def impl(df):\n'
    if df.has_runtime_cols:
        vnm__tref += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        heo__fscq = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        vnm__tref += f'  return {heo__fscq}'
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo}, smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    check_runtime_cols_unsupported(df, 'DataFrame.values')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.values')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.values: only supported for dataframes containing numeric values'
            )
    mwiri__mtof = len(df.columns)
    ubiil__ojsep = set(i for i in range(mwiri__mtof) if isinstance(df.data[
        i], IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in ubiil__ojsep else '') for i in
        range(mwiri__mtof))
    vnm__tref = 'def f(df):\n'.format()
    vnm__tref += '    return np.stack(({},), 1)\n'.format(data_args)
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo, 'np': np}, smeb__ayk)
    wtct__pamrp = smeb__ayk['f']
    return wtct__pamrp


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False, na_value=_no_input
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.to_numpy()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.to_numpy()')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.to_numpy(): only supported for dataframes containing numeric values'
            )
    mevk__wfors = {'dtype': dtype, 'na_value': na_value}
    xntb__gcvqi = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', mevk__wfors, xntb__gcvqi,
        package_name='pandas', module_name='DataFrame')

    def impl(df, dtype=None, copy=False, na_value=_no_input):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            gupmn__lnrt = bodo.hiframes.table.compute_num_runtime_columns(t)
            return gupmn__lnrt * len(t)
        return impl
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@lower_getattr(DataFrameType, 'shape')
def lower_dataframe_shape(context, builder, typ, val):
    impl = overload_dataframe_shape(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def overload_dataframe_shape(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            gupmn__lnrt = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), gupmn__lnrt
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    vnm__tref = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    dfsri__qeqq = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    vnm__tref += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{dfsri__qeqq}), {index}, None)
"""
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo}, smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    check_runtime_cols_unsupported(df, 'DataFrame.empty')
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    check_runtime_cols_unsupported(df, 'DataFrame.assign()')
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    check_runtime_cols_unsupported(df, 'DataFrame.insert()')
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if isinstance(dtype, types.PyObject) or dtype in (object, 'object'):
        return "'object'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True, _bodo_object_typeref=None):
    check_runtime_cols_unsupported(df, 'DataFrame.astype()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.astype()')
    mevk__wfors = {'copy': copy, 'errors': errors}
    xntb__gcvqi = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', mevk__wfors, xntb__gcvqi,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        xnly__mhr = _bodo_object_typeref.instance_type
        assert isinstance(xnly__mhr, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        fussz__uzg = {}
        for i, name in enumerate(xnly__mhr.columns):
            arr_typ = xnly__mhr.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                qadp__grysq = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                qadp__grysq = boolean_dtype
            else:
                qadp__grysq = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = qadp__grysq
            fussz__uzg[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {fussz__uzg[xihz__ins]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if xihz__ins in fussz__uzg else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, xihz__ins in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        jfk__wpdwg = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(jfk__wpdwg[xihz__ins])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if xihz__ins in jfk__wpdwg else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, xihz__ins in enumerate(df.columns))
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    header = """def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True, _bodo_object_typeref=None):
"""
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    check_runtime_cols_unsupported(df, 'DataFrame.copy()')
    dpypk__fgmoj = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(deep):
            dpypk__fgmoj.append(arr + '.copy()')
        elif is_overload_false(deep):
            dpypk__fgmoj.append(arr)
        else:
            dpypk__fgmoj.append(f'{arr}.copy() if deep else {arr}')
    header = 'def impl(df, deep=True):\n'
    return _gen_init_df(header, df.columns, ', '.join(dpypk__fgmoj))


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    mevk__wfors = {'index': index, 'level': level, 'errors': errors}
    xntb__gcvqi = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', mevk__wfors, xntb__gcvqi,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        aqvg__gjo = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        aqvg__gjo = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    rehs__ffk = [aqvg__gjo.get(df.columns[i], df.columns[i]) for i in range
        (len(df.columns))]
    dpypk__fgmoj = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(copy):
            dpypk__fgmoj.append(arr + '.copy()')
        elif is_overload_false(copy):
            dpypk__fgmoj.append(arr)
        else:
            dpypk__fgmoj.append(f'{arr}.copy() if copy else {arr}')
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    return _gen_init_df(header, rehs__ffk, ', '.join(dpypk__fgmoj))


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    yss__eabn = not is_overload_none(items)
    tgbb__vclmu = not is_overload_none(like)
    fksum__oeyf = not is_overload_none(regex)
    kpen__idyx = yss__eabn ^ tgbb__vclmu ^ fksum__oeyf
    kbjjx__yfxh = not (yss__eabn or tgbb__vclmu or fksum__oeyf)
    if kbjjx__yfxh:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not kpen__idyx:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        if axis not in {'index', 'columns'}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either "index" or "columns" if string'
                )
        yyx__bsgo = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        yyx__bsgo = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert yyx__bsgo in {0, 1}
    vnm__tref = 'def impl(df, items=None, like=None, regex=None, axis=None):\n'
    if yyx__bsgo == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if yyx__bsgo == 1:
        arty__txqxg = []
        dxdt__ruc = []
        fhzm__fgnkz = []
        if yss__eabn:
            if is_overload_constant_list(items):
                rja__cmqq = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if tgbb__vclmu:
            if is_overload_constant_str(like):
                zbdrh__ojbd = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if fksum__oeyf:
            if is_overload_constant_str(regex):
                gkn__jnac = get_overload_const_str(regex)
                pnnp__wadh = re.compile(gkn__jnac)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, xihz__ins in enumerate(df.columns):
            if not is_overload_none(items
                ) and xihz__ins in rja__cmqq or not is_overload_none(like
                ) and zbdrh__ojbd in str(xihz__ins) or not is_overload_none(
                regex) and pnnp__wadh.search(str(xihz__ins)):
                dxdt__ruc.append(xihz__ins)
                fhzm__fgnkz.append(i)
        for i in fhzm__fgnkz:
            var_name = f'data_{i}'
            arty__txqxg.append(var_name)
            vnm__tref += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(arty__txqxg)
        return _gen_init_df(vnm__tref, dxdt__ruc, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        ddc__uzla = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([ddc__uzla] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': ddc__uzla}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    check_runtime_cols_unsupported(df, 'DataFrame.select_dtypes')
    ppu__bxwfc = is_overload_none(include)
    pmr__nfpda = is_overload_none(exclude)
    fefpx__cwh = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if ppu__bxwfc and pmr__nfpda:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not ppu__bxwfc:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            czfo__twcgq = [dtype_to_array_type(parse_dtype(elem, fefpx__cwh
                )) for elem in include]
        elif is_legal_input(include):
            czfo__twcgq = [dtype_to_array_type(parse_dtype(include,
                fefpx__cwh))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        czfo__twcgq = get_nullable_and_non_nullable_types(czfo__twcgq)
        sdjtg__pjts = tuple(xihz__ins for i, xihz__ins in enumerate(df.
            columns) if df.data[i] in czfo__twcgq)
    else:
        sdjtg__pjts = df.columns
    if not pmr__nfpda:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            xrvz__fqx = [dtype_to_array_type(parse_dtype(elem, fefpx__cwh)) for
                elem in exclude]
        elif is_legal_input(exclude):
            xrvz__fqx = [dtype_to_array_type(parse_dtype(exclude, fefpx__cwh))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        xrvz__fqx = get_nullable_and_non_nullable_types(xrvz__fqx)
        sdjtg__pjts = tuple(xihz__ins for xihz__ins in sdjtg__pjts if df.
            data[df.columns.index(xihz__ins)] not in xrvz__fqx)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(xihz__ins)})'
         for xihz__ins in sdjtg__pjts)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, sdjtg__pjts, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        ddc__uzla = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([ddc__uzla] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': ddc__uzla}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'~bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


def overload_dataframe_head(df, n=5):
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    check_runtime_cols_unsupported(df, 'DataFrame.tail()')
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'first', inline='always', no_unliteral=True)
def overload_dataframe_first(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.first()')
    kpg__adlh = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in kpg__adlh:
        raise BodoError(
            "DataFrame.first(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.first()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:valid_entries]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:valid_entries]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    start_date = df_index[0]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, start_date, False)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'last', inline='always', no_unliteral=True)
def overload_dataframe_last(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.last()')
    kpg__adlh = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in kpg__adlh:
        raise BodoError(
            "DataFrame.last(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.last()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[len(df)-valid_entries:]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[len(df)-valid_entries:]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    final_date = df_index[-1]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, final_date, True)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_string()')

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    check_runtime_cols_unsupported(df, 'DataFrame.isin()')
    from bodo.utils.typing import is_iterable_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.isin()')
    vnm__tref = 'def impl(df, values):\n'
    vixu__aay = {}
    sir__cxtyr = False
    if isinstance(values, DataFrameType):
        sir__cxtyr = True
        for i, xihz__ins in enumerate(df.columns):
            if xihz__ins in values.columns:
                txm__usr = 'val{}'.format(i)
                vnm__tref += (
                    """  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {})
"""
                    .format(txm__usr, values.columns.index(xihz__ins)))
                vixu__aay[xihz__ins] = txm__usr
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        vixu__aay = {xihz__ins: 'values' for xihz__ins in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        txm__usr = 'data{}'.format(i)
        vnm__tref += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(txm__usr, i))
        data.append(txm__usr)
    cymg__grx = ['out{}'.format(i) for i in range(len(df.columns))]
    pis__hjpal = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    axpdw__esgef = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    hwd__ecifl = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, kkk__ldsy) in enumerate(zip(df.columns, data)):
        if cname in vixu__aay:
            yxg__kep = vixu__aay[cname]
            if sir__cxtyr:
                vnm__tref += pis__hjpal.format(kkk__ldsy, yxg__kep,
                    cymg__grx[i])
            else:
                vnm__tref += axpdw__esgef.format(kkk__ldsy, yxg__kep,
                    cymg__grx[i])
        else:
            vnm__tref += hwd__ecifl.format(cymg__grx[i])
    return _gen_init_df(vnm__tref, df.columns, ','.join(cymg__grx))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    mwiri__mtof = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(mwiri__mtof))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    qmtei__dcrdt = [xihz__ins for xihz__ins, wsnt__cxgd in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(wsnt__cxgd.
        dtype)]
    assert len(qmtei__dcrdt) != 0
    bqcvf__ikn = ''
    if not any(wsnt__cxgd == types.float64 for wsnt__cxgd in df.data):
        bqcvf__ikn = '.astype(np.float64)'
    evnyw__fzxjq = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(xihz__ins), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(xihz__ins)], IntegerArrayType) or
        df.data[df.columns.index(xihz__ins)] == boolean_array else '') for
        xihz__ins in qmtei__dcrdt)
    bswl__ogg = 'np.stack(({},), 1){}'.format(evnyw__fzxjq, bqcvf__ikn)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        qmtei__dcrdt)))
    index = f'{generate_col_to_index_func_text(qmtei__dcrdt)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(bswl__ogg)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, qmtei__dcrdt, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    zexc__qca = dict(ddof=ddof)
    cvbs__imxb = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    nqt__argdf = '1' if is_overload_none(min_periods) else 'min_periods'
    qmtei__dcrdt = [xihz__ins for xihz__ins, wsnt__cxgd in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(wsnt__cxgd.
        dtype)]
    if len(qmtei__dcrdt) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    bqcvf__ikn = ''
    if not any(wsnt__cxgd == types.float64 for wsnt__cxgd in df.data):
        bqcvf__ikn = '.astype(np.float64)'
    evnyw__fzxjq = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(xihz__ins), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(xihz__ins)], IntegerArrayType) or
        df.data[df.columns.index(xihz__ins)] == boolean_array else '') for
        xihz__ins in qmtei__dcrdt)
    bswl__ogg = 'np.stack(({},), 1){}'.format(evnyw__fzxjq, bqcvf__ikn)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        qmtei__dcrdt)))
    index = f'pd.Index({qmtei__dcrdt})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(bswl__ogg)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        nqt__argdf)
    return _gen_init_df(header, qmtei__dcrdt, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    zexc__qca = dict(axis=axis, level=level, numeric_only=numeric_only)
    cvbs__imxb = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    vnm__tref = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    vnm__tref += '  data = np.array([{}])\n'.format(data_args)
    heo__fscq = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    vnm__tref += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {heo__fscq})\n'
        )
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo, 'np': np}, smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    zexc__qca = dict(axis=axis)
    cvbs__imxb = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    vnm__tref = 'def impl(df, axis=0, dropna=True):\n'
    vnm__tref += '  data = np.asarray(({},))\n'.format(data_args)
    heo__fscq = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    vnm__tref += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {heo__fscq})\n'
        )
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo, 'np': np}, smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    zexc__qca = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    cvbs__imxb = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    zexc__qca = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    cvbs__imxb = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    zexc__qca = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cvbs__imxb = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    zexc__qca = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cvbs__imxb = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    zexc__qca = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cvbs__imxb = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    zexc__qca = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    cvbs__imxb = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    zexc__qca = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    cvbs__imxb = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    zexc__qca = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    cvbs__imxb = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    zexc__qca = dict(numeric_only=numeric_only, interpolation=interpolation)
    cvbs__imxb = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    zexc__qca = dict(axis=axis, skipna=skipna)
    cvbs__imxb = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for igrp__adx in df.data:
        if not (bodo.utils.utils.is_np_array_typ(igrp__adx) and (igrp__adx.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            igrp__adx.dtype, (types.Number, types.Boolean))) or isinstance(
            igrp__adx, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or
            igrp__adx in [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {igrp__adx} not supported.'
                )
        if isinstance(igrp__adx, bodo.CategoricalArrayType
            ) and not igrp__adx.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    zexc__qca = dict(axis=axis, skipna=skipna)
    cvbs__imxb = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for igrp__adx in df.data:
        if not (bodo.utils.utils.is_np_array_typ(igrp__adx) and (igrp__adx.
            dtype in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            igrp__adx.dtype, (types.Number, types.Boolean))) or isinstance(
            igrp__adx, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or
            igrp__adx in [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {igrp__adx} not supported.'
                )
        if isinstance(igrp__adx, bodo.CategoricalArrayType
            ) and not igrp__adx.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


@overload_method(DataFrameType, 'infer_objects', inline='always')
def overload_dataframe_infer_objects(df):
    check_runtime_cols_unsupported(df, 'DataFrame.infer_objects()')
    return lambda df: df.copy()


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
    else:
        raise_bodo_error(
            f'DataFrame.{func_name}: axis must be a constant Integer')
    assert axis in (0, 1), f'invalid axis argument for DataFrame.{func_name}'
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        qmtei__dcrdt = tuple(xihz__ins for xihz__ins, wsnt__cxgd in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (wsnt__cxgd.dtype))
        out_colnames = qmtei__dcrdt
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            tqg__ovpn = [numba.np.numpy_support.as_dtype(df.data[df.columns
                .index(xihz__ins)].dtype) for xihz__ins in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(tqg__ovpn, []))
    except NotImplementedError as bir__hwr:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    vzf__vyjk = ''
    if func_name in ('sum', 'prod'):
        vzf__vyjk = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    vnm__tref = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, vzf__vyjk))
    if func_name == 'quantile':
        vnm__tref = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        vnm__tref = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        vnm__tref += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        vnm__tref += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    nry__gzy = ''
    if func_name in ('min', 'max'):
        nry__gzy = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        nry__gzy = ', dtype=np.float32'
    khsy__qupg = f'bodo.libs.array_ops.array_op_{func_name}'
    osech__dkpv = ''
    if func_name in ['sum', 'prod']:
        osech__dkpv = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        osech__dkpv = 'index'
    elif func_name == 'quantile':
        osech__dkpv = 'q'
    elif func_name in ['std', 'var']:
        osech__dkpv = 'True, ddof'
    elif func_name == 'median':
        osech__dkpv = 'True'
    data_args = ', '.join(
        f'{khsy__qupg}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(xihz__ins)}), {osech__dkpv})'
         for xihz__ins in out_colnames)
    vnm__tref = ''
    if func_name in ('idxmax', 'idxmin'):
        vnm__tref += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        vnm__tref += ('  data = bodo.utils.conversion.coerce_to_array(({},))\n'
            .format(data_args))
    else:
        vnm__tref += '  data = np.asarray(({},){})\n'.format(data_args,
            nry__gzy)
    vnm__tref += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return vnm__tref


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    hkt__trro = [df_type.columns.index(xihz__ins) for xihz__ins in out_colnames
        ]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in hkt__trro)
    frl__ycbxc = '\n        '.join(f'row[{i}] = arr_{hkt__trro[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    flwmj__saz = f'len(arr_{hkt__trro[0]})'
    zvc__sui = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum': 'np.nansum',
        'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in zvc__sui:
        pxb__staz = zvc__sui[func_name]
        mnkn__grpay = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        vnm__tref = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {flwmj__saz}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{mnkn__grpay})
    for i in numba.parfors.parfor.internal_prange(n):
        {frl__ycbxc}
        A[i] = {pxb__staz}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return vnm__tref
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    zexc__qca = dict(fill_method=fill_method, limit=limit, freq=freq)
    cvbs__imxb = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.pct_change()')
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumprod()')
    zexc__qca = dict(axis=axis, skipna=skipna)
    cvbs__imxb = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumprod()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumsum()')
    zexc__qca = dict(skipna=skipna)
    cvbs__imxb = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumsum()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, IntegerArrayType) or isinstance(data, types.Array
        ) and isinstance(data.dtype, types.Number
        ) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    check_runtime_cols_unsupported(df, 'DataFrame.describe()')
    zexc__qca = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    cvbs__imxb = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    qmtei__dcrdt = [xihz__ins for xihz__ins, wsnt__cxgd in zip(df.columns,
        df.data) if _is_describe_type(wsnt__cxgd)]
    if len(qmtei__dcrdt) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    rjckj__wwhks = sum(df.data[df.columns.index(xihz__ins)].dtype == bodo.
        datetime64ns for xihz__ins in qmtei__dcrdt)

    def _get_describe(col_ind):
        cdl__ushm = df.data[col_ind].dtype == bodo.datetime64ns
        if rjckj__wwhks and rjckj__wwhks != len(qmtei__dcrdt):
            if cdl__ushm:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for xihz__ins in qmtei__dcrdt:
        col_ind = df.columns.index(xihz__ins)
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.columns.index(xihz__ins)) for
        xihz__ins in qmtei__dcrdt)
    dlh__kiaqo = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if rjckj__wwhks == len(qmtei__dcrdt):
        dlh__kiaqo = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif rjckj__wwhks:
        dlh__kiaqo = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({dlh__kiaqo})'
    return _gen_init_df(header, qmtei__dcrdt, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    zexc__qca = dict(axis=axis, convert=convert, is_copy=is_copy)
    cvbs__imxb = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.shift()')
    zexc__qca = dict(freq=freq, axis=axis, fill_value=fill_value)
    cvbs__imxb = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for eact__ffwr in df.data:
        if not is_supported_shift_array_type(eact__ffwr):
            raise BodoError(
                f'Dataframe.shift() column input type {eact__ffwr.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    check_runtime_cols_unsupported(df, 'DataFrame.diff()')
    zexc__qca = dict(axis=axis)
    cvbs__imxb = dict(axis=0)
    check_unsupported_args('DataFrame.diff', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for eact__ffwr in df.data:
        if not (isinstance(eact__ffwr, types.Array) and (isinstance(
            eact__ffwr.dtype, types.Number) or eact__ffwr.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {eact__ffwr.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'explode', inline='always', no_unliteral=True)
def overload_dataframe_explode(df, column, ignore_index=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.explode()')
    zmqdr__kxreg = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(zmqdr__kxreg)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        lkptn__vfblk = get_overload_const_list(column)
    else:
        lkptn__vfblk = [get_literal_value(column)]
    kple__tpx = {xihz__ins: i for i, xihz__ins in enumerate(df.columns)}
    ztfeo__nlq = [kple__tpx[xihz__ins] for xihz__ins in lkptn__vfblk]
    for i in ztfeo__nlq:
        if not isinstance(df.data[i], ArrayItemArrayType) and df.data[i
            ].dtype != string_array_split_view_type:
            raise BodoError(
                f'DataFrame.explode(): columns must have array-like entries')
    n = len(df.columns)
    header = 'def impl(df, column, ignore_index=False):\n'
    header += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    header += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    for i in range(n):
        header += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    header += (
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{ztfeo__nlq[0]})\n'
        )
    for i in range(n):
        if i in ztfeo__nlq:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.explode_no_index(data{i}, counts)\n'
                )
        else:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.repeat_kernel(data{i}, counts)\n'
                )
    header += (
        '  new_index = bodo.libs.array_kernels.repeat_kernel(index_arr, counts)\n'
        )
    data_args = ', '.join(f'out_data{i}' for i in range(n))
    index = 'bodo.utils.conversion.convert_to_index(new_index)'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    check_runtime_cols_unsupported(df, 'DataFrame.set_index()')
    mevk__wfors = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    xntb__gcvqi = {'inplace': False, 'append': False, 'verify_integrity': False
        }
    check_unsupported_args('DataFrame.set_index', mevk__wfors, xntb__gcvqi,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    columns = tuple(xihz__ins for xihz__ins in df.columns if xihz__ins !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    mevk__wfors = {'inplace': inplace}
    xntb__gcvqi = {'inplace': False}
    check_unsupported_args('query', mevk__wfors, xntb__gcvqi, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        kdg__iuz = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[kdg__iuz]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    mevk__wfors = {'subset': subset, 'keep': keep}
    xntb__gcvqi = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', mevk__wfors, xntb__gcvqi,
        package_name='pandas', module_name='DataFrame')
    mwiri__mtof = len(df.columns)
    vnm__tref = "def impl(df, subset=None, keep='first'):\n"
    for i in range(mwiri__mtof):
        vnm__tref += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    twui__qqg = ', '.join(f'data_{i}' for i in range(mwiri__mtof))
    twui__qqg += ',' if mwiri__mtof == 1 else ''
    vnm__tref += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({twui__qqg}))\n')
    vnm__tref += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    vnm__tref += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo}, smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    mevk__wfors = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    xntb__gcvqi = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    vuy__xpv = []
    if is_overload_constant_list(subset):
        vuy__xpv = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        vuy__xpv = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        vuy__xpv = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    rpmj__wupp = []
    for col_name in vuy__xpv:
        if col_name not in df.columns:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        rpmj__wupp.append(df.columns.index(col_name))
    check_unsupported_args('DataFrame.drop_duplicates', mevk__wfors,
        xntb__gcvqi, package_name='pandas', module_name='DataFrame')
    tbo__jhj = []
    if rpmj__wupp:
        for zcg__hybax in rpmj__wupp:
            if isinstance(df.data[zcg__hybax], bodo.MapArrayType):
                tbo__jhj.append(df.columns[zcg__hybax])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                tbo__jhj.append(col_name)
    if tbo__jhj:
        raise BodoError(f'DataFrame.drop_duplicates(): Columns {tbo__jhj} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    mwiri__mtof = len(df.columns)
    fssy__xqax = ['data_{}'.format(i) for i in rpmj__wupp]
    xfhi__otni = ['data_{}'.format(i) for i in range(mwiri__mtof) if i not in
        rpmj__wupp]
    if fssy__xqax:
        urqv__xgrmg = len(fssy__xqax)
    else:
        urqv__xgrmg = mwiri__mtof
    qtjzm__jnnda = ', '.join(fssy__xqax + xfhi__otni)
    data_args = ', '.join('data_{}'.format(i) for i in range(mwiri__mtof))
    vnm__tref = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(mwiri__mtof):
        vnm__tref += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    vnm__tref += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(qtjzm__jnnda, index, urqv__xgrmg))
    vnm__tref += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(vnm__tref, df.columns, data_args, 'index')


def create_dataframe_mask_where_overload(func_name):

    def overload_dataframe_mask_where(df, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
            f'DataFrame.{func_name}()')
        _validate_arguments_mask_where(f'DataFrame.{func_name}', df, cond,
            other, inplace, axis, level, errors, try_cast)
        header = """def impl(df, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False):
"""
        if func_name == 'mask':
            header += '  cond = ~cond\n'
        gen_all_false = [False]
        if cond.ndim == 1:
            cond_str = lambda i, _: 'cond'
        elif cond.ndim == 2:
            if isinstance(cond, DataFrameType):
                qcjev__zjze = {xihz__ins: i for i, xihz__ins in enumerate(
                    cond.columns)}

                def cond_str(i, gen_all_false):
                    if df.columns[i] in qcjev__zjze:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {qcjev__zjze[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            itda__ucpg = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                other_map = {xihz__ins: i for i, xihz__ins in enumerate(
                    other.columns)}
                itda__ucpg = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other_map[df.columns[i]]})'
                     if df.columns[i] in other_map else 'None')
            elif isinstance(other, types.Array):
                itda__ucpg = lambda i: f'other[:,{i}]'
        mwiri__mtof = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {itda__ucpg(i)})'
             for i in range(mwiri__mtof))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        goewf__mrden = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(
            goewf__mrden)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    zexc__qca = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    cvbs__imxb = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        (cond.ndim == 1 or cond.ndim == 2) and cond.dtype == types.bool_
        ) and not (isinstance(cond, DataFrameType) and cond.ndim == 2 and
        all(cond.data[i].dtype == types.bool_ for i in range(len(df.columns)))
        ):
        raise BodoError(
            f"{func_name}(): 'cond' argument must be a DataFrame, Series, 1- or 2-dimensional array of booleans"
            )
    mwiri__mtof = len(df.columns)
    if hasattr(other, 'ndim') and (other.ndim != 1 or other.ndim != 2):
        if other.ndim == 2:
            if not isinstance(other, (DataFrameType, types.Array)):
                raise BodoError(
                    f"{func_name}(): 'other', if 2-dimensional, must be a DataFrame or array."
                    )
        elif other.ndim != 1:
            raise BodoError(
                f"{func_name}(): 'other' must be either 1 or 2-dimensional")
    if isinstance(other, DataFrameType):
        other_map = {xihz__ins: i for i, xihz__ins in enumerate(other.columns)}
        for i in range(mwiri__mtof):
            if df.columns[i] in other_map:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other_map[df.columns[i]]]
                    )
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(mwiri__mtof):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(mwiri__mtof):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other, max_ndim=2)


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None,
    out_df_type=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    if out_df_type is not None:
        extra_globals['out_df_type'] = out_df_type
        lwot__qdwy = 'out_df_type'
    else:
        lwot__qdwy = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    vnm__tref = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {lwot__qdwy})
"""
    smeb__ayk = {}
    pzl__ugyjl = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    pzl__ugyjl.update(extra_globals)
    exec(vnm__tref, pzl__ugyjl, smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        mxb__cdz = pd.Index(lhs.columns)
        tbu__kjlkl = pd.Index(rhs.columns)
        lho__luj, vzzm__mbnm, byk__oliv = mxb__cdz.join(tbu__kjlkl, how=
            'left' if is_inplace else 'outer', level=None, return_indexers=True
            )
        return tuple(lho__luj), vzzm__mbnm, byk__oliv
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        ivt__sljky = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        cba__tpkh = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, ivt__sljky)
        check_runtime_cols_unsupported(rhs, ivt__sljky)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                lho__luj, vzzm__mbnm, byk__oliv = _get_binop_columns(lhs, rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {sgmf__duj}) {ivt__sljky}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {wojw__dplhg})'
                     if sgmf__duj != -1 and wojw__dplhg != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for sgmf__duj, wojw__dplhg in zip(vzzm__mbnm, byk__oliv))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, lho__luj, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            tvaxs__wqe = []
            flvoj__mcdfb = []
            if op in cba__tpkh:
                for i, qgi__hywra in enumerate(lhs.data):
                    if is_common_scalar_dtype([qgi__hywra.dtype, rhs]):
                        tvaxs__wqe.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {ivt__sljky} rhs'
                            )
                    else:
                        bgp__jad = f'arr{i}'
                        flvoj__mcdfb.append(bgp__jad)
                        tvaxs__wqe.append(bgp__jad)
                data_args = ', '.join(tvaxs__wqe)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {ivt__sljky} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(flvoj__mcdfb) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {bgp__jad} = np.empty(n, dtype=np.bool_)\n' for
                    bgp__jad in flvoj__mcdfb)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(bgp__jad, op ==
                    operator.ne) for bgp__jad in flvoj__mcdfb)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            tvaxs__wqe = []
            flvoj__mcdfb = []
            if op in cba__tpkh:
                for i, qgi__hywra in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, qgi__hywra.dtype]):
                        tvaxs__wqe.append(
                            f'lhs {ivt__sljky} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        bgp__jad = f'arr{i}'
                        flvoj__mcdfb.append(bgp__jad)
                        tvaxs__wqe.append(bgp__jad)
                data_args = ', '.join(tvaxs__wqe)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, ivt__sljky) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(flvoj__mcdfb) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(bgp__jad) for bgp__jad in flvoj__mcdfb)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(bgp__jad, op ==
                    operator.ne) for bgp__jad in flvoj__mcdfb)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        goewf__mrden = create_binary_op_overload(op)
        overload(op)(goewf__mrden)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        ivt__sljky = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, ivt__sljky)
        check_runtime_cols_unsupported(right, ivt__sljky)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                lho__luj, _, byk__oliv = _get_binop_columns(left, right, True)
                vnm__tref = 'def impl(left, right):\n'
                for i, wojw__dplhg in enumerate(byk__oliv):
                    if wojw__dplhg == -1:
                        vnm__tref += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    vnm__tref += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    vnm__tref += f"""  df_arr{i} {ivt__sljky} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {wojw__dplhg})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    lho__luj)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(vnm__tref, lho__luj, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            vnm__tref = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                vnm__tref += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                vnm__tref += '  df_arr{0} {1} right\n'.format(i, ivt__sljky)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(vnm__tref, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        goewf__mrden = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(goewf__mrden)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            ivt__sljky = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, ivt__sljky)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, ivt__sljky) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        goewf__mrden = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(goewf__mrden)


_install_unary_ops()


def overload_isna(obj):
    check_runtime_cols_unsupported(obj, 'pd.isna()')
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            eklg__uvtf = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                eklg__uvtf[i] = bodo.libs.array_kernels.isna(obj, i)
            return eklg__uvtf
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            eklg__uvtf = np.empty(n, np.bool_)
            for i in range(n):
                eklg__uvtf[i] = pd.isna(obj[i])
            return eklg__uvtf
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if isinstance(obj, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    check_runtime_cols_unsupported(obj, 'pd.notna()')
    if isinstance(obj, (DataFrameType, SeriesType)):
        return lambda obj: obj.notna()
    if isinstance(obj, (types.List, types.UniTuple)) or is_array_typ(obj,
        include_index_series=True):
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    check_runtime_cols_unsupported(df, 'DataFrame.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.replace()')
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    mevk__wfors = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    xntb__gcvqi = {'inplace': False, 'limit': None, 'regex': False,
        'method': 'pad'}
    check_unsupported_args('replace', mevk__wfors, xntb__gcvqi,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    cbz__ums = str(expr_node)
    return cbz__ums.startswith('left.') or cbz__ums.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    uoxn__hoyq = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (uoxn__hoyq,))
    dodm__xifrq = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        vwzbs__zzd = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        mnrg__cny = {('NOT_NA', dodm__xifrq(qgi__hywra)): qgi__hywra for
            qgi__hywra in null_set}
        aaonz__qfp, _, _ = _parse_query_expr(vwzbs__zzd, env, [], [], None,
            join_cleaned_cols=mnrg__cny)
        ltwm__uix = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            xzkp__deso = pd.core.computation.ops.BinOp('&', aaonz__qfp,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = ltwm__uix
        return xzkp__deso

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                npis__xcq = set()
                ypcs__dhm = set()
                usfb__huc = _insert_NA_cond_body(expr_node.lhs, npis__xcq)
                kfka__fbmwx = _insert_NA_cond_body(expr_node.rhs, ypcs__dhm)
                rdj__ukbn = npis__xcq.intersection(ypcs__dhm)
                npis__xcq.difference_update(rdj__ukbn)
                ypcs__dhm.difference_update(rdj__ukbn)
                null_set.update(rdj__ukbn)
                expr_node.lhs = append_null_checks(usfb__huc, npis__xcq)
                expr_node.rhs = append_null_checks(kfka__fbmwx, ypcs__dhm)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            bga__bxxsx = expr_node.name
            tho__uvda, col_name = bga__bxxsx.split('.')
            if tho__uvda == 'left':
                xbtn__kbsd = left_columns
                data = left_data
            else:
                xbtn__kbsd = right_columns
                data = right_data
            vim__khm = data[xbtn__kbsd.index(col_name)]
            if bodo.utils.typing.is_nullable(vim__khm):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    fud__lyoro = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        wuv__fodo = str(expr_node.lhs)
        skuf__ipy = str(expr_node.rhs)
        if wuv__fodo.startswith('left.') and skuf__ipy.startswith('left.'
            ) or wuv__fodo.startswith('right.') and skuf__ipy.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [wuv__fodo.split('.')[1]]
        right_on = [skuf__ipy.split('.')[1]]
        if wuv__fodo.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        tez__uzzdk, mjw__vfako, jngsl__gljn = _extract_equal_conds(expr_node
            .lhs)
        ddbd__xeu, gwp__bked, rytox__nod = _extract_equal_conds(expr_node.rhs)
        left_on = tez__uzzdk + ddbd__xeu
        right_on = mjw__vfako + gwp__bked
        if jngsl__gljn is None:
            return left_on, right_on, rytox__nod
        if rytox__nod is None:
            return left_on, right_on, jngsl__gljn
        expr_node.lhs = jngsl__gljn
        expr_node.rhs = rytox__nod
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    uoxn__hoyq = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (uoxn__hoyq,))
    aqvg__gjo = dict()
    dodm__xifrq = pd.core.computation.parsing.clean_column_name
    for name, twbdy__szot in (('left', left_columns), ('right', right_columns)
        ):
        for qgi__hywra in twbdy__szot:
            cha__amn = dodm__xifrq(qgi__hywra)
            knwk__noqe = name, cha__amn
            if knwk__noqe in aqvg__gjo:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{qgi__hywra}' and '{aqvg__gjo[cha__amn]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            aqvg__gjo[knwk__noqe] = qgi__hywra
    buua__yuq, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=aqvg__gjo)
    left_on, right_on, zkg__lplnj = _extract_equal_conds(buua__yuq.terms)
    return left_on, right_on, _insert_NA_cond(zkg__lplnj, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    zexc__qca = dict(sort=sort, copy=copy, validate=validate)
    cvbs__imxb = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    zklrg__evpol = tuple(sorted(set(left.columns) & set(right.columns), key
        =lambda k: str(k)))
    pfham__foram = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in zklrg__evpol and ('left.' in on_str or 
                'right.' in on_str):
                left_on, right_on, fqr__zph = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if fqr__zph is None:
                    pfham__foram = ''
                else:
                    pfham__foram = str(fqr__zph)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = zklrg__evpol
        right_keys = zklrg__evpol
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    if (not left_on or not right_on) and not is_overload_none(on):
        raise BodoError(
            f"DataFrame.merge(): Merge condition '{get_overload_const_str(on)}' requires a cross join to implement, but cross join is not supported."
            )
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    lsykf__xclj = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        kxiay__ghugd = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        kxiay__ghugd = list(get_overload_const_list(suffixes))
    suffix_x = kxiay__ghugd[0]
    suffix_y = kxiay__ghugd[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    vnm__tref = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    vnm__tref += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    vnm__tref += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    vnm__tref += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, lsykf__xclj, pfham__foram))
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo}, smeb__ayk)
    _impl = smeb__ayk['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    valid_dataframe_column_types = (ArrayItemArrayType, MapArrayType,
        StructArrayType, CategoricalArrayType, types.Array,
        IntegerArrayType, DecimalArrayType, IntervalArrayType, bodo.
        DatetimeArrayType)
    mpae__uvgf = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    fxgn__drt = {get_overload_const_str(qpl__xqn) for qpl__xqn in (left_on,
        right_on, on) if is_overload_constant_str(qpl__xqn)}
    for df in (left, right):
        for i, qgi__hywra in enumerate(df.data):
            if not isinstance(qgi__hywra, valid_dataframe_column_types
                ) and qgi__hywra not in mpae__uvgf:
                raise BodoError(
                    f'{name_func}(): use of column with {type(qgi__hywra)} in merge unsupported'
                    )
            if df.columns[i] in fxgn__drt and isinstance(qgi__hywra,
                MapArrayType):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        kxiay__ghugd = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        kxiay__ghugd = list(get_overload_const_list(suffixes))
    if len(kxiay__ghugd) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    zklrg__evpol = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        vev__aeujg = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            vev__aeujg = on_str not in zklrg__evpol and ('left.' in on_str or
                'right.' in on_str)
        if len(zklrg__evpol) == 0 and not vev__aeujg:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    lvae__lyddm = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            rkaxt__nlraq = left.index
            hsc__kprlu = isinstance(rkaxt__nlraq, StringIndexType)
            ytin__ljx = right.index
            xswxp__lck = isinstance(ytin__ljx, StringIndexType)
        elif is_overload_true(left_index):
            rkaxt__nlraq = left.index
            hsc__kprlu = isinstance(rkaxt__nlraq, StringIndexType)
            ytin__ljx = right.data[right.columns.index(right_keys[0])]
            xswxp__lck = ytin__ljx.dtype == string_type
        elif is_overload_true(right_index):
            rkaxt__nlraq = left.data[left.columns.index(left_keys[0])]
            hsc__kprlu = rkaxt__nlraq.dtype == string_type
            ytin__ljx = right.index
            xswxp__lck = isinstance(ytin__ljx, StringIndexType)
        if hsc__kprlu and xswxp__lck:
            return
        rkaxt__nlraq = rkaxt__nlraq.dtype
        ytin__ljx = ytin__ljx.dtype
        try:
            bzce__ghtf = lvae__lyddm.resolve_function_type(operator.eq, (
                rkaxt__nlraq, ytin__ljx), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=rkaxt__nlraq, rk_dtype=ytin__ljx))
    else:
        for cjo__ksu, bwb__jkfk in zip(left_keys, right_keys):
            rkaxt__nlraq = left.data[left.columns.index(cjo__ksu)].dtype
            ecnlf__ivr = left.data[left.columns.index(cjo__ksu)]
            ytin__ljx = right.data[right.columns.index(bwb__jkfk)].dtype
            hjqr__cysdk = right.data[right.columns.index(bwb__jkfk)]
            if ecnlf__ivr == hjqr__cysdk:
                continue
            znhj__ozat = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=cjo__ksu, lk_dtype=rkaxt__nlraq, rk=bwb__jkfk,
                rk_dtype=ytin__ljx))
            rftk__juyn = rkaxt__nlraq == string_type
            xoajt__rabg = ytin__ljx == string_type
            if rftk__juyn ^ xoajt__rabg:
                raise_bodo_error(znhj__ozat)
            try:
                bzce__ghtf = lvae__lyddm.resolve_function_type(operator.eq,
                    (rkaxt__nlraq, ytin__ljx), {})
            except:
                raise_bodo_error(znhj__ozat)


def validate_keys(keys, df):
    atzdc__zhd = set(keys).difference(set(df.columns))
    if len(atzdc__zhd) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in atzdc__zhd:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {atzdc__zhd} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    zexc__qca = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    cvbs__imxb = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    vnm__tref = "def _impl(left, other, on=None, how='left',\n"
    vnm__tref += "    lsuffix='', rsuffix='', sort=False):\n"
    vnm__tref += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo}, smeb__ayk)
    _impl = smeb__ayk['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        xbhoy__alpm = get_overload_const_list(on)
        validate_keys(xbhoy__alpm, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    zklrg__evpol = tuple(set(left.columns) & set(other.columns))
    if len(zklrg__evpol) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=zklrg__evpol))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    elal__bsg = set(left_keys) & set(right_keys)
    jkk__layd = set(left_columns) & set(right_columns)
    xynj__qgv = jkk__layd - elal__bsg
    wxq__vvf = set(left_columns) - jkk__layd
    xls__djoov = set(right_columns) - jkk__layd
    loya__ads = {}

    def insertOutColumn(col_name):
        if col_name in loya__ads:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        loya__ads[col_name] = 0
    for nrv__tpjor in elal__bsg:
        insertOutColumn(nrv__tpjor)
    for nrv__tpjor in xynj__qgv:
        ajek__wfq = str(nrv__tpjor) + suffix_x
        ekt__pmhax = str(nrv__tpjor) + suffix_y
        insertOutColumn(ajek__wfq)
        insertOutColumn(ekt__pmhax)
    for nrv__tpjor in wxq__vvf:
        insertOutColumn(nrv__tpjor)
    for nrv__tpjor in xls__djoov:
        insertOutColumn(nrv__tpjor)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    zklrg__evpol = tuple(sorted(set(left.columns) & set(right.columns), key
        =lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = zklrg__evpol
        right_keys = zklrg__evpol
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        kxiay__ghugd = suffixes
    if is_overload_constant_list(suffixes):
        kxiay__ghugd = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        kxiay__ghugd = suffixes.value
    suffix_x = kxiay__ghugd[0]
    suffix_y = kxiay__ghugd[1]
    vnm__tref = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    vnm__tref += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    vnm__tref += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    vnm__tref += "    allow_exact_matches=True, direction='backward'):\n"
    vnm__tref += '  suffix_x = suffixes[0]\n'
    vnm__tref += '  suffix_y = suffixes[1]\n'
    vnm__tref += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo}, smeb__ayk)
    _impl = smeb__ayk['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True):
    check_runtime_cols_unsupported(df, 'DataFrame.groupby()')
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_bodo_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_bodo_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_bodo_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_bodo_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    zexc__qca = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    zeyra__dacyx = dict(sort=False, group_keys=True, squeeze=False,
        observed=True)
    check_unsupported_args('Dataframe.groupby', zexc__qca, zeyra__dacyx,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    ahz__ufkm = func_name == 'DataFrame.pivot_table'
    if ahz__ufkm:
        if is_overload_none(index) or not is_literal_type(index):
            raise_bodo_error(
                f"DataFrame.pivot_table(): 'index' argument is required and must be constant column labels"
                )
    elif not is_overload_none(index) and not is_literal_type(index):
        raise_bodo_error(
            f"{func_name}(): if 'index' argument is provided it must be constant column labels"
            )
    if is_overload_none(columns) or not is_literal_type(columns):
        raise_bodo_error(
            f"{func_name}(): 'columns' argument is required and must be a constant column label"
            )
    if not is_overload_none(values) and not is_literal_type(values):
        raise_bodo_error(
            f"{func_name}(): if 'values' argument is provided it must be constant column labels"
            )
    onzww__egit = get_literal_value(columns)
    if isinstance(onzww__egit, (list, tuple)):
        if len(onzww__egit) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {onzww__egit}"
                )
        onzww__egit = onzww__egit[0]
    if onzww__egit not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {onzww__egit} not found in DataFrame {df}."
            )
    ktnr__rpg = {xihz__ins: i for i, xihz__ins in enumerate(df.columns)}
    bswb__ikk = ktnr__rpg[onzww__egit]
    if is_overload_none(index):
        zjfme__ggb = []
        sxzea__ovxy = []
    else:
        sxzea__ovxy = get_literal_value(index)
        if not isinstance(sxzea__ovxy, (list, tuple)):
            sxzea__ovxy = [sxzea__ovxy]
        zjfme__ggb = []
        for index in sxzea__ovxy:
            if index not in ktnr__rpg:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            zjfme__ggb.append(ktnr__rpg[index])
    if not (all(isinstance(xihz__ins, int) for xihz__ins in sxzea__ovxy) or
        all(isinstance(xihz__ins, str) for xihz__ins in sxzea__ovxy)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        zeas__bgzyh = []
        xgh__updo = []
        elzlw__wthm = zjfme__ggb + [bswb__ikk]
        for i, xihz__ins in enumerate(df.columns):
            if i not in elzlw__wthm:
                zeas__bgzyh.append(i)
                xgh__updo.append(xihz__ins)
    else:
        xgh__updo = get_literal_value(values)
        if not isinstance(xgh__updo, (list, tuple)):
            xgh__updo = [xgh__updo]
        zeas__bgzyh = []
        for val in xgh__updo:
            if val not in ktnr__rpg:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            zeas__bgzyh.append(ktnr__rpg[val])
    if all(isinstance(xihz__ins, int) for xihz__ins in xgh__updo):
        xgh__updo = np.array(xgh__updo, 'int64')
    elif all(isinstance(xihz__ins, str) for xihz__ins in xgh__updo):
        xgh__updo = pd.array(xgh__updo, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    jno__bxf = set(zeas__bgzyh) | set(zjfme__ggb) | {bswb__ikk}
    if len(jno__bxf) != len(zeas__bgzyh) + len(zjfme__ggb) + 1:
        raise BodoError(
            f"{func_name}(): 'index', 'columns', and 'values' must all refer to different columns"
            )

    def check_valid_index_typ(index_column):
        if isinstance(index_column, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType, bodo.
            IntervalArrayType)):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column must have scalar rows"
                )
        if isinstance(index_column, bodo.CategoricalArrayType):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column does not support categorical data"
                )
    if len(zjfme__ggb) == 0:
        index = df.index
        if isinstance(index, MultiIndexType):
            raise BodoError(
                f"{func_name}(): 'index' cannot be None with a DataFrame with a multi-index"
                )
        if not isinstance(index, RangeIndexType):
            check_valid_index_typ(index.data)
        if not is_literal_type(df.index.name_typ):
            raise BodoError(
                f"{func_name}(): If 'index' is None, the name of the DataFrame's Index must be constant at compile-time"
                )
    else:
        for jgaiq__tuaj in zjfme__ggb:
            index_column = df.data[jgaiq__tuaj]
            check_valid_index_typ(index_column)
    sos__rbv = df.data[bswb__ikk]
    if isinstance(sos__rbv, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(sos__rbv, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for mpkr__egbz in zeas__bgzyh:
        rzpwz__zrll = df.data[mpkr__egbz]
        if isinstance(rzpwz__zrll, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or rzpwz__zrll == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (sxzea__ovxy, onzww__egit, xgh__updo, zjfme__ggb, bswb__ikk,
        zeas__bgzyh)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (sxzea__ovxy, onzww__egit, xgh__updo, jgaiq__tuaj, bswb__ikk, rsp__ynmd
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(sxzea__ovxy) == 0:
        if is_overload_none(data.index.name_typ):
            sxzea__ovxy = [None]
        else:
            sxzea__ovxy = [get_literal_value(data.index.name_typ)]
    if len(xgh__updo) == 1:
        gnbv__mjf = None
    else:
        gnbv__mjf = xgh__updo
    vnm__tref = 'def impl(data, index=None, columns=None, values=None):\n'
    vnm__tref += f'    pivot_values = data.iloc[:, {bswb__ikk}].unique()\n'
    vnm__tref += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(jgaiq__tuaj) == 0:
        vnm__tref += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        vnm__tref += '        (\n'
        for sbgga__kel in jgaiq__tuaj:
            vnm__tref += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {sbgga__kel}),
"""
        vnm__tref += '        ),\n'
    vnm__tref += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {bswb__ikk}),),
"""
    vnm__tref += '        (\n'
    for mpkr__egbz in rsp__ynmd:
        vnm__tref += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {mpkr__egbz}),
"""
    vnm__tref += '        ),\n'
    vnm__tref += '        pivot_values,\n'
    vnm__tref += '        index_lit_tup,\n'
    vnm__tref += '        columns_lit,\n'
    vnm__tref += '        values_name_const,\n'
    vnm__tref += '    )\n'
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo, 'index_lit_tup': tuple(sxzea__ovxy),
        'columns_lit': onzww__egit, 'values_name_const': gnbv__mjf}, smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


@overload(pd.pivot_table, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(data, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=False, sort=True, _pivot_values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot_table()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot_table()')
    zexc__qca = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    cvbs__imxb = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (sxzea__ovxy, onzww__egit, xgh__updo, jgaiq__tuaj, bswb__ikk, rsp__ynmd
            ) = (pivot_error_checking(data, index, columns, values,
            'DataFrame.pivot_table'))
        if len(xgh__updo) == 1:
            gnbv__mjf = None
        else:
            gnbv__mjf = xgh__updo
        vnm__tref = 'def impl(\n'
        vnm__tref += '    data,\n'
        vnm__tref += '    values=None,\n'
        vnm__tref += '    index=None,\n'
        vnm__tref += '    columns=None,\n'
        vnm__tref += '    aggfunc="mean",\n'
        vnm__tref += '    fill_value=None,\n'
        vnm__tref += '    margins=False,\n'
        vnm__tref += '    dropna=True,\n'
        vnm__tref += '    margins_name="All",\n'
        vnm__tref += '    observed=False,\n'
        vnm__tref += '    sort=True,\n'
        vnm__tref += '    _pivot_values=None,\n'
        vnm__tref += '):\n'
        pngeu__ofxi = jgaiq__tuaj + [bswb__ikk] + rsp__ynmd
        vnm__tref += f'    data = data.iloc[:, {pngeu__ofxi}]\n'
        ctrjk__culg = sxzea__ovxy + [onzww__egit]
        vnm__tref += (
            f'    data = data.groupby({ctrjk__culg!r}, as_index=False).agg(aggfunc)\n'
            )
        vnm__tref += (
            f'    pivot_values = data.iloc[:, {len(jgaiq__tuaj)}].unique()\n')
        vnm__tref += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
        vnm__tref += '        (\n'
        for i in range(0, len(jgaiq__tuaj)):
            vnm__tref += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        vnm__tref += '        ),\n'
        vnm__tref += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(jgaiq__tuaj)}),),
"""
        vnm__tref += '        (\n'
        for i in range(len(jgaiq__tuaj) + 1, len(rsp__ynmd) + len(
            jgaiq__tuaj) + 1):
            vnm__tref += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        vnm__tref += '        ),\n'
        vnm__tref += '        pivot_values,\n'
        vnm__tref += '        index_lit_tup,\n'
        vnm__tref += '        columns_lit,\n'
        vnm__tref += '        values_name_const,\n'
        vnm__tref += '        check_duplicates=False,\n'
        vnm__tref += '    )\n'
        smeb__ayk = {}
        exec(vnm__tref, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(sxzea__ovxy), 'columns_lit': onzww__egit,
            'values_name_const': gnbv__mjf}, smeb__ayk)
        impl = smeb__ayk['impl']
        return impl
    if aggfunc == 'mean':

        def _impl(data, values=None, index=None, columns=None, aggfunc=
            'mean', fill_value=None, margins=False, dropna=True,
            margins_name='All', observed=False, sort=True, _pivot_values=None):
            return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(data,
                values, index, columns, 'mean', _pivot_values)
        return _impl

    def _impl(data, values=None, index=None, columns=None, aggfunc='mean',
        fill_value=None, margins=False, dropna=True, margins_name='All',
        observed=False, sort=True, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(data, values,
            index, columns, aggfunc, _pivot_values)
    return _impl


@overload(pd.melt, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'melt', inline='always', no_unliteral=True)
def overload_dataframe_melt(frame, id_vars=None, value_vars=None, var_name=
    None, value_name='value', col_level=None, ignore_index=True):
    zexc__qca = dict(var_name=var_name, value_name=value_name, col_level=
        col_level, ignore_index=ignore_index)
    cvbs__imxb = dict(var_name=None, value_name='value', col_level=None,
        ignore_index=True)
    check_unsupported_args('DataFrame.melt', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise BodoError(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise BodoError(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal")
    ojcbl__kxj = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(ojcbl__kxj, (list, tuple)):
        ojcbl__kxj = [ojcbl__kxj]
    for xihz__ins in ojcbl__kxj:
        if xihz__ins not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {xihz__ins} not found in {frame}"
                )
    aqvg__gjo = {xihz__ins: i for i, xihz__ins in enumerate(frame.columns)}
    uhd__fpq = [aqvg__gjo[i] for i in ojcbl__kxj]
    if is_overload_none(value_vars):
        jtzue__nlflw = []
        bsx__uxkn = []
        for i, xihz__ins in enumerate(frame.columns):
            if i not in uhd__fpq:
                jtzue__nlflw.append(i)
                bsx__uxkn.append(xihz__ins)
    else:
        bsx__uxkn = get_literal_value(value_vars)
        if not isinstance(bsx__uxkn, (list, tuple)):
            bsx__uxkn = [bsx__uxkn]
        bsx__uxkn = [v for v in bsx__uxkn if v not in ojcbl__kxj]
        if not bsx__uxkn:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        jtzue__nlflw = []
        for val in bsx__uxkn:
            if val not in aqvg__gjo:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            jtzue__nlflw.append(aqvg__gjo[val])
    for xihz__ins in bsx__uxkn:
        if xihz__ins not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {xihz__ins} not found in {frame}"
                )
    if not (all(isinstance(xihz__ins, int) for xihz__ins in bsx__uxkn) or
        all(isinstance(xihz__ins, str) for xihz__ins in bsx__uxkn)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    xzmgm__msqpq = frame.data[jtzue__nlflw[0]]
    ayd__cngj = [frame.data[i].dtype for i in jtzue__nlflw]
    jtzue__nlflw = np.array(jtzue__nlflw, dtype=np.int64)
    uhd__fpq = np.array(uhd__fpq, dtype=np.int64)
    _, jnu__itgpa = bodo.utils.typing.get_common_scalar_dtype(ayd__cngj)
    if not jnu__itgpa:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': bsx__uxkn, 'val_type': xzmgm__msqpq
        }
    header = 'def impl(\n'
    header += '  frame,\n'
    header += '  id_vars=None,\n'
    header += '  value_vars=None,\n'
    header += '  var_name=None,\n'
    header += "  value_name='value',\n"
    header += '  col_level=None,\n'
    header += '  ignore_index=True,\n'
    header += '):\n'
    header += (
        '  dummy_id = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, 0)\n'
        )
    if frame.is_table_format and all(v == xzmgm__msqpq.dtype for v in ayd__cngj
        ):
        extra_globals['value_idxs'] = jtzue__nlflw
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(bsx__uxkn) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {jtzue__nlflw[0]})
"""
    else:
        pbil__dvtfq = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in jtzue__nlflw)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({pbil__dvtfq},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in uhd__fpq:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(bsx__uxkn)})\n'
            )
    tldrw__hyi = ', '.join(f'out_id{i}' for i in uhd__fpq) + (', ' if len(
        uhd__fpq) > 0 else '')
    data_args = tldrw__hyi + 'var_col, val_col'
    columns = tuple(ojcbl__kxj + ['variable', 'value'])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(bsx__uxkn)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    zexc__qca = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    cvbs__imxb = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(index,
        'pandas.crosstab()')
    if not isinstance(index, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'index' argument only supported for Series types, found {index}"
            )
    if not isinstance(columns, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'columns' argument only supported for Series types, found {columns}"
            )

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_values()')
    zexc__qca = dict(ignore_index=ignore_index, key=key)
    cvbs__imxb = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_bodo_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    lgisw__hhpz = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        lgisw__hhpz.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        zeoc__mil = [get_overload_const_tuple(by)]
    else:
        zeoc__mil = get_overload_const_list(by)
    zeoc__mil = set((k, '') if (k, '') in lgisw__hhpz else k for k in zeoc__mil
        )
    if len(zeoc__mil.difference(lgisw__hhpz)) > 0:
        uiwt__cpj = list(set(get_overload_const_list(by)).difference(
            lgisw__hhpz))
        raise_bodo_error(f'sort_values(): invalid keys {uiwt__cpj} for by.')
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        allm__euysz = get_overload_const_list(na_position)
        for na_position in allm__euysz:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_bodo_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_index()')
    zexc__qca = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    cvbs__imxb = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_bool(ascending):
        raise BodoError(
            "DataFrame.sort_index(): 'ascending' parameter must be of type bool"
            )
    if not is_overload_bool(inplace):
        raise BodoError(
            "DataFrame.sort_index(): 'inplace' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "DataFrame.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position)
    return _impl


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    zexc__qca = dict(limit=limit, downcast=downcast)
    cvbs__imxb = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    cab__wuhrl = not is_overload_none(value)
    uur__sqbc = not is_overload_none(method)
    if cab__wuhrl and uur__sqbc:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not cab__wuhrl and not uur__sqbc:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if cab__wuhrl:
        buce__gda = 'value=value'
    else:
        buce__gda = 'method=method'
    data_args = [(f"df['{xihz__ins}'].fillna({buce__gda}, inplace=inplace)" if
        isinstance(xihz__ins, str) else
        f'df[{xihz__ins}].fillna({buce__gda}, inplace=inplace)') for
        xihz__ins in df.columns]
    vnm__tref = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        vnm__tref += '  ' + '  \n'.join(data_args) + '\n'
        smeb__ayk = {}
        exec(vnm__tref, {}, smeb__ayk)
        impl = smeb__ayk['impl']
        return impl
    else:
        return _gen_init_df(vnm__tref, df.columns, ', '.join(wsnt__cxgd +
            '.values' for wsnt__cxgd in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    zexc__qca = dict(col_level=col_level, col_fill=col_fill)
    cvbs__imxb = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    vnm__tref = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    vnm__tref += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        rqbq__qrxv = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            rqbq__qrxv)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            vnm__tref += (
                '  m_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
                )
            cdi__bhti = ['m_index._data[{}]'.format(i) for i in range(df.
                index.nlevels)]
            data_args = cdi__bhti + data_args
        else:
            yvx__oxvop = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [yvx__oxvop] + data_args
    return _gen_init_df(vnm__tref, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    oefj__ltl = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and oefj__ltl == 1 or is_overload_constant_list(level) and list(
        get_overload_const_list(level)) == list(range(oefj__ltl))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.dropna()')
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        uqv__ubazu = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        pexwt__btr = get_overload_const_list(subset)
        uqv__ubazu = []
        for hxe__vglc in pexwt__btr:
            if hxe__vglc not in df.columns:
                raise_bodo_error(
                    f"df.dropna(): column '{hxe__vglc}' not in data frame columns {df}"
                    )
            uqv__ubazu.append(df.columns.index(hxe__vglc))
    mwiri__mtof = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(mwiri__mtof))
    vnm__tref = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(mwiri__mtof):
        vnm__tref += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    vnm__tref += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in uqv__ubazu)))
    vnm__tref += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(vnm__tref, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    zexc__qca = dict(index=index, level=level, errors=errors)
    cvbs__imxb = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', zexc__qca, cvbs__imxb,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            xosip__nuzf = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            xosip__nuzf = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            xosip__nuzf = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            xosip__nuzf = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for xihz__ins in xosip__nuzf:
        if xihz__ins not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(xihz__ins, df.columns))
    if len(set(xosip__nuzf)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    rehs__ffk = tuple(xihz__ins for xihz__ins in df.columns if xihz__ins not in
        xosip__nuzf)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(xihz__ins), '.copy()' if not inplace else
        '') for xihz__ins in rehs__ffk)
    vnm__tref = 'def impl(df, labels=None, axis=0, index=None, columns=None,\n'
    vnm__tref += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(vnm__tref, rehs__ffk, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    check_runtime_cols_unsupported(df, 'DataFrame.append()')
    check_runtime_cols_unsupported(other, 'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'DataFrame.append()')
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sample()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sample()')
    zexc__qca = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    anzvo__bear = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', zexc__qca, anzvo__bear,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    mwiri__mtof = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(mwiri__mtof))
    mzkcg__oze = ', '.join('rhs_data_{}'.format(i) for i in range(mwiri__mtof))
    vnm__tref = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    vnm__tref += '  if (frac == 1 or n == len(df)) and not replace:\n'
    vnm__tref += '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n'
    for i in range(mwiri__mtof):
        vnm__tref += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    vnm__tref += '  if frac is None:\n'
    vnm__tref += '    frac_d = -1.0\n'
    vnm__tref += '  else:\n'
    vnm__tref += '    frac_d = frac\n'
    vnm__tref += '  if n is None:\n'
    vnm__tref += '    n_i = 0\n'
    vnm__tref += '  else:\n'
    vnm__tref += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    vnm__tref += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({mzkcg__oze},), {index}, n_i, frac_d, replace)
"""
    vnm__tref += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(vnm__tref, df.columns,
        data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {x}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    check_runtime_cols_unsupported(df, 'DataFrame.info()')
    mevk__wfors = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    xntb__gcvqi = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', mevk__wfors, xntb__gcvqi,
        package_name='pandas', module_name='DataFrame')
    med__mnzll = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            fef__agy = med__mnzll + '\n'
            fef__agy += 'Index: 0 entries\n'
            fef__agy += 'Empty DataFrame'
            print(fef__agy)
        return _info_impl
    else:
        vnm__tref = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        vnm__tref += '    ncols = df.shape[1]\n'
        vnm__tref += f'    lines = "{med__mnzll}\\n"\n'
        vnm__tref += f'    lines += "{df.index}: "\n'
        vnm__tref += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            vnm__tref += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            vnm__tref += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            vnm__tref += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        vnm__tref += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        vnm__tref += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        vnm__tref += '    column_width = max(space, 7)\n'
        vnm__tref += '    column= "Column"\n'
        vnm__tref += '    underl= "------"\n'
        vnm__tref += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        vnm__tref += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        vnm__tref += '    mem_size = 0\n'
        vnm__tref += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        vnm__tref += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        vnm__tref += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        aqc__qki = dict()
        for i in range(len(df.columns)):
            vnm__tref += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            tygma__xynw = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                tygma__xynw = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                jxeq__hphc = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                tygma__xynw = f'{jxeq__hphc[:-7]}'
            vnm__tref += f'    col_dtype[{i}] = "{tygma__xynw}"\n'
            if tygma__xynw in aqc__qki:
                aqc__qki[tygma__xynw] += 1
            else:
                aqc__qki[tygma__xynw] = 1
            vnm__tref += f'    col_name[{i}] = "{df.columns[i]}"\n'
            vnm__tref += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        vnm__tref += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        vnm__tref += '    for i in column_info:\n'
        vnm__tref += "        lines += f'{i}\\n'\n"
        ixp__qxqou = ', '.join(f'{k}({aqc__qki[k]})' for k in sorted(aqc__qki))
        vnm__tref += f"    lines += 'dtypes: {ixp__qxqou}\\n'\n"
        vnm__tref += '    mem_size += df.index.nbytes\n'
        vnm__tref += '    total_size = _sizeof_fmt(mem_size)\n'
        vnm__tref += "    lines += f'memory usage: {total_size}'\n"
        vnm__tref += '    print(lines)\n'
        smeb__ayk = {}
        exec(vnm__tref, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo': bodo,
            'np': np}, smeb__ayk)
        _info_impl = smeb__ayk['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    vnm__tref = 'def impl(df, index=True, deep=False):\n'
    abgoi__hura = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes')
    uikhr__kvgk = is_overload_true(index)
    columns = df.columns
    if uikhr__kvgk:
        columns = ('Index',) + columns
    if len(columns) == 0:
        gfp__qpko = ()
    elif all(isinstance(xihz__ins, int) for xihz__ins in columns):
        gfp__qpko = np.array(columns, 'int64')
    elif all(isinstance(xihz__ins, str) for xihz__ins in columns):
        gfp__qpko = pd.array(columns, 'string')
    else:
        gfp__qpko = columns
    if df.is_table_format:
        xwjl__bnoxe = int(uikhr__kvgk)
        gupmn__lnrt = len(columns)
        vnm__tref += f'  nbytes_arr = np.empty({gupmn__lnrt}, np.int64)\n'
        vnm__tref += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        vnm__tref += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {xwjl__bnoxe})
"""
        if uikhr__kvgk:
            vnm__tref += f'  nbytes_arr[0] = {abgoi__hura}\n'
        vnm__tref += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if uikhr__kvgk:
            data = f'{abgoi__hura},{data}'
        else:
            dfsri__qeqq = ',' if len(columns) == 1 else ''
            data = f'{data}{dfsri__qeqq}'
        vnm__tref += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        gfp__qpko}, smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    yjix__tjdoi = 'read_excel_df{}'.format(next_label())
    setattr(types, yjix__tjdoi, df_type)
    rgzl__rdtsc = False
    if is_overload_constant_list(parse_dates):
        rgzl__rdtsc = get_overload_const_list(parse_dates)
    ryu__zgon = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    vnm__tref = f"""
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{yjix__tjdoi}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{ryu__zgon}}},
            engine=engine,
            converters=converters,
            true_values=true_values,
            false_values=false_values,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            keep_default_na=keep_default_na,
            na_filter=na_filter,
            verbose=verbose,
            parse_dates={rgzl__rdtsc},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    smeb__ayk = {}
    exec(vnm__tref, globals(), smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as bir__hwr:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    vnm__tref = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    vnm__tref += '    ylabel=None, title=None, legend=True, fontsize=None, \n'
    vnm__tref += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        vnm__tref += '   fig, ax = plt.subplots()\n'
    else:
        vnm__tref += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        vnm__tref += '   fig.set_figwidth(figsize[0])\n'
        vnm__tref += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        vnm__tref += '   xlabel = x\n'
    vnm__tref += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        vnm__tref += '   ylabel = y\n'
    else:
        vnm__tref += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        vnm__tref += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        vnm__tref += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    vnm__tref += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            vnm__tref += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            bksyn__kvlo = get_overload_const_str(x)
            sexmh__ihyj = df.columns.index(bksyn__kvlo)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if sexmh__ihyj != i:
                        vnm__tref += (
                            f'   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])\n'
                            )
        else:
            vnm__tref += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        vnm__tref += '   ax.scatter(df[x], df[y], s=20)\n'
        vnm__tref += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        vnm__tref += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        vnm__tref += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        vnm__tref += '   ax.legend()\n'
    vnm__tref += '   return ax\n'
    smeb__ayk = {}
    exec(vnm__tref, {'bodo': bodo, 'plt': plt}, smeb__ayk)
    impl = smeb__ayk['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for vcf__yaxo in df_typ.data:
        if not (isinstance(vcf__yaxo, IntegerArrayType) or isinstance(
            vcf__yaxo.dtype, types.Number) or vcf__yaxo.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns)):
            return False
    return True


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        vvumr__wrhed = args[0]
        rkt__lnwn = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        thr__zbkvf = vvumr__wrhed
        check_runtime_cols_unsupported(vvumr__wrhed, 'set_df_col()')
        if isinstance(vvumr__wrhed, DataFrameType):
            index = vvumr__wrhed.index
            if len(vvumr__wrhed.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(vvumr__wrhed.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if rkt__lnwn in vvumr__wrhed.columns:
                rehs__ffk = vvumr__wrhed.columns
                fwhub__uvird = vvumr__wrhed.columns.index(rkt__lnwn)
                xxzm__hrgkd = list(vvumr__wrhed.data)
                xxzm__hrgkd[fwhub__uvird] = val
                xxzm__hrgkd = tuple(xxzm__hrgkd)
            else:
                rehs__ffk = vvumr__wrhed.columns + (rkt__lnwn,)
                xxzm__hrgkd = vvumr__wrhed.data + (val,)
            thr__zbkvf = DataFrameType(xxzm__hrgkd, index, rehs__ffk,
                vvumr__wrhed.dist, vvumr__wrhed.is_table_format)
        return thr__zbkvf(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    wjeb__jxmq = {}

    def _rewrite_membership_op(self, node, left, right):
        wipko__jir = node.op
        op = self.visit(wipko__jir)
        return op, wipko__jir, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    qmtt__yitdh = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in qmtt__yitdh:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in qmtt__yitdh:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        mgex__hwxk = node.attr
        value = node.value
        lvkl__pwx = pd.core.computation.ops.LOCAL_TAG
        if mgex__hwxk in ('str', 'dt'):
            try:
                eno__cpy = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as lpg__lkf:
                col_name = lpg__lkf.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            eno__cpy = str(self.visit(value))
        knwk__noqe = eno__cpy, mgex__hwxk
        if knwk__noqe in join_cleaned_cols:
            mgex__hwxk = join_cleaned_cols[knwk__noqe]
        name = eno__cpy + '.' + mgex__hwxk
        if name.startswith(lvkl__pwx):
            name = name[len(lvkl__pwx):]
        if mgex__hwxk in ('str', 'dt'):
            qrb__byc = columns[cleaned_columns.index(eno__cpy)]
            wjeb__jxmq[qrb__byc] = eno__cpy
            self.env.scope[name] = 0
            return self.term_type(lvkl__pwx + name, self.env)
        qmtt__yitdh.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in qmtt__yitdh:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        dko__nkzgy = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        rkt__lnwn = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(dko__nkzgy), rkt__lnwn))

    def op__str__(self):
        oqbds__pctc = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            nrai__pojmj)) for nrai__pojmj in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(oqbds__pctc)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(oqbds__pctc)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(oqbds__pctc))
    nntmn__wymbg = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    mrtdj__ujsac = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_evaluate_binop)
    oui__qrm = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    ugkr__ngqh = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    hggt__xzh = pd.core.computation.ops.Term.__str__
    oycl__pezy = pd.core.computation.ops.MathCall.__str__
    pgg__eljn = pd.core.computation.ops.Op.__str__
    ltwm__uix = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        buua__yuq = pd.core.computation.expr.Expr(expr, env=env)
        fcla__iomf = str(buua__yuq)
    except pd.core.computation.ops.UndefinedVariableError as lpg__lkf:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == lpg__lkf.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {lpg__lkf}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            nntmn__wymbg)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            mrtdj__ujsac)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = oui__qrm
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = ugkr__ngqh
        pd.core.computation.ops.Term.__str__ = hggt__xzh
        pd.core.computation.ops.MathCall.__str__ = oycl__pezy
        pd.core.computation.ops.Op.__str__ = pgg__eljn
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            ltwm__uix)
    zmee__sxvg = pd.core.computation.parsing.clean_column_name
    wjeb__jxmq.update({xihz__ins: zmee__sxvg(xihz__ins) for xihz__ins in
        columns if zmee__sxvg(xihz__ins) in buua__yuq.names})
    return buua__yuq, fcla__iomf, wjeb__jxmq


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        mwz__zwu = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(mwz__zwu))
        urg__hzdm = namedtuple('Pandas', col_names)
        asmon__rlj = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], urg__hzdm)
        super(DataFrameTupleIterator, self).__init__(name, asmon__rlj)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        ddk__fkbar = [if_series_to_array_type(a) for a in args[len(args) // 2:]
            ]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        ddk__fkbar = [types.Array(types.int64, 1, 'C')] + ddk__fkbar
        lxktj__gpti = DataFrameTupleIterator(col_names, ddk__fkbar)
        return lxktj__gpti(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        aecze__dvfyo = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            aecze__dvfyo)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    tmq__dqvna = args[len(args) // 2:]
    eihox__pgtq = sig.args[len(sig.args) // 2:]
    tbpyi__fje = context.make_helper(builder, sig.return_type)
    ukpes__dqg = context.get_constant(types.intp, 0)
    yjg__iuw = cgutils.alloca_once_value(builder, ukpes__dqg)
    tbpyi__fje.index = yjg__iuw
    for i, arr in enumerate(tmq__dqvna):
        setattr(tbpyi__fje, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(tmq__dqvna, eihox__pgtq):
        context.nrt.incref(builder, arr_typ, arr)
    res = tbpyi__fje._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    puo__fjpm, = sig.args
    xqqof__kpbql, = args
    tbpyi__fje = context.make_helper(builder, puo__fjpm, value=xqqof__kpbql)
    dhlz__qcj = signature(types.intp, puo__fjpm.array_types[1])
    jfjjh__kvio = context.compile_internal(builder, lambda a: len(a),
        dhlz__qcj, [tbpyi__fje.array0])
    index = builder.load(tbpyi__fje.index)
    fbojs__rvv = builder.icmp_signed('<', index, jfjjh__kvio)
    result.set_valid(fbojs__rvv)
    with builder.if_then(fbojs__rvv):
        values = [index]
        for i, arr_typ in enumerate(puo__fjpm.array_types[1:]):
            ron__shuqx = getattr(tbpyi__fje, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                fyfoq__gsh = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    fyfoq__gsh, [ron__shuqx, index])
            else:
                fyfoq__gsh = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    fyfoq__gsh, [ron__shuqx, index])
            values.append(val)
        value = context.make_tuple(builder, puo__fjpm.yield_type, values)
        result.yield_(value)
        nray__rovgv = cgutils.increment_index(builder, index)
        builder.store(nray__rovgv, tbpyi__fje.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    xue__wsci = ir.Assign(rhs, lhs, expr.loc)
    ooc__eek = lhs
    ryw__xmfon = []
    duk__sbal = []
    jwh__tybqk = typ.count
    for i in range(jwh__tybqk):
        fadnk__shv = ir.Var(ooc__eek.scope, mk_unique_var('{}_size{}'.
            format(ooc__eek.name, i)), ooc__eek.loc)
        vswgq__lpi = ir.Expr.static_getitem(lhs, i, None, ooc__eek.loc)
        self.calltypes[vswgq__lpi] = None
        ryw__xmfon.append(ir.Assign(vswgq__lpi, fadnk__shv, ooc__eek.loc))
        self._define(equiv_set, fadnk__shv, types.intp, vswgq__lpi)
        duk__sbal.append(fadnk__shv)
    vpr__bha = tuple(duk__sbal)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        vpr__bha, pre=[xue__wsci] + ryw__xmfon)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
