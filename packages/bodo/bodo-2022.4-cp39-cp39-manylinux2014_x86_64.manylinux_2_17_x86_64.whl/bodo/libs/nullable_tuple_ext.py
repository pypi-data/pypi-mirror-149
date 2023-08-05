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
        nkqm__zmx = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, nkqm__zmx)


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
        ixogq__gsbvh = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ixogq__gsbvh.data = data_tuple
        ixogq__gsbvh.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return ixogq__gsbvh._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    vylji__brzj = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, vylji__brzj.data)
    c.context.nrt.incref(c.builder, typ.null_typ, vylji__brzj.null_values)
    vdmnq__wsi = c.pyapi.from_native_value(typ.tuple_typ, vylji__brzj.data,
        c.env_manager)
    loha__zhdf = c.pyapi.from_native_value(typ.null_typ, vylji__brzj.
        null_values, c.env_manager)
    xuhvp__eyv = c.context.get_constant(types.int64, len(typ.tuple_typ))
    trq__hqh = c.pyapi.list_new(xuhvp__eyv)
    with cgutils.for_range(c.builder, xuhvp__eyv) as zovp__dnqq:
        i = zovp__dnqq.index
        hlk__crvx = c.pyapi.long_from_longlong(i)
        ipgqo__rqdx = c.pyapi.object_getitem(loha__zhdf, hlk__crvx)
        cxjs__tuek = c.pyapi.to_native_value(types.bool_, ipgqo__rqdx).value
        with c.builder.if_else(cxjs__tuek) as (zlve__dnby, kpiu__tlrus):
            with zlve__dnby:
                c.pyapi.list_setitem(trq__hqh, i, c.pyapi.make_none())
            with kpiu__tlrus:
                khak__vxbsw = c.pyapi.object_getitem(vdmnq__wsi, hlk__crvx)
                c.pyapi.list_setitem(trq__hqh, i, khak__vxbsw)
        c.pyapi.decref(hlk__crvx)
        c.pyapi.decref(ipgqo__rqdx)
    xwkq__abhvv = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    vmdkr__vzb = c.pyapi.call_function_objargs(xwkq__abhvv, (trq__hqh,))
    c.pyapi.decref(vdmnq__wsi)
    c.pyapi.decref(loha__zhdf)
    c.pyapi.decref(xwkq__abhvv)
    c.pyapi.decref(trq__hqh)
    c.context.nrt.decref(c.builder, typ, val)
    return vmdkr__vzb


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
    ixogq__gsbvh = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (ixogq__gsbvh.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    ohnyw__nytqx = 'def impl(val1, val2):\n'
    ohnyw__nytqx += '    data_tup1 = val1._data\n'
    ohnyw__nytqx += '    null_tup1 = val1._null_values\n'
    ohnyw__nytqx += '    data_tup2 = val2._data\n'
    ohnyw__nytqx += '    null_tup2 = val2._null_values\n'
    dygyh__dzw = val1._tuple_typ
    for i in range(len(dygyh__dzw)):
        ohnyw__nytqx += f'    null1_{i} = null_tup1[{i}]\n'
        ohnyw__nytqx += f'    null2_{i} = null_tup2[{i}]\n'
        ohnyw__nytqx += f'    data1_{i} = data_tup1[{i}]\n'
        ohnyw__nytqx += f'    data2_{i} = data_tup2[{i}]\n'
        ohnyw__nytqx += f'    if null1_{i} != null2_{i}:\n'
        ohnyw__nytqx += '        return False\n'
        ohnyw__nytqx += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        ohnyw__nytqx += f'        return False\n'
    ohnyw__nytqx += f'    return True\n'
    ihn__qrp = {}
    exec(ohnyw__nytqx, {}, ihn__qrp)
    impl = ihn__qrp['impl']
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
    ohnyw__nytqx = 'def impl(nullable_tup):\n'
    ohnyw__nytqx += '    data_tup = nullable_tup._data\n'
    ohnyw__nytqx += '    null_tup = nullable_tup._null_values\n'
    ohnyw__nytqx += (
        '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n')
    ohnyw__nytqx += '    acc = _PyHASH_XXPRIME_5\n'
    dygyh__dzw = nullable_tup._tuple_typ
    for i in range(len(dygyh__dzw)):
        ohnyw__nytqx += f'    null_val_{i} = null_tup[{i}]\n'
        ohnyw__nytqx += f'    null_lane_{i} = hash(null_val_{i})\n'
        ohnyw__nytqx += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        ohnyw__nytqx += '        return -1\n'
        ohnyw__nytqx += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        ohnyw__nytqx += (
            '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        ohnyw__nytqx += '    acc *= _PyHASH_XXPRIME_1\n'
        ohnyw__nytqx += f'    if not null_val_{i}:\n'
        ohnyw__nytqx += f'        lane_{i} = hash(data_tup[{i}])\n'
        ohnyw__nytqx += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        ohnyw__nytqx += f'            return -1\n'
        ohnyw__nytqx += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        ohnyw__nytqx += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        ohnyw__nytqx += '        acc *= _PyHASH_XXPRIME_1\n'
    ohnyw__nytqx += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    ohnyw__nytqx += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    ohnyw__nytqx += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    ohnyw__nytqx += '    return numba.cpython.hashing.process_return(acc)\n'
    ihn__qrp = {}
    exec(ohnyw__nytqx, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, ihn__qrp)
    impl = ihn__qrp['impl']
    return impl
