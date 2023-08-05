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
        nkyps__wcme = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, nkyps__wcme)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[xdsmn__fcyv].values) for
        xdsmn__fcyv in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (kjhd__cfdxk) for kjhd__cfdxk in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    kmdjr__npidk = c.context.insert_const_string(c.builder.module, 'pandas')
    uro__wup = c.pyapi.import_module_noblock(kmdjr__npidk)
    rjntl__sokm = c.pyapi.object_getattr_string(uro__wup, 'MultiIndex')
    gnp__ygyqk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        gnp__ygyqk.data)
    pge__clll = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        gnp__ygyqk.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), gnp__ygyqk.
        names)
    apmxk__gxo = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        gnp__ygyqk.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, gnp__ygyqk.name)
    jhd__lxsuw = c.pyapi.from_native_value(typ.name_typ, gnp__ygyqk.name, c
        .env_manager)
    fohf__ydun = c.pyapi.borrow_none()
    alw__ctdyb = c.pyapi.call_method(rjntl__sokm, 'from_arrays', (pge__clll,
        fohf__ydun, apmxk__gxo))
    c.pyapi.object_setattr_string(alw__ctdyb, 'name', jhd__lxsuw)
    c.pyapi.decref(pge__clll)
    c.pyapi.decref(apmxk__gxo)
    c.pyapi.decref(jhd__lxsuw)
    c.pyapi.decref(uro__wup)
    c.pyapi.decref(rjntl__sokm)
    c.context.nrt.decref(c.builder, typ, val)
    return alw__ctdyb


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    kfc__fdwf = []
    qtf__rpgua = []
    for xdsmn__fcyv in range(typ.nlevels):
        qbfl__oly = c.pyapi.unserialize(c.pyapi.serialize_object(xdsmn__fcyv))
        omyjs__fvkss = c.pyapi.call_method(val, 'get_level_values', (
            qbfl__oly,))
        ibl__wptw = c.pyapi.object_getattr_string(omyjs__fvkss, 'values')
        c.pyapi.decref(omyjs__fvkss)
        c.pyapi.decref(qbfl__oly)
        zudze__zrax = c.pyapi.to_native_value(typ.array_types[xdsmn__fcyv],
            ibl__wptw).value
        kfc__fdwf.append(zudze__zrax)
        qtf__rpgua.append(ibl__wptw)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, kfc__fdwf)
    else:
        data = cgutils.pack_struct(c.builder, kfc__fdwf)
    apmxk__gxo = c.pyapi.object_getattr_string(val, 'names')
    bvegu__gxxe = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    hnp__ewwrs = c.pyapi.call_function_objargs(bvegu__gxxe, (apmxk__gxo,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), hnp__ewwrs
        ).value
    jhd__lxsuw = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jhd__lxsuw).value
    gnp__ygyqk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gnp__ygyqk.data = data
    gnp__ygyqk.names = names
    gnp__ygyqk.name = name
    for ibl__wptw in qtf__rpgua:
        c.pyapi.decref(ibl__wptw)
    c.pyapi.decref(apmxk__gxo)
    c.pyapi.decref(bvegu__gxxe)
    c.pyapi.decref(hnp__ewwrs)
    c.pyapi.decref(jhd__lxsuw)
    return NativeValue(gnp__ygyqk._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    gyv__eymd = 'pandas.MultiIndex.from_product'
    yqky__brv = dict(sortorder=sortorder)
    qsq__dlqk = dict(sortorder=None)
    check_unsupported_args(gyv__eymd, yqky__brv, qsq__dlqk, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{gyv__eymd}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{gyv__eymd}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{gyv__eymd}: iterables and names must be of the same length.')


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
    usidk__kop = MultiIndexType(array_types, names_typ)
    dwwy__niyz = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, dwwy__niyz, usidk__kop)
    sflu__fdo = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{dwwy__niyz}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    btal__uags = {}
    exec(sflu__fdo, globals(), btal__uags)
    yxagy__cjm = btal__uags['impl']
    return yxagy__cjm


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        swi__fdlp, wyej__tyny, bfz__hoawu = args
        quuiu__olcp = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        quuiu__olcp.data = swi__fdlp
        quuiu__olcp.names = wyej__tyny
        quuiu__olcp.name = bfz__hoawu
        context.nrt.incref(builder, signature.args[0], swi__fdlp)
        context.nrt.incref(builder, signature.args[1], wyej__tyny)
        context.nrt.incref(builder, signature.args[2], bfz__hoawu)
        return quuiu__olcp._getvalue()
    zxxt__wvdv = MultiIndexType(data.types, names.types, name)
    return zxxt__wvdv(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        bclm__ypsfk = len(I.array_types)
        sflu__fdo = 'def impl(I, ind):\n'
        sflu__fdo += '  data = I._data\n'
        sflu__fdo += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{xdsmn__fcyv}][ind])' for
            xdsmn__fcyv in range(bclm__ypsfk))))
        btal__uags = {}
        exec(sflu__fdo, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, btal__uags)
        yxagy__cjm = btal__uags['impl']
        return yxagy__cjm


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    qnco__cld, xsct__qcq = sig.args
    if qnco__cld != xsct__qcq:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
