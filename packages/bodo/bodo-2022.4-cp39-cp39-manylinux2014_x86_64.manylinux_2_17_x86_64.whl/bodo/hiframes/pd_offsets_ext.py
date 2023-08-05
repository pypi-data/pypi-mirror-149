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
        hwhnw__xfcsf = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, hwhnw__xfcsf)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    snv__tua = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    jov__gqhm = c.pyapi.long_from_longlong(snv__tua.n)
    ikd__lodni = c.pyapi.from_native_value(types.boolean, snv__tua.
        normalize, c.env_manager)
    ink__fzbm = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    xcmj__urw = c.pyapi.call_function_objargs(ink__fzbm, (jov__gqhm,
        ikd__lodni))
    c.pyapi.decref(jov__gqhm)
    c.pyapi.decref(ikd__lodni)
    c.pyapi.decref(ink__fzbm)
    return xcmj__urw


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    jov__gqhm = c.pyapi.object_getattr_string(val, 'n')
    ikd__lodni = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(jov__gqhm)
    normalize = c.pyapi.to_native_value(types.bool_, ikd__lodni).value
    snv__tua = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    snv__tua.n = n
    snv__tua.normalize = normalize
    c.pyapi.decref(jov__gqhm)
    c.pyapi.decref(ikd__lodni)
    nkzv__hlc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(snv__tua._getvalue(), is_error=nkzv__hlc)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        snv__tua = cgutils.create_struct_proxy(typ)(context, builder)
        snv__tua.n = args[0]
        snv__tua.normalize = args[1]
        return snv__tua._getvalue()
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
        hwhnw__xfcsf = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, hwhnw__xfcsf)


@box(MonthEndType)
def box_month_end(typ, val, c):
    iuxuu__abv = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jov__gqhm = c.pyapi.long_from_longlong(iuxuu__abv.n)
    ikd__lodni = c.pyapi.from_native_value(types.boolean, iuxuu__abv.
        normalize, c.env_manager)
    cqxbz__eaz = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    xcmj__urw = c.pyapi.call_function_objargs(cqxbz__eaz, (jov__gqhm,
        ikd__lodni))
    c.pyapi.decref(jov__gqhm)
    c.pyapi.decref(ikd__lodni)
    c.pyapi.decref(cqxbz__eaz)
    return xcmj__urw


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    jov__gqhm = c.pyapi.object_getattr_string(val, 'n')
    ikd__lodni = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(jov__gqhm)
    normalize = c.pyapi.to_native_value(types.bool_, ikd__lodni).value
    iuxuu__abv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    iuxuu__abv.n = n
    iuxuu__abv.normalize = normalize
    c.pyapi.decref(jov__gqhm)
    c.pyapi.decref(ikd__lodni)
    nkzv__hlc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(iuxuu__abv._getvalue(), is_error=nkzv__hlc)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        iuxuu__abv = cgutils.create_struct_proxy(typ)(context, builder)
        iuxuu__abv.n = args[0]
        iuxuu__abv.normalize = args[1]
        return iuxuu__abv._getvalue()
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
        iuxuu__abv = get_days_in_month(year, month)
        if iuxuu__abv > day:
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
        hwhnw__xfcsf = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, hwhnw__xfcsf)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    wndn__eov = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    neekh__svq = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for syqj__kocua, yhz__jgc in enumerate(date_offset_fields):
        c.builder.store(getattr(wndn__eov, yhz__jgc), c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(neekh__svq, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * syqj__kocua)), lir.IntType(64
            ).as_pointer()))
    tof__lve = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    wpfzp__lqkpk = cgutils.get_or_insert_function(c.builder.module,
        tof__lve, name='box_date_offset')
    qvnik__who = c.builder.call(wpfzp__lqkpk, [wndn__eov.n, wndn__eov.
        normalize, neekh__svq, wndn__eov.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return qvnik__who


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    jov__gqhm = c.pyapi.object_getattr_string(val, 'n')
    ikd__lodni = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(jov__gqhm)
    normalize = c.pyapi.to_native_value(types.bool_, ikd__lodni).value
    neekh__svq = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    tof__lve = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer(
        ), lir.IntType(64).as_pointer()])
    ckj__uigy = cgutils.get_or_insert_function(c.builder.module, tof__lve,
        name='unbox_date_offset')
    has_kws = c.builder.call(ckj__uigy, [val, neekh__svq])
    wndn__eov = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    wndn__eov.n = n
    wndn__eov.normalize = normalize
    for syqj__kocua, yhz__jgc in enumerate(date_offset_fields):
        setattr(wndn__eov, yhz__jgc, c.builder.load(c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(neekh__svq, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * syqj__kocua)), lir.IntType(64
            ).as_pointer())))
    wndn__eov.has_kws = has_kws
    c.pyapi.decref(jov__gqhm)
    c.pyapi.decref(ikd__lodni)
    nkzv__hlc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wndn__eov._getvalue(), is_error=nkzv__hlc)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    vid__mar = [n, normalize]
    has_kws = False
    hxktd__hkhpw = [0] * 9 + [-1] * 9
    for syqj__kocua, yhz__jgc in enumerate(date_offset_fields):
        if hasattr(pyval, yhz__jgc):
            ajy__asuok = context.get_constant(types.int64, getattr(pyval,
                yhz__jgc))
            if yhz__jgc != 'nanoseconds' and yhz__jgc != 'nanosecond':
                has_kws = True
        else:
            ajy__asuok = context.get_constant(types.int64, hxktd__hkhpw[
                syqj__kocua])
        vid__mar.append(ajy__asuok)
    has_kws = context.get_constant(types.boolean, has_kws)
    vid__mar.append(has_kws)
    return lir.Constant.literal_struct(vid__mar)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    xswh__sopmb = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for lrf__zem in xswh__sopmb:
        if not is_overload_none(lrf__zem):
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
        wndn__eov = cgutils.create_struct_proxy(typ)(context, builder)
        wndn__eov.n = args[0]
        wndn__eov.normalize = args[1]
        wndn__eov.years = args[2]
        wndn__eov.months = args[3]
        wndn__eov.weeks = args[4]
        wndn__eov.days = args[5]
        wndn__eov.hours = args[6]
        wndn__eov.minutes = args[7]
        wndn__eov.seconds = args[8]
        wndn__eov.microseconds = args[9]
        wndn__eov.nanoseconds = args[10]
        wndn__eov.year = args[11]
        wndn__eov.month = args[12]
        wndn__eov.day = args[13]
        wndn__eov.weekday = args[14]
        wndn__eov.hour = args[15]
        wndn__eov.minute = args[16]
        wndn__eov.second = args[17]
        wndn__eov.microsecond = args[18]
        wndn__eov.nanosecond = args[19]
        wndn__eov.has_kws = args[20]
        return wndn__eov._getvalue()
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
        buii__ulkvg = -1 if dateoffset.n < 0 else 1
        for wvsy__liwi in range(np.abs(dateoffset.n)):
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
            year += buii__ulkvg * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += buii__ulkvg * dateoffset._months
            year, month, pjliz__acfok = calculate_month_end_date(year,
                month, day, 0)
            if day > pjliz__acfok:
                day = pjliz__acfok
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
            gke__drhlf = pd.Timedelta(days=dateoffset._days + 7 *
                dateoffset._weeks, hours=dateoffset._hours, minutes=
                dateoffset._minutes, seconds=dateoffset._seconds,
                microseconds=dateoffset._microseconds)
            if buii__ulkvg == -1:
                gke__drhlf = -gke__drhlf
            ts = ts + gke__drhlf
            if dateoffset._weekday != -1:
                qzulm__kxfjw = ts.weekday()
                ttxl__pxw = (dateoffset._weekday - qzulm__kxfjw) % 7
                ts = ts + pd.Timedelta(days=ttxl__pxw)
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
        hwhnw__xfcsf = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, hwhnw__xfcsf)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        crf__oihyk = -1 if weekday is None else weekday
        return init_week(n, normalize, crf__oihyk)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        eayw__yedkj = cgutils.create_struct_proxy(typ)(context, builder)
        eayw__yedkj.n = args[0]
        eayw__yedkj.normalize = args[1]
        eayw__yedkj.weekday = args[2]
        return eayw__yedkj._getvalue()
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
    eayw__yedkj = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jov__gqhm = c.pyapi.long_from_longlong(eayw__yedkj.n)
    ikd__lodni = c.pyapi.from_native_value(types.boolean, eayw__yedkj.
        normalize, c.env_manager)
    taew__drknk = c.pyapi.long_from_longlong(eayw__yedkj.weekday)
    gtgyz__sxkq = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    xyf__kgbi = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -
        1), eayw__yedkj.weekday)
    with c.builder.if_else(xyf__kgbi) as (tekk__zfwvb, gjbi__unnd):
        with tekk__zfwvb:
            pqhv__mubnj = c.pyapi.call_function_objargs(gtgyz__sxkq, (
                jov__gqhm, ikd__lodni, taew__drknk))
            rcsq__rhpe = c.builder.block
        with gjbi__unnd:
            uzg__lalb = c.pyapi.call_function_objargs(gtgyz__sxkq, (
                jov__gqhm, ikd__lodni))
            qykmw__gwvo = c.builder.block
    xcmj__urw = c.builder.phi(pqhv__mubnj.type)
    xcmj__urw.add_incoming(pqhv__mubnj, rcsq__rhpe)
    xcmj__urw.add_incoming(uzg__lalb, qykmw__gwvo)
    c.pyapi.decref(taew__drknk)
    c.pyapi.decref(jov__gqhm)
    c.pyapi.decref(ikd__lodni)
    c.pyapi.decref(gtgyz__sxkq)
    return xcmj__urw


@unbox(WeekType)
def unbox_week(typ, val, c):
    jov__gqhm = c.pyapi.object_getattr_string(val, 'n')
    ikd__lodni = c.pyapi.object_getattr_string(val, 'normalize')
    taew__drknk = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(jov__gqhm)
    normalize = c.pyapi.to_native_value(types.bool_, ikd__lodni).value
    bkehn__eoss = c.pyapi.make_none()
    vrib__lxlmi = c.builder.icmp_unsigned('==', taew__drknk, bkehn__eoss)
    with c.builder.if_else(vrib__lxlmi) as (gjbi__unnd, tekk__zfwvb):
        with tekk__zfwvb:
            pqhv__mubnj = c.pyapi.long_as_longlong(taew__drknk)
            rcsq__rhpe = c.builder.block
        with gjbi__unnd:
            uzg__lalb = lir.Constant(lir.IntType(64), -1)
            qykmw__gwvo = c.builder.block
    xcmj__urw = c.builder.phi(pqhv__mubnj.type)
    xcmj__urw.add_incoming(pqhv__mubnj, rcsq__rhpe)
    xcmj__urw.add_incoming(uzg__lalb, qykmw__gwvo)
    eayw__yedkj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    eayw__yedkj.n = n
    eayw__yedkj.normalize = normalize
    eayw__yedkj.weekday = xcmj__urw
    c.pyapi.decref(jov__gqhm)
    c.pyapi.decref(ikd__lodni)
    c.pyapi.decref(taew__drknk)
    nkzv__hlc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(eayw__yedkj._getvalue(), is_error=nkzv__hlc)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            fgfc__myqtv = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                syjlf__nddwa = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                syjlf__nddwa = rhs
            return syjlf__nddwa + fgfc__myqtv
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            fgfc__myqtv = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                syjlf__nddwa = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                syjlf__nddwa = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return syjlf__nddwa + fgfc__myqtv
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            fgfc__myqtv = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            return rhs + fgfc__myqtv
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
        jrjut__kay = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=jrjut__kay)


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
    for cbx__mmint in date_offset_unsupported_attrs:
        fmxh__zindb = 'pandas.tseries.offsets.DateOffset.' + cbx__mmint
        overload_attribute(DateOffsetType, cbx__mmint)(
            create_unsupported_overload(fmxh__zindb))
    for cbx__mmint in date_offset_unsupported:
        fmxh__zindb = 'pandas.tseries.offsets.DateOffset.' + cbx__mmint
        overload_method(DateOffsetType, cbx__mmint)(create_unsupported_overload
            (fmxh__zindb))


def _install_month_begin_unsupported():
    for cbx__mmint in month_begin_unsupported_attrs:
        fmxh__zindb = 'pandas.tseries.offsets.MonthBegin.' + cbx__mmint
        overload_attribute(MonthBeginType, cbx__mmint)(
            create_unsupported_overload(fmxh__zindb))
    for cbx__mmint in month_begin_unsupported:
        fmxh__zindb = 'pandas.tseries.offsets.MonthBegin.' + cbx__mmint
        overload_method(MonthBeginType, cbx__mmint)(create_unsupported_overload
            (fmxh__zindb))


def _install_month_end_unsupported():
    for cbx__mmint in date_offset_unsupported_attrs:
        fmxh__zindb = 'pandas.tseries.offsets.MonthEnd.' + cbx__mmint
        overload_attribute(MonthEndType, cbx__mmint)(
            create_unsupported_overload(fmxh__zindb))
    for cbx__mmint in date_offset_unsupported:
        fmxh__zindb = 'pandas.tseries.offsets.MonthEnd.' + cbx__mmint
        overload_method(MonthEndType, cbx__mmint)(create_unsupported_overload
            (fmxh__zindb))


def _install_week_unsupported():
    for cbx__mmint in week_unsupported_attrs:
        fmxh__zindb = 'pandas.tseries.offsets.Week.' + cbx__mmint
        overload_attribute(WeekType, cbx__mmint)(create_unsupported_overload
            (fmxh__zindb))
    for cbx__mmint in week_unsupported:
        fmxh__zindb = 'pandas.tseries.offsets.Week.' + cbx__mmint
        overload_method(WeekType, cbx__mmint)(create_unsupported_overload(
            fmxh__zindb))


def _install_offsets_unsupported():
    for ajy__asuok in offsets_unsupported:
        fmxh__zindb = 'pandas.tseries.offsets.' + ajy__asuok.__name__
        overload(ajy__asuok)(create_unsupported_overload(fmxh__zindb))


def _install_frequencies_unsupported():
    for ajy__asuok in frequencies_unsupported:
        fmxh__zindb = 'pandas.tseries.frequencies.' + ajy__asuok.__name__
        overload(ajy__asuok)(create_unsupported_overload(fmxh__zindb))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
