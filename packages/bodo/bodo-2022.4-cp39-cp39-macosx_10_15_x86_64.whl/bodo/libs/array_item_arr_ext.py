"""Array implementation for variable-size array items.
Corresponds to Spark's ArrayType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Variable-size List: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in a contingous data array, while an offsets array marks the
individual arrays. For example:
value:             [[1, 2], [3], None, [5, 4, 6], []]
data:              [1, 2, 3, 5, 4, 6]
offsets:           [0, 2, 3, 3, 6, 6]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('array_item_array_from_sequence', array_ext.
    array_item_array_from_sequence)
ll.add_symbol('np_array_from_array_item_array', array_ext.
    np_array_from_array_item_array)
offset_type = types.uint64
np_offset_type = numba.np.numpy_support.as_dtype(offset_type)


class ArrayItemArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        assert bodo.utils.utils.is_array_typ(dtype, False)
        self.dtype = dtype
        super(ArrayItemArrayType, self).__init__(name=
            'ArrayItemArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return ArrayItemArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class ArrayItemArrayPayloadType(types.Type):

    def __init__(self, array_type):
        self.array_type = array_type
        super(ArrayItemArrayPayloadType, self).__init__(name=
            'ArrayItemArrayPayloadType({})'.format(array_type))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(ArrayItemArrayPayloadType)
class ArrayItemArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        enn__pskhp = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, enn__pskhp)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        enn__pskhp = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, enn__pskhp)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    qzm__fokdp = builder.module
    rwdp__lgh = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    scc__ica = cgutils.get_or_insert_function(qzm__fokdp, rwdp__lgh, name=
        '.dtor.array_item.{}'.format(array_item_type.dtype))
    if not scc__ica.is_declaration:
        return scc__ica
    scc__ica.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(scc__ica.append_basic_block())
    zicub__eqee = scc__ica.args[0]
    kixv__xhlsk = context.get_value_type(payload_type).as_pointer()
    hllfr__seocu = builder.bitcast(zicub__eqee, kixv__xhlsk)
    xmfh__tof = context.make_helper(builder, payload_type, ref=hllfr__seocu)
    context.nrt.decref(builder, array_item_type.dtype, xmfh__tof.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), xmfh__tof
        .offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), xmfh__tof
        .null_bitmap)
    builder.ret_void()
    return scc__ica


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    xmvco__euf = context.get_value_type(payload_type)
    hpac__dgkv = context.get_abi_sizeof(xmvco__euf)
    mzzwo__wps = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    saz__ihdx = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, hpac__dgkv), mzzwo__wps)
    nvo__zrh = context.nrt.meminfo_data(builder, saz__ihdx)
    toqcv__hckcb = builder.bitcast(nvo__zrh, xmvco__euf.as_pointer())
    xmfh__tof = cgutils.create_struct_proxy(payload_type)(context, builder)
    xmfh__tof.n_arrays = n_arrays
    lqs__kln = n_elems.type.count
    daa__dytq = builder.extract_value(n_elems, 0)
    suixe__apt = cgutils.alloca_once_value(builder, daa__dytq)
    cxbpi__cex = builder.icmp_signed('==', daa__dytq, lir.Constant(
        daa__dytq.type, -1))
    with builder.if_then(cxbpi__cex):
        builder.store(n_arrays, suixe__apt)
    n_elems = cgutils.pack_array(builder, [builder.load(suixe__apt)] + [
        builder.extract_value(n_elems, bbz__kqsw) for bbz__kqsw in range(1,
        lqs__kln)])
    xmfh__tof.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    gejtf__xabzm = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    nnjyt__tnj = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [gejtf__xabzm])
    offsets_ptr = nnjyt__tnj.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    xmfh__tof.offsets = nnjyt__tnj._getvalue()
    mls__rsfl = builder.udiv(builder.add(n_arrays, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    sxdb__gfmmc = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [mls__rsfl])
    null_bitmap_ptr = sxdb__gfmmc.data
    xmfh__tof.null_bitmap = sxdb__gfmmc._getvalue()
    builder.store(xmfh__tof._getvalue(), toqcv__hckcb)
    return saz__ihdx, xmfh__tof.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    zthy__vjdx, yhjxj__gpciq = c.pyapi.call_jit_code(copy_data, sig, [
        data_arr, item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    lld__hljs = context.insert_const_string(builder.module, 'pandas')
    vrff__hemj = c.pyapi.import_module_noblock(lld__hljs)
    qts__ihu = c.pyapi.object_getattr_string(vrff__hemj, 'NA')
    nbors__dvrqo = c.context.get_constant(offset_type, 0)
    builder.store(nbors__dvrqo, offsets_ptr)
    veed__yfb = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as ofn__ebun:
        nrzed__xab = ofn__ebun.index
        item_ind = builder.load(veed__yfb)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [nrzed__xab]))
        arr_obj = seq_getitem(builder, context, val, nrzed__xab)
        set_bitmap_bit(builder, null_bitmap_ptr, nrzed__xab, 0)
        uuubx__zpzgg = is_na_value(builder, context, arr_obj, qts__ihu)
        ydp__dvntt = builder.icmp_unsigned('!=', uuubx__zpzgg, lir.Constant
            (uuubx__zpzgg.type, 1))
        with builder.if_then(ydp__dvntt):
            set_bitmap_bit(builder, null_bitmap_ptr, nrzed__xab, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), veed__yfb)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(veed__yfb), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(vrff__hemj)
    c.pyapi.decref(qts__ihu)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    igcj__nmro = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if igcj__nmro:
        rwdp__lgh = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        xmhk__wbfz = cgutils.get_or_insert_function(c.builder.module,
            rwdp__lgh, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(xmhk__wbfz,
            [val])])
    else:
        ogwws__psrcu = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            ogwws__psrcu, bbz__kqsw) for bbz__kqsw in range(1, ogwws__psrcu
            .type.count)])
    saz__ihdx, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if igcj__nmro:
        txfh__xiqr = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        yms__vya = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        rwdp__lgh = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        scc__ica = cgutils.get_or_insert_function(c.builder.module,
            rwdp__lgh, name='array_item_array_from_sequence')
        c.builder.call(scc__ica, [val, c.builder.bitcast(yms__vya, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), txfh__xiqr)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    qmbn__zcama = c.context.make_helper(c.builder, typ)
    qmbn__zcama.meminfo = saz__ihdx
    cpqbe__vbaed = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qmbn__zcama._getvalue(), is_error=cpqbe__vbaed)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    qmbn__zcama = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    nvo__zrh = context.nrt.meminfo_data(builder, qmbn__zcama.meminfo)
    toqcv__hckcb = builder.bitcast(nvo__zrh, context.get_value_type(
        payload_type).as_pointer())
    xmfh__tof = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(toqcv__hckcb))
    return xmfh__tof


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    lld__hljs = context.insert_const_string(builder.module, 'numpy')
    yvbc__fclg = c.pyapi.import_module_noblock(lld__hljs)
    vrdco__puq = c.pyapi.object_getattr_string(yvbc__fclg, 'object_')
    nfxn__uabdw = c.pyapi.long_from_longlong(n_arrays)
    kkcn__scnak = c.pyapi.call_method(yvbc__fclg, 'ndarray', (nfxn__uabdw,
        vrdco__puq))
    qaes__eyv = c.pyapi.object_getattr_string(yvbc__fclg, 'nan')
    veed__yfb = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_arrays) as ofn__ebun:
        nrzed__xab = ofn__ebun.index
        pyarray_setitem(builder, context, kkcn__scnak, nrzed__xab, qaes__eyv)
        kkf__sotcz = get_bitmap_bit(builder, null_bitmap_ptr, nrzed__xab)
        jvsy__qynrc = builder.icmp_unsigned('!=', kkf__sotcz, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(jvsy__qynrc):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(nrzed__xab, lir.Constant(
                nrzed__xab.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [nrzed__xab]))), lir.IntType(64))
            item_ind = builder.load(veed__yfb)
            zthy__vjdx, xyfxe__yccjs = c.pyapi.call_jit_code(lambda
                data_arr, item_ind, n_items: data_arr[item_ind:item_ind +
                n_items], typ.dtype(typ.dtype, types.int64, types.int64), [
                data_arr, item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), veed__yfb)
            arr_obj = c.pyapi.from_native_value(typ.dtype, xyfxe__yccjs, c.
                env_manager)
            pyarray_setitem(builder, context, kkcn__scnak, nrzed__xab, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(yvbc__fclg)
    c.pyapi.decref(vrdco__puq)
    c.pyapi.decref(nfxn__uabdw)
    c.pyapi.decref(qaes__eyv)
    return kkcn__scnak


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    xmfh__tof = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = xmfh__tof.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), xmfh__tof.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), xmfh__tof.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        txfh__xiqr = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        yms__vya = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        rwdp__lgh = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        pmoc__iwd = cgutils.get_or_insert_function(c.builder.module,
            rwdp__lgh, name='np_array_from_array_item_array')
        arr = c.builder.call(pmoc__iwd, [xmfh__tof.n_arrays, c.builder.
            bitcast(yms__vya, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), txfh__xiqr)])
    else:
        arr = _box_array_item_array_generic(typ, c, xmfh__tof.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    wabps__iwq, swlwe__kztl, scxpc__mmek = args
    chbj__whyz = bodo.utils.transform.get_type_alloc_counts(array_item_type
        .dtype)
    bwo__cpy = sig.args[1]
    if not isinstance(bwo__cpy, types.UniTuple):
        swlwe__kztl = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), -1) for scxpc__mmek in range(chbj__whyz)])
    elif bwo__cpy.count < chbj__whyz:
        swlwe__kztl = cgutils.pack_array(builder, [builder.extract_value(
            swlwe__kztl, bbz__kqsw) for bbz__kqsw in range(bwo__cpy.count)] +
            [lir.Constant(lir.IntType(64), -1) for scxpc__mmek in range(
            chbj__whyz - bwo__cpy.count)])
    saz__ihdx, scxpc__mmek, scxpc__mmek, scxpc__mmek = (
        construct_array_item_array(context, builder, array_item_type,
        wabps__iwq, swlwe__kztl))
    qmbn__zcama = context.make_helper(builder, array_item_type)
    qmbn__zcama.meminfo = saz__ihdx
    return qmbn__zcama._getvalue()


@intrinsic
def pre_alloc_array_item_array(typingctx, num_arrs_typ, num_values_typ,
    dtype_typ=None):
    assert isinstance(num_arrs_typ, types.Integer)
    array_item_type = ArrayItemArrayType(dtype_typ.instance_type)
    num_values_typ = types.unliteral(num_values_typ)
    return array_item_type(types.int64, num_values_typ, dtype_typ
        ), lower_pre_alloc_array_item_array


def pre_alloc_array_item_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_array_item_arr_ext_pre_alloc_array_item_array
    ) = pre_alloc_array_item_array_equiv


def init_array_item_array_codegen(context, builder, signature, args):
    n_arrays, jcun__owdo, nnjyt__tnj, sxdb__gfmmc = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    xmvco__euf = context.get_value_type(payload_type)
    hpac__dgkv = context.get_abi_sizeof(xmvco__euf)
    mzzwo__wps = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    saz__ihdx = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, hpac__dgkv), mzzwo__wps)
    nvo__zrh = context.nrt.meminfo_data(builder, saz__ihdx)
    toqcv__hckcb = builder.bitcast(nvo__zrh, xmvco__euf.as_pointer())
    xmfh__tof = cgutils.create_struct_proxy(payload_type)(context, builder)
    xmfh__tof.n_arrays = n_arrays
    xmfh__tof.data = jcun__owdo
    xmfh__tof.offsets = nnjyt__tnj
    xmfh__tof.null_bitmap = sxdb__gfmmc
    builder.store(xmfh__tof._getvalue(), toqcv__hckcb)
    context.nrt.incref(builder, signature.args[1], jcun__owdo)
    context.nrt.incref(builder, signature.args[2], nnjyt__tnj)
    context.nrt.incref(builder, signature.args[3], sxdb__gfmmc)
    qmbn__zcama = context.make_helper(builder, array_item_type)
    qmbn__zcama.meminfo = saz__ihdx
    return qmbn__zcama._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    xahlq__mhj = ArrayItemArrayType(data_type)
    sig = xahlq__mhj(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xmfh__tof = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xmfh__tof.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        xmfh__tof = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        yms__vya = context.make_array(types.Array(offset_type, 1, 'C'))(context
            , builder, xmfh__tof.offsets).data
        nnjyt__tnj = builder.bitcast(yms__vya, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(nnjyt__tnj, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xmfh__tof = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xmfh__tof.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xmfh__tof = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xmfh__tof.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


def alias_ext_single_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_offsets',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_data',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_null_bitmap',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array


@intrinsic
def get_n_arrays(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xmfh__tof = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return xmfh__tof.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, hvxwm__wlba = args
        qmbn__zcama = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        nvo__zrh = context.nrt.meminfo_data(builder, qmbn__zcama.meminfo)
        toqcv__hckcb = builder.bitcast(nvo__zrh, context.get_value_type(
            payload_type).as_pointer())
        xmfh__tof = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(toqcv__hckcb))
        context.nrt.decref(builder, data_typ, xmfh__tof.data)
        xmfh__tof.data = hvxwm__wlba
        context.nrt.incref(builder, data_typ, hvxwm__wlba)
        builder.store(xmfh__tof._getvalue(), toqcv__hckcb)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    jcun__owdo = get_data(arr)
    yqaq__bwbgt = len(jcun__owdo)
    if yqaq__bwbgt < new_size:
        xkfta__smjc = max(2 * yqaq__bwbgt, new_size)
        hvxwm__wlba = bodo.libs.array_kernels.resize_and_copy(jcun__owdo,
            old_size, xkfta__smjc)
        replace_data_arr(arr, hvxwm__wlba)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    jcun__owdo = get_data(arr)
    nnjyt__tnj = get_offsets(arr)
    xfbo__nfpza = len(jcun__owdo)
    wtg__zqc = nnjyt__tnj[-1]
    if xfbo__nfpza != wtg__zqc:
        hvxwm__wlba = bodo.libs.array_kernels.resize_and_copy(jcun__owdo,
            wtg__zqc, wtg__zqc)
        replace_data_arr(arr, hvxwm__wlba)


@overload(len, no_unliteral=True)
def overload_array_item_arr_len(A):
    if isinstance(A, ArrayItemArrayType):
        return lambda A: get_n_arrays(A)


@overload_attribute(ArrayItemArrayType, 'shape')
def overload_array_item_arr_shape(A):
    return lambda A: (get_n_arrays(A),)


@overload_attribute(ArrayItemArrayType, 'dtype')
def overload_array_item_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(ArrayItemArrayType, 'ndim')
def overload_array_item_arr_ndim(A):
    return lambda A: 1


@overload_attribute(ArrayItemArrayType, 'nbytes')
def overload_array_item_arr_nbytes(A):
    return lambda A: get_data(A).nbytes + get_offsets(A
        ).nbytes + get_null_bitmap(A).nbytes


@overload(operator.getitem, no_unliteral=True)
def array_item_arr_getitem_array(arr, ind):
    if not isinstance(arr, ArrayItemArrayType):
        return
    if isinstance(ind, types.Integer):

        def array_item_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            nnjyt__tnj = get_offsets(arr)
            jcun__owdo = get_data(arr)
            irkf__vpz = nnjyt__tnj[ind]
            vgya__edrh = nnjyt__tnj[ind + 1]
            return jcun__owdo[irkf__vpz:vgya__edrh]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        zugx__ncxdr = arr.dtype

        def impl_bool(arr, ind):
            jlfqy__wufb = len(arr)
            if jlfqy__wufb != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            sxdb__gfmmc = get_null_bitmap(arr)
            n_arrays = 0
            kec__xblw = init_nested_counts(zugx__ncxdr)
            for bbz__kqsw in range(jlfqy__wufb):
                if ind[bbz__kqsw]:
                    n_arrays += 1
                    kytoe__kdxqc = arr[bbz__kqsw]
                    kec__xblw = add_nested_counts(kec__xblw, kytoe__kdxqc)
            kkcn__scnak = pre_alloc_array_item_array(n_arrays, kec__xblw,
                zugx__ncxdr)
            eucd__gxny = get_null_bitmap(kkcn__scnak)
            njf__hcj = 0
            for zbwuc__lga in range(jlfqy__wufb):
                if ind[zbwuc__lga]:
                    kkcn__scnak[njf__hcj] = arr[zbwuc__lga]
                    qwyh__jtmmw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        sxdb__gfmmc, zbwuc__lga)
                    bodo.libs.int_arr_ext.set_bit_to_arr(eucd__gxny,
                        njf__hcj, qwyh__jtmmw)
                    njf__hcj += 1
            return kkcn__scnak
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        zugx__ncxdr = arr.dtype

        def impl_int(arr, ind):
            sxdb__gfmmc = get_null_bitmap(arr)
            jlfqy__wufb = len(ind)
            n_arrays = jlfqy__wufb
            kec__xblw = init_nested_counts(zugx__ncxdr)
            for oabks__ypzeb in range(jlfqy__wufb):
                bbz__kqsw = ind[oabks__ypzeb]
                kytoe__kdxqc = arr[bbz__kqsw]
                kec__xblw = add_nested_counts(kec__xblw, kytoe__kdxqc)
            kkcn__scnak = pre_alloc_array_item_array(n_arrays, kec__xblw,
                zugx__ncxdr)
            eucd__gxny = get_null_bitmap(kkcn__scnak)
            for ttk__gpuzz in range(jlfqy__wufb):
                zbwuc__lga = ind[ttk__gpuzz]
                kkcn__scnak[ttk__gpuzz] = arr[zbwuc__lga]
                qwyh__jtmmw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    sxdb__gfmmc, zbwuc__lga)
                bodo.libs.int_arr_ext.set_bit_to_arr(eucd__gxny, ttk__gpuzz,
                    qwyh__jtmmw)
            return kkcn__scnak
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            jlfqy__wufb = len(arr)
            eeang__rtmdb = numba.cpython.unicode._normalize_slice(ind,
                jlfqy__wufb)
            whznd__odion = np.arange(eeang__rtmdb.start, eeang__rtmdb.stop,
                eeang__rtmdb.step)
            return arr[whznd__odion]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            nnjyt__tnj = get_offsets(A)
            sxdb__gfmmc = get_null_bitmap(A)
            if idx == 0:
                nnjyt__tnj[0] = 0
            n_items = len(val)
            kbl__rshri = nnjyt__tnj[idx] + n_items
            ensure_data_capacity(A, nnjyt__tnj[idx], kbl__rshri)
            jcun__owdo = get_data(A)
            nnjyt__tnj[idx + 1] = nnjyt__tnj[idx] + n_items
            jcun__owdo[nnjyt__tnj[idx]:nnjyt__tnj[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(sxdb__gfmmc, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            eeang__rtmdb = numba.cpython.unicode._normalize_slice(idx, len(A))
            for bbz__kqsw in range(eeang__rtmdb.start, eeang__rtmdb.stop,
                eeang__rtmdb.step):
                A[bbz__kqsw] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            nnjyt__tnj = get_offsets(A)
            sxdb__gfmmc = get_null_bitmap(A)
            mhz__npq = get_offsets(val)
            iddbd__eghm = get_data(val)
            wnf__cbq = get_null_bitmap(val)
            jlfqy__wufb = len(A)
            eeang__rtmdb = numba.cpython.unicode._normalize_slice(idx,
                jlfqy__wufb)
            xep__wdilh, saib__psc = eeang__rtmdb.start, eeang__rtmdb.stop
            assert eeang__rtmdb.step == 1
            if xep__wdilh == 0:
                nnjyt__tnj[xep__wdilh] = 0
            ueqj__ugolu = nnjyt__tnj[xep__wdilh]
            kbl__rshri = ueqj__ugolu + len(iddbd__eghm)
            ensure_data_capacity(A, ueqj__ugolu, kbl__rshri)
            jcun__owdo = get_data(A)
            jcun__owdo[ueqj__ugolu:ueqj__ugolu + len(iddbd__eghm)
                ] = iddbd__eghm
            nnjyt__tnj[xep__wdilh:saib__psc + 1] = mhz__npq + ueqj__ugolu
            xhn__xrk = 0
            for bbz__kqsw in range(xep__wdilh, saib__psc):
                qwyh__jtmmw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(wnf__cbq
                    , xhn__xrk)
                bodo.libs.int_arr_ext.set_bit_to_arr(sxdb__gfmmc, bbz__kqsw,
                    qwyh__jtmmw)
                xhn__xrk += 1
        return impl_slice
    raise BodoError(
        'only setitem with scalar index is currently supported for list arrays'
        )


@overload_method(ArrayItemArrayType, 'copy', no_unliteral=True)
def overload_array_item_arr_copy(A):

    def copy_impl(A):
        return init_array_item_array(len(A), get_data(A).copy(),
            get_offsets(A).copy(), get_null_bitmap(A).copy())
    return copy_impl
