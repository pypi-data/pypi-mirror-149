"""
Implements array kernels such as median and quantile.
"""
import hashlib
import inspect
import math
import operator
import re
import warnings
from math import sqrt
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types, typing
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_const, guard
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload, overload_attribute, register_jitable
from numba.np.arrayobj import make_array
from numba.np.numpy_support import as_dtype
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, init_categorical_array
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import quantile_alg
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, drop_duplicates_table, info_from_table, info_to_array, sample_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import DictionaryArrayType
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import str_arr_set_na, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, check_unsupported_args, decode_if_dict_array, element_type, find_common_np_dtype, get_overload_const_bool, get_overload_const_list, get_overload_const_str, is_overload_none, is_str_arr_type, raise_bodo_error, to_str_arr_if_dict_array
from bodo.utils.utils import build_set_seen_na, check_and_propagate_cpp_exception, numba_to_c_type, unliteral_all
ll.add_symbol('quantile_sequential', quantile_alg.quantile_sequential)
ll.add_symbol('quantile_parallel', quantile_alg.quantile_parallel)
MPI_ROOT = 0
sum_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)
max_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Max.value)
min_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Min.value)


def isna(arr, i):
    return False


@overload(isna)
def overload_isna(arr, i):
    i = types.unliteral(i)
    if arr == string_array_type:
        return lambda arr, i: bodo.libs.str_arr_ext.str_arr_is_na(arr, i)
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type,
        datetime_timedelta_array_type, string_array_split_view_type):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._null_bitmap, i)
    if isinstance(arr, ArrayItemArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, StructArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.struct_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, TupleArrayType):
        return lambda arr, i: bodo.libs.array_kernels.isna(arr._data, i)
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return lambda arr, i: arr.codes[i] == -1
    if arr == bodo.binary_array_type:
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, types.List):
        if arr.dtype == types.none:
            return lambda arr, i: True
        elif isinstance(arr.dtype, types.optional):
            return lambda arr, i: arr[i] is None
        else:
            return lambda arr, i: False
    if isinstance(arr, bodo.NullableTupleType):
        return lambda arr, i: arr._null_values[i]
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._indices._null_bitmap, i) or bodo.libs.array_kernels.isna(arr.
            _data, arr._indices[i])
    if isinstance(arr, DatetimeArrayType):
        return lambda arr, i: np.isnat(arr._data[i])
    assert isinstance(arr, types.Array), f'Invalid array type in isna(): {arr}'
    dtype = arr.dtype
    if isinstance(dtype, types.Float):
        return lambda arr, i: np.isnan(arr[i])
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)):
        return lambda arr, i: np.isnat(arr[i])
    return lambda arr, i: False


def setna(arr, ind, int_nan_const=0):
    arr[ind] = np.nan


@overload(setna, no_unliteral=True)
def setna_overload(arr, ind, int_nan_const=0):
    if isinstance(arr.dtype, types.Float):
        return setna
    if isinstance(arr.dtype, (types.NPDatetime, types.NPTimedelta)):
        isez__utfv = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = isez__utfv
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        isez__utfv = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = isez__utfv
        return _setnan_impl
    if arr == string_array_type:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = ''
            str_arr_set_na(arr, ind)
        return impl
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, ind, int_nan_const=0: bodo.libs.array_kernels.setna(
            arr._indices, ind)
    if arr == boolean_array:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = False
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)):
        return (lambda arr, ind, int_nan_const=0: bodo.libs.int_arr_ext.
            set_bit_to_arr(arr._null_bitmap, ind, 0))
    if arr == bodo.binary_array_type:

        def impl_binary_arr(arr, ind, int_nan_const=0):
            afjf__qabf = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            afjf__qabf[ind + 1] = afjf__qabf[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            afjf__qabf = bodo.libs.array_item_arr_ext.get_offsets(arr)
            afjf__qabf[ind + 1] = afjf__qabf[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.struct_arr_ext.StructArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.struct_arr_ext.
                get_null_bitmap(arr), ind, 0)
            data = bodo.libs.struct_arr_ext.get_data(arr)
            setna_tup(data, ind)
        return impl
    if isinstance(arr, TupleArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._data, ind)
        return impl
    if arr.dtype == types.bool_:

        def b_set(arr, ind, int_nan_const=0):
            arr[ind] = False
        return b_set
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):

        def setna_cat(arr, ind, int_nan_const=0):
            arr.codes[ind] = -1
        return setna_cat
    if isinstance(arr.dtype, types.Integer):

        def setna_int(arr, ind, int_nan_const=0):
            arr[ind] = int_nan_const
        return setna_int
    if arr == datetime_date_array_type:

        def setna_datetime_date(arr, ind, int_nan_const=0):
            arr._data[ind] = (1970 << 32) + (1 << 16) + 1
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_date
    if arr == datetime_timedelta_array_type:

        def setna_datetime_timedelta(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._days_data, ind)
            bodo.libs.array_kernels.setna(arr._seconds_data, ind)
            bodo.libs.array_kernels.setna(arr._microseconds_data, ind)
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_timedelta
    return lambda arr, ind, int_nan_const=0: None


def setna_tup(arr_tup, ind, int_nan_const=0):
    for arr in arr_tup:
        arr[ind] = np.nan


@overload(setna_tup, no_unliteral=True)
def overload_setna_tup(arr_tup, ind, int_nan_const=0):
    zlj__dnwwm = arr_tup.count
    xcu__dgn = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(zlj__dnwwm):
        xcu__dgn += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    xcu__dgn += '  return\n'
    rdjbn__wyuc = {}
    exec(xcu__dgn, {'setna': setna}, rdjbn__wyuc)
    impl = rdjbn__wyuc['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        kxag__sdn = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(kxag__sdn.start, kxag__sdn.stop, kxag__sdn.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        jgthq__ptxc = 'n'
        nka__qog = 'n_pes'
        rar__srtv = 'min_op'
    else:
        jgthq__ptxc = 'n-1, -1, -1'
        nka__qog = '-1'
        rar__srtv = 'max_op'
    xcu__dgn = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {nka__qog}
    for i in range({jgthq__ptxc}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {rar__srtv}))
        if possible_valid_rank != {nka__qog}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    rdjbn__wyuc = {}
    exec(xcu__dgn, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op': max_op,
        'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.box_if_dt64},
        rdjbn__wyuc)
    impl = rdjbn__wyuc['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    mnyfs__apmf = array_to_info(arr)
    _median_series_computation(res, mnyfs__apmf, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(mnyfs__apmf)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    mnyfs__apmf = array_to_info(arr)
    _autocorr_series_computation(res, mnyfs__apmf, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(mnyfs__apmf)


@numba.njit
def autocorr(arr, lag=1, parallel=False):
    res = np.empty(1, types.float64)
    autocorr_series_computation(res.ctypes, arr, lag, parallel)
    return res[0]


ll.add_symbol('compute_series_monotonicity', quantile_alg.
    compute_series_monotonicity)
_compute_series_monotonicity = types.ExternalFunction(
    'compute_series_monotonicity', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def series_monotonicity_call(res, arr, inc_dec, is_parallel):
    mnyfs__apmf = array_to_info(arr)
    _compute_series_monotonicity(res, mnyfs__apmf, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(mnyfs__apmf)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    omze__bbl = res[0] > 0.5
    return omze__bbl


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        pwfl__wrzoj = '-'
        gttx__xkstu = 'index_arr[0] > threshhold_date'
        jgthq__ptxc = '1, n+1'
        gyr__nku = 'index_arr[-i] <= threshhold_date'
        lsxw__zea = 'i - 1'
    else:
        pwfl__wrzoj = '+'
        gttx__xkstu = 'index_arr[-1] < threshhold_date'
        jgthq__ptxc = 'n'
        gyr__nku = 'index_arr[i] >= threshhold_date'
        lsxw__zea = 'i'
    xcu__dgn = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        xcu__dgn += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        xcu__dgn += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            xcu__dgn += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            xcu__dgn += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            xcu__dgn += '    else:\n'
            xcu__dgn += '      threshhold_date = initial_date + date_offset\n'
        else:
            xcu__dgn += (
                f'    threshhold_date = initial_date {pwfl__wrzoj} date_offset\n'
                )
    else:
        xcu__dgn += f'  threshhold_date = initial_date {pwfl__wrzoj} offset\n'
    xcu__dgn += '  local_valid = 0\n'
    xcu__dgn += f'  n = len(index_arr)\n'
    xcu__dgn += f'  if n:\n'
    xcu__dgn += f'    if {gttx__xkstu}:\n'
    xcu__dgn += '      loc_valid = n\n'
    xcu__dgn += '    else:\n'
    xcu__dgn += f'      for i in range({jgthq__ptxc}):\n'
    xcu__dgn += f'        if {gyr__nku}:\n'
    xcu__dgn += f'          loc_valid = {lsxw__zea}\n'
    xcu__dgn += '          break\n'
    xcu__dgn += '  if is_parallel:\n'
    xcu__dgn += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    xcu__dgn += '    return total_valid\n'
    xcu__dgn += '  else:\n'
    xcu__dgn += '    return loc_valid\n'
    rdjbn__wyuc = {}
    exec(xcu__dgn, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, rdjbn__wyuc)
    return rdjbn__wyuc['impl']


def quantile(A, q):
    return 0


def quantile_parallel(A, q):
    return 0


@infer_global(quantile)
@infer_global(quantile_parallel)
class QuantileType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) in [2, 3]
        return signature(types.float64, *unliteral_all(args))


@lower_builtin(quantile, types.Array, types.float64)
@lower_builtin(quantile, IntegerArrayType, types.float64)
@lower_builtin(quantile, BooleanArrayType, types.float64)
def lower_dist_quantile_seq(context, builder, sig, args):
    nxh__rjady = numba_to_c_type(sig.args[0].dtype)
    cfw__hkveg = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), nxh__rjady))
    ppk__uucm = args[0]
    egu__bml = sig.args[0]
    if isinstance(egu__bml, (IntegerArrayType, BooleanArrayType)):
        ppk__uucm = cgutils.create_struct_proxy(egu__bml)(context, builder,
            ppk__uucm).data
        egu__bml = types.Array(egu__bml.dtype, 1, 'C')
    assert egu__bml.ndim == 1
    arr = make_array(egu__bml)(context, builder, ppk__uucm)
    iqbso__ippo = builder.extract_value(arr.shape, 0)
    iqa__hqk = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        iqbso__ippo, args[1], builder.load(cfw__hkveg)]
    uvj__apn = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    uqom__bqzf = lir.FunctionType(lir.DoubleType(), uvj__apn)
    lptom__objac = cgutils.get_or_insert_function(builder.module,
        uqom__bqzf, name='quantile_sequential')
    sdi__nlk = builder.call(lptom__objac, iqa__hqk)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return sdi__nlk


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    nxh__rjady = numba_to_c_type(sig.args[0].dtype)
    cfw__hkveg = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), nxh__rjady))
    ppk__uucm = args[0]
    egu__bml = sig.args[0]
    if isinstance(egu__bml, (IntegerArrayType, BooleanArrayType)):
        ppk__uucm = cgutils.create_struct_proxy(egu__bml)(context, builder,
            ppk__uucm).data
        egu__bml = types.Array(egu__bml.dtype, 1, 'C')
    assert egu__bml.ndim == 1
    arr = make_array(egu__bml)(context, builder, ppk__uucm)
    iqbso__ippo = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        izfdn__zcmml = args[2]
    else:
        izfdn__zcmml = iqbso__ippo
    iqa__hqk = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        iqbso__ippo, izfdn__zcmml, args[1], builder.load(cfw__hkveg)]
    uvj__apn = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType(
        64), lir.DoubleType(), lir.IntType(32)]
    uqom__bqzf = lir.FunctionType(lir.DoubleType(), uvj__apn)
    lptom__objac = cgutils.get_or_insert_function(builder.module,
        uqom__bqzf, name='quantile_parallel')
    sdi__nlk = builder.call(lptom__objac, iqa__hqk)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return sdi__nlk


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    vpdoz__govp = start
    dku__qxat = 2 * start + 1
    zga__vgvop = 2 * start + 2
    if dku__qxat < n and not cmp_f(arr[dku__qxat], arr[vpdoz__govp]):
        vpdoz__govp = dku__qxat
    if zga__vgvop < n and not cmp_f(arr[zga__vgvop], arr[vpdoz__govp]):
        vpdoz__govp = zga__vgvop
    if vpdoz__govp != start:
        arr[start], arr[vpdoz__govp] = arr[vpdoz__govp], arr[start]
        ind_arr[start], ind_arr[vpdoz__govp] = ind_arr[vpdoz__govp], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, vpdoz__govp, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        dmg__aiee = np.empty(k, A.dtype)
        loncm__qjy = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                dmg__aiee[ind] = A[i]
                loncm__qjy[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            dmg__aiee = dmg__aiee[:ind]
            loncm__qjy = loncm__qjy[:ind]
        return dmg__aiee, loncm__qjy, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        xttck__xsflg = np.sort(A)
        atnka__xre = index_arr[np.argsort(A)]
        qja__pgs = pd.Series(xttck__xsflg).notna().values
        xttck__xsflg = xttck__xsflg[qja__pgs]
        atnka__xre = atnka__xre[qja__pgs]
        if is_largest:
            xttck__xsflg = xttck__xsflg[::-1]
            atnka__xre = atnka__xre[::-1]
        return np.ascontiguousarray(xttck__xsflg), np.ascontiguousarray(
            atnka__xre)
    dmg__aiee, loncm__qjy, start = select_k_nonan(A, index_arr, m, k)
    loncm__qjy = loncm__qjy[dmg__aiee.argsort()]
    dmg__aiee.sort()
    if not is_largest:
        dmg__aiee = np.ascontiguousarray(dmg__aiee[::-1])
        loncm__qjy = np.ascontiguousarray(loncm__qjy[::-1])
    for i in range(start, m):
        if cmp_f(A[i], dmg__aiee[0]):
            dmg__aiee[0] = A[i]
            loncm__qjy[0] = index_arr[i]
            min_heapify(dmg__aiee, loncm__qjy, k, 0, cmp_f)
    loncm__qjy = loncm__qjy[dmg__aiee.argsort()]
    dmg__aiee.sort()
    if is_largest:
        dmg__aiee = dmg__aiee[::-1]
        loncm__qjy = loncm__qjy[::-1]
    return np.ascontiguousarray(dmg__aiee), np.ascontiguousarray(loncm__qjy)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    lpb__qohy = bodo.libs.distributed_api.get_rank()
    usxyr__dhcsg, phzfv__pjtib = nlargest(A, I, k, is_largest, cmp_f)
    sjqq__vtin = bodo.libs.distributed_api.gatherv(usxyr__dhcsg)
    geeg__mcqks = bodo.libs.distributed_api.gatherv(phzfv__pjtib)
    if lpb__qohy == MPI_ROOT:
        res, mfnv__cvqzr = nlargest(sjqq__vtin, geeg__mcqks, k, is_largest,
            cmp_f)
    else:
        res = np.empty(k, A.dtype)
        mfnv__cvqzr = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(mfnv__cvqzr)
    return res, mfnv__cvqzr


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    hzsur__kvqaw, nvf__apmc = mat.shape
    fgkrz__oaflz = np.empty((nvf__apmc, nvf__apmc), dtype=np.float64)
    for kyoe__ate in range(nvf__apmc):
        for oxcf__iwt in range(kyoe__ate + 1):
            eci__tcxfp = 0
            idk__inqm = tjxv__uhr = hka__ylg = dcebw__rdiyk = 0.0
            for i in range(hzsur__kvqaw):
                if np.isfinite(mat[i, kyoe__ate]) and np.isfinite(mat[i,
                    oxcf__iwt]):
                    iiafy__zqrmz = mat[i, kyoe__ate]
                    usod__hsl = mat[i, oxcf__iwt]
                    eci__tcxfp += 1
                    hka__ylg += iiafy__zqrmz
                    dcebw__rdiyk += usod__hsl
            if parallel:
                eci__tcxfp = bodo.libs.distributed_api.dist_reduce(eci__tcxfp,
                    sum_op)
                hka__ylg = bodo.libs.distributed_api.dist_reduce(hka__ylg,
                    sum_op)
                dcebw__rdiyk = bodo.libs.distributed_api.dist_reduce(
                    dcebw__rdiyk, sum_op)
            if eci__tcxfp < minpv:
                fgkrz__oaflz[kyoe__ate, oxcf__iwt] = fgkrz__oaflz[oxcf__iwt,
                    kyoe__ate] = np.nan
            else:
                ztlf__wod = hka__ylg / eci__tcxfp
                lrstj__ogqis = dcebw__rdiyk / eci__tcxfp
                hka__ylg = 0.0
                for i in range(hzsur__kvqaw):
                    if np.isfinite(mat[i, kyoe__ate]) and np.isfinite(mat[i,
                        oxcf__iwt]):
                        iiafy__zqrmz = mat[i, kyoe__ate] - ztlf__wod
                        usod__hsl = mat[i, oxcf__iwt] - lrstj__ogqis
                        hka__ylg += iiafy__zqrmz * usod__hsl
                        idk__inqm += iiafy__zqrmz * iiafy__zqrmz
                        tjxv__uhr += usod__hsl * usod__hsl
                if parallel:
                    hka__ylg = bodo.libs.distributed_api.dist_reduce(hka__ylg,
                        sum_op)
                    idk__inqm = bodo.libs.distributed_api.dist_reduce(idk__inqm
                        , sum_op)
                    tjxv__uhr = bodo.libs.distributed_api.dist_reduce(tjxv__uhr
                        , sum_op)
                fus__vbfvt = eci__tcxfp - 1.0 if cov else sqrt(idk__inqm *
                    tjxv__uhr)
                if fus__vbfvt != 0.0:
                    fgkrz__oaflz[kyoe__ate, oxcf__iwt] = fgkrz__oaflz[
                        oxcf__iwt, kyoe__ate] = hka__ylg / fus__vbfvt
                else:
                    fgkrz__oaflz[kyoe__ate, oxcf__iwt] = fgkrz__oaflz[
                        oxcf__iwt, kyoe__ate] = np.nan
    return fgkrz__oaflz


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    ahvj__dunx = n != 1
    xcu__dgn = 'def impl(data, parallel=False):\n'
    xcu__dgn += '  if parallel:\n'
    cxw__rzgkl = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    xcu__dgn += f'    cpp_table = arr_info_list_to_table([{cxw__rzgkl}])\n'
    xcu__dgn += (
        f'    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)\n'
        )
    zuw__qjol = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    xcu__dgn += f'    data = ({zuw__qjol},)\n'
    xcu__dgn += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    xcu__dgn += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    xcu__dgn += '    bodo.libs.array.delete_table(cpp_table)\n'
    xcu__dgn += '  n = len(data[0])\n'
    xcu__dgn += '  out = np.empty(n, np.bool_)\n'
    xcu__dgn += '  uniqs = dict()\n'
    if ahvj__dunx:
        xcu__dgn += '  for i in range(n):\n'
        fyhw__drdsj = ', '.join(f'data[{i}][i]' for i in range(n))
        omyfx__gzuv = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        xcu__dgn += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({fyhw__drdsj},), ({omyfx__gzuv},))
"""
        xcu__dgn += '    if val in uniqs:\n'
        xcu__dgn += '      out[i] = True\n'
        xcu__dgn += '    else:\n'
        xcu__dgn += '      out[i] = False\n'
        xcu__dgn += '      uniqs[val] = 0\n'
    else:
        xcu__dgn += '  data = data[0]\n'
        xcu__dgn += '  hasna = False\n'
        xcu__dgn += '  for i in range(n):\n'
        xcu__dgn += '    if bodo.libs.array_kernels.isna(data, i):\n'
        xcu__dgn += '      out[i] = hasna\n'
        xcu__dgn += '      hasna = True\n'
        xcu__dgn += '    else:\n'
        xcu__dgn += '      val = data[i]\n'
        xcu__dgn += '      if val in uniqs:\n'
        xcu__dgn += '        out[i] = True\n'
        xcu__dgn += '      else:\n'
        xcu__dgn += '        out[i] = False\n'
        xcu__dgn += '        uniqs[val] = 0\n'
    xcu__dgn += '  if parallel:\n'
    xcu__dgn += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    xcu__dgn += '  return out\n'
    rdjbn__wyuc = {}
    exec(xcu__dgn, {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table}, rdjbn__wyuc)
    impl = rdjbn__wyuc['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    zlj__dnwwm = len(data)
    xcu__dgn = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    xcu__dgn += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        zlj__dnwwm)))
    xcu__dgn += '  table_total = arr_info_list_to_table(info_list_total)\n'
    xcu__dgn += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(zlj__dnwwm))
    for mcsvo__admt in range(zlj__dnwwm):
        xcu__dgn += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(mcsvo__admt, mcsvo__admt, mcsvo__admt))
    xcu__dgn += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(zlj__dnwwm))
    xcu__dgn += '  delete_table(out_table)\n'
    xcu__dgn += '  delete_table(table_total)\n'
    xcu__dgn += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(zlj__dnwwm)))
    rdjbn__wyuc = {}
    exec(xcu__dgn, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'sample_table': sample_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, rdjbn__wyuc)
    impl = rdjbn__wyuc['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    zlj__dnwwm = len(data)
    xcu__dgn = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    xcu__dgn += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        zlj__dnwwm)))
    xcu__dgn += '  table_total = arr_info_list_to_table(info_list_total)\n'
    xcu__dgn += '  keep_i = 0\n'
    xcu__dgn += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for mcsvo__admt in range(zlj__dnwwm):
        xcu__dgn += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(mcsvo__admt, mcsvo__admt, mcsvo__admt))
    xcu__dgn += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(zlj__dnwwm))
    xcu__dgn += '  delete_table(out_table)\n'
    xcu__dgn += '  delete_table(table_total)\n'
    xcu__dgn += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(zlj__dnwwm)))
    rdjbn__wyuc = {}
    exec(xcu__dgn, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, rdjbn__wyuc)
    impl = rdjbn__wyuc['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        tpch__ziokf = [array_to_info(data_arr)]
        pajqf__zjrvj = arr_info_list_to_table(tpch__ziokf)
        stsku__yff = 0
        jhvub__tao = drop_duplicates_table(pajqf__zjrvj, parallel, 1,
            stsku__yff, False, True)
        mhynn__eldsl = info_to_array(info_from_table(jhvub__tao, 0), data_arr)
        delete_table(jhvub__tao)
        delete_table(pajqf__zjrvj)
        return mhynn__eldsl
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    aelgo__wvhg = len(data.types)
    jrzcc__fnmg = [('out' + str(i)) for i in range(aelgo__wvhg)]
    rshdc__hvy = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    gjh__smcgh = ['isna(data[{}], i)'.format(i) for i in rshdc__hvy]
    mfesr__rkra = 'not ({})'.format(' or '.join(gjh__smcgh))
    if not is_overload_none(thresh):
        mfesr__rkra = '(({}) <= ({}) - thresh)'.format(' + '.join(
            gjh__smcgh), aelgo__wvhg - 1)
    elif how == 'all':
        mfesr__rkra = 'not ({})'.format(' and '.join(gjh__smcgh))
    xcu__dgn = 'def _dropna_imp(data, how, thresh, subset):\n'
    xcu__dgn += '  old_len = len(data[0])\n'
    xcu__dgn += '  new_len = 0\n'
    xcu__dgn += '  for i in range(old_len):\n'
    xcu__dgn += '    if {}:\n'.format(mfesr__rkra)
    xcu__dgn += '      new_len += 1\n'
    for i, out in enumerate(jrzcc__fnmg):
        if isinstance(data[i], bodo.CategoricalArrayType):
            xcu__dgn += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            xcu__dgn += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    xcu__dgn += '  curr_ind = 0\n'
    xcu__dgn += '  for i in range(old_len):\n'
    xcu__dgn += '    if {}:\n'.format(mfesr__rkra)
    for i in range(aelgo__wvhg):
        xcu__dgn += '      if isna(data[{}], i):\n'.format(i)
        xcu__dgn += '        setna({}, curr_ind)\n'.format(jrzcc__fnmg[i])
        xcu__dgn += '      else:\n'
        xcu__dgn += '        {}[curr_ind] = data[{}][i]\n'.format(jrzcc__fnmg
            [i], i)
    xcu__dgn += '      curr_ind += 1\n'
    xcu__dgn += '  return {}\n'.format(', '.join(jrzcc__fnmg))
    rdjbn__wyuc = {}
    uxb__bhz = {'t{}'.format(i): zae__eoiz for i, zae__eoiz in enumerate(
        data.types)}
    uxb__bhz.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(xcu__dgn, uxb__bhz, rdjbn__wyuc)
    feh__thh = rdjbn__wyuc['_dropna_imp']
    return feh__thh


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        egu__bml = arr.dtype
        calzb__mysd = egu__bml.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            smhet__jyxyr = init_nested_counts(calzb__mysd)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                smhet__jyxyr = add_nested_counts(smhet__jyxyr, val[ind])
            mhynn__eldsl = bodo.utils.utils.alloc_type(n, egu__bml,
                smhet__jyxyr)
            for igock__snmv in range(n):
                if bodo.libs.array_kernels.isna(arr, igock__snmv):
                    setna(mhynn__eldsl, igock__snmv)
                    continue
                val = arr[igock__snmv]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(mhynn__eldsl, igock__snmv)
                    continue
                mhynn__eldsl[igock__snmv] = val[ind]
            return mhynn__eldsl
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    jadh__jokxg = _to_readonly(arr_types.types[0])
    return all(isinstance(zae__eoiz, CategoricalArrayType) and _to_readonly
        (zae__eoiz) == jadh__jokxg for zae__eoiz in arr_types.types)


def concat(arr_list):
    return pd.concat(arr_list)


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arr_list.
        dtype, 'bodo.concat()')
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        jmwfj__pyxv = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            xos__nzy = 0
            flpmn__ekxa = []
            for A in arr_list:
                jlgbe__ljr = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                flpmn__ekxa.append(bodo.libs.array_item_arr_ext.get_data(A))
                xos__nzy += jlgbe__ljr
            fted__ewzq = np.empty(xos__nzy + 1, offset_type)
            yjg__crbj = bodo.libs.array_kernels.concat(flpmn__ekxa)
            npd__pcxv = np.empty(xos__nzy + 7 >> 3, np.uint8)
            ueoxe__phz = 0
            eqlq__apfcm = 0
            for A in arr_list:
                chzk__fft = bodo.libs.array_item_arr_ext.get_offsets(A)
                frcxd__wvojw = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                jlgbe__ljr = len(A)
                yfagy__pdrn = chzk__fft[jlgbe__ljr]
                for i in range(jlgbe__ljr):
                    fted__ewzq[i + ueoxe__phz] = chzk__fft[i] + eqlq__apfcm
                    xrdvn__hbevl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        frcxd__wvojw, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(npd__pcxv, i +
                        ueoxe__phz, xrdvn__hbevl)
                ueoxe__phz += jlgbe__ljr
                eqlq__apfcm += yfagy__pdrn
            fted__ewzq[ueoxe__phz] = eqlq__apfcm
            mhynn__eldsl = bodo.libs.array_item_arr_ext.init_array_item_array(
                xos__nzy, yjg__crbj, fted__ewzq, npd__pcxv)
            return mhynn__eldsl
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        pyvo__hifw = arr_list.dtype.names
        xcu__dgn = 'def struct_array_concat_impl(arr_list):\n'
        xcu__dgn += f'    n_all = 0\n'
        for i in range(len(pyvo__hifw)):
            xcu__dgn += f'    concat_list{i} = []\n'
        xcu__dgn += '    for A in arr_list:\n'
        xcu__dgn += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(pyvo__hifw)):
            xcu__dgn += f'        concat_list{i}.append(data_tuple[{i}])\n'
        xcu__dgn += '        n_all += len(A)\n'
        xcu__dgn += '    n_bytes = (n_all + 7) >> 3\n'
        xcu__dgn += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        xcu__dgn += '    curr_bit = 0\n'
        xcu__dgn += '    for A in arr_list:\n'
        xcu__dgn += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        xcu__dgn += '        for j in range(len(A)):\n'
        xcu__dgn += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        xcu__dgn += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        xcu__dgn += '            curr_bit += 1\n'
        xcu__dgn += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        yii__srrx = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(pyvo__hifw))])
        xcu__dgn += f'        ({yii__srrx},),\n'
        xcu__dgn += '        new_mask,\n'
        xcu__dgn += f'        {pyvo__hifw},\n'
        xcu__dgn += '    )\n'
        rdjbn__wyuc = {}
        exec(xcu__dgn, {'bodo': bodo, 'np': np}, rdjbn__wyuc)
        return rdjbn__wyuc['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            eixx__pexo = 0
            for A in arr_list:
                eixx__pexo += len(A)
            gjmh__bsvd = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(eixx__pexo))
            bilpb__kaq = 0
            for A in arr_list:
                for i in range(len(A)):
                    gjmh__bsvd._data[i + bilpb__kaq] = A._data[i]
                    xrdvn__hbevl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gjmh__bsvd.
                        _null_bitmap, i + bilpb__kaq, xrdvn__hbevl)
                bilpb__kaq += len(A)
            return gjmh__bsvd
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            eixx__pexo = 0
            for A in arr_list:
                eixx__pexo += len(A)
            gjmh__bsvd = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(eixx__pexo))
            bilpb__kaq = 0
            for A in arr_list:
                for i in range(len(A)):
                    gjmh__bsvd._days_data[i + bilpb__kaq] = A._days_data[i]
                    gjmh__bsvd._seconds_data[i + bilpb__kaq] = A._seconds_data[
                        i]
                    gjmh__bsvd._microseconds_data[i + bilpb__kaq
                        ] = A._microseconds_data[i]
                    xrdvn__hbevl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gjmh__bsvd.
                        _null_bitmap, i + bilpb__kaq, xrdvn__hbevl)
                bilpb__kaq += len(A)
            return gjmh__bsvd
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        uyrk__orw = arr_list.dtype.precision
        rnsu__zuuxi = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            eixx__pexo = 0
            for A in arr_list:
                eixx__pexo += len(A)
            gjmh__bsvd = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                eixx__pexo, uyrk__orw, rnsu__zuuxi)
            bilpb__kaq = 0
            for A in arr_list:
                for i in range(len(A)):
                    gjmh__bsvd._data[i + bilpb__kaq] = A._data[i]
                    xrdvn__hbevl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gjmh__bsvd.
                        _null_bitmap, i + bilpb__kaq, xrdvn__hbevl)
                bilpb__kaq += len(A)
            return gjmh__bsvd
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        zae__eoiz) for zae__eoiz in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            ziu__gdahq = arr_list.types[0]
        else:
            ziu__gdahq = arr_list.dtype
        ziu__gdahq = to_str_arr_if_dict_array(ziu__gdahq)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            npg__iflc = 0
            vlo__hwjv = 0
            for A in arr_list:
                arr = A
                npg__iflc += len(arr)
                vlo__hwjv += bodo.libs.str_arr_ext.num_total_chars(arr)
            mhynn__eldsl = bodo.utils.utils.alloc_type(npg__iflc,
                ziu__gdahq, (vlo__hwjv,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(mhynn__eldsl, -1)
            pisu__bmmtx = 0
            aruq__ahsf = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(mhynn__eldsl,
                    arr, pisu__bmmtx, aruq__ahsf)
                pisu__bmmtx += len(arr)
                aruq__ahsf += bodo.libs.str_arr_ext.num_total_chars(arr)
            return mhynn__eldsl
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(zae__eoiz.dtype, types.Integer) for
        zae__eoiz in arr_list.types) and any(isinstance(zae__eoiz,
        IntegerArrayType) for zae__eoiz in arr_list.types):

        def impl_int_arr_list(arr_list):
            bfxs__bps = convert_to_nullable_tup(arr_list)
            dqu__avknq = []
            rnn__pgej = 0
            for A in bfxs__bps:
                dqu__avknq.append(A._data)
                rnn__pgej += len(A)
            yjg__crbj = bodo.libs.array_kernels.concat(dqu__avknq)
            xqloi__rsbd = rnn__pgej + 7 >> 3
            dvjje__upxl = np.empty(xqloi__rsbd, np.uint8)
            ehfma__lrtsi = 0
            for A in bfxs__bps:
                ade__iym = A._null_bitmap
                for igock__snmv in range(len(A)):
                    xrdvn__hbevl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        ade__iym, igock__snmv)
                    bodo.libs.int_arr_ext.set_bit_to_arr(dvjje__upxl,
                        ehfma__lrtsi, xrdvn__hbevl)
                    ehfma__lrtsi += 1
            return bodo.libs.int_arr_ext.init_integer_array(yjg__crbj,
                dvjje__upxl)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(zae__eoiz.dtype == types.bool_ for zae__eoiz in
        arr_list.types) and any(zae__eoiz == boolean_array for zae__eoiz in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            bfxs__bps = convert_to_nullable_tup(arr_list)
            dqu__avknq = []
            rnn__pgej = 0
            for A in bfxs__bps:
                dqu__avknq.append(A._data)
                rnn__pgej += len(A)
            yjg__crbj = bodo.libs.array_kernels.concat(dqu__avknq)
            xqloi__rsbd = rnn__pgej + 7 >> 3
            dvjje__upxl = np.empty(xqloi__rsbd, np.uint8)
            ehfma__lrtsi = 0
            for A in bfxs__bps:
                ade__iym = A._null_bitmap
                for igock__snmv in range(len(A)):
                    xrdvn__hbevl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        ade__iym, igock__snmv)
                    bodo.libs.int_arr_ext.set_bit_to_arr(dvjje__upxl,
                        ehfma__lrtsi, xrdvn__hbevl)
                    ehfma__lrtsi += 1
            return bodo.libs.bool_arr_ext.init_bool_array(yjg__crbj,
                dvjje__upxl)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            dbbcc__ucfcf = []
            for A in arr_list:
                dbbcc__ucfcf.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                dbbcc__ucfcf), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        myrza__sik = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        xcu__dgn = 'def impl(arr_list):\n'
        xcu__dgn += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({myrza__sik},)), arr_list[0].dtype)
"""
        wrs__icy = {}
        exec(xcu__dgn, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, wrs__icy)
        return wrs__icy['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            rnn__pgej = 0
            for A in arr_list:
                rnn__pgej += len(A)
            mhynn__eldsl = np.empty(rnn__pgej, dtype)
            quh__fcwnp = 0
            for A in arr_list:
                n = len(A)
                mhynn__eldsl[quh__fcwnp:quh__fcwnp + n] = A
                quh__fcwnp += n
            return mhynn__eldsl
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(zae__eoiz,
        (types.Array, IntegerArrayType)) and isinstance(zae__eoiz.dtype,
        types.Integer) for zae__eoiz in arr_list.types) and any(isinstance(
        zae__eoiz, types.Array) and isinstance(zae__eoiz.dtype, types.Float
        ) for zae__eoiz in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            syyk__sgoc = []
            for A in arr_list:
                syyk__sgoc.append(A._data)
            liy__yll = bodo.libs.array_kernels.concat(syyk__sgoc)
            fgkrz__oaflz = bodo.libs.map_arr_ext.init_map_arr(liy__yll)
            return fgkrz__oaflz
        return impl_map_arr_list
    for slgf__xzp in arr_list:
        if not isinstance(slgf__xzp, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(zae__eoiz.astype(np.float64) for zae__eoiz in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    zlj__dnwwm = len(arr_tup.types)
    xcu__dgn = 'def f(arr_tup):\n'
    xcu__dgn += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        zlj__dnwwm)), ',' if zlj__dnwwm == 1 else '')
    rdjbn__wyuc = {}
    exec(xcu__dgn, {'np': np}, rdjbn__wyuc)
    uivdy__azd = rdjbn__wyuc['f']
    return uivdy__azd


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    zlj__dnwwm = len(arr_tup.types)
    xbyny__qoehm = find_common_np_dtype(arr_tup.types)
    calzb__mysd = None
    uvwu__mtqw = ''
    if isinstance(xbyny__qoehm, types.Integer):
        calzb__mysd = bodo.libs.int_arr_ext.IntDtype(xbyny__qoehm)
        uvwu__mtqw = '.astype(out_dtype, False)'
    xcu__dgn = 'def f(arr_tup):\n'
    xcu__dgn += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, uvwu__mtqw) for i in range(zlj__dnwwm)), ',' if 
        zlj__dnwwm == 1 else '')
    rdjbn__wyuc = {}
    exec(xcu__dgn, {'bodo': bodo, 'out_dtype': calzb__mysd}, rdjbn__wyuc)
    lrpg__ykskm = rdjbn__wyuc['f']
    return lrpg__ykskm


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, vtv__wyl = build_set_seen_na(A)
        return len(s) + int(not dropna and vtv__wyl)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        qor__xogmq = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        reoz__fjy = len(qor__xogmq)
        return bodo.libs.distributed_api.dist_reduce(reoz__fjy, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([gety__fqinm for gety__fqinm in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        ynxlq__vryp = np.finfo(A.dtype(1).dtype).max
    else:
        ynxlq__vryp = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        mhynn__eldsl = np.empty(n, A.dtype)
        rxtjl__dvvq = ynxlq__vryp
        for i in range(n):
            rxtjl__dvvq = min(rxtjl__dvvq, A[i])
            mhynn__eldsl[i] = rxtjl__dvvq
        return mhynn__eldsl
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        ynxlq__vryp = np.finfo(A.dtype(1).dtype).min
    else:
        ynxlq__vryp = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        mhynn__eldsl = np.empty(n, A.dtype)
        rxtjl__dvvq = ynxlq__vryp
        for i in range(n):
            rxtjl__dvvq = max(rxtjl__dvvq, A[i])
            mhynn__eldsl[i] = rxtjl__dvvq
        return mhynn__eldsl
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        krva__ofm = arr_info_list_to_table([array_to_info(A)])
        kezj__wycot = 1
        stsku__yff = 0
        jhvub__tao = drop_duplicates_table(krva__ofm, parallel, kezj__wycot,
            stsku__yff, dropna, True)
        mhynn__eldsl = info_to_array(info_from_table(jhvub__tao, 0), A)
        delete_table(krva__ofm)
        delete_table(jhvub__tao)
        return mhynn__eldsl
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    jmwfj__pyxv = bodo.utils.typing.to_nullable_type(arr.dtype)
    sbv__aphsa = index_arr
    dblq__zqias = sbv__aphsa.dtype

    def impl(arr, index_arr):
        n = len(arr)
        smhet__jyxyr = init_nested_counts(jmwfj__pyxv)
        npyyk__wpz = init_nested_counts(dblq__zqias)
        for i in range(n):
            tvy__hntxc = index_arr[i]
            if isna(arr, i):
                smhet__jyxyr = (smhet__jyxyr[0] + 1,) + smhet__jyxyr[1:]
                npyyk__wpz = add_nested_counts(npyyk__wpz, tvy__hntxc)
                continue
            eqzad__ntms = arr[i]
            if len(eqzad__ntms) == 0:
                smhet__jyxyr = (smhet__jyxyr[0] + 1,) + smhet__jyxyr[1:]
                npyyk__wpz = add_nested_counts(npyyk__wpz, tvy__hntxc)
                continue
            smhet__jyxyr = add_nested_counts(smhet__jyxyr, eqzad__ntms)
            for evk__nyzze in range(len(eqzad__ntms)):
                npyyk__wpz = add_nested_counts(npyyk__wpz, tvy__hntxc)
        mhynn__eldsl = bodo.utils.utils.alloc_type(smhet__jyxyr[0],
            jmwfj__pyxv, smhet__jyxyr[1:])
        nss__oqc = bodo.utils.utils.alloc_type(smhet__jyxyr[0], sbv__aphsa,
            npyyk__wpz)
        eqlq__apfcm = 0
        for i in range(n):
            if isna(arr, i):
                setna(mhynn__eldsl, eqlq__apfcm)
                nss__oqc[eqlq__apfcm] = index_arr[i]
                eqlq__apfcm += 1
                continue
            eqzad__ntms = arr[i]
            yfagy__pdrn = len(eqzad__ntms)
            if yfagy__pdrn == 0:
                setna(mhynn__eldsl, eqlq__apfcm)
                nss__oqc[eqlq__apfcm] = index_arr[i]
                eqlq__apfcm += 1
                continue
            mhynn__eldsl[eqlq__apfcm:eqlq__apfcm + yfagy__pdrn] = eqzad__ntms
            nss__oqc[eqlq__apfcm:eqlq__apfcm + yfagy__pdrn] = index_arr[i]
            eqlq__apfcm += yfagy__pdrn
        return mhynn__eldsl, nss__oqc
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    jmwfj__pyxv = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        smhet__jyxyr = init_nested_counts(jmwfj__pyxv)
        for i in range(n):
            if isna(arr, i):
                smhet__jyxyr = (smhet__jyxyr[0] + 1,) + smhet__jyxyr[1:]
                qyjl__gvq = 1
            else:
                eqzad__ntms = arr[i]
                baqda__rmlqh = len(eqzad__ntms)
                if baqda__rmlqh == 0:
                    smhet__jyxyr = (smhet__jyxyr[0] + 1,) + smhet__jyxyr[1:]
                    qyjl__gvq = 1
                    continue
                else:
                    smhet__jyxyr = add_nested_counts(smhet__jyxyr, eqzad__ntms)
                    qyjl__gvq = baqda__rmlqh
            if counts[i] != qyjl__gvq:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        mhynn__eldsl = bodo.utils.utils.alloc_type(smhet__jyxyr[0],
            jmwfj__pyxv, smhet__jyxyr[1:])
        eqlq__apfcm = 0
        for i in range(n):
            if isna(arr, i):
                setna(mhynn__eldsl, eqlq__apfcm)
                eqlq__apfcm += 1
                continue
            eqzad__ntms = arr[i]
            yfagy__pdrn = len(eqzad__ntms)
            if yfagy__pdrn == 0:
                setna(mhynn__eldsl, eqlq__apfcm)
                eqlq__apfcm += 1
                continue
            mhynn__eldsl[eqlq__apfcm:eqlq__apfcm + yfagy__pdrn] = eqzad__ntms
            eqlq__apfcm += yfagy__pdrn
        return mhynn__eldsl
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(fpz__mwuul) for fpz__mwuul in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        cftky__hpt = 'np.empty(n, np.int64)'
        mah__inif = 'out_arr[i] = 1'
        jnzdz__xyx = 'max(len(arr[i]), 1)'
    else:
        cftky__hpt = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        mah__inif = 'bodo.libs.array_kernels.setna(out_arr, i)'
        jnzdz__xyx = 'len(arr[i])'
    xcu__dgn = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {cftky__hpt}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {mah__inif}
        else:
            out_arr[i] = {jnzdz__xyx}
    return out_arr
    """
    rdjbn__wyuc = {}
    exec(xcu__dgn, {'bodo': bodo, 'numba': numba, 'np': np}, rdjbn__wyuc)
    impl = rdjbn__wyuc['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    sbv__aphsa = index_arr
    dblq__zqias = sbv__aphsa.dtype

    def impl(arr, pat, n, index_arr):
        tnjq__eov = pat is not None and len(pat) > 1
        if tnjq__eov:
            gkfen__lfrvh = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        evh__ogryw = len(arr)
        npg__iflc = 0
        vlo__hwjv = 0
        npyyk__wpz = init_nested_counts(dblq__zqias)
        for i in range(evh__ogryw):
            tvy__hntxc = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                npg__iflc += 1
                npyyk__wpz = add_nested_counts(npyyk__wpz, tvy__hntxc)
                continue
            if tnjq__eov:
                hwls__blu = gkfen__lfrvh.split(arr[i], maxsplit=n)
            else:
                hwls__blu = arr[i].split(pat, n)
            npg__iflc += len(hwls__blu)
            for s in hwls__blu:
                npyyk__wpz = add_nested_counts(npyyk__wpz, tvy__hntxc)
                vlo__hwjv += bodo.libs.str_arr_ext.get_utf8_size(s)
        mhynn__eldsl = bodo.libs.str_arr_ext.pre_alloc_string_array(npg__iflc,
            vlo__hwjv)
        nss__oqc = bodo.utils.utils.alloc_type(npg__iflc, sbv__aphsa,
            npyyk__wpz)
        iuw__zrjqq = 0
        for igock__snmv in range(evh__ogryw):
            if isna(arr, igock__snmv):
                mhynn__eldsl[iuw__zrjqq] = ''
                bodo.libs.array_kernels.setna(mhynn__eldsl, iuw__zrjqq)
                nss__oqc[iuw__zrjqq] = index_arr[igock__snmv]
                iuw__zrjqq += 1
                continue
            if tnjq__eov:
                hwls__blu = gkfen__lfrvh.split(arr[igock__snmv], maxsplit=n)
            else:
                hwls__blu = arr[igock__snmv].split(pat, n)
            clj__ywm = len(hwls__blu)
            mhynn__eldsl[iuw__zrjqq:iuw__zrjqq + clj__ywm] = hwls__blu
            nss__oqc[iuw__zrjqq:iuw__zrjqq + clj__ywm] = index_arr[igock__snmv]
            iuw__zrjqq += clj__ywm
        return mhynn__eldsl, nss__oqc
    return impl


def gen_na_array(n, arr):
    return np.full(n, np.nan)


@overload(gen_na_array, no_unliteral=True)
def overload_gen_na_array(n, arr):
    if isinstance(arr, types.TypeRef):
        arr = arr.instance_type
    dtype = arr.dtype
    if isinstance(dtype, (types.Integer, types.Float)):
        dtype = dtype if isinstance(dtype, types.Float) else types.float64

        def impl_float(n, arr):
            numba.parfors.parfor.init_prange()
            mhynn__eldsl = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                mhynn__eldsl[i] = np.nan
            return mhynn__eldsl
        return impl_float
    glrtg__oukz = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        mhynn__eldsl = bodo.utils.utils.alloc_type(n, glrtg__oukz, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(mhynn__eldsl, i)
        return mhynn__eldsl
    return impl


def gen_na_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_gen_na_array = (
    gen_na_array_equiv)


def resize_and_copy(A, new_len):
    return A


@overload(resize_and_copy, no_unliteral=True)
def overload_resize_and_copy(A, old_size, new_len):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.resize_and_copy()')
    jzqp__hiha = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            mhynn__eldsl = bodo.utils.utils.alloc_type(new_len, jzqp__hiha)
            bodo.libs.str_arr_ext.str_copy_ptr(mhynn__eldsl.ctypes, 0, A.
                ctypes, old_size)
            return mhynn__eldsl
        return impl_char

    def impl(A, old_size, new_len):
        mhynn__eldsl = bodo.utils.utils.alloc_type(new_len, jzqp__hiha, (-1,))
        mhynn__eldsl[:old_size] = A[:old_size]
        return mhynn__eldsl
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    pbpms__xyti = math.ceil((stop - start) / step)
    return int(max(pbpms__xyti, 0))


def calc_nitems_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    if guard(find_const, self.func_ir, args[0]) == 0 and guard(find_const,
        self.func_ir, args[2]) == 1:
        return ArrayAnalysis.AnalyzeResult(shape=args[1], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_calc_nitems = (
    calc_nitems_equiv)


def arange_parallel_impl(return_type, *args):
    dtype = as_dtype(return_type.dtype)

    def arange_1(stop):
        return np.arange(0, stop, 1, dtype)

    def arange_2(start, stop):
        return np.arange(start, stop, 1, dtype)

    def arange_3(start, stop, step):
        return np.arange(start, stop, step, dtype)
    if any(isinstance(gety__fqinm, types.Complex) for gety__fqinm in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            gyj__vwevo = (stop - start) / step
            pbpms__xyti = math.ceil(gyj__vwevo.real)
            vtn__ovq = math.ceil(gyj__vwevo.imag)
            yqib__nwjr = int(max(min(vtn__ovq, pbpms__xyti), 0))
            arr = np.empty(yqib__nwjr, dtype)
            for i in numba.parfors.parfor.internal_prange(yqib__nwjr):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            yqib__nwjr = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(yqib__nwjr, dtype)
            for i in numba.parfors.parfor.internal_prange(yqib__nwjr):
                arr[i] = start + i * step
            return arr
    if len(args) == 1:
        return arange_1
    elif len(args) == 2:
        return arange_2
    elif len(args) == 3:
        return arange_3
    elif len(args) == 4:
        return arange_4
    else:
        raise BodoError('parallel arange with types {}'.format(args))


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.arange_parallel_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c72b0390b4f3e52dcc5426bd42c6b55ff96bae5a425381900985d36e7527a4bd':
        warnings.warn('numba.parfors.parfor.arange_parallel_impl has changed')
numba.parfors.parfor.swap_functions_map['arange', 'numpy'
    ] = arange_parallel_impl


def sort(arr, ascending, inplace):
    return np.sort(arr)


@overload(sort, no_unliteral=True)
def overload_sort(arr, ascending, inplace):

    def impl(arr, ascending, inplace):
        n = len(arr)
        data = np.arange(n),
        zay__qvqyy = arr,
        if not inplace:
            zay__qvqyy = arr.copy(),
        mxxwq__qiz = bodo.libs.str_arr_ext.to_list_if_immutable_arr(zay__qvqyy)
        kwg__dlkas = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(mxxwq__qiz, 0, n, kwg__dlkas)
        if not ascending:
            bodo.libs.timsort.reverseRange(mxxwq__qiz, 0, n, kwg__dlkas)
        bodo.libs.str_arr_ext.cp_str_list_to_array(zay__qvqyy, mxxwq__qiz)
        return zay__qvqyy[0]
    return impl


def overload_array_max(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).max()
        return impl


overload(np.max, inline='always', no_unliteral=True)(overload_array_max)
overload(max, inline='always', no_unliteral=True)(overload_array_max)


def overload_array_min(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).min()
        return impl


overload(np.min, inline='always', no_unliteral=True)(overload_array_min)
overload(min, inline='always', no_unliteral=True)(overload_array_min)


def overload_array_sum(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).sum()
    return impl


overload(np.sum, inline='always', no_unliteral=True)(overload_array_sum)
overload(sum, inline='always', no_unliteral=True)(overload_array_sum)


@overload(np.prod, inline='always', no_unliteral=True)
def overload_array_prod(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).prod()
    return impl


def nonzero(arr):
    return arr,


@overload(nonzero, no_unliteral=True)
def nonzero_overload(A, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.nonzero()')
    if not bodo.utils.utils.is_array_typ(A, False):
        return

    def impl(A, parallel=False):
        n = len(A)
        if parallel:
            offset = bodo.libs.distributed_api.dist_exscan(n, Reduce_Type.
                Sum.value)
        else:
            offset = 0
        fgkrz__oaflz = []
        for i in range(n):
            if A[i]:
                fgkrz__oaflz.append(i + offset)
        return np.array(fgkrz__oaflz, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    jzqp__hiha = element_type(A)
    if jzqp__hiha == types.unicode_type:
        null_value = '""'
    elif jzqp__hiha == types.bool_:
        null_value = 'False'
    elif jzqp__hiha == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif jzqp__hiha == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    iuw__zrjqq = 'i'
    lhgkv__srm = False
    evt__jejak = get_overload_const_str(method)
    if evt__jejak in ('ffill', 'pad'):
        kwx__jqm = 'n'
        send_right = True
    elif evt__jejak in ('backfill', 'bfill'):
        kwx__jqm = 'n-1, -1, -1'
        send_right = False
        if jzqp__hiha == types.unicode_type:
            iuw__zrjqq = '(n - 1) - i'
            lhgkv__srm = True
    xcu__dgn = 'def impl(A, method, parallel=False):\n'
    xcu__dgn += '  A = decode_if_dict_array(A)\n'
    xcu__dgn += '  has_last_value = False\n'
    xcu__dgn += f'  last_value = {null_value}\n'
    xcu__dgn += '  if parallel:\n'
    xcu__dgn += '    rank = bodo.libs.distributed_api.get_rank()\n'
    xcu__dgn += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    xcu__dgn += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    xcu__dgn += '  n = len(A)\n'
    xcu__dgn += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    xcu__dgn += f'  for i in range({kwx__jqm}):\n'
    xcu__dgn += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    xcu__dgn += f'      bodo.libs.array_kernels.setna(out_arr, {iuw__zrjqq})\n'
    xcu__dgn += '      continue\n'
    xcu__dgn += '    s = A[i]\n'
    xcu__dgn += '    if bodo.libs.array_kernels.isna(A, i):\n'
    xcu__dgn += '      s = last_value\n'
    xcu__dgn += f'    out_arr[{iuw__zrjqq}] = s\n'
    xcu__dgn += '    last_value = s\n'
    xcu__dgn += '    has_last_value = True\n'
    if lhgkv__srm:
        xcu__dgn += '  return out_arr[::-1]\n'
    else:
        xcu__dgn += '  return out_arr\n'
    uye__iurkm = {}
    exec(xcu__dgn, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, uye__iurkm)
    impl = uye__iurkm['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        ovgrl__cqqm = 0
        npmdj__cbyog = n_pes - 1
        drtu__dbfu = np.int32(rank + 1)
        lwb__hfxlg = np.int32(rank - 1)
        qyc__ifo = len(in_arr) - 1
        zsf__bcbak = -1
        okm__jrlao = -1
    else:
        ovgrl__cqqm = n_pes - 1
        npmdj__cbyog = 0
        drtu__dbfu = np.int32(rank - 1)
        lwb__hfxlg = np.int32(rank + 1)
        qyc__ifo = 0
        zsf__bcbak = len(in_arr)
        okm__jrlao = 1
    tmk__qtxf = np.int32(bodo.hiframes.rolling.comm_border_tag)
    pmy__wcfzy = np.empty(1, dtype=np.bool_)
    yhnsi__iga = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    kxoa__vtrj = np.empty(1, dtype=np.bool_)
    nct__tzk = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    dsi__tht = False
    ukhz__syoax = null_value
    for i in range(qyc__ifo, zsf__bcbak, okm__jrlao):
        if not isna(in_arr, i):
            dsi__tht = True
            ukhz__syoax = in_arr[i]
            break
    if rank != ovgrl__cqqm:
        lnui__orva = bodo.libs.distributed_api.irecv(pmy__wcfzy, 1,
            lwb__hfxlg, tmk__qtxf, True)
        bodo.libs.distributed_api.wait(lnui__orva, True)
        kok__cerh = bodo.libs.distributed_api.irecv(yhnsi__iga, 1,
            lwb__hfxlg, tmk__qtxf, True)
        bodo.libs.distributed_api.wait(kok__cerh, True)
        shis__pxsdb = pmy__wcfzy[0]
        pkhsd__vzxte = yhnsi__iga[0]
    else:
        shis__pxsdb = False
        pkhsd__vzxte = null_value
    if dsi__tht:
        kxoa__vtrj[0] = dsi__tht
        nct__tzk[0] = ukhz__syoax
    else:
        kxoa__vtrj[0] = shis__pxsdb
        nct__tzk[0] = pkhsd__vzxte
    if rank != npmdj__cbyog:
        adcqk__rrmb = bodo.libs.distributed_api.isend(kxoa__vtrj, 1,
            drtu__dbfu, tmk__qtxf, True)
        vvgz__xql = bodo.libs.distributed_api.isend(nct__tzk, 1, drtu__dbfu,
            tmk__qtxf, True)
    return shis__pxsdb, pkhsd__vzxte


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    dan__hvand = {'axis': axis, 'kind': kind, 'order': order}
    mejtr__gbt = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', dan__hvand, mejtr__gbt, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    jzqp__hiha = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            evh__ogryw = len(A)
            mhynn__eldsl = bodo.utils.utils.alloc_type(evh__ogryw * repeats,
                jzqp__hiha, (-1,))
            for i in range(evh__ogryw):
                iuw__zrjqq = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for igock__snmv in range(repeats):
                        bodo.libs.array_kernels.setna(mhynn__eldsl, 
                            iuw__zrjqq + igock__snmv)
                else:
                    mhynn__eldsl[iuw__zrjqq:iuw__zrjqq + repeats] = A[i]
            return mhynn__eldsl
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        evh__ogryw = len(A)
        mhynn__eldsl = bodo.utils.utils.alloc_type(repeats.sum(),
            jzqp__hiha, (-1,))
        iuw__zrjqq = 0
        for i in range(evh__ogryw):
            xsr__thko = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for igock__snmv in range(xsr__thko):
                    bodo.libs.array_kernels.setna(mhynn__eldsl, iuw__zrjqq +
                        igock__snmv)
            else:
                mhynn__eldsl[iuw__zrjqq:iuw__zrjqq + xsr__thko] = A[i]
            iuw__zrjqq += xsr__thko
        return mhynn__eldsl
    return impl_arr


@overload(np.repeat, inline='always', no_unliteral=True)
def np_repeat(A, repeats):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    if not isinstance(repeats, types.Integer):
        raise BodoError(
            'Only integer type supported for repeats in np.repeat()')

    def impl(A, repeats):
        return bodo.libs.array_kernels.repeat_kernel(A, repeats)
    return impl


@numba.generated_jit
def repeat_like(A, dist_like_arr):
    if not bodo.utils.utils.is_array_typ(A, False
        ) or not bodo.utils.utils.is_array_typ(dist_like_arr, False):
        raise BodoError('Both A and dist_like_arr must be array-like.')

    def impl(A, dist_like_arr):
        return bodo.libs.array_kernels.repeat_kernel(A, len(dist_like_arr))
    return impl


@overload(np.unique, inline='always', no_unliteral=True)
def np_unique(A):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return

    def impl(A):
        jxk__tda = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(jxk__tda, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        zjbfl__rlgzc = bodo.libs.array_kernels.concat([A1, A2])
        mwpqm__llm = bodo.libs.array_kernels.unique(zjbfl__rlgzc)
        return pd.Series(mwpqm__llm).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    dan__hvand = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    mejtr__gbt = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', dan__hvand, mejtr__gbt, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        mbfij__pbe = bodo.libs.array_kernels.unique(A1)
        bclv__gitqu = bodo.libs.array_kernels.unique(A2)
        zjbfl__rlgzc = bodo.libs.array_kernels.concat([mbfij__pbe, bclv__gitqu]
            )
        fomlw__nbmap = pd.Series(zjbfl__rlgzc).sort_values().values
        return slice_array_intersect1d(fomlw__nbmap)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    qja__pgs = arr[1:] == arr[:-1]
    return arr[:-1][qja__pgs]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    dan__hvand = {'assume_unique': assume_unique}
    mejtr__gbt = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', dan__hvand, mejtr__gbt, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        mbfij__pbe = bodo.libs.array_kernels.unique(A1)
        bclv__gitqu = bodo.libs.array_kernels.unique(A2)
        qja__pgs = calculate_mask_setdiff1d(mbfij__pbe, bclv__gitqu)
        return pd.Series(mbfij__pbe[qja__pgs]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    qja__pgs = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        qja__pgs &= A1 != A2[i]
    return qja__pgs


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    dan__hvand = {'retstep': retstep, 'axis': axis}
    mejtr__gbt = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', dan__hvand, mejtr__gbt, 'numpy')
    ozlqb__cmigs = False
    if is_overload_none(dtype):
        jzqp__hiha = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            ozlqb__cmigs = True
        jzqp__hiha = numba.np.numpy_support.as_dtype(dtype).type
    if ozlqb__cmigs:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            ith__lyd = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            mhynn__eldsl = np.empty(num, jzqp__hiha)
            for i in numba.parfors.parfor.internal_prange(num):
                mhynn__eldsl[i] = jzqp__hiha(np.floor(start + i * ith__lyd))
            return mhynn__eldsl
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            ith__lyd = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            mhynn__eldsl = np.empty(num, jzqp__hiha)
            for i in numba.parfors.parfor.internal_prange(num):
                mhynn__eldsl[i] = jzqp__hiha(start + i * ith__lyd)
            return mhynn__eldsl
        return impl


def np_linspace_get_stepsize(start, stop, num, endpoint):
    return 0


@overload(np_linspace_get_stepsize, no_unliteral=True)
def overload_np_linspace_get_stepsize(start, stop, num, endpoint):

    def impl(start, stop, num, endpoint):
        if num < 0:
            raise ValueError('np.linspace() Num must be >= 0')
        if endpoint:
            num -= 1
        if num > 1:
            return (stop - start) / num
        return 0
    return impl


@overload(operator.contains, no_unliteral=True)
def arr_contains(A, val):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'np.contains()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.dtype == types.
        unliteral(val)):
        return

    def impl(A, val):
        numba.parfors.parfor.init_prange()
        zlj__dnwwm = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                zlj__dnwwm += A[i] == val
        return zlj__dnwwm > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    dan__hvand = {'axis': axis, 'out': out, 'keepdims': keepdims}
    mejtr__gbt = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', dan__hvand, mejtr__gbt, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        zlj__dnwwm = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                zlj__dnwwm += int(bool(A[i]))
        return zlj__dnwwm > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    dan__hvand = {'axis': axis, 'out': out, 'keepdims': keepdims}
    mejtr__gbt = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', dan__hvand, mejtr__gbt, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        zlj__dnwwm = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                zlj__dnwwm += int(bool(A[i]))
        return zlj__dnwwm == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    dan__hvand = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    mejtr__gbt = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', dan__hvand, mejtr__gbt, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        mwq__rml = np.promote_types(numba.np.numpy_support.as_dtype(A.dtype
            ), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            mhynn__eldsl = np.empty(n, mwq__rml)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(mhynn__eldsl, i)
                    continue
                mhynn__eldsl[i] = np_cbrt_scalar(A[i], mwq__rml)
            return mhynn__eldsl
        return impl_arr
    mwq__rml = np.promote_types(numba.np.numpy_support.as_dtype(A), numba.
        np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, mwq__rml)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    dwahu__eeq = x < 0
    if dwahu__eeq:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if dwahu__eeq:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    kqcbo__ozp = isinstance(tup, (types.BaseTuple, types.List))
    jbwt__rxr = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for slgf__xzp in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(slgf__xzp
                , 'numpy.hstack()')
            kqcbo__ozp = kqcbo__ozp and bodo.utils.utils.is_array_typ(slgf__xzp
                , False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        kqcbo__ozp = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif jbwt__rxr:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        axkwf__ylonv = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for slgf__xzp in axkwf__ylonv.types:
            jbwt__rxr = jbwt__rxr and bodo.utils.utils.is_array_typ(slgf__xzp,
                False)
    if not (kqcbo__ozp or jbwt__rxr):
        return
    if jbwt__rxr:

        def impl_series(tup):
            arr_tup = bodo.hiframes.pd_series_ext.get_series_data(tup)
            return bodo.libs.array_kernels.concat(arr_tup)
        return impl_series

    def impl(tup):
        return bodo.libs.array_kernels.concat(tup)
    return impl


@overload(np.random.multivariate_normal, inline='always', no_unliteral=True)
def np_random_multivariate_normal(mean, cov, size=None, check_valid='warn',
    tol=1e-08):
    dan__hvand = {'check_valid': check_valid, 'tol': tol}
    mejtr__gbt = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', dan__hvand,
        mejtr__gbt, 'numpy')
    if not isinstance(size, types.Integer):
        raise BodoError(
            'np.random.multivariate_normal() size argument is required and must be an integer'
            )
    if not (bodo.utils.utils.is_array_typ(mean, False) and mean.ndim == 1):
        raise BodoError(
            'np.random.multivariate_normal() mean must be a 1 dimensional numpy array'
            )
    if not (bodo.utils.utils.is_array_typ(cov, False) and cov.ndim == 2):
        raise BodoError(
            'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
            )

    def impl(mean, cov, size=None, check_valid='warn', tol=1e-08):
        _validate_multivar_norm(cov)
        hzsur__kvqaw = mean.shape[0]
        sej__moezi = size, hzsur__kvqaw
        pxso__ukc = np.random.standard_normal(sej__moezi)
        cov = cov.astype(np.float64)
        hkhpw__sews, s, azd__hot = np.linalg.svd(cov)
        res = np.dot(pxso__ukc, np.sqrt(s).reshape(hzsur__kvqaw, 1) * azd__hot)
        fyf__gflkv = res + mean
        return fyf__gflkv
    return impl


def _validate_multivar_norm(cov):
    return


@overload(_validate_multivar_norm, no_unliteral=True)
def _overload_validate_multivar_norm(cov):

    def impl(cov):
        if cov.shape[0] != cov.shape[1]:
            raise ValueError(
                'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
                )
    return impl


def _nan_argmin(arr):
    return


@overload(_nan_argmin, no_unliteral=True)
def _overload_nan_argmin(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            numba.parfors.parfor.init_prange()
            nka__qog = bodo.hiframes.series_kernels._get_type_max_value(arr)
            bnh__yrum = typing.builtins.IndexValue(-1, nka__qog)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xar__jvur = typing.builtins.IndexValue(i, arr[i])
                bnh__yrum = min(bnh__yrum, xar__jvur)
            return bnh__yrum.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        lnjl__cnr = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            win__wvndd = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            nka__qog = lnjl__cnr(len(arr.dtype.categories) + 1)
            bnh__yrum = typing.builtins.IndexValue(-1, nka__qog)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xar__jvur = typing.builtins.IndexValue(i, win__wvndd[i])
                bnh__yrum = min(bnh__yrum, xar__jvur)
            return bnh__yrum.index
        return impl_cat_arr
    return lambda arr: arr.argmin()


def _nan_argmax(arr):
    return


@overload(_nan_argmax, no_unliteral=True)
def _overload_nan_argmax(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            n = len(arr)
            numba.parfors.parfor.init_prange()
            nka__qog = bodo.hiframes.series_kernels._get_type_min_value(arr)
            bnh__yrum = typing.builtins.IndexValue(-1, nka__qog)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xar__jvur = typing.builtins.IndexValue(i, arr[i])
                bnh__yrum = max(bnh__yrum, xar__jvur)
            return bnh__yrum.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        lnjl__cnr = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            win__wvndd = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            nka__qog = lnjl__cnr(-1)
            bnh__yrum = typing.builtins.IndexValue(-1, nka__qog)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                xar__jvur = typing.builtins.IndexValue(i, win__wvndd[i])
                bnh__yrum = max(bnh__yrum, xar__jvur)
            return bnh__yrum.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
