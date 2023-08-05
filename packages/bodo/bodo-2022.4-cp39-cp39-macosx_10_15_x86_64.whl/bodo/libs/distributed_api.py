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
    gpn__vkq = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, gpn__vkq, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    gpn__vkq = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, gpn__vkq, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            gpn__vkq = get_type_enum(arr)
            return _isend(arr.ctypes, size, gpn__vkq, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        gpn__vkq = np.int32(numba_to_c_type(arr.dtype))
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            cye__hbjuk = size + 7 >> 3
            uzxcf__ttem = _isend(arr._data.ctypes, size, gpn__vkq, pe, tag,
                cond)
            zwu__zvc = _isend(arr._null_bitmap.ctypes, cye__hbjuk,
                nzbl__qnzy, pe, tag, cond)
            return uzxcf__ttem, zwu__zvc
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        spf__vzg = np.int32(numba_to_c_type(offset_type))
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            otjr__ivky = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(otjr__ivky, pe, tag - 1)
            cye__hbjuk = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                spf__vzg, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), otjr__ivky,
                nzbl__qnzy, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                cye__hbjuk, nzbl__qnzy, pe, tag)
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
            gpn__vkq = get_type_enum(arr)
            return _irecv(arr.ctypes, size, gpn__vkq, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        gpn__vkq = np.int32(numba_to_c_type(arr.dtype))
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            cye__hbjuk = size + 7 >> 3
            uzxcf__ttem = _irecv(arr._data.ctypes, size, gpn__vkq, pe, tag,
                cond)
            zwu__zvc = _irecv(arr._null_bitmap.ctypes, cye__hbjuk,
                nzbl__qnzy, pe, tag, cond)
            return uzxcf__ttem, zwu__zvc
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        spf__vzg = np.int32(numba_to_c_type(offset_type))
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            sklra__tbhng = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            sklra__tbhng = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        omck__xwc = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {sklra__tbhng}(size, n_chars)
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
        ossv__aaoc = dict()
        exec(omck__xwc, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            spf__vzg, 'char_typ_enum': nzbl__qnzy}, ossv__aaoc)
        impl = ossv__aaoc['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    gpn__vkq = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), gpn__vkq)


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
        wgh__kcew = n_pes if rank == root or allgather else 0
        iupk__mxr = np.empty(wgh__kcew, dtype)
        c_gather_scalar(send.ctypes, iupk__mxr.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return iupk__mxr
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
        bvmn__bltl = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], bvmn__bltl)
        return builder.bitcast(bvmn__bltl, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        bvmn__bltl = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(bvmn__bltl)
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
    utzfz__zku = types.unliteral(value)
    if isinstance(utzfz__zku, IndexValueType):
        utzfz__zku = utzfz__zku.val_typ
        hda__sjtgw = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            hda__sjtgw.append(types.int64)
            hda__sjtgw.append(bodo.datetime64ns)
            hda__sjtgw.append(bodo.timedelta64ns)
            hda__sjtgw.append(bodo.datetime_date_type)
        if utzfz__zku not in hda__sjtgw:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(utzfz__zku))
    typ_enum = np.int32(numba_to_c_type(utzfz__zku))

    def impl(value, reduce_op):
        hbg__tzolj = value_to_ptr(value)
        oemku__veh = value_to_ptr(value)
        _dist_reduce(hbg__tzolj, oemku__veh, reduce_op, typ_enum)
        return load_val_ptr(oemku__veh, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    utzfz__zku = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(utzfz__zku))
    wjt__wjyhr = utzfz__zku(0)

    def impl(value, reduce_op):
        hbg__tzolj = value_to_ptr(value)
        oemku__veh = value_to_ptr(wjt__wjyhr)
        _dist_exscan(hbg__tzolj, oemku__veh, reduce_op, typ_enum)
        return load_val_ptr(oemku__veh, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    xvj__ikzsl = 0
    ogd__xsb = 0
    for i in range(len(recv_counts)):
        opb__pxxj = recv_counts[i]
        cye__hbjuk = recv_counts_nulls[i]
        ebsag__cve = tmp_null_bytes[xvj__ikzsl:xvj__ikzsl + cye__hbjuk]
        for ktr__abaj in range(opb__pxxj):
            set_bit_to(null_bitmap_ptr, ogd__xsb, get_bit(ebsag__cve,
                ktr__abaj))
            ogd__xsb += 1
        xvj__ikzsl += cye__hbjuk


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            vow__mtlkh = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                vow__mtlkh, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            nqi__pbtjp = data.size
            recv_counts = gather_scalar(np.int32(nqi__pbtjp), allgather,
                root=root)
            gyf__mmew = recv_counts.sum()
            rmu__xkj = empty_like_type(gyf__mmew, data)
            fkt__ughg = np.empty(1, np.int32)
            if rank == root or allgather:
                fkt__ughg = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(nqi__pbtjp), rmu__xkj.ctypes,
                recv_counts.ctypes, fkt__ughg.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return rmu__xkj.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            rmu__xkj = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(rmu__xkj)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rmu__xkj = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(rmu__xkj)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            nqi__pbtjp = len(data)
            cye__hbjuk = nqi__pbtjp + 7 >> 3
            recv_counts = gather_scalar(np.int32(nqi__pbtjp), allgather,
                root=root)
            gyf__mmew = recv_counts.sum()
            rmu__xkj = empty_like_type(gyf__mmew, data)
            fkt__ughg = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            oiby__epls = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                fkt__ughg = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                oiby__epls = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(nqi__pbtjp),
                rmu__xkj._days_data.ctypes, recv_counts.ctypes, fkt__ughg.
                ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(nqi__pbtjp),
                rmu__xkj._seconds_data.ctypes, recv_counts.ctypes,
                fkt__ughg.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(nqi__pbtjp),
                rmu__xkj._microseconds_data.ctypes, recv_counts.ctypes,
                fkt__ughg.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(cye__hbjuk),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, oiby__epls
                .ctypes, nzbl__qnzy, allgather, np.int32(root))
            copy_gathered_null_bytes(rmu__xkj._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return rmu__xkj
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            nqi__pbtjp = len(data)
            cye__hbjuk = nqi__pbtjp + 7 >> 3
            recv_counts = gather_scalar(np.int32(nqi__pbtjp), allgather,
                root=root)
            gyf__mmew = recv_counts.sum()
            rmu__xkj = empty_like_type(gyf__mmew, data)
            fkt__ughg = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            oiby__epls = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                fkt__ughg = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                oiby__epls = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(nqi__pbtjp), rmu__xkj.
                _data.ctypes, recv_counts.ctypes, fkt__ughg.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(cye__hbjuk),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, oiby__epls
                .ctypes, nzbl__qnzy, allgather, np.int32(root))
            copy_gathered_null_bytes(rmu__xkj._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return rmu__xkj
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        rjc__emzfa = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            oye__bhjfm = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                oye__bhjfm, rjc__emzfa)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            drohx__fgids = bodo.gatherv(data._left, allgather, warn_if_rep,
                root)
            fzvyh__umv = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(drohx__fgids,
                fzvyh__umv)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            fht__wbljr = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            cdt__btdw = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cdt__btdw, fht__wbljr)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        vogg__mvjd = np.iinfo(np.int64).max
        hfngi__gpffs = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            start = data._start
            stop = data._stop
            if len(data) == 0:
                start = vogg__mvjd
                stop = hfngi__gpffs
            start = bodo.libs.distributed_api.dist_reduce(start, np.int32(
                Reduce_Type.Min.value))
            stop = bodo.libs.distributed_api.dist_reduce(stop, np.int32(
                Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if start == vogg__mvjd and stop == hfngi__gpffs:
                start = 0
                stop = 0
            ave__dvhbm = max(0, -(-(stop - start) // data._step))
            if ave__dvhbm < total_len:
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
            ewjck__bbur = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, ewjck__bbur)
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
            rmu__xkj = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(rmu__xkj,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        godzz__xxdk = {'bodo': bodo, 'get_table_block': bodo.hiframes.table
            .get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        omck__xwc = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        omck__xwc += '  T = data\n'
        omck__xwc += '  T2 = init_table(T, True)\n'
        for yaldt__zwvnt in data.type_to_blk.values():
            godzz__xxdk[f'arr_inds_{yaldt__zwvnt}'] = np.array(data.
                block_to_arr_ind[yaldt__zwvnt], dtype=np.int64)
            omck__xwc += (
                f'  arr_list_{yaldt__zwvnt} = get_table_block(T, {yaldt__zwvnt})\n'
                )
            omck__xwc += f"""  out_arr_list_{yaldt__zwvnt} = alloc_list_like(arr_list_{yaldt__zwvnt}, True)
"""
            omck__xwc += f'  for i in range(len(arr_list_{yaldt__zwvnt})):\n'
            omck__xwc += (
                f'    arr_ind_{yaldt__zwvnt} = arr_inds_{yaldt__zwvnt}[i]\n')
            omck__xwc += f"""    ensure_column_unboxed(T, arr_list_{yaldt__zwvnt}, i, arr_ind_{yaldt__zwvnt})
"""
            omck__xwc += f"""    out_arr_{yaldt__zwvnt} = bodo.gatherv(arr_list_{yaldt__zwvnt}[i], allgather, warn_if_rep, root)
"""
            omck__xwc += (
                f'    out_arr_list_{yaldt__zwvnt}[i] = out_arr_{yaldt__zwvnt}\n'
                )
            omck__xwc += f"""  T2 = set_table_block(T2, out_arr_list_{yaldt__zwvnt}, {yaldt__zwvnt})
"""
        omck__xwc += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        omck__xwc += f'  T2 = set_table_len(T2, length)\n'
        omck__xwc += f'  return T2\n'
        ossv__aaoc = {}
        exec(omck__xwc, godzz__xxdk, ossv__aaoc)
        uheh__kpvhn = ossv__aaoc['impl_table']
        return uheh__kpvhn
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        kdm__ozwzt = len(data.columns)
        if kdm__ozwzt == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                yrj__nxblo = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    yrj__nxblo, ())
            return impl
        ifror__ohqi = ', '.join(f'g_data_{i}' for i in range(kdm__ozwzt))
        udn__vraah = bodo.utils.transform.gen_const_tup(data.columns)
        omck__xwc = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            dvi__iotl = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            godzz__xxdk = {'bodo': bodo, 'df_type': dvi__iotl}
            ifror__ohqi = 'T2'
            udn__vraah = 'df_type'
            omck__xwc += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            omck__xwc += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            godzz__xxdk = {'bodo': bodo}
            for i in range(kdm__ozwzt):
                omck__xwc += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                omck__xwc += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        omck__xwc += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        omck__xwc += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        omck__xwc += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(ifror__ohqi, udn__vraah))
        ossv__aaoc = {}
        exec(omck__xwc, godzz__xxdk, ossv__aaoc)
        inmu__ekjns = ossv__aaoc['impl_df']
        return inmu__ekjns
    if isinstance(data, ArrayItemArrayType):
        ikbl__klejz = np.int32(numba_to_c_type(types.int32))
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            zmrka__zpw = bodo.libs.array_item_arr_ext.get_offsets(data)
            bmim__zoh = bodo.libs.array_item_arr_ext.get_data(data)
            bmim__zoh = bmim__zoh[:zmrka__zpw[-1]]
            zeyip__zxclb = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            nqi__pbtjp = len(data)
            bzbz__mdq = np.empty(nqi__pbtjp, np.uint32)
            cye__hbjuk = nqi__pbtjp + 7 >> 3
            for i in range(nqi__pbtjp):
                bzbz__mdq[i] = zmrka__zpw[i + 1] - zmrka__zpw[i]
            recv_counts = gather_scalar(np.int32(nqi__pbtjp), allgather,
                root=root)
            gyf__mmew = recv_counts.sum()
            fkt__ughg = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            oiby__epls = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                fkt__ughg = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for uco__ukkmn in range(len(recv_counts)):
                    recv_counts_nulls[uco__ukkmn] = recv_counts[uco__ukkmn
                        ] + 7 >> 3
                oiby__epls = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            nqeiv__rpi = np.empty(gyf__mmew + 1, np.uint32)
            hmvf__qltc = bodo.gatherv(bmim__zoh, allgather, warn_if_rep, root)
            oeucb__abuw = np.empty(gyf__mmew + 7 >> 3, np.uint8)
            c_gatherv(bzbz__mdq.ctypes, np.int32(nqi__pbtjp), nqeiv__rpi.
                ctypes, recv_counts.ctypes, fkt__ughg.ctypes, ikbl__klejz,
                allgather, np.int32(root))
            c_gatherv(zeyip__zxclb.ctypes, np.int32(cye__hbjuk),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, oiby__epls
                .ctypes, nzbl__qnzy, allgather, np.int32(root))
            dummy_use(data)
            ggzkk__jzxn = np.empty(gyf__mmew + 1, np.uint64)
            convert_len_arr_to_offset(nqeiv__rpi.ctypes, ggzkk__jzxn.ctypes,
                gyf__mmew)
            copy_gathered_null_bytes(oeucb__abuw.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                gyf__mmew, hmvf__qltc, ggzkk__jzxn, oeucb__abuw)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        vcjfw__tacl = data.names
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            fdj__sky = bodo.libs.struct_arr_ext.get_data(data)
            keiic__fesk = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            geao__dbbc = bodo.gatherv(fdj__sky, allgather=allgather, root=root)
            rank = bodo.libs.distributed_api.get_rank()
            nqi__pbtjp = len(data)
            cye__hbjuk = nqi__pbtjp + 7 >> 3
            recv_counts = gather_scalar(np.int32(nqi__pbtjp), allgather,
                root=root)
            gyf__mmew = recv_counts.sum()
            oueft__gnmj = np.empty(gyf__mmew + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            oiby__epls = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                oiby__epls = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(keiic__fesk.ctypes, np.int32(cye__hbjuk),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, oiby__epls
                .ctypes, nzbl__qnzy, allgather, np.int32(root))
            copy_gathered_null_bytes(oueft__gnmj.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(geao__dbbc,
                oueft__gnmj, vcjfw__tacl)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            rmu__xkj = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(rmu__xkj)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            rmu__xkj = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(rmu__xkj)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            rmu__xkj = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(rmu__xkj)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            rmu__xkj = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            lcju__spvx = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            xkcq__vnqjl = bodo.gatherv(data.indptr, allgather, warn_if_rep,
                root)
            kccb__wwq = gather_scalar(data.shape[0], allgather, root=root)
            tcp__anam = kccb__wwq.sum()
            kdm__ozwzt = bodo.libs.distributed_api.dist_reduce(data.shape[1
                ], np.int32(Reduce_Type.Max.value))
            cxo__qfb = np.empty(tcp__anam + 1, np.int64)
            lcju__spvx = lcju__spvx.astype(np.int64)
            cxo__qfb[0] = 0
            suk__hshs = 1
            vvu__sbcwg = 0
            for oeb__acf in kccb__wwq:
                for yemcv__yhhbc in range(oeb__acf):
                    dnnwl__num = xkcq__vnqjl[vvu__sbcwg + 1] - xkcq__vnqjl[
                        vvu__sbcwg]
                    cxo__qfb[suk__hshs] = cxo__qfb[suk__hshs - 1] + dnnwl__num
                    suk__hshs += 1
                    vvu__sbcwg += 1
                vvu__sbcwg += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(rmu__xkj,
                lcju__spvx, cxo__qfb, (tcp__anam, kdm__ozwzt))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        omck__xwc = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        omck__xwc += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        ossv__aaoc = {}
        exec(omck__xwc, {'bodo': bodo}, ossv__aaoc)
        zzu__ecvju = ossv__aaoc['impl_tuple']
        return zzu__ecvju
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    omck__xwc = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    omck__xwc += '    if random:\n'
    omck__xwc += '        if random_seed is None:\n'
    omck__xwc += '            random = 1\n'
    omck__xwc += '        else:\n'
    omck__xwc += '            random = 2\n'
    omck__xwc += '    if random_seed is None:\n'
    omck__xwc += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        wisu__khidg = data
        kdm__ozwzt = len(wisu__khidg.columns)
        for i in range(kdm__ozwzt):
            omck__xwc += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        omck__xwc += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        ifror__ohqi = ', '.join(f'data_{i}' for i in range(kdm__ozwzt))
        omck__xwc += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(emoiu__mwif) for
            emoiu__mwif in range(kdm__ozwzt))))
        omck__xwc += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        omck__xwc += '    if dests is None:\n'
        omck__xwc += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        omck__xwc += '    else:\n'
        omck__xwc += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for dhh__xwf in range(kdm__ozwzt):
            omck__xwc += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(dhh__xwf))
        omck__xwc += (
            '    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
            .format(kdm__ozwzt))
        omck__xwc += '    delete_table(out_table)\n'
        omck__xwc += '    if parallel:\n'
        omck__xwc += '        delete_table(table_total)\n'
        ifror__ohqi = ', '.join('out_arr_{}'.format(i) for i in range(
            kdm__ozwzt))
        udn__vraah = bodo.utils.transform.gen_const_tup(wisu__khidg.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        omck__xwc += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(ifror__ohqi, index, udn__vraah))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        omck__xwc += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        omck__xwc += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        omck__xwc += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        omck__xwc += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        omck__xwc += '    if dests is None:\n'
        omck__xwc += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        omck__xwc += '    else:\n'
        omck__xwc += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        omck__xwc += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        omck__xwc += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        omck__xwc += '    delete_table(out_table)\n'
        omck__xwc += '    if parallel:\n'
        omck__xwc += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        omck__xwc += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        omck__xwc += '    if not parallel:\n'
        omck__xwc += '        return data\n'
        omck__xwc += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        omck__xwc += '    if dests is None:\n'
        omck__xwc += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        omck__xwc += '    elif bodo.get_rank() not in dests:\n'
        omck__xwc += '        dim0_local_size = 0\n'
        omck__xwc += '    else:\n'
        omck__xwc += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        omck__xwc += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        omck__xwc += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        omck__xwc += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        omck__xwc += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        omck__xwc += '    if dests is None:\n'
        omck__xwc += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        omck__xwc += '    else:\n'
        omck__xwc += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        omck__xwc += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        omck__xwc += '    delete_table(out_table)\n'
        omck__xwc += '    if parallel:\n'
        omck__xwc += '        delete_table(table_total)\n'
        omck__xwc += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    ossv__aaoc = {}
    exec(omck__xwc, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table},
        ossv__aaoc)
    impl = ossv__aaoc['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    omck__xwc = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        omck__xwc += '    if seed is None:\n'
        omck__xwc += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        omck__xwc += '    np.random.seed(seed)\n'
        omck__xwc += '    if not parallel:\n'
        omck__xwc += '        data = data.copy()\n'
        omck__xwc += '        np.random.shuffle(data)\n'
        omck__xwc += '        return data\n'
        omck__xwc += '    else:\n'
        omck__xwc += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        omck__xwc += '        permutation = np.arange(dim0_global_size)\n'
        omck__xwc += '        np.random.shuffle(permutation)\n'
        omck__xwc += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        omck__xwc += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        omck__xwc += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        omck__xwc += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        omck__xwc += '        return output\n'
    else:
        omck__xwc += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    ossv__aaoc = {}
    exec(omck__xwc, {'np': np, 'bodo': bodo}, ossv__aaoc)
    impl = ossv__aaoc['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    yqysx__eull = np.empty(sendcounts_nulls.sum(), np.uint8)
    xvj__ikzsl = 0
    ogd__xsb = 0
    for abkdc__wudjc in range(len(sendcounts)):
        opb__pxxj = sendcounts[abkdc__wudjc]
        cye__hbjuk = sendcounts_nulls[abkdc__wudjc]
        ebsag__cve = yqysx__eull[xvj__ikzsl:xvj__ikzsl + cye__hbjuk]
        for ktr__abaj in range(opb__pxxj):
            set_bit_to_arr(ebsag__cve, ktr__abaj, get_bit_bitmap(
                null_bitmap_ptr, ogd__xsb))
            ogd__xsb += 1
        xvj__ikzsl += cye__hbjuk
    return yqysx__eull


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    iglt__ihi = MPI.COMM_WORLD
    data = iglt__ihi.bcast(data, root)
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
    kspb__lbe = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    fcfr__zgb = (0,) * kspb__lbe

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        vjj__otpnx = np.ascontiguousarray(data)
        njq__swkq = data.ctypes
        hxno__idiqb = fcfr__zgb
        if rank == MPI_ROOT:
            hxno__idiqb = vjj__otpnx.shape
        hxno__idiqb = bcast_tuple(hxno__idiqb)
        tlf__lrixa = get_tuple_prod(hxno__idiqb[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            hxno__idiqb[0])
        send_counts *= tlf__lrixa
        nqi__pbtjp = send_counts[rank]
        zeqv__plibq = np.empty(nqi__pbtjp, dtype)
        fkt__ughg = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(njq__swkq, send_counts.ctypes, fkt__ughg.ctypes,
            zeqv__plibq.ctypes, np.int32(nqi__pbtjp), np.int32(typ_val))
        return zeqv__plibq.reshape((-1,) + hxno__idiqb[1:])
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
        xeabh__dbbwb = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], xeabh__dbbwb)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        fht__wbljr = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=fht__wbljr)
        seax__hltj = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(seax__hltj)
        return pd.Index(arr, name=fht__wbljr)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        fht__wbljr = _get_name_value_for_type(dtype.name_typ)
        vcjfw__tacl = tuple(_get_name_value_for_type(t) for t in dtype.
            names_typ)
        dhm__mkc = tuple(get_value_for_type(t) for t in dtype.array_types)
        dhm__mkc = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in dhm__mkc)
        val = pd.MultiIndex.from_arrays(dhm__mkc, names=vcjfw__tacl)
        val.name = fht__wbljr
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        fht__wbljr = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=fht__wbljr)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        dhm__mkc = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({fht__wbljr: arr for fht__wbljr, arr in zip(
            dtype.columns, dhm__mkc)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        seax__hltj = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(seax__hltj[0],
            seax__hltj[0])])
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
        ikbl__klejz = np.int32(numba_to_c_type(types.int32))
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            sklra__tbhng = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            sklra__tbhng = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        omck__xwc = f"""def impl(
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
            recv_arr = {sklra__tbhng}(n_loc, n_loc_char)

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
        ossv__aaoc = dict()
        exec(omck__xwc, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            ikbl__klejz, 'char_typ_enum': nzbl__qnzy,
            'decode_if_dict_array': decode_if_dict_array}, ossv__aaoc)
        impl = ossv__aaoc['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        ikbl__klejz = np.int32(numba_to_c_type(types.int32))
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            jgvjh__yge = bodo.libs.array_item_arr_ext.get_offsets(data)
            upphj__swi = bodo.libs.array_item_arr_ext.get_data(data)
            upphj__swi = upphj__swi[:jgvjh__yge[-1]]
            uyx__wjgf = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            nmxs__dvbvj = bcast_scalar(len(data))
            var__kcl = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                var__kcl[i] = jgvjh__yge[i + 1] - jgvjh__yge[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                nmxs__dvbvj)
            fkt__ughg = bodo.ir.join.calc_disp(send_counts)
            fgwd__omym = np.empty(n_pes, np.int32)
            if rank == 0:
                eqvnv__nrxhi = 0
                for i in range(n_pes):
                    ebja__hxthx = 0
                    for yemcv__yhhbc in range(send_counts[i]):
                        ebja__hxthx += var__kcl[eqvnv__nrxhi]
                        eqvnv__nrxhi += 1
                    fgwd__omym[i] = ebja__hxthx
            bcast(fgwd__omym)
            fdgeg__rsbfc = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                fdgeg__rsbfc[i] = send_counts[i] + 7 >> 3
            oiby__epls = bodo.ir.join.calc_disp(fdgeg__rsbfc)
            nqi__pbtjp = send_counts[rank]
            mzq__ipqdo = np.empty(nqi__pbtjp + 1, np_offset_type)
            ory__cxgtc = bodo.libs.distributed_api.scatterv_impl(upphj__swi,
                fgwd__omym)
            kyqo__ixwws = nqi__pbtjp + 7 >> 3
            ehycv__mdo = np.empty(kyqo__ixwws, np.uint8)
            helx__dnqxu = np.empty(nqi__pbtjp, np.uint32)
            c_scatterv(var__kcl.ctypes, send_counts.ctypes, fkt__ughg.
                ctypes, helx__dnqxu.ctypes, np.int32(nqi__pbtjp), ikbl__klejz)
            convert_len_arr_to_offset(helx__dnqxu.ctypes, mzq__ipqdo.ctypes,
                nqi__pbtjp)
            qwyrm__adnzf = get_scatter_null_bytes_buff(uyx__wjgf.ctypes,
                send_counts, fdgeg__rsbfc)
            c_scatterv(qwyrm__adnzf.ctypes, fdgeg__rsbfc.ctypes, oiby__epls
                .ctypes, ehycv__mdo.ctypes, np.int32(kyqo__ixwws), nzbl__qnzy)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                nqi__pbtjp, ory__cxgtc, mzq__ipqdo, ehycv__mdo)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            jvb__yjtl = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            jvb__yjtl = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            jvb__yjtl = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            jvb__yjtl = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            vjj__otpnx = data._data
            keiic__fesk = data._null_bitmap
            wlui__usc = len(vjj__otpnx)
            pme__xpw = _scatterv_np(vjj__otpnx, send_counts)
            nmxs__dvbvj = bcast_scalar(wlui__usc)
            dty__ezsu = len(pme__xpw) + 7 >> 3
            vwf__ylk = np.empty(dty__ezsu, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                nmxs__dvbvj)
            fdgeg__rsbfc = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                fdgeg__rsbfc[i] = send_counts[i] + 7 >> 3
            oiby__epls = bodo.ir.join.calc_disp(fdgeg__rsbfc)
            qwyrm__adnzf = get_scatter_null_bytes_buff(keiic__fesk.ctypes,
                send_counts, fdgeg__rsbfc)
            c_scatterv(qwyrm__adnzf.ctypes, fdgeg__rsbfc.ctypes, oiby__epls
                .ctypes, vwf__ylk.ctypes, np.int32(dty__ezsu), nzbl__qnzy)
            return jvb__yjtl(pme__xpw, vwf__ylk)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            osn__hsvmr = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            qbxyi__hnbox = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(osn__hsvmr,
                qbxyi__hnbox)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            rji__zpmqb = data._step
            fht__wbljr = data._name
            fht__wbljr = bcast_scalar(fht__wbljr)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            rji__zpmqb = bcast_scalar(rji__zpmqb)
            whmoc__vaj = bodo.libs.array_kernels.calc_nitems(start, stop,
                rji__zpmqb)
            chunk_start = bodo.libs.distributed_api.get_start(whmoc__vaj,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(whmoc__vaj
                , n_pes, rank)
            eyyv__yod = start + rji__zpmqb * chunk_start
            rxm__tbcs = start + rji__zpmqb * (chunk_start + chunk_count)
            rxm__tbcs = min(rxm__tbcs, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(eyyv__yod,
                rxm__tbcs, rji__zpmqb, fht__wbljr)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        ewjck__bbur = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            vjj__otpnx = data._data
            fht__wbljr = data._name
            fht__wbljr = bcast_scalar(fht__wbljr)
            arr = bodo.libs.distributed_api.scatterv_impl(vjj__otpnx,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                fht__wbljr, ewjck__bbur)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            vjj__otpnx = data._data
            fht__wbljr = data._name
            fht__wbljr = bcast_scalar(fht__wbljr)
            arr = bodo.libs.distributed_api.scatterv_impl(vjj__otpnx,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, fht__wbljr)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            rmu__xkj = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            fht__wbljr = bcast_scalar(data._name)
            vcjfw__tacl = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(rmu__xkj,
                vcjfw__tacl, fht__wbljr)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            fht__wbljr = bodo.hiframes.pd_series_ext.get_series_name(data)
            kih__dbj = bcast_scalar(fht__wbljr)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            cdt__btdw = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cdt__btdw, kih__dbj)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        kdm__ozwzt = len(data.columns)
        ifror__ohqi = ', '.join('g_data_{}'.format(i) for i in range(
            kdm__ozwzt))
        udn__vraah = bodo.utils.transform.gen_const_tup(data.columns)
        omck__xwc = 'def impl_df(data, send_counts=None, warn_if_dist=True):\n'
        for i in range(kdm__ozwzt):
            omck__xwc += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            omck__xwc += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        omck__xwc += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        omck__xwc += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        omck__xwc += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(ifror__ohqi, udn__vraah))
        ossv__aaoc = {}
        exec(omck__xwc, {'bodo': bodo}, ossv__aaoc)
        inmu__ekjns = ossv__aaoc['impl_df']
        return inmu__ekjns
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            vow__mtlkh = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                vow__mtlkh, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        omck__xwc = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        omck__xwc += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        ossv__aaoc = {}
        exec(omck__xwc, {'bodo': bodo}, ossv__aaoc)
        zzu__ecvju = ossv__aaoc['impl_tuple']
        return zzu__ecvju
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
        spf__vzg = np.int32(numba_to_c_type(offset_type))
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            nqi__pbtjp = len(data)
            tigmp__zzlja = num_total_chars(data)
            assert nqi__pbtjp < INT_MAX
            assert tigmp__zzlja < INT_MAX
            ydl__aqyhg = get_offset_ptr(data)
            njq__swkq = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            cye__hbjuk = nqi__pbtjp + 7 >> 3
            c_bcast(ydl__aqyhg, np.int32(nqi__pbtjp + 1), spf__vzg, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(njq__swkq, np.int32(tigmp__zzlja), nzbl__qnzy, np.array
                ([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(cye__hbjuk), nzbl__qnzy, np.
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
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                pssyz__vxpli = 0
                zxp__tbwno = np.empty(0, np.uint8).ctypes
            else:
                zxp__tbwno, pssyz__vxpli = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            pssyz__vxpli = bodo.libs.distributed_api.bcast_scalar(pssyz__vxpli,
                root)
            if rank != root:
                yyc__znvb = np.empty(pssyz__vxpli + 1, np.uint8)
                yyc__znvb[pssyz__vxpli] = 0
                zxp__tbwno = yyc__znvb.ctypes
            c_bcast(zxp__tbwno, np.int32(pssyz__vxpli), nzbl__qnzy, np.
                array([-1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(zxp__tbwno, pssyz__vxpli)
        return impl_str
    typ_val = numba_to_c_type(val)
    omck__xwc = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    ossv__aaoc = {}
    exec(omck__xwc, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, ossv__aaoc)
    guaeu__nzfb = ossv__aaoc['bcast_scalar_impl']
    return guaeu__nzfb


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    deok__ksx = len(val)
    omck__xwc = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    omck__xwc += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(deok__ksx)),
        ',' if deok__ksx else '')
    ossv__aaoc = {}
    exec(omck__xwc, {'bcast_scalar': bcast_scalar}, ossv__aaoc)
    yiwt__akuwn = ossv__aaoc['bcast_tuple_impl']
    return yiwt__akuwn


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            nqi__pbtjp = bcast_scalar(len(arr), root)
            wkd__iia = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(nqi__pbtjp, wkd__iia)
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
        rji__zpmqb = slice_index.step
        qpibr__hyib = 0 if rji__zpmqb == 1 or start > arr_start else abs(
            rji__zpmqb - arr_start % rji__zpmqb) % rji__zpmqb
        eyyv__yod = max(arr_start, slice_index.start) - arr_start + qpibr__hyib
        rxm__tbcs = max(slice_index.stop - arr_start, 0)
        return slice(eyyv__yod, rxm__tbcs, rji__zpmqb)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        rna__xrpkq = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[rna__xrpkq])
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
        xmur__rdvq = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        nzbl__qnzy = np.int32(numba_to_c_type(types.uint8))
        uken__qvgph = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            qxbh__wfga = np.int32(10)
            tag = np.int32(11)
            lcl__teb = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                bmim__zoh = arr._data
                xqoz__yrjlu = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    bmim__zoh, ind)
                ecfyf__celb = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    bmim__zoh, ind + 1)
                length = ecfyf__celb - xqoz__yrjlu
                bvmn__bltl = bmim__zoh[ind]
                lcl__teb[0] = length
                isend(lcl__teb, np.int32(1), root, qxbh__wfga, True)
                isend(bvmn__bltl, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                uken__qvgph, xmur__rdvq, 0, 1)
            ave__dvhbm = 0
            if rank == root:
                ave__dvhbm = recv(np.int64, ANY_SOURCE, qxbh__wfga)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    uken__qvgph, xmur__rdvq, ave__dvhbm, 1)
                njq__swkq = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(njq__swkq, np.int32(ave__dvhbm), nzbl__qnzy,
                    ANY_SOURCE, tag)
            dummy_use(lcl__teb)
            ave__dvhbm = bcast_scalar(ave__dvhbm)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    uken__qvgph, xmur__rdvq, ave__dvhbm, 1)
            njq__swkq = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(njq__swkq, np.int32(ave__dvhbm), nzbl__qnzy, np.array([
                -1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, ave__dvhbm)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        pzd__noi = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, pzd__noi)
            if arr_start <= ind < arr_start + len(arr):
                vow__mtlkh = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = vow__mtlkh[ind - arr_start]
                send_arr = np.full(1, data, pzd__noi)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = pzd__noi(-1)
            if rank == root:
                val = recv(pzd__noi, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            cwuhn__waf = arr.dtype.categories[max(val, 0)]
            return cwuhn__waf
        return cat_getitem_impl
    ahdt__uyg = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, ahdt__uyg)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, ahdt__uyg)[0]
        if rank == root:
            val = recv(ahdt__uyg, ANY_SOURCE, tag)
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
    fam__wfhm = get_type_enum(out_data)
    assert typ_enum == fam__wfhm
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
    omck__xwc = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        omck__xwc += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    omck__xwc += '  return\n'
    ossv__aaoc = {}
    exec(omck__xwc, {'alltoallv': alltoallv}, ossv__aaoc)
    zwy__hocha = ossv__aaoc['f']
    return zwy__hocha


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    start = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return start, count


@numba.njit
def get_start(total_size, pes, rank):
    iupk__mxr = total_size % pes
    fnp__wvs = (total_size - iupk__mxr) // pes
    return rank * fnp__wvs + min(rank, iupk__mxr)


@numba.njit
def get_end(total_size, pes, rank):
    iupk__mxr = total_size % pes
    fnp__wvs = (total_size - iupk__mxr) // pes
    return (rank + 1) * fnp__wvs + min(rank + 1, iupk__mxr)


@numba.njit
def get_node_portion(total_size, pes, rank):
    iupk__mxr = total_size % pes
    fnp__wvs = (total_size - iupk__mxr) // pes
    if rank < iupk__mxr:
        return fnp__wvs + 1
    else:
        return fnp__wvs


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    wjt__wjyhr = in_arr.dtype(0)
    kia__kxpom = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        ebja__hxthx = wjt__wjyhr
        for phh__fbz in np.nditer(in_arr):
            ebja__hxthx += phh__fbz.item()
        efcu__qvfh = dist_exscan(ebja__hxthx, kia__kxpom)
        for i in range(in_arr.size):
            efcu__qvfh += in_arr[i]
            out_arr[i] = efcu__qvfh
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    fofhu__jmmt = in_arr.dtype(1)
    kia__kxpom = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        ebja__hxthx = fofhu__jmmt
        for phh__fbz in np.nditer(in_arr):
            ebja__hxthx *= phh__fbz.item()
        efcu__qvfh = dist_exscan(ebja__hxthx, kia__kxpom)
        if get_rank() == 0:
            efcu__qvfh = fofhu__jmmt
        for i in range(in_arr.size):
            efcu__qvfh *= in_arr[i]
            out_arr[i] = efcu__qvfh
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        fofhu__jmmt = np.finfo(in_arr.dtype(1).dtype).max
    else:
        fofhu__jmmt = np.iinfo(in_arr.dtype(1).dtype).max
    kia__kxpom = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        ebja__hxthx = fofhu__jmmt
        for phh__fbz in np.nditer(in_arr):
            ebja__hxthx = min(ebja__hxthx, phh__fbz.item())
        efcu__qvfh = dist_exscan(ebja__hxthx, kia__kxpom)
        if get_rank() == 0:
            efcu__qvfh = fofhu__jmmt
        for i in range(in_arr.size):
            efcu__qvfh = min(efcu__qvfh, in_arr[i])
            out_arr[i] = efcu__qvfh
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        fofhu__jmmt = np.finfo(in_arr.dtype(1).dtype).min
    else:
        fofhu__jmmt = np.iinfo(in_arr.dtype(1).dtype).min
    fofhu__jmmt = in_arr.dtype(1)
    kia__kxpom = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        ebja__hxthx = fofhu__jmmt
        for phh__fbz in np.nditer(in_arr):
            ebja__hxthx = max(ebja__hxthx, phh__fbz.item())
        efcu__qvfh = dist_exscan(ebja__hxthx, kia__kxpom)
        if get_rank() == 0:
            efcu__qvfh = fofhu__jmmt
        for i in range(in_arr.size):
            efcu__qvfh = max(efcu__qvfh, in_arr[i])
            out_arr[i] = efcu__qvfh
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    gpn__vkq = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), gpn__vkq)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    htwb__wcvq = args[0]
    if equiv_set.has_shape(htwb__wcvq):
        return ArrayAnalysis.AnalyzeResult(shape=htwb__wcvq, pre=[])
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
        knd__bpxd = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        omck__xwc = 'def f(req, cond=True):\n'
        omck__xwc += f'  return {knd__bpxd}\n'
        ossv__aaoc = {}
        exec(omck__xwc, {'_wait': _wait}, ossv__aaoc)
        impl = ossv__aaoc['f']
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
    eyyv__yod = max(start, chunk_start)
    rxm__tbcs = min(stop, chunk_start + chunk_count)
    llxp__uwc = eyyv__yod - chunk_start
    czdhc__poyi = rxm__tbcs - chunk_start
    if llxp__uwc < 0 or czdhc__poyi < 0:
        llxp__uwc = 1
        czdhc__poyi = 0
    return llxp__uwc, czdhc__poyi


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
        iupk__mxr = 1
        for a in t:
            iupk__mxr *= a
        return iupk__mxr
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    pwwh__sna = np.ascontiguousarray(in_arr)
    gecif__ikxi = get_tuple_prod(pwwh__sna.shape[1:])
    marm__ksi = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        aad__xgkqz = np.array(dest_ranks, dtype=np.int32)
    else:
        aad__xgkqz = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, pwwh__sna.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * marm__ksi, dtype_size * gecif__ikxi, len(
        aad__xgkqz), aad__xgkqz.ctypes)
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
    yrhv__vgt = np.ascontiguousarray(rhs)
    wbvf__jqxdq = get_tuple_prod(yrhv__vgt.shape[1:])
    rhis__eink = dtype_size * wbvf__jqxdq
    permutation_array_index(lhs.ctypes, lhs_len, rhis__eink, yrhv__vgt.
        ctypes, yrhv__vgt.shape[0], p.ctypes, p_len)
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
        omck__xwc = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        ossv__aaoc = {}
        exec(omck__xwc, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, ossv__aaoc)
        guaeu__nzfb = ossv__aaoc['bcast_scalar_impl']
        return guaeu__nzfb
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        kdm__ozwzt = len(data.columns)
        ifror__ohqi = ', '.join('g_data_{}'.format(i) for i in range(
            kdm__ozwzt))
        udn__vraah = bodo.utils.transform.gen_const_tup(data.columns)
        omck__xwc = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(kdm__ozwzt):
            omck__xwc += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            omck__xwc += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        omck__xwc += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        omck__xwc += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        omck__xwc += (
            '  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})\n'
            .format(ifror__ohqi, udn__vraah))
        ossv__aaoc = {}
        exec(omck__xwc, {'bodo': bodo}, ossv__aaoc)
        inmu__ekjns = ossv__aaoc['impl_df']
        return inmu__ekjns
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            rji__zpmqb = data._step
            fht__wbljr = data._name
            fht__wbljr = bcast_scalar(fht__wbljr, root)
            start = bcast_scalar(start, root)
            stop = bcast_scalar(stop, root)
            rji__zpmqb = bcast_scalar(rji__zpmqb, root)
            whmoc__vaj = bodo.libs.array_kernels.calc_nitems(start, stop,
                rji__zpmqb)
            chunk_start = bodo.libs.distributed_api.get_start(whmoc__vaj,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(whmoc__vaj
                , n_pes, rank)
            eyyv__yod = start + rji__zpmqb * chunk_start
            rxm__tbcs = start + rji__zpmqb * (chunk_start + chunk_count)
            rxm__tbcs = min(rxm__tbcs, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(eyyv__yod,
                rxm__tbcs, rji__zpmqb, fht__wbljr)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            vjj__otpnx = data._data
            fht__wbljr = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(vjj__otpnx,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, fht__wbljr)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            fht__wbljr = bodo.hiframes.pd_series_ext.get_series_name(data)
            kih__dbj = bodo.libs.distributed_api.bcast_comm_impl(fht__wbljr,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            cdt__btdw = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cdt__btdw, kih__dbj)
        return impl_series
    if isinstance(data, types.BaseTuple):
        omck__xwc = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        omck__xwc += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        ossv__aaoc = {}
        exec(omck__xwc, {'bcast_comm_impl': bcast_comm_impl}, ossv__aaoc)
        zzu__ecvju = ossv__aaoc['impl_tuple']
        return zzu__ecvju
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    kspb__lbe = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    fcfr__zgb = (0,) * kspb__lbe

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        vjj__otpnx = np.ascontiguousarray(data)
        njq__swkq = data.ctypes
        hxno__idiqb = fcfr__zgb
        if rank == root:
            hxno__idiqb = vjj__otpnx.shape
        hxno__idiqb = bcast_tuple(hxno__idiqb, root)
        tlf__lrixa = get_tuple_prod(hxno__idiqb[1:])
        send_counts = hxno__idiqb[0] * tlf__lrixa
        zeqv__plibq = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(njq__swkq, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(zeqv__plibq.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return zeqv__plibq.reshape((-1,) + hxno__idiqb[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        iglt__ihi = MPI.COMM_WORLD
        mhw__abvrr = MPI.Get_processor_name()
        uwo__ldwnk = iglt__ihi.allgather(mhw__abvrr)
        node_ranks = defaultdict(list)
        for i, migm__xulj in enumerate(uwo__ldwnk):
            node_ranks[migm__xulj].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    iglt__ihi = MPI.COMM_WORLD
    xnvx__fzb = iglt__ihi.Get_group()
    njspl__ufjo = xnvx__fzb.Incl(comm_ranks)
    eez__fzda = iglt__ihi.Create_group(njspl__ufjo)
    return eez__fzda


def get_nodes_first_ranks():
    pal__rcazf = get_host_ranks()
    return np.array([ekfnw__wdm[0] for ekfnw__wdm in pal__rcazf.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
