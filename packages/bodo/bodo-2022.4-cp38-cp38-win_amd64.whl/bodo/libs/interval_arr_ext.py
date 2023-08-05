"""
Array of intervals corresponding to IntervalArray of Pandas.
Used for IntervalIndex, which is necessary for Series.value_counts() with 'bins'
argument.
"""
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo


class IntervalType(types.Type):

    def __init__(self):
        super(IntervalType, self).__init__('IntervalType()')


class IntervalArrayType(types.ArrayCompatible):

    def __init__(self, arr_type):
        self.arr_type = arr_type
        self.dtype = IntervalType()
        super(IntervalArrayType, self).__init__(name=
            f'IntervalArrayType({arr_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntervalArrayType(self.arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(IntervalArrayType)
class IntervalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        anaf__cml = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, anaf__cml)


make_attribute_wrapper(IntervalArrayType, 'left', '_left')
make_attribute_wrapper(IntervalArrayType, 'right', '_right')


@typeof_impl.register(pd.arrays.IntervalArray)
def typeof_interval_array(val, c):
    arr_type = bodo.typeof(val._left)
    return IntervalArrayType(arr_type)


@intrinsic
def init_interval_array(typingctx, left, right=None):
    assert left == right, 'Interval left/right array types should be the same'

    def codegen(context, builder, signature, args):
        oumn__aktf, rhr__xzj = args
        kfkv__aeenk = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        kfkv__aeenk.left = oumn__aktf
        kfkv__aeenk.right = rhr__xzj
        context.nrt.incref(builder, signature.args[0], oumn__aktf)
        context.nrt.incref(builder, signature.args[1], rhr__xzj)
        return kfkv__aeenk._getvalue()
    jxsv__vbwt = IntervalArrayType(left)
    ymy__bzdi = jxsv__vbwt(left, right)
    return ymy__bzdi, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    wvjum__grigu = []
    for cgm__gehf in args:
        srwk__rlp = equiv_set.get_shape(cgm__gehf)
        if srwk__rlp is not None:
            wvjum__grigu.append(srwk__rlp[0])
    if len(wvjum__grigu) > 1:
        equiv_set.insert_equiv(*wvjum__grigu)
    left = args[0]
    if equiv_set.has_shape(left):
        return ArrayAnalysis.AnalyzeResult(shape=left, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_interval_arr_ext_init_interval_array
    ) = init_interval_array_equiv


def alias_ext_init_interval_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_interval_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_interval_array


@box(IntervalArrayType)
def box_interval_arr(typ, val, c):
    kfkv__aeenk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, kfkv__aeenk.left)
    wzfp__irp = c.pyapi.from_native_value(typ.arr_type, kfkv__aeenk.left, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, kfkv__aeenk.right)
    kpz__iyb = c.pyapi.from_native_value(typ.arr_type, kfkv__aeenk.right, c
        .env_manager)
    wljk__jtw = c.context.insert_const_string(c.builder.module, 'pandas')
    trrzh__owj = c.pyapi.import_module_noblock(wljk__jtw)
    oka__ihfmp = c.pyapi.object_getattr_string(trrzh__owj, 'arrays')
    vgcdw__ter = c.pyapi.object_getattr_string(oka__ihfmp, 'IntervalArray')
    vdrz__zvekv = c.pyapi.call_method(vgcdw__ter, 'from_arrays', (wzfp__irp,
        kpz__iyb))
    c.pyapi.decref(wzfp__irp)
    c.pyapi.decref(kpz__iyb)
    c.pyapi.decref(trrzh__owj)
    c.pyapi.decref(oka__ihfmp)
    c.pyapi.decref(vgcdw__ter)
    c.context.nrt.decref(c.builder, typ, val)
    return vdrz__zvekv


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    wzfp__irp = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, wzfp__irp).value
    c.pyapi.decref(wzfp__irp)
    kpz__iyb = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, kpz__iyb).value
    c.pyapi.decref(kpz__iyb)
    kfkv__aeenk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    kfkv__aeenk.left = left
    kfkv__aeenk.right = right
    hurb__njmx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(kfkv__aeenk._getvalue(), is_error=hurb__njmx)


@overload(len, no_unliteral=True)
def overload_interval_arr_len(A):
    if isinstance(A, IntervalArrayType):
        return lambda A: len(A._left)


@overload_attribute(IntervalArrayType, 'shape')
def overload_interval_arr_shape(A):
    return lambda A: (len(A._left),)


@overload_attribute(IntervalArrayType, 'ndim')
def overload_interval_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntervalArrayType, 'nbytes')
def overload_interval_arr_nbytes(A):
    return lambda A: A._left.nbytes + A._right.nbytes


@overload_method(IntervalArrayType, 'copy', no_unliteral=True)
def overload_interval_arr_copy(A):
    return lambda A: bodo.libs.interval_arr_ext.init_interval_array(A._left
        .copy(), A._right.copy())
