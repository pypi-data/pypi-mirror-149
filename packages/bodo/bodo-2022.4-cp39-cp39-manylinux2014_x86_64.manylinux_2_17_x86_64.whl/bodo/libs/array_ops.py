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
    fhxk__xavz = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(fhxk__xavz.ctypes,
        arr, parallel, skipna)
    return fhxk__xavz[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dvlhu__ipdcj = len(arr)
        qsy__loaf = np.empty(dvlhu__ipdcj, np.bool_)
        for efozj__pln in numba.parfors.parfor.internal_prange(dvlhu__ipdcj):
            qsy__loaf[efozj__pln] = bodo.libs.array_kernels.isna(arr,
                efozj__pln)
        return qsy__loaf
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        gxcw__ohncw = 0
        for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
            ccm__askz = 0
            if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                ccm__askz = 1
            gxcw__ohncw += ccm__askz
        fhxk__xavz = gxcw__ohncw
        return fhxk__xavz
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    huzy__njol = array_op_count(arr)
    duze__qong = array_op_min(arr)
    plx__xzky = array_op_max(arr)
    ivbmm__qdcl = array_op_mean(arr)
    cxfvn__swc = array_op_std(arr)
    vyhs__ypbnm = array_op_quantile(arr, 0.25)
    dymib__nnjj = array_op_quantile(arr, 0.5)
    jsfm__mszf = array_op_quantile(arr, 0.75)
    return (huzy__njol, ivbmm__qdcl, cxfvn__swc, duze__qong, vyhs__ypbnm,
        dymib__nnjj, jsfm__mszf, plx__xzky)


def array_op_describe_dt_impl(arr):
    huzy__njol = array_op_count(arr)
    duze__qong = array_op_min(arr)
    plx__xzky = array_op_max(arr)
    ivbmm__qdcl = array_op_mean(arr)
    vyhs__ypbnm = array_op_quantile(arr, 0.25)
    dymib__nnjj = array_op_quantile(arr, 0.5)
    jsfm__mszf = array_op_quantile(arr, 0.75)
    return (huzy__njol, ivbmm__qdcl, duze__qong, vyhs__ypbnm, dymib__nnjj,
        jsfm__mszf, plx__xzky)


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
            jpcq__afyto = numba.cpython.builtins.get_type_max_value(np.int64)
            gxcw__ohncw = 0
            for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
                yilkz__zuyq = jpcq__afyto
                ccm__askz = 0
                if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                    yilkz__zuyq = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[efozj__pln]))
                    ccm__askz = 1
                jpcq__afyto = min(jpcq__afyto, yilkz__zuyq)
                gxcw__ohncw += ccm__askz
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(jpcq__afyto,
                gxcw__ohncw)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            jpcq__afyto = numba.cpython.builtins.get_type_max_value(np.int64)
            gxcw__ohncw = 0
            for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
                yilkz__zuyq = jpcq__afyto
                ccm__askz = 0
                if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                    yilkz__zuyq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[efozj__pln]))
                    ccm__askz = 1
                jpcq__afyto = min(jpcq__afyto, yilkz__zuyq)
                gxcw__ohncw += ccm__askz
            return bodo.hiframes.pd_index_ext._dti_val_finalize(jpcq__afyto,
                gxcw__ohncw)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            tincx__snvd = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            jpcq__afyto = numba.cpython.builtins.get_type_max_value(np.int64)
            gxcw__ohncw = 0
            for efozj__pln in numba.parfors.parfor.internal_prange(len(
                tincx__snvd)):
                pmh__azzx = tincx__snvd[efozj__pln]
                if pmh__azzx == -1:
                    continue
                jpcq__afyto = min(jpcq__afyto, pmh__azzx)
                gxcw__ohncw += 1
            fhxk__xavz = bodo.hiframes.series_kernels._box_cat_val(jpcq__afyto,
                arr.dtype, gxcw__ohncw)
            return fhxk__xavz
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            jpcq__afyto = bodo.hiframes.series_kernels._get_date_max_value()
            gxcw__ohncw = 0
            for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
                yilkz__zuyq = jpcq__afyto
                ccm__askz = 0
                if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                    yilkz__zuyq = arr[efozj__pln]
                    ccm__askz = 1
                jpcq__afyto = min(jpcq__afyto, yilkz__zuyq)
                gxcw__ohncw += ccm__askz
            fhxk__xavz = bodo.hiframes.series_kernels._sum_handle_nan(
                jpcq__afyto, gxcw__ohncw)
            return fhxk__xavz
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        jpcq__afyto = bodo.hiframes.series_kernels._get_type_max_value(arr.
            dtype)
        gxcw__ohncw = 0
        for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
            yilkz__zuyq = jpcq__afyto
            ccm__askz = 0
            if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                yilkz__zuyq = arr[efozj__pln]
                ccm__askz = 1
            jpcq__afyto = min(jpcq__afyto, yilkz__zuyq)
            gxcw__ohncw += ccm__askz
        fhxk__xavz = bodo.hiframes.series_kernels._sum_handle_nan(jpcq__afyto,
            gxcw__ohncw)
        return fhxk__xavz
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            jpcq__afyto = numba.cpython.builtins.get_type_min_value(np.int64)
            gxcw__ohncw = 0
            for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
                yilkz__zuyq = jpcq__afyto
                ccm__askz = 0
                if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                    yilkz__zuyq = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[efozj__pln]))
                    ccm__askz = 1
                jpcq__afyto = max(jpcq__afyto, yilkz__zuyq)
                gxcw__ohncw += ccm__askz
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(jpcq__afyto,
                gxcw__ohncw)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            jpcq__afyto = numba.cpython.builtins.get_type_min_value(np.int64)
            gxcw__ohncw = 0
            for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
                yilkz__zuyq = jpcq__afyto
                ccm__askz = 0
                if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                    yilkz__zuyq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[efozj__pln]))
                    ccm__askz = 1
                jpcq__afyto = max(jpcq__afyto, yilkz__zuyq)
                gxcw__ohncw += ccm__askz
            return bodo.hiframes.pd_index_ext._dti_val_finalize(jpcq__afyto,
                gxcw__ohncw)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            tincx__snvd = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            jpcq__afyto = -1
            for efozj__pln in numba.parfors.parfor.internal_prange(len(
                tincx__snvd)):
                jpcq__afyto = max(jpcq__afyto, tincx__snvd[efozj__pln])
            fhxk__xavz = bodo.hiframes.series_kernels._box_cat_val(jpcq__afyto,
                arr.dtype, 1)
            return fhxk__xavz
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            jpcq__afyto = bodo.hiframes.series_kernels._get_date_min_value()
            gxcw__ohncw = 0
            for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
                yilkz__zuyq = jpcq__afyto
                ccm__askz = 0
                if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                    yilkz__zuyq = arr[efozj__pln]
                    ccm__askz = 1
                jpcq__afyto = max(jpcq__afyto, yilkz__zuyq)
                gxcw__ohncw += ccm__askz
            fhxk__xavz = bodo.hiframes.series_kernels._sum_handle_nan(
                jpcq__afyto, gxcw__ohncw)
            return fhxk__xavz
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        jpcq__afyto = bodo.hiframes.series_kernels._get_type_min_value(arr.
            dtype)
        gxcw__ohncw = 0
        for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
            yilkz__zuyq = jpcq__afyto
            ccm__askz = 0
            if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                yilkz__zuyq = arr[efozj__pln]
                ccm__askz = 1
            jpcq__afyto = max(jpcq__afyto, yilkz__zuyq)
            gxcw__ohncw += ccm__askz
        fhxk__xavz = bodo.hiframes.series_kernels._sum_handle_nan(jpcq__afyto,
            gxcw__ohncw)
        return fhxk__xavz
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
    hmpn__mnyhx = types.float64
    fioyp__wjcx = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        hmpn__mnyhx = types.float32
        fioyp__wjcx = types.float32
    pegnk__hfej = hmpn__mnyhx(0)
    zmbv__hlkdm = fioyp__wjcx(0)
    emb__pkgv = fioyp__wjcx(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        jpcq__afyto = pegnk__hfej
        gxcw__ohncw = zmbv__hlkdm
        for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
            yilkz__zuyq = pegnk__hfej
            ccm__askz = zmbv__hlkdm
            if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                yilkz__zuyq = arr[efozj__pln]
                ccm__askz = emb__pkgv
            jpcq__afyto += yilkz__zuyq
            gxcw__ohncw += ccm__askz
        fhxk__xavz = bodo.hiframes.series_kernels._mean_handle_nan(jpcq__afyto,
            gxcw__ohncw)
        return fhxk__xavz
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        bki__alpcf = 0.0
        xbu__hrl = 0.0
        gxcw__ohncw = 0
        for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
            yilkz__zuyq = 0.0
            ccm__askz = 0
            if not bodo.libs.array_kernels.isna(arr, efozj__pln) or not skipna:
                yilkz__zuyq = arr[efozj__pln]
                ccm__askz = 1
            bki__alpcf += yilkz__zuyq
            xbu__hrl += yilkz__zuyq * yilkz__zuyq
            gxcw__ohncw += ccm__askz
        fhxk__xavz = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            bki__alpcf, xbu__hrl, gxcw__ohncw, ddof)
        return fhxk__xavz
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
                qsy__loaf = np.empty(len(q), np.int64)
                for efozj__pln in range(len(q)):
                    kls__lshb = np.float64(q[efozj__pln])
                    qsy__loaf[efozj__pln] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), kls__lshb)
                return qsy__loaf.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            qsy__loaf = np.empty(len(q), np.float64)
            for efozj__pln in range(len(q)):
                kls__lshb = np.float64(q[efozj__pln])
                qsy__loaf[efozj__pln] = bodo.libs.array_kernels.quantile(arr,
                    kls__lshb)
            return qsy__loaf
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
        ykx__wwfzi = types.intp
    elif arr.dtype == types.bool_:
        ykx__wwfzi = np.int64
    else:
        ykx__wwfzi = arr.dtype
    dqpbh__mbkja = ykx__wwfzi(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            jpcq__afyto = dqpbh__mbkja
            dvlhu__ipdcj = len(arr)
            gxcw__ohncw = 0
            for efozj__pln in numba.parfors.parfor.internal_prange(dvlhu__ipdcj
                ):
                yilkz__zuyq = dqpbh__mbkja
                ccm__askz = 0
                if not bodo.libs.array_kernels.isna(arr, efozj__pln
                    ) or not skipna:
                    yilkz__zuyq = arr[efozj__pln]
                    ccm__askz = 1
                jpcq__afyto += yilkz__zuyq
                gxcw__ohncw += ccm__askz
            fhxk__xavz = bodo.hiframes.series_kernels._var_handle_mincount(
                jpcq__afyto, gxcw__ohncw, min_count)
            return fhxk__xavz
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            jpcq__afyto = dqpbh__mbkja
            dvlhu__ipdcj = len(arr)
            for efozj__pln in numba.parfors.parfor.internal_prange(dvlhu__ipdcj
                ):
                yilkz__zuyq = dqpbh__mbkja
                if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                    yilkz__zuyq = arr[efozj__pln]
                jpcq__afyto += yilkz__zuyq
            return jpcq__afyto
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    dmoso__ivhr = arr.dtype(1)
    if arr.dtype == types.bool_:
        dmoso__ivhr = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            jpcq__afyto = dmoso__ivhr
            gxcw__ohncw = 0
            for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
                yilkz__zuyq = dmoso__ivhr
                ccm__askz = 0
                if not bodo.libs.array_kernels.isna(arr, efozj__pln
                    ) or not skipna:
                    yilkz__zuyq = arr[efozj__pln]
                    ccm__askz = 1
                gxcw__ohncw += ccm__askz
                jpcq__afyto *= yilkz__zuyq
            fhxk__xavz = bodo.hiframes.series_kernels._var_handle_mincount(
                jpcq__afyto, gxcw__ohncw, min_count)
            return fhxk__xavz
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            jpcq__afyto = dmoso__ivhr
            for efozj__pln in numba.parfors.parfor.internal_prange(len(arr)):
                yilkz__zuyq = dmoso__ivhr
                if not bodo.libs.array_kernels.isna(arr, efozj__pln):
                    yilkz__zuyq = arr[efozj__pln]
                jpcq__afyto *= yilkz__zuyq
            return jpcq__afyto
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        efozj__pln = bodo.libs.array_kernels._nan_argmax(arr)
        return index[efozj__pln]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        efozj__pln = bodo.libs.array_kernels._nan_argmin(arr)
        return index[efozj__pln]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            vvjk__bcbvg = {}
            for ovjw__rdn in values:
                vvjk__bcbvg[bodo.utils.conversion.box_if_dt64(ovjw__rdn)] = 0
            return vvjk__bcbvg
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
        dvlhu__ipdcj = len(arr)
        qsy__loaf = np.empty(dvlhu__ipdcj, np.bool_)
        for efozj__pln in numba.parfors.parfor.internal_prange(dvlhu__ipdcj):
            qsy__loaf[efozj__pln] = bodo.utils.conversion.box_if_dt64(arr[
                efozj__pln]) in values
        return qsy__loaf
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    puoxx__mgux = len(in_arr_tup) != 1
    szqda__tfxh = list(in_arr_tup.types)
    vlv__xvehv = 'def impl(in_arr_tup):\n'
    vlv__xvehv += '  n = len(in_arr_tup[0])\n'
    if puoxx__mgux:
        kls__akcn = ', '.join([f'in_arr_tup[{efozj__pln}][unused]' for
            efozj__pln in range(len(in_arr_tup))])
        oyp__dmwph = ', '.join(['False' for hko__duhwn in range(len(
            in_arr_tup))])
        vlv__xvehv += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({kls__akcn},), ({oyp__dmwph},)): 0 for unused in range(0)}}
"""
        vlv__xvehv += '  map_vector = np.empty(n, np.int64)\n'
        for efozj__pln, hvm__esng in enumerate(szqda__tfxh):
            vlv__xvehv += f'  in_lst_{efozj__pln} = []\n'
            if is_str_arr_type(hvm__esng):
                vlv__xvehv += f'  total_len_{efozj__pln} = 0\n'
            vlv__xvehv += f'  null_in_lst_{efozj__pln} = []\n'
        vlv__xvehv += '  for i in range(n):\n'
        ydmwi__ntil = ', '.join([f'in_arr_tup[{efozj__pln}][i]' for
            efozj__pln in range(len(szqda__tfxh))])
        gey__vqbuf = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{efozj__pln}], i)' for
            efozj__pln in range(len(szqda__tfxh))])
        vlv__xvehv += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({ydmwi__ntil},), ({gey__vqbuf},))
"""
        vlv__xvehv += '    if data_val not in arr_map:\n'
        vlv__xvehv += '      set_val = len(arr_map)\n'
        vlv__xvehv += '      values_tup = data_val._data\n'
        vlv__xvehv += '      nulls_tup = data_val._null_values\n'
        for efozj__pln, hvm__esng in enumerate(szqda__tfxh):
            vlv__xvehv += (
                f'      in_lst_{efozj__pln}.append(values_tup[{efozj__pln}])\n'
                )
            vlv__xvehv += (
                f'      null_in_lst_{efozj__pln}.append(nulls_tup[{efozj__pln}])\n'
                )
            if is_str_arr_type(hvm__esng):
                vlv__xvehv += f"""      total_len_{efozj__pln}  += nulls_tup[{efozj__pln}] * len(values_tup[{efozj__pln}])
"""
        vlv__xvehv += '      arr_map[data_val] = len(arr_map)\n'
        vlv__xvehv += '    else:\n'
        vlv__xvehv += '      set_val = arr_map[data_val]\n'
        vlv__xvehv += '    map_vector[i] = set_val\n'
        vlv__xvehv += '  n_rows = len(arr_map)\n'
        for efozj__pln, hvm__esng in enumerate(szqda__tfxh):
            if is_str_arr_type(hvm__esng):
                vlv__xvehv += f"""  out_arr_{efozj__pln} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{efozj__pln})
"""
            else:
                vlv__xvehv += f"""  out_arr_{efozj__pln} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{efozj__pln}], (-1,))
"""
        vlv__xvehv += '  for j in range(len(arr_map)):\n'
        for efozj__pln in range(len(szqda__tfxh)):
            vlv__xvehv += f'    if null_in_lst_{efozj__pln}[j]:\n'
            vlv__xvehv += (
                f'      bodo.libs.array_kernels.setna(out_arr_{efozj__pln}, j)\n'
                )
            vlv__xvehv += '    else:\n'
            vlv__xvehv += (
                f'      out_arr_{efozj__pln}[j] = in_lst_{efozj__pln}[j]\n')
        cndtb__nuucq = ', '.join([f'out_arr_{efozj__pln}' for efozj__pln in
            range(len(szqda__tfxh))])
        vlv__xvehv += f'  return ({cndtb__nuucq},), map_vector\n'
    else:
        vlv__xvehv += '  in_arr = in_arr_tup[0]\n'
        vlv__xvehv += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        vlv__xvehv += '  map_vector = np.empty(n, np.int64)\n'
        vlv__xvehv += '  is_na = 0\n'
        vlv__xvehv += '  in_lst = []\n'
        if is_str_arr_type(szqda__tfxh[0]):
            vlv__xvehv += '  total_len = 0\n'
        vlv__xvehv += '  for i in range(n):\n'
        vlv__xvehv += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        vlv__xvehv += '      is_na = 1\n'
        vlv__xvehv += (
            '      # Always put NA in the last location. We can safely use\n')
        vlv__xvehv += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        vlv__xvehv += '      set_val = -1\n'
        vlv__xvehv += '    else:\n'
        vlv__xvehv += '      data_val = in_arr[i]\n'
        vlv__xvehv += '      if data_val not in arr_map:\n'
        vlv__xvehv += '        set_val = len(arr_map)\n'
        vlv__xvehv += '        in_lst.append(data_val)\n'
        if is_str_arr_type(szqda__tfxh[0]):
            vlv__xvehv += '        total_len += len(data_val)\n'
        vlv__xvehv += '        arr_map[data_val] = len(arr_map)\n'
        vlv__xvehv += '      else:\n'
        vlv__xvehv += '        set_val = arr_map[data_val]\n'
        vlv__xvehv += '    map_vector[i] = set_val\n'
        vlv__xvehv += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(szqda__tfxh[0]):
            vlv__xvehv += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            vlv__xvehv += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        vlv__xvehv += '  for j in range(len(arr_map)):\n'
        vlv__xvehv += '    out_arr[j] = in_lst[j]\n'
        vlv__xvehv += '  if is_na:\n'
        vlv__xvehv += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        vlv__xvehv += f'  return (out_arr,), map_vector\n'
    mnaai__rku = {}
    exec(vlv__xvehv, {'bodo': bodo, 'np': np}, mnaai__rku)
    impl = mnaai__rku['impl']
    return impl
