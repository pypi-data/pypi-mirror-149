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
    rlb__pcl = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(rlb__pcl)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wbleu__nlcnc = _get_map_arr_data_type(fe_type)
        ftfr__rmnx = [('data', wbleu__nlcnc)]
        models.StructModel.__init__(self, dmm, fe_type, ftfr__rmnx)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    jdcsn__loh = all(isinstance(eok__fwlzm, types.Array) and eok__fwlzm.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for eok__fwlzm in (typ.key_arr_type, typ.
        value_arr_type))
    if jdcsn__loh:
        tgy__khc = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        ppm__tjv = cgutils.get_or_insert_function(c.builder.module,
            tgy__khc, name='count_total_elems_list_array')
        yhrho__xjfrv = cgutils.pack_array(c.builder, [n_maps, c.builder.
            call(ppm__tjv, [val])])
    else:
        yhrho__xjfrv = get_array_elem_counts(c, c.builder, c.context, val, typ)
    wbleu__nlcnc = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, wbleu__nlcnc,
        yhrho__xjfrv, c)
    zqq__vzdta = _get_array_item_arr_payload(c.context, c.builder,
        wbleu__nlcnc, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, zqq__vzdta.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, zqq__vzdta.offsets).data
    wstk__awn = _get_struct_arr_payload(c.context, c.builder, wbleu__nlcnc.
        dtype, zqq__vzdta.data)
    key_arr = c.builder.extract_value(wstk__awn.data, 0)
    value_arr = c.builder.extract_value(wstk__awn.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    uqac__dtqz, qyyzi__yqh = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [wstk__awn.null_bitmap])
    if jdcsn__loh:
        nmj__pri = c.context.make_array(wbleu__nlcnc.dtype.data[0])(c.
            context, c.builder, key_arr).data
        rslp__wqo = c.context.make_array(wbleu__nlcnc.dtype.data[1])(c.
            context, c.builder, value_arr).data
        tgy__khc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        xnpq__mhxij = cgutils.get_or_insert_function(c.builder.module,
            tgy__khc, name='map_array_from_sequence')
        xnsr__fjn = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        raj__oxr = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(xnpq__mhxij, [val, c.builder.bitcast(nmj__pri, lir.
            IntType(8).as_pointer()), c.builder.bitcast(rslp__wqo, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), xnsr__fjn), lir.Constant(lir.IntType(
            32), raj__oxr)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    yszig__vze = c.context.make_helper(c.builder, typ)
    yszig__vze.data = data_arr
    sllk__fmfu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yszig__vze._getvalue(), is_error=sllk__fmfu)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    gujc__kmcc = context.insert_const_string(builder.module, 'pandas')
    ucbk__mxbw = c.pyapi.import_module_noblock(gujc__kmcc)
    rvpcp__kyd = c.pyapi.object_getattr_string(ucbk__mxbw, 'NA')
    okfgh__seca = c.context.get_constant(offset_type, 0)
    builder.store(okfgh__seca, offsets_ptr)
    tjz__xyg = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as rfmxp__lugce:
        aehoe__ipaj = rfmxp__lugce.index
        item_ind = builder.load(tjz__xyg)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [aehoe__ipaj]))
        vff__ycj = seq_getitem(builder, context, val, aehoe__ipaj)
        set_bitmap_bit(builder, null_bitmap_ptr, aehoe__ipaj, 0)
        lsg__thx = is_na_value(builder, context, vff__ycj, rvpcp__kyd)
        czmue__wrkm = builder.icmp_unsigned('!=', lsg__thx, lir.Constant(
            lsg__thx.type, 1))
        with builder.if_then(czmue__wrkm):
            set_bitmap_bit(builder, null_bitmap_ptr, aehoe__ipaj, 1)
            syva__mpoy = dict_keys(builder, context, vff__ycj)
            goowz__zas = dict_values(builder, context, vff__ycj)
            n_items = bodo.utils.utils.object_length(c, syva__mpoy)
            _unbox_array_item_array_copy_data(typ.key_arr_type, syva__mpoy,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                goowz__zas, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), tjz__xyg)
            c.pyapi.decref(syva__mpoy)
            c.pyapi.decref(goowz__zas)
        c.pyapi.decref(vff__ycj)
    builder.store(builder.trunc(builder.load(tjz__xyg), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(ucbk__mxbw)
    c.pyapi.decref(rvpcp__kyd)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    yszig__vze = c.context.make_helper(c.builder, typ, val)
    data_arr = yszig__vze.data
    wbleu__nlcnc = _get_map_arr_data_type(typ)
    zqq__vzdta = _get_array_item_arr_payload(c.context, c.builder,
        wbleu__nlcnc, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, zqq__vzdta.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, zqq__vzdta.offsets).data
    wstk__awn = _get_struct_arr_payload(c.context, c.builder, wbleu__nlcnc.
        dtype, zqq__vzdta.data)
    key_arr = c.builder.extract_value(wstk__awn.data, 0)
    value_arr = c.builder.extract_value(wstk__awn.data, 1)
    if all(isinstance(eok__fwlzm, types.Array) and eok__fwlzm.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type) for
        eok__fwlzm in (typ.key_arr_type, typ.value_arr_type)):
        nmj__pri = c.context.make_array(wbleu__nlcnc.dtype.data[0])(c.
            context, c.builder, key_arr).data
        rslp__wqo = c.context.make_array(wbleu__nlcnc.dtype.data[1])(c.
            context, c.builder, value_arr).data
        tgy__khc = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        nttaq__rhn = cgutils.get_or_insert_function(c.builder.module,
            tgy__khc, name='np_array_from_map_array')
        xnsr__fjn = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        raj__oxr = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(nttaq__rhn, [zqq__vzdta.n_arrays, c.builder.
            bitcast(nmj__pri, lir.IntType(8).as_pointer()), c.builder.
            bitcast(rslp__wqo, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), xnsr__fjn), lir.
            Constant(lir.IntType(32), raj__oxr)])
    else:
        arr = _box_map_array_generic(typ, c, zqq__vzdta.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    gujc__kmcc = context.insert_const_string(builder.module, 'numpy')
    mdgn__qxyxr = c.pyapi.import_module_noblock(gujc__kmcc)
    cjf__degp = c.pyapi.object_getattr_string(mdgn__qxyxr, 'object_')
    sfpsz__ktyw = c.pyapi.long_from_longlong(n_maps)
    jeuk__zykg = c.pyapi.call_method(mdgn__qxyxr, 'ndarray', (sfpsz__ktyw,
        cjf__degp))
    obnag__kpegb = c.pyapi.object_getattr_string(mdgn__qxyxr, 'nan')
    rmbsk__fusq = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    tjz__xyg = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType(
        64), 0))
    with cgutils.for_range(builder, n_maps) as rfmxp__lugce:
        xvmzb__dzhj = rfmxp__lugce.index
        pyarray_setitem(builder, context, jeuk__zykg, xvmzb__dzhj, obnag__kpegb
            )
        zeqo__roxvw = get_bitmap_bit(builder, null_bitmap_ptr, xvmzb__dzhj)
        tqhx__qpvrj = builder.icmp_unsigned('!=', zeqo__roxvw, lir.Constant
            (lir.IntType(8), 0))
        with builder.if_then(tqhx__qpvrj):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(xvmzb__dzhj, lir.Constant(
                xvmzb__dzhj.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [xvmzb__dzhj]))), lir.IntType(64))
            item_ind = builder.load(tjz__xyg)
            vff__ycj = c.pyapi.dict_new()
            llq__drvt = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            uqac__dtqz, ddg__ngf = c.pyapi.call_jit_code(llq__drvt, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            uqac__dtqz, yeafk__izcu = c.pyapi.call_jit_code(llq__drvt, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            ilwop__lisn = c.pyapi.from_native_value(typ.key_arr_type,
                ddg__ngf, c.env_manager)
            jts__fcmyc = c.pyapi.from_native_value(typ.value_arr_type,
                yeafk__izcu, c.env_manager)
            efft__fbks = c.pyapi.call_function_objargs(rmbsk__fusq, (
                ilwop__lisn, jts__fcmyc))
            dict_merge_from_seq2(builder, context, vff__ycj, efft__fbks)
            builder.store(builder.add(item_ind, n_items), tjz__xyg)
            pyarray_setitem(builder, context, jeuk__zykg, xvmzb__dzhj, vff__ycj
                )
            c.pyapi.decref(efft__fbks)
            c.pyapi.decref(ilwop__lisn)
            c.pyapi.decref(jts__fcmyc)
            c.pyapi.decref(vff__ycj)
    c.pyapi.decref(rmbsk__fusq)
    c.pyapi.decref(mdgn__qxyxr)
    c.pyapi.decref(cjf__degp)
    c.pyapi.decref(sfpsz__ktyw)
    c.pyapi.decref(obnag__kpegb)
    return jeuk__zykg


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    yszig__vze = context.make_helper(builder, sig.return_type)
    yszig__vze.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return yszig__vze._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    cykab__wjbu = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return cykab__wjbu(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    llq__hprmh = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(llq__hprmh)


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
    gjodu__cupf = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            rfwu__gjj = val.keys()
            qfv__fjnao = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), gjodu__cupf, ('key', 'value'))
            for kgem__uxb, fmb__xqaym in enumerate(rfwu__gjj):
                qfv__fjnao[kgem__uxb] = bodo.libs.struct_arr_ext.init_struct((
                    fmb__xqaym, val[fmb__xqaym]), ('key', 'value'))
            arr._data[ind] = qfv__fjnao
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
            jqhqu__dzic = dict()
            ssvu__pxr = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            qfv__fjnao = bodo.libs.array_item_arr_ext.get_data(arr._data)
            ebsn__adkut, fgy__eycu = bodo.libs.struct_arr_ext.get_data(
                qfv__fjnao)
            bya__zczr = ssvu__pxr[ind]
            myhx__tacpl = ssvu__pxr[ind + 1]
            for kgem__uxb in range(bya__zczr, myhx__tacpl):
                jqhqu__dzic[ebsn__adkut[kgem__uxb]] = fgy__eycu[kgem__uxb]
            return jqhqu__dzic
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
