"""Array implementation for map values.
Corresponds to Spark's MapType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Map arrays: https://github.com/apache/arrow/blob/master/format/Schema.fbs

The implementation uses an array(struct) array underneath similar to Spark and Arrow.
For example: [{1: 2.1, 3: 1.1}, {5: -1.0}]
[[{"key": 1, "value" 2.1}, {"key": 3, "value": 1.1}], [{"key": 5, "value": -1.0}]]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, _get_array_item_arr_payload, offset_type
from bodo.libs.struct_arr_ext import StructArrayType, _get_struct_arr_payload
from bodo.utils.cg_helpers import dict_keys, dict_merge_from_seq2, dict_values, gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit
from bodo.utils.typing import BodoError
from bodo.libs import array_ext, hdist
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('map_array_from_sequence', array_ext.map_array_from_sequence)
ll.add_symbol('np_array_from_map_array', array_ext.np_array_from_map_array)


class MapArrayType(types.ArrayCompatible):

    def __init__(self, key_arr_type, value_arr_type):
        self.key_arr_type = key_arr_type
        self.value_arr_type = value_arr_type
        super(MapArrayType, self).__init__(name='MapArrayType({}, {})'.
            format(key_arr_type, value_arr_type))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.DictType(self.key_arr_type.dtype, self.value_arr_type.
            dtype)

    def copy(self):
        return MapArrayType(self.key_arr_type, self.value_arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_map_arr_data_type(map_type):
    twqqx__uosz = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(twqqx__uosz)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ljwrr__axfjo = _get_map_arr_data_type(fe_type)
        wnazl__jtp = [('data', ljwrr__axfjo)]
        models.StructModel.__init__(self, dmm, fe_type, wnazl__jtp)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    oxs__wbw = all(isinstance(ccdod__mnud, types.Array) and ccdod__mnud.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for ccdod__mnud in (typ.key_arr_type, typ.
        value_arr_type))
    if oxs__wbw:
        vbg__qmr = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        ryb__stbg = cgutils.get_or_insert_function(c.builder.module,
            vbg__qmr, name='count_total_elems_list_array')
        nalck__nkzbq = cgutils.pack_array(c.builder, [n_maps, c.builder.
            call(ryb__stbg, [val])])
    else:
        nalck__nkzbq = get_array_elem_counts(c, c.builder, c.context, val, typ)
    ljwrr__axfjo = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, ljwrr__axfjo,
        nalck__nkzbq, c)
    uxf__gpyo = _get_array_item_arr_payload(c.context, c.builder,
        ljwrr__axfjo, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, uxf__gpyo.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, uxf__gpyo.offsets).data
    mcw__exj = _get_struct_arr_payload(c.context, c.builder, ljwrr__axfjo.
        dtype, uxf__gpyo.data)
    key_arr = c.builder.extract_value(mcw__exj.data, 0)
    value_arr = c.builder.extract_value(mcw__exj.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    lmm__knust, mpxg__iyk = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [mcw__exj.null_bitmap])
    if oxs__wbw:
        nkr__mejy = c.context.make_array(ljwrr__axfjo.dtype.data[0])(c.
            context, c.builder, key_arr).data
        lqk__kdvb = c.context.make_array(ljwrr__axfjo.dtype.data[1])(c.
            context, c.builder, value_arr).data
        vbg__qmr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        mtey__wknod = cgutils.get_or_insert_function(c.builder.module,
            vbg__qmr, name='map_array_from_sequence')
        macdr__ictrp = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        afeb__focx = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(mtey__wknod, [val, c.builder.bitcast(nkr__mejy, lir.
            IntType(8).as_pointer()), c.builder.bitcast(lqk__kdvb, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), macdr__ictrp), lir.Constant(lir.
            IntType(32), afeb__focx)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    zatwp__orosa = c.context.make_helper(c.builder, typ)
    zatwp__orosa.data = data_arr
    hzo__ntkzn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zatwp__orosa._getvalue(), is_error=hzo__ntkzn)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    fvuhf__plh = context.insert_const_string(builder.module, 'pandas')
    hloc__ukg = c.pyapi.import_module_noblock(fvuhf__plh)
    sxmr__zilf = c.pyapi.object_getattr_string(hloc__ukg, 'NA')
    qoakn__zdr = c.context.get_constant(offset_type, 0)
    builder.store(qoakn__zdr, offsets_ptr)
    gzj__tahqz = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as ugm__knt:
        ctg__jus = ugm__knt.index
        item_ind = builder.load(gzj__tahqz)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [ctg__jus]))
        xquk__cdtij = seq_getitem(builder, context, val, ctg__jus)
        set_bitmap_bit(builder, null_bitmap_ptr, ctg__jus, 0)
        eusa__hux = is_na_value(builder, context, xquk__cdtij, sxmr__zilf)
        ijgn__wma = builder.icmp_unsigned('!=', eusa__hux, lir.Constant(
            eusa__hux.type, 1))
        with builder.if_then(ijgn__wma):
            set_bitmap_bit(builder, null_bitmap_ptr, ctg__jus, 1)
            ryqkc__zukt = dict_keys(builder, context, xquk__cdtij)
            otw__bdwt = dict_values(builder, context, xquk__cdtij)
            n_items = bodo.utils.utils.object_length(c, ryqkc__zukt)
            _unbox_array_item_array_copy_data(typ.key_arr_type, ryqkc__zukt,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type, otw__bdwt,
                c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), gzj__tahqz)
            c.pyapi.decref(ryqkc__zukt)
            c.pyapi.decref(otw__bdwt)
        c.pyapi.decref(xquk__cdtij)
    builder.store(builder.trunc(builder.load(gzj__tahqz), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(hloc__ukg)
    c.pyapi.decref(sxmr__zilf)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    zatwp__orosa = c.context.make_helper(c.builder, typ, val)
    data_arr = zatwp__orosa.data
    ljwrr__axfjo = _get_map_arr_data_type(typ)
    uxf__gpyo = _get_array_item_arr_payload(c.context, c.builder,
        ljwrr__axfjo, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, uxf__gpyo.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, uxf__gpyo.offsets).data
    mcw__exj = _get_struct_arr_payload(c.context, c.builder, ljwrr__axfjo.
        dtype, uxf__gpyo.data)
    key_arr = c.builder.extract_value(mcw__exj.data, 0)
    value_arr = c.builder.extract_value(mcw__exj.data, 1)
    if all(isinstance(ccdod__mnud, types.Array) and ccdod__mnud.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type) for
        ccdod__mnud in (typ.key_arr_type, typ.value_arr_type)):
        nkr__mejy = c.context.make_array(ljwrr__axfjo.dtype.data[0])(c.
            context, c.builder, key_arr).data
        lqk__kdvb = c.context.make_array(ljwrr__axfjo.dtype.data[1])(c.
            context, c.builder, value_arr).data
        vbg__qmr = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        rkcsn__ayc = cgutils.get_or_insert_function(c.builder.module,
            vbg__qmr, name='np_array_from_map_array')
        macdr__ictrp = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        afeb__focx = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(rkcsn__ayc, [uxf__gpyo.n_arrays, c.builder.
            bitcast(nkr__mejy, lir.IntType(8).as_pointer()), c.builder.
            bitcast(lqk__kdvb, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), macdr__ictrp),
            lir.Constant(lir.IntType(32), afeb__focx)])
    else:
        arr = _box_map_array_generic(typ, c, uxf__gpyo.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    fvuhf__plh = context.insert_const_string(builder.module, 'numpy')
    zcoez__ocpp = c.pyapi.import_module_noblock(fvuhf__plh)
    tyf__oeo = c.pyapi.object_getattr_string(zcoez__ocpp, 'object_')
    wzps__rnie = c.pyapi.long_from_longlong(n_maps)
    qxswx__hzu = c.pyapi.call_method(zcoez__ocpp, 'ndarray', (wzps__rnie,
        tyf__oeo))
    gbhfc__wgk = c.pyapi.object_getattr_string(zcoez__ocpp, 'nan')
    vlbqp__jbua = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    gzj__tahqz = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as ugm__knt:
        hpff__moyb = ugm__knt.index
        pyarray_setitem(builder, context, qxswx__hzu, hpff__moyb, gbhfc__wgk)
        zgr__cear = get_bitmap_bit(builder, null_bitmap_ptr, hpff__moyb)
        iuj__veqaf = builder.icmp_unsigned('!=', zgr__cear, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(iuj__veqaf):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(hpff__moyb, lir.Constant(
                hpff__moyb.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [hpff__moyb]))), lir.IntType(64))
            item_ind = builder.load(gzj__tahqz)
            xquk__cdtij = c.pyapi.dict_new()
            cbzcd__emzd = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            lmm__knust, cuo__xpdb = c.pyapi.call_jit_code(cbzcd__emzd, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            lmm__knust, gqo__aivhk = c.pyapi.call_jit_code(cbzcd__emzd, typ
                .value_arr_type(typ.value_arr_type, types.int64, types.
                int64), [value_arr, item_ind, n_items])
            rfda__jcoy = c.pyapi.from_native_value(typ.key_arr_type,
                cuo__xpdb, c.env_manager)
            kuqul__ehlc = c.pyapi.from_native_value(typ.value_arr_type,
                gqo__aivhk, c.env_manager)
            ttej__pxu = c.pyapi.call_function_objargs(vlbqp__jbua, (
                rfda__jcoy, kuqul__ehlc))
            dict_merge_from_seq2(builder, context, xquk__cdtij, ttej__pxu)
            builder.store(builder.add(item_ind, n_items), gzj__tahqz)
            pyarray_setitem(builder, context, qxswx__hzu, hpff__moyb,
                xquk__cdtij)
            c.pyapi.decref(ttej__pxu)
            c.pyapi.decref(rfda__jcoy)
            c.pyapi.decref(kuqul__ehlc)
            c.pyapi.decref(xquk__cdtij)
    c.pyapi.decref(vlbqp__jbua)
    c.pyapi.decref(zcoez__ocpp)
    c.pyapi.decref(tyf__oeo)
    c.pyapi.decref(wzps__rnie)
    c.pyapi.decref(gbhfc__wgk)
    return qxswx__hzu


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    zatwp__orosa = context.make_helper(builder, sig.return_type)
    zatwp__orosa.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return zatwp__orosa._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    auox__jgk = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return auox__jgk(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    ttg__klwe = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(ttg__klwe)


def pre_alloc_map_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_map_arr_ext_pre_alloc_map_array
    ) = pre_alloc_map_array_equiv


@overload(len, no_unliteral=True)
def overload_map_arr_len(A):
    if isinstance(A, MapArrayType):
        return lambda A: len(A._data)


@overload_attribute(MapArrayType, 'shape')
def overload_map_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(MapArrayType, 'dtype')
def overload_map_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(MapArrayType, 'ndim')
def overload_map_arr_ndim(A):
    return lambda A: 1


@overload_attribute(MapArrayType, 'nbytes')
def overload_map_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(MapArrayType, 'copy')
def overload_map_arr_copy(A):
    return lambda A: init_map_arr(A._data.copy())


@overload(operator.setitem, no_unliteral=True)
def map_arr_setitem(arr, ind, val):
    if not isinstance(arr, MapArrayType):
        return
    hvbdr__bqgcj = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            dyoh__kmq = val.keys()
            wvi__bciom = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), hvbdr__bqgcj, ('key', 'value'))
            for nrj__pijxn, slzhi__mnqrt in enumerate(dyoh__kmq):
                wvi__bciom[nrj__pijxn] = bodo.libs.struct_arr_ext.init_struct((
                    slzhi__mnqrt, val[slzhi__mnqrt]), ('key', 'value'))
            arr._data[ind] = wvi__bciom
        return map_arr_setitem_impl
    raise BodoError(
        'operator.setitem with MapArrays is only supported with an integer index.'
        )


@overload(operator.getitem, no_unliteral=True)
def map_arr_getitem(arr, ind):
    if not isinstance(arr, MapArrayType):
        return
    if isinstance(ind, types.Integer):

        def map_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            ktvd__vgt = dict()
            uyzcf__tbiga = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            wvi__bciom = bodo.libs.array_item_arr_ext.get_data(arr._data)
            pht__ttenp, apeew__vowlm = bodo.libs.struct_arr_ext.get_data(
                wvi__bciom)
            wse__cidfa = uyzcf__tbiga[ind]
            kph__sqf = uyzcf__tbiga[ind + 1]
            for nrj__pijxn in range(wse__cidfa, kph__sqf):
                ktvd__vgt[pht__ttenp[nrj__pijxn]] = apeew__vowlm[nrj__pijxn]
            return ktvd__vgt
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
