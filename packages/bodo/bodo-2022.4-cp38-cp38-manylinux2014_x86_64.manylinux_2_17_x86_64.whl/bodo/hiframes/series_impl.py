"""
Implementation of Series attributes and methods using overload.
"""
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, overload_attribute, overload_method, register_jitable
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, datetime_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_offsets_ext import is_offsets_type
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType, if_series_to_array_type, is_series_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.transform import gen_const_tup, is_var_size_item_array_type
from bodo.utils.typing import BodoError, can_replace, check_unsupported_args, dtype_to_array_type, element_type, get_common_scalar_dtype, get_literal_value, get_overload_const_bytes, get_overload_const_int, get_overload_const_str, is_common_scalar_dtype, is_iterable_type, is_literal_type, is_nullable_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_int, is_overload_constant_nan, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, is_str_arr_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array


@overload_attribute(HeterogeneousSeriesType, 'index', inline='always')
@overload_attribute(SeriesType, 'index', inline='always')
def overload_series_index(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_index(s)


@overload_attribute(HeterogeneousSeriesType, 'values', inline='always')
@overload_attribute(SeriesType, 'values', inline='always')
def overload_series_values(s):
    if isinstance(s.data, bodo.DatetimeArrayType):

        def impl(s):
            ieeje__temb = bodo.hiframes.pd_series_ext.get_series_data(s)
            vxun__rxaaw = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                ieeje__temb)
            return vxun__rxaaw
        return impl
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s)


@overload_attribute(SeriesType, 'dtype', inline='always')
def overload_series_dtype(s):
    if s.dtype == bodo.string_type:
        raise BodoError('Series.dtype not supported for string Series yet')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(s, 'Series.dtype'
        )
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s).dtype


@overload_attribute(HeterogeneousSeriesType, 'shape')
@overload_attribute(SeriesType, 'shape')
def overload_series_shape(s):
    return lambda s: (len(bodo.hiframes.pd_series_ext.get_series_data(s)),)


@overload_attribute(HeterogeneousSeriesType, 'ndim', inline='always')
@overload_attribute(SeriesType, 'ndim', inline='always')
def overload_series_ndim(s):
    return lambda s: 1


@overload_attribute(HeterogeneousSeriesType, 'size')
@overload_attribute(SeriesType, 'size')
def overload_series_size(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s))


@overload_attribute(HeterogeneousSeriesType, 'T', inline='always')
@overload_attribute(SeriesType, 'T', inline='always')
def overload_series_T(s):
    return lambda s: s


@overload_attribute(SeriesType, 'hasnans', inline='always')
def overload_series_hasnans(s):
    return lambda s: s.isna().sum() != 0


@overload_attribute(HeterogeneousSeriesType, 'empty')
@overload_attribute(SeriesType, 'empty')
def overload_series_empty(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s)) == 0


@overload_attribute(SeriesType, 'dtypes', inline='always')
def overload_series_dtypes(s):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(s,
        'Series.dtypes')
    return lambda s: s.dtype


@overload_attribute(HeterogeneousSeriesType, 'name', inline='always')
@overload_attribute(SeriesType, 'name', inline='always')
def overload_series_name(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_name(s)


@overload(len, no_unliteral=True)
def overload_series_len(S):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)):
        return lambda S: len(bodo.hiframes.pd_series_ext.get_series_data(S))


@overload_method(SeriesType, 'copy', inline='always', no_unliteral=True)
def overload_series_copy(S, deep=True):
    if is_overload_true(deep):

        def impl1(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr.copy(),
                index, name)
        return impl1
    if is_overload_false(deep):

        def impl2(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl2

    def impl(S, deep=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        if deep:
            arr = arr.copy()
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'to_list', no_unliteral=True)
@overload_method(SeriesType, 'tolist', no_unliteral=True)
def overload_series_to_list(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.tolist()')
    if isinstance(S.dtype, types.Float):

        def impl_float(S):
            doom__iesow = list()
            for bfuho__etxot in range(len(S)):
                doom__iesow.append(S.iat[bfuho__etxot])
            return doom__iesow
        return impl_float

    def impl(S):
        doom__iesow = list()
        for bfuho__etxot in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, bfuho__etxot):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            doom__iesow.append(S.iat[bfuho__etxot])
        return doom__iesow
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    abe__jlau = dict(dtype=dtype, copy=copy, na_value=na_value)
    obdgq__bisy = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    abe__jlau = dict(name=name, inplace=inplace)
    obdgq__bisy = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not bodo.hiframes.dataframe_impl._is_all_levels(S, level):
        raise_bodo_error(
            'Series.reset_index(): only dropping all index levels supported')
    if not is_overload_constant_bool(drop):
        raise_bodo_error(
            "Series.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if is_overload_true(drop):

        def impl_drop(S, level=None, drop=False, name=None, inplace=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_index_ext.init_range_index(0, len(arr),
                1, None)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl_drop

    def get_name_literal(name_typ, is_index=False, series_name=None):
        if is_overload_none(name_typ):
            if is_index:
                return 'index' if series_name != 'index' else 'level_0'
            return 0
        if is_literal_type(name_typ):
            return get_literal_value(name_typ)
        else:
            raise BodoError(
                'Series.reset_index() not supported for non-literal series names'
                )
    series_name = get_name_literal(S.name_typ)
    ygwk__ccwft = get_name_literal(S.index.name_typ, True, series_name)
    columns = [ygwk__ccwft, series_name]
    lfjvl__qgur = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    lfjvl__qgur += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    lfjvl__qgur += """    index = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S))
"""
    lfjvl__qgur += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    lfjvl__qgur += '    col_var = {}\n'.format(gen_const_tup(columns))
    lfjvl__qgur += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe((index, arr), df_index, col_var)
"""
    gzzqa__ovg = {}
    exec(lfjvl__qgur, {'bodo': bodo}, gzzqa__ovg)
    gxpnh__qjq = gzzqa__ovg['_impl']
    return gxpnh__qjq


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        yeqbi__wwxm = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


@overload_method(SeriesType, 'round', inline='always', no_unliteral=True)
def overload_series_round(S, decimals=0):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.round()')

    def impl(S, decimals=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        yeqbi__wwxm = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[bfuho__etxot]):
                bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot)
            else:
                yeqbi__wwxm[bfuho__etxot] = np.round(arr[bfuho__etxot],
                    decimals)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    abe__jlau = dict(level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sum(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sum(): skipna argument must be a boolean')
    if not is_overload_int(min_count):
        raise BodoError('Series.sum(): min_count argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sum()'
        )

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_sum(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'prod', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'product', inline='always', no_unliteral=True)
def overload_series_prod(S, axis=None, skipna=True, level=None,
    numeric_only=None, min_count=0):
    abe__jlau = dict(level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.product(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.product(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.product()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_prod(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'any', inline='always', no_unliteral=True)
def overload_series_any(S, axis=0, bool_only=None, skipna=True, level=None):
    abe__jlau = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    obdgq__bisy = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        edpuv__rkd = 0
        for bfuho__etxot in numba.parfors.parfor.internal_prange(len(A)):
            kiyjo__rzagr = 0
            if not bodo.libs.array_kernels.isna(A, bfuho__etxot):
                kiyjo__rzagr = int(A[bfuho__etxot])
            edpuv__rkd += kiyjo__rzagr
        return edpuv__rkd != 0
    return impl


@overload_method(SeriesType, 'equals', inline='always', no_unliteral=True)
def overload_series_equals(S, other):
    if not isinstance(other, SeriesType):
        raise BodoError("Series.equals() 'other' must be a Series")
    if isinstance(S.data, bodo.ArrayItemArrayType):
        raise BodoError(
            'Series.equals() not supported for Series where each element is an array or list'
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.equals()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.equals()')
    if S.data != other.data:
        return lambda S, other: False

    def impl(S, other):
        jojuz__khr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xnh__bioj = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        edpuv__rkd = 0
        for bfuho__etxot in numba.parfors.parfor.internal_prange(len(
            jojuz__khr)):
            kiyjo__rzagr = 0
            ppwe__paf = bodo.libs.array_kernels.isna(jojuz__khr, bfuho__etxot)
            pfqvy__udevn = bodo.libs.array_kernels.isna(xnh__bioj, bfuho__etxot
                )
            if (ppwe__paf and not pfqvy__udevn or not ppwe__paf and
                pfqvy__udevn):
                kiyjo__rzagr = 1
            elif not ppwe__paf:
                if jojuz__khr[bfuho__etxot] != xnh__bioj[bfuho__etxot]:
                    kiyjo__rzagr = 1
            edpuv__rkd += kiyjo__rzagr
        return edpuv__rkd == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    abe__jlau = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    obdgq__bisy = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        edpuv__rkd = 0
        for bfuho__etxot in numba.parfors.parfor.internal_prange(len(A)):
            kiyjo__rzagr = 0
            if not bodo.libs.array_kernels.isna(A, bfuho__etxot):
                kiyjo__rzagr = int(not A[bfuho__etxot])
            edpuv__rkd += kiyjo__rzagr
        return edpuv__rkd == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    abe__jlau = dict(level=level)
    obdgq__bisy = dict(level=None)
    check_unsupported_args('Series.mad', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    cykfz__jow = types.float64
    zls__nrjat = types.float64
    if S.dtype == types.float32:
        cykfz__jow = types.float32
        zls__nrjat = types.float32
    gudwo__ufokt = cykfz__jow(0)
    fxr__kjtyb = zls__nrjat(0)
    gtbhz__hrep = zls__nrjat(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        usxe__akf = gudwo__ufokt
        edpuv__rkd = fxr__kjtyb
        for bfuho__etxot in numba.parfors.parfor.internal_prange(len(A)):
            kiyjo__rzagr = gudwo__ufokt
            siv__jpjsb = fxr__kjtyb
            if not bodo.libs.array_kernels.isna(A, bfuho__etxot) or not skipna:
                kiyjo__rzagr = A[bfuho__etxot]
                siv__jpjsb = gtbhz__hrep
            usxe__akf += kiyjo__rzagr
            edpuv__rkd += siv__jpjsb
        vmmsc__lga = bodo.hiframes.series_kernels._mean_handle_nan(usxe__akf,
            edpuv__rkd)
        jpqa__raqi = gudwo__ufokt
        for bfuho__etxot in numba.parfors.parfor.internal_prange(len(A)):
            kiyjo__rzagr = gudwo__ufokt
            if not bodo.libs.array_kernels.isna(A, bfuho__etxot) or not skipna:
                kiyjo__rzagr = abs(A[bfuho__etxot] - vmmsc__lga)
            jpqa__raqi += kiyjo__rzagr
        qgehd__qjvpr = bodo.hiframes.series_kernels._mean_handle_nan(jpqa__raqi
            , edpuv__rkd)
        return qgehd__qjvpr
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    abe__jlau = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mean(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.mean()')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_mean(arr)
    return impl


@overload_method(SeriesType, 'sem', inline='always', no_unliteral=True)
def overload_series_sem(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    abe__jlau = dict(level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sem(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sem(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.sem(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sem()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        tou__okz = 0
        bqqxp__gkvk = 0
        edpuv__rkd = 0
        for bfuho__etxot in numba.parfors.parfor.internal_prange(len(A)):
            kiyjo__rzagr = 0
            siv__jpjsb = 0
            if not bodo.libs.array_kernels.isna(A, bfuho__etxot) or not skipna:
                kiyjo__rzagr = A[bfuho__etxot]
                siv__jpjsb = 1
            tou__okz += kiyjo__rzagr
            bqqxp__gkvk += kiyjo__rzagr * kiyjo__rzagr
            edpuv__rkd += siv__jpjsb
        joyq__xcd = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            tou__okz, bqqxp__gkvk, edpuv__rkd, ddof)
        swts__nyfxf = bodo.hiframes.series_kernels._sem_handle_nan(joyq__xcd,
            edpuv__rkd)
        return swts__nyfxf
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    abe__jlau = dict(level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.kurtosis(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError(
            "Series.kurtosis(): 'skipna' argument must be a boolean")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.kurtosis()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        tou__okz = 0.0
        bqqxp__gkvk = 0.0
        axfpd__jipaw = 0.0
        nnxft__gnd = 0.0
        edpuv__rkd = 0
        for bfuho__etxot in numba.parfors.parfor.internal_prange(len(A)):
            kiyjo__rzagr = 0.0
            siv__jpjsb = 0
            if not bodo.libs.array_kernels.isna(A, bfuho__etxot) or not skipna:
                kiyjo__rzagr = np.float64(A[bfuho__etxot])
                siv__jpjsb = 1
            tou__okz += kiyjo__rzagr
            bqqxp__gkvk += kiyjo__rzagr ** 2
            axfpd__jipaw += kiyjo__rzagr ** 3
            nnxft__gnd += kiyjo__rzagr ** 4
            edpuv__rkd += siv__jpjsb
        joyq__xcd = bodo.hiframes.series_kernels.compute_kurt(tou__okz,
            bqqxp__gkvk, axfpd__jipaw, nnxft__gnd, edpuv__rkd)
        return joyq__xcd
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    abe__jlau = dict(level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.skew(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.skew(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.skew()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        tou__okz = 0.0
        bqqxp__gkvk = 0.0
        axfpd__jipaw = 0.0
        edpuv__rkd = 0
        for bfuho__etxot in numba.parfors.parfor.internal_prange(len(A)):
            kiyjo__rzagr = 0.0
            siv__jpjsb = 0
            if not bodo.libs.array_kernels.isna(A, bfuho__etxot) or not skipna:
                kiyjo__rzagr = np.float64(A[bfuho__etxot])
                siv__jpjsb = 1
            tou__okz += kiyjo__rzagr
            bqqxp__gkvk += kiyjo__rzagr ** 2
            axfpd__jipaw += kiyjo__rzagr ** 3
            edpuv__rkd += siv__jpjsb
        joyq__xcd = bodo.hiframes.series_kernels.compute_skew(tou__okz,
            bqqxp__gkvk, axfpd__jipaw, edpuv__rkd)
        return joyq__xcd
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    abe__jlau = dict(level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.var(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.var(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.var(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.var()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_var(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'std', inline='always', no_unliteral=True)
def overload_series_std(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    abe__jlau = dict(level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.std(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.std(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.std(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.std()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_std(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'dot', inline='always', no_unliteral=True)
def overload_series_dot(S, other):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.dot()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.dot()')

    def impl(S, other):
        jojuz__khr = bodo.hiframes.pd_series_ext.get_series_data(S)
        xnh__bioj = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        fvl__mhb = 0
        for bfuho__etxot in numba.parfors.parfor.internal_prange(len(
            jojuz__khr)):
            aueft__egon = jojuz__khr[bfuho__etxot]
            fhp__qzamh = xnh__bioj[bfuho__etxot]
            fvl__mhb += aueft__egon * fhp__qzamh
        return fvl__mhb
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    abe__jlau = dict(skipna=skipna)
    obdgq__bisy = dict(skipna=True)
    check_unsupported_args('Series.cumsum', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumsum(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumsum()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumsum(), index, name)
    return impl


@overload_method(SeriesType, 'cumprod', inline='always', no_unliteral=True)
def overload_series_cumprod(S, axis=None, skipna=True):
    abe__jlau = dict(skipna=skipna)
    obdgq__bisy = dict(skipna=True)
    check_unsupported_args('Series.cumprod', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumprod(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumprod()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumprod(), index, name
            )
    return impl


@overload_method(SeriesType, 'cummin', inline='always', no_unliteral=True)
def overload_series_cummin(S, axis=None, skipna=True):
    abe__jlau = dict(skipna=skipna)
    obdgq__bisy = dict(skipna=True)
    check_unsupported_args('Series.cummin', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummin(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummin()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummin(arr), index, name)
    return impl


@overload_method(SeriesType, 'cummax', inline='always', no_unliteral=True)
def overload_series_cummax(S, axis=None, skipna=True):
    abe__jlau = dict(skipna=skipna)
    obdgq__bisy = dict(skipna=True)
    check_unsupported_args('Series.cummax', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummax(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummax()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummax(arr), index, name)
    return impl


@overload_method(SeriesType, 'rename', inline='always', no_unliteral=True)
def overload_series_rename(S, index=None, axis=None, copy=True, inplace=
    False, level=None, errors='ignore'):
    if not (index == bodo.string_type or isinstance(index, types.StringLiteral)
        ):
        raise BodoError("Series.rename() 'index' can only be a string")
    abe__jlau = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    obdgq__bisy = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        swip__lfkt = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, swip__lfkt, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    abe__jlau = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    obdgq__bisy = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if is_overload_none(mapper) or not is_scalar_type(mapper):
        raise BodoError(
            "Series.rename_axis(): 'mapper' is required and must be a scalar type."
            )

    def impl(S, mapper=None, index=None, columns=None, axis=None, copy=True,
        inplace=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        index = index.rename(mapper)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'abs', inline='always', no_unliteral=True)
def overload_series_abs(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.abs()'
        )

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(np.abs(A), index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    abe__jlau = dict(level=level)
    obdgq__bisy = dict(level=None)
    check_unsupported_args('Series.count', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    abe__jlau = dict(method=method, min_periods=min_periods)
    obdgq__bisy = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        vimd__xpv = S.sum()
        dlhp__ptpd = other.sum()
        a = n * (S * other).sum() - vimd__xpv * dlhp__ptpd
        tjbz__anr = n * (S ** 2).sum() - vimd__xpv ** 2
        iisw__klv = n * (other ** 2).sum() - dlhp__ptpd ** 2
        return a / np.sqrt(tjbz__anr * iisw__klv)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    abe__jlau = dict(min_periods=min_periods)
    obdgq__bisy = dict(min_periods=None)
    check_unsupported_args('Series.cov', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        vimd__xpv = S.mean()
        dlhp__ptpd = other.mean()
        pvibs__enmwa = ((S - vimd__xpv) * (other - dlhp__ptpd)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(pvibs__enmwa, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            fgwr__uxh = np.sign(sum_val)
            return np.inf * fgwr__uxh
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    abe__jlau = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.min()'
        )

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_min(arr)
    return impl


@overload(max, no_unliteral=True)
def overload_series_builtins_max(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.max()
        return impl


@overload(min, no_unliteral=True)
def overload_series_builtins_min(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.min()
        return impl


@overload(sum, no_unliteral=True)
def overload_series_builtins_sum(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.sum()
        return impl


@overload(np.prod, inline='always', no_unliteral=True)
def overload_series_np_prod(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.prod()
        return impl


@overload_method(SeriesType, 'max', inline='always', no_unliteral=True)
def overload_series_max(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    abe__jlau = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.max()'
        )

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    abe__jlau = dict(axis=axis, skipna=skipna)
    obdgq__bisy = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmin()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmin() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmin(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmin(arr, index)
    return impl


@overload_method(SeriesType, 'idxmax', inline='always', no_unliteral=True)
def overload_series_idxmax(S, axis=0, skipna=True):
    abe__jlau = dict(axis=axis, skipna=skipna)
    obdgq__bisy = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmax()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmax() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmax(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmax(arr, index)
    return impl


@overload_method(SeriesType, 'infer_objects', inline='always')
def overload_series_infer_objects(S):
    return lambda S: S.copy()


@overload_attribute(SeriesType, 'is_monotonic', inline='always')
@overload_attribute(SeriesType, 'is_monotonic_increasing', inline='always')
def overload_series_is_monotonic_increasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_increasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 1)


@overload_attribute(SeriesType, 'is_monotonic_decreasing', inline='always')
def overload_series_is_monotonic_decreasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_decreasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 2)


@overload_attribute(SeriesType, 'nbytes', inline='always')
def overload_series_nbytes(S):
    return lambda S: bodo.hiframes.pd_series_ext.get_series_data(S).nbytes


@overload_method(SeriesType, 'autocorr', inline='always', no_unliteral=True)
def overload_series_autocorr(S, lag=1):
    return lambda S, lag=1: bodo.libs.array_kernels.autocorr(bodo.hiframes.
        pd_series_ext.get_series_data(S), lag)


@overload_method(SeriesType, 'median', inline='always', no_unliteral=True)
def overload_series_median(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    abe__jlau = dict(level=level, numeric_only=numeric_only)
    obdgq__bisy = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.median(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.median(): skipna argument must be a boolean')
    return (lambda S, axis=None, skipna=True, level=None, numeric_only=None:
        bodo.libs.array_ops.array_op_median(bodo.hiframes.pd_series_ext.
        get_series_data(S), skipna))


def overload_series_head(S, n=5):

    def impl(S, n=5):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        iho__xpp = arr[:n]
        dsc__upb = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(iho__xpp, dsc__upb, name
            )
    return impl


@lower_builtin('series.head', SeriesType, types.Integer)
@lower_builtin('series.head', SeriesType, types.Omitted)
def series_head_lower(context, builder, sig, args):
    impl = overload_series_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@numba.extending.register_jitable
def tail_slice(k, n):
    if n == 0:
        return k
    return -n


@overload_method(SeriesType, 'tail', inline='always', no_unliteral=True)
def overload_series_tail(S, n=5):
    if not is_overload_int(n):
        raise BodoError("Series.tail(): 'n' must be an Integer")

    def impl(S, n=5):
        ybgp__nryxc = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        iho__xpp = arr[ybgp__nryxc:]
        dsc__upb = index[ybgp__nryxc:]
        return bodo.hiframes.pd_series_ext.init_series(iho__xpp, dsc__upb, name
            )
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    pwdti__nbkw = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in pwdti__nbkw:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            ecinv__iaj = index[0]
            ihk__bci = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                ecinv__iaj, False))
        else:
            ihk__bci = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        iho__xpp = arr[:ihk__bci]
        dsc__upb = index[:ihk__bci]
        return bodo.hiframes.pd_series_ext.init_series(iho__xpp, dsc__upb, name
            )
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    pwdti__nbkw = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in pwdti__nbkw:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            vpxv__bugz = index[-1]
            ihk__bci = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                vpxv__bugz, True))
        else:
            ihk__bci = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        iho__xpp = arr[len(arr) - ihk__bci:]
        dsc__upb = index[len(arr) - ihk__bci:]
        return bodo.hiframes.pd_series_ext.init_series(iho__xpp, dsc__upb, name
            )
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pqy__gic = bodo.utils.conversion.index_to_array(index)
        bmj__vynpv, qmv__yvwk = bodo.libs.array_kernels.first_last_valid_index(
            arr, pqy__gic)
        return qmv__yvwk if bmj__vynpv else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pqy__gic = bodo.utils.conversion.index_to_array(index)
        bmj__vynpv, qmv__yvwk = bodo.libs.array_kernels.first_last_valid_index(
            arr, pqy__gic, False)
        return qmv__yvwk if bmj__vynpv else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    abe__jlau = dict(keep=keep)
    obdgq__bisy = dict(keep='first')
    check_unsupported_args('Series.nlargest', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pqy__gic = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        yeqbi__wwxm, zwgzz__lpjv = bodo.libs.array_kernels.nlargest(arr,
            pqy__gic, n, True, bodo.hiframes.series_kernels.gt_f)
        ymg__upqp = bodo.utils.conversion.convert_to_index(zwgzz__lpjv)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
            ymg__upqp, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    abe__jlau = dict(keep=keep)
    obdgq__bisy = dict(keep='first')
    check_unsupported_args('Series.nsmallest', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pqy__gic = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        yeqbi__wwxm, zwgzz__lpjv = bodo.libs.array_kernels.nlargest(arr,
            pqy__gic, n, False, bodo.hiframes.series_kernels.lt_f)
        ymg__upqp = bodo.utils.conversion.convert_to_index(zwgzz__lpjv)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
            ymg__upqp, name)
    return impl


@overload_method(SeriesType, 'notnull', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'notna', inline='always', no_unliteral=True)
def overload_series_notna(S):
    return lambda S: S.isna() == False


@overload_method(SeriesType, 'astype', inline='always', no_unliteral=True)
@overload_method(HeterogeneousSeriesType, 'astype', inline='always',
    no_unliteral=True)
def overload_series_astype(S, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    abe__jlau = dict(errors=errors)
    obdgq__bisy = dict(errors='raise')
    check_unsupported_args('Series.astype', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "Series.astype(): 'dtype' when passed as string must be a constant value"
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.astype()')

    def impl(S, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        yeqbi__wwxm = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    abe__jlau = dict(axis=axis, is_copy=is_copy)
    obdgq__bisy = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        zcx__rklnj = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[zcx__rklnj],
            index[zcx__rklnj], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    abe__jlau = dict(axis=axis, kind=kind, order=order)
    obdgq__bisy = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        dkh__drqi = S.notna().values
        if not dkh__drqi.all():
            yeqbi__wwxm = np.full(n, -1, np.int64)
            yeqbi__wwxm[dkh__drqi] = argsort(arr[dkh__drqi])
        else:
            yeqbi__wwxm = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    abe__jlau = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    obdgq__bisy = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xkvyc__rsubr = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        kjn__ooz = xkvyc__rsubr.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        yeqbi__wwxm = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            kjn__ooz, 0)
        ymg__upqp = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(kjn__ooz
            )
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
            ymg__upqp, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    abe__jlau = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    obdgq__bisy = dict(axis=0, inplace=False, kind='quicksort',
        ignore_index=False, key=None)
    check_unsupported_args('Series.sort_values', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xkvyc__rsubr = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        kjn__ooz = xkvyc__rsubr.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        yeqbi__wwxm = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            kjn__ooz, 0)
        ymg__upqp = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(kjn__ooz
            )
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
            ymg__upqp, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    ossip__dsaw = is_overload_true(is_nullable)
    lfjvl__qgur = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    lfjvl__qgur += '  numba.parfors.parfor.init_prange()\n'
    lfjvl__qgur += '  n = len(arr)\n'
    if ossip__dsaw:
        lfjvl__qgur += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        lfjvl__qgur += '  out_arr = np.empty(n, np.int64)\n'
    lfjvl__qgur += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    lfjvl__qgur += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if ossip__dsaw:
        lfjvl__qgur += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        lfjvl__qgur += '      out_arr[i] = -1\n'
    lfjvl__qgur += '      continue\n'
    lfjvl__qgur += '    val = arr[i]\n'
    lfjvl__qgur += '    if include_lowest and val == bins[0]:\n'
    lfjvl__qgur += '      ind = 1\n'
    lfjvl__qgur += '    else:\n'
    lfjvl__qgur += '      ind = np.searchsorted(bins, val)\n'
    lfjvl__qgur += '    if ind == 0 or ind == len(bins):\n'
    if ossip__dsaw:
        lfjvl__qgur += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        lfjvl__qgur += '      out_arr[i] = -1\n'
    lfjvl__qgur += '    else:\n'
    lfjvl__qgur += '      out_arr[i] = ind - 1\n'
    lfjvl__qgur += '  return out_arr\n'
    gzzqa__ovg = {}
    exec(lfjvl__qgur, {'bodo': bodo, 'np': np, 'numba': numba}, gzzqa__ovg)
    impl = gzzqa__ovg['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        kub__ikmwh, bij__sxkg = np.divmod(x, 1)
        if kub__ikmwh == 0:
            rjz__yxkj = -int(np.floor(np.log10(abs(bij__sxkg)))
                ) - 1 + precision
        else:
            rjz__yxkj = precision
        return np.around(x, rjz__yxkj)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        aqdnz__wdgo = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(aqdnz__wdgo)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        nhg__ojizv = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            fiksf__syfho = bins.copy()
            if right and include_lowest:
                fiksf__syfho[0] = fiksf__syfho[0] - nhg__ojizv
            qnfh__nug = bodo.libs.interval_arr_ext.init_interval_array(
                fiksf__syfho[:-1], fiksf__syfho[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(qnfh__nug,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        fiksf__syfho = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            fiksf__syfho[0] = fiksf__syfho[0] - 10.0 ** -precision
        qnfh__nug = bodo.libs.interval_arr_ext.init_interval_array(fiksf__syfho
            [:-1], fiksf__syfho[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(qnfh__nug, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        irq__mbdi = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        tpxf__dmro = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        yeqbi__wwxm = np.zeros(nbins, np.int64)
        for bfuho__etxot in range(len(irq__mbdi)):
            yeqbi__wwxm[tpxf__dmro[bfuho__etxot]] = irq__mbdi[bfuho__etxot]
        return yeqbi__wwxm
    return impl


def compute_bins(nbins, min_val, max_val):
    pass


@overload(compute_bins, no_unliteral=True)
def overload_compute_bins(nbins, min_val, max_val, right=True):

    def impl(nbins, min_val, max_val, right=True):
        if nbins < 1:
            raise ValueError('`bins` should be a positive integer.')
        min_val = min_val + 0.0
        max_val = max_val + 0.0
        if np.isinf(min_val) or np.isinf(max_val):
            raise ValueError(
                'cannot specify integer `bins` when input data contains infinity'
                )
        elif min_val == max_val:
            min_val -= 0.001 * abs(min_val) if min_val != 0 else 0.001
            max_val += 0.001 * abs(max_val) if max_val != 0 else 0.001
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
        else:
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
            tiq__cca = (max_val - min_val) * 0.001
            if right:
                bins[0] -= tiq__cca
            else:
                bins[-1] += tiq__cca
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    abe__jlau = dict(dropna=dropna)
    obdgq__bisy = dict(dropna=True)
    check_unsupported_args('Series.value_counts', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            'Series.value_counts(): normalize argument must be a constant boolean'
            )
    if not is_overload_constant_bool(sort):
        raise_bodo_error(
            'Series.value_counts(): sort argument must be a constant boolean')
    if not is_overload_bool(ascending):
        raise_bodo_error(
            'Series.value_counts(): ascending argument must be a constant boolean'
            )
    nlyof__wahna = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    lfjvl__qgur = 'def impl(\n'
    lfjvl__qgur += '    S,\n'
    lfjvl__qgur += '    normalize=False,\n'
    lfjvl__qgur += '    sort=True,\n'
    lfjvl__qgur += '    ascending=False,\n'
    lfjvl__qgur += '    bins=None,\n'
    lfjvl__qgur += '    dropna=True,\n'
    lfjvl__qgur += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    lfjvl__qgur += '):\n'
    lfjvl__qgur += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    lfjvl__qgur += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lfjvl__qgur += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if nlyof__wahna:
        lfjvl__qgur += '    right = True\n'
        lfjvl__qgur += _gen_bins_handling(bins, S.dtype)
        lfjvl__qgur += '    arr = get_bin_inds(bins, arr)\n'
    lfjvl__qgur += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    lfjvl__qgur += "        (arr,), index, ('$_bodo_col2_',)\n"
    lfjvl__qgur += '    )\n'
    lfjvl__qgur += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if nlyof__wahna:
        lfjvl__qgur += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        lfjvl__qgur += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        lfjvl__qgur += '    index = get_bin_labels(bins)\n'
    else:
        lfjvl__qgur += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        lfjvl__qgur += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        lfjvl__qgur += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        lfjvl__qgur += '    )\n'
        lfjvl__qgur += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    lfjvl__qgur += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        lfjvl__qgur += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        tkeec__hoacw = 'len(S)' if nlyof__wahna else 'count_arr.sum()'
        lfjvl__qgur += f'    res = res / float({tkeec__hoacw})\n'
    lfjvl__qgur += '    return res\n'
    gzzqa__ovg = {}
    exec(lfjvl__qgur, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, gzzqa__ovg)
    impl = gzzqa__ovg['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    lfjvl__qgur = ''
    if isinstance(bins, types.Integer):
        lfjvl__qgur += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        lfjvl__qgur += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            lfjvl__qgur += '    min_val = min_val.value\n'
            lfjvl__qgur += '    max_val = max_val.value\n'
        lfjvl__qgur += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            lfjvl__qgur += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        lfjvl__qgur += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return lfjvl__qgur


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    abe__jlau = dict(right=right, labels=labels, retbins=retbins, precision
        =precision, duplicates=duplicates, ordered=ordered)
    obdgq__bisy = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    lfjvl__qgur = 'def impl(\n'
    lfjvl__qgur += '    x,\n'
    lfjvl__qgur += '    bins,\n'
    lfjvl__qgur += '    right=True,\n'
    lfjvl__qgur += '    labels=None,\n'
    lfjvl__qgur += '    retbins=False,\n'
    lfjvl__qgur += '    precision=3,\n'
    lfjvl__qgur += '    include_lowest=False,\n'
    lfjvl__qgur += "    duplicates='raise',\n"
    lfjvl__qgur += '    ordered=True\n'
    lfjvl__qgur += '):\n'
    if isinstance(x, SeriesType):
        lfjvl__qgur += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        lfjvl__qgur += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        lfjvl__qgur += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        lfjvl__qgur += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    lfjvl__qgur += _gen_bins_handling(bins, x.dtype)
    lfjvl__qgur += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    lfjvl__qgur += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    lfjvl__qgur += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    lfjvl__qgur += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        lfjvl__qgur += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        lfjvl__qgur += '    return res\n'
    else:
        lfjvl__qgur += '    return out_arr\n'
    gzzqa__ovg = {}
    exec(lfjvl__qgur, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, gzzqa__ovg)
    impl = gzzqa__ovg['impl']
    return impl


def _get_q_list(q):
    return q


@overload(_get_q_list, no_unliteral=True)
def get_q_list_overload(q):
    if is_overload_int(q):
        return lambda q: np.linspace(0, 1, q + 1)
    return lambda q: q


@overload(pd.unique, inline='always', no_unliteral=True)
def overload_unique(values):
    if not is_series_type(values) and not (bodo.utils.utils.is_array_typ(
        values, False) and values.ndim == 1):
        raise BodoError(
            "pd.unique(): 'values' must be either a Series or a 1-d array")
    if is_series_type(values):

        def impl(values):
            arr = bodo.hiframes.pd_series_ext.get_series_data(values)
            return bodo.allgatherv(bodo.libs.array_kernels.unique(arr), False)
        return impl
    else:
        return lambda values: bodo.allgatherv(bodo.libs.array_kernels.
            unique(values), False)


@overload(pd.qcut, inline='always', no_unliteral=True)
def overload_qcut(x, q, labels=None, retbins=False, precision=3, duplicates
    ='raise'):
    abe__jlau = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    obdgq__bisy = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        xpb__wfbo = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, xpb__wfbo)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    abe__jlau = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    obdgq__bisy = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='GroupBy')
    if not is_overload_true(as_index):
        raise BodoError('as_index=False only valid with DataFrame')
    if is_overload_none(by) and is_overload_none(level):
        raise BodoError("You have to supply one of 'by' and 'level'")
    if not is_overload_none(by) and not is_overload_none(level):
        raise BodoError(
            "Series.groupby(): 'level' argument should be None if 'by' is not None"
            )
    if not is_overload_none(level):
        if not (is_overload_constant_int(level) and get_overload_const_int(
            level) == 0) or isinstance(S.index, bodo.hiframes.
            pd_multi_index_ext.MultiIndexType):
            raise BodoError(
                "Series.groupby(): MultiIndex case or 'level' other than 0 not supported yet"
                )

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            wllvm__blpr = bodo.utils.conversion.coerce_to_array(index)
            xkvyc__rsubr = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                wllvm__blpr, arr), index, (' ', ''))
            return xkvyc__rsubr.groupby(' ')['']
        return impl_index
    nfkm__jsdl = by
    if isinstance(by, SeriesType):
        nfkm__jsdl = by.data
    if isinstance(nfkm__jsdl, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        wllvm__blpr = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        xkvyc__rsubr = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            wllvm__blpr, arr), index, (' ', ''))
        return xkvyc__rsubr.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    abe__jlau = dict(verify_integrity=verify_integrity)
    obdgq__bisy = dict(verify_integrity=False)
    check_unsupported_args('Series.append', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_append,
        'Series.append()')
    if isinstance(to_append, SeriesType):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S, to_append), ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    if isinstance(to_append, types.BaseTuple):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S,) + to_append, ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    return (lambda S, to_append, ignore_index=False, verify_integrity=False:
        pd.concat([S] + to_append, ignore_index=ignore_index,
        verify_integrity=verify_integrity))


@overload_method(SeriesType, 'isin', inline='always', no_unliteral=True)
def overload_series_isin(S, values):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.isin()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(values,
        'Series.isin()')
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(S, values):
            sjdqm__emou = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            yeqbi__wwxm = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(yeqbi__wwxm, A, sjdqm__emou, False)
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        yeqbi__wwxm = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    abe__jlau = dict(interpolation=interpolation)
    obdgq__bisy = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            yeqbi__wwxm = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                index, name)
        return impl_list
    elif isinstance(q, (float, types.Number)) or is_overload_constant_int(q):

        def impl(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return bodo.libs.array_ops.array_op_quantile(arr, q)
        return impl
    else:
        raise BodoError(
            f'Series.quantile() q type must be float or iterable of floats only.'
            )


@overload_method(SeriesType, 'nunique', inline='always', no_unliteral=True)
def overload_series_nunique(S, dropna=True):
    if not is_overload_bool(dropna):
        raise BodoError('Series.nunique: dropna must be a boolean value')

    def impl(S, dropna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_kernels.nunique(arr, dropna)
    return impl


@overload_method(SeriesType, 'unique', inline='always', no_unliteral=True)
def overload_series_unique(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        qry__jdn = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(qry__jdn, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    abe__jlau = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    obdgq__bisy = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.describe()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)
        ) and not isinstance(S.data, IntegerArrayType):
        raise BodoError(f'describe() column input type {S.data} not supported.'
            )
    if S.data.dtype == bodo.datetime64ns:

        def impl_dt(S, percentiles=None, include=None, exclude=None,
            datetime_is_numeric=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
                array_ops.array_op_describe(arr), bodo.utils.conversion.
                convert_to_index(['count', 'mean', 'min', '25%', '50%',
                '75%', 'max']), name)
        return impl_dt

    def impl(S, percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.array_ops.
            array_op_describe(arr), bodo.utils.conversion.convert_to_index(
            ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']), name)
    return impl


@overload_method(SeriesType, 'memory_usage', inline='always', no_unliteral=True
    )
def overload_series_memory_usage(S, index=True, deep=False):
    if is_overload_true(index):

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            return arr.nbytes + index.nbytes
        return impl
    else:

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return arr.nbytes
        return impl


def binary_str_fillna_inplace_series_impl(is_binary=False):
    if is_binary:
        sjj__mpbg = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        sjj__mpbg = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    lfjvl__qgur = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {sjj__mpbg}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    bjdxf__cbpp = dict()
    exec(lfjvl__qgur, {'bodo': bodo, 'numba': numba}, bjdxf__cbpp)
    uhit__saos = bjdxf__cbpp['impl']
    return uhit__saos


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        sjj__mpbg = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        sjj__mpbg = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    lfjvl__qgur = 'def impl(S,\n'
    lfjvl__qgur += '     value=None,\n'
    lfjvl__qgur += '    method=None,\n'
    lfjvl__qgur += '    axis=None,\n'
    lfjvl__qgur += '    inplace=False,\n'
    lfjvl__qgur += '    limit=None,\n'
    lfjvl__qgur += '   downcast=None,\n'
    lfjvl__qgur += '):\n'
    lfjvl__qgur += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    lfjvl__qgur += '    n = len(in_arr)\n'
    lfjvl__qgur += f'    out_arr = {sjj__mpbg}(n, -1)\n'
    lfjvl__qgur += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    lfjvl__qgur += '        s = in_arr[j]\n'
    lfjvl__qgur += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    lfjvl__qgur += '            s = value\n'
    lfjvl__qgur += '        out_arr[j] = s\n'
    lfjvl__qgur += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    bjdxf__cbpp = dict()
    exec(lfjvl__qgur, {'bodo': bodo, 'numba': numba}, bjdxf__cbpp)
    uhit__saos = bjdxf__cbpp['impl']
    return uhit__saos


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
    usxhk__npbpo = bodo.hiframes.pd_series_ext.get_series_data(value)
    for bfuho__etxot in numba.parfors.parfor.internal_prange(len(hmpk__tkg)):
        s = hmpk__tkg[bfuho__etxot]
        if bodo.libs.array_kernels.isna(hmpk__tkg, bfuho__etxot
            ) and not bodo.libs.array_kernels.isna(usxhk__npbpo, bfuho__etxot):
            s = usxhk__npbpo[bfuho__etxot]
        hmpk__tkg[bfuho__etxot] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
    for bfuho__etxot in numba.parfors.parfor.internal_prange(len(hmpk__tkg)):
        s = hmpk__tkg[bfuho__etxot]
        if bodo.libs.array_kernels.isna(hmpk__tkg, bfuho__etxot):
            s = value
        hmpk__tkg[bfuho__etxot] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    usxhk__npbpo = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(hmpk__tkg)
    yeqbi__wwxm = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for hivtc__xjb in numba.parfors.parfor.internal_prange(n):
        s = hmpk__tkg[hivtc__xjb]
        if bodo.libs.array_kernels.isna(hmpk__tkg, hivtc__xjb
            ) and not bodo.libs.array_kernels.isna(usxhk__npbpo, hivtc__xjb):
            s = usxhk__npbpo[hivtc__xjb]
        yeqbi__wwxm[hivtc__xjb] = s
        if bodo.libs.array_kernels.isna(hmpk__tkg, hivtc__xjb
            ) and bodo.libs.array_kernels.isna(usxhk__npbpo, hivtc__xjb):
            bodo.libs.array_kernels.setna(yeqbi__wwxm, hivtc__xjb)
    return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    usxhk__npbpo = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(hmpk__tkg)
    yeqbi__wwxm = bodo.utils.utils.alloc_type(n, hmpk__tkg.dtype, (-1,))
    for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
        s = hmpk__tkg[bfuho__etxot]
        if bodo.libs.array_kernels.isna(hmpk__tkg, bfuho__etxot
            ) and not bodo.libs.array_kernels.isna(usxhk__npbpo, bfuho__etxot):
            s = usxhk__npbpo[bfuho__etxot]
        yeqbi__wwxm[bfuho__etxot] = s
    return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    abe__jlau = dict(limit=limit, downcast=downcast)
    obdgq__bisy = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    tnjnu__kvpum = not is_overload_none(value)
    zslvz__xuh = not is_overload_none(method)
    if tnjnu__kvpum and zslvz__xuh:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not tnjnu__kvpum and not zslvz__xuh:
        raise BodoError(
            "Series.fillna(): Must specify one of 'value' and 'method'.")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.fillna(): axis argument not supported')
    elif is_iterable_type(value) and not isinstance(value, SeriesType):
        raise BodoError('Series.fillna(): "value" parameter cannot be a list')
    elif is_var_size_item_array_type(S.data
        ) and not S.dtype == bodo.string_type:
        raise BodoError(
            f'Series.fillna() with inplace=True not supported for {S.dtype} values yet.'
            )
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "Series.fillna(): 'inplace' argument must be a constant boolean")
    if zslvz__xuh:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        epm__ooelw = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(epm__ooelw)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(epm__ooelw)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    pxq__qhpd = element_type(S.data)
    qjm__xspnf = None
    if tnjnu__kvpum:
        qjm__xspnf = element_type(types.unliteral(value))
    if qjm__xspnf and not can_replace(pxq__qhpd, qjm__xspnf):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {qjm__xspnf} with series type {pxq__qhpd}'
            )
    if is_overload_true(inplace):
        if S.dtype == bodo.string_type:
            if S.data == bodo.dict_str_arr_type:
                raise_bodo_error(
                    "Series.fillna(): 'inplace' not supported for dictionary-encoded string arrays yet."
                    )
            if is_overload_constant_str(value) and get_overload_const_str(value
                ) == '':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=False)
            return binary_str_fillna_inplace_impl(is_binary=False)
        if S.dtype == bodo.bytes_type:
            if is_overload_constant_bytes(value) and get_overload_const_bytes(
                value) == b'':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=True)
            return binary_str_fillna_inplace_impl(is_binary=True)
        else:
            if isinstance(value, SeriesType):
                return fillna_inplace_series_impl
            return fillna_inplace_impl
    else:
        vwqef__sejcf = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                usxhk__npbpo = bodo.hiframes.pd_series_ext.get_series_data(
                    value)
                n = len(hmpk__tkg)
                yeqbi__wwxm = bodo.utils.utils.alloc_type(n, vwqef__sejcf,
                    (-1,))
                for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(hmpk__tkg, bfuho__etxot
                        ) and bodo.libs.array_kernels.isna(usxhk__npbpo,
                        bfuho__etxot):
                        bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot
                            )
                        continue
                    if bodo.libs.array_kernels.isna(hmpk__tkg, bfuho__etxot):
                        yeqbi__wwxm[bfuho__etxot
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            usxhk__npbpo[bfuho__etxot])
                        continue
                    yeqbi__wwxm[bfuho__etxot
                        ] = bodo.utils.conversion.unbox_if_timestamp(hmpk__tkg
                        [bfuho__etxot])
                return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                    index, name)
            return fillna_series_impl
        if zslvz__xuh:
            mbya__voex = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(pxq__qhpd, (types.Integer, types.Float)
                ) and pxq__qhpd not in mbya__voex:
                raise BodoError(
                    f"Series.fillna(): series of type {pxq__qhpd} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                yeqbi__wwxm = bodo.libs.array_kernels.ffill_bfill_arr(hmpk__tkg
                    , method)
                return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(hmpk__tkg)
            yeqbi__wwxm = bodo.utils.utils.alloc_type(n, vwqef__sejcf, (-1,))
            for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(hmpk__tkg[
                    bfuho__etxot])
                if bodo.libs.array_kernels.isna(hmpk__tkg, bfuho__etxot):
                    s = value
                yeqbi__wwxm[bfuho__etxot] = s
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        uny__hrcr = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        abe__jlau = dict(limit=limit, downcast=downcast)
        obdgq__bisy = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', abe__jlau,
            obdgq__bisy, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        pxq__qhpd = element_type(S.data)
        mbya__voex = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(pxq__qhpd, (types.Integer, types.Float)
            ) and pxq__qhpd not in mbya__voex:
            raise BodoError(
                f'Series.{overload_name}(): series of type {pxq__qhpd} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            yeqbi__wwxm = bodo.libs.array_kernels.ffill_bfill_arr(hmpk__tkg,
                uny__hrcr)
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        qarnu__tswr = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            qarnu__tswr)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        hgo__fassw = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(hgo__fassw)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        hgo__fassw = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(hgo__fassw)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        hgo__fassw = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(hgo__fassw)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    abe__jlau = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    bemqn__chphy = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', abe__jlau, bemqn__chphy,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    pxq__qhpd = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        ukmfs__juko = element_type(to_replace.key_type)
        qjm__xspnf = element_type(to_replace.value_type)
    else:
        ukmfs__juko = element_type(to_replace)
        qjm__xspnf = element_type(value)
    yxmym__iypje = None
    if pxq__qhpd != types.unliteral(ukmfs__juko):
        if bodo.utils.typing.equality_always_false(pxq__qhpd, types.
            unliteral(ukmfs__juko)
            ) or not bodo.utils.typing.types_equality_exists(pxq__qhpd,
            ukmfs__juko):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(pxq__qhpd, (types.Float, types.Integer)
            ) or pxq__qhpd == np.bool_:
            yxmym__iypje = pxq__qhpd
    if not can_replace(pxq__qhpd, types.unliteral(qjm__xspnf)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    fggop__vivba = to_str_arr_if_dict_array(S.data)
    if isinstance(fggop__vivba, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(hmpk__tkg.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(hmpk__tkg)
        yeqbi__wwxm = bodo.utils.utils.alloc_type(n, fggop__vivba, (-1,))
        vrai__zgs = build_replace_dict(to_replace, value, yxmym__iypje)
        for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(hmpk__tkg, bfuho__etxot):
                bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot)
                continue
            s = hmpk__tkg[bfuho__etxot]
            if s in vrai__zgs:
                s = vrai__zgs[s]
            yeqbi__wwxm[bfuho__etxot] = s
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    lykt__sjl = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    yhej__era = is_iterable_type(to_replace)
    eqbkm__wssw = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    yxqyd__yxew = is_iterable_type(value)
    if lykt__sjl and eqbkm__wssw:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                vrai__zgs = {}
                vrai__zgs[key_dtype_conv(to_replace)] = value
                return vrai__zgs
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            vrai__zgs = {}
            vrai__zgs[to_replace] = value
            return vrai__zgs
        return impl
    if yhej__era and eqbkm__wssw:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                vrai__zgs = {}
                for pjhth__fndy in to_replace:
                    vrai__zgs[key_dtype_conv(pjhth__fndy)] = value
                return vrai__zgs
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            vrai__zgs = {}
            for pjhth__fndy in to_replace:
                vrai__zgs[pjhth__fndy] = value
            return vrai__zgs
        return impl
    if yhej__era and yxqyd__yxew:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                vrai__zgs = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for bfuho__etxot in range(len(to_replace)):
                    vrai__zgs[key_dtype_conv(to_replace[bfuho__etxot])
                        ] = value[bfuho__etxot]
                return vrai__zgs
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            vrai__zgs = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for bfuho__etxot in range(len(to_replace)):
                vrai__zgs[to_replace[bfuho__etxot]] = value[bfuho__etxot]
            return vrai__zgs
        return impl
    if isinstance(to_replace, numba.types.DictType) and is_overload_none(value
        ):
        return lambda to_replace, value, key_dtype_conv: to_replace
    raise BodoError(
        'Series.replace(): Not supported for types to_replace={} and value={}'
        .format(to_replace, value))


@overload_method(SeriesType, 'diff', inline='always', no_unliteral=True)
def overload_series_diff(S, periods=1):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.diff()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)):
        raise BodoError(
            f'Series.diff() column input type {S.data} not supported.')
    if not is_overload_int(periods):
        raise BodoError("Series.diff(): 'periods' input must be an integer.")
    if S.data == types.Array(bodo.datetime64ns, 1, 'C'):

        def impl_datetime(S, periods=1):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            yeqbi__wwxm = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        yeqbi__wwxm = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    abe__jlau = dict(ignore_index=ignore_index)
    onv__qzo = dict(ignore_index=False)
    check_unsupported_args('Series.explode', abe__jlau, onv__qzo,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pqy__gic = bodo.utils.conversion.index_to_array(index)
        yeqbi__wwxm, gnp__boa = bodo.libs.array_kernels.explode(arr, pqy__gic)
        ymg__upqp = bodo.utils.conversion.index_from_array(gnp__boa)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
            ymg__upqp, name)
    return impl


@overload(np.digitize, inline='always', no_unliteral=True)
def overload_series_np_digitize(x, bins, right=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.digitize()')
    if isinstance(x, SeriesType):

        def impl(x, bins, right=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(x)
            return np.digitize(arr, bins, right)
        return impl


@overload(np.argmax, inline='always', no_unliteral=True)
def argmax_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            jozrv__mlinb = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                jozrv__mlinb[bfuho__etxot] = np.argmax(a[bfuho__etxot])
            return jozrv__mlinb
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            ssdbn__gmd = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                ssdbn__gmd[bfuho__etxot] = np.argmin(a[bfuho__etxot])
            return ssdbn__gmd
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(a)
            return np.dot(arr, b)
        return impl
    if isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(b)
            return np.dot(a, arr)
        return impl


overload(np.dot, inline='always', no_unliteral=True)(overload_series_np_dot)
overload(operator.matmul, inline='always', no_unliteral=True)(
    overload_series_np_dot)


@overload_method(SeriesType, 'dropna', inline='always', no_unliteral=True)
def overload_series_dropna(S, axis=0, inplace=False, how=None):
    abe__jlau = dict(axis=axis, inplace=inplace, how=how)
    mhqcl__acrlx = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', abe__jlau, mhqcl__acrlx,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            dkh__drqi = S.notna().values
            pqy__gic = bodo.utils.conversion.extract_index_array(S)
            ymg__upqp = bodo.utils.conversion.convert_to_index(pqy__gic[
                dkh__drqi])
            yeqbi__wwxm = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(hmpk__tkg))
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                ymg__upqp, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pqy__gic = bodo.utils.conversion.extract_index_array(S)
            dkh__drqi = S.notna().values
            ymg__upqp = bodo.utils.conversion.convert_to_index(pqy__gic[
                dkh__drqi])
            yeqbi__wwxm = hmpk__tkg[dkh__drqi]
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                ymg__upqp, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    abe__jlau = dict(freq=freq, axis=axis, fill_value=fill_value)
    obdgq__bisy = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.shift()')
    if not is_supported_shift_array_type(S.data):
        raise BodoError(
            f"Series.shift(): Series input type '{S.data.dtype}' not supported yet."
            )
    if not is_overload_int(periods):
        raise BodoError("Series.shift(): 'periods' input must be an integer.")

    def impl(S, periods=1, freq=None, axis=0, fill_value=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        yeqbi__wwxm = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    abe__jlau = dict(fill_method=fill_method, limit=limit, freq=freq)
    obdgq__bisy = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not is_overload_int(periods):
        raise BodoError(
            'Series.pct_change(): periods argument must be an Integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.pct_change()')

    def impl(S, periods=1, fill_method='pad', limit=None, freq=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        yeqbi__wwxm = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


def create_series_mask_where_overload(func_name):

    def overload_series_mask_where(S, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
            f'Series.{func_name}()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
            f'Series.{func_name}()')
        _validate_arguments_mask_where(f'Series.{func_name}', S, cond,
            other, inplace, axis, level, errors, try_cast)
        if is_overload_constant_nan(other):
            jfc__xflwe = 'None'
        else:
            jfc__xflwe = 'other'
        lfjvl__qgur = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            lfjvl__qgur += '  cond = ~cond\n'
        lfjvl__qgur += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        lfjvl__qgur += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        lfjvl__qgur += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        lfjvl__qgur += f"""  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {jfc__xflwe})
"""
        lfjvl__qgur += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        gzzqa__ovg = {}
        exec(lfjvl__qgur, {'bodo': bodo, 'np': np}, gzzqa__ovg)
        impl = gzzqa__ovg['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        qarnu__tswr = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(qarnu__tswr)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    abe__jlau = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    obdgq__bisy = dict(inplace=False, level=None, errors='raise', try_cast=
        False)
    check_unsupported_args(f'{func_name}', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if isinstance(other, SeriesType):
        _validate_self_other_mask_where(func_name, S.data, other.data)
    else:
        _validate_self_other_mask_where(func_name, S.data, other)
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        cond.ndim == 1 and cond.dtype == types.bool_):
        raise BodoError(
            f"{func_name}() 'cond' argument must be a Series or 1-dim array of booleans"
            )


def _validate_self_other_mask_where(func_name, arr, other, max_ndim=1,
    is_default=False):
    if not (isinstance(arr, types.Array) or isinstance(arr,
        BooleanArrayType) or isinstance(arr, IntegerArrayType) or bodo.
        utils.utils.is_array_typ(arr, False) and arr.dtype in [bodo.
        string_type, bodo.bytes_type] or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type not in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.pd_timestamp_type, bodo.
        pd_timedelta_type]):
        raise BodoError(
            f'{func_name}() Series data with type {arr} not yet supported')
    axuo__sejn = is_overload_constant_nan(other)
    if not (is_default or axuo__sejn or is_scalar_type(other) or isinstance
        (other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
        isinstance(other, SeriesType) and (isinstance(arr, types.Array) or 
        arr.dtype in [bodo.string_type, bodo.bytes_type]) or 
        is_str_arr_type(other) and (arr.dtype == bodo.string_type or 
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type ==
        bodo.string_type) or isinstance(other, BinaryArrayType) and (arr.
        dtype == bodo.bytes_type or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type == bodo.bytes_type) or
        (not (isinstance(other, (StringArrayType, BinaryArrayType)) or 
        other == bodo.dict_str_arr_type) and (isinstance(arr.dtype, types.
        Integer) and (bodo.utils.utils.is_array_typ(other) and isinstance(
        other.dtype, types.Integer) or is_series_type(other) and isinstance
        (other.dtype, types.Integer))) or (bodo.utils.utils.is_array_typ(
        other) and arr.dtype == other.dtype or is_series_type(other) and 
        arr.dtype == other.dtype)) and (isinstance(arr, BooleanArrayType) or
        isinstance(arr, IntegerArrayType))):
        raise BodoError(
            f"{func_name}() 'other' must be a scalar, non-categorical series, 1-dim numpy array or StringArray with a matching type for Series."
            )
    if not is_default:
        if isinstance(arr.dtype, bodo.PDCategoricalDtype):
            njz__sbidc = arr.dtype.elem_type
        else:
            njz__sbidc = arr.dtype
        if is_iterable_type(other):
            dnozx__lzu = other.dtype
        elif axuo__sejn:
            dnozx__lzu = types.float64
        else:
            dnozx__lzu = types.unliteral(other)
        if not axuo__sejn and not is_common_scalar_dtype([njz__sbidc,
            dnozx__lzu]):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        abe__jlau = dict(level=level, axis=axis)
        obdgq__bisy = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), abe__jlau,
            obdgq__bisy, package_name='pandas', module_name='Series')
        pkc__aziii = other == string_type or is_overload_constant_str(other)
        jzl__gfei = is_iterable_type(other) and other.dtype == string_type
        oaxon__qxpth = S.dtype == string_type and (op == operator.add and (
            pkc__aziii or jzl__gfei) or op == operator.mul and isinstance(
            other, types.Integer))
        zwez__tabb = S.dtype == bodo.timedelta64ns
        ada__pgatn = S.dtype == bodo.datetime64ns
        xbl__bzw = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        exor__honl = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        dkt__mqdnl = zwez__tabb and (xbl__bzw or exor__honl
            ) or ada__pgatn and xbl__bzw
        dkt__mqdnl = dkt__mqdnl and op == operator.add
        if not (isinstance(S.dtype, types.Number) or oaxon__qxpth or dkt__mqdnl
            ):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        ugtbo__tlogn = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            fggop__vivba = ugtbo__tlogn.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and fggop__vivba == types.Array(types.bool_, 1, 'C'):
                fggop__vivba = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                yeqbi__wwxm = bodo.utils.utils.alloc_type(n, fggop__vivba,
                    (-1,))
                for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                    bhna__gpdot = bodo.libs.array_kernels.isna(arr,
                        bfuho__etxot)
                    if bhna__gpdot:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(yeqbi__wwxm,
                                bfuho__etxot)
                        else:
                            yeqbi__wwxm[bfuho__etxot] = op(fill_value, other)
                    else:
                        yeqbi__wwxm[bfuho__etxot] = op(arr[bfuho__etxot], other
                            )
                return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        fggop__vivba = ugtbo__tlogn.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, IntegerArrayType
            ) and fggop__vivba == types.Array(types.bool_, 1, 'C'):
            fggop__vivba = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ekjmf__wda = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            yeqbi__wwxm = bodo.utils.utils.alloc_type(n, fggop__vivba, (-1,))
            for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                bhna__gpdot = bodo.libs.array_kernels.isna(arr, bfuho__etxot)
                qii__neuq = bodo.libs.array_kernels.isna(ekjmf__wda,
                    bfuho__etxot)
                if bhna__gpdot and qii__neuq:
                    bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot)
                elif bhna__gpdot:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot
                            )
                    else:
                        yeqbi__wwxm[bfuho__etxot] = op(fill_value,
                            ekjmf__wda[bfuho__etxot])
                elif qii__neuq:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot
                            )
                    else:
                        yeqbi__wwxm[bfuho__etxot] = op(arr[bfuho__etxot],
                            fill_value)
                else:
                    yeqbi__wwxm[bfuho__etxot] = op(arr[bfuho__etxot],
                        ekjmf__wda[bfuho__etxot])
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                index, name)
        return impl
    return overload_series_explicit_binary_op


def create_explicit_binary_reverse_op_overload(op):

    def overload_series_explicit_binary_reverse_op(S, other, level=None,
        fill_value=None, axis=0):
        if not is_overload_none(level):
            raise BodoError('level argument not supported')
        if not is_overload_zero(axis):
            raise BodoError('axis argument not supported')
        if not isinstance(S.dtype, types.Number):
            raise BodoError('only numeric values supported')
        ugtbo__tlogn = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            fggop__vivba = ugtbo__tlogn.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and fggop__vivba == types.Array(types.bool_, 1, 'C'):
                fggop__vivba = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                yeqbi__wwxm = bodo.utils.utils.alloc_type(n, fggop__vivba, None
                    )
                for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                    bhna__gpdot = bodo.libs.array_kernels.isna(arr,
                        bfuho__etxot)
                    if bhna__gpdot:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(yeqbi__wwxm,
                                bfuho__etxot)
                        else:
                            yeqbi__wwxm[bfuho__etxot] = op(other, fill_value)
                    else:
                        yeqbi__wwxm[bfuho__etxot] = op(other, arr[bfuho__etxot]
                            )
                return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        fggop__vivba = ugtbo__tlogn.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, IntegerArrayType
            ) and fggop__vivba == types.Array(types.bool_, 1, 'C'):
            fggop__vivba = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ekjmf__wda = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            yeqbi__wwxm = bodo.utils.utils.alloc_type(n, fggop__vivba, None)
            for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                bhna__gpdot = bodo.libs.array_kernels.isna(arr, bfuho__etxot)
                qii__neuq = bodo.libs.array_kernels.isna(ekjmf__wda,
                    bfuho__etxot)
                yeqbi__wwxm[bfuho__etxot] = op(ekjmf__wda[bfuho__etxot],
                    arr[bfuho__etxot])
                if bhna__gpdot and qii__neuq:
                    bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot)
                elif bhna__gpdot:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot
                            )
                    else:
                        yeqbi__wwxm[bfuho__etxot] = op(ekjmf__wda[
                            bfuho__etxot], fill_value)
                elif qii__neuq:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot
                            )
                    else:
                        yeqbi__wwxm[bfuho__etxot] = op(fill_value, arr[
                            bfuho__etxot])
                else:
                    yeqbi__wwxm[bfuho__etxot] = op(ekjmf__wda[bfuho__etxot],
                        arr[bfuho__etxot])
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                index, name)
        return impl
    return overload_series_explicit_binary_reverse_op


explicit_binop_funcs_two_ways = {operator.add: {'add'}, operator.sub: {
    'sub'}, operator.mul: {'mul'}, operator.truediv: {'div', 'truediv'},
    operator.floordiv: {'floordiv'}, operator.mod: {'mod'}, operator.pow: {
    'pow'}}
explicit_binop_funcs_single = {operator.lt: 'lt', operator.gt: 'gt',
    operator.le: 'le', operator.ge: 'ge', operator.ne: 'ne', operator.eq: 'eq'}
explicit_binop_funcs = set()
split_logical_binops_funcs = [operator.or_, operator.and_]


def _install_explicit_binary_ops():
    for op, com__dokf in explicit_binop_funcs_two_ways.items():
        for name in com__dokf:
            qarnu__tswr = create_explicit_binary_op_overload(op)
            iqmnu__iwn = create_explicit_binary_reverse_op_overload(op)
            rkz__pnlcx = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(qarnu__tswr)
            overload_method(SeriesType, rkz__pnlcx, no_unliteral=True)(
                iqmnu__iwn)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        qarnu__tswr = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(qarnu__tswr)
        explicit_binop_funcs.add(name)


_install_explicit_binary_ops()


def create_binary_op_overload(op):

    def overload_series_binary_op(lhs, rhs):
        if (isinstance(lhs, SeriesType) and isinstance(rhs, SeriesType) and
            lhs.dtype == bodo.datetime64ns and rhs.dtype == bodo.
            datetime64ns and op == operator.sub):

            def impl_dt64(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                ixmm__bfkrs = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                yeqbi__wwxm = dt64_arr_sub(arr, ixmm__bfkrs)
                return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                    index, name)
            return impl_dt64
        if op in [operator.add, operator.sub] and isinstance(lhs, SeriesType
            ) and lhs.dtype == bodo.datetime64ns and is_offsets_type(rhs):

            def impl_offsets(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                yeqbi__wwxm = np.empty(n, np.dtype('datetime64[ns]'))
                for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, bfuho__etxot):
                        bodo.libs.array_kernels.setna(yeqbi__wwxm, bfuho__etxot
                            )
                        continue
                    sudji__aubic = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[bfuho__etxot]))
                    gpc__rqfu = op(sudji__aubic, rhs)
                    yeqbi__wwxm[bfuho__etxot
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gpc__rqfu.value)
                return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                    index, name)
            return impl_offsets
        if op == operator.add and is_offsets_type(lhs) and isinstance(rhs,
            SeriesType) and rhs.dtype == bodo.datetime64ns:

            def impl(lhs, rhs):
                return op(rhs, lhs)
            return impl
        if isinstance(lhs, SeriesType):
            if lhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                    ixmm__bfkrs = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    yeqbi__wwxm = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(ixmm__bfkrs))
                    return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                ixmm__bfkrs = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                yeqbi__wwxm = op(arr, ixmm__bfkrs)
                return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    lixp__phc = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    yeqbi__wwxm = op(bodo.utils.conversion.
                        unbox_if_timestamp(lixp__phc), arr)
                    return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                lixp__phc = bodo.utils.conversion.get_array_if_series_or_index(
                    lhs)
                yeqbi__wwxm = op(lixp__phc, arr)
                return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        qarnu__tswr = create_binary_op_overload(op)
        overload(op)(qarnu__tswr)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    ogvwq__nra = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, ogvwq__nra)
        for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, bfuho__etxot
                ) or bodo.libs.array_kernels.isna(arg2, bfuho__etxot):
                bodo.libs.array_kernels.setna(S, bfuho__etxot)
                continue
            S[bfuho__etxot
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                bfuho__etxot]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[bfuho__etxot]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                ekjmf__wda = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, ekjmf__wda)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        qarnu__tswr = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(qarnu__tswr)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                yeqbi__wwxm = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        qarnu__tswr = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(qarnu__tswr)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    yeqbi__wwxm = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                        index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    ekjmf__wda = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    yeqbi__wwxm = ufunc(arr, ekjmf__wda)
                    return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    ekjmf__wda = bodo.hiframes.pd_series_ext.get_series_data(S2
                        )
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    yeqbi__wwxm = ufunc(arr, ekjmf__wda)
                    return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        qarnu__tswr = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(qarnu__tswr)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        gzl__iwpm = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),))
        ieeje__temb = np.arange(n),
        bodo.libs.timsort.sort(gzl__iwpm, 0, n, ieeje__temb)
        return ieeje__temb[0]
    return impl


@overload(pd.to_numeric, inline='always', no_unliteral=True)
def overload_to_numeric(arg_a, errors='raise', downcast=None):
    if not is_overload_none(downcast) and not (is_overload_constant_str(
        downcast) and get_overload_const_str(downcast) in ('integer',
        'signed', 'unsigned', 'float')):
        raise BodoError(
            'pd.to_numeric(): invalid downcasting method provided {}'.
            format(downcast))
    out_dtype = types.float64
    if not is_overload_none(downcast):
        vvdhh__ojjh = get_overload_const_str(downcast)
        if vvdhh__ojjh in ('integer', 'signed'):
            out_dtype = types.int64
        elif vvdhh__ojjh == 'unsigned':
            out_dtype = types.uint64
        else:
            assert vvdhh__ojjh == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            hmpk__tkg = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            yeqbi__wwxm = pd.to_numeric(hmpk__tkg, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            tqg__geor = np.empty(n, np.float64)
            for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, bfuho__etxot):
                    bodo.libs.array_kernels.setna(tqg__geor, bfuho__etxot)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(tqg__geor,
                        bfuho__etxot, arg_a, bfuho__etxot)
            return tqg__geor
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            tqg__geor = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, bfuho__etxot):
                    bodo.libs.array_kernels.setna(tqg__geor, bfuho__etxot)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(tqg__geor,
                        bfuho__etxot, arg_a, bfuho__etxot)
            return tqg__geor
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        rfd__tvpcl = if_series_to_array_type(args[0])
        if isinstance(rfd__tvpcl, types.Array) and isinstance(rfd__tvpcl.
            dtype, types.Integer):
            rfd__tvpcl = types.Array(types.float64, 1, 'C')
        return rfd__tvpcl(*args)


def where_impl_one_arg(c):
    return np.where(c)


@overload(where_impl_one_arg, no_unliteral=True)
def overload_where_unsupported_one_arg(condition):
    if isinstance(condition, SeriesType) or bodo.utils.utils.is_array_typ(
        condition, False):
        return lambda condition: np.where(condition)


def overload_np_where_one_arg(condition):
    if isinstance(condition, SeriesType):

        def impl_series(condition):
            condition = bodo.hiframes.pd_series_ext.get_series_data(condition)
            return bodo.libs.array_kernels.nonzero(condition)
        return impl_series
    elif bodo.utils.utils.is_array_typ(condition, False):

        def impl(condition):
            return bodo.libs.array_kernels.nonzero(condition)
        return impl


overload(np.where, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)
overload(where_impl_one_arg, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)


def where_impl(c, x, y):
    return np.where(c, x, y)


@overload(where_impl, no_unliteral=True)
def overload_where_unsupported(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return lambda condition, x, y: np.where(condition, x, y)


@overload(where_impl, no_unliteral=True)
@overload(np.where, no_unliteral=True)
def overload_np_where(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return
    assert condition.dtype == types.bool_, 'invalid condition dtype'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.where()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(y,
        'numpy.where()')
    dub__jsxvi = bodo.utils.utils.is_array_typ(x, True)
    eyzxw__ructc = bodo.utils.utils.is_array_typ(y, True)
    lfjvl__qgur = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        lfjvl__qgur += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if dub__jsxvi and not bodo.utils.utils.is_array_typ(x, False):
        lfjvl__qgur += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if eyzxw__ructc and not bodo.utils.utils.is_array_typ(y, False):
        lfjvl__qgur += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    lfjvl__qgur += '  n = len(condition)\n'
    dwt__xhbe = x.dtype if dub__jsxvi else types.unliteral(x)
    ncov__nzjw = y.dtype if eyzxw__ructc else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        dwt__xhbe = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        ncov__nzjw = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    cvgxx__rpbc = get_data(x)
    ytmpr__soay = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(ieeje__temb) for
        ieeje__temb in [cvgxx__rpbc, ytmpr__soay])
    if ytmpr__soay == types.none:
        if isinstance(dwt__xhbe, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif cvgxx__rpbc == ytmpr__soay and not is_nullable:
        out_dtype = dtype_to_array_type(dwt__xhbe)
    elif dwt__xhbe == string_type or ncov__nzjw == string_type:
        out_dtype = bodo.string_array_type
    elif cvgxx__rpbc == bytes_type or (dub__jsxvi and dwt__xhbe == bytes_type
        ) and (ytmpr__soay == bytes_type or eyzxw__ructc and ncov__nzjw ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(dwt__xhbe, bodo.PDCategoricalDtype):
        out_dtype = None
    elif dwt__xhbe in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(dwt__xhbe, 1, 'C')
    elif ncov__nzjw in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(ncov__nzjw, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(dwt__xhbe), numba.np.numpy_support.
            as_dtype(ncov__nzjw)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(dwt__xhbe, bodo.PDCategoricalDtype):
        eac__vfzj = 'x'
    else:
        eac__vfzj = 'out_dtype'
    lfjvl__qgur += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {eac__vfzj}, (-1,))\n')
    if isinstance(dwt__xhbe, bodo.PDCategoricalDtype):
        lfjvl__qgur += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        lfjvl__qgur += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    lfjvl__qgur += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    lfjvl__qgur += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if dub__jsxvi:
        lfjvl__qgur += '      if bodo.libs.array_kernels.isna(x, j):\n'
        lfjvl__qgur += '        setna(out_arr, j)\n'
        lfjvl__qgur += '        continue\n'
    if isinstance(dwt__xhbe, bodo.PDCategoricalDtype):
        lfjvl__qgur += '      out_codes[j] = x_codes[j]\n'
    else:
        lfjvl__qgur += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if dub__jsxvi else 'x'))
    lfjvl__qgur += '    else:\n'
    if eyzxw__ructc:
        lfjvl__qgur += '      if bodo.libs.array_kernels.isna(y, j):\n'
        lfjvl__qgur += '        setna(out_arr, j)\n'
        lfjvl__qgur += '        continue\n'
    if ytmpr__soay == types.none:
        if isinstance(dwt__xhbe, bodo.PDCategoricalDtype):
            lfjvl__qgur += '      out_codes[j] = -1\n'
        else:
            lfjvl__qgur += '      setna(out_arr, j)\n'
    else:
        lfjvl__qgur += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if eyzxw__ructc else 'y'))
    lfjvl__qgur += '  return out_arr\n'
    gzzqa__ovg = {}
    exec(lfjvl__qgur, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, gzzqa__ovg)
    gxpnh__qjq = gzzqa__ovg['_impl']
    return gxpnh__qjq


def _verify_np_select_arg_typs(condlist, choicelist, default):
    if isinstance(condlist, (types.List, types.UniTuple)):
        if not (bodo.utils.utils.is_np_array_typ(condlist.dtype) and 
            condlist.dtype.dtype == types.bool_):
            raise BodoError(
                "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
                )
    else:
        raise BodoError(
            "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
            )
    if not isinstance(choicelist, (types.List, types.UniTuple, types.BaseTuple)
        ):
        raise BodoError(
            "np.select(): 'choicelist' argument must be list or tuple type")
    if isinstance(choicelist, (types.List, types.UniTuple)):
        cbx__bfm = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(cbx__bfm, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(cbx__bfm):
            nvd__dbmuc = cbx__bfm.data.dtype
        else:
            nvd__dbmuc = cbx__bfm.dtype
        if isinstance(nvd__dbmuc, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        hgoe__typz = cbx__bfm
    else:
        amuld__vwkni = []
        for cbx__bfm in choicelist:
            if not bodo.utils.utils.is_array_typ(cbx__bfm, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(cbx__bfm):
                nvd__dbmuc = cbx__bfm.data.dtype
            else:
                nvd__dbmuc = cbx__bfm.dtype
            if isinstance(nvd__dbmuc, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            amuld__vwkni.append(nvd__dbmuc)
        if not is_common_scalar_dtype(amuld__vwkni):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        hgoe__typz = choicelist[0]
    if is_series_type(hgoe__typz):
        hgoe__typz = hgoe__typz.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, hgoe__typz.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(hgoe__typz, types.Array) or isinstance(hgoe__typz,
        BooleanArrayType) or isinstance(hgoe__typz, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(hgoe__typz, False) and hgoe__typz.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {hgoe__typz} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    eut__miwzy = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        disac__ilmtk = choicelist.dtype
    else:
        mdk__gbpws = False
        amuld__vwkni = []
        for cbx__bfm in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(cbx__bfm,
                'numpy.select()')
            if is_nullable_type(cbx__bfm):
                mdk__gbpws = True
            if is_series_type(cbx__bfm):
                nvd__dbmuc = cbx__bfm.data.dtype
            else:
                nvd__dbmuc = cbx__bfm.dtype
            if isinstance(nvd__dbmuc, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            amuld__vwkni.append(nvd__dbmuc)
        zlnvh__hwak, dwqp__mrpo = get_common_scalar_dtype(amuld__vwkni)
        if not dwqp__mrpo:
            raise BodoError('Internal error in overload_np_select')
        sug__inui = dtype_to_array_type(zlnvh__hwak)
        if mdk__gbpws:
            sug__inui = to_nullable_type(sug__inui)
        disac__ilmtk = sug__inui
    if isinstance(disac__ilmtk, SeriesType):
        disac__ilmtk = disac__ilmtk.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        brzfx__dil = True
    else:
        brzfx__dil = False
    neki__vcq = False
    dprtn__dbv = False
    if brzfx__dil:
        if isinstance(disac__ilmtk.dtype, types.Number):
            pass
        elif disac__ilmtk.dtype == types.bool_:
            dprtn__dbv = True
        else:
            neki__vcq = True
            disac__ilmtk = to_nullable_type(disac__ilmtk)
    elif default == types.none or is_overload_constant_nan(default):
        neki__vcq = True
        disac__ilmtk = to_nullable_type(disac__ilmtk)
    lfjvl__qgur = 'def np_select_impl(condlist, choicelist, default=0):\n'
    lfjvl__qgur += '  if len(condlist) != len(choicelist):\n'
    lfjvl__qgur += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    lfjvl__qgur += '  output_len = len(choicelist[0])\n'
    lfjvl__qgur += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    lfjvl__qgur += '  for i in range(output_len):\n'
    if neki__vcq:
        lfjvl__qgur += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif dprtn__dbv:
        lfjvl__qgur += '    out[i] = False\n'
    else:
        lfjvl__qgur += '    out[i] = default\n'
    if eut__miwzy:
        lfjvl__qgur += '  for i in range(len(condlist) - 1, -1, -1):\n'
        lfjvl__qgur += '    cond = condlist[i]\n'
        lfjvl__qgur += '    choice = choicelist[i]\n'
        lfjvl__qgur += '    out = np.where(cond, choice, out)\n'
    else:
        for bfuho__etxot in range(len(choicelist) - 1, -1, -1):
            lfjvl__qgur += f'  cond = condlist[{bfuho__etxot}]\n'
            lfjvl__qgur += f'  choice = choicelist[{bfuho__etxot}]\n'
            lfjvl__qgur += f'  out = np.where(cond, choice, out)\n'
    lfjvl__qgur += '  return out'
    gzzqa__ovg = dict()
    exec(lfjvl__qgur, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': disac__ilmtk}, gzzqa__ovg)
    impl = gzzqa__ovg['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        yeqbi__wwxm = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    abe__jlau = dict(subset=subset, keep=keep, inplace=inplace)
    obdgq__bisy = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        rile__xoly = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (rile__xoly,), pqy__gic = bodo.libs.array_kernels.drop_duplicates((
            rile__xoly,), index, 1)
        index = bodo.utils.conversion.index_from_array(pqy__gic)
        return bodo.hiframes.pd_series_ext.init_series(rile__xoly, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    deto__uizsy = element_type(S.data)
    if not is_common_scalar_dtype([deto__uizsy, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([deto__uizsy, right]):
        raise_bodo_error(
            "Series.between(): 'right' must be compariable with the Series data"
            )
    if not is_overload_constant_str(inclusive) or get_overload_const_str(
        inclusive) not in ('both', 'neither'):
        raise_bodo_error(
            "Series.between(): 'inclusive' must be a constant string and one of ('both', 'neither')"
            )

    def impl(S, left, right, inclusive='both'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        yeqbi__wwxm = np.empty(n, np.bool_)
        for bfuho__etxot in numba.parfors.parfor.internal_prange(n):
            kiyjo__rzagr = bodo.utils.conversion.box_if_dt64(arr[bfuho__etxot])
            if inclusive == 'both':
                yeqbi__wwxm[bfuho__etxot
                    ] = kiyjo__rzagr <= right and kiyjo__rzagr >= left
            else:
                yeqbi__wwxm[bfuho__etxot
                    ] = kiyjo__rzagr < right and kiyjo__rzagr > left
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm, index, name
            )
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    abe__jlau = dict(axis=axis)
    obdgq__bisy = dict(axis=None)
    check_unsupported_args('Series.repeat', abe__jlau, obdgq__bisy,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.repeat()')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Series.repeat(): 'repeats' should be an integer or array of integers"
            )
    if isinstance(repeats, types.Integer):

        def impl_int(S, repeats, axis=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pqy__gic = bodo.utils.conversion.index_to_array(index)
            yeqbi__wwxm = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            gnp__boa = bodo.libs.array_kernels.repeat_kernel(pqy__gic, repeats)
            ymg__upqp = bodo.utils.conversion.index_from_array(gnp__boa)
            return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
                ymg__upqp, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pqy__gic = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        yeqbi__wwxm = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        gnp__boa = bodo.libs.array_kernels.repeat_kernel(pqy__gic, repeats)
        ymg__upqp = bodo.utils.conversion.index_from_array(gnp__boa)
        return bodo.hiframes.pd_series_ext.init_series(yeqbi__wwxm,
            ymg__upqp, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        ieeje__temb = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(ieeje__temb)
        ahe__jucp = {}
        for bfuho__etxot in range(n):
            kiyjo__rzagr = bodo.utils.conversion.box_if_dt64(ieeje__temb[
                bfuho__etxot])
            ahe__jucp[index[bfuho__etxot]] = kiyjo__rzagr
        return ahe__jucp
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    epm__ooelw = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            lazt__kaskc = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(epm__ooelw)
    elif is_literal_type(name):
        lazt__kaskc = get_literal_value(name)
    else:
        raise_bodo_error(epm__ooelw)
    lazt__kaskc = 0 if lazt__kaskc is None else lazt__kaskc

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (lazt__kaskc,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
