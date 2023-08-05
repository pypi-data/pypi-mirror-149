"""Nullable boolean array that stores data in Numpy format (1 byte per value)
but nulls are stored in bit arrays (1 bit per value) similar to Arrow's nulls.
Pandas converts boolean array to object when NAs are introduced.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import is_list_like_index_type
ll.add_symbol('is_bool_array', hstr_ext.is_bool_array)
ll.add_symbol('is_pd_boolean_array', hstr_ext.is_pd_boolean_array)
ll.add_symbol('unbox_bool_array_obj', hstr_ext.unbox_bool_array_obj)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_overload_false, is_overload_true, parse_dtype, raise_bodo_error


class BooleanArrayType(types.ArrayCompatible):

    def __init__(self):
        super(BooleanArrayType, self).__init__(name='BooleanArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.bool_

    def copy(self):
        return BooleanArrayType()


boolean_array = BooleanArrayType()


@typeof_impl.register(pd.arrays.BooleanArray)
def typeof_boolean_array(val, c):
    return boolean_array


data_type = types.Array(types.bool_, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(BooleanArrayType)
class BooleanArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        tgim__vupuq = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, tgim__vupuq)


make_attribute_wrapper(BooleanArrayType, 'data', '_data')
make_attribute_wrapper(BooleanArrayType, 'null_bitmap', '_null_bitmap')


class BooleanDtype(types.Number):

    def __init__(self):
        self.dtype = types.bool_
        super(BooleanDtype, self).__init__('BooleanDtype')


boolean_dtype = BooleanDtype()
register_model(BooleanDtype)(models.OpaqueModel)


@box(BooleanDtype)
def box_boolean_dtype(typ, val, c):
    himwy__zgvu = c.context.insert_const_string(c.builder.module, 'pandas')
    raz__fbqc = c.pyapi.import_module_noblock(himwy__zgvu)
    wrqta__bomtv = c.pyapi.call_method(raz__fbqc, 'BooleanDtype', ())
    c.pyapi.decref(raz__fbqc)
    return wrqta__bomtv


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    nqcj__ajx = n + 7 >> 3
    return np.full(nqcj__ajx, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    rej__gcmg = c.context.typing_context.resolve_value_type(func)
    igz__roa = rej__gcmg.get_call_type(c.context.typing_context, arg_typs, {})
    zch__pvo = c.context.get_function(rej__gcmg, igz__roa)
    haqr__yujg = c.context.call_conv.get_function_type(igz__roa.return_type,
        igz__roa.args)
    iqaff__hwuho = c.builder.module
    pgka__uxcnf = lir.Function(iqaff__hwuho, haqr__yujg, name=iqaff__hwuho.
        get_unique_name('.func_conv'))
    pgka__uxcnf.linkage = 'internal'
    bbpgz__ezkac = lir.IRBuilder(pgka__uxcnf.append_basic_block())
    wlvsw__nvd = c.context.call_conv.decode_arguments(bbpgz__ezkac,
        igz__roa.args, pgka__uxcnf)
    lnb__ruuj = zch__pvo(bbpgz__ezkac, wlvsw__nvd)
    c.context.call_conv.return_value(bbpgz__ezkac, lnb__ruuj)
    pzhwk__krs, wprjv__kmjk = c.context.call_conv.call_function(c.builder,
        pgka__uxcnf, igz__roa.return_type, igz__roa.args, args)
    return wprjv__kmjk


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    vihuu__swbq = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(vihuu__swbq)
    c.pyapi.decref(vihuu__swbq)
    haqr__yujg = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    qpefs__kzg = cgutils.get_or_insert_function(c.builder.module,
        haqr__yujg, name='is_bool_array')
    haqr__yujg = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    pgka__uxcnf = cgutils.get_or_insert_function(c.builder.module,
        haqr__yujg, name='is_pd_boolean_array')
    bsayy__wkldh = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    uuo__kixq = c.builder.call(pgka__uxcnf, [obj])
    idw__dtz = c.builder.icmp_unsigned('!=', uuo__kixq, uuo__kixq.type(0))
    with c.builder.if_else(idw__dtz) as (ajuy__kurnc, wwdwr__rtge):
        with ajuy__kurnc:
            itiw__conk = c.pyapi.object_getattr_string(obj, '_data')
            bsayy__wkldh.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), itiw__conk).value
            fwxm__lkdkz = c.pyapi.object_getattr_string(obj, '_mask')
            knhx__fcdb = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), fwxm__lkdkz).value
            nqcj__ajx = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            liy__kck = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, knhx__fcdb)
            pjhv__hbh = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [nqcj__ajx])
            haqr__yujg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            pgka__uxcnf = cgutils.get_or_insert_function(c.builder.module,
                haqr__yujg, name='mask_arr_to_bitmap')
            c.builder.call(pgka__uxcnf, [pjhv__hbh.data, liy__kck.data, n])
            bsayy__wkldh.null_bitmap = pjhv__hbh._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), knhx__fcdb)
            c.pyapi.decref(itiw__conk)
            c.pyapi.decref(fwxm__lkdkz)
        with wwdwr__rtge:
            zdyjm__iqa = c.builder.call(qpefs__kzg, [obj])
            bvbdx__xcp = c.builder.icmp_unsigned('!=', zdyjm__iqa,
                zdyjm__iqa.type(0))
            with c.builder.if_else(bvbdx__xcp) as (xooku__oqmq, ypa__nwye):
                with xooku__oqmq:
                    bsayy__wkldh.data = c.pyapi.to_native_value(types.Array
                        (types.bool_, 1, 'C'), obj).value
                    bsayy__wkldh.null_bitmap = call_func_in_unbox(
                        gen_full_bitmap, (n,), (types.int64,), c)
                with ypa__nwye:
                    bsayy__wkldh.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    nqcj__ajx = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    bsayy__wkldh.null_bitmap = bodo.utils.utils._empty_nd_impl(
                        c.context, c.builder, types.Array(types.uint8, 1,
                        'C'), [nqcj__ajx])._getvalue()
                    dguo__vnkk = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, bsayy__wkldh.data
                        ).data
                    zpf__cplw = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, bsayy__wkldh.
                        null_bitmap).data
                    haqr__yujg = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    pgka__uxcnf = cgutils.get_or_insert_function(c.builder.
                        module, haqr__yujg, name='unbox_bool_array_obj')
                    c.builder.call(pgka__uxcnf, [obj, dguo__vnkk, zpf__cplw, n]
                        )
    return NativeValue(bsayy__wkldh._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    bsayy__wkldh = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        bsayy__wkldh.data, c.env_manager)
    riglr__tfla = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, bsayy__wkldh.null_bitmap).data
    vihuu__swbq = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(vihuu__swbq)
    himwy__zgvu = c.context.insert_const_string(c.builder.module, 'numpy')
    txpi__msgjn = c.pyapi.import_module_noblock(himwy__zgvu)
    qve__hgcx = c.pyapi.object_getattr_string(txpi__msgjn, 'bool_')
    knhx__fcdb = c.pyapi.call_method(txpi__msgjn, 'empty', (vihuu__swbq,
        qve__hgcx))
    cbquy__smwjb = c.pyapi.object_getattr_string(knhx__fcdb, 'ctypes')
    ymthj__bgsxz = c.pyapi.object_getattr_string(cbquy__smwjb, 'data')
    ogvib__uvp = c.builder.inttoptr(c.pyapi.long_as_longlong(ymthj__bgsxz),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as zvz__rqld:
        ewvwi__pbnl = zvz__rqld.index
        dxooi__idm = c.builder.lshr(ewvwi__pbnl, lir.Constant(lir.IntType(
            64), 3))
        chb__ioe = c.builder.load(cgutils.gep(c.builder, riglr__tfla,
            dxooi__idm))
        bodof__omb = c.builder.trunc(c.builder.and_(ewvwi__pbnl, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(chb__ioe, bodof__omb), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        wom__nkzfw = cgutils.gep(c.builder, ogvib__uvp, ewvwi__pbnl)
        c.builder.store(val, wom__nkzfw)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        bsayy__wkldh.null_bitmap)
    himwy__zgvu = c.context.insert_const_string(c.builder.module, 'pandas')
    raz__fbqc = c.pyapi.import_module_noblock(himwy__zgvu)
    qrsm__facl = c.pyapi.object_getattr_string(raz__fbqc, 'arrays')
    wrqta__bomtv = c.pyapi.call_method(qrsm__facl, 'BooleanArray', (data,
        knhx__fcdb))
    c.pyapi.decref(raz__fbqc)
    c.pyapi.decref(vihuu__swbq)
    c.pyapi.decref(txpi__msgjn)
    c.pyapi.decref(qve__hgcx)
    c.pyapi.decref(cbquy__smwjb)
    c.pyapi.decref(ymthj__bgsxz)
    c.pyapi.decref(qrsm__facl)
    c.pyapi.decref(data)
    c.pyapi.decref(knhx__fcdb)
    return wrqta__bomtv


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    lmf__gel = np.empty(n, np.bool_)
    oqj__jmzll = np.empty(n + 7 >> 3, np.uint8)
    for ewvwi__pbnl, s in enumerate(pyval):
        wru__ekp = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(oqj__jmzll, ewvwi__pbnl, int(
            not wru__ekp))
        if not wru__ekp:
            lmf__gel[ewvwi__pbnl] = s
    bngn__zesjb = context.get_constant_generic(builder, data_type, lmf__gel)
    zcxd__rpoqh = context.get_constant_generic(builder, nulls_type, oqj__jmzll)
    return lir.Constant.literal_struct([bngn__zesjb, zcxd__rpoqh])


def lower_init_bool_array(context, builder, signature, args):
    ouwm__kmbjm, spms__yqpb = args
    bsayy__wkldh = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    bsayy__wkldh.data = ouwm__kmbjm
    bsayy__wkldh.null_bitmap = spms__yqpb
    context.nrt.incref(builder, signature.args[0], ouwm__kmbjm)
    context.nrt.incref(builder, signature.args[1], spms__yqpb)
    return bsayy__wkldh._getvalue()


@intrinsic
def init_bool_array(typingctx, data, null_bitmap=None):
    assert data == types.Array(types.bool_, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    sig = boolean_array(data, null_bitmap)
    return sig, lower_init_bool_array


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_bool_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    fdrpf__jhhnr = args[0]
    if equiv_set.has_shape(fdrpf__jhhnr):
        return ArrayAnalysis.AnalyzeResult(shape=fdrpf__jhhnr, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    fdrpf__jhhnr = args[0]
    if equiv_set.has_shape(fdrpf__jhhnr):
        return ArrayAnalysis.AnalyzeResult(shape=fdrpf__jhhnr, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_init_bool_array = (
    init_bool_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_bool_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_bool_array',
    'bodo.libs.bool_arr_ext'] = alias_ext_init_bool_array
numba.core.ir_utils.alias_func_extensions['get_bool_arr_data',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_bool_arr_bitmap',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_bool_array(n):
    lmf__gel = np.empty(n, dtype=np.bool_)
    ntwk__sjmgo = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(lmf__gel, ntwk__sjmgo)


def alloc_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_alloc_bool_array = (
    alloc_bool_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def bool_arr_getitem(A, ind):
    if A != boolean_array:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            mztg__srid, zuaoh__amxye = array_getitem_bool_index(A, ind)
            return init_bool_array(mztg__srid, zuaoh__amxye)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            mztg__srid, zuaoh__amxye = array_getitem_int_index(A, ind)
            return init_bool_array(mztg__srid, zuaoh__amxye)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            mztg__srid, zuaoh__amxye = array_getitem_slice_index(A, ind)
            return init_bool_array(mztg__srid, zuaoh__amxye)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    yils__chol = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(yils__chol)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(yils__chol)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for BooleanArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_bool_arr_len(A):
    if A == boolean_array:
        return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'shape')
def overload_bool_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(BooleanArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: pd.BooleanDtype()


@overload_attribute(BooleanArrayType, 'ndim')
def overload_bool_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BooleanArrayType, 'nbytes')
def bool_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(BooleanArrayType, 'copy', no_unliteral=True)
def overload_bool_arr_copy(A):
    return lambda A: bodo.libs.bool_arr_ext.init_bool_array(bodo.libs.
        bool_arr_ext.get_bool_arr_data(A).copy(), bodo.libs.bool_arr_ext.
        get_bool_arr_bitmap(A).copy())


@overload_method(BooleanArrayType, 'sum', no_unliteral=True, inline='always')
def overload_bool_sum(A):

    def impl(A):
        numba.parfors.parfor.init_prange()
        s = 0
        for ewvwi__pbnl in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, ewvwi__pbnl):
                val = A[ewvwi__pbnl]
            s += val
        return s
    return impl


@overload_method(BooleanArrayType, 'astype', no_unliteral=True)
def overload_bool_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "BooleanArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if dtype == types.bool_:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    nb_dtype = parse_dtype(dtype, 'BooleanArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
            n = len(data)
            nfohx__mit = np.empty(n, nb_dtype)
            for ewvwi__pbnl in numba.parfors.parfor.internal_prange(n):
                nfohx__mit[ewvwi__pbnl] = data[ewvwi__pbnl]
                if bodo.libs.array_kernels.isna(A, ewvwi__pbnl):
                    nfohx__mit[ewvwi__pbnl] = np.nan
            return nfohx__mit
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload(str, no_unliteral=True)
def overload_str_bool(val):
    if val == types.bool_:

        def impl(val):
            if val:
                return 'True'
            return 'False'
        return impl


ufunc_aliases = {'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    ebfu__snmdv = op.__name__
    ebfu__snmdv = ufunc_aliases.get(ebfu__snmdv, ebfu__snmdv)
    if n_inputs == 1:

        def overload_bool_arr_op_nin_1(A):
            if isinstance(A, BooleanArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_bool_arr_op_nin_1
    elif n_inputs == 2:

        def overload_bool_arr_op_nin_2(lhs, rhs):
            if lhs == boolean_array or rhs == boolean_array:
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_bool_arr_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for uowfr__pds in numba.np.ufunc_db.get_ufuncs():
        wszck__ajm = create_op_overload(uowfr__pds, uowfr__pds.nin)
        overload(uowfr__pds, no_unliteral=True)(wszck__ajm)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        wszck__ajm = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(wszck__ajm)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        wszck__ajm = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(wszck__ajm)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        wszck__ajm = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(wszck__ajm)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        bodof__omb = []
        too__czkpz = False
        zxgki__qgpl = False
        ytub__zvkbi = False
        for ewvwi__pbnl in range(len(A)):
            if bodo.libs.array_kernels.isna(A, ewvwi__pbnl):
                if not too__czkpz:
                    data.append(False)
                    bodof__omb.append(False)
                    too__czkpz = True
                continue
            val = A[ewvwi__pbnl]
            if val and not zxgki__qgpl:
                data.append(True)
                bodof__omb.append(True)
                zxgki__qgpl = True
            if not val and not ytub__zvkbi:
                data.append(False)
                bodof__omb.append(True)
                ytub__zvkbi = True
            if too__czkpz and zxgki__qgpl and ytub__zvkbi:
                break
        mztg__srid = np.array(data)
        n = len(mztg__srid)
        nqcj__ajx = 1
        zuaoh__amxye = np.empty(nqcj__ajx, np.uint8)
        for puhb__uzp in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(zuaoh__amxye, puhb__uzp,
                bodof__omb[puhb__uzp])
        return init_bool_array(mztg__srid, zuaoh__amxye)
    return impl_bool_arr


@overload(operator.getitem, no_unliteral=True)
def bool_arr_ind_getitem(A, ind):
    if ind == boolean_array and (isinstance(A, (types.Array, bodo.libs.
        int_arr_ext.IntegerArrayType)) or isinstance(A, bodo.libs.
        struct_arr_ext.StructArrayType) or isinstance(A, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType) or isinstance(A, bodo.libs.
        map_arr_ext.MapArrayType) or A in (string_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type, boolean_array)):
        return lambda A, ind: A[ind._data]


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    wrqta__bomtv = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, wrqta__bomtv)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    ffrf__vndf = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        otwf__fuh = bodo.utils.utils.is_array_typ(val1, False)
        ocfym__vsfon = bodo.utils.utils.is_array_typ(val2, False)
        efmw__xhxb = 'val1' if otwf__fuh else 'val2'
        diif__biii = 'def impl(val1, val2):\n'
        diif__biii += f'  n = len({efmw__xhxb})\n'
        diif__biii += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        diif__biii += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if otwf__fuh:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            ilnv__vhbnp = 'val1[i]'
        else:
            null1 = 'False\n'
            ilnv__vhbnp = 'val1'
        if ocfym__vsfon:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            fpvvj__oxjp = 'val2[i]'
        else:
            null2 = 'False\n'
            fpvvj__oxjp = 'val2'
        if ffrf__vndf:
            diif__biii += f"""    result, isna_val = compute_or_body({null1}, {null2}, {ilnv__vhbnp}, {fpvvj__oxjp})
"""
        else:
            diif__biii += f"""    result, isna_val = compute_and_body({null1}, {null2}, {ilnv__vhbnp}, {fpvvj__oxjp})
"""
        diif__biii += '    out_arr[i] = result\n'
        diif__biii += '    if isna_val:\n'
        diif__biii += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        diif__biii += '      continue\n'
        diif__biii += '  return out_arr\n'
        dhq__kagqe = {}
        exec(diif__biii, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, dhq__kagqe)
        impl = dhq__kagqe['impl']
        return impl
    return bool_array_impl


def compute_or_body(null1, null2, val1, val2):
    pass


@overload(compute_or_body)
def overload_compute_or_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == False
        elif null2:
            return val1, val1 == False
        else:
            return val1 | val2, False
    return impl


def compute_and_body(null1, null2, val1, val2):
    pass


@overload(compute_and_body)
def overload_compute_and_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == True
        elif null2:
            return val1, val1 == True
        else:
            return val1 & val2, False
    return impl


def create_boolean_array_logical_lower_impl(op):

    def logical_lower_impl(context, builder, sig, args):
        impl = create_nullable_logical_op_overload(op)(*sig.args)
        return context.compile_internal(builder, impl, sig, args)
    return logical_lower_impl


class BooleanArrayLogicalOperatorTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        if not is_valid_boolean_array_logical_op(args[0], args[1]):
            return
        qrnf__jqf = boolean_array
        return qrnf__jqf(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    sut__asrr = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return sut__asrr


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        mmfh__vatx = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(mmfh__vatx)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(mmfh__vatx)


_install_nullable_logical_lowering()
