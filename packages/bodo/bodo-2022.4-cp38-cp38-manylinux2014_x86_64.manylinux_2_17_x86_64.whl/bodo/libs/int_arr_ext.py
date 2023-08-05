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
        iyefu__htbdx = int(np.log2(self.dtype.bitwidth // 8))
        aaa__hhun = 0 if self.dtype.signed else 4
        idx = iyefu__htbdx + aaa__hhun
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        rfe__scea = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, rfe__scea)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    hkcb__necir = 8 * val.dtype.itemsize
    kst__lsep = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(kst__lsep, hkcb__necir))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        jplc__qkwmw = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(jplc__qkwmw)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    hku__zhnil = c.context.insert_const_string(c.builder.module, 'pandas')
    omusm__eii = c.pyapi.import_module_noblock(hku__zhnil)
    jwkb__divjk = c.pyapi.call_method(omusm__eii, str(typ)[:-2], ())
    c.pyapi.decref(omusm__eii)
    return jwkb__divjk


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    hkcb__necir = 8 * val.itemsize
    kst__lsep = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(kst__lsep, hkcb__necir))
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
    vjt__wbieb = n + 7 >> 3
    wiriy__lxk = np.empty(vjt__wbieb, np.uint8)
    for i in range(n):
        zyk__jijp = i // 8
        wiriy__lxk[zyk__jijp] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            wiriy__lxk[zyk__jijp]) & kBitmask[i % 8]
    return wiriy__lxk


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    ccodd__qlho = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ccodd__qlho)
    c.pyapi.decref(ccodd__qlho)
    nve__skg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vjt__wbieb = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    lsbg__nfw = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [vjt__wbieb])
    eoss__ljbx = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    rfmoi__idb = cgutils.get_or_insert_function(c.builder.module,
        eoss__ljbx, name='is_pd_int_array')
    vsxtn__snx = c.builder.call(rfmoi__idb, [obj])
    nwoof__grhdk = c.builder.icmp_unsigned('!=', vsxtn__snx, vsxtn__snx.type(0)
        )
    with c.builder.if_else(nwoof__grhdk) as (ixnu__bsxp, mngk__agi):
        with ixnu__bsxp:
            rnnhg__gtg = c.pyapi.object_getattr_string(obj, '_data')
            nve__skg.data = c.pyapi.to_native_value(types.Array(typ.dtype, 
                1, 'C'), rnnhg__gtg).value
            txrx__gjofg = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), txrx__gjofg).value
            c.pyapi.decref(rnnhg__gtg)
            c.pyapi.decref(txrx__gjofg)
            gyh__gph = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, mask_arr)
            eoss__ljbx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            rfmoi__idb = cgutils.get_or_insert_function(c.builder.module,
                eoss__ljbx, name='mask_arr_to_bitmap')
            c.builder.call(rfmoi__idb, [lsbg__nfw.data, gyh__gph.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with mngk__agi:
            gggrz__unr = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            eoss__ljbx = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            icmvm__rylfl = cgutils.get_or_insert_function(c.builder.module,
                eoss__ljbx, name='int_array_from_sequence')
            c.builder.call(icmvm__rylfl, [obj, c.builder.bitcast(gggrz__unr
                .data, lir.IntType(8).as_pointer()), lsbg__nfw.data])
            nve__skg.data = gggrz__unr._getvalue()
    nve__skg.null_bitmap = lsbg__nfw._getvalue()
    inej__wfg = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nve__skg._getvalue(), is_error=inej__wfg)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    nve__skg = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        nve__skg.data, c.env_manager)
    fwlup__bjtxp = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, nve__skg.null_bitmap).data
    ccodd__qlho = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ccodd__qlho)
    hku__zhnil = c.context.insert_const_string(c.builder.module, 'numpy')
    rer__dtit = c.pyapi.import_module_noblock(hku__zhnil)
    udsn__mrf = c.pyapi.object_getattr_string(rer__dtit, 'bool_')
    mask_arr = c.pyapi.call_method(rer__dtit, 'empty', (ccodd__qlho, udsn__mrf)
        )
    uqut__kzy = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    fiuyx__ngb = c.pyapi.object_getattr_string(uqut__kzy, 'data')
    vrd__ulzie = c.builder.inttoptr(c.pyapi.long_as_longlong(fiuyx__ngb),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as akhoi__yoa:
        i = akhoi__yoa.index
        zollh__rbrt = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        aslrt__gqx = c.builder.load(cgutils.gep(c.builder, fwlup__bjtxp,
            zollh__rbrt))
        vmd__epdl = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(aslrt__gqx, vmd__epdl), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        eos__tle = cgutils.gep(c.builder, vrd__ulzie, i)
        c.builder.store(val, eos__tle)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        nve__skg.null_bitmap)
    hku__zhnil = c.context.insert_const_string(c.builder.module, 'pandas')
    omusm__eii = c.pyapi.import_module_noblock(hku__zhnil)
    cytii__uhu = c.pyapi.object_getattr_string(omusm__eii, 'arrays')
    jwkb__divjk = c.pyapi.call_method(cytii__uhu, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(omusm__eii)
    c.pyapi.decref(ccodd__qlho)
    c.pyapi.decref(rer__dtit)
    c.pyapi.decref(udsn__mrf)
    c.pyapi.decref(uqut__kzy)
    c.pyapi.decref(fiuyx__ngb)
    c.pyapi.decref(cytii__uhu)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return jwkb__divjk


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        zbi__wqkd, htf__oagkk = args
        nve__skg = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        nve__skg.data = zbi__wqkd
        nve__skg.null_bitmap = htf__oagkk
        context.nrt.incref(builder, signature.args[0], zbi__wqkd)
        context.nrt.incref(builder, signature.args[1], htf__oagkk)
        return nve__skg._getvalue()
    fap__jbi = IntegerArrayType(data.dtype)
    eifjy__wkm = fap__jbi(data, null_bitmap)
    return eifjy__wkm, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    hcan__qgzq = np.empty(n, pyval.dtype.type)
    whtnz__sgmtk = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        gqigx__ctaz = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(whtnz__sgmtk, i, int(not
            gqigx__ctaz))
        if not gqigx__ctaz:
            hcan__qgzq[i] = s
    dnscn__ubx = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), hcan__qgzq)
    xeji__rqm = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), whtnz__sgmtk)
    return lir.Constant.literal_struct([dnscn__ubx, xeji__rqm])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    ewn__vzgzz = args[0]
    if equiv_set.has_shape(ewn__vzgzz):
        return ArrayAnalysis.AnalyzeResult(shape=ewn__vzgzz, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ewn__vzgzz = args[0]
    if equiv_set.has_shape(ewn__vzgzz):
        return ArrayAnalysis.AnalyzeResult(shape=ewn__vzgzz, pre=[])
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
    hcan__qgzq = np.empty(n, dtype)
    ezgp__faf = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(hcan__qgzq, ezgp__faf)


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
            imfaq__lbefy, qqu__yxea = array_getitem_bool_index(A, ind)
            return init_integer_array(imfaq__lbefy, qqu__yxea)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            imfaq__lbefy, qqu__yxea = array_getitem_int_index(A, ind)
            return init_integer_array(imfaq__lbefy, qqu__yxea)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            imfaq__lbefy, qqu__yxea = array_getitem_slice_index(A, ind)
            return init_integer_array(imfaq__lbefy, qqu__yxea)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    gyynq__qzgfi = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    zybkm__qbhs = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if zybkm__qbhs:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(gyynq__qzgfi)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or zybkm__qbhs):
        raise BodoError(gyynq__qzgfi)
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
            tzh__egclm = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                tzh__egclm[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    tzh__egclm[i] = np.nan
            return tzh__egclm
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
                kzldm__axi = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                iunmt__mcac = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                ydv__xfg = kzldm__axi & iunmt__mcac
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, ydv__xfg)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        vjt__wbieb = n + 7 >> 3
        tzh__egclm = np.empty(vjt__wbieb, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            kzldm__axi = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            iunmt__mcac = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            ydv__xfg = kzldm__axi & iunmt__mcac
            bodo.libs.int_arr_ext.set_bit_to_arr(tzh__egclm, i, ydv__xfg)
        return tzh__egclm
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
    for mllau__jlml in numba.np.ufunc_db.get_ufuncs():
        xxa__tavzx = create_op_overload(mllau__jlml, mllau__jlml.nin)
        overload(mllau__jlml, no_unliteral=True)(xxa__tavzx)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        xxa__tavzx = create_op_overload(op, 2)
        overload(op)(xxa__tavzx)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        xxa__tavzx = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(xxa__tavzx)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        xxa__tavzx = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(xxa__tavzx)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    nwsqn__bbm = len(arrs.types)
    raxit__bos = 'def f(arrs):\n'
    jwkb__divjk = ', '.join('arrs[{}]._data'.format(i) for i in range(
        nwsqn__bbm))
    raxit__bos += '  return ({}{})\n'.format(jwkb__divjk, ',' if nwsqn__bbm ==
        1 else '')
    gjqkr__lai = {}
    exec(raxit__bos, {}, gjqkr__lai)
    impl = gjqkr__lai['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    nwsqn__bbm = len(arrs.types)
    dygix__jwn = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        nwsqn__bbm))
    raxit__bos = 'def f(arrs):\n'
    raxit__bos += '  n = {}\n'.format(dygix__jwn)
    raxit__bos += '  n_bytes = (n + 7) >> 3\n'
    raxit__bos += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    raxit__bos += '  curr_bit = 0\n'
    for i in range(nwsqn__bbm):
        raxit__bos += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        raxit__bos += '  for j in range(len(arrs[{}])):\n'.format(i)
        raxit__bos += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        raxit__bos += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        raxit__bos += '    curr_bit += 1\n'
    raxit__bos += '  return new_mask\n'
    gjqkr__lai = {}
    exec(raxit__bos, {'np': np, 'bodo': bodo}, gjqkr__lai)
    impl = gjqkr__lai['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    utk__gez = dict(skipna=skipna, min_count=min_count)
    dwnj__aauvi = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', utk__gez, dwnj__aauvi)

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
        vmd__epdl = []
        qabt__yvebs = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not qabt__yvebs:
                    data.append(dtype(1))
                    vmd__epdl.append(False)
                    qabt__yvebs = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                vmd__epdl.append(True)
        imfaq__lbefy = np.array(data)
        n = len(imfaq__lbefy)
        vjt__wbieb = n + 7 >> 3
        qqu__yxea = np.empty(vjt__wbieb, np.uint8)
        for wwgo__owxwu in range(n):
            set_bit_to_arr(qqu__yxea, wwgo__owxwu, vmd__epdl[wwgo__owxwu])
        return init_integer_array(imfaq__lbefy, qqu__yxea)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    alt__xgjz = numba.core.registry.cpu_target.typing_context
    wlpr__mrcf = alt__xgjz.resolve_function_type(op, (types.Array(A.dtype, 
        1, 'C'),), {}).return_type
    wlpr__mrcf = to_nullable_type(wlpr__mrcf)

    def impl(A):
        n = len(A)
        xouw__dwmjo = bodo.utils.utils.alloc_type(n, wlpr__mrcf, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(xouw__dwmjo, i)
                continue
            xouw__dwmjo[i] = op(A[i])
        return xouw__dwmjo
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    qbqge__rdu = isinstance(lhs, (types.Number, types.Boolean))
    nyszw__kxmqz = isinstance(rhs, (types.Number, types.Boolean))
    bwofa__eapy = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    jqyfb__hkcr = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    alt__xgjz = numba.core.registry.cpu_target.typing_context
    wlpr__mrcf = alt__xgjz.resolve_function_type(op, (bwofa__eapy,
        jqyfb__hkcr), {}).return_type
    wlpr__mrcf = to_nullable_type(wlpr__mrcf)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    vhmx__baye = 'lhs' if qbqge__rdu else 'lhs[i]'
    xqn__ydmtd = 'rhs' if nyszw__kxmqz else 'rhs[i]'
    yqqy__beadd = ('False' if qbqge__rdu else
        'bodo.libs.array_kernels.isna(lhs, i)')
    vqxf__yqt = ('False' if nyszw__kxmqz else
        'bodo.libs.array_kernels.isna(rhs, i)')
    raxit__bos = 'def impl(lhs, rhs):\n'
    raxit__bos += '  n = len({})\n'.format('lhs' if not qbqge__rdu else 'rhs')
    if inplace:
        raxit__bos += '  out_arr = {}\n'.format('lhs' if not qbqge__rdu else
            'rhs')
    else:
        raxit__bos += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    raxit__bos += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    raxit__bos += '    if ({}\n'.format(yqqy__beadd)
    raxit__bos += '        or {}):\n'.format(vqxf__yqt)
    raxit__bos += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    raxit__bos += '      continue\n'
    raxit__bos += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(vhmx__baye, xqn__ydmtd))
    raxit__bos += '  return out_arr\n'
    gjqkr__lai = {}
    exec(raxit__bos, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        wlpr__mrcf, 'op': op}, gjqkr__lai)
    impl = gjqkr__lai['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        qbqge__rdu = lhs in [pd_timedelta_type]
        nyszw__kxmqz = rhs in [pd_timedelta_type]
        if qbqge__rdu:

            def impl(lhs, rhs):
                n = len(rhs)
                xouw__dwmjo = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(xouw__dwmjo, i)
                        continue
                    xouw__dwmjo[i] = bodo.utils.conversion.unbox_if_timestamp(
                        op(lhs, rhs[i]))
                return xouw__dwmjo
            return impl
        elif nyszw__kxmqz:

            def impl(lhs, rhs):
                n = len(lhs)
                xouw__dwmjo = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(xouw__dwmjo, i)
                        continue
                    xouw__dwmjo[i] = bodo.utils.conversion.unbox_if_timestamp(
                        op(lhs[i], rhs))
                return xouw__dwmjo
            return impl
    return impl
