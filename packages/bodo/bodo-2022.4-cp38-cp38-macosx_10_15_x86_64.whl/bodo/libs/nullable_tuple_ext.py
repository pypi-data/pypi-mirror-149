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
        uwx__zwpxd = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, uwx__zwpxd)


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
        xptku__gwmod = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        xptku__gwmod.data = data_tuple
        xptku__gwmod.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return xptku__gwmod._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    mdyc__igbk = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, mdyc__igbk.data)
    c.context.nrt.incref(c.builder, typ.null_typ, mdyc__igbk.null_values)
    rzs__lbaxk = c.pyapi.from_native_value(typ.tuple_typ, mdyc__igbk.data,
        c.env_manager)
    gswh__qtupw = c.pyapi.from_native_value(typ.null_typ, mdyc__igbk.
        null_values, c.env_manager)
    mnw__gyflx = c.context.get_constant(types.int64, len(typ.tuple_typ))
    gms__giwm = c.pyapi.list_new(mnw__gyflx)
    with cgutils.for_range(c.builder, mnw__gyflx) as gkpyi__extgq:
        i = gkpyi__extgq.index
        zcvlx__qaood = c.pyapi.long_from_longlong(i)
        acs__ght = c.pyapi.object_getitem(gswh__qtupw, zcvlx__qaood)
        pdlx__wohp = c.pyapi.to_native_value(types.bool_, acs__ght).value
        with c.builder.if_else(pdlx__wohp) as (ocn__ttv, aijwx__ugx):
            with ocn__ttv:
                c.pyapi.list_setitem(gms__giwm, i, c.pyapi.make_none())
            with aijwx__ugx:
                jjip__ohcuk = c.pyapi.object_getitem(rzs__lbaxk, zcvlx__qaood)
                c.pyapi.list_setitem(gms__giwm, i, jjip__ohcuk)
        c.pyapi.decref(zcvlx__qaood)
        c.pyapi.decref(acs__ght)
    jeurz__hop = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    xwrx__xpm = c.pyapi.call_function_objargs(jeurz__hop, (gms__giwm,))
    c.pyapi.decref(rzs__lbaxk)
    c.pyapi.decref(gswh__qtupw)
    c.pyapi.decref(jeurz__hop)
    c.pyapi.decref(gms__giwm)
    c.context.nrt.decref(c.builder, typ, val)
    return xwrx__xpm


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
    xptku__gwmod = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (xptku__gwmod.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    pzqy__nemdt = 'def impl(val1, val2):\n'
    pzqy__nemdt += '    data_tup1 = val1._data\n'
    pzqy__nemdt += '    null_tup1 = val1._null_values\n'
    pzqy__nemdt += '    data_tup2 = val2._data\n'
    pzqy__nemdt += '    null_tup2 = val2._null_values\n'
    ztbii__nnok = val1._tuple_typ
    for i in range(len(ztbii__nnok)):
        pzqy__nemdt += f'    null1_{i} = null_tup1[{i}]\n'
        pzqy__nemdt += f'    null2_{i} = null_tup2[{i}]\n'
        pzqy__nemdt += f'    data1_{i} = data_tup1[{i}]\n'
        pzqy__nemdt += f'    data2_{i} = data_tup2[{i}]\n'
        pzqy__nemdt += f'    if null1_{i} != null2_{i}:\n'
        pzqy__nemdt += '        return False\n'
        pzqy__nemdt += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        pzqy__nemdt += f'        return False\n'
    pzqy__nemdt += f'    return True\n'
    jiqp__lyxl = {}
    exec(pzqy__nemdt, {}, jiqp__lyxl)
    impl = jiqp__lyxl['impl']
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
    pzqy__nemdt = 'def impl(nullable_tup):\n'
    pzqy__nemdt += '    data_tup = nullable_tup._data\n'
    pzqy__nemdt += '    null_tup = nullable_tup._null_values\n'
    pzqy__nemdt += (
        '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n')
    pzqy__nemdt += '    acc = _PyHASH_XXPRIME_5\n'
    ztbii__nnok = nullable_tup._tuple_typ
    for i in range(len(ztbii__nnok)):
        pzqy__nemdt += f'    null_val_{i} = null_tup[{i}]\n'
        pzqy__nemdt += f'    null_lane_{i} = hash(null_val_{i})\n'
        pzqy__nemdt += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        pzqy__nemdt += '        return -1\n'
        pzqy__nemdt += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        pzqy__nemdt += (
            '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        pzqy__nemdt += '    acc *= _PyHASH_XXPRIME_1\n'
        pzqy__nemdt += f'    if not null_val_{i}:\n'
        pzqy__nemdt += f'        lane_{i} = hash(data_tup[{i}])\n'
        pzqy__nemdt += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        pzqy__nemdt += f'            return -1\n'
        pzqy__nemdt += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        pzqy__nemdt += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        pzqy__nemdt += '        acc *= _PyHASH_XXPRIME_1\n'
    pzqy__nemdt += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    pzqy__nemdt += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    pzqy__nemdt += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    pzqy__nemdt += '    return numba.cpython.hashing.process_return(acc)\n'
    jiqp__lyxl = {}
    exec(pzqy__nemdt, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, jiqp__lyxl)
    impl = jiqp__lyxl['impl']
    return impl
