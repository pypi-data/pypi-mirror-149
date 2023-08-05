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
        guchk__ebcts = [('left', fe_type.arr_type), ('right', fe_type.arr_type)
            ]
        models.StructModel.__init__(self, dmm, fe_type, guchk__ebcts)


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
        uxq__fydy, qwvoc__fmp = args
        pkuwy__sbn = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        pkuwy__sbn.left = uxq__fydy
        pkuwy__sbn.right = qwvoc__fmp
        context.nrt.incref(builder, signature.args[0], uxq__fydy)
        context.nrt.incref(builder, signature.args[1], qwvoc__fmp)
        return pkuwy__sbn._getvalue()
    eul__ogey = IntervalArrayType(left)
    qhmxn__eqe = eul__ogey(left, right)
    return qhmxn__eqe, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    kve__qsz = []
    for fohn__scm in args:
        xflg__apgf = equiv_set.get_shape(fohn__scm)
        if xflg__apgf is not None:
            kve__qsz.append(xflg__apgf[0])
    if len(kve__qsz) > 1:
        equiv_set.insert_equiv(*kve__qsz)
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
    pkuwy__sbn = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, pkuwy__sbn.left)
    xmqfc__gpwmz = c.pyapi.from_native_value(typ.arr_type, pkuwy__sbn.left,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, pkuwy__sbn.right)
    epfsl__hxip = c.pyapi.from_native_value(typ.arr_type, pkuwy__sbn.right,
        c.env_manager)
    ilunq__wpcom = c.context.insert_const_string(c.builder.module, 'pandas')
    toeu__hxb = c.pyapi.import_module_noblock(ilunq__wpcom)
    hhct__dtxf = c.pyapi.object_getattr_string(toeu__hxb, 'arrays')
    hpplq__yhdd = c.pyapi.object_getattr_string(hhct__dtxf, 'IntervalArray')
    ena__kxu = c.pyapi.call_method(hpplq__yhdd, 'from_arrays', (
        xmqfc__gpwmz, epfsl__hxip))
    c.pyapi.decref(xmqfc__gpwmz)
    c.pyapi.decref(epfsl__hxip)
    c.pyapi.decref(toeu__hxb)
    c.pyapi.decref(hhct__dtxf)
    c.pyapi.decref(hpplq__yhdd)
    c.context.nrt.decref(c.builder, typ, val)
    return ena__kxu


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    xmqfc__gpwmz = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, xmqfc__gpwmz).value
    c.pyapi.decref(xmqfc__gpwmz)
    epfsl__hxip = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, epfsl__hxip).value
    c.pyapi.decref(epfsl__hxip)
    pkuwy__sbn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    pkuwy__sbn.left = left
    pkuwy__sbn.right = right
    zpj__bvr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(pkuwy__sbn._getvalue(), is_error=zpj__bvr)


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
