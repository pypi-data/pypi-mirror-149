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
        tidzk__dym = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, tidzk__dym)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        tidzk__dym = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, tidzk__dym)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    xck__bbzdl = builder.module
    qfun__pkiep = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    afrf__xduf = cgutils.get_or_insert_function(xck__bbzdl, qfun__pkiep,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not afrf__xduf.is_declaration:
        return afrf__xduf
    afrf__xduf.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(afrf__xduf.append_basic_block())
    lnz__edv = afrf__xduf.args[0]
    rqcu__osugf = context.get_value_type(payload_type).as_pointer()
    zsnt__fhyy = builder.bitcast(lnz__edv, rqcu__osugf)
    ioeq__jvxvs = context.make_helper(builder, payload_type, ref=zsnt__fhyy)
    context.nrt.decref(builder, array_item_type.dtype, ioeq__jvxvs.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        ioeq__jvxvs.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        ioeq__jvxvs.null_bitmap)
    builder.ret_void()
    return afrf__xduf


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    yhyas__xxq = context.get_value_type(payload_type)
    xqbzt__inkc = context.get_abi_sizeof(yhyas__xxq)
    dcq__tteo = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    yybt__bdmf = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, xqbzt__inkc), dcq__tteo)
    rusb__ynro = context.nrt.meminfo_data(builder, yybt__bdmf)
    ezktq__gtef = builder.bitcast(rusb__ynro, yhyas__xxq.as_pointer())
    ioeq__jvxvs = cgutils.create_struct_proxy(payload_type)(context, builder)
    ioeq__jvxvs.n_arrays = n_arrays
    omi__jbtpn = n_elems.type.count
    lzwzj__tta = builder.extract_value(n_elems, 0)
    dmdi__pybg = cgutils.alloca_once_value(builder, lzwzj__tta)
    pbs__akzw = builder.icmp_signed('==', lzwzj__tta, lir.Constant(
        lzwzj__tta.type, -1))
    with builder.if_then(pbs__akzw):
        builder.store(n_arrays, dmdi__pybg)
    n_elems = cgutils.pack_array(builder, [builder.load(dmdi__pybg)] + [
        builder.extract_value(n_elems, vsdrk__dvxy) for vsdrk__dvxy in
        range(1, omi__jbtpn)])
    ioeq__jvxvs.data = gen_allocate_array(context, builder, array_item_type
        .dtype, n_elems, c)
    bdjku__nsd = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    ztvja__beeep = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [bdjku__nsd])
    offsets_ptr = ztvja__beeep.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    ioeq__jvxvs.offsets = ztvja__beeep._getvalue()
    jjlf__gsqa = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    gzwh__gdi = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [jjlf__gsqa])
    null_bitmap_ptr = gzwh__gdi.data
    ioeq__jvxvs.null_bitmap = gzwh__gdi._getvalue()
    builder.store(ioeq__jvxvs._getvalue(), ezktq__gtef)
    return yybt__bdmf, ioeq__jvxvs.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    nyn__jvd, qjo__czwl = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    sexjn__qjsf = context.insert_const_string(builder.module, 'pandas')
    bfsfc__ugv = c.pyapi.import_module_noblock(sexjn__qjsf)
    sqvy__ttqs = c.pyapi.object_getattr_string(bfsfc__ugv, 'NA')
    htwv__nezdu = c.context.get_constant(offset_type, 0)
    builder.store(htwv__nezdu, offsets_ptr)
    tdv__zpp = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as gbdq__flzg:
        orihj__lbv = gbdq__flzg.index
        item_ind = builder.load(tdv__zpp)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [orihj__lbv]))
        arr_obj = seq_getitem(builder, context, val, orihj__lbv)
        set_bitmap_bit(builder, null_bitmap_ptr, orihj__lbv, 0)
        sqfym__rbh = is_na_value(builder, context, arr_obj, sqvy__ttqs)
        ifuf__sjv = builder.icmp_unsigned('!=', sqfym__rbh, lir.Constant(
            sqfym__rbh.type, 1))
        with builder.if_then(ifuf__sjv):
            set_bitmap_bit(builder, null_bitmap_ptr, orihj__lbv, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), tdv__zpp)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(tdv__zpp), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(bfsfc__ugv)
    c.pyapi.decref(sqvy__ttqs)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    mtx__zkb = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types
        .int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if mtx__zkb:
        qfun__pkiep = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        zgxr__qlzjl = cgutils.get_or_insert_function(c.builder.module,
            qfun__pkiep, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(zgxr__qlzjl,
            [val])])
    else:
        ejs__gvihj = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            ejs__gvihj, vsdrk__dvxy) for vsdrk__dvxy in range(1, ejs__gvihj
            .type.count)])
    yybt__bdmf, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if mtx__zkb:
        jsm__xcxx = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ppw__qnq = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        qfun__pkiep = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        afrf__xduf = cgutils.get_or_insert_function(c.builder.module,
            qfun__pkiep, name='array_item_array_from_sequence')
        c.builder.call(afrf__xduf, [val, c.builder.bitcast(ppw__qnq, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), jsm__xcxx)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    sfku__evh = c.context.make_helper(c.builder, typ)
    sfku__evh.meminfo = yybt__bdmf
    eyuso__amnz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(sfku__evh._getvalue(), is_error=eyuso__amnz)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    sfku__evh = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    rusb__ynro = context.nrt.meminfo_data(builder, sfku__evh.meminfo)
    ezktq__gtef = builder.bitcast(rusb__ynro, context.get_value_type(
        payload_type).as_pointer())
    ioeq__jvxvs = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(ezktq__gtef))
    return ioeq__jvxvs


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    sexjn__qjsf = context.insert_const_string(builder.module, 'numpy')
    lihw__nrwpu = c.pyapi.import_module_noblock(sexjn__qjsf)
    mwgce__bxu = c.pyapi.object_getattr_string(lihw__nrwpu, 'object_')
    ttahd__tkha = c.pyapi.long_from_longlong(n_arrays)
    rjuim__eykcp = c.pyapi.call_method(lihw__nrwpu, 'ndarray', (ttahd__tkha,
        mwgce__bxu))
    smt__mfoa = c.pyapi.object_getattr_string(lihw__nrwpu, 'nan')
    tdv__zpp = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType(
        64), 0))
    with cgutils.for_range(builder, n_arrays) as gbdq__flzg:
        orihj__lbv = gbdq__flzg.index
        pyarray_setitem(builder, context, rjuim__eykcp, orihj__lbv, smt__mfoa)
        kca__iqd = get_bitmap_bit(builder, null_bitmap_ptr, orihj__lbv)
        kjorf__sbjvk = builder.icmp_unsigned('!=', kca__iqd, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(kjorf__sbjvk):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(orihj__lbv, lir.Constant(
                orihj__lbv.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [orihj__lbv]))), lir.IntType(64))
            item_ind = builder.load(tdv__zpp)
            nyn__jvd, kjz__wfd = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), tdv__zpp)
            arr_obj = c.pyapi.from_native_value(typ.dtype, kjz__wfd, c.
                env_manager)
            pyarray_setitem(builder, context, rjuim__eykcp, orihj__lbv, arr_obj
                )
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(lihw__nrwpu)
    c.pyapi.decref(mwgce__bxu)
    c.pyapi.decref(ttahd__tkha)
    c.pyapi.decref(smt__mfoa)
    return rjuim__eykcp


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    ioeq__jvxvs = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = ioeq__jvxvs.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), ioeq__jvxvs.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), ioeq__jvxvs.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        jsm__xcxx = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ppw__qnq = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        qfun__pkiep = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        klbea__evk = cgutils.get_or_insert_function(c.builder.module,
            qfun__pkiep, name='np_array_from_array_item_array')
        arr = c.builder.call(klbea__evk, [ioeq__jvxvs.n_arrays, c.builder.
            bitcast(ppw__qnq, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), jsm__xcxx)])
    else:
        arr = _box_array_item_array_generic(typ, c, ioeq__jvxvs.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    rud__gmtbz, yybth__xgxa, putw__ojbfb = args
    iwn__eyu = bodo.utils.transform.get_type_alloc_counts(array_item_type.dtype
        )
    qgch__qusjw = sig.args[1]
    if not isinstance(qgch__qusjw, types.UniTuple):
        yybth__xgxa = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), -1) for putw__ojbfb in range(iwn__eyu)])
    elif qgch__qusjw.count < iwn__eyu:
        yybth__xgxa = cgutils.pack_array(builder, [builder.extract_value(
            yybth__xgxa, vsdrk__dvxy) for vsdrk__dvxy in range(qgch__qusjw.
            count)] + [lir.Constant(lir.IntType(64), -1) for putw__ojbfb in
            range(iwn__eyu - qgch__qusjw.count)])
    yybt__bdmf, putw__ojbfb, putw__ojbfb, putw__ojbfb = (
        construct_array_item_array(context, builder, array_item_type,
        rud__gmtbz, yybth__xgxa))
    sfku__evh = context.make_helper(builder, array_item_type)
    sfku__evh.meminfo = yybt__bdmf
    return sfku__evh._getvalue()


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
    n_arrays, qzwz__hayyq, ztvja__beeep, gzwh__gdi = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    yhyas__xxq = context.get_value_type(payload_type)
    xqbzt__inkc = context.get_abi_sizeof(yhyas__xxq)
    dcq__tteo = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    yybt__bdmf = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, xqbzt__inkc), dcq__tteo)
    rusb__ynro = context.nrt.meminfo_data(builder, yybt__bdmf)
    ezktq__gtef = builder.bitcast(rusb__ynro, yhyas__xxq.as_pointer())
    ioeq__jvxvs = cgutils.create_struct_proxy(payload_type)(context, builder)
    ioeq__jvxvs.n_arrays = n_arrays
    ioeq__jvxvs.data = qzwz__hayyq
    ioeq__jvxvs.offsets = ztvja__beeep
    ioeq__jvxvs.null_bitmap = gzwh__gdi
    builder.store(ioeq__jvxvs._getvalue(), ezktq__gtef)
    context.nrt.incref(builder, signature.args[1], qzwz__hayyq)
    context.nrt.incref(builder, signature.args[2], ztvja__beeep)
    context.nrt.incref(builder, signature.args[3], gzwh__gdi)
    sfku__evh = context.make_helper(builder, array_item_type)
    sfku__evh.meminfo = yybt__bdmf
    return sfku__evh._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    zqz__satg = ArrayItemArrayType(data_type)
    sig = zqz__satg(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ioeq__jvxvs = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ioeq__jvxvs.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        ioeq__jvxvs = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        ppw__qnq = context.make_array(types.Array(offset_type, 1, 'C'))(context
            , builder, ioeq__jvxvs.offsets).data
        ztvja__beeep = builder.bitcast(ppw__qnq, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(ztvja__beeep, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ioeq__jvxvs = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ioeq__jvxvs.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ioeq__jvxvs = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ioeq__jvxvs.null_bitmap)
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
        ioeq__jvxvs = _get_array_item_arr_payload(context, builder, arr_typ,
            arr)
        return ioeq__jvxvs.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, lgkco__yaoij = args
        sfku__evh = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        rusb__ynro = context.nrt.meminfo_data(builder, sfku__evh.meminfo)
        ezktq__gtef = builder.bitcast(rusb__ynro, context.get_value_type(
            payload_type).as_pointer())
        ioeq__jvxvs = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(ezktq__gtef))
        context.nrt.decref(builder, data_typ, ioeq__jvxvs.data)
        ioeq__jvxvs.data = lgkco__yaoij
        context.nrt.incref(builder, data_typ, lgkco__yaoij)
        builder.store(ioeq__jvxvs._getvalue(), ezktq__gtef)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    qzwz__hayyq = get_data(arr)
    wkp__owbyf = len(qzwz__hayyq)
    if wkp__owbyf < new_size:
        euk__pbp = max(2 * wkp__owbyf, new_size)
        lgkco__yaoij = bodo.libs.array_kernels.resize_and_copy(qzwz__hayyq,
            old_size, euk__pbp)
        replace_data_arr(arr, lgkco__yaoij)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    qzwz__hayyq = get_data(arr)
    ztvja__beeep = get_offsets(arr)
    mgsg__jutga = len(qzwz__hayyq)
    vidvm__sxsy = ztvja__beeep[-1]
    if mgsg__jutga != vidvm__sxsy:
        lgkco__yaoij = bodo.libs.array_kernels.resize_and_copy(qzwz__hayyq,
            vidvm__sxsy, vidvm__sxsy)
        replace_data_arr(arr, lgkco__yaoij)


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
            ztvja__beeep = get_offsets(arr)
            qzwz__hayyq = get_data(arr)
            glds__dodoi = ztvja__beeep[ind]
            kokpr__hbtn = ztvja__beeep[ind + 1]
            return qzwz__hayyq[glds__dodoi:kokpr__hbtn]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        djrpv__raxu = arr.dtype

        def impl_bool(arr, ind):
            isryf__losk = len(arr)
            if isryf__losk != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            gzwh__gdi = get_null_bitmap(arr)
            n_arrays = 0
            xft__jtpmz = init_nested_counts(djrpv__raxu)
            for vsdrk__dvxy in range(isryf__losk):
                if ind[vsdrk__dvxy]:
                    n_arrays += 1
                    hod__xdulf = arr[vsdrk__dvxy]
                    xft__jtpmz = add_nested_counts(xft__jtpmz, hod__xdulf)
            rjuim__eykcp = pre_alloc_array_item_array(n_arrays, xft__jtpmz,
                djrpv__raxu)
            acpf__gzf = get_null_bitmap(rjuim__eykcp)
            yqv__xji = 0
            for ldoe__crhh in range(isryf__losk):
                if ind[ldoe__crhh]:
                    rjuim__eykcp[yqv__xji] = arr[ldoe__crhh]
                    ysjv__faa = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        gzwh__gdi, ldoe__crhh)
                    bodo.libs.int_arr_ext.set_bit_to_arr(acpf__gzf,
                        yqv__xji, ysjv__faa)
                    yqv__xji += 1
            return rjuim__eykcp
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        djrpv__raxu = arr.dtype

        def impl_int(arr, ind):
            gzwh__gdi = get_null_bitmap(arr)
            isryf__losk = len(ind)
            n_arrays = isryf__losk
            xft__jtpmz = init_nested_counts(djrpv__raxu)
            for bnjmo__gjog in range(isryf__losk):
                vsdrk__dvxy = ind[bnjmo__gjog]
                hod__xdulf = arr[vsdrk__dvxy]
                xft__jtpmz = add_nested_counts(xft__jtpmz, hod__xdulf)
            rjuim__eykcp = pre_alloc_array_item_array(n_arrays, xft__jtpmz,
                djrpv__raxu)
            acpf__gzf = get_null_bitmap(rjuim__eykcp)
            for bcri__qzuxq in range(isryf__losk):
                ldoe__crhh = ind[bcri__qzuxq]
                rjuim__eykcp[bcri__qzuxq] = arr[ldoe__crhh]
                ysjv__faa = bodo.libs.int_arr_ext.get_bit_bitmap_arr(gzwh__gdi,
                    ldoe__crhh)
                bodo.libs.int_arr_ext.set_bit_to_arr(acpf__gzf, bcri__qzuxq,
                    ysjv__faa)
            return rjuim__eykcp
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            isryf__losk = len(arr)
            oyk__xbwlz = numba.cpython.unicode._normalize_slice(ind,
                isryf__losk)
            sphol__ispko = np.arange(oyk__xbwlz.start, oyk__xbwlz.stop,
                oyk__xbwlz.step)
            return arr[sphol__ispko]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            ztvja__beeep = get_offsets(A)
            gzwh__gdi = get_null_bitmap(A)
            if idx == 0:
                ztvja__beeep[0] = 0
            n_items = len(val)
            qtddi__wral = ztvja__beeep[idx] + n_items
            ensure_data_capacity(A, ztvja__beeep[idx], qtddi__wral)
            qzwz__hayyq = get_data(A)
            ztvja__beeep[idx + 1] = ztvja__beeep[idx] + n_items
            qzwz__hayyq[ztvja__beeep[idx]:ztvja__beeep[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(gzwh__gdi, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            oyk__xbwlz = numba.cpython.unicode._normalize_slice(idx, len(A))
            for vsdrk__dvxy in range(oyk__xbwlz.start, oyk__xbwlz.stop,
                oyk__xbwlz.step):
                A[vsdrk__dvxy] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            ztvja__beeep = get_offsets(A)
            gzwh__gdi = get_null_bitmap(A)
            uaf__qbgzi = get_offsets(val)
            mtwix__awvef = get_data(val)
            jjm__xaug = get_null_bitmap(val)
            isryf__losk = len(A)
            oyk__xbwlz = numba.cpython.unicode._normalize_slice(idx,
                isryf__losk)
            yar__hgwq, zjr__vgwr = oyk__xbwlz.start, oyk__xbwlz.stop
            assert oyk__xbwlz.step == 1
            if yar__hgwq == 0:
                ztvja__beeep[yar__hgwq] = 0
            roumo__usi = ztvja__beeep[yar__hgwq]
            qtddi__wral = roumo__usi + len(mtwix__awvef)
            ensure_data_capacity(A, roumo__usi, qtddi__wral)
            qzwz__hayyq = get_data(A)
            qzwz__hayyq[roumo__usi:roumo__usi + len(mtwix__awvef)
                ] = mtwix__awvef
            ztvja__beeep[yar__hgwq:zjr__vgwr + 1] = uaf__qbgzi + roumo__usi
            vfvk__qcsq = 0
            for vsdrk__dvxy in range(yar__hgwq, zjr__vgwr):
                ysjv__faa = bodo.libs.int_arr_ext.get_bit_bitmap_arr(jjm__xaug,
                    vfvk__qcsq)
                bodo.libs.int_arr_ext.set_bit_to_arr(gzwh__gdi, vsdrk__dvxy,
                    ysjv__faa)
                vfvk__qcsq += 1
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
