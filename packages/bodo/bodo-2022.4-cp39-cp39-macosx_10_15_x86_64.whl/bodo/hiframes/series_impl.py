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
            sbwn__rrd = bodo.hiframes.pd_series_ext.get_series_data(s)
            inz__nytgm = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                sbwn__rrd)
            return inz__nytgm
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
            uzftc__kej = list()
            for tazsb__mvow in range(len(S)):
                uzftc__kej.append(S.iat[tazsb__mvow])
            return uzftc__kej
        return impl_float

    def impl(S):
        uzftc__kej = list()
        for tazsb__mvow in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, tazsb__mvow):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            uzftc__kej.append(S.iat[tazsb__mvow])
        return uzftc__kej
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    xci__flkyz = dict(dtype=dtype, copy=copy, na_value=na_value)
    mldpl__xnwz = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    xci__flkyz = dict(name=name, inplace=inplace)
    mldpl__xnwz = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', xci__flkyz, mldpl__xnwz,
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
    zxvrp__rnipl = get_name_literal(S.index.name_typ, True, series_name)
    columns = [zxvrp__rnipl, series_name]
    jpf__wcv = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    jpf__wcv += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    jpf__wcv += """    index = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S))
"""
    jpf__wcv += (
        '    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)\n'
        )
    jpf__wcv += '    col_var = {}\n'.format(gen_const_tup(columns))
    jpf__wcv += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe((index, arr), df_index, col_var)
"""
    hfkvs__ogzi = {}
    exec(jpf__wcv, {'bodo': bodo}, hfkvs__ogzi)
    lae__tevq = hfkvs__ogzi['_impl']
    return lae__tevq


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wkfhu__uqi = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
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
        wkfhu__uqi = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[tazsb__mvow]):
                bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
            else:
                wkfhu__uqi[tazsb__mvow] = np.round(arr[tazsb__mvow], decimals)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    xci__flkyz = dict(level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    mldpl__xnwz = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        slcie__hmtop = 0
        for tazsb__mvow in numba.parfors.parfor.internal_prange(len(A)):
            cwxw__vqg = 0
            if not bodo.libs.array_kernels.isna(A, tazsb__mvow):
                cwxw__vqg = int(A[tazsb__mvow])
            slcie__hmtop += cwxw__vqg
        return slcie__hmtop != 0
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
        ewmpc__tmn = bodo.hiframes.pd_series_ext.get_series_data(S)
        oftcc__ffzu = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        slcie__hmtop = 0
        for tazsb__mvow in numba.parfors.parfor.internal_prange(len(ewmpc__tmn)
            ):
            cwxw__vqg = 0
            yiv__xdrno = bodo.libs.array_kernels.isna(ewmpc__tmn, tazsb__mvow)
            qfqy__cho = bodo.libs.array_kernels.isna(oftcc__ffzu, tazsb__mvow)
            if yiv__xdrno and not qfqy__cho or not yiv__xdrno and qfqy__cho:
                cwxw__vqg = 1
            elif not yiv__xdrno:
                if ewmpc__tmn[tazsb__mvow] != oftcc__ffzu[tazsb__mvow]:
                    cwxw__vqg = 1
            slcie__hmtop += cwxw__vqg
        return slcie__hmtop == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    xci__flkyz = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=
        level)
    mldpl__xnwz = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        slcie__hmtop = 0
        for tazsb__mvow in numba.parfors.parfor.internal_prange(len(A)):
            cwxw__vqg = 0
            if not bodo.libs.array_kernels.isna(A, tazsb__mvow):
                cwxw__vqg = int(not A[tazsb__mvow])
            slcie__hmtop += cwxw__vqg
        return slcie__hmtop == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    xci__flkyz = dict(level=level)
    mldpl__xnwz = dict(level=None)
    check_unsupported_args('Series.mad', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    yzcaw__hhjeq = types.float64
    seow__qef = types.float64
    if S.dtype == types.float32:
        yzcaw__hhjeq = types.float32
        seow__qef = types.float32
    dvkx__bmo = yzcaw__hhjeq(0)
    tlmrk__mpt = seow__qef(0)
    uljz__xla = seow__qef(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        dtj__zuyjt = dvkx__bmo
        slcie__hmtop = tlmrk__mpt
        for tazsb__mvow in numba.parfors.parfor.internal_prange(len(A)):
            cwxw__vqg = dvkx__bmo
            xwvrq__dkq = tlmrk__mpt
            if not bodo.libs.array_kernels.isna(A, tazsb__mvow) or not skipna:
                cwxw__vqg = A[tazsb__mvow]
                xwvrq__dkq = uljz__xla
            dtj__zuyjt += cwxw__vqg
            slcie__hmtop += xwvrq__dkq
        ery__hmr = bodo.hiframes.series_kernels._mean_handle_nan(dtj__zuyjt,
            slcie__hmtop)
        bndat__lqg = dvkx__bmo
        for tazsb__mvow in numba.parfors.parfor.internal_prange(len(A)):
            cwxw__vqg = dvkx__bmo
            if not bodo.libs.array_kernels.isna(A, tazsb__mvow) or not skipna:
                cwxw__vqg = abs(A[tazsb__mvow] - ery__hmr)
            bndat__lqg += cwxw__vqg
        mwzl__vke = bodo.hiframes.series_kernels._mean_handle_nan(bndat__lqg,
            slcie__hmtop)
        return mwzl__vke
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    xci__flkyz = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', xci__flkyz, mldpl__xnwz,
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
        woy__jvgk = 0
        xeo__flvbj = 0
        slcie__hmtop = 0
        for tazsb__mvow in numba.parfors.parfor.internal_prange(len(A)):
            cwxw__vqg = 0
            xwvrq__dkq = 0
            if not bodo.libs.array_kernels.isna(A, tazsb__mvow) or not skipna:
                cwxw__vqg = A[tazsb__mvow]
                xwvrq__dkq = 1
            woy__jvgk += cwxw__vqg
            xeo__flvbj += cwxw__vqg * cwxw__vqg
            slcie__hmtop += xwvrq__dkq
        xzcul__zyk = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            woy__jvgk, xeo__flvbj, slcie__hmtop, ddof)
        ehfa__igfqn = bodo.hiframes.series_kernels._sem_handle_nan(xzcul__zyk,
            slcie__hmtop)
        return ehfa__igfqn
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    xci__flkyz = dict(level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', xci__flkyz, mldpl__xnwz,
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
        woy__jvgk = 0.0
        xeo__flvbj = 0.0
        madeu__ialk = 0.0
        cwycz__vtn = 0.0
        slcie__hmtop = 0
        for tazsb__mvow in numba.parfors.parfor.internal_prange(len(A)):
            cwxw__vqg = 0.0
            xwvrq__dkq = 0
            if not bodo.libs.array_kernels.isna(A, tazsb__mvow) or not skipna:
                cwxw__vqg = np.float64(A[tazsb__mvow])
                xwvrq__dkq = 1
            woy__jvgk += cwxw__vqg
            xeo__flvbj += cwxw__vqg ** 2
            madeu__ialk += cwxw__vqg ** 3
            cwycz__vtn += cwxw__vqg ** 4
            slcie__hmtop += xwvrq__dkq
        xzcul__zyk = bodo.hiframes.series_kernels.compute_kurt(woy__jvgk,
            xeo__flvbj, madeu__ialk, cwycz__vtn, slcie__hmtop)
        return xzcul__zyk
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    xci__flkyz = dict(level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', xci__flkyz, mldpl__xnwz,
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
        woy__jvgk = 0.0
        xeo__flvbj = 0.0
        madeu__ialk = 0.0
        slcie__hmtop = 0
        for tazsb__mvow in numba.parfors.parfor.internal_prange(len(A)):
            cwxw__vqg = 0.0
            xwvrq__dkq = 0
            if not bodo.libs.array_kernels.isna(A, tazsb__mvow) or not skipna:
                cwxw__vqg = np.float64(A[tazsb__mvow])
                xwvrq__dkq = 1
            woy__jvgk += cwxw__vqg
            xeo__flvbj += cwxw__vqg ** 2
            madeu__ialk += cwxw__vqg ** 3
            slcie__hmtop += xwvrq__dkq
        xzcul__zyk = bodo.hiframes.series_kernels.compute_skew(woy__jvgk,
            xeo__flvbj, madeu__ialk, slcie__hmtop)
        return xzcul__zyk
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    xci__flkyz = dict(level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', xci__flkyz, mldpl__xnwz,
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
        ewmpc__tmn = bodo.hiframes.pd_series_ext.get_series_data(S)
        oftcc__ffzu = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        afrcl__gbmx = 0
        for tazsb__mvow in numba.parfors.parfor.internal_prange(len(ewmpc__tmn)
            ):
            tmn__zncmq = ewmpc__tmn[tazsb__mvow]
            ayej__dte = oftcc__ffzu[tazsb__mvow]
            afrcl__gbmx += tmn__zncmq * ayej__dte
        return afrcl__gbmx
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    xci__flkyz = dict(skipna=skipna)
    mldpl__xnwz = dict(skipna=True)
    check_unsupported_args('Series.cumsum', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(skipna=skipna)
    mldpl__xnwz = dict(skipna=True)
    check_unsupported_args('Series.cumprod', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(skipna=skipna)
    mldpl__xnwz = dict(skipna=True)
    check_unsupported_args('Series.cummin', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(skipna=skipna)
    mldpl__xnwz = dict(skipna=True)
    check_unsupported_args('Series.cummax', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    mldpl__xnwz = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        cgm__hrycg = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, cgm__hrycg, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    xci__flkyz = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    mldpl__xnwz = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(level=level)
    mldpl__xnwz = dict(level=None)
    check_unsupported_args('Series.count', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    xci__flkyz = dict(method=method, min_periods=min_periods)
    mldpl__xnwz = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        kfzl__smbk = S.sum()
        qevmp__fdyep = other.sum()
        a = n * (S * other).sum() - kfzl__smbk * qevmp__fdyep
        eikz__lcgnf = n * (S ** 2).sum() - kfzl__smbk ** 2
        itk__qqn = n * (other ** 2).sum() - qevmp__fdyep ** 2
        return a / np.sqrt(eikz__lcgnf * itk__qqn)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    xci__flkyz = dict(min_periods=min_periods)
    mldpl__xnwz = dict(min_periods=None)
    check_unsupported_args('Series.cov', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        kfzl__smbk = S.mean()
        qevmp__fdyep = other.mean()
        xmch__abstf = ((S - kfzl__smbk) * (other - qevmp__fdyep)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(xmch__abstf, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            lrvr__pbx = np.sign(sum_val)
            return np.inf * lrvr__pbx
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    xci__flkyz = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(axis=axis, skipna=skipna)
    mldpl__xnwz = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(axis=axis, skipna=skipna)
    mldpl__xnwz = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', xci__flkyz, mldpl__xnwz,
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
    xci__flkyz = dict(level=level, numeric_only=numeric_only)
    mldpl__xnwz = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', xci__flkyz, mldpl__xnwz,
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
        npd__fgxm = arr[:n]
        xkw__fzvz = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(npd__fgxm, xkw__fzvz,
            name)
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
        tffm__rfpo = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        npd__fgxm = arr[tffm__rfpo:]
        xkw__fzvz = index[tffm__rfpo:]
        return bodo.hiframes.pd_series_ext.init_series(npd__fgxm, xkw__fzvz,
            name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    ldbij__ahosu = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ldbij__ahosu:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            neldn__fme = index[0]
            qke__rhfek = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                neldn__fme, False))
        else:
            qke__rhfek = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        npd__fgxm = arr[:qke__rhfek]
        xkw__fzvz = index[:qke__rhfek]
        return bodo.hiframes.pd_series_ext.init_series(npd__fgxm, xkw__fzvz,
            name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    ldbij__ahosu = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ldbij__ahosu:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            exp__qtf = index[-1]
            qke__rhfek = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, exp__qtf,
                True))
        else:
            qke__rhfek = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        npd__fgxm = arr[len(arr) - qke__rhfek:]
        xkw__fzvz = index[len(arr) - qke__rhfek:]
        return bodo.hiframes.pd_series_ext.init_series(npd__fgxm, xkw__fzvz,
            name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        dimgb__iyfy = bodo.utils.conversion.index_to_array(index)
        fanfz__grrib, jgcx__oajwt = (bodo.libs.array_kernels.
            first_last_valid_index(arr, dimgb__iyfy))
        return jgcx__oajwt if fanfz__grrib else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        dimgb__iyfy = bodo.utils.conversion.index_to_array(index)
        fanfz__grrib, jgcx__oajwt = (bodo.libs.array_kernels.
            first_last_valid_index(arr, dimgb__iyfy, False))
        return jgcx__oajwt if fanfz__grrib else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    xci__flkyz = dict(keep=keep)
    mldpl__xnwz = dict(keep='first')
    check_unsupported_args('Series.nlargest', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        dimgb__iyfy = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wkfhu__uqi, bgyd__axnnr = bodo.libs.array_kernels.nlargest(arr,
            dimgb__iyfy, n, True, bodo.hiframes.series_kernels.gt_f)
        zvc__zur = bodo.utils.conversion.convert_to_index(bgyd__axnnr)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, zvc__zur,
            name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    xci__flkyz = dict(keep=keep)
    mldpl__xnwz = dict(keep='first')
    check_unsupported_args('Series.nsmallest', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        dimgb__iyfy = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wkfhu__uqi, bgyd__axnnr = bodo.libs.array_kernels.nlargest(arr,
            dimgb__iyfy, n, False, bodo.hiframes.series_kernels.lt_f)
        zvc__zur = bodo.utils.conversion.convert_to_index(bgyd__axnnr)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, zvc__zur,
            name)
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
    xci__flkyz = dict(errors=errors)
    mldpl__xnwz = dict(errors='raise')
    check_unsupported_args('Series.astype', xci__flkyz, mldpl__xnwz,
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
        wkfhu__uqi = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    xci__flkyz = dict(axis=axis, is_copy=is_copy)
    mldpl__xnwz = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        bzlq__lyecu = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[bzlq__lyecu],
            index[bzlq__lyecu], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    xci__flkyz = dict(axis=axis, kind=kind, order=order)
    mldpl__xnwz = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        owwsd__qkgrs = S.notna().values
        if not owwsd__qkgrs.all():
            wkfhu__uqi = np.full(n, -1, np.int64)
            wkfhu__uqi[owwsd__qkgrs] = argsort(arr[owwsd__qkgrs])
        else:
            wkfhu__uqi = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    xci__flkyz = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    mldpl__xnwz = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', xci__flkyz, mldpl__xnwz,
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
        ntcqr__snn = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        ajko__fzuxp = ntcqr__snn.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        wkfhu__uqi = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            ajko__fzuxp, 0)
        zvc__zur = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            ajko__fzuxp)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, zvc__zur,
            name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    xci__flkyz = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    mldpl__xnwz = dict(axis=0, inplace=False, kind='quicksort',
        ignore_index=False, key=None)
    check_unsupported_args('Series.sort_values', xci__flkyz, mldpl__xnwz,
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
        ntcqr__snn = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        ajko__fzuxp = ntcqr__snn.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        wkfhu__uqi = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            ajko__fzuxp, 0)
        zvc__zur = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            ajko__fzuxp)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, zvc__zur,
            name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    jgn__gegiw = is_overload_true(is_nullable)
    jpf__wcv = 'def impl(bins, arr, is_nullable=True, include_lowest=True):\n'
    jpf__wcv += '  numba.parfors.parfor.init_prange()\n'
    jpf__wcv += '  n = len(arr)\n'
    if jgn__gegiw:
        jpf__wcv += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        jpf__wcv += '  out_arr = np.empty(n, np.int64)\n'
    jpf__wcv += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    jpf__wcv += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if jgn__gegiw:
        jpf__wcv += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        jpf__wcv += '      out_arr[i] = -1\n'
    jpf__wcv += '      continue\n'
    jpf__wcv += '    val = arr[i]\n'
    jpf__wcv += '    if include_lowest and val == bins[0]:\n'
    jpf__wcv += '      ind = 1\n'
    jpf__wcv += '    else:\n'
    jpf__wcv += '      ind = np.searchsorted(bins, val)\n'
    jpf__wcv += '    if ind == 0 or ind == len(bins):\n'
    if jgn__gegiw:
        jpf__wcv += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        jpf__wcv += '      out_arr[i] = -1\n'
    jpf__wcv += '    else:\n'
    jpf__wcv += '      out_arr[i] = ind - 1\n'
    jpf__wcv += '  return out_arr\n'
    hfkvs__ogzi = {}
    exec(jpf__wcv, {'bodo': bodo, 'np': np, 'numba': numba}, hfkvs__ogzi)
    impl = hfkvs__ogzi['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        kqgia__vyb, rmraj__jakf = np.divmod(x, 1)
        if kqgia__vyb == 0:
            bunv__jxjjj = -int(np.floor(np.log10(abs(rmraj__jakf)))
                ) - 1 + precision
        else:
            bunv__jxjjj = precision
        return np.around(x, bunv__jxjjj)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        iki__rfoi = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(iki__rfoi)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        lnkfy__crxx = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            hav__drm = bins.copy()
            if right and include_lowest:
                hav__drm[0] = hav__drm[0] - lnkfy__crxx
            frur__pgdk = bodo.libs.interval_arr_ext.init_interval_array(
                hav__drm[:-1], hav__drm[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(frur__pgdk,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        hav__drm = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            hav__drm[0] = hav__drm[0] - 10.0 ** -precision
        frur__pgdk = bodo.libs.interval_arr_ext.init_interval_array(hav__drm
            [:-1], hav__drm[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(frur__pgdk, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        dlwmk__rcmf = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        mtgp__srcm = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        wkfhu__uqi = np.zeros(nbins, np.int64)
        for tazsb__mvow in range(len(dlwmk__rcmf)):
            wkfhu__uqi[mtgp__srcm[tazsb__mvow]] = dlwmk__rcmf[tazsb__mvow]
        return wkfhu__uqi
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
            gfcga__vus = (max_val - min_val) * 0.001
            if right:
                bins[0] -= gfcga__vus
            else:
                bins[-1] += gfcga__vus
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    xci__flkyz = dict(dropna=dropna)
    mldpl__xnwz = dict(dropna=True)
    check_unsupported_args('Series.value_counts', xci__flkyz, mldpl__xnwz,
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
    uvmo__cqwdz = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    jpf__wcv = 'def impl(\n'
    jpf__wcv += '    S,\n'
    jpf__wcv += '    normalize=False,\n'
    jpf__wcv += '    sort=True,\n'
    jpf__wcv += '    ascending=False,\n'
    jpf__wcv += '    bins=None,\n'
    jpf__wcv += '    dropna=True,\n'
    jpf__wcv += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    jpf__wcv += '):\n'
    jpf__wcv += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    jpf__wcv += '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    jpf__wcv += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if uvmo__cqwdz:
        jpf__wcv += '    right = True\n'
        jpf__wcv += _gen_bins_handling(bins, S.dtype)
        jpf__wcv += '    arr = get_bin_inds(bins, arr)\n'
    jpf__wcv += '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n'
    jpf__wcv += "        (arr,), index, ('$_bodo_col2_',)\n"
    jpf__wcv += '    )\n'
    jpf__wcv += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if uvmo__cqwdz:
        jpf__wcv += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        jpf__wcv += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        jpf__wcv += '    index = get_bin_labels(bins)\n'
    else:
        jpf__wcv += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        jpf__wcv += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        jpf__wcv += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        jpf__wcv += '    )\n'
        jpf__wcv += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    jpf__wcv += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        jpf__wcv += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        gof__hwcq = 'len(S)' if uvmo__cqwdz else 'count_arr.sum()'
        jpf__wcv += f'    res = res / float({gof__hwcq})\n'
    jpf__wcv += '    return res\n'
    hfkvs__ogzi = {}
    exec(jpf__wcv, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, hfkvs__ogzi)
    impl = hfkvs__ogzi['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    jpf__wcv = ''
    if isinstance(bins, types.Integer):
        jpf__wcv += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        jpf__wcv += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            jpf__wcv += '    min_val = min_val.value\n'
            jpf__wcv += '    max_val = max_val.value\n'
        jpf__wcv += '    bins = compute_bins(bins, min_val, max_val, right)\n'
        if dtype == bodo.datetime64ns:
            jpf__wcv += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        jpf__wcv += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return jpf__wcv


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    xci__flkyz = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    mldpl__xnwz = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    jpf__wcv = 'def impl(\n'
    jpf__wcv += '    x,\n'
    jpf__wcv += '    bins,\n'
    jpf__wcv += '    right=True,\n'
    jpf__wcv += '    labels=None,\n'
    jpf__wcv += '    retbins=False,\n'
    jpf__wcv += '    precision=3,\n'
    jpf__wcv += '    include_lowest=False,\n'
    jpf__wcv += "    duplicates='raise',\n"
    jpf__wcv += '    ordered=True\n'
    jpf__wcv += '):\n'
    if isinstance(x, SeriesType):
        jpf__wcv += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        jpf__wcv += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        jpf__wcv += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        jpf__wcv += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    jpf__wcv += _gen_bins_handling(bins, x.dtype)
    jpf__wcv += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    jpf__wcv += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    jpf__wcv += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    jpf__wcv += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        jpf__wcv += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        jpf__wcv += '    return res\n'
    else:
        jpf__wcv += '    return out_arr\n'
    hfkvs__ogzi = {}
    exec(jpf__wcv, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, hfkvs__ogzi)
    impl = hfkvs__ogzi['impl']
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
    xci__flkyz = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    mldpl__xnwz = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        dbyaa__khgif = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, dbyaa__khgif)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    xci__flkyz = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    mldpl__xnwz = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', xci__flkyz, mldpl__xnwz,
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
            xcm__xpou = bodo.utils.conversion.coerce_to_array(index)
            ntcqr__snn = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                xcm__xpou, arr), index, (' ', ''))
            return ntcqr__snn.groupby(' ')['']
        return impl_index
    awf__ywy = by
    if isinstance(by, SeriesType):
        awf__ywy = by.data
    if isinstance(awf__ywy, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        xcm__xpou = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        ntcqr__snn = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            xcm__xpou, arr), index, (' ', ''))
        return ntcqr__snn.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    xci__flkyz = dict(verify_integrity=verify_integrity)
    mldpl__xnwz = dict(verify_integrity=False)
    check_unsupported_args('Series.append', xci__flkyz, mldpl__xnwz,
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
            hxhq__wgr = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            wkfhu__uqi = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(wkfhu__uqi, A, hxhq__wgr, False)
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wkfhu__uqi = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    xci__flkyz = dict(interpolation=interpolation)
    mldpl__xnwz = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            wkfhu__uqi = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
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
        pbvfa__gchql = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(pbvfa__gchql, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    xci__flkyz = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    mldpl__xnwz = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', xci__flkyz, mldpl__xnwz,
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
        uoag__xhdcy = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        uoag__xhdcy = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    jpf__wcv = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {uoag__xhdcy}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    rsdk__vayx = dict()
    exec(jpf__wcv, {'bodo': bodo, 'numba': numba}, rsdk__vayx)
    nrc__upuw = rsdk__vayx['impl']
    return nrc__upuw


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        uoag__xhdcy = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        uoag__xhdcy = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    jpf__wcv = 'def impl(S,\n'
    jpf__wcv += '     value=None,\n'
    jpf__wcv += '    method=None,\n'
    jpf__wcv += '    axis=None,\n'
    jpf__wcv += '    inplace=False,\n'
    jpf__wcv += '    limit=None,\n'
    jpf__wcv += '   downcast=None,\n'
    jpf__wcv += '):\n'
    jpf__wcv += '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    jpf__wcv += '    n = len(in_arr)\n'
    jpf__wcv += f'    out_arr = {uoag__xhdcy}(n, -1)\n'
    jpf__wcv += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    jpf__wcv += '        s = in_arr[j]\n'
    jpf__wcv += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    jpf__wcv += '            s = value\n'
    jpf__wcv += '        out_arr[j] = s\n'
    jpf__wcv += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    rsdk__vayx = dict()
    exec(jpf__wcv, {'bodo': bodo, 'numba': numba}, rsdk__vayx)
    nrc__upuw = rsdk__vayx['impl']
    return nrc__upuw


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
    nky__yxmox = bodo.hiframes.pd_series_ext.get_series_data(value)
    for tazsb__mvow in numba.parfors.parfor.internal_prange(len(kvfo__pudn)):
        s = kvfo__pudn[tazsb__mvow]
        if bodo.libs.array_kernels.isna(kvfo__pudn, tazsb__mvow
            ) and not bodo.libs.array_kernels.isna(nky__yxmox, tazsb__mvow):
            s = nky__yxmox[tazsb__mvow]
        kvfo__pudn[tazsb__mvow] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
    for tazsb__mvow in numba.parfors.parfor.internal_prange(len(kvfo__pudn)):
        s = kvfo__pudn[tazsb__mvow]
        if bodo.libs.array_kernels.isna(kvfo__pudn, tazsb__mvow):
            s = value
        kvfo__pudn[tazsb__mvow] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    nky__yxmox = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(kvfo__pudn)
    wkfhu__uqi = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for zrj__tie in numba.parfors.parfor.internal_prange(n):
        s = kvfo__pudn[zrj__tie]
        if bodo.libs.array_kernels.isna(kvfo__pudn, zrj__tie
            ) and not bodo.libs.array_kernels.isna(nky__yxmox, zrj__tie):
            s = nky__yxmox[zrj__tie]
        wkfhu__uqi[zrj__tie] = s
        if bodo.libs.array_kernels.isna(kvfo__pudn, zrj__tie
            ) and bodo.libs.array_kernels.isna(nky__yxmox, zrj__tie):
            bodo.libs.array_kernels.setna(wkfhu__uqi, zrj__tie)
    return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    nky__yxmox = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(kvfo__pudn)
    wkfhu__uqi = bodo.utils.utils.alloc_type(n, kvfo__pudn.dtype, (-1,))
    for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
        s = kvfo__pudn[tazsb__mvow]
        if bodo.libs.array_kernels.isna(kvfo__pudn, tazsb__mvow
            ) and not bodo.libs.array_kernels.isna(nky__yxmox, tazsb__mvow):
            s = nky__yxmox[tazsb__mvow]
        wkfhu__uqi[tazsb__mvow] = s
    return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    xci__flkyz = dict(limit=limit, downcast=downcast)
    mldpl__xnwz = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', xci__flkyz, mldpl__xnwz,
        package_name='pandas', module_name='Series')
    tjaai__inex = not is_overload_none(value)
    jlby__zgxer = not is_overload_none(method)
    if tjaai__inex and jlby__zgxer:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not tjaai__inex and not jlby__zgxer:
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
    if jlby__zgxer:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        liq__fcrs = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(liq__fcrs)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(liq__fcrs)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    jxoa__geel = element_type(S.data)
    ybv__tyajj = None
    if tjaai__inex:
        ybv__tyajj = element_type(types.unliteral(value))
    if ybv__tyajj and not can_replace(jxoa__geel, ybv__tyajj):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {ybv__tyajj} with series type {jxoa__geel}'
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
        ljd__uotye = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                nky__yxmox = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(kvfo__pudn)
                wkfhu__uqi = bodo.utils.utils.alloc_type(n, ljd__uotye, (-1,))
                for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(kvfo__pudn, tazsb__mvow
                        ) and bodo.libs.array_kernels.isna(nky__yxmox,
                        tazsb__mvow):
                        bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
                        continue
                    if bodo.libs.array_kernels.isna(kvfo__pudn, tazsb__mvow):
                        wkfhu__uqi[tazsb__mvow
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            nky__yxmox[tazsb__mvow])
                        continue
                    wkfhu__uqi[tazsb__mvow
                        ] = bodo.utils.conversion.unbox_if_timestamp(kvfo__pudn
                        [tazsb__mvow])
                return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                    index, name)
            return fillna_series_impl
        if jlby__zgxer:
            zqwth__ywhqp = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(jxoa__geel, (types.Integer, types.Float)
                ) and jxoa__geel not in zqwth__ywhqp:
                raise BodoError(
                    f"Series.fillna(): series of type {jxoa__geel} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                wkfhu__uqi = bodo.libs.array_kernels.ffill_bfill_arr(kvfo__pudn
                    , method)
                return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(kvfo__pudn)
            wkfhu__uqi = bodo.utils.utils.alloc_type(n, ljd__uotye, (-1,))
            for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(kvfo__pudn[
                    tazsb__mvow])
                if bodo.libs.array_kernels.isna(kvfo__pudn, tazsb__mvow):
                    s = value
                wkfhu__uqi[tazsb__mvow] = s
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        vaxuo__dldx = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        xci__flkyz = dict(limit=limit, downcast=downcast)
        mldpl__xnwz = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', xci__flkyz,
            mldpl__xnwz, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        jxoa__geel = element_type(S.data)
        zqwth__ywhqp = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(jxoa__geel, (types.Integer, types.Float)
            ) and jxoa__geel not in zqwth__ywhqp:
            raise BodoError(
                f'Series.{overload_name}(): series of type {jxoa__geel} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            wkfhu__uqi = bodo.libs.array_kernels.ffill_bfill_arr(kvfo__pudn,
                vaxuo__dldx)
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        zdxpg__kha = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            zdxpg__kha)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        zxb__ywl = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(zxb__ywl)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        zxb__ywl = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(zxb__ywl)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        zxb__ywl = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(zxb__ywl)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    xci__flkyz = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    dqw__ygy = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', xci__flkyz, dqw__ygy,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    jxoa__geel = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        lqk__cadku = element_type(to_replace.key_type)
        ybv__tyajj = element_type(to_replace.value_type)
    else:
        lqk__cadku = element_type(to_replace)
        ybv__tyajj = element_type(value)
    kqnox__zfbjg = None
    if jxoa__geel != types.unliteral(lqk__cadku):
        if bodo.utils.typing.equality_always_false(jxoa__geel, types.
            unliteral(lqk__cadku)
            ) or not bodo.utils.typing.types_equality_exists(jxoa__geel,
            lqk__cadku):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(jxoa__geel, (types.Float, types.Integer)
            ) or jxoa__geel == np.bool_:
            kqnox__zfbjg = jxoa__geel
    if not can_replace(jxoa__geel, types.unliteral(ybv__tyajj)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    yop__cpsvb = to_str_arr_if_dict_array(S.data)
    if isinstance(yop__cpsvb, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(kvfo__pudn.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(kvfo__pudn)
        wkfhu__uqi = bodo.utils.utils.alloc_type(n, yop__cpsvb, (-1,))
        syp__dvftz = build_replace_dict(to_replace, value, kqnox__zfbjg)
        for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(kvfo__pudn, tazsb__mvow):
                bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
                continue
            s = kvfo__pudn[tazsb__mvow]
            if s in syp__dvftz:
                s = syp__dvftz[s]
            wkfhu__uqi[tazsb__mvow] = s
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    embkr__fdu = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    hdy__pph = is_iterable_type(to_replace)
    hsq__chsr = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    ogco__xchw = is_iterable_type(value)
    if embkr__fdu and hsq__chsr:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                syp__dvftz = {}
                syp__dvftz[key_dtype_conv(to_replace)] = value
                return syp__dvftz
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            syp__dvftz = {}
            syp__dvftz[to_replace] = value
            return syp__dvftz
        return impl
    if hdy__pph and hsq__chsr:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                syp__dvftz = {}
                for gqd__yyao in to_replace:
                    syp__dvftz[key_dtype_conv(gqd__yyao)] = value
                return syp__dvftz
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            syp__dvftz = {}
            for gqd__yyao in to_replace:
                syp__dvftz[gqd__yyao] = value
            return syp__dvftz
        return impl
    if hdy__pph and ogco__xchw:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                syp__dvftz = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for tazsb__mvow in range(len(to_replace)):
                    syp__dvftz[key_dtype_conv(to_replace[tazsb__mvow])
                        ] = value[tazsb__mvow]
                return syp__dvftz
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            syp__dvftz = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for tazsb__mvow in range(len(to_replace)):
                syp__dvftz[to_replace[tazsb__mvow]] = value[tazsb__mvow]
            return syp__dvftz
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
            wkfhu__uqi = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wkfhu__uqi = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    xci__flkyz = dict(ignore_index=ignore_index)
    ybnaz__recl = dict(ignore_index=False)
    check_unsupported_args('Series.explode', xci__flkyz, ybnaz__recl,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        dimgb__iyfy = bodo.utils.conversion.index_to_array(index)
        wkfhu__uqi, qejz__ojikv = bodo.libs.array_kernels.explode(arr,
            dimgb__iyfy)
        zvc__zur = bodo.utils.conversion.index_from_array(qejz__ojikv)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, zvc__zur,
            name)
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
            ljup__lkik = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                ljup__lkik[tazsb__mvow] = np.argmax(a[tazsb__mvow])
            return ljup__lkik
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            zbn__dgjt = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                zbn__dgjt[tazsb__mvow] = np.argmin(a[tazsb__mvow])
            return zbn__dgjt
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
    xci__flkyz = dict(axis=axis, inplace=inplace, how=how)
    kom__wtfx = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', xci__flkyz, kom__wtfx,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            owwsd__qkgrs = S.notna().values
            dimgb__iyfy = bodo.utils.conversion.extract_index_array(S)
            zvc__zur = bodo.utils.conversion.convert_to_index(dimgb__iyfy[
                owwsd__qkgrs])
            wkfhu__uqi = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(kvfo__pudn))
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                zvc__zur, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            dimgb__iyfy = bodo.utils.conversion.extract_index_array(S)
            owwsd__qkgrs = S.notna().values
            zvc__zur = bodo.utils.conversion.convert_to_index(dimgb__iyfy[
                owwsd__qkgrs])
            wkfhu__uqi = kvfo__pudn[owwsd__qkgrs]
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                zvc__zur, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    xci__flkyz = dict(freq=freq, axis=axis, fill_value=fill_value)
    mldpl__xnwz = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', xci__flkyz, mldpl__xnwz,
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
        wkfhu__uqi = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    xci__flkyz = dict(fill_method=fill_method, limit=limit, freq=freq)
    mldpl__xnwz = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', xci__flkyz, mldpl__xnwz,
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
        wkfhu__uqi = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
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
            bob__umkz = 'None'
        else:
            bob__umkz = 'other'
        jpf__wcv = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            jpf__wcv += '  cond = ~cond\n'
        jpf__wcv += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        jpf__wcv += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        jpf__wcv += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
        jpf__wcv += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {bob__umkz})\n'
            )
        jpf__wcv += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        hfkvs__ogzi = {}
        exec(jpf__wcv, {'bodo': bodo, 'np': np}, hfkvs__ogzi)
        impl = hfkvs__ogzi['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        zdxpg__kha = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(zdxpg__kha)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    xci__flkyz = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    mldpl__xnwz = dict(inplace=False, level=None, errors='raise', try_cast=
        False)
    check_unsupported_args(f'{func_name}', xci__flkyz, mldpl__xnwz,
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
    mkoft__tpevm = is_overload_constant_nan(other)
    if not (is_default or mkoft__tpevm or is_scalar_type(other) or 
        isinstance(other, types.Array) and other.ndim >= 1 and other.ndim <=
        max_ndim or isinstance(other, SeriesType) and (isinstance(arr,
        types.Array) or arr.dtype in [bodo.string_type, bodo.bytes_type]) or
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
            wst__ayzgq = arr.dtype.elem_type
        else:
            wst__ayzgq = arr.dtype
        if is_iterable_type(other):
            mgkk__xbq = other.dtype
        elif mkoft__tpevm:
            mgkk__xbq = types.float64
        else:
            mgkk__xbq = types.unliteral(other)
        if not mkoft__tpevm and not is_common_scalar_dtype([wst__ayzgq,
            mgkk__xbq]):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        xci__flkyz = dict(level=level, axis=axis)
        mldpl__xnwz = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), xci__flkyz,
            mldpl__xnwz, package_name='pandas', module_name='Series')
        taa__bncyg = other == string_type or is_overload_constant_str(other)
        hqs__ehtd = is_iterable_type(other) and other.dtype == string_type
        oyvlx__thl = S.dtype == string_type and (op == operator.add and (
            taa__bncyg or hqs__ehtd) or op == operator.mul and isinstance(
            other, types.Integer))
        zqr__fdthf = S.dtype == bodo.timedelta64ns
        gmhc__kazn = S.dtype == bodo.datetime64ns
        hfxev__htm = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        ruxsv__knpz = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        juvog__vtu = zqr__fdthf and (hfxev__htm or ruxsv__knpz
            ) or gmhc__kazn and hfxev__htm
        juvog__vtu = juvog__vtu and op == operator.add
        if not (isinstance(S.dtype, types.Number) or oyvlx__thl or juvog__vtu):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        www__annj = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            yop__cpsvb = www__annj.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and yop__cpsvb == types.Array(types.bool_, 1, 'C'):
                yop__cpsvb = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                wkfhu__uqi = bodo.utils.utils.alloc_type(n, yop__cpsvb, (-1,))
                for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                    ysz__kpkhv = bodo.libs.array_kernels.isna(arr, tazsb__mvow)
                    if ysz__kpkhv:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(wkfhu__uqi,
                                tazsb__mvow)
                        else:
                            wkfhu__uqi[tazsb__mvow] = op(fill_value, other)
                    else:
                        wkfhu__uqi[tazsb__mvow] = op(arr[tazsb__mvow], other)
                return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        yop__cpsvb = www__annj.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and yop__cpsvb == types.Array(
            types.bool_, 1, 'C'):
            yop__cpsvb = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            puskz__tpzsj = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            wkfhu__uqi = bodo.utils.utils.alloc_type(n, yop__cpsvb, (-1,))
            for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                ysz__kpkhv = bodo.libs.array_kernels.isna(arr, tazsb__mvow)
                rzj__puq = bodo.libs.array_kernels.isna(puskz__tpzsj,
                    tazsb__mvow)
                if ysz__kpkhv and rzj__puq:
                    bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
                elif ysz__kpkhv:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
                    else:
                        wkfhu__uqi[tazsb__mvow] = op(fill_value,
                            puskz__tpzsj[tazsb__mvow])
                elif rzj__puq:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
                    else:
                        wkfhu__uqi[tazsb__mvow] = op(arr[tazsb__mvow],
                            fill_value)
                else:
                    wkfhu__uqi[tazsb__mvow] = op(arr[tazsb__mvow],
                        puskz__tpzsj[tazsb__mvow])
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
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
        www__annj = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            yop__cpsvb = www__annj.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and yop__cpsvb == types.Array(types.bool_, 1, 'C'):
                yop__cpsvb = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                wkfhu__uqi = bodo.utils.utils.alloc_type(n, yop__cpsvb, None)
                for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                    ysz__kpkhv = bodo.libs.array_kernels.isna(arr, tazsb__mvow)
                    if ysz__kpkhv:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(wkfhu__uqi,
                                tazsb__mvow)
                        else:
                            wkfhu__uqi[tazsb__mvow] = op(other, fill_value)
                    else:
                        wkfhu__uqi[tazsb__mvow] = op(other, arr[tazsb__mvow])
                return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        yop__cpsvb = www__annj.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and yop__cpsvb == types.Array(
            types.bool_, 1, 'C'):
            yop__cpsvb = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            puskz__tpzsj = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            wkfhu__uqi = bodo.utils.utils.alloc_type(n, yop__cpsvb, None)
            for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                ysz__kpkhv = bodo.libs.array_kernels.isna(arr, tazsb__mvow)
                rzj__puq = bodo.libs.array_kernels.isna(puskz__tpzsj,
                    tazsb__mvow)
                wkfhu__uqi[tazsb__mvow] = op(puskz__tpzsj[tazsb__mvow], arr
                    [tazsb__mvow])
                if ysz__kpkhv and rzj__puq:
                    bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
                elif ysz__kpkhv:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
                    else:
                        wkfhu__uqi[tazsb__mvow] = op(puskz__tpzsj[
                            tazsb__mvow], fill_value)
                elif rzj__puq:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
                    else:
                        wkfhu__uqi[tazsb__mvow] = op(fill_value, arr[
                            tazsb__mvow])
                else:
                    wkfhu__uqi[tazsb__mvow] = op(puskz__tpzsj[tazsb__mvow],
                        arr[tazsb__mvow])
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
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
    for op, jakhj__qjpdq in explicit_binop_funcs_two_ways.items():
        for name in jakhj__qjpdq:
            zdxpg__kha = create_explicit_binary_op_overload(op)
            tmu__kzn = create_explicit_binary_reverse_op_overload(op)
            wnpnl__nmo = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(zdxpg__kha)
            overload_method(SeriesType, wnpnl__nmo, no_unliteral=True)(tmu__kzn
                )
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        zdxpg__kha = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(zdxpg__kha)
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
                rkvqa__wzbpz = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                wkfhu__uqi = dt64_arr_sub(arr, rkvqa__wzbpz)
                return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
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
                wkfhu__uqi = np.empty(n, np.dtype('datetime64[ns]'))
                for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, tazsb__mvow):
                        bodo.libs.array_kernels.setna(wkfhu__uqi, tazsb__mvow)
                        continue
                    rcnj__xywm = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[tazsb__mvow]))
                    eua__szdpn = op(rcnj__xywm, rhs)
                    wkfhu__uqi[tazsb__mvow
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        eua__szdpn.value)
                return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
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
                    rkvqa__wzbpz = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    wkfhu__uqi = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(rkvqa__wzbpz))
                    return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rkvqa__wzbpz = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                wkfhu__uqi = op(arr, rkvqa__wzbpz)
                return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    badyb__wcn = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    wkfhu__uqi = op(bodo.utils.conversion.
                        unbox_if_timestamp(badyb__wcn), arr)
                    return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                badyb__wcn = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                wkfhu__uqi = op(badyb__wcn, arr)
                return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        zdxpg__kha = create_binary_op_overload(op)
        overload(op)(zdxpg__kha)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    esdx__dok = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, esdx__dok)
        for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, tazsb__mvow
                ) or bodo.libs.array_kernels.isna(arg2, tazsb__mvow):
                bodo.libs.array_kernels.setna(S, tazsb__mvow)
                continue
            S[tazsb__mvow
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                tazsb__mvow]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[tazsb__mvow]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                puskz__tpzsj = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, puskz__tpzsj)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        zdxpg__kha = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(zdxpg__kha)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                wkfhu__uqi = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        zdxpg__kha = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(zdxpg__kha)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    wkfhu__uqi = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
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
                    puskz__tpzsj = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    wkfhu__uqi = ufunc(arr, puskz__tpzsj)
                    return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    puskz__tpzsj = bodo.hiframes.pd_series_ext.get_series_data(
                        S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    wkfhu__uqi = ufunc(arr, puskz__tpzsj)
                    return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        zdxpg__kha = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(zdxpg__kha)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        lctd__eyhs = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),)
            )
        sbwn__rrd = np.arange(n),
        bodo.libs.timsort.sort(lctd__eyhs, 0, n, sbwn__rrd)
        return sbwn__rrd[0]
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
        uuudw__nyhlg = get_overload_const_str(downcast)
        if uuudw__nyhlg in ('integer', 'signed'):
            out_dtype = types.int64
        elif uuudw__nyhlg == 'unsigned':
            out_dtype = types.uint64
        else:
            assert uuudw__nyhlg == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            kvfo__pudn = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            wkfhu__uqi = pd.to_numeric(kvfo__pudn, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            kyls__hfa = np.empty(n, np.float64)
            for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, tazsb__mvow):
                    bodo.libs.array_kernels.setna(kyls__hfa, tazsb__mvow)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(kyls__hfa,
                        tazsb__mvow, arg_a, tazsb__mvow)
            return kyls__hfa
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            kyls__hfa = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, tazsb__mvow):
                    bodo.libs.array_kernels.setna(kyls__hfa, tazsb__mvow)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(kyls__hfa,
                        tazsb__mvow, arg_a, tazsb__mvow)
            return kyls__hfa
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        ijz__rpc = if_series_to_array_type(args[0])
        if isinstance(ijz__rpc, types.Array) and isinstance(ijz__rpc.dtype,
            types.Integer):
            ijz__rpc = types.Array(types.float64, 1, 'C')
        return ijz__rpc(*args)


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
    hizb__mmop = bodo.utils.utils.is_array_typ(x, True)
    uiu__bfx = bodo.utils.utils.is_array_typ(y, True)
    jpf__wcv = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        jpf__wcv += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if hizb__mmop and not bodo.utils.utils.is_array_typ(x, False):
        jpf__wcv += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if uiu__bfx and not bodo.utils.utils.is_array_typ(y, False):
        jpf__wcv += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    jpf__wcv += '  n = len(condition)\n'
    ylhgb__isiz = x.dtype if hizb__mmop else types.unliteral(x)
    slr__imzm = y.dtype if uiu__bfx else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        ylhgb__isiz = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        slr__imzm = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    pybg__iqpws = get_data(x)
    fks__exfh = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(sbwn__rrd) for
        sbwn__rrd in [pybg__iqpws, fks__exfh])
    if fks__exfh == types.none:
        if isinstance(ylhgb__isiz, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif pybg__iqpws == fks__exfh and not is_nullable:
        out_dtype = dtype_to_array_type(ylhgb__isiz)
    elif ylhgb__isiz == string_type or slr__imzm == string_type:
        out_dtype = bodo.string_array_type
    elif pybg__iqpws == bytes_type or (hizb__mmop and ylhgb__isiz == bytes_type
        ) and (fks__exfh == bytes_type or uiu__bfx and slr__imzm == bytes_type
        ):
        out_dtype = binary_array_type
    elif isinstance(ylhgb__isiz, bodo.PDCategoricalDtype):
        out_dtype = None
    elif ylhgb__isiz in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(ylhgb__isiz, 1, 'C')
    elif slr__imzm in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(slr__imzm, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(ylhgb__isiz), numba.np.numpy_support.
            as_dtype(slr__imzm)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(ylhgb__isiz, bodo.PDCategoricalDtype):
        fha__siij = 'x'
    else:
        fha__siij = 'out_dtype'
    jpf__wcv += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {fha__siij}, (-1,))\n')
    if isinstance(ylhgb__isiz, bodo.PDCategoricalDtype):
        jpf__wcv += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        jpf__wcv += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    jpf__wcv += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    jpf__wcv += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if hizb__mmop:
        jpf__wcv += '      if bodo.libs.array_kernels.isna(x, j):\n'
        jpf__wcv += '        setna(out_arr, j)\n'
        jpf__wcv += '        continue\n'
    if isinstance(ylhgb__isiz, bodo.PDCategoricalDtype):
        jpf__wcv += '      out_codes[j] = x_codes[j]\n'
    else:
        jpf__wcv += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if hizb__mmop else 'x'))
    jpf__wcv += '    else:\n'
    if uiu__bfx:
        jpf__wcv += '      if bodo.libs.array_kernels.isna(y, j):\n'
        jpf__wcv += '        setna(out_arr, j)\n'
        jpf__wcv += '        continue\n'
    if fks__exfh == types.none:
        if isinstance(ylhgb__isiz, bodo.PDCategoricalDtype):
            jpf__wcv += '      out_codes[j] = -1\n'
        else:
            jpf__wcv += '      setna(out_arr, j)\n'
    else:
        jpf__wcv += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if uiu__bfx else 'y'))
    jpf__wcv += '  return out_arr\n'
    hfkvs__ogzi = {}
    exec(jpf__wcv, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, hfkvs__ogzi)
    lae__tevq = hfkvs__ogzi['_impl']
    return lae__tevq


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
        eygv__mlckc = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(eygv__mlckc, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(eygv__mlckc):
            dis__aogp = eygv__mlckc.data.dtype
        else:
            dis__aogp = eygv__mlckc.dtype
        if isinstance(dis__aogp, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        bxdxq__ucr = eygv__mlckc
    else:
        kzw__wup = []
        for eygv__mlckc in choicelist:
            if not bodo.utils.utils.is_array_typ(eygv__mlckc, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(eygv__mlckc):
                dis__aogp = eygv__mlckc.data.dtype
            else:
                dis__aogp = eygv__mlckc.dtype
            if isinstance(dis__aogp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            kzw__wup.append(dis__aogp)
        if not is_common_scalar_dtype(kzw__wup):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        bxdxq__ucr = choicelist[0]
    if is_series_type(bxdxq__ucr):
        bxdxq__ucr = bxdxq__ucr.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, bxdxq__ucr.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(bxdxq__ucr, types.Array) or isinstance(bxdxq__ucr,
        BooleanArrayType) or isinstance(bxdxq__ucr, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(bxdxq__ucr, False) and bxdxq__ucr.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {bxdxq__ucr} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    lpv__qyjne = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        dvb__mdqfm = choicelist.dtype
    else:
        mzdrw__dkz = False
        kzw__wup = []
        for eygv__mlckc in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                eygv__mlckc, 'numpy.select()')
            if is_nullable_type(eygv__mlckc):
                mzdrw__dkz = True
            if is_series_type(eygv__mlckc):
                dis__aogp = eygv__mlckc.data.dtype
            else:
                dis__aogp = eygv__mlckc.dtype
            if isinstance(dis__aogp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            kzw__wup.append(dis__aogp)
        unpbn__txc, pax__zmk = get_common_scalar_dtype(kzw__wup)
        if not pax__zmk:
            raise BodoError('Internal error in overload_np_select')
        drcfx__faxvi = dtype_to_array_type(unpbn__txc)
        if mzdrw__dkz:
            drcfx__faxvi = to_nullable_type(drcfx__faxvi)
        dvb__mdqfm = drcfx__faxvi
    if isinstance(dvb__mdqfm, SeriesType):
        dvb__mdqfm = dvb__mdqfm.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        ule__gthxr = True
    else:
        ule__gthxr = False
    aoxmo__tvp = False
    llsqm__qfpsl = False
    if ule__gthxr:
        if isinstance(dvb__mdqfm.dtype, types.Number):
            pass
        elif dvb__mdqfm.dtype == types.bool_:
            llsqm__qfpsl = True
        else:
            aoxmo__tvp = True
            dvb__mdqfm = to_nullable_type(dvb__mdqfm)
    elif default == types.none or is_overload_constant_nan(default):
        aoxmo__tvp = True
        dvb__mdqfm = to_nullable_type(dvb__mdqfm)
    jpf__wcv = 'def np_select_impl(condlist, choicelist, default=0):\n'
    jpf__wcv += '  if len(condlist) != len(choicelist):\n'
    jpf__wcv += (
        "    raise ValueError('list of cases must be same length as list of conditions')\n"
        )
    jpf__wcv += '  output_len = len(choicelist[0])\n'
    jpf__wcv += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    jpf__wcv += '  for i in range(output_len):\n'
    if aoxmo__tvp:
        jpf__wcv += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif llsqm__qfpsl:
        jpf__wcv += '    out[i] = False\n'
    else:
        jpf__wcv += '    out[i] = default\n'
    if lpv__qyjne:
        jpf__wcv += '  for i in range(len(condlist) - 1, -1, -1):\n'
        jpf__wcv += '    cond = condlist[i]\n'
        jpf__wcv += '    choice = choicelist[i]\n'
        jpf__wcv += '    out = np.where(cond, choice, out)\n'
    else:
        for tazsb__mvow in range(len(choicelist) - 1, -1, -1):
            jpf__wcv += f'  cond = condlist[{tazsb__mvow}]\n'
            jpf__wcv += f'  choice = choicelist[{tazsb__mvow}]\n'
            jpf__wcv += f'  out = np.where(cond, choice, out)\n'
    jpf__wcv += '  return out'
    hfkvs__ogzi = dict()
    exec(jpf__wcv, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': dvb__mdqfm}, hfkvs__ogzi)
    impl = hfkvs__ogzi['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wkfhu__uqi = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    xci__flkyz = dict(subset=subset, keep=keep, inplace=inplace)
    mldpl__xnwz = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', xci__flkyz,
        mldpl__xnwz, package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        isr__zvy = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (isr__zvy,), dimgb__iyfy = bodo.libs.array_kernels.drop_duplicates((
            isr__zvy,), index, 1)
        index = bodo.utils.conversion.index_from_array(dimgb__iyfy)
        return bodo.hiframes.pd_series_ext.init_series(isr__zvy, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    onaak__wzbyv = element_type(S.data)
    if not is_common_scalar_dtype([onaak__wzbyv, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([onaak__wzbyv, right]):
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
        wkfhu__uqi = np.empty(n, np.bool_)
        for tazsb__mvow in numba.parfors.parfor.internal_prange(n):
            cwxw__vqg = bodo.utils.conversion.box_if_dt64(arr[tazsb__mvow])
            if inclusive == 'both':
                wkfhu__uqi[tazsb__mvow
                    ] = cwxw__vqg <= right and cwxw__vqg >= left
            else:
                wkfhu__uqi[tazsb__mvow
                    ] = cwxw__vqg < right and cwxw__vqg > left
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    xci__flkyz = dict(axis=axis)
    mldpl__xnwz = dict(axis=None)
    check_unsupported_args('Series.repeat', xci__flkyz, mldpl__xnwz,
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
            dimgb__iyfy = bodo.utils.conversion.index_to_array(index)
            wkfhu__uqi = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            qejz__ojikv = bodo.libs.array_kernels.repeat_kernel(dimgb__iyfy,
                repeats)
            zvc__zur = bodo.utils.conversion.index_from_array(qejz__ojikv)
            return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi,
                zvc__zur, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        dimgb__iyfy = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        wkfhu__uqi = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        qejz__ojikv = bodo.libs.array_kernels.repeat_kernel(dimgb__iyfy,
            repeats)
        zvc__zur = bodo.utils.conversion.index_from_array(qejz__ojikv)
        return bodo.hiframes.pd_series_ext.init_series(wkfhu__uqi, zvc__zur,
            name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        sbwn__rrd = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(sbwn__rrd)
        ffmjx__qmbl = {}
        for tazsb__mvow in range(n):
            cwxw__vqg = bodo.utils.conversion.box_if_dt64(sbwn__rrd[
                tazsb__mvow])
            ffmjx__qmbl[index[tazsb__mvow]] = cwxw__vqg
        return ffmjx__qmbl
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    liq__fcrs = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            iqd__fcri = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(liq__fcrs)
    elif is_literal_type(name):
        iqd__fcri = get_literal_value(name)
    else:
        raise_bodo_error(liq__fcrs)
    iqd__fcri = 0 if iqd__fcri is None else iqd__fcri

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (iqd__fcri,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
