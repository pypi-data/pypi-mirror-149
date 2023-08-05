"""Array implementation for string objects, which are usually immutable.
The characters are stored in a contingous data array, and an offsets array marks the
the individual strings. For example:
value:             ['a', 'bc', '', 'abc', None, 'bb']
data:              [a, b, c, a, b, c, b, b]
offsets:           [0, 1, 3, 3, 6, 6, 8]
"""
import glob
import operator
import numba
import numba.core.typing.typeof
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.unsafe.bytes import memcpy_region
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, pre_alloc_binary_array
from bodo.libs.str_ext import memcmp, string_type, unicode_to_utf8_and_len
from bodo.utils.typing import BodoArrayIterator, BodoError, decode_if_dict_array, is_list_like_index_type, is_overload_constant_int, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
use_pd_string_array = False
char_type = types.uint8
char_arr_type = types.Array(char_type, 1, 'C')
offset_arr_type = types.Array(offset_type, 1, 'C')
null_bitmap_arr_type = types.Array(types.uint8, 1, 'C')
data_ctypes_type = types.ArrayCTypes(char_arr_type)
offset_ctypes_type = types.ArrayCTypes(offset_arr_type)


class StringArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(StringArrayType, self).__init__(name='StringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    def copy(self):
        return StringArrayType()


string_array_type = StringArrayType()


@typeof_impl.register(pd.arrays.StringArray)
def typeof_string_array(val, c):
    return string_array_type


@register_model(BinaryArrayType)
@register_model(StringArrayType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ljy__dore = ArrayItemArrayType(char_arr_type)
        vgwjj__pnst = [('data', ljy__dore)]
        models.StructModel.__init__(self, dmm, fe_type, vgwjj__pnst)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        sau__auktc, = args
        tru__ctfen = context.make_helper(builder, string_array_type)
        tru__ctfen.data = sau__auktc
        context.nrt.incref(builder, data_typ, sau__auktc)
        return tru__ctfen._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    vbu__jku = c.context.insert_const_string(c.builder.module, 'pandas')
    edwps__khvj = c.pyapi.import_module_noblock(vbu__jku)
    aill__ied = c.pyapi.call_method(edwps__khvj, 'StringDtype', ())
    c.pyapi.decref(edwps__khvj)
    return aill__ied


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        bnb__noel = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs)
        if bnb__noel is not None:
            return bnb__noel
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                imf__tflh = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(imf__tflh)
                for i in numba.parfors.parfor.internal_prange(imf__tflh):
                    if bodo.libs.array_kernels.isna(lhs, i
                        ) or bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_both
        if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

            def impl_left(lhs, rhs):
                numba.parfors.parfor.init_prange()
                imf__tflh = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(imf__tflh)
                for i in numba.parfors.parfor.internal_prange(imf__tflh):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs)
                    out_arr[i] = val
                return out_arr
            return impl_left
        if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

            def impl_right(lhs, rhs):
                numba.parfors.parfor.init_prange()
                imf__tflh = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(imf__tflh)
                for i in numba.parfors.parfor.internal_prange(imf__tflh):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs, rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_right
        raise_bodo_error(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_string_array_binary_op


def overload_add_operator_string_array(lhs, rhs):
    anjv__ggt = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    ogc__dps = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and ogc__dps or anjv__ggt and is_str_arr_type(rhs):

        def impl_both(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j
                    ) or bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs[j]
            return out_arr
        return impl_both
    if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

        def impl_left(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs
            return out_arr
        return impl_left
    if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

        def impl_right(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(rhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs + rhs[j]
            return out_arr
        return impl_right


def overload_mul_operator_str_arr(lhs, rhs):
    if is_str_arr_type(lhs) and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] * rhs
            return out_arr
        return impl
    if isinstance(lhs, types.Integer) and is_str_arr_type(rhs):

        def impl(lhs, rhs):
            return rhs * lhs
        return impl


def _get_str_binary_arr_payload(context, builder, arr_value, arr_typ):
    assert arr_typ == string_array_type or arr_typ == binary_array_type
    zkytl__cdrm = context.make_helper(builder, arr_typ, arr_value)
    ljy__dore = ArrayItemArrayType(char_arr_type)
    ivb__pcm = _get_array_item_arr_payload(context, builder, ljy__dore,
        zkytl__cdrm.data)
    return ivb__pcm


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        return ivb__pcm.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        xtkc__flnsy = context.make_helper(builder, offset_arr_type,
            ivb__pcm.offsets).data
        return _get_num_total_chars(builder, xtkc__flnsy, ivb__pcm.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        zhs__kmewt = context.make_helper(builder, offset_arr_type, ivb__pcm
            .offsets)
        gylu__ayxc = context.make_helper(builder, offset_ctypes_type)
        gylu__ayxc.data = builder.bitcast(zhs__kmewt.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        gylu__ayxc.meminfo = zhs__kmewt.meminfo
        aill__ied = gylu__ayxc._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            aill__ied)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        sau__auktc = context.make_helper(builder, char_arr_type, ivb__pcm.data)
        gylu__ayxc = context.make_helper(builder, data_ctypes_type)
        gylu__ayxc.data = sau__auktc.data
        gylu__ayxc.meminfo = sau__auktc.meminfo
        aill__ied = gylu__ayxc._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, aill__ied)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        dvj__vawkq, ind = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, dvj__vawkq,
            sig.args[0])
        sau__auktc = context.make_helper(builder, char_arr_type, ivb__pcm.data)
        gylu__ayxc = context.make_helper(builder, data_ctypes_type)
        gylu__ayxc.data = builder.gep(sau__auktc.data, [ind])
        gylu__ayxc.meminfo = sau__auktc.meminfo
        aill__ied = gylu__ayxc._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, aill__ied)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        ckp__exty, ktx__lle, rgw__onrvt, ltdy__pqwt = args
        vnwis__qwca = builder.bitcast(builder.gep(ckp__exty, [ktx__lle]),
            lir.IntType(8).as_pointer())
        ihwi__ynddu = builder.bitcast(builder.gep(rgw__onrvt, [ltdy__pqwt]),
            lir.IntType(8).as_pointer())
        zmw__mfyy = builder.load(ihwi__ynddu)
        builder.store(zmw__mfyy, vnwis__qwca)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        qqu__baoc = context.make_helper(builder, null_bitmap_arr_type,
            ivb__pcm.null_bitmap)
        gylu__ayxc = context.make_helper(builder, data_ctypes_type)
        gylu__ayxc.data = qqu__baoc.data
        gylu__ayxc.meminfo = qqu__baoc.meminfo
        aill__ied = gylu__ayxc._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, aill__ied)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        xtkc__flnsy = context.make_helper(builder, offset_arr_type,
            ivb__pcm.offsets).data
        return builder.load(builder.gep(xtkc__flnsy, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, ivb__pcm.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        rqj__ynvpa, ind = args
        if in_bitmap_typ == data_ctypes_type:
            gylu__ayxc = context.make_helper(builder, data_ctypes_type,
                rqj__ynvpa)
            rqj__ynvpa = gylu__ayxc.data
        return builder.load(builder.gep(rqj__ynvpa, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        rqj__ynvpa, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            gylu__ayxc = context.make_helper(builder, data_ctypes_type,
                rqj__ynvpa)
            rqj__ynvpa = gylu__ayxc.data
        builder.store(val, builder.gep(rqj__ynvpa, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        gpfio__sobp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        uoxhv__mezm = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        wzc__hnq = context.make_helper(builder, offset_arr_type,
            gpfio__sobp.offsets).data
        apwm__qqcbj = context.make_helper(builder, offset_arr_type,
            uoxhv__mezm.offsets).data
        nkelm__eqf = context.make_helper(builder, char_arr_type,
            gpfio__sobp.data).data
        uxlu__fgwt = context.make_helper(builder, char_arr_type,
            uoxhv__mezm.data).data
        rrs__dilgj = context.make_helper(builder, null_bitmap_arr_type,
            gpfio__sobp.null_bitmap).data
        ieiv__amcqy = context.make_helper(builder, null_bitmap_arr_type,
            uoxhv__mezm.null_bitmap).data
        nwdyt__xto = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, apwm__qqcbj, wzc__hnq, nwdyt__xto)
        cgutils.memcpy(builder, uxlu__fgwt, nkelm__eqf, builder.load(
            builder.gep(wzc__hnq, [ind])))
        asez__suy = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        mrce__gwp = builder.lshr(asez__suy, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, ieiv__amcqy, rrs__dilgj, mrce__gwp)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        gpfio__sobp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        uoxhv__mezm = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        wzc__hnq = context.make_helper(builder, offset_arr_type,
            gpfio__sobp.offsets).data
        nkelm__eqf = context.make_helper(builder, char_arr_type,
            gpfio__sobp.data).data
        uxlu__fgwt = context.make_helper(builder, char_arr_type,
            uoxhv__mezm.data).data
        num_total_chars = _get_num_total_chars(builder, wzc__hnq,
            gpfio__sobp.n_arrays)
        cgutils.memcpy(builder, uxlu__fgwt, nkelm__eqf, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        gpfio__sobp = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        uoxhv__mezm = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        wzc__hnq = context.make_helper(builder, offset_arr_type,
            gpfio__sobp.offsets).data
        apwm__qqcbj = context.make_helper(builder, offset_arr_type,
            uoxhv__mezm.offsets).data
        rrs__dilgj = context.make_helper(builder, null_bitmap_arr_type,
            gpfio__sobp.null_bitmap).data
        imf__tflh = gpfio__sobp.n_arrays
        zhuuf__ecvq = context.get_constant(offset_type, 0)
        rwq__ztw = cgutils.alloca_once_value(builder, zhuuf__ecvq)
        with cgutils.for_range(builder, imf__tflh) as oemf__joof:
            zus__sng = lower_is_na(context, builder, rrs__dilgj, oemf__joof
                .index)
            with cgutils.if_likely(builder, builder.not_(zus__sng)):
                jhmsu__pdze = builder.load(builder.gep(wzc__hnq, [
                    oemf__joof.index]))
                ujxm__tsarv = builder.load(rwq__ztw)
                builder.store(jhmsu__pdze, builder.gep(apwm__qqcbj, [
                    ujxm__tsarv]))
                builder.store(builder.add(ujxm__tsarv, lir.Constant(context
                    .get_value_type(offset_type), 1)), rwq__ztw)
        ujxm__tsarv = builder.load(rwq__ztw)
        jhmsu__pdze = builder.load(builder.gep(wzc__hnq, [imf__tflh]))
        builder.store(jhmsu__pdze, builder.gep(apwm__qqcbj, [ujxm__tsarv]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        sxr__hmg, ind, str, qfqi__vquw = args
        sxr__hmg = context.make_array(sig.args[0])(context, builder, sxr__hmg)
        vrub__vcxq = builder.gep(sxr__hmg.data, [ind])
        cgutils.raw_memcpy(builder, vrub__vcxq, str, qfqi__vquw, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        vrub__vcxq, ind, tmuza__dijra, qfqi__vquw = args
        vrub__vcxq = builder.gep(vrub__vcxq, [ind])
        cgutils.raw_memcpy(builder, vrub__vcxq, tmuza__dijra, qfqi__vquw, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    otaan__lgsvv = np.int64(getitem_str_offset(A, i))
    fuy__fdmwd = np.int64(getitem_str_offset(A, i + 1))
    l = fuy__fdmwd - otaan__lgsvv
    bnhcq__drv = get_data_ptr_ind(A, otaan__lgsvv)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(bnhcq__drv, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    uaal__wrrrl = getitem_str_offset(A, i)
    clv__lazv = getitem_str_offset(A, i + 1)
    txmfn__smr = clv__lazv - uaal__wrrrl
    otl__adp = getitem_str_offset(B, j)
    vvr__ekgmi = otl__adp + txmfn__smr
    setitem_str_offset(B, j + 1, vvr__ekgmi)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if txmfn__smr != 0:
        sau__auktc = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(sau__auktc, np.
            int64(otl__adp), np.int64(vvr__ekgmi))
        enida__kjd = get_data_ptr(B).data
        whndc__jgle = get_data_ptr(A).data
        memcpy_region(enida__kjd, otl__adp, whndc__jgle, uaal__wrrrl,
            txmfn__smr, 1)


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    imf__tflh = len(str_arr)
    paeg__aqrmd = np.empty(imf__tflh, np.bool_)
    for i in range(imf__tflh):
        paeg__aqrmd[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return paeg__aqrmd


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            imf__tflh = len(data)
            l = []
            for i in range(imf__tflh):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        ujhm__jfqy = data.count
        mhfb__etutu = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(ujhm__jfqy)]
        if is_overload_true(str_null_bools):
            mhfb__etutu += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(ujhm__jfqy) if is_str_arr_type(data.types[i]) or data
                .types[i] == binary_array_type]
        lcjq__vsa = 'def f(data, str_null_bools=None):\n'
        lcjq__vsa += '  return ({}{})\n'.format(', '.join(mhfb__etutu), ',' if
            ujhm__jfqy == 1 else '')
        rbni__fcn = {}
        exec(lcjq__vsa, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, rbni__fcn)
        sfd__qylj = rbni__fcn['f']
        return sfd__qylj
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                imf__tflh = len(list_data)
                for i in range(imf__tflh):
                    tmuza__dijra = list_data[i]
                    str_arr[i] = tmuza__dijra
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                imf__tflh = len(list_data)
                for i in range(imf__tflh):
                    tmuza__dijra = list_data[i]
                    str_arr[i] = tmuza__dijra
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        ujhm__jfqy = str_arr.count
        xbm__hcrn = 0
        lcjq__vsa = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(ujhm__jfqy):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                lcjq__vsa += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, ujhm__jfqy + xbm__hcrn))
                xbm__hcrn += 1
            else:
                lcjq__vsa += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        lcjq__vsa += '  return\n'
        rbni__fcn = {}
        exec(lcjq__vsa, {'cp_str_list_to_array': cp_str_list_to_array},
            rbni__fcn)
        ebu__jylb = rbni__fcn['f']
        return ebu__jylb
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            imf__tflh = len(str_list)
            str_arr = pre_alloc_string_array(imf__tflh, -1)
            for i in range(imf__tflh):
                tmuza__dijra = str_list[i]
                str_arr[i] = tmuza__dijra
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            imf__tflh = len(A)
            xyme__mhmvp = 0
            for i in range(imf__tflh):
                tmuza__dijra = A[i]
                xyme__mhmvp += get_utf8_size(tmuza__dijra)
            return xyme__mhmvp
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        imf__tflh = len(arr)
        n_chars = num_total_chars(arr)
        wgrtd__cka = pre_alloc_string_array(imf__tflh, np.int64(n_chars))
        copy_str_arr_slice(wgrtd__cka, arr, imf__tflh)
        return wgrtd__cka
    return copy_impl


@overload(len, no_unliteral=True)
def str_arr_len_overload(str_arr):
    if str_arr == string_array_type:

        def str_arr_len(str_arr):
            return str_arr.size
        return str_arr_len


@overload_attribute(StringArrayType, 'size')
def str_arr_size_overload(str_arr):
    return lambda str_arr: len(str_arr._data)


@overload_attribute(StringArrayType, 'shape')
def str_arr_shape_overload(str_arr):
    return lambda str_arr: (str_arr.size,)


@overload_attribute(StringArrayType, 'nbytes')
def str_arr_nbytes_overload(str_arr):
    return lambda str_arr: str_arr._data.nbytes


@overload_method(types.Array, 'tolist', no_unliteral=True)
@overload_method(StringArrayType, 'tolist', no_unliteral=True)
def overload_to_list(arr):
    return lambda arr: list(arr)


import llvmlite.binding as ll
from llvmlite import ir as lir
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('setitem_string_array', hstr_ext.setitem_string_array)
ll.add_symbol('is_na', hstr_ext.is_na)
ll.add_symbol('string_array_from_sequence', array_ext.
    string_array_from_sequence)
ll.add_symbol('pd_array_from_string_array', hstr_ext.pd_array_from_string_array
    )
ll.add_symbol('np_array_from_string_array', hstr_ext.np_array_from_string_array
    )
ll.add_symbol('convert_len_arr_to_offset32', hstr_ext.
    convert_len_arr_to_offset32)
ll.add_symbol('convert_len_arr_to_offset', hstr_ext.convert_len_arr_to_offset)
ll.add_symbol('set_string_array_range', hstr_ext.set_string_array_range)
ll.add_symbol('str_arr_to_int64', hstr_ext.str_arr_to_int64)
ll.add_symbol('str_arr_to_float64', hstr_ext.str_arr_to_float64)
ll.add_symbol('get_utf8_size', hstr_ext.get_utf8_size)
ll.add_symbol('print_str_arr', hstr_ext.print_str_arr)
ll.add_symbol('inplace_int64_to_str', hstr_ext.inplace_int64_to_str)
inplace_int64_to_str = types.ExternalFunction('inplace_int64_to_str', types
    .void(types.voidptr, types.int64, types.int64))
convert_len_arr_to_offset32 = types.ExternalFunction(
    'convert_len_arr_to_offset32', types.void(types.voidptr, types.intp))
convert_len_arr_to_offset = types.ExternalFunction('convert_len_arr_to_offset',
    types.void(types.voidptr, types.voidptr, types.intp))
setitem_string_array = types.ExternalFunction('setitem_string_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, offset_type, offset_type, types.intp))
_get_utf8_size = types.ExternalFunction('get_utf8_size', types.intp(types.
    voidptr, types.intp, offset_type))
_print_str_arr = types.ExternalFunction('print_str_arr', types.void(types.
    uint64, types.uint64, types.CPointer(offset_type), types.CPointer(
    char_type)))


@numba.generated_jit(nopython=True)
def empty_str_arr(in_seq):
    lcjq__vsa = 'def f(in_seq):\n'
    lcjq__vsa += '    n_strs = len(in_seq)\n'
    lcjq__vsa += '    A = pre_alloc_string_array(n_strs, -1)\n'
    lcjq__vsa += '    return A\n'
    rbni__fcn = {}
    exec(lcjq__vsa, {'pre_alloc_string_array': pre_alloc_string_array},
        rbni__fcn)
    gota__pin = rbni__fcn['f']
    return gota__pin


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        diq__zrdk = 'pre_alloc_binary_array'
    else:
        diq__zrdk = 'pre_alloc_string_array'
    lcjq__vsa = 'def f(in_seq):\n'
    lcjq__vsa += '    n_strs = len(in_seq)\n'
    lcjq__vsa += f'    A = {diq__zrdk}(n_strs, -1)\n'
    lcjq__vsa += '    for i in range(n_strs):\n'
    lcjq__vsa += '        A[i] = in_seq[i]\n'
    lcjq__vsa += '    return A\n'
    rbni__fcn = {}
    exec(lcjq__vsa, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, rbni__fcn)
    gota__pin = rbni__fcn['f']
    return gota__pin


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        wae__lonm = builder.add(ivb__pcm.n_arrays, lir.Constant(lir.IntType
            (64), 1))
        muv__niy = builder.lshr(lir.Constant(lir.IntType(64), offset_type.
            bitwidth), lir.Constant(lir.IntType(64), 3))
        mrce__gwp = builder.mul(wae__lonm, muv__niy)
        wtdue__izptx = context.make_array(offset_arr_type)(context, builder,
            ivb__pcm.offsets).data
        cgutils.memset(builder, wtdue__izptx, mrce__gwp, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        fgw__kwkf = ivb__pcm.n_arrays
        mrce__gwp = builder.lshr(builder.add(fgw__kwkf, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        sge__bmkj = context.make_array(null_bitmap_arr_type)(context,
            builder, ivb__pcm.null_bitmap).data
        cgutils.memset(builder, sge__bmkj, mrce__gwp, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@numba.njit
def pre_alloc_string_array(n_strs, n_chars):
    if n_chars is None:
        n_chars = -1
    str_arr = init_str_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_strs), (np.int64(n_chars),),
        char_arr_type))
    if n_chars == 0:
        set_all_offsets_to_0(str_arr)
    return str_arr


@register_jitable
def gen_na_str_array_lens(n_strs, total_len, len_arr):
    str_arr = pre_alloc_string_array(n_strs, total_len)
    set_bitmap_all_NA(str_arr)
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    oib__usb = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        jlb__ckqn = len(len_arr)
        for i in range(jlb__ckqn):
            offsets[i] = oib__usb
            oib__usb += len_arr[i]
        offsets[jlb__ckqn] = oib__usb
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    xzmlr__wzjwd = i // 8
    ujl__zxzx = getitem_str_bitmap(bits, xzmlr__wzjwd)
    ujl__zxzx ^= np.uint8(-np.uint8(bit_is_set) ^ ujl__zxzx) & kBitmask[i % 8]
    setitem_str_bitmap(bits, xzmlr__wzjwd, ujl__zxzx)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    slkdf__mcv = get_null_bitmap_ptr(out_str_arr)
    omp__zhtph = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        sce__fup = get_bit_bitmap(omp__zhtph, j)
        set_bit_to(slkdf__mcv, out_start + j, sce__fup)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, dvj__vawkq, ylboe__hzo, kwew__dcq = args
        gpfio__sobp = _get_str_binary_arr_payload(context, builder,
            dvj__vawkq, string_array_type)
        uoxhv__mezm = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        wzc__hnq = context.make_helper(builder, offset_arr_type,
            gpfio__sobp.offsets).data
        apwm__qqcbj = context.make_helper(builder, offset_arr_type,
            uoxhv__mezm.offsets).data
        nkelm__eqf = context.make_helper(builder, char_arr_type,
            gpfio__sobp.data).data
        uxlu__fgwt = context.make_helper(builder, char_arr_type,
            uoxhv__mezm.data).data
        num_total_chars = _get_num_total_chars(builder, wzc__hnq,
            gpfio__sobp.n_arrays)
        iqti__jwd = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        vqurl__qfkm = cgutils.get_or_insert_function(builder.module,
            iqti__jwd, name='set_string_array_range')
        builder.call(vqurl__qfkm, [apwm__qqcbj, uxlu__fgwt, wzc__hnq,
            nkelm__eqf, ylboe__hzo, kwew__dcq, gpfio__sobp.n_arrays,
            num_total_chars])
        zqt__eyvmd = context.typing_context.resolve_value_type(copy_nulls_range
            )
        qkkn__fwwcm = zqt__eyvmd.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        aupre__pmsmv = context.get_function(zqt__eyvmd, qkkn__fwwcm)
        aupre__pmsmv(builder, (out_arr, dvj__vawkq, ylboe__hzo))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    cvpd__jrlxi = c.context.make_helper(c.builder, typ, val)
    ljy__dore = ArrayItemArrayType(char_arr_type)
    ivb__pcm = _get_array_item_arr_payload(c.context, c.builder, ljy__dore,
        cvpd__jrlxi.data)
    rhwn__ozmbf = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    rpkxi__kmq = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        rpkxi__kmq = 'pd_array_from_string_array'
    iqti__jwd = lir.FunctionType(c.context.get_argument_type(types.pyobject
        ), [lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
        lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
        IntType(32)])
    ogwb__aisgr = cgutils.get_or_insert_function(c.builder.module,
        iqti__jwd, name=rpkxi__kmq)
    xtkc__flnsy = c.context.make_array(offset_arr_type)(c.context, c.
        builder, ivb__pcm.offsets).data
    bnhcq__drv = c.context.make_array(char_arr_type)(c.context, c.builder,
        ivb__pcm.data).data
    sge__bmkj = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, ivb__pcm.null_bitmap).data
    arr = c.builder.call(ogwb__aisgr, [ivb__pcm.n_arrays, xtkc__flnsy,
        bnhcq__drv, sge__bmkj, rhwn__ozmbf])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        sge__bmkj = context.make_array(null_bitmap_arr_type)(context,
            builder, ivb__pcm.null_bitmap).data
        xhgei__hoi = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        qud__kpa = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        ujl__zxzx = builder.load(builder.gep(sge__bmkj, [xhgei__hoi],
            inbounds=True))
        weulp__sxf = lir.ArrayType(lir.IntType(8), 8)
        wcriv__uwze = cgutils.alloca_once_value(builder, lir.Constant(
            weulp__sxf, (1, 2, 4, 8, 16, 32, 64, 128)))
        vlai__pwvtv = builder.load(builder.gep(wcriv__uwze, [lir.Constant(
            lir.IntType(64), 0), qud__kpa], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(ujl__zxzx,
            vlai__pwvtv), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        xhgei__hoi = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        qud__kpa = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        sge__bmkj = context.make_array(null_bitmap_arr_type)(context,
            builder, ivb__pcm.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, ivb__pcm.
            offsets).data
        sgm__hvbf = builder.gep(sge__bmkj, [xhgei__hoi], inbounds=True)
        ujl__zxzx = builder.load(sgm__hvbf)
        weulp__sxf = lir.ArrayType(lir.IntType(8), 8)
        wcriv__uwze = cgutils.alloca_once_value(builder, lir.Constant(
            weulp__sxf, (1, 2, 4, 8, 16, 32, 64, 128)))
        vlai__pwvtv = builder.load(builder.gep(wcriv__uwze, [lir.Constant(
            lir.IntType(64), 0), qud__kpa], inbounds=True))
        vlai__pwvtv = builder.xor(vlai__pwvtv, lir.Constant(lir.IntType(8), -1)
            )
        builder.store(builder.and_(ujl__zxzx, vlai__pwvtv), sgm__hvbf)
        if str_arr_typ == string_array_type:
            gxt__ker = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            xey__yxzzi = builder.icmp_unsigned('!=', gxt__ker, ivb__pcm.
                n_arrays)
            with builder.if_then(xey__yxzzi):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [gxt__ker]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        xhgei__hoi = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        qud__kpa = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        sge__bmkj = context.make_array(null_bitmap_arr_type)(context,
            builder, ivb__pcm.null_bitmap).data
        sgm__hvbf = builder.gep(sge__bmkj, [xhgei__hoi], inbounds=True)
        ujl__zxzx = builder.load(sgm__hvbf)
        weulp__sxf = lir.ArrayType(lir.IntType(8), 8)
        wcriv__uwze = cgutils.alloca_once_value(builder, lir.Constant(
            weulp__sxf, (1, 2, 4, 8, 16, 32, 64, 128)))
        vlai__pwvtv = builder.load(builder.gep(wcriv__uwze, [lir.Constant(
            lir.IntType(64), 0), qud__kpa], inbounds=True))
        builder.store(builder.or_(ujl__zxzx, vlai__pwvtv), sgm__hvbf)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        mrce__gwp = builder.udiv(builder.add(ivb__pcm.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        sge__bmkj = context.make_array(null_bitmap_arr_type)(context,
            builder, ivb__pcm.null_bitmap).data
        cgutils.memset(builder, sge__bmkj, mrce__gwp, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    fgsdi__gsu = context.make_helper(builder, string_array_type, str_arr)
    ljy__dore = ArrayItemArrayType(char_arr_type)
    bhh__lyq = context.make_helper(builder, ljy__dore, fgsdi__gsu.data)
    zrv__mti = ArrayItemArrayPayloadType(ljy__dore)
    kgk__ymo = context.nrt.meminfo_data(builder, bhh__lyq.meminfo)
    gqp__gzhsm = builder.bitcast(kgk__ymo, context.get_value_type(zrv__mti)
        .as_pointer())
    return gqp__gzhsm


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        bezi__wtmr, itvki__fitfp = args
        uqhcg__htm = _get_str_binary_arr_data_payload_ptr(context, builder,
            itvki__fitfp)
        nhvaf__xpvn = _get_str_binary_arr_data_payload_ptr(context, builder,
            bezi__wtmr)
        uki__sxtah = _get_str_binary_arr_payload(context, builder,
            itvki__fitfp, sig.args[1])
        jxlm__svmox = _get_str_binary_arr_payload(context, builder,
            bezi__wtmr, sig.args[0])
        context.nrt.incref(builder, char_arr_type, uki__sxtah.data)
        context.nrt.incref(builder, offset_arr_type, uki__sxtah.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, uki__sxtah.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, jxlm__svmox.data)
        context.nrt.decref(builder, offset_arr_type, jxlm__svmox.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, jxlm__svmox.
            null_bitmap)
        builder.store(builder.load(uqhcg__htm), nhvaf__xpvn)
        return context.get_dummy_value()
    return types.none(to_arr_typ, from_arr_typ), codegen


dummy_use = numba.njit(lambda a: None)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_utf8_size(s):
    if isinstance(s, types.StringLiteral):
        l = len(s.literal_value.encode())
        return lambda s: l

    def impl(s):
        if s is None:
            return 0
        s = bodo.utils.indexing.unoptional(s)
        if s._is_ascii == 1:
            return len(s)
        imf__tflh = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return imf__tflh
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, vrub__vcxq, qbcb__rbyen = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, arr, sig.
            args[0])
        offsets = context.make_helper(builder, offset_arr_type, ivb__pcm.
            offsets).data
        data = context.make_helper(builder, char_arr_type, ivb__pcm.data).data
        iqti__jwd = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        xdpoe__jfp = cgutils.get_or_insert_function(builder.module,
            iqti__jwd, name='setitem_string_array')
        sdl__ywtmp = context.get_constant(types.int32, -1)
        piv__xaow = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, ivb__pcm.
            n_arrays)
        builder.call(xdpoe__jfp, [offsets, data, num_total_chars, builder.
            extract_value(vrub__vcxq, 0), qbcb__rbyen, sdl__ywtmp,
            piv__xaow, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    iqti__jwd = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64)])
    aye__acec = cgutils.get_or_insert_function(builder.module, iqti__jwd,
        name='is_na')
    return builder.call(aye__acec, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        vnwis__qwca, ihwi__ynddu, ujhm__jfqy, xnzir__kftk = args
        cgutils.raw_memcpy(builder, vnwis__qwca, ihwi__ynddu, ujhm__jfqy,
            xnzir__kftk)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.voidptr, types.intp, types.intp
        ), codegen


@numba.njit
def print_str_arr(arr):
    _print_str_arr(num_strings(arr), num_total_chars(arr), get_offset_ptr(
        arr), get_data_ptr(arr))


def inplace_eq(A, i, val):
    return A[i] == val


@overload(inplace_eq)
def inplace_eq_overload(A, ind, val):

    def impl(A, ind, val):
        mqgh__derl, quk__ssh = unicode_to_utf8_and_len(val)
        oxj__ivb = getitem_str_offset(A, ind)
        pfzy__coe = getitem_str_offset(A, ind + 1)
        fcedq__hfb = pfzy__coe - oxj__ivb
        if fcedq__hfb != quk__ssh:
            return False
        vrub__vcxq = get_data_ptr_ind(A, oxj__ivb)
        return memcmp(vrub__vcxq, mqgh__derl, quk__ssh) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        oxj__ivb = getitem_str_offset(A, ind)
        fcedq__hfb = bodo.libs.str_ext.int_to_str_len(val)
        kng__vovl = oxj__ivb + fcedq__hfb
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data, oxj__ivb,
            kng__vovl)
        vrub__vcxq = get_data_ptr_ind(A, oxj__ivb)
        inplace_int64_to_str(vrub__vcxq, fcedq__hfb, val)
        setitem_str_offset(A, ind + 1, oxj__ivb + fcedq__hfb)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        vrub__vcxq, = args
        ztjw__rqrad = context.insert_const_string(builder.module, '<NA>')
        kpbe__zkh = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, vrub__vcxq, ztjw__rqrad, kpbe__zkh, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    zzx__wffua = len('<NA>')

    def impl(A, ind):
        oxj__ivb = getitem_str_offset(A, ind)
        kng__vovl = oxj__ivb + zzx__wffua
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data, oxj__ivb,
            kng__vovl)
        vrub__vcxq = get_data_ptr_ind(A, oxj__ivb)
        inplace_set_NA_str(vrub__vcxq)
        setitem_str_offset(A, ind + 1, oxj__ivb + zzx__wffua)
        str_arr_set_not_na(A, ind)
    return impl


@overload(operator.getitem, no_unliteral=True)
def str_arr_getitem_int(A, ind):
    if A != string_array_type:
        return
    if isinstance(ind, types.Integer):

        def str_arr_getitem_impl(A, ind):
            if ind < 0:
                ind += A.size
            oxj__ivb = getitem_str_offset(A, ind)
            pfzy__coe = getitem_str_offset(A, ind + 1)
            qbcb__rbyen = pfzy__coe - oxj__ivb
            vrub__vcxq = get_data_ptr_ind(A, oxj__ivb)
            ifki__nlhsz = decode_utf8(vrub__vcxq, qbcb__rbyen)
            return ifki__nlhsz
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            imf__tflh = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(imf__tflh):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            enida__kjd = get_data_ptr(out_arr).data
            whndc__jgle = get_data_ptr(A).data
            xbm__hcrn = 0
            ujxm__tsarv = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(imf__tflh):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    rmjr__ahpob = get_str_arr_item_length(A, i)
                    if rmjr__ahpob == 1:
                        copy_single_char(enida__kjd, ujxm__tsarv,
                            whndc__jgle, getitem_str_offset(A, i))
                    else:
                        memcpy_region(enida__kjd, ujxm__tsarv, whndc__jgle,
                            getitem_str_offset(A, i), rmjr__ahpob, 1)
                    ujxm__tsarv += rmjr__ahpob
                    setitem_str_offset(out_arr, xbm__hcrn + 1, ujxm__tsarv)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, xbm__hcrn)
                    else:
                        str_arr_set_not_na(out_arr, xbm__hcrn)
                    xbm__hcrn += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            imf__tflh = len(ind)
            out_arr = pre_alloc_string_array(imf__tflh, -1)
            xbm__hcrn = 0
            for i in range(imf__tflh):
                tmuza__dijra = A[ind[i]]
                out_arr[xbm__hcrn] = tmuza__dijra
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, xbm__hcrn)
                xbm__hcrn += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            imf__tflh = len(A)
            eor__ekl = numba.cpython.unicode._normalize_slice(ind, imf__tflh)
            jjht__iefcb = numba.cpython.unicode._slice_span(eor__ekl)
            if eor__ekl.step == 1:
                oxj__ivb = getitem_str_offset(A, eor__ekl.start)
                pfzy__coe = getitem_str_offset(A, eor__ekl.stop)
                n_chars = pfzy__coe - oxj__ivb
                wgrtd__cka = pre_alloc_string_array(jjht__iefcb, np.int64(
                    n_chars))
                for i in range(jjht__iefcb):
                    wgrtd__cka[i] = A[eor__ekl.start + i]
                    if str_arr_is_na(A, eor__ekl.start + i):
                        str_arr_set_na(wgrtd__cka, i)
                return wgrtd__cka
            else:
                wgrtd__cka = pre_alloc_string_array(jjht__iefcb, -1)
                for i in range(jjht__iefcb):
                    wgrtd__cka[i] = A[eor__ekl.start + i * eor__ekl.step]
                    if str_arr_is_na(A, eor__ekl.start + i * eor__ekl.step):
                        str_arr_set_na(wgrtd__cka, i)
                return wgrtd__cka
        return str_arr_slice_impl
    raise BodoError(
        f'getitem for StringArray with indexing type {ind} not supported.')


dummy_use = numba.njit(lambda a: None)


@overload(operator.setitem)
def str_arr_setitem(A, idx, val):
    if A != string_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    wohed__svi = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(wohed__svi)
        mkl__ihxn = 4

        def impl_scalar(A, idx, val):
            syiyv__bdqt = (val._length if val._is_ascii else mkl__ihxn *
                val._length)
            sau__auktc = A._data
            oxj__ivb = np.int64(getitem_str_offset(A, idx))
            kng__vovl = oxj__ivb + syiyv__bdqt
            bodo.libs.array_item_arr_ext.ensure_data_capacity(sau__auktc,
                oxj__ivb, kng__vovl)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                kng__vovl, val._data, val._length, val._kind, val._is_ascii,
                idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                eor__ekl = numba.cpython.unicode._normalize_slice(idx, len(A))
                otaan__lgsvv = eor__ekl.start
                sau__auktc = A._data
                oxj__ivb = np.int64(getitem_str_offset(A, otaan__lgsvv))
                kng__vovl = oxj__ivb + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(sau__auktc,
                    oxj__ivb, kng__vovl)
                set_string_array_range(A, val, otaan__lgsvv, oxj__ivb)
                xenfm__lnsbp = 0
                for i in range(eor__ekl.start, eor__ekl.stop, eor__ekl.step):
                    if str_arr_is_na(val, xenfm__lnsbp):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    xenfm__lnsbp += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                grjn__tjcz = str_list_to_array(val)
                A[idx] = grjn__tjcz
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                eor__ekl = numba.cpython.unicode._normalize_slice(idx, len(A))
                for i in range(eor__ekl.start, eor__ekl.stop, eor__ekl.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(wohed__svi)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                imf__tflh = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(imf__tflh, -1)
                for i in numba.parfors.parfor.internal_prange(imf__tflh):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        out_arr[i] = val
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_scalar
        elif val == string_array_type or isinstance(val, types.Array
            ) and isinstance(val.dtype, types.UnicodeCharSeq):

            def impl_bool_arr(A, idx, val):
                imf__tflh = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(imf__tflh, -1)
                rcrhu__xln = 0
                for i in numba.parfors.parfor.internal_prange(imf__tflh):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, rcrhu__xln):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, rcrhu__xln)
                        else:
                            out_arr[i] = str(val[rcrhu__xln])
                        rcrhu__xln += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(wohed__svi)
    raise BodoError(wohed__svi)


@overload_attribute(StringArrayType, 'dtype')
def overload_str_arr_dtype(A):
    return lambda A: pd.StringDtype()


@overload_attribute(StringArrayType, 'ndim')
def overload_str_arr_ndim(A):
    return lambda A: 1


@overload_method(StringArrayType, 'astype', no_unliteral=True)
def overload_str_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "StringArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.Function) and dtype.key[0] == str:
        return lambda A, dtype, copy=True: A
    ijyz__oewn = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(ijyz__oewn, (types.Float, types.Integer)
        ) and ijyz__oewn not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(ijyz__oewn, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            imf__tflh = len(A)
            B = np.empty(imf__tflh, ijyz__oewn)
            for i in numba.parfors.parfor.internal_prange(imf__tflh):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif ijyz__oewn == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            imf__tflh = len(A)
            B = np.empty(imf__tflh, ijyz__oewn)
            for i in numba.parfors.parfor.internal_prange(imf__tflh):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif ijyz__oewn == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            imf__tflh = len(A)
            B = np.empty(imf__tflh, ijyz__oewn)
            for i in numba.parfors.parfor.internal_prange(imf__tflh):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            imf__tflh = len(A)
            B = np.empty(imf__tflh, ijyz__oewn)
            for i in numba.parfors.parfor.internal_prange(imf__tflh):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        vrub__vcxq, qbcb__rbyen = args
        qaxl__gsh = context.get_python_api(builder)
        ocprq__lgp = qaxl__gsh.string_from_string_and_size(vrub__vcxq,
            qbcb__rbyen)
        ffc__rrvhi = qaxl__gsh.to_native_value(string_type, ocprq__lgp).value
        shm__vne = cgutils.create_struct_proxy(string_type)(context,
            builder, ffc__rrvhi)
        shm__vne.hash = shm__vne.hash.type(-1)
        qaxl__gsh.decref(ocprq__lgp)
        return shm__vne._getvalue()
    return string_type(types.voidptr, types.intp), codegen


def get_arr_data_ptr(arr, ind):
    return arr


@overload(get_arr_data_ptr, no_unliteral=True)
def overload_get_arr_data_ptr(arr, ind):
    assert isinstance(types.unliteral(ind), types.Integer)
    if isinstance(arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(arr, ind):
            return bodo.hiframes.split_impl.get_c_arr_ptr(arr._data.ctypes, ind
                )
        return impl_int
    assert isinstance(arr, types.Array)

    def impl_np(arr, ind):
        return bodo.hiframes.split_impl.get_c_arr_ptr(arr.ctypes, ind)
    return impl_np


def set_to_numeric_out_na_err(out_arr, out_ind, err_code):
    pass


@overload(set_to_numeric_out_na_err)
def set_to_numeric_out_na_err_overload(out_arr, out_ind, err_code):
    if isinstance(out_arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(out_arr, out_ind, err_code):
            bodo.libs.int_arr_ext.set_bit_to_arr(out_arr._null_bitmap,
                out_ind, 0 if err_code == -1 else 1)
        return impl_int
    assert isinstance(out_arr, types.Array)
    if isinstance(out_arr.dtype, types.Float):

        def impl_np(out_arr, out_ind, err_code):
            if err_code == -1:
                out_arr[out_ind] = np.nan
        return impl_np
    return lambda out_arr, out_ind, err_code: None


@numba.njit(no_cpython_wrapper=True)
def str_arr_item_to_numeric(out_arr, out_ind, str_arr, ind):
    str_arr = decode_if_dict_array(str_arr)
    err_code = _str_arr_item_to_numeric(get_arr_data_ptr(out_arr, out_ind),
        str_arr, ind, out_arr.dtype)
    set_to_numeric_out_na_err(out_arr, out_ind, err_code)


@intrinsic
def _str_arr_item_to_numeric(typingctx, out_ptr_t, str_arr_t, ind_t,
    out_dtype_t=None):
    assert str_arr_t == string_array_type, '_str_arr_item_to_numeric: str arr expected'
    assert ind_t == types.int64, '_str_arr_item_to_numeric: integer index expected'

    def codegen(context, builder, sig, args):
        vegkk__ank, arr, ind, zzlv__nesnd = args
        ivb__pcm = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, ivb__pcm.
            offsets).data
        data = context.make_helper(builder, char_arr_type, ivb__pcm.data).data
        iqti__jwd = lir.FunctionType(lir.IntType(32), [vegkk__ank.type, lir
            .IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        kxg__amyo = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            kxg__amyo = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        jdjp__zmbv = cgutils.get_or_insert_function(builder.module,
            iqti__jwd, kxg__amyo)
        return builder.call(jdjp__zmbv, [vegkk__ank, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    rhwn__ozmbf = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    iqti__jwd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(32)])
    rhvbe__yrej = cgutils.get_or_insert_function(c.builder.module,
        iqti__jwd, name='string_array_from_sequence')
    rxh__uzy = c.builder.call(rhvbe__yrej, [val, rhwn__ozmbf])
    ljy__dore = ArrayItemArrayType(char_arr_type)
    bhh__lyq = c.context.make_helper(c.builder, ljy__dore)
    bhh__lyq.meminfo = rxh__uzy
    fgsdi__gsu = c.context.make_helper(c.builder, typ)
    sau__auktc = bhh__lyq._getvalue()
    fgsdi__gsu.data = sau__auktc
    wguwq__zfna = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(fgsdi__gsu._getvalue(), is_error=wguwq__zfna)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    imf__tflh = len(pyval)
    ujxm__tsarv = 0
    bcll__hzstx = np.empty(imf__tflh + 1, np_offset_type)
    ycmu__ndhcm = []
    bqot__vrdoe = np.empty(imf__tflh + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        bcll__hzstx[i] = ujxm__tsarv
        rfs__xlk = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(bqot__vrdoe, i, int(not rfs__xlk))
        if rfs__xlk:
            continue
        jut__ssl = list(s.encode()) if isinstance(s, str) else list(s)
        ycmu__ndhcm.extend(jut__ssl)
        ujxm__tsarv += len(jut__ssl)
    bcll__hzstx[imf__tflh] = ujxm__tsarv
    dqmfd__itdv = np.array(ycmu__ndhcm, np.uint8)
    pdpyd__bvhr = context.get_constant(types.int64, imf__tflh)
    tleiw__wrsxk = context.get_constant_generic(builder, char_arr_type,
        dqmfd__itdv)
    wgc__qhhsi = context.get_constant_generic(builder, offset_arr_type,
        bcll__hzstx)
    ozlc__exes = context.get_constant_generic(builder, null_bitmap_arr_type,
        bqot__vrdoe)
    ivb__pcm = lir.Constant.literal_struct([pdpyd__bvhr, tleiw__wrsxk,
        wgc__qhhsi, ozlc__exes])
    ivb__pcm = cgutils.global_constant(builder, '.const.payload', ivb__pcm
        ).bitcast(cgutils.voidptr_t)
    rfw__cfocs = context.get_constant(types.int64, -1)
    flmjb__ubj = context.get_constant_null(types.voidptr)
    iwo__gvl = lir.Constant.literal_struct([rfw__cfocs, flmjb__ubj,
        flmjb__ubj, ivb__pcm, rfw__cfocs])
    iwo__gvl = cgutils.global_constant(builder, '.const.meminfo', iwo__gvl
        ).bitcast(cgutils.voidptr_t)
    sau__auktc = lir.Constant.literal_struct([iwo__gvl])
    fgsdi__gsu = lir.Constant.literal_struct([sau__auktc])
    return fgsdi__gsu


def pre_alloc_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_str_arr_ext_pre_alloc_string_array
    ) = pre_alloc_str_arr_equiv


@overload(glob.glob, no_unliteral=True)
def overload_glob_glob(pathname, recursive=False):

    def _glob_glob_impl(pathname, recursive=False):
        with numba.objmode(l='list_str_type'):
            l = glob.glob(pathname, recursive=recursive)
        return l
    return _glob_glob_impl
