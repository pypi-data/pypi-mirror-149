"""
Implement support for the various classes in pd.tseries.offsets.
"""
import operator
import llvmlite.binding as ll
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.pd_timestamp_ext import get_days_in_month, pd_timestamp_type
from bodo.libs import hdatetime_ext
from bodo.utils.typing import BodoError, create_unsupported_overload, is_overload_none
ll.add_symbol('box_date_offset', hdatetime_ext.box_date_offset)
ll.add_symbol('unbox_date_offset', hdatetime_ext.unbox_date_offset)


class MonthBeginType(types.Type):

    def __init__(self):
        super(MonthBeginType, self).__init__(name='MonthBeginType()')


month_begin_type = MonthBeginType()


@typeof_impl.register(pd.tseries.offsets.MonthBegin)
def typeof_month_begin(val, c):
    return month_begin_type


@register_model(MonthBeginType)
class MonthBeginModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yihfn__vugb = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, yihfn__vugb)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    orq__ghec = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    vfo__jrn = c.pyapi.long_from_longlong(orq__ghec.n)
    iuq__kkajs = c.pyapi.from_native_value(types.boolean, orq__ghec.
        normalize, c.env_manager)
    nayzy__mvn = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    nwbu__dtow = c.pyapi.call_function_objargs(nayzy__mvn, (vfo__jrn,
        iuq__kkajs))
    c.pyapi.decref(vfo__jrn)
    c.pyapi.decref(iuq__kkajs)
    c.pyapi.decref(nayzy__mvn)
    return nwbu__dtow


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    vfo__jrn = c.pyapi.object_getattr_string(val, 'n')
    iuq__kkajs = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(vfo__jrn)
    normalize = c.pyapi.to_native_value(types.bool_, iuq__kkajs).value
    orq__ghec = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    orq__ghec.n = n
    orq__ghec.normalize = normalize
    c.pyapi.decref(vfo__jrn)
    c.pyapi.decref(iuq__kkajs)
    hek__glioq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(orq__ghec._getvalue(), is_error=hek__glioq)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        orq__ghec = cgutils.create_struct_proxy(typ)(context, builder)
        orq__ghec.n = args[0]
        orq__ghec.normalize = args[1]
        return orq__ghec._getvalue()
    return MonthBeginType()(n, normalize), codegen


make_attribute_wrapper(MonthBeginType, 'n', 'n')
make_attribute_wrapper(MonthBeginType, 'normalize', 'normalize')


@register_jitable
def calculate_month_begin_date(year, month, day, n):
    if n <= 0:
        if day > 1:
            n += 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = 1
    return year, month, day


def overload_add_operator_month_begin_offset_type(lhs, rhs):
    if lhs == month_begin_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_begin_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_begin_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_begin_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


class MonthEndType(types.Type):

    def __init__(self):
        super(MonthEndType, self).__init__(name='MonthEndType()')


month_end_type = MonthEndType()


@typeof_impl.register(pd.tseries.offsets.MonthEnd)
def typeof_month_end(val, c):
    return month_end_type


@register_model(MonthEndType)
class MonthEndModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yihfn__vugb = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, yihfn__vugb)


@box(MonthEndType)
def box_month_end(typ, val, c):
    qld__ynzad = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    vfo__jrn = c.pyapi.long_from_longlong(qld__ynzad.n)
    iuq__kkajs = c.pyapi.from_native_value(types.boolean, qld__ynzad.
        normalize, c.env_manager)
    sagd__oyt = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    nwbu__dtow = c.pyapi.call_function_objargs(sagd__oyt, (vfo__jrn,
        iuq__kkajs))
    c.pyapi.decref(vfo__jrn)
    c.pyapi.decref(iuq__kkajs)
    c.pyapi.decref(sagd__oyt)
    return nwbu__dtow


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    vfo__jrn = c.pyapi.object_getattr_string(val, 'n')
    iuq__kkajs = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(vfo__jrn)
    normalize = c.pyapi.to_native_value(types.bool_, iuq__kkajs).value
    qld__ynzad = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qld__ynzad.n = n
    qld__ynzad.normalize = normalize
    c.pyapi.decref(vfo__jrn)
    c.pyapi.decref(iuq__kkajs)
    hek__glioq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qld__ynzad._getvalue(), is_error=hek__glioq)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        qld__ynzad = cgutils.create_struct_proxy(typ)(context, builder)
        qld__ynzad.n = args[0]
        qld__ynzad.normalize = args[1]
        return qld__ynzad._getvalue()
    return MonthEndType()(n, normalize), codegen


make_attribute_wrapper(MonthEndType, 'n', 'n')
make_attribute_wrapper(MonthEndType, 'normalize', 'normalize')


@lower_constant(MonthBeginType)
@lower_constant(MonthEndType)
def lower_constant_month_end(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    return lir.Constant.literal_struct([n, normalize])


@register_jitable
def calculate_month_end_date(year, month, day, n):
    if n > 0:
        qld__ynzad = get_days_in_month(year, month)
        if qld__ynzad > day:
            n -= 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = get_days_in_month(year, month)
    return year, month, day


def overload_add_operator_month_end_offset_type(lhs, rhs):
    if lhs == month_end_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_end_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_end_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_end_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_mul_date_offset_types(lhs, rhs):
    if lhs == month_begin_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthBegin(lhs.n * rhs, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthEnd(lhs.n * rhs, lhs.normalize)
    if lhs == week_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.Week(lhs.n * rhs, lhs.normalize, lhs.
                weekday)
    if lhs == date_offset_type:

        def impl(lhs, rhs):
            n = lhs.n * rhs
            normalize = lhs.normalize
            nanoseconds = lhs._nanoseconds
            nanosecond = lhs._nanosecond
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize,
                    nanoseconds=nanoseconds, nanosecond=nanosecond)
    if rhs in [week_type, month_end_type, month_begin_type, date_offset_type]:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl
    return impl


class DateOffsetType(types.Type):

    def __init__(self):
        super(DateOffsetType, self).__init__(name='DateOffsetType()')


date_offset_type = DateOffsetType()
date_offset_fields = ['years', 'months', 'weeks', 'days', 'hours',
    'minutes', 'seconds', 'microseconds', 'nanoseconds', 'year', 'month',
    'day', 'weekday', 'hour', 'minute', 'second', 'microsecond', 'nanosecond']


@typeof_impl.register(pd.tseries.offsets.DateOffset)
def type_of_date_offset(val, c):
    return date_offset_type


@register_model(DateOffsetType)
class DateOffsetModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yihfn__vugb = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, yihfn__vugb)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    qepx__uhcd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    nduwz__cchn = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for bmm__lfc, cfqq__kgp in enumerate(date_offset_fields):
        c.builder.store(getattr(qepx__uhcd, cfqq__kgp), c.builder.inttoptr(
            c.builder.add(c.builder.ptrtoint(nduwz__cchn, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * bmm__lfc)), lir.IntType(64).
            as_pointer()))
    whbx__ecw = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    gde__ius = cgutils.get_or_insert_function(c.builder.module, whbx__ecw,
        name='box_date_offset')
    kkcl__erml = c.builder.call(gde__ius, [qepx__uhcd.n, qepx__uhcd.
        normalize, nduwz__cchn, qepx__uhcd.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return kkcl__erml


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    vfo__jrn = c.pyapi.object_getattr_string(val, 'n')
    iuq__kkajs = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(vfo__jrn)
    normalize = c.pyapi.to_native_value(types.bool_, iuq__kkajs).value
    nduwz__cchn = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    whbx__ecw = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64).as_pointer()])
    hgixn__duet = cgutils.get_or_insert_function(c.builder.module,
        whbx__ecw, name='unbox_date_offset')
    has_kws = c.builder.call(hgixn__duet, [val, nduwz__cchn])
    qepx__uhcd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qepx__uhcd.n = n
    qepx__uhcd.normalize = normalize
    for bmm__lfc, cfqq__kgp in enumerate(date_offset_fields):
        setattr(qepx__uhcd, cfqq__kgp, c.builder.load(c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(nduwz__cchn, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * bmm__lfc)), lir.IntType(64).
            as_pointer())))
    qepx__uhcd.has_kws = has_kws
    c.pyapi.decref(vfo__jrn)
    c.pyapi.decref(iuq__kkajs)
    hek__glioq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qepx__uhcd._getvalue(), is_error=hek__glioq)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    auoz__etijk = [n, normalize]
    has_kws = False
    myu__rhuac = [0] * 9 + [-1] * 9
    for bmm__lfc, cfqq__kgp in enumerate(date_offset_fields):
        if hasattr(pyval, cfqq__kgp):
            yvpc__mvnzz = context.get_constant(types.int64, getattr(pyval,
                cfqq__kgp))
            if cfqq__kgp != 'nanoseconds' and cfqq__kgp != 'nanosecond':
                has_kws = True
        else:
            yvpc__mvnzz = context.get_constant(types.int64, myu__rhuac[
                bmm__lfc])
        auoz__etijk.append(yvpc__mvnzz)
    has_kws = context.get_constant(types.boolean, has_kws)
    auoz__etijk.append(has_kws)
    return lir.Constant.literal_struct(auoz__etijk)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    mhbno__tczu = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for zvf__jykdy in mhbno__tczu:
        if not is_overload_none(zvf__jykdy):
            has_kws = True
            break

    def impl(n=1, normalize=False, years=None, months=None, weeks=None,
        days=None, hours=None, minutes=None, seconds=None, microseconds=
        None, nanoseconds=None, year=None, month=None, day=None, weekday=
        None, hour=None, minute=None, second=None, microsecond=None,
        nanosecond=None):
        years = 0 if years is None else years
        months = 0 if months is None else months
        weeks = 0 if weeks is None else weeks
        days = 0 if days is None else days
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        seconds = 0 if seconds is None else seconds
        microseconds = 0 if microseconds is None else microseconds
        nanoseconds = 0 if nanoseconds is None else nanoseconds
        year = -1 if year is None else year
        month = -1 if month is None else month
        weekday = -1 if weekday is None else weekday
        day = -1 if day is None else day
        hour = -1 if hour is None else hour
        minute = -1 if minute is None else minute
        second = -1 if second is None else second
        microsecond = -1 if microsecond is None else microsecond
        nanosecond = -1 if nanosecond is None else nanosecond
        return init_date_offset(n, normalize, years, months, weeks, days,
            hours, minutes, seconds, microseconds, nanoseconds, year, month,
            day, weekday, hour, minute, second, microsecond, nanosecond,
            has_kws)
    return impl


@intrinsic
def init_date_offset(typingctx, n, normalize, years, months, weeks, days,
    hours, minutes, seconds, microseconds, nanoseconds, year, month, day,
    weekday, hour, minute, second, microsecond, nanosecond, has_kws):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        qepx__uhcd = cgutils.create_struct_proxy(typ)(context, builder)
        qepx__uhcd.n = args[0]
        qepx__uhcd.normalize = args[1]
        qepx__uhcd.years = args[2]
        qepx__uhcd.months = args[3]
        qepx__uhcd.weeks = args[4]
        qepx__uhcd.days = args[5]
        qepx__uhcd.hours = args[6]
        qepx__uhcd.minutes = args[7]
        qepx__uhcd.seconds = args[8]
        qepx__uhcd.microseconds = args[9]
        qepx__uhcd.nanoseconds = args[10]
        qepx__uhcd.year = args[11]
        qepx__uhcd.month = args[12]
        qepx__uhcd.day = args[13]
        qepx__uhcd.weekday = args[14]
        qepx__uhcd.hour = args[15]
        qepx__uhcd.minute = args[16]
        qepx__uhcd.second = args[17]
        qepx__uhcd.microsecond = args[18]
        qepx__uhcd.nanosecond = args[19]
        qepx__uhcd.has_kws = args[20]
        return qepx__uhcd._getvalue()
    return DateOffsetType()(n, normalize, years, months, weeks, days, hours,
        minutes, seconds, microseconds, nanoseconds, year, month, day,
        weekday, hour, minute, second, microsecond, nanosecond, has_kws
        ), codegen


make_attribute_wrapper(DateOffsetType, 'n', 'n')
make_attribute_wrapper(DateOffsetType, 'normalize', 'normalize')
make_attribute_wrapper(DateOffsetType, 'years', '_years')
make_attribute_wrapper(DateOffsetType, 'months', '_months')
make_attribute_wrapper(DateOffsetType, 'weeks', '_weeks')
make_attribute_wrapper(DateOffsetType, 'days', '_days')
make_attribute_wrapper(DateOffsetType, 'hours', '_hours')
make_attribute_wrapper(DateOffsetType, 'minutes', '_minutes')
make_attribute_wrapper(DateOffsetType, 'seconds', '_seconds')
make_attribute_wrapper(DateOffsetType, 'microseconds', '_microseconds')
make_attribute_wrapper(DateOffsetType, 'nanoseconds', '_nanoseconds')
make_attribute_wrapper(DateOffsetType, 'year', '_year')
make_attribute_wrapper(DateOffsetType, 'month', '_month')
make_attribute_wrapper(DateOffsetType, 'weekday', '_weekday')
make_attribute_wrapper(DateOffsetType, 'day', '_day')
make_attribute_wrapper(DateOffsetType, 'hour', '_hour')
make_attribute_wrapper(DateOffsetType, 'minute', '_minute')
make_attribute_wrapper(DateOffsetType, 'second', '_second')
make_attribute_wrapper(DateOffsetType, 'microsecond', '_microsecond')
make_attribute_wrapper(DateOffsetType, 'nanosecond', '_nanosecond')
make_attribute_wrapper(DateOffsetType, 'has_kws', '_has_kws')


@register_jitable
def relative_delta_addition(dateoffset, ts):
    if dateoffset._has_kws:
        wnoj__ghlf = -1 if dateoffset.n < 0 else 1
        for gffi__pcw in range(np.abs(dateoffset.n)):
            year = ts.year
            month = ts.month
            day = ts.day
            hour = ts.hour
            minute = ts.minute
            second = ts.second
            microsecond = ts.microsecond
            nanosecond = ts.nanosecond
            if dateoffset._year != -1:
                year = dateoffset._year
            year += wnoj__ghlf * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += wnoj__ghlf * dateoffset._months
            year, month, vtj__ggcmh = calculate_month_end_date(year, month,
                day, 0)
            if day > vtj__ggcmh:
                day = vtj__ggcmh
            if dateoffset._day != -1:
                day = dateoffset._day
            if dateoffset._hour != -1:
                hour = dateoffset._hour
            if dateoffset._minute != -1:
                minute = dateoffset._minute
            if dateoffset._second != -1:
                second = dateoffset._second
            if dateoffset._microsecond != -1:
                microsecond = dateoffset._microsecond
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour,
                minute=minute, second=second, microsecond=microsecond,
                nanosecond=nanosecond)
            log__pah = pd.Timedelta(days=dateoffset._days + 7 * dateoffset.
                _weeks, hours=dateoffset._hours, minutes=dateoffset.
                _minutes, seconds=dateoffset._seconds, microseconds=
                dateoffset._microseconds)
            if wnoj__ghlf == -1:
                log__pah = -log__pah
            ts = ts + log__pah
            if dateoffset._weekday != -1:
                lzk__ldzty = ts.weekday()
                hzo__dguk = (dateoffset._weekday - lzk__ldzty) % 7
                ts = ts + pd.Timedelta(days=hzo__dguk)
        return ts
    else:
        return pd.Timedelta(days=dateoffset.n) + ts


def overload_add_operator_date_offset_type(lhs, rhs):
    if lhs == date_offset_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, rhs)
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs == date_offset_type and rhs in [datetime_date_type,
        datetime_datetime_type]:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, pd.Timestamp(rhs))
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == date_offset_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_sub_operator_offsets(lhs, rhs):
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs in [date_offset_type, month_begin_type, month_end_type,
        week_type]:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


@overload(operator.neg, no_unliteral=True)
def overload_neg(lhs):
    if lhs == month_begin_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthBegin(-lhs.n, lhs.normalize)
    elif lhs == month_end_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthEnd(-lhs.n, lhs.normalize)
    elif lhs == week_type:

        def impl(lhs):
            return pd.tseries.offsets.Week(-lhs.n, lhs.normalize, lhs.weekday)
    elif lhs == date_offset_type:

        def impl(lhs):
            n = -lhs.n
            normalize = lhs.normalize
            nanoseconds = lhs._nanoseconds
            nanosecond = lhs._nanosecond
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize,
                    nanoseconds=nanoseconds, nanosecond=nanosecond)
    else:
        return
    return impl


def is_offsets_type(val):
    return val in [date_offset_type, month_begin_type, month_end_type,
        week_type]


class WeekType(types.Type):

    def __init__(self):
        super(WeekType, self).__init__(name='WeekType()')


week_type = WeekType()


@typeof_impl.register(pd.tseries.offsets.Week)
def typeof_week(val, c):
    return week_type


@register_model(WeekType)
class WeekModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yihfn__vugb = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, yihfn__vugb)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        pehs__gqjmg = -1 if weekday is None else weekday
        return init_week(n, normalize, pehs__gqjmg)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        wgqp__xlcj = cgutils.create_struct_proxy(typ)(context, builder)
        wgqp__xlcj.n = args[0]
        wgqp__xlcj.normalize = args[1]
        wgqp__xlcj.weekday = args[2]
        return wgqp__xlcj._getvalue()
    return WeekType()(n, normalize, weekday), codegen


@lower_constant(WeekType)
def lower_constant_week(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    if pyval.weekday is not None:
        weekday = context.get_constant(types.int64, pyval.weekday)
    else:
        weekday = context.get_constant(types.int64, -1)
    return lir.Constant.literal_struct([n, normalize, weekday])


@box(WeekType)
def box_week(typ, val, c):
    wgqp__xlcj = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    vfo__jrn = c.pyapi.long_from_longlong(wgqp__xlcj.n)
    iuq__kkajs = c.pyapi.from_native_value(types.boolean, wgqp__xlcj.
        normalize, c.env_manager)
    xdw__yxg = c.pyapi.long_from_longlong(wgqp__xlcj.weekday)
    mqru__ybe = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    pmyu__vfc = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -
        1), wgqp__xlcj.weekday)
    with c.builder.if_else(pmyu__vfc) as (syv__phvly, reu__owcly):
        with syv__phvly:
            nurrv__ywexq = c.pyapi.call_function_objargs(mqru__ybe, (
                vfo__jrn, iuq__kkajs, xdw__yxg))
            tys__hrk = c.builder.block
        with reu__owcly:
            qolc__sxw = c.pyapi.call_function_objargs(mqru__ybe, (vfo__jrn,
                iuq__kkajs))
            chbg__zdu = c.builder.block
    nwbu__dtow = c.builder.phi(nurrv__ywexq.type)
    nwbu__dtow.add_incoming(nurrv__ywexq, tys__hrk)
    nwbu__dtow.add_incoming(qolc__sxw, chbg__zdu)
    c.pyapi.decref(xdw__yxg)
    c.pyapi.decref(vfo__jrn)
    c.pyapi.decref(iuq__kkajs)
    c.pyapi.decref(mqru__ybe)
    return nwbu__dtow


@unbox(WeekType)
def unbox_week(typ, val, c):
    vfo__jrn = c.pyapi.object_getattr_string(val, 'n')
    iuq__kkajs = c.pyapi.object_getattr_string(val, 'normalize')
    xdw__yxg = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(vfo__jrn)
    normalize = c.pyapi.to_native_value(types.bool_, iuq__kkajs).value
    tpfmz__udws = c.pyapi.make_none()
    ray__eelz = c.builder.icmp_unsigned('==', xdw__yxg, tpfmz__udws)
    with c.builder.if_else(ray__eelz) as (reu__owcly, syv__phvly):
        with syv__phvly:
            nurrv__ywexq = c.pyapi.long_as_longlong(xdw__yxg)
            tys__hrk = c.builder.block
        with reu__owcly:
            qolc__sxw = lir.Constant(lir.IntType(64), -1)
            chbg__zdu = c.builder.block
    nwbu__dtow = c.builder.phi(nurrv__ywexq.type)
    nwbu__dtow.add_incoming(nurrv__ywexq, tys__hrk)
    nwbu__dtow.add_incoming(qolc__sxw, chbg__zdu)
    wgqp__xlcj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    wgqp__xlcj.n = n
    wgqp__xlcj.normalize = normalize
    wgqp__xlcj.weekday = nwbu__dtow
    c.pyapi.decref(vfo__jrn)
    c.pyapi.decref(iuq__kkajs)
    c.pyapi.decref(xdw__yxg)
    hek__glioq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wgqp__xlcj._getvalue(), is_error=hek__glioq)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            hsn__xim = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                xav__wii = pd.Timestamp(year=rhs.year, month=rhs.month, day
                    =rhs.day)
            else:
                xav__wii = rhs
            return xav__wii + hsn__xim
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            hsn__xim = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                xav__wii = pd.Timestamp(year=rhs.year, month=rhs.month, day
                    =rhs.day)
            else:
                xav__wii = pd.Timestamp(year=rhs.year, month=rhs.month, day
                    =rhs.day, hour=rhs.hour, minute=rhs.minute, second=rhs.
                    second, microsecond=rhs.microsecond)
            return xav__wii + hsn__xim
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            hsn__xim = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            return rhs + hsn__xim
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == week_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


@register_jitable
def calculate_week_date(n, weekday, other_weekday):
    if weekday == -1:
        return pd.Timedelta(weeks=n)
    if weekday != other_weekday:
        vhko__ajng = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=vhko__ajng)


date_offset_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
date_offset_unsupported = {'__call__', 'rollback', 'rollforward',
    'is_month_start', 'is_month_end', 'apply', 'apply_index', 'copy',
    'isAnchored', 'onOffset', 'is_anchored', 'is_on_offset',
    'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end'}
month_end_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_end_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
month_begin_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_begin_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
week_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos', 'rule_code'}
week_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
offsets_unsupported = {pd.tseries.offsets.BusinessDay, pd.tseries.offsets.
    BDay, pd.tseries.offsets.BusinessHour, pd.tseries.offsets.
    CustomBusinessDay, pd.tseries.offsets.CDay, pd.tseries.offsets.
    CustomBusinessHour, pd.tseries.offsets.BusinessMonthEnd, pd.tseries.
    offsets.BMonthEnd, pd.tseries.offsets.BusinessMonthBegin, pd.tseries.
    offsets.BMonthBegin, pd.tseries.offsets.CustomBusinessMonthEnd, pd.
    tseries.offsets.CBMonthEnd, pd.tseries.offsets.CustomBusinessMonthBegin,
    pd.tseries.offsets.CBMonthBegin, pd.tseries.offsets.SemiMonthEnd, pd.
    tseries.offsets.SemiMonthBegin, pd.tseries.offsets.WeekOfMonth, pd.
    tseries.offsets.LastWeekOfMonth, pd.tseries.offsets.BQuarterEnd, pd.
    tseries.offsets.BQuarterBegin, pd.tseries.offsets.QuarterEnd, pd.
    tseries.offsets.QuarterBegin, pd.tseries.offsets.BYearEnd, pd.tseries.
    offsets.BYearBegin, pd.tseries.offsets.YearEnd, pd.tseries.offsets.
    YearBegin, pd.tseries.offsets.FY5253, pd.tseries.offsets.FY5253Quarter,
    pd.tseries.offsets.Easter, pd.tseries.offsets.Tick, pd.tseries.offsets.
    Day, pd.tseries.offsets.Hour, pd.tseries.offsets.Minute, pd.tseries.
    offsets.Second, pd.tseries.offsets.Milli, pd.tseries.offsets.Micro, pd.
    tseries.offsets.Nano}
frequencies_unsupported = {pd.tseries.frequencies.to_offset}


def _install_date_offsets_unsupported():
    for ibb__foqhr in date_offset_unsupported_attrs:
        comu__mxo = 'pandas.tseries.offsets.DateOffset.' + ibb__foqhr
        overload_attribute(DateOffsetType, ibb__foqhr)(
            create_unsupported_overload(comu__mxo))
    for ibb__foqhr in date_offset_unsupported:
        comu__mxo = 'pandas.tseries.offsets.DateOffset.' + ibb__foqhr
        overload_method(DateOffsetType, ibb__foqhr)(create_unsupported_overload
            (comu__mxo))


def _install_month_begin_unsupported():
    for ibb__foqhr in month_begin_unsupported_attrs:
        comu__mxo = 'pandas.tseries.offsets.MonthBegin.' + ibb__foqhr
        overload_attribute(MonthBeginType, ibb__foqhr)(
            create_unsupported_overload(comu__mxo))
    for ibb__foqhr in month_begin_unsupported:
        comu__mxo = 'pandas.tseries.offsets.MonthBegin.' + ibb__foqhr
        overload_method(MonthBeginType, ibb__foqhr)(create_unsupported_overload
            (comu__mxo))


def _install_month_end_unsupported():
    for ibb__foqhr in date_offset_unsupported_attrs:
        comu__mxo = 'pandas.tseries.offsets.MonthEnd.' + ibb__foqhr
        overload_attribute(MonthEndType, ibb__foqhr)(
            create_unsupported_overload(comu__mxo))
    for ibb__foqhr in date_offset_unsupported:
        comu__mxo = 'pandas.tseries.offsets.MonthEnd.' + ibb__foqhr
        overload_method(MonthEndType, ibb__foqhr)(create_unsupported_overload
            (comu__mxo))


def _install_week_unsupported():
    for ibb__foqhr in week_unsupported_attrs:
        comu__mxo = 'pandas.tseries.offsets.Week.' + ibb__foqhr
        overload_attribute(WeekType, ibb__foqhr)(create_unsupported_overload
            (comu__mxo))
    for ibb__foqhr in week_unsupported:
        comu__mxo = 'pandas.tseries.offsets.Week.' + ibb__foqhr
        overload_method(WeekType, ibb__foqhr)(create_unsupported_overload(
            comu__mxo))


def _install_offsets_unsupported():
    for yvpc__mvnzz in offsets_unsupported:
        comu__mxo = 'pandas.tseries.offsets.' + yvpc__mvnzz.__name__
        overload(yvpc__mvnzz)(create_unsupported_overload(comu__mxo))


def _install_frequencies_unsupported():
    for yvpc__mvnzz in frequencies_unsupported:
        comu__mxo = 'pandas.tseries.frequencies.' + yvpc__mvnzz.__name__
        overload(yvpc__mvnzz)(create_unsupported_overload(comu__mxo))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
