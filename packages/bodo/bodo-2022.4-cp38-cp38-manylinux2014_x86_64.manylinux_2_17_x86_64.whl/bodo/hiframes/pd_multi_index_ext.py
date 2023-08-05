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
        dkqu__akfli = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, dkqu__akfli)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[sco__pcov].values) for
        sco__pcov in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (qxkv__lsohg) for qxkv__lsohg in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    kcqx__ehc = c.context.insert_const_string(c.builder.module, 'pandas')
    outts__fsk = c.pyapi.import_module_noblock(kcqx__ehc)
    zho__oqcx = c.pyapi.object_getattr_string(outts__fsk, 'MultiIndex')
    oak__tevg = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types), oak__tevg
        .data)
    vxtt__hmza = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        oak__tevg.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), oak__tevg.names
        )
    kjou__mggc = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        oak__tevg.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, oak__tevg.name)
    jfi__dgg = c.pyapi.from_native_value(typ.name_typ, oak__tevg.name, c.
        env_manager)
    ynnr__zki = c.pyapi.borrow_none()
    vua__ttit = c.pyapi.call_method(zho__oqcx, 'from_arrays', (vxtt__hmza,
        ynnr__zki, kjou__mggc))
    c.pyapi.object_setattr_string(vua__ttit, 'name', jfi__dgg)
    c.pyapi.decref(vxtt__hmza)
    c.pyapi.decref(kjou__mggc)
    c.pyapi.decref(jfi__dgg)
    c.pyapi.decref(outts__fsk)
    c.pyapi.decref(zho__oqcx)
    c.context.nrt.decref(c.builder, typ, val)
    return vua__ttit


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    boyrf__xcyzu = []
    gms__ptt = []
    for sco__pcov in range(typ.nlevels):
        zlkvp__mubp = c.pyapi.unserialize(c.pyapi.serialize_object(sco__pcov))
        mcrm__rzgl = c.pyapi.call_method(val, 'get_level_values', (
            zlkvp__mubp,))
        zqwdg__zytgv = c.pyapi.object_getattr_string(mcrm__rzgl, 'values')
        c.pyapi.decref(mcrm__rzgl)
        c.pyapi.decref(zlkvp__mubp)
        bhqvl__lgy = c.pyapi.to_native_value(typ.array_types[sco__pcov],
            zqwdg__zytgv).value
        boyrf__xcyzu.append(bhqvl__lgy)
        gms__ptt.append(zqwdg__zytgv)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, boyrf__xcyzu)
    else:
        data = cgutils.pack_struct(c.builder, boyrf__xcyzu)
    kjou__mggc = c.pyapi.object_getattr_string(val, 'names')
    tlnb__ahh = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    ajs__icwdf = c.pyapi.call_function_objargs(tlnb__ahh, (kjou__mggc,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), ajs__icwdf
        ).value
    jfi__dgg = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, jfi__dgg).value
    oak__tevg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oak__tevg.data = data
    oak__tevg.names = names
    oak__tevg.name = name
    for zqwdg__zytgv in gms__ptt:
        c.pyapi.decref(zqwdg__zytgv)
    c.pyapi.decref(kjou__mggc)
    c.pyapi.decref(tlnb__ahh)
    c.pyapi.decref(ajs__icwdf)
    c.pyapi.decref(jfi__dgg)
    return NativeValue(oak__tevg._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    onwnk__zwve = 'pandas.MultiIndex.from_product'
    rfjht__czgt = dict(sortorder=sortorder)
    usrcz__iahx = dict(sortorder=None)
    check_unsupported_args(onwnk__zwve, rfjht__czgt, usrcz__iahx,
        package_name='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{onwnk__zwve}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{onwnk__zwve}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{onwnk__zwve}: iterables and names must be of the same length.')


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
    ulp__tfhdi = MultiIndexType(array_types, names_typ)
    mdwmm__gvn = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, mdwmm__gvn, ulp__tfhdi)
    uuc__ojoy = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{mdwmm__gvn}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    fhqex__pby = {}
    exec(uuc__ojoy, globals(), fhqex__pby)
    wkqe__thuup = fhqex__pby['impl']
    return wkqe__thuup


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        idw__ystoj, bdpko__gzb, ymqzy__mhzl = args
        fnw__ipq = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        fnw__ipq.data = idw__ystoj
        fnw__ipq.names = bdpko__gzb
        fnw__ipq.name = ymqzy__mhzl
        context.nrt.incref(builder, signature.args[0], idw__ystoj)
        context.nrt.incref(builder, signature.args[1], bdpko__gzb)
        context.nrt.incref(builder, signature.args[2], ymqzy__mhzl)
        return fnw__ipq._getvalue()
    timjq__gzjhp = MultiIndexType(data.types, names.types, name)
    return timjq__gzjhp(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        qbfiq__aszwm = len(I.array_types)
        uuc__ojoy = 'def impl(I, ind):\n'
        uuc__ojoy += '  data = I._data\n'
        uuc__ojoy += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{sco__pcov}][ind])' for sco__pcov in
            range(qbfiq__aszwm))))
        fhqex__pby = {}
        exec(uuc__ojoy, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, fhqex__pby)
        wkqe__thuup = fhqex__pby['impl']
        return wkqe__thuup


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    vchza__uxlav, qcil__upk = sig.args
    if vchza__uxlav != qcil__upk:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
