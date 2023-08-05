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
        xmmao__ipl = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, xmmao__ipl)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        xmmao__ipl = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, xmmao__ipl)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    wal__pkl = builder.module
    fsdp__qennh = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    oaig__zshbr = cgutils.get_or_insert_function(wal__pkl, fsdp__qennh,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not oaig__zshbr.is_declaration:
        return oaig__zshbr
    oaig__zshbr.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(oaig__zshbr.append_basic_block())
    kzgzr__nfr = oaig__zshbr.args[0]
    lwdto__fghtl = context.get_value_type(payload_type).as_pointer()
    wyzg__fgpqk = builder.bitcast(kzgzr__nfr, lwdto__fghtl)
    flc__nnlp = context.make_helper(builder, payload_type, ref=wyzg__fgpqk)
    context.nrt.decref(builder, array_item_type.dtype, flc__nnlp.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), flc__nnlp
        .offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), flc__nnlp
        .null_bitmap)
    builder.ret_void()
    return oaig__zshbr


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    sbkc__cjir = context.get_value_type(payload_type)
    rps__leab = context.get_abi_sizeof(sbkc__cjir)
    qtao__sdi = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    qlqi__kru = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, rps__leab), qtao__sdi)
    xmq__gdv = context.nrt.meminfo_data(builder, qlqi__kru)
    oxmt__yuxnd = builder.bitcast(xmq__gdv, sbkc__cjir.as_pointer())
    flc__nnlp = cgutils.create_struct_proxy(payload_type)(context, builder)
    flc__nnlp.n_arrays = n_arrays
    xhfle__icxak = n_elems.type.count
    btlgr__iuevl = builder.extract_value(n_elems, 0)
    whjv__omwu = cgutils.alloca_once_value(builder, btlgr__iuevl)
    tyae__deas = builder.icmp_signed('==', btlgr__iuevl, lir.Constant(
        btlgr__iuevl.type, -1))
    with builder.if_then(tyae__deas):
        builder.store(n_arrays, whjv__omwu)
    n_elems = cgutils.pack_array(builder, [builder.load(whjv__omwu)] + [
        builder.extract_value(n_elems, fsjc__jnyha) for fsjc__jnyha in
        range(1, xhfle__icxak)])
    flc__nnlp.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    xunu__mqwlj = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    dgirl__yziz = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [xunu__mqwlj])
    offsets_ptr = dgirl__yziz.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    flc__nnlp.offsets = dgirl__yziz._getvalue()
    bgj__vous = builder.udiv(builder.add(n_arrays, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    lqn__bdh = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [bgj__vous])
    null_bitmap_ptr = lqn__bdh.data
    flc__nnlp.null_bitmap = lqn__bdh._getvalue()
    builder.store(flc__nnlp._getvalue(), oxmt__yuxnd)
    return qlqi__kru, flc__nnlp.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    paj__czalb, bjgo__qax = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    tebzk__fxup = context.insert_const_string(builder.module, 'pandas')
    ylzxs__csrj = c.pyapi.import_module_noblock(tebzk__fxup)
    fwg__ygfwu = c.pyapi.object_getattr_string(ylzxs__csrj, 'NA')
    npfx__otoks = c.context.get_constant(offset_type, 0)
    builder.store(npfx__otoks, offsets_ptr)
    use__omm = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as qgjn__fssri:
        fstty__xets = qgjn__fssri.index
        item_ind = builder.load(use__omm)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [fstty__xets]))
        arr_obj = seq_getitem(builder, context, val, fstty__xets)
        set_bitmap_bit(builder, null_bitmap_ptr, fstty__xets, 0)
        jlwmq__iaxu = is_na_value(builder, context, arr_obj, fwg__ygfwu)
        ooq__jnchr = builder.icmp_unsigned('!=', jlwmq__iaxu, lir.Constant(
            jlwmq__iaxu.type, 1))
        with builder.if_then(ooq__jnchr):
            set_bitmap_bit(builder, null_bitmap_ptr, fstty__xets, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), use__omm)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(use__omm), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(ylzxs__csrj)
    c.pyapi.decref(fwg__ygfwu)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    sik__esl = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types
        .int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if sik__esl:
        fsdp__qennh = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        iogjn__ygxh = cgutils.get_or_insert_function(c.builder.module,
            fsdp__qennh, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(iogjn__ygxh,
            [val])])
    else:
        hwnyl__pna = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            hwnyl__pna, fsjc__jnyha) for fsjc__jnyha in range(1, hwnyl__pna
            .type.count)])
    qlqi__kru, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if sik__esl:
        biyh__nzq = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        jto__gaecb = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        fsdp__qennh = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        oaig__zshbr = cgutils.get_or_insert_function(c.builder.module,
            fsdp__qennh, name='array_item_array_from_sequence')
        c.builder.call(oaig__zshbr, [val, c.builder.bitcast(jto__gaecb, lir
            .IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), biyh__nzq)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    awzwu__hlak = c.context.make_helper(c.builder, typ)
    awzwu__hlak.meminfo = qlqi__kru
    zpmv__kmpo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(awzwu__hlak._getvalue(), is_error=zpmv__kmpo)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    awzwu__hlak = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    xmq__gdv = context.nrt.meminfo_data(builder, awzwu__hlak.meminfo)
    oxmt__yuxnd = builder.bitcast(xmq__gdv, context.get_value_type(
        payload_type).as_pointer())
    flc__nnlp = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(oxmt__yuxnd))
    return flc__nnlp


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    tebzk__fxup = context.insert_const_string(builder.module, 'numpy')
    sois__wev = c.pyapi.import_module_noblock(tebzk__fxup)
    thkyz__ydg = c.pyapi.object_getattr_string(sois__wev, 'object_')
    llxva__gma = c.pyapi.long_from_longlong(n_arrays)
    jkfmr__ckqe = c.pyapi.call_method(sois__wev, 'ndarray', (llxva__gma,
        thkyz__ydg))
    gsib__jgptn = c.pyapi.object_getattr_string(sois__wev, 'nan')
    use__omm = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType(
        64), 0))
    with cgutils.for_range(builder, n_arrays) as qgjn__fssri:
        fstty__xets = qgjn__fssri.index
        pyarray_setitem(builder, context, jkfmr__ckqe, fstty__xets, gsib__jgptn
            )
        iegzk__fownq = get_bitmap_bit(builder, null_bitmap_ptr, fstty__xets)
        zsiow__duj = builder.icmp_unsigned('!=', iegzk__fownq, lir.Constant
            (lir.IntType(8), 0))
        with builder.if_then(zsiow__duj):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(fstty__xets, lir.Constant(
                fstty__xets.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [fstty__xets]))), lir.IntType(64))
            item_ind = builder.load(use__omm)
            paj__czalb, ihmc__dvni = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), use__omm)
            arr_obj = c.pyapi.from_native_value(typ.dtype, ihmc__dvni, c.
                env_manager)
            pyarray_setitem(builder, context, jkfmr__ckqe, fstty__xets, arr_obj
                )
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(sois__wev)
    c.pyapi.decref(thkyz__ydg)
    c.pyapi.decref(llxva__gma)
    c.pyapi.decref(gsib__jgptn)
    return jkfmr__ckqe


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    flc__nnlp = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = flc__nnlp.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), flc__nnlp.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), flc__nnlp.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        biyh__nzq = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        jto__gaecb = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        fsdp__qennh = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        tlxo__bjp = cgutils.get_or_insert_function(c.builder.module,
            fsdp__qennh, name='np_array_from_array_item_array')
        arr = c.builder.call(tlxo__bjp, [flc__nnlp.n_arrays, c.builder.
            bitcast(jto__gaecb, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), biyh__nzq)])
    else:
        arr = _box_array_item_array_generic(typ, c, flc__nnlp.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    wxpyc__wlruz, zurid__kcz, fzlt__ujkrv = args
    mgwm__gnx = bodo.utils.transform.get_type_alloc_counts(array_item_type.
        dtype)
    hke__wrqka = sig.args[1]
    if not isinstance(hke__wrqka, types.UniTuple):
        zurid__kcz = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for fzlt__ujkrv in range(mgwm__gnx)])
    elif hke__wrqka.count < mgwm__gnx:
        zurid__kcz = cgutils.pack_array(builder, [builder.extract_value(
            zurid__kcz, fsjc__jnyha) for fsjc__jnyha in range(hke__wrqka.
            count)] + [lir.Constant(lir.IntType(64), -1) for fzlt__ujkrv in
            range(mgwm__gnx - hke__wrqka.count)])
    qlqi__kru, fzlt__ujkrv, fzlt__ujkrv, fzlt__ujkrv = (
        construct_array_item_array(context, builder, array_item_type,
        wxpyc__wlruz, zurid__kcz))
    awzwu__hlak = context.make_helper(builder, array_item_type)
    awzwu__hlak.meminfo = qlqi__kru
    return awzwu__hlak._getvalue()


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
    n_arrays, jptb__okhm, dgirl__yziz, lqn__bdh = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    sbkc__cjir = context.get_value_type(payload_type)
    rps__leab = context.get_abi_sizeof(sbkc__cjir)
    qtao__sdi = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    qlqi__kru = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, rps__leab), qtao__sdi)
    xmq__gdv = context.nrt.meminfo_data(builder, qlqi__kru)
    oxmt__yuxnd = builder.bitcast(xmq__gdv, sbkc__cjir.as_pointer())
    flc__nnlp = cgutils.create_struct_proxy(payload_type)(context, builder)
    flc__nnlp.n_arrays = n_arrays
    flc__nnlp.data = jptb__okhm
    flc__nnlp.offsets = dgirl__yziz
    flc__nnlp.null_bitmap = lqn__bdh
    builder.store(flc__nnlp._getvalue(), oxmt__yuxnd)
    context.nrt.incref(builder, signature.args[1], jptb__okhm)
    context.nrt.incref(builder, signature.args[2], dgirl__yziz)
    context.nrt.incref(builder, signature.args[3], lqn__bdh)
    awzwu__hlak = context.make_helper(builder, array_item_type)
    awzwu__hlak.meminfo = qlqi__kru
    return awzwu__hlak._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    fypqm__vxj = ArrayItemArrayType(data_type)
    sig = fypqm__vxj(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        flc__nnlp = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            flc__nnlp.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        flc__nnlp = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        jto__gaecb = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, flc__nnlp.offsets).data
        dgirl__yziz = builder.bitcast(jto__gaecb, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(dgirl__yziz, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        flc__nnlp = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            flc__nnlp.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        flc__nnlp = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            flc__nnlp.null_bitmap)
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
        flc__nnlp = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return flc__nnlp.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, pwqq__eur = args
        awzwu__hlak = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        xmq__gdv = context.nrt.meminfo_data(builder, awzwu__hlak.meminfo)
        oxmt__yuxnd = builder.bitcast(xmq__gdv, context.get_value_type(
            payload_type).as_pointer())
        flc__nnlp = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(oxmt__yuxnd))
        context.nrt.decref(builder, data_typ, flc__nnlp.data)
        flc__nnlp.data = pwqq__eur
        context.nrt.incref(builder, data_typ, pwqq__eur)
        builder.store(flc__nnlp._getvalue(), oxmt__yuxnd)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    jptb__okhm = get_data(arr)
    uhjjn__flftb = len(jptb__okhm)
    if uhjjn__flftb < new_size:
        dmmg__sxm = max(2 * uhjjn__flftb, new_size)
        pwqq__eur = bodo.libs.array_kernels.resize_and_copy(jptb__okhm,
            old_size, dmmg__sxm)
        replace_data_arr(arr, pwqq__eur)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    jptb__okhm = get_data(arr)
    dgirl__yziz = get_offsets(arr)
    lqa__hqki = len(jptb__okhm)
    ivsm__jma = dgirl__yziz[-1]
    if lqa__hqki != ivsm__jma:
        pwqq__eur = bodo.libs.array_kernels.resize_and_copy(jptb__okhm,
            ivsm__jma, ivsm__jma)
        replace_data_arr(arr, pwqq__eur)


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
            dgirl__yziz = get_offsets(arr)
            jptb__okhm = get_data(arr)
            jzxds__ehb = dgirl__yziz[ind]
            hcq__pbp = dgirl__yziz[ind + 1]
            return jptb__okhm[jzxds__ehb:hcq__pbp]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        omif__fzu = arr.dtype

        def impl_bool(arr, ind):
            dkbaa__ylaxu = len(arr)
            if dkbaa__ylaxu != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            lqn__bdh = get_null_bitmap(arr)
            n_arrays = 0
            snlzr__uip = init_nested_counts(omif__fzu)
            for fsjc__jnyha in range(dkbaa__ylaxu):
                if ind[fsjc__jnyha]:
                    n_arrays += 1
                    zzydr__ljhz = arr[fsjc__jnyha]
                    snlzr__uip = add_nested_counts(snlzr__uip, zzydr__ljhz)
            jkfmr__ckqe = pre_alloc_array_item_array(n_arrays, snlzr__uip,
                omif__fzu)
            lib__urna = get_null_bitmap(jkfmr__ckqe)
            fmc__zoy = 0
            for ohp__pggv in range(dkbaa__ylaxu):
                if ind[ohp__pggv]:
                    jkfmr__ckqe[fmc__zoy] = arr[ohp__pggv]
                    ldsm__pze = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        lqn__bdh, ohp__pggv)
                    bodo.libs.int_arr_ext.set_bit_to_arr(lib__urna,
                        fmc__zoy, ldsm__pze)
                    fmc__zoy += 1
            return jkfmr__ckqe
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        omif__fzu = arr.dtype

        def impl_int(arr, ind):
            lqn__bdh = get_null_bitmap(arr)
            dkbaa__ylaxu = len(ind)
            n_arrays = dkbaa__ylaxu
            snlzr__uip = init_nested_counts(omif__fzu)
            for zuxi__vec in range(dkbaa__ylaxu):
                fsjc__jnyha = ind[zuxi__vec]
                zzydr__ljhz = arr[fsjc__jnyha]
                snlzr__uip = add_nested_counts(snlzr__uip, zzydr__ljhz)
            jkfmr__ckqe = pre_alloc_array_item_array(n_arrays, snlzr__uip,
                omif__fzu)
            lib__urna = get_null_bitmap(jkfmr__ckqe)
            for ouxyc__aky in range(dkbaa__ylaxu):
                ohp__pggv = ind[ouxyc__aky]
                jkfmr__ckqe[ouxyc__aky] = arr[ohp__pggv]
                ldsm__pze = bodo.libs.int_arr_ext.get_bit_bitmap_arr(lqn__bdh,
                    ohp__pggv)
                bodo.libs.int_arr_ext.set_bit_to_arr(lib__urna, ouxyc__aky,
                    ldsm__pze)
            return jkfmr__ckqe
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            dkbaa__ylaxu = len(arr)
            qkmrz__jto = numba.cpython.unicode._normalize_slice(ind,
                dkbaa__ylaxu)
            winne__bmev = np.arange(qkmrz__jto.start, qkmrz__jto.stop,
                qkmrz__jto.step)
            return arr[winne__bmev]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            dgirl__yziz = get_offsets(A)
            lqn__bdh = get_null_bitmap(A)
            if idx == 0:
                dgirl__yziz[0] = 0
            n_items = len(val)
            akfy__ozav = dgirl__yziz[idx] + n_items
            ensure_data_capacity(A, dgirl__yziz[idx], akfy__ozav)
            jptb__okhm = get_data(A)
            dgirl__yziz[idx + 1] = dgirl__yziz[idx] + n_items
            jptb__okhm[dgirl__yziz[idx]:dgirl__yziz[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(lqn__bdh, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            qkmrz__jto = numba.cpython.unicode._normalize_slice(idx, len(A))
            for fsjc__jnyha in range(qkmrz__jto.start, qkmrz__jto.stop,
                qkmrz__jto.step):
                A[fsjc__jnyha] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            dgirl__yziz = get_offsets(A)
            lqn__bdh = get_null_bitmap(A)
            gdym__anofv = get_offsets(val)
            iqs__xjxdq = get_data(val)
            xoyrp__pkur = get_null_bitmap(val)
            dkbaa__ylaxu = len(A)
            qkmrz__jto = numba.cpython.unicode._normalize_slice(idx,
                dkbaa__ylaxu)
            nsivy__jxws, dwr__tznoc = qkmrz__jto.start, qkmrz__jto.stop
            assert qkmrz__jto.step == 1
            if nsivy__jxws == 0:
                dgirl__yziz[nsivy__jxws] = 0
            epg__elg = dgirl__yziz[nsivy__jxws]
            akfy__ozav = epg__elg + len(iqs__xjxdq)
            ensure_data_capacity(A, epg__elg, akfy__ozav)
            jptb__okhm = get_data(A)
            jptb__okhm[epg__elg:epg__elg + len(iqs__xjxdq)] = iqs__xjxdq
            dgirl__yziz[nsivy__jxws:dwr__tznoc + 1] = gdym__anofv + epg__elg
            ompa__cevd = 0
            for fsjc__jnyha in range(nsivy__jxws, dwr__tznoc):
                ldsm__pze = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    xoyrp__pkur, ompa__cevd)
                bodo.libs.int_arr_ext.set_bit_to_arr(lqn__bdh, fsjc__jnyha,
                    ldsm__pze)
                ompa__cevd += 1
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
