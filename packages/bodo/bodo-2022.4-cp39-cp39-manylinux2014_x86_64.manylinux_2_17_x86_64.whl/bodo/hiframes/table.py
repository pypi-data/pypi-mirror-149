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
            hcisp__ssbwb = 0
            rnmxc__hesxj = []
            for i in range(usecols[-1] + 1):
                if i == usecols[hcisp__ssbwb]:
                    rnmxc__hesxj.append(arrs[hcisp__ssbwb])
                    hcisp__ssbwb += 1
                else:
                    rnmxc__hesxj.append(None)
            for nsvg__bnsrb in range(usecols[-1] + 1, num_arrs):
                rnmxc__hesxj.append(None)
            self.arrays = rnmxc__hesxj
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((qqzpq__nfrb == edc__zhqxx).all() for 
            qqzpq__nfrb, edc__zhqxx in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        ski__czgys = len(self.arrays)
        nbnm__fjc = dict(zip(range(ski__czgys), self.arrays))
        df = pd.DataFrame(nbnm__fjc, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        rzeig__xlh = []
        bizkx__liiaw = []
        zmugv__hlkp = {}
        ftu__veo = defaultdict(int)
        vlok__vfrjt = defaultdict(list)
        if not has_runtime_cols:
            for i, myyql__urc in enumerate(arr_types):
                if myyql__urc not in zmugv__hlkp:
                    zmugv__hlkp[myyql__urc] = len(zmugv__hlkp)
                jajt__nqgc = zmugv__hlkp[myyql__urc]
                rzeig__xlh.append(jajt__nqgc)
                bizkx__liiaw.append(ftu__veo[jajt__nqgc])
                ftu__veo[jajt__nqgc] += 1
                vlok__vfrjt[jajt__nqgc].append(i)
        self.block_nums = rzeig__xlh
        self.block_offsets = bizkx__liiaw
        self.type_to_blk = zmugv__hlkp
        self.block_to_arr_ind = vlok__vfrjt
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
    return TableType(tuple(numba.typeof(ywnvj__jiz) for ywnvj__jiz in val.
        arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            nzkft__zchrv = [(f'block_{i}', types.List(myyql__urc)) for i,
                myyql__urc in enumerate(fe_type.arr_types)]
        else:
            nzkft__zchrv = [(f'block_{jajt__nqgc}', types.List(myyql__urc)) for
                myyql__urc, jajt__nqgc in fe_type.type_to_blk.items()]
        nzkft__zchrv.append(('parent', types.pyobject))
        nzkft__zchrv.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, nzkft__zchrv)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    kasv__fhg = c.pyapi.object_getattr_string(val, 'arrays')
    aktoe__qldd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    aktoe__qldd.parent = cgutils.get_null_value(aktoe__qldd.parent.type)
    mha__bld = c.pyapi.make_none()
    qpt__nxzyi = c.context.get_constant(types.int64, 0)
    kdu__tfuqm = cgutils.alloca_once_value(c.builder, qpt__nxzyi)
    for myyql__urc, jajt__nqgc in typ.type_to_blk.items():
        hncw__eitr = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[jajt__nqgc]))
        nsvg__bnsrb, yhy__xlaz = ListInstance.allocate_ex(c.context, c.
            builder, types.List(myyql__urc), hncw__eitr)
        yhy__xlaz.size = hncw__eitr
        iupg__zho = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[jajt__nqgc],
            dtype=np.int64))
        dmqrh__jvefw = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, iupg__zho)
        with cgutils.for_range(c.builder, hncw__eitr) as qzrxw__tzd:
            i = qzrxw__tzd.index
            main__dsz = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), dmqrh__jvefw, i)
            wkbty__vzkzu = c.pyapi.long_from_longlong(main__dsz)
            veeah__bvvso = c.pyapi.object_getitem(kasv__fhg, wkbty__vzkzu)
            tbunh__fvg = c.builder.icmp_unsigned('==', veeah__bvvso, mha__bld)
            with c.builder.if_else(tbunh__fvg) as (cylne__fne, qgrfk__nzr):
                with cylne__fne:
                    rrua__qdb = c.context.get_constant_null(myyql__urc)
                    yhy__xlaz.inititem(i, rrua__qdb, incref=False)
                with qgrfk__nzr:
                    sab__gufrg = c.pyapi.call_method(veeah__bvvso,
                        '__len__', ())
                    cukh__cnte = c.pyapi.long_as_longlong(sab__gufrg)
                    c.builder.store(cukh__cnte, kdu__tfuqm)
                    c.pyapi.decref(sab__gufrg)
                    ywnvj__jiz = c.pyapi.to_native_value(myyql__urc,
                        veeah__bvvso).value
                    yhy__xlaz.inititem(i, ywnvj__jiz, incref=False)
            c.pyapi.decref(veeah__bvvso)
            c.pyapi.decref(wkbty__vzkzu)
        setattr(aktoe__qldd, f'block_{jajt__nqgc}', yhy__xlaz.value)
    aktoe__qldd.len = c.builder.load(kdu__tfuqm)
    c.pyapi.decref(kasv__fhg)
    c.pyapi.decref(mha__bld)
    ivvxy__iekz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(aktoe__qldd._getvalue(), is_error=ivvxy__iekz)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    aktoe__qldd = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        rko__txqlx = c.context.get_constant(types.int64, 0)
        for i, myyql__urc in enumerate(typ.arr_types):
            rnmxc__hesxj = getattr(aktoe__qldd, f'block_{i}')
            slbie__xel = ListInstance(c.context, c.builder, types.List(
                myyql__urc), rnmxc__hesxj)
            rko__txqlx = c.builder.add(rko__txqlx, slbie__xel.size)
        iovy__gmekq = c.pyapi.list_new(rko__txqlx)
        qedlq__wad = c.context.get_constant(types.int64, 0)
        for i, myyql__urc in enumerate(typ.arr_types):
            rnmxc__hesxj = getattr(aktoe__qldd, f'block_{i}')
            slbie__xel = ListInstance(c.context, c.builder, types.List(
                myyql__urc), rnmxc__hesxj)
            with cgutils.for_range(c.builder, slbie__xel.size) as qzrxw__tzd:
                i = qzrxw__tzd.index
                ywnvj__jiz = slbie__xel.getitem(i)
                c.context.nrt.incref(c.builder, myyql__urc, ywnvj__jiz)
                idx = c.builder.add(qedlq__wad, i)
                c.pyapi.list_setitem(iovy__gmekq, idx, c.pyapi.
                    from_native_value(myyql__urc, ywnvj__jiz, c.env_manager))
            qedlq__wad = c.builder.add(qedlq__wad, slbie__xel.size)
        vemmn__mthez = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        npbex__vjj = c.pyapi.call_function_objargs(vemmn__mthez, (iovy__gmekq,)
            )
        c.pyapi.decref(vemmn__mthez)
        c.pyapi.decref(iovy__gmekq)
        c.context.nrt.decref(c.builder, typ, val)
        return npbex__vjj
    iovy__gmekq = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    qxnod__otpjq = cgutils.is_not_null(c.builder, aktoe__qldd.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for myyql__urc, jajt__nqgc in typ.type_to_blk.items():
        rnmxc__hesxj = getattr(aktoe__qldd, f'block_{jajt__nqgc}')
        slbie__xel = ListInstance(c.context, c.builder, types.List(
            myyql__urc), rnmxc__hesxj)
        iupg__zho = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[jajt__nqgc],
            dtype=np.int64))
        dmqrh__jvefw = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, iupg__zho)
        with cgutils.for_range(c.builder, slbie__xel.size) as qzrxw__tzd:
            i = qzrxw__tzd.index
            main__dsz = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), dmqrh__jvefw, i)
            ywnvj__jiz = slbie__xel.getitem(i)
            vitxx__zka = cgutils.alloca_once_value(c.builder, ywnvj__jiz)
            mlw__asmf = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(myyql__urc))
            fua__flg = is_ll_eq(c.builder, vitxx__zka, mlw__asmf)
            with c.builder.if_else(c.builder.and_(fua__flg, c.builder.not_(
                ensure_unboxed))) as (cylne__fne, qgrfk__nzr):
                with cylne__fne:
                    mha__bld = c.pyapi.make_none()
                    c.pyapi.list_setitem(iovy__gmekq, main__dsz, mha__bld)
                with qgrfk__nzr:
                    veeah__bvvso = cgutils.alloca_once(c.builder, c.context
                        .get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(fua__flg,
                        qxnod__otpjq)) as (iyvq__sggg, njwlt__ozqui):
                        with iyvq__sggg:
                            sgda__znj = get_df_obj_column_codegen(c.context,
                                c.builder, c.pyapi, aktoe__qldd.parent,
                                main__dsz, myyql__urc)
                            c.builder.store(sgda__znj, veeah__bvvso)
                        with njwlt__ozqui:
                            c.context.nrt.incref(c.builder, myyql__urc,
                                ywnvj__jiz)
                            c.builder.store(c.pyapi.from_native_value(
                                myyql__urc, ywnvj__jiz, c.env_manager),
                                veeah__bvvso)
                    c.pyapi.list_setitem(iovy__gmekq, main__dsz, c.builder.
                        load(veeah__bvvso))
    vemmn__mthez = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    npbex__vjj = c.pyapi.call_function_objargs(vemmn__mthez, (iovy__gmekq,))
    c.pyapi.decref(vemmn__mthez)
    c.pyapi.decref(iovy__gmekq)
    c.context.nrt.decref(c.builder, typ, val)
    return npbex__vjj


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
        aktoe__qldd = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        esiu__nekz = context.get_constant(types.int64, 0)
        for i, myyql__urc in enumerate(table_type.arr_types):
            rnmxc__hesxj = getattr(aktoe__qldd, f'block_{i}')
            slbie__xel = ListInstance(context, builder, types.List(
                myyql__urc), rnmxc__hesxj)
            esiu__nekz = builder.add(esiu__nekz, slbie__xel.size)
        return esiu__nekz
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    aktoe__qldd = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    jajt__nqgc = table_type.block_nums[col_ind]
    vxpox__baee = table_type.block_offsets[col_ind]
    rnmxc__hesxj = getattr(aktoe__qldd, f'block_{jajt__nqgc}')
    slbie__xel = ListInstance(context, builder, types.List(arr_type),
        rnmxc__hesxj)
    ywnvj__jiz = slbie__xel.getitem(vxpox__baee)
    return ywnvj__jiz


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, nsvg__bnsrb = args
        ywnvj__jiz = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, ywnvj__jiz)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, nsvg__bnsrb = args
        aktoe__qldd = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        jajt__nqgc = table_type.block_nums[col_ind]
        vxpox__baee = table_type.block_offsets[col_ind]
        rnmxc__hesxj = getattr(aktoe__qldd, f'block_{jajt__nqgc}')
        slbie__xel = ListInstance(context, builder, types.List(arr_type),
            rnmxc__hesxj)
        ywnvj__jiz = slbie__xel.getitem(vxpox__baee)
        context.nrt.decref(builder, arr_type, ywnvj__jiz)
        rrua__qdb = context.get_constant_null(arr_type)
        slbie__xel.inititem(vxpox__baee, rrua__qdb, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    qpt__nxzyi = context.get_constant(types.int64, 0)
    taus__fvda = context.get_constant(types.int64, 1)
    hkwpf__tdqzt = arr_type not in in_table_type.type_to_blk
    for myyql__urc, jajt__nqgc in out_table_type.type_to_blk.items():
        if myyql__urc in in_table_type.type_to_blk:
            wvhy__kttr = in_table_type.type_to_blk[myyql__urc]
            yhy__xlaz = ListInstance(context, builder, types.List(
                myyql__urc), getattr(in_table, f'block_{wvhy__kttr}'))
            context.nrt.incref(builder, types.List(myyql__urc), yhy__xlaz.value
                )
            setattr(out_table, f'block_{jajt__nqgc}', yhy__xlaz.value)
    if hkwpf__tdqzt:
        nsvg__bnsrb, yhy__xlaz = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), taus__fvda)
        yhy__xlaz.size = taus__fvda
        yhy__xlaz.inititem(qpt__nxzyi, arr_arg, incref=True)
        jajt__nqgc = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{jajt__nqgc}', yhy__xlaz.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        jajt__nqgc = out_table_type.type_to_blk[arr_type]
        yhy__xlaz = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{jajt__nqgc}'))
        if is_new_col:
            n = yhy__xlaz.size
            iodx__gfrkl = builder.add(n, taus__fvda)
            yhy__xlaz.resize(iodx__gfrkl)
            yhy__xlaz.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            kbibt__qizbu = context.get_constant(types.int64, out_table_type
                .block_offsets[col_ind])
            yhy__xlaz.setitem(kbibt__qizbu, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            kbibt__qizbu = context.get_constant(types.int64, out_table_type
                .block_offsets[col_ind])
            n = yhy__xlaz.size
            iodx__gfrkl = builder.add(n, taus__fvda)
            yhy__xlaz.resize(iodx__gfrkl)
            context.nrt.incref(builder, arr_type, yhy__xlaz.getitem(
                kbibt__qizbu))
            yhy__xlaz.move(builder.add(kbibt__qizbu, taus__fvda),
                kbibt__qizbu, builder.sub(n, kbibt__qizbu))
            yhy__xlaz.setitem(kbibt__qizbu, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    xyemx__nkle = in_table_type.arr_types[col_ind]
    if xyemx__nkle in out_table_type.type_to_blk:
        jajt__nqgc = out_table_type.type_to_blk[xyemx__nkle]
        wnxg__mrlyw = getattr(out_table, f'block_{jajt__nqgc}')
        rbwdy__ewd = types.List(xyemx__nkle)
        kbibt__qizbu = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        xsza__iwx = rbwdy__ewd.dtype(rbwdy__ewd, types.intp)
        jxr__fjx = context.compile_internal(builder, lambda lst, i: lst.pop
            (i), xsza__iwx, (wnxg__mrlyw, kbibt__qizbu))
        context.nrt.decref(builder, xyemx__nkle, jxr__fjx)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    pxi__mqcrn = list(table_type.arr_types)
    if is_new_col:
        pxi__mqcrn.append(arr_type)
    else:
        pxi__mqcrn[col_ind] = arr_type
    out_table_type = TableType(tuple(pxi__mqcrn))

    def codegen(context, builder, sig, args):
        table_arg, nsvg__bnsrb, vwc__ptypa = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, vwc__ptypa, col_ind,
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
    axjsv__ray = args[0]
    if equiv_set.has_shape(axjsv__ray):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            axjsv__ray)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    jlsn__pfko = []
    for myyql__urc, jajt__nqgc in table_type.type_to_blk.items():
        oemi__vokwd = len(table_type.block_to_arr_ind[jajt__nqgc])
        zgfrm__squk = []
        for i in range(oemi__vokwd):
            main__dsz = table_type.block_to_arr_ind[jajt__nqgc][i]
            zgfrm__squk.append(pyval.arrays[main__dsz])
        jlsn__pfko.append(context.get_constant_generic(builder, types.List(
            myyql__urc), zgfrm__squk))
    wdvp__jvzbi = context.get_constant_null(types.pyobject)
    fmiwe__urhm = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(jlsn__pfko + [wdvp__jvzbi, fmiwe__urhm])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        aktoe__qldd = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for myyql__urc, jajt__nqgc in out_table_type.type_to_blk.items():
            vdcpp__bba = context.get_constant_null(types.List(myyql__urc))
            setattr(aktoe__qldd, f'block_{jajt__nqgc}', vdcpp__bba)
        return aktoe__qldd._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    yry__hob = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        yry__hob[typ.dtype] = i
    wra__gniyc = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(wra__gniyc, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        obay__flntm, nsvg__bnsrb = args
        aktoe__qldd = cgutils.create_struct_proxy(wra__gniyc)(context, builder)
        for myyql__urc, jajt__nqgc in wra__gniyc.type_to_blk.items():
            idx = yry__hob[myyql__urc]
            ugk__enzw = signature(types.List(myyql__urc),
                tuple_of_lists_type, types.literal(idx))
            elj__ynkv = obay__flntm, idx
            ejct__aqi = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, ugk__enzw, elj__ynkv)
            setattr(aktoe__qldd, f'block_{jajt__nqgc}', ejct__aqi)
        return aktoe__qldd._getvalue()
    sig = wra__gniyc(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    jajt__nqgc = get_overload_const_int(blk_type)
    arr_type = None
    for myyql__urc, edc__zhqxx in table_type.type_to_blk.items():
        if edc__zhqxx == jajt__nqgc:
            arr_type = myyql__urc
            break
    assert arr_type is not None, 'invalid table type block'
    jmjnt__fqhod = types.List(arr_type)

    def codegen(context, builder, sig, args):
        aktoe__qldd = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        rnmxc__hesxj = getattr(aktoe__qldd, f'block_{jajt__nqgc}')
        return impl_ret_borrowed(context, builder, jmjnt__fqhod, rnmxc__hesxj)
    sig = jmjnt__fqhod(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, gdcp__cnh = args
        uibnj__vllyn = context.get_python_api(builder)
        ael__cqg = used_cols_typ == types.none
        if not ael__cqg:
            wgwbl__gdb = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), gdcp__cnh)
        aktoe__qldd = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        qxnod__otpjq = cgutils.is_not_null(builder, aktoe__qldd.parent)
        for myyql__urc, jajt__nqgc in table_type.type_to_blk.items():
            hncw__eitr = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[jajt__nqgc]))
            iupg__zho = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                jajt__nqgc], dtype=np.int64))
            dmqrh__jvefw = context.make_array(types.Array(types.int64, 1, 'C')
                )(context, builder, iupg__zho)
            rnmxc__hesxj = getattr(aktoe__qldd, f'block_{jajt__nqgc}')
            with cgutils.for_range(builder, hncw__eitr) as qzrxw__tzd:
                i = qzrxw__tzd.index
                main__dsz = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    dmqrh__jvefw, i)
                bmd__cco = types.none(table_type, types.List(myyql__urc),
                    types.int64, types.int64)
                axd__kwkd = table_arg, rnmxc__hesxj, i, main__dsz
                if ael__cqg:
                    ensure_column_unboxed_codegen(context, builder,
                        bmd__cco, axd__kwkd)
                else:
                    fsdn__balis = wgwbl__gdb.contains(main__dsz)
                    with builder.if_then(fsdn__balis):
                        ensure_column_unboxed_codegen(context, builder,
                            bmd__cco, axd__kwkd)
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
    table_arg, dwtpq__jzaaf, mgang__uykp, zun__lin = args
    uibnj__vllyn = context.get_python_api(builder)
    aktoe__qldd = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    qxnod__otpjq = cgutils.is_not_null(builder, aktoe__qldd.parent)
    slbie__xel = ListInstance(context, builder, sig.args[1], dwtpq__jzaaf)
    mle__kgv = slbie__xel.getitem(mgang__uykp)
    vitxx__zka = cgutils.alloca_once_value(builder, mle__kgv)
    mlw__asmf = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    fua__flg = is_ll_eq(builder, vitxx__zka, mlw__asmf)
    with builder.if_then(fua__flg):
        with builder.if_else(qxnod__otpjq) as (cylne__fne, qgrfk__nzr):
            with cylne__fne:
                veeah__bvvso = get_df_obj_column_codegen(context, builder,
                    uibnj__vllyn, aktoe__qldd.parent, zun__lin, sig.args[1]
                    .dtype)
                ywnvj__jiz = uibnj__vllyn.to_native_value(sig.args[1].dtype,
                    veeah__bvvso).value
                slbie__xel.inititem(mgang__uykp, ywnvj__jiz, incref=False)
                uibnj__vllyn.decref(veeah__bvvso)
            with qgrfk__nzr:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    jajt__nqgc = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, clk__osgur, nsvg__bnsrb = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{jajt__nqgc}', clk__osgur)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, wof__aqjhn = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = wof__aqjhn
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    jmjnt__fqhod = list_type
    if is_overload_true(to_str_if_dict_t):
        jmjnt__fqhod = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        xgg__fxzn = ListInstance(context, builder, list_type, args[0])
        fgd__bir = xgg__fxzn.size
        nsvg__bnsrb, yhy__xlaz = ListInstance.allocate_ex(context, builder,
            jmjnt__fqhod, fgd__bir)
        yhy__xlaz.size = fgd__bir
        return yhy__xlaz.value
    sig = jmjnt__fqhod(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    xfdbb__hvxxb = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(xfdbb__hvxxb)

    def codegen(context, builder, sig, args):
        fgd__bir, nsvg__bnsrb = args
        nsvg__bnsrb, yhy__xlaz = ListInstance.allocate_ex(context, builder,
            list_type, fgd__bir)
        yhy__xlaz.size = fgd__bir
        return yhy__xlaz.value
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
        dsn__rrpq = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(dsn__rrpq)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    mjdyu__rhk = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        mjdyu__rhk['used_cols'] = used_cols
    fsdq__fbga = 'def impl(T, idx):\n'
    fsdq__fbga += f'  T2 = init_table(T, False)\n'
    fsdq__fbga += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        fsdq__fbga += f'  l = _get_idx_length(idx, len(T))\n'
        fsdq__fbga += f'  T2 = set_table_len(T2, l)\n'
        fsdq__fbga += f'  return T2\n'
        pkbud__xjm = {}
        exec(fsdq__fbga, mjdyu__rhk, pkbud__xjm)
        return pkbud__xjm['impl']
    if used_cols is not None:
        fsdq__fbga += f'  used_set = set(used_cols)\n'
    for jajt__nqgc in T.type_to_blk.values():
        mjdyu__rhk[f'arr_inds_{jajt__nqgc}'] = np.array(T.block_to_arr_ind[
            jajt__nqgc], dtype=np.int64)
        fsdq__fbga += (
            f'  arr_list_{jajt__nqgc} = get_table_block(T, {jajt__nqgc})\n')
        fsdq__fbga += f"""  out_arr_list_{jajt__nqgc} = alloc_list_like(arr_list_{jajt__nqgc}, False)
"""
        fsdq__fbga += f'  for i in range(len(arr_list_{jajt__nqgc})):\n'
        fsdq__fbga += f'    arr_ind_{jajt__nqgc} = arr_inds_{jajt__nqgc}[i]\n'
        if used_cols is not None:
            fsdq__fbga += (
                f'    if arr_ind_{jajt__nqgc} not in used_set: continue\n')
        fsdq__fbga += f"""    ensure_column_unboxed(T, arr_list_{jajt__nqgc}, i, arr_ind_{jajt__nqgc})
"""
        fsdq__fbga += f"""    out_arr_{jajt__nqgc} = ensure_contig_if_np(arr_list_{jajt__nqgc}[i][idx])
"""
        fsdq__fbga += f'    l = len(out_arr_{jajt__nqgc})\n'
        fsdq__fbga += (
            f'    out_arr_list_{jajt__nqgc}[i] = out_arr_{jajt__nqgc}\n')
        fsdq__fbga += (
            f'  T2 = set_table_block(T2, out_arr_list_{jajt__nqgc}, {jajt__nqgc})\n'
            )
    fsdq__fbga += f'  T2 = set_table_len(T2, l)\n'
    fsdq__fbga += f'  return T2\n'
    pkbud__xjm = {}
    exec(fsdq__fbga, mjdyu__rhk, pkbud__xjm)
    return pkbud__xjm['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    fsdq__fbga = 'def impl(T):\n'
    fsdq__fbga += f'  T2 = init_table(T, True)\n'
    fsdq__fbga += f'  l = len(T)\n'
    mjdyu__rhk = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for jajt__nqgc in T.type_to_blk.values():
        mjdyu__rhk[f'arr_inds_{jajt__nqgc}'] = np.array(T.block_to_arr_ind[
            jajt__nqgc], dtype=np.int64)
        fsdq__fbga += (
            f'  arr_list_{jajt__nqgc} = get_table_block(T, {jajt__nqgc})\n')
        fsdq__fbga += f"""  out_arr_list_{jajt__nqgc} = alloc_list_like(arr_list_{jajt__nqgc}, True)
"""
        fsdq__fbga += f'  for i in range(len(arr_list_{jajt__nqgc})):\n'
        fsdq__fbga += f'    arr_ind_{jajt__nqgc} = arr_inds_{jajt__nqgc}[i]\n'
        fsdq__fbga += f"""    ensure_column_unboxed(T, arr_list_{jajt__nqgc}, i, arr_ind_{jajt__nqgc})
"""
        fsdq__fbga += (
            f'    out_arr_{jajt__nqgc} = decode_if_dict_array(arr_list_{jajt__nqgc}[i])\n'
            )
        fsdq__fbga += (
            f'    out_arr_list_{jajt__nqgc}[i] = out_arr_{jajt__nqgc}\n')
        fsdq__fbga += (
            f'  T2 = set_table_block(T2, out_arr_list_{jajt__nqgc}, {jajt__nqgc})\n'
            )
    fsdq__fbga += f'  T2 = set_table_len(T2, l)\n'
    fsdq__fbga += f'  return T2\n'
    pkbud__xjm = {}
    exec(fsdq__fbga, mjdyu__rhk, pkbud__xjm)
    return pkbud__xjm['impl']


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
        cbwo__yzc = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        cbwo__yzc = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            cbwo__yzc.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        hyfg__goot, gbvit__muzi = args
        aktoe__qldd = cgutils.create_struct_proxy(table_type)(context, builder)
        aktoe__qldd.len = gbvit__muzi
        jlsn__pfko = cgutils.unpack_tuple(builder, hyfg__goot)
        for i, rnmxc__hesxj in enumerate(jlsn__pfko):
            setattr(aktoe__qldd, f'block_{i}', rnmxc__hesxj)
            context.nrt.incref(builder, types.List(cbwo__yzc[i]), rnmxc__hesxj)
        return aktoe__qldd._getvalue()
    table_type = TableType(tuple(cbwo__yzc), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
