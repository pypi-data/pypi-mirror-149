"""Table data type for storing dataframe column arrays. Supports storing many columns
(e.g. >10k) efficiently.
"""
import operator
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.parfors.array_analysis import ArrayAnalysis
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.typing import BodoError, decode_if_dict_array, get_overload_const_int, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_true, to_str_arr_if_dict_array


class Table:

    def __init__(self, arrs, usecols=None, num_arrs=-1):
        if usecols is not None:
            assert num_arrs != -1, 'num_arrs must be provided if usecols is not None'
            ccy__hhu = 0
            ilrs__mqjz = []
            for i in range(usecols[-1] + 1):
                if i == usecols[ccy__hhu]:
                    ilrs__mqjz.append(arrs[ccy__hhu])
                    ccy__hhu += 1
                else:
                    ilrs__mqjz.append(None)
            for tzq__mnf in range(usecols[-1] + 1, num_arrs):
                ilrs__mqjz.append(None)
            self.arrays = ilrs__mqjz
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((xxwh__qwvnh == lhdp__bacb).all() for 
            xxwh__qwvnh, lhdp__bacb in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        olxd__urkh = len(self.arrays)
        xrs__cwrv = dict(zip(range(olxd__urkh), self.arrays))
        df = pd.DataFrame(xrs__cwrv, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        yshm__cat = []
        alex__cdv = []
        whbx__mvl = {}
        kyy__wqdn = defaultdict(int)
        wrqq__wdw = defaultdict(list)
        if not has_runtime_cols:
            for i, ysvc__tjqt in enumerate(arr_types):
                if ysvc__tjqt not in whbx__mvl:
                    whbx__mvl[ysvc__tjqt] = len(whbx__mvl)
                kbjw__sctsq = whbx__mvl[ysvc__tjqt]
                yshm__cat.append(kbjw__sctsq)
                alex__cdv.append(kyy__wqdn[kbjw__sctsq])
                kyy__wqdn[kbjw__sctsq] += 1
                wrqq__wdw[kbjw__sctsq].append(i)
        self.block_nums = yshm__cat
        self.block_offsets = alex__cdv
        self.type_to_blk = whbx__mvl
        self.block_to_arr_ind = wrqq__wdw
        super(TableType, self).__init__(name=
            f'TableType({arr_types}, {has_runtime_cols})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return self.arr_types, self.has_runtime_cols

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(Table)
def typeof_table(val, c):
    return TableType(tuple(numba.typeof(zbbb__erqwl) for zbbb__erqwl in val
        .arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            bdek__hjj = [(f'block_{i}', types.List(ysvc__tjqt)) for i,
                ysvc__tjqt in enumerate(fe_type.arr_types)]
        else:
            bdek__hjj = [(f'block_{kbjw__sctsq}', types.List(ysvc__tjqt)) for
                ysvc__tjqt, kbjw__sctsq in fe_type.type_to_blk.items()]
        bdek__hjj.append(('parent', types.pyobject))
        bdek__hjj.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, bdek__hjj)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    ktjbm__rgeln = c.pyapi.object_getattr_string(val, 'arrays')
    rsqig__geij = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    rsqig__geij.parent = cgutils.get_null_value(rsqig__geij.parent.type)
    umc__eqa = c.pyapi.make_none()
    odub__htzys = c.context.get_constant(types.int64, 0)
    lvh__sogp = cgutils.alloca_once_value(c.builder, odub__htzys)
    for ysvc__tjqt, kbjw__sctsq in typ.type_to_blk.items():
        kgkuf__xwt = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[kbjw__sctsq]))
        tzq__mnf, ehd__hmtj = ListInstance.allocate_ex(c.context, c.builder,
            types.List(ysvc__tjqt), kgkuf__xwt)
        ehd__hmtj.size = kgkuf__xwt
        tuhlc__vwt = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[kbjw__sctsq
            ], dtype=np.int64))
        jot__upj = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, tuhlc__vwt)
        with cgutils.for_range(c.builder, kgkuf__xwt) as msko__wyxeu:
            i = msko__wyxeu.index
            okzk__oqnj = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), jot__upj, i)
            msn__xbdet = c.pyapi.long_from_longlong(okzk__oqnj)
            dnvl__fwj = c.pyapi.object_getitem(ktjbm__rgeln, msn__xbdet)
            ixu__gpan = c.builder.icmp_unsigned('==', dnvl__fwj, umc__eqa)
            with c.builder.if_else(ixu__gpan) as (pqt__dcedk, oad__ogc):
                with pqt__dcedk:
                    uomci__hzbn = c.context.get_constant_null(ysvc__tjqt)
                    ehd__hmtj.inititem(i, uomci__hzbn, incref=False)
                with oad__ogc:
                    jmea__ffof = c.pyapi.call_method(dnvl__fwj, '__len__', ())
                    itw__eoa = c.pyapi.long_as_longlong(jmea__ffof)
                    c.builder.store(itw__eoa, lvh__sogp)
                    c.pyapi.decref(jmea__ffof)
                    zbbb__erqwl = c.pyapi.to_native_value(ysvc__tjqt, dnvl__fwj
                        ).value
                    ehd__hmtj.inititem(i, zbbb__erqwl, incref=False)
            c.pyapi.decref(dnvl__fwj)
            c.pyapi.decref(msn__xbdet)
        setattr(rsqig__geij, f'block_{kbjw__sctsq}', ehd__hmtj.value)
    rsqig__geij.len = c.builder.load(lvh__sogp)
    c.pyapi.decref(ktjbm__rgeln)
    c.pyapi.decref(umc__eqa)
    pfmdx__mxl = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rsqig__geij._getvalue(), is_error=pfmdx__mxl)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    rsqig__geij = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        eygtf__rxoab = c.context.get_constant(types.int64, 0)
        for i, ysvc__tjqt in enumerate(typ.arr_types):
            ilrs__mqjz = getattr(rsqig__geij, f'block_{i}')
            hek__vkz = ListInstance(c.context, c.builder, types.List(
                ysvc__tjqt), ilrs__mqjz)
            eygtf__rxoab = c.builder.add(eygtf__rxoab, hek__vkz.size)
        vrn__hmpc = c.pyapi.list_new(eygtf__rxoab)
        izd__pts = c.context.get_constant(types.int64, 0)
        for i, ysvc__tjqt in enumerate(typ.arr_types):
            ilrs__mqjz = getattr(rsqig__geij, f'block_{i}')
            hek__vkz = ListInstance(c.context, c.builder, types.List(
                ysvc__tjqt), ilrs__mqjz)
            with cgutils.for_range(c.builder, hek__vkz.size) as msko__wyxeu:
                i = msko__wyxeu.index
                zbbb__erqwl = hek__vkz.getitem(i)
                c.context.nrt.incref(c.builder, ysvc__tjqt, zbbb__erqwl)
                idx = c.builder.add(izd__pts, i)
                c.pyapi.list_setitem(vrn__hmpc, idx, c.pyapi.
                    from_native_value(ysvc__tjqt, zbbb__erqwl, c.env_manager))
            izd__pts = c.builder.add(izd__pts, hek__vkz.size)
        dpt__iaqj = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        dxufi__fmo = c.pyapi.call_function_objargs(dpt__iaqj, (vrn__hmpc,))
        c.pyapi.decref(dpt__iaqj)
        c.pyapi.decref(vrn__hmpc)
        c.context.nrt.decref(c.builder, typ, val)
        return dxufi__fmo
    vrn__hmpc = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    wix__ghn = cgutils.is_not_null(c.builder, rsqig__geij.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for ysvc__tjqt, kbjw__sctsq in typ.type_to_blk.items():
        ilrs__mqjz = getattr(rsqig__geij, f'block_{kbjw__sctsq}')
        hek__vkz = ListInstance(c.context, c.builder, types.List(ysvc__tjqt
            ), ilrs__mqjz)
        tuhlc__vwt = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[kbjw__sctsq
            ], dtype=np.int64))
        jot__upj = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, tuhlc__vwt)
        with cgutils.for_range(c.builder, hek__vkz.size) as msko__wyxeu:
            i = msko__wyxeu.index
            okzk__oqnj = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), jot__upj, i)
            zbbb__erqwl = hek__vkz.getitem(i)
            icnks__pslm = cgutils.alloca_once_value(c.builder, zbbb__erqwl)
            mvlqd__zxtbb = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(ysvc__tjqt))
            enoli__jpfn = is_ll_eq(c.builder, icnks__pslm, mvlqd__zxtbb)
            with c.builder.if_else(c.builder.and_(enoli__jpfn, c.builder.
                not_(ensure_unboxed))) as (pqt__dcedk, oad__ogc):
                with pqt__dcedk:
                    umc__eqa = c.pyapi.make_none()
                    c.pyapi.list_setitem(vrn__hmpc, okzk__oqnj, umc__eqa)
                with oad__ogc:
                    dnvl__fwj = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(enoli__jpfn,
                        wix__ghn)) as (lua__mjq, rtbqs__ood):
                        with lua__mjq:
                            lnaw__wlf = get_df_obj_column_codegen(c.context,
                                c.builder, c.pyapi, rsqig__geij.parent,
                                okzk__oqnj, ysvc__tjqt)
                            c.builder.store(lnaw__wlf, dnvl__fwj)
                        with rtbqs__ood:
                            c.context.nrt.incref(c.builder, ysvc__tjqt,
                                zbbb__erqwl)
                            c.builder.store(c.pyapi.from_native_value(
                                ysvc__tjqt, zbbb__erqwl, c.env_manager),
                                dnvl__fwj)
                    c.pyapi.list_setitem(vrn__hmpc, okzk__oqnj, c.builder.
                        load(dnvl__fwj))
    dpt__iaqj = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    dxufi__fmo = c.pyapi.call_function_objargs(dpt__iaqj, (vrn__hmpc,))
    c.pyapi.decref(dpt__iaqj)
    c.pyapi.decref(vrn__hmpc)
    c.context.nrt.decref(c.builder, typ, val)
    return dxufi__fmo


@lower_builtin(len, TableType)
def table_len_lower(context, builder, sig, args):
    impl = table_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def table_len_overload(T):
    if not isinstance(T, TableType):
        return

    def impl(T):
        return T._len
    return impl


@lower_getattr(TableType, 'shape')
def lower_table_shape(context, builder, typ, val):
    impl = table_shape_overload(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def table_shape_overload(T):
    if T.has_runtime_cols:

        def impl(T):
            return T._len, compute_num_runtime_columns(T)
        return impl
    ncols = len(T.arr_types)
    return lambda T: (T._len, types.int64(ncols))


@intrinsic
def compute_num_runtime_columns(typingctx, table_type):
    assert isinstance(table_type, TableType)

    def codegen(context, builder, sig, args):
        table_arg, = args
        rsqig__geij = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        tjyq__pqp = context.get_constant(types.int64, 0)
        for i, ysvc__tjqt in enumerate(table_type.arr_types):
            ilrs__mqjz = getattr(rsqig__geij, f'block_{i}')
            hek__vkz = ListInstance(context, builder, types.List(ysvc__tjqt
                ), ilrs__mqjz)
            tjyq__pqp = builder.add(tjyq__pqp, hek__vkz.size)
        return tjyq__pqp
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    rsqig__geij = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    kbjw__sctsq = table_type.block_nums[col_ind]
    dyye__cwxas = table_type.block_offsets[col_ind]
    ilrs__mqjz = getattr(rsqig__geij, f'block_{kbjw__sctsq}')
    hek__vkz = ListInstance(context, builder, types.List(arr_type), ilrs__mqjz)
    zbbb__erqwl = hek__vkz.getitem(dyye__cwxas)
    return zbbb__erqwl


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, tzq__mnf = args
        zbbb__erqwl = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, zbbb__erqwl)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, tzq__mnf = args
        rsqig__geij = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        kbjw__sctsq = table_type.block_nums[col_ind]
        dyye__cwxas = table_type.block_offsets[col_ind]
        ilrs__mqjz = getattr(rsqig__geij, f'block_{kbjw__sctsq}')
        hek__vkz = ListInstance(context, builder, types.List(arr_type),
            ilrs__mqjz)
        zbbb__erqwl = hek__vkz.getitem(dyye__cwxas)
        context.nrt.decref(builder, arr_type, zbbb__erqwl)
        uomci__hzbn = context.get_constant_null(arr_type)
        hek__vkz.inititem(dyye__cwxas, uomci__hzbn, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    odub__htzys = context.get_constant(types.int64, 0)
    zjx__yal = context.get_constant(types.int64, 1)
    oax__gtp = arr_type not in in_table_type.type_to_blk
    for ysvc__tjqt, kbjw__sctsq in out_table_type.type_to_blk.items():
        if ysvc__tjqt in in_table_type.type_to_blk:
            ezsas__tsa = in_table_type.type_to_blk[ysvc__tjqt]
            ehd__hmtj = ListInstance(context, builder, types.List(
                ysvc__tjqt), getattr(in_table, f'block_{ezsas__tsa}'))
            context.nrt.incref(builder, types.List(ysvc__tjqt), ehd__hmtj.value
                )
            setattr(out_table, f'block_{kbjw__sctsq}', ehd__hmtj.value)
    if oax__gtp:
        tzq__mnf, ehd__hmtj = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), zjx__yal)
        ehd__hmtj.size = zjx__yal
        ehd__hmtj.inititem(odub__htzys, arr_arg, incref=True)
        kbjw__sctsq = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{kbjw__sctsq}', ehd__hmtj.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        kbjw__sctsq = out_table_type.type_to_blk[arr_type]
        ehd__hmtj = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{kbjw__sctsq}'))
        if is_new_col:
            n = ehd__hmtj.size
            mpb__dzpp = builder.add(n, zjx__yal)
            ehd__hmtj.resize(mpb__dzpp)
            ehd__hmtj.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            xlky__mpw = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            ehd__hmtj.setitem(xlky__mpw, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            xlky__mpw = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = ehd__hmtj.size
            mpb__dzpp = builder.add(n, zjx__yal)
            ehd__hmtj.resize(mpb__dzpp)
            context.nrt.incref(builder, arr_type, ehd__hmtj.getitem(xlky__mpw))
            ehd__hmtj.move(builder.add(xlky__mpw, zjx__yal), xlky__mpw,
                builder.sub(n, xlky__mpw))
            ehd__hmtj.setitem(xlky__mpw, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    wek__lthqh = in_table_type.arr_types[col_ind]
    if wek__lthqh in out_table_type.type_to_blk:
        kbjw__sctsq = out_table_type.type_to_blk[wek__lthqh]
        ilhw__lqd = getattr(out_table, f'block_{kbjw__sctsq}')
        dfi__bik = types.List(wek__lthqh)
        xlky__mpw = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        wdebf__jgfx = dfi__bik.dtype(dfi__bik, types.intp)
        huqal__mqfa = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), wdebf__jgfx, (ilhw__lqd, xlky__mpw))
        context.nrt.decref(builder, wek__lthqh, huqal__mqfa)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    wzl__hly = list(table_type.arr_types)
    if is_new_col:
        wzl__hly.append(arr_type)
    else:
        wzl__hly[col_ind] = arr_type
    out_table_type = TableType(tuple(wzl__hly))

    def codegen(context, builder, sig, args):
        table_arg, tzq__mnf, imsh__xenu = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, imsh__xenu, col_ind,
            is_new_col)
        return out_table
    return out_table_type(table_type, ind_type, arr_type), codegen


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    fpl__poa = args[0]
    if equiv_set.has_shape(fpl__poa):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            fpl__poa)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    wti__cdzrn = []
    for ysvc__tjqt, kbjw__sctsq in table_type.type_to_blk.items():
        zxr__vrow = len(table_type.block_to_arr_ind[kbjw__sctsq])
        tzi__qmr = []
        for i in range(zxr__vrow):
            okzk__oqnj = table_type.block_to_arr_ind[kbjw__sctsq][i]
            tzi__qmr.append(pyval.arrays[okzk__oqnj])
        wti__cdzrn.append(context.get_constant_generic(builder, types.List(
            ysvc__tjqt), tzi__qmr))
    fhd__yze = context.get_constant_null(types.pyobject)
    sdr__ifwl = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(wti__cdzrn + [fhd__yze, sdr__ifwl])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        rsqig__geij = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for ysvc__tjqt, kbjw__sctsq in out_table_type.type_to_blk.items():
            fpvx__ekug = context.get_constant_null(types.List(ysvc__tjqt))
            setattr(rsqig__geij, f'block_{kbjw__sctsq}', fpvx__ekug)
        return rsqig__geij._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    tnb__qtekf = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        tnb__qtekf[typ.dtype] = i
    vmdy__svr = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(vmdy__svr, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        tpydz__kuadq, tzq__mnf = args
        rsqig__geij = cgutils.create_struct_proxy(vmdy__svr)(context, builder)
        for ysvc__tjqt, kbjw__sctsq in vmdy__svr.type_to_blk.items():
            idx = tnb__qtekf[ysvc__tjqt]
            fvb__gpx = signature(types.List(ysvc__tjqt),
                tuple_of_lists_type, types.literal(idx))
            ovex__qebv = tpydz__kuadq, idx
            geg__qeeo = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, fvb__gpx, ovex__qebv)
            setattr(rsqig__geij, f'block_{kbjw__sctsq}', geg__qeeo)
        return rsqig__geij._getvalue()
    sig = vmdy__svr(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    kbjw__sctsq = get_overload_const_int(blk_type)
    arr_type = None
    for ysvc__tjqt, lhdp__bacb in table_type.type_to_blk.items():
        if lhdp__bacb == kbjw__sctsq:
            arr_type = ysvc__tjqt
            break
    assert arr_type is not None, 'invalid table type block'
    baq__prsa = types.List(arr_type)

    def codegen(context, builder, sig, args):
        rsqig__geij = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        ilrs__mqjz = getattr(rsqig__geij, f'block_{kbjw__sctsq}')
        return impl_ret_borrowed(context, builder, baq__prsa, ilrs__mqjz)
    sig = baq__prsa(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, rxz__cml = args
        hcg__xsf = context.get_python_api(builder)
        dam__ukfg = used_cols_typ == types.none
        if not dam__ukfg:
            klxq__afyr = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), rxz__cml)
        rsqig__geij = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        wix__ghn = cgutils.is_not_null(builder, rsqig__geij.parent)
        for ysvc__tjqt, kbjw__sctsq in table_type.type_to_blk.items():
            kgkuf__xwt = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[kbjw__sctsq]))
            tuhlc__vwt = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                kbjw__sctsq], dtype=np.int64))
            jot__upj = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, tuhlc__vwt)
            ilrs__mqjz = getattr(rsqig__geij, f'block_{kbjw__sctsq}')
            with cgutils.for_range(builder, kgkuf__xwt) as msko__wyxeu:
                i = msko__wyxeu.index
                okzk__oqnj = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'), jot__upj, i)
                kfe__shxma = types.none(table_type, types.List(ysvc__tjqt),
                    types.int64, types.int64)
                tkwxx__jhoiw = table_arg, ilrs__mqjz, i, okzk__oqnj
                if dam__ukfg:
                    ensure_column_unboxed_codegen(context, builder,
                        kfe__shxma, tkwxx__jhoiw)
                else:
                    nvx__dcp = klxq__afyr.contains(okzk__oqnj)
                    with builder.if_then(nvx__dcp):
                        ensure_column_unboxed_codegen(context, builder,
                            kfe__shxma, tkwxx__jhoiw)
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, used_cols_typ)
    return sig, codegen


@intrinsic
def ensure_column_unboxed(typingctx, table_type, arr_list_t, ind_t, arr_ind_t):
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, arr_list_t, ind_t, arr_ind_t)
    return sig, ensure_column_unboxed_codegen


def ensure_column_unboxed_codegen(context, builder, sig, args):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table_arg, igwcu__iiuoe, vif__fved, okz__yfid = args
    hcg__xsf = context.get_python_api(builder)
    rsqig__geij = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    wix__ghn = cgutils.is_not_null(builder, rsqig__geij.parent)
    hek__vkz = ListInstance(context, builder, sig.args[1], igwcu__iiuoe)
    ppj__domc = hek__vkz.getitem(vif__fved)
    icnks__pslm = cgutils.alloca_once_value(builder, ppj__domc)
    mvlqd__zxtbb = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    enoli__jpfn = is_ll_eq(builder, icnks__pslm, mvlqd__zxtbb)
    with builder.if_then(enoli__jpfn):
        with builder.if_else(wix__ghn) as (pqt__dcedk, oad__ogc):
            with pqt__dcedk:
                dnvl__fwj = get_df_obj_column_codegen(context, builder,
                    hcg__xsf, rsqig__geij.parent, okz__yfid, sig.args[1].dtype)
                zbbb__erqwl = hcg__xsf.to_native_value(sig.args[1].dtype,
                    dnvl__fwj).value
                hek__vkz.inititem(vif__fved, zbbb__erqwl, incref=False)
                hcg__xsf.decref(dnvl__fwj)
            with oad__ogc:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    kbjw__sctsq = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, lczpz__xvxl, tzq__mnf = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{kbjw__sctsq}', lczpz__xvxl)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, iqbh__mnp = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = iqbh__mnp
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    baq__prsa = list_type
    if is_overload_true(to_str_if_dict_t):
        baq__prsa = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        ynbx__ywkwu = ListInstance(context, builder, list_type, args[0])
        ocmed__ryr = ynbx__ywkwu.size
        tzq__mnf, ehd__hmtj = ListInstance.allocate_ex(context, builder,
            baq__prsa, ocmed__ryr)
        ehd__hmtj.size = ocmed__ryr
        return ehd__hmtj.value
    sig = baq__prsa(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    onfae__nbv = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(onfae__nbv)

    def codegen(context, builder, sig, args):
        ocmed__ryr, tzq__mnf = args
        tzq__mnf, ehd__hmtj = ListInstance.allocate_ex(context, builder,
            list_type, ocmed__ryr)
        ehd__hmtj.size = ocmed__ryr
        return ehd__hmtj.value
    sig = list_type(size_typ, data_typ)
    return sig, codegen


def _get_idx_length(idx):
    pass


@overload(_get_idx_length)
def overload_get_idx_length(idx, n):
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        return lambda idx, n: idx.sum()
    assert isinstance(idx, types.SliceType), 'slice index expected'

    def impl(idx, n):
        lhlvh__bmuw = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(lhlvh__bmuw)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    yer__qzm = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        yer__qzm['used_cols'] = used_cols
    qdy__tmkc = 'def impl(T, idx):\n'
    qdy__tmkc += f'  T2 = init_table(T, False)\n'
    qdy__tmkc += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        qdy__tmkc += f'  l = _get_idx_length(idx, len(T))\n'
        qdy__tmkc += f'  T2 = set_table_len(T2, l)\n'
        qdy__tmkc += f'  return T2\n'
        epg__griyq = {}
        exec(qdy__tmkc, yer__qzm, epg__griyq)
        return epg__griyq['impl']
    if used_cols is not None:
        qdy__tmkc += f'  used_set = set(used_cols)\n'
    for kbjw__sctsq in T.type_to_blk.values():
        yer__qzm[f'arr_inds_{kbjw__sctsq}'] = np.array(T.block_to_arr_ind[
            kbjw__sctsq], dtype=np.int64)
        qdy__tmkc += (
            f'  arr_list_{kbjw__sctsq} = get_table_block(T, {kbjw__sctsq})\n')
        qdy__tmkc += f"""  out_arr_list_{kbjw__sctsq} = alloc_list_like(arr_list_{kbjw__sctsq}, False)
"""
        qdy__tmkc += f'  for i in range(len(arr_list_{kbjw__sctsq})):\n'
        qdy__tmkc += f'    arr_ind_{kbjw__sctsq} = arr_inds_{kbjw__sctsq}[i]\n'
        if used_cols is not None:
            qdy__tmkc += (
                f'    if arr_ind_{kbjw__sctsq} not in used_set: continue\n')
        qdy__tmkc += f"""    ensure_column_unboxed(T, arr_list_{kbjw__sctsq}, i, arr_ind_{kbjw__sctsq})
"""
        qdy__tmkc += f"""    out_arr_{kbjw__sctsq} = ensure_contig_if_np(arr_list_{kbjw__sctsq}[i][idx])
"""
        qdy__tmkc += f'    l = len(out_arr_{kbjw__sctsq})\n'
        qdy__tmkc += (
            f'    out_arr_list_{kbjw__sctsq}[i] = out_arr_{kbjw__sctsq}\n')
        qdy__tmkc += (
            f'  T2 = set_table_block(T2, out_arr_list_{kbjw__sctsq}, {kbjw__sctsq})\n'
            )
    qdy__tmkc += f'  T2 = set_table_len(T2, l)\n'
    qdy__tmkc += f'  return T2\n'
    epg__griyq = {}
    exec(qdy__tmkc, yer__qzm, epg__griyq)
    return epg__griyq['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    qdy__tmkc = 'def impl(T):\n'
    qdy__tmkc += f'  T2 = init_table(T, True)\n'
    qdy__tmkc += f'  l = len(T)\n'
    yer__qzm = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for kbjw__sctsq in T.type_to_blk.values():
        yer__qzm[f'arr_inds_{kbjw__sctsq}'] = np.array(T.block_to_arr_ind[
            kbjw__sctsq], dtype=np.int64)
        qdy__tmkc += (
            f'  arr_list_{kbjw__sctsq} = get_table_block(T, {kbjw__sctsq})\n')
        qdy__tmkc += f"""  out_arr_list_{kbjw__sctsq} = alloc_list_like(arr_list_{kbjw__sctsq}, True)
"""
        qdy__tmkc += f'  for i in range(len(arr_list_{kbjw__sctsq})):\n'
        qdy__tmkc += f'    arr_ind_{kbjw__sctsq} = arr_inds_{kbjw__sctsq}[i]\n'
        qdy__tmkc += f"""    ensure_column_unboxed(T, arr_list_{kbjw__sctsq}, i, arr_ind_{kbjw__sctsq})
"""
        qdy__tmkc += f"""    out_arr_{kbjw__sctsq} = decode_if_dict_array(arr_list_{kbjw__sctsq}[i])
"""
        qdy__tmkc += (
            f'    out_arr_list_{kbjw__sctsq}[i] = out_arr_{kbjw__sctsq}\n')
        qdy__tmkc += (
            f'  T2 = set_table_block(T2, out_arr_list_{kbjw__sctsq}, {kbjw__sctsq})\n'
            )
    qdy__tmkc += f'  T2 = set_table_len(T2, l)\n'
    qdy__tmkc += f'  return T2\n'
    epg__griyq = {}
    exec(qdy__tmkc, yer__qzm, epg__griyq)
    return epg__griyq['impl']


@overload(operator.getitem, no_unliteral=True)
def table_getitem(T, idx):
    if not isinstance(T, TableType):
        return
    return gen_table_filter(T)


@intrinsic
def init_runtime_table_from_lists(typingctx, arr_list_tup_typ, nrows_typ=None):
    assert isinstance(arr_list_tup_typ, types.BaseTuple
        ), 'init_runtime_table_from_lists requires a tuple of list of arrays'
    if isinstance(arr_list_tup_typ, types.UniTuple):
        if arr_list_tup_typ.dtype.dtype == types.undefined:
            return
        eea__gav = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        eea__gav = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            eea__gav.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        qmp__armqt, dxubl__pfggf = args
        rsqig__geij = cgutils.create_struct_proxy(table_type)(context, builder)
        rsqig__geij.len = dxubl__pfggf
        wti__cdzrn = cgutils.unpack_tuple(builder, qmp__armqt)
        for i, ilrs__mqjz in enumerate(wti__cdzrn):
            setattr(rsqig__geij, f'block_{i}', ilrs__mqjz)
            context.nrt.incref(builder, types.List(eea__gav[i]), ilrs__mqjz)
        return rsqig__geij._getvalue()
    table_type = TableType(tuple(eea__gav), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
