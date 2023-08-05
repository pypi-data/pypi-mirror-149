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
        wvna__nklv = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, wvna__nklv)


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
    dpqil__imkq = context.get_value_type(str_arr_split_view_payload_type)
    dnnax__gqrcn = context.get_abi_sizeof(dpqil__imkq)
    bntde__jeal = context.get_value_type(types.voidptr)
    jax__cba = context.get_value_type(types.uintp)
    bbhlt__dkw = lir.FunctionType(lir.VoidType(), [bntde__jeal, jax__cba,
        bntde__jeal])
    pugd__yfw = cgutils.get_or_insert_function(builder.module, bbhlt__dkw,
        name='dtor_str_arr_split_view')
    cdi__dpnn = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, dnnax__gqrcn), pugd__yfw)
    otjak__ryh = context.nrt.meminfo_data(builder, cdi__dpnn)
    febap__tdacr = builder.bitcast(otjak__ryh, dpqil__imkq.as_pointer())
    return cdi__dpnn, febap__tdacr


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        nyb__xzkw, owanc__etw = args
        cdi__dpnn, febap__tdacr = construct_str_arr_split_view(context, builder
            )
        ybtxl__koxdw = _get_str_binary_arr_payload(context, builder,
            nyb__xzkw, string_array_type)
        ahjsl__ywv = lir.FunctionType(lir.VoidType(), [febap__tdacr.type,
            lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        rvmx__xlfpk = cgutils.get_or_insert_function(builder.module,
            ahjsl__ywv, name='str_arr_split_view_impl')
        rxck__uul = context.make_helper(builder, offset_arr_type,
            ybtxl__koxdw.offsets).data
        lfe__clfhs = context.make_helper(builder, char_arr_type,
            ybtxl__koxdw.data).data
        udccl__jnqyi = context.make_helper(builder, null_bitmap_arr_type,
            ybtxl__koxdw.null_bitmap).data
        wqycg__ullps = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(rvmx__xlfpk, [febap__tdacr, ybtxl__koxdw.n_arrays,
            rxck__uul, lfe__clfhs, udccl__jnqyi, wqycg__ullps])
        cevkk__byh = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(febap__tdacr))
        fst__hkz = context.make_helper(builder, string_array_split_view_type)
        fst__hkz.num_items = ybtxl__koxdw.n_arrays
        fst__hkz.index_offsets = cevkk__byh.index_offsets
        fst__hkz.data_offsets = cevkk__byh.data_offsets
        fst__hkz.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [nyb__xzkw])
        fst__hkz.null_bitmap = cevkk__byh.null_bitmap
        fst__hkz.meminfo = cdi__dpnn
        gnneu__ztyht = fst__hkz._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, gnneu__ztyht)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    gusib__htwp = context.make_helper(builder, string_array_split_view_type,
        val)
    mif__xonw = context.insert_const_string(builder.module, 'numpy')
    ozm__sdew = c.pyapi.import_module_noblock(mif__xonw)
    dtype = c.pyapi.object_getattr_string(ozm__sdew, 'object_')
    zeq__tgk = builder.sext(gusib__htwp.num_items, c.pyapi.longlong)
    reyt__zcgn = c.pyapi.long_from_longlong(zeq__tgk)
    thj__cjk = c.pyapi.call_method(ozm__sdew, 'ndarray', (reyt__zcgn, dtype))
    dioo__cksii = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    yyd__peq = c.pyapi._get_function(dioo__cksii, name='array_getptr1')
    bdrf__puhye = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    pbywg__mchev = c.pyapi._get_function(bdrf__puhye, name='array_setitem')
    lyef__ely = c.pyapi.object_getattr_string(ozm__sdew, 'nan')
    with cgutils.for_range(builder, gusib__htwp.num_items) as fbzws__exe:
        str_ind = fbzws__exe.index
        nfhm__wirk = builder.sext(builder.load(builder.gep(gusib__htwp.
            index_offsets, [str_ind])), lir.IntType(64))
        armh__rtr = builder.sext(builder.load(builder.gep(gusib__htwp.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        hktu__hyuk = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        lwed__uwwh = builder.gep(gusib__htwp.null_bitmap, [hktu__hyuk])
        vnahv__skdjf = builder.load(lwed__uwwh)
        kwuw__pkzvh = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(vnahv__skdjf, kwuw__pkzvh), lir.
            Constant(lir.IntType(8), 1))
        the__ttrzj = builder.sub(armh__rtr, nfhm__wirk)
        the__ttrzj = builder.sub(the__ttrzj, the__ttrzj.type(1))
        jqwgv__tsab = builder.call(yyd__peq, [thj__cjk, str_ind])
        omc__pego = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(omc__pego) as (asfdp__hmgz, lqnk__wbkzj):
            with asfdp__hmgz:
                pza__mqpn = c.pyapi.list_new(the__ttrzj)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    pza__mqpn), likely=True):
                    with cgutils.for_range(c.builder, the__ttrzj
                        ) as fbzws__exe:
                        tmkwu__rfz = builder.add(nfhm__wirk, fbzws__exe.index)
                        data_start = builder.load(builder.gep(gusib__htwp.
                            data_offsets, [tmkwu__rfz]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        dyd__ekjz = builder.load(builder.gep(gusib__htwp.
                            data_offsets, [builder.add(tmkwu__rfz,
                            tmkwu__rfz.type(1))]))
                        izsez__cdybm = builder.gep(builder.extract_value(
                            gusib__htwp.data, 0), [data_start])
                        kwu__qclw = builder.sext(builder.sub(dyd__ekjz,
                            data_start), lir.IntType(64))
                        hnvzm__zgmvt = c.pyapi.string_from_string_and_size(
                            izsez__cdybm, kwu__qclw)
                        c.pyapi.list_setitem(pza__mqpn, fbzws__exe.index,
                            hnvzm__zgmvt)
                builder.call(pbywg__mchev, [thj__cjk, jqwgv__tsab, pza__mqpn])
            with lqnk__wbkzj:
                builder.call(pbywg__mchev, [thj__cjk, jqwgv__tsab, lyef__ely])
    c.pyapi.decref(ozm__sdew)
    c.pyapi.decref(dtype)
    c.pyapi.decref(lyef__ely)
    return thj__cjk


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        uqz__phhq, ybhat__xag, izsez__cdybm = args
        cdi__dpnn, febap__tdacr = construct_str_arr_split_view(context, builder
            )
        ahjsl__ywv = lir.FunctionType(lir.VoidType(), [febap__tdacr.type,
            lir.IntType(64), lir.IntType(64)])
        rvmx__xlfpk = cgutils.get_or_insert_function(builder.module,
            ahjsl__ywv, name='str_arr_split_view_alloc')
        builder.call(rvmx__xlfpk, [febap__tdacr, uqz__phhq, ybhat__xag])
        cevkk__byh = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(febap__tdacr))
        fst__hkz = context.make_helper(builder, string_array_split_view_type)
        fst__hkz.num_items = uqz__phhq
        fst__hkz.index_offsets = cevkk__byh.index_offsets
        fst__hkz.data_offsets = cevkk__byh.data_offsets
        fst__hkz.data = izsez__cdybm
        fst__hkz.null_bitmap = cevkk__byh.null_bitmap
        context.nrt.incref(builder, data_t, izsez__cdybm)
        fst__hkz.meminfo = cdi__dpnn
        gnneu__ztyht = fst__hkz._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, gnneu__ztyht)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        apabk__tkodb, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            apabk__tkodb = builder.extract_value(apabk__tkodb, 0)
        return builder.bitcast(builder.gep(apabk__tkodb, [ind]), lir.
            IntType(8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        apabk__tkodb, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            apabk__tkodb = builder.extract_value(apabk__tkodb, 0)
        return builder.load(builder.gep(apabk__tkodb, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        apabk__tkodb, ind, xtl__dgaz = args
        yrgez__pof = builder.gep(apabk__tkodb, [ind])
        builder.store(xtl__dgaz, yrgez__pof)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        cxvac__xgng, ind = args
        iha__kufle = context.make_helper(builder, arr_ctypes_t, cxvac__xgng)
        xtng__lhnp = context.make_helper(builder, arr_ctypes_t)
        xtng__lhnp.data = builder.gep(iha__kufle.data, [ind])
        xtng__lhnp.meminfo = iha__kufle.meminfo
        aon__ahlzi = xtng__lhnp._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, aon__ahlzi)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    qxtfn__bbis = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not qxtfn__bbis:
        return 0, 0, 0
    tmkwu__rfz = getitem_c_arr(arr._index_offsets, item_ind)
    jxkq__ekv = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    usrj__emt = jxkq__ekv - tmkwu__rfz
    if str_ind >= usrj__emt:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, tmkwu__rfz + str_ind)
    data_start += 1
    if tmkwu__rfz + str_ind == 0:
        data_start = 0
    dyd__ekjz = getitem_c_arr(arr._data_offsets, tmkwu__rfz + str_ind + 1)
    osxyd__jyk = dyd__ekjz - data_start
    return 1, data_start, osxyd__jyk


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
        iht__cuqz = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            tmkwu__rfz = getitem_c_arr(A._index_offsets, ind)
            jxkq__ekv = getitem_c_arr(A._index_offsets, ind + 1)
            jok__ius = jxkq__ekv - tmkwu__rfz - 1
            nyb__xzkw = bodo.libs.str_arr_ext.pre_alloc_string_array(jok__ius,
                -1)
            for ktrtv__gmn in range(jok__ius):
                data_start = getitem_c_arr(A._data_offsets, tmkwu__rfz +
                    ktrtv__gmn)
                data_start += 1
                if tmkwu__rfz + ktrtv__gmn == 0:
                    data_start = 0
                dyd__ekjz = getitem_c_arr(A._data_offsets, tmkwu__rfz +
                    ktrtv__gmn + 1)
                osxyd__jyk = dyd__ekjz - data_start
                yrgez__pof = get_array_ctypes_ptr(A._data, data_start)
                nzton__nawnl = bodo.libs.str_arr_ext.decode_utf8(yrgez__pof,
                    osxyd__jyk)
                nyb__xzkw[ktrtv__gmn] = nzton__nawnl
            return nyb__xzkw
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        kslod__pgr = offset_type.bitwidth // 8

        def _impl(A, ind):
            jok__ius = len(A)
            if jok__ius != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            uqz__phhq = 0
            ybhat__xag = 0
            for ktrtv__gmn in range(jok__ius):
                if ind[ktrtv__gmn]:
                    uqz__phhq += 1
                    tmkwu__rfz = getitem_c_arr(A._index_offsets, ktrtv__gmn)
                    jxkq__ekv = getitem_c_arr(A._index_offsets, ktrtv__gmn + 1)
                    ybhat__xag += jxkq__ekv - tmkwu__rfz
            thj__cjk = pre_alloc_str_arr_view(uqz__phhq, ybhat__xag, A._data)
            item_ind = 0
            nsyfo__rprw = 0
            for ktrtv__gmn in range(jok__ius):
                if ind[ktrtv__gmn]:
                    tmkwu__rfz = getitem_c_arr(A._index_offsets, ktrtv__gmn)
                    jxkq__ekv = getitem_c_arr(A._index_offsets, ktrtv__gmn + 1)
                    six__ldob = jxkq__ekv - tmkwu__rfz
                    setitem_c_arr(thj__cjk._index_offsets, item_ind,
                        nsyfo__rprw)
                    yrgez__pof = get_c_arr_ptr(A._data_offsets, tmkwu__rfz)
                    enny__ilx = get_c_arr_ptr(thj__cjk._data_offsets,
                        nsyfo__rprw)
                    _memcpy(enny__ilx, yrgez__pof, six__ldob, kslod__pgr)
                    qxtfn__bbis = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, ktrtv__gmn)
                    bodo.libs.int_arr_ext.set_bit_to_arr(thj__cjk.
                        _null_bitmap, item_ind, qxtfn__bbis)
                    item_ind += 1
                    nsyfo__rprw += six__ldob
            setitem_c_arr(thj__cjk._index_offsets, item_ind, nsyfo__rprw)
            return thj__cjk
        return _impl
