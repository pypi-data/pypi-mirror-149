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
            .utils.is_array_typ(pwc__ggx, False) for pwc__ggx in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(pwc__ggx,
                str) for pwc__ggx in names) and len(names) == len(data)
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
        return StructType(tuple(psdjk__vzna.dtype for psdjk__vzna in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(pwc__ggx) for pwc__ggx in d.keys())
        data = tuple(dtype_to_array_type(psdjk__vzna) for psdjk__vzna in d.
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
            is_array_typ(pwc__ggx, False) for pwc__ggx in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ugrdh__nzy = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, ugrdh__nzy)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        ugrdh__nzy = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ugrdh__nzy)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    vbmz__xhrl = builder.module
    zbjd__qeq = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    ojbsa__hhk = cgutils.get_or_insert_function(vbmz__xhrl, zbjd__qeq, name
        ='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not ojbsa__hhk.is_declaration:
        return ojbsa__hhk
    ojbsa__hhk.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(ojbsa__hhk.append_basic_block())
    rof__hwq = ojbsa__hhk.args[0]
    dtb__upe = context.get_value_type(payload_type).as_pointer()
    jwmc__sar = builder.bitcast(rof__hwq, dtb__upe)
    pgd__ydw = context.make_helper(builder, payload_type, ref=jwmc__sar)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), pgd__ydw.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), pgd__ydw.
        null_bitmap)
    builder.ret_void()
    return ojbsa__hhk


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    pyp__rbqi = context.get_value_type(payload_type)
    octl__ygzu = context.get_abi_sizeof(pyp__rbqi)
    usbk__qaglw = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    nxcvb__wtikm = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, octl__ygzu), usbk__qaglw)
    lsddu__xup = context.nrt.meminfo_data(builder, nxcvb__wtikm)
    ylrt__wlw = builder.bitcast(lsddu__xup, pyp__rbqi.as_pointer())
    pgd__ydw = cgutils.create_struct_proxy(payload_type)(context, builder)
    fjwc__wbcao = []
    xofe__dta = 0
    for arr_typ in struct_arr_type.data:
        dhzq__lqqz = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        ljqma__uen = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(xofe__dta, xofe__dta +
            dhzq__lqqz)])
        arr = gen_allocate_array(context, builder, arr_typ, ljqma__uen, c)
        fjwc__wbcao.append(arr)
        xofe__dta += dhzq__lqqz
    pgd__ydw.data = cgutils.pack_array(builder, fjwc__wbcao
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, fjwc__wbcao)
    lnl__mixf = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    djcp__cfl = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [lnl__mixf])
    null_bitmap_ptr = djcp__cfl.data
    pgd__ydw.null_bitmap = djcp__cfl._getvalue()
    builder.store(pgd__ydw._getvalue(), ylrt__wlw)
    return nxcvb__wtikm, pgd__ydw.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    lixqa__mpwe = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        pgf__etx = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            pgf__etx)
        lixqa__mpwe.append(arr.data)
    zgvia__chlqk = cgutils.pack_array(c.builder, lixqa__mpwe
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, lixqa__mpwe)
    esj__tmldl = cgutils.alloca_once_value(c.builder, zgvia__chlqk)
    ahje__giz = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(pwc__ggx.dtype)) for pwc__ggx in data_typ]
    vgoq__kpfjq = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c
        .builder, ahje__giz))
    xfzx__kvu = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, pwc__ggx) for pwc__ggx in names])
    dxs__nqzac = cgutils.alloca_once_value(c.builder, xfzx__kvu)
    return esj__tmldl, vgoq__kpfjq, dxs__nqzac


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    acrhl__sbitf = all(isinstance(psdjk__vzna, types.Array) and psdjk__vzna
        .dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for psdjk__vzna in typ.data)
    if acrhl__sbitf:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        ijn__mynv = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            ijn__mynv, i) for i in range(1, ijn__mynv.type.count)], lir.
            IntType(64))
    nxcvb__wtikm, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if acrhl__sbitf:
        esj__tmldl, vgoq__kpfjq, dxs__nqzac = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        zbjd__qeq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        ojbsa__hhk = cgutils.get_or_insert_function(c.builder.module,
            zbjd__qeq, name='struct_array_from_sequence')
        c.builder.call(ojbsa__hhk, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(esj__tmldl, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(vgoq__kpfjq,
            lir.IntType(8).as_pointer()), c.builder.bitcast(dxs__nqzac, lir
            .IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    borj__qgws = c.context.make_helper(c.builder, typ)
    borj__qgws.meminfo = nxcvb__wtikm
    jhzx__rndr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(borj__qgws._getvalue(), is_error=jhzx__rndr)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    dzij__ljg = context.insert_const_string(builder.module, 'pandas')
    tmifp__ikpx = c.pyapi.import_module_noblock(dzij__ljg)
    iayu__nzro = c.pyapi.object_getattr_string(tmifp__ikpx, 'NA')
    with cgutils.for_range(builder, n_structs) as igil__dhiq:
        ame__dvrur = igil__dhiq.index
        syr__owt = seq_getitem(builder, context, val, ame__dvrur)
        set_bitmap_bit(builder, null_bitmap_ptr, ame__dvrur, 0)
        for nbbx__uchmh in range(len(typ.data)):
            arr_typ = typ.data[nbbx__uchmh]
            data_arr = builder.extract_value(data_tup, nbbx__uchmh)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            ptjxw__azw, uhu__vyrg = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, ame__dvrur])
        nqhj__txwjh = is_na_value(builder, context, syr__owt, iayu__nzro)
        lugdr__biyp = builder.icmp_unsigned('!=', nqhj__txwjh, lir.Constant
            (nqhj__txwjh.type, 1))
        with builder.if_then(lugdr__biyp):
            set_bitmap_bit(builder, null_bitmap_ptr, ame__dvrur, 1)
            for nbbx__uchmh in range(len(typ.data)):
                arr_typ = typ.data[nbbx__uchmh]
                if is_tuple_array:
                    hust__ewd = c.pyapi.tuple_getitem(syr__owt, nbbx__uchmh)
                else:
                    hust__ewd = c.pyapi.dict_getitem_string(syr__owt, typ.
                        names[nbbx__uchmh])
                nqhj__txwjh = is_na_value(builder, context, hust__ewd,
                    iayu__nzro)
                lugdr__biyp = builder.icmp_unsigned('!=', nqhj__txwjh, lir.
                    Constant(nqhj__txwjh.type, 1))
                with builder.if_then(lugdr__biyp):
                    hust__ewd = to_arr_obj_if_list_obj(c, context, builder,
                        hust__ewd, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        hust__ewd).value
                    data_arr = builder.extract_value(data_tup, nbbx__uchmh)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    ptjxw__azw, uhu__vyrg = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, ame__dvrur, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(syr__owt)
    c.pyapi.decref(tmifp__ikpx)
    c.pyapi.decref(iayu__nzro)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    borj__qgws = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    lsddu__xup = context.nrt.meminfo_data(builder, borj__qgws.meminfo)
    ylrt__wlw = builder.bitcast(lsddu__xup, context.get_value_type(
        payload_type).as_pointer())
    pgd__ydw = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(ylrt__wlw))
    return pgd__ydw


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    pgd__ydw = _get_struct_arr_payload(c.context, c.builder, typ, val)
    ptjxw__azw, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), pgd__ydw.null_bitmap).data
    acrhl__sbitf = all(isinstance(psdjk__vzna, types.Array) and psdjk__vzna
        .dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for psdjk__vzna in typ.data)
    if acrhl__sbitf:
        esj__tmldl, vgoq__kpfjq, dxs__nqzac = _get_C_API_ptrs(c, pgd__ydw.
            data, typ.data, typ.names)
        zbjd__qeq = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        yjeib__rgkm = cgutils.get_or_insert_function(c.builder.module,
            zbjd__qeq, name='np_array_from_struct_array')
        arr = c.builder.call(yjeib__rgkm, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(esj__tmldl, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            vgoq__kpfjq, lir.IntType(8).as_pointer()), c.builder.bitcast(
            dxs__nqzac, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, pgd__ydw.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    dzij__ljg = context.insert_const_string(builder.module, 'numpy')
    zen__ruivu = c.pyapi.import_module_noblock(dzij__ljg)
    zbfs__ykjtt = c.pyapi.object_getattr_string(zen__ruivu, 'object_')
    yfqey__vdre = c.pyapi.long_from_longlong(length)
    jongn__rirtn = c.pyapi.call_method(zen__ruivu, 'ndarray', (yfqey__vdre,
        zbfs__ykjtt))
    azqk__kjjig = c.pyapi.object_getattr_string(zen__ruivu, 'nan')
    with cgutils.for_range(builder, length) as igil__dhiq:
        ame__dvrur = igil__dhiq.index
        pyarray_setitem(builder, context, jongn__rirtn, ame__dvrur, azqk__kjjig
            )
        yuzao__mlopy = get_bitmap_bit(builder, null_bitmap_ptr, ame__dvrur)
        lxp__mpjsn = builder.icmp_unsigned('!=', yuzao__mlopy, lir.Constant
            (lir.IntType(8), 0))
        with builder.if_then(lxp__mpjsn):
            if is_tuple_array:
                syr__owt = c.pyapi.tuple_new(len(typ.data))
            else:
                syr__owt = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(azqk__kjjig)
                    c.pyapi.tuple_setitem(syr__owt, i, azqk__kjjig)
                else:
                    c.pyapi.dict_setitem_string(syr__owt, typ.names[i],
                        azqk__kjjig)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                ptjxw__azw, sszwm__sjf = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, ame__dvrur])
                with builder.if_then(sszwm__sjf):
                    ptjxw__azw, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, ame__dvrur])
                    wxu__cxpj = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(syr__owt, i, wxu__cxpj)
                    else:
                        c.pyapi.dict_setitem_string(syr__owt, typ.names[i],
                            wxu__cxpj)
                        c.pyapi.decref(wxu__cxpj)
            pyarray_setitem(builder, context, jongn__rirtn, ame__dvrur,
                syr__owt)
            c.pyapi.decref(syr__owt)
    c.pyapi.decref(zen__ruivu)
    c.pyapi.decref(zbfs__ykjtt)
    c.pyapi.decref(yfqey__vdre)
    c.pyapi.decref(azqk__kjjig)
    return jongn__rirtn


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    ozob__fkf = bodo.utils.transform.get_type_alloc_counts(struct_arr_type) - 1
    if ozob__fkf == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for yvt__ctpqu in range(ozob__fkf)])
    elif nested_counts_type.count < ozob__fkf:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for yvt__ctpqu in range(
            ozob__fkf - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(psdjk__vzna) for psdjk__vzna in
            names_typ.types)
    qffyl__kgo = tuple(psdjk__vzna.instance_type for psdjk__vzna in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(qffyl__kgo, names)

    def codegen(context, builder, sig, args):
        wot__tfqcn, nested_counts, yvt__ctpqu, yvt__ctpqu = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        nxcvb__wtikm, yvt__ctpqu, yvt__ctpqu = construct_struct_array(context,
            builder, struct_arr_type, wot__tfqcn, nested_counts)
        borj__qgws = context.make_helper(builder, struct_arr_type)
        borj__qgws.meminfo = nxcvb__wtikm
        return borj__qgws._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(pwc__ggx, str) for
            pwc__ggx in names) and len(names) == len(data)
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
        ugrdh__nzy = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, ugrdh__nzy)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        ugrdh__nzy = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ugrdh__nzy)


def define_struct_dtor(context, builder, struct_type, payload_type):
    vbmz__xhrl = builder.module
    zbjd__qeq = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    ojbsa__hhk = cgutils.get_or_insert_function(vbmz__xhrl, zbjd__qeq, name
        ='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not ojbsa__hhk.is_declaration:
        return ojbsa__hhk
    ojbsa__hhk.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(ojbsa__hhk.append_basic_block())
    rof__hwq = ojbsa__hhk.args[0]
    dtb__upe = context.get_value_type(payload_type).as_pointer()
    jwmc__sar = builder.bitcast(rof__hwq, dtb__upe)
    pgd__ydw = context.make_helper(builder, payload_type, ref=jwmc__sar)
    for i in range(len(struct_type.data)):
        qubw__swn = builder.extract_value(pgd__ydw.null_bitmap, i)
        lxp__mpjsn = builder.icmp_unsigned('==', qubw__swn, lir.Constant(
            qubw__swn.type, 1))
        with builder.if_then(lxp__mpjsn):
            val = builder.extract_value(pgd__ydw.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return ojbsa__hhk


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    lsddu__xup = context.nrt.meminfo_data(builder, struct.meminfo)
    ylrt__wlw = builder.bitcast(lsddu__xup, context.get_value_type(
        payload_type).as_pointer())
    pgd__ydw = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(ylrt__wlw))
    return pgd__ydw, ylrt__wlw


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    dzij__ljg = context.insert_const_string(builder.module, 'pandas')
    tmifp__ikpx = c.pyapi.import_module_noblock(dzij__ljg)
    iayu__nzro = c.pyapi.object_getattr_string(tmifp__ikpx, 'NA')
    lyzm__rllij = []
    nulls = []
    for i, psdjk__vzna in enumerate(typ.data):
        wxu__cxpj = c.pyapi.dict_getitem_string(val, typ.names[i])
        awuc__iypn = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        lajee__fkjk = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(psdjk__vzna)))
        nqhj__txwjh = is_na_value(builder, context, wxu__cxpj, iayu__nzro)
        lxp__mpjsn = builder.icmp_unsigned('!=', nqhj__txwjh, lir.Constant(
            nqhj__txwjh.type, 1))
        with builder.if_then(lxp__mpjsn):
            builder.store(context.get_constant(types.uint8, 1), awuc__iypn)
            field_val = c.pyapi.to_native_value(psdjk__vzna, wxu__cxpj).value
            builder.store(field_val, lajee__fkjk)
        lyzm__rllij.append(builder.load(lajee__fkjk))
        nulls.append(builder.load(awuc__iypn))
    c.pyapi.decref(tmifp__ikpx)
    c.pyapi.decref(iayu__nzro)
    nxcvb__wtikm = construct_struct(context, builder, typ, lyzm__rllij, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = nxcvb__wtikm
    jhzx__rndr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=jhzx__rndr)


@box(StructType)
def box_struct(typ, val, c):
    pcdfu__tijit = c.pyapi.dict_new(len(typ.data))
    pgd__ydw, yvt__ctpqu = _get_struct_payload(c.context, c.builder, typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(pcdfu__tijit, typ.names[i], c.pyapi.
            borrow_none())
        qubw__swn = c.builder.extract_value(pgd__ydw.null_bitmap, i)
        lxp__mpjsn = c.builder.icmp_unsigned('==', qubw__swn, lir.Constant(
            qubw__swn.type, 1))
        with c.builder.if_then(lxp__mpjsn):
            ptj__covzy = c.builder.extract_value(pgd__ydw.data, i)
            c.context.nrt.incref(c.builder, val_typ, ptj__covzy)
            hust__ewd = c.pyapi.from_native_value(val_typ, ptj__covzy, c.
                env_manager)
            c.pyapi.dict_setitem_string(pcdfu__tijit, typ.names[i], hust__ewd)
            c.pyapi.decref(hust__ewd)
    c.context.nrt.decref(c.builder, typ, val)
    return pcdfu__tijit


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(psdjk__vzna) for psdjk__vzna in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, gza__fjub = args
        payload_type = StructPayloadType(struct_type.data)
        pyp__rbqi = context.get_value_type(payload_type)
        octl__ygzu = context.get_abi_sizeof(pyp__rbqi)
        usbk__qaglw = define_struct_dtor(context, builder, struct_type,
            payload_type)
        nxcvb__wtikm = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, octl__ygzu), usbk__qaglw)
        lsddu__xup = context.nrt.meminfo_data(builder, nxcvb__wtikm)
        ylrt__wlw = builder.bitcast(lsddu__xup, pyp__rbqi.as_pointer())
        pgd__ydw = cgutils.create_struct_proxy(payload_type)(context, builder)
        pgd__ydw.data = data
        pgd__ydw.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for yvt__ctpqu in range(len(
            data_typ.types))])
        builder.store(pgd__ydw._getvalue(), ylrt__wlw)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = nxcvb__wtikm
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        pgd__ydw, yvt__ctpqu = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            pgd__ydw.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        pgd__ydw, yvt__ctpqu = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            pgd__ydw.null_bitmap)
    rscqp__mecm = types.UniTuple(types.int8, len(struct_typ.data))
    return rscqp__mecm(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, yvt__ctpqu, val = args
        pgd__ydw, ylrt__wlw = _get_struct_payload(context, builder,
            struct_typ, struct)
        lgnm__dxj = pgd__ydw.data
        eab__eot = builder.insert_value(lgnm__dxj, val, field_ind)
        rdpi__oxut = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, rdpi__oxut, lgnm__dxj)
        context.nrt.incref(builder, rdpi__oxut, eab__eot)
        pgd__ydw.data = eab__eot
        builder.store(pgd__ydw._getvalue(), ylrt__wlw)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    ucte__dnlms = get_overload_const_str(ind)
    if ucte__dnlms not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            ucte__dnlms, struct))
    return struct.names.index(ucte__dnlms)


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
    pyp__rbqi = context.get_value_type(payload_type)
    octl__ygzu = context.get_abi_sizeof(pyp__rbqi)
    usbk__qaglw = define_struct_dtor(context, builder, struct_type,
        payload_type)
    nxcvb__wtikm = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, octl__ygzu), usbk__qaglw)
    lsddu__xup = context.nrt.meminfo_data(builder, nxcvb__wtikm)
    ylrt__wlw = builder.bitcast(lsddu__xup, pyp__rbqi.as_pointer())
    pgd__ydw = cgutils.create_struct_proxy(payload_type)(context, builder)
    pgd__ydw.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    pgd__ydw.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(pgd__ydw._getvalue(), ylrt__wlw)
    return nxcvb__wtikm


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    omua__lrmll = tuple(d.dtype for d in struct_arr_typ.data)
    kqqi__vgost = StructType(omua__lrmll, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        viq__ndte, ind = args
        pgd__ydw = _get_struct_arr_payload(context, builder, struct_arr_typ,
            viq__ndte)
        lyzm__rllij = []
        jlgia__else = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            pgf__etx = builder.extract_value(pgd__ydw.data, i)
            lzm__lccuh = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [pgf__etx, ind]
                )
            jlgia__else.append(lzm__lccuh)
            estpw__mjtm = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            lxp__mpjsn = builder.icmp_unsigned('==', lzm__lccuh, lir.
                Constant(lzm__lccuh.type, 1))
            with builder.if_then(lxp__mpjsn):
                dxq__chsy = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    pgf__etx, ind])
                builder.store(dxq__chsy, estpw__mjtm)
            lyzm__rllij.append(builder.load(estpw__mjtm))
        if isinstance(kqqi__vgost, types.DictType):
            warhw__ojfi = [context.insert_const_string(builder.module,
                tgqx__exd) for tgqx__exd in struct_arr_typ.names]
            svxkt__vqxfo = cgutils.pack_array(builder, lyzm__rllij)
            swuxc__hnm = cgutils.pack_array(builder, warhw__ojfi)

            def impl(names, vals):
                d = {}
                for i, tgqx__exd in enumerate(names):
                    d[tgqx__exd] = vals[i]
                return d
            jzty__auuk = context.compile_internal(builder, impl,
                kqqi__vgost(types.Tuple(tuple(types.StringLiteral(tgqx__exd
                ) for tgqx__exd in struct_arr_typ.names)), types.Tuple(
                omua__lrmll)), [swuxc__hnm, svxkt__vqxfo])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                omua__lrmll), svxkt__vqxfo)
            return jzty__auuk
        nxcvb__wtikm = construct_struct(context, builder, kqqi__vgost,
            lyzm__rllij, jlgia__else)
        struct = context.make_helper(builder, kqqi__vgost)
        struct.meminfo = nxcvb__wtikm
        return struct._getvalue()
    return kqqi__vgost(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        pgd__ydw = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            pgd__ydw.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        pgd__ydw = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            pgd__ydw.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(psdjk__vzna) for psdjk__vzna in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, djcp__cfl, gza__fjub = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        pyp__rbqi = context.get_value_type(payload_type)
        octl__ygzu = context.get_abi_sizeof(pyp__rbqi)
        usbk__qaglw = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        nxcvb__wtikm = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, octl__ygzu), usbk__qaglw)
        lsddu__xup = context.nrt.meminfo_data(builder, nxcvb__wtikm)
        ylrt__wlw = builder.bitcast(lsddu__xup, pyp__rbqi.as_pointer())
        pgd__ydw = cgutils.create_struct_proxy(payload_type)(context, builder)
        pgd__ydw.data = data
        pgd__ydw.null_bitmap = djcp__cfl
        builder.store(pgd__ydw._getvalue(), ylrt__wlw)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, djcp__cfl)
        borj__qgws = context.make_helper(builder, struct_arr_type)
        borj__qgws.meminfo = nxcvb__wtikm
        return borj__qgws._getvalue()
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
    lxsnz__dejg = len(arr.data)
    xpaxj__fmuay = 'def impl(arr, ind):\n'
    xpaxj__fmuay += '  data = get_data(arr)\n'
    xpaxj__fmuay += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        xpaxj__fmuay += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        xpaxj__fmuay += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        xpaxj__fmuay += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    xpaxj__fmuay += (
        '  return init_struct_arr(({},), out_null_bitmap, ({},))\n'.format(
        ', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for i in
        range(lxsnz__dejg)), ', '.join("'{}'".format(tgqx__exd) for
        tgqx__exd in arr.names)))
    nocgk__hfhbq = {}
    exec(xpaxj__fmuay, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, nocgk__hfhbq)
    impl = nocgk__hfhbq['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        lxsnz__dejg = len(arr.data)
        xpaxj__fmuay = 'def impl(arr, ind, val):\n'
        xpaxj__fmuay += '  data = get_data(arr)\n'
        xpaxj__fmuay += '  null_bitmap = get_null_bitmap(arr)\n'
        xpaxj__fmuay += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(lxsnz__dejg):
            if isinstance(val, StructType):
                xpaxj__fmuay += ("  if is_field_value_null(val, '{}'):\n".
                    format(arr.names[i]))
                xpaxj__fmuay += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                xpaxj__fmuay += '  else:\n'
                xpaxj__fmuay += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                xpaxj__fmuay += "  data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
        nocgk__hfhbq = {}
        exec(xpaxj__fmuay, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, nocgk__hfhbq)
        impl = nocgk__hfhbq['impl']
        return impl
    if isinstance(ind, types.SliceType):
        lxsnz__dejg = len(arr.data)
        xpaxj__fmuay = 'def impl(arr, ind, val):\n'
        xpaxj__fmuay += '  data = get_data(arr)\n'
        xpaxj__fmuay += '  null_bitmap = get_null_bitmap(arr)\n'
        xpaxj__fmuay += '  val_data = get_data(val)\n'
        xpaxj__fmuay += '  val_null_bitmap = get_null_bitmap(val)\n'
        xpaxj__fmuay += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(lxsnz__dejg):
            xpaxj__fmuay += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        nocgk__hfhbq = {}
        exec(xpaxj__fmuay, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, nocgk__hfhbq)
        impl = nocgk__hfhbq['impl']
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
    xpaxj__fmuay = 'def impl(A):\n'
    xpaxj__fmuay += '  total_nbytes = 0\n'
    xpaxj__fmuay += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        xpaxj__fmuay += f'  total_nbytes += data[{i}].nbytes\n'
    xpaxj__fmuay += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    xpaxj__fmuay += '  return total_nbytes\n'
    nocgk__hfhbq = {}
    exec(xpaxj__fmuay, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, nocgk__hfhbq)
    impl = nocgk__hfhbq['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        djcp__cfl = get_null_bitmap(A)
        tzrpp__ldstb = bodo.ir.join.copy_arr_tup(data)
        ndyos__ili = djcp__cfl.copy()
        return init_struct_arr(tzrpp__ldstb, ndyos__ili, names)
    return copy_impl
