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
        mejdz__dslum = [('left', fe_type.arr_type), ('right', fe_type.arr_type)
            ]
        models.StructModel.__init__(self, dmm, fe_type, mejdz__dslum)


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
        kcf__qepn, jyjuw__myk = args
        lluwv__yyg = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        lluwv__yyg.left = kcf__qepn
        lluwv__yyg.right = jyjuw__myk
        context.nrt.incref(builder, signature.args[0], kcf__qepn)
        context.nrt.incref(builder, signature.args[1], jyjuw__myk)
        return lluwv__yyg._getvalue()
    nyn__tsu = IntervalArrayType(left)
    orjt__att = nyn__tsu(left, right)
    return orjt__att, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ghi__ntihk = []
    for pizny__xkpj in args:
        trjzp__bhc = equiv_set.get_shape(pizny__xkpj)
        if trjzp__bhc is not None:
            ghi__ntihk.append(trjzp__bhc[0])
    if len(ghi__ntihk) > 1:
        equiv_set.insert_equiv(*ghi__ntihk)
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
    lluwv__yyg = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, lluwv__yyg.left)
    mgws__hmjz = c.pyapi.from_native_value(typ.arr_type, lluwv__yyg.left, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, lluwv__yyg.right)
    ozmc__tml = c.pyapi.from_native_value(typ.arr_type, lluwv__yyg.right, c
        .env_manager)
    verxs__zdcut = c.context.insert_const_string(c.builder.module, 'pandas')
    wunjd__wwkhv = c.pyapi.import_module_noblock(verxs__zdcut)
    rncz__uoq = c.pyapi.object_getattr_string(wunjd__wwkhv, 'arrays')
    bocqy__sou = c.pyapi.object_getattr_string(rncz__uoq, 'IntervalArray')
    zxq__jkqs = c.pyapi.call_method(bocqy__sou, 'from_arrays', (mgws__hmjz,
        ozmc__tml))
    c.pyapi.decref(mgws__hmjz)
    c.pyapi.decref(ozmc__tml)
    c.pyapi.decref(wunjd__wwkhv)
    c.pyapi.decref(rncz__uoq)
    c.pyapi.decref(bocqy__sou)
    c.context.nrt.decref(c.builder, typ, val)
    return zxq__jkqs


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    mgws__hmjz = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, mgws__hmjz).value
    c.pyapi.decref(mgws__hmjz)
    ozmc__tml = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, ozmc__tml).value
    c.pyapi.decref(ozmc__tml)
    lluwv__yyg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lluwv__yyg.left = left
    lluwv__yyg.right = right
    ach__exier = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lluwv__yyg._getvalue(), is_error=ach__exier)


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
