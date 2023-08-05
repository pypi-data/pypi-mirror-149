"""
Wrapper class for Tuples that supports tracking null entries.
This is primarily used for maintaining null information for
Series values used in df.apply
"""
import operator
import numba
from numba.core import cgutils, types
from numba.extending import box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model


class NullableTupleType(types.IterableType):

    def __init__(self, tuple_typ, null_typ):
        self._tuple_typ = tuple_typ
        self._null_typ = null_typ
        super(NullableTupleType, self).__init__(name=
            f'NullableTupleType({tuple_typ}, {null_typ})')

    @property
    def tuple_typ(self):
        return self._tuple_typ

    @property
    def null_typ(self):
        return self._null_typ

    def __getitem__(self, i):
        return self._tuple_typ[i]

    @property
    def key(self):
        return self._tuple_typ

    @property
    def dtype(self):
        return self.tuple_typ.dtype

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def iterator_type(self):
        return self.tuple_typ.iterator_type

    def __len__(self):
        return len(self.tuple_typ)


@register_model(NullableTupleType)
class NullableTupleModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        oitgk__rozwc = [('data', fe_type.tuple_typ), ('null_values',
            fe_type.null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, oitgk__rozwc)


make_attribute_wrapper(NullableTupleType, 'data', '_data')
make_attribute_wrapper(NullableTupleType, 'null_values', '_null_values')


@intrinsic
def build_nullable_tuple(typingctx, data_tuple, null_values):
    assert isinstance(data_tuple, types.BaseTuple
        ), "build_nullable_tuple 'data_tuple' argument must be a tuple"
    assert isinstance(null_values, types.BaseTuple
        ), "build_nullable_tuple 'null_values' argument must be a tuple"
    data_tuple = types.unliteral(data_tuple)
    null_values = types.unliteral(null_values)

    def codegen(context, builder, signature, args):
        data_tuple, null_values = args
        jdimh__rdhqh = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        jdimh__rdhqh.data = data_tuple
        jdimh__rdhqh.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return jdimh__rdhqh._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    hihrs__zpe = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, hihrs__zpe.data)
    c.context.nrt.incref(c.builder, typ.null_typ, hihrs__zpe.null_values)
    jpbr__yqwc = c.pyapi.from_native_value(typ.tuple_typ, hihrs__zpe.data,
        c.env_manager)
    ulpkr__ghqr = c.pyapi.from_native_value(typ.null_typ, hihrs__zpe.
        null_values, c.env_manager)
    arjcc__ynzqx = c.context.get_constant(types.int64, len(typ.tuple_typ))
    oziz__qxdnr = c.pyapi.list_new(arjcc__ynzqx)
    with cgutils.for_range(c.builder, arjcc__ynzqx) as ydbr__rzra:
        i = ydbr__rzra.index
        lvx__vje = c.pyapi.long_from_longlong(i)
        rbey__luloq = c.pyapi.object_getitem(ulpkr__ghqr, lvx__vje)
        fxg__pofbz = c.pyapi.to_native_value(types.bool_, rbey__luloq).value
        with c.builder.if_else(fxg__pofbz) as (pnwu__glle, yby__brieh):
            with pnwu__glle:
                c.pyapi.list_setitem(oziz__qxdnr, i, c.pyapi.make_none())
            with yby__brieh:
                nrpiy__iios = c.pyapi.object_getitem(jpbr__yqwc, lvx__vje)
                c.pyapi.list_setitem(oziz__qxdnr, i, nrpiy__iios)
        c.pyapi.decref(lvx__vje)
        c.pyapi.decref(rbey__luloq)
    dantd__oywlp = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    zhlh__dyg = c.pyapi.call_function_objargs(dantd__oywlp, (oziz__qxdnr,))
    c.pyapi.decref(jpbr__yqwc)
    c.pyapi.decref(ulpkr__ghqr)
    c.pyapi.decref(dantd__oywlp)
    c.pyapi.decref(oziz__qxdnr)
    c.context.nrt.decref(c.builder, typ, val)
    return zhlh__dyg


@overload(operator.getitem)
def overload_getitem(A, idx):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A, idx: A._data[idx]


@overload(len)
def overload_len(A):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A: len(A._data)


@lower_builtin('getiter', NullableTupleType)
def nullable_tuple_getiter(context, builder, sig, args):
    jdimh__rdhqh = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (jdimh__rdhqh.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    qghdo__modo = 'def impl(val1, val2):\n'
    qghdo__modo += '    data_tup1 = val1._data\n'
    qghdo__modo += '    null_tup1 = val1._null_values\n'
    qghdo__modo += '    data_tup2 = val2._data\n'
    qghdo__modo += '    null_tup2 = val2._null_values\n'
    rtu__azek = val1._tuple_typ
    for i in range(len(rtu__azek)):
        qghdo__modo += f'    null1_{i} = null_tup1[{i}]\n'
        qghdo__modo += f'    null2_{i} = null_tup2[{i}]\n'
        qghdo__modo += f'    data1_{i} = data_tup1[{i}]\n'
        qghdo__modo += f'    data2_{i} = data_tup2[{i}]\n'
        qghdo__modo += f'    if null1_{i} != null2_{i}:\n'
        qghdo__modo += '        return False\n'
        qghdo__modo += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        qghdo__modo += f'        return False\n'
    qghdo__modo += f'    return True\n'
    ztv__pvjb = {}
    exec(qghdo__modo, {}, ztv__pvjb)
    impl = ztv__pvjb['impl']
    return impl


@overload_method(NullableTupleType, '__hash__')
def nullable_tuple_hash(val):

    def impl(val):
        return _nullable_tuple_hash(val)
    return impl


_PyHASH_XXPRIME_1 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_2 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_5 = numba.cpython.hashing._PyHASH_XXPRIME_1


@numba.generated_jit(nopython=True)
def _nullable_tuple_hash(nullable_tup):
    qghdo__modo = 'def impl(nullable_tup):\n'
    qghdo__modo += '    data_tup = nullable_tup._data\n'
    qghdo__modo += '    null_tup = nullable_tup._null_values\n'
    qghdo__modo += (
        '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n')
    qghdo__modo += '    acc = _PyHASH_XXPRIME_5\n'
    rtu__azek = nullable_tup._tuple_typ
    for i in range(len(rtu__azek)):
        qghdo__modo += f'    null_val_{i} = null_tup[{i}]\n'
        qghdo__modo += f'    null_lane_{i} = hash(null_val_{i})\n'
        qghdo__modo += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        qghdo__modo += '        return -1\n'
        qghdo__modo += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        qghdo__modo += (
            '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        qghdo__modo += '    acc *= _PyHASH_XXPRIME_1\n'
        qghdo__modo += f'    if not null_val_{i}:\n'
        qghdo__modo += f'        lane_{i} = hash(data_tup[{i}])\n'
        qghdo__modo += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        qghdo__modo += f'            return -1\n'
        qghdo__modo += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        qghdo__modo += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        qghdo__modo += '        acc *= _PyHASH_XXPRIME_1\n'
    qghdo__modo += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    qghdo__modo += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    qghdo__modo += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    qghdo__modo += '    return numba.cpython.hashing.process_return(acc)\n'
    ztv__pvjb = {}
    exec(qghdo__modo, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, ztv__pvjb)
    impl = ztv__pvjb['impl']
    return impl
