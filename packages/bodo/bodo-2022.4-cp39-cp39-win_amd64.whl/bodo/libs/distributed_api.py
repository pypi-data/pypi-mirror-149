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
    aging__kyxuc = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, aging__kyxuc, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    aging__kyxuc = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, aging__kyxuc, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            aging__kyxuc = get_type_enum(arr)
            return _isend(arr.ctypes, size, aging__kyxuc, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        aging__kyxuc = np.int32(numba_to_c_type(arr.dtype))
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            ndsz__ily = size + 7 >> 3
            vxla__cgc = _isend(arr._data.ctypes, size, aging__kyxuc, pe,
                tag, cond)
            xlj__nuweu = _isend(arr._null_bitmap.ctypes, ndsz__ily,
                glyl__tra, pe, tag, cond)
            return vxla__cgc, xlj__nuweu
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        xqols__qudk = np.int32(numba_to_c_type(offset_type))
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            blxei__gwx = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(blxei__gwx, pe, tag - 1)
            ndsz__ily = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                xqols__qudk, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), blxei__gwx,
                glyl__tra, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), ndsz__ily,
                glyl__tra, pe, tag)
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
            aging__kyxuc = get_type_enum(arr)
            return _irecv(arr.ctypes, size, aging__kyxuc, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        aging__kyxuc = np.int32(numba_to_c_type(arr.dtype))
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            ndsz__ily = size + 7 >> 3
            vxla__cgc = _irecv(arr._data.ctypes, size, aging__kyxuc, pe,
                tag, cond)
            xlj__nuweu = _irecv(arr._null_bitmap.ctypes, ndsz__ily,
                glyl__tra, pe, tag, cond)
            return vxla__cgc, xlj__nuweu
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        xqols__qudk = np.int32(numba_to_c_type(offset_type))
        glyl__tra = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            drdt__xpdfj = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            drdt__xpdfj = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        doptj__girhh = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {drdt__xpdfj}(size, n_chars)
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
        oxsgo__wqprq = dict()
        exec(doptj__girhh, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            xqols__qudk, 'char_typ_enum': glyl__tra}, oxsgo__wqprq)
        impl = oxsgo__wqprq['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    aging__kyxuc = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), aging__kyxuc)


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
        pph__ekfr = n_pes if rank == root or allgather else 0
        euhj__pgwp = np.empty(pph__ekfr, dtype)
        c_gather_scalar(send.ctypes, euhj__pgwp.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return euhj__pgwp
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
        whqq__admwl = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], whqq__admwl)
        return builder.bitcast(whqq__admwl, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        whqq__admwl = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(whqq__admwl)
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
    vcd__wdcj = types.unliteral(value)
    if isinstance(vcd__wdcj, IndexValueType):
        vcd__wdcj = vcd__wdcj.val_typ
        qct__bbekc = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            qct__bbekc.append(types.int64)
            qct__bbekc.append(bodo.datetime64ns)
            qct__bbekc.append(bodo.timedelta64ns)
            qct__bbekc.append(bodo.datetime_date_type)
        if vcd__wdcj not in qct__bbekc:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(vcd__wdcj))
    typ_enum = np.int32(numba_to_c_type(vcd__wdcj))

    def impl(value, reduce_op):
        sts__kydv = value_to_ptr(value)
        gvbml__aav = value_to_ptr(value)
        _dist_reduce(sts__kydv, gvbml__aav, reduce_op, typ_enum)
        return load_val_ptr(gvbml__aav, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    vcd__wdcj = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(vcd__wdcj))
    inyr__ixpcf = vcd__wdcj(0)

    def impl(value, reduce_op):
        sts__kydv = value_to_ptr(value)
        gvbml__aav = value_to_ptr(inyr__ixpcf)
        _dist_exscan(sts__kydv, gvbml__aav, reduce_op, typ_enum)
        return load_val_ptr(gvbml__aav, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    lhdoi__oiv = 0
    oxanp__fosbc = 0
    for i in range(len(recv_counts)):
        wabtz__crxp = recv_counts[i]
        ndsz__ily = recv_counts_nulls[i]
        cvo__rwjk = tmp_null_bytes[lhdoi__oiv:lhdoi__oiv + ndsz__ily]
        for hpdm__iluku in range(wabtz__crxp):
            set_bit_to(null_bitmap_ptr, oxanp__fosbc, get_bit(cvo__rwjk,
                hpdm__iluku))
            oxanp__fosbc += 1
        lhdoi__oiv += ndsz__ily


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            drc__clgbc = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                drc__clgbc, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            sll__ugwyh = data.size
            recv_counts = gather_scalar(np.int32(sll__ugwyh), allgather,
                root=root)
            tpe__kswxf = recv_counts.sum()
            mwcjk__agjgx = empty_like_type(tpe__kswxf, data)
            aalbc__eemfy = np.empty(1, np.int32)
            if rank == root or allgather:
                aalbc__eemfy = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(sll__ugwyh), mwcjk__agjgx.
                ctypes, recv_counts.ctypes, aalbc__eemfy.ctypes, np.int32(
                typ_val), allgather, np.int32(root))
            return mwcjk__agjgx.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            mwcjk__agjgx = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.str_arr_ext.init_str_arr(mwcjk__agjgx)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            mwcjk__agjgx = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.binary_arr_ext.init_binary_arr(mwcjk__agjgx)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            sll__ugwyh = len(data)
            ndsz__ily = sll__ugwyh + 7 >> 3
            recv_counts = gather_scalar(np.int32(sll__ugwyh), allgather,
                root=root)
            tpe__kswxf = recv_counts.sum()
            mwcjk__agjgx = empty_like_type(tpe__kswxf, data)
            aalbc__eemfy = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            rfwk__muf = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                aalbc__eemfy = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                rfwk__muf = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(sll__ugwyh),
                mwcjk__agjgx._days_data.ctypes, recv_counts.ctypes,
                aalbc__eemfy.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._seconds_data.ctypes, np.int32(sll__ugwyh),
                mwcjk__agjgx._seconds_data.ctypes, recv_counts.ctypes,
                aalbc__eemfy.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(sll__ugwyh),
                mwcjk__agjgx._microseconds_data.ctypes, recv_counts.ctypes,
                aalbc__eemfy.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(ndsz__ily),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, rfwk__muf.
                ctypes, glyl__tra, allgather, np.int32(root))
            copy_gathered_null_bytes(mwcjk__agjgx._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return mwcjk__agjgx
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            sll__ugwyh = len(data)
            ndsz__ily = sll__ugwyh + 7 >> 3
            recv_counts = gather_scalar(np.int32(sll__ugwyh), allgather,
                root=root)
            tpe__kswxf = recv_counts.sum()
            mwcjk__agjgx = empty_like_type(tpe__kswxf, data)
            aalbc__eemfy = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            rfwk__muf = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                aalbc__eemfy = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                rfwk__muf = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(sll__ugwyh), mwcjk__agjgx
                ._data.ctypes, recv_counts.ctypes, aalbc__eemfy.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(ndsz__ily),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, rfwk__muf.
                ctypes, glyl__tra, allgather, np.int32(root))
            copy_gathered_null_bytes(mwcjk__agjgx._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return mwcjk__agjgx
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        cfdku__arsl = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            uzm__jhcac = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                uzm__jhcac, cfdku__arsl)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            cyjf__cakzj = bodo.gatherv(data._left, allgather, warn_if_rep, root
                )
            jzg__bevh = bodo.gatherv(data._right, allgather, warn_if_rep, root)
            return bodo.libs.interval_arr_ext.init_interval_array(cyjf__cakzj,
                jzg__bevh)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            fxyj__kqf = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            blif__wkg = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                blif__wkg, fxyj__kqf)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        tquvy__hjd = np.iinfo(np.int64).max
        cdy__fkdn = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            start = data._start
            stop = data._stop
            if len(data) == 0:
                start = tquvy__hjd
                stop = cdy__fkdn
            start = bodo.libs.distributed_api.dist_reduce(start, np.int32(
                Reduce_Type.Min.value))
            stop = bodo.libs.distributed_api.dist_reduce(stop, np.int32(
                Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if start == tquvy__hjd and stop == cdy__fkdn:
                start = 0
                stop = 0
            cpeb__ydn = max(0, -(-(stop - start) // data._step))
            if cpeb__ydn < total_len:
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
            pfs__fcdvt = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, pfs__fcdvt)
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
            mwcjk__agjgx = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                mwcjk__agjgx, data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        cbdam__ime = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        doptj__girhh = f"""def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        doptj__girhh += '  T = data\n'
        doptj__girhh += '  T2 = init_table(T, True)\n'
        for byk__tosz in data.type_to_blk.values():
            cbdam__ime[f'arr_inds_{byk__tosz}'] = np.array(data.
                block_to_arr_ind[byk__tosz], dtype=np.int64)
            doptj__girhh += (
                f'  arr_list_{byk__tosz} = get_table_block(T, {byk__tosz})\n')
            doptj__girhh += f"""  out_arr_list_{byk__tosz} = alloc_list_like(arr_list_{byk__tosz}, True)
"""
            doptj__girhh += f'  for i in range(len(arr_list_{byk__tosz})):\n'
            doptj__girhh += (
                f'    arr_ind_{byk__tosz} = arr_inds_{byk__tosz}[i]\n')
            doptj__girhh += f"""    ensure_column_unboxed(T, arr_list_{byk__tosz}, i, arr_ind_{byk__tosz})
"""
            doptj__girhh += f"""    out_arr_{byk__tosz} = bodo.gatherv(arr_list_{byk__tosz}[i], allgather, warn_if_rep, root)
"""
            doptj__girhh += (
                f'    out_arr_list_{byk__tosz}[i] = out_arr_{byk__tosz}\n')
            doptj__girhh += (
                f'  T2 = set_table_block(T2, out_arr_list_{byk__tosz}, {byk__tosz})\n'
                )
        doptj__girhh += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        doptj__girhh += f'  T2 = set_table_len(T2, length)\n'
        doptj__girhh += f'  return T2\n'
        oxsgo__wqprq = {}
        exec(doptj__girhh, cbdam__ime, oxsgo__wqprq)
        zhh__crvnw = oxsgo__wqprq['impl_table']
        return zhh__crvnw
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        bxkux__jukvm = len(data.columns)
        if bxkux__jukvm == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                ttcl__xmph = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    ttcl__xmph, ())
            return impl
        fgdpq__eqgoo = ', '.join(f'g_data_{i}' for i in range(bxkux__jukvm))
        irlgp__dgh = bodo.utils.transform.gen_const_tup(data.columns)
        doptj__girhh = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            hviy__qld = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            cbdam__ime = {'bodo': bodo, 'df_type': hviy__qld}
            fgdpq__eqgoo = 'T2'
            irlgp__dgh = 'df_type'
            doptj__girhh += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            doptj__girhh += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            cbdam__ime = {'bodo': bodo}
            for i in range(bxkux__jukvm):
                doptj__girhh += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                doptj__girhh += (
                    """  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)
"""
                    .format(i, i))
        doptj__girhh += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        doptj__girhh += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        doptj__girhh += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(fgdpq__eqgoo, irlgp__dgh))
        oxsgo__wqprq = {}
        exec(doptj__girhh, cbdam__ime, oxsgo__wqprq)
        gwv__ddnrw = oxsgo__wqprq['impl_df']
        return gwv__ddnrw
    if isinstance(data, ArrayItemArrayType):
        pkbu__sfpnh = np.int32(numba_to_c_type(types.int32))
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            lhsge__mlgp = bodo.libs.array_item_arr_ext.get_offsets(data)
            stmwl__cjtcu = bodo.libs.array_item_arr_ext.get_data(data)
            stmwl__cjtcu = stmwl__cjtcu[:lhsge__mlgp[-1]]
            qfgbs__ifsw = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            sll__ugwyh = len(data)
            jtzw__xocvl = np.empty(sll__ugwyh, np.uint32)
            ndsz__ily = sll__ugwyh + 7 >> 3
            for i in range(sll__ugwyh):
                jtzw__xocvl[i] = lhsge__mlgp[i + 1] - lhsge__mlgp[i]
            recv_counts = gather_scalar(np.int32(sll__ugwyh), allgather,
                root=root)
            tpe__kswxf = recv_counts.sum()
            aalbc__eemfy = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            rfwk__muf = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                aalbc__eemfy = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for hiz__dyo in range(len(recv_counts)):
                    recv_counts_nulls[hiz__dyo] = recv_counts[hiz__dyo
                        ] + 7 >> 3
                rfwk__muf = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            dcx__tgz = np.empty(tpe__kswxf + 1, np.uint32)
            afe__qqwpz = bodo.gatherv(stmwl__cjtcu, allgather, warn_if_rep,
                root)
            pbh__kvrcl = np.empty(tpe__kswxf + 7 >> 3, np.uint8)
            c_gatherv(jtzw__xocvl.ctypes, np.int32(sll__ugwyh), dcx__tgz.
                ctypes, recv_counts.ctypes, aalbc__eemfy.ctypes,
                pkbu__sfpnh, allgather, np.int32(root))
            c_gatherv(qfgbs__ifsw.ctypes, np.int32(ndsz__ily),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, rfwk__muf.
                ctypes, glyl__tra, allgather, np.int32(root))
            dummy_use(data)
            wzsx__gat = np.empty(tpe__kswxf + 1, np.uint64)
            convert_len_arr_to_offset(dcx__tgz.ctypes, wzsx__gat.ctypes,
                tpe__kswxf)
            copy_gathered_null_bytes(pbh__kvrcl.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                tpe__kswxf, afe__qqwpz, wzsx__gat, pbh__kvrcl)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        eiq__iviy = data.names
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            cqd__ujb = bodo.libs.struct_arr_ext.get_data(data)
            rwre__icwzz = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            hncux__lyig = bodo.gatherv(cqd__ujb, allgather=allgather, root=root
                )
            rank = bodo.libs.distributed_api.get_rank()
            sll__ugwyh = len(data)
            ndsz__ily = sll__ugwyh + 7 >> 3
            recv_counts = gather_scalar(np.int32(sll__ugwyh), allgather,
                root=root)
            tpe__kswxf = recv_counts.sum()
            jksy__ysgw = np.empty(tpe__kswxf + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            rfwk__muf = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                rfwk__muf = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(rwre__icwzz.ctypes, np.int32(ndsz__ily),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, rfwk__muf.
                ctypes, glyl__tra, allgather, np.int32(root))
            copy_gathered_null_bytes(jksy__ysgw.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(hncux__lyig,
                jksy__ysgw, eiq__iviy)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            mwcjk__agjgx = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.binary_arr_ext.init_binary_arr(mwcjk__agjgx)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            mwcjk__agjgx = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(mwcjk__agjgx)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            mwcjk__agjgx = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.map_arr_ext.init_map_arr(mwcjk__agjgx)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            mwcjk__agjgx = bodo.gatherv(data.data, allgather, warn_if_rep, root
                )
            ddqjx__sojai = bodo.gatherv(data.indices, allgather,
                warn_if_rep, root)
            vqgz__jsazb = bodo.gatherv(data.indptr, allgather, warn_if_rep,
                root)
            ikct__jal = gather_scalar(data.shape[0], allgather, root=root)
            nvgx__caxt = ikct__jal.sum()
            bxkux__jukvm = bodo.libs.distributed_api.dist_reduce(data.shape
                [1], np.int32(Reduce_Type.Max.value))
            nyn__oboip = np.empty(nvgx__caxt + 1, np.int64)
            ddqjx__sojai = ddqjx__sojai.astype(np.int64)
            nyn__oboip[0] = 0
            gzexd__iai = 1
            bvzl__rprf = 0
            for bud__mugvw in ikct__jal:
                for eoejq__ubhzt in range(bud__mugvw):
                    qhg__pkdt = vqgz__jsazb[bvzl__rprf + 1] - vqgz__jsazb[
                        bvzl__rprf]
                    nyn__oboip[gzexd__iai] = nyn__oboip[gzexd__iai - 1
                        ] + qhg__pkdt
                    gzexd__iai += 1
                    bvzl__rprf += 1
                bvzl__rprf += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(mwcjk__agjgx,
                ddqjx__sojai, nyn__oboip, (nvgx__caxt, bxkux__jukvm))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        doptj__girhh = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        doptj__girhh += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        oxsgo__wqprq = {}
        exec(doptj__girhh, {'bodo': bodo}, oxsgo__wqprq)
        aeipw__cdl = oxsgo__wqprq['impl_tuple']
        return aeipw__cdl
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    doptj__girhh = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    doptj__girhh += '    if random:\n'
    doptj__girhh += '        if random_seed is None:\n'
    doptj__girhh += '            random = 1\n'
    doptj__girhh += '        else:\n'
    doptj__girhh += '            random = 2\n'
    doptj__girhh += '    if random_seed is None:\n'
    doptj__girhh += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        qkejs__yayg = data
        bxkux__jukvm = len(qkejs__yayg.columns)
        for i in range(bxkux__jukvm):
            doptj__girhh += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        doptj__girhh += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        fgdpq__eqgoo = ', '.join(f'data_{i}' for i in range(bxkux__jukvm))
        doptj__girhh += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(upe__ufum) for
            upe__ufum in range(bxkux__jukvm))))
        doptj__girhh += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        doptj__girhh += '    if dests is None:\n'
        doptj__girhh += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        doptj__girhh += '    else:\n'
        doptj__girhh += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for qtrdp__ekhzr in range(bxkux__jukvm):
            doptj__girhh += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(qtrdp__ekhzr))
        doptj__girhh += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(bxkux__jukvm))
        doptj__girhh += '    delete_table(out_table)\n'
        doptj__girhh += '    if parallel:\n'
        doptj__girhh += '        delete_table(table_total)\n'
        fgdpq__eqgoo = ', '.join('out_arr_{}'.format(i) for i in range(
            bxkux__jukvm))
        irlgp__dgh = bodo.utils.transform.gen_const_tup(qkejs__yayg.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        doptj__girhh += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(fgdpq__eqgoo, index, irlgp__dgh))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        doptj__girhh += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        doptj__girhh += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        doptj__girhh += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        doptj__girhh += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        doptj__girhh += '    if dests is None:\n'
        doptj__girhh += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        doptj__girhh += '    else:\n'
        doptj__girhh += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        doptj__girhh += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        doptj__girhh += """    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)
"""
        doptj__girhh += '    delete_table(out_table)\n'
        doptj__girhh += '    if parallel:\n'
        doptj__girhh += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        doptj__girhh += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        doptj__girhh += '    if not parallel:\n'
        doptj__girhh += '        return data\n'
        doptj__girhh += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        doptj__girhh += '    if dests is None:\n'
        doptj__girhh += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        doptj__girhh += '    elif bodo.get_rank() not in dests:\n'
        doptj__girhh += '        dim0_local_size = 0\n'
        doptj__girhh += '    else:\n'
        doptj__girhh += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        doptj__girhh += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        doptj__girhh += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        doptj__girhh += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        doptj__girhh += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        doptj__girhh += '    if dests is None:\n'
        doptj__girhh += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        doptj__girhh += '    else:\n'
        doptj__girhh += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        doptj__girhh += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        doptj__girhh += '    delete_table(out_table)\n'
        doptj__girhh += '    if parallel:\n'
        doptj__girhh += '        delete_table(table_total)\n'
        doptj__girhh += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    oxsgo__wqprq = {}
    exec(doptj__girhh, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table},
        oxsgo__wqprq)
    impl = oxsgo__wqprq['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    doptj__girhh = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        doptj__girhh += '    if seed is None:\n'
        doptj__girhh += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        doptj__girhh += '    np.random.seed(seed)\n'
        doptj__girhh += '    if not parallel:\n'
        doptj__girhh += '        data = data.copy()\n'
        doptj__girhh += '        np.random.shuffle(data)\n'
        doptj__girhh += '        return data\n'
        doptj__girhh += '    else:\n'
        doptj__girhh += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        doptj__girhh += '        permutation = np.arange(dim0_global_size)\n'
        doptj__girhh += '        np.random.shuffle(permutation)\n'
        doptj__girhh += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        doptj__girhh += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        doptj__girhh += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        doptj__girhh += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        doptj__girhh += '        return output\n'
    else:
        doptj__girhh += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    oxsgo__wqprq = {}
    exec(doptj__girhh, {'np': np, 'bodo': bodo}, oxsgo__wqprq)
    impl = oxsgo__wqprq['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    hyjd__avppa = np.empty(sendcounts_nulls.sum(), np.uint8)
    lhdoi__oiv = 0
    oxanp__fosbc = 0
    for tsq__rwjx in range(len(sendcounts)):
        wabtz__crxp = sendcounts[tsq__rwjx]
        ndsz__ily = sendcounts_nulls[tsq__rwjx]
        cvo__rwjk = hyjd__avppa[lhdoi__oiv:lhdoi__oiv + ndsz__ily]
        for hpdm__iluku in range(wabtz__crxp):
            set_bit_to_arr(cvo__rwjk, hpdm__iluku, get_bit_bitmap(
                null_bitmap_ptr, oxanp__fosbc))
            oxanp__fosbc += 1
        lhdoi__oiv += ndsz__ily
    return hyjd__avppa


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    dkbjo__abqjn = MPI.COMM_WORLD
    data = dkbjo__abqjn.bcast(data, root)
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
    hepxq__mzod = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    twaqc__fwlpc = (0,) * hepxq__mzod

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        oyald__fpgjx = np.ascontiguousarray(data)
        vyvaz__rogh = data.ctypes
        dtt__mzmky = twaqc__fwlpc
        if rank == MPI_ROOT:
            dtt__mzmky = oyald__fpgjx.shape
        dtt__mzmky = bcast_tuple(dtt__mzmky)
        yegnl__uoyzj = get_tuple_prod(dtt__mzmky[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            dtt__mzmky[0])
        send_counts *= yegnl__uoyzj
        sll__ugwyh = send_counts[rank]
        ossqc__sfnlp = np.empty(sll__ugwyh, dtype)
        aalbc__eemfy = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(vyvaz__rogh, send_counts.ctypes, aalbc__eemfy.ctypes,
            ossqc__sfnlp.ctypes, np.int32(sll__ugwyh), np.int32(typ_val))
        return ossqc__sfnlp.reshape((-1,) + dtt__mzmky[1:])
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
        gqh__baaj = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], gqh__baaj)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        fxyj__kqf = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=fxyj__kqf)
        rhuk__diej = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(rhuk__diej)
        return pd.Index(arr, name=fxyj__kqf)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        fxyj__kqf = _get_name_value_for_type(dtype.name_typ)
        eiq__iviy = tuple(_get_name_value_for_type(t) for t in dtype.names_typ)
        srfug__etn = tuple(get_value_for_type(t) for t in dtype.array_types)
        srfug__etn = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in srfug__etn)
        val = pd.MultiIndex.from_arrays(srfug__etn, names=eiq__iviy)
        val.name = fxyj__kqf
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        fxyj__kqf = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=fxyj__kqf)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        srfug__etn = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({fxyj__kqf: arr for fxyj__kqf, arr in zip(dtype
            .columns, srfug__etn)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        rhuk__diej = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(rhuk__diej[0],
            rhuk__diej[0])])
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
        pkbu__sfpnh = np.int32(numba_to_c_type(types.int32))
        glyl__tra = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            drdt__xpdfj = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            drdt__xpdfj = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        doptj__girhh = f"""def impl(
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
            recv_arr = {drdt__xpdfj}(n_loc, n_loc_char)

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
        oxsgo__wqprq = dict()
        exec(doptj__girhh, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            pkbu__sfpnh, 'char_typ_enum': glyl__tra, 'decode_if_dict_array':
            decode_if_dict_array}, oxsgo__wqprq)
        impl = oxsgo__wqprq['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        pkbu__sfpnh = np.int32(numba_to_c_type(types.int32))
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            ucfh__eiunj = bodo.libs.array_item_arr_ext.get_offsets(data)
            mui__iyua = bodo.libs.array_item_arr_ext.get_data(data)
            mui__iyua = mui__iyua[:ucfh__eiunj[-1]]
            nqhzs__tgw = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            fjpkf__haekk = bcast_scalar(len(data))
            noak__yap = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                noak__yap[i] = ucfh__eiunj[i + 1] - ucfh__eiunj[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                fjpkf__haekk)
            aalbc__eemfy = bodo.ir.join.calc_disp(send_counts)
            epavg__xqqox = np.empty(n_pes, np.int32)
            if rank == 0:
                vch__zfc = 0
                for i in range(n_pes):
                    are__xfsf = 0
                    for eoejq__ubhzt in range(send_counts[i]):
                        are__xfsf += noak__yap[vch__zfc]
                        vch__zfc += 1
                    epavg__xqqox[i] = are__xfsf
            bcast(epavg__xqqox)
            vyo__xvqac = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                vyo__xvqac[i] = send_counts[i] + 7 >> 3
            rfwk__muf = bodo.ir.join.calc_disp(vyo__xvqac)
            sll__ugwyh = send_counts[rank]
            wjfm__zwuz = np.empty(sll__ugwyh + 1, np_offset_type)
            bbvt__xgut = bodo.libs.distributed_api.scatterv_impl(mui__iyua,
                epavg__xqqox)
            kwbb__hsc = sll__ugwyh + 7 >> 3
            jvn__tna = np.empty(kwbb__hsc, np.uint8)
            mdvf__bwgg = np.empty(sll__ugwyh, np.uint32)
            c_scatterv(noak__yap.ctypes, send_counts.ctypes, aalbc__eemfy.
                ctypes, mdvf__bwgg.ctypes, np.int32(sll__ugwyh), pkbu__sfpnh)
            convert_len_arr_to_offset(mdvf__bwgg.ctypes, wjfm__zwuz.ctypes,
                sll__ugwyh)
            mujud__eajf = get_scatter_null_bytes_buff(nqhzs__tgw.ctypes,
                send_counts, vyo__xvqac)
            c_scatterv(mujud__eajf.ctypes, vyo__xvqac.ctypes, rfwk__muf.
                ctypes, jvn__tna.ctypes, np.int32(kwbb__hsc), glyl__tra)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                sll__ugwyh, bbvt__xgut, wjfm__zwuz, jvn__tna)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        glyl__tra = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            ojwvs__ewx = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            ojwvs__ewx = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            ojwvs__ewx = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            ojwvs__ewx = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            oyald__fpgjx = data._data
            rwre__icwzz = data._null_bitmap
            rqsyi__pbll = len(oyald__fpgjx)
            fjq__cfjel = _scatterv_np(oyald__fpgjx, send_counts)
            fjpkf__haekk = bcast_scalar(rqsyi__pbll)
            mou__ckrzi = len(fjq__cfjel) + 7 >> 3
            tfo__meji = np.empty(mou__ckrzi, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                fjpkf__haekk)
            vyo__xvqac = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                vyo__xvqac[i] = send_counts[i] + 7 >> 3
            rfwk__muf = bodo.ir.join.calc_disp(vyo__xvqac)
            mujud__eajf = get_scatter_null_bytes_buff(rwre__icwzz.ctypes,
                send_counts, vyo__xvqac)
            c_scatterv(mujud__eajf.ctypes, vyo__xvqac.ctypes, rfwk__muf.
                ctypes, tfo__meji.ctypes, np.int32(mou__ckrzi), glyl__tra)
            return ojwvs__ewx(fjq__cfjel, tfo__meji)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            mexnq__hkhfe = bodo.libs.distributed_api.scatterv_impl(data.
                _left, send_counts)
            jsqf__shn = bodo.libs.distributed_api.scatterv_impl(data._right,
                send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(mexnq__hkhfe,
                jsqf__shn)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            hjpva__fahgi = data._step
            fxyj__kqf = data._name
            fxyj__kqf = bcast_scalar(fxyj__kqf)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            hjpva__fahgi = bcast_scalar(hjpva__fahgi)
            pqeb__abpxq = bodo.libs.array_kernels.calc_nitems(start, stop,
                hjpva__fahgi)
            chunk_start = bodo.libs.distributed_api.get_start(pqeb__abpxq,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(
                pqeb__abpxq, n_pes, rank)
            ckch__mot = start + hjpva__fahgi * chunk_start
            vbe__uxyq = start + hjpva__fahgi * (chunk_start + chunk_count)
            vbe__uxyq = min(vbe__uxyq, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(ckch__mot,
                vbe__uxyq, hjpva__fahgi, fxyj__kqf)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        pfs__fcdvt = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            oyald__fpgjx = data._data
            fxyj__kqf = data._name
            fxyj__kqf = bcast_scalar(fxyj__kqf)
            arr = bodo.libs.distributed_api.scatterv_impl(oyald__fpgjx,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                fxyj__kqf, pfs__fcdvt)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            oyald__fpgjx = data._data
            fxyj__kqf = data._name
            fxyj__kqf = bcast_scalar(fxyj__kqf)
            arr = bodo.libs.distributed_api.scatterv_impl(oyald__fpgjx,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, fxyj__kqf)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            mwcjk__agjgx = bodo.libs.distributed_api.scatterv_impl(data.
                _data, send_counts)
            fxyj__kqf = bcast_scalar(data._name)
            eiq__iviy = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                mwcjk__agjgx, eiq__iviy, fxyj__kqf)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            fxyj__kqf = bodo.hiframes.pd_series_ext.get_series_name(data)
            zeeed__mdza = bcast_scalar(fxyj__kqf)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            blif__wkg = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                blif__wkg, zeeed__mdza)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        bxkux__jukvm = len(data.columns)
        fgdpq__eqgoo = ', '.join('g_data_{}'.format(i) for i in range(
            bxkux__jukvm))
        irlgp__dgh = bodo.utils.transform.gen_const_tup(data.columns)
        doptj__girhh = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        for i in range(bxkux__jukvm):
            doptj__girhh += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            doptj__girhh += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        doptj__girhh += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        doptj__girhh += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        doptj__girhh += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(fgdpq__eqgoo, irlgp__dgh))
        oxsgo__wqprq = {}
        exec(doptj__girhh, {'bodo': bodo}, oxsgo__wqprq)
        gwv__ddnrw = oxsgo__wqprq['impl_df']
        return gwv__ddnrw
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            drc__clgbc = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                drc__clgbc, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        doptj__girhh = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        doptj__girhh += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        oxsgo__wqprq = {}
        exec(doptj__girhh, {'bodo': bodo}, oxsgo__wqprq)
        aeipw__cdl = oxsgo__wqprq['impl_tuple']
        return aeipw__cdl
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
        xqols__qudk = np.int32(numba_to_c_type(offset_type))
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            sll__ugwyh = len(data)
            mevj__kzxiw = num_total_chars(data)
            assert sll__ugwyh < INT_MAX
            assert mevj__kzxiw < INT_MAX
            tbsbo__ige = get_offset_ptr(data)
            vyvaz__rogh = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            ndsz__ily = sll__ugwyh + 7 >> 3
            c_bcast(tbsbo__ige, np.int32(sll__ugwyh + 1), xqols__qudk, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(vyvaz__rogh, np.int32(mevj__kzxiw), glyl__tra, np.array
                ([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(ndsz__ily), glyl__tra, np.
                array([-1]).ctypes, 0, np.int32(root))
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
        glyl__tra = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                pbqt__hzyw = 0
                jawei__sywj = np.empty(0, np.uint8).ctypes
            else:
                jawei__sywj, pbqt__hzyw = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            pbqt__hzyw = bodo.libs.distributed_api.bcast_scalar(pbqt__hzyw,
                root)
            if rank != root:
                miuv__gcqsm = np.empty(pbqt__hzyw + 1, np.uint8)
                miuv__gcqsm[pbqt__hzyw] = 0
                jawei__sywj = miuv__gcqsm.ctypes
            c_bcast(jawei__sywj, np.int32(pbqt__hzyw), glyl__tra, np.array(
                [-1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(jawei__sywj, pbqt__hzyw)
        return impl_str
    typ_val = numba_to_c_type(val)
    doptj__girhh = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    oxsgo__wqprq = {}
    exec(doptj__girhh, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, oxsgo__wqprq)
    hkoce__znbmk = oxsgo__wqprq['bcast_scalar_impl']
    return hkoce__znbmk


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    sgny__lyu = len(val)
    doptj__girhh = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    doptj__girhh += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(sgny__lyu)),
        ',' if sgny__lyu else '')
    oxsgo__wqprq = {}
    exec(doptj__girhh, {'bcast_scalar': bcast_scalar}, oxsgo__wqprq)
    uvhks__vuug = oxsgo__wqprq['bcast_tuple_impl']
    return uvhks__vuug


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            sll__ugwyh = bcast_scalar(len(arr), root)
            ekxpi__kyjp = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(sll__ugwyh, ekxpi__kyjp)
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
        hjpva__fahgi = slice_index.step
        ztavm__yqdcg = 0 if hjpva__fahgi == 1 or start > arr_start else abs(
            hjpva__fahgi - arr_start % hjpva__fahgi) % hjpva__fahgi
        ckch__mot = max(arr_start, slice_index.start
            ) - arr_start + ztavm__yqdcg
        vbe__uxyq = max(slice_index.stop - arr_start, 0)
        return slice(ckch__mot, vbe__uxyq, hjpva__fahgi)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        xszte__vvfnt = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[xszte__vvfnt])
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
        iawbd__nnzl = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        glyl__tra = np.int32(numba_to_c_type(types.uint8))
        vswb__evwax = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            srtsb__gjtn = np.int32(10)
            tag = np.int32(11)
            nkb__lio = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                stmwl__cjtcu = arr._data
                fpy__bsra = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    stmwl__cjtcu, ind)
                lyi__zdgr = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    stmwl__cjtcu, ind + 1)
                length = lyi__zdgr - fpy__bsra
                whqq__admwl = stmwl__cjtcu[ind]
                nkb__lio[0] = length
                isend(nkb__lio, np.int32(1), root, srtsb__gjtn, True)
                isend(whqq__admwl, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                vswb__evwax, iawbd__nnzl, 0, 1)
            cpeb__ydn = 0
            if rank == root:
                cpeb__ydn = recv(np.int64, ANY_SOURCE, srtsb__gjtn)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    vswb__evwax, iawbd__nnzl, cpeb__ydn, 1)
                vyvaz__rogh = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(vyvaz__rogh, np.int32(cpeb__ydn), glyl__tra,
                    ANY_SOURCE, tag)
            dummy_use(nkb__lio)
            cpeb__ydn = bcast_scalar(cpeb__ydn)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    vswb__evwax, iawbd__nnzl, cpeb__ydn, 1)
            vyvaz__rogh = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(vyvaz__rogh, np.int32(cpeb__ydn), glyl__tra, np.array([
                -1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, cpeb__ydn)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        vlp__exbo = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, vlp__exbo)
            if arr_start <= ind < arr_start + len(arr):
                drc__clgbc = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = drc__clgbc[ind - arr_start]
                send_arr = np.full(1, data, vlp__exbo)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = vlp__exbo(-1)
            if rank == root:
                val = recv(vlp__exbo, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            kswqs__hka = arr.dtype.categories[max(val, 0)]
            return kswqs__hka
        return cat_getitem_impl
    zsrce__tvsp = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, zsrce__tvsp)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, zsrce__tvsp)[0]
        if rank == root:
            val = recv(zsrce__tvsp, ANY_SOURCE, tag)
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
    kut__hdam = get_type_enum(out_data)
    assert typ_enum == kut__hdam
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
    doptj__girhh = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        doptj__girhh += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    doptj__girhh += '  return\n'
    oxsgo__wqprq = {}
    exec(doptj__girhh, {'alltoallv': alltoallv}, oxsgo__wqprq)
    odowb__mkmld = oxsgo__wqprq['f']
    return odowb__mkmld


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    start = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return start, count


@numba.njit
def get_start(total_size, pes, rank):
    euhj__pgwp = total_size % pes
    gzqy__mbe = (total_size - euhj__pgwp) // pes
    return rank * gzqy__mbe + min(rank, euhj__pgwp)


@numba.njit
def get_end(total_size, pes, rank):
    euhj__pgwp = total_size % pes
    gzqy__mbe = (total_size - euhj__pgwp) // pes
    return (rank + 1) * gzqy__mbe + min(rank + 1, euhj__pgwp)


@numba.njit
def get_node_portion(total_size, pes, rank):
    euhj__pgwp = total_size % pes
    gzqy__mbe = (total_size - euhj__pgwp) // pes
    if rank < euhj__pgwp:
        return gzqy__mbe + 1
    else:
        return gzqy__mbe


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    inyr__ixpcf = in_arr.dtype(0)
    xygh__joii = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        are__xfsf = inyr__ixpcf
        for kacrc__gjmq in np.nditer(in_arr):
            are__xfsf += kacrc__gjmq.item()
        cythg__godm = dist_exscan(are__xfsf, xygh__joii)
        for i in range(in_arr.size):
            cythg__godm += in_arr[i]
            out_arr[i] = cythg__godm
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    ctlk__xwhg = in_arr.dtype(1)
    xygh__joii = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        are__xfsf = ctlk__xwhg
        for kacrc__gjmq in np.nditer(in_arr):
            are__xfsf *= kacrc__gjmq.item()
        cythg__godm = dist_exscan(are__xfsf, xygh__joii)
        if get_rank() == 0:
            cythg__godm = ctlk__xwhg
        for i in range(in_arr.size):
            cythg__godm *= in_arr[i]
            out_arr[i] = cythg__godm
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        ctlk__xwhg = np.finfo(in_arr.dtype(1).dtype).max
    else:
        ctlk__xwhg = np.iinfo(in_arr.dtype(1).dtype).max
    xygh__joii = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        are__xfsf = ctlk__xwhg
        for kacrc__gjmq in np.nditer(in_arr):
            are__xfsf = min(are__xfsf, kacrc__gjmq.item())
        cythg__godm = dist_exscan(are__xfsf, xygh__joii)
        if get_rank() == 0:
            cythg__godm = ctlk__xwhg
        for i in range(in_arr.size):
            cythg__godm = min(cythg__godm, in_arr[i])
            out_arr[i] = cythg__godm
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        ctlk__xwhg = np.finfo(in_arr.dtype(1).dtype).min
    else:
        ctlk__xwhg = np.iinfo(in_arr.dtype(1).dtype).min
    ctlk__xwhg = in_arr.dtype(1)
    xygh__joii = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        are__xfsf = ctlk__xwhg
        for kacrc__gjmq in np.nditer(in_arr):
            are__xfsf = max(are__xfsf, kacrc__gjmq.item())
        cythg__godm = dist_exscan(are__xfsf, xygh__joii)
        if get_rank() == 0:
            cythg__godm = ctlk__xwhg
        for i in range(in_arr.size):
            cythg__godm = max(cythg__godm, in_arr[i])
            out_arr[i] = cythg__godm
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    aging__kyxuc = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), aging__kyxuc)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    fykqj__ivxrc = args[0]
    if equiv_set.has_shape(fykqj__ivxrc):
        return ArrayAnalysis.AnalyzeResult(shape=fykqj__ivxrc, pre=[])
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
        vlse__wdwmo = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        doptj__girhh = 'def f(req, cond=True):\n'
        doptj__girhh += f'  return {vlse__wdwmo}\n'
        oxsgo__wqprq = {}
        exec(doptj__girhh, {'_wait': _wait}, oxsgo__wqprq)
        impl = oxsgo__wqprq['f']
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
    ckch__mot = max(start, chunk_start)
    vbe__uxyq = min(stop, chunk_start + chunk_count)
    tqwdg__eabkh = ckch__mot - chunk_start
    htgv__vqw = vbe__uxyq - chunk_start
    if tqwdg__eabkh < 0 or htgv__vqw < 0:
        tqwdg__eabkh = 1
        htgv__vqw = 0
    return tqwdg__eabkh, htgv__vqw


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
        euhj__pgwp = 1
        for a in t:
            euhj__pgwp *= a
        return euhj__pgwp
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    jjotf__ryrdl = np.ascontiguousarray(in_arr)
    yqjq__npuv = get_tuple_prod(jjotf__ryrdl.shape[1:])
    siil__hmefm = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        ezen__yzpwx = np.array(dest_ranks, dtype=np.int32)
    else:
        ezen__yzpwx = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, jjotf__ryrdl.ctypes,
        new_dim0_global_len, len(in_arr), dtype_size * siil__hmefm, 
        dtype_size * yqjq__npuv, len(ezen__yzpwx), ezen__yzpwx.ctypes)
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
    genur__otzi = np.ascontiguousarray(rhs)
    ytddj__ilyd = get_tuple_prod(genur__otzi.shape[1:])
    icao__hyn = dtype_size * ytddj__ilyd
    permutation_array_index(lhs.ctypes, lhs_len, icao__hyn, genur__otzi.
        ctypes, genur__otzi.shape[0], p.ctypes, p_len)
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
        doptj__girhh = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        oxsgo__wqprq = {}
        exec(doptj__girhh, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, oxsgo__wqprq)
        hkoce__znbmk = oxsgo__wqprq['bcast_scalar_impl']
        return hkoce__znbmk
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        bxkux__jukvm = len(data.columns)
        fgdpq__eqgoo = ', '.join('g_data_{}'.format(i) for i in range(
            bxkux__jukvm))
        irlgp__dgh = bodo.utils.transform.gen_const_tup(data.columns)
        doptj__girhh = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(bxkux__jukvm):
            doptj__girhh += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            doptj__girhh += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        doptj__girhh += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        doptj__girhh += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        doptj__girhh += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(fgdpq__eqgoo, irlgp__dgh))
        oxsgo__wqprq = {}
        exec(doptj__girhh, {'bodo': bodo}, oxsgo__wqprq)
        gwv__ddnrw = oxsgo__wqprq['impl_df']
        return gwv__ddnrw
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            hjpva__fahgi = data._step
            fxyj__kqf = data._name
            fxyj__kqf = bcast_scalar(fxyj__kqf, root)
            start = bcast_scalar(start, root)
            stop = bcast_scalar(stop, root)
            hjpva__fahgi = bcast_scalar(hjpva__fahgi, root)
            pqeb__abpxq = bodo.libs.array_kernels.calc_nitems(start, stop,
                hjpva__fahgi)
            chunk_start = bodo.libs.distributed_api.get_start(pqeb__abpxq,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(
                pqeb__abpxq, n_pes, rank)
            ckch__mot = start + hjpva__fahgi * chunk_start
            vbe__uxyq = start + hjpva__fahgi * (chunk_start + chunk_count)
            vbe__uxyq = min(vbe__uxyq, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(ckch__mot,
                vbe__uxyq, hjpva__fahgi, fxyj__kqf)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            oyald__fpgjx = data._data
            fxyj__kqf = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(oyald__fpgjx,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, fxyj__kqf)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            fxyj__kqf = bodo.hiframes.pd_series_ext.get_series_name(data)
            zeeed__mdza = bodo.libs.distributed_api.bcast_comm_impl(fxyj__kqf,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            blif__wkg = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                blif__wkg, zeeed__mdza)
        return impl_series
    if isinstance(data, types.BaseTuple):
        doptj__girhh = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        doptj__girhh += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        oxsgo__wqprq = {}
        exec(doptj__girhh, {'bcast_comm_impl': bcast_comm_impl}, oxsgo__wqprq)
        aeipw__cdl = oxsgo__wqprq['impl_tuple']
        return aeipw__cdl
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    hepxq__mzod = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    twaqc__fwlpc = (0,) * hepxq__mzod

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        oyald__fpgjx = np.ascontiguousarray(data)
        vyvaz__rogh = data.ctypes
        dtt__mzmky = twaqc__fwlpc
        if rank == root:
            dtt__mzmky = oyald__fpgjx.shape
        dtt__mzmky = bcast_tuple(dtt__mzmky, root)
        yegnl__uoyzj = get_tuple_prod(dtt__mzmky[1:])
        send_counts = dtt__mzmky[0] * yegnl__uoyzj
        ossqc__sfnlp = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(vyvaz__rogh, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(ossqc__sfnlp.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return ossqc__sfnlp.reshape((-1,) + dtt__mzmky[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        dkbjo__abqjn = MPI.COMM_WORLD
        gcvwe__nlt = MPI.Get_processor_name()
        ltnmn__bow = dkbjo__abqjn.allgather(gcvwe__nlt)
        node_ranks = defaultdict(list)
        for i, vkj__avspi in enumerate(ltnmn__bow):
            node_ranks[vkj__avspi].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    dkbjo__abqjn = MPI.COMM_WORLD
    dgpz__vxwap = dkbjo__abqjn.Get_group()
    ajc__xyc = dgpz__vxwap.Incl(comm_ranks)
    yhr__dbm = dkbjo__abqjn.Create_group(ajc__xyc)
    return yhr__dbm


def get_nodes_first_ranks():
    xpcg__zwag = get_host_ranks()
    return np.array([fatu__ppkd[0] for fatu__ppkd in xpcg__zwag.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
