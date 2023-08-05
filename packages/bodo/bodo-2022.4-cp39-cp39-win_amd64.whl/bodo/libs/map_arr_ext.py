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
    gkrl__sypj = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(gkrl__sypj)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        frv__lsjpg = _get_map_arr_data_type(fe_type)
        pmvcr__bmn = [('data', frv__lsjpg)]
        models.StructModel.__init__(self, dmm, fe_type, pmvcr__bmn)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    dror__eepzy = all(isinstance(swtei__ccy, types.Array) and swtei__ccy.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for swtei__ccy in (typ.key_arr_type, typ.
        value_arr_type))
    if dror__eepzy:
        rie__bps = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        xshr__cqza = cgutils.get_or_insert_function(c.builder.module,
            rie__bps, name='count_total_elems_list_array')
        wqvm__elxvb = cgutils.pack_array(c.builder, [n_maps, c.builder.call
            (xshr__cqza, [val])])
    else:
        wqvm__elxvb = get_array_elem_counts(c, c.builder, c.context, val, typ)
    frv__lsjpg = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, frv__lsjpg,
        wqvm__elxvb, c)
    rzcyb__ibz = _get_array_item_arr_payload(c.context, c.builder,
        frv__lsjpg, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, rzcyb__ibz.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, rzcyb__ibz.offsets).data
    vsp__legwt = _get_struct_arr_payload(c.context, c.builder, frv__lsjpg.
        dtype, rzcyb__ibz.data)
    key_arr = c.builder.extract_value(vsp__legwt.data, 0)
    value_arr = c.builder.extract_value(vsp__legwt.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    tfba__vofa, cge__pqct = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [vsp__legwt.null_bitmap])
    if dror__eepzy:
        tsz__nfeen = c.context.make_array(frv__lsjpg.dtype.data[0])(c.
            context, c.builder, key_arr).data
        fya__nokze = c.context.make_array(frv__lsjpg.dtype.data[1])(c.
            context, c.builder, value_arr).data
        rie__bps = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        ayw__cdla = cgutils.get_or_insert_function(c.builder.module,
            rie__bps, name='map_array_from_sequence')
        dks__gmvy = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        dbhp__jnn = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(ayw__cdla, [val, c.builder.bitcast(tsz__nfeen, lir.
            IntType(8).as_pointer()), c.builder.bitcast(fya__nokze, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), dks__gmvy), lir.Constant(lir.IntType(
            32), dbhp__jnn)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    wzfe__jcou = c.context.make_helper(c.builder, typ)
    wzfe__jcou.data = data_arr
    znzb__ulwm = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wzfe__jcou._getvalue(), is_error=znzb__ulwm)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    bewg__mspyq = context.insert_const_string(builder.module, 'pandas')
    ayl__jcan = c.pyapi.import_module_noblock(bewg__mspyq)
    sirlz__oebfm = c.pyapi.object_getattr_string(ayl__jcan, 'NA')
    kkb__ujny = c.context.get_constant(offset_type, 0)
    builder.store(kkb__ujny, offsets_ptr)
    ihshd__oqpp = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as akr__pzl:
        xfu__xnyb = akr__pzl.index
        item_ind = builder.load(ihshd__oqpp)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [xfu__xnyb]))
        jdioo__srso = seq_getitem(builder, context, val, xfu__xnyb)
        set_bitmap_bit(builder, null_bitmap_ptr, xfu__xnyb, 0)
        wmslp__wxp = is_na_value(builder, context, jdioo__srso, sirlz__oebfm)
        zjcvx__trryp = builder.icmp_unsigned('!=', wmslp__wxp, lir.Constant
            (wmslp__wxp.type, 1))
        with builder.if_then(zjcvx__trryp):
            set_bitmap_bit(builder, null_bitmap_ptr, xfu__xnyb, 1)
            ydgd__zrsor = dict_keys(builder, context, jdioo__srso)
            pef__mxan = dict_values(builder, context, jdioo__srso)
            n_items = bodo.utils.utils.object_length(c, ydgd__zrsor)
            _unbox_array_item_array_copy_data(typ.key_arr_type, ydgd__zrsor,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type, pef__mxan,
                c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), ihshd__oqpp)
            c.pyapi.decref(ydgd__zrsor)
            c.pyapi.decref(pef__mxan)
        c.pyapi.decref(jdioo__srso)
    builder.store(builder.trunc(builder.load(ihshd__oqpp), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(ayl__jcan)
    c.pyapi.decref(sirlz__oebfm)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    wzfe__jcou = c.context.make_helper(c.builder, typ, val)
    data_arr = wzfe__jcou.data
    frv__lsjpg = _get_map_arr_data_type(typ)
    rzcyb__ibz = _get_array_item_arr_payload(c.context, c.builder,
        frv__lsjpg, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, rzcyb__ibz.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, rzcyb__ibz.offsets).data
    vsp__legwt = _get_struct_arr_payload(c.context, c.builder, frv__lsjpg.
        dtype, rzcyb__ibz.data)
    key_arr = c.builder.extract_value(vsp__legwt.data, 0)
    value_arr = c.builder.extract_value(vsp__legwt.data, 1)
    if all(isinstance(swtei__ccy, types.Array) and swtei__ccy.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type) for
        swtei__ccy in (typ.key_arr_type, typ.value_arr_type)):
        tsz__nfeen = c.context.make_array(frv__lsjpg.dtype.data[0])(c.
            context, c.builder, key_arr).data
        fya__nokze = c.context.make_array(frv__lsjpg.dtype.data[1])(c.
            context, c.builder, value_arr).data
        rie__bps = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        uotfr__sdxs = cgutils.get_or_insert_function(c.builder.module,
            rie__bps, name='np_array_from_map_array')
        dks__gmvy = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        dbhp__jnn = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(uotfr__sdxs, [rzcyb__ibz.n_arrays, c.builder.
            bitcast(tsz__nfeen, lir.IntType(8).as_pointer()), c.builder.
            bitcast(fya__nokze, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), dks__gmvy), lir.
            Constant(lir.IntType(32), dbhp__jnn)])
    else:
        arr = _box_map_array_generic(typ, c, rzcyb__ibz.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    bewg__mspyq = context.insert_const_string(builder.module, 'numpy')
    tklop__dwgv = c.pyapi.import_module_noblock(bewg__mspyq)
    kyb__jnpo = c.pyapi.object_getattr_string(tklop__dwgv, 'object_')
    iaj__plml = c.pyapi.long_from_longlong(n_maps)
    nwciy__dmq = c.pyapi.call_method(tklop__dwgv, 'ndarray', (iaj__plml,
        kyb__jnpo))
    iwtc__fwn = c.pyapi.object_getattr_string(tklop__dwgv, 'nan')
    qsbc__ahnex = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    ihshd__oqpp = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as akr__pzl:
        bzk__kmhxo = akr__pzl.index
        pyarray_setitem(builder, context, nwciy__dmq, bzk__kmhxo, iwtc__fwn)
        kqxd__elyry = get_bitmap_bit(builder, null_bitmap_ptr, bzk__kmhxo)
        rkv__zqzqd = builder.icmp_unsigned('!=', kqxd__elyry, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(rkv__zqzqd):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(bzk__kmhxo, lir.Constant(
                bzk__kmhxo.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [bzk__kmhxo]))), lir.IntType(64))
            item_ind = builder.load(ihshd__oqpp)
            jdioo__srso = c.pyapi.dict_new()
            lvc__vhiiq = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            tfba__vofa, npgf__msti = c.pyapi.call_jit_code(lvc__vhiiq, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            tfba__vofa, evaap__ybwm = c.pyapi.call_jit_code(lvc__vhiiq, typ
                .value_arr_type(typ.value_arr_type, types.int64, types.
                int64), [value_arr, item_ind, n_items])
            crt__jhtsp = c.pyapi.from_native_value(typ.key_arr_type,
                npgf__msti, c.env_manager)
            zkhb__hpxzr = c.pyapi.from_native_value(typ.value_arr_type,
                evaap__ybwm, c.env_manager)
            dfls__phrk = c.pyapi.call_function_objargs(qsbc__ahnex, (
                crt__jhtsp, zkhb__hpxzr))
            dict_merge_from_seq2(builder, context, jdioo__srso, dfls__phrk)
            builder.store(builder.add(item_ind, n_items), ihshd__oqpp)
            pyarray_setitem(builder, context, nwciy__dmq, bzk__kmhxo,
                jdioo__srso)
            c.pyapi.decref(dfls__phrk)
            c.pyapi.decref(crt__jhtsp)
            c.pyapi.decref(zkhb__hpxzr)
            c.pyapi.decref(jdioo__srso)
    c.pyapi.decref(qsbc__ahnex)
    c.pyapi.decref(tklop__dwgv)
    c.pyapi.decref(kyb__jnpo)
    c.pyapi.decref(iaj__plml)
    c.pyapi.decref(iwtc__fwn)
    return nwciy__dmq


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    wzfe__jcou = context.make_helper(builder, sig.return_type)
    wzfe__jcou.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return wzfe__jcou._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    diulq__liqp = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return diulq__liqp(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    mcpor__jwpl = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(mcpor__jwpl)


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
    wlnls__opd = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            xdlz__qugnl = val.keys()
            mkvey__wdlq = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), wlnls__opd, ('key', 'value'))
            for qicny__quq, idzlb__hiarz in enumerate(xdlz__qugnl):
                mkvey__wdlq[qicny__quq] = bodo.libs.struct_arr_ext.init_struct(
                    (idzlb__hiarz, val[idzlb__hiarz]), ('key', 'value'))
            arr._data[ind] = mkvey__wdlq
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
            ihx__ked = dict()
            mwbpo__ijrf = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            mkvey__wdlq = bodo.libs.array_item_arr_ext.get_data(arr._data)
            atin__pru, iltjy__bev = bodo.libs.struct_arr_ext.get_data(
                mkvey__wdlq)
            qncdg__bgv = mwbpo__ijrf[ind]
            snrh__znohw = mwbpo__ijrf[ind + 1]
            for qicny__quq in range(qncdg__bgv, snrh__znohw):
                ihx__ked[atin__pru[qicny__quq]] = iltjy__bev[qicny__quq]
            return ihx__ked
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
