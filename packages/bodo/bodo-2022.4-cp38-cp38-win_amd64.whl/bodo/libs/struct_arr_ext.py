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
            .utils.is_array_typ(glwco__ioy, False) for glwco__ioy in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(glwco__ioy,
                str) for glwco__ioy in names) and len(names) == len(data)
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
        return StructType(tuple(vdm__jwtro.dtype for vdm__jwtro in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(glwco__ioy) for glwco__ioy in d.keys())
        data = tuple(dtype_to_array_type(vdm__jwtro) for vdm__jwtro in d.
            values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(glwco__ioy, False) for glwco__ioy in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        khu__ozerv = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, khu__ozerv)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        khu__ozerv = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, khu__ozerv)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    xmzyt__kaexi = builder.module
    lic__vjo = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    lsael__vhpmo = cgutils.get_or_insert_function(xmzyt__kaexi, lic__vjo,
        name='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not lsael__vhpmo.is_declaration:
        return lsael__vhpmo
    lsael__vhpmo.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(lsael__vhpmo.append_basic_block())
    ecu__dkkfy = lsael__vhpmo.args[0]
    ledje__bay = context.get_value_type(payload_type).as_pointer()
    fpju__ykac = builder.bitcast(ecu__dkkfy, ledje__bay)
    jfioc__umwja = context.make_helper(builder, payload_type, ref=fpju__ykac)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), jfioc__umwja.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        jfioc__umwja.null_bitmap)
    builder.ret_void()
    return lsael__vhpmo


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    iwa__fcedo = context.get_value_type(payload_type)
    uqos__acs = context.get_abi_sizeof(iwa__fcedo)
    wexlz__pgq = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    czlr__oyj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, uqos__acs), wexlz__pgq)
    qvvze__iqjeh = context.nrt.meminfo_data(builder, czlr__oyj)
    rblx__wirl = builder.bitcast(qvvze__iqjeh, iwa__fcedo.as_pointer())
    jfioc__umwja = cgutils.create_struct_proxy(payload_type)(context, builder)
    ruj__dwejw = []
    bqmc__wqa = 0
    for arr_typ in struct_arr_type.data:
        wags__viupr = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        his__tilk = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(bqmc__wqa, bqmc__wqa +
            wags__viupr)])
        arr = gen_allocate_array(context, builder, arr_typ, his__tilk, c)
        ruj__dwejw.append(arr)
        bqmc__wqa += wags__viupr
    jfioc__umwja.data = cgutils.pack_array(builder, ruj__dwejw
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, ruj__dwejw)
    iir__gnodg = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    gnv__xilfu = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [iir__gnodg])
    null_bitmap_ptr = gnv__xilfu.data
    jfioc__umwja.null_bitmap = gnv__xilfu._getvalue()
    builder.store(jfioc__umwja._getvalue(), rblx__wirl)
    return czlr__oyj, jfioc__umwja.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    vtnyj__aqvz = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        pui__rru = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            pui__rru)
        vtnyj__aqvz.append(arr.data)
    kea__fnqrl = cgutils.pack_array(c.builder, vtnyj__aqvz
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, vtnyj__aqvz)
    voex__gqjmm = cgutils.alloca_once_value(c.builder, kea__fnqrl)
    xpw__jplgl = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(glwco__ioy.dtype)) for glwco__ioy in data_typ]
    gle__yawf = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, xpw__jplgl))
    fxpfb__fndnl = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, glwco__ioy) for glwco__ioy in
        names])
    bggsr__lijx = cgutils.alloca_once_value(c.builder, fxpfb__fndnl)
    return voex__gqjmm, gle__yawf, bggsr__lijx


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    kbfoi__auqo = all(isinstance(vdm__jwtro, types.Array) and vdm__jwtro.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for vdm__jwtro in typ.data)
    if kbfoi__auqo:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        hhqz__qhug = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            hhqz__qhug, i) for i in range(1, hhqz__qhug.type.count)], lir.
            IntType(64))
    czlr__oyj, data_tup, null_bitmap_ptr = construct_struct_array(c.context,
        c.builder, typ, n_structs, n_elems, c)
    if kbfoi__auqo:
        voex__gqjmm, gle__yawf, bggsr__lijx = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        lic__vjo = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        lsael__vhpmo = cgutils.get_or_insert_function(c.builder.module,
            lic__vjo, name='struct_array_from_sequence')
        c.builder.call(lsael__vhpmo, [val, c.context.get_constant(types.
            int32, len(typ.data)), c.builder.bitcast(voex__gqjmm, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            gle__yawf, lir.IntType(8).as_pointer()), c.builder.bitcast(
            bggsr__lijx, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    ryzn__lgtvr = c.context.make_helper(c.builder, typ)
    ryzn__lgtvr.meminfo = czlr__oyj
    owev__sabb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ryzn__lgtvr._getvalue(), is_error=owev__sabb)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    srvdp__mtqh = context.insert_const_string(builder.module, 'pandas')
    wmtzs__kdcpx = c.pyapi.import_module_noblock(srvdp__mtqh)
    mbf__wayqi = c.pyapi.object_getattr_string(wmtzs__kdcpx, 'NA')
    with cgutils.for_range(builder, n_structs) as zyaye__gbt:
        jqwzm__cab = zyaye__gbt.index
        nhbhu__pbta = seq_getitem(builder, context, val, jqwzm__cab)
        set_bitmap_bit(builder, null_bitmap_ptr, jqwzm__cab, 0)
        for fdoy__bvpr in range(len(typ.data)):
            arr_typ = typ.data[fdoy__bvpr]
            data_arr = builder.extract_value(data_tup, fdoy__bvpr)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            rpswz__wwd, rmc__pmjgq = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, jqwzm__cab])
        fydnz__kxqp = is_na_value(builder, context, nhbhu__pbta, mbf__wayqi)
        bdr__xypz = builder.icmp_unsigned('!=', fydnz__kxqp, lir.Constant(
            fydnz__kxqp.type, 1))
        with builder.if_then(bdr__xypz):
            set_bitmap_bit(builder, null_bitmap_ptr, jqwzm__cab, 1)
            for fdoy__bvpr in range(len(typ.data)):
                arr_typ = typ.data[fdoy__bvpr]
                if is_tuple_array:
                    vmtdg__rbzh = c.pyapi.tuple_getitem(nhbhu__pbta, fdoy__bvpr
                        )
                else:
                    vmtdg__rbzh = c.pyapi.dict_getitem_string(nhbhu__pbta,
                        typ.names[fdoy__bvpr])
                fydnz__kxqp = is_na_value(builder, context, vmtdg__rbzh,
                    mbf__wayqi)
                bdr__xypz = builder.icmp_unsigned('!=', fydnz__kxqp, lir.
                    Constant(fydnz__kxqp.type, 1))
                with builder.if_then(bdr__xypz):
                    vmtdg__rbzh = to_arr_obj_if_list_obj(c, context,
                        builder, vmtdg__rbzh, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        vmtdg__rbzh).value
                    data_arr = builder.extract_value(data_tup, fdoy__bvpr)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    rpswz__wwd, rmc__pmjgq = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, jqwzm__cab, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(nhbhu__pbta)
    c.pyapi.decref(wmtzs__kdcpx)
    c.pyapi.decref(mbf__wayqi)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    ryzn__lgtvr = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    qvvze__iqjeh = context.nrt.meminfo_data(builder, ryzn__lgtvr.meminfo)
    rblx__wirl = builder.bitcast(qvvze__iqjeh, context.get_value_type(
        payload_type).as_pointer())
    jfioc__umwja = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(rblx__wirl))
    return jfioc__umwja


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    jfioc__umwja = _get_struct_arr_payload(c.context, c.builder, typ, val)
    rpswz__wwd, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), jfioc__umwja.null_bitmap).data
    kbfoi__auqo = all(isinstance(vdm__jwtro, types.Array) and vdm__jwtro.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for vdm__jwtro in typ.data)
    if kbfoi__auqo:
        voex__gqjmm, gle__yawf, bggsr__lijx = _get_C_API_ptrs(c,
            jfioc__umwja.data, typ.data, typ.names)
        lic__vjo = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        eby__ssu = cgutils.get_or_insert_function(c.builder.module,
            lic__vjo, name='np_array_from_struct_array')
        arr = c.builder.call(eby__ssu, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(voex__gqjmm, lir
            .IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            gle__yawf, lir.IntType(8).as_pointer()), c.builder.bitcast(
            bggsr__lijx, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, jfioc__umwja.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    srvdp__mtqh = context.insert_const_string(builder.module, 'numpy')
    esm__xyqe = c.pyapi.import_module_noblock(srvdp__mtqh)
    ovk__xjkt = c.pyapi.object_getattr_string(esm__xyqe, 'object_')
    gulqi__rni = c.pyapi.long_from_longlong(length)
    gwyo__rpb = c.pyapi.call_method(esm__xyqe, 'ndarray', (gulqi__rni,
        ovk__xjkt))
    svpx__pvni = c.pyapi.object_getattr_string(esm__xyqe, 'nan')
    with cgutils.for_range(builder, length) as zyaye__gbt:
        jqwzm__cab = zyaye__gbt.index
        pyarray_setitem(builder, context, gwyo__rpb, jqwzm__cab, svpx__pvni)
        fckwj__wwox = get_bitmap_bit(builder, null_bitmap_ptr, jqwzm__cab)
        wizje__vzmb = builder.icmp_unsigned('!=', fckwj__wwox, lir.Constant
            (lir.IntType(8), 0))
        with builder.if_then(wizje__vzmb):
            if is_tuple_array:
                nhbhu__pbta = c.pyapi.tuple_new(len(typ.data))
            else:
                nhbhu__pbta = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(svpx__pvni)
                    c.pyapi.tuple_setitem(nhbhu__pbta, i, svpx__pvni)
                else:
                    c.pyapi.dict_setitem_string(nhbhu__pbta, typ.names[i],
                        svpx__pvni)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                rpswz__wwd, pggyi__vje = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, jqwzm__cab])
                with builder.if_then(pggyi__vje):
                    rpswz__wwd, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, jqwzm__cab])
                    raaod__vmerr = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(nhbhu__pbta, i, raaod__vmerr)
                    else:
                        c.pyapi.dict_setitem_string(nhbhu__pbta, typ.names[
                            i], raaod__vmerr)
                        c.pyapi.decref(raaod__vmerr)
            pyarray_setitem(builder, context, gwyo__rpb, jqwzm__cab,
                nhbhu__pbta)
            c.pyapi.decref(nhbhu__pbta)
    c.pyapi.decref(esm__xyqe)
    c.pyapi.decref(ovk__xjkt)
    c.pyapi.decref(gulqi__rni)
    c.pyapi.decref(svpx__pvni)
    return gwyo__rpb


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    vdfzo__crl = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if vdfzo__crl == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for fvaah__klyw in range(vdfzo__crl)])
    elif nested_counts_type.count < vdfzo__crl:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for fvaah__klyw in range(
            vdfzo__crl - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(vdm__jwtro) for vdm__jwtro in
            names_typ.types)
    posu__asp = tuple(vdm__jwtro.instance_type for vdm__jwtro in dtypes_typ
        .types)
    struct_arr_type = StructArrayType(posu__asp, names)

    def codegen(context, builder, sig, args):
        hgcc__jarl, nested_counts, fvaah__klyw, fvaah__klyw = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        czlr__oyj, fvaah__klyw, fvaah__klyw = construct_struct_array(context,
            builder, struct_arr_type, hgcc__jarl, nested_counts)
        ryzn__lgtvr = context.make_helper(builder, struct_arr_type)
        ryzn__lgtvr.meminfo = czlr__oyj
        return ryzn__lgtvr._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(glwco__ioy, str) for
            glwco__ioy in names) and len(names) == len(data)
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
        khu__ozerv = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, khu__ozerv)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        khu__ozerv = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, khu__ozerv)


def define_struct_dtor(context, builder, struct_type, payload_type):
    xmzyt__kaexi = builder.module
    lic__vjo = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    lsael__vhpmo = cgutils.get_or_insert_function(xmzyt__kaexi, lic__vjo,
        name='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not lsael__vhpmo.is_declaration:
        return lsael__vhpmo
    lsael__vhpmo.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(lsael__vhpmo.append_basic_block())
    ecu__dkkfy = lsael__vhpmo.args[0]
    ledje__bay = context.get_value_type(payload_type).as_pointer()
    fpju__ykac = builder.bitcast(ecu__dkkfy, ledje__bay)
    jfioc__umwja = context.make_helper(builder, payload_type, ref=fpju__ykac)
    for i in range(len(struct_type.data)):
        qxwa__dfcgm = builder.extract_value(jfioc__umwja.null_bitmap, i)
        wizje__vzmb = builder.icmp_unsigned('==', qxwa__dfcgm, lir.Constant
            (qxwa__dfcgm.type, 1))
        with builder.if_then(wizje__vzmb):
            val = builder.extract_value(jfioc__umwja.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return lsael__vhpmo


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    qvvze__iqjeh = context.nrt.meminfo_data(builder, struct.meminfo)
    rblx__wirl = builder.bitcast(qvvze__iqjeh, context.get_value_type(
        payload_type).as_pointer())
    jfioc__umwja = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(rblx__wirl))
    return jfioc__umwja, rblx__wirl


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    srvdp__mtqh = context.insert_const_string(builder.module, 'pandas')
    wmtzs__kdcpx = c.pyapi.import_module_noblock(srvdp__mtqh)
    mbf__wayqi = c.pyapi.object_getattr_string(wmtzs__kdcpx, 'NA')
    goj__mqc = []
    nulls = []
    for i, vdm__jwtro in enumerate(typ.data):
        raaod__vmerr = c.pyapi.dict_getitem_string(val, typ.names[i])
        dvdtd__vuzqh = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        lbmm__mkx = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(vdm__jwtro)))
        fydnz__kxqp = is_na_value(builder, context, raaod__vmerr, mbf__wayqi)
        wizje__vzmb = builder.icmp_unsigned('!=', fydnz__kxqp, lir.Constant
            (fydnz__kxqp.type, 1))
        with builder.if_then(wizje__vzmb):
            builder.store(context.get_constant(types.uint8, 1), dvdtd__vuzqh)
            field_val = c.pyapi.to_native_value(vdm__jwtro, raaod__vmerr).value
            builder.store(field_val, lbmm__mkx)
        goj__mqc.append(builder.load(lbmm__mkx))
        nulls.append(builder.load(dvdtd__vuzqh))
    c.pyapi.decref(wmtzs__kdcpx)
    c.pyapi.decref(mbf__wayqi)
    czlr__oyj = construct_struct(context, builder, typ, goj__mqc, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = czlr__oyj
    owev__sabb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=owev__sabb)


@box(StructType)
def box_struct(typ, val, c):
    dgve__eeyc = c.pyapi.dict_new(len(typ.data))
    jfioc__umwja, fvaah__klyw = _get_struct_payload(c.context, c.builder,
        typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(dgve__eeyc, typ.names[i], c.pyapi.
            borrow_none())
        qxwa__dfcgm = c.builder.extract_value(jfioc__umwja.null_bitmap, i)
        wizje__vzmb = c.builder.icmp_unsigned('==', qxwa__dfcgm, lir.
            Constant(qxwa__dfcgm.type, 1))
        with c.builder.if_then(wizje__vzmb):
            htt__bgdj = c.builder.extract_value(jfioc__umwja.data, i)
            c.context.nrt.incref(c.builder, val_typ, htt__bgdj)
            vmtdg__rbzh = c.pyapi.from_native_value(val_typ, htt__bgdj, c.
                env_manager)
            c.pyapi.dict_setitem_string(dgve__eeyc, typ.names[i], vmtdg__rbzh)
            c.pyapi.decref(vmtdg__rbzh)
    c.context.nrt.decref(c.builder, typ, val)
    return dgve__eeyc


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(vdm__jwtro) for vdm__jwtro in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, gsrex__bos = args
        payload_type = StructPayloadType(struct_type.data)
        iwa__fcedo = context.get_value_type(payload_type)
        uqos__acs = context.get_abi_sizeof(iwa__fcedo)
        wexlz__pgq = define_struct_dtor(context, builder, struct_type,
            payload_type)
        czlr__oyj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, uqos__acs), wexlz__pgq)
        qvvze__iqjeh = context.nrt.meminfo_data(builder, czlr__oyj)
        rblx__wirl = builder.bitcast(qvvze__iqjeh, iwa__fcedo.as_pointer())
        jfioc__umwja = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        jfioc__umwja.data = data
        jfioc__umwja.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for fvaah__klyw in range(len(
            data_typ.types))])
        builder.store(jfioc__umwja._getvalue(), rblx__wirl)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = czlr__oyj
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        jfioc__umwja, fvaah__klyw = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            jfioc__umwja.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        jfioc__umwja, fvaah__klyw = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            jfioc__umwja.null_bitmap)
    efj__miil = types.UniTuple(types.int8, len(struct_typ.data))
    return efj__miil(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, fvaah__klyw, val = args
        jfioc__umwja, rblx__wirl = _get_struct_payload(context, builder,
            struct_typ, struct)
        bgffz__tdj = jfioc__umwja.data
        dfcg__eeklb = builder.insert_value(bgffz__tdj, val, field_ind)
        ucr__ufijo = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, ucr__ufijo, bgffz__tdj)
        context.nrt.incref(builder, ucr__ufijo, dfcg__eeklb)
        jfioc__umwja.data = dfcg__eeklb
        builder.store(jfioc__umwja._getvalue(), rblx__wirl)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    qldh__xeshh = get_overload_const_str(ind)
    if qldh__xeshh not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            qldh__xeshh, struct))
    return struct.names.index(qldh__xeshh)


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
    iwa__fcedo = context.get_value_type(payload_type)
    uqos__acs = context.get_abi_sizeof(iwa__fcedo)
    wexlz__pgq = define_struct_dtor(context, builder, struct_type, payload_type
        )
    czlr__oyj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, uqos__acs), wexlz__pgq)
    qvvze__iqjeh = context.nrt.meminfo_data(builder, czlr__oyj)
    rblx__wirl = builder.bitcast(qvvze__iqjeh, iwa__fcedo.as_pointer())
    jfioc__umwja = cgutils.create_struct_proxy(payload_type)(context, builder)
    jfioc__umwja.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    jfioc__umwja.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(jfioc__umwja._getvalue(), rblx__wirl)
    return czlr__oyj


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    tdmu__mhx = tuple(d.dtype for d in struct_arr_typ.data)
    kwlz__dmyo = StructType(tdmu__mhx, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        qztw__tydkh, ind = args
        jfioc__umwja = _get_struct_arr_payload(context, builder,
            struct_arr_typ, qztw__tydkh)
        goj__mqc = []
        kxxzx__xpave = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            pui__rru = builder.extract_value(jfioc__umwja.data, i)
            rott__xqysx = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [pui__rru, ind]
                )
            kxxzx__xpave.append(rott__xqysx)
            zmxl__orv = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            wizje__vzmb = builder.icmp_unsigned('==', rott__xqysx, lir.
                Constant(rott__xqysx.type, 1))
            with builder.if_then(wizje__vzmb):
                awdj__mcpr = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    pui__rru, ind])
                builder.store(awdj__mcpr, zmxl__orv)
            goj__mqc.append(builder.load(zmxl__orv))
        if isinstance(kwlz__dmyo, types.DictType):
            mxgbl__dlbs = [context.insert_const_string(builder.module,
                anpn__xhhv) for anpn__xhhv in struct_arr_typ.names]
            opyif__hux = cgutils.pack_array(builder, goj__mqc)
            rqs__aym = cgutils.pack_array(builder, mxgbl__dlbs)

            def impl(names, vals):
                d = {}
                for i, anpn__xhhv in enumerate(names):
                    d[anpn__xhhv] = vals[i]
                return d
            bcv__ycg = context.compile_internal(builder, impl, kwlz__dmyo(
                types.Tuple(tuple(types.StringLiteral(anpn__xhhv) for
                anpn__xhhv in struct_arr_typ.names)), types.Tuple(tdmu__mhx
                )), [rqs__aym, opyif__hux])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                tdmu__mhx), opyif__hux)
            return bcv__ycg
        czlr__oyj = construct_struct(context, builder, kwlz__dmyo, goj__mqc,
            kxxzx__xpave)
        struct = context.make_helper(builder, kwlz__dmyo)
        struct.meminfo = czlr__oyj
        return struct._getvalue()
    return kwlz__dmyo(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        jfioc__umwja = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            jfioc__umwja.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        jfioc__umwja = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            jfioc__umwja.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(vdm__jwtro) for vdm__jwtro in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, gnv__xilfu, gsrex__bos = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        iwa__fcedo = context.get_value_type(payload_type)
        uqos__acs = context.get_abi_sizeof(iwa__fcedo)
        wexlz__pgq = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        czlr__oyj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, uqos__acs), wexlz__pgq)
        qvvze__iqjeh = context.nrt.meminfo_data(builder, czlr__oyj)
        rblx__wirl = builder.bitcast(qvvze__iqjeh, iwa__fcedo.as_pointer())
        jfioc__umwja = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        jfioc__umwja.data = data
        jfioc__umwja.null_bitmap = gnv__xilfu
        builder.store(jfioc__umwja._getvalue(), rblx__wirl)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, gnv__xilfu)
        ryzn__lgtvr = context.make_helper(builder, struct_arr_type)
        ryzn__lgtvr.meminfo = czlr__oyj
        return ryzn__lgtvr._getvalue()
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
    kdrm__aldyr = len(arr.data)
    spl__wwhc = 'def impl(arr, ind):\n'
    spl__wwhc += '  data = get_data(arr)\n'
    spl__wwhc += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        spl__wwhc += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        spl__wwhc += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        spl__wwhc += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    spl__wwhc += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(kdrm__aldyr)), ', '.join("'{}'".format(anpn__xhhv) for
        anpn__xhhv in arr.names)))
    nqso__npxog = {}
    exec(spl__wwhc, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, nqso__npxog)
    impl = nqso__npxog['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        kdrm__aldyr = len(arr.data)
        spl__wwhc = 'def impl(arr, ind, val):\n'
        spl__wwhc += '  data = get_data(arr)\n'
        spl__wwhc += '  null_bitmap = get_null_bitmap(arr)\n'
        spl__wwhc += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(kdrm__aldyr):
            if isinstance(val, StructType):
                spl__wwhc += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                spl__wwhc += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                spl__wwhc += '  else:\n'
                spl__wwhc += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                spl__wwhc += "  data[{}][ind] = val['{}']\n".format(i, arr.
                    names[i])
        nqso__npxog = {}
        exec(spl__wwhc, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, nqso__npxog)
        impl = nqso__npxog['impl']
        return impl
    if isinstance(ind, types.SliceType):
        kdrm__aldyr = len(arr.data)
        spl__wwhc = 'def impl(arr, ind, val):\n'
        spl__wwhc += '  data = get_data(arr)\n'
        spl__wwhc += '  null_bitmap = get_null_bitmap(arr)\n'
        spl__wwhc += '  val_data = get_data(val)\n'
        spl__wwhc += '  val_null_bitmap = get_null_bitmap(val)\n'
        spl__wwhc += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(kdrm__aldyr):
            spl__wwhc += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        nqso__npxog = {}
        exec(spl__wwhc, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, nqso__npxog)
        impl = nqso__npxog['impl']
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
    spl__wwhc = 'def impl(A):\n'
    spl__wwhc += '  total_nbytes = 0\n'
    spl__wwhc += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        spl__wwhc += f'  total_nbytes += data[{i}].nbytes\n'
    spl__wwhc += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    spl__wwhc += '  return total_nbytes\n'
    nqso__npxog = {}
    exec(spl__wwhc, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, nqso__npxog)
    impl = nqso__npxog['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        gnv__xilfu = get_null_bitmap(A)
        ykj__agtqi = bodo.ir.join.copy_arr_tup(data)
        emri__dwty = gnv__xilfu.copy()
        return init_struct_arr(ykj__agtqi, emri__dwty, names)
    return copy_impl
