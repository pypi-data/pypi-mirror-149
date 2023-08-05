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
        wuzpr__ovfvi = ArrayItemArrayType(char_arr_type)
        qqkls__gxobx = [('data', wuzpr__ovfvi)]
        models.StructModel.__init__(self, dmm, fe_type, qqkls__gxobx)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        epmv__jcpnn, = args
        dinsv__svdl = context.make_helper(builder, string_array_type)
        dinsv__svdl.data = epmv__jcpnn
        context.nrt.incref(builder, data_typ, epmv__jcpnn)
        return dinsv__svdl._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    pbqc__zajt = c.context.insert_const_string(c.builder.module, 'pandas')
    slc__hgrm = c.pyapi.import_module_noblock(pbqc__zajt)
    rktrx__tlog = c.pyapi.call_method(slc__hgrm, 'StringDtype', ())
    c.pyapi.decref(slc__hgrm)
    return rktrx__tlog


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        ulfmd__mvpwa = bodo.libs.dict_arr_ext.get_binary_op_overload(op,
            lhs, rhs)
        if ulfmd__mvpwa is not None:
            return ulfmd__mvpwa
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kwmjz__xrpk = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(kwmjz__xrpk)
                for i in numba.parfors.parfor.internal_prange(kwmjz__xrpk):
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
                kwmjz__xrpk = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(kwmjz__xrpk)
                for i in numba.parfors.parfor.internal_prange(kwmjz__xrpk):
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
                kwmjz__xrpk = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(kwmjz__xrpk)
                for i in numba.parfors.parfor.internal_prange(kwmjz__xrpk):
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
    ipp__rrefx = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    vgqj__rkzrq = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and vgqj__rkzrq or ipp__rrefx and is_str_arr_type(
        rhs):

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
    xrs__tjx = context.make_helper(builder, arr_typ, arr_value)
    wuzpr__ovfvi = ArrayItemArrayType(char_arr_type)
    lhy__erv = _get_array_item_arr_payload(context, builder, wuzpr__ovfvi,
        xrs__tjx.data)
    return lhy__erv


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        return lhy__erv.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        ilbti__bacxr = context.make_helper(builder, offset_arr_type,
            lhy__erv.offsets).data
        return _get_num_total_chars(builder, ilbti__bacxr, lhy__erv.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        pwg__aruc = context.make_helper(builder, offset_arr_type, lhy__erv.
            offsets)
        tujkt__igyu = context.make_helper(builder, offset_ctypes_type)
        tujkt__igyu.data = builder.bitcast(pwg__aruc.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        tujkt__igyu.meminfo = pwg__aruc.meminfo
        rktrx__tlog = tujkt__igyu._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            rktrx__tlog)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        epmv__jcpnn = context.make_helper(builder, char_arr_type, lhy__erv.data
            )
        tujkt__igyu = context.make_helper(builder, data_ctypes_type)
        tujkt__igyu.data = epmv__jcpnn.data
        tujkt__igyu.meminfo = epmv__jcpnn.meminfo
        rktrx__tlog = tujkt__igyu._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            rktrx__tlog)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        ehn__ztcf, ind = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, ehn__ztcf,
            sig.args[0])
        epmv__jcpnn = context.make_helper(builder, char_arr_type, lhy__erv.data
            )
        tujkt__igyu = context.make_helper(builder, data_ctypes_type)
        tujkt__igyu.data = builder.gep(epmv__jcpnn.data, [ind])
        tujkt__igyu.meminfo = epmv__jcpnn.meminfo
        rktrx__tlog = tujkt__igyu._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            rktrx__tlog)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        ulx__nfoe, vbez__cyob, oeavs__ndd, imj__nemk = args
        oezm__axq = builder.bitcast(builder.gep(ulx__nfoe, [vbez__cyob]),
            lir.IntType(8).as_pointer())
        ramq__tfwul = builder.bitcast(builder.gep(oeavs__ndd, [imj__nemk]),
            lir.IntType(8).as_pointer())
        uijxf__qvv = builder.load(ramq__tfwul)
        builder.store(uijxf__qvv, oezm__axq)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        ufe__fvirc = context.make_helper(builder, null_bitmap_arr_type,
            lhy__erv.null_bitmap)
        tujkt__igyu = context.make_helper(builder, data_ctypes_type)
        tujkt__igyu.data = ufe__fvirc.data
        tujkt__igyu.meminfo = ufe__fvirc.meminfo
        rktrx__tlog = tujkt__igyu._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            rktrx__tlog)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        ilbti__bacxr = context.make_helper(builder, offset_arr_type,
            lhy__erv.offsets).data
        return builder.load(builder.gep(ilbti__bacxr, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, lhy__erv.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        bsv__joiq, ind = args
        if in_bitmap_typ == data_ctypes_type:
            tujkt__igyu = context.make_helper(builder, data_ctypes_type,
                bsv__joiq)
            bsv__joiq = tujkt__igyu.data
        return builder.load(builder.gep(bsv__joiq, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        bsv__joiq, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            tujkt__igyu = context.make_helper(builder, data_ctypes_type,
                bsv__joiq)
            bsv__joiq = tujkt__igyu.data
        builder.store(val, builder.gep(bsv__joiq, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        okzh__cdg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        gfv__bgcix = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        pihou__lnsyp = context.make_helper(builder, offset_arr_type,
            okzh__cdg.offsets).data
        fqyuf__deced = context.make_helper(builder, offset_arr_type,
            gfv__bgcix.offsets).data
        mrxv__zoxd = context.make_helper(builder, char_arr_type, okzh__cdg.data
            ).data
        pczcx__inb = context.make_helper(builder, char_arr_type, gfv__bgcix
            .data).data
        xmi__rty = context.make_helper(builder, null_bitmap_arr_type,
            okzh__cdg.null_bitmap).data
        tmjbt__efxd = context.make_helper(builder, null_bitmap_arr_type,
            gfv__bgcix.null_bitmap).data
        xmyj__zenn = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, fqyuf__deced, pihou__lnsyp, xmyj__zenn)
        cgutils.memcpy(builder, pczcx__inb, mrxv__zoxd, builder.load(
            builder.gep(pihou__lnsyp, [ind])))
        fieaf__gedwn = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        zwg__pgmk = builder.lshr(fieaf__gedwn, lir.Constant(lir.IntType(64), 3)
            )
        cgutils.memcpy(builder, tmjbt__efxd, xmi__rty, zwg__pgmk)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        okzh__cdg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        gfv__bgcix = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        pihou__lnsyp = context.make_helper(builder, offset_arr_type,
            okzh__cdg.offsets).data
        mrxv__zoxd = context.make_helper(builder, char_arr_type, okzh__cdg.data
            ).data
        pczcx__inb = context.make_helper(builder, char_arr_type, gfv__bgcix
            .data).data
        num_total_chars = _get_num_total_chars(builder, pihou__lnsyp,
            okzh__cdg.n_arrays)
        cgutils.memcpy(builder, pczcx__inb, mrxv__zoxd, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        okzh__cdg = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        gfv__bgcix = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        pihou__lnsyp = context.make_helper(builder, offset_arr_type,
            okzh__cdg.offsets).data
        fqyuf__deced = context.make_helper(builder, offset_arr_type,
            gfv__bgcix.offsets).data
        xmi__rty = context.make_helper(builder, null_bitmap_arr_type,
            okzh__cdg.null_bitmap).data
        kwmjz__xrpk = okzh__cdg.n_arrays
        ffqi__uud = context.get_constant(offset_type, 0)
        klgh__hrlkb = cgutils.alloca_once_value(builder, ffqi__uud)
        with cgutils.for_range(builder, kwmjz__xrpk) as hzwy__tyoh:
            mmkr__lamv = lower_is_na(context, builder, xmi__rty, hzwy__tyoh
                .index)
            with cgutils.if_likely(builder, builder.not_(mmkr__lamv)):
                jyw__eyir = builder.load(builder.gep(pihou__lnsyp, [
                    hzwy__tyoh.index]))
                ydr__hgtku = builder.load(klgh__hrlkb)
                builder.store(jyw__eyir, builder.gep(fqyuf__deced, [
                    ydr__hgtku]))
                builder.store(builder.add(ydr__hgtku, lir.Constant(context.
                    get_value_type(offset_type), 1)), klgh__hrlkb)
        ydr__hgtku = builder.load(klgh__hrlkb)
        jyw__eyir = builder.load(builder.gep(pihou__lnsyp, [kwmjz__xrpk]))
        builder.store(jyw__eyir, builder.gep(fqyuf__deced, [ydr__hgtku]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        adjlo__foc, ind, str, rcox__ugf = args
        adjlo__foc = context.make_array(sig.args[0])(context, builder,
            adjlo__foc)
        kjtcn__igbkx = builder.gep(adjlo__foc.data, [ind])
        cgutils.raw_memcpy(builder, kjtcn__igbkx, str, rcox__ugf, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        kjtcn__igbkx, ind, sucpk__nsq, rcox__ugf = args
        kjtcn__igbkx = builder.gep(kjtcn__igbkx, [ind])
        cgutils.raw_memcpy(builder, kjtcn__igbkx, sucpk__nsq, rcox__ugf, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    gdey__nzhh = np.int64(getitem_str_offset(A, i))
    bgom__cir = np.int64(getitem_str_offset(A, i + 1))
    l = bgom__cir - gdey__nzhh
    ugut__egjp = get_data_ptr_ind(A, gdey__nzhh)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(ugut__egjp, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    ugdoj__cepk = getitem_str_offset(A, i)
    acamq__rgn = getitem_str_offset(A, i + 1)
    inmiq__pjxay = acamq__rgn - ugdoj__cepk
    ozn__rva = getitem_str_offset(B, j)
    qgbt__acb = ozn__rva + inmiq__pjxay
    setitem_str_offset(B, j + 1, qgbt__acb)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if inmiq__pjxay != 0:
        epmv__jcpnn = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(epmv__jcpnn, np.
            int64(ozn__rva), np.int64(qgbt__acb))
        vkw__cwd = get_data_ptr(B).data
        mlq__auzil = get_data_ptr(A).data
        memcpy_region(vkw__cwd, ozn__rva, mlq__auzil, ugdoj__cepk,
            inmiq__pjxay, 1)


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    kwmjz__xrpk = len(str_arr)
    ghfwx__ngp = np.empty(kwmjz__xrpk, np.bool_)
    for i in range(kwmjz__xrpk):
        ghfwx__ngp[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return ghfwx__ngp


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            kwmjz__xrpk = len(data)
            l = []
            for i in range(kwmjz__xrpk):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        ayvde__vbsx = data.count
        wathv__hqou = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(ayvde__vbsx)]
        if is_overload_true(str_null_bools):
            wathv__hqou += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(ayvde__vbsx) if is_str_arr_type(data.types[i]) or 
                data.types[i] == binary_array_type]
        cbtji__ast = 'def f(data, str_null_bools=None):\n'
        cbtji__ast += '  return ({}{})\n'.format(', '.join(wathv__hqou), 
            ',' if ayvde__vbsx == 1 else '')
        ocbjr__ijpzx = {}
        exec(cbtji__ast, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, ocbjr__ijpzx)
        teqc__tae = ocbjr__ijpzx['f']
        return teqc__tae
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                kwmjz__xrpk = len(list_data)
                for i in range(kwmjz__xrpk):
                    sucpk__nsq = list_data[i]
                    str_arr[i] = sucpk__nsq
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                kwmjz__xrpk = len(list_data)
                for i in range(kwmjz__xrpk):
                    sucpk__nsq = list_data[i]
                    str_arr[i] = sucpk__nsq
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        ayvde__vbsx = str_arr.count
        wyyz__wdy = 0
        cbtji__ast = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(ayvde__vbsx):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                cbtji__ast += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, ayvde__vbsx + wyyz__wdy))
                wyyz__wdy += 1
            else:
                cbtji__ast += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        cbtji__ast += '  return\n'
        ocbjr__ijpzx = {}
        exec(cbtji__ast, {'cp_str_list_to_array': cp_str_list_to_array},
            ocbjr__ijpzx)
        umi__xkmwo = ocbjr__ijpzx['f']
        return umi__xkmwo
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            kwmjz__xrpk = len(str_list)
            str_arr = pre_alloc_string_array(kwmjz__xrpk, -1)
            for i in range(kwmjz__xrpk):
                sucpk__nsq = str_list[i]
                str_arr[i] = sucpk__nsq
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            kwmjz__xrpk = len(A)
            ypmnj__hxiq = 0
            for i in range(kwmjz__xrpk):
                sucpk__nsq = A[i]
                ypmnj__hxiq += get_utf8_size(sucpk__nsq)
            return ypmnj__hxiq
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        kwmjz__xrpk = len(arr)
        n_chars = num_total_chars(arr)
        znbnd__inxz = pre_alloc_string_array(kwmjz__xrpk, np.int64(n_chars))
        copy_str_arr_slice(znbnd__inxz, arr, kwmjz__xrpk)
        return znbnd__inxz
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
    cbtji__ast = 'def f(in_seq):\n'
    cbtji__ast += '    n_strs = len(in_seq)\n'
    cbtji__ast += '    A = pre_alloc_string_array(n_strs, -1)\n'
    cbtji__ast += '    return A\n'
    ocbjr__ijpzx = {}
    exec(cbtji__ast, {'pre_alloc_string_array': pre_alloc_string_array},
        ocbjr__ijpzx)
    zzq__yity = ocbjr__ijpzx['f']
    return zzq__yity


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        dwv__bbn = 'pre_alloc_binary_array'
    else:
        dwv__bbn = 'pre_alloc_string_array'
    cbtji__ast = 'def f(in_seq):\n'
    cbtji__ast += '    n_strs = len(in_seq)\n'
    cbtji__ast += f'    A = {dwv__bbn}(n_strs, -1)\n'
    cbtji__ast += '    for i in range(n_strs):\n'
    cbtji__ast += '        A[i] = in_seq[i]\n'
    cbtji__ast += '    return A\n'
    ocbjr__ijpzx = {}
    exec(cbtji__ast, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, ocbjr__ijpzx)
    zzq__yity = ocbjr__ijpzx['f']
    return zzq__yity


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        qkcqv__evnc = builder.add(lhy__erv.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        cxcr__omonr = builder.lshr(lir.Constant(lir.IntType(64),
            offset_type.bitwidth), lir.Constant(lir.IntType(64), 3))
        zwg__pgmk = builder.mul(qkcqv__evnc, cxcr__omonr)
        rmjao__uadjw = context.make_array(offset_arr_type)(context, builder,
            lhy__erv.offsets).data
        cgutils.memset(builder, rmjao__uadjw, zwg__pgmk, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        ymmpj__mxrq = lhy__erv.n_arrays
        zwg__pgmk = builder.lshr(builder.add(ymmpj__mxrq, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        wnz__fovpi = context.make_array(null_bitmap_arr_type)(context,
            builder, lhy__erv.null_bitmap).data
        cgutils.memset(builder, wnz__fovpi, zwg__pgmk, 0)
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
    hlw__myq = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        hcgrm__ohgfh = len(len_arr)
        for i in range(hcgrm__ohgfh):
            offsets[i] = hlw__myq
            hlw__myq += len_arr[i]
        offsets[hcgrm__ohgfh] = hlw__myq
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    idjjp__owsb = i // 8
    tee__hlo = getitem_str_bitmap(bits, idjjp__owsb)
    tee__hlo ^= np.uint8(-np.uint8(bit_is_set) ^ tee__hlo) & kBitmask[i % 8]
    setitem_str_bitmap(bits, idjjp__owsb, tee__hlo)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    enmla__gqv = get_null_bitmap_ptr(out_str_arr)
    juym__oxc = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        lsbi__giva = get_bit_bitmap(juym__oxc, j)
        set_bit_to(enmla__gqv, out_start + j, lsbi__giva)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, ehn__ztcf, slop__mmsif, sbs__yos = args
        okzh__cdg = _get_str_binary_arr_payload(context, builder, ehn__ztcf,
            string_array_type)
        gfv__bgcix = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        pihou__lnsyp = context.make_helper(builder, offset_arr_type,
            okzh__cdg.offsets).data
        fqyuf__deced = context.make_helper(builder, offset_arr_type,
            gfv__bgcix.offsets).data
        mrxv__zoxd = context.make_helper(builder, char_arr_type, okzh__cdg.data
            ).data
        pczcx__inb = context.make_helper(builder, char_arr_type, gfv__bgcix
            .data).data
        num_total_chars = _get_num_total_chars(builder, pihou__lnsyp,
            okzh__cdg.n_arrays)
        ngei__qaz = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        ffbix__baohp = cgutils.get_or_insert_function(builder.module,
            ngei__qaz, name='set_string_array_range')
        builder.call(ffbix__baohp, [fqyuf__deced, pczcx__inb, pihou__lnsyp,
            mrxv__zoxd, slop__mmsif, sbs__yos, okzh__cdg.n_arrays,
            num_total_chars])
        zlbgd__pahla = context.typing_context.resolve_value_type(
            copy_nulls_range)
        bot__eve = zlbgd__pahla.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        vjt__eirv = context.get_function(zlbgd__pahla, bot__eve)
        vjt__eirv(builder, (out_arr, ehn__ztcf, slop__mmsif))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    sdig__cckv = c.context.make_helper(c.builder, typ, val)
    wuzpr__ovfvi = ArrayItemArrayType(char_arr_type)
    lhy__erv = _get_array_item_arr_payload(c.context, c.builder,
        wuzpr__ovfvi, sdig__cckv.data)
    vif__vehc = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    pbduy__dipr = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        pbduy__dipr = 'pd_array_from_string_array'
    ngei__qaz = lir.FunctionType(c.context.get_argument_type(types.pyobject
        ), [lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
        lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
        IntType(32)])
    sylng__pje = cgutils.get_or_insert_function(c.builder.module, ngei__qaz,
        name=pbduy__dipr)
    ilbti__bacxr = c.context.make_array(offset_arr_type)(c.context, c.
        builder, lhy__erv.offsets).data
    ugut__egjp = c.context.make_array(char_arr_type)(c.context, c.builder,
        lhy__erv.data).data
    wnz__fovpi = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, lhy__erv.null_bitmap).data
    arr = c.builder.call(sylng__pje, [lhy__erv.n_arrays, ilbti__bacxr,
        ugut__egjp, wnz__fovpi, vif__vehc])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        wnz__fovpi = context.make_array(null_bitmap_arr_type)(context,
            builder, lhy__erv.null_bitmap).data
        celn__dsnpk = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        ldjt__kfabs = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        tee__hlo = builder.load(builder.gep(wnz__fovpi, [celn__dsnpk],
            inbounds=True))
        sfqe__ogl = lir.ArrayType(lir.IntType(8), 8)
        lyvu__brv = cgutils.alloca_once_value(builder, lir.Constant(
            sfqe__ogl, (1, 2, 4, 8, 16, 32, 64, 128)))
        btg__krv = builder.load(builder.gep(lyvu__brv, [lir.Constant(lir.
            IntType(64), 0), ldjt__kfabs], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(tee__hlo, btg__krv),
            lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        celn__dsnpk = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        ldjt__kfabs = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        wnz__fovpi = context.make_array(null_bitmap_arr_type)(context,
            builder, lhy__erv.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, lhy__erv.
            offsets).data
        aed__nlyy = builder.gep(wnz__fovpi, [celn__dsnpk], inbounds=True)
        tee__hlo = builder.load(aed__nlyy)
        sfqe__ogl = lir.ArrayType(lir.IntType(8), 8)
        lyvu__brv = cgutils.alloca_once_value(builder, lir.Constant(
            sfqe__ogl, (1, 2, 4, 8, 16, 32, 64, 128)))
        btg__krv = builder.load(builder.gep(lyvu__brv, [lir.Constant(lir.
            IntType(64), 0), ldjt__kfabs], inbounds=True))
        btg__krv = builder.xor(btg__krv, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(tee__hlo, btg__krv), aed__nlyy)
        if str_arr_typ == string_array_type:
            cowam__btua = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            zbr__wfd = builder.icmp_unsigned('!=', cowam__btua, lhy__erv.
                n_arrays)
            with builder.if_then(zbr__wfd):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [cowam__btua]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        celn__dsnpk = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        ldjt__kfabs = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        wnz__fovpi = context.make_array(null_bitmap_arr_type)(context,
            builder, lhy__erv.null_bitmap).data
        aed__nlyy = builder.gep(wnz__fovpi, [celn__dsnpk], inbounds=True)
        tee__hlo = builder.load(aed__nlyy)
        sfqe__ogl = lir.ArrayType(lir.IntType(8), 8)
        lyvu__brv = cgutils.alloca_once_value(builder, lir.Constant(
            sfqe__ogl, (1, 2, 4, 8, 16, 32, 64, 128)))
        btg__krv = builder.load(builder.gep(lyvu__brv, [lir.Constant(lir.
            IntType(64), 0), ldjt__kfabs], inbounds=True))
        builder.store(builder.or_(tee__hlo, btg__krv), aed__nlyy)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        zwg__pgmk = builder.udiv(builder.add(lhy__erv.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        wnz__fovpi = context.make_array(null_bitmap_arr_type)(context,
            builder, lhy__erv.null_bitmap).data
        cgutils.memset(builder, wnz__fovpi, zwg__pgmk, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    iym__ntrl = context.make_helper(builder, string_array_type, str_arr)
    wuzpr__ovfvi = ArrayItemArrayType(char_arr_type)
    bhzdm__tjvdv = context.make_helper(builder, wuzpr__ovfvi, iym__ntrl.data)
    sbc__hhygj = ArrayItemArrayPayloadType(wuzpr__ovfvi)
    wlows__bmixq = context.nrt.meminfo_data(builder, bhzdm__tjvdv.meminfo)
    chrzz__auii = builder.bitcast(wlows__bmixq, context.get_value_type(
        sbc__hhygj).as_pointer())
    return chrzz__auii


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        wkook__tseuj, ruwt__njdu = args
        nujk__uut = _get_str_binary_arr_data_payload_ptr(context, builder,
            ruwt__njdu)
        fzjgb__awhit = _get_str_binary_arr_data_payload_ptr(context,
            builder, wkook__tseuj)
        kuhg__yqm = _get_str_binary_arr_payload(context, builder,
            ruwt__njdu, sig.args[1])
        fol__yizc = _get_str_binary_arr_payload(context, builder,
            wkook__tseuj, sig.args[0])
        context.nrt.incref(builder, char_arr_type, kuhg__yqm.data)
        context.nrt.incref(builder, offset_arr_type, kuhg__yqm.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, kuhg__yqm.null_bitmap
            )
        context.nrt.decref(builder, char_arr_type, fol__yizc.data)
        context.nrt.decref(builder, offset_arr_type, fol__yizc.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, fol__yizc.null_bitmap
            )
        builder.store(builder.load(nujk__uut), fzjgb__awhit)
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
        kwmjz__xrpk = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return kwmjz__xrpk
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, kjtcn__igbkx, jlpzi__ozrv = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, arr, sig.
            args[0])
        offsets = context.make_helper(builder, offset_arr_type, lhy__erv.
            offsets).data
        data = context.make_helper(builder, char_arr_type, lhy__erv.data).data
        ngei__qaz = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        vhnj__ufpu = cgutils.get_or_insert_function(builder.module,
            ngei__qaz, name='setitem_string_array')
        cnrqz__zhqzs = context.get_constant(types.int32, -1)
        gcwh__grg = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, lhy__erv.
            n_arrays)
        builder.call(vhnj__ufpu, [offsets, data, num_total_chars, builder.
            extract_value(kjtcn__igbkx, 0), jlpzi__ozrv, cnrqz__zhqzs,
            gcwh__grg, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    ngei__qaz = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64)])
    tju__xqvt = cgutils.get_or_insert_function(builder.module, ngei__qaz,
        name='is_na')
    return builder.call(tju__xqvt, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        oezm__axq, ramq__tfwul, ayvde__vbsx, erj__lre = args
        cgutils.raw_memcpy(builder, oezm__axq, ramq__tfwul, ayvde__vbsx,
            erj__lre)
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
        ztps__aka, qui__lrs = unicode_to_utf8_and_len(val)
        xtvo__aali = getitem_str_offset(A, ind)
        sip__fok = getitem_str_offset(A, ind + 1)
        gevhn__mcs = sip__fok - xtvo__aali
        if gevhn__mcs != qui__lrs:
            return False
        kjtcn__igbkx = get_data_ptr_ind(A, xtvo__aali)
        return memcmp(kjtcn__igbkx, ztps__aka, qui__lrs) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        xtvo__aali = getitem_str_offset(A, ind)
        gevhn__mcs = bodo.libs.str_ext.int_to_str_len(val)
        fvc__aron = xtvo__aali + gevhn__mcs
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            xtvo__aali, fvc__aron)
        kjtcn__igbkx = get_data_ptr_ind(A, xtvo__aali)
        inplace_int64_to_str(kjtcn__igbkx, gevhn__mcs, val)
        setitem_str_offset(A, ind + 1, xtvo__aali + gevhn__mcs)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        kjtcn__igbkx, = args
        ibuw__umb = context.insert_const_string(builder.module, '<NA>')
        wnf__msim = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, kjtcn__igbkx, ibuw__umb, wnf__msim, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    ngerh__kqzpp = len('<NA>')

    def impl(A, ind):
        xtvo__aali = getitem_str_offset(A, ind)
        fvc__aron = xtvo__aali + ngerh__kqzpp
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            xtvo__aali, fvc__aron)
        kjtcn__igbkx = get_data_ptr_ind(A, xtvo__aali)
        inplace_set_NA_str(kjtcn__igbkx)
        setitem_str_offset(A, ind + 1, xtvo__aali + ngerh__kqzpp)
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
            xtvo__aali = getitem_str_offset(A, ind)
            sip__fok = getitem_str_offset(A, ind + 1)
            jlpzi__ozrv = sip__fok - xtvo__aali
            kjtcn__igbkx = get_data_ptr_ind(A, xtvo__aali)
            mrvbe__uxc = decode_utf8(kjtcn__igbkx, jlpzi__ozrv)
            return mrvbe__uxc
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            kwmjz__xrpk = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(kwmjz__xrpk):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            vkw__cwd = get_data_ptr(out_arr).data
            mlq__auzil = get_data_ptr(A).data
            wyyz__wdy = 0
            ydr__hgtku = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(kwmjz__xrpk):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    aebd__yyf = get_str_arr_item_length(A, i)
                    if aebd__yyf == 1:
                        copy_single_char(vkw__cwd, ydr__hgtku, mlq__auzil,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(vkw__cwd, ydr__hgtku, mlq__auzil,
                            getitem_str_offset(A, i), aebd__yyf, 1)
                    ydr__hgtku += aebd__yyf
                    setitem_str_offset(out_arr, wyyz__wdy + 1, ydr__hgtku)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, wyyz__wdy)
                    else:
                        str_arr_set_not_na(out_arr, wyyz__wdy)
                    wyyz__wdy += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            kwmjz__xrpk = len(ind)
            out_arr = pre_alloc_string_array(kwmjz__xrpk, -1)
            wyyz__wdy = 0
            for i in range(kwmjz__xrpk):
                sucpk__nsq = A[ind[i]]
                out_arr[wyyz__wdy] = sucpk__nsq
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, wyyz__wdy)
                wyyz__wdy += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            kwmjz__xrpk = len(A)
            upqmk__nwopv = numba.cpython.unicode._normalize_slice(ind,
                kwmjz__xrpk)
            gaha__ujixe = numba.cpython.unicode._slice_span(upqmk__nwopv)
            if upqmk__nwopv.step == 1:
                xtvo__aali = getitem_str_offset(A, upqmk__nwopv.start)
                sip__fok = getitem_str_offset(A, upqmk__nwopv.stop)
                n_chars = sip__fok - xtvo__aali
                znbnd__inxz = pre_alloc_string_array(gaha__ujixe, np.int64(
                    n_chars))
                for i in range(gaha__ujixe):
                    znbnd__inxz[i] = A[upqmk__nwopv.start + i]
                    if str_arr_is_na(A, upqmk__nwopv.start + i):
                        str_arr_set_na(znbnd__inxz, i)
                return znbnd__inxz
            else:
                znbnd__inxz = pre_alloc_string_array(gaha__ujixe, -1)
                for i in range(gaha__ujixe):
                    znbnd__inxz[i] = A[upqmk__nwopv.start + i *
                        upqmk__nwopv.step]
                    if str_arr_is_na(A, upqmk__nwopv.start + i *
                        upqmk__nwopv.step):
                        str_arr_set_na(znbnd__inxz, i)
                return znbnd__inxz
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
    ynza__cylv = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(ynza__cylv)
        hoo__bbl = 4

        def impl_scalar(A, idx, val):
            ssu__ajggx = (val._length if val._is_ascii else hoo__bbl * val.
                _length)
            epmv__jcpnn = A._data
            xtvo__aali = np.int64(getitem_str_offset(A, idx))
            fvc__aron = xtvo__aali + ssu__ajggx
            bodo.libs.array_item_arr_ext.ensure_data_capacity(epmv__jcpnn,
                xtvo__aali, fvc__aron)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                fvc__aron, val._data, val._length, val._kind, val._is_ascii,
                idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                upqmk__nwopv = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                gdey__nzhh = upqmk__nwopv.start
                epmv__jcpnn = A._data
                xtvo__aali = np.int64(getitem_str_offset(A, gdey__nzhh))
                fvc__aron = xtvo__aali + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(epmv__jcpnn,
                    xtvo__aali, fvc__aron)
                set_string_array_range(A, val, gdey__nzhh, xtvo__aali)
                zvsm__zmxvo = 0
                for i in range(upqmk__nwopv.start, upqmk__nwopv.stop,
                    upqmk__nwopv.step):
                    if str_arr_is_na(val, zvsm__zmxvo):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    zvsm__zmxvo += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                cks__gnrw = str_list_to_array(val)
                A[idx] = cks__gnrw
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                upqmk__nwopv = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(upqmk__nwopv.start, upqmk__nwopv.stop,
                    upqmk__nwopv.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(ynza__cylv)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                kwmjz__xrpk = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(kwmjz__xrpk, -1)
                for i in numba.parfors.parfor.internal_prange(kwmjz__xrpk):
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
                kwmjz__xrpk = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(kwmjz__xrpk, -1)
                ufm__vsa = 0
                for i in numba.parfors.parfor.internal_prange(kwmjz__xrpk):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, ufm__vsa):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, ufm__vsa)
                        else:
                            out_arr[i] = str(val[ufm__vsa])
                        ufm__vsa += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(ynza__cylv)
    raise BodoError(ynza__cylv)


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
    zjfp__gex = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(zjfp__gex, (types.Float, types.Integer)
        ) and zjfp__gex not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(zjfp__gex, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            kwmjz__xrpk = len(A)
            B = np.empty(kwmjz__xrpk, zjfp__gex)
            for i in numba.parfors.parfor.internal_prange(kwmjz__xrpk):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif zjfp__gex == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            kwmjz__xrpk = len(A)
            B = np.empty(kwmjz__xrpk, zjfp__gex)
            for i in numba.parfors.parfor.internal_prange(kwmjz__xrpk):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif zjfp__gex == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            kwmjz__xrpk = len(A)
            B = np.empty(kwmjz__xrpk, zjfp__gex)
            for i in numba.parfors.parfor.internal_prange(kwmjz__xrpk):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            kwmjz__xrpk = len(A)
            B = np.empty(kwmjz__xrpk, zjfp__gex)
            for i in numba.parfors.parfor.internal_prange(kwmjz__xrpk):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        kjtcn__igbkx, jlpzi__ozrv = args
        nfyy__boz = context.get_python_api(builder)
        aqe__kucvk = nfyy__boz.string_from_string_and_size(kjtcn__igbkx,
            jlpzi__ozrv)
        scvk__qdclv = nfyy__boz.to_native_value(string_type, aqe__kucvk).value
        dsjfq__elxuy = cgutils.create_struct_proxy(string_type)(context,
            builder, scvk__qdclv)
        dsjfq__elxuy.hash = dsjfq__elxuy.hash.type(-1)
        nfyy__boz.decref(aqe__kucvk)
        return dsjfq__elxuy._getvalue()
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
        mgxf__ciwfs, arr, ind, pcumc__dxr = args
        lhy__erv = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, lhy__erv.
            offsets).data
        data = context.make_helper(builder, char_arr_type, lhy__erv.data).data
        ngei__qaz = lir.FunctionType(lir.IntType(32), [mgxf__ciwfs.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        wtvg__asrts = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            wtvg__asrts = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        dyu__rzzm = cgutils.get_or_insert_function(builder.module,
            ngei__qaz, wtvg__asrts)
        return builder.call(dyu__rzzm, [mgxf__ciwfs, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    vif__vehc = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    ngei__qaz = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(32)])
    hjtiv__cpbx = cgutils.get_or_insert_function(c.builder.module,
        ngei__qaz, name='string_array_from_sequence')
    buv__dix = c.builder.call(hjtiv__cpbx, [val, vif__vehc])
    wuzpr__ovfvi = ArrayItemArrayType(char_arr_type)
    bhzdm__tjvdv = c.context.make_helper(c.builder, wuzpr__ovfvi)
    bhzdm__tjvdv.meminfo = buv__dix
    iym__ntrl = c.context.make_helper(c.builder, typ)
    epmv__jcpnn = bhzdm__tjvdv._getvalue()
    iym__ntrl.data = epmv__jcpnn
    osa__iuct = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(iym__ntrl._getvalue(), is_error=osa__iuct)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    kwmjz__xrpk = len(pyval)
    ydr__hgtku = 0
    jnsrj__imoqc = np.empty(kwmjz__xrpk + 1, np_offset_type)
    wavkq__ifqf = []
    qvyz__mxi = np.empty(kwmjz__xrpk + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        jnsrj__imoqc[i] = ydr__hgtku
        ccwv__hed = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(qvyz__mxi, i, int(not ccwv__hed))
        if ccwv__hed:
            continue
        xbk__rmkwg = list(s.encode()) if isinstance(s, str) else list(s)
        wavkq__ifqf.extend(xbk__rmkwg)
        ydr__hgtku += len(xbk__rmkwg)
    jnsrj__imoqc[kwmjz__xrpk] = ydr__hgtku
    woz__tgqjh = np.array(wavkq__ifqf, np.uint8)
    jal__sxk = context.get_constant(types.int64, kwmjz__xrpk)
    vsdi__mzmng = context.get_constant_generic(builder, char_arr_type,
        woz__tgqjh)
    qbpjd__ekey = context.get_constant_generic(builder, offset_arr_type,
        jnsrj__imoqc)
    wodrp__ryu = context.get_constant_generic(builder, null_bitmap_arr_type,
        qvyz__mxi)
    lhy__erv = lir.Constant.literal_struct([jal__sxk, vsdi__mzmng,
        qbpjd__ekey, wodrp__ryu])
    lhy__erv = cgutils.global_constant(builder, '.const.payload', lhy__erv
        ).bitcast(cgutils.voidptr_t)
    lii__kxoi = context.get_constant(types.int64, -1)
    muzr__uyoxg = context.get_constant_null(types.voidptr)
    pemy__nfqfw = lir.Constant.literal_struct([lii__kxoi, muzr__uyoxg,
        muzr__uyoxg, lhy__erv, lii__kxoi])
    pemy__nfqfw = cgutils.global_constant(builder, '.const.meminfo',
        pemy__nfqfw).bitcast(cgutils.voidptr_t)
    epmv__jcpnn = lir.Constant.literal_struct([pemy__nfqfw])
    iym__ntrl = lir.Constant.literal_struct([epmv__jcpnn])
    return iym__ntrl


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
