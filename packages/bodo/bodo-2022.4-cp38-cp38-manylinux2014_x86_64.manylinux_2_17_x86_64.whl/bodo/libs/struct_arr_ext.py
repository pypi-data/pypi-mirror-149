"""Array implementation for structs of values.
Corresponds to Spark's StructType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Struct arrays: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in contiguous data arrays; one array per field. For example:
A:             ["AA", "B", "C"]
B:             [1, 2, 4]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
from numba.typed.typedobjectutils import _cast
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_int, get_overload_const_str, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
ll.add_symbol('struct_array_from_sequence', array_ext.
    struct_array_from_sequence)
ll.add_symbol('np_array_from_struct_array', array_ext.
    np_array_from_struct_array)


class StructArrayType(types.ArrayCompatible):

    def __init__(self, data, names=None):
        assert isinstance(data, tuple) and len(data) > 0 and all(bodo.utils
            .utils.is_array_typ(lsdz__gsbv, False) for lsdz__gsbv in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(lsdz__gsbv,
                str) for lsdz__gsbv in names) and len(names) == len(data)
        else:
            names = tuple('f{}'.format(i) for i in range(len(data)))
        self.data = data
        self.names = names
        super(StructArrayType, self).__init__(name=
            'StructArrayType({}, {})'.format(data, names))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return StructType(tuple(xbs__yod.dtype for xbs__yod in self.data),
            self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(lsdz__gsbv) for lsdz__gsbv in d.keys())
        data = tuple(dtype_to_array_type(xbs__yod) for xbs__yod in d.values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(lsdz__gsbv, False) for lsdz__gsbv in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        motu__pans = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, motu__pans)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        motu__pans = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, motu__pans)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    ape__efkpc = builder.module
    tqhf__ewd = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    cdnqj__odtxi = cgutils.get_or_insert_function(ape__efkpc, tqhf__ewd,
        name='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not cdnqj__odtxi.is_declaration:
        return cdnqj__odtxi
    cdnqj__odtxi.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(cdnqj__odtxi.append_basic_block())
    azbz__qjk = cdnqj__odtxi.args[0]
    vsqnn__cofrj = context.get_value_type(payload_type).as_pointer()
    ddn__mbyj = builder.bitcast(azbz__qjk, vsqnn__cofrj)
    mmuf__ddw = context.make_helper(builder, payload_type, ref=ddn__mbyj)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), mmuf__ddw.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), mmuf__ddw
        .null_bitmap)
    builder.ret_void()
    return cdnqj__odtxi


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    gdrtu__lznm = context.get_value_type(payload_type)
    ujdnv__sus = context.get_abi_sizeof(gdrtu__lznm)
    vqmqn__dda = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    pxh__nypp = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ujdnv__sus), vqmqn__dda)
    btho__twzzr = context.nrt.meminfo_data(builder, pxh__nypp)
    ypx__hkd = builder.bitcast(btho__twzzr, gdrtu__lznm.as_pointer())
    mmuf__ddw = cgutils.create_struct_proxy(payload_type)(context, builder)
    iuu__fqsxj = []
    xju__var = 0
    for arr_typ in struct_arr_type.data:
        klal__szapw = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        wno__ykcb = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(xju__var, xju__var +
            klal__szapw)])
        arr = gen_allocate_array(context, builder, arr_typ, wno__ykcb, c)
        iuu__fqsxj.append(arr)
        xju__var += klal__szapw
    mmuf__ddw.data = cgutils.pack_array(builder, iuu__fqsxj
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, iuu__fqsxj)
    seah__soo = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    ovkru__edcn = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [seah__soo])
    null_bitmap_ptr = ovkru__edcn.data
    mmuf__ddw.null_bitmap = ovkru__edcn._getvalue()
    builder.store(mmuf__ddw._getvalue(), ypx__hkd)
    return pxh__nypp, mmuf__ddw.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    exnp__iwki = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        ykv__hze = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            ykv__hze)
        exnp__iwki.append(arr.data)
    ytq__ijkbx = cgutils.pack_array(c.builder, exnp__iwki
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, exnp__iwki)
    kfa__rmw = cgutils.alloca_once_value(c.builder, ytq__ijkbx)
    mbls__vkvw = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(lsdz__gsbv.dtype)) for lsdz__gsbv in data_typ]
    gth__jneq = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, mbls__vkvw))
    uhag__zfbjv = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, lsdz__gsbv) for lsdz__gsbv in
        names])
    veas__rini = cgutils.alloca_once_value(c.builder, uhag__zfbjv)
    return kfa__rmw, gth__jneq, veas__rini


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    mrpta__igfts = all(isinstance(xbs__yod, types.Array) and xbs__yod.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        xbs__yod in typ.data)
    if mrpta__igfts:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        ali__gnr = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            ali__gnr, i) for i in range(1, ali__gnr.type.count)], lir.
            IntType(64))
    pxh__nypp, data_tup, null_bitmap_ptr = construct_struct_array(c.context,
        c.builder, typ, n_structs, n_elems, c)
    if mrpta__igfts:
        kfa__rmw, gth__jneq, veas__rini = _get_C_API_ptrs(c, data_tup, typ.
            data, typ.names)
        tqhf__ewd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        cdnqj__odtxi = cgutils.get_or_insert_function(c.builder.module,
            tqhf__ewd, name='struct_array_from_sequence')
        c.builder.call(cdnqj__odtxi, [val, c.context.get_constant(types.
            int32, len(typ.data)), c.builder.bitcast(kfa__rmw, lir.IntType(
            8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(gth__jneq,
            lir.IntType(8).as_pointer()), c.builder.bitcast(veas__rini, lir
            .IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    bymw__rpxm = c.context.make_helper(c.builder, typ)
    bymw__rpxm.meminfo = pxh__nypp
    whn__ewfo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bymw__rpxm._getvalue(), is_error=whn__ewfo)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    ubl__nosx = context.insert_const_string(builder.module, 'pandas')
    xvfhw__opvf = c.pyapi.import_module_noblock(ubl__nosx)
    dggu__okjbc = c.pyapi.object_getattr_string(xvfhw__opvf, 'NA')
    with cgutils.for_range(builder, n_structs) as tha__jdu:
        zxhqs__njwyy = tha__jdu.index
        mpbk__aemm = seq_getitem(builder, context, val, zxhqs__njwyy)
        set_bitmap_bit(builder, null_bitmap_ptr, zxhqs__njwyy, 0)
        for rse__shwpb in range(len(typ.data)):
            arr_typ = typ.data[rse__shwpb]
            data_arr = builder.extract_value(data_tup, rse__shwpb)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            oja__kdlgr, hqrs__uponw = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, zxhqs__njwyy])
        clt__iqi = is_na_value(builder, context, mpbk__aemm, dggu__okjbc)
        esri__omxup = builder.icmp_unsigned('!=', clt__iqi, lir.Constant(
            clt__iqi.type, 1))
        with builder.if_then(esri__omxup):
            set_bitmap_bit(builder, null_bitmap_ptr, zxhqs__njwyy, 1)
            for rse__shwpb in range(len(typ.data)):
                arr_typ = typ.data[rse__shwpb]
                if is_tuple_array:
                    tcunt__cpl = c.pyapi.tuple_getitem(mpbk__aemm, rse__shwpb)
                else:
                    tcunt__cpl = c.pyapi.dict_getitem_string(mpbk__aemm,
                        typ.names[rse__shwpb])
                clt__iqi = is_na_value(builder, context, tcunt__cpl,
                    dggu__okjbc)
                esri__omxup = builder.icmp_unsigned('!=', clt__iqi, lir.
                    Constant(clt__iqi.type, 1))
                with builder.if_then(esri__omxup):
                    tcunt__cpl = to_arr_obj_if_list_obj(c, context, builder,
                        tcunt__cpl, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        tcunt__cpl).value
                    data_arr = builder.extract_value(data_tup, rse__shwpb)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    oja__kdlgr, hqrs__uponw = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, zxhqs__njwyy, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(mpbk__aemm)
    c.pyapi.decref(xvfhw__opvf)
    c.pyapi.decref(dggu__okjbc)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    bymw__rpxm = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    btho__twzzr = context.nrt.meminfo_data(builder, bymw__rpxm.meminfo)
    ypx__hkd = builder.bitcast(btho__twzzr, context.get_value_type(
        payload_type).as_pointer())
    mmuf__ddw = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(ypx__hkd))
    return mmuf__ddw


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    mmuf__ddw = _get_struct_arr_payload(c.context, c.builder, typ, val)
    oja__kdlgr, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), mmuf__ddw.null_bitmap).data
    mrpta__igfts = all(isinstance(xbs__yod, types.Array) and xbs__yod.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        xbs__yod in typ.data)
    if mrpta__igfts:
        kfa__rmw, gth__jneq, veas__rini = _get_C_API_ptrs(c, mmuf__ddw.data,
            typ.data, typ.names)
        tqhf__ewd = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        bone__khvuv = cgutils.get_or_insert_function(c.builder.module,
            tqhf__ewd, name='np_array_from_struct_array')
        arr = c.builder.call(bone__khvuv, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(kfa__rmw, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            gth__jneq, lir.IntType(8).as_pointer()), c.builder.bitcast(
            veas__rini, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, mmuf__ddw.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    ubl__nosx = context.insert_const_string(builder.module, 'numpy')
    zrox__hae = c.pyapi.import_module_noblock(ubl__nosx)
    segso__zfw = c.pyapi.object_getattr_string(zrox__hae, 'object_')
    anh__lyjil = c.pyapi.long_from_longlong(length)
    keii__himup = c.pyapi.call_method(zrox__hae, 'ndarray', (anh__lyjil,
        segso__zfw))
    uhzyb__wkpi = c.pyapi.object_getattr_string(zrox__hae, 'nan')
    with cgutils.for_range(builder, length) as tha__jdu:
        zxhqs__njwyy = tha__jdu.index
        pyarray_setitem(builder, context, keii__himup, zxhqs__njwyy,
            uhzyb__wkpi)
        ajcx__vanzl = get_bitmap_bit(builder, null_bitmap_ptr, zxhqs__njwyy)
        qqg__mebj = builder.icmp_unsigned('!=', ajcx__vanzl, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(qqg__mebj):
            if is_tuple_array:
                mpbk__aemm = c.pyapi.tuple_new(len(typ.data))
            else:
                mpbk__aemm = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(uhzyb__wkpi)
                    c.pyapi.tuple_setitem(mpbk__aemm, i, uhzyb__wkpi)
                else:
                    c.pyapi.dict_setitem_string(mpbk__aemm, typ.names[i],
                        uhzyb__wkpi)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                oja__kdlgr, vuy__uuik = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, zxhqs__njwyy])
                with builder.if_then(vuy__uuik):
                    oja__kdlgr, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, zxhqs__njwyy])
                    uns__gss = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(mpbk__aemm, i, uns__gss)
                    else:
                        c.pyapi.dict_setitem_string(mpbk__aemm, typ.names[i
                            ], uns__gss)
                        c.pyapi.decref(uns__gss)
            pyarray_setitem(builder, context, keii__himup, zxhqs__njwyy,
                mpbk__aemm)
            c.pyapi.decref(mpbk__aemm)
    c.pyapi.decref(zrox__hae)
    c.pyapi.decref(segso__zfw)
    c.pyapi.decref(anh__lyjil)
    c.pyapi.decref(uhzyb__wkpi)
    return keii__himup


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    pxr__oaz = bodo.utils.transform.get_type_alloc_counts(struct_arr_type) - 1
    if pxr__oaz == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for hohey__kdf in range(pxr__oaz)])
    elif nested_counts_type.count < pxr__oaz:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for hohey__kdf in range(
            pxr__oaz - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(xbs__yod) for xbs__yod in
            names_typ.types)
    uww__psa = tuple(xbs__yod.instance_type for xbs__yod in dtypes_typ.types)
    struct_arr_type = StructArrayType(uww__psa, names)

    def codegen(context, builder, sig, args):
        pyb__lucb, nested_counts, hohey__kdf, hohey__kdf = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        pxh__nypp, hohey__kdf, hohey__kdf = construct_struct_array(context,
            builder, struct_arr_type, pyb__lucb, nested_counts)
        bymw__rpxm = context.make_helper(builder, struct_arr_type)
        bymw__rpxm.meminfo = pxh__nypp
        return bymw__rpxm._getvalue()
    return struct_arr_type(num_structs_typ, nested_counts_typ, dtypes_typ,
        names_typ), codegen


def pre_alloc_struct_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_struct_arr_ext_pre_alloc_struct_array
    ) = pre_alloc_struct_array_equiv


class StructType(types.Type):

    def __init__(self, data, names):
        assert isinstance(data, tuple) and len(data) > 0
        assert isinstance(names, tuple) and all(isinstance(lsdz__gsbv, str) for
            lsdz__gsbv in names) and len(names) == len(data)
        self.data = data
        self.names = names
        super(StructType, self).__init__(name='StructType({}, {})'.format(
            data, names))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple)
        self.data = data
        super(StructPayloadType, self).__init__(name=
            'StructPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructPayloadType)
class StructPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        motu__pans = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, motu__pans)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        motu__pans = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, motu__pans)


def define_struct_dtor(context, builder, struct_type, payload_type):
    ape__efkpc = builder.module
    tqhf__ewd = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    cdnqj__odtxi = cgutils.get_or_insert_function(ape__efkpc, tqhf__ewd,
        name='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not cdnqj__odtxi.is_declaration:
        return cdnqj__odtxi
    cdnqj__odtxi.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(cdnqj__odtxi.append_basic_block())
    azbz__qjk = cdnqj__odtxi.args[0]
    vsqnn__cofrj = context.get_value_type(payload_type).as_pointer()
    ddn__mbyj = builder.bitcast(azbz__qjk, vsqnn__cofrj)
    mmuf__ddw = context.make_helper(builder, payload_type, ref=ddn__mbyj)
    for i in range(len(struct_type.data)):
        vinqi__nzkx = builder.extract_value(mmuf__ddw.null_bitmap, i)
        qqg__mebj = builder.icmp_unsigned('==', vinqi__nzkx, lir.Constant(
            vinqi__nzkx.type, 1))
        with builder.if_then(qqg__mebj):
            val = builder.extract_value(mmuf__ddw.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return cdnqj__odtxi


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    btho__twzzr = context.nrt.meminfo_data(builder, struct.meminfo)
    ypx__hkd = builder.bitcast(btho__twzzr, context.get_value_type(
        payload_type).as_pointer())
    mmuf__ddw = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(ypx__hkd))
    return mmuf__ddw, ypx__hkd


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    ubl__nosx = context.insert_const_string(builder.module, 'pandas')
    xvfhw__opvf = c.pyapi.import_module_noblock(ubl__nosx)
    dggu__okjbc = c.pyapi.object_getattr_string(xvfhw__opvf, 'NA')
    husvx__jom = []
    nulls = []
    for i, xbs__yod in enumerate(typ.data):
        uns__gss = c.pyapi.dict_getitem_string(val, typ.names[i])
        zjyt__jbjqh = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        pgpcd__cac = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(xbs__yod)))
        clt__iqi = is_na_value(builder, context, uns__gss, dggu__okjbc)
        qqg__mebj = builder.icmp_unsigned('!=', clt__iqi, lir.Constant(
            clt__iqi.type, 1))
        with builder.if_then(qqg__mebj):
            builder.store(context.get_constant(types.uint8, 1), zjyt__jbjqh)
            field_val = c.pyapi.to_native_value(xbs__yod, uns__gss).value
            builder.store(field_val, pgpcd__cac)
        husvx__jom.append(builder.load(pgpcd__cac))
        nulls.append(builder.load(zjyt__jbjqh))
    c.pyapi.decref(xvfhw__opvf)
    c.pyapi.decref(dggu__okjbc)
    pxh__nypp = construct_struct(context, builder, typ, husvx__jom, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = pxh__nypp
    whn__ewfo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=whn__ewfo)


@box(StructType)
def box_struct(typ, val, c):
    qhfj__ojl = c.pyapi.dict_new(len(typ.data))
    mmuf__ddw, hohey__kdf = _get_struct_payload(c.context, c.builder, typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(qhfj__ojl, typ.names[i], c.pyapi.
            borrow_none())
        vinqi__nzkx = c.builder.extract_value(mmuf__ddw.null_bitmap, i)
        qqg__mebj = c.builder.icmp_unsigned('==', vinqi__nzkx, lir.Constant
            (vinqi__nzkx.type, 1))
        with c.builder.if_then(qqg__mebj):
            arh__kvb = c.builder.extract_value(mmuf__ddw.data, i)
            c.context.nrt.incref(c.builder, val_typ, arh__kvb)
            tcunt__cpl = c.pyapi.from_native_value(val_typ, arh__kvb, c.
                env_manager)
            c.pyapi.dict_setitem_string(qhfj__ojl, typ.names[i], tcunt__cpl)
            c.pyapi.decref(tcunt__cpl)
    c.context.nrt.decref(c.builder, typ, val)
    return qhfj__ojl


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(xbs__yod) for xbs__yod in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, jwz__geg = args
        payload_type = StructPayloadType(struct_type.data)
        gdrtu__lznm = context.get_value_type(payload_type)
        ujdnv__sus = context.get_abi_sizeof(gdrtu__lznm)
        vqmqn__dda = define_struct_dtor(context, builder, struct_type,
            payload_type)
        pxh__nypp = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, ujdnv__sus), vqmqn__dda)
        btho__twzzr = context.nrt.meminfo_data(builder, pxh__nypp)
        ypx__hkd = builder.bitcast(btho__twzzr, gdrtu__lznm.as_pointer())
        mmuf__ddw = cgutils.create_struct_proxy(payload_type)(context, builder)
        mmuf__ddw.data = data
        mmuf__ddw.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for hohey__kdf in range(len(
            data_typ.types))])
        builder.store(mmuf__ddw._getvalue(), ypx__hkd)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = pxh__nypp
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        mmuf__ddw, hohey__kdf = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mmuf__ddw.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        mmuf__ddw, hohey__kdf = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mmuf__ddw.null_bitmap)
    drkw__mcco = types.UniTuple(types.int8, len(struct_typ.data))
    return drkw__mcco(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, hohey__kdf, val = args
        mmuf__ddw, ypx__hkd = _get_struct_payload(context, builder,
            struct_typ, struct)
        idhia__tmc = mmuf__ddw.data
        muv__lnu = builder.insert_value(idhia__tmc, val, field_ind)
        nrhpx__ohlqa = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, nrhpx__ohlqa, idhia__tmc)
        context.nrt.incref(builder, nrhpx__ohlqa, muv__lnu)
        mmuf__ddw.data = muv__lnu
        builder.store(mmuf__ddw._getvalue(), ypx__hkd)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    klg__zzxor = get_overload_const_str(ind)
    if klg__zzxor not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            klg__zzxor, struct))
    return struct.names.index(klg__zzxor)


def is_field_value_null(s, field_name):
    pass


@overload(is_field_value_null, no_unliteral=True)
def overload_is_field_value_null(s, field_name):
    field_ind = _get_struct_field_ind(s, field_name, 'element access (getitem)'
        )
    return lambda s, field_name: get_struct_null_bitmap(s)[field_ind] == 0


@overload(operator.getitem, no_unliteral=True)
def struct_getitem(struct, ind):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'element access (getitem)')
    return lambda struct, ind: get_struct_data(struct)[field_ind]


@overload(operator.setitem, no_unliteral=True)
def struct_setitem(struct, ind, val):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'item assignment (setitem)')
    field_typ = struct.data[field_ind]
    return lambda struct, ind, val: set_struct_data(struct, field_ind,
        _cast(val, field_typ))


@overload(len, no_unliteral=True)
def overload_struct_arr_len(struct):
    if isinstance(struct, StructType):
        num_fields = len(struct.data)
        return lambda struct: num_fields


def construct_struct(context, builder, struct_type, values, nulls):
    payload_type = StructPayloadType(struct_type.data)
    gdrtu__lznm = context.get_value_type(payload_type)
    ujdnv__sus = context.get_abi_sizeof(gdrtu__lznm)
    vqmqn__dda = define_struct_dtor(context, builder, struct_type, payload_type
        )
    pxh__nypp = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ujdnv__sus), vqmqn__dda)
    btho__twzzr = context.nrt.meminfo_data(builder, pxh__nypp)
    ypx__hkd = builder.bitcast(btho__twzzr, gdrtu__lznm.as_pointer())
    mmuf__ddw = cgutils.create_struct_proxy(payload_type)(context, builder)
    mmuf__ddw.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    mmuf__ddw.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(mmuf__ddw._getvalue(), ypx__hkd)
    return pxh__nypp


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    mid__opq = tuple(d.dtype for d in struct_arr_typ.data)
    zujiu__evyw = StructType(mid__opq, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        xezq__yjo, ind = args
        mmuf__ddw = _get_struct_arr_payload(context, builder,
            struct_arr_typ, xezq__yjo)
        husvx__jom = []
        ixsbz__yoe = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            ykv__hze = builder.extract_value(mmuf__ddw.data, i)
            kxrg__ihy = context.compile_internal(builder, lambda arr, ind: 
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [ykv__hze, ind]
                )
            ixsbz__yoe.append(kxrg__ihy)
            dcbm__bbx = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            qqg__mebj = builder.icmp_unsigned('==', kxrg__ihy, lir.Constant
                (kxrg__ihy.type, 1))
            with builder.if_then(qqg__mebj):
                tjut__ehwk = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    ykv__hze, ind])
                builder.store(tjut__ehwk, dcbm__bbx)
            husvx__jom.append(builder.load(dcbm__bbx))
        if isinstance(zujiu__evyw, types.DictType):
            thaed__nodf = [context.insert_const_string(builder.module,
                olwn__ikdg) for olwn__ikdg in struct_arr_typ.names]
            wpvf__besq = cgutils.pack_array(builder, husvx__jom)
            qdc__sburo = cgutils.pack_array(builder, thaed__nodf)

            def impl(names, vals):
                d = {}
                for i, olwn__ikdg in enumerate(names):
                    d[olwn__ikdg] = vals[i]
                return d
            renza__kmix = context.compile_internal(builder, impl,
                zujiu__evyw(types.Tuple(tuple(types.StringLiteral(
                olwn__ikdg) for olwn__ikdg in struct_arr_typ.names)), types
                .Tuple(mid__opq)), [qdc__sburo, wpvf__besq])
            context.nrt.decref(builder, types.BaseTuple.from_types(mid__opq
                ), wpvf__besq)
            return renza__kmix
        pxh__nypp = construct_struct(context, builder, zujiu__evyw,
            husvx__jom, ixsbz__yoe)
        struct = context.make_helper(builder, zujiu__evyw)
        struct.meminfo = pxh__nypp
        return struct._getvalue()
    return zujiu__evyw(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        mmuf__ddw = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mmuf__ddw.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        mmuf__ddw = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mmuf__ddw.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(xbs__yod) for xbs__yod in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, ovkru__edcn, jwz__geg = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        gdrtu__lznm = context.get_value_type(payload_type)
        ujdnv__sus = context.get_abi_sizeof(gdrtu__lznm)
        vqmqn__dda = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        pxh__nypp = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, ujdnv__sus), vqmqn__dda)
        btho__twzzr = context.nrt.meminfo_data(builder, pxh__nypp)
        ypx__hkd = builder.bitcast(btho__twzzr, gdrtu__lznm.as_pointer())
        mmuf__ddw = cgutils.create_struct_proxy(payload_type)(context, builder)
        mmuf__ddw.data = data
        mmuf__ddw.null_bitmap = ovkru__edcn
        builder.store(mmuf__ddw._getvalue(), ypx__hkd)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, ovkru__edcn)
        bymw__rpxm = context.make_helper(builder, struct_arr_type)
        bymw__rpxm.meminfo = pxh__nypp
        return bymw__rpxm._getvalue()
    return struct_arr_type(data_typ, null_bitmap_typ, names_typ), codegen


@overload(operator.getitem, no_unliteral=True)
def struct_arr_getitem(arr, ind):
    if not isinstance(arr, StructArrayType):
        return
    if isinstance(ind, types.Integer):

        def struct_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            return struct_array_get_struct(arr, ind)
        return struct_arr_getitem_impl
    dil__lwjj = len(arr.data)
    cdvt__kmku = 'def impl(arr, ind):\n'
    cdvt__kmku += '  data = get_data(arr)\n'
    cdvt__kmku += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        cdvt__kmku += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        cdvt__kmku += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        cdvt__kmku += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    cdvt__kmku += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(dil__lwjj)), ', '.join("'{}'".format(olwn__ikdg) for
        olwn__ikdg in arr.names)))
    weoo__duea = {}
    exec(cdvt__kmku, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, weoo__duea)
    impl = weoo__duea['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        dil__lwjj = len(arr.data)
        cdvt__kmku = 'def impl(arr, ind, val):\n'
        cdvt__kmku += '  data = get_data(arr)\n'
        cdvt__kmku += '  null_bitmap = get_null_bitmap(arr)\n'
        cdvt__kmku += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(dil__lwjj):
            if isinstance(val, StructType):
                cdvt__kmku += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                cdvt__kmku += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                cdvt__kmku += '  else:\n'
                cdvt__kmku += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                cdvt__kmku += "  data[{}][ind] = val['{}']\n".format(i, arr
                    .names[i])
        weoo__duea = {}
        exec(cdvt__kmku, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, weoo__duea)
        impl = weoo__duea['impl']
        return impl
    if isinstance(ind, types.SliceType):
        dil__lwjj = len(arr.data)
        cdvt__kmku = 'def impl(arr, ind, val):\n'
        cdvt__kmku += '  data = get_data(arr)\n'
        cdvt__kmku += '  null_bitmap = get_null_bitmap(arr)\n'
        cdvt__kmku += '  val_data = get_data(val)\n'
        cdvt__kmku += '  val_null_bitmap = get_null_bitmap(val)\n'
        cdvt__kmku += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(dil__lwjj):
            cdvt__kmku += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        weoo__duea = {}
        exec(cdvt__kmku, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, weoo__duea)
        impl = weoo__duea['impl']
        return impl
    raise BodoError(
        'only setitem with scalar/slice index is currently supported for struct arrays'
        )


@overload(len, no_unliteral=True)
def overload_struct_arr_len(A):
    if isinstance(A, StructArrayType):
        return lambda A: len(get_data(A)[0])


@overload_attribute(StructArrayType, 'shape')
def overload_struct_arr_shape(A):
    return lambda A: (len(get_data(A)[0]),)


@overload_attribute(StructArrayType, 'dtype')
def overload_struct_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(StructArrayType, 'ndim')
def overload_struct_arr_ndim(A):
    return lambda A: 1


@overload_attribute(StructArrayType, 'nbytes')
def overload_struct_arr_nbytes(A):
    cdvt__kmku = 'def impl(A):\n'
    cdvt__kmku += '  total_nbytes = 0\n'
    cdvt__kmku += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        cdvt__kmku += f'  total_nbytes += data[{i}].nbytes\n'
    cdvt__kmku += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    cdvt__kmku += '  return total_nbytes\n'
    weoo__duea = {}
    exec(cdvt__kmku, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, weoo__duea)
    impl = weoo__duea['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        ovkru__edcn = get_null_bitmap(A)
        aqa__qwvg = bodo.ir.join.copy_arr_tup(data)
        yqrpo__pgty = ovkru__edcn.copy()
        return init_struct_arr(aqa__qwvg, yqrpo__pgty, names)
    return copy_impl
