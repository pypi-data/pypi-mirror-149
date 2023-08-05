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
        dvte__pac = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = dvte__pac
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        dvte__pac = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = dvte__pac
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
            lxl__zxcak = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            lxl__zxcak[ind + 1] = lxl__zxcak[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            lxl__zxcak = bodo.libs.array_item_arr_ext.get_offsets(arr)
            lxl__zxcak[ind + 1] = lxl__zxcak[ind]
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
    llqns__ithah = arr_tup.count
    fjbtv__jljq = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(llqns__ithah):
        fjbtv__jljq += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    fjbtv__jljq += '  return\n'
    ghf__scrn = {}
    exec(fjbtv__jljq, {'setna': setna}, ghf__scrn)
    impl = ghf__scrn['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        fuecb__jfwu = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(fuecb__jfwu.start, fuecb__jfwu.stop, fuecb__jfwu.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        wymu__hmmo = 'n'
        rmy__kisjj = 'n_pes'
        cydu__yois = 'min_op'
    else:
        wymu__hmmo = 'n-1, -1, -1'
        rmy__kisjj = '-1'
        cydu__yois = 'max_op'
    fjbtv__jljq = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {rmy__kisjj}
    for i in range({wymu__hmmo}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {cydu__yois}))
        if possible_valid_rank != {rmy__kisjj}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    ghf__scrn = {}
    exec(fjbtv__jljq, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, ghf__scrn)
    impl = ghf__scrn['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    lrv__qezde = array_to_info(arr)
    _median_series_computation(res, lrv__qezde, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(lrv__qezde)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    lrv__qezde = array_to_info(arr)
    _autocorr_series_computation(res, lrv__qezde, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(lrv__qezde)


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
    lrv__qezde = array_to_info(arr)
    _compute_series_monotonicity(res, lrv__qezde, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(lrv__qezde)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    dwl__eir = res[0] > 0.5
    return dwl__eir


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        qvz__uxea = '-'
        wpij__qpq = 'index_arr[0] > threshhold_date'
        wymu__hmmo = '1, n+1'
        aknu__wejio = 'index_arr[-i] <= threshhold_date'
        aqm__pgl = 'i - 1'
    else:
        qvz__uxea = '+'
        wpij__qpq = 'index_arr[-1] < threshhold_date'
        wymu__hmmo = 'n'
        aknu__wejio = 'index_arr[i] >= threshhold_date'
        aqm__pgl = 'i'
    fjbtv__jljq = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        fjbtv__jljq += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        fjbtv__jljq += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            fjbtv__jljq += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            fjbtv__jljq += """      threshhold_date = initial_date - date_offset.base + date_offset
"""
            fjbtv__jljq += '    else:\n'
            fjbtv__jljq += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            fjbtv__jljq += (
                f'    threshhold_date = initial_date {qvz__uxea} date_offset\n'
                )
    else:
        fjbtv__jljq += f'  threshhold_date = initial_date {qvz__uxea} offset\n'
    fjbtv__jljq += '  local_valid = 0\n'
    fjbtv__jljq += f'  n = len(index_arr)\n'
    fjbtv__jljq += f'  if n:\n'
    fjbtv__jljq += f'    if {wpij__qpq}:\n'
    fjbtv__jljq += '      loc_valid = n\n'
    fjbtv__jljq += '    else:\n'
    fjbtv__jljq += f'      for i in range({wymu__hmmo}):\n'
    fjbtv__jljq += f'        if {aknu__wejio}:\n'
    fjbtv__jljq += f'          loc_valid = {aqm__pgl}\n'
    fjbtv__jljq += '          break\n'
    fjbtv__jljq += '  if is_parallel:\n'
    fjbtv__jljq += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    fjbtv__jljq += '    return total_valid\n'
    fjbtv__jljq += '  else:\n'
    fjbtv__jljq += '    return loc_valid\n'
    ghf__scrn = {}
    exec(fjbtv__jljq, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, ghf__scrn)
    return ghf__scrn['impl']


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
    hkwae__gtoet = numba_to_c_type(sig.args[0].dtype)
    oknlb__fjy = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), hkwae__gtoet))
    lodyv__prdfm = args[0]
    qqu__atf = sig.args[0]
    if isinstance(qqu__atf, (IntegerArrayType, BooleanArrayType)):
        lodyv__prdfm = cgutils.create_struct_proxy(qqu__atf)(context,
            builder, lodyv__prdfm).data
        qqu__atf = types.Array(qqu__atf.dtype, 1, 'C')
    assert qqu__atf.ndim == 1
    arr = make_array(qqu__atf)(context, builder, lodyv__prdfm)
    aar__crrva = builder.extract_value(arr.shape, 0)
    hmiqm__aodk = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        aar__crrva, args[1], builder.load(oknlb__fjy)]
    tcn__vyx = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    fox__hdt = lir.FunctionType(lir.DoubleType(), tcn__vyx)
    payyl__dks = cgutils.get_or_insert_function(builder.module, fox__hdt,
        name='quantile_sequential')
    jqql__hnour = builder.call(payyl__dks, hmiqm__aodk)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return jqql__hnour


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    hkwae__gtoet = numba_to_c_type(sig.args[0].dtype)
    oknlb__fjy = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), hkwae__gtoet))
    lodyv__prdfm = args[0]
    qqu__atf = sig.args[0]
    if isinstance(qqu__atf, (IntegerArrayType, BooleanArrayType)):
        lodyv__prdfm = cgutils.create_struct_proxy(qqu__atf)(context,
            builder, lodyv__prdfm).data
        qqu__atf = types.Array(qqu__atf.dtype, 1, 'C')
    assert qqu__atf.ndim == 1
    arr = make_array(qqu__atf)(context, builder, lodyv__prdfm)
    aar__crrva = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        ptlkj__cfez = args[2]
    else:
        ptlkj__cfez = aar__crrva
    hmiqm__aodk = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        aar__crrva, ptlkj__cfez, args[1], builder.load(oknlb__fjy)]
    tcn__vyx = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType(
        64), lir.DoubleType(), lir.IntType(32)]
    fox__hdt = lir.FunctionType(lir.DoubleType(), tcn__vyx)
    payyl__dks = cgutils.get_or_insert_function(builder.module, fox__hdt,
        name='quantile_parallel')
    jqql__hnour = builder.call(payyl__dks, hmiqm__aodk)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return jqql__hnour


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    hqfek__xuh = start
    cazoh__sqikw = 2 * start + 1
    bay__azpi = 2 * start + 2
    if cazoh__sqikw < n and not cmp_f(arr[cazoh__sqikw], arr[hqfek__xuh]):
        hqfek__xuh = cazoh__sqikw
    if bay__azpi < n and not cmp_f(arr[bay__azpi], arr[hqfek__xuh]):
        hqfek__xuh = bay__azpi
    if hqfek__xuh != start:
        arr[start], arr[hqfek__xuh] = arr[hqfek__xuh], arr[start]
        ind_arr[start], ind_arr[hqfek__xuh] = ind_arr[hqfek__xuh], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, hqfek__xuh, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        aejo__olkg = np.empty(k, A.dtype)
        lwno__lgau = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                aejo__olkg[ind] = A[i]
                lwno__lgau[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            aejo__olkg = aejo__olkg[:ind]
            lwno__lgau = lwno__lgau[:ind]
        return aejo__olkg, lwno__lgau, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        oicbz__kqus = np.sort(A)
        fax__zasvu = index_arr[np.argsort(A)]
        hkroe__ndeta = pd.Series(oicbz__kqus).notna().values
        oicbz__kqus = oicbz__kqus[hkroe__ndeta]
        fax__zasvu = fax__zasvu[hkroe__ndeta]
        if is_largest:
            oicbz__kqus = oicbz__kqus[::-1]
            fax__zasvu = fax__zasvu[::-1]
        return np.ascontiguousarray(oicbz__kqus), np.ascontiguousarray(
            fax__zasvu)
    aejo__olkg, lwno__lgau, start = select_k_nonan(A, index_arr, m, k)
    lwno__lgau = lwno__lgau[aejo__olkg.argsort()]
    aejo__olkg.sort()
    if not is_largest:
        aejo__olkg = np.ascontiguousarray(aejo__olkg[::-1])
        lwno__lgau = np.ascontiguousarray(lwno__lgau[::-1])
    for i in range(start, m):
        if cmp_f(A[i], aejo__olkg[0]):
            aejo__olkg[0] = A[i]
            lwno__lgau[0] = index_arr[i]
            min_heapify(aejo__olkg, lwno__lgau, k, 0, cmp_f)
    lwno__lgau = lwno__lgau[aejo__olkg.argsort()]
    aejo__olkg.sort()
    if is_largest:
        aejo__olkg = aejo__olkg[::-1]
        lwno__lgau = lwno__lgau[::-1]
    return np.ascontiguousarray(aejo__olkg), np.ascontiguousarray(lwno__lgau)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    woj__rzuf = bodo.libs.distributed_api.get_rank()
    duvn__rdt, edunc__kkaiu = nlargest(A, I, k, is_largest, cmp_f)
    mcmy__yrfav = bodo.libs.distributed_api.gatherv(duvn__rdt)
    ldwbr__etl = bodo.libs.distributed_api.gatherv(edunc__kkaiu)
    if woj__rzuf == MPI_ROOT:
        res, mjnkv__ucsow = nlargest(mcmy__yrfav, ldwbr__etl, k, is_largest,
            cmp_f)
    else:
        res = np.empty(k, A.dtype)
        mjnkv__ucsow = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(mjnkv__ucsow)
    return res, mjnkv__ucsow


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    anni__ozin, qsjc__fuic = mat.shape
    mkng__iuia = np.empty((qsjc__fuic, qsjc__fuic), dtype=np.float64)
    for xfcd__lrq in range(qsjc__fuic):
        for qpjnw__emt in range(xfcd__lrq + 1):
            wrs__gmn = 0
            bargu__rki = hlydj__buncv = krfs__yauv = clior__apsrk = 0.0
            for i in range(anni__ozin):
                if np.isfinite(mat[i, xfcd__lrq]) and np.isfinite(mat[i,
                    qpjnw__emt]):
                    izdq__xuun = mat[i, xfcd__lrq]
                    socfz__odv = mat[i, qpjnw__emt]
                    wrs__gmn += 1
                    krfs__yauv += izdq__xuun
                    clior__apsrk += socfz__odv
            if parallel:
                wrs__gmn = bodo.libs.distributed_api.dist_reduce(wrs__gmn,
                    sum_op)
                krfs__yauv = bodo.libs.distributed_api.dist_reduce(krfs__yauv,
                    sum_op)
                clior__apsrk = bodo.libs.distributed_api.dist_reduce(
                    clior__apsrk, sum_op)
            if wrs__gmn < minpv:
                mkng__iuia[xfcd__lrq, qpjnw__emt] = mkng__iuia[qpjnw__emt,
                    xfcd__lrq] = np.nan
            else:
                dfrx__vqg = krfs__yauv / wrs__gmn
                wtj__ffu = clior__apsrk / wrs__gmn
                krfs__yauv = 0.0
                for i in range(anni__ozin):
                    if np.isfinite(mat[i, xfcd__lrq]) and np.isfinite(mat[i,
                        qpjnw__emt]):
                        izdq__xuun = mat[i, xfcd__lrq] - dfrx__vqg
                        socfz__odv = mat[i, qpjnw__emt] - wtj__ffu
                        krfs__yauv += izdq__xuun * socfz__odv
                        bargu__rki += izdq__xuun * izdq__xuun
                        hlydj__buncv += socfz__odv * socfz__odv
                if parallel:
                    krfs__yauv = bodo.libs.distributed_api.dist_reduce(
                        krfs__yauv, sum_op)
                    bargu__rki = bodo.libs.distributed_api.dist_reduce(
                        bargu__rki, sum_op)
                    hlydj__buncv = bodo.libs.distributed_api.dist_reduce(
                        hlydj__buncv, sum_op)
                bvdt__cvevh = wrs__gmn - 1.0 if cov else sqrt(bargu__rki *
                    hlydj__buncv)
                if bvdt__cvevh != 0.0:
                    mkng__iuia[xfcd__lrq, qpjnw__emt] = mkng__iuia[
                        qpjnw__emt, xfcd__lrq] = krfs__yauv / bvdt__cvevh
                else:
                    mkng__iuia[xfcd__lrq, qpjnw__emt] = mkng__iuia[
                        qpjnw__emt, xfcd__lrq] = np.nan
    return mkng__iuia


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    ajsy__xuq = n != 1
    fjbtv__jljq = 'def impl(data, parallel=False):\n'
    fjbtv__jljq += '  if parallel:\n'
    tnm__csx = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    fjbtv__jljq += f'    cpp_table = arr_info_list_to_table([{tnm__csx}])\n'
    fjbtv__jljq += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    cqqpw__ksfz = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    fjbtv__jljq += f'    data = ({cqqpw__ksfz},)\n'
    fjbtv__jljq += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    fjbtv__jljq += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    fjbtv__jljq += '    bodo.libs.array.delete_table(cpp_table)\n'
    fjbtv__jljq += '  n = len(data[0])\n'
    fjbtv__jljq += '  out = np.empty(n, np.bool_)\n'
    fjbtv__jljq += '  uniqs = dict()\n'
    if ajsy__xuq:
        fjbtv__jljq += '  for i in range(n):\n'
        kwzoq__yyn = ', '.join(f'data[{i}][i]' for i in range(n))
        vdqpt__fwpes = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        fjbtv__jljq += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({kwzoq__yyn},), ({vdqpt__fwpes},))
"""
        fjbtv__jljq += '    if val in uniqs:\n'
        fjbtv__jljq += '      out[i] = True\n'
        fjbtv__jljq += '    else:\n'
        fjbtv__jljq += '      out[i] = False\n'
        fjbtv__jljq += '      uniqs[val] = 0\n'
    else:
        fjbtv__jljq += '  data = data[0]\n'
        fjbtv__jljq += '  hasna = False\n'
        fjbtv__jljq += '  for i in range(n):\n'
        fjbtv__jljq += '    if bodo.libs.array_kernels.isna(data, i):\n'
        fjbtv__jljq += '      out[i] = hasna\n'
        fjbtv__jljq += '      hasna = True\n'
        fjbtv__jljq += '    else:\n'
        fjbtv__jljq += '      val = data[i]\n'
        fjbtv__jljq += '      if val in uniqs:\n'
        fjbtv__jljq += '        out[i] = True\n'
        fjbtv__jljq += '      else:\n'
        fjbtv__jljq += '        out[i] = False\n'
        fjbtv__jljq += '        uniqs[val] = 0\n'
    fjbtv__jljq += '  if parallel:\n'
    fjbtv__jljq += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    fjbtv__jljq += '  return out\n'
    ghf__scrn = {}
    exec(fjbtv__jljq, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        ghf__scrn)
    impl = ghf__scrn['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    llqns__ithah = len(data)
    fjbtv__jljq = (
        'def impl(data, ind_arr, n, frac, replace, parallel=False):\n')
    fjbtv__jljq += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        llqns__ithah)))
    fjbtv__jljq += '  table_total = arr_info_list_to_table(info_list_total)\n'
    fjbtv__jljq += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(llqns__ithah))
    for zekl__joakl in range(llqns__ithah):
        fjbtv__jljq += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(zekl__joakl, zekl__joakl, zekl__joakl))
    fjbtv__jljq += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(llqns__ithah))
    fjbtv__jljq += '  delete_table(out_table)\n'
    fjbtv__jljq += '  delete_table(table_total)\n'
    fjbtv__jljq += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(llqns__ithah)))
    ghf__scrn = {}
    exec(fjbtv__jljq, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, ghf__scrn)
    impl = ghf__scrn['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    llqns__ithah = len(data)
    fjbtv__jljq = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    fjbtv__jljq += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        llqns__ithah)))
    fjbtv__jljq += '  table_total = arr_info_list_to_table(info_list_total)\n'
    fjbtv__jljq += '  keep_i = 0\n'
    fjbtv__jljq += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for zekl__joakl in range(llqns__ithah):
        fjbtv__jljq += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(zekl__joakl, zekl__joakl, zekl__joakl))
    fjbtv__jljq += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(llqns__ithah))
    fjbtv__jljq += '  delete_table(out_table)\n'
    fjbtv__jljq += '  delete_table(table_total)\n'
    fjbtv__jljq += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(llqns__ithah)))
    ghf__scrn = {}
    exec(fjbtv__jljq, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, ghf__scrn)
    impl = ghf__scrn['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        rluo__pcfr = [array_to_info(data_arr)]
        fkd__usz = arr_info_list_to_table(rluo__pcfr)
        woqj__mfs = 0
        gpsfo__wbs = drop_duplicates_table(fkd__usz, parallel, 1, woqj__mfs,
            False, True)
        lifi__ogpfv = info_to_array(info_from_table(gpsfo__wbs, 0), data_arr)
        delete_table(gpsfo__wbs)
        delete_table(fkd__usz)
        return lifi__ogpfv
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    kcpn__fccnm = len(data.types)
    bcs__askjp = [('out' + str(i)) for i in range(kcpn__fccnm)]
    xca__cjl = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    nin__bcr = ['isna(data[{}], i)'.format(i) for i in xca__cjl]
    ymv__jexb = 'not ({})'.format(' or '.join(nin__bcr))
    if not is_overload_none(thresh):
        ymv__jexb = '(({}) <= ({}) - thresh)'.format(' + '.join(nin__bcr), 
            kcpn__fccnm - 1)
    elif how == 'all':
        ymv__jexb = 'not ({})'.format(' and '.join(nin__bcr))
    fjbtv__jljq = 'def _dropna_imp(data, how, thresh, subset):\n'
    fjbtv__jljq += '  old_len = len(data[0])\n'
    fjbtv__jljq += '  new_len = 0\n'
    fjbtv__jljq += '  for i in range(old_len):\n'
    fjbtv__jljq += '    if {}:\n'.format(ymv__jexb)
    fjbtv__jljq += '      new_len += 1\n'
    for i, out in enumerate(bcs__askjp):
        if isinstance(data[i], bodo.CategoricalArrayType):
            fjbtv__jljq += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            fjbtv__jljq += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    fjbtv__jljq += '  curr_ind = 0\n'
    fjbtv__jljq += '  for i in range(old_len):\n'
    fjbtv__jljq += '    if {}:\n'.format(ymv__jexb)
    for i in range(kcpn__fccnm):
        fjbtv__jljq += '      if isna(data[{}], i):\n'.format(i)
        fjbtv__jljq += '        setna({}, curr_ind)\n'.format(bcs__askjp[i])
        fjbtv__jljq += '      else:\n'
        fjbtv__jljq += '        {}[curr_ind] = data[{}][i]\n'.format(bcs__askjp
            [i], i)
    fjbtv__jljq += '      curr_ind += 1\n'
    fjbtv__jljq += '  return {}\n'.format(', '.join(bcs__askjp))
    ghf__scrn = {}
    zyt__rscq = {'t{}'.format(i): ztj__sgfm for i, ztj__sgfm in enumerate(
        data.types)}
    zyt__rscq.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(fjbtv__jljq, zyt__rscq, ghf__scrn)
    ymxmq__qztf = ghf__scrn['_dropna_imp']
    return ymxmq__qztf


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        qqu__atf = arr.dtype
        dnsva__tnn = qqu__atf.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            qeo__inzne = init_nested_counts(dnsva__tnn)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                qeo__inzne = add_nested_counts(qeo__inzne, val[ind])
            lifi__ogpfv = bodo.utils.utils.alloc_type(n, qqu__atf, qeo__inzne)
            for ofvy__ywjmz in range(n):
                if bodo.libs.array_kernels.isna(arr, ofvy__ywjmz):
                    setna(lifi__ogpfv, ofvy__ywjmz)
                    continue
                val = arr[ofvy__ywjmz]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(lifi__ogpfv, ofvy__ywjmz)
                    continue
                lifi__ogpfv[ofvy__ywjmz] = val[ind]
            return lifi__ogpfv
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    yynui__gghba = _to_readonly(arr_types.types[0])
    return all(isinstance(ztj__sgfm, CategoricalArrayType) and _to_readonly
        (ztj__sgfm) == yynui__gghba for ztj__sgfm in arr_types.types)


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
        flkv__oagrn = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            tnz__otq = 0
            hxlb__fjrc = []
            for A in arr_list:
                kaolf__cynzy = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                hxlb__fjrc.append(bodo.libs.array_item_arr_ext.get_data(A))
                tnz__otq += kaolf__cynzy
            wnaf__lhmsp = np.empty(tnz__otq + 1, offset_type)
            kkopj__rprk = bodo.libs.array_kernels.concat(hxlb__fjrc)
            eeep__yspa = np.empty(tnz__otq + 7 >> 3, np.uint8)
            ttdg__nlgd = 0
            aoey__lfttx = 0
            for A in arr_list:
                yjn__oais = bodo.libs.array_item_arr_ext.get_offsets(A)
                pcq__syxf = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                kaolf__cynzy = len(A)
                ydrbr__vurgd = yjn__oais[kaolf__cynzy]
                for i in range(kaolf__cynzy):
                    wnaf__lhmsp[i + ttdg__nlgd] = yjn__oais[i] + aoey__lfttx
                    itgr__afxy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        pcq__syxf, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(eeep__yspa, i +
                        ttdg__nlgd, itgr__afxy)
                ttdg__nlgd += kaolf__cynzy
                aoey__lfttx += ydrbr__vurgd
            wnaf__lhmsp[ttdg__nlgd] = aoey__lfttx
            lifi__ogpfv = bodo.libs.array_item_arr_ext.init_array_item_array(
                tnz__otq, kkopj__rprk, wnaf__lhmsp, eeep__yspa)
            return lifi__ogpfv
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        oheq__eoci = arr_list.dtype.names
        fjbtv__jljq = 'def struct_array_concat_impl(arr_list):\n'
        fjbtv__jljq += f'    n_all = 0\n'
        for i in range(len(oheq__eoci)):
            fjbtv__jljq += f'    concat_list{i} = []\n'
        fjbtv__jljq += '    for A in arr_list:\n'
        fjbtv__jljq += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(oheq__eoci)):
            fjbtv__jljq += f'        concat_list{i}.append(data_tuple[{i}])\n'
        fjbtv__jljq += '        n_all += len(A)\n'
        fjbtv__jljq += '    n_bytes = (n_all + 7) >> 3\n'
        fjbtv__jljq += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        fjbtv__jljq += '    curr_bit = 0\n'
        fjbtv__jljq += '    for A in arr_list:\n'
        fjbtv__jljq += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        fjbtv__jljq += '        for j in range(len(A)):\n'
        fjbtv__jljq += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        fjbtv__jljq += """            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)
"""
        fjbtv__jljq += '            curr_bit += 1\n'
        fjbtv__jljq += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        meiiz__adi = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(oheq__eoci))])
        fjbtv__jljq += f'        ({meiiz__adi},),\n'
        fjbtv__jljq += '        new_mask,\n'
        fjbtv__jljq += f'        {oheq__eoci},\n'
        fjbtv__jljq += '    )\n'
        ghf__scrn = {}
        exec(fjbtv__jljq, {'bodo': bodo, 'np': np}, ghf__scrn)
        return ghf__scrn['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            ekj__xapqd = 0
            for A in arr_list:
                ekj__xapqd += len(A)
            cpli__ejh = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(ekj__xapqd))
            ucs__blkm = 0
            for A in arr_list:
                for i in range(len(A)):
                    cpli__ejh._data[i + ucs__blkm] = A._data[i]
                    itgr__afxy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(cpli__ejh.
                        _null_bitmap, i + ucs__blkm, itgr__afxy)
                ucs__blkm += len(A)
            return cpli__ejh
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            ekj__xapqd = 0
            for A in arr_list:
                ekj__xapqd += len(A)
            cpli__ejh = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(ekj__xapqd))
            ucs__blkm = 0
            for A in arr_list:
                for i in range(len(A)):
                    cpli__ejh._days_data[i + ucs__blkm] = A._days_data[i]
                    cpli__ejh._seconds_data[i + ucs__blkm] = A._seconds_data[i]
                    cpli__ejh._microseconds_data[i + ucs__blkm
                        ] = A._microseconds_data[i]
                    itgr__afxy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(cpli__ejh.
                        _null_bitmap, i + ucs__blkm, itgr__afxy)
                ucs__blkm += len(A)
            return cpli__ejh
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        hrq__skpgc = arr_list.dtype.precision
        wax__owrcq = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            ekj__xapqd = 0
            for A in arr_list:
                ekj__xapqd += len(A)
            cpli__ejh = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                ekj__xapqd, hrq__skpgc, wax__owrcq)
            ucs__blkm = 0
            for A in arr_list:
                for i in range(len(A)):
                    cpli__ejh._data[i + ucs__blkm] = A._data[i]
                    itgr__afxy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(cpli__ejh.
                        _null_bitmap, i + ucs__blkm, itgr__afxy)
                ucs__blkm += len(A)
            return cpli__ejh
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        ztj__sgfm) for ztj__sgfm in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            xph__lgxu = arr_list.types[0]
        else:
            xph__lgxu = arr_list.dtype
        xph__lgxu = to_str_arr_if_dict_array(xph__lgxu)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            ylmtu__lpc = 0
            iglo__kmygp = 0
            for A in arr_list:
                arr = A
                ylmtu__lpc += len(arr)
                iglo__kmygp += bodo.libs.str_arr_ext.num_total_chars(arr)
            lifi__ogpfv = bodo.utils.utils.alloc_type(ylmtu__lpc, xph__lgxu,
                (iglo__kmygp,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(lifi__ogpfv, -1)
            rejc__podhn = 0
            lhvlz__phcv = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(lifi__ogpfv,
                    arr, rejc__podhn, lhvlz__phcv)
                rejc__podhn += len(arr)
                lhvlz__phcv += bodo.libs.str_arr_ext.num_total_chars(arr)
            return lifi__ogpfv
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(ztj__sgfm.dtype, types.Integer) for
        ztj__sgfm in arr_list.types) and any(isinstance(ztj__sgfm,
        IntegerArrayType) for ztj__sgfm in arr_list.types):

        def impl_int_arr_list(arr_list):
            ezc__gcdo = convert_to_nullable_tup(arr_list)
            hgr__mgj = []
            aah__isif = 0
            for A in ezc__gcdo:
                hgr__mgj.append(A._data)
                aah__isif += len(A)
            kkopj__rprk = bodo.libs.array_kernels.concat(hgr__mgj)
            bcnd__cxjo = aah__isif + 7 >> 3
            mjsp__mykmd = np.empty(bcnd__cxjo, np.uint8)
            cez__dmoqb = 0
            for A in ezc__gcdo:
                bjzi__lme = A._null_bitmap
                for ofvy__ywjmz in range(len(A)):
                    itgr__afxy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        bjzi__lme, ofvy__ywjmz)
                    bodo.libs.int_arr_ext.set_bit_to_arr(mjsp__mykmd,
                        cez__dmoqb, itgr__afxy)
                    cez__dmoqb += 1
            return bodo.libs.int_arr_ext.init_integer_array(kkopj__rprk,
                mjsp__mykmd)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(ztj__sgfm.dtype == types.bool_ for ztj__sgfm in
        arr_list.types) and any(ztj__sgfm == boolean_array for ztj__sgfm in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            ezc__gcdo = convert_to_nullable_tup(arr_list)
            hgr__mgj = []
            aah__isif = 0
            for A in ezc__gcdo:
                hgr__mgj.append(A._data)
                aah__isif += len(A)
            kkopj__rprk = bodo.libs.array_kernels.concat(hgr__mgj)
            bcnd__cxjo = aah__isif + 7 >> 3
            mjsp__mykmd = np.empty(bcnd__cxjo, np.uint8)
            cez__dmoqb = 0
            for A in ezc__gcdo:
                bjzi__lme = A._null_bitmap
                for ofvy__ywjmz in range(len(A)):
                    itgr__afxy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        bjzi__lme, ofvy__ywjmz)
                    bodo.libs.int_arr_ext.set_bit_to_arr(mjsp__mykmd,
                        cez__dmoqb, itgr__afxy)
                    cez__dmoqb += 1
            return bodo.libs.bool_arr_ext.init_bool_array(kkopj__rprk,
                mjsp__mykmd)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            jum__jth = []
            for A in arr_list:
                jum__jth.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                jum__jth), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        rcft__znmns = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        fjbtv__jljq = 'def impl(arr_list):\n'
        fjbtv__jljq += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({rcft__znmns},)), arr_list[0].dtype)
"""
        xyya__icn = {}
        exec(fjbtv__jljq, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, xyya__icn)
        return xyya__icn['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            aah__isif = 0
            for A in arr_list:
                aah__isif += len(A)
            lifi__ogpfv = np.empty(aah__isif, dtype)
            hzvuh__mngm = 0
            for A in arr_list:
                n = len(A)
                lifi__ogpfv[hzvuh__mngm:hzvuh__mngm + n] = A
                hzvuh__mngm += n
            return lifi__ogpfv
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(ztj__sgfm,
        (types.Array, IntegerArrayType)) and isinstance(ztj__sgfm.dtype,
        types.Integer) for ztj__sgfm in arr_list.types) and any(isinstance(
        ztj__sgfm, types.Array) and isinstance(ztj__sgfm.dtype, types.Float
        ) for ztj__sgfm in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            xztfr__njugp = []
            for A in arr_list:
                xztfr__njugp.append(A._data)
            bvaj__ogmlq = bodo.libs.array_kernels.concat(xztfr__njugp)
            mkng__iuia = bodo.libs.map_arr_ext.init_map_arr(bvaj__ogmlq)
            return mkng__iuia
        return impl_map_arr_list
    for ddzm__and in arr_list:
        if not isinstance(ddzm__and, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(ztj__sgfm.astype(np.float64) for ztj__sgfm in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    llqns__ithah = len(arr_tup.types)
    fjbtv__jljq = 'def f(arr_tup):\n'
    fjbtv__jljq += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        llqns__ithah)), ',' if llqns__ithah == 1 else '')
    ghf__scrn = {}
    exec(fjbtv__jljq, {'np': np}, ghf__scrn)
    qwyem__lfn = ghf__scrn['f']
    return qwyem__lfn


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    llqns__ithah = len(arr_tup.types)
    tbl__klvrk = find_common_np_dtype(arr_tup.types)
    dnsva__tnn = None
    uydvi__lxic = ''
    if isinstance(tbl__klvrk, types.Integer):
        dnsva__tnn = bodo.libs.int_arr_ext.IntDtype(tbl__klvrk)
        uydvi__lxic = '.astype(out_dtype, False)'
    fjbtv__jljq = 'def f(arr_tup):\n'
    fjbtv__jljq += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, uydvi__lxic) for i in range(llqns__ithah)), ',' if 
        llqns__ithah == 1 else '')
    ghf__scrn = {}
    exec(fjbtv__jljq, {'bodo': bodo, 'out_dtype': dnsva__tnn}, ghf__scrn)
    thz__heu = ghf__scrn['f']
    return thz__heu


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, hvsg__fst = build_set_seen_na(A)
        return len(s) + int(not dropna and hvsg__fst)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        ncm__kmgxt = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        htg__rgtzz = len(ncm__kmgxt)
        return bodo.libs.distributed_api.dist_reduce(htg__rgtzz, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([ftas__evb for ftas__evb in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        hgu__gnps = np.finfo(A.dtype(1).dtype).max
    else:
        hgu__gnps = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        lifi__ogpfv = np.empty(n, A.dtype)
        fhztj__xsd = hgu__gnps
        for i in range(n):
            fhztj__xsd = min(fhztj__xsd, A[i])
            lifi__ogpfv[i] = fhztj__xsd
        return lifi__ogpfv
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        hgu__gnps = np.finfo(A.dtype(1).dtype).min
    else:
        hgu__gnps = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        lifi__ogpfv = np.empty(n, A.dtype)
        fhztj__xsd = hgu__gnps
        for i in range(n):
            fhztj__xsd = max(fhztj__xsd, A[i])
            lifi__ogpfv[i] = fhztj__xsd
        return lifi__ogpfv
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        gxeui__zclor = arr_info_list_to_table([array_to_info(A)])
        veesj__edkr = 1
        woqj__mfs = 0
        gpsfo__wbs = drop_duplicates_table(gxeui__zclor, parallel,
            veesj__edkr, woqj__mfs, dropna, True)
        lifi__ogpfv = info_to_array(info_from_table(gpsfo__wbs, 0), A)
        delete_table(gxeui__zclor)
        delete_table(gpsfo__wbs)
        return lifi__ogpfv
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    flkv__oagrn = bodo.utils.typing.to_nullable_type(arr.dtype)
    way__ysmqk = index_arr
    wxel__yewxj = way__ysmqk.dtype

    def impl(arr, index_arr):
        n = len(arr)
        qeo__inzne = init_nested_counts(flkv__oagrn)
        awmmr__zsus = init_nested_counts(wxel__yewxj)
        for i in range(n):
            xdvva__cgsa = index_arr[i]
            if isna(arr, i):
                qeo__inzne = (qeo__inzne[0] + 1,) + qeo__inzne[1:]
                awmmr__zsus = add_nested_counts(awmmr__zsus, xdvva__cgsa)
                continue
            zac__qoamo = arr[i]
            if len(zac__qoamo) == 0:
                qeo__inzne = (qeo__inzne[0] + 1,) + qeo__inzne[1:]
                awmmr__zsus = add_nested_counts(awmmr__zsus, xdvva__cgsa)
                continue
            qeo__inzne = add_nested_counts(qeo__inzne, zac__qoamo)
            for adw__msk in range(len(zac__qoamo)):
                awmmr__zsus = add_nested_counts(awmmr__zsus, xdvva__cgsa)
        lifi__ogpfv = bodo.utils.utils.alloc_type(qeo__inzne[0],
            flkv__oagrn, qeo__inzne[1:])
        sycpz__kpzon = bodo.utils.utils.alloc_type(qeo__inzne[0],
            way__ysmqk, awmmr__zsus)
        aoey__lfttx = 0
        for i in range(n):
            if isna(arr, i):
                setna(lifi__ogpfv, aoey__lfttx)
                sycpz__kpzon[aoey__lfttx] = index_arr[i]
                aoey__lfttx += 1
                continue
            zac__qoamo = arr[i]
            ydrbr__vurgd = len(zac__qoamo)
            if ydrbr__vurgd == 0:
                setna(lifi__ogpfv, aoey__lfttx)
                sycpz__kpzon[aoey__lfttx] = index_arr[i]
                aoey__lfttx += 1
                continue
            lifi__ogpfv[aoey__lfttx:aoey__lfttx + ydrbr__vurgd] = zac__qoamo
            sycpz__kpzon[aoey__lfttx:aoey__lfttx + ydrbr__vurgd] = index_arr[i]
            aoey__lfttx += ydrbr__vurgd
        return lifi__ogpfv, sycpz__kpzon
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    flkv__oagrn = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        qeo__inzne = init_nested_counts(flkv__oagrn)
        for i in range(n):
            if isna(arr, i):
                qeo__inzne = (qeo__inzne[0] + 1,) + qeo__inzne[1:]
                zneu__zjpnn = 1
            else:
                zac__qoamo = arr[i]
                vyyy__yfjr = len(zac__qoamo)
                if vyyy__yfjr == 0:
                    qeo__inzne = (qeo__inzne[0] + 1,) + qeo__inzne[1:]
                    zneu__zjpnn = 1
                    continue
                else:
                    qeo__inzne = add_nested_counts(qeo__inzne, zac__qoamo)
                    zneu__zjpnn = vyyy__yfjr
            if counts[i] != zneu__zjpnn:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        lifi__ogpfv = bodo.utils.utils.alloc_type(qeo__inzne[0],
            flkv__oagrn, qeo__inzne[1:])
        aoey__lfttx = 0
        for i in range(n):
            if isna(arr, i):
                setna(lifi__ogpfv, aoey__lfttx)
                aoey__lfttx += 1
                continue
            zac__qoamo = arr[i]
            ydrbr__vurgd = len(zac__qoamo)
            if ydrbr__vurgd == 0:
                setna(lifi__ogpfv, aoey__lfttx)
                aoey__lfttx += 1
                continue
            lifi__ogpfv[aoey__lfttx:aoey__lfttx + ydrbr__vurgd] = zac__qoamo
            aoey__lfttx += ydrbr__vurgd
        return lifi__ogpfv
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(vmgft__iwuu) for vmgft__iwuu in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        krl__xqr = 'np.empty(n, np.int64)'
        fsky__trxr = 'out_arr[i] = 1'
        vwzhe__inzeg = 'max(len(arr[i]), 1)'
    else:
        krl__xqr = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        fsky__trxr = 'bodo.libs.array_kernels.setna(out_arr, i)'
        vwzhe__inzeg = 'len(arr[i])'
    fjbtv__jljq = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {krl__xqr}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {fsky__trxr}
        else:
            out_arr[i] = {vwzhe__inzeg}
    return out_arr
    """
    ghf__scrn = {}
    exec(fjbtv__jljq, {'bodo': bodo, 'numba': numba, 'np': np}, ghf__scrn)
    impl = ghf__scrn['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    way__ysmqk = index_arr
    wxel__yewxj = way__ysmqk.dtype

    def impl(arr, pat, n, index_arr):
        nnjo__rsu = pat is not None and len(pat) > 1
        if nnjo__rsu:
            lpv__jzg = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        omcnd__nkuhk = len(arr)
        ylmtu__lpc = 0
        iglo__kmygp = 0
        awmmr__zsus = init_nested_counts(wxel__yewxj)
        for i in range(omcnd__nkuhk):
            xdvva__cgsa = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                ylmtu__lpc += 1
                awmmr__zsus = add_nested_counts(awmmr__zsus, xdvva__cgsa)
                continue
            if nnjo__rsu:
                ugba__rikj = lpv__jzg.split(arr[i], maxsplit=n)
            else:
                ugba__rikj = arr[i].split(pat, n)
            ylmtu__lpc += len(ugba__rikj)
            for s in ugba__rikj:
                awmmr__zsus = add_nested_counts(awmmr__zsus, xdvva__cgsa)
                iglo__kmygp += bodo.libs.str_arr_ext.get_utf8_size(s)
        lifi__ogpfv = bodo.libs.str_arr_ext.pre_alloc_string_array(ylmtu__lpc,
            iglo__kmygp)
        sycpz__kpzon = bodo.utils.utils.alloc_type(ylmtu__lpc, way__ysmqk,
            awmmr__zsus)
        nsk__ajrha = 0
        for ofvy__ywjmz in range(omcnd__nkuhk):
            if isna(arr, ofvy__ywjmz):
                lifi__ogpfv[nsk__ajrha] = ''
                bodo.libs.array_kernels.setna(lifi__ogpfv, nsk__ajrha)
                sycpz__kpzon[nsk__ajrha] = index_arr[ofvy__ywjmz]
                nsk__ajrha += 1
                continue
            if nnjo__rsu:
                ugba__rikj = lpv__jzg.split(arr[ofvy__ywjmz], maxsplit=n)
            else:
                ugba__rikj = arr[ofvy__ywjmz].split(pat, n)
            vffy__sip = len(ugba__rikj)
            lifi__ogpfv[nsk__ajrha:nsk__ajrha + vffy__sip] = ugba__rikj
            sycpz__kpzon[nsk__ajrha:nsk__ajrha + vffy__sip] = index_arr[
                ofvy__ywjmz]
            nsk__ajrha += vffy__sip
        return lifi__ogpfv, sycpz__kpzon
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
            lifi__ogpfv = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                lifi__ogpfv[i] = np.nan
            return lifi__ogpfv
        return impl_float
    pdjh__ihg = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        lifi__ogpfv = bodo.utils.utils.alloc_type(n, pdjh__ihg, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(lifi__ogpfv, i)
        return lifi__ogpfv
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
    rtdno__fso = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            lifi__ogpfv = bodo.utils.utils.alloc_type(new_len, rtdno__fso)
            bodo.libs.str_arr_ext.str_copy_ptr(lifi__ogpfv.ctypes, 0, A.
                ctypes, old_size)
            return lifi__ogpfv
        return impl_char

    def impl(A, old_size, new_len):
        lifi__ogpfv = bodo.utils.utils.alloc_type(new_len, rtdno__fso, (-1,))
        lifi__ogpfv[:old_size] = A[:old_size]
        return lifi__ogpfv
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    leyr__znx = math.ceil((stop - start) / step)
    return int(max(leyr__znx, 0))


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
    if any(isinstance(ftas__evb, types.Complex) for ftas__evb in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            meba__gxgnk = (stop - start) / step
            leyr__znx = math.ceil(meba__gxgnk.real)
            foz__inq = math.ceil(meba__gxgnk.imag)
            gmi__dcg = int(max(min(foz__inq, leyr__znx), 0))
            arr = np.empty(gmi__dcg, dtype)
            for i in numba.parfors.parfor.internal_prange(gmi__dcg):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            gmi__dcg = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(gmi__dcg, dtype)
            for i in numba.parfors.parfor.internal_prange(gmi__dcg):
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
        ssfy__wcd = arr,
        if not inplace:
            ssfy__wcd = arr.copy(),
        scss__nuwde = bodo.libs.str_arr_ext.to_list_if_immutable_arr(ssfy__wcd)
        mqg__see = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(scss__nuwde, 0, n, mqg__see)
        if not ascending:
            bodo.libs.timsort.reverseRange(scss__nuwde, 0, n, mqg__see)
        bodo.libs.str_arr_ext.cp_str_list_to_array(ssfy__wcd, scss__nuwde)
        return ssfy__wcd[0]
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
        mkng__iuia = []
        for i in range(n):
            if A[i]:
                mkng__iuia.append(i + offset)
        return np.array(mkng__iuia, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    rtdno__fso = element_type(A)
    if rtdno__fso == types.unicode_type:
        null_value = '""'
    elif rtdno__fso == types.bool_:
        null_value = 'False'
    elif rtdno__fso == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif rtdno__fso == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    nsk__ajrha = 'i'
    nqb__bac = False
    baag__ckdm = get_overload_const_str(method)
    if baag__ckdm in ('ffill', 'pad'):
        qabjq__npsr = 'n'
        send_right = True
    elif baag__ckdm in ('backfill', 'bfill'):
        qabjq__npsr = 'n-1, -1, -1'
        send_right = False
        if rtdno__fso == types.unicode_type:
            nsk__ajrha = '(n - 1) - i'
            nqb__bac = True
    fjbtv__jljq = 'def impl(A, method, parallel=False):\n'
    fjbtv__jljq += '  A = decode_if_dict_array(A)\n'
    fjbtv__jljq += '  has_last_value = False\n'
    fjbtv__jljq += f'  last_value = {null_value}\n'
    fjbtv__jljq += '  if parallel:\n'
    fjbtv__jljq += '    rank = bodo.libs.distributed_api.get_rank()\n'
    fjbtv__jljq += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    fjbtv__jljq += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    fjbtv__jljq += '  n = len(A)\n'
    fjbtv__jljq += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    fjbtv__jljq += f'  for i in range({qabjq__npsr}):\n'
    fjbtv__jljq += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    fjbtv__jljq += (
        f'      bodo.libs.array_kernels.setna(out_arr, {nsk__ajrha})\n')
    fjbtv__jljq += '      continue\n'
    fjbtv__jljq += '    s = A[i]\n'
    fjbtv__jljq += '    if bodo.libs.array_kernels.isna(A, i):\n'
    fjbtv__jljq += '      s = last_value\n'
    fjbtv__jljq += f'    out_arr[{nsk__ajrha}] = s\n'
    fjbtv__jljq += '    last_value = s\n'
    fjbtv__jljq += '    has_last_value = True\n'
    if nqb__bac:
        fjbtv__jljq += '  return out_arr[::-1]\n'
    else:
        fjbtv__jljq += '  return out_arr\n'
    nor__abff = {}
    exec(fjbtv__jljq, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, nor__abff)
    impl = nor__abff['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        wwkg__jioxi = 0
        ovitw__pcet = n_pes - 1
        wtwob__uvmyn = np.int32(rank + 1)
        mwd__ihruo = np.int32(rank - 1)
        jdd__qpiy = len(in_arr) - 1
        zqre__lboup = -1
        zthpm__lkj = -1
    else:
        wwkg__jioxi = n_pes - 1
        ovitw__pcet = 0
        wtwob__uvmyn = np.int32(rank - 1)
        mwd__ihruo = np.int32(rank + 1)
        jdd__qpiy = 0
        zqre__lboup = len(in_arr)
        zthpm__lkj = 1
    hjpru__geq = np.int32(bodo.hiframes.rolling.comm_border_tag)
    mrx__nosdb = np.empty(1, dtype=np.bool_)
    sofhx__tbnpl = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    rrxr__nzoeo = np.empty(1, dtype=np.bool_)
    xlvw__heio = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    kuybc__qmu = False
    ukdmg__xcyli = null_value
    for i in range(jdd__qpiy, zqre__lboup, zthpm__lkj):
        if not isna(in_arr, i):
            kuybc__qmu = True
            ukdmg__xcyli = in_arr[i]
            break
    if rank != wwkg__jioxi:
        ocecc__birba = bodo.libs.distributed_api.irecv(mrx__nosdb, 1,
            mwd__ihruo, hjpru__geq, True)
        bodo.libs.distributed_api.wait(ocecc__birba, True)
        rso__okfp = bodo.libs.distributed_api.irecv(sofhx__tbnpl, 1,
            mwd__ihruo, hjpru__geq, True)
        bodo.libs.distributed_api.wait(rso__okfp, True)
        pva__xtp = mrx__nosdb[0]
        lrw__uxd = sofhx__tbnpl[0]
    else:
        pva__xtp = False
        lrw__uxd = null_value
    if kuybc__qmu:
        rrxr__nzoeo[0] = kuybc__qmu
        xlvw__heio[0] = ukdmg__xcyli
    else:
        rrxr__nzoeo[0] = pva__xtp
        xlvw__heio[0] = lrw__uxd
    if rank != ovitw__pcet:
        axmzk__cis = bodo.libs.distributed_api.isend(rrxr__nzoeo, 1,
            wtwob__uvmyn, hjpru__geq, True)
        coa__xhyov = bodo.libs.distributed_api.isend(xlvw__heio, 1,
            wtwob__uvmyn, hjpru__geq, True)
    return pva__xtp, lrw__uxd


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    kkl__heou = {'axis': axis, 'kind': kind, 'order': order}
    nvmcq__svh = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', kkl__heou, nvmcq__svh, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    rtdno__fso = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            omcnd__nkuhk = len(A)
            lifi__ogpfv = bodo.utils.utils.alloc_type(omcnd__nkuhk *
                repeats, rtdno__fso, (-1,))
            for i in range(omcnd__nkuhk):
                nsk__ajrha = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for ofvy__ywjmz in range(repeats):
                        bodo.libs.array_kernels.setna(lifi__ogpfv, 
                            nsk__ajrha + ofvy__ywjmz)
                else:
                    lifi__ogpfv[nsk__ajrha:nsk__ajrha + repeats] = A[i]
            return lifi__ogpfv
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        omcnd__nkuhk = len(A)
        lifi__ogpfv = bodo.utils.utils.alloc_type(repeats.sum(), rtdno__fso,
            (-1,))
        nsk__ajrha = 0
        for i in range(omcnd__nkuhk):
            kwuf__wrtlg = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for ofvy__ywjmz in range(kwuf__wrtlg):
                    bodo.libs.array_kernels.setna(lifi__ogpfv, nsk__ajrha +
                        ofvy__ywjmz)
            else:
                lifi__ogpfv[nsk__ajrha:nsk__ajrha + kwuf__wrtlg] = A[i]
            nsk__ajrha += kwuf__wrtlg
        return lifi__ogpfv
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
        ijyy__moa = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(ijyy__moa, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        swar__fmj = bodo.libs.array_kernels.concat([A1, A2])
        vydd__kgetu = bodo.libs.array_kernels.unique(swar__fmj)
        return pd.Series(vydd__kgetu).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    kkl__heou = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    nvmcq__svh = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', kkl__heou, nvmcq__svh, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        usip__mtweh = bodo.libs.array_kernels.unique(A1)
        xwt__eid = bodo.libs.array_kernels.unique(A2)
        swar__fmj = bodo.libs.array_kernels.concat([usip__mtweh, xwt__eid])
        ebh__bxjz = pd.Series(swar__fmj).sort_values().values
        return slice_array_intersect1d(ebh__bxjz)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    hkroe__ndeta = arr[1:] == arr[:-1]
    return arr[:-1][hkroe__ndeta]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    kkl__heou = {'assume_unique': assume_unique}
    nvmcq__svh = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', kkl__heou, nvmcq__svh, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        usip__mtweh = bodo.libs.array_kernels.unique(A1)
        xwt__eid = bodo.libs.array_kernels.unique(A2)
        hkroe__ndeta = calculate_mask_setdiff1d(usip__mtweh, xwt__eid)
        return pd.Series(usip__mtweh[hkroe__ndeta]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    hkroe__ndeta = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        hkroe__ndeta &= A1 != A2[i]
    return hkroe__ndeta


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    kkl__heou = {'retstep': retstep, 'axis': axis}
    nvmcq__svh = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', kkl__heou, nvmcq__svh, 'numpy')
    atqcm__ttluv = False
    if is_overload_none(dtype):
        rtdno__fso = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            atqcm__ttluv = True
        rtdno__fso = numba.np.numpy_support.as_dtype(dtype).type
    if atqcm__ttluv:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            dxvfx__yng = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            lifi__ogpfv = np.empty(num, rtdno__fso)
            for i in numba.parfors.parfor.internal_prange(num):
                lifi__ogpfv[i] = rtdno__fso(np.floor(start + i * dxvfx__yng))
            return lifi__ogpfv
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            dxvfx__yng = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            lifi__ogpfv = np.empty(num, rtdno__fso)
            for i in numba.parfors.parfor.internal_prange(num):
                lifi__ogpfv[i] = rtdno__fso(start + i * dxvfx__yng)
            return lifi__ogpfv
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
        llqns__ithah = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                llqns__ithah += A[i] == val
        return llqns__ithah > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    kkl__heou = {'axis': axis, 'out': out, 'keepdims': keepdims}
    nvmcq__svh = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', kkl__heou, nvmcq__svh, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        llqns__ithah = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                llqns__ithah += int(bool(A[i]))
        return llqns__ithah > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    kkl__heou = {'axis': axis, 'out': out, 'keepdims': keepdims}
    nvmcq__svh = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', kkl__heou, nvmcq__svh, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        llqns__ithah = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                llqns__ithah += int(bool(A[i]))
        return llqns__ithah == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    kkl__heou = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    nvmcq__svh = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', kkl__heou, nvmcq__svh, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        fvq__lki = np.promote_types(numba.np.numpy_support.as_dtype(A.dtype
            ), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            lifi__ogpfv = np.empty(n, fvq__lki)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(lifi__ogpfv, i)
                    continue
                lifi__ogpfv[i] = np_cbrt_scalar(A[i], fvq__lki)
            return lifi__ogpfv
        return impl_arr
    fvq__lki = np.promote_types(numba.np.numpy_support.as_dtype(A), numba.
        np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, fvq__lki)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    izcgc__wuas = x < 0
    if izcgc__wuas:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if izcgc__wuas:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    sxa__ljmf = isinstance(tup, (types.BaseTuple, types.List))
    atq__sprkl = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for ddzm__and in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ddzm__and
                , 'numpy.hstack()')
            sxa__ljmf = sxa__ljmf and bodo.utils.utils.is_array_typ(ddzm__and,
                False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        sxa__ljmf = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif atq__sprkl:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        bmqs__qxps = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for ddzm__and in bmqs__qxps.types:
            atq__sprkl = atq__sprkl and bodo.utils.utils.is_array_typ(ddzm__and
                , False)
    if not (sxa__ljmf or atq__sprkl):
        return
    if atq__sprkl:

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
    kkl__heou = {'check_valid': check_valid, 'tol': tol}
    nvmcq__svh = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', kkl__heou,
        nvmcq__svh, 'numpy')
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
        anni__ozin = mean.shape[0]
        rrgtj__zqdg = size, anni__ozin
        dhnu__vhcks = np.random.standard_normal(rrgtj__zqdg)
        cov = cov.astype(np.float64)
        tgs__dsfv, s, eia__jeuc = np.linalg.svd(cov)
        res = np.dot(dhnu__vhcks, np.sqrt(s).reshape(anni__ozin, 1) * eia__jeuc
            )
        szuj__flqaf = res + mean
        return szuj__flqaf
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
            rmy__kisjj = bodo.hiframes.series_kernels._get_type_max_value(arr)
            zvrl__dvf = typing.builtins.IndexValue(-1, rmy__kisjj)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                acb__cual = typing.builtins.IndexValue(i, arr[i])
                zvrl__dvf = min(zvrl__dvf, acb__cual)
            return zvrl__dvf.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        cfxee__gnzq = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            smpq__gnaaq = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            rmy__kisjj = cfxee__gnzq(len(arr.dtype.categories) + 1)
            zvrl__dvf = typing.builtins.IndexValue(-1, rmy__kisjj)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                acb__cual = typing.builtins.IndexValue(i, smpq__gnaaq[i])
                zvrl__dvf = min(zvrl__dvf, acb__cual)
            return zvrl__dvf.index
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
            rmy__kisjj = bodo.hiframes.series_kernels._get_type_min_value(arr)
            zvrl__dvf = typing.builtins.IndexValue(-1, rmy__kisjj)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                acb__cual = typing.builtins.IndexValue(i, arr[i])
                zvrl__dvf = max(zvrl__dvf, acb__cual)
            return zvrl__dvf.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        cfxee__gnzq = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            smpq__gnaaq = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            rmy__kisjj = cfxee__gnzq(-1)
            zvrl__dvf = typing.builtins.IndexValue(-1, rmy__kisjj)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                acb__cual = typing.builtins.IndexValue(i, smpq__gnaaq[i])
                zvrl__dvf = max(zvrl__dvf, acb__cual)
            return zvrl__dvf.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
