import operator
import llvmlite.binding as ll
import numba
import numba.core.typing.typeof
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, impl_ret_new_ref
from numba.extending import box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, _memcpy, char_arr_type, get_data_ptr, null_bitmap_arr_type, offset_arr_type, string_array_type
ll.add_symbol('array_setitem', hstr_ext.array_setitem)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
ll.add_symbol('dtor_str_arr_split_view', hstr_ext.dtor_str_arr_split_view)
ll.add_symbol('str_arr_split_view_impl', hstr_ext.str_arr_split_view_impl)
ll.add_symbol('str_arr_split_view_alloc', hstr_ext.str_arr_split_view_alloc)
char_typ = types.uint8
data_ctypes_type = types.ArrayCTypes(types.Array(char_typ, 1, 'C'))
offset_ctypes_type = types.ArrayCTypes(types.Array(offset_type, 1, 'C'))


class StringArraySplitViewType(types.ArrayCompatible):

    def __init__(self):
        super(StringArraySplitViewType, self).__init__(name=
            'StringArraySplitViewType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_array_type

    def copy(self):
        return StringArraySplitViewType()


string_array_split_view_type = StringArraySplitViewType()


class StringArraySplitViewPayloadType(types.Type):

    def __init__(self):
        super(StringArraySplitViewPayloadType, self).__init__(name=
            'StringArraySplitViewPayloadType()')


str_arr_split_view_payload_type = StringArraySplitViewPayloadType()


@register_model(StringArraySplitViewPayloadType)
class StringArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        leeh__zxv = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, leeh__zxv)


str_arr_model_members = [('num_items', types.uint64), ('index_offsets',
    types.CPointer(offset_type)), ('data_offsets', types.CPointer(
    offset_type)), ('data', data_ctypes_type), ('null_bitmap', types.
    CPointer(char_typ)), ('meminfo', types.MemInfoPointer(
    str_arr_split_view_payload_type))]


@register_model(StringArraySplitViewType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        models.StructModel.__init__(self, dmm, fe_type, str_arr_model_members)


make_attribute_wrapper(StringArraySplitViewType, 'num_items', '_num_items')
make_attribute_wrapper(StringArraySplitViewType, 'index_offsets',
    '_index_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data_offsets',
    '_data_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data', '_data')
make_attribute_wrapper(StringArraySplitViewType, 'null_bitmap', '_null_bitmap')


def construct_str_arr_split_view(context, builder):
    gsebk__tsi = context.get_value_type(str_arr_split_view_payload_type)
    gfjy__xrw = context.get_abi_sizeof(gsebk__tsi)
    ptg__gbm = context.get_value_type(types.voidptr)
    tynyi__eqp = context.get_value_type(types.uintp)
    uxkd__ivi = lir.FunctionType(lir.VoidType(), [ptg__gbm, tynyi__eqp,
        ptg__gbm])
    has__fthmv = cgutils.get_or_insert_function(builder.module, uxkd__ivi,
        name='dtor_str_arr_split_view')
    eajw__nle = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, gfjy__xrw), has__fthmv)
    lhgn__vsbg = context.nrt.meminfo_data(builder, eajw__nle)
    zra__zxib = builder.bitcast(lhgn__vsbg, gsebk__tsi.as_pointer())
    return eajw__nle, zra__zxib


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        jpif__ohxq, kavgr__ipswr = args
        eajw__nle, zra__zxib = construct_str_arr_split_view(context, builder)
        kewok__ntinm = _get_str_binary_arr_payload(context, builder,
            jpif__ohxq, string_array_type)
        sgwl__ncb = lir.FunctionType(lir.VoidType(), [zra__zxib.type, lir.
            IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        kvumz__sydc = cgutils.get_or_insert_function(builder.module,
            sgwl__ncb, name='str_arr_split_view_impl')
        xnv__mifu = context.make_helper(builder, offset_arr_type,
            kewok__ntinm.offsets).data
        ttqe__vfm = context.make_helper(builder, char_arr_type,
            kewok__ntinm.data).data
        boqy__svzao = context.make_helper(builder, null_bitmap_arr_type,
            kewok__ntinm.null_bitmap).data
        jue__olbyv = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(kvumz__sydc, [zra__zxib, kewok__ntinm.n_arrays,
            xnv__mifu, ttqe__vfm, boqy__svzao, jue__olbyv])
        mdd__eprmf = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(zra__zxib))
        lhzw__jlzsf = context.make_helper(builder, string_array_split_view_type
            )
        lhzw__jlzsf.num_items = kewok__ntinm.n_arrays
        lhzw__jlzsf.index_offsets = mdd__eprmf.index_offsets
        lhzw__jlzsf.data_offsets = mdd__eprmf.data_offsets
        lhzw__jlzsf.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [jpif__ohxq])
        lhzw__jlzsf.null_bitmap = mdd__eprmf.null_bitmap
        lhzw__jlzsf.meminfo = eajw__nle
        wxw__tgivt = lhzw__jlzsf._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, wxw__tgivt)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    qhih__fum = context.make_helper(builder, string_array_split_view_type, val)
    lrci__tqsm = context.insert_const_string(builder.module, 'numpy')
    gir__vtsf = c.pyapi.import_module_noblock(lrci__tqsm)
    dtype = c.pyapi.object_getattr_string(gir__vtsf, 'object_')
    sqe__swor = builder.sext(qhih__fum.num_items, c.pyapi.longlong)
    jbtf__lcotg = c.pyapi.long_from_longlong(sqe__swor)
    ttraq__uadro = c.pyapi.call_method(gir__vtsf, 'ndarray', (jbtf__lcotg,
        dtype))
    wew__sotxp = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    ayhqj__zip = c.pyapi._get_function(wew__sotxp, name='array_getptr1')
    vrigb__klm = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    xgrj__rspyl = c.pyapi._get_function(vrigb__klm, name='array_setitem')
    vgro__zhzb = c.pyapi.object_getattr_string(gir__vtsf, 'nan')
    with cgutils.for_range(builder, qhih__fum.num_items) as ovt__mxfiq:
        str_ind = ovt__mxfiq.index
        bqq__edqqh = builder.sext(builder.load(builder.gep(qhih__fum.
            index_offsets, [str_ind])), lir.IntType(64))
        mbly__bfviv = builder.sext(builder.load(builder.gep(qhih__fum.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        nylxs__owv = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        vziq__ogsn = builder.gep(qhih__fum.null_bitmap, [nylxs__owv])
        eqmaf__gqegh = builder.load(vziq__ogsn)
        cxiu__jnmge = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(eqmaf__gqegh, cxiu__jnmge), lir.
            Constant(lir.IntType(8), 1))
        qfif__uzlmh = builder.sub(mbly__bfviv, bqq__edqqh)
        qfif__uzlmh = builder.sub(qfif__uzlmh, qfif__uzlmh.type(1))
        fyq__lqvlv = builder.call(ayhqj__zip, [ttraq__uadro, str_ind])
        ckh__etj = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(ckh__etj) as (mat__pyi, aidmp__hlo):
            with mat__pyi:
                bocc__ddjx = c.pyapi.list_new(qfif__uzlmh)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    bocc__ddjx), likely=True):
                    with cgutils.for_range(c.builder, qfif__uzlmh
                        ) as ovt__mxfiq:
                        tghto__lxtyo = builder.add(bqq__edqqh, ovt__mxfiq.index
                            )
                        data_start = builder.load(builder.gep(qhih__fum.
                            data_offsets, [tghto__lxtyo]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        octm__eew = builder.load(builder.gep(qhih__fum.
                            data_offsets, [builder.add(tghto__lxtyo,
                            tghto__lxtyo.type(1))]))
                        gyc__edmj = builder.gep(builder.extract_value(
                            qhih__fum.data, 0), [data_start])
                        sssis__vpc = builder.sext(builder.sub(octm__eew,
                            data_start), lir.IntType(64))
                        bsoqx__mih = c.pyapi.string_from_string_and_size(
                            gyc__edmj, sssis__vpc)
                        c.pyapi.list_setitem(bocc__ddjx, ovt__mxfiq.index,
                            bsoqx__mih)
                builder.call(xgrj__rspyl, [ttraq__uadro, fyq__lqvlv,
                    bocc__ddjx])
            with aidmp__hlo:
                builder.call(xgrj__rspyl, [ttraq__uadro, fyq__lqvlv,
                    vgro__zhzb])
    c.pyapi.decref(gir__vtsf)
    c.pyapi.decref(dtype)
    c.pyapi.decref(vgro__zhzb)
    return ttraq__uadro


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        kbczd__tsi, bxbz__tor, gyc__edmj = args
        eajw__nle, zra__zxib = construct_str_arr_split_view(context, builder)
        sgwl__ncb = lir.FunctionType(lir.VoidType(), [zra__zxib.type, lir.
            IntType(64), lir.IntType(64)])
        kvumz__sydc = cgutils.get_or_insert_function(builder.module,
            sgwl__ncb, name='str_arr_split_view_alloc')
        builder.call(kvumz__sydc, [zra__zxib, kbczd__tsi, bxbz__tor])
        mdd__eprmf = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(zra__zxib))
        lhzw__jlzsf = context.make_helper(builder, string_array_split_view_type
            )
        lhzw__jlzsf.num_items = kbczd__tsi
        lhzw__jlzsf.index_offsets = mdd__eprmf.index_offsets
        lhzw__jlzsf.data_offsets = mdd__eprmf.data_offsets
        lhzw__jlzsf.data = gyc__edmj
        lhzw__jlzsf.null_bitmap = mdd__eprmf.null_bitmap
        context.nrt.incref(builder, data_t, gyc__edmj)
        lhzw__jlzsf.meminfo = eajw__nle
        wxw__tgivt = lhzw__jlzsf._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, wxw__tgivt)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        xoep__kdor, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            xoep__kdor = builder.extract_value(xoep__kdor, 0)
        return builder.bitcast(builder.gep(xoep__kdor, [ind]), lir.IntType(
            8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        xoep__kdor, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            xoep__kdor = builder.extract_value(xoep__kdor, 0)
        return builder.load(builder.gep(xoep__kdor, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        xoep__kdor, ind, iak__mxl = args
        spung__hhycf = builder.gep(xoep__kdor, [ind])
        builder.store(iak__mxl, spung__hhycf)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        iqbhx__kjxmb, ind = args
        vixod__jkxzd = context.make_helper(builder, arr_ctypes_t, iqbhx__kjxmb)
        aznj__istlx = context.make_helper(builder, arr_ctypes_t)
        aznj__istlx.data = builder.gep(vixod__jkxzd.data, [ind])
        aznj__istlx.meminfo = vixod__jkxzd.meminfo
        ofnej__ztxjg = aznj__istlx._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, ofnej__ztxjg)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    gqx__hbzpo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not gqx__hbzpo:
        return 0, 0, 0
    tghto__lxtyo = getitem_c_arr(arr._index_offsets, item_ind)
    vnsed__vtw = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    yalvd__irvd = vnsed__vtw - tghto__lxtyo
    if str_ind >= yalvd__irvd:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, tghto__lxtyo + str_ind)
    data_start += 1
    if tghto__lxtyo + str_ind == 0:
        data_start = 0
    octm__eew = getitem_c_arr(arr._data_offsets, tghto__lxtyo + str_ind + 1)
    vine__bjisq = octm__eew - data_start
    return 1, data_start, vine__bjisq


@numba.njit(no_cpython_wrapper=True)
def get_split_view_data_ptr(arr, data_start):
    return get_array_ctypes_ptr(arr._data, data_start)


@overload(len, no_unliteral=True)
def str_arr_split_view_len_overload(arr):
    if arr == string_array_split_view_type:
        return lambda arr: np.int64(arr._num_items)


@overload_attribute(StringArraySplitViewType, 'shape')
def overload_split_view_arr_shape(A):
    return lambda A: (np.int64(A._num_items),)


@overload(operator.getitem, no_unliteral=True)
def str_arr_split_view_getitem_overload(A, ind):
    if A != string_array_split_view_type:
        return
    if A == string_array_split_view_type and isinstance(ind, types.Integer):
        npc__kkr = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            tghto__lxtyo = getitem_c_arr(A._index_offsets, ind)
            vnsed__vtw = getitem_c_arr(A._index_offsets, ind + 1)
            xnfww__alt = vnsed__vtw - tghto__lxtyo - 1
            jpif__ohxq = bodo.libs.str_arr_ext.pre_alloc_string_array(
                xnfww__alt, -1)
            for iaer__xfg in range(xnfww__alt):
                data_start = getitem_c_arr(A._data_offsets, tghto__lxtyo +
                    iaer__xfg)
                data_start += 1
                if tghto__lxtyo + iaer__xfg == 0:
                    data_start = 0
                octm__eew = getitem_c_arr(A._data_offsets, tghto__lxtyo +
                    iaer__xfg + 1)
                vine__bjisq = octm__eew - data_start
                spung__hhycf = get_array_ctypes_ptr(A._data, data_start)
                nqqlj__xsw = bodo.libs.str_arr_ext.decode_utf8(spung__hhycf,
                    vine__bjisq)
                jpif__ohxq[iaer__xfg] = nqqlj__xsw
            return jpif__ohxq
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        cjg__wbbp = offset_type.bitwidth // 8

        def _impl(A, ind):
            xnfww__alt = len(A)
            if xnfww__alt != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            kbczd__tsi = 0
            bxbz__tor = 0
            for iaer__xfg in range(xnfww__alt):
                if ind[iaer__xfg]:
                    kbczd__tsi += 1
                    tghto__lxtyo = getitem_c_arr(A._index_offsets, iaer__xfg)
                    vnsed__vtw = getitem_c_arr(A._index_offsets, iaer__xfg + 1)
                    bxbz__tor += vnsed__vtw - tghto__lxtyo
            ttraq__uadro = pre_alloc_str_arr_view(kbczd__tsi, bxbz__tor, A.
                _data)
            item_ind = 0
            pvljd__hsnas = 0
            for iaer__xfg in range(xnfww__alt):
                if ind[iaer__xfg]:
                    tghto__lxtyo = getitem_c_arr(A._index_offsets, iaer__xfg)
                    vnsed__vtw = getitem_c_arr(A._index_offsets, iaer__xfg + 1)
                    fqcvs__asm = vnsed__vtw - tghto__lxtyo
                    setitem_c_arr(ttraq__uadro._index_offsets, item_ind,
                        pvljd__hsnas)
                    spung__hhycf = get_c_arr_ptr(A._data_offsets, tghto__lxtyo)
                    xji__recss = get_c_arr_ptr(ttraq__uadro._data_offsets,
                        pvljd__hsnas)
                    _memcpy(xji__recss, spung__hhycf, fqcvs__asm, cjg__wbbp)
                    gqx__hbzpo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, iaer__xfg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ttraq__uadro.
                        _null_bitmap, item_ind, gqx__hbzpo)
                    item_ind += 1
                    pvljd__hsnas += fqcvs__asm
            setitem_c_arr(ttraq__uadro._index_offsets, item_ind, pvljd__hsnas)
            return ttraq__uadro
        return _impl
