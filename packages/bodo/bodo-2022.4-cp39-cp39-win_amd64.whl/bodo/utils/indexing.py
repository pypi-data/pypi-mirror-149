"""
Collection of utility functions for indexing implementation (getitem/setitem)
"""
import operator
import numba
import numpy as np
from numba.core import types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import intrinsic, overload, register_jitable
import bodo
from bodo.utils.typing import BodoError


@register_jitable
def get_new_null_mask_bool_index(old_mask, ind, n):
    uqe__kaov = n + 7 >> 3
    mtyld__akrv = np.empty(uqe__kaov, np.uint8)
    wuw__zvv = 0
    for ndhf__fpy in range(len(ind)):
        if ind[ndhf__fpy]:
            rpx__wwjve = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask,
                ndhf__fpy)
            bodo.libs.int_arr_ext.set_bit_to_arr(mtyld__akrv, wuw__zvv,
                rpx__wwjve)
            wuw__zvv += 1
    return mtyld__akrv


@register_jitable
def array_getitem_bool_index(A, ind):
    ind = bodo.utils.conversion.coerce_to_ndarray(ind)
    old_mask = A._null_bitmap
    uqq__qsse = A._data[ind]
    n = len(uqq__qsse)
    mtyld__akrv = get_new_null_mask_bool_index(old_mask, ind, n)
    return uqq__qsse, mtyld__akrv


@register_jitable
def get_new_null_mask_int_index(old_mask, ind, n):
    uqe__kaov = n + 7 >> 3
    mtyld__akrv = np.empty(uqe__kaov, np.uint8)
    wuw__zvv = 0
    for ndhf__fpy in range(len(ind)):
        rpx__wwjve = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, ind
            [ndhf__fpy])
        bodo.libs.int_arr_ext.set_bit_to_arr(mtyld__akrv, wuw__zvv, rpx__wwjve)
        wuw__zvv += 1
    return mtyld__akrv


@register_jitable
def array_getitem_int_index(A, ind):
    dof__iyi = bodo.utils.conversion.coerce_to_ndarray(ind)
    old_mask = A._null_bitmap
    uqq__qsse = A._data[dof__iyi]
    n = len(uqq__qsse)
    mtyld__akrv = get_new_null_mask_int_index(old_mask, dof__iyi, n)
    return uqq__qsse, mtyld__akrv


@register_jitable
def get_new_null_mask_slice_index(old_mask, ind, n):
    dxb__jtve = numba.cpython.unicode._normalize_slice(ind, n)
    bkge__ykxwj = numba.cpython.unicode._slice_span(dxb__jtve)
    uqe__kaov = bkge__ykxwj + 7 >> 3
    mtyld__akrv = np.empty(uqe__kaov, np.uint8)
    wuw__zvv = 0
    for ndhf__fpy in range(dxb__jtve.start, dxb__jtve.stop, dxb__jtve.step):
        rpx__wwjve = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask,
            ndhf__fpy)
        bodo.libs.int_arr_ext.set_bit_to_arr(mtyld__akrv, wuw__zvv, rpx__wwjve)
        wuw__zvv += 1
    return mtyld__akrv


@register_jitable
def array_getitem_slice_index(A, ind):
    n = len(A._data)
    old_mask = A._null_bitmap
    uqq__qsse = np.ascontiguousarray(A._data[ind])
    mtyld__akrv = get_new_null_mask_slice_index(old_mask, ind, n)
    return uqq__qsse, mtyld__akrv


def array_setitem_int_index(A, idx, val):
    return


@overload(array_setitem_int_index, no_unliteral=True)
def array_setitem_int_index_overload(A, idx, val):
    if bodo.utils.utils.is_array_typ(val
        ) or bodo.utils.typing.is_iterable_type(val):

        def impl_arr(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            n = len(val._data)
            for ndhf__fpy in range(n):
                A._data[idx[ndhf__fpy]] = val._data[ndhf__fpy]
                rpx__wwjve = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val.
                    _null_bitmap, ndhf__fpy)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx[
                    ndhf__fpy], rpx__wwjve)
        return impl_arr
    if bodo.utils.typing.is_scalar_type(val):

        def impl_scalar(A, idx, val):
            for ndhf__fpy in idx:
                A._data[ndhf__fpy] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                    ndhf__fpy, 1)
        return impl_scalar
    raise BodoError(f'setitem not supported for {A} with value {val}')


def array_setitem_bool_index(A, idx, val):
    A[idx] = val


@overload(array_setitem_bool_index, no_unliteral=True)
def array_setitem_bool_index_overload(A, idx, val):
    if bodo.utils.utils.is_array_typ(val
        ) or bodo.utils.typing.is_iterable_type(val):

        def impl_arr(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            n = len(idx)
            pggp__qfnhf = 0
            for ndhf__fpy in range(n):
                if not bodo.libs.array_kernels.isna(idx, ndhf__fpy) and idx[
                    ndhf__fpy]:
                    A._data[ndhf__fpy] = val._data[pggp__qfnhf]
                    rpx__wwjve = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, pggp__qfnhf)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ndhf__fpy, rpx__wwjve)
                    pggp__qfnhf += 1
        return impl_arr
    if bodo.utils.typing.is_scalar_type(val):

        def impl_scalar(A, idx, val):
            n = len(idx)
            pggp__qfnhf = 0
            for ndhf__fpy in range(n):
                if not bodo.libs.array_kernels.isna(idx, ndhf__fpy) and idx[
                    ndhf__fpy]:
                    A._data[ndhf__fpy] = val
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ndhf__fpy, 1)
                    pggp__qfnhf += 1
        return impl_scalar
    raise BodoError(f'setitem not supported for {A} with value {val}')


@register_jitable
def setitem_slice_index_null_bits(dst_bitmap, src_bitmap, idx, n):
    dxb__jtve = numba.cpython.unicode._normalize_slice(idx, n)
    pggp__qfnhf = 0
    for ndhf__fpy in range(dxb__jtve.start, dxb__jtve.stop, dxb__jtve.step):
        rpx__wwjve = bodo.libs.int_arr_ext.get_bit_bitmap_arr(src_bitmap,
            pggp__qfnhf)
        bodo.libs.int_arr_ext.set_bit_to_arr(dst_bitmap, ndhf__fpy, rpx__wwjve)
        pggp__qfnhf += 1


def array_setitem_slice_index(A, idx, val):
    return


@overload(array_setitem_slice_index, no_unliteral=True)
def array_setitem_slice_index_overload(A, idx, val):
    if bodo.utils.utils.is_array_typ(val
        ) or bodo.utils.typing.is_iterable_type(val):

        def impl_arr(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            n = len(A._data)
            A._data[idx] = val._data
            src_bitmap = val._null_bitmap.copy()
            setitem_slice_index_null_bits(A._null_bitmap, src_bitmap, idx, n)
        return impl_arr
    if bodo.utils.typing.is_scalar_type(val):

        def impl_scalar(A, idx, val):
            dxb__jtve = numba.cpython.unicode._normalize_slice(idx, len(A))
            for ndhf__fpy in range(dxb__jtve.start, dxb__jtve.stop,
                dxb__jtve.step):
                A._data[ndhf__fpy] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                    ndhf__fpy, 1)
        return impl_scalar
    raise BodoError(f'setitem not supported for {A} with value {val}')


def untuple_if_one_tuple(v):
    return v


@overload(untuple_if_one_tuple)
def untuple_if_one_tuple_overload(v):
    if isinstance(v, types.BaseTuple) and len(v.types) == 1:
        return lambda v: v[0]
    return lambda v: v


def init_nested_counts(arr_typ):
    return 0,


@overload(init_nested_counts)
def overload_init_nested_counts(arr_typ):
    arr_typ = arr_typ.instance_type
    if isinstance(arr_typ, bodo.libs.array_item_arr_ext.ArrayItemArrayType
        ) or arr_typ == bodo.string_array_type:
        data_arr_typ = arr_typ.dtype
        return lambda arr_typ: (0,) + init_nested_counts(data_arr_typ)
    if bodo.utils.utils.is_array_typ(arr_typ, False
        ) or arr_typ == bodo.string_type:
        return lambda arr_typ: (0,)
    return lambda arr_typ: ()


def add_nested_counts(nested_counts, arr_item):
    return 0,


@overload(add_nested_counts)
def overload_add_nested_counts(nested_counts, arr_item):
    from bodo.libs.str_arr_ext import get_utf8_size
    arr_item = arr_item.type if isinstance(arr_item, types.Optional
        ) else arr_item
    if isinstance(arr_item, bodo.libs.array_item_arr_ext.ArrayItemArrayType):
        return lambda nested_counts, arr_item: (nested_counts[0] + len(
            arr_item),) + add_nested_counts(nested_counts[1:], bodo.libs.
            array_item_arr_ext.get_data(arr_item))
    if isinstance(arr_item, types.List):
        return lambda nested_counts, arr_item: add_nested_counts(nested_counts,
            bodo.utils.conversion.coerce_to_array(arr_item))
    if arr_item == bodo.string_array_type:
        return lambda nested_counts, arr_item: (nested_counts[0] + len(
            arr_item), nested_counts[1] + np.int64(bodo.libs.str_arr_ext.
            num_total_chars(arr_item)))
    if bodo.utils.utils.is_array_typ(arr_item, False):
        return lambda nested_counts, arr_item: (nested_counts[0] + len(
            arr_item),)
    if arr_item == bodo.string_type:
        return lambda nested_counts, arr_item: (nested_counts[0] +
            get_utf8_size(arr_item),)
    return lambda nested_counts, arr_item: ()


@overload(operator.setitem)
def none_optional_setitem_overload(A, idx, val):
    if not bodo.utils.utils.is_array_typ(A, False):
        return
    elif val == types.none:
        if isinstance(idx, types.Integer):
            return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)
        elif bodo.utils.typing.is_list_like_index_type(idx) and isinstance(idx
            .dtype, types.Integer):

            def setitem_none_int_arr(A, idx, val):
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                for ndhf__fpy in idx:
                    bodo.libs.array_kernels.setna(A, ndhf__fpy)
            return setitem_none_int_arr
        elif bodo.utils.typing.is_list_like_index_type(idx
            ) and idx.dtype == types.bool_:
            if A == bodo.string_array_type:

                def string_arr_impl(A, idx, val):
                    n = len(A)
                    idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                    jsxv__erm = bodo.libs.str_arr_ext.pre_alloc_string_array(n,
                        -1)
                    for ndhf__fpy in numba.parfors.parfor.internal_prange(n):
                        if idx[ndhf__fpy] or bodo.libs.array_kernels.isna(A,
                            ndhf__fpy):
                            jsxv__erm[ndhf__fpy] = ''
                            bodo.libs.str_arr_ext.str_arr_set_na(jsxv__erm,
                                ndhf__fpy)
                        else:
                            jsxv__erm[ndhf__fpy] = A[ndhf__fpy]
                    bodo.libs.str_arr_ext.move_str_binary_arr_payload(A,
                        jsxv__erm)
                return string_arr_impl

            def setitem_none_bool_arr(A, idx, val):
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                n = len(idx)
                for ndhf__fpy in range(n):
                    if not bodo.libs.array_kernels.isna(idx, ndhf__fpy
                        ) and idx[ndhf__fpy]:
                        bodo.libs.array_kernels.setna(A, ndhf__fpy)
            return setitem_none_bool_arr
        elif isinstance(idx, types.SliceType):

            def setitem_none_slice(A, idx, val):
                n = len(A)
                dxb__jtve = numba.cpython.unicode._normalize_slice(idx, n)
                for ndhf__fpy in range(dxb__jtve.start, dxb__jtve.stop,
                    dxb__jtve.step):
                    bodo.libs.array_kernels.setna(A, ndhf__fpy)
            return setitem_none_slice
        raise BodoError(
            f'setitem for {A} with indexing type {idx} and None value not supported.'
            )
    elif isinstance(val, types.optional):
        if isinstance(idx, types.Integer):

            def impl_optional(A, idx, val):
                if val is None:
                    bodo.libs.array_kernels.setna(A, idx)
                else:
                    A[idx] = bodo.utils.indexing.unoptional(val)
            return impl_optional
        elif bodo.utils.typing.is_list_like_index_type(idx) and isinstance(idx
            .dtype, types.Integer):

            def setitem_optional_int_arr(A, idx, val):
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                for ndhf__fpy in idx:
                    if val is None:
                        bodo.libs.array_kernels.setna(A, ndhf__fpy)
                        continue
                    A[ndhf__fpy] = bodo.utils.indexing.unoptional(val)
            return setitem_optional_int_arr
        elif bodo.utils.typing.is_list_like_index_type(idx
            ) and idx.dtype == types.bool_:
            if A == bodo.string_array_type:

                def string_arr_impl(A, idx, val):
                    if val is None:
                        A[idx] = None
                    else:
                        A[idx] = bodo.utils.indexing.unoptional(val)
                return string_arr_impl

            def setitem_optional_bool_arr(A, idx, val):
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                n = len(idx)
                for ndhf__fpy in range(n):
                    if not bodo.libs.array_kernels.isna(idx, ndhf__fpy
                        ) and idx[ndhf__fpy]:
                        if val is None:
                            bodo.libs.array_kernels.setna(A, ndhf__fpy)
                            continue
                        A[ndhf__fpy] = bodo.utils.indexing.unoptional(val)
            return setitem_optional_bool_arr
        elif isinstance(idx, types.SliceType):

            def setitem_optional_slice(A, idx, val):
                n = len(A)
                dxb__jtve = numba.cpython.unicode._normalize_slice(idx, n)
                for ndhf__fpy in range(dxb__jtve.start, dxb__jtve.stop,
                    dxb__jtve.step):
                    if val is None:
                        bodo.libs.array_kernels.setna(A, ndhf__fpy)
                        continue
                    A[ndhf__fpy] = bodo.utils.indexing.unoptional(val)
            return setitem_optional_slice
        raise BodoError(
            f'setitem for {A} with indexing type {idx} and optional value not supported.'
            )


@intrinsic
def unoptional(typingctx, val_t=None):
    if not isinstance(val_t, types.Optional):
        return val_t(val_t), lambda c, b, s, args: impl_ret_borrowed(c, b,
            val_t, args[0])

    def codegen(context, builder, signature, args):
        djrv__mlr = context.make_helper(builder, val_t, args[0])
        foeiv__kdm = djrv__mlr.data
        context.nrt.incref(builder, val_t.type, foeiv__kdm)
        return foeiv__kdm
    return val_t.type(val_t), codegen
