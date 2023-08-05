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
        scbwh__zaehl = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, scbwh__zaehl)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    tvdm__uyvy = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    sui__uqadh = c.pyapi.long_from_longlong(tvdm__uyvy.n)
    fged__tdmpt = c.pyapi.from_native_value(types.boolean, tvdm__uyvy.
        normalize, c.env_manager)
    skrc__gln = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    vxwfi__jhu = c.pyapi.call_function_objargs(skrc__gln, (sui__uqadh,
        fged__tdmpt))
    c.pyapi.decref(sui__uqadh)
    c.pyapi.decref(fged__tdmpt)
    c.pyapi.decref(skrc__gln)
    return vxwfi__jhu


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    sui__uqadh = c.pyapi.object_getattr_string(val, 'n')
    fged__tdmpt = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(sui__uqadh)
    normalize = c.pyapi.to_native_value(types.bool_, fged__tdmpt).value
    tvdm__uyvy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tvdm__uyvy.n = n
    tvdm__uyvy.normalize = normalize
    c.pyapi.decref(sui__uqadh)
    c.pyapi.decref(fged__tdmpt)
    qkfk__ptru = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(tvdm__uyvy._getvalue(), is_error=qkfk__ptru)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        tvdm__uyvy = cgutils.create_struct_proxy(typ)(context, builder)
        tvdm__uyvy.n = args[0]
        tvdm__uyvy.normalize = args[1]
        return tvdm__uyvy._getvalue()
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
        scbwh__zaehl = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, scbwh__zaehl)


@box(MonthEndType)
def box_month_end(typ, val, c):
    hzzj__cwc = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    sui__uqadh = c.pyapi.long_from_longlong(hzzj__cwc.n)
    fged__tdmpt = c.pyapi.from_native_value(types.boolean, hzzj__cwc.
        normalize, c.env_manager)
    kdi__qrkgz = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    vxwfi__jhu = c.pyapi.call_function_objargs(kdi__qrkgz, (sui__uqadh,
        fged__tdmpt))
    c.pyapi.decref(sui__uqadh)
    c.pyapi.decref(fged__tdmpt)
    c.pyapi.decref(kdi__qrkgz)
    return vxwfi__jhu


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    sui__uqadh = c.pyapi.object_getattr_string(val, 'n')
    fged__tdmpt = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(sui__uqadh)
    normalize = c.pyapi.to_native_value(types.bool_, fged__tdmpt).value
    hzzj__cwc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hzzj__cwc.n = n
    hzzj__cwc.normalize = normalize
    c.pyapi.decref(sui__uqadh)
    c.pyapi.decref(fged__tdmpt)
    qkfk__ptru = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hzzj__cwc._getvalue(), is_error=qkfk__ptru)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        hzzj__cwc = cgutils.create_struct_proxy(typ)(context, builder)
        hzzj__cwc.n = args[0]
        hzzj__cwc.normalize = args[1]
        return hzzj__cwc._getvalue()
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
        hzzj__cwc = get_days_in_month(year, month)
        if hzzj__cwc > day:
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
        scbwh__zaehl = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, scbwh__zaehl)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    sflal__yoo = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    nxiwh__jrk = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for awbmf__bcbs, aayh__zdr in enumerate(date_offset_fields):
        c.builder.store(getattr(sflal__yoo, aayh__zdr), c.builder.inttoptr(
            c.builder.add(c.builder.ptrtoint(nxiwh__jrk, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * awbmf__bcbs)), lir.IntType(64
            ).as_pointer()))
    yzmcy__dxcz = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    aox__frqx = cgutils.get_or_insert_function(c.builder.module,
        yzmcy__dxcz, name='box_date_offset')
    aav__rmb = c.builder.call(aox__frqx, [sflal__yoo.n, sflal__yoo.
        normalize, nxiwh__jrk, sflal__yoo.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return aav__rmb


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    sui__uqadh = c.pyapi.object_getattr_string(val, 'n')
    fged__tdmpt = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(sui__uqadh)
    normalize = c.pyapi.to_native_value(types.bool_, fged__tdmpt).value
    nxiwh__jrk = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    yzmcy__dxcz = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    ovxu__lyk = cgutils.get_or_insert_function(c.builder.module,
        yzmcy__dxcz, name='unbox_date_offset')
    has_kws = c.builder.call(ovxu__lyk, [val, nxiwh__jrk])
    sflal__yoo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    sflal__yoo.n = n
    sflal__yoo.normalize = normalize
    for awbmf__bcbs, aayh__zdr in enumerate(date_offset_fields):
        setattr(sflal__yoo, aayh__zdr, c.builder.load(c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(nxiwh__jrk, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * awbmf__bcbs)), lir.IntType(64
            ).as_pointer())))
    sflal__yoo.has_kws = has_kws
    c.pyapi.decref(sui__uqadh)
    c.pyapi.decref(fged__tdmpt)
    qkfk__ptru = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(sflal__yoo._getvalue(), is_error=qkfk__ptru)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    jda__yyvt = [n, normalize]
    has_kws = False
    bbvhd__halu = [0] * 9 + [-1] * 9
    for awbmf__bcbs, aayh__zdr in enumerate(date_offset_fields):
        if hasattr(pyval, aayh__zdr):
            xepu__woip = context.get_constant(types.int64, getattr(pyval,
                aayh__zdr))
            if aayh__zdr != 'nanoseconds' and aayh__zdr != 'nanosecond':
                has_kws = True
        else:
            xepu__woip = context.get_constant(types.int64, bbvhd__halu[
                awbmf__bcbs])
        jda__yyvt.append(xepu__woip)
    has_kws = context.get_constant(types.boolean, has_kws)
    jda__yyvt.append(has_kws)
    return lir.Constant.literal_struct(jda__yyvt)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    lxkiq__nbit = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for zceu__dly in lxkiq__nbit:
        if not is_overload_none(zceu__dly):
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
        sflal__yoo = cgutils.create_struct_proxy(typ)(context, builder)
        sflal__yoo.n = args[0]
        sflal__yoo.normalize = args[1]
        sflal__yoo.years = args[2]
        sflal__yoo.months = args[3]
        sflal__yoo.weeks = args[4]
        sflal__yoo.days = args[5]
        sflal__yoo.hours = args[6]
        sflal__yoo.minutes = args[7]
        sflal__yoo.seconds = args[8]
        sflal__yoo.microseconds = args[9]
        sflal__yoo.nanoseconds = args[10]
        sflal__yoo.year = args[11]
        sflal__yoo.month = args[12]
        sflal__yoo.day = args[13]
        sflal__yoo.weekday = args[14]
        sflal__yoo.hour = args[15]
        sflal__yoo.minute = args[16]
        sflal__yoo.second = args[17]
        sflal__yoo.microsecond = args[18]
        sflal__yoo.nanosecond = args[19]
        sflal__yoo.has_kws = args[20]
        return sflal__yoo._getvalue()
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
        jins__ier = -1 if dateoffset.n < 0 else 1
        for dafvv__frms in range(np.abs(dateoffset.n)):
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
            year += jins__ier * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += jins__ier * dateoffset._months
            year, month, pcc__hjkfo = calculate_month_end_date(year, month,
                day, 0)
            if day > pcc__hjkfo:
                day = pcc__hjkfo
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
            csc__lnb = pd.Timedelta(days=dateoffset._days + 7 * dateoffset.
                _weeks, hours=dateoffset._hours, minutes=dateoffset.
                _minutes, seconds=dateoffset._seconds, microseconds=
                dateoffset._microseconds)
            if jins__ier == -1:
                csc__lnb = -csc__lnb
            ts = ts + csc__lnb
            if dateoffset._weekday != -1:
                xzrjc__spoe = ts.weekday()
                vseg__ggrm = (dateoffset._weekday - xzrjc__spoe) % 7
                ts = ts + pd.Timedelta(days=vseg__ggrm)
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
        scbwh__zaehl = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, scbwh__zaehl)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        iawl__srpyu = -1 if weekday is None else weekday
        return init_week(n, normalize, iawl__srpyu)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        kyn__hyut = cgutils.create_struct_proxy(typ)(context, builder)
        kyn__hyut.n = args[0]
        kyn__hyut.normalize = args[1]
        kyn__hyut.weekday = args[2]
        return kyn__hyut._getvalue()
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
    kyn__hyut = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    sui__uqadh = c.pyapi.long_from_longlong(kyn__hyut.n)
    fged__tdmpt = c.pyapi.from_native_value(types.boolean, kyn__hyut.
        normalize, c.env_manager)
    wyzez__gfkz = c.pyapi.long_from_longlong(kyn__hyut.weekday)
    ohk__sjf = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    zpk__ajm = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -1
        ), kyn__hyut.weekday)
    with c.builder.if_else(zpk__ajm) as (kwfnf__rjikl, bqq__diiza):
        with kwfnf__rjikl:
            wjpd__wyu = c.pyapi.call_function_objargs(ohk__sjf, (sui__uqadh,
                fged__tdmpt, wyzez__gfkz))
            tkzz__cjfdp = c.builder.block
        with bqq__diiza:
            vmmk__owv = c.pyapi.call_function_objargs(ohk__sjf, (sui__uqadh,
                fged__tdmpt))
            utnze__ldsdz = c.builder.block
    vxwfi__jhu = c.builder.phi(wjpd__wyu.type)
    vxwfi__jhu.add_incoming(wjpd__wyu, tkzz__cjfdp)
    vxwfi__jhu.add_incoming(vmmk__owv, utnze__ldsdz)
    c.pyapi.decref(wyzez__gfkz)
    c.pyapi.decref(sui__uqadh)
    c.pyapi.decref(fged__tdmpt)
    c.pyapi.decref(ohk__sjf)
    return vxwfi__jhu


@unbox(WeekType)
def unbox_week(typ, val, c):
    sui__uqadh = c.pyapi.object_getattr_string(val, 'n')
    fged__tdmpt = c.pyapi.object_getattr_string(val, 'normalize')
    wyzez__gfkz = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(sui__uqadh)
    normalize = c.pyapi.to_native_value(types.bool_, fged__tdmpt).value
    guy__wkft = c.pyapi.make_none()
    bqj__vrrwy = c.builder.icmp_unsigned('==', wyzez__gfkz, guy__wkft)
    with c.builder.if_else(bqj__vrrwy) as (bqq__diiza, kwfnf__rjikl):
        with kwfnf__rjikl:
            wjpd__wyu = c.pyapi.long_as_longlong(wyzez__gfkz)
            tkzz__cjfdp = c.builder.block
        with bqq__diiza:
            vmmk__owv = lir.Constant(lir.IntType(64), -1)
            utnze__ldsdz = c.builder.block
    vxwfi__jhu = c.builder.phi(wjpd__wyu.type)
    vxwfi__jhu.add_incoming(wjpd__wyu, tkzz__cjfdp)
    vxwfi__jhu.add_incoming(vmmk__owv, utnze__ldsdz)
    kyn__hyut = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    kyn__hyut.n = n
    kyn__hyut.normalize = normalize
    kyn__hyut.weekday = vxwfi__jhu
    c.pyapi.decref(sui__uqadh)
    c.pyapi.decref(fged__tdmpt)
    c.pyapi.decref(wyzez__gfkz)
    qkfk__ptru = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(kyn__hyut._getvalue(), is_error=qkfk__ptru)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            zheuo__legy = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                bwyjd__wgn = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                bwyjd__wgn = rhs
            return bwyjd__wgn + zheuo__legy
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            zheuo__legy = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                bwyjd__wgn = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                bwyjd__wgn = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return bwyjd__wgn + zheuo__legy
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            zheuo__legy = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            return rhs + zheuo__legy
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
        iuu__tls = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=iuu__tls)


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
    for blrd__nqms in date_offset_unsupported_attrs:
        wxo__ezjyn = 'pandas.tseries.offsets.DateOffset.' + blrd__nqms
        overload_attribute(DateOffsetType, blrd__nqms)(
            create_unsupported_overload(wxo__ezjyn))
    for blrd__nqms in date_offset_unsupported:
        wxo__ezjyn = 'pandas.tseries.offsets.DateOffset.' + blrd__nqms
        overload_method(DateOffsetType, blrd__nqms)(create_unsupported_overload
            (wxo__ezjyn))


def _install_month_begin_unsupported():
    for blrd__nqms in month_begin_unsupported_attrs:
        wxo__ezjyn = 'pandas.tseries.offsets.MonthBegin.' + blrd__nqms
        overload_attribute(MonthBeginType, blrd__nqms)(
            create_unsupported_overload(wxo__ezjyn))
    for blrd__nqms in month_begin_unsupported:
        wxo__ezjyn = 'pandas.tseries.offsets.MonthBegin.' + blrd__nqms
        overload_method(MonthBeginType, blrd__nqms)(create_unsupported_overload
            (wxo__ezjyn))


def _install_month_end_unsupported():
    for blrd__nqms in date_offset_unsupported_attrs:
        wxo__ezjyn = 'pandas.tseries.offsets.MonthEnd.' + blrd__nqms
        overload_attribute(MonthEndType, blrd__nqms)(
            create_unsupported_overload(wxo__ezjyn))
    for blrd__nqms in date_offset_unsupported:
        wxo__ezjyn = 'pandas.tseries.offsets.MonthEnd.' + blrd__nqms
        overload_method(MonthEndType, blrd__nqms)(create_unsupported_overload
            (wxo__ezjyn))


def _install_week_unsupported():
    for blrd__nqms in week_unsupported_attrs:
        wxo__ezjyn = 'pandas.tseries.offsets.Week.' + blrd__nqms
        overload_attribute(WeekType, blrd__nqms)(create_unsupported_overload
            (wxo__ezjyn))
    for blrd__nqms in week_unsupported:
        wxo__ezjyn = 'pandas.tseries.offsets.Week.' + blrd__nqms
        overload_method(WeekType, blrd__nqms)(create_unsupported_overload(
            wxo__ezjyn))


def _install_offsets_unsupported():
    for xepu__woip in offsets_unsupported:
        wxo__ezjyn = 'pandas.tseries.offsets.' + xepu__woip.__name__
        overload(xepu__woip)(create_unsupported_overload(wxo__ezjyn))


def _install_frequencies_unsupported():
    for xepu__woip in frequencies_unsupported:
        wxo__ezjyn = 'pandas.tseries.frequencies.' + xepu__woip.__name__
        overload(xepu__woip)(create_unsupported_overload(wxo__ezjyn))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
