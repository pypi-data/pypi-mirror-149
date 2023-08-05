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
        bxa__mgerh = ArrayItemArrayType(char_arr_type)
        kikue__jdg = [('data', bxa__mgerh)]
        models.StructModel.__init__(self, dmm, fe_type, kikue__jdg)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        ykab__akg, = args
        vmhl__eoec = context.make_helper(builder, string_array_type)
        vmhl__eoec.data = ykab__akg
        context.nrt.incref(builder, data_typ, ykab__akg)
        return vmhl__eoec._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    njoh__dhp = c.context.insert_const_string(c.builder.module, 'pandas')
    lhxjk__pjk = c.pyapi.import_module_noblock(njoh__dhp)
    eupt__zpwrg = c.pyapi.call_method(lhxjk__pjk, 'StringDtype', ())
    c.pyapi.decref(lhxjk__pjk)
    return eupt__zpwrg


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        ynk__zxf = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs)
        if ynk__zxf is not None:
            return ynk__zxf
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                yjgki__wuu = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(yjgki__wuu)
                for i in numba.parfors.parfor.internal_prange(yjgki__wuu):
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
                yjgki__wuu = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(yjgki__wuu)
                for i in numba.parfors.parfor.internal_prange(yjgki__wuu):
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
                yjgki__wuu = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(yjgki__wuu)
                for i in numba.parfors.parfor.internal_prange(yjgki__wuu):
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
    wubfr__sncnf = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    ynkws__awdqy = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs
        ) and ynkws__awdqy or wubfr__sncnf and is_str_arr_type(rhs):

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
    wvwj__lxb = context.make_helper(builder, arr_typ, arr_value)
    bxa__mgerh = ArrayItemArrayType(char_arr_type)
    tnl__osi = _get_array_item_arr_payload(context, builder, bxa__mgerh,
        wvwj__lxb.data)
    return tnl__osi


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        return tnl__osi.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        dgbag__bhqf = context.make_helper(builder, offset_arr_type,
            tnl__osi.offsets).data
        return _get_num_total_chars(builder, dgbag__bhqf, tnl__osi.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        zdlj__shuee = context.make_helper(builder, offset_arr_type,
            tnl__osi.offsets)
        tnoeh__omb = context.make_helper(builder, offset_ctypes_type)
        tnoeh__omb.data = builder.bitcast(zdlj__shuee.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        tnoeh__omb.meminfo = zdlj__shuee.meminfo
        eupt__zpwrg = tnoeh__omb._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            eupt__zpwrg)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        ykab__akg = context.make_helper(builder, char_arr_type, tnl__osi.data)
        tnoeh__omb = context.make_helper(builder, data_ctypes_type)
        tnoeh__omb.data = ykab__akg.data
        tnoeh__omb.meminfo = ykab__akg.meminfo
        eupt__zpwrg = tnoeh__omb._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            eupt__zpwrg)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        rikrf__ccw, ind = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, rikrf__ccw,
            sig.args[0])
        ykab__akg = context.make_helper(builder, char_arr_type, tnl__osi.data)
        tnoeh__omb = context.make_helper(builder, data_ctypes_type)
        tnoeh__omb.data = builder.gep(ykab__akg.data, [ind])
        tnoeh__omb.meminfo = ykab__akg.meminfo
        eupt__zpwrg = tnoeh__omb._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            eupt__zpwrg)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        vij__sts, pqghl__itp, pdrb__cqzw, hxz__swblf = args
        eiyx__madi = builder.bitcast(builder.gep(vij__sts, [pqghl__itp]),
            lir.IntType(8).as_pointer())
        odxfk__yscre = builder.bitcast(builder.gep(pdrb__cqzw, [hxz__swblf]
            ), lir.IntType(8).as_pointer())
        hbm__wpjt = builder.load(odxfk__yscre)
        builder.store(hbm__wpjt, eiyx__madi)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        omrn__gdyj = context.make_helper(builder, null_bitmap_arr_type,
            tnl__osi.null_bitmap)
        tnoeh__omb = context.make_helper(builder, data_ctypes_type)
        tnoeh__omb.data = omrn__gdyj.data
        tnoeh__omb.meminfo = omrn__gdyj.meminfo
        eupt__zpwrg = tnoeh__omb._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            eupt__zpwrg)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        dgbag__bhqf = context.make_helper(builder, offset_arr_type,
            tnl__osi.offsets).data
        return builder.load(builder.gep(dgbag__bhqf, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, tnl__osi.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        xyqwh__icxin, ind = args
        if in_bitmap_typ == data_ctypes_type:
            tnoeh__omb = context.make_helper(builder, data_ctypes_type,
                xyqwh__icxin)
            xyqwh__icxin = tnoeh__omb.data
        return builder.load(builder.gep(xyqwh__icxin, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        xyqwh__icxin, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            tnoeh__omb = context.make_helper(builder, data_ctypes_type,
                xyqwh__icxin)
            xyqwh__icxin = tnoeh__omb.data
        builder.store(val, builder.gep(xyqwh__icxin, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        moakd__guin = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        dteu__murmy = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        hhzbj__xgi = context.make_helper(builder, offset_arr_type,
            moakd__guin.offsets).data
        rgcbi__hpvrd = context.make_helper(builder, offset_arr_type,
            dteu__murmy.offsets).data
        hhtjg__uhvf = context.make_helper(builder, char_arr_type,
            moakd__guin.data).data
        refv__igg = context.make_helper(builder, char_arr_type, dteu__murmy
            .data).data
        cxpkj__wbfid = context.make_helper(builder, null_bitmap_arr_type,
            moakd__guin.null_bitmap).data
        yfvx__mazf = context.make_helper(builder, null_bitmap_arr_type,
            dteu__murmy.null_bitmap).data
        tbuwj__rgsd = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, rgcbi__hpvrd, hhzbj__xgi, tbuwj__rgsd)
        cgutils.memcpy(builder, refv__igg, hhtjg__uhvf, builder.load(
            builder.gep(hhzbj__xgi, [ind])))
        lvq__wblg = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        rjw__bloor = builder.lshr(lvq__wblg, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, yfvx__mazf, cxpkj__wbfid, rjw__bloor)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        moakd__guin = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        dteu__murmy = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        hhzbj__xgi = context.make_helper(builder, offset_arr_type,
            moakd__guin.offsets).data
        hhtjg__uhvf = context.make_helper(builder, char_arr_type,
            moakd__guin.data).data
        refv__igg = context.make_helper(builder, char_arr_type, dteu__murmy
            .data).data
        num_total_chars = _get_num_total_chars(builder, hhzbj__xgi,
            moakd__guin.n_arrays)
        cgutils.memcpy(builder, refv__igg, hhtjg__uhvf, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        moakd__guin = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        dteu__murmy = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        hhzbj__xgi = context.make_helper(builder, offset_arr_type,
            moakd__guin.offsets).data
        rgcbi__hpvrd = context.make_helper(builder, offset_arr_type,
            dteu__murmy.offsets).data
        cxpkj__wbfid = context.make_helper(builder, null_bitmap_arr_type,
            moakd__guin.null_bitmap).data
        yjgki__wuu = moakd__guin.n_arrays
        rslo__rvgz = context.get_constant(offset_type, 0)
        cvz__ghh = cgutils.alloca_once_value(builder, rslo__rvgz)
        with cgutils.for_range(builder, yjgki__wuu) as czoof__wnp:
            jnrct__sds = lower_is_na(context, builder, cxpkj__wbfid,
                czoof__wnp.index)
            with cgutils.if_likely(builder, builder.not_(jnrct__sds)):
                bkb__hspl = builder.load(builder.gep(hhzbj__xgi, [
                    czoof__wnp.index]))
                dhw__ghs = builder.load(cvz__ghh)
                builder.store(bkb__hspl, builder.gep(rgcbi__hpvrd, [dhw__ghs]))
                builder.store(builder.add(dhw__ghs, lir.Constant(context.
                    get_value_type(offset_type), 1)), cvz__ghh)
        dhw__ghs = builder.load(cvz__ghh)
        bkb__hspl = builder.load(builder.gep(hhzbj__xgi, [yjgki__wuu]))
        builder.store(bkb__hspl, builder.gep(rgcbi__hpvrd, [dhw__ghs]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        jjjsv__uxoky, ind, str, dnu__hfcr = args
        jjjsv__uxoky = context.make_array(sig.args[0])(context, builder,
            jjjsv__uxoky)
        ixsfb__jhf = builder.gep(jjjsv__uxoky.data, [ind])
        cgutils.raw_memcpy(builder, ixsfb__jhf, str, dnu__hfcr, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        ixsfb__jhf, ind, xncc__tpuuq, dnu__hfcr = args
        ixsfb__jhf = builder.gep(ixsfb__jhf, [ind])
        cgutils.raw_memcpy(builder, ixsfb__jhf, xncc__tpuuq, dnu__hfcr, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    vbk__fov = np.int64(getitem_str_offset(A, i))
    ndi__dve = np.int64(getitem_str_offset(A, i + 1))
    l = ndi__dve - vbk__fov
    cfcyg__cziiw = get_data_ptr_ind(A, vbk__fov)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(cfcyg__cziiw, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    onzg__rednd = getitem_str_offset(A, i)
    uirl__lxick = getitem_str_offset(A, i + 1)
    aagi__kehg = uirl__lxick - onzg__rednd
    puu__rzex = getitem_str_offset(B, j)
    hwxf__ucl = puu__rzex + aagi__kehg
    setitem_str_offset(B, j + 1, hwxf__ucl)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if aagi__kehg != 0:
        ykab__akg = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(ykab__akg, np.
            int64(puu__rzex), np.int64(hwxf__ucl))
        rvznf__hnhqf = get_data_ptr(B).data
        fmt__jiycn = get_data_ptr(A).data
        memcpy_region(rvznf__hnhqf, puu__rzex, fmt__jiycn, onzg__rednd,
            aagi__kehg, 1)


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    yjgki__wuu = len(str_arr)
    ait__jvj = np.empty(yjgki__wuu, np.bool_)
    for i in range(yjgki__wuu):
        ait__jvj[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return ait__jvj


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            yjgki__wuu = len(data)
            l = []
            for i in range(yjgki__wuu):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        arpjv__fpot = data.count
        jec__urlx = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(arpjv__fpot)]
        if is_overload_true(str_null_bools):
            jec__urlx += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(arpjv__fpot) if is_str_arr_type(data.types[i]) or 
                data.types[i] == binary_array_type]
        cva__mzrw = 'def f(data, str_null_bools=None):\n'
        cva__mzrw += '  return ({}{})\n'.format(', '.join(jec__urlx), ',' if
            arpjv__fpot == 1 else '')
        wuwft__dhtgv = {}
        exec(cva__mzrw, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, wuwft__dhtgv)
        qgsew__ihd = wuwft__dhtgv['f']
        return qgsew__ihd
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                yjgki__wuu = len(list_data)
                for i in range(yjgki__wuu):
                    xncc__tpuuq = list_data[i]
                    str_arr[i] = xncc__tpuuq
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                yjgki__wuu = len(list_data)
                for i in range(yjgki__wuu):
                    xncc__tpuuq = list_data[i]
                    str_arr[i] = xncc__tpuuq
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        arpjv__fpot = str_arr.count
        mmtw__onmg = 0
        cva__mzrw = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(arpjv__fpot):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                cva__mzrw += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, arpjv__fpot + mmtw__onmg))
                mmtw__onmg += 1
            else:
                cva__mzrw += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        cva__mzrw += '  return\n'
        wuwft__dhtgv = {}
        exec(cva__mzrw, {'cp_str_list_to_array': cp_str_list_to_array},
            wuwft__dhtgv)
        dqk__gowfi = wuwft__dhtgv['f']
        return dqk__gowfi
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            yjgki__wuu = len(str_list)
            str_arr = pre_alloc_string_array(yjgki__wuu, -1)
            for i in range(yjgki__wuu):
                xncc__tpuuq = str_list[i]
                str_arr[i] = xncc__tpuuq
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            yjgki__wuu = len(A)
            uskkt__dld = 0
            for i in range(yjgki__wuu):
                xncc__tpuuq = A[i]
                uskkt__dld += get_utf8_size(xncc__tpuuq)
            return uskkt__dld
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        yjgki__wuu = len(arr)
        n_chars = num_total_chars(arr)
        mkxl__faqid = pre_alloc_string_array(yjgki__wuu, np.int64(n_chars))
        copy_str_arr_slice(mkxl__faqid, arr, yjgki__wuu)
        return mkxl__faqid
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
    cva__mzrw = 'def f(in_seq):\n'
    cva__mzrw += '    n_strs = len(in_seq)\n'
    cva__mzrw += '    A = pre_alloc_string_array(n_strs, -1)\n'
    cva__mzrw += '    return A\n'
    wuwft__dhtgv = {}
    exec(cva__mzrw, {'pre_alloc_string_array': pre_alloc_string_array},
        wuwft__dhtgv)
    xfuxv__hpfmp = wuwft__dhtgv['f']
    return xfuxv__hpfmp


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        dotv__nhoj = 'pre_alloc_binary_array'
    else:
        dotv__nhoj = 'pre_alloc_string_array'
    cva__mzrw = 'def f(in_seq):\n'
    cva__mzrw += '    n_strs = len(in_seq)\n'
    cva__mzrw += f'    A = {dotv__nhoj}(n_strs, -1)\n'
    cva__mzrw += '    for i in range(n_strs):\n'
    cva__mzrw += '        A[i] = in_seq[i]\n'
    cva__mzrw += '    return A\n'
    wuwft__dhtgv = {}
    exec(cva__mzrw, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, wuwft__dhtgv)
    xfuxv__hpfmp = wuwft__dhtgv['f']
    return xfuxv__hpfmp


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        fmbz__ysled = builder.add(tnl__osi.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        kyxlm__kxvq = builder.lshr(lir.Constant(lir.IntType(64),
            offset_type.bitwidth), lir.Constant(lir.IntType(64), 3))
        rjw__bloor = builder.mul(fmbz__ysled, kyxlm__kxvq)
        tdnt__shngr = context.make_array(offset_arr_type)(context, builder,
            tnl__osi.offsets).data
        cgutils.memset(builder, tdnt__shngr, rjw__bloor, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        tlxn__nlsdn = tnl__osi.n_arrays
        rjw__bloor = builder.lshr(builder.add(tlxn__nlsdn, lir.Constant(lir
            .IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        urkls__almyx = context.make_array(null_bitmap_arr_type)(context,
            builder, tnl__osi.null_bitmap).data
        cgutils.memset(builder, urkls__almyx, rjw__bloor, 0)
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
    fyxb__rnug = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        oolzx__iaw = len(len_arr)
        for i in range(oolzx__iaw):
            offsets[i] = fyxb__rnug
            fyxb__rnug += len_arr[i]
        offsets[oolzx__iaw] = fyxb__rnug
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    msrz__vkekz = i // 8
    qqf__yad = getitem_str_bitmap(bits, msrz__vkekz)
    qqf__yad ^= np.uint8(-np.uint8(bit_is_set) ^ qqf__yad) & kBitmask[i % 8]
    setitem_str_bitmap(bits, msrz__vkekz, qqf__yad)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    nwxq__xbrp = get_null_bitmap_ptr(out_str_arr)
    vdgb__dnpgu = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        ufijc__aociw = get_bit_bitmap(vdgb__dnpgu, j)
        set_bit_to(nwxq__xbrp, out_start + j, ufijc__aociw)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, rikrf__ccw, wcpo__ieqmi, ohxij__vouje = args
        moakd__guin = _get_str_binary_arr_payload(context, builder,
            rikrf__ccw, string_array_type)
        dteu__murmy = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        hhzbj__xgi = context.make_helper(builder, offset_arr_type,
            moakd__guin.offsets).data
        rgcbi__hpvrd = context.make_helper(builder, offset_arr_type,
            dteu__murmy.offsets).data
        hhtjg__uhvf = context.make_helper(builder, char_arr_type,
            moakd__guin.data).data
        refv__igg = context.make_helper(builder, char_arr_type, dteu__murmy
            .data).data
        num_total_chars = _get_num_total_chars(builder, hhzbj__xgi,
            moakd__guin.n_arrays)
        lamkx__nkpdy = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        dkjj__musn = cgutils.get_or_insert_function(builder.module,
            lamkx__nkpdy, name='set_string_array_range')
        builder.call(dkjj__musn, [rgcbi__hpvrd, refv__igg, hhzbj__xgi,
            hhtjg__uhvf, wcpo__ieqmi, ohxij__vouje, moakd__guin.n_arrays,
            num_total_chars])
        xaoej__yuhvi = context.typing_context.resolve_value_type(
            copy_nulls_range)
        rybbp__eec = xaoej__yuhvi.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        vfkqq__bzsg = context.get_function(xaoej__yuhvi, rybbp__eec)
        vfkqq__bzsg(builder, (out_arr, rikrf__ccw, wcpo__ieqmi))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    cfh__vckc = c.context.make_helper(c.builder, typ, val)
    bxa__mgerh = ArrayItemArrayType(char_arr_type)
    tnl__osi = _get_array_item_arr_payload(c.context, c.builder, bxa__mgerh,
        cfh__vckc.data)
    xpl__ijh = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    tcwkf__ang = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        tcwkf__ang = 'pd_array_from_string_array'
    lamkx__nkpdy = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    egy__pcf = cgutils.get_or_insert_function(c.builder.module,
        lamkx__nkpdy, name=tcwkf__ang)
    dgbag__bhqf = c.context.make_array(offset_arr_type)(c.context, c.
        builder, tnl__osi.offsets).data
    cfcyg__cziiw = c.context.make_array(char_arr_type)(c.context, c.builder,
        tnl__osi.data).data
    urkls__almyx = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, tnl__osi.null_bitmap).data
    arr = c.builder.call(egy__pcf, [tnl__osi.n_arrays, dgbag__bhqf,
        cfcyg__cziiw, urkls__almyx, xpl__ijh])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        urkls__almyx = context.make_array(null_bitmap_arr_type)(context,
            builder, tnl__osi.null_bitmap).data
        svqt__inaa = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        zjn__cmyg = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        qqf__yad = builder.load(builder.gep(urkls__almyx, [svqt__inaa],
            inbounds=True))
        vscf__qub = lir.ArrayType(lir.IntType(8), 8)
        pzgr__nhee = cgutils.alloca_once_value(builder, lir.Constant(
            vscf__qub, (1, 2, 4, 8, 16, 32, 64, 128)))
        qkox__zgi = builder.load(builder.gep(pzgr__nhee, [lir.Constant(lir.
            IntType(64), 0), zjn__cmyg], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(qqf__yad, qkox__zgi
            ), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        svqt__inaa = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        zjn__cmyg = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        urkls__almyx = context.make_array(null_bitmap_arr_type)(context,
            builder, tnl__osi.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, tnl__osi.
            offsets).data
        pvbmn__pjd = builder.gep(urkls__almyx, [svqt__inaa], inbounds=True)
        qqf__yad = builder.load(pvbmn__pjd)
        vscf__qub = lir.ArrayType(lir.IntType(8), 8)
        pzgr__nhee = cgutils.alloca_once_value(builder, lir.Constant(
            vscf__qub, (1, 2, 4, 8, 16, 32, 64, 128)))
        qkox__zgi = builder.load(builder.gep(pzgr__nhee, [lir.Constant(lir.
            IntType(64), 0), zjn__cmyg], inbounds=True))
        qkox__zgi = builder.xor(qkox__zgi, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(qqf__yad, qkox__zgi), pvbmn__pjd)
        if str_arr_typ == string_array_type:
            upvy__pjvqs = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            ecnw__vrued = builder.icmp_unsigned('!=', upvy__pjvqs, tnl__osi
                .n_arrays)
            with builder.if_then(ecnw__vrued):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [upvy__pjvqs]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        svqt__inaa = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        zjn__cmyg = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        urkls__almyx = context.make_array(null_bitmap_arr_type)(context,
            builder, tnl__osi.null_bitmap).data
        pvbmn__pjd = builder.gep(urkls__almyx, [svqt__inaa], inbounds=True)
        qqf__yad = builder.load(pvbmn__pjd)
        vscf__qub = lir.ArrayType(lir.IntType(8), 8)
        pzgr__nhee = cgutils.alloca_once_value(builder, lir.Constant(
            vscf__qub, (1, 2, 4, 8, 16, 32, 64, 128)))
        qkox__zgi = builder.load(builder.gep(pzgr__nhee, [lir.Constant(lir.
            IntType(64), 0), zjn__cmyg], inbounds=True))
        builder.store(builder.or_(qqf__yad, qkox__zgi), pvbmn__pjd)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        rjw__bloor = builder.udiv(builder.add(tnl__osi.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        urkls__almyx = context.make_array(null_bitmap_arr_type)(context,
            builder, tnl__osi.null_bitmap).data
        cgutils.memset(builder, urkls__almyx, rjw__bloor, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    mjncj__hvwk = context.make_helper(builder, string_array_type, str_arr)
    bxa__mgerh = ArrayItemArrayType(char_arr_type)
    afdh__vcdq = context.make_helper(builder, bxa__mgerh, mjncj__hvwk.data)
    iruvp__nqua = ArrayItemArrayPayloadType(bxa__mgerh)
    zejab__gdzxj = context.nrt.meminfo_data(builder, afdh__vcdq.meminfo)
    mod__fde = builder.bitcast(zejab__gdzxj, context.get_value_type(
        iruvp__nqua).as_pointer())
    return mod__fde


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        vgpvh__ngfmy, xof__ket = args
        rnvm__bzqxu = _get_str_binary_arr_data_payload_ptr(context, builder,
            xof__ket)
        ywq__pcy = _get_str_binary_arr_data_payload_ptr(context, builder,
            vgpvh__ngfmy)
        kike__ahc = _get_str_binary_arr_payload(context, builder, xof__ket,
            sig.args[1])
        eqfhw__hbc = _get_str_binary_arr_payload(context, builder,
            vgpvh__ngfmy, sig.args[0])
        context.nrt.incref(builder, char_arr_type, kike__ahc.data)
        context.nrt.incref(builder, offset_arr_type, kike__ahc.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, kike__ahc.null_bitmap
            )
        context.nrt.decref(builder, char_arr_type, eqfhw__hbc.data)
        context.nrt.decref(builder, offset_arr_type, eqfhw__hbc.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, eqfhw__hbc.
            null_bitmap)
        builder.store(builder.load(rnvm__bzqxu), ywq__pcy)
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
        yjgki__wuu = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return yjgki__wuu
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, ixsfb__jhf, idhzl__uiyc = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, arr, sig.
            args[0])
        offsets = context.make_helper(builder, offset_arr_type, tnl__osi.
            offsets).data
        data = context.make_helper(builder, char_arr_type, tnl__osi.data).data
        lamkx__nkpdy = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        oxvf__fgbaq = cgutils.get_or_insert_function(builder.module,
            lamkx__nkpdy, name='setitem_string_array')
        nwjl__elbj = context.get_constant(types.int32, -1)
        ndh__ovdbu = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, tnl__osi.
            n_arrays)
        builder.call(oxvf__fgbaq, [offsets, data, num_total_chars, builder.
            extract_value(ixsfb__jhf, 0), idhzl__uiyc, nwjl__elbj,
            ndh__ovdbu, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    lamkx__nkpdy = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    ocbh__wrp = cgutils.get_or_insert_function(builder.module, lamkx__nkpdy,
        name='is_na')
    return builder.call(ocbh__wrp, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        eiyx__madi, odxfk__yscre, arpjv__fpot, lpme__emne = args
        cgutils.raw_memcpy(builder, eiyx__madi, odxfk__yscre, arpjv__fpot,
            lpme__emne)
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
        ytw__ukncb, kul__vxtn = unicode_to_utf8_and_len(val)
        ijpz__ehe = getitem_str_offset(A, ind)
        rcq__yzmh = getitem_str_offset(A, ind + 1)
        kefl__cgd = rcq__yzmh - ijpz__ehe
        if kefl__cgd != kul__vxtn:
            return False
        ixsfb__jhf = get_data_ptr_ind(A, ijpz__ehe)
        return memcmp(ixsfb__jhf, ytw__ukncb, kul__vxtn) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        ijpz__ehe = getitem_str_offset(A, ind)
        kefl__cgd = bodo.libs.str_ext.int_to_str_len(val)
        qnpf__rwe = ijpz__ehe + kefl__cgd
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ijpz__ehe, qnpf__rwe)
        ixsfb__jhf = get_data_ptr_ind(A, ijpz__ehe)
        inplace_int64_to_str(ixsfb__jhf, kefl__cgd, val)
        setitem_str_offset(A, ind + 1, ijpz__ehe + kefl__cgd)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        ixsfb__jhf, = args
        plvyk__onx = context.insert_const_string(builder.module, '<NA>')
        bicd__poir = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, ixsfb__jhf, plvyk__onx, bicd__poir, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    iseu__xsh = len('<NA>')

    def impl(A, ind):
        ijpz__ehe = getitem_str_offset(A, ind)
        qnpf__rwe = ijpz__ehe + iseu__xsh
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ijpz__ehe, qnpf__rwe)
        ixsfb__jhf = get_data_ptr_ind(A, ijpz__ehe)
        inplace_set_NA_str(ixsfb__jhf)
        setitem_str_offset(A, ind + 1, ijpz__ehe + iseu__xsh)
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
            ijpz__ehe = getitem_str_offset(A, ind)
            rcq__yzmh = getitem_str_offset(A, ind + 1)
            idhzl__uiyc = rcq__yzmh - ijpz__ehe
            ixsfb__jhf = get_data_ptr_ind(A, ijpz__ehe)
            yio__evjzb = decode_utf8(ixsfb__jhf, idhzl__uiyc)
            return yio__evjzb
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            yjgki__wuu = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(yjgki__wuu):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            rvznf__hnhqf = get_data_ptr(out_arr).data
            fmt__jiycn = get_data_ptr(A).data
            mmtw__onmg = 0
            dhw__ghs = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(yjgki__wuu):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    zfhh__wmk = get_str_arr_item_length(A, i)
                    if zfhh__wmk == 1:
                        copy_single_char(rvznf__hnhqf, dhw__ghs, fmt__jiycn,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(rvznf__hnhqf, dhw__ghs, fmt__jiycn,
                            getitem_str_offset(A, i), zfhh__wmk, 1)
                    dhw__ghs += zfhh__wmk
                    setitem_str_offset(out_arr, mmtw__onmg + 1, dhw__ghs)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, mmtw__onmg)
                    else:
                        str_arr_set_not_na(out_arr, mmtw__onmg)
                    mmtw__onmg += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            yjgki__wuu = len(ind)
            out_arr = pre_alloc_string_array(yjgki__wuu, -1)
            mmtw__onmg = 0
            for i in range(yjgki__wuu):
                xncc__tpuuq = A[ind[i]]
                out_arr[mmtw__onmg] = xncc__tpuuq
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, mmtw__onmg)
                mmtw__onmg += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            yjgki__wuu = len(A)
            ecqfn__qbdgf = numba.cpython.unicode._normalize_slice(ind,
                yjgki__wuu)
            ncilb__vsdk = numba.cpython.unicode._slice_span(ecqfn__qbdgf)
            if ecqfn__qbdgf.step == 1:
                ijpz__ehe = getitem_str_offset(A, ecqfn__qbdgf.start)
                rcq__yzmh = getitem_str_offset(A, ecqfn__qbdgf.stop)
                n_chars = rcq__yzmh - ijpz__ehe
                mkxl__faqid = pre_alloc_string_array(ncilb__vsdk, np.int64(
                    n_chars))
                for i in range(ncilb__vsdk):
                    mkxl__faqid[i] = A[ecqfn__qbdgf.start + i]
                    if str_arr_is_na(A, ecqfn__qbdgf.start + i):
                        str_arr_set_na(mkxl__faqid, i)
                return mkxl__faqid
            else:
                mkxl__faqid = pre_alloc_string_array(ncilb__vsdk, -1)
                for i in range(ncilb__vsdk):
                    mkxl__faqid[i] = A[ecqfn__qbdgf.start + i *
                        ecqfn__qbdgf.step]
                    if str_arr_is_na(A, ecqfn__qbdgf.start + i *
                        ecqfn__qbdgf.step):
                        str_arr_set_na(mkxl__faqid, i)
                return mkxl__faqid
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
    gvu__qed = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(gvu__qed)
        vztn__nzbw = 4

        def impl_scalar(A, idx, val):
            pvnl__skrho = (val._length if val._is_ascii else vztn__nzbw *
                val._length)
            ykab__akg = A._data
            ijpz__ehe = np.int64(getitem_str_offset(A, idx))
            qnpf__rwe = ijpz__ehe + pvnl__skrho
            bodo.libs.array_item_arr_ext.ensure_data_capacity(ykab__akg,
                ijpz__ehe, qnpf__rwe)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                qnpf__rwe, val._data, val._length, val._kind, val._is_ascii,
                idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                ecqfn__qbdgf = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                vbk__fov = ecqfn__qbdgf.start
                ykab__akg = A._data
                ijpz__ehe = np.int64(getitem_str_offset(A, vbk__fov))
                qnpf__rwe = ijpz__ehe + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(ykab__akg,
                    ijpz__ehe, qnpf__rwe)
                set_string_array_range(A, val, vbk__fov, ijpz__ehe)
                sfhyi__nxma = 0
                for i in range(ecqfn__qbdgf.start, ecqfn__qbdgf.stop,
                    ecqfn__qbdgf.step):
                    if str_arr_is_na(val, sfhyi__nxma):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    sfhyi__nxma += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                gigpy__olnqz = str_list_to_array(val)
                A[idx] = gigpy__olnqz
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                ecqfn__qbdgf = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(ecqfn__qbdgf.start, ecqfn__qbdgf.stop,
                    ecqfn__qbdgf.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(gvu__qed)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                yjgki__wuu = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(yjgki__wuu, -1)
                for i in numba.parfors.parfor.internal_prange(yjgki__wuu):
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
                yjgki__wuu = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(yjgki__wuu, -1)
                mll__gnrpi = 0
                for i in numba.parfors.parfor.internal_prange(yjgki__wuu):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, mll__gnrpi):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, mll__gnrpi)
                        else:
                            out_arr[i] = str(val[mll__gnrpi])
                        mll__gnrpi += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(gvu__qed)
    raise BodoError(gvu__qed)


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
    heiy__qtpsu = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(heiy__qtpsu, (types.Float, types.Integer)
        ) and heiy__qtpsu not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(heiy__qtpsu, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            yjgki__wuu = len(A)
            B = np.empty(yjgki__wuu, heiy__qtpsu)
            for i in numba.parfors.parfor.internal_prange(yjgki__wuu):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif heiy__qtpsu == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            yjgki__wuu = len(A)
            B = np.empty(yjgki__wuu, heiy__qtpsu)
            for i in numba.parfors.parfor.internal_prange(yjgki__wuu):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif heiy__qtpsu == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            yjgki__wuu = len(A)
            B = np.empty(yjgki__wuu, heiy__qtpsu)
            for i in numba.parfors.parfor.internal_prange(yjgki__wuu):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            yjgki__wuu = len(A)
            B = np.empty(yjgki__wuu, heiy__qtpsu)
            for i in numba.parfors.parfor.internal_prange(yjgki__wuu):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        ixsfb__jhf, idhzl__uiyc = args
        xsnhw__pans = context.get_python_api(builder)
        yzkod__bbrd = xsnhw__pans.string_from_string_and_size(ixsfb__jhf,
            idhzl__uiyc)
        oaby__exu = xsnhw__pans.to_native_value(string_type, yzkod__bbrd).value
        zqrcg__uzjv = cgutils.create_struct_proxy(string_type)(context,
            builder, oaby__exu)
        zqrcg__uzjv.hash = zqrcg__uzjv.hash.type(-1)
        xsnhw__pans.decref(yzkod__bbrd)
        return zqrcg__uzjv._getvalue()
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
        jogd__cfjtl, arr, ind, tvkjn__xpfdz = args
        tnl__osi = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, tnl__osi.
            offsets).data
        data = context.make_helper(builder, char_arr_type, tnl__osi.data).data
        lamkx__nkpdy = lir.FunctionType(lir.IntType(32), [jogd__cfjtl.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        osaj__hbk = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            osaj__hbk = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        tqqs__dbvgm = cgutils.get_or_insert_function(builder.module,
            lamkx__nkpdy, osaj__hbk)
        return builder.call(tqqs__dbvgm, [jogd__cfjtl, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    xpl__ijh = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    lamkx__nkpdy = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(32)])
    drxp__mmee = cgutils.get_or_insert_function(c.builder.module,
        lamkx__nkpdy, name='string_array_from_sequence')
    idzax__hrhw = c.builder.call(drxp__mmee, [val, xpl__ijh])
    bxa__mgerh = ArrayItemArrayType(char_arr_type)
    afdh__vcdq = c.context.make_helper(c.builder, bxa__mgerh)
    afdh__vcdq.meminfo = idzax__hrhw
    mjncj__hvwk = c.context.make_helper(c.builder, typ)
    ykab__akg = afdh__vcdq._getvalue()
    mjncj__hvwk.data = ykab__akg
    nkmr__atay = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mjncj__hvwk._getvalue(), is_error=nkmr__atay)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    yjgki__wuu = len(pyval)
    dhw__ghs = 0
    qgj__srgcy = np.empty(yjgki__wuu + 1, np_offset_type)
    pjrp__ffcl = []
    kgd__ftkx = np.empty(yjgki__wuu + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        qgj__srgcy[i] = dhw__ghs
        mltan__qqoie = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(kgd__ftkx, i, int(not
            mltan__qqoie))
        if mltan__qqoie:
            continue
        vkm__xqp = list(s.encode()) if isinstance(s, str) else list(s)
        pjrp__ffcl.extend(vkm__xqp)
        dhw__ghs += len(vkm__xqp)
    qgj__srgcy[yjgki__wuu] = dhw__ghs
    rzwj__wuvv = np.array(pjrp__ffcl, np.uint8)
    qfrpx__wrz = context.get_constant(types.int64, yjgki__wuu)
    pgim__jtf = context.get_constant_generic(builder, char_arr_type, rzwj__wuvv
        )
    rnwyt__tgfvv = context.get_constant_generic(builder, offset_arr_type,
        qgj__srgcy)
    tyzo__isy = context.get_constant_generic(builder, null_bitmap_arr_type,
        kgd__ftkx)
    tnl__osi = lir.Constant.literal_struct([qfrpx__wrz, pgim__jtf,
        rnwyt__tgfvv, tyzo__isy])
    tnl__osi = cgutils.global_constant(builder, '.const.payload', tnl__osi
        ).bitcast(cgutils.voidptr_t)
    gxbk__hsrm = context.get_constant(types.int64, -1)
    wawuw__bwq = context.get_constant_null(types.voidptr)
    jsk__mikqi = lir.Constant.literal_struct([gxbk__hsrm, wawuw__bwq,
        wawuw__bwq, tnl__osi, gxbk__hsrm])
    jsk__mikqi = cgutils.global_constant(builder, '.const.meminfo', jsk__mikqi
        ).bitcast(cgutils.voidptr_t)
    ykab__akg = lir.Constant.literal_struct([jsk__mikqi])
    mjncj__hvwk = lir.Constant.literal_struct([ykab__akg])
    return mjncj__hvwk


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
