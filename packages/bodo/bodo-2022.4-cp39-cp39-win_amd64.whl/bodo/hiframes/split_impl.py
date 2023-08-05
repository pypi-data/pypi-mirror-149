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
        yxbbp__nyx = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, yxbbp__nyx)


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
    zxp__mbwg = context.get_value_type(str_arr_split_view_payload_type)
    qjihe__yzfv = context.get_abi_sizeof(zxp__mbwg)
    zncp__nto = context.get_value_type(types.voidptr)
    txxp__nuzy = context.get_value_type(types.uintp)
    pot__cpfxq = lir.FunctionType(lir.VoidType(), [zncp__nto, txxp__nuzy,
        zncp__nto])
    bryt__gzt = cgutils.get_or_insert_function(builder.module, pot__cpfxq,
        name='dtor_str_arr_split_view')
    incqq__qydz = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, qjihe__yzfv), bryt__gzt)
    tny__hosj = context.nrt.meminfo_data(builder, incqq__qydz)
    bhx__qhqno = builder.bitcast(tny__hosj, zxp__mbwg.as_pointer())
    return incqq__qydz, bhx__qhqno


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        ygfr__gyn, jxocs__snol = args
        incqq__qydz, bhx__qhqno = construct_str_arr_split_view(context, builder
            )
        ymb__ume = _get_str_binary_arr_payload(context, builder, ygfr__gyn,
            string_array_type)
        dvmz__pya = lir.FunctionType(lir.VoidType(), [bhx__qhqno.type, lir.
            IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        hnte__naxr = cgutils.get_or_insert_function(builder.module,
            dvmz__pya, name='str_arr_split_view_impl')
        vyhnt__dzwy = context.make_helper(builder, offset_arr_type,
            ymb__ume.offsets).data
        sdytq__qtc = context.make_helper(builder, char_arr_type, ymb__ume.data
            ).data
        wwg__mjq = context.make_helper(builder, null_bitmap_arr_type,
            ymb__ume.null_bitmap).data
        xybvb__vhzw = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(hnte__naxr, [bhx__qhqno, ymb__ume.n_arrays,
            vyhnt__dzwy, sdytq__qtc, wwg__mjq, xybvb__vhzw])
        xrce__sms = cgutils.create_struct_proxy(str_arr_split_view_payload_type
            )(context, builder, value=builder.load(bhx__qhqno))
        nhauf__rmkaq = context.make_helper(builder,
            string_array_split_view_type)
        nhauf__rmkaq.num_items = ymb__ume.n_arrays
        nhauf__rmkaq.index_offsets = xrce__sms.index_offsets
        nhauf__rmkaq.data_offsets = xrce__sms.data_offsets
        nhauf__rmkaq.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [ygfr__gyn])
        nhauf__rmkaq.null_bitmap = xrce__sms.null_bitmap
        nhauf__rmkaq.meminfo = incqq__qydz
        axzje__ema = nhauf__rmkaq._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, axzje__ema)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    uljm__pihjg = context.make_helper(builder, string_array_split_view_type,
        val)
    ijt__zgnnr = context.insert_const_string(builder.module, 'numpy')
    mbbus__nskb = c.pyapi.import_module_noblock(ijt__zgnnr)
    dtype = c.pyapi.object_getattr_string(mbbus__nskb, 'object_')
    elfb__qggl = builder.sext(uljm__pihjg.num_items, c.pyapi.longlong)
    uouhc__jgsdw = c.pyapi.long_from_longlong(elfb__qggl)
    hgltz__xqj = c.pyapi.call_method(mbbus__nskb, 'ndarray', (uouhc__jgsdw,
        dtype))
    pqfbq__snqs = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    szsht__diazh = c.pyapi._get_function(pqfbq__snqs, name='array_getptr1')
    yxs__rdr = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.IntType
        (8).as_pointer(), c.pyapi.pyobj])
    sfcta__doo = c.pyapi._get_function(yxs__rdr, name='array_setitem')
    pvsgb__xlyq = c.pyapi.object_getattr_string(mbbus__nskb, 'nan')
    with cgutils.for_range(builder, uljm__pihjg.num_items) as gtyg__mszcj:
        str_ind = gtyg__mszcj.index
        cbcld__pzi = builder.sext(builder.load(builder.gep(uljm__pihjg.
            index_offsets, [str_ind])), lir.IntType(64))
        lvwv__zrv = builder.sext(builder.load(builder.gep(uljm__pihjg.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        zue__ffji = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        uof__knj = builder.gep(uljm__pihjg.null_bitmap, [zue__ffji])
        pyfiz__rpk = builder.load(uof__knj)
        wipbj__jvv = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(pyfiz__rpk, wipbj__jvv), lir.
            Constant(lir.IntType(8), 1))
        aab__ejzk = builder.sub(lvwv__zrv, cbcld__pzi)
        aab__ejzk = builder.sub(aab__ejzk, aab__ejzk.type(1))
        aer__uqgt = builder.call(szsht__diazh, [hgltz__xqj, str_ind])
        uufp__ticss = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(uufp__ticss) as (afq__fxz, zjg__nmxlx):
            with afq__fxz:
                qtzrp__jpncd = c.pyapi.list_new(aab__ejzk)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    qtzrp__jpncd), likely=True):
                    with cgutils.for_range(c.builder, aab__ejzk
                        ) as gtyg__mszcj:
                        bvxjd__xlpw = builder.add(cbcld__pzi, gtyg__mszcj.index
                            )
                        data_start = builder.load(builder.gep(uljm__pihjg.
                            data_offsets, [bvxjd__xlpw]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        vptci__xmje = builder.load(builder.gep(uljm__pihjg.
                            data_offsets, [builder.add(bvxjd__xlpw,
                            bvxjd__xlpw.type(1))]))
                        botf__rjpb = builder.gep(builder.extract_value(
                            uljm__pihjg.data, 0), [data_start])
                        vqdn__ttxn = builder.sext(builder.sub(vptci__xmje,
                            data_start), lir.IntType(64))
                        eoxaj__htop = c.pyapi.string_from_string_and_size(
                            botf__rjpb, vqdn__ttxn)
                        c.pyapi.list_setitem(qtzrp__jpncd, gtyg__mszcj.
                            index, eoxaj__htop)
                builder.call(sfcta__doo, [hgltz__xqj, aer__uqgt, qtzrp__jpncd])
            with zjg__nmxlx:
                builder.call(sfcta__doo, [hgltz__xqj, aer__uqgt, pvsgb__xlyq])
    c.pyapi.decref(mbbus__nskb)
    c.pyapi.decref(dtype)
    c.pyapi.decref(pvsgb__xlyq)
    return hgltz__xqj


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        tca__dcxhk, dxqnk__unq, botf__rjpb = args
        incqq__qydz, bhx__qhqno = construct_str_arr_split_view(context, builder
            )
        dvmz__pya = lir.FunctionType(lir.VoidType(), [bhx__qhqno.type, lir.
            IntType(64), lir.IntType(64)])
        hnte__naxr = cgutils.get_or_insert_function(builder.module,
            dvmz__pya, name='str_arr_split_view_alloc')
        builder.call(hnte__naxr, [bhx__qhqno, tca__dcxhk, dxqnk__unq])
        xrce__sms = cgutils.create_struct_proxy(str_arr_split_view_payload_type
            )(context, builder, value=builder.load(bhx__qhqno))
        nhauf__rmkaq = context.make_helper(builder,
            string_array_split_view_type)
        nhauf__rmkaq.num_items = tca__dcxhk
        nhauf__rmkaq.index_offsets = xrce__sms.index_offsets
        nhauf__rmkaq.data_offsets = xrce__sms.data_offsets
        nhauf__rmkaq.data = botf__rjpb
        nhauf__rmkaq.null_bitmap = xrce__sms.null_bitmap
        context.nrt.incref(builder, data_t, botf__rjpb)
        nhauf__rmkaq.meminfo = incqq__qydz
        axzje__ema = nhauf__rmkaq._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, axzje__ema)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        ycx__laj, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            ycx__laj = builder.extract_value(ycx__laj, 0)
        return builder.bitcast(builder.gep(ycx__laj, [ind]), lir.IntType(8)
            .as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        ycx__laj, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            ycx__laj = builder.extract_value(ycx__laj, 0)
        return builder.load(builder.gep(ycx__laj, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        ycx__laj, ind, ath__odlu = args
        ptuz__hnb = builder.gep(ycx__laj, [ind])
        builder.store(ath__odlu, ptuz__hnb)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        vipny__ztevm, ind = args
        kfbg__hak = context.make_helper(builder, arr_ctypes_t, vipny__ztevm)
        wpojw__cxmy = context.make_helper(builder, arr_ctypes_t)
        wpojw__cxmy.data = builder.gep(kfbg__hak.data, [ind])
        wpojw__cxmy.meminfo = kfbg__hak.meminfo
        jgmbp__fahgc = wpojw__cxmy._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, jgmbp__fahgc)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    vrt__chqo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not vrt__chqo:
        return 0, 0, 0
    bvxjd__xlpw = getitem_c_arr(arr._index_offsets, item_ind)
    jnp__wdtx = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    dqtb__ojct = jnp__wdtx - bvxjd__xlpw
    if str_ind >= dqtb__ojct:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, bvxjd__xlpw + str_ind)
    data_start += 1
    if bvxjd__xlpw + str_ind == 0:
        data_start = 0
    vptci__xmje = getitem_c_arr(arr._data_offsets, bvxjd__xlpw + str_ind + 1)
    eequ__lwvy = vptci__xmje - data_start
    return 1, data_start, eequ__lwvy


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
        qxpq__pjsq = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            bvxjd__xlpw = getitem_c_arr(A._index_offsets, ind)
            jnp__wdtx = getitem_c_arr(A._index_offsets, ind + 1)
            xxfh__clhut = jnp__wdtx - bvxjd__xlpw - 1
            ygfr__gyn = bodo.libs.str_arr_ext.pre_alloc_string_array(
                xxfh__clhut, -1)
            for pcnv__ufwf in range(xxfh__clhut):
                data_start = getitem_c_arr(A._data_offsets, bvxjd__xlpw +
                    pcnv__ufwf)
                data_start += 1
                if bvxjd__xlpw + pcnv__ufwf == 0:
                    data_start = 0
                vptci__xmje = getitem_c_arr(A._data_offsets, bvxjd__xlpw +
                    pcnv__ufwf + 1)
                eequ__lwvy = vptci__xmje - data_start
                ptuz__hnb = get_array_ctypes_ptr(A._data, data_start)
                vxfn__gjek = bodo.libs.str_arr_ext.decode_utf8(ptuz__hnb,
                    eequ__lwvy)
                ygfr__gyn[pcnv__ufwf] = vxfn__gjek
            return ygfr__gyn
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        vevxy__ituc = offset_type.bitwidth // 8

        def _impl(A, ind):
            xxfh__clhut = len(A)
            if xxfh__clhut != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            tca__dcxhk = 0
            dxqnk__unq = 0
            for pcnv__ufwf in range(xxfh__clhut):
                if ind[pcnv__ufwf]:
                    tca__dcxhk += 1
                    bvxjd__xlpw = getitem_c_arr(A._index_offsets, pcnv__ufwf)
                    jnp__wdtx = getitem_c_arr(A._index_offsets, pcnv__ufwf + 1)
                    dxqnk__unq += jnp__wdtx - bvxjd__xlpw
            hgltz__xqj = pre_alloc_str_arr_view(tca__dcxhk, dxqnk__unq, A._data
                )
            item_ind = 0
            osvr__jkfbt = 0
            for pcnv__ufwf in range(xxfh__clhut):
                if ind[pcnv__ufwf]:
                    bvxjd__xlpw = getitem_c_arr(A._index_offsets, pcnv__ufwf)
                    jnp__wdtx = getitem_c_arr(A._index_offsets, pcnv__ufwf + 1)
                    eqeqf__vtd = jnp__wdtx - bvxjd__xlpw
                    setitem_c_arr(hgltz__xqj._index_offsets, item_ind,
                        osvr__jkfbt)
                    ptuz__hnb = get_c_arr_ptr(A._data_offsets, bvxjd__xlpw)
                    yis__tiurz = get_c_arr_ptr(hgltz__xqj._data_offsets,
                        osvr__jkfbt)
                    _memcpy(yis__tiurz, ptuz__hnb, eqeqf__vtd, vevxy__ituc)
                    vrt__chqo = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, pcnv__ufwf)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hgltz__xqj.
                        _null_bitmap, item_ind, vrt__chqo)
                    item_ind += 1
                    osvr__jkfbt += eqeqf__vtd
            setitem_c_arr(hgltz__xqj._index_offsets, item_ind, osvr__jkfbt)
            return hgltz__xqj
        return _impl
