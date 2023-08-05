"""
Implements array operations for usage by DataFrames and Series
such as count and max.
"""
import numba
import numpy as np
import pandas as pd
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.utils.typing import element_type, is_hashable_type, is_iterable_type, is_overload_true, is_overload_zero, is_str_arr_type


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    hkez__rep = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(hkez__rep.ctypes, arr,
        parallel, skipna)
    return hkez__rep[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        kmdgk__ltr = len(arr)
        amrey__bybqx = np.empty(kmdgk__ltr, np.bool_)
        for zii__vmhrh in numba.parfors.parfor.internal_prange(kmdgk__ltr):
            amrey__bybqx[zii__vmhrh] = bodo.libs.array_kernels.isna(arr,
                zii__vmhrh)
        return amrey__bybqx
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        uzk__dpelo = 0
        for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
            lxeaf__cwan = 0
            if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                lxeaf__cwan = 1
            uzk__dpelo += lxeaf__cwan
        hkez__rep = uzk__dpelo
        return hkez__rep
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    uaz__dnk = array_op_count(arr)
    nela__tzs = array_op_min(arr)
    tjbd__grq = array_op_max(arr)
    wdnw__nhf = array_op_mean(arr)
    uyanz__xupu = array_op_std(arr)
    vnwlf__cpfn = array_op_quantile(arr, 0.25)
    fxkgl__yqyb = array_op_quantile(arr, 0.5)
    hmewc__rizb = array_op_quantile(arr, 0.75)
    return (uaz__dnk, wdnw__nhf, uyanz__xupu, nela__tzs, vnwlf__cpfn,
        fxkgl__yqyb, hmewc__rizb, tjbd__grq)


def array_op_describe_dt_impl(arr):
    uaz__dnk = array_op_count(arr)
    nela__tzs = array_op_min(arr)
    tjbd__grq = array_op_max(arr)
    wdnw__nhf = array_op_mean(arr)
    vnwlf__cpfn = array_op_quantile(arr, 0.25)
    fxkgl__yqyb = array_op_quantile(arr, 0.5)
    hmewc__rizb = array_op_quantile(arr, 0.75)
    return (uaz__dnk, wdnw__nhf, nela__tzs, vnwlf__cpfn, fxkgl__yqyb,
        hmewc__rizb, tjbd__grq)


@overload(array_op_describe)
def overload_array_op_describe(arr):
    if arr.dtype == bodo.datetime64ns:
        return array_op_describe_dt_impl
    return array_op_describe_impl


@generated_jit(nopython=True)
def array_op_nbytes(arr):
    return array_op_nbytes_impl


def array_op_nbytes_impl(arr):
    return arr.nbytes


def array_op_min(arr):
    pass


@overload(array_op_min)
def overload_array_op_min(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = numba.cpython.builtins.get_type_max_value(np.int64)
            uzk__dpelo = 0
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
                gyvay__yptgk = ewiom__rczc
                lxeaf__cwan = 0
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                    gyvay__yptgk = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[zii__vmhrh]))
                    lxeaf__cwan = 1
                ewiom__rczc = min(ewiom__rczc, gyvay__yptgk)
                uzk__dpelo += lxeaf__cwan
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(ewiom__rczc,
                uzk__dpelo)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = numba.cpython.builtins.get_type_max_value(np.int64)
            uzk__dpelo = 0
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
                gyvay__yptgk = ewiom__rczc
                lxeaf__cwan = 0
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                    gyvay__yptgk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[zii__vmhrh]))
                    lxeaf__cwan = 1
                ewiom__rczc = min(ewiom__rczc, gyvay__yptgk)
                uzk__dpelo += lxeaf__cwan
            return bodo.hiframes.pd_index_ext._dti_val_finalize(ewiom__rczc,
                uzk__dpelo)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            kkfxb__jmxnp = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            ewiom__rczc = numba.cpython.builtins.get_type_max_value(np.int64)
            uzk__dpelo = 0
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(
                kkfxb__jmxnp)):
                lwdg__dlaef = kkfxb__jmxnp[zii__vmhrh]
                if lwdg__dlaef == -1:
                    continue
                ewiom__rczc = min(ewiom__rczc, lwdg__dlaef)
                uzk__dpelo += 1
            hkez__rep = bodo.hiframes.series_kernels._box_cat_val(ewiom__rczc,
                arr.dtype, uzk__dpelo)
            return hkez__rep
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = bodo.hiframes.series_kernels._get_date_max_value()
            uzk__dpelo = 0
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
                gyvay__yptgk = ewiom__rczc
                lxeaf__cwan = 0
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                    gyvay__yptgk = arr[zii__vmhrh]
                    lxeaf__cwan = 1
                ewiom__rczc = min(ewiom__rczc, gyvay__yptgk)
                uzk__dpelo += lxeaf__cwan
            hkez__rep = bodo.hiframes.series_kernels._sum_handle_nan(
                ewiom__rczc, uzk__dpelo)
            return hkez__rep
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ewiom__rczc = bodo.hiframes.series_kernels._get_type_max_value(arr.
            dtype)
        uzk__dpelo = 0
        for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
            gyvay__yptgk = ewiom__rczc
            lxeaf__cwan = 0
            if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                gyvay__yptgk = arr[zii__vmhrh]
                lxeaf__cwan = 1
            ewiom__rczc = min(ewiom__rczc, gyvay__yptgk)
            uzk__dpelo += lxeaf__cwan
        hkez__rep = bodo.hiframes.series_kernels._sum_handle_nan(ewiom__rczc,
            uzk__dpelo)
        return hkez__rep
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = numba.cpython.builtins.get_type_min_value(np.int64)
            uzk__dpelo = 0
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
                gyvay__yptgk = ewiom__rczc
                lxeaf__cwan = 0
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                    gyvay__yptgk = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[zii__vmhrh]))
                    lxeaf__cwan = 1
                ewiom__rczc = max(ewiom__rczc, gyvay__yptgk)
                uzk__dpelo += lxeaf__cwan
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(ewiom__rczc,
                uzk__dpelo)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = numba.cpython.builtins.get_type_min_value(np.int64)
            uzk__dpelo = 0
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
                gyvay__yptgk = ewiom__rczc
                lxeaf__cwan = 0
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                    gyvay__yptgk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[zii__vmhrh]))
                    lxeaf__cwan = 1
                ewiom__rczc = max(ewiom__rczc, gyvay__yptgk)
                uzk__dpelo += lxeaf__cwan
            return bodo.hiframes.pd_index_ext._dti_val_finalize(ewiom__rczc,
                uzk__dpelo)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            kkfxb__jmxnp = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            ewiom__rczc = -1
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(
                kkfxb__jmxnp)):
                ewiom__rczc = max(ewiom__rczc, kkfxb__jmxnp[zii__vmhrh])
            hkez__rep = bodo.hiframes.series_kernels._box_cat_val(ewiom__rczc,
                arr.dtype, 1)
            return hkez__rep
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = bodo.hiframes.series_kernels._get_date_min_value()
            uzk__dpelo = 0
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
                gyvay__yptgk = ewiom__rczc
                lxeaf__cwan = 0
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                    gyvay__yptgk = arr[zii__vmhrh]
                    lxeaf__cwan = 1
                ewiom__rczc = max(ewiom__rczc, gyvay__yptgk)
                uzk__dpelo += lxeaf__cwan
            hkez__rep = bodo.hiframes.series_kernels._sum_handle_nan(
                ewiom__rczc, uzk__dpelo)
            return hkez__rep
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ewiom__rczc = bodo.hiframes.series_kernels._get_type_min_value(arr.
            dtype)
        uzk__dpelo = 0
        for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
            gyvay__yptgk = ewiom__rczc
            lxeaf__cwan = 0
            if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                gyvay__yptgk = arr[zii__vmhrh]
                lxeaf__cwan = 1
            ewiom__rczc = max(ewiom__rczc, gyvay__yptgk)
            uzk__dpelo += lxeaf__cwan
        hkez__rep = bodo.hiframes.series_kernels._sum_handle_nan(ewiom__rczc,
            uzk__dpelo)
        return hkez__rep
    return impl


def array_op_mean(arr):
    pass


@overload(array_op_mean)
def overload_array_op_mean(arr):
    if arr.dtype == bodo.datetime64ns:

        def impl(arr):
            return pd.Timestamp(types.int64(bodo.libs.array_ops.
                array_op_mean(arr.view(np.int64))))
        return impl
    owt__ubgc = types.float64
    bsas__jhz = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        owt__ubgc = types.float32
        bsas__jhz = types.float32
    cnei__hsk = owt__ubgc(0)
    crans__dgvgj = bsas__jhz(0)
    lrltw__ktot = bsas__jhz(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ewiom__rczc = cnei__hsk
        uzk__dpelo = crans__dgvgj
        for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
            gyvay__yptgk = cnei__hsk
            lxeaf__cwan = crans__dgvgj
            if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                gyvay__yptgk = arr[zii__vmhrh]
                lxeaf__cwan = lrltw__ktot
            ewiom__rczc += gyvay__yptgk
            uzk__dpelo += lxeaf__cwan
        hkez__rep = bodo.hiframes.series_kernels._mean_handle_nan(ewiom__rczc,
            uzk__dpelo)
        return hkez__rep
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        qnigs__htczd = 0.0
        snv__umn = 0.0
        uzk__dpelo = 0
        for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
            gyvay__yptgk = 0.0
            lxeaf__cwan = 0
            if not bodo.libs.array_kernels.isna(arr, zii__vmhrh) or not skipna:
                gyvay__yptgk = arr[zii__vmhrh]
                lxeaf__cwan = 1
            qnigs__htczd += gyvay__yptgk
            snv__umn += gyvay__yptgk * gyvay__yptgk
            uzk__dpelo += lxeaf__cwan
        hkez__rep = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            qnigs__htczd, snv__umn, uzk__dpelo, ddof)
        return hkez__rep
    return impl


def array_op_std(arr, skipna=True, ddof=1):
    pass


@overload(array_op_std)
def overload_array_op_std(arr, skipna=True, ddof=1):
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr, skipna=True, ddof=1):
            return pd.Timedelta(types.int64(array_op_var(arr.view(np.int64),
                skipna, ddof) ** 0.5))
        return impl_dt64
    return lambda arr, skipna=True, ddof=1: array_op_var(arr, skipna, ddof
        ) ** 0.5


def array_op_quantile(arr, q):
    pass


@overload(array_op_quantile)
def overload_array_op_quantile(arr, q):
    if is_iterable_type(q):
        if arr.dtype == bodo.datetime64ns:

            def _impl_list_dt(arr, q):
                amrey__bybqx = np.empty(len(q), np.int64)
                for zii__vmhrh in range(len(q)):
                    gzf__zmhjg = np.float64(q[zii__vmhrh])
                    amrey__bybqx[zii__vmhrh
                        ] = bodo.libs.array_kernels.quantile(arr.view(np.
                        int64), gzf__zmhjg)
                return amrey__bybqx.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            amrey__bybqx = np.empty(len(q), np.float64)
            for zii__vmhrh in range(len(q)):
                gzf__zmhjg = np.float64(q[zii__vmhrh])
                amrey__bybqx[zii__vmhrh] = bodo.libs.array_kernels.quantile(arr
                    , gzf__zmhjg)
            return amrey__bybqx
        return impl_list
    if arr.dtype == bodo.datetime64ns:

        def _impl_dt(arr, q):
            return pd.Timestamp(bodo.libs.array_kernels.quantile(arr.view(
                np.int64), np.float64(q)))
        return _impl_dt

    def impl(arr, q):
        return bodo.libs.array_kernels.quantile(arr, np.float64(q))
    return impl


def array_op_sum(arr, skipna, min_count):
    pass


@overload(array_op_sum, no_unliteral=True)
def overload_array_op_sum(arr, skipna, min_count):
    if isinstance(arr.dtype, types.Integer):
        fxj__mjjpl = types.intp
    elif arr.dtype == types.bool_:
        fxj__mjjpl = np.int64
    else:
        fxj__mjjpl = arr.dtype
    ybj__qpkp = fxj__mjjpl(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = ybj__qpkp
            kmdgk__ltr = len(arr)
            uzk__dpelo = 0
            for zii__vmhrh in numba.parfors.parfor.internal_prange(kmdgk__ltr):
                gyvay__yptgk = ybj__qpkp
                lxeaf__cwan = 0
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh
                    ) or not skipna:
                    gyvay__yptgk = arr[zii__vmhrh]
                    lxeaf__cwan = 1
                ewiom__rczc += gyvay__yptgk
                uzk__dpelo += lxeaf__cwan
            hkez__rep = bodo.hiframes.series_kernels._var_handle_mincount(
                ewiom__rczc, uzk__dpelo, min_count)
            return hkez__rep
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = ybj__qpkp
            kmdgk__ltr = len(arr)
            for zii__vmhrh in numba.parfors.parfor.internal_prange(kmdgk__ltr):
                gyvay__yptgk = ybj__qpkp
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                    gyvay__yptgk = arr[zii__vmhrh]
                ewiom__rczc += gyvay__yptgk
            return ewiom__rczc
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    wcg__rzfpw = arr.dtype(1)
    if arr.dtype == types.bool_:
        wcg__rzfpw = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = wcg__rzfpw
            uzk__dpelo = 0
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
                gyvay__yptgk = wcg__rzfpw
                lxeaf__cwan = 0
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh
                    ) or not skipna:
                    gyvay__yptgk = arr[zii__vmhrh]
                    lxeaf__cwan = 1
                uzk__dpelo += lxeaf__cwan
                ewiom__rczc *= gyvay__yptgk
            hkez__rep = bodo.hiframes.series_kernels._var_handle_mincount(
                ewiom__rczc, uzk__dpelo, min_count)
            return hkez__rep
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            ewiom__rczc = wcg__rzfpw
            for zii__vmhrh in numba.parfors.parfor.internal_prange(len(arr)):
                gyvay__yptgk = wcg__rzfpw
                if not bodo.libs.array_kernels.isna(arr, zii__vmhrh):
                    gyvay__yptgk = arr[zii__vmhrh]
                ewiom__rczc *= gyvay__yptgk
            return ewiom__rczc
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        zii__vmhrh = bodo.libs.array_kernels._nan_argmax(arr)
        return index[zii__vmhrh]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        zii__vmhrh = bodo.libs.array_kernels._nan_argmin(arr)
        return index[zii__vmhrh]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            eknqg__cxuu = {}
            for jzwyi__dxkkh in values:
                eknqg__cxuu[bodo.utils.conversion.box_if_dt64(jzwyi__dxkkh)
                    ] = 0
            return eknqg__cxuu
        return impl
    else:

        def impl(values, use_hash_impl):
            return values
        return impl


def array_op_isin(arr, values):
    pass


@overload(array_op_isin, inline='always')
def overload_array_op_isin(arr, values):
    use_hash_impl = element_type(values) == element_type(arr
        ) and is_hashable_type(element_type(values))

    def impl(arr, values):
        values = bodo.libs.array_ops._convert_isin_values(values, use_hash_impl
            )
        numba.parfors.parfor.init_prange()
        kmdgk__ltr = len(arr)
        amrey__bybqx = np.empty(kmdgk__ltr, np.bool_)
        for zii__vmhrh in numba.parfors.parfor.internal_prange(kmdgk__ltr):
            amrey__bybqx[zii__vmhrh] = bodo.utils.conversion.box_if_dt64(arr
                [zii__vmhrh]) in values
        return amrey__bybqx
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    irs__sle = len(in_arr_tup) != 1
    aew__hgqh = list(in_arr_tup.types)
    mcq__aveoq = 'def impl(in_arr_tup):\n'
    mcq__aveoq += '  n = len(in_arr_tup[0])\n'
    if irs__sle:
        unsh__odmg = ', '.join([f'in_arr_tup[{zii__vmhrh}][unused]' for
            zii__vmhrh in range(len(in_arr_tup))])
        juyk__yfjzq = ', '.join(['False' for zbg__whhfa in range(len(
            in_arr_tup))])
        mcq__aveoq += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({unsh__odmg},), ({juyk__yfjzq},)): 0 for unused in range(0)}}
"""
        mcq__aveoq += '  map_vector = np.empty(n, np.int64)\n'
        for zii__vmhrh, rat__clfuo in enumerate(aew__hgqh):
            mcq__aveoq += f'  in_lst_{zii__vmhrh} = []\n'
            if is_str_arr_type(rat__clfuo):
                mcq__aveoq += f'  total_len_{zii__vmhrh} = 0\n'
            mcq__aveoq += f'  null_in_lst_{zii__vmhrh} = []\n'
        mcq__aveoq += '  for i in range(n):\n'
        qpv__wsng = ', '.join([f'in_arr_tup[{zii__vmhrh}][i]' for
            zii__vmhrh in range(len(aew__hgqh))])
        zrfz__rmxl = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{zii__vmhrh}], i)' for
            zii__vmhrh in range(len(aew__hgqh))])
        mcq__aveoq += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({qpv__wsng},), ({zrfz__rmxl},))
"""
        mcq__aveoq += '    if data_val not in arr_map:\n'
        mcq__aveoq += '      set_val = len(arr_map)\n'
        mcq__aveoq += '      values_tup = data_val._data\n'
        mcq__aveoq += '      nulls_tup = data_val._null_values\n'
        for zii__vmhrh, rat__clfuo in enumerate(aew__hgqh):
            mcq__aveoq += (
                f'      in_lst_{zii__vmhrh}.append(values_tup[{zii__vmhrh}])\n'
                )
            mcq__aveoq += (
                f'      null_in_lst_{zii__vmhrh}.append(nulls_tup[{zii__vmhrh}])\n'
                )
            if is_str_arr_type(rat__clfuo):
                mcq__aveoq += f"""      total_len_{zii__vmhrh}  += nulls_tup[{zii__vmhrh}] * len(values_tup[{zii__vmhrh}])
"""
        mcq__aveoq += '      arr_map[data_val] = len(arr_map)\n'
        mcq__aveoq += '    else:\n'
        mcq__aveoq += '      set_val = arr_map[data_val]\n'
        mcq__aveoq += '    map_vector[i] = set_val\n'
        mcq__aveoq += '  n_rows = len(arr_map)\n'
        for zii__vmhrh, rat__clfuo in enumerate(aew__hgqh):
            if is_str_arr_type(rat__clfuo):
                mcq__aveoq += f"""  out_arr_{zii__vmhrh} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{zii__vmhrh})
"""
            else:
                mcq__aveoq += f"""  out_arr_{zii__vmhrh} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{zii__vmhrh}], (-1,))
"""
        mcq__aveoq += '  for j in range(len(arr_map)):\n'
        for zii__vmhrh in range(len(aew__hgqh)):
            mcq__aveoq += f'    if null_in_lst_{zii__vmhrh}[j]:\n'
            mcq__aveoq += (
                f'      bodo.libs.array_kernels.setna(out_arr_{zii__vmhrh}, j)\n'
                )
            mcq__aveoq += '    else:\n'
            mcq__aveoq += (
                f'      out_arr_{zii__vmhrh}[j] = in_lst_{zii__vmhrh}[j]\n')
        lii__udo = ', '.join([f'out_arr_{zii__vmhrh}' for zii__vmhrh in
            range(len(aew__hgqh))])
        mcq__aveoq += f'  return ({lii__udo},), map_vector\n'
    else:
        mcq__aveoq += '  in_arr = in_arr_tup[0]\n'
        mcq__aveoq += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        mcq__aveoq += '  map_vector = np.empty(n, np.int64)\n'
        mcq__aveoq += '  is_na = 0\n'
        mcq__aveoq += '  in_lst = []\n'
        if is_str_arr_type(aew__hgqh[0]):
            mcq__aveoq += '  total_len = 0\n'
        mcq__aveoq += '  for i in range(n):\n'
        mcq__aveoq += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        mcq__aveoq += '      is_na = 1\n'
        mcq__aveoq += (
            '      # Always put NA in the last location. We can safely use\n')
        mcq__aveoq += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        mcq__aveoq += '      set_val = -1\n'
        mcq__aveoq += '    else:\n'
        mcq__aveoq += '      data_val = in_arr[i]\n'
        mcq__aveoq += '      if data_val not in arr_map:\n'
        mcq__aveoq += '        set_val = len(arr_map)\n'
        mcq__aveoq += '        in_lst.append(data_val)\n'
        if is_str_arr_type(aew__hgqh[0]):
            mcq__aveoq += '        total_len += len(data_val)\n'
        mcq__aveoq += '        arr_map[data_val] = len(arr_map)\n'
        mcq__aveoq += '      else:\n'
        mcq__aveoq += '        set_val = arr_map[data_val]\n'
        mcq__aveoq += '    map_vector[i] = set_val\n'
        mcq__aveoq += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(aew__hgqh[0]):
            mcq__aveoq += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            mcq__aveoq += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        mcq__aveoq += '  for j in range(len(arr_map)):\n'
        mcq__aveoq += '    out_arr[j] = in_lst[j]\n'
        mcq__aveoq += '  if is_na:\n'
        mcq__aveoq += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        mcq__aveoq += f'  return (out_arr,), map_vector\n'
    fmrub__ytjeb = {}
    exec(mcq__aveoq, {'bodo': bodo, 'np': np}, fmrub__ytjeb)
    impl = fmrub__ytjeb['impl']
    return impl
