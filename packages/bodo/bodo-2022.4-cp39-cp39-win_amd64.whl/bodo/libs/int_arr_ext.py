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
        iwl__bfb = int(np.log2(self.dtype.bitwidth // 8))
        quuv__mkaw = 0 if self.dtype.signed else 4
        idx = iwl__bfb + quuv__mkaw
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mgz__jxuk = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, mgz__jxuk)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    oko__yxkca = 8 * val.dtype.itemsize
    uevj__okk = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(uevj__okk, oko__yxkca))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        dukjs__rss = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(dukjs__rss)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    tva__ulwdx = c.context.insert_const_string(c.builder.module, 'pandas')
    mkdg__mgmm = c.pyapi.import_module_noblock(tva__ulwdx)
    vitfk__fboxt = c.pyapi.call_method(mkdg__mgmm, str(typ)[:-2], ())
    c.pyapi.decref(mkdg__mgmm)
    return vitfk__fboxt


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    oko__yxkca = 8 * val.itemsize
    uevj__okk = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(uevj__okk, oko__yxkca))
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
    qxal__xuwn = n + 7 >> 3
    vnc__scs = np.empty(qxal__xuwn, np.uint8)
    for i in range(n):
        afyqz__rua = i // 8
        vnc__scs[afyqz__rua] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            vnc__scs[afyqz__rua]) & kBitmask[i % 8]
    return vnc__scs


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    twfaf__mrcd = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(twfaf__mrcd)
    c.pyapi.decref(twfaf__mrcd)
    ntl__saf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qxal__xuwn = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    etv__phvfi = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [qxal__xuwn])
    nlf__heblf = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    vyjf__bcq = cgutils.get_or_insert_function(c.builder.module, nlf__heblf,
        name='is_pd_int_array')
    ezko__vmlqn = c.builder.call(vyjf__bcq, [obj])
    vxpqy__rxpt = c.builder.icmp_unsigned('!=', ezko__vmlqn, ezko__vmlqn.
        type(0))
    with c.builder.if_else(vxpqy__rxpt) as (will__oghbr, cfv__gec):
        with will__oghbr:
            zuv__auh = c.pyapi.object_getattr_string(obj, '_data')
            ntl__saf.data = c.pyapi.to_native_value(types.Array(typ.dtype, 
                1, 'C'), zuv__auh).value
            ddp__dosjs = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), ddp__dosjs).value
            c.pyapi.decref(zuv__auh)
            c.pyapi.decref(ddp__dosjs)
            wkb__pzqgz = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, mask_arr)
            nlf__heblf = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            vyjf__bcq = cgutils.get_or_insert_function(c.builder.module,
                nlf__heblf, name='mask_arr_to_bitmap')
            c.builder.call(vyjf__bcq, [etv__phvfi.data, wkb__pzqgz.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with cfv__gec:
            nnau__pxji = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            nlf__heblf = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            bipyp__cvglo = cgutils.get_or_insert_function(c.builder.module,
                nlf__heblf, name='int_array_from_sequence')
            c.builder.call(bipyp__cvglo, [obj, c.builder.bitcast(nnau__pxji
                .data, lir.IntType(8).as_pointer()), etv__phvfi.data])
            ntl__saf.data = nnau__pxji._getvalue()
    ntl__saf.null_bitmap = etv__phvfi._getvalue()
    gdqz__ldi = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ntl__saf._getvalue(), is_error=gdqz__ldi)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    ntl__saf = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        ntl__saf.data, c.env_manager)
    ssex__iibe = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, ntl__saf.null_bitmap).data
    twfaf__mrcd = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(twfaf__mrcd)
    tva__ulwdx = c.context.insert_const_string(c.builder.module, 'numpy')
    mtlj__qnbg = c.pyapi.import_module_noblock(tva__ulwdx)
    dtonu__tfd = c.pyapi.object_getattr_string(mtlj__qnbg, 'bool_')
    mask_arr = c.pyapi.call_method(mtlj__qnbg, 'empty', (twfaf__mrcd,
        dtonu__tfd))
    ypndi__ooxxq = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    jmlba__llgtm = c.pyapi.object_getattr_string(ypndi__ooxxq, 'data')
    cbu__nsohy = c.builder.inttoptr(c.pyapi.long_as_longlong(jmlba__llgtm),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as lim__shjhj:
        i = lim__shjhj.index
        brx__zqj = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        fgp__ldufx = c.builder.load(cgutils.gep(c.builder, ssex__iibe,
            brx__zqj))
        cgnjx__tlij = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(fgp__ldufx, cgnjx__tlij), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        iwf__nlhfq = cgutils.gep(c.builder, cbu__nsohy, i)
        c.builder.store(val, iwf__nlhfq)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        ntl__saf.null_bitmap)
    tva__ulwdx = c.context.insert_const_string(c.builder.module, 'pandas')
    mkdg__mgmm = c.pyapi.import_module_noblock(tva__ulwdx)
    ayka__qpr = c.pyapi.object_getattr_string(mkdg__mgmm, 'arrays')
    vitfk__fboxt = c.pyapi.call_method(ayka__qpr, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(mkdg__mgmm)
    c.pyapi.decref(twfaf__mrcd)
    c.pyapi.decref(mtlj__qnbg)
    c.pyapi.decref(dtonu__tfd)
    c.pyapi.decref(ypndi__ooxxq)
    c.pyapi.decref(jmlba__llgtm)
    c.pyapi.decref(ayka__qpr)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return vitfk__fboxt


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        lns__cnml, vyxu__yton = args
        ntl__saf = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        ntl__saf.data = lns__cnml
        ntl__saf.null_bitmap = vyxu__yton
        context.nrt.incref(builder, signature.args[0], lns__cnml)
        context.nrt.incref(builder, signature.args[1], vyxu__yton)
        return ntl__saf._getvalue()
    hapo__ejc = IntegerArrayType(data.dtype)
    cwzso__mqr = hapo__ejc(data, null_bitmap)
    return cwzso__mqr, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    uhdc__kbljg = np.empty(n, pyval.dtype.type)
    ejhht__nodur = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        zbdlo__fzvmd = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ejhht__nodur, i, int(not
            zbdlo__fzvmd))
        if not zbdlo__fzvmd:
            uhdc__kbljg[i] = s
    koypu__vxdf = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), uhdc__kbljg)
    vbtwm__gbbqe = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), ejhht__nodur)
    return lir.Constant.literal_struct([koypu__vxdf, vbtwm__gbbqe])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    avuo__mcdds = args[0]
    if equiv_set.has_shape(avuo__mcdds):
        return ArrayAnalysis.AnalyzeResult(shape=avuo__mcdds, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    avuo__mcdds = args[0]
    if equiv_set.has_shape(avuo__mcdds):
        return ArrayAnalysis.AnalyzeResult(shape=avuo__mcdds, pre=[])
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
    uhdc__kbljg = np.empty(n, dtype)
    wpm__cmbrm = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(uhdc__kbljg, wpm__cmbrm)


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
            biyo__jwwtx, vntqu__dvpts = array_getitem_bool_index(A, ind)
            return init_integer_array(biyo__jwwtx, vntqu__dvpts)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            biyo__jwwtx, vntqu__dvpts = array_getitem_int_index(A, ind)
            return init_integer_array(biyo__jwwtx, vntqu__dvpts)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            biyo__jwwtx, vntqu__dvpts = array_getitem_slice_index(A, ind)
            return init_integer_array(biyo__jwwtx, vntqu__dvpts)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    ytzow__swbn = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    iyrxz__aiofq = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if iyrxz__aiofq:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(ytzow__swbn)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or iyrxz__aiofq):
        raise BodoError(ytzow__swbn)
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
            skm__buq = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                skm__buq[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    skm__buq[i] = np.nan
            return skm__buq
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
                dcsh__djwgl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                gdsk__xwpuw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                vpkso__depk = dcsh__djwgl & gdsk__xwpuw
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, vpkso__depk)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        qxal__xuwn = n + 7 >> 3
        skm__buq = np.empty(qxal__xuwn, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            dcsh__djwgl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            gdsk__xwpuw = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            vpkso__depk = dcsh__djwgl & gdsk__xwpuw
            bodo.libs.int_arr_ext.set_bit_to_arr(skm__buq, i, vpkso__depk)
        return skm__buq
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
    for qnqq__auru in numba.np.ufunc_db.get_ufuncs():
        efn__xwhe = create_op_overload(qnqq__auru, qnqq__auru.nin)
        overload(qnqq__auru, no_unliteral=True)(efn__xwhe)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        efn__xwhe = create_op_overload(op, 2)
        overload(op)(efn__xwhe)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        efn__xwhe = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(efn__xwhe)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        efn__xwhe = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(efn__xwhe)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    vxuh__qbk = len(arrs.types)
    nza__lhj = 'def f(arrs):\n'
    vitfk__fboxt = ', '.join('arrs[{}]._data'.format(i) for i in range(
        vxuh__qbk))
    nza__lhj += '  return ({}{})\n'.format(vitfk__fboxt, ',' if vxuh__qbk ==
        1 else '')
    tmz__lvyqi = {}
    exec(nza__lhj, {}, tmz__lvyqi)
    impl = tmz__lvyqi['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    vxuh__qbk = len(arrs.types)
    rik__vbw = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        vxuh__qbk))
    nza__lhj = 'def f(arrs):\n'
    nza__lhj += '  n = {}\n'.format(rik__vbw)
    nza__lhj += '  n_bytes = (n + 7) >> 3\n'
    nza__lhj += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    nza__lhj += '  curr_bit = 0\n'
    for i in range(vxuh__qbk):
        nza__lhj += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        nza__lhj += '  for j in range(len(arrs[{}])):\n'.format(i)
        nza__lhj += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        nza__lhj += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        nza__lhj += '    curr_bit += 1\n'
    nza__lhj += '  return new_mask\n'
    tmz__lvyqi = {}
    exec(nza__lhj, {'np': np, 'bodo': bodo}, tmz__lvyqi)
    impl = tmz__lvyqi['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    wnhml__vredd = dict(skipna=skipna, min_count=min_count)
    zbx__rvf = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', wnhml__vredd, zbx__rvf)

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
        cgnjx__tlij = []
        naxjs__fzfh = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not naxjs__fzfh:
                    data.append(dtype(1))
                    cgnjx__tlij.append(False)
                    naxjs__fzfh = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                cgnjx__tlij.append(True)
        biyo__jwwtx = np.array(data)
        n = len(biyo__jwwtx)
        qxal__xuwn = n + 7 >> 3
        vntqu__dvpts = np.empty(qxal__xuwn, np.uint8)
        for xuep__qlcnj in range(n):
            set_bit_to_arr(vntqu__dvpts, xuep__qlcnj, cgnjx__tlij[xuep__qlcnj])
        return init_integer_array(biyo__jwwtx, vntqu__dvpts)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    vyjdr__ofzyj = numba.core.registry.cpu_target.typing_context
    dnlcs__asp = vyjdr__ofzyj.resolve_function_type(op, (types.Array(A.
        dtype, 1, 'C'),), {}).return_type
    dnlcs__asp = to_nullable_type(dnlcs__asp)

    def impl(A):
        n = len(A)
        ycxs__zqvr = bodo.utils.utils.alloc_type(n, dnlcs__asp, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(ycxs__zqvr, i)
                continue
            ycxs__zqvr[i] = op(A[i])
        return ycxs__zqvr
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    cma__asbb = isinstance(lhs, (types.Number, types.Boolean))
    xpxyo__pids = isinstance(rhs, (types.Number, types.Boolean))
    evsh__dsotk = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    uwyf__hzvh = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    vyjdr__ofzyj = numba.core.registry.cpu_target.typing_context
    dnlcs__asp = vyjdr__ofzyj.resolve_function_type(op, (evsh__dsotk,
        uwyf__hzvh), {}).return_type
    dnlcs__asp = to_nullable_type(dnlcs__asp)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    ivma__jmu = 'lhs' if cma__asbb else 'lhs[i]'
    fou__njvpx = 'rhs' if xpxyo__pids else 'rhs[i]'
    zph__opgv = ('False' if cma__asbb else
        'bodo.libs.array_kernels.isna(lhs, i)')
    himfu__eddop = ('False' if xpxyo__pids else
        'bodo.libs.array_kernels.isna(rhs, i)')
    nza__lhj = 'def impl(lhs, rhs):\n'
    nza__lhj += '  n = len({})\n'.format('lhs' if not cma__asbb else 'rhs')
    if inplace:
        nza__lhj += '  out_arr = {}\n'.format('lhs' if not cma__asbb else 'rhs'
            )
    else:
        nza__lhj += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    nza__lhj += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    nza__lhj += '    if ({}\n'.format(zph__opgv)
    nza__lhj += '        or {}):\n'.format(himfu__eddop)
    nza__lhj += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    nza__lhj += '      continue\n'
    nza__lhj += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(ivma__jmu, fou__njvpx))
    nza__lhj += '  return out_arr\n'
    tmz__lvyqi = {}
    exec(nza__lhj, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        dnlcs__asp, 'op': op}, tmz__lvyqi)
    impl = tmz__lvyqi['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        cma__asbb = lhs in [pd_timedelta_type]
        xpxyo__pids = rhs in [pd_timedelta_type]
        if cma__asbb:

            def impl(lhs, rhs):
                n = len(rhs)
                ycxs__zqvr = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(ycxs__zqvr, i)
                        continue
                    ycxs__zqvr[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return ycxs__zqvr
            return impl
        elif xpxyo__pids:

            def impl(lhs, rhs):
                n = len(lhs)
                ycxs__zqvr = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(ycxs__zqvr, i)
                        continue
                    ycxs__zqvr[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return ycxs__zqvr
            return impl
    return impl
