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
            rdx__dko = 0
            epauj__lle = []
            for i in range(usecols[-1] + 1):
                if i == usecols[rdx__dko]:
                    epauj__lle.append(arrs[rdx__dko])
                    rdx__dko += 1
                else:
                    epauj__lle.append(None)
            for wpgq__yciuy in range(usecols[-1] + 1, num_arrs):
                epauj__lle.append(None)
            self.arrays = epauj__lle
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((mrl__nbvl == qoewk__hhp).all() for mrl__nbvl,
            qoewk__hhp in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        guhf__xjlzw = len(self.arrays)
        hpt__fouz = dict(zip(range(guhf__xjlzw), self.arrays))
        df = pd.DataFrame(hpt__fouz, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        bbpr__dwdyv = []
        drja__pnx = []
        dkf__usk = {}
        pbd__jvis = defaultdict(int)
        omhsj__sobc = defaultdict(list)
        if not has_runtime_cols:
            for i, sne__nuhyv in enumerate(arr_types):
                if sne__nuhyv not in dkf__usk:
                    dkf__usk[sne__nuhyv] = len(dkf__usk)
                qzaja__vagep = dkf__usk[sne__nuhyv]
                bbpr__dwdyv.append(qzaja__vagep)
                drja__pnx.append(pbd__jvis[qzaja__vagep])
                pbd__jvis[qzaja__vagep] += 1
                omhsj__sobc[qzaja__vagep].append(i)
        self.block_nums = bbpr__dwdyv
        self.block_offsets = drja__pnx
        self.type_to_blk = dkf__usk
        self.block_to_arr_ind = omhsj__sobc
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
    return TableType(tuple(numba.typeof(zyr__wpv) for zyr__wpv in val.arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            dtsd__tpgjy = [(f'block_{i}', types.List(sne__nuhyv)) for i,
                sne__nuhyv in enumerate(fe_type.arr_types)]
        else:
            dtsd__tpgjy = [(f'block_{qzaja__vagep}', types.List(sne__nuhyv)
                ) for sne__nuhyv, qzaja__vagep in fe_type.type_to_blk.items()]
        dtsd__tpgjy.append(('parent', types.pyobject))
        dtsd__tpgjy.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, dtsd__tpgjy)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    pytc__xzmx = c.pyapi.object_getattr_string(val, 'arrays')
    occa__cnec = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    occa__cnec.parent = cgutils.get_null_value(occa__cnec.parent.type)
    rxmyr__omg = c.pyapi.make_none()
    wepo__cfxc = c.context.get_constant(types.int64, 0)
    bzn__rhg = cgutils.alloca_once_value(c.builder, wepo__cfxc)
    for sne__nuhyv, qzaja__vagep in typ.type_to_blk.items():
        bkjxo__jshe = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[qzaja__vagep]))
        wpgq__yciuy, vegq__exzs = ListInstance.allocate_ex(c.context, c.
            builder, types.List(sne__nuhyv), bkjxo__jshe)
        vegq__exzs.size = bkjxo__jshe
        wcaf__zozhk = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[
            qzaja__vagep], dtype=np.int64))
        czae__udb = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, wcaf__zozhk)
        with cgutils.for_range(c.builder, bkjxo__jshe) as euegt__zeas:
            i = euegt__zeas.index
            nvhee__xro = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), czae__udb, i)
            jonlv__essgs = c.pyapi.long_from_longlong(nvhee__xro)
            vzu__ogo = c.pyapi.object_getitem(pytc__xzmx, jonlv__essgs)
            osf__hlfnx = c.builder.icmp_unsigned('==', vzu__ogo, rxmyr__omg)
            with c.builder.if_else(osf__hlfnx) as (uwf__mny, mzbwf__ibyge):
                with uwf__mny:
                    fne__grex = c.context.get_constant_null(sne__nuhyv)
                    vegq__exzs.inititem(i, fne__grex, incref=False)
                with mzbwf__ibyge:
                    ojh__tpbyu = c.pyapi.call_method(vzu__ogo, '__len__', ())
                    kpp__ujigw = c.pyapi.long_as_longlong(ojh__tpbyu)
                    c.builder.store(kpp__ujigw, bzn__rhg)
                    c.pyapi.decref(ojh__tpbyu)
                    zyr__wpv = c.pyapi.to_native_value(sne__nuhyv, vzu__ogo
                        ).value
                    vegq__exzs.inititem(i, zyr__wpv, incref=False)
            c.pyapi.decref(vzu__ogo)
            c.pyapi.decref(jonlv__essgs)
        setattr(occa__cnec, f'block_{qzaja__vagep}', vegq__exzs.value)
    occa__cnec.len = c.builder.load(bzn__rhg)
    c.pyapi.decref(pytc__xzmx)
    c.pyapi.decref(rxmyr__omg)
    areh__cjz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(occa__cnec._getvalue(), is_error=areh__cjz)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    occa__cnec = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        ioj__cgc = c.context.get_constant(types.int64, 0)
        for i, sne__nuhyv in enumerate(typ.arr_types):
            epauj__lle = getattr(occa__cnec, f'block_{i}')
            ias__wbkrj = ListInstance(c.context, c.builder, types.List(
                sne__nuhyv), epauj__lle)
            ioj__cgc = c.builder.add(ioj__cgc, ias__wbkrj.size)
        rcp__lkl = c.pyapi.list_new(ioj__cgc)
        xpl__eydy = c.context.get_constant(types.int64, 0)
        for i, sne__nuhyv in enumerate(typ.arr_types):
            epauj__lle = getattr(occa__cnec, f'block_{i}')
            ias__wbkrj = ListInstance(c.context, c.builder, types.List(
                sne__nuhyv), epauj__lle)
            with cgutils.for_range(c.builder, ias__wbkrj.size) as euegt__zeas:
                i = euegt__zeas.index
                zyr__wpv = ias__wbkrj.getitem(i)
                c.context.nrt.incref(c.builder, sne__nuhyv, zyr__wpv)
                idx = c.builder.add(xpl__eydy, i)
                c.pyapi.list_setitem(rcp__lkl, idx, c.pyapi.
                    from_native_value(sne__nuhyv, zyr__wpv, c.env_manager))
            xpl__eydy = c.builder.add(xpl__eydy, ias__wbkrj.size)
        kazur__ppcdj = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        hsyom__bft = c.pyapi.call_function_objargs(kazur__ppcdj, (rcp__lkl,))
        c.pyapi.decref(kazur__ppcdj)
        c.pyapi.decref(rcp__lkl)
        c.context.nrt.decref(c.builder, typ, val)
        return hsyom__bft
    rcp__lkl = c.pyapi.list_new(c.context.get_constant(types.int64, len(typ
        .arr_types)))
    zyp__qpcum = cgutils.is_not_null(c.builder, occa__cnec.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for sne__nuhyv, qzaja__vagep in typ.type_to_blk.items():
        epauj__lle = getattr(occa__cnec, f'block_{qzaja__vagep}')
        ias__wbkrj = ListInstance(c.context, c.builder, types.List(
            sne__nuhyv), epauj__lle)
        wcaf__zozhk = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[
            qzaja__vagep], dtype=np.int64))
        czae__udb = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, wcaf__zozhk)
        with cgutils.for_range(c.builder, ias__wbkrj.size) as euegt__zeas:
            i = euegt__zeas.index
            nvhee__xro = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), czae__udb, i)
            zyr__wpv = ias__wbkrj.getitem(i)
            tri__yidd = cgutils.alloca_once_value(c.builder, zyr__wpv)
            ebhd__xrhze = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(sne__nuhyv))
            glpiu__fyff = is_ll_eq(c.builder, tri__yidd, ebhd__xrhze)
            with c.builder.if_else(c.builder.and_(glpiu__fyff, c.builder.
                not_(ensure_unboxed))) as (uwf__mny, mzbwf__ibyge):
                with uwf__mny:
                    rxmyr__omg = c.pyapi.make_none()
                    c.pyapi.list_setitem(rcp__lkl, nvhee__xro, rxmyr__omg)
                with mzbwf__ibyge:
                    vzu__ogo = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(glpiu__fyff,
                        zyp__qpcum)) as (xhnjg__rid, rwsz__hpc):
                        with xhnjg__rid:
                            gaops__pvoe = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, occa__cnec.
                                parent, nvhee__xro, sne__nuhyv)
                            c.builder.store(gaops__pvoe, vzu__ogo)
                        with rwsz__hpc:
                            c.context.nrt.incref(c.builder, sne__nuhyv,
                                zyr__wpv)
                            c.builder.store(c.pyapi.from_native_value(
                                sne__nuhyv, zyr__wpv, c.env_manager), vzu__ogo)
                    c.pyapi.list_setitem(rcp__lkl, nvhee__xro, c.builder.
                        load(vzu__ogo))
    kazur__ppcdj = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    hsyom__bft = c.pyapi.call_function_objargs(kazur__ppcdj, (rcp__lkl,))
    c.pyapi.decref(kazur__ppcdj)
    c.pyapi.decref(rcp__lkl)
    c.context.nrt.decref(c.builder, typ, val)
    return hsyom__bft


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
        occa__cnec = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        kevo__wglqj = context.get_constant(types.int64, 0)
        for i, sne__nuhyv in enumerate(table_type.arr_types):
            epauj__lle = getattr(occa__cnec, f'block_{i}')
            ias__wbkrj = ListInstance(context, builder, types.List(
                sne__nuhyv), epauj__lle)
            kevo__wglqj = builder.add(kevo__wglqj, ias__wbkrj.size)
        return kevo__wglqj
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    occa__cnec = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    qzaja__vagep = table_type.block_nums[col_ind]
    zotmy__iwi = table_type.block_offsets[col_ind]
    epauj__lle = getattr(occa__cnec, f'block_{qzaja__vagep}')
    ias__wbkrj = ListInstance(context, builder, types.List(arr_type),
        epauj__lle)
    zyr__wpv = ias__wbkrj.getitem(zotmy__iwi)
    return zyr__wpv


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, wpgq__yciuy = args
        zyr__wpv = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, zyr__wpv)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, wpgq__yciuy = args
        occa__cnec = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        qzaja__vagep = table_type.block_nums[col_ind]
        zotmy__iwi = table_type.block_offsets[col_ind]
        epauj__lle = getattr(occa__cnec, f'block_{qzaja__vagep}')
        ias__wbkrj = ListInstance(context, builder, types.List(arr_type),
            epauj__lle)
        zyr__wpv = ias__wbkrj.getitem(zotmy__iwi)
        context.nrt.decref(builder, arr_type, zyr__wpv)
        fne__grex = context.get_constant_null(arr_type)
        ias__wbkrj.inititem(zotmy__iwi, fne__grex, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    wepo__cfxc = context.get_constant(types.int64, 0)
    nag__ohzey = context.get_constant(types.int64, 1)
    ekd__yht = arr_type not in in_table_type.type_to_blk
    for sne__nuhyv, qzaja__vagep in out_table_type.type_to_blk.items():
        if sne__nuhyv in in_table_type.type_to_blk:
            sijcj__hzz = in_table_type.type_to_blk[sne__nuhyv]
            vegq__exzs = ListInstance(context, builder, types.List(
                sne__nuhyv), getattr(in_table, f'block_{sijcj__hzz}'))
            context.nrt.incref(builder, types.List(sne__nuhyv), vegq__exzs.
                value)
            setattr(out_table, f'block_{qzaja__vagep}', vegq__exzs.value)
    if ekd__yht:
        wpgq__yciuy, vegq__exzs = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), nag__ohzey)
        vegq__exzs.size = nag__ohzey
        vegq__exzs.inititem(wepo__cfxc, arr_arg, incref=True)
        qzaja__vagep = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{qzaja__vagep}', vegq__exzs.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        qzaja__vagep = out_table_type.type_to_blk[arr_type]
        vegq__exzs = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{qzaja__vagep}'))
        if is_new_col:
            n = vegq__exzs.size
            vpwh__vasnv = builder.add(n, nag__ohzey)
            vegq__exzs.resize(vpwh__vasnv)
            vegq__exzs.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            vce__bnwr = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            vegq__exzs.setitem(vce__bnwr, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            vce__bnwr = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = vegq__exzs.size
            vpwh__vasnv = builder.add(n, nag__ohzey)
            vegq__exzs.resize(vpwh__vasnv)
            context.nrt.incref(builder, arr_type, vegq__exzs.getitem(vce__bnwr)
                )
            vegq__exzs.move(builder.add(vce__bnwr, nag__ohzey), vce__bnwr,
                builder.sub(n, vce__bnwr))
            vegq__exzs.setitem(vce__bnwr, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    yfopm__hvi = in_table_type.arr_types[col_ind]
    if yfopm__hvi in out_table_type.type_to_blk:
        qzaja__vagep = out_table_type.type_to_blk[yfopm__hvi]
        bjb__tmyoc = getattr(out_table, f'block_{qzaja__vagep}')
        jpgnp__obxvb = types.List(yfopm__hvi)
        vce__bnwr = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        hdbyh__qkiej = jpgnp__obxvb.dtype(jpgnp__obxvb, types.intp)
        irlmi__kgl = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), hdbyh__qkiej, (bjb__tmyoc, vce__bnwr))
        context.nrt.decref(builder, yfopm__hvi, irlmi__kgl)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    vozf__xbtjv = list(table_type.arr_types)
    if is_new_col:
        vozf__xbtjv.append(arr_type)
    else:
        vozf__xbtjv[col_ind] = arr_type
    out_table_type = TableType(tuple(vozf__xbtjv))

    def codegen(context, builder, sig, args):
        table_arg, wpgq__yciuy, iogd__baq = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, iogd__baq, col_ind, is_new_col
            )
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
    nfz__lmnj = args[0]
    if equiv_set.has_shape(nfz__lmnj):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            nfz__lmnj)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    snrtg__tky = []
    for sne__nuhyv, qzaja__vagep in table_type.type_to_blk.items():
        pxu__bqyhw = len(table_type.block_to_arr_ind[qzaja__vagep])
        knc__ezdq = []
        for i in range(pxu__bqyhw):
            nvhee__xro = table_type.block_to_arr_ind[qzaja__vagep][i]
            knc__ezdq.append(pyval.arrays[nvhee__xro])
        snrtg__tky.append(context.get_constant_generic(builder, types.List(
            sne__nuhyv), knc__ezdq))
    lkk__nutp = context.get_constant_null(types.pyobject)
    iwdm__nsnv = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(snrtg__tky + [lkk__nutp, iwdm__nsnv])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        occa__cnec = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for sne__nuhyv, qzaja__vagep in out_table_type.type_to_blk.items():
            pzpe__pdrs = context.get_constant_null(types.List(sne__nuhyv))
            setattr(occa__cnec, f'block_{qzaja__vagep}', pzpe__pdrs)
        return occa__cnec._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    cibo__zzbx = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        cibo__zzbx[typ.dtype] = i
    hdzv__mit = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(hdzv__mit, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        ytnfu__drsps, wpgq__yciuy = args
        occa__cnec = cgutils.create_struct_proxy(hdzv__mit)(context, builder)
        for sne__nuhyv, qzaja__vagep in hdzv__mit.type_to_blk.items():
            idx = cibo__zzbx[sne__nuhyv]
            xbhm__lef = signature(types.List(sne__nuhyv),
                tuple_of_lists_type, types.literal(idx))
            nuvvm__rjv = ytnfu__drsps, idx
            ijry__gvizm = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, xbhm__lef, nuvvm__rjv)
            setattr(occa__cnec, f'block_{qzaja__vagep}', ijry__gvizm)
        return occa__cnec._getvalue()
    sig = hdzv__mit(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    qzaja__vagep = get_overload_const_int(blk_type)
    arr_type = None
    for sne__nuhyv, qoewk__hhp in table_type.type_to_blk.items():
        if qoewk__hhp == qzaja__vagep:
            arr_type = sne__nuhyv
            break
    assert arr_type is not None, 'invalid table type block'
    enxa__hno = types.List(arr_type)

    def codegen(context, builder, sig, args):
        occa__cnec = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        epauj__lle = getattr(occa__cnec, f'block_{qzaja__vagep}')
        return impl_ret_borrowed(context, builder, enxa__hno, epauj__lle)
    sig = enxa__hno(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, wno__apex = args
        pcc__wps = context.get_python_api(builder)
        ioalo__jwd = used_cols_typ == types.none
        if not ioalo__jwd:
            uont__xmxe = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), wno__apex)
        occa__cnec = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        zyp__qpcum = cgutils.is_not_null(builder, occa__cnec.parent)
        for sne__nuhyv, qzaja__vagep in table_type.type_to_blk.items():
            bkjxo__jshe = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[qzaja__vagep]))
            wcaf__zozhk = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                qzaja__vagep], dtype=np.int64))
            czae__udb = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, wcaf__zozhk)
            epauj__lle = getattr(occa__cnec, f'block_{qzaja__vagep}')
            with cgutils.for_range(builder, bkjxo__jshe) as euegt__zeas:
                i = euegt__zeas.index
                nvhee__xro = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'), czae__udb, i
                    )
                dthz__ttejn = types.none(table_type, types.List(sne__nuhyv),
                    types.int64, types.int64)
                skv__fnfpk = table_arg, epauj__lle, i, nvhee__xro
                if ioalo__jwd:
                    ensure_column_unboxed_codegen(context, builder,
                        dthz__ttejn, skv__fnfpk)
                else:
                    exya__dhg = uont__xmxe.contains(nvhee__xro)
                    with builder.if_then(exya__dhg):
                        ensure_column_unboxed_codegen(context, builder,
                            dthz__ttejn, skv__fnfpk)
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
    table_arg, ymkrg__rdk, skew__hbb, uznbd__dvo = args
    pcc__wps = context.get_python_api(builder)
    occa__cnec = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    zyp__qpcum = cgutils.is_not_null(builder, occa__cnec.parent)
    ias__wbkrj = ListInstance(context, builder, sig.args[1], ymkrg__rdk)
    hyp__jjzi = ias__wbkrj.getitem(skew__hbb)
    tri__yidd = cgutils.alloca_once_value(builder, hyp__jjzi)
    ebhd__xrhze = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    glpiu__fyff = is_ll_eq(builder, tri__yidd, ebhd__xrhze)
    with builder.if_then(glpiu__fyff):
        with builder.if_else(zyp__qpcum) as (uwf__mny, mzbwf__ibyge):
            with uwf__mny:
                vzu__ogo = get_df_obj_column_codegen(context, builder,
                    pcc__wps, occa__cnec.parent, uznbd__dvo, sig.args[1].dtype)
                zyr__wpv = pcc__wps.to_native_value(sig.args[1].dtype, vzu__ogo
                    ).value
                ias__wbkrj.inititem(skew__hbb, zyr__wpv, incref=False)
                pcc__wps.decref(vzu__ogo)
            with mzbwf__ibyge:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    qzaja__vagep = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, mibn__msqvl, wpgq__yciuy = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{qzaja__vagep}', mibn__msqvl)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, doppr__uufza = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = doppr__uufza
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    enxa__hno = list_type
    if is_overload_true(to_str_if_dict_t):
        enxa__hno = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        yjluh__fmc = ListInstance(context, builder, list_type, args[0])
        dybf__aoomb = yjluh__fmc.size
        wpgq__yciuy, vegq__exzs = ListInstance.allocate_ex(context, builder,
            enxa__hno, dybf__aoomb)
        vegq__exzs.size = dybf__aoomb
        return vegq__exzs.value
    sig = enxa__hno(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    jadyc__sqp = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(jadyc__sqp)

    def codegen(context, builder, sig, args):
        dybf__aoomb, wpgq__yciuy = args
        wpgq__yciuy, vegq__exzs = ListInstance.allocate_ex(context, builder,
            list_type, dybf__aoomb)
        vegq__exzs.size = dybf__aoomb
        return vegq__exzs.value
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
        plk__rrtq = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(plk__rrtq)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    jucc__nvxqd = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        jucc__nvxqd['used_cols'] = used_cols
    rwvoq__pnkh = 'def impl(T, idx):\n'
    rwvoq__pnkh += f'  T2 = init_table(T, False)\n'
    rwvoq__pnkh += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        rwvoq__pnkh += f'  l = _get_idx_length(idx, len(T))\n'
        rwvoq__pnkh += f'  T2 = set_table_len(T2, l)\n'
        rwvoq__pnkh += f'  return T2\n'
        hay__redlo = {}
        exec(rwvoq__pnkh, jucc__nvxqd, hay__redlo)
        return hay__redlo['impl']
    if used_cols is not None:
        rwvoq__pnkh += f'  used_set = set(used_cols)\n'
    for qzaja__vagep in T.type_to_blk.values():
        jucc__nvxqd[f'arr_inds_{qzaja__vagep}'] = np.array(T.
            block_to_arr_ind[qzaja__vagep], dtype=np.int64)
        rwvoq__pnkh += (
            f'  arr_list_{qzaja__vagep} = get_table_block(T, {qzaja__vagep})\n'
            )
        rwvoq__pnkh += f"""  out_arr_list_{qzaja__vagep} = alloc_list_like(arr_list_{qzaja__vagep}, False)
"""
        rwvoq__pnkh += f'  for i in range(len(arr_list_{qzaja__vagep})):\n'
        rwvoq__pnkh += (
            f'    arr_ind_{qzaja__vagep} = arr_inds_{qzaja__vagep}[i]\n')
        if used_cols is not None:
            rwvoq__pnkh += (
                f'    if arr_ind_{qzaja__vagep} not in used_set: continue\n')
        rwvoq__pnkh += f"""    ensure_column_unboxed(T, arr_list_{qzaja__vagep}, i, arr_ind_{qzaja__vagep})
"""
        rwvoq__pnkh += f"""    out_arr_{qzaja__vagep} = ensure_contig_if_np(arr_list_{qzaja__vagep}[i][idx])
"""
        rwvoq__pnkh += f'    l = len(out_arr_{qzaja__vagep})\n'
        rwvoq__pnkh += (
            f'    out_arr_list_{qzaja__vagep}[i] = out_arr_{qzaja__vagep}\n')
        rwvoq__pnkh += (
            f'  T2 = set_table_block(T2, out_arr_list_{qzaja__vagep}, {qzaja__vagep})\n'
            )
    rwvoq__pnkh += f'  T2 = set_table_len(T2, l)\n'
    rwvoq__pnkh += f'  return T2\n'
    hay__redlo = {}
    exec(rwvoq__pnkh, jucc__nvxqd, hay__redlo)
    return hay__redlo['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    rwvoq__pnkh = 'def impl(T):\n'
    rwvoq__pnkh += f'  T2 = init_table(T, True)\n'
    rwvoq__pnkh += f'  l = len(T)\n'
    jucc__nvxqd = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for qzaja__vagep in T.type_to_blk.values():
        jucc__nvxqd[f'arr_inds_{qzaja__vagep}'] = np.array(T.
            block_to_arr_ind[qzaja__vagep], dtype=np.int64)
        rwvoq__pnkh += (
            f'  arr_list_{qzaja__vagep} = get_table_block(T, {qzaja__vagep})\n'
            )
        rwvoq__pnkh += f"""  out_arr_list_{qzaja__vagep} = alloc_list_like(arr_list_{qzaja__vagep}, True)
"""
        rwvoq__pnkh += f'  for i in range(len(arr_list_{qzaja__vagep})):\n'
        rwvoq__pnkh += (
            f'    arr_ind_{qzaja__vagep} = arr_inds_{qzaja__vagep}[i]\n')
        rwvoq__pnkh += f"""    ensure_column_unboxed(T, arr_list_{qzaja__vagep}, i, arr_ind_{qzaja__vagep})
"""
        rwvoq__pnkh += f"""    out_arr_{qzaja__vagep} = decode_if_dict_array(arr_list_{qzaja__vagep}[i])
"""
        rwvoq__pnkh += (
            f'    out_arr_list_{qzaja__vagep}[i] = out_arr_{qzaja__vagep}\n')
        rwvoq__pnkh += (
            f'  T2 = set_table_block(T2, out_arr_list_{qzaja__vagep}, {qzaja__vagep})\n'
            )
    rwvoq__pnkh += f'  T2 = set_table_len(T2, l)\n'
    rwvoq__pnkh += f'  return T2\n'
    hay__redlo = {}
    exec(rwvoq__pnkh, jucc__nvxqd, hay__redlo)
    return hay__redlo['impl']


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
        ckmx__jsa = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        ckmx__jsa = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            ckmx__jsa.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        ccgh__ons, vmcz__qbcw = args
        occa__cnec = cgutils.create_struct_proxy(table_type)(context, builder)
        occa__cnec.len = vmcz__qbcw
        snrtg__tky = cgutils.unpack_tuple(builder, ccgh__ons)
        for i, epauj__lle in enumerate(snrtg__tky):
            setattr(occa__cnec, f'block_{i}', epauj__lle)
            context.nrt.incref(builder, types.List(ckmx__jsa[i]), epauj__lle)
        return occa__cnec._getvalue()
    table_type = TableType(tuple(ckmx__jsa), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
