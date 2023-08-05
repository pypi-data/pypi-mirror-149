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
        tcpwm__yaaf = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = tcpwm__yaaf
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        tcpwm__yaaf = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = tcpwm__yaaf
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
            lqo__jfomj = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            lqo__jfomj[ind + 1] = lqo__jfomj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            lqo__jfomj = bodo.libs.array_item_arr_ext.get_offsets(arr)
            lqo__jfomj[ind + 1] = lqo__jfomj[ind]
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
    gonbq__vpbf = arr_tup.count
    jrqc__cvfzx = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(gonbq__vpbf):
        jrqc__cvfzx += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    jrqc__cvfzx += '  return\n'
    zht__uxyib = {}
    exec(jrqc__cvfzx, {'setna': setna}, zht__uxyib)
    impl = zht__uxyib['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        yhxk__fkz = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(yhxk__fkz.start, yhxk__fkz.stop, yhxk__fkz.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        meowt__oic = 'n'
        hrzou__ggdw = 'n_pes'
        xugs__zygth = 'min_op'
    else:
        meowt__oic = 'n-1, -1, -1'
        hrzou__ggdw = '-1'
        xugs__zygth = 'max_op'
    jrqc__cvfzx = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {hrzou__ggdw}
    for i in range({meowt__oic}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {xugs__zygth}))
        if possible_valid_rank != {hrzou__ggdw}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    zht__uxyib = {}
    exec(jrqc__cvfzx, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, zht__uxyib)
    impl = zht__uxyib['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    rixkx__jbjem = array_to_info(arr)
    _median_series_computation(res, rixkx__jbjem, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(rixkx__jbjem)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    rixkx__jbjem = array_to_info(arr)
    _autocorr_series_computation(res, rixkx__jbjem, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(rixkx__jbjem)


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
    rixkx__jbjem = array_to_info(arr)
    _compute_series_monotonicity(res, rixkx__jbjem, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(rixkx__jbjem)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    lebaa__avqth = res[0] > 0.5
    return lebaa__avqth


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        myaqg__nksgi = '-'
        nuld__wmbm = 'index_arr[0] > threshhold_date'
        meowt__oic = '1, n+1'
        unim__fedb = 'index_arr[-i] <= threshhold_date'
        fmqm__kual = 'i - 1'
    else:
        myaqg__nksgi = '+'
        nuld__wmbm = 'index_arr[-1] < threshhold_date'
        meowt__oic = 'n'
        unim__fedb = 'index_arr[i] >= threshhold_date'
        fmqm__kual = 'i'
    jrqc__cvfzx = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        jrqc__cvfzx += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        jrqc__cvfzx += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            jrqc__cvfzx += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            jrqc__cvfzx += """      threshhold_date = initial_date - date_offset.base + date_offset
"""
            jrqc__cvfzx += '    else:\n'
            jrqc__cvfzx += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            jrqc__cvfzx += (
                f'    threshhold_date = initial_date {myaqg__nksgi} date_offset\n'
                )
    else:
        jrqc__cvfzx += (
            f'  threshhold_date = initial_date {myaqg__nksgi} offset\n')
    jrqc__cvfzx += '  local_valid = 0\n'
    jrqc__cvfzx += f'  n = len(index_arr)\n'
    jrqc__cvfzx += f'  if n:\n'
    jrqc__cvfzx += f'    if {nuld__wmbm}:\n'
    jrqc__cvfzx += '      loc_valid = n\n'
    jrqc__cvfzx += '    else:\n'
    jrqc__cvfzx += f'      for i in range({meowt__oic}):\n'
    jrqc__cvfzx += f'        if {unim__fedb}:\n'
    jrqc__cvfzx += f'          loc_valid = {fmqm__kual}\n'
    jrqc__cvfzx += '          break\n'
    jrqc__cvfzx += '  if is_parallel:\n'
    jrqc__cvfzx += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    jrqc__cvfzx += '    return total_valid\n'
    jrqc__cvfzx += '  else:\n'
    jrqc__cvfzx += '    return loc_valid\n'
    zht__uxyib = {}
    exec(jrqc__cvfzx, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, zht__uxyib)
    return zht__uxyib['impl']


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
    plm__cqih = numba_to_c_type(sig.args[0].dtype)
    yea__zrtlm = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), plm__cqih))
    bgfc__jtq = args[0]
    yptp__oxub = sig.args[0]
    if isinstance(yptp__oxub, (IntegerArrayType, BooleanArrayType)):
        bgfc__jtq = cgutils.create_struct_proxy(yptp__oxub)(context,
            builder, bgfc__jtq).data
        yptp__oxub = types.Array(yptp__oxub.dtype, 1, 'C')
    assert yptp__oxub.ndim == 1
    arr = make_array(yptp__oxub)(context, builder, bgfc__jtq)
    duok__lthm = builder.extract_value(arr.shape, 0)
    fjovs__qnv = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        duok__lthm, args[1], builder.load(yea__zrtlm)]
    dtgqq__cffy = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    ojwbw__wpz = lir.FunctionType(lir.DoubleType(), dtgqq__cffy)
    rigz__eppxq = cgutils.get_or_insert_function(builder.module, ojwbw__wpz,
        name='quantile_sequential')
    clvtt__qllw = builder.call(rigz__eppxq, fjovs__qnv)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return clvtt__qllw


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    plm__cqih = numba_to_c_type(sig.args[0].dtype)
    yea__zrtlm = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), plm__cqih))
    bgfc__jtq = args[0]
    yptp__oxub = sig.args[0]
    if isinstance(yptp__oxub, (IntegerArrayType, BooleanArrayType)):
        bgfc__jtq = cgutils.create_struct_proxy(yptp__oxub)(context,
            builder, bgfc__jtq).data
        yptp__oxub = types.Array(yptp__oxub.dtype, 1, 'C')
    assert yptp__oxub.ndim == 1
    arr = make_array(yptp__oxub)(context, builder, bgfc__jtq)
    duok__lthm = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        olwb__pap = args[2]
    else:
        olwb__pap = duok__lthm
    fjovs__qnv = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        duok__lthm, olwb__pap, args[1], builder.load(yea__zrtlm)]
    dtgqq__cffy = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        IntType(64), lir.DoubleType(), lir.IntType(32)]
    ojwbw__wpz = lir.FunctionType(lir.DoubleType(), dtgqq__cffy)
    rigz__eppxq = cgutils.get_or_insert_function(builder.module, ojwbw__wpz,
        name='quantile_parallel')
    clvtt__qllw = builder.call(rigz__eppxq, fjovs__qnv)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return clvtt__qllw


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    udlmh__cwqk = start
    cphdo__fbia = 2 * start + 1
    pvmpd__yzcug = 2 * start + 2
    if cphdo__fbia < n and not cmp_f(arr[cphdo__fbia], arr[udlmh__cwqk]):
        udlmh__cwqk = cphdo__fbia
    if pvmpd__yzcug < n and not cmp_f(arr[pvmpd__yzcug], arr[udlmh__cwqk]):
        udlmh__cwqk = pvmpd__yzcug
    if udlmh__cwqk != start:
        arr[start], arr[udlmh__cwqk] = arr[udlmh__cwqk], arr[start]
        ind_arr[start], ind_arr[udlmh__cwqk] = ind_arr[udlmh__cwqk], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, udlmh__cwqk, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        jayi__pnyn = np.empty(k, A.dtype)
        wvno__ecjkj = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                jayi__pnyn[ind] = A[i]
                wvno__ecjkj[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            jayi__pnyn = jayi__pnyn[:ind]
            wvno__ecjkj = wvno__ecjkj[:ind]
        return jayi__pnyn, wvno__ecjkj, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        niyt__wjliz = np.sort(A)
        rzlnc__vau = index_arr[np.argsort(A)]
        lkm__ujwq = pd.Series(niyt__wjliz).notna().values
        niyt__wjliz = niyt__wjliz[lkm__ujwq]
        rzlnc__vau = rzlnc__vau[lkm__ujwq]
        if is_largest:
            niyt__wjliz = niyt__wjliz[::-1]
            rzlnc__vau = rzlnc__vau[::-1]
        return np.ascontiguousarray(niyt__wjliz), np.ascontiguousarray(
            rzlnc__vau)
    jayi__pnyn, wvno__ecjkj, start = select_k_nonan(A, index_arr, m, k)
    wvno__ecjkj = wvno__ecjkj[jayi__pnyn.argsort()]
    jayi__pnyn.sort()
    if not is_largest:
        jayi__pnyn = np.ascontiguousarray(jayi__pnyn[::-1])
        wvno__ecjkj = np.ascontiguousarray(wvno__ecjkj[::-1])
    for i in range(start, m):
        if cmp_f(A[i], jayi__pnyn[0]):
            jayi__pnyn[0] = A[i]
            wvno__ecjkj[0] = index_arr[i]
            min_heapify(jayi__pnyn, wvno__ecjkj, k, 0, cmp_f)
    wvno__ecjkj = wvno__ecjkj[jayi__pnyn.argsort()]
    jayi__pnyn.sort()
    if is_largest:
        jayi__pnyn = jayi__pnyn[::-1]
        wvno__ecjkj = wvno__ecjkj[::-1]
    return np.ascontiguousarray(jayi__pnyn), np.ascontiguousarray(wvno__ecjkj)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    oeqh__dpr = bodo.libs.distributed_api.get_rank()
    nbtq__gjmw, mlwx__raxo = nlargest(A, I, k, is_largest, cmp_f)
    bswrj__ars = bodo.libs.distributed_api.gatherv(nbtq__gjmw)
    nfjrf__vimur = bodo.libs.distributed_api.gatherv(mlwx__raxo)
    if oeqh__dpr == MPI_ROOT:
        res, dxb__yzoo = nlargest(bswrj__ars, nfjrf__vimur, k, is_largest,
            cmp_f)
    else:
        res = np.empty(k, A.dtype)
        dxb__yzoo = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(dxb__yzoo)
    return res, dxb__yzoo


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    iigdx__bot, ivk__mya = mat.shape
    qai__buvxv = np.empty((ivk__mya, ivk__mya), dtype=np.float64)
    for wuy__dgxn in range(ivk__mya):
        for bwzy__edl in range(wuy__dgxn + 1):
            jhulp__npxps = 0
            rsnwd__cct = grj__kvi = dwixw__uotpi = dwg__ipu = 0.0
            for i in range(iigdx__bot):
                if np.isfinite(mat[i, wuy__dgxn]) and np.isfinite(mat[i,
                    bwzy__edl]):
                    uhul__rlnk = mat[i, wuy__dgxn]
                    rees__qseqm = mat[i, bwzy__edl]
                    jhulp__npxps += 1
                    dwixw__uotpi += uhul__rlnk
                    dwg__ipu += rees__qseqm
            if parallel:
                jhulp__npxps = bodo.libs.distributed_api.dist_reduce(
                    jhulp__npxps, sum_op)
                dwixw__uotpi = bodo.libs.distributed_api.dist_reduce(
                    dwixw__uotpi, sum_op)
                dwg__ipu = bodo.libs.distributed_api.dist_reduce(dwg__ipu,
                    sum_op)
            if jhulp__npxps < minpv:
                qai__buvxv[wuy__dgxn, bwzy__edl] = qai__buvxv[bwzy__edl,
                    wuy__dgxn] = np.nan
            else:
                dvp__ohxay = dwixw__uotpi / jhulp__npxps
                hfecc__kwm = dwg__ipu / jhulp__npxps
                dwixw__uotpi = 0.0
                for i in range(iigdx__bot):
                    if np.isfinite(mat[i, wuy__dgxn]) and np.isfinite(mat[i,
                        bwzy__edl]):
                        uhul__rlnk = mat[i, wuy__dgxn] - dvp__ohxay
                        rees__qseqm = mat[i, bwzy__edl] - hfecc__kwm
                        dwixw__uotpi += uhul__rlnk * rees__qseqm
                        rsnwd__cct += uhul__rlnk * uhul__rlnk
                        grj__kvi += rees__qseqm * rees__qseqm
                if parallel:
                    dwixw__uotpi = bodo.libs.distributed_api.dist_reduce(
                        dwixw__uotpi, sum_op)
                    rsnwd__cct = bodo.libs.distributed_api.dist_reduce(
                        rsnwd__cct, sum_op)
                    grj__kvi = bodo.libs.distributed_api.dist_reduce(grj__kvi,
                        sum_op)
                rujm__dsu = jhulp__npxps - 1.0 if cov else sqrt(rsnwd__cct *
                    grj__kvi)
                if rujm__dsu != 0.0:
                    qai__buvxv[wuy__dgxn, bwzy__edl] = qai__buvxv[bwzy__edl,
                        wuy__dgxn] = dwixw__uotpi / rujm__dsu
                else:
                    qai__buvxv[wuy__dgxn, bwzy__edl] = qai__buvxv[bwzy__edl,
                        wuy__dgxn] = np.nan
    return qai__buvxv


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    gfzay__krnel = n != 1
    jrqc__cvfzx = 'def impl(data, parallel=False):\n'
    jrqc__cvfzx += '  if parallel:\n'
    gngo__faqx = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    jrqc__cvfzx += f'    cpp_table = arr_info_list_to_table([{gngo__faqx}])\n'
    jrqc__cvfzx += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    yatg__gznz = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    jrqc__cvfzx += f'    data = ({yatg__gznz},)\n'
    jrqc__cvfzx += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    jrqc__cvfzx += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    jrqc__cvfzx += '    bodo.libs.array.delete_table(cpp_table)\n'
    jrqc__cvfzx += '  n = len(data[0])\n'
    jrqc__cvfzx += '  out = np.empty(n, np.bool_)\n'
    jrqc__cvfzx += '  uniqs = dict()\n'
    if gfzay__krnel:
        jrqc__cvfzx += '  for i in range(n):\n'
        akqhx__itg = ', '.join(f'data[{i}][i]' for i in range(n))
        ulh__xqht = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        jrqc__cvfzx += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({akqhx__itg},), ({ulh__xqht},))
"""
        jrqc__cvfzx += '    if val in uniqs:\n'
        jrqc__cvfzx += '      out[i] = True\n'
        jrqc__cvfzx += '    else:\n'
        jrqc__cvfzx += '      out[i] = False\n'
        jrqc__cvfzx += '      uniqs[val] = 0\n'
    else:
        jrqc__cvfzx += '  data = data[0]\n'
        jrqc__cvfzx += '  hasna = False\n'
        jrqc__cvfzx += '  for i in range(n):\n'
        jrqc__cvfzx += '    if bodo.libs.array_kernels.isna(data, i):\n'
        jrqc__cvfzx += '      out[i] = hasna\n'
        jrqc__cvfzx += '      hasna = True\n'
        jrqc__cvfzx += '    else:\n'
        jrqc__cvfzx += '      val = data[i]\n'
        jrqc__cvfzx += '      if val in uniqs:\n'
        jrqc__cvfzx += '        out[i] = True\n'
        jrqc__cvfzx += '      else:\n'
        jrqc__cvfzx += '        out[i] = False\n'
        jrqc__cvfzx += '        uniqs[val] = 0\n'
    jrqc__cvfzx += '  if parallel:\n'
    jrqc__cvfzx += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    jrqc__cvfzx += '  return out\n'
    zht__uxyib = {}
    exec(jrqc__cvfzx, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        zht__uxyib)
    impl = zht__uxyib['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    gonbq__vpbf = len(data)
    jrqc__cvfzx = (
        'def impl(data, ind_arr, n, frac, replace, parallel=False):\n')
    jrqc__cvfzx += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        gonbq__vpbf)))
    jrqc__cvfzx += '  table_total = arr_info_list_to_table(info_list_total)\n'
    jrqc__cvfzx += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(gonbq__vpbf))
    for yilr__mgl in range(gonbq__vpbf):
        jrqc__cvfzx += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(yilr__mgl, yilr__mgl, yilr__mgl))
    jrqc__cvfzx += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(gonbq__vpbf))
    jrqc__cvfzx += '  delete_table(out_table)\n'
    jrqc__cvfzx += '  delete_table(table_total)\n'
    jrqc__cvfzx += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(gonbq__vpbf)))
    zht__uxyib = {}
    exec(jrqc__cvfzx, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, zht__uxyib)
    impl = zht__uxyib['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    gonbq__vpbf = len(data)
    jrqc__cvfzx = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    jrqc__cvfzx += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        gonbq__vpbf)))
    jrqc__cvfzx += '  table_total = arr_info_list_to_table(info_list_total)\n'
    jrqc__cvfzx += '  keep_i = 0\n'
    jrqc__cvfzx += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for yilr__mgl in range(gonbq__vpbf):
        jrqc__cvfzx += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(yilr__mgl, yilr__mgl, yilr__mgl))
    jrqc__cvfzx += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(gonbq__vpbf))
    jrqc__cvfzx += '  delete_table(out_table)\n'
    jrqc__cvfzx += '  delete_table(table_total)\n'
    jrqc__cvfzx += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(gonbq__vpbf)))
    zht__uxyib = {}
    exec(jrqc__cvfzx, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, zht__uxyib)
    impl = zht__uxyib['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        wgp__apfok = [array_to_info(data_arr)]
        ghgc__syb = arr_info_list_to_table(wgp__apfok)
        fklv__nqyw = 0
        ook__yweiw = drop_duplicates_table(ghgc__syb, parallel, 1,
            fklv__nqyw, False, True)
        rtmm__gqtgo = info_to_array(info_from_table(ook__yweiw, 0), data_arr)
        delete_table(ook__yweiw)
        delete_table(ghgc__syb)
        return rtmm__gqtgo
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    fsb__qxg = len(data.types)
    qbtb__vma = [('out' + str(i)) for i in range(fsb__qxg)]
    adjc__twbjr = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    kun__nukpo = ['isna(data[{}], i)'.format(i) for i in adjc__twbjr]
    hkho__mlurq = 'not ({})'.format(' or '.join(kun__nukpo))
    if not is_overload_none(thresh):
        hkho__mlurq = '(({}) <= ({}) - thresh)'.format(' + '.join(
            kun__nukpo), fsb__qxg - 1)
    elif how == 'all':
        hkho__mlurq = 'not ({})'.format(' and '.join(kun__nukpo))
    jrqc__cvfzx = 'def _dropna_imp(data, how, thresh, subset):\n'
    jrqc__cvfzx += '  old_len = len(data[0])\n'
    jrqc__cvfzx += '  new_len = 0\n'
    jrqc__cvfzx += '  for i in range(old_len):\n'
    jrqc__cvfzx += '    if {}:\n'.format(hkho__mlurq)
    jrqc__cvfzx += '      new_len += 1\n'
    for i, out in enumerate(qbtb__vma):
        if isinstance(data[i], bodo.CategoricalArrayType):
            jrqc__cvfzx += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            jrqc__cvfzx += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    jrqc__cvfzx += '  curr_ind = 0\n'
    jrqc__cvfzx += '  for i in range(old_len):\n'
    jrqc__cvfzx += '    if {}:\n'.format(hkho__mlurq)
    for i in range(fsb__qxg):
        jrqc__cvfzx += '      if isna(data[{}], i):\n'.format(i)
        jrqc__cvfzx += '        setna({}, curr_ind)\n'.format(qbtb__vma[i])
        jrqc__cvfzx += '      else:\n'
        jrqc__cvfzx += '        {}[curr_ind] = data[{}][i]\n'.format(qbtb__vma
            [i], i)
    jrqc__cvfzx += '      curr_ind += 1\n'
    jrqc__cvfzx += '  return {}\n'.format(', '.join(qbtb__vma))
    zht__uxyib = {}
    dfr__nubeh = {'t{}'.format(i): vpcm__mzzc for i, vpcm__mzzc in
        enumerate(data.types)}
    dfr__nubeh.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(jrqc__cvfzx, dfr__nubeh, zht__uxyib)
    pdd__pzbr = zht__uxyib['_dropna_imp']
    return pdd__pzbr


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        yptp__oxub = arr.dtype
        gpan__qujhi = yptp__oxub.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            kufa__tst = init_nested_counts(gpan__qujhi)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                kufa__tst = add_nested_counts(kufa__tst, val[ind])
            rtmm__gqtgo = bodo.utils.utils.alloc_type(n, yptp__oxub, kufa__tst)
            for gyg__knqs in range(n):
                if bodo.libs.array_kernels.isna(arr, gyg__knqs):
                    setna(rtmm__gqtgo, gyg__knqs)
                    continue
                val = arr[gyg__knqs]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(rtmm__gqtgo, gyg__knqs)
                    continue
                rtmm__gqtgo[gyg__knqs] = val[ind]
            return rtmm__gqtgo
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    nrk__uwibf = _to_readonly(arr_types.types[0])
    return all(isinstance(vpcm__mzzc, CategoricalArrayType) and 
        _to_readonly(vpcm__mzzc) == nrk__uwibf for vpcm__mzzc in arr_types.
        types)


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
        uen__cpic = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            uaz__ugmrc = 0
            gilvr__wyhad = []
            for A in arr_list:
                fvu__jykyb = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                gilvr__wyhad.append(bodo.libs.array_item_arr_ext.get_data(A))
                uaz__ugmrc += fvu__jykyb
            hmvc__rxq = np.empty(uaz__ugmrc + 1, offset_type)
            abivd__oyjso = bodo.libs.array_kernels.concat(gilvr__wyhad)
            vfhlk__tnk = np.empty(uaz__ugmrc + 7 >> 3, np.uint8)
            gcxvy__oapmz = 0
            wrr__hakua = 0
            for A in arr_list:
                etfk__xltic = bodo.libs.array_item_arr_ext.get_offsets(A)
                kltu__nin = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                fvu__jykyb = len(A)
                fsu__rrh = etfk__xltic[fvu__jykyb]
                for i in range(fvu__jykyb):
                    hmvc__rxq[i + gcxvy__oapmz] = etfk__xltic[i] + wrr__hakua
                    efda__hsrx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        kltu__nin, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vfhlk__tnk, i +
                        gcxvy__oapmz, efda__hsrx)
                gcxvy__oapmz += fvu__jykyb
                wrr__hakua += fsu__rrh
            hmvc__rxq[gcxvy__oapmz] = wrr__hakua
            rtmm__gqtgo = bodo.libs.array_item_arr_ext.init_array_item_array(
                uaz__ugmrc, abivd__oyjso, hmvc__rxq, vfhlk__tnk)
            return rtmm__gqtgo
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        ogi__ttbv = arr_list.dtype.names
        jrqc__cvfzx = 'def struct_array_concat_impl(arr_list):\n'
        jrqc__cvfzx += f'    n_all = 0\n'
        for i in range(len(ogi__ttbv)):
            jrqc__cvfzx += f'    concat_list{i} = []\n'
        jrqc__cvfzx += '    for A in arr_list:\n'
        jrqc__cvfzx += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(ogi__ttbv)):
            jrqc__cvfzx += f'        concat_list{i}.append(data_tuple[{i}])\n'
        jrqc__cvfzx += '        n_all += len(A)\n'
        jrqc__cvfzx += '    n_bytes = (n_all + 7) >> 3\n'
        jrqc__cvfzx += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        jrqc__cvfzx += '    curr_bit = 0\n'
        jrqc__cvfzx += '    for A in arr_list:\n'
        jrqc__cvfzx += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        jrqc__cvfzx += '        for j in range(len(A)):\n'
        jrqc__cvfzx += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        jrqc__cvfzx += """            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)
"""
        jrqc__cvfzx += '            curr_bit += 1\n'
        jrqc__cvfzx += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        pgwct__nvpv = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(ogi__ttbv))])
        jrqc__cvfzx += f'        ({pgwct__nvpv},),\n'
        jrqc__cvfzx += '        new_mask,\n'
        jrqc__cvfzx += f'        {ogi__ttbv},\n'
        jrqc__cvfzx += '    )\n'
        zht__uxyib = {}
        exec(jrqc__cvfzx, {'bodo': bodo, 'np': np}, zht__uxyib)
        return zht__uxyib['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            ubm__fydf = 0
            for A in arr_list:
                ubm__fydf += len(A)
            cudwo__tcbw = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(ubm__fydf))
            bxl__mbk = 0
            for A in arr_list:
                for i in range(len(A)):
                    cudwo__tcbw._data[i + bxl__mbk] = A._data[i]
                    efda__hsrx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(cudwo__tcbw.
                        _null_bitmap, i + bxl__mbk, efda__hsrx)
                bxl__mbk += len(A)
            return cudwo__tcbw
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            ubm__fydf = 0
            for A in arr_list:
                ubm__fydf += len(A)
            cudwo__tcbw = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(ubm__fydf))
            bxl__mbk = 0
            for A in arr_list:
                for i in range(len(A)):
                    cudwo__tcbw._days_data[i + bxl__mbk] = A._days_data[i]
                    cudwo__tcbw._seconds_data[i + bxl__mbk] = A._seconds_data[i
                        ]
                    cudwo__tcbw._microseconds_data[i + bxl__mbk
                        ] = A._microseconds_data[i]
                    efda__hsrx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(cudwo__tcbw.
                        _null_bitmap, i + bxl__mbk, efda__hsrx)
                bxl__mbk += len(A)
            return cudwo__tcbw
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        nbfb__wxblu = arr_list.dtype.precision
        elzka__rdjg = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            ubm__fydf = 0
            for A in arr_list:
                ubm__fydf += len(A)
            cudwo__tcbw = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                ubm__fydf, nbfb__wxblu, elzka__rdjg)
            bxl__mbk = 0
            for A in arr_list:
                for i in range(len(A)):
                    cudwo__tcbw._data[i + bxl__mbk] = A._data[i]
                    efda__hsrx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(cudwo__tcbw.
                        _null_bitmap, i + bxl__mbk, efda__hsrx)
                bxl__mbk += len(A)
            return cudwo__tcbw
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        vpcm__mzzc) for vpcm__mzzc in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            ldn__uax = arr_list.types[0]
        else:
            ldn__uax = arr_list.dtype
        ldn__uax = to_str_arr_if_dict_array(ldn__uax)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            ujbz__ggh = 0
            euo__ioa = 0
            for A in arr_list:
                arr = A
                ujbz__ggh += len(arr)
                euo__ioa += bodo.libs.str_arr_ext.num_total_chars(arr)
            rtmm__gqtgo = bodo.utils.utils.alloc_type(ujbz__ggh, ldn__uax,
                (euo__ioa,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(rtmm__gqtgo, -1)
            klfu__arfj = 0
            uct__mnscf = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(rtmm__gqtgo,
                    arr, klfu__arfj, uct__mnscf)
                klfu__arfj += len(arr)
                uct__mnscf += bodo.libs.str_arr_ext.num_total_chars(arr)
            return rtmm__gqtgo
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(vpcm__mzzc.dtype, types.Integer) for
        vpcm__mzzc in arr_list.types) and any(isinstance(vpcm__mzzc,
        IntegerArrayType) for vpcm__mzzc in arr_list.types):

        def impl_int_arr_list(arr_list):
            mgt__vhfki = convert_to_nullable_tup(arr_list)
            axa__ycr = []
            hlcl__lst = 0
            for A in mgt__vhfki:
                axa__ycr.append(A._data)
                hlcl__lst += len(A)
            abivd__oyjso = bodo.libs.array_kernels.concat(axa__ycr)
            cnay__atu = hlcl__lst + 7 >> 3
            neh__mtavb = np.empty(cnay__atu, np.uint8)
            hqw__qgy = 0
            for A in mgt__vhfki:
                dqcj__sbo = A._null_bitmap
                for gyg__knqs in range(len(A)):
                    efda__hsrx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        dqcj__sbo, gyg__knqs)
                    bodo.libs.int_arr_ext.set_bit_to_arr(neh__mtavb,
                        hqw__qgy, efda__hsrx)
                    hqw__qgy += 1
            return bodo.libs.int_arr_ext.init_integer_array(abivd__oyjso,
                neh__mtavb)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(vpcm__mzzc.dtype == types.bool_ for vpcm__mzzc in
        arr_list.types) and any(vpcm__mzzc == boolean_array for vpcm__mzzc in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            mgt__vhfki = convert_to_nullable_tup(arr_list)
            axa__ycr = []
            hlcl__lst = 0
            for A in mgt__vhfki:
                axa__ycr.append(A._data)
                hlcl__lst += len(A)
            abivd__oyjso = bodo.libs.array_kernels.concat(axa__ycr)
            cnay__atu = hlcl__lst + 7 >> 3
            neh__mtavb = np.empty(cnay__atu, np.uint8)
            hqw__qgy = 0
            for A in mgt__vhfki:
                dqcj__sbo = A._null_bitmap
                for gyg__knqs in range(len(A)):
                    efda__hsrx = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        dqcj__sbo, gyg__knqs)
                    bodo.libs.int_arr_ext.set_bit_to_arr(neh__mtavb,
                        hqw__qgy, efda__hsrx)
                    hqw__qgy += 1
            return bodo.libs.bool_arr_ext.init_bool_array(abivd__oyjso,
                neh__mtavb)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            edqi__dmoic = []
            for A in arr_list:
                edqi__dmoic.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                edqi__dmoic), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        ihhyi__zdjou = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        jrqc__cvfzx = 'def impl(arr_list):\n'
        jrqc__cvfzx += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({ihhyi__zdjou},)), arr_list[0].dtype)
"""
        xaw__tcsg = {}
        exec(jrqc__cvfzx, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, xaw__tcsg)
        return xaw__tcsg['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            hlcl__lst = 0
            for A in arr_list:
                hlcl__lst += len(A)
            rtmm__gqtgo = np.empty(hlcl__lst, dtype)
            llvls__wsux = 0
            for A in arr_list:
                n = len(A)
                rtmm__gqtgo[llvls__wsux:llvls__wsux + n] = A
                llvls__wsux += n
            return rtmm__gqtgo
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(vpcm__mzzc,
        (types.Array, IntegerArrayType)) and isinstance(vpcm__mzzc.dtype,
        types.Integer) for vpcm__mzzc in arr_list.types) and any(isinstance
        (vpcm__mzzc, types.Array) and isinstance(vpcm__mzzc.dtype, types.
        Float) for vpcm__mzzc in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            svfiy__fok = []
            for A in arr_list:
                svfiy__fok.append(A._data)
            bidi__atiwo = bodo.libs.array_kernels.concat(svfiy__fok)
            qai__buvxv = bodo.libs.map_arr_ext.init_map_arr(bidi__atiwo)
            return qai__buvxv
        return impl_map_arr_list
    for mrj__cob in arr_list:
        if not isinstance(mrj__cob, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(vpcm__mzzc.astype(np.float64) for vpcm__mzzc in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    gonbq__vpbf = len(arr_tup.types)
    jrqc__cvfzx = 'def f(arr_tup):\n'
    jrqc__cvfzx += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        gonbq__vpbf)), ',' if gonbq__vpbf == 1 else '')
    zht__uxyib = {}
    exec(jrqc__cvfzx, {'np': np}, zht__uxyib)
    tado__jxet = zht__uxyib['f']
    return tado__jxet


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    gonbq__vpbf = len(arr_tup.types)
    ird__nsvf = find_common_np_dtype(arr_tup.types)
    gpan__qujhi = None
    noqis__ajdhm = ''
    if isinstance(ird__nsvf, types.Integer):
        gpan__qujhi = bodo.libs.int_arr_ext.IntDtype(ird__nsvf)
        noqis__ajdhm = '.astype(out_dtype, False)'
    jrqc__cvfzx = 'def f(arr_tup):\n'
    jrqc__cvfzx += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, noqis__ajdhm) for i in range(gonbq__vpbf)), ',' if 
        gonbq__vpbf == 1 else '')
    zht__uxyib = {}
    exec(jrqc__cvfzx, {'bodo': bodo, 'out_dtype': gpan__qujhi}, zht__uxyib)
    mwvh__jbnjr = zht__uxyib['f']
    return mwvh__jbnjr


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, qxi__ofry = build_set_seen_na(A)
        return len(s) + int(not dropna and qxi__ofry)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        zlub__nie = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        adiv__zyjw = len(zlub__nie)
        return bodo.libs.distributed_api.dist_reduce(adiv__zyjw, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([ryi__wygbw for ryi__wygbw in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        dymey__vtelc = np.finfo(A.dtype(1).dtype).max
    else:
        dymey__vtelc = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        rtmm__gqtgo = np.empty(n, A.dtype)
        pqafo__zudxl = dymey__vtelc
        for i in range(n):
            pqafo__zudxl = min(pqafo__zudxl, A[i])
            rtmm__gqtgo[i] = pqafo__zudxl
        return rtmm__gqtgo
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        dymey__vtelc = np.finfo(A.dtype(1).dtype).min
    else:
        dymey__vtelc = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        rtmm__gqtgo = np.empty(n, A.dtype)
        pqafo__zudxl = dymey__vtelc
        for i in range(n):
            pqafo__zudxl = max(pqafo__zudxl, A[i])
            rtmm__gqtgo[i] = pqafo__zudxl
        return rtmm__gqtgo
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        bptr__nafdy = arr_info_list_to_table([array_to_info(A)])
        fdts__baik = 1
        fklv__nqyw = 0
        ook__yweiw = drop_duplicates_table(bptr__nafdy, parallel,
            fdts__baik, fklv__nqyw, dropna, True)
        rtmm__gqtgo = info_to_array(info_from_table(ook__yweiw, 0), A)
        delete_table(bptr__nafdy)
        delete_table(ook__yweiw)
        return rtmm__gqtgo
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    uen__cpic = bodo.utils.typing.to_nullable_type(arr.dtype)
    aufqm__hft = index_arr
    zherf__fyla = aufqm__hft.dtype

    def impl(arr, index_arr):
        n = len(arr)
        kufa__tst = init_nested_counts(uen__cpic)
        pdc__fmqp = init_nested_counts(zherf__fyla)
        for i in range(n):
            dxpbq__vmhm = index_arr[i]
            if isna(arr, i):
                kufa__tst = (kufa__tst[0] + 1,) + kufa__tst[1:]
                pdc__fmqp = add_nested_counts(pdc__fmqp, dxpbq__vmhm)
                continue
            oiwi__pkccy = arr[i]
            if len(oiwi__pkccy) == 0:
                kufa__tst = (kufa__tst[0] + 1,) + kufa__tst[1:]
                pdc__fmqp = add_nested_counts(pdc__fmqp, dxpbq__vmhm)
                continue
            kufa__tst = add_nested_counts(kufa__tst, oiwi__pkccy)
            for ovd__bkeyp in range(len(oiwi__pkccy)):
                pdc__fmqp = add_nested_counts(pdc__fmqp, dxpbq__vmhm)
        rtmm__gqtgo = bodo.utils.utils.alloc_type(kufa__tst[0], uen__cpic,
            kufa__tst[1:])
        unrh__idvvd = bodo.utils.utils.alloc_type(kufa__tst[0], aufqm__hft,
            pdc__fmqp)
        wrr__hakua = 0
        for i in range(n):
            if isna(arr, i):
                setna(rtmm__gqtgo, wrr__hakua)
                unrh__idvvd[wrr__hakua] = index_arr[i]
                wrr__hakua += 1
                continue
            oiwi__pkccy = arr[i]
            fsu__rrh = len(oiwi__pkccy)
            if fsu__rrh == 0:
                setna(rtmm__gqtgo, wrr__hakua)
                unrh__idvvd[wrr__hakua] = index_arr[i]
                wrr__hakua += 1
                continue
            rtmm__gqtgo[wrr__hakua:wrr__hakua + fsu__rrh] = oiwi__pkccy
            unrh__idvvd[wrr__hakua:wrr__hakua + fsu__rrh] = index_arr[i]
            wrr__hakua += fsu__rrh
        return rtmm__gqtgo, unrh__idvvd
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    uen__cpic = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        kufa__tst = init_nested_counts(uen__cpic)
        for i in range(n):
            if isna(arr, i):
                kufa__tst = (kufa__tst[0] + 1,) + kufa__tst[1:]
                wpxtz__zqxeg = 1
            else:
                oiwi__pkccy = arr[i]
                vzw__otx = len(oiwi__pkccy)
                if vzw__otx == 0:
                    kufa__tst = (kufa__tst[0] + 1,) + kufa__tst[1:]
                    wpxtz__zqxeg = 1
                    continue
                else:
                    kufa__tst = add_nested_counts(kufa__tst, oiwi__pkccy)
                    wpxtz__zqxeg = vzw__otx
            if counts[i] != wpxtz__zqxeg:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        rtmm__gqtgo = bodo.utils.utils.alloc_type(kufa__tst[0], uen__cpic,
            kufa__tst[1:])
        wrr__hakua = 0
        for i in range(n):
            if isna(arr, i):
                setna(rtmm__gqtgo, wrr__hakua)
                wrr__hakua += 1
                continue
            oiwi__pkccy = arr[i]
            fsu__rrh = len(oiwi__pkccy)
            if fsu__rrh == 0:
                setna(rtmm__gqtgo, wrr__hakua)
                wrr__hakua += 1
                continue
            rtmm__gqtgo[wrr__hakua:wrr__hakua + fsu__rrh] = oiwi__pkccy
            wrr__hakua += fsu__rrh
        return rtmm__gqtgo
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(lph__ftnu) for lph__ftnu in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        zauxp__gey = 'np.empty(n, np.int64)'
        mesiy__hfps = 'out_arr[i] = 1'
        eek__saw = 'max(len(arr[i]), 1)'
    else:
        zauxp__gey = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        mesiy__hfps = 'bodo.libs.array_kernels.setna(out_arr, i)'
        eek__saw = 'len(arr[i])'
    jrqc__cvfzx = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {zauxp__gey}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {mesiy__hfps}
        else:
            out_arr[i] = {eek__saw}
    return out_arr
    """
    zht__uxyib = {}
    exec(jrqc__cvfzx, {'bodo': bodo, 'numba': numba, 'np': np}, zht__uxyib)
    impl = zht__uxyib['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    aufqm__hft = index_arr
    zherf__fyla = aufqm__hft.dtype

    def impl(arr, pat, n, index_arr):
        mzshc__nnlii = pat is not None and len(pat) > 1
        if mzshc__nnlii:
            xqg__jgb = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        faatw__fhu = len(arr)
        ujbz__ggh = 0
        euo__ioa = 0
        pdc__fmqp = init_nested_counts(zherf__fyla)
        for i in range(faatw__fhu):
            dxpbq__vmhm = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                ujbz__ggh += 1
                pdc__fmqp = add_nested_counts(pdc__fmqp, dxpbq__vmhm)
                continue
            if mzshc__nnlii:
                nctuq__geqn = xqg__jgb.split(arr[i], maxsplit=n)
            else:
                nctuq__geqn = arr[i].split(pat, n)
            ujbz__ggh += len(nctuq__geqn)
            for s in nctuq__geqn:
                pdc__fmqp = add_nested_counts(pdc__fmqp, dxpbq__vmhm)
                euo__ioa += bodo.libs.str_arr_ext.get_utf8_size(s)
        rtmm__gqtgo = bodo.libs.str_arr_ext.pre_alloc_string_array(ujbz__ggh,
            euo__ioa)
        unrh__idvvd = bodo.utils.utils.alloc_type(ujbz__ggh, aufqm__hft,
            pdc__fmqp)
        qlrm__osm = 0
        for gyg__knqs in range(faatw__fhu):
            if isna(arr, gyg__knqs):
                rtmm__gqtgo[qlrm__osm] = ''
                bodo.libs.array_kernels.setna(rtmm__gqtgo, qlrm__osm)
                unrh__idvvd[qlrm__osm] = index_arr[gyg__knqs]
                qlrm__osm += 1
                continue
            if mzshc__nnlii:
                nctuq__geqn = xqg__jgb.split(arr[gyg__knqs], maxsplit=n)
            else:
                nctuq__geqn = arr[gyg__knqs].split(pat, n)
            ahrle__zrfd = len(nctuq__geqn)
            rtmm__gqtgo[qlrm__osm:qlrm__osm + ahrle__zrfd] = nctuq__geqn
            unrh__idvvd[qlrm__osm:qlrm__osm + ahrle__zrfd] = index_arr[
                gyg__knqs]
            qlrm__osm += ahrle__zrfd
        return rtmm__gqtgo, unrh__idvvd
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
            rtmm__gqtgo = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                rtmm__gqtgo[i] = np.nan
            return rtmm__gqtgo
        return impl_float
    hnip__ywy = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        rtmm__gqtgo = bodo.utils.utils.alloc_type(n, hnip__ywy, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(rtmm__gqtgo, i)
        return rtmm__gqtgo
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
    whkq__ielah = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            rtmm__gqtgo = bodo.utils.utils.alloc_type(new_len, whkq__ielah)
            bodo.libs.str_arr_ext.str_copy_ptr(rtmm__gqtgo.ctypes, 0, A.
                ctypes, old_size)
            return rtmm__gqtgo
        return impl_char

    def impl(A, old_size, new_len):
        rtmm__gqtgo = bodo.utils.utils.alloc_type(new_len, whkq__ielah, (-1,))
        rtmm__gqtgo[:old_size] = A[:old_size]
        return rtmm__gqtgo
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    dvym__nkqnf = math.ceil((stop - start) / step)
    return int(max(dvym__nkqnf, 0))


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
    if any(isinstance(ryi__wygbw, types.Complex) for ryi__wygbw in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            ory__xzubc = (stop - start) / step
            dvym__nkqnf = math.ceil(ory__xzubc.real)
            pwwv__wqi = math.ceil(ory__xzubc.imag)
            pzpm__hiad = int(max(min(pwwv__wqi, dvym__nkqnf), 0))
            arr = np.empty(pzpm__hiad, dtype)
            for i in numba.parfors.parfor.internal_prange(pzpm__hiad):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            pzpm__hiad = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(pzpm__hiad, dtype)
            for i in numba.parfors.parfor.internal_prange(pzpm__hiad):
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
        tld__mqn = arr,
        if not inplace:
            tld__mqn = arr.copy(),
        gpel__ihpi = bodo.libs.str_arr_ext.to_list_if_immutable_arr(tld__mqn)
        watj__ocdz = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(gpel__ihpi, 0, n, watj__ocdz)
        if not ascending:
            bodo.libs.timsort.reverseRange(gpel__ihpi, 0, n, watj__ocdz)
        bodo.libs.str_arr_ext.cp_str_list_to_array(tld__mqn, gpel__ihpi)
        return tld__mqn[0]
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
        qai__buvxv = []
        for i in range(n):
            if A[i]:
                qai__buvxv.append(i + offset)
        return np.array(qai__buvxv, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    whkq__ielah = element_type(A)
    if whkq__ielah == types.unicode_type:
        null_value = '""'
    elif whkq__ielah == types.bool_:
        null_value = 'False'
    elif whkq__ielah == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif whkq__ielah == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    qlrm__osm = 'i'
    tykzv__lnpz = False
    vvamd__imktg = get_overload_const_str(method)
    if vvamd__imktg in ('ffill', 'pad'):
        xhi__ctuoq = 'n'
        send_right = True
    elif vvamd__imktg in ('backfill', 'bfill'):
        xhi__ctuoq = 'n-1, -1, -1'
        send_right = False
        if whkq__ielah == types.unicode_type:
            qlrm__osm = '(n - 1) - i'
            tykzv__lnpz = True
    jrqc__cvfzx = 'def impl(A, method, parallel=False):\n'
    jrqc__cvfzx += '  A = decode_if_dict_array(A)\n'
    jrqc__cvfzx += '  has_last_value = False\n'
    jrqc__cvfzx += f'  last_value = {null_value}\n'
    jrqc__cvfzx += '  if parallel:\n'
    jrqc__cvfzx += '    rank = bodo.libs.distributed_api.get_rank()\n'
    jrqc__cvfzx += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    jrqc__cvfzx += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    jrqc__cvfzx += '  n = len(A)\n'
    jrqc__cvfzx += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    jrqc__cvfzx += f'  for i in range({xhi__ctuoq}):\n'
    jrqc__cvfzx += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    jrqc__cvfzx += (
        f'      bodo.libs.array_kernels.setna(out_arr, {qlrm__osm})\n')
    jrqc__cvfzx += '      continue\n'
    jrqc__cvfzx += '    s = A[i]\n'
    jrqc__cvfzx += '    if bodo.libs.array_kernels.isna(A, i):\n'
    jrqc__cvfzx += '      s = last_value\n'
    jrqc__cvfzx += f'    out_arr[{qlrm__osm}] = s\n'
    jrqc__cvfzx += '    last_value = s\n'
    jrqc__cvfzx += '    has_last_value = True\n'
    if tykzv__lnpz:
        jrqc__cvfzx += '  return out_arr[::-1]\n'
    else:
        jrqc__cvfzx += '  return out_arr\n'
    udoei__hjtbk = {}
    exec(jrqc__cvfzx, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, udoei__hjtbk)
    impl = udoei__hjtbk['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        liyu__knr = 0
        amv__brukz = n_pes - 1
        xdaw__dzzyt = np.int32(rank + 1)
        zcq__xer = np.int32(rank - 1)
        tbtjb__smi = len(in_arr) - 1
        sam__tze = -1
        bfb__yner = -1
    else:
        liyu__knr = n_pes - 1
        amv__brukz = 0
        xdaw__dzzyt = np.int32(rank - 1)
        zcq__xer = np.int32(rank + 1)
        tbtjb__smi = 0
        sam__tze = len(in_arr)
        bfb__yner = 1
    qsbgk__qxszq = np.int32(bodo.hiframes.rolling.comm_border_tag)
    inkb__byv = np.empty(1, dtype=np.bool_)
    qmk__vbop = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    hzmyo__bjde = np.empty(1, dtype=np.bool_)
    vjn__ikvd = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    yvt__exbzl = False
    sunk__rknio = null_value
    for i in range(tbtjb__smi, sam__tze, bfb__yner):
        if not isna(in_arr, i):
            yvt__exbzl = True
            sunk__rknio = in_arr[i]
            break
    if rank != liyu__knr:
        icjk__idp = bodo.libs.distributed_api.irecv(inkb__byv, 1, zcq__xer,
            qsbgk__qxszq, True)
        bodo.libs.distributed_api.wait(icjk__idp, True)
        bem__niiz = bodo.libs.distributed_api.irecv(qmk__vbop, 1, zcq__xer,
            qsbgk__qxszq, True)
        bodo.libs.distributed_api.wait(bem__niiz, True)
        vuf__ovrll = inkb__byv[0]
        eoi__hjn = qmk__vbop[0]
    else:
        vuf__ovrll = False
        eoi__hjn = null_value
    if yvt__exbzl:
        hzmyo__bjde[0] = yvt__exbzl
        vjn__ikvd[0] = sunk__rknio
    else:
        hzmyo__bjde[0] = vuf__ovrll
        vjn__ikvd[0] = eoi__hjn
    if rank != amv__brukz:
        ial__tgm = bodo.libs.distributed_api.isend(hzmyo__bjde, 1,
            xdaw__dzzyt, qsbgk__qxszq, True)
        amps__caep = bodo.libs.distributed_api.isend(vjn__ikvd, 1,
            xdaw__dzzyt, qsbgk__qxszq, True)
    return vuf__ovrll, eoi__hjn


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    iax__fund = {'axis': axis, 'kind': kind, 'order': order}
    cxqn__tloq = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', iax__fund, cxqn__tloq, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    whkq__ielah = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            faatw__fhu = len(A)
            rtmm__gqtgo = bodo.utils.utils.alloc_type(faatw__fhu * repeats,
                whkq__ielah, (-1,))
            for i in range(faatw__fhu):
                qlrm__osm = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for gyg__knqs in range(repeats):
                        bodo.libs.array_kernels.setna(rtmm__gqtgo, 
                            qlrm__osm + gyg__knqs)
                else:
                    rtmm__gqtgo[qlrm__osm:qlrm__osm + repeats] = A[i]
            return rtmm__gqtgo
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        faatw__fhu = len(A)
        rtmm__gqtgo = bodo.utils.utils.alloc_type(repeats.sum(),
            whkq__ielah, (-1,))
        qlrm__osm = 0
        for i in range(faatw__fhu):
            whehn__tcgx = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for gyg__knqs in range(whehn__tcgx):
                    bodo.libs.array_kernels.setna(rtmm__gqtgo, qlrm__osm +
                        gyg__knqs)
            else:
                rtmm__gqtgo[qlrm__osm:qlrm__osm + whehn__tcgx] = A[i]
            qlrm__osm += whehn__tcgx
        return rtmm__gqtgo
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
        aktox__yxl = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(aktox__yxl, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        rgb__towti = bodo.libs.array_kernels.concat([A1, A2])
        ewx__czuw = bodo.libs.array_kernels.unique(rgb__towti)
        return pd.Series(ewx__czuw).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    iax__fund = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    cxqn__tloq = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', iax__fund, cxqn__tloq, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        pkx__focb = bodo.libs.array_kernels.unique(A1)
        njx__lap = bodo.libs.array_kernels.unique(A2)
        rgb__towti = bodo.libs.array_kernels.concat([pkx__focb, njx__lap])
        prol__buus = pd.Series(rgb__towti).sort_values().values
        return slice_array_intersect1d(prol__buus)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    lkm__ujwq = arr[1:] == arr[:-1]
    return arr[:-1][lkm__ujwq]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    iax__fund = {'assume_unique': assume_unique}
    cxqn__tloq = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', iax__fund, cxqn__tloq, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        pkx__focb = bodo.libs.array_kernels.unique(A1)
        njx__lap = bodo.libs.array_kernels.unique(A2)
        lkm__ujwq = calculate_mask_setdiff1d(pkx__focb, njx__lap)
        return pd.Series(pkx__focb[lkm__ujwq]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    lkm__ujwq = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        lkm__ujwq &= A1 != A2[i]
    return lkm__ujwq


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    iax__fund = {'retstep': retstep, 'axis': axis}
    cxqn__tloq = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', iax__fund, cxqn__tloq, 'numpy')
    tmvc__zbnfi = False
    if is_overload_none(dtype):
        whkq__ielah = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            tmvc__zbnfi = True
        whkq__ielah = numba.np.numpy_support.as_dtype(dtype).type
    if tmvc__zbnfi:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            wwxc__vpdfy = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            rtmm__gqtgo = np.empty(num, whkq__ielah)
            for i in numba.parfors.parfor.internal_prange(num):
                rtmm__gqtgo[i] = whkq__ielah(np.floor(start + i * wwxc__vpdfy))
            return rtmm__gqtgo
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            wwxc__vpdfy = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            rtmm__gqtgo = np.empty(num, whkq__ielah)
            for i in numba.parfors.parfor.internal_prange(num):
                rtmm__gqtgo[i] = whkq__ielah(start + i * wwxc__vpdfy)
            return rtmm__gqtgo
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
        gonbq__vpbf = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                gonbq__vpbf += A[i] == val
        return gonbq__vpbf > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    iax__fund = {'axis': axis, 'out': out, 'keepdims': keepdims}
    cxqn__tloq = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', iax__fund, cxqn__tloq, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        gonbq__vpbf = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                gonbq__vpbf += int(bool(A[i]))
        return gonbq__vpbf > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    iax__fund = {'axis': axis, 'out': out, 'keepdims': keepdims}
    cxqn__tloq = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', iax__fund, cxqn__tloq, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        gonbq__vpbf = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                gonbq__vpbf += int(bool(A[i]))
        return gonbq__vpbf == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    iax__fund = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    cxqn__tloq = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', iax__fund, cxqn__tloq, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        pawy__wcvkx = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            rtmm__gqtgo = np.empty(n, pawy__wcvkx)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(rtmm__gqtgo, i)
                    continue
                rtmm__gqtgo[i] = np_cbrt_scalar(A[i], pawy__wcvkx)
            return rtmm__gqtgo
        return impl_arr
    pawy__wcvkx = np.promote_types(numba.np.numpy_support.as_dtype(A),
        numba.np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, pawy__wcvkx)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    ivde__efumi = x < 0
    if ivde__efumi:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if ivde__efumi:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    mrt__cjo = isinstance(tup, (types.BaseTuple, types.List))
    jix__qeakr = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for mrj__cob in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(mrj__cob,
                'numpy.hstack()')
            mrt__cjo = mrt__cjo and bodo.utils.utils.is_array_typ(mrj__cob,
                False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        mrt__cjo = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif jix__qeakr:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        ywlb__lob = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for mrj__cob in ywlb__lob.types:
            jix__qeakr = jix__qeakr and bodo.utils.utils.is_array_typ(mrj__cob,
                False)
    if not (mrt__cjo or jix__qeakr):
        return
    if jix__qeakr:

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
    iax__fund = {'check_valid': check_valid, 'tol': tol}
    cxqn__tloq = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', iax__fund,
        cxqn__tloq, 'numpy')
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
        iigdx__bot = mean.shape[0]
        eeubh__vilij = size, iigdx__bot
        weqlv__bcmzw = np.random.standard_normal(eeubh__vilij)
        cov = cov.astype(np.float64)
        bfo__zdt, s, wezg__ret = np.linalg.svd(cov)
        res = np.dot(weqlv__bcmzw, np.sqrt(s).reshape(iigdx__bot, 1) *
            wezg__ret)
        igcfr__aem = res + mean
        return igcfr__aem
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
            hrzou__ggdw = bodo.hiframes.series_kernels._get_type_max_value(arr)
            tjvn__pjmp = typing.builtins.IndexValue(-1, hrzou__ggdw)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                umpo__ujxtk = typing.builtins.IndexValue(i, arr[i])
                tjvn__pjmp = min(tjvn__pjmp, umpo__ujxtk)
            return tjvn__pjmp.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        gyy__jvo = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def impl_cat_arr(arr):
            gxo__txi = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            hrzou__ggdw = gyy__jvo(len(arr.dtype.categories) + 1)
            tjvn__pjmp = typing.builtins.IndexValue(-1, hrzou__ggdw)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                umpo__ujxtk = typing.builtins.IndexValue(i, gxo__txi[i])
                tjvn__pjmp = min(tjvn__pjmp, umpo__ujxtk)
            return tjvn__pjmp.index
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
            hrzou__ggdw = bodo.hiframes.series_kernels._get_type_min_value(arr)
            tjvn__pjmp = typing.builtins.IndexValue(-1, hrzou__ggdw)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                umpo__ujxtk = typing.builtins.IndexValue(i, arr[i])
                tjvn__pjmp = max(tjvn__pjmp, umpo__ujxtk)
            return tjvn__pjmp.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        gyy__jvo = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            gxo__txi = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            hrzou__ggdw = gyy__jvo(-1)
            tjvn__pjmp = typing.builtins.IndexValue(-1, hrzou__ggdw)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                umpo__ujxtk = typing.builtins.IndexValue(i, gxo__txi[i])
                tjvn__pjmp = max(tjvn__pjmp, umpo__ujxtk)
            return tjvn__pjmp.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
