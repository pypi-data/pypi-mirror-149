"""Numba extension support for datetime.date objects and their arrays.
"""
import datetime
import operator
import warnings
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.typing.templates import AttributeTemplate, infer_getattr
from numba.core.utils import PYVERSION
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import DatetimeDatetimeType
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type, is_overload_int, is_overload_none
ll.add_symbol('box_datetime_date_array', hdatetime_ext.box_datetime_date_array)
ll.add_symbol('unbox_datetime_date_array', hdatetime_ext.
    unbox_datetime_date_array)
ll.add_symbol('get_isocalendar', hdatetime_ext.get_isocalendar)


class DatetimeDateType(types.Type):

    def __init__(self):
        super(DatetimeDateType, self).__init__(name='DatetimeDateType()')
        self.bitwidth = 64


datetime_date_type = DatetimeDateType()


@typeof_impl.register(datetime.date)
def typeof_datetime_date(val, c):
    return datetime_date_type


register_model(DatetimeDateType)(models.IntegerModel)


@infer_getattr
class DatetimeAttribute(AttributeTemplate):
    key = DatetimeDateType

    def resolve_year(self, typ):
        return types.int64

    def resolve_month(self, typ):
        return types.int64

    def resolve_day(self, typ):
        return types.int64


@lower_getattr(DatetimeDateType, 'year')
def datetime_get_year(context, builder, typ, val):
    return builder.lshr(val, lir.Constant(lir.IntType(64), 32))


@lower_getattr(DatetimeDateType, 'month')
def datetime_get_month(context, builder, typ, val):
    return builder.and_(builder.lshr(val, lir.Constant(lir.IntType(64), 16)
        ), lir.Constant(lir.IntType(64), 65535))


@lower_getattr(DatetimeDateType, 'day')
def datetime_get_day(context, builder, typ, val):
    return builder.and_(val, lir.Constant(lir.IntType(64), 65535))


@unbox(DatetimeDateType)
def unbox_datetime_date(typ, val, c):
    ode__qutxg = c.pyapi.object_getattr_string(val, 'year')
    vgdyn__wxte = c.pyapi.object_getattr_string(val, 'month')
    dolcj__hvmj = c.pyapi.object_getattr_string(val, 'day')
    xuqm__sfo = c.pyapi.long_as_longlong(ode__qutxg)
    liuz__dgys = c.pyapi.long_as_longlong(vgdyn__wxte)
    xmpee__papc = c.pyapi.long_as_longlong(dolcj__hvmj)
    sdm__yca = c.builder.add(xmpee__papc, c.builder.add(c.builder.shl(
        xuqm__sfo, lir.Constant(lir.IntType(64), 32)), c.builder.shl(
        liuz__dgys, lir.Constant(lir.IntType(64), 16))))
    c.pyapi.decref(ode__qutxg)
    c.pyapi.decref(vgdyn__wxte)
    c.pyapi.decref(dolcj__hvmj)
    zky__fgne = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(sdm__yca, is_error=zky__fgne)


@lower_constant(DatetimeDateType)
def lower_constant_datetime_date(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    sdm__yca = builder.add(day, builder.add(builder.shl(year, lir.Constant(
        lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir.IntType(
        64), 16))))
    return sdm__yca


@box(DatetimeDateType)
def box_datetime_date(typ, val, c):
    ode__qutxg = c.pyapi.long_from_longlong(c.builder.lshr(val, lir.
        Constant(lir.IntType(64), 32)))
    vgdyn__wxte = c.pyapi.long_from_longlong(c.builder.and_(c.builder.lshr(
        val, lir.Constant(lir.IntType(64), 16)), lir.Constant(lir.IntType(
        64), 65535)))
    dolcj__hvmj = c.pyapi.long_from_longlong(c.builder.and_(val, lir.
        Constant(lir.IntType(64), 65535)))
    orbp__htyt = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.date))
    xjuxv__uig = c.pyapi.call_function_objargs(orbp__htyt, (ode__qutxg,
        vgdyn__wxte, dolcj__hvmj))
    c.pyapi.decref(ode__qutxg)
    c.pyapi.decref(vgdyn__wxte)
    c.pyapi.decref(dolcj__hvmj)
    c.pyapi.decref(orbp__htyt)
    return xjuxv__uig


@type_callable(datetime.date)
def type_datetime_date(context):

    def typer(year, month, day):
        return datetime_date_type
    return typer


@lower_builtin(datetime.date, types.IntegerLiteral, types.IntegerLiteral,
    types.IntegerLiteral)
@lower_builtin(datetime.date, types.int64, types.int64, types.int64)
def impl_ctor_datetime_date(context, builder, sig, args):
    year, month, day = args
    sdm__yca = builder.add(day, builder.add(builder.shl(year, lir.Constant(
        lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir.IntType(
        64), 16))))
    return sdm__yca


@intrinsic
def cast_int_to_datetime_date(typingctx, val=None):
    assert val == types.int64

    def codegen(context, builder, signature, args):
        return args[0]
    return datetime_date_type(types.int64), codegen


@intrinsic
def cast_datetime_date_to_int(typingctx, val=None):
    assert val == datetime_date_type

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(datetime_date_type), codegen


"""
Following codes are copied from
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""
_MAXORDINAL = 3652059
_DAYS_IN_MONTH = np.array([-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 
    31], dtype=np.int64)
_DAYS_BEFORE_MONTH = np.array([-1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 
    273, 304, 334], dtype=np.int64)


@register_jitable
def _is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


@register_jitable
def _days_before_year(year):
    y = year - 1
    return y * 365 + y // 4 - y // 100 + y // 400


@register_jitable
def _days_in_month(year, month):
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


@register_jitable
def _days_before_month(year, month):
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


_DI400Y = _days_before_year(401)
_DI100Y = _days_before_year(101)
_DI4Y = _days_before_year(5)


@register_jitable
def _ymd2ord(year, month, day):
    fxqt__twhc = _days_in_month(year, month)
    return _days_before_year(year) + _days_before_month(year, month) + day


@register_jitable
def _ord2ymd(n):
    n -= 1
    zrvxr__unxmd, n = divmod(n, _DI400Y)
    year = zrvxr__unxmd * 400 + 1
    yszb__zcyry, n = divmod(n, _DI100Y)
    zcnnb__fvqvm, n = divmod(n, _DI4Y)
    uuzd__xsct, n = divmod(n, 365)
    year += yszb__zcyry * 100 + zcnnb__fvqvm * 4 + uuzd__xsct
    if uuzd__xsct == 4 or yszb__zcyry == 4:
        return year - 1, 12, 31
    ewgvz__izqqq = uuzd__xsct == 3 and (zcnnb__fvqvm != 24 or yszb__zcyry == 3)
    month = n + 50 >> 5
    mctv__fkerr = _DAYS_BEFORE_MONTH[month] + (month > 2 and ewgvz__izqqq)
    if mctv__fkerr > n:
        month -= 1
        mctv__fkerr -= _DAYS_IN_MONTH[month] + (month == 2 and ewgvz__izqqq)
    n -= mctv__fkerr
    return year, month, n + 1


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@intrinsic
def get_isocalendar(typingctx, dt_year, dt_month, dt_day):

    def codegen(context, builder, sig, args):
        year = cgutils.alloca_once(builder, lir.IntType(64))
        bte__igk = cgutils.alloca_once(builder, lir.IntType(64))
        dmg__ilizz = cgutils.alloca_once(builder, lir.IntType(64))
        aoq__vef = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir.
            IntType(64), lir.IntType(64), lir.IntType(64).as_pointer(), lir
            .IntType(64).as_pointer(), lir.IntType(64).as_pointer()])
        dgfz__ciyxi = cgutils.get_or_insert_function(builder.module,
            aoq__vef, name='get_isocalendar')
        builder.call(dgfz__ciyxi, [args[0], args[1], args[2], year,
            bte__igk, dmg__ilizz])
        return cgutils.pack_array(builder, [builder.load(year), builder.
            load(bte__igk), builder.load(dmg__ilizz)])
    xjuxv__uig = types.Tuple([types.int64, types.int64, types.int64])(types
        .int64, types.int64, types.int64), codegen
    return xjuxv__uig


types.datetime_date_type = datetime_date_type


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_date_type'):
        d = datetime.date.today()
    return d


@register_jitable
def fromordinal_impl(n):
    y, wsuda__wkipz, d = _ord2ymd(n)
    return datetime.date(y, wsuda__wkipz, d)


@overload_method(DatetimeDateType, 'replace')
def replace_overload(date, year=None, month=None, day=None):
    if not is_overload_none(year) and not is_overload_int(year):
        raise BodoError('date.replace(): year must be an integer')
    elif not is_overload_none(month) and not is_overload_int(month):
        raise BodoError('date.replace(): month must be an integer')
    elif not is_overload_none(day) and not is_overload_int(day):
        raise BodoError('date.replace(): day must be an integer')

    def impl(date, year=None, month=None, day=None):
        oekli__rjrh = date.year if year is None else year
        gjsyu__isin = date.month if month is None else month
        vvdw__uozgo = date.day if day is None else day
        return datetime.date(oekli__rjrh, gjsyu__isin, vvdw__uozgo)
    return impl


@overload_method(DatetimeDatetimeType, 'toordinal', no_unliteral=True)
@overload_method(DatetimeDateType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


@overload_method(DatetimeDatetimeType, 'weekday', no_unliteral=True)
@overload_method(DatetimeDateType, 'weekday', no_unliteral=True)
def weekday(date):

    def impl(date):
        return (date.toordinal() + 6) % 7
    return impl


@overload_method(DatetimeDateType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(date):

    def impl(date):
        year, bte__igk, widrg__ozsri = get_isocalendar(date.year, date.
            month, date.day)
        return year, bte__igk, widrg__ozsri
    return impl


def overload_add_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            pbhg__zhoh = lhs.toordinal() + rhs.days
            if 0 < pbhg__zhoh <= _MAXORDINAL:
                return fromordinal_impl(pbhg__zhoh)
            raise OverflowError('result out of range')
        return impl
    elif lhs == datetime_timedelta_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            pbhg__zhoh = lhs.days + rhs.toordinal()
            if 0 < pbhg__zhoh <= _MAXORDINAL:
                return fromordinal_impl(pbhg__zhoh)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + datetime.timedelta(-rhs.days)
        return impl
    elif lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            oebip__ijqcd = lhs.toordinal()
            tnfyf__azu = rhs.toordinal()
            return datetime.timedelta(oebip__ijqcd - tnfyf__azu)
        return impl
    if lhs == datetime_date_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            xbtl__ifc = lhs
            numba.parfors.parfor.init_prange()
            n = len(xbtl__ifc)
            A = alloc_datetime_date_array(n)
            for drdy__xcxye in numba.parfors.parfor.internal_prange(n):
                A[drdy__xcxye] = xbtl__ifc[drdy__xcxye] - rhs
            return A
        return impl


@overload(min, no_unliteral=True)
def date_min(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def date_max(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        bqhfa__emql = np.uint8(td.year // 256)
        fjef__qdiuf = np.uint8(td.year % 256)
        month = np.uint8(td.month)
        day = np.uint8(td.day)
        vxyl__pujx = bqhfa__emql, fjef__qdiuf, month, day
        return hash(vxyl__pujx)
    return impl


@overload(bool, inline='always', no_unliteral=True)
def date_to_bool(date):
    if date != datetime_date_type:
        return

    def impl(date):
        return True
    return impl


if PYVERSION >= (3, 9):
    IsoCalendarDate = datetime.date(2011, 1, 1).isocalendar().__class__


    class IsoCalendarDateType(types.Type):

        def __init__(self):
            super(IsoCalendarDateType, self).__init__(name=
                'IsoCalendarDateType()')
    iso_calendar_date_type = DatetimeDateType()

    @typeof_impl.register(IsoCalendarDate)
    def typeof_datetime_date(val, c):
        return iso_calendar_date_type


class DatetimeDateArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeDateArrayType, self).__init__(name=
            'DatetimeDateArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_date_type

    def copy(self):
        return DatetimeDateArrayType()


datetime_date_array_type = DatetimeDateArrayType()
types.datetime_date_array_type = datetime_date_array_type
data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeDateArrayType)
class DatetimeDateArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cmkly__iwkvo = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, cmkly__iwkvo)


make_attribute_wrapper(DatetimeDateArrayType, 'data', '_data')
make_attribute_wrapper(DatetimeDateArrayType, 'null_bitmap', '_null_bitmap')


@overload_method(DatetimeDateArrayType, 'copy', no_unliteral=True)
def overload_datetime_date_arr_copy(A):
    return lambda A: bodo.hiframes.datetime_date_ext.init_datetime_date_array(A
        ._data.copy(), A._null_bitmap.copy())


@overload_attribute(DatetimeDateArrayType, 'dtype')
def overload_datetime_date_arr_dtype(A):
    return lambda A: np.object_


@unbox(DatetimeDateArrayType)
def unbox_datetime_date_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    hcffs__vuzz = types.Array(types.intp, 1, 'C')
    bywld__ltzsi = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        hcffs__vuzz, [n])
    bramq__peol = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    uuz__jfe = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types.
        Array(types.uint8, 1, 'C'), [bramq__peol])
    aoq__vef = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer(
        ), lir.IntType(64), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer()])
    lhacq__nxg = cgutils.get_or_insert_function(c.builder.module, aoq__vef,
        name='unbox_datetime_date_array')
    c.builder.call(lhacq__nxg, [val, n, bywld__ltzsi.data, uuz__jfe.data])
    ueo__vtvmy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ueo__vtvmy.data = bywld__ltzsi._getvalue()
    ueo__vtvmy.null_bitmap = uuz__jfe._getvalue()
    zky__fgne = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ueo__vtvmy._getvalue(), is_error=zky__fgne)


def int_to_datetime_date_python(ia):
    return datetime.date(ia >> 32, ia >> 16 & 65535, ia & 65535)


def int_array_to_datetime_date(ia):
    return np.vectorize(int_to_datetime_date_python, otypes=[object])(ia)


@box(DatetimeDateArrayType)
def box_datetime_date_array(typ, val, c):
    xbtl__ifc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    bywld__ltzsi = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
        .context, c.builder, xbtl__ifc.data)
    cnuh__fsli = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, xbtl__ifc.null_bitmap).data
    n = c.builder.extract_value(bywld__ltzsi.shape, 0)
    aoq__vef = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(8).as_pointer()])
    yliea__lylk = cgutils.get_or_insert_function(c.builder.module, aoq__vef,
        name='box_datetime_date_array')
    svo__emi = c.builder.call(yliea__lylk, [n, bywld__ltzsi.data, cnuh__fsli])
    c.context.nrt.decref(c.builder, typ, val)
    return svo__emi


@intrinsic
def init_datetime_date_array(typingctx, data, nulls=None):
    assert data == types.Array(types.int64, 1, 'C') or data == types.Array(
        types.NPDatetime('ns'), 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        dswzy__icw, oat__rkgw = args
        ach__str = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        ach__str.data = dswzy__icw
        ach__str.null_bitmap = oat__rkgw
        context.nrt.incref(builder, signature.args[0], dswzy__icw)
        context.nrt.incref(builder, signature.args[1], oat__rkgw)
        return ach__str._getvalue()
    sig = datetime_date_array_type(data, nulls)
    return sig, codegen


@lower_constant(DatetimeDateArrayType)
def lower_constant_datetime_date_arr(context, builder, typ, pyval):
    n = len(pyval)
    jed__lkzj = (1970 << 32) + (1 << 16) + 1
    bywld__ltzsi = np.full(n, jed__lkzj, np.int64)
    amhb__rbja = np.empty(n + 7 >> 3, np.uint8)
    for drdy__xcxye, ukzro__ivx in enumerate(pyval):
        grw__cnzpd = pd.isna(ukzro__ivx)
        bodo.libs.int_arr_ext.set_bit_to_arr(amhb__rbja, drdy__xcxye, int(
            not grw__cnzpd))
        if not grw__cnzpd:
            bywld__ltzsi[drdy__xcxye] = (ukzro__ivx.year << 32) + (ukzro__ivx
                .month << 16) + ukzro__ivx.day
    nybip__icb = context.get_constant_generic(builder, data_type, bywld__ltzsi)
    sxnj__dwka = context.get_constant_generic(builder, nulls_type, amhb__rbja)
    return lir.Constant.literal_struct([nybip__icb, sxnj__dwka])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_date_array(n):
    bywld__ltzsi = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_date_array(bywld__ltzsi, nulls)


def alloc_datetime_date_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_date_ext_alloc_datetime_date_array
    ) = alloc_datetime_date_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_date_arr_getitem(A, ind):
    if A != datetime_date_array_type:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: cast_int_to_datetime_date(A._data[ind])
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            xigx__szn, qdffi__yfiw = array_getitem_bool_index(A, ind)
            return init_datetime_date_array(xigx__szn, qdffi__yfiw)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            xigx__szn, qdffi__yfiw = array_getitem_int_index(A, ind)
            return init_datetime_date_array(xigx__szn, qdffi__yfiw)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            xigx__szn, qdffi__yfiw = array_getitem_slice_index(A, ind)
            return init_datetime_date_array(xigx__szn, qdffi__yfiw)
        return impl_slice
    raise BodoError(
        f'getitem for DatetimeDateArray with indexing type {ind} not supported.'
        )


@overload(operator.setitem, no_unliteral=True)
def dt_date_arr_setitem(A, idx, val):
    if A != datetime_date_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    kltjp__bku = (
        f"setitem for DatetimeDateArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == datetime_date_type:

            def impl(A, idx, val):
                A._data[idx] = cast_datetime_date_to_int(val)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl
        else:
            raise BodoError(kltjp__bku)
    if not (is_iterable_type(val) and val.dtype == bodo.datetime_date_type or
        types.unliteral(val) == datetime_date_type):
        raise BodoError(kltjp__bku)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_int_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_arr_ind(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_bool_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_slice_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeDateArray with indexing type {idx} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_date_arr(A):
    if A == datetime_date_array_type:
        return lambda A: len(A._data)


@overload_attribute(DatetimeDateArrayType, 'shape')
def overload_datetime_date_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(DatetimeDateArrayType, 'nbytes')
def datetime_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


def create_cmp_op_overload(op):

    def overload_date_cmp(lhs, rhs):
        if lhs == datetime_date_type and rhs == datetime_date_type:

            def impl(lhs, rhs):
                y, dkbnn__wha = lhs.year, rhs.year
                wsuda__wkipz, rnjw__roii = lhs.month, rhs.month
                d, iwx__bijh = lhs.day, rhs.day
                return op(_cmp((y, wsuda__wkipz, d), (dkbnn__wha,
                    rnjw__roii, iwx__bijh)), 0)
            return impl
    return overload_date_cmp


def create_datetime_date_cmp_op_overload(op):

    def overload_cmp(lhs, rhs):
        zqubb__tndm = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[op]} {rhs} is always {op == operator.ne} in Python. If this is unexpected there may be a bug in your code.'
            )
        warnings.warn(zqubb__tndm, bodo.utils.typing.BodoWarning)
        if op == operator.eq:
            return lambda lhs, rhs: False
        elif op == operator.ne:
            return lambda lhs, rhs: True
    return overload_cmp


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            ouv__kieqj = True
        else:
            ouv__kieqj = False
        if lhs == datetime_date_array_type and rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                dmpj__nefao = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for drdy__xcxye in numba.parfors.parfor.internal_prange(n):
                    lush__lyn = bodo.libs.array_kernels.isna(lhs, drdy__xcxye)
                    bcxa__vjdm = bodo.libs.array_kernels.isna(rhs, drdy__xcxye)
                    if lush__lyn or bcxa__vjdm:
                        ovc__xjvx = ouv__kieqj
                    else:
                        ovc__xjvx = op(lhs[drdy__xcxye], rhs[drdy__xcxye])
                    dmpj__nefao[drdy__xcxye] = ovc__xjvx
                return dmpj__nefao
            return impl
        elif lhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                dmpj__nefao = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for drdy__xcxye in numba.parfors.parfor.internal_prange(n):
                    vons__vbkdn = bodo.libs.array_kernels.isna(lhs, drdy__xcxye
                        )
                    if vons__vbkdn:
                        ovc__xjvx = ouv__kieqj
                    else:
                        ovc__xjvx = op(lhs[drdy__xcxye], rhs)
                    dmpj__nefao[drdy__xcxye] = ovc__xjvx
                return dmpj__nefao
            return impl
        elif rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                dmpj__nefao = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for drdy__xcxye in numba.parfors.parfor.internal_prange(n):
                    vons__vbkdn = bodo.libs.array_kernels.isna(rhs, drdy__xcxye
                        )
                    if vons__vbkdn:
                        ovc__xjvx = ouv__kieqj
                    else:
                        ovc__xjvx = op(lhs, rhs[drdy__xcxye])
                    dmpj__nefao[drdy__xcxye] = ovc__xjvx
                return dmpj__nefao
            return impl
    return overload_date_arr_cmp
