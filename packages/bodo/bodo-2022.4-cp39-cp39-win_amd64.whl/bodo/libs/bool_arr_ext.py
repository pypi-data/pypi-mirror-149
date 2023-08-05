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
        plkg__zza = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, plkg__zza)


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
    ppfyv__mjz = c.context.insert_const_string(c.builder.module, 'pandas')
    mmqi__wkbw = c.pyapi.import_module_noblock(ppfyv__mjz)
    rcip__qducr = c.pyapi.call_method(mmqi__wkbw, 'BooleanDtype', ())
    c.pyapi.decref(mmqi__wkbw)
    return rcip__qducr


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    qxr__gtzf = n + 7 >> 3
    return np.full(qxr__gtzf, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    grj__ozu = c.context.typing_context.resolve_value_type(func)
    wra__sccjm = grj__ozu.get_call_type(c.context.typing_context, arg_typs, {})
    tyim__eee = c.context.get_function(grj__ozu, wra__sccjm)
    muf__wyetj = c.context.call_conv.get_function_type(wra__sccjm.
        return_type, wra__sccjm.args)
    ugm__gubqs = c.builder.module
    nix__vcn = lir.Function(ugm__gubqs, muf__wyetj, name=ugm__gubqs.
        get_unique_name('.func_conv'))
    nix__vcn.linkage = 'internal'
    cgg__ykf = lir.IRBuilder(nix__vcn.append_basic_block())
    vohqz__nopnf = c.context.call_conv.decode_arguments(cgg__ykf,
        wra__sccjm.args, nix__vcn)
    eoq__ooebq = tyim__eee(cgg__ykf, vohqz__nopnf)
    c.context.call_conv.return_value(cgg__ykf, eoq__ooebq)
    fgbu__ovqvq, qqtcn__nvkcd = c.context.call_conv.call_function(c.builder,
        nix__vcn, wra__sccjm.return_type, wra__sccjm.args, args)
    return qqtcn__nvkcd


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    fsa__hnpx = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(fsa__hnpx)
    c.pyapi.decref(fsa__hnpx)
    muf__wyetj = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    ugcgk__kdn = cgutils.get_or_insert_function(c.builder.module,
        muf__wyetj, name='is_bool_array')
    muf__wyetj = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    nix__vcn = cgutils.get_or_insert_function(c.builder.module, muf__wyetj,
        name='is_pd_boolean_array')
    sxh__bxtva = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mcv__bxcsa = c.builder.call(nix__vcn, [obj])
    jus__omjm = c.builder.icmp_unsigned('!=', mcv__bxcsa, mcv__bxcsa.type(0))
    with c.builder.if_else(jus__omjm) as (dujm__gvmlv, pqz__dkra):
        with dujm__gvmlv:
            xjpws__aewd = c.pyapi.object_getattr_string(obj, '_data')
            sxh__bxtva.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), xjpws__aewd).value
            jgqbw__lvh = c.pyapi.object_getattr_string(obj, '_mask')
            tdla__bcan = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), jgqbw__lvh).value
            qxr__gtzf = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            oyk__zyju = c.context.make_array(types.Array(types.bool_, 1, 'C'))(
                c.context, c.builder, tdla__bcan)
            xqqf__res = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [qxr__gtzf])
            muf__wyetj = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            nix__vcn = cgutils.get_or_insert_function(c.builder.module,
                muf__wyetj, name='mask_arr_to_bitmap')
            c.builder.call(nix__vcn, [xqqf__res.data, oyk__zyju.data, n])
            sxh__bxtva.null_bitmap = xqqf__res._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), tdla__bcan)
            c.pyapi.decref(xjpws__aewd)
            c.pyapi.decref(jgqbw__lvh)
        with pqz__dkra:
            ankrd__omvky = c.builder.call(ugcgk__kdn, [obj])
            uuci__mzf = c.builder.icmp_unsigned('!=', ankrd__omvky,
                ankrd__omvky.type(0))
            with c.builder.if_else(uuci__mzf) as (hqs__mce, tbfd__bcs):
                with hqs__mce:
                    sxh__bxtva.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    sxh__bxtva.null_bitmap = call_func_in_unbox(gen_full_bitmap
                        , (n,), (types.int64,), c)
                with tbfd__bcs:
                    sxh__bxtva.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    qxr__gtzf = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    sxh__bxtva.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [qxr__gtzf])._getvalue()
                    ohyn__zynq = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, sxh__bxtva.data
                        ).data
                    boqdn__ejyx = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, sxh__bxtva.
                        null_bitmap).data
                    muf__wyetj = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    nix__vcn = cgutils.get_or_insert_function(c.builder.
                        module, muf__wyetj, name='unbox_bool_array_obj')
                    c.builder.call(nix__vcn, [obj, ohyn__zynq, boqdn__ejyx, n])
    return NativeValue(sxh__bxtva._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    sxh__bxtva = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        sxh__bxtva.data, c.env_manager)
    qayxh__zgj = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, sxh__bxtva.null_bitmap).data
    fsa__hnpx = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(fsa__hnpx)
    ppfyv__mjz = c.context.insert_const_string(c.builder.module, 'numpy')
    tug__laul = c.pyapi.import_module_noblock(ppfyv__mjz)
    dhp__hob = c.pyapi.object_getattr_string(tug__laul, 'bool_')
    tdla__bcan = c.pyapi.call_method(tug__laul, 'empty', (fsa__hnpx, dhp__hob))
    jnrn__zax = c.pyapi.object_getattr_string(tdla__bcan, 'ctypes')
    avey__gikch = c.pyapi.object_getattr_string(jnrn__zax, 'data')
    ksx__uzvru = c.builder.inttoptr(c.pyapi.long_as_longlong(avey__gikch),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as tlm__lbpj:
        ijif__zlbgs = tlm__lbpj.index
        dvwix__qnl = c.builder.lshr(ijif__zlbgs, lir.Constant(lir.IntType(
            64), 3))
        shcga__zyyb = c.builder.load(cgutils.gep(c.builder, qayxh__zgj,
            dvwix__qnl))
        kvorv__rjop = c.builder.trunc(c.builder.and_(ijif__zlbgs, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(shcga__zyyb, kvorv__rjop), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        gioxt__joao = cgutils.gep(c.builder, ksx__uzvru, ijif__zlbgs)
        c.builder.store(val, gioxt__joao)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        sxh__bxtva.null_bitmap)
    ppfyv__mjz = c.context.insert_const_string(c.builder.module, 'pandas')
    mmqi__wkbw = c.pyapi.import_module_noblock(ppfyv__mjz)
    ekrp__pem = c.pyapi.object_getattr_string(mmqi__wkbw, 'arrays')
    rcip__qducr = c.pyapi.call_method(ekrp__pem, 'BooleanArray', (data,
        tdla__bcan))
    c.pyapi.decref(mmqi__wkbw)
    c.pyapi.decref(fsa__hnpx)
    c.pyapi.decref(tug__laul)
    c.pyapi.decref(dhp__hob)
    c.pyapi.decref(jnrn__zax)
    c.pyapi.decref(avey__gikch)
    c.pyapi.decref(ekrp__pem)
    c.pyapi.decref(data)
    c.pyapi.decref(tdla__bcan)
    return rcip__qducr


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    cuwqg__lumdh = np.empty(n, np.bool_)
    tela__uzfsm = np.empty(n + 7 >> 3, np.uint8)
    for ijif__zlbgs, s in enumerate(pyval):
        dkuno__dtcmk = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(tela__uzfsm, ijif__zlbgs, int(
            not dkuno__dtcmk))
        if not dkuno__dtcmk:
            cuwqg__lumdh[ijif__zlbgs] = s
    autw__sfyr = context.get_constant_generic(builder, data_type, cuwqg__lumdh)
    iah__pvyk = context.get_constant_generic(builder, nulls_type, tela__uzfsm)
    return lir.Constant.literal_struct([autw__sfyr, iah__pvyk])


def lower_init_bool_array(context, builder, signature, args):
    usedo__dlywd, ruczn__yduv = args
    sxh__bxtva = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    sxh__bxtva.data = usedo__dlywd
    sxh__bxtva.null_bitmap = ruczn__yduv
    context.nrt.incref(builder, signature.args[0], usedo__dlywd)
    context.nrt.incref(builder, signature.args[1], ruczn__yduv)
    return sxh__bxtva._getvalue()


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
    ory__ooo = args[0]
    if equiv_set.has_shape(ory__ooo):
        return ArrayAnalysis.AnalyzeResult(shape=ory__ooo, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ory__ooo = args[0]
    if equiv_set.has_shape(ory__ooo):
        return ArrayAnalysis.AnalyzeResult(shape=ory__ooo, pre=[])
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
    cuwqg__lumdh = np.empty(n, dtype=np.bool_)
    dkuw__voscv = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(cuwqg__lumdh, dkuw__voscv)


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
            vtpf__yyeiy, gzql__rpcq = array_getitem_bool_index(A, ind)
            return init_bool_array(vtpf__yyeiy, gzql__rpcq)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            vtpf__yyeiy, gzql__rpcq = array_getitem_int_index(A, ind)
            return init_bool_array(vtpf__yyeiy, gzql__rpcq)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            vtpf__yyeiy, gzql__rpcq = array_getitem_slice_index(A, ind)
            return init_bool_array(vtpf__yyeiy, gzql__rpcq)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    zovww__pnyn = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(zovww__pnyn)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(zovww__pnyn)
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
        for ijif__zlbgs in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, ijif__zlbgs):
                val = A[ijif__zlbgs]
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
            hzixj__tfk = np.empty(n, nb_dtype)
            for ijif__zlbgs in numba.parfors.parfor.internal_prange(n):
                hzixj__tfk[ijif__zlbgs] = data[ijif__zlbgs]
                if bodo.libs.array_kernels.isna(A, ijif__zlbgs):
                    hzixj__tfk[ijif__zlbgs] = np.nan
            return hzixj__tfk
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
    kpb__bufy = op.__name__
    kpb__bufy = ufunc_aliases.get(kpb__bufy, kpb__bufy)
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
    for yajwr__lovtd in numba.np.ufunc_db.get_ufuncs():
        kzmx__iut = create_op_overload(yajwr__lovtd, yajwr__lovtd.nin)
        overload(yajwr__lovtd, no_unliteral=True)(kzmx__iut)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        kzmx__iut = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(kzmx__iut)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        kzmx__iut = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(kzmx__iut)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        kzmx__iut = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(kzmx__iut)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        kvorv__rjop = []
        wcfyn__coa = False
        ekq__xsg = False
        ntubg__shc = False
        for ijif__zlbgs in range(len(A)):
            if bodo.libs.array_kernels.isna(A, ijif__zlbgs):
                if not wcfyn__coa:
                    data.append(False)
                    kvorv__rjop.append(False)
                    wcfyn__coa = True
                continue
            val = A[ijif__zlbgs]
            if val and not ekq__xsg:
                data.append(True)
                kvorv__rjop.append(True)
                ekq__xsg = True
            if not val and not ntubg__shc:
                data.append(False)
                kvorv__rjop.append(True)
                ntubg__shc = True
            if wcfyn__coa and ekq__xsg and ntubg__shc:
                break
        vtpf__yyeiy = np.array(data)
        n = len(vtpf__yyeiy)
        qxr__gtzf = 1
        gzql__rpcq = np.empty(qxr__gtzf, np.uint8)
        for uikq__hsdo in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(gzql__rpcq, uikq__hsdo,
                kvorv__rjop[uikq__hsdo])
        return init_bool_array(vtpf__yyeiy, gzql__rpcq)
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
    rcip__qducr = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, rcip__qducr)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    helu__ernz = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        wfwuq__ghe = bodo.utils.utils.is_array_typ(val1, False)
        vgycm__lgl = bodo.utils.utils.is_array_typ(val2, False)
        mjsgj__cei = 'val1' if wfwuq__ghe else 'val2'
        nnmvp__mvhh = 'def impl(val1, val2):\n'
        nnmvp__mvhh += f'  n = len({mjsgj__cei})\n'
        nnmvp__mvhh += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        nnmvp__mvhh += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if wfwuq__ghe:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            xtpf__cca = 'val1[i]'
        else:
            null1 = 'False\n'
            xtpf__cca = 'val1'
        if vgycm__lgl:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            qtkav__saiq = 'val2[i]'
        else:
            null2 = 'False\n'
            qtkav__saiq = 'val2'
        if helu__ernz:
            nnmvp__mvhh += f"""    result, isna_val = compute_or_body({null1}, {null2}, {xtpf__cca}, {qtkav__saiq})
"""
        else:
            nnmvp__mvhh += f"""    result, isna_val = compute_and_body({null1}, {null2}, {xtpf__cca}, {qtkav__saiq})
"""
        nnmvp__mvhh += '    out_arr[i] = result\n'
        nnmvp__mvhh += '    if isna_val:\n'
        nnmvp__mvhh += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        nnmvp__mvhh += '      continue\n'
        nnmvp__mvhh += '  return out_arr\n'
        xiobl__psa = {}
        exec(nnmvp__mvhh, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, xiobl__psa)
        impl = xiobl__psa['impl']
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
        ohzq__wvql = boolean_array
        return ohzq__wvql(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    iyuhz__xkh = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return iyuhz__xkh


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        zwzsu__enur = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(zwzsu__enur)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(zwzsu__enur)


_install_nullable_logical_lowering()
