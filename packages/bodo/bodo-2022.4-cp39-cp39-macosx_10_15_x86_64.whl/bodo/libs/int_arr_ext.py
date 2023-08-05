"""Nullable integer array corresponding to Pandas IntegerArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.str_arr_ext import kBitmask
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('mask_arr_to_bitmap', hstr_ext.mask_arr_to_bitmap)
ll.add_symbol('is_pd_int_array', array_ext.is_pd_int_array)
ll.add_symbol('int_array_from_sequence', array_ext.int_array_from_sequence)
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error, to_nullable_type


class IntegerArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(IntegerArrayType, self).__init__(name=
            f'IntegerArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntegerArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        rtkag__tls = int(np.log2(self.dtype.bitwidth // 8))
        agyne__pejy = 0 if self.dtype.signed else 4
        idx = rtkag__tls + agyne__pejy
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nqy__gafra = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, nqy__gafra)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    yzbp__taon = 8 * val.dtype.itemsize
    iksy__pxos = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(iksy__pxos, yzbp__taon))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        oel__dkt = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(oel__dkt)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    mbi__ufyke = c.context.insert_const_string(c.builder.module, 'pandas')
    llc__icd = c.pyapi.import_module_noblock(mbi__ufyke)
    vssa__eazp = c.pyapi.call_method(llc__icd, str(typ)[:-2], ())
    c.pyapi.decref(llc__icd)
    return vssa__eazp


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    yzbp__taon = 8 * val.itemsize
    iksy__pxos = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(iksy__pxos, yzbp__taon))
    return IntDtype(dtype)


def _register_int_dtype(t):
    typeof_impl.register(t)(typeof_pd_int_dtype)
    int_dtype = typeof_pd_int_dtype(t(), None)
    type_callable(t)(lambda c: lambda : int_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


pd_int_dtype_classes = (pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.
    Int64Dtype, pd.UInt8Dtype, pd.UInt16Dtype, pd.UInt32Dtype, pd.UInt64Dtype)
for t in pd_int_dtype_classes:
    _register_int_dtype(t)


@numba.extending.register_jitable
def mask_arr_to_bitmap(mask_arr):
    n = len(mask_arr)
    eeg__oig = n + 7 >> 3
    sjoy__unpo = np.empty(eeg__oig, np.uint8)
    for i in range(n):
        vdtq__ecdb = i // 8
        sjoy__unpo[vdtq__ecdb] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            sjoy__unpo[vdtq__ecdb]) & kBitmask[i % 8]
    return sjoy__unpo


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    awko__vjs = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(awko__vjs)
    c.pyapi.decref(awko__vjs)
    gaa__plk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    eeg__oig = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64),
        7)), lir.Constant(lir.IntType(64), 8))
    pybec__xeldp = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [eeg__oig])
    bycc__beubv = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    eekkm__lzz = cgutils.get_or_insert_function(c.builder.module,
        bycc__beubv, name='is_pd_int_array')
    lvab__bhkrl = c.builder.call(eekkm__lzz, [obj])
    xdrv__vxbxd = c.builder.icmp_unsigned('!=', lvab__bhkrl, lvab__bhkrl.
        type(0))
    with c.builder.if_else(xdrv__vxbxd) as (wri__gmi, mxm__umsq):
        with wri__gmi:
            tlxl__afs = c.pyapi.object_getattr_string(obj, '_data')
            gaa__plk.data = c.pyapi.to_native_value(types.Array(typ.dtype, 
                1, 'C'), tlxl__afs).value
            kjcn__bvj = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), kjcn__bvj).value
            c.pyapi.decref(tlxl__afs)
            c.pyapi.decref(kjcn__bvj)
            bbbj__zkcx = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, mask_arr)
            bycc__beubv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            eekkm__lzz = cgutils.get_or_insert_function(c.builder.module,
                bycc__beubv, name='mask_arr_to_bitmap')
            c.builder.call(eekkm__lzz, [pybec__xeldp.data, bbbj__zkcx.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with mxm__umsq:
            lyu__fcstz = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            bycc__beubv = lir.FunctionType(lir.IntType(32), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            xhu__ddqv = cgutils.get_or_insert_function(c.builder.module,
                bycc__beubv, name='int_array_from_sequence')
            c.builder.call(xhu__ddqv, [obj, c.builder.bitcast(lyu__fcstz.
                data, lir.IntType(8).as_pointer()), pybec__xeldp.data])
            gaa__plk.data = lyu__fcstz._getvalue()
    gaa__plk.null_bitmap = pybec__xeldp._getvalue()
    lxtq__ils = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gaa__plk._getvalue(), is_error=lxtq__ils)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    gaa__plk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        gaa__plk.data, c.env_manager)
    iqagt__tsd = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, gaa__plk.null_bitmap).data
    awko__vjs = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(awko__vjs)
    mbi__ufyke = c.context.insert_const_string(c.builder.module, 'numpy')
    zrtw__folkx = c.pyapi.import_module_noblock(mbi__ufyke)
    xfiak__krg = c.pyapi.object_getattr_string(zrtw__folkx, 'bool_')
    mask_arr = c.pyapi.call_method(zrtw__folkx, 'empty', (awko__vjs,
        xfiak__krg))
    rpzbz__wjh = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    ooy__yhps = c.pyapi.object_getattr_string(rpzbz__wjh, 'data')
    enjgq__xaw = c.builder.inttoptr(c.pyapi.long_as_longlong(ooy__yhps),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as bchqq__frvw:
        i = bchqq__frvw.index
        bpd__kpth = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        pjtj__dgluw = c.builder.load(cgutils.gep(c.builder, iqagt__tsd,
            bpd__kpth))
        ktzam__wfb = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(pjtj__dgluw, ktzam__wfb), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        rgt__gvg = cgutils.gep(c.builder, enjgq__xaw, i)
        c.builder.store(val, rgt__gvg)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        gaa__plk.null_bitmap)
    mbi__ufyke = c.context.insert_const_string(c.builder.module, 'pandas')
    llc__icd = c.pyapi.import_module_noblock(mbi__ufyke)
    lpi__ichp = c.pyapi.object_getattr_string(llc__icd, 'arrays')
    vssa__eazp = c.pyapi.call_method(lpi__ichp, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(llc__icd)
    c.pyapi.decref(awko__vjs)
    c.pyapi.decref(zrtw__folkx)
    c.pyapi.decref(xfiak__krg)
    c.pyapi.decref(rpzbz__wjh)
    c.pyapi.decref(ooy__yhps)
    c.pyapi.decref(lpi__ichp)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return vssa__eazp


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        bfzrh__pihsq, kqqy__exup = args
        gaa__plk = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        gaa__plk.data = bfzrh__pihsq
        gaa__plk.null_bitmap = kqqy__exup
        context.nrt.incref(builder, signature.args[0], bfzrh__pihsq)
        context.nrt.incref(builder, signature.args[1], kqqy__exup)
        return gaa__plk._getvalue()
    qxsjh__nqz = IntegerArrayType(data.dtype)
    yhbg__mav = qxsjh__nqz(data, null_bitmap)
    return yhbg__mav, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    dsopg__vfr = np.empty(n, pyval.dtype.type)
    dhamo__vvo = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        gyg__dxji = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(dhamo__vvo, i, int(not gyg__dxji))
        if not gyg__dxji:
            dsopg__vfr[i] = s
    hossf__uro = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), dsopg__vfr)
    czdxd__nhc = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), dhamo__vvo)
    return lir.Constant.literal_struct([hossf__uro, czdxd__nhc])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    eqq__czyhj = args[0]
    if equiv_set.has_shape(eqq__czyhj):
        return ArrayAnalysis.AnalyzeResult(shape=eqq__czyhj, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    eqq__czyhj = args[0]
    if equiv_set.has_shape(eqq__czyhj):
        return ArrayAnalysis.AnalyzeResult(shape=eqq__czyhj, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_init_integer_array = (
    init_integer_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_integer_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_integer_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_integer_array
numba.core.ir_utils.alias_func_extensions['get_int_arr_data',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_int_arr_bitmap',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_int_array(n, dtype):
    dsopg__vfr = np.empty(n, dtype)
    esczi__mlriu = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(dsopg__vfr, esczi__mlriu)


def alloc_int_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_alloc_int_array = (
    alloc_int_array_equiv)


@numba.extending.register_jitable
def set_bit_to_arr(bits, i, bit_is_set):
    bits[i // 8] ^= np.uint8(-np.uint8(bit_is_set) ^ bits[i // 8]) & kBitmask[
        i % 8]


@numba.extending.register_jitable
def get_bit_bitmap_arr(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@overload(operator.getitem, no_unliteral=True)
def int_arr_getitem(A, ind):
    if not isinstance(A, IntegerArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            adat__hog, pmlzb__qqj = array_getitem_bool_index(A, ind)
            return init_integer_array(adat__hog, pmlzb__qqj)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            adat__hog, pmlzb__qqj = array_getitem_int_index(A, ind)
            return init_integer_array(adat__hog, pmlzb__qqj)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            adat__hog, pmlzb__qqj = array_getitem_slice_index(A, ind)
            return init_integer_array(adat__hog, pmlzb__qqj)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    dalv__ztbv = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    qck__qlji = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if qck__qlji:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(dalv__ztbv)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or qck__qlji):
        raise BodoError(dalv__ztbv)
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
        f'setitem for IntegerArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_int_arr_len(A):
    if isinstance(A, IntegerArrayType):
        return lambda A: len(A._data)


@overload_attribute(IntegerArrayType, 'shape')
def overload_int_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(IntegerArrayType, 'dtype')
def overload_int_arr_dtype(A):
    dtype_class = getattr(pd, '{}Int{}Dtype'.format('' if A.dtype.signed else
        'U', A.dtype.bitwidth))
    return lambda A: dtype_class()


@overload_attribute(IntegerArrayType, 'ndim')
def overload_int_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntegerArrayType, 'nbytes')
def int_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(IntegerArrayType, 'copy', no_unliteral=True)
def overload_int_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.int_arr_ext.init_integer_array(
            bodo.libs.int_arr_ext.get_int_arr_data(A).copy(), bodo.libs.
            int_arr_ext.get_int_arr_bitmap(A).copy())


@overload_method(IntegerArrayType, 'astype', no_unliteral=True)
def overload_int_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "IntegerArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, IntDtype) and A.dtype == dtype.dtype:
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
    if isinstance(dtype, IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.int_arr_ext.get_int_arr_data(A).
            astype(np_dtype), bodo.libs.int_arr_ext.get_int_arr_bitmap(A).
            copy()))
    nb_dtype = parse_dtype(dtype, 'IntegerArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.int_arr_ext.get_int_arr_data(A)
            n = len(data)
            raj__rjo = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                raj__rjo[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    raj__rjo[i] = np.nan
            return raj__rjo
        return impl_float
    return lambda A, dtype, copy=True: bodo.libs.int_arr_ext.get_int_arr_data(A
        ).astype(nb_dtype)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def apply_null_mask(arr, bitmap, mask_fill, inplace):
    assert isinstance(arr, types.Array)
    if isinstance(arr.dtype, types.Integer):
        if is_overload_none(inplace):
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap.copy()))
        else:
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap))
    if isinstance(arr.dtype, types.Float):

        def impl(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = np.nan
            return arr
        return impl
    if arr.dtype == types.bool_:

        def impl_bool(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = mask_fill
            return arr
        return impl_bool
    return lambda arr, bitmap, mask_fill, inplace: arr


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def merge_bitmaps(B1, B2, n, inplace):
    assert B1 == types.Array(types.uint8, 1, 'C')
    assert B2 == types.Array(types.uint8, 1, 'C')
    if not is_overload_none(inplace):

        def impl_inplace(B1, B2, n, inplace):
            for i in numba.parfors.parfor.internal_prange(n):
                hzgy__klf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                xmt__enad = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                hlkhh__ytj = hzgy__klf & xmt__enad
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, hlkhh__ytj)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        eeg__oig = n + 7 >> 3
        raj__rjo = np.empty(eeg__oig, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            hzgy__klf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            xmt__enad = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            hlkhh__ytj = hzgy__klf & xmt__enad
            bodo.libs.int_arr_ext.set_bit_to_arr(raj__rjo, i, hlkhh__ytj)
        return raj__rjo
    return impl


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_int_arr_op_nin_1(A):
            if isinstance(A, IntegerArrayType):
                return get_nullable_array_unary_impl(op, A)
        return overload_int_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
                IntegerArrayType):
                return get_nullable_array_binary_impl(op, lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for oiymi__uih in numba.np.ufunc_db.get_ufuncs():
        jex__qrf = create_op_overload(oiymi__uih, oiymi__uih.nin)
        overload(oiymi__uih, no_unliteral=True)(jex__qrf)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        jex__qrf = create_op_overload(op, 2)
        overload(op)(jex__qrf)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        jex__qrf = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(jex__qrf)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        jex__qrf = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(jex__qrf)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    aekv__ajq = len(arrs.types)
    fhx__pojt = 'def f(arrs):\n'
    vssa__eazp = ', '.join('arrs[{}]._data'.format(i) for i in range(aekv__ajq)
        )
    fhx__pojt += '  return ({}{})\n'.format(vssa__eazp, ',' if aekv__ajq ==
        1 else '')
    jnf__lanmg = {}
    exec(fhx__pojt, {}, jnf__lanmg)
    impl = jnf__lanmg['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    aekv__ajq = len(arrs.types)
    fhxo__soo = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        aekv__ajq))
    fhx__pojt = 'def f(arrs):\n'
    fhx__pojt += '  n = {}\n'.format(fhxo__soo)
    fhx__pojt += '  n_bytes = (n + 7) >> 3\n'
    fhx__pojt += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    fhx__pojt += '  curr_bit = 0\n'
    for i in range(aekv__ajq):
        fhx__pojt += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        fhx__pojt += '  for j in range(len(arrs[{}])):\n'.format(i)
        fhx__pojt += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        fhx__pojt += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        fhx__pojt += '    curr_bit += 1\n'
    fhx__pojt += '  return new_mask\n'
    jnf__lanmg = {}
    exec(fhx__pojt, {'np': np, 'bodo': bodo}, jnf__lanmg)
    impl = jnf__lanmg['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    rjgsz__gfb = dict(skipna=skipna, min_count=min_count)
    wgdb__pjy = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', rjgsz__gfb, wgdb__pjy)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0
        for i in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, i):
                val = A[i]
            s += val
        return s
    return impl


@overload_method(IntegerArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_int_arr(A):
        data = []
        ktzam__wfb = []
        nqaqu__ycic = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not nqaqu__ycic:
                    data.append(dtype(1))
                    ktzam__wfb.append(False)
                    nqaqu__ycic = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                ktzam__wfb.append(True)
        adat__hog = np.array(data)
        n = len(adat__hog)
        eeg__oig = n + 7 >> 3
        pmlzb__qqj = np.empty(eeg__oig, np.uint8)
        for iykxi__dhnv in range(n):
            set_bit_to_arr(pmlzb__qqj, iykxi__dhnv, ktzam__wfb[iykxi__dhnv])
        return init_integer_array(adat__hog, pmlzb__qqj)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    cdeo__ncet = numba.core.registry.cpu_target.typing_context
    tqqn__cvd = cdeo__ncet.resolve_function_type(op, (types.Array(A.dtype, 
        1, 'C'),), {}).return_type
    tqqn__cvd = to_nullable_type(tqqn__cvd)

    def impl(A):
        n = len(A)
        gxpk__ihd = bodo.utils.utils.alloc_type(n, tqqn__cvd, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(gxpk__ihd, i)
                continue
            gxpk__ihd[i] = op(A[i])
        return gxpk__ihd
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    xom__jege = isinstance(lhs, (types.Number, types.Boolean))
    pjx__ixai = isinstance(rhs, (types.Number, types.Boolean))
    uof__yiv = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    adaaw__pvirr = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    cdeo__ncet = numba.core.registry.cpu_target.typing_context
    tqqn__cvd = cdeo__ncet.resolve_function_type(op, (uof__yiv,
        adaaw__pvirr), {}).return_type
    tqqn__cvd = to_nullable_type(tqqn__cvd)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    szjwn__aplk = 'lhs' if xom__jege else 'lhs[i]'
    pledl__ssdnv = 'rhs' if pjx__ixai else 'rhs[i]'
    xwcz__rpai = ('False' if xom__jege else
        'bodo.libs.array_kernels.isna(lhs, i)')
    tao__wuk = 'False' if pjx__ixai else 'bodo.libs.array_kernels.isna(rhs, i)'
    fhx__pojt = 'def impl(lhs, rhs):\n'
    fhx__pojt += '  n = len({})\n'.format('lhs' if not xom__jege else 'rhs')
    if inplace:
        fhx__pojt += '  out_arr = {}\n'.format('lhs' if not xom__jege else
            'rhs')
    else:
        fhx__pojt += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    fhx__pojt += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    fhx__pojt += '    if ({}\n'.format(xwcz__rpai)
    fhx__pojt += '        or {}):\n'.format(tao__wuk)
    fhx__pojt += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    fhx__pojt += '      continue\n'
    fhx__pojt += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(szjwn__aplk, pledl__ssdnv))
    fhx__pojt += '  return out_arr\n'
    jnf__lanmg = {}
    exec(fhx__pojt, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        tqqn__cvd, 'op': op}, jnf__lanmg)
    impl = jnf__lanmg['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        xom__jege = lhs in [pd_timedelta_type]
        pjx__ixai = rhs in [pd_timedelta_type]
        if xom__jege:

            def impl(lhs, rhs):
                n = len(rhs)
                gxpk__ihd = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(gxpk__ihd, i)
                        continue
                    gxpk__ihd[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return gxpk__ihd
            return impl
        elif pjx__ixai:

            def impl(lhs, rhs):
                n = len(lhs)
                gxpk__ihd = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(gxpk__ihd, i)
                        continue
                    gxpk__ihd[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return gxpk__ihd
            return impl
    return impl
