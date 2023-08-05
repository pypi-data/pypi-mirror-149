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
    geoh__yzuy = c.pyapi.object_getattr_string(val, 'year')
    jee__bacqu = c.pyapi.object_getattr_string(val, 'month')
    qttj__lurk = c.pyapi.object_getattr_string(val, 'day')
    iqbil__vsa = c.pyapi.long_as_longlong(geoh__yzuy)
    woisa__mcjdh = c.pyapi.long_as_longlong(jee__bacqu)
    rsz__erkv = c.pyapi.long_as_longlong(qttj__lurk)
    uyizz__vtvn = c.builder.add(rsz__erkv, c.builder.add(c.builder.shl(
        iqbil__vsa, lir.Constant(lir.IntType(64), 32)), c.builder.shl(
        woisa__mcjdh, lir.Constant(lir.IntType(64), 16))))
    c.pyapi.decref(geoh__yzuy)
    c.pyapi.decref(jee__bacqu)
    c.pyapi.decref(qttj__lurk)
    fadei__onqy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(uyizz__vtvn, is_error=fadei__onqy)


@lower_constant(DatetimeDateType)
def lower_constant_datetime_date(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    uyizz__vtvn = builder.add(day, builder.add(builder.shl(year, lir.
        Constant(lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir
        .IntType(64), 16))))
    return uyizz__vtvn


@box(DatetimeDateType)
def box_datetime_date(typ, val, c):
    geoh__yzuy = c.pyapi.long_from_longlong(c.builder.lshr(val, lir.
        Constant(lir.IntType(64), 32)))
    jee__bacqu = c.pyapi.long_from_longlong(c.builder.and_(c.builder.lshr(
        val, lir.Constant(lir.IntType(64), 16)), lir.Constant(lir.IntType(
        64), 65535)))
    qttj__lurk = c.pyapi.long_from_longlong(c.builder.and_(val, lir.
        Constant(lir.IntType(64), 65535)))
    apoh__lne = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.date))
    oxwvf__xlemx = c.pyapi.call_function_objargs(apoh__lne, (geoh__yzuy,
        jee__bacqu, qttj__lurk))
    c.pyapi.decref(geoh__yzuy)
    c.pyapi.decref(jee__bacqu)
    c.pyapi.decref(qttj__lurk)
    c.pyapi.decref(apoh__lne)
    return oxwvf__xlemx


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
    uyizz__vtvn = builder.add(day, builder.add(builder.shl(year, lir.
        Constant(lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir
        .IntType(64), 16))))
    return uyizz__vtvn


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
    hix__qmivx = _days_in_month(year, month)
    return _days_before_year(year) + _days_before_month(year, month) + day


@register_jitable
def _ord2ymd(n):
    n -= 1
    atu__slaza, n = divmod(n, _DI400Y)
    year = atu__slaza * 400 + 1
    wzy__tbdtt, n = divmod(n, _DI100Y)
    dpiqq__lso, n = divmod(n, _DI4Y)
    crdf__qgzea, n = divmod(n, 365)
    year += wzy__tbdtt * 100 + dpiqq__lso * 4 + crdf__qgzea
    if crdf__qgzea == 4 or wzy__tbdtt == 4:
        return year - 1, 12, 31
    ljiag__flife = crdf__qgzea == 3 and (dpiqq__lso != 24 or wzy__tbdtt == 3)
    month = n + 50 >> 5
    jbfcy__tdsp = _DAYS_BEFORE_MONTH[month] + (month > 2 and ljiag__flife)
    if jbfcy__tdsp > n:
        month -= 1
        jbfcy__tdsp -= _DAYS_IN_MONTH[month] + (month == 2 and ljiag__flife)
    n -= jbfcy__tdsp
    return year, month, n + 1


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@intrinsic
def get_isocalendar(typingctx, dt_year, dt_month, dt_day):

    def codegen(context, builder, sig, args):
        year = cgutils.alloca_once(builder, lir.IntType(64))
        yvtrp__oywq = cgutils.alloca_once(builder, lir.IntType(64))
        rdqci__vxp = cgutils.alloca_once(builder, lir.IntType(64))
        mhaq__tpp = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir.
            IntType(64), lir.IntType(64), lir.IntType(64).as_pointer(), lir
            .IntType(64).as_pointer(), lir.IntType(64).as_pointer()])
        iamdr__hxt = cgutils.get_or_insert_function(builder.module,
            mhaq__tpp, name='get_isocalendar')
        builder.call(iamdr__hxt, [args[0], args[1], args[2], year,
            yvtrp__oywq, rdqci__vxp])
        return cgutils.pack_array(builder, [builder.load(year), builder.
            load(yvtrp__oywq), builder.load(rdqci__vxp)])
    oxwvf__xlemx = types.Tuple([types.int64, types.int64, types.int64])(types
        .int64, types.int64, types.int64), codegen
    return oxwvf__xlemx


types.datetime_date_type = datetime_date_type


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_date_type'):
        d = datetime.date.today()
    return d


@register_jitable
def fromordinal_impl(n):
    y, blqw__vuofl, d = _ord2ymd(n)
    return datetime.date(y, blqw__vuofl, d)


@overload_method(DatetimeDateType, 'replace')
def replace_overload(date, year=None, month=None, day=None):
    if not is_overload_none(year) and not is_overload_int(year):
        raise BodoError('date.replace(): year must be an integer')
    elif not is_overload_none(month) and not is_overload_int(month):
        raise BodoError('date.replace(): month must be an integer')
    elif not is_overload_none(day) and not is_overload_int(day):
        raise BodoError('date.replace(): day must be an integer')

    def impl(date, year=None, month=None, day=None):
        gord__zidpi = date.year if year is None else year
        bjd__mguzj = date.month if month is None else month
        dfiy__wgo = date.day if day is None else day
        return datetime.date(gord__zidpi, bjd__mguzj, dfiy__wgo)
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
        year, yvtrp__oywq, rwu__hhhb = get_isocalendar(date.year, date.
            month, date.day)
        return year, yvtrp__oywq, rwu__hhhb
    return impl


def overload_add_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            piqgw__jgcu = lhs.toordinal() + rhs.days
            if 0 < piqgw__jgcu <= _MAXORDINAL:
                return fromordinal_impl(piqgw__jgcu)
            raise OverflowError('result out of range')
        return impl
    elif lhs == datetime_timedelta_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            piqgw__jgcu = lhs.days + rhs.toordinal()
            if 0 < piqgw__jgcu <= _MAXORDINAL:
                return fromordinal_impl(piqgw__jgcu)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + datetime.timedelta(-rhs.days)
        return impl
    elif lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            xxyo__vbs = lhs.toordinal()
            vumh__wpqm = rhs.toordinal()
            return datetime.timedelta(xxyo__vbs - vumh__wpqm)
        return impl
    if lhs == datetime_date_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            kep__lhfs = lhs
            numba.parfors.parfor.init_prange()
            n = len(kep__lhfs)
            A = alloc_datetime_date_array(n)
            for fov__hclwd in numba.parfors.parfor.internal_prange(n):
                A[fov__hclwd] = kep__lhfs[fov__hclwd] - rhs
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
        snvvd__yboj = np.uint8(td.year // 256)
        vrnaf__ulckt = np.uint8(td.year % 256)
        month = np.uint8(td.month)
        day = np.uint8(td.day)
        xouzl__laufv = snvvd__yboj, vrnaf__ulckt, month, day
        return hash(xouzl__laufv)
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
        oyvg__exk = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, oyvg__exk)


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
    gob__txeic = types.Array(types.intp, 1, 'C')
    kbxgw__pswli = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        gob__txeic, [n])
    yfx__vyprb = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    ojvmm__jqh = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [yfx__vyprb])
    mhaq__tpp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer()])
    ljo__msw = cgutils.get_or_insert_function(c.builder.module, mhaq__tpp,
        name='unbox_datetime_date_array')
    c.builder.call(ljo__msw, [val, n, kbxgw__pswli.data, ojvmm__jqh.data])
    yeav__xurtp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yeav__xurtp.data = kbxgw__pswli._getvalue()
    yeav__xurtp.null_bitmap = ojvmm__jqh._getvalue()
    fadei__onqy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yeav__xurtp._getvalue(), is_error=fadei__onqy)


def int_to_datetime_date_python(ia):
    return datetime.date(ia >> 32, ia >> 16 & 65535, ia & 65535)


def int_array_to_datetime_date(ia):
    return np.vectorize(int_to_datetime_date_python, otypes=[object])(ia)


@box(DatetimeDateArrayType)
def box_datetime_date_array(typ, val, c):
    kep__lhfs = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    kbxgw__pswli = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
        .context, c.builder, kep__lhfs.data)
    dmdf__nkgh = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, kep__lhfs.null_bitmap).data
    n = c.builder.extract_value(kbxgw__pswli.shape, 0)
    mhaq__tpp = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(8).as_pointer()])
    axebk__ctoyy = cgutils.get_or_insert_function(c.builder.module,
        mhaq__tpp, name='box_datetime_date_array')
    ncemj__jhooy = c.builder.call(axebk__ctoyy, [n, kbxgw__pswli.data,
        dmdf__nkgh])
    c.context.nrt.decref(c.builder, typ, val)
    return ncemj__jhooy


@intrinsic
def init_datetime_date_array(typingctx, data, nulls=None):
    assert data == types.Array(types.int64, 1, 'C') or data == types.Array(
        types.NPDatetime('ns'), 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        dmdq__widvy, vmh__igfo = args
        vjt__bhdc = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        vjt__bhdc.data = dmdq__widvy
        vjt__bhdc.null_bitmap = vmh__igfo
        context.nrt.incref(builder, signature.args[0], dmdq__widvy)
        context.nrt.incref(builder, signature.args[1], vmh__igfo)
        return vjt__bhdc._getvalue()
    sig = datetime_date_array_type(data, nulls)
    return sig, codegen


@lower_constant(DatetimeDateArrayType)
def lower_constant_datetime_date_arr(context, builder, typ, pyval):
    n = len(pyval)
    ynsy__koyo = (1970 << 32) + (1 << 16) + 1
    kbxgw__pswli = np.full(n, ynsy__koyo, np.int64)
    tces__jjdp = np.empty(n + 7 >> 3, np.uint8)
    for fov__hclwd, jyg__uvaza in enumerate(pyval):
        fxoad__rohpq = pd.isna(jyg__uvaza)
        bodo.libs.int_arr_ext.set_bit_to_arr(tces__jjdp, fov__hclwd, int(
            not fxoad__rohpq))
        if not fxoad__rohpq:
            kbxgw__pswli[fov__hclwd] = (jyg__uvaza.year << 32) + (jyg__uvaza
                .month << 16) + jyg__uvaza.day
    rny__erlou = context.get_constant_generic(builder, data_type, kbxgw__pswli)
    htd__epib = context.get_constant_generic(builder, nulls_type, tces__jjdp)
    return lir.Constant.literal_struct([rny__erlou, htd__epib])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_date_array(n):
    kbxgw__pswli = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_date_array(kbxgw__pswli, nulls)


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
            nfbz__ubrc, vrhr__vgyug = array_getitem_bool_index(A, ind)
            return init_datetime_date_array(nfbz__ubrc, vrhr__vgyug)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            nfbz__ubrc, vrhr__vgyug = array_getitem_int_index(A, ind)
            return init_datetime_date_array(nfbz__ubrc, vrhr__vgyug)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            nfbz__ubrc, vrhr__vgyug = array_getitem_slice_index(A, ind)
            return init_datetime_date_array(nfbz__ubrc, vrhr__vgyug)
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
    jgjom__ual = (
        f"setitem for DatetimeDateArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == datetime_date_type:

            def impl(A, idx, val):
                A._data[idx] = cast_datetime_date_to_int(val)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl
        else:
            raise BodoError(jgjom__ual)
    if not (is_iterable_type(val) and val.dtype == bodo.datetime_date_type or
        types.unliteral(val) == datetime_date_type):
        raise BodoError(jgjom__ual)
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
                y, lghm__mboa = lhs.year, rhs.year
                blqw__vuofl, ijrle__spvn = lhs.month, rhs.month
                d, sdof__dsm = lhs.day, rhs.day
                return op(_cmp((y, blqw__vuofl, d), (lghm__mboa,
                    ijrle__spvn, sdof__dsm)), 0)
            return impl
    return overload_date_cmp


def create_datetime_date_cmp_op_overload(op):

    def overload_cmp(lhs, rhs):
        hbx__uiz = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[op]} {rhs} is always {op == operator.ne} in Python. If this is unexpected there may be a bug in your code.'
            )
        warnings.warn(hbx__uiz, bodo.utils.typing.BodoWarning)
        if op == operator.eq:
            return lambda lhs, rhs: False
        elif op == operator.ne:
            return lambda lhs, rhs: True
    return overload_cmp


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            zta__twf = True
        else:
            zta__twf = False
        if lhs == datetime_date_array_type and rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                mtfm__kck = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for fov__hclwd in numba.parfors.parfor.internal_prange(n):
                    bozsn__wlb = bodo.libs.array_kernels.isna(lhs, fov__hclwd)
                    cqd__qddx = bodo.libs.array_kernels.isna(rhs, fov__hclwd)
                    if bozsn__wlb or cqd__qddx:
                        lha__ucfua = zta__twf
                    else:
                        lha__ucfua = op(lhs[fov__hclwd], rhs[fov__hclwd])
                    mtfm__kck[fov__hclwd] = lha__ucfua
                return mtfm__kck
            return impl
        elif lhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                mtfm__kck = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for fov__hclwd in numba.parfors.parfor.internal_prange(n):
                    eiqdf__ssxo = bodo.libs.array_kernels.isna(lhs, fov__hclwd)
                    if eiqdf__ssxo:
                        lha__ucfua = zta__twf
                    else:
                        lha__ucfua = op(lhs[fov__hclwd], rhs)
                    mtfm__kck[fov__hclwd] = lha__ucfua
                return mtfm__kck
            return impl
        elif rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                mtfm__kck = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for fov__hclwd in numba.parfors.parfor.internal_prange(n):
                    eiqdf__ssxo = bodo.libs.array_kernels.isna(rhs, fov__hclwd)
                    if eiqdf__ssxo:
                        lha__ucfua = zta__twf
                    else:
                        lha__ucfua = op(lhs, rhs[fov__hclwd])
                    mtfm__kck[fov__hclwd] = lha__ucfua
                return mtfm__kck
            return impl
    return overload_date_arr_cmp
