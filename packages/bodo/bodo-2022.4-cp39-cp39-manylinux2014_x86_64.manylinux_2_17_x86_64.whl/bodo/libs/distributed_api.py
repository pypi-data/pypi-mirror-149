import atexit
import datetime
import operator
import sys
import time
import warnings
from collections import defaultdict
from decimal import Decimal
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir_utils, types
from numba.core.typing import signature
from numba.core.typing.builtins import IndexValueType
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, models, overload, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdist
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, set_bit_to_arr
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, num_total_chars, pre_alloc_string_array, set_bit_to, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, BodoWarning, decode_if_dict_array, is_overload_false, is_overload_none, is_str_arr_type
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, empty_like_type, numba_to_c_type
ll.add_symbol('dist_get_time', hdist.dist_get_time)
ll.add_symbol('get_time', hdist.get_time)
ll.add_symbol('dist_reduce', hdist.dist_reduce)
ll.add_symbol('dist_arr_reduce', hdist.dist_arr_reduce)
ll.add_symbol('dist_exscan', hdist.dist_exscan)
ll.add_symbol('dist_irecv', hdist.dist_irecv)
ll.add_symbol('dist_isend', hdist.dist_isend)
ll.add_symbol('dist_wait', hdist.dist_wait)
ll.add_symbol('dist_get_item_pointer', hdist.dist_get_item_pointer)
ll.add_symbol('get_dummy_ptr', hdist.get_dummy_ptr)
ll.add_symbol('allgather', hdist.allgather)
ll.add_symbol('comm_req_alloc', hdist.comm_req_alloc)
ll.add_symbol('comm_req_dealloc', hdist.comm_req_dealloc)
ll.add_symbol('req_array_setitem', hdist.req_array_setitem)
ll.add_symbol('dist_waitall', hdist.dist_waitall)
ll.add_symbol('oneD_reshape_shuffle', hdist.oneD_reshape_shuffle)
ll.add_symbol('permutation_int', hdist.permutation_int)
ll.add_symbol('permutation_array_index', hdist.permutation_array_index)
ll.add_symbol('c_get_rank', hdist.dist_get_rank)
ll.add_symbol('c_get_size', hdist.dist_get_size)
ll.add_symbol('c_barrier', hdist.barrier)
ll.add_symbol('c_alltoall', hdist.c_alltoall)
ll.add_symbol('c_gather_scalar', hdist.c_gather_scalar)
ll.add_symbol('c_gatherv', hdist.c_gatherv)
ll.add_symbol('c_scatterv', hdist.c_scatterv)
ll.add_symbol('c_allgatherv', hdist.c_allgatherv)
ll.add_symbol('c_bcast', hdist.c_bcast)
ll.add_symbol('c_recv', hdist.dist_recv)
ll.add_symbol('c_send', hdist.dist_send)
mpi_req_numba_type = getattr(types, 'int' + str(8 * hdist.mpi_req_num_bytes))
MPI_ROOT = 0
ANY_SOURCE = np.int32(hdist.ANY_SOURCE)


class Reduce_Type(Enum):
    Sum = 0
    Prod = 1
    Min = 2
    Max = 3
    Argmin = 4
    Argmax = 5
    Or = 6
    Concat = 7
    No_Op = 8


_get_rank = types.ExternalFunction('c_get_rank', types.int32())
_get_size = types.ExternalFunction('c_get_size', types.int32())
_barrier = types.ExternalFunction('c_barrier', types.int32())


@numba.njit
def get_rank():
    return _get_rank()


@numba.njit
def get_size():
    return _get_size()


@numba.njit
def barrier():
    _barrier()


_get_time = types.ExternalFunction('get_time', types.float64())
dist_time = types.ExternalFunction('dist_get_time', types.float64())


@overload(time.time, no_unliteral=True)
def overload_time_time():
    return lambda : _get_time()


@numba.generated_jit(nopython=True)
def get_type_enum(arr):
    arr = arr.instance_type if isinstance(arr, types.TypeRef) else arr
    dtype = arr.dtype
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = bodo.hiframes.pd_categorical_ext.get_categories_int_type(dtype)
    typ_val = numba_to_c_type(dtype)
    return lambda arr: np.int32(typ_val)


INT_MAX = np.iinfo(np.int32).max
_send = types.ExternalFunction('c_send', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def send(val, rank, tag):
    send_arr = np.full(1, val)
    fgs__kclbr = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, fgs__kclbr, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    fgs__kclbr = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, fgs__kclbr, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            fgs__kclbr = get_type_enum(arr)
            return _isend(arr.ctypes, size, fgs__kclbr, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        fgs__kclbr = np.int32(numba_to_c_type(arr.dtype))
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            pssg__niht = size + 7 >> 3
            krwr__bozfy = _isend(arr._data.ctypes, size, fgs__kclbr, pe,
                tag, cond)
            ptiom__kho = _isend(arr._null_bitmap.ctypes, pssg__niht,
                nvwpo__gvshs, pe, tag, cond)
            return krwr__bozfy, ptiom__kho
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        bow__uqi = np.int32(numba_to_c_type(offset_type))
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            vuw__fsia = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(vuw__fsia, pe, tag - 1)
            pssg__niht = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                bow__uqi, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), vuw__fsia,
                nvwpo__gvshs, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                pssg__niht, nvwpo__gvshs, pe, tag)
            return None
        return impl_str_arr
    typ_enum = numba_to_c_type(types.uint8)

    def impl_voidptr(arr, size, pe, tag, cond=True):
        return _isend(arr, size, typ_enum, pe, tag, cond)
    return impl_voidptr


_irecv = types.ExternalFunction('dist_irecv', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def irecv(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            fgs__kclbr = get_type_enum(arr)
            return _irecv(arr.ctypes, size, fgs__kclbr, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        fgs__kclbr = np.int32(numba_to_c_type(arr.dtype))
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            pssg__niht = size + 7 >> 3
            krwr__bozfy = _irecv(arr._data.ctypes, size, fgs__kclbr, pe,
                tag, cond)
            ptiom__kho = _irecv(arr._null_bitmap.ctypes, pssg__niht,
                nvwpo__gvshs, pe, tag, cond)
            return krwr__bozfy, ptiom__kho
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        bow__uqi = np.int32(numba_to_c_type(offset_type))
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            bhrm__qrch = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            bhrm__qrch = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        siu__xdug = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {bhrm__qrch}(size, n_chars)
            bodo.libs.str_arr_ext.move_str_binary_arr_payload(arr, new_arr)

            n_bytes = (size + 7) >> 3
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_offset_ptr(arr),
                size + 1,
                offset_typ_enum,
                pe,
                tag,
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_data_ptr(arr), n_chars, char_typ_enum, pe, tag
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                n_bytes,
                char_typ_enum,
                pe,
                tag,
            )
            return None"""
        ppv__qtmn = dict()
        exec(siu__xdug, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            bow__uqi, 'char_typ_enum': nvwpo__gvshs}, ppv__qtmn)
        impl = ppv__qtmn['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    fgs__kclbr = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), fgs__kclbr)


@numba.generated_jit(nopython=True)
def gather_scalar(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    data = types.unliteral(data)
    typ_val = numba_to_c_type(data)
    dtype = data

    def gather_scalar_impl(data, allgather=False, warn_if_rep=True, root=
        MPI_ROOT):
        n_pes = bodo.libs.distributed_api.get_size()
        rank = bodo.libs.distributed_api.get_rank()
        send = np.full(1, data, dtype)
        odljg__ezfef = n_pes if rank == root or allgather else 0
        mxh__hkfsg = np.empty(odljg__ezfef, dtype)
        c_gather_scalar(send.ctypes, mxh__hkfsg.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return mxh__hkfsg
    return gather_scalar_impl


c_gather_scalar = types.ExternalFunction('c_gather_scalar', types.void(
    types.voidptr, types.voidptr, types.int32, types.bool_, types.int32))
c_gatherv = types.ExternalFunction('c_gatherv', types.void(types.voidptr,
    types.int32, types.voidptr, types.voidptr, types.voidptr, types.int32,
    types.bool_, types.int32))
c_scatterv = types.ExternalFunction('c_scatterv', types.void(types.voidptr,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.int32))


@intrinsic
def value_to_ptr(typingctx, val_tp=None):

    def codegen(context, builder, sig, args):
        ifv__pwlq = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], ifv__pwlq)
        return builder.bitcast(ifv__pwlq, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        ifv__pwlq = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(ifv__pwlq)
    return val_tp(ptr_tp, val_tp), codegen


_dist_reduce = types.ExternalFunction('dist_reduce', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))
_dist_arr_reduce = types.ExternalFunction('dist_arr_reduce', types.void(
    types.voidptr, types.int64, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_reduce(value, reduce_op):
    if isinstance(value, types.Array):
        typ_enum = np.int32(numba_to_c_type(value.dtype))

        def impl_arr(value, reduce_op):
            A = np.ascontiguousarray(value)
            _dist_arr_reduce(A.ctypes, A.size, reduce_op, typ_enum)
            return A
        return impl_arr
    dif__igcu = types.unliteral(value)
    if isinstance(dif__igcu, IndexValueType):
        dif__igcu = dif__igcu.val_typ
        izxx__jnget = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            izxx__jnget.append(types.int64)
            izxx__jnget.append(bodo.datetime64ns)
            izxx__jnget.append(bodo.timedelta64ns)
            izxx__jnget.append(bodo.datetime_date_type)
        if dif__igcu not in izxx__jnget:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(dif__igcu))
    typ_enum = np.int32(numba_to_c_type(dif__igcu))

    def impl(value, reduce_op):
        ipf__xwua = value_to_ptr(value)
        ihb__xwuma = value_to_ptr(value)
        _dist_reduce(ipf__xwua, ihb__xwuma, reduce_op, typ_enum)
        return load_val_ptr(ihb__xwuma, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    dif__igcu = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(dif__igcu))
    xebxg__rmn = dif__igcu(0)

    def impl(value, reduce_op):
        ipf__xwua = value_to_ptr(value)
        ihb__xwuma = value_to_ptr(xebxg__rmn)
        _dist_exscan(ipf__xwua, ihb__xwuma, reduce_op, typ_enum)
        return load_val_ptr(ihb__xwuma, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    bxd__fozz = 0
    ndw__vkf = 0
    for i in range(len(recv_counts)):
        cvnb__fnrw = recv_counts[i]
        pssg__niht = recv_counts_nulls[i]
        nje__hcaf = tmp_null_bytes[bxd__fozz:bxd__fozz + pssg__niht]
        for owqc__rglj in range(cvnb__fnrw):
            set_bit_to(null_bitmap_ptr, ndw__vkf, get_bit(nje__hcaf,
                owqc__rglj))
            ndw__vkf += 1
        bxd__fozz += pssg__niht


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            qug__elqy = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                qug__elqy, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            evwau__coluc = data.size
            recv_counts = gather_scalar(np.int32(evwau__coluc), allgather,
                root=root)
            letd__alcjo = recv_counts.sum()
            cpfl__eok = empty_like_type(letd__alcjo, data)
            meyu__cvc = np.empty(1, np.int32)
            if rank == root or allgather:
                meyu__cvc = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(evwau__coluc), cpfl__eok.ctypes,
                recv_counts.ctypes, meyu__cvc.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return cpfl__eok.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            cpfl__eok = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(cpfl__eok)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            cpfl__eok = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(cpfl__eok)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            evwau__coluc = len(data)
            pssg__niht = evwau__coluc + 7 >> 3
            recv_counts = gather_scalar(np.int32(evwau__coluc), allgather,
                root=root)
            letd__alcjo = recv_counts.sum()
            cpfl__eok = empty_like_type(letd__alcjo, data)
            meyu__cvc = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            mif__wol = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                meyu__cvc = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                mif__wol = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(evwau__coluc),
                cpfl__eok._days_data.ctypes, recv_counts.ctypes, meyu__cvc.
                ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(evwau__coluc),
                cpfl__eok._seconds_data.ctypes, recv_counts.ctypes,
                meyu__cvc.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(evwau__coluc
                ), cpfl__eok._microseconds_data.ctypes, recv_counts.ctypes,
                meyu__cvc.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(pssg__niht),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, mif__wol.
                ctypes, nvwpo__gvshs, allgather, np.int32(root))
            copy_gathered_null_bytes(cpfl__eok._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return cpfl__eok
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            evwau__coluc = len(data)
            pssg__niht = evwau__coluc + 7 >> 3
            recv_counts = gather_scalar(np.int32(evwau__coluc), allgather,
                root=root)
            letd__alcjo = recv_counts.sum()
            cpfl__eok = empty_like_type(letd__alcjo, data)
            meyu__cvc = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            mif__wol = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                meyu__cvc = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                mif__wol = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(evwau__coluc), cpfl__eok.
                _data.ctypes, recv_counts.ctypes, meyu__cvc.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(pssg__niht),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, mif__wol.
                ctypes, nvwpo__gvshs, allgather, np.int32(root))
            copy_gathered_null_bytes(cpfl__eok._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return cpfl__eok
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        nckk__xclk = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            ksba__kdh = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                ksba__kdh, nckk__xclk)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            nqfn__ygwom = bodo.gatherv(data._left, allgather, warn_if_rep, root
                )
            jkiar__fjh = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(nqfn__ygwom,
                jkiar__fjh)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            uhaxy__qsxdp = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            ngcs__kwmp = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ngcs__kwmp, uhaxy__qsxdp)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        uvhg__knqee = np.iinfo(np.int64).max
        zux__xuug = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            start = data._start
            stop = data._stop
            if len(data) == 0:
                start = uvhg__knqee
                stop = zux__xuug
            start = bodo.libs.distributed_api.dist_reduce(start, np.int32(
                Reduce_Type.Min.value))
            stop = bodo.libs.distributed_api.dist_reduce(stop, np.int32(
                Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if start == uvhg__knqee and stop == zux__xuug:
                start = 0
                stop = 0
            wwj__csepx = max(0, -(-(stop - start) // data._step))
            if wwj__csepx < total_len:
                stop = start + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                start = 0
                stop = 0
            return bodo.hiframes.pd_index_ext.init_range_index(start, stop,
                data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            qlcr__grlp = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, qlcr__grlp)
        else:

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.utils.conversion.index_from_array(arr, data._name)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            cpfl__eok = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(cpfl__eok,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        pslhy__wky = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        siu__xdug = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        siu__xdug += '  T = data\n'
        siu__xdug += '  T2 = init_table(T, True)\n'
        for wrbkm__vfp in data.type_to_blk.values():
            pslhy__wky[f'arr_inds_{wrbkm__vfp}'] = np.array(data.
                block_to_arr_ind[wrbkm__vfp], dtype=np.int64)
            siu__xdug += (
                f'  arr_list_{wrbkm__vfp} = get_table_block(T, {wrbkm__vfp})\n'
                )
            siu__xdug += f"""  out_arr_list_{wrbkm__vfp} = alloc_list_like(arr_list_{wrbkm__vfp}, True)
"""
            siu__xdug += f'  for i in range(len(arr_list_{wrbkm__vfp})):\n'
            siu__xdug += (
                f'    arr_ind_{wrbkm__vfp} = arr_inds_{wrbkm__vfp}[i]\n')
            siu__xdug += f"""    ensure_column_unboxed(T, arr_list_{wrbkm__vfp}, i, arr_ind_{wrbkm__vfp})
"""
            siu__xdug += f"""    out_arr_{wrbkm__vfp} = bodo.gatherv(arr_list_{wrbkm__vfp}[i], allgather, warn_if_rep, root)
"""
            siu__xdug += (
                f'    out_arr_list_{wrbkm__vfp}[i] = out_arr_{wrbkm__vfp}\n')
            siu__xdug += (
                f'  T2 = set_table_block(T2, out_arr_list_{wrbkm__vfp}, {wrbkm__vfp})\n'
                )
        siu__xdug += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        siu__xdug += f'  T2 = set_table_len(T2, length)\n'
        siu__xdug += f'  return T2\n'
        ppv__qtmn = {}
        exec(siu__xdug, pslhy__wky, ppv__qtmn)
        zsyd__flxi = ppv__qtmn['impl_table']
        return zsyd__flxi
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ubo__zdaiq = len(data.columns)
        if ubo__zdaiq == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                vhixo__zjqf = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    vhixo__zjqf, ())
            return impl
        tdvxq__qljeb = ', '.join(f'g_data_{i}' for i in range(ubo__zdaiq))
        ohag__ejynx = bodo.utils.transform.gen_const_tup(data.columns)
        siu__xdug = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            gfxf__dfvzo = bodo.hiframes.pd_dataframe_ext.DataFrameType(data
                .data, data.index, data.columns, Distribution.REP, True)
            pslhy__wky = {'bodo': bodo, 'df_type': gfxf__dfvzo}
            tdvxq__qljeb = 'T2'
            ohag__ejynx = 'df_type'
            siu__xdug += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            siu__xdug += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            pslhy__wky = {'bodo': bodo}
            for i in range(ubo__zdaiq):
                siu__xdug += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                siu__xdug += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        siu__xdug += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        siu__xdug += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        siu__xdug += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(tdvxq__qljeb, ohag__ejynx))
        ppv__qtmn = {}
        exec(siu__xdug, pslhy__wky, ppv__qtmn)
        nnqh__kfar = ppv__qtmn['impl_df']
        return nnqh__kfar
    if isinstance(data, ArrayItemArrayType):
        sopfs__vrsgv = np.int32(numba_to_c_type(types.int32))
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            akznu__sab = bodo.libs.array_item_arr_ext.get_offsets(data)
            nkpw__tim = bodo.libs.array_item_arr_ext.get_data(data)
            nkpw__tim = nkpw__tim[:akznu__sab[-1]]
            fme__ccyng = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            evwau__coluc = len(data)
            effjq__asai = np.empty(evwau__coluc, np.uint32)
            pssg__niht = evwau__coluc + 7 >> 3
            for i in range(evwau__coluc):
                effjq__asai[i] = akznu__sab[i + 1] - akznu__sab[i]
            recv_counts = gather_scalar(np.int32(evwau__coluc), allgather,
                root=root)
            letd__alcjo = recv_counts.sum()
            meyu__cvc = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            mif__wol = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                meyu__cvc = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for kqxe__zlo in range(len(recv_counts)):
                    recv_counts_nulls[kqxe__zlo] = recv_counts[kqxe__zlo
                        ] + 7 >> 3
                mif__wol = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            emnb__dhi = np.empty(letd__alcjo + 1, np.uint32)
            nde__tzz = bodo.gatherv(nkpw__tim, allgather, warn_if_rep, root)
            nyfod__edo = np.empty(letd__alcjo + 7 >> 3, np.uint8)
            c_gatherv(effjq__asai.ctypes, np.int32(evwau__coluc), emnb__dhi
                .ctypes, recv_counts.ctypes, meyu__cvc.ctypes, sopfs__vrsgv,
                allgather, np.int32(root))
            c_gatherv(fme__ccyng.ctypes, np.int32(pssg__niht),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, mif__wol.
                ctypes, nvwpo__gvshs, allgather, np.int32(root))
            dummy_use(data)
            rkr__ajzeg = np.empty(letd__alcjo + 1, np.uint64)
            convert_len_arr_to_offset(emnb__dhi.ctypes, rkr__ajzeg.ctypes,
                letd__alcjo)
            copy_gathered_null_bytes(nyfod__edo.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                letd__alcjo, nde__tzz, rkr__ajzeg, nyfod__edo)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        psojj__wdw = data.names
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            zdmr__rcn = bodo.libs.struct_arr_ext.get_data(data)
            iui__fqr = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            ycorh__yiu = bodo.gatherv(zdmr__rcn, allgather=allgather, root=root
                )
            rank = bodo.libs.distributed_api.get_rank()
            evwau__coluc = len(data)
            pssg__niht = evwau__coluc + 7 >> 3
            recv_counts = gather_scalar(np.int32(evwau__coluc), allgather,
                root=root)
            letd__alcjo = recv_counts.sum()
            nbv__azim = np.empty(letd__alcjo + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            mif__wol = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                mif__wol = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(iui__fqr.ctypes, np.int32(pssg__niht), tmp_null_bytes
                .ctypes, recv_counts_nulls.ctypes, mif__wol.ctypes,
                nvwpo__gvshs, allgather, np.int32(root))
            copy_gathered_null_bytes(nbv__azim.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(ycorh__yiu,
                nbv__azim, psojj__wdw)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            cpfl__eok = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(cpfl__eok)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            cpfl__eok = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(cpfl__eok)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            cpfl__eok = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(cpfl__eok)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            cpfl__eok = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            ufqgp__zncg = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            anlo__mdr = bodo.gatherv(data.indptr, allgather, warn_if_rep, root)
            xnio__wtsx = gather_scalar(data.shape[0], allgather, root=root)
            mtdc__ulgz = xnio__wtsx.sum()
            ubo__zdaiq = bodo.libs.distributed_api.dist_reduce(data.shape[1
                ], np.int32(Reduce_Type.Max.value))
            spskl__bwr = np.empty(mtdc__ulgz + 1, np.int64)
            ufqgp__zncg = ufqgp__zncg.astype(np.int64)
            spskl__bwr[0] = 0
            fyk__lmm = 1
            nahez__oteq = 0
            for kvq__trcbr in xnio__wtsx:
                for qfskl__cjen in range(kvq__trcbr):
                    lcqlk__jdwht = anlo__mdr[nahez__oteq + 1] - anlo__mdr[
                        nahez__oteq]
                    spskl__bwr[fyk__lmm] = spskl__bwr[fyk__lmm - 1
                        ] + lcqlk__jdwht
                    fyk__lmm += 1
                    nahez__oteq += 1
                nahez__oteq += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(cpfl__eok,
                ufqgp__zncg, spskl__bwr, (mtdc__ulgz, ubo__zdaiq))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        siu__xdug = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        siu__xdug += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        ppv__qtmn = {}
        exec(siu__xdug, {'bodo': bodo}, ppv__qtmn)
        oxjxq__xif = ppv__qtmn['impl_tuple']
        return oxjxq__xif
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    siu__xdug = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    siu__xdug += '    if random:\n'
    siu__xdug += '        if random_seed is None:\n'
    siu__xdug += '            random = 1\n'
    siu__xdug += '        else:\n'
    siu__xdug += '            random = 2\n'
    siu__xdug += '    if random_seed is None:\n'
    siu__xdug += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        thqf__oiq = data
        ubo__zdaiq = len(thqf__oiq.columns)
        for i in range(ubo__zdaiq):
            siu__xdug += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        siu__xdug += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        tdvxq__qljeb = ', '.join(f'data_{i}' for i in range(ubo__zdaiq))
        siu__xdug += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(zqatg__cim) for
            zqatg__cim in range(ubo__zdaiq))))
        siu__xdug += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        siu__xdug += '    if dests is None:\n'
        siu__xdug += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        siu__xdug += '    else:\n'
        siu__xdug += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for jtyqo__zhwur in range(ubo__zdaiq):
            siu__xdug += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(jtyqo__zhwur))
        siu__xdug += (
            '    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
            .format(ubo__zdaiq))
        siu__xdug += '    delete_table(out_table)\n'
        siu__xdug += '    if parallel:\n'
        siu__xdug += '        delete_table(table_total)\n'
        tdvxq__qljeb = ', '.join('out_arr_{}'.format(i) for i in range(
            ubo__zdaiq))
        ohag__ejynx = bodo.utils.transform.gen_const_tup(thqf__oiq.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        siu__xdug += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(tdvxq__qljeb, index, ohag__ejynx))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        siu__xdug += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        siu__xdug += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        siu__xdug += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        siu__xdug += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        siu__xdug += '    if dests is None:\n'
        siu__xdug += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        siu__xdug += '    else:\n'
        siu__xdug += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        siu__xdug += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        siu__xdug += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        siu__xdug += '    delete_table(out_table)\n'
        siu__xdug += '    if parallel:\n'
        siu__xdug += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        siu__xdug += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        siu__xdug += '    if not parallel:\n'
        siu__xdug += '        return data\n'
        siu__xdug += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        siu__xdug += '    if dests is None:\n'
        siu__xdug += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        siu__xdug += '    elif bodo.get_rank() not in dests:\n'
        siu__xdug += '        dim0_local_size = 0\n'
        siu__xdug += '    else:\n'
        siu__xdug += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        siu__xdug += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        siu__xdug += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        siu__xdug += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        siu__xdug += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        siu__xdug += '    if dests is None:\n'
        siu__xdug += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        siu__xdug += '    else:\n'
        siu__xdug += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        siu__xdug += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        siu__xdug += '    delete_table(out_table)\n'
        siu__xdug += '    if parallel:\n'
        siu__xdug += '        delete_table(table_total)\n'
        siu__xdug += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    ppv__qtmn = {}
    exec(siu__xdug, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}, ppv__qtmn
        )
    impl = ppv__qtmn['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    siu__xdug = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        siu__xdug += '    if seed is None:\n'
        siu__xdug += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        siu__xdug += '    np.random.seed(seed)\n'
        siu__xdug += '    if not parallel:\n'
        siu__xdug += '        data = data.copy()\n'
        siu__xdug += '        np.random.shuffle(data)\n'
        siu__xdug += '        return data\n'
        siu__xdug += '    else:\n'
        siu__xdug += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        siu__xdug += '        permutation = np.arange(dim0_global_size)\n'
        siu__xdug += '        np.random.shuffle(permutation)\n'
        siu__xdug += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        siu__xdug += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        siu__xdug += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        siu__xdug += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        siu__xdug += '        return output\n'
    else:
        siu__xdug += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    ppv__qtmn = {}
    exec(siu__xdug, {'np': np, 'bodo': bodo}, ppv__qtmn)
    impl = ppv__qtmn['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    gcspp__qgbem = np.empty(sendcounts_nulls.sum(), np.uint8)
    bxd__fozz = 0
    ndw__vkf = 0
    for fbk__oakbm in range(len(sendcounts)):
        cvnb__fnrw = sendcounts[fbk__oakbm]
        pssg__niht = sendcounts_nulls[fbk__oakbm]
        nje__hcaf = gcspp__qgbem[bxd__fozz:bxd__fozz + pssg__niht]
        for owqc__rglj in range(cvnb__fnrw):
            set_bit_to_arr(nje__hcaf, owqc__rglj, get_bit_bitmap(
                null_bitmap_ptr, ndw__vkf))
            ndw__vkf += 1
        bxd__fozz += pssg__niht
    return gcspp__qgbem


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    lil__meb = MPI.COMM_WORLD
    data = lil__meb.bcast(data, root)
    return data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_scatterv_send_counts(send_counts, n_pes, n):
    if not is_overload_none(send_counts):
        return lambda send_counts, n_pes, n: send_counts

    def impl(send_counts, n_pes, n):
        send_counts = np.empty(n_pes, np.int32)
        for i in range(n_pes):
            send_counts[i] = get_node_portion(n, n_pes, i)
        return send_counts
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _scatterv_np(data, send_counts=None, warn_if_dist=True):
    typ_val = numba_to_c_type(data.dtype)
    qlszl__fgsi = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    lauve__hqird = (0,) * qlszl__fgsi

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        jpfzq__xklpo = np.ascontiguousarray(data)
        vfv__dbhu = data.ctypes
        nakpt__qrkjj = lauve__hqird
        if rank == MPI_ROOT:
            nakpt__qrkjj = jpfzq__xklpo.shape
        nakpt__qrkjj = bcast_tuple(nakpt__qrkjj)
        kmtxv__rvaei = get_tuple_prod(nakpt__qrkjj[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            nakpt__qrkjj[0])
        send_counts *= kmtxv__rvaei
        evwau__coluc = send_counts[rank]
        trojl__pkiaz = np.empty(evwau__coluc, dtype)
        meyu__cvc = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(vfv__dbhu, send_counts.ctypes, meyu__cvc.ctypes,
            trojl__pkiaz.ctypes, np.int32(evwau__coluc), np.int32(typ_val))
        return trojl__pkiaz.reshape((-1,) + nakpt__qrkjj[1:])
    return scatterv_arr_impl


def _get_name_value_for_type(name_typ):
    assert isinstance(name_typ, (types.UnicodeType, types.StringLiteral)
        ) or name_typ == types.none
    return None if name_typ == types.none else '_' + str(ir_utils.next_label())


def get_value_for_type(dtype):
    if isinstance(dtype, types.Array):
        return np.zeros((1,) * dtype.ndim, numba.np.numpy_support.as_dtype(
            dtype.dtype))
    if dtype == string_array_type:
        return pd.array(['A'], 'string')
    if dtype == bodo.dict_str_arr_type:
        import pyarrow as pa
        return pa.array(['a'], type=pa.dictionary(pa.int32(), pa.string()))
    if dtype == binary_array_type:
        return np.array([b'A'], dtype=object)
    if isinstance(dtype, IntegerArrayType):
        scwxn__jjit = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], scwxn__jjit)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        uhaxy__qsxdp = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=uhaxy__qsxdp)
        brts__tbw = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(brts__tbw)
        return pd.Index(arr, name=uhaxy__qsxdp)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        uhaxy__qsxdp = _get_name_value_for_type(dtype.name_typ)
        psojj__wdw = tuple(_get_name_value_for_type(t) for t in dtype.names_typ
            )
        lurgx__qss = tuple(get_value_for_type(t) for t in dtype.array_types)
        lurgx__qss = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in lurgx__qss)
        val = pd.MultiIndex.from_arrays(lurgx__qss, names=psojj__wdw)
        val.name = uhaxy__qsxdp
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        uhaxy__qsxdp = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=uhaxy__qsxdp)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        lurgx__qss = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({uhaxy__qsxdp: arr for uhaxy__qsxdp, arr in zip
            (dtype.columns, lurgx__qss)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        brts__tbw = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(brts__tbw[0], brts__tbw
            [0])])
    raise BodoError(f'get_value_for_type(dtype): Missing data type {dtype}')


def scatterv(data, send_counts=None, warn_if_dist=True):
    rank = bodo.libs.distributed_api.get_rank()
    if rank != MPI_ROOT and data is not None:
        warnings.warn(BodoWarning(
            "bodo.scatterv(): A non-None value for 'data' was found on a rank other than the root. This data won't be sent to any other ranks and will be overwritten with data from rank 0."
            ))
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return scatterv_impl(data, send_counts)


@overload(scatterv)
def scatterv_overload(data, send_counts=None, warn_if_dist=True):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.scatterv()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.scatterv()')
    return lambda data, send_counts=None, warn_if_dist=True: scatterv_impl(data
        , send_counts)


@numba.generated_jit(nopython=True)
def scatterv_impl(data, send_counts=None, warn_if_dist=True):
    if isinstance(data, types.Array):
        return lambda data, send_counts=None, warn_if_dist=True: _scatterv_np(
            data, send_counts)
    if is_str_arr_type(data) or data == binary_array_type:
        sopfs__vrsgv = np.int32(numba_to_c_type(types.int32))
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            bhrm__qrch = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            bhrm__qrch = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        siu__xdug = f"""def impl(
            data, send_counts=None, warn_if_dist=True
        ):  # pragma: no cover
            data = decode_if_dict_array(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            n_all = bodo.libs.distributed_api.bcast_scalar(len(data))

            # convert offsets to lengths of strings
            send_arr_lens = np.empty(
                len(data), np.uint32
            )  # XXX offset type is offset_type, lengths for comm are uint32
            for i in range(len(data)):
                send_arr_lens[i] = bodo.libs.str_arr_ext.get_str_arr_item_length(
                    data, i
                )

            # ------- calculate buffer counts -------

            send_counts = bodo.libs.distributed_api._get_scatterv_send_counts(send_counts, n_pes, n_all)

            # displacements
            displs = bodo.ir.join.calc_disp(send_counts)

            # compute send counts for characters
            send_counts_char = np.empty(n_pes, np.int32)
            if rank == 0:
                curr_str = 0
                for i in range(n_pes):
                    c = 0
                    for _ in range(send_counts[i]):
                        c += send_arr_lens[curr_str]
                        curr_str += 1
                    send_counts_char[i] = c

            bodo.libs.distributed_api.bcast(send_counts_char)

            # displacements for characters
            displs_char = bodo.ir.join.calc_disp(send_counts_char)

            # compute send counts for nulls
            send_counts_nulls = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                send_counts_nulls[i] = (send_counts[i] + 7) >> 3

            # displacements for nulls
            displs_nulls = bodo.ir.join.calc_disp(send_counts_nulls)

            # alloc output array
            n_loc = send_counts[rank]  # total number of elements on this PE
            n_loc_char = send_counts_char[rank]
            recv_arr = {bhrm__qrch}(n_loc, n_loc_char)

            # ----- string lengths -----------

            recv_lens = np.empty(n_loc, np.uint32)
            bodo.libs.distributed_api.c_scatterv(
                send_arr_lens.ctypes,
                send_counts.ctypes,
                displs.ctypes,
                recv_lens.ctypes,
                np.int32(n_loc),
                int32_typ_enum,
            )

            # TODO: don't hardcode offset type. Also, if offset is 32 bit we can
            # use the same buffer
            bodo.libs.str_arr_ext.convert_len_arr_to_offset(recv_lens.ctypes, bodo.libs.str_arr_ext.get_offset_ptr(recv_arr), n_loc)

            # ----- string characters -----------

            bodo.libs.distributed_api.c_scatterv(
                bodo.libs.str_arr_ext.get_data_ptr(data),
                send_counts_char.ctypes,
                displs_char.ctypes,
                bodo.libs.str_arr_ext.get_data_ptr(recv_arr),
                np.int32(n_loc_char),
                char_typ_enum,
            )

            # ----------- null bitmap -------------

            n_recv_bytes = (n_loc + 7) >> 3

            send_null_bitmap = bodo.libs.distributed_api.get_scatter_null_bytes_buff(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(data), send_counts, send_counts_nulls
            )

            bodo.libs.distributed_api.c_scatterv(
                send_null_bitmap.ctypes,
                send_counts_nulls.ctypes,
                displs_nulls.ctypes,
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(recv_arr),
                np.int32(n_recv_bytes),
                char_typ_enum,
            )

            return recv_arr"""
        ppv__qtmn = dict()
        exec(siu__xdug, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            sopfs__vrsgv, 'char_typ_enum': nvwpo__gvshs,
            'decode_if_dict_array': decode_if_dict_array}, ppv__qtmn)
        impl = ppv__qtmn['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        sopfs__vrsgv = np.int32(numba_to_c_type(types.int32))
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            iijhl__kex = bodo.libs.array_item_arr_ext.get_offsets(data)
            xfg__bhzsf = bodo.libs.array_item_arr_ext.get_data(data)
            xfg__bhzsf = xfg__bhzsf[:iijhl__kex[-1]]
            qwigz__gtq = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            qne__eak = bcast_scalar(len(data))
            yszh__sos = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                yszh__sos[i] = iijhl__kex[i + 1] - iijhl__kex[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                qne__eak)
            meyu__cvc = bodo.ir.join.calc_disp(send_counts)
            yptca__uqi = np.empty(n_pes, np.int32)
            if rank == 0:
                tlx__agwhw = 0
                for i in range(n_pes):
                    foocn__kskqo = 0
                    for qfskl__cjen in range(send_counts[i]):
                        foocn__kskqo += yszh__sos[tlx__agwhw]
                        tlx__agwhw += 1
                    yptca__uqi[i] = foocn__kskqo
            bcast(yptca__uqi)
            uqptj__pdtu = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                uqptj__pdtu[i] = send_counts[i] + 7 >> 3
            mif__wol = bodo.ir.join.calc_disp(uqptj__pdtu)
            evwau__coluc = send_counts[rank]
            hwpe__mqupn = np.empty(evwau__coluc + 1, np_offset_type)
            mjveu__bhl = bodo.libs.distributed_api.scatterv_impl(xfg__bhzsf,
                yptca__uqi)
            blo__jktxc = evwau__coluc + 7 >> 3
            itun__zorc = np.empty(blo__jktxc, np.uint8)
            bhfrs__tro = np.empty(evwau__coluc, np.uint32)
            c_scatterv(yszh__sos.ctypes, send_counts.ctypes, meyu__cvc.
                ctypes, bhfrs__tro.ctypes, np.int32(evwau__coluc), sopfs__vrsgv
                )
            convert_len_arr_to_offset(bhfrs__tro.ctypes, hwpe__mqupn.ctypes,
                evwau__coluc)
            ikibd__vdri = get_scatter_null_bytes_buff(qwigz__gtq.ctypes,
                send_counts, uqptj__pdtu)
            c_scatterv(ikibd__vdri.ctypes, uqptj__pdtu.ctypes, mif__wol.
                ctypes, itun__zorc.ctypes, np.int32(blo__jktxc), nvwpo__gvshs)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                evwau__coluc, mjveu__bhl, hwpe__mqupn, itun__zorc)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            rcg__ugxgf = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            rcg__ugxgf = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            rcg__ugxgf = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            rcg__ugxgf = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            jpfzq__xklpo = data._data
            iui__fqr = data._null_bitmap
            quzaf__vjnrm = len(jpfzq__xklpo)
            dls__xrns = _scatterv_np(jpfzq__xklpo, send_counts)
            qne__eak = bcast_scalar(quzaf__vjnrm)
            hubi__vpd = len(dls__xrns) + 7 >> 3
            tfgld__pmlek = np.empty(hubi__vpd, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                qne__eak)
            uqptj__pdtu = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                uqptj__pdtu[i] = send_counts[i] + 7 >> 3
            mif__wol = bodo.ir.join.calc_disp(uqptj__pdtu)
            ikibd__vdri = get_scatter_null_bytes_buff(iui__fqr.ctypes,
                send_counts, uqptj__pdtu)
            c_scatterv(ikibd__vdri.ctypes, uqptj__pdtu.ctypes, mif__wol.
                ctypes, tfgld__pmlek.ctypes, np.int32(hubi__vpd), nvwpo__gvshs)
            return rcg__ugxgf(dls__xrns, tfgld__pmlek)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            glyc__mksf = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            ljelt__zkhzt = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(glyc__mksf,
                ljelt__zkhzt)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            pnul__iczz = data._step
            uhaxy__qsxdp = data._name
            uhaxy__qsxdp = bcast_scalar(uhaxy__qsxdp)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            pnul__iczz = bcast_scalar(pnul__iczz)
            mcl__vply = bodo.libs.array_kernels.calc_nitems(start, stop,
                pnul__iczz)
            chunk_start = bodo.libs.distributed_api.get_start(mcl__vply,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(mcl__vply,
                n_pes, rank)
            pjiu__gfsl = start + pnul__iczz * chunk_start
            pog__fqhgl = start + pnul__iczz * (chunk_start + chunk_count)
            pog__fqhgl = min(pog__fqhgl, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(pjiu__gfsl,
                pog__fqhgl, pnul__iczz, uhaxy__qsxdp)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        qlcr__grlp = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            jpfzq__xklpo = data._data
            uhaxy__qsxdp = data._name
            uhaxy__qsxdp = bcast_scalar(uhaxy__qsxdp)
            arr = bodo.libs.distributed_api.scatterv_impl(jpfzq__xklpo,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                uhaxy__qsxdp, qlcr__grlp)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            jpfzq__xklpo = data._data
            uhaxy__qsxdp = data._name
            uhaxy__qsxdp = bcast_scalar(uhaxy__qsxdp)
            arr = bodo.libs.distributed_api.scatterv_impl(jpfzq__xklpo,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, uhaxy__qsxdp)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            cpfl__eok = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            uhaxy__qsxdp = bcast_scalar(data._name)
            psojj__wdw = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(cpfl__eok,
                psojj__wdw, uhaxy__qsxdp)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            uhaxy__qsxdp = bodo.hiframes.pd_series_ext.get_series_name(data)
            oatl__phj = bcast_scalar(uhaxy__qsxdp)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            ngcs__kwmp = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ngcs__kwmp, oatl__phj)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ubo__zdaiq = len(data.columns)
        tdvxq__qljeb = ', '.join('g_data_{}'.format(i) for i in range(
            ubo__zdaiq))
        ohag__ejynx = bodo.utils.transform.gen_const_tup(data.columns)
        siu__xdug = 'def impl_df(data, send_counts=None, warn_if_dist=True):\n'
        for i in range(ubo__zdaiq):
            siu__xdug += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            siu__xdug += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        siu__xdug += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        siu__xdug += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        siu__xdug += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(tdvxq__qljeb, ohag__ejynx))
        ppv__qtmn = {}
        exec(siu__xdug, {'bodo': bodo}, ppv__qtmn)
        nnqh__kfar = ppv__qtmn['impl_df']
        return nnqh__kfar
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            qug__elqy = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                qug__elqy, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        siu__xdug = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        siu__xdug += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        ppv__qtmn = {}
        exec(siu__xdug, {'bodo': bodo}, ppv__qtmn)
        oxjxq__xif = ppv__qtmn['impl_tuple']
        return oxjxq__xif
    if data is types.none:
        return lambda data, send_counts=None, warn_if_dist=True: None
    raise BodoError('scatterv() not available for {}'.format(data))


@intrinsic
def cptr_to_voidptr(typingctx, cptr_tp=None):

    def codegen(context, builder, sig, args):
        return builder.bitcast(args[0], lir.IntType(8).as_pointer())
    return types.voidptr(cptr_tp), codegen


def bcast(data, root=MPI_ROOT):
    return


@overload(bcast, no_unliteral=True)
def bcast_overload(data, root=MPI_ROOT):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.bcast()')
    if isinstance(data, types.Array):

        def bcast_impl(data, root=MPI_ROOT):
            typ_enum = get_type_enum(data)
            count = data.size
            assert count < INT_MAX
            c_bcast(data.ctypes, np.int32(count), typ_enum, np.array([-1]).
                ctypes, 0, np.int32(root))
            return
        return bcast_impl
    if isinstance(data, DecimalArrayType):

        def bcast_decimal_arr(data, root=MPI_ROOT):
            count = data._data.size
            assert count < INT_MAX
            c_bcast(data._data.ctypes, np.int32(count), CTypeEnum.Int128.
                value, np.array([-1]).ctypes, 0, np.int32(root))
            bcast(data._null_bitmap, root)
            return
        return bcast_decimal_arr
    if isinstance(data, IntegerArrayType) or data in (boolean_array,
        datetime_date_array_type):

        def bcast_impl_int_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            bcast(data._null_bitmap, root)
            return
        return bcast_impl_int_arr
    if is_str_arr_type(data) or data == binary_array_type:
        bow__uqi = np.int32(numba_to_c_type(offset_type))
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            evwau__coluc = len(data)
            ypqth__obr = num_total_chars(data)
            assert evwau__coluc < INT_MAX
            assert ypqth__obr < INT_MAX
            uktwx__cnujz = get_offset_ptr(data)
            vfv__dbhu = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            pssg__niht = evwau__coluc + 7 >> 3
            c_bcast(uktwx__cnujz, np.int32(evwau__coluc + 1), bow__uqi, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(vfv__dbhu, np.int32(ypqth__obr), nvwpo__gvshs, np.array
                ([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(pssg__niht), nvwpo__gvshs, np
                .array([-1]).ctypes, 0, np.int32(root))
        return bcast_str_impl


c_bcast = types.ExternalFunction('c_bcast', types.void(types.voidptr, types
    .int32, types.int32, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def bcast_scalar(val, root=MPI_ROOT):
    val = types.unliteral(val)
    if not (isinstance(val, (types.Integer, types.Float)) or val in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.string_type, types.none,
        types.bool_]):
        raise BodoError(
            f'bcast_scalar requires an argument of type Integer, Float, datetime64ns, timedelta64ns, string, None, or Bool. Found type {val}'
            )
    if val == types.none:
        return lambda val, root=MPI_ROOT: None
    if val == bodo.string_type:
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                wpxx__pun = 0
                xqkop__zysm = np.empty(0, np.uint8).ctypes
            else:
                xqkop__zysm, wpxx__pun = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            wpxx__pun = bodo.libs.distributed_api.bcast_scalar(wpxx__pun, root)
            if rank != root:
                kyw__kob = np.empty(wpxx__pun + 1, np.uint8)
                kyw__kob[wpxx__pun] = 0
                xqkop__zysm = kyw__kob.ctypes
            c_bcast(xqkop__zysm, np.int32(wpxx__pun), nvwpo__gvshs, np.
                array([-1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(xqkop__zysm, wpxx__pun)
        return impl_str
    typ_val = numba_to_c_type(val)
    siu__xdug = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    ppv__qtmn = {}
    exec(siu__xdug, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, ppv__qtmn)
    glq__uca = ppv__qtmn['bcast_scalar_impl']
    return glq__uca


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    hefjt__erzte = len(val)
    siu__xdug = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    siu__xdug += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(hefjt__erzte
        )), ',' if hefjt__erzte else '')
    ppv__qtmn = {}
    exec(siu__xdug, {'bcast_scalar': bcast_scalar}, ppv__qtmn)
    enkh__zhq = ppv__qtmn['bcast_tuple_impl']
    return enkh__zhq


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            evwau__coluc = bcast_scalar(len(arr), root)
            npcog__vjghe = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(evwau__coluc, npcog__vjghe)
            return arr
        return prealloc_impl
    return lambda arr, root=MPI_ROOT: arr


def get_local_slice(idx, arr_start, total_len):
    return idx


@overload(get_local_slice, no_unliteral=True, jit_options={'cache': True,
    'no_cpython_wrapper': True})
def get_local_slice_overload(idx, arr_start, total_len):

    def impl(idx, arr_start, total_len):
        slice_index = numba.cpython.unicode._normalize_slice(idx, total_len)
        start = slice_index.start
        pnul__iczz = slice_index.step
        zdcf__sri = 0 if pnul__iczz == 1 or start > arr_start else abs(
            pnul__iczz - arr_start % pnul__iczz) % pnul__iczz
        pjiu__gfsl = max(arr_start, slice_index.start) - arr_start + zdcf__sri
        pog__fqhgl = max(slice_index.stop - arr_start, 0)
        return slice(pjiu__gfsl, pog__fqhgl, pnul__iczz)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        owysd__hohv = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[owysd__hohv])
    return getitem_impl


dummy_use = numba.njit(lambda a: None)


def int_getitem(arr, ind, arr_start, total_len, is_1D):
    return arr[ind]


def transform_str_getitem_output(data, length):
    pass


@overload(transform_str_getitem_output)
def overload_transform_str_getitem_output(data, length):
    if data == bodo.string_type:
        return lambda data, length: bodo.libs.str_arr_ext.decode_utf8(data.
            _data, length)
    if data == types.Array(types.uint8, 1, 'C'):
        return lambda data, length: bodo.libs.binary_arr_ext.init_bytes_type(
            data, length)
    raise BodoError(
        f'Internal Error: Expected String or Uint8 Array, found {data}')


@overload(int_getitem, no_unliteral=True)
def int_getitem_overload(arr, ind, arr_start, total_len, is_1D):
    if is_str_arr_type(arr) or arr == bodo.binary_array_type:
        kwe__gnx = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        nvwpo__gvshs = np.int32(numba_to_c_type(types.uint8))
        lwpmp__sdf = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            vofq__ubxvh = np.int32(10)
            tag = np.int32(11)
            dsw__yzf = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                nkpw__tim = arr._data
                kqpeg__wxp = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    nkpw__tim, ind)
                aevki__mvj = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    nkpw__tim, ind + 1)
                length = aevki__mvj - kqpeg__wxp
                ifv__pwlq = nkpw__tim[ind]
                dsw__yzf[0] = length
                isend(dsw__yzf, np.int32(1), root, vofq__ubxvh, True)
                isend(ifv__pwlq, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(lwpmp__sdf
                , kwe__gnx, 0, 1)
            wwj__csepx = 0
            if rank == root:
                wwj__csepx = recv(np.int64, ANY_SOURCE, vofq__ubxvh)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    lwpmp__sdf, kwe__gnx, wwj__csepx, 1)
                vfv__dbhu = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(vfv__dbhu, np.int32(wwj__csepx), nvwpo__gvshs,
                    ANY_SOURCE, tag)
            dummy_use(dsw__yzf)
            wwj__csepx = bcast_scalar(wwj__csepx)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    lwpmp__sdf, kwe__gnx, wwj__csepx, 1)
            vfv__dbhu = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(vfv__dbhu, np.int32(wwj__csepx), nvwpo__gvshs, np.array
                ([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, wwj__csepx)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        tkwjt__hpalw = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, tkwjt__hpalw)
            if arr_start <= ind < arr_start + len(arr):
                qug__elqy = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = qug__elqy[ind - arr_start]
                send_arr = np.full(1, data, tkwjt__hpalw)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = tkwjt__hpalw(-1)
            if rank == root:
                val = recv(tkwjt__hpalw, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            hrmju__oplak = arr.dtype.categories[max(val, 0)]
            return hrmju__oplak
        return cat_getitem_impl
    cni__mfrkx = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, cni__mfrkx)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, cni__mfrkx)[0]
        if rank == root:
            val = recv(cni__mfrkx, ANY_SOURCE, tag)
        dummy_use(send_arr)
        val = bcast_scalar(val)
        return val
    return getitem_impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    cde__lmbff = get_type_enum(out_data)
    assert typ_enum == cde__lmbff
    if isinstance(send_data, (IntegerArrayType, DecimalArrayType)
        ) or send_data in (boolean_array, datetime_date_array_type):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data._data.ctypes,
            out_data._data.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    if isinstance(send_data, bodo.CategoricalArrayType):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data.codes.ctypes,
            out_data.codes.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    return (lambda send_data, out_data, send_counts, recv_counts, send_disp,
        recv_disp: c_alltoallv(send_data.ctypes, out_data.ctypes,
        send_counts.ctypes, recv_counts.ctypes, send_disp.ctypes, recv_disp
        .ctypes, typ_enum))


def alltoallv_tup(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    return


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(send_data, out_data, send_counts, recv_counts,
    send_disp, recv_disp):
    count = send_data.count
    assert out_data.count == count
    siu__xdug = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        siu__xdug += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    siu__xdug += '  return\n'
    ppv__qtmn = {}
    exec(siu__xdug, {'alltoallv': alltoallv}, ppv__qtmn)
    pdg__pplfv = ppv__qtmn['f']
    return pdg__pplfv


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    start = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return start, count


@numba.njit
def get_start(total_size, pes, rank):
    mxh__hkfsg = total_size % pes
    mhab__itwx = (total_size - mxh__hkfsg) // pes
    return rank * mhab__itwx + min(rank, mxh__hkfsg)


@numba.njit
def get_end(total_size, pes, rank):
    mxh__hkfsg = total_size % pes
    mhab__itwx = (total_size - mxh__hkfsg) // pes
    return (rank + 1) * mhab__itwx + min(rank + 1, mxh__hkfsg)


@numba.njit
def get_node_portion(total_size, pes, rank):
    mxh__hkfsg = total_size % pes
    mhab__itwx = (total_size - mxh__hkfsg) // pes
    if rank < mxh__hkfsg:
        return mhab__itwx + 1
    else:
        return mhab__itwx


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    xebxg__rmn = in_arr.dtype(0)
    tnq__yhnf = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        foocn__kskqo = xebxg__rmn
        for rsqb__fnb in np.nditer(in_arr):
            foocn__kskqo += rsqb__fnb.item()
        iwja__grmpi = dist_exscan(foocn__kskqo, tnq__yhnf)
        for i in range(in_arr.size):
            iwja__grmpi += in_arr[i]
            out_arr[i] = iwja__grmpi
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    wowbc__gyzpl = in_arr.dtype(1)
    tnq__yhnf = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        foocn__kskqo = wowbc__gyzpl
        for rsqb__fnb in np.nditer(in_arr):
            foocn__kskqo *= rsqb__fnb.item()
        iwja__grmpi = dist_exscan(foocn__kskqo, tnq__yhnf)
        if get_rank() == 0:
            iwja__grmpi = wowbc__gyzpl
        for i in range(in_arr.size):
            iwja__grmpi *= in_arr[i]
            out_arr[i] = iwja__grmpi
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        wowbc__gyzpl = np.finfo(in_arr.dtype(1).dtype).max
    else:
        wowbc__gyzpl = np.iinfo(in_arr.dtype(1).dtype).max
    tnq__yhnf = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        foocn__kskqo = wowbc__gyzpl
        for rsqb__fnb in np.nditer(in_arr):
            foocn__kskqo = min(foocn__kskqo, rsqb__fnb.item())
        iwja__grmpi = dist_exscan(foocn__kskqo, tnq__yhnf)
        if get_rank() == 0:
            iwja__grmpi = wowbc__gyzpl
        for i in range(in_arr.size):
            iwja__grmpi = min(iwja__grmpi, in_arr[i])
            out_arr[i] = iwja__grmpi
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        wowbc__gyzpl = np.finfo(in_arr.dtype(1).dtype).min
    else:
        wowbc__gyzpl = np.iinfo(in_arr.dtype(1).dtype).min
    wowbc__gyzpl = in_arr.dtype(1)
    tnq__yhnf = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        foocn__kskqo = wowbc__gyzpl
        for rsqb__fnb in np.nditer(in_arr):
            foocn__kskqo = max(foocn__kskqo, rsqb__fnb.item())
        iwja__grmpi = dist_exscan(foocn__kskqo, tnq__yhnf)
        if get_rank() == 0:
            iwja__grmpi = wowbc__gyzpl
        for i in range(in_arr.size):
            iwja__grmpi = max(iwja__grmpi, in_arr[i])
            out_arr[i] = iwja__grmpi
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    fgs__kclbr = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), fgs__kclbr)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    bkcx__cmf = args[0]
    if equiv_set.has_shape(bkcx__cmf):
        return ArrayAnalysis.AnalyzeResult(shape=bkcx__cmf, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_dist_return = (
    dist_return_equiv)
ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_rep_return = (
    dist_return_equiv)


def threaded_return(A):
    return A


@numba.njit
def set_arr_local(arr, ind, val):
    arr[ind] = val


@numba.njit
def local_alloc_size(n, in_arr):
    return n


@infer_global(threaded_return)
@infer_global(dist_return)
@infer_global(rep_return)
class ThreadedRetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        return signature(args[0], *args)


@numba.njit
def parallel_print(*args):
    print(*args)


@numba.njit
def single_print(*args):
    if bodo.libs.distributed_api.get_rank() == 0:
        print(*args)


@numba.njit(no_cpython_wrapper=True)
def print_if_not_empty(arg):
    if len(arg) != 0 or bodo.get_rank() == 0:
        print(arg)


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        pklns__nxws = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        siu__xdug = 'def f(req, cond=True):\n'
        siu__xdug += f'  return {pklns__nxws}\n'
        ppv__qtmn = {}
        exec(siu__xdug, {'_wait': _wait}, ppv__qtmn)
        impl = ppv__qtmn['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


class ReqArrayType(types.Type):

    def __init__(self):
        super(ReqArrayType, self).__init__(name='ReqArrayType()')


req_array_type = ReqArrayType()
register_model(ReqArrayType)(models.OpaqueModel)
waitall = types.ExternalFunction('dist_waitall', types.void(types.int32,
    req_array_type))
comm_req_alloc = types.ExternalFunction('comm_req_alloc', req_array_type(
    types.int32))
comm_req_dealloc = types.ExternalFunction('comm_req_dealloc', types.void(
    req_array_type))
req_array_setitem = types.ExternalFunction('req_array_setitem', types.void(
    req_array_type, types.int64, mpi_req_numba_type))


@overload(operator.setitem, no_unliteral=True)
def overload_req_arr_setitem(A, idx, val):
    if A == req_array_type:
        assert val == mpi_req_numba_type
        return lambda A, idx, val: req_array_setitem(A, idx, val)


@numba.njit
def _get_local_range(start, stop, chunk_start, chunk_count):
    assert start >= 0 and stop > 0
    pjiu__gfsl = max(start, chunk_start)
    pog__fqhgl = min(stop, chunk_start + chunk_count)
    gfgq__fsyh = pjiu__gfsl - chunk_start
    xtw__tluej = pog__fqhgl - chunk_start
    if gfgq__fsyh < 0 or xtw__tluej < 0:
        gfgq__fsyh = 1
        xtw__tluej = 0
    return gfgq__fsyh, xtw__tluej


@register_jitable
def _set_if_in_range(A, val, index, chunk_start):
    if index >= chunk_start and index < chunk_start + len(A):
        A[index - chunk_start] = val


@register_jitable
def _root_rank_select(old_val, new_val):
    if get_rank() == 0:
        return old_val
    return new_val


def get_tuple_prod(t):
    return np.prod(t)


@overload(get_tuple_prod, no_unliteral=True)
def get_tuple_prod_overload(t):
    if t == numba.core.types.containers.Tuple(()):
        return lambda t: 1

    def get_tuple_prod_impl(t):
        mxh__hkfsg = 1
        for a in t:
            mxh__hkfsg *= a
        return mxh__hkfsg
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    aqjsb__pnpik = np.ascontiguousarray(in_arr)
    uypkj__kzv = get_tuple_prod(aqjsb__pnpik.shape[1:])
    fgkh__csq = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        dmhsx__vwxsv = np.array(dest_ranks, dtype=np.int32)
    else:
        dmhsx__vwxsv = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, aqjsb__pnpik.ctypes,
        new_dim0_global_len, len(in_arr), dtype_size * fgkh__csq, 
        dtype_size * uypkj__kzv, len(dmhsx__vwxsv), dmhsx__vwxsv.ctypes)
    check_and_propagate_cpp_exception()


permutation_int = types.ExternalFunction('permutation_int', types.void(
    types.voidptr, types.intp))


@numba.njit
def dist_permutation_int(lhs, n):
    permutation_int(lhs.ctypes, n)


permutation_array_index = types.ExternalFunction('permutation_array_index',
    types.void(types.voidptr, types.intp, types.intp, types.voidptr, types.
    int64, types.voidptr, types.intp))


@numba.njit
def dist_permutation_array_index(lhs, lhs_len, dtype_size, rhs, p, p_len):
    xbolw__xscs = np.ascontiguousarray(rhs)
    drp__fvwl = get_tuple_prod(xbolw__xscs.shape[1:])
    fgjde__vwjt = dtype_size * drp__fvwl
    permutation_array_index(lhs.ctypes, lhs_len, fgjde__vwjt, xbolw__xscs.
        ctypes, xbolw__xscs.shape[0], p.ctypes, p_len)
    check_and_propagate_cpp_exception()


from bodo.io import fsspec_reader, hdfs_reader, s3_reader
ll.add_symbol('finalize', hdist.finalize)
finalize = types.ExternalFunction('finalize', types.int32())
ll.add_symbol('finalize_s3', s3_reader.finalize_s3)
finalize_s3 = types.ExternalFunction('finalize_s3', types.int32())
ll.add_symbol('finalize_fsspec', fsspec_reader.finalize_fsspec)
finalize_fsspec = types.ExternalFunction('finalize_fsspec', types.int32())
ll.add_symbol('disconnect_hdfs', hdfs_reader.disconnect_hdfs)
disconnect_hdfs = types.ExternalFunction('disconnect_hdfs', types.int32())


def _check_for_cpp_errors():
    pass


@overload(_check_for_cpp_errors)
def overload_check_for_cpp_errors():
    return lambda : check_and_propagate_cpp_exception()


@numba.njit
def call_finalize():
    finalize()
    finalize_s3()
    finalize_fsspec()
    _check_for_cpp_errors()
    disconnect_hdfs()


def flush_stdout():
    if not sys.stdout.closed:
        sys.stdout.flush()


atexit.register(call_finalize)
atexit.register(flush_stdout)


def bcast_comm(data, comm_ranks, nranks, root=MPI_ROOT):
    rank = bodo.libs.distributed_api.get_rank()
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype, root)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return bcast_comm_impl(data, comm_ranks, nranks, root)


@overload(bcast_comm)
def bcast_comm_overload(data, comm_ranks, nranks, root=MPI_ROOT):
    return lambda data, comm_ranks, nranks, root=MPI_ROOT: bcast_comm_impl(data
        , comm_ranks, nranks, root)


@numba.generated_jit(nopython=True)
def bcast_comm_impl(data, comm_ranks, nranks, root=MPI_ROOT):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.bcast_comm()')
    if isinstance(data, (types.Integer, types.Float)):
        typ_val = numba_to_c_type(data)
        siu__xdug = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        ppv__qtmn = {}
        exec(siu__xdug, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, ppv__qtmn)
        glq__uca = ppv__qtmn['bcast_scalar_impl']
        return glq__uca
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ubo__zdaiq = len(data.columns)
        tdvxq__qljeb = ', '.join('g_data_{}'.format(i) for i in range(
            ubo__zdaiq))
        ohag__ejynx = bodo.utils.transform.gen_const_tup(data.columns)
        siu__xdug = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(ubo__zdaiq):
            siu__xdug += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            siu__xdug += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        siu__xdug += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        siu__xdug += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        siu__xdug += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(tdvxq__qljeb, ohag__ejynx))
        ppv__qtmn = {}
        exec(siu__xdug, {'bodo': bodo}, ppv__qtmn)
        nnqh__kfar = ppv__qtmn['impl_df']
        return nnqh__kfar
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            pnul__iczz = data._step
            uhaxy__qsxdp = data._name
            uhaxy__qsxdp = bcast_scalar(uhaxy__qsxdp, root)
            start = bcast_scalar(start, root)
            stop = bcast_scalar(stop, root)
            pnul__iczz = bcast_scalar(pnul__iczz, root)
            mcl__vply = bodo.libs.array_kernels.calc_nitems(start, stop,
                pnul__iczz)
            chunk_start = bodo.libs.distributed_api.get_start(mcl__vply,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(mcl__vply,
                n_pes, rank)
            pjiu__gfsl = start + pnul__iczz * chunk_start
            pog__fqhgl = start + pnul__iczz * (chunk_start + chunk_count)
            pog__fqhgl = min(pog__fqhgl, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(pjiu__gfsl,
                pog__fqhgl, pnul__iczz, uhaxy__qsxdp)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            jpfzq__xklpo = data._data
            uhaxy__qsxdp = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(jpfzq__xklpo,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, uhaxy__qsxdp)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            uhaxy__qsxdp = bodo.hiframes.pd_series_ext.get_series_name(data)
            oatl__phj = bodo.libs.distributed_api.bcast_comm_impl(uhaxy__qsxdp,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            ngcs__kwmp = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ngcs__kwmp, oatl__phj)
        return impl_series
    if isinstance(data, types.BaseTuple):
        siu__xdug = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        siu__xdug += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        ppv__qtmn = {}
        exec(siu__xdug, {'bcast_comm_impl': bcast_comm_impl}, ppv__qtmn)
        oxjxq__xif = ppv__qtmn['impl_tuple']
        return oxjxq__xif
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    qlszl__fgsi = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    lauve__hqird = (0,) * qlszl__fgsi

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        jpfzq__xklpo = np.ascontiguousarray(data)
        vfv__dbhu = data.ctypes
        nakpt__qrkjj = lauve__hqird
        if rank == root:
            nakpt__qrkjj = jpfzq__xklpo.shape
        nakpt__qrkjj = bcast_tuple(nakpt__qrkjj, root)
        kmtxv__rvaei = get_tuple_prod(nakpt__qrkjj[1:])
        send_counts = nakpt__qrkjj[0] * kmtxv__rvaei
        trojl__pkiaz = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(vfv__dbhu, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(trojl__pkiaz.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return trojl__pkiaz.reshape((-1,) + nakpt__qrkjj[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        lil__meb = MPI.COMM_WORLD
        laz__hpj = MPI.Get_processor_name()
        wws__kdg = lil__meb.allgather(laz__hpj)
        node_ranks = defaultdict(list)
        for i, wjfc__dleea in enumerate(wws__kdg):
            node_ranks[wjfc__dleea].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    lil__meb = MPI.COMM_WORLD
    fyddi__kvo = lil__meb.Get_group()
    hdqx__pxzk = fyddi__kvo.Incl(comm_ranks)
    owq__xlhg = lil__meb.Create_group(hdqx__pxzk)
    return owq__xlhg


def get_nodes_first_ranks():
    yutx__zhjna = get_host_ranks()
    return np.array([meeu__brn[0] for meeu__brn in yutx__zhjna.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
