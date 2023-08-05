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
            hyo__simwi = bodo.hiframes.pd_series_ext.get_series_data(s)
            tbkgs__bucng = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                hyo__simwi)
            return tbkgs__bucng
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
            lkod__rdqsf = list()
            for lhnw__ryuk in range(len(S)):
                lkod__rdqsf.append(S.iat[lhnw__ryuk])
            return lkod__rdqsf
        return impl_float

    def impl(S):
        lkod__rdqsf = list()
        for lhnw__ryuk in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, lhnw__ryuk):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            lkod__rdqsf.append(S.iat[lhnw__ryuk])
        return lkod__rdqsf
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    vfux__wdfe = dict(dtype=dtype, copy=copy, na_value=na_value)
    vouw__wvnw = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    vfux__wdfe = dict(name=name, inplace=inplace)
    vouw__wvnw = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', vfux__wdfe, vouw__wvnw,
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
    jwho__chsk = get_name_literal(S.index.name_typ, True, series_name)
    columns = [jwho__chsk, series_name]
    rzqff__jutx = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    rzqff__jutx += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    rzqff__jutx += """    index = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S))
"""
    rzqff__jutx += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    rzqff__jutx += '    col_var = {}\n'.format(gen_const_tup(columns))
    rzqff__jutx += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe((index, arr), df_index, col_var)
"""
    qcurl__owbzg = {}
    exec(rzqff__jutx, {'bodo': bodo}, qcurl__owbzg)
    hugts__mkjrt = qcurl__owbzg['_impl']
    return hugts__mkjrt


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ufvss__jolvb = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
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
        ufvss__jolvb = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[lhnw__ryuk]):
                bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
            else:
                ufvss__jolvb[lhnw__ryuk] = np.round(arr[lhnw__ryuk], decimals)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    vfux__wdfe = dict(level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    vouw__wvnw = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        myz__ghvf = 0
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(A)):
            shgaa__wjvzm = 0
            if not bodo.libs.array_kernels.isna(A, lhnw__ryuk):
                shgaa__wjvzm = int(A[lhnw__ryuk])
            myz__ghvf += shgaa__wjvzm
        return myz__ghvf != 0
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
        ynlq__skmq = bodo.hiframes.pd_series_ext.get_series_data(S)
        zmhax__wxps = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        myz__ghvf = 0
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(ynlq__skmq)
            ):
            shgaa__wjvzm = 0
            aykpx__hxt = bodo.libs.array_kernels.isna(ynlq__skmq, lhnw__ryuk)
            oafz__iju = bodo.libs.array_kernels.isna(zmhax__wxps, lhnw__ryuk)
            if aykpx__hxt and not oafz__iju or not aykpx__hxt and oafz__iju:
                shgaa__wjvzm = 1
            elif not aykpx__hxt:
                if ynlq__skmq[lhnw__ryuk] != zmhax__wxps[lhnw__ryuk]:
                    shgaa__wjvzm = 1
            myz__ghvf += shgaa__wjvzm
        return myz__ghvf == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    vfux__wdfe = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    vouw__wvnw = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        myz__ghvf = 0
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(A)):
            shgaa__wjvzm = 0
            if not bodo.libs.array_kernels.isna(A, lhnw__ryuk):
                shgaa__wjvzm = int(not A[lhnw__ryuk])
            myz__ghvf += shgaa__wjvzm
        return myz__ghvf == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    vfux__wdfe = dict(level=level)
    vouw__wvnw = dict(level=None)
    check_unsupported_args('Series.mad', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    vilis__nlnn = types.float64
    yvrop__lbo = types.float64
    if S.dtype == types.float32:
        vilis__nlnn = types.float32
        yvrop__lbo = types.float32
    raov__qpv = vilis__nlnn(0)
    juktd__gehw = yvrop__lbo(0)
    szhid__wsb = yvrop__lbo(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        pslpx__ppb = raov__qpv
        myz__ghvf = juktd__gehw
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(A)):
            shgaa__wjvzm = raov__qpv
            wszhn__zahge = juktd__gehw
            if not bodo.libs.array_kernels.isna(A, lhnw__ryuk) or not skipna:
                shgaa__wjvzm = A[lhnw__ryuk]
                wszhn__zahge = szhid__wsb
            pslpx__ppb += shgaa__wjvzm
            myz__ghvf += wszhn__zahge
        bym__xssix = bodo.hiframes.series_kernels._mean_handle_nan(pslpx__ppb,
            myz__ghvf)
        iufpa__foc = raov__qpv
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(A)):
            shgaa__wjvzm = raov__qpv
            if not bodo.libs.array_kernels.isna(A, lhnw__ryuk) or not skipna:
                shgaa__wjvzm = abs(A[lhnw__ryuk] - bym__xssix)
            iufpa__foc += shgaa__wjvzm
        phdcp__iufra = bodo.hiframes.series_kernels._mean_handle_nan(iufpa__foc
            , myz__ghvf)
        return phdcp__iufra
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    vfux__wdfe = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', vfux__wdfe, vouw__wvnw,
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
        ijy__bwcqm = 0
        vbmdu__deqz = 0
        myz__ghvf = 0
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(A)):
            shgaa__wjvzm = 0
            wszhn__zahge = 0
            if not bodo.libs.array_kernels.isna(A, lhnw__ryuk) or not skipna:
                shgaa__wjvzm = A[lhnw__ryuk]
                wszhn__zahge = 1
            ijy__bwcqm += shgaa__wjvzm
            vbmdu__deqz += shgaa__wjvzm * shgaa__wjvzm
            myz__ghvf += wszhn__zahge
        uzj__ukuhn = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            ijy__bwcqm, vbmdu__deqz, myz__ghvf, ddof)
        vkxk__rtudp = bodo.hiframes.series_kernels._sem_handle_nan(uzj__ukuhn,
            myz__ghvf)
        return vkxk__rtudp
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    vfux__wdfe = dict(level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', vfux__wdfe, vouw__wvnw,
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
        ijy__bwcqm = 0.0
        vbmdu__deqz = 0.0
        phpdd__lmwes = 0.0
        mqzc__rzc = 0.0
        myz__ghvf = 0
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(A)):
            shgaa__wjvzm = 0.0
            wszhn__zahge = 0
            if not bodo.libs.array_kernels.isna(A, lhnw__ryuk) or not skipna:
                shgaa__wjvzm = np.float64(A[lhnw__ryuk])
                wszhn__zahge = 1
            ijy__bwcqm += shgaa__wjvzm
            vbmdu__deqz += shgaa__wjvzm ** 2
            phpdd__lmwes += shgaa__wjvzm ** 3
            mqzc__rzc += shgaa__wjvzm ** 4
            myz__ghvf += wszhn__zahge
        uzj__ukuhn = bodo.hiframes.series_kernels.compute_kurt(ijy__bwcqm,
            vbmdu__deqz, phpdd__lmwes, mqzc__rzc, myz__ghvf)
        return uzj__ukuhn
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    vfux__wdfe = dict(level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', vfux__wdfe, vouw__wvnw,
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
        ijy__bwcqm = 0.0
        vbmdu__deqz = 0.0
        phpdd__lmwes = 0.0
        myz__ghvf = 0
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(A)):
            shgaa__wjvzm = 0.0
            wszhn__zahge = 0
            if not bodo.libs.array_kernels.isna(A, lhnw__ryuk) or not skipna:
                shgaa__wjvzm = np.float64(A[lhnw__ryuk])
                wszhn__zahge = 1
            ijy__bwcqm += shgaa__wjvzm
            vbmdu__deqz += shgaa__wjvzm ** 2
            phpdd__lmwes += shgaa__wjvzm ** 3
            myz__ghvf += wszhn__zahge
        uzj__ukuhn = bodo.hiframes.series_kernels.compute_skew(ijy__bwcqm,
            vbmdu__deqz, phpdd__lmwes, myz__ghvf)
        return uzj__ukuhn
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    vfux__wdfe = dict(level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', vfux__wdfe, vouw__wvnw,
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
        ynlq__skmq = bodo.hiframes.pd_series_ext.get_series_data(S)
        zmhax__wxps = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        koye__fhfh = 0
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(ynlq__skmq)
            ):
            zohl__mhpey = ynlq__skmq[lhnw__ryuk]
            uyy__wgh = zmhax__wxps[lhnw__ryuk]
            koye__fhfh += zohl__mhpey * uyy__wgh
        return koye__fhfh
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    vfux__wdfe = dict(skipna=skipna)
    vouw__wvnw = dict(skipna=True)
    check_unsupported_args('Series.cumsum', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(skipna=skipna)
    vouw__wvnw = dict(skipna=True)
    check_unsupported_args('Series.cumprod', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(skipna=skipna)
    vouw__wvnw = dict(skipna=True)
    check_unsupported_args('Series.cummin', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(skipna=skipna)
    vouw__wvnw = dict(skipna=True)
    check_unsupported_args('Series.cummax', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    vouw__wvnw = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        ndv__ultj = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, ndv__ultj, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    vfux__wdfe = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    vouw__wvnw = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(level=level)
    vouw__wvnw = dict(level=None)
    check_unsupported_args('Series.count', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    vfux__wdfe = dict(method=method, min_periods=min_periods)
    vouw__wvnw = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        nsiaj__kch = S.sum()
        zpzt__unwv = other.sum()
        a = n * (S * other).sum() - nsiaj__kch * zpzt__unwv
        hjfu__uryij = n * (S ** 2).sum() - nsiaj__kch ** 2
        ati__bqho = n * (other ** 2).sum() - zpzt__unwv ** 2
        return a / np.sqrt(hjfu__uryij * ati__bqho)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    vfux__wdfe = dict(min_periods=min_periods)
    vouw__wvnw = dict(min_periods=None)
    check_unsupported_args('Series.cov', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        nsiaj__kch = S.mean()
        zpzt__unwv = other.mean()
        rkc__evvq = ((S - nsiaj__kch) * (other - zpzt__unwv)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(rkc__evvq, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            klu__gge = np.sign(sum_val)
            return np.inf * klu__gge
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    vfux__wdfe = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(axis=axis, skipna=skipna)
    vouw__wvnw = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(axis=axis, skipna=skipna)
    vouw__wvnw = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', vfux__wdfe, vouw__wvnw,
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
    vfux__wdfe = dict(level=level, numeric_only=numeric_only)
    vouw__wvnw = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', vfux__wdfe, vouw__wvnw,
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
        zfnxf__lpjc = arr[:n]
        qbdqs__apsg = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(zfnxf__lpjc,
            qbdqs__apsg, name)
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
        mnh__wqee = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        zfnxf__lpjc = arr[mnh__wqee:]
        qbdqs__apsg = index[mnh__wqee:]
        return bodo.hiframes.pd_series_ext.init_series(zfnxf__lpjc,
            qbdqs__apsg, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    hmkau__zly = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in hmkau__zly:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            gbko__mieka = index[0]
            eurf__lygo = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                gbko__mieka, False))
        else:
            eurf__lygo = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        zfnxf__lpjc = arr[:eurf__lygo]
        qbdqs__apsg = index[:eurf__lygo]
        return bodo.hiframes.pd_series_ext.init_series(zfnxf__lpjc,
            qbdqs__apsg, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    hmkau__zly = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in hmkau__zly:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            bsn__qhy = index[-1]
            eurf__lygo = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, bsn__qhy,
                True))
        else:
            eurf__lygo = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        zfnxf__lpjc = arr[len(arr) - eurf__lygo:]
        qbdqs__apsg = index[len(arr) - eurf__lygo:]
        return bodo.hiframes.pd_series_ext.init_series(zfnxf__lpjc,
            qbdqs__apsg, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        fyrh__zmkw = bodo.utils.conversion.index_to_array(index)
        weisi__fei, hzi__jrc = bodo.libs.array_kernels.first_last_valid_index(
            arr, fyrh__zmkw)
        return hzi__jrc if weisi__fei else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        fyrh__zmkw = bodo.utils.conversion.index_to_array(index)
        weisi__fei, hzi__jrc = bodo.libs.array_kernels.first_last_valid_index(
            arr, fyrh__zmkw, False)
        return hzi__jrc if weisi__fei else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    vfux__wdfe = dict(keep=keep)
    vouw__wvnw = dict(keep='first')
    check_unsupported_args('Series.nlargest', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        fyrh__zmkw = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ufvss__jolvb, yghet__sjy = bodo.libs.array_kernels.nlargest(arr,
            fyrh__zmkw, n, True, bodo.hiframes.series_kernels.gt_f)
        pve__ruyu = bodo.utils.conversion.convert_to_index(yghet__sjy)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
            pve__ruyu, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    vfux__wdfe = dict(keep=keep)
    vouw__wvnw = dict(keep='first')
    check_unsupported_args('Series.nsmallest', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        fyrh__zmkw = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ufvss__jolvb, yghet__sjy = bodo.libs.array_kernels.nlargest(arr,
            fyrh__zmkw, n, False, bodo.hiframes.series_kernels.lt_f)
        pve__ruyu = bodo.utils.conversion.convert_to_index(yghet__sjy)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
            pve__ruyu, name)
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
    vfux__wdfe = dict(errors=errors)
    vouw__wvnw = dict(errors='raise')
    check_unsupported_args('Series.astype', vfux__wdfe, vouw__wvnw,
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
        ufvss__jolvb = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    vfux__wdfe = dict(axis=axis, is_copy=is_copy)
    vouw__wvnw = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        ewb__dfj = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[ewb__dfj], index
            [ewb__dfj], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    vfux__wdfe = dict(axis=axis, kind=kind, order=order)
    vouw__wvnw = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ojb__lhce = S.notna().values
        if not ojb__lhce.all():
            ufvss__jolvb = np.full(n, -1, np.int64)
            ufvss__jolvb[ojb__lhce] = argsort(arr[ojb__lhce])
        else:
            ufvss__jolvb = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    vfux__wdfe = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    vouw__wvnw = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', vfux__wdfe, vouw__wvnw,
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
        tsu__rre = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        qboj__ils = tsu__rre.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        ufvss__jolvb = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            qboj__ils, 0)
        pve__ruyu = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            qboj__ils)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
            pve__ruyu, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    vfux__wdfe = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    vouw__wvnw = dict(axis=0, inplace=False, kind='quicksort', ignore_index
        =False, key=None)
    check_unsupported_args('Series.sort_values', vfux__wdfe, vouw__wvnw,
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
        tsu__rre = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        qboj__ils = tsu__rre.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        ufvss__jolvb = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            qboj__ils, 0)
        pve__ruyu = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            qboj__ils)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
            pve__ruyu, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    lfr__xwg = is_overload_true(is_nullable)
    rzqff__jutx = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    rzqff__jutx += '  numba.parfors.parfor.init_prange()\n'
    rzqff__jutx += '  n = len(arr)\n'
    if lfr__xwg:
        rzqff__jutx += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        rzqff__jutx += '  out_arr = np.empty(n, np.int64)\n'
    rzqff__jutx += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    rzqff__jutx += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if lfr__xwg:
        rzqff__jutx += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        rzqff__jutx += '      out_arr[i] = -1\n'
    rzqff__jutx += '      continue\n'
    rzqff__jutx += '    val = arr[i]\n'
    rzqff__jutx += '    if include_lowest and val == bins[0]:\n'
    rzqff__jutx += '      ind = 1\n'
    rzqff__jutx += '    else:\n'
    rzqff__jutx += '      ind = np.searchsorted(bins, val)\n'
    rzqff__jutx += '    if ind == 0 or ind == len(bins):\n'
    if lfr__xwg:
        rzqff__jutx += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        rzqff__jutx += '      out_arr[i] = -1\n'
    rzqff__jutx += '    else:\n'
    rzqff__jutx += '      out_arr[i] = ind - 1\n'
    rzqff__jutx += '  return out_arr\n'
    qcurl__owbzg = {}
    exec(rzqff__jutx, {'bodo': bodo, 'np': np, 'numba': numba}, qcurl__owbzg)
    impl = qcurl__owbzg['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        fxunx__rgbib, ear__kqtbl = np.divmod(x, 1)
        if fxunx__rgbib == 0:
            pzjy__atl = -int(np.floor(np.log10(abs(ear__kqtbl)))
                ) - 1 + precision
        else:
            pzjy__atl = precision
        return np.around(x, pzjy__atl)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        leo__owcs = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(leo__owcs)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        iovmf__hfhb = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            qti__wgrnx = bins.copy()
            if right and include_lowest:
                qti__wgrnx[0] = qti__wgrnx[0] - iovmf__hfhb
            zwh__emxfs = bodo.libs.interval_arr_ext.init_interval_array(
                qti__wgrnx[:-1], qti__wgrnx[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(zwh__emxfs,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        qti__wgrnx = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            qti__wgrnx[0] = qti__wgrnx[0] - 10.0 ** -precision
        zwh__emxfs = bodo.libs.interval_arr_ext.init_interval_array(qti__wgrnx
            [:-1], qti__wgrnx[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(zwh__emxfs, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        nieyq__jxpp = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        bmwbq__dcqs = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        ufvss__jolvb = np.zeros(nbins, np.int64)
        for lhnw__ryuk in range(len(nieyq__jxpp)):
            ufvss__jolvb[bmwbq__dcqs[lhnw__ryuk]] = nieyq__jxpp[lhnw__ryuk]
        return ufvss__jolvb
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
            qdlm__lijhq = (max_val - min_val) * 0.001
            if right:
                bins[0] -= qdlm__lijhq
            else:
                bins[-1] += qdlm__lijhq
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    vfux__wdfe = dict(dropna=dropna)
    vouw__wvnw = dict(dropna=True)
    check_unsupported_args('Series.value_counts', vfux__wdfe, vouw__wvnw,
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
    jiid__ejj = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    rzqff__jutx = 'def impl(\n'
    rzqff__jutx += '    S,\n'
    rzqff__jutx += '    normalize=False,\n'
    rzqff__jutx += '    sort=True,\n'
    rzqff__jutx += '    ascending=False,\n'
    rzqff__jutx += '    bins=None,\n'
    rzqff__jutx += '    dropna=True,\n'
    rzqff__jutx += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    rzqff__jutx += '):\n'
    rzqff__jutx += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    rzqff__jutx += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    rzqff__jutx += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if jiid__ejj:
        rzqff__jutx += '    right = True\n'
        rzqff__jutx += _gen_bins_handling(bins, S.dtype)
        rzqff__jutx += '    arr = get_bin_inds(bins, arr)\n'
    rzqff__jutx += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    rzqff__jutx += "        (arr,), index, ('$_bodo_col2_',)\n"
    rzqff__jutx += '    )\n'
    rzqff__jutx += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if jiid__ejj:
        rzqff__jutx += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        rzqff__jutx += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        rzqff__jutx += '    index = get_bin_labels(bins)\n'
    else:
        rzqff__jutx += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        rzqff__jutx += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        rzqff__jutx += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        rzqff__jutx += '    )\n'
        rzqff__jutx += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    rzqff__jutx += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        rzqff__jutx += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        owgx__bofqi = 'len(S)' if jiid__ejj else 'count_arr.sum()'
        rzqff__jutx += f'    res = res / float({owgx__bofqi})\n'
    rzqff__jutx += '    return res\n'
    qcurl__owbzg = {}
    exec(rzqff__jutx, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, qcurl__owbzg)
    impl = qcurl__owbzg['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    rzqff__jutx = ''
    if isinstance(bins, types.Integer):
        rzqff__jutx += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        rzqff__jutx += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            rzqff__jutx += '    min_val = min_val.value\n'
            rzqff__jutx += '    max_val = max_val.value\n'
        rzqff__jutx += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            rzqff__jutx += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        rzqff__jutx += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return rzqff__jutx


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    vfux__wdfe = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    vouw__wvnw = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    rzqff__jutx = 'def impl(\n'
    rzqff__jutx += '    x,\n'
    rzqff__jutx += '    bins,\n'
    rzqff__jutx += '    right=True,\n'
    rzqff__jutx += '    labels=None,\n'
    rzqff__jutx += '    retbins=False,\n'
    rzqff__jutx += '    precision=3,\n'
    rzqff__jutx += '    include_lowest=False,\n'
    rzqff__jutx += "    duplicates='raise',\n"
    rzqff__jutx += '    ordered=True\n'
    rzqff__jutx += '):\n'
    if isinstance(x, SeriesType):
        rzqff__jutx += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        rzqff__jutx += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        rzqff__jutx += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        rzqff__jutx += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    rzqff__jutx += _gen_bins_handling(bins, x.dtype)
    rzqff__jutx += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    rzqff__jutx += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    rzqff__jutx += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    rzqff__jutx += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        rzqff__jutx += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        rzqff__jutx += '    return res\n'
    else:
        rzqff__jutx += '    return out_arr\n'
    qcurl__owbzg = {}
    exec(rzqff__jutx, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, qcurl__owbzg)
    impl = qcurl__owbzg['impl']
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
    vfux__wdfe = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    vouw__wvnw = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        dkmva__ayn = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, dkmva__ayn)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    vfux__wdfe = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    vouw__wvnw = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', vfux__wdfe, vouw__wvnw,
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
            hho__azhwi = bodo.utils.conversion.coerce_to_array(index)
            tsu__rre = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                hho__azhwi, arr), index, (' ', ''))
            return tsu__rre.groupby(' ')['']
        return impl_index
    dfu__eby = by
    if isinstance(by, SeriesType):
        dfu__eby = by.data
    if isinstance(dfu__eby, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        hho__azhwi = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        tsu__rre = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            hho__azhwi, arr), index, (' ', ''))
        return tsu__rre.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    vfux__wdfe = dict(verify_integrity=verify_integrity)
    vouw__wvnw = dict(verify_integrity=False)
    check_unsupported_args('Series.append', vfux__wdfe, vouw__wvnw,
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
            htf__pyz = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            ufvss__jolvb = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(ufvss__jolvb, A, htf__pyz, False)
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ufvss__jolvb = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    vfux__wdfe = dict(interpolation=interpolation)
    vouw__wvnw = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            ufvss__jolvb = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
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
        tdk__ynh = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(tdk__ynh, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    vfux__wdfe = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    vouw__wvnw = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', vfux__wdfe, vouw__wvnw,
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
        ueklo__fmm = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        ueklo__fmm = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    rzqff__jutx = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {ueklo__fmm}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    pch__xmovx = dict()
    exec(rzqff__jutx, {'bodo': bodo, 'numba': numba}, pch__xmovx)
    xibx__xlje = pch__xmovx['impl']
    return xibx__xlje


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        ueklo__fmm = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        ueklo__fmm = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    rzqff__jutx = 'def impl(S,\n'
    rzqff__jutx += '     value=None,\n'
    rzqff__jutx += '    method=None,\n'
    rzqff__jutx += '    axis=None,\n'
    rzqff__jutx += '    inplace=False,\n'
    rzqff__jutx += '    limit=None,\n'
    rzqff__jutx += '   downcast=None,\n'
    rzqff__jutx += '):\n'
    rzqff__jutx += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    rzqff__jutx += '    n = len(in_arr)\n'
    rzqff__jutx += f'    out_arr = {ueklo__fmm}(n, -1)\n'
    rzqff__jutx += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    rzqff__jutx += '        s = in_arr[j]\n'
    rzqff__jutx += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    rzqff__jutx += '            s = value\n'
    rzqff__jutx += '        out_arr[j] = s\n'
    rzqff__jutx += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    pch__xmovx = dict()
    exec(rzqff__jutx, {'bodo': bodo, 'numba': numba}, pch__xmovx)
    xibx__xlje = pch__xmovx['impl']
    return xibx__xlje


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
    tyx__emqq = bodo.hiframes.pd_series_ext.get_series_data(value)
    for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(oxrl__oat)):
        s = oxrl__oat[lhnw__ryuk]
        if bodo.libs.array_kernels.isna(oxrl__oat, lhnw__ryuk
            ) and not bodo.libs.array_kernels.isna(tyx__emqq, lhnw__ryuk):
            s = tyx__emqq[lhnw__ryuk]
        oxrl__oat[lhnw__ryuk] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
    for lhnw__ryuk in numba.parfors.parfor.internal_prange(len(oxrl__oat)):
        s = oxrl__oat[lhnw__ryuk]
        if bodo.libs.array_kernels.isna(oxrl__oat, lhnw__ryuk):
            s = value
        oxrl__oat[lhnw__ryuk] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    tyx__emqq = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(oxrl__oat)
    ufvss__jolvb = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for sjl__sqkrm in numba.parfors.parfor.internal_prange(n):
        s = oxrl__oat[sjl__sqkrm]
        if bodo.libs.array_kernels.isna(oxrl__oat, sjl__sqkrm
            ) and not bodo.libs.array_kernels.isna(tyx__emqq, sjl__sqkrm):
            s = tyx__emqq[sjl__sqkrm]
        ufvss__jolvb[sjl__sqkrm] = s
        if bodo.libs.array_kernels.isna(oxrl__oat, sjl__sqkrm
            ) and bodo.libs.array_kernels.isna(tyx__emqq, sjl__sqkrm):
            bodo.libs.array_kernels.setna(ufvss__jolvb, sjl__sqkrm)
    return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    tyx__emqq = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(oxrl__oat)
    ufvss__jolvb = bodo.utils.utils.alloc_type(n, oxrl__oat.dtype, (-1,))
    for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
        s = oxrl__oat[lhnw__ryuk]
        if bodo.libs.array_kernels.isna(oxrl__oat, lhnw__ryuk
            ) and not bodo.libs.array_kernels.isna(tyx__emqq, lhnw__ryuk):
            s = tyx__emqq[lhnw__ryuk]
        ufvss__jolvb[lhnw__ryuk] = s
    return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    vfux__wdfe = dict(limit=limit, downcast=downcast)
    vouw__wvnw = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')
    nbpbf__xbxqu = not is_overload_none(value)
    qgsk__hncp = not is_overload_none(method)
    if nbpbf__xbxqu and qgsk__hncp:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not nbpbf__xbxqu and not qgsk__hncp:
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
    if qgsk__hncp:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        nzei__pcwf = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(nzei__pcwf)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(nzei__pcwf)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    vxfih__mkwl = element_type(S.data)
    uyqu__xws = None
    if nbpbf__xbxqu:
        uyqu__xws = element_type(types.unliteral(value))
    if uyqu__xws and not can_replace(vxfih__mkwl, uyqu__xws):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {uyqu__xws} with series type {vxfih__mkwl}'
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
        lood__hltky = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                tyx__emqq = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(oxrl__oat)
                ufvss__jolvb = bodo.utils.utils.alloc_type(n, lood__hltky,
                    (-1,))
                for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(oxrl__oat, lhnw__ryuk
                        ) and bodo.libs.array_kernels.isna(tyx__emqq,
                        lhnw__ryuk):
                        bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
                        continue
                    if bodo.libs.array_kernels.isna(oxrl__oat, lhnw__ryuk):
                        ufvss__jolvb[lhnw__ryuk
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            tyx__emqq[lhnw__ryuk])
                        continue
                    ufvss__jolvb[lhnw__ryuk
                        ] = bodo.utils.conversion.unbox_if_timestamp(oxrl__oat
                        [lhnw__ryuk])
                return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                    index, name)
            return fillna_series_impl
        if qgsk__hncp:
            ydmc__agkm = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(vxfih__mkwl, (types.Integer, types.Float)
                ) and vxfih__mkwl not in ydmc__agkm:
                raise BodoError(
                    f"Series.fillna(): series of type {vxfih__mkwl} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                ufvss__jolvb = bodo.libs.array_kernels.ffill_bfill_arr(
                    oxrl__oat, method)
                return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(oxrl__oat)
            ufvss__jolvb = bodo.utils.utils.alloc_type(n, lood__hltky, (-1,))
            for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(oxrl__oat[
                    lhnw__ryuk])
                if bodo.libs.array_kernels.isna(oxrl__oat, lhnw__ryuk):
                    s = value
                ufvss__jolvb[lhnw__ryuk] = s
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        iieud__nldoc = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        vfux__wdfe = dict(limit=limit, downcast=downcast)
        vouw__wvnw = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', vfux__wdfe,
            vouw__wvnw, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        vxfih__mkwl = element_type(S.data)
        ydmc__agkm = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(vxfih__mkwl, (types.Integer, types.Float)
            ) and vxfih__mkwl not in ydmc__agkm:
            raise BodoError(
                f'Series.{overload_name}(): series of type {vxfih__mkwl} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ufvss__jolvb = bodo.libs.array_kernels.ffill_bfill_arr(oxrl__oat,
                iieud__nldoc)
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        fmibi__vjy = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            fmibi__vjy)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        lztnn__uzoyc = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(lztnn__uzoyc)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        lztnn__uzoyc = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(lztnn__uzoyc)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        lztnn__uzoyc = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(lztnn__uzoyc)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    vfux__wdfe = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    peyie__vmq = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', vfux__wdfe, peyie__vmq,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    vxfih__mkwl = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        ggjma__thav = element_type(to_replace.key_type)
        uyqu__xws = element_type(to_replace.value_type)
    else:
        ggjma__thav = element_type(to_replace)
        uyqu__xws = element_type(value)
    ecm__bizp = None
    if vxfih__mkwl != types.unliteral(ggjma__thav):
        if bodo.utils.typing.equality_always_false(vxfih__mkwl, types.
            unliteral(ggjma__thav)
            ) or not bodo.utils.typing.types_equality_exists(vxfih__mkwl,
            ggjma__thav):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(vxfih__mkwl, (types.Float, types.Integer)
            ) or vxfih__mkwl == np.bool_:
            ecm__bizp = vxfih__mkwl
    if not can_replace(vxfih__mkwl, types.unliteral(uyqu__xws)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    wawth__ntcz = to_str_arr_if_dict_array(S.data)
    if isinstance(wawth__ntcz, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(oxrl__oat.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(oxrl__oat)
        ufvss__jolvb = bodo.utils.utils.alloc_type(n, wawth__ntcz, (-1,))
        bqdlc__bdlr = build_replace_dict(to_replace, value, ecm__bizp)
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(oxrl__oat, lhnw__ryuk):
                bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
                continue
            s = oxrl__oat[lhnw__ryuk]
            if s in bqdlc__bdlr:
                s = bqdlc__bdlr[s]
            ufvss__jolvb[lhnw__ryuk] = s
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    xurd__adcdt = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    hgx__fgia = is_iterable_type(to_replace)
    vxc__hhpy = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    eayt__rjxpx = is_iterable_type(value)
    if xurd__adcdt and vxc__hhpy:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                bqdlc__bdlr = {}
                bqdlc__bdlr[key_dtype_conv(to_replace)] = value
                return bqdlc__bdlr
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            bqdlc__bdlr = {}
            bqdlc__bdlr[to_replace] = value
            return bqdlc__bdlr
        return impl
    if hgx__fgia and vxc__hhpy:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                bqdlc__bdlr = {}
                for jhf__jif in to_replace:
                    bqdlc__bdlr[key_dtype_conv(jhf__jif)] = value
                return bqdlc__bdlr
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            bqdlc__bdlr = {}
            for jhf__jif in to_replace:
                bqdlc__bdlr[jhf__jif] = value
            return bqdlc__bdlr
        return impl
    if hgx__fgia and eayt__rjxpx:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                bqdlc__bdlr = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for lhnw__ryuk in range(len(to_replace)):
                    bqdlc__bdlr[key_dtype_conv(to_replace[lhnw__ryuk])
                        ] = value[lhnw__ryuk]
                return bqdlc__bdlr
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            bqdlc__bdlr = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for lhnw__ryuk in range(len(to_replace)):
                bqdlc__bdlr[to_replace[lhnw__ryuk]] = value[lhnw__ryuk]
            return bqdlc__bdlr
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
            ufvss__jolvb = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo
                .hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ufvss__jolvb = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    vfux__wdfe = dict(ignore_index=ignore_index)
    gtwo__bpmg = dict(ignore_index=False)
    check_unsupported_args('Series.explode', vfux__wdfe, gtwo__bpmg,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fyrh__zmkw = bodo.utils.conversion.index_to_array(index)
        ufvss__jolvb, vrubw__ikpfm = bodo.libs.array_kernels.explode(arr,
            fyrh__zmkw)
        pve__ruyu = bodo.utils.conversion.index_from_array(vrubw__ikpfm)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
            pve__ruyu, name)
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
            dgn__rpniq = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                dgn__rpniq[lhnw__ryuk] = np.argmax(a[lhnw__ryuk])
            return dgn__rpniq
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            fxoy__kzq = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                fxoy__kzq[lhnw__ryuk] = np.argmin(a[lhnw__ryuk])
            return fxoy__kzq
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
    vfux__wdfe = dict(axis=axis, inplace=inplace, how=how)
    vkkx__peaky = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', vfux__wdfe, vkkx__peaky,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ojb__lhce = S.notna().values
            fyrh__zmkw = bodo.utils.conversion.extract_index_array(S)
            pve__ruyu = bodo.utils.conversion.convert_to_index(fyrh__zmkw[
                ojb__lhce])
            ufvss__jolvb = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(oxrl__oat))
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                pve__ruyu, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            fyrh__zmkw = bodo.utils.conversion.extract_index_array(S)
            ojb__lhce = S.notna().values
            pve__ruyu = bodo.utils.conversion.convert_to_index(fyrh__zmkw[
                ojb__lhce])
            ufvss__jolvb = oxrl__oat[ojb__lhce]
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                pve__ruyu, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    vfux__wdfe = dict(freq=freq, axis=axis, fill_value=fill_value)
    vouw__wvnw = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', vfux__wdfe, vouw__wvnw,
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
        ufvss__jolvb = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    vfux__wdfe = dict(fill_method=fill_method, limit=limit, freq=freq)
    vouw__wvnw = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', vfux__wdfe, vouw__wvnw,
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
        ufvss__jolvb = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
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
            njsv__aotbo = 'None'
        else:
            njsv__aotbo = 'other'
        rzqff__jutx = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            rzqff__jutx += '  cond = ~cond\n'
        rzqff__jutx += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        rzqff__jutx += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rzqff__jutx += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        rzqff__jutx += f"""  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {njsv__aotbo})
"""
        rzqff__jutx += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        qcurl__owbzg = {}
        exec(rzqff__jutx, {'bodo': bodo, 'np': np}, qcurl__owbzg)
        impl = qcurl__owbzg['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        fmibi__vjy = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(fmibi__vjy)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    vfux__wdfe = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    vouw__wvnw = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', vfux__wdfe, vouw__wvnw,
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
    ckxt__ziy = is_overload_constant_nan(other)
    if not (is_default or ckxt__ziy or is_scalar_type(other) or isinstance(
        other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
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
            lnst__gvl = arr.dtype.elem_type
        else:
            lnst__gvl = arr.dtype
        if is_iterable_type(other):
            gts__twk = other.dtype
        elif ckxt__ziy:
            gts__twk = types.float64
        else:
            gts__twk = types.unliteral(other)
        if not ckxt__ziy and not is_common_scalar_dtype([lnst__gvl, gts__twk]):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        vfux__wdfe = dict(level=level, axis=axis)
        vouw__wvnw = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), vfux__wdfe,
            vouw__wvnw, package_name='pandas', module_name='Series')
        wde__ttbbc = other == string_type or is_overload_constant_str(other)
        hid__srqu = is_iterable_type(other) and other.dtype == string_type
        arl__ife = S.dtype == string_type and (op == operator.add and (
            wde__ttbbc or hid__srqu) or op == operator.mul and isinstance(
            other, types.Integer))
        tmzg__xxfe = S.dtype == bodo.timedelta64ns
        uudah__quhgb = S.dtype == bodo.datetime64ns
        kvl__ibtr = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        iggqf__eeh = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        aav__tcpn = tmzg__xxfe and (kvl__ibtr or iggqf__eeh
            ) or uudah__quhgb and kvl__ibtr
        aav__tcpn = aav__tcpn and op == operator.add
        if not (isinstance(S.dtype, types.Number) or arl__ife or aav__tcpn):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        prv__ouu = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            wawth__ntcz = prv__ouu.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and wawth__ntcz == types.Array(types.bool_, 1, 'C'):
                wawth__ntcz = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                ufvss__jolvb = bodo.utils.utils.alloc_type(n, wawth__ntcz,
                    (-1,))
                for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                    llcuy__ygz = bodo.libs.array_kernels.isna(arr, lhnw__ryuk)
                    if llcuy__ygz:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(ufvss__jolvb,
                                lhnw__ryuk)
                        else:
                            ufvss__jolvb[lhnw__ryuk] = op(fill_value, other)
                    else:
                        ufvss__jolvb[lhnw__ryuk] = op(arr[lhnw__ryuk], other)
                return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        wawth__ntcz = prv__ouu.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and wawth__ntcz == types.Array(
            types.bool_, 1, 'C'):
            wawth__ntcz = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            bfsk__zpwn = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            ufvss__jolvb = bodo.utils.utils.alloc_type(n, wawth__ntcz, (-1,))
            for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                llcuy__ygz = bodo.libs.array_kernels.isna(arr, lhnw__ryuk)
                zoldt__scfi = bodo.libs.array_kernels.isna(bfsk__zpwn,
                    lhnw__ryuk)
                if llcuy__ygz and zoldt__scfi:
                    bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
                elif llcuy__ygz:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
                    else:
                        ufvss__jolvb[lhnw__ryuk] = op(fill_value,
                            bfsk__zpwn[lhnw__ryuk])
                elif zoldt__scfi:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
                    else:
                        ufvss__jolvb[lhnw__ryuk] = op(arr[lhnw__ryuk],
                            fill_value)
                else:
                    ufvss__jolvb[lhnw__ryuk] = op(arr[lhnw__ryuk],
                        bfsk__zpwn[lhnw__ryuk])
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
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
        prv__ouu = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            wawth__ntcz = prv__ouu.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and wawth__ntcz == types.Array(types.bool_, 1, 'C'):
                wawth__ntcz = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                ufvss__jolvb = bodo.utils.utils.alloc_type(n, wawth__ntcz, None
                    )
                for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                    llcuy__ygz = bodo.libs.array_kernels.isna(arr, lhnw__ryuk)
                    if llcuy__ygz:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(ufvss__jolvb,
                                lhnw__ryuk)
                        else:
                            ufvss__jolvb[lhnw__ryuk] = op(other, fill_value)
                    else:
                        ufvss__jolvb[lhnw__ryuk] = op(other, arr[lhnw__ryuk])
                return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        wawth__ntcz = prv__ouu.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and wawth__ntcz == types.Array(
            types.bool_, 1, 'C'):
            wawth__ntcz = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            bfsk__zpwn = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            ufvss__jolvb = bodo.utils.utils.alloc_type(n, wawth__ntcz, None)
            for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                llcuy__ygz = bodo.libs.array_kernels.isna(arr, lhnw__ryuk)
                zoldt__scfi = bodo.libs.array_kernels.isna(bfsk__zpwn,
                    lhnw__ryuk)
                ufvss__jolvb[lhnw__ryuk] = op(bfsk__zpwn[lhnw__ryuk], arr[
                    lhnw__ryuk])
                if llcuy__ygz and zoldt__scfi:
                    bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
                elif llcuy__ygz:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
                    else:
                        ufvss__jolvb[lhnw__ryuk] = op(bfsk__zpwn[lhnw__ryuk
                            ], fill_value)
                elif zoldt__scfi:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
                    else:
                        ufvss__jolvb[lhnw__ryuk] = op(fill_value, arr[
                            lhnw__ryuk])
                else:
                    ufvss__jolvb[lhnw__ryuk] = op(bfsk__zpwn[lhnw__ryuk],
                        arr[lhnw__ryuk])
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
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
    for op, vczzg__viv in explicit_binop_funcs_two_ways.items():
        for name in vczzg__viv:
            fmibi__vjy = create_explicit_binary_op_overload(op)
            nnr__ikjlh = create_explicit_binary_reverse_op_overload(op)
            hzm__miko = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(fmibi__vjy)
            overload_method(SeriesType, hzm__miko, no_unliteral=True)(
                nnr__ikjlh)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        fmibi__vjy = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(fmibi__vjy)
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
                awidy__iqkf = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                ufvss__jolvb = dt64_arr_sub(arr, awidy__iqkf)
                return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
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
                ufvss__jolvb = np.empty(n, np.dtype('datetime64[ns]'))
                for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, lhnw__ryuk):
                        bodo.libs.array_kernels.setna(ufvss__jolvb, lhnw__ryuk)
                        continue
                    szvz__bkwuj = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[lhnw__ryuk]))
                    tyth__kpnfv = op(szvz__bkwuj, rhs)
                    ufvss__jolvb[lhnw__ryuk
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        tyth__kpnfv.value)
                return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
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
                    awidy__iqkf = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    ufvss__jolvb = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(awidy__iqkf))
                    return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb
                        , index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                awidy__iqkf = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                ufvss__jolvb = op(arr, awidy__iqkf)
                return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    ccvta__ndac = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    ufvss__jolvb = op(bodo.utils.conversion.
                        unbox_if_timestamp(ccvta__ndac), arr)
                    return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb
                        , index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                ccvta__ndac = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                ufvss__jolvb = op(ccvta__ndac, arr)
                return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        fmibi__vjy = create_binary_op_overload(op)
        overload(op)(fmibi__vjy)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    hda__bkh = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, hda__bkh)
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, lhnw__ryuk
                ) or bodo.libs.array_kernels.isna(arg2, lhnw__ryuk):
                bodo.libs.array_kernels.setna(S, lhnw__ryuk)
                continue
            S[lhnw__ryuk
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                lhnw__ryuk]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[lhnw__ryuk]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                bfsk__zpwn = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, bfsk__zpwn)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        fmibi__vjy = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(fmibi__vjy)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                ufvss__jolvb = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        fmibi__vjy = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(fmibi__vjy)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    ufvss__jolvb = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb
                        , index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    bfsk__zpwn = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    ufvss__jolvb = ufunc(arr, bfsk__zpwn)
                    return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb
                        , index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    bfsk__zpwn = bodo.hiframes.pd_series_ext.get_series_data(S2
                        )
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    ufvss__jolvb = ufunc(arr, bfsk__zpwn)
                    return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb
                        , index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        fmibi__vjy = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(fmibi__vjy)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        huw__znywg = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),)
            )
        hyo__simwi = np.arange(n),
        bodo.libs.timsort.sort(huw__znywg, 0, n, hyo__simwi)
        return hyo__simwi[0]
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
        ulqjf__iyvf = get_overload_const_str(downcast)
        if ulqjf__iyvf in ('integer', 'signed'):
            out_dtype = types.int64
        elif ulqjf__iyvf == 'unsigned':
            out_dtype = types.uint64
        else:
            assert ulqjf__iyvf == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            oxrl__oat = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            ufvss__jolvb = pd.to_numeric(oxrl__oat, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            wcgk__xqje = np.empty(n, np.float64)
            for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, lhnw__ryuk):
                    bodo.libs.array_kernels.setna(wcgk__xqje, lhnw__ryuk)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(wcgk__xqje,
                        lhnw__ryuk, arg_a, lhnw__ryuk)
            return wcgk__xqje
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            wcgk__xqje = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, lhnw__ryuk):
                    bodo.libs.array_kernels.setna(wcgk__xqje, lhnw__ryuk)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(wcgk__xqje,
                        lhnw__ryuk, arg_a, lhnw__ryuk)
            return wcgk__xqje
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        nwm__ztfj = if_series_to_array_type(args[0])
        if isinstance(nwm__ztfj, types.Array) and isinstance(nwm__ztfj.
            dtype, types.Integer):
            nwm__ztfj = types.Array(types.float64, 1, 'C')
        return nwm__ztfj(*args)


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
    asie__irg = bodo.utils.utils.is_array_typ(x, True)
    kie__abq = bodo.utils.utils.is_array_typ(y, True)
    rzqff__jutx = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        rzqff__jutx += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if asie__irg and not bodo.utils.utils.is_array_typ(x, False):
        rzqff__jutx += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if kie__abq and not bodo.utils.utils.is_array_typ(y, False):
        rzqff__jutx += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    rzqff__jutx += '  n = len(condition)\n'
    elz__floxo = x.dtype if asie__irg else types.unliteral(x)
    clx__yoy = y.dtype if kie__abq else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        elz__floxo = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        clx__yoy = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    pyx__rgybf = get_data(x)
    wjfv__delrf = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(hyo__simwi) for
        hyo__simwi in [pyx__rgybf, wjfv__delrf])
    if wjfv__delrf == types.none:
        if isinstance(elz__floxo, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif pyx__rgybf == wjfv__delrf and not is_nullable:
        out_dtype = dtype_to_array_type(elz__floxo)
    elif elz__floxo == string_type or clx__yoy == string_type:
        out_dtype = bodo.string_array_type
    elif pyx__rgybf == bytes_type or (asie__irg and elz__floxo == bytes_type
        ) and (wjfv__delrf == bytes_type or kie__abq and clx__yoy == bytes_type
        ):
        out_dtype = binary_array_type
    elif isinstance(elz__floxo, bodo.PDCategoricalDtype):
        out_dtype = None
    elif elz__floxo in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(elz__floxo, 1, 'C')
    elif clx__yoy in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(clx__yoy, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(elz__floxo), numba.np.numpy_support.
            as_dtype(clx__yoy)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(elz__floxo, bodo.PDCategoricalDtype):
        gizwi__whhfy = 'x'
    else:
        gizwi__whhfy = 'out_dtype'
    rzqff__jutx += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {gizwi__whhfy}, (-1,))\n')
    if isinstance(elz__floxo, bodo.PDCategoricalDtype):
        rzqff__jutx += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        rzqff__jutx += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    rzqff__jutx += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    rzqff__jutx += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if asie__irg:
        rzqff__jutx += '      if bodo.libs.array_kernels.isna(x, j):\n'
        rzqff__jutx += '        setna(out_arr, j)\n'
        rzqff__jutx += '        continue\n'
    if isinstance(elz__floxo, bodo.PDCategoricalDtype):
        rzqff__jutx += '      out_codes[j] = x_codes[j]\n'
    else:
        rzqff__jutx += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if asie__irg else 'x'))
    rzqff__jutx += '    else:\n'
    if kie__abq:
        rzqff__jutx += '      if bodo.libs.array_kernels.isna(y, j):\n'
        rzqff__jutx += '        setna(out_arr, j)\n'
        rzqff__jutx += '        continue\n'
    if wjfv__delrf == types.none:
        if isinstance(elz__floxo, bodo.PDCategoricalDtype):
            rzqff__jutx += '      out_codes[j] = -1\n'
        else:
            rzqff__jutx += '      setna(out_arr, j)\n'
    else:
        rzqff__jutx += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if kie__abq else 'y'))
    rzqff__jutx += '  return out_arr\n'
    qcurl__owbzg = {}
    exec(rzqff__jutx, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, qcurl__owbzg)
    hugts__mkjrt = qcurl__owbzg['_impl']
    return hugts__mkjrt


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
        eooou__ckmz = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(eooou__ckmz, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(eooou__ckmz):
            qfura__yjk = eooou__ckmz.data.dtype
        else:
            qfura__yjk = eooou__ckmz.dtype
        if isinstance(qfura__yjk, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        nzg__dskzj = eooou__ckmz
    else:
        wdn__vrxl = []
        for eooou__ckmz in choicelist:
            if not bodo.utils.utils.is_array_typ(eooou__ckmz, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(eooou__ckmz):
                qfura__yjk = eooou__ckmz.data.dtype
            else:
                qfura__yjk = eooou__ckmz.dtype
            if isinstance(qfura__yjk, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            wdn__vrxl.append(qfura__yjk)
        if not is_common_scalar_dtype(wdn__vrxl):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        nzg__dskzj = choicelist[0]
    if is_series_type(nzg__dskzj):
        nzg__dskzj = nzg__dskzj.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, nzg__dskzj.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(nzg__dskzj, types.Array) or isinstance(nzg__dskzj,
        BooleanArrayType) or isinstance(nzg__dskzj, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(nzg__dskzj, False) and nzg__dskzj.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {nzg__dskzj} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    gis__cgv = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        dfyz__ipyx = choicelist.dtype
    else:
        cws__uzzth = False
        wdn__vrxl = []
        for eooou__ckmz in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                eooou__ckmz, 'numpy.select()')
            if is_nullable_type(eooou__ckmz):
                cws__uzzth = True
            if is_series_type(eooou__ckmz):
                qfura__yjk = eooou__ckmz.data.dtype
            else:
                qfura__yjk = eooou__ckmz.dtype
            if isinstance(qfura__yjk, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            wdn__vrxl.append(qfura__yjk)
        guwrn__hehjm, srj__lsk = get_common_scalar_dtype(wdn__vrxl)
        if not srj__lsk:
            raise BodoError('Internal error in overload_np_select')
        jisv__xwyum = dtype_to_array_type(guwrn__hehjm)
        if cws__uzzth:
            jisv__xwyum = to_nullable_type(jisv__xwyum)
        dfyz__ipyx = jisv__xwyum
    if isinstance(dfyz__ipyx, SeriesType):
        dfyz__ipyx = dfyz__ipyx.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        iebl__mikn = True
    else:
        iebl__mikn = False
    ykfb__uoas = False
    ndc__bpdks = False
    if iebl__mikn:
        if isinstance(dfyz__ipyx.dtype, types.Number):
            pass
        elif dfyz__ipyx.dtype == types.bool_:
            ndc__bpdks = True
        else:
            ykfb__uoas = True
            dfyz__ipyx = to_nullable_type(dfyz__ipyx)
    elif default == types.none or is_overload_constant_nan(default):
        ykfb__uoas = True
        dfyz__ipyx = to_nullable_type(dfyz__ipyx)
    rzqff__jutx = 'def np_select_impl(condlist, choicelist, default=0):\n'
    rzqff__jutx += '  if len(condlist) != len(choicelist):\n'
    rzqff__jutx += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    rzqff__jutx += '  output_len = len(choicelist[0])\n'
    rzqff__jutx += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    rzqff__jutx += '  for i in range(output_len):\n'
    if ykfb__uoas:
        rzqff__jutx += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif ndc__bpdks:
        rzqff__jutx += '    out[i] = False\n'
    else:
        rzqff__jutx += '    out[i] = default\n'
    if gis__cgv:
        rzqff__jutx += '  for i in range(len(condlist) - 1, -1, -1):\n'
        rzqff__jutx += '    cond = condlist[i]\n'
        rzqff__jutx += '    choice = choicelist[i]\n'
        rzqff__jutx += '    out = np.where(cond, choice, out)\n'
    else:
        for lhnw__ryuk in range(len(choicelist) - 1, -1, -1):
            rzqff__jutx += f'  cond = condlist[{lhnw__ryuk}]\n'
            rzqff__jutx += f'  choice = choicelist[{lhnw__ryuk}]\n'
            rzqff__jutx += f'  out = np.where(cond, choice, out)\n'
    rzqff__jutx += '  return out'
    qcurl__owbzg = dict()
    exec(rzqff__jutx, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': dfyz__ipyx}, qcurl__owbzg)
    impl = qcurl__owbzg['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ufvss__jolvb = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    vfux__wdfe = dict(subset=subset, keep=keep, inplace=inplace)
    vouw__wvnw = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', vfux__wdfe, vouw__wvnw,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        xqa__wysez = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (xqa__wysez,), fyrh__zmkw = bodo.libs.array_kernels.drop_duplicates((
            xqa__wysez,), index, 1)
        index = bodo.utils.conversion.index_from_array(fyrh__zmkw)
        return bodo.hiframes.pd_series_ext.init_series(xqa__wysez, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    ggd__tac = element_type(S.data)
    if not is_common_scalar_dtype([ggd__tac, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([ggd__tac, right]):
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
        ufvss__jolvb = np.empty(n, np.bool_)
        for lhnw__ryuk in numba.parfors.parfor.internal_prange(n):
            shgaa__wjvzm = bodo.utils.conversion.box_if_dt64(arr[lhnw__ryuk])
            if inclusive == 'both':
                ufvss__jolvb[lhnw__ryuk
                    ] = shgaa__wjvzm <= right and shgaa__wjvzm >= left
            else:
                ufvss__jolvb[lhnw__ryuk
                    ] = shgaa__wjvzm < right and shgaa__wjvzm > left
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb, index,
            name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    vfux__wdfe = dict(axis=axis)
    vouw__wvnw = dict(axis=None)
    check_unsupported_args('Series.repeat', vfux__wdfe, vouw__wvnw,
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
            fyrh__zmkw = bodo.utils.conversion.index_to_array(index)
            ufvss__jolvb = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            vrubw__ikpfm = bodo.libs.array_kernels.repeat_kernel(fyrh__zmkw,
                repeats)
            pve__ruyu = bodo.utils.conversion.index_from_array(vrubw__ikpfm)
            return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
                pve__ruyu, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fyrh__zmkw = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        ufvss__jolvb = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        vrubw__ikpfm = bodo.libs.array_kernels.repeat_kernel(fyrh__zmkw,
            repeats)
        pve__ruyu = bodo.utils.conversion.index_from_array(vrubw__ikpfm)
        return bodo.hiframes.pd_series_ext.init_series(ufvss__jolvb,
            pve__ruyu, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        hyo__simwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(hyo__simwi)
        kkwyx__erxyz = {}
        for lhnw__ryuk in range(n):
            shgaa__wjvzm = bodo.utils.conversion.box_if_dt64(hyo__simwi[
                lhnw__ryuk])
            kkwyx__erxyz[index[lhnw__ryuk]] = shgaa__wjvzm
        return kkwyx__erxyz
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    nzei__pcwf = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            hucrw__asgh = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(nzei__pcwf)
    elif is_literal_type(name):
        hucrw__asgh = get_literal_value(name)
    else:
        raise_bodo_error(nzei__pcwf)
    hucrw__asgh = 0 if hucrw__asgh is None else hucrw__asgh

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (hucrw__asgh,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
