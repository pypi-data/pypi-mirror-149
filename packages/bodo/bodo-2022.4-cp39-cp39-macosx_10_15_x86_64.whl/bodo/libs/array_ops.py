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
    ktby__dod = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(ktby__dod.ctypes, arr,
        parallel, skipna)
    return ktby__dod[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ggra__fgsdx = len(arr)
        ewxck__xjxv = np.empty(ggra__fgsdx, np.bool_)
        for kle__khdp in numba.parfors.parfor.internal_prange(ggra__fgsdx):
            ewxck__xjxv[kle__khdp] = bodo.libs.array_kernels.isna(arr,
                kle__khdp)
        return ewxck__xjxv
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        juv__hgj = 0
        for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
            ost__iiwv = 0
            if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                ost__iiwv = 1
            juv__hgj += ost__iiwv
        ktby__dod = juv__hgj
        return ktby__dod
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    hhnrw__aoqj = array_op_count(arr)
    fisa__afn = array_op_min(arr)
    juba__borr = array_op_max(arr)
    xert__lfnpg = array_op_mean(arr)
    ubok__opr = array_op_std(arr)
    odbu__bivxt = array_op_quantile(arr, 0.25)
    cyod__kvqh = array_op_quantile(arr, 0.5)
    jhiev__dcm = array_op_quantile(arr, 0.75)
    return (hhnrw__aoqj, xert__lfnpg, ubok__opr, fisa__afn, odbu__bivxt,
        cyod__kvqh, jhiev__dcm, juba__borr)


def array_op_describe_dt_impl(arr):
    hhnrw__aoqj = array_op_count(arr)
    fisa__afn = array_op_min(arr)
    juba__borr = array_op_max(arr)
    xert__lfnpg = array_op_mean(arr)
    odbu__bivxt = array_op_quantile(arr, 0.25)
    cyod__kvqh = array_op_quantile(arr, 0.5)
    jhiev__dcm = array_op_quantile(arr, 0.75)
    return (hhnrw__aoqj, xert__lfnpg, fisa__afn, odbu__bivxt, cyod__kvqh,
        jhiev__dcm, juba__borr)


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
            dmao__mmwvn = numba.cpython.builtins.get_type_max_value(np.int64)
            juv__hgj = 0
            for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
                kdor__grgv = dmao__mmwvn
                ost__iiwv = 0
                if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                    kdor__grgv = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[kle__khdp]))
                    ost__iiwv = 1
                dmao__mmwvn = min(dmao__mmwvn, kdor__grgv)
                juv__hgj += ost__iiwv
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(dmao__mmwvn,
                juv__hgj)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = numba.cpython.builtins.get_type_max_value(np.int64)
            juv__hgj = 0
            for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
                kdor__grgv = dmao__mmwvn
                ost__iiwv = 0
                if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                    kdor__grgv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[kle__khdp]))
                    ost__iiwv = 1
                dmao__mmwvn = min(dmao__mmwvn, kdor__grgv)
                juv__hgj += ost__iiwv
            return bodo.hiframes.pd_index_ext._dti_val_finalize(dmao__mmwvn,
                juv__hgj)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            jbpe__ebru = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = numba.cpython.builtins.get_type_max_value(np.int64)
            juv__hgj = 0
            for kle__khdp in numba.parfors.parfor.internal_prange(len(
                jbpe__ebru)):
                bzv__tlhz = jbpe__ebru[kle__khdp]
                if bzv__tlhz == -1:
                    continue
                dmao__mmwvn = min(dmao__mmwvn, bzv__tlhz)
                juv__hgj += 1
            ktby__dod = bodo.hiframes.series_kernels._box_cat_val(dmao__mmwvn,
                arr.dtype, juv__hgj)
            return ktby__dod
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = bodo.hiframes.series_kernels._get_date_max_value()
            juv__hgj = 0
            for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
                kdor__grgv = dmao__mmwvn
                ost__iiwv = 0
                if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                    kdor__grgv = arr[kle__khdp]
                    ost__iiwv = 1
                dmao__mmwvn = min(dmao__mmwvn, kdor__grgv)
                juv__hgj += ost__iiwv
            ktby__dod = bodo.hiframes.series_kernels._sum_handle_nan(
                dmao__mmwvn, juv__hgj)
            return ktby__dod
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dmao__mmwvn = bodo.hiframes.series_kernels._get_type_max_value(arr.
            dtype)
        juv__hgj = 0
        for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
            kdor__grgv = dmao__mmwvn
            ost__iiwv = 0
            if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                kdor__grgv = arr[kle__khdp]
                ost__iiwv = 1
            dmao__mmwvn = min(dmao__mmwvn, kdor__grgv)
            juv__hgj += ost__iiwv
        ktby__dod = bodo.hiframes.series_kernels._sum_handle_nan(dmao__mmwvn,
            juv__hgj)
        return ktby__dod
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = numba.cpython.builtins.get_type_min_value(np.int64)
            juv__hgj = 0
            for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
                kdor__grgv = dmao__mmwvn
                ost__iiwv = 0
                if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                    kdor__grgv = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[kle__khdp]))
                    ost__iiwv = 1
                dmao__mmwvn = max(dmao__mmwvn, kdor__grgv)
                juv__hgj += ost__iiwv
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(dmao__mmwvn,
                juv__hgj)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = numba.cpython.builtins.get_type_min_value(np.int64)
            juv__hgj = 0
            for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
                kdor__grgv = dmao__mmwvn
                ost__iiwv = 0
                if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                    kdor__grgv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[kle__khdp]))
                    ost__iiwv = 1
                dmao__mmwvn = max(dmao__mmwvn, kdor__grgv)
                juv__hgj += ost__iiwv
            return bodo.hiframes.pd_index_ext._dti_val_finalize(dmao__mmwvn,
                juv__hgj)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            jbpe__ebru = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = -1
            for kle__khdp in numba.parfors.parfor.internal_prange(len(
                jbpe__ebru)):
                dmao__mmwvn = max(dmao__mmwvn, jbpe__ebru[kle__khdp])
            ktby__dod = bodo.hiframes.series_kernels._box_cat_val(dmao__mmwvn,
                arr.dtype, 1)
            return ktby__dod
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = bodo.hiframes.series_kernels._get_date_min_value()
            juv__hgj = 0
            for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
                kdor__grgv = dmao__mmwvn
                ost__iiwv = 0
                if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                    kdor__grgv = arr[kle__khdp]
                    ost__iiwv = 1
                dmao__mmwvn = max(dmao__mmwvn, kdor__grgv)
                juv__hgj += ost__iiwv
            ktby__dod = bodo.hiframes.series_kernels._sum_handle_nan(
                dmao__mmwvn, juv__hgj)
            return ktby__dod
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dmao__mmwvn = bodo.hiframes.series_kernels._get_type_min_value(arr.
            dtype)
        juv__hgj = 0
        for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
            kdor__grgv = dmao__mmwvn
            ost__iiwv = 0
            if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                kdor__grgv = arr[kle__khdp]
                ost__iiwv = 1
            dmao__mmwvn = max(dmao__mmwvn, kdor__grgv)
            juv__hgj += ost__iiwv
        ktby__dod = bodo.hiframes.series_kernels._sum_handle_nan(dmao__mmwvn,
            juv__hgj)
        return ktby__dod
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
    vrddg__pnnlr = types.float64
    dxj__mmp = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        vrddg__pnnlr = types.float32
        dxj__mmp = types.float32
    jgnmz__nbbmc = vrddg__pnnlr(0)
    idx__eyei = dxj__mmp(0)
    nlki__eevd = dxj__mmp(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dmao__mmwvn = jgnmz__nbbmc
        juv__hgj = idx__eyei
        for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
            kdor__grgv = jgnmz__nbbmc
            ost__iiwv = idx__eyei
            if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                kdor__grgv = arr[kle__khdp]
                ost__iiwv = nlki__eevd
            dmao__mmwvn += kdor__grgv
            juv__hgj += ost__iiwv
        ktby__dod = bodo.hiframes.series_kernels._mean_handle_nan(dmao__mmwvn,
            juv__hgj)
        return ktby__dod
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        vpyg__imm = 0.0
        ojl__plk = 0.0
        juv__hgj = 0
        for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
            kdor__grgv = 0.0
            ost__iiwv = 0
            if not bodo.libs.array_kernels.isna(arr, kle__khdp) or not skipna:
                kdor__grgv = arr[kle__khdp]
                ost__iiwv = 1
            vpyg__imm += kdor__grgv
            ojl__plk += kdor__grgv * kdor__grgv
            juv__hgj += ost__iiwv
        ktby__dod = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            vpyg__imm, ojl__plk, juv__hgj, ddof)
        return ktby__dod
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
                ewxck__xjxv = np.empty(len(q), np.int64)
                for kle__khdp in range(len(q)):
                    onpem__vdn = np.float64(q[kle__khdp])
                    ewxck__xjxv[kle__khdp] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), onpem__vdn)
                return ewxck__xjxv.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            ewxck__xjxv = np.empty(len(q), np.float64)
            for kle__khdp in range(len(q)):
                onpem__vdn = np.float64(q[kle__khdp])
                ewxck__xjxv[kle__khdp] = bodo.libs.array_kernels.quantile(arr,
                    onpem__vdn)
            return ewxck__xjxv
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
        vrj__aywfv = types.intp
    elif arr.dtype == types.bool_:
        vrj__aywfv = np.int64
    else:
        vrj__aywfv = arr.dtype
    ivy__foleu = vrj__aywfv(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = ivy__foleu
            ggra__fgsdx = len(arr)
            juv__hgj = 0
            for kle__khdp in numba.parfors.parfor.internal_prange(ggra__fgsdx):
                kdor__grgv = ivy__foleu
                ost__iiwv = 0
                if not bodo.libs.array_kernels.isna(arr, kle__khdp
                    ) or not skipna:
                    kdor__grgv = arr[kle__khdp]
                    ost__iiwv = 1
                dmao__mmwvn += kdor__grgv
                juv__hgj += ost__iiwv
            ktby__dod = bodo.hiframes.series_kernels._var_handle_mincount(
                dmao__mmwvn, juv__hgj, min_count)
            return ktby__dod
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = ivy__foleu
            ggra__fgsdx = len(arr)
            for kle__khdp in numba.parfors.parfor.internal_prange(ggra__fgsdx):
                kdor__grgv = ivy__foleu
                if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                    kdor__grgv = arr[kle__khdp]
                dmao__mmwvn += kdor__grgv
            return dmao__mmwvn
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    qgm__vnssk = arr.dtype(1)
    if arr.dtype == types.bool_:
        qgm__vnssk = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = qgm__vnssk
            juv__hgj = 0
            for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
                kdor__grgv = qgm__vnssk
                ost__iiwv = 0
                if not bodo.libs.array_kernels.isna(arr, kle__khdp
                    ) or not skipna:
                    kdor__grgv = arr[kle__khdp]
                    ost__iiwv = 1
                juv__hgj += ost__iiwv
                dmao__mmwvn *= kdor__grgv
            ktby__dod = bodo.hiframes.series_kernels._var_handle_mincount(
                dmao__mmwvn, juv__hgj, min_count)
            return ktby__dod
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dmao__mmwvn = qgm__vnssk
            for kle__khdp in numba.parfors.parfor.internal_prange(len(arr)):
                kdor__grgv = qgm__vnssk
                if not bodo.libs.array_kernels.isna(arr, kle__khdp):
                    kdor__grgv = arr[kle__khdp]
                dmao__mmwvn *= kdor__grgv
            return dmao__mmwvn
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        kle__khdp = bodo.libs.array_kernels._nan_argmax(arr)
        return index[kle__khdp]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        kle__khdp = bodo.libs.array_kernels._nan_argmin(arr)
        return index[kle__khdp]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            lsyc__itaqd = {}
            for mrb__nsfk in values:
                lsyc__itaqd[bodo.utils.conversion.box_if_dt64(mrb__nsfk)] = 0
            return lsyc__itaqd
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
        ggra__fgsdx = len(arr)
        ewxck__xjxv = np.empty(ggra__fgsdx, np.bool_)
        for kle__khdp in numba.parfors.parfor.internal_prange(ggra__fgsdx):
            ewxck__xjxv[kle__khdp] = bodo.utils.conversion.box_if_dt64(arr[
                kle__khdp]) in values
        return ewxck__xjxv
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    rpd__ubzir = len(in_arr_tup) != 1
    hjah__tutlv = list(in_arr_tup.types)
    fyvg__tgssd = 'def impl(in_arr_tup):\n'
    fyvg__tgssd += '  n = len(in_arr_tup[0])\n'
    if rpd__ubzir:
        vvt__ojyki = ', '.join([f'in_arr_tup[{kle__khdp}][unused]' for
            kle__khdp in range(len(in_arr_tup))])
        smv__cvbn = ', '.join(['False' for itdz__grbsh in range(len(
            in_arr_tup))])
        fyvg__tgssd += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({vvt__ojyki},), ({smv__cvbn},)): 0 for unused in range(0)}}
"""
        fyvg__tgssd += '  map_vector = np.empty(n, np.int64)\n'
        for kle__khdp, hqr__unu in enumerate(hjah__tutlv):
            fyvg__tgssd += f'  in_lst_{kle__khdp} = []\n'
            if is_str_arr_type(hqr__unu):
                fyvg__tgssd += f'  total_len_{kle__khdp} = 0\n'
            fyvg__tgssd += f'  null_in_lst_{kle__khdp} = []\n'
        fyvg__tgssd += '  for i in range(n):\n'
        jmlry__tyucx = ', '.join([f'in_arr_tup[{kle__khdp}][i]' for
            kle__khdp in range(len(hjah__tutlv))])
        yfy__itqb = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{kle__khdp}], i)' for
            kle__khdp in range(len(hjah__tutlv))])
        fyvg__tgssd += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({jmlry__tyucx},), ({yfy__itqb},))
"""
        fyvg__tgssd += '    if data_val not in arr_map:\n'
        fyvg__tgssd += '      set_val = len(arr_map)\n'
        fyvg__tgssd += '      values_tup = data_val._data\n'
        fyvg__tgssd += '      nulls_tup = data_val._null_values\n'
        for kle__khdp, hqr__unu in enumerate(hjah__tutlv):
            fyvg__tgssd += (
                f'      in_lst_{kle__khdp}.append(values_tup[{kle__khdp}])\n')
            fyvg__tgssd += (
                f'      null_in_lst_{kle__khdp}.append(nulls_tup[{kle__khdp}])\n'
                )
            if is_str_arr_type(hqr__unu):
                fyvg__tgssd += f"""      total_len_{kle__khdp}  += nulls_tup[{kle__khdp}] * len(values_tup[{kle__khdp}])
"""
        fyvg__tgssd += '      arr_map[data_val] = len(arr_map)\n'
        fyvg__tgssd += '    else:\n'
        fyvg__tgssd += '      set_val = arr_map[data_val]\n'
        fyvg__tgssd += '    map_vector[i] = set_val\n'
        fyvg__tgssd += '  n_rows = len(arr_map)\n'
        for kle__khdp, hqr__unu in enumerate(hjah__tutlv):
            if is_str_arr_type(hqr__unu):
                fyvg__tgssd += f"""  out_arr_{kle__khdp} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{kle__khdp})
"""
            else:
                fyvg__tgssd += f"""  out_arr_{kle__khdp} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{kle__khdp}], (-1,))
"""
        fyvg__tgssd += '  for j in range(len(arr_map)):\n'
        for kle__khdp in range(len(hjah__tutlv)):
            fyvg__tgssd += f'    if null_in_lst_{kle__khdp}[j]:\n'
            fyvg__tgssd += (
                f'      bodo.libs.array_kernels.setna(out_arr_{kle__khdp}, j)\n'
                )
            fyvg__tgssd += '    else:\n'
            fyvg__tgssd += (
                f'      out_arr_{kle__khdp}[j] = in_lst_{kle__khdp}[j]\n')
        gvzo__imr = ', '.join([f'out_arr_{kle__khdp}' for kle__khdp in
            range(len(hjah__tutlv))])
        fyvg__tgssd += f'  return ({gvzo__imr},), map_vector\n'
    else:
        fyvg__tgssd += '  in_arr = in_arr_tup[0]\n'
        fyvg__tgssd += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        fyvg__tgssd += '  map_vector = np.empty(n, np.int64)\n'
        fyvg__tgssd += '  is_na = 0\n'
        fyvg__tgssd += '  in_lst = []\n'
        if is_str_arr_type(hjah__tutlv[0]):
            fyvg__tgssd += '  total_len = 0\n'
        fyvg__tgssd += '  for i in range(n):\n'
        fyvg__tgssd += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        fyvg__tgssd += '      is_na = 1\n'
        fyvg__tgssd += (
            '      # Always put NA in the last location. We can safely use\n')
        fyvg__tgssd += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        fyvg__tgssd += '      set_val = -1\n'
        fyvg__tgssd += '    else:\n'
        fyvg__tgssd += '      data_val = in_arr[i]\n'
        fyvg__tgssd += '      if data_val not in arr_map:\n'
        fyvg__tgssd += '        set_val = len(arr_map)\n'
        fyvg__tgssd += '        in_lst.append(data_val)\n'
        if is_str_arr_type(hjah__tutlv[0]):
            fyvg__tgssd += '        total_len += len(data_val)\n'
        fyvg__tgssd += '        arr_map[data_val] = len(arr_map)\n'
        fyvg__tgssd += '      else:\n'
        fyvg__tgssd += '        set_val = arr_map[data_val]\n'
        fyvg__tgssd += '    map_vector[i] = set_val\n'
        fyvg__tgssd += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(hjah__tutlv[0]):
            fyvg__tgssd += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            fyvg__tgssd += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        fyvg__tgssd += '  for j in range(len(arr_map)):\n'
        fyvg__tgssd += '    out_arr[j] = in_lst[j]\n'
        fyvg__tgssd += '  if is_na:\n'
        fyvg__tgssd += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        fyvg__tgssd += f'  return (out_arr,), map_vector\n'
    rsril__bozn = {}
    exec(fyvg__tgssd, {'bodo': bodo, 'np': np}, rsril__bozn)
    impl = rsril__bozn['impl']
    return impl
