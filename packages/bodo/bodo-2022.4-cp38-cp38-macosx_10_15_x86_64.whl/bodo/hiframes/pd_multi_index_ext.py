"""Support for MultiIndex type of Pandas
"""
import operator
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_val_type_maybe_str_literal, is_overload_none


class MultiIndexType(types.Type):

    def __init__(self, array_types, names_typ=None, name_typ=None):
        names_typ = (types.none,) * len(array_types
            ) if names_typ is None else names_typ
        name_typ = types.none if name_typ is None else name_typ
        self.array_types = array_types
        self.names_typ = names_typ
        self.name_typ = name_typ
        super(MultiIndexType, self).__init__(name=
            'MultiIndexType({}, {}, {})'.format(array_types, names_typ,
            name_typ))
    ndim = 1

    def copy(self):
        return MultiIndexType(self.array_types, self.names_typ, self.name_typ)

    @property
    def nlevels(self):
        return len(self.array_types)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(MultiIndexType)
class MultiIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pbv__dddgx = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, pbv__dddgx)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[kyd__bjth].values) for
        kyd__bjth in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (cykt__cau) for cykt__cau in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    wms__jlih = c.context.insert_const_string(c.builder.module, 'pandas')
    qbvq__okq = c.pyapi.import_module_noblock(wms__jlih)
    ctxpk__uxe = c.pyapi.object_getattr_string(qbvq__okq, 'MultiIndex')
    fjiw__hkpbc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        fjiw__hkpbc.data)
    mlw__fiyp = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        fjiw__hkpbc.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), fjiw__hkpbc
        .names)
    qyij__xbsnk = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        fjiw__hkpbc.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, fjiw__hkpbc.name)
    zbpcc__yibrd = c.pyapi.from_native_value(typ.name_typ, fjiw__hkpbc.name,
        c.env_manager)
    ajcn__uljp = c.pyapi.borrow_none()
    meozp__ewrwq = c.pyapi.call_method(ctxpk__uxe, 'from_arrays', (
        mlw__fiyp, ajcn__uljp, qyij__xbsnk))
    c.pyapi.object_setattr_string(meozp__ewrwq, 'name', zbpcc__yibrd)
    c.pyapi.decref(mlw__fiyp)
    c.pyapi.decref(qyij__xbsnk)
    c.pyapi.decref(zbpcc__yibrd)
    c.pyapi.decref(qbvq__okq)
    c.pyapi.decref(ctxpk__uxe)
    c.context.nrt.decref(c.builder, typ, val)
    return meozp__ewrwq


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    utplu__nwfqh = []
    qwo__hjtah = []
    for kyd__bjth in range(typ.nlevels):
        sll__aro = c.pyapi.unserialize(c.pyapi.serialize_object(kyd__bjth))
        zrn__ijs = c.pyapi.call_method(val, 'get_level_values', (sll__aro,))
        edv__ygnk = c.pyapi.object_getattr_string(zrn__ijs, 'values')
        c.pyapi.decref(zrn__ijs)
        c.pyapi.decref(sll__aro)
        fvk__vrfj = c.pyapi.to_native_value(typ.array_types[kyd__bjth],
            edv__ygnk).value
        utplu__nwfqh.append(fvk__vrfj)
        qwo__hjtah.append(edv__ygnk)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, utplu__nwfqh)
    else:
        data = cgutils.pack_struct(c.builder, utplu__nwfqh)
    qyij__xbsnk = c.pyapi.object_getattr_string(val, 'names')
    zaoiw__oabtc = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    fwrpf__ielrh = c.pyapi.call_function_objargs(zaoiw__oabtc, (qyij__xbsnk,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), fwrpf__ielrh
        ).value
    zbpcc__yibrd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zbpcc__yibrd).value
    fjiw__hkpbc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fjiw__hkpbc.data = data
    fjiw__hkpbc.names = names
    fjiw__hkpbc.name = name
    for edv__ygnk in qwo__hjtah:
        c.pyapi.decref(edv__ygnk)
    c.pyapi.decref(qyij__xbsnk)
    c.pyapi.decref(zaoiw__oabtc)
    c.pyapi.decref(fwrpf__ielrh)
    c.pyapi.decref(zbpcc__yibrd)
    return NativeValue(fjiw__hkpbc._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    prr__tgsv = 'pandas.MultiIndex.from_product'
    rlhj__uyu = dict(sortorder=sortorder)
    zdukl__ejb = dict(sortorder=None)
    check_unsupported_args(prr__tgsv, rlhj__uyu, zdukl__ejb, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{prr__tgsv}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{prr__tgsv}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{prr__tgsv}: iterables and names must be of the same length.')


def from_product(iterable, sortorder=None, names=None):
    pass


@overload(from_product)
def from_product_overload(iterables, sortorder=None, names=None):
    from_product_error_checking(iterables, sortorder, names)
    array_types = tuple(dtype_to_array_type(iterable.dtype) for iterable in
        iterables)
    if is_overload_none(names):
        names_typ = tuple([types.none] * len(iterables))
    else:
        names_typ = names.types
    jah__uta = MultiIndexType(array_types, names_typ)
    excum__yzx = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, excum__yzx, jah__uta)
    vex__ouar = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{excum__yzx}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    xpyg__dvm = {}
    exec(vex__ouar, globals(), xpyg__dvm)
    oqlnm__gvp = xpyg__dvm['impl']
    return oqlnm__gvp


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        woobr__jyq, rpog__pti, lvnzw__xns = args
        cnaln__low = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        cnaln__low.data = woobr__jyq
        cnaln__low.names = rpog__pti
        cnaln__low.name = lvnzw__xns
        context.nrt.incref(builder, signature.args[0], woobr__jyq)
        context.nrt.incref(builder, signature.args[1], rpog__pti)
        context.nrt.incref(builder, signature.args[2], lvnzw__xns)
        return cnaln__low._getvalue()
    zept__tzbdq = MultiIndexType(data.types, names.types, name)
    return zept__tzbdq(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        epc__mbii = len(I.array_types)
        vex__ouar = 'def impl(I, ind):\n'
        vex__ouar += '  data = I._data\n'
        vex__ouar += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{kyd__bjth}][ind])' for kyd__bjth in
            range(epc__mbii))))
        xpyg__dvm = {}
        exec(vex__ouar, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, xpyg__dvm)
        oqlnm__gvp = xpyg__dvm['impl']
        return oqlnm__gvp


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    cud__zynt, qdh__tghgi = sig.args
    if cud__zynt != qdh__tghgi:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
