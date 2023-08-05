"""Timestamp extension for Pandas Timestamp with timezone support."""
import calendar
import datetime
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import ConcreteTemplate, infer_global, signature
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo.libs.str_ext
import bodo.utils.utils
from bodo.hiframes.datetime_date_ext import DatetimeDateType, _ord2ymd, _ymd2ord, get_isocalendar
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, _no_input, datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdatetime_ext
from bodo.libs.pd_datetime_arr_ext import get_pytz_type_info
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import BodoError, check_unsupported_args, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_iterable_type, is_overload_constant_int, is_overload_constant_str, is_overload_none, raise_bodo_error
ll.add_symbol('extract_year_days', hdatetime_ext.extract_year_days)
ll.add_symbol('get_month_day', hdatetime_ext.get_month_day)
ll.add_symbol('npy_datetimestruct_to_datetime', hdatetime_ext.
    npy_datetimestruct_to_datetime)
npy_datetimestruct_to_datetime = types.ExternalFunction(
    'npy_datetimestruct_to_datetime', types.int64(types.int64, types.int32,
    types.int32, types.int32, types.int32, types.int32, types.int32))
date_fields = ['year', 'month', 'day', 'hour', 'minute', 'second',
    'microsecond', 'nanosecond', 'quarter', 'dayofyear', 'day_of_year',
    'dayofweek', 'day_of_week', 'daysinmonth', 'days_in_month',
    'is_leap_year', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end', 'week', 'weekofyear',
    'weekday']
date_methods = ['normalize', 'day_name', 'month_name']
timedelta_fields = ['days', 'seconds', 'microseconds', 'nanoseconds']
timedelta_methods = ['total_seconds', 'to_pytimedelta']
iNaT = pd._libs.tslibs.iNaT


class PandasTimestampType(types.Type):

    def __init__(self, tz_val=None):
        self.tz = tz_val
        if tz_val is None:
            ckxoe__itik = 'PandasTimestampType()'
        else:
            ckxoe__itik = f'PandasTimestampType({tz_val})'
        super(PandasTimestampType, self).__init__(name=ckxoe__itik)


pd_timestamp_type = PandasTimestampType()


def check_tz_aware_unsupported(val, func_name):
    if isinstance(val, bodo.hiframes.series_dt_impl.
        SeriesDatetimePropertiesType):
        val = val.stype
    if isinstance(val, PandasTimestampType) and val.tz is not None:
        raise BodoError(
            f'{func_name} on Timezone-aware timestamp not yet supported. Please convert to timezone naive with ts.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware array not yet supported. Please convert to timezone naive with arr.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeIndexType) and isinstance(val.data,
        bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware index not yet supported. Please convert to timezone naive with index.tz_convert(None)'
            )
    elif isinstance(val, bodo.SeriesType) and isinstance(val.data, bodo.
        DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware series not yet supported. Please convert to timezone naive with series.dt.tz_convert(None)'
            )
    elif isinstance(val, bodo.DataFrameType):
        for twk__gakc in val.data:
            if isinstance(twk__gakc, bodo.DatetimeArrayType):
                raise BodoError(
                    f'{func_name} on Timezone-aware columns not yet supported. Please convert each column to timezone naive with series.dt.tz_convert(None)'
                    )


@typeof_impl.register(pd.Timestamp)
def typeof_pd_timestamp(val, c):
    return PandasTimestampType(get_pytz_type_info(val.tz) if val.tz else None)


ts_field_typ = types.int64


@register_model(PandasTimestampType)
class PandasTimestampModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        oah__gjc = [('year', ts_field_typ), ('month', ts_field_typ), ('day',
            ts_field_typ), ('hour', ts_field_typ), ('minute', ts_field_typ),
            ('second', ts_field_typ), ('microsecond', ts_field_typ), (
            'nanosecond', ts_field_typ), ('value', ts_field_typ)]
        models.StructModel.__init__(self, dmm, fe_type, oah__gjc)


make_attribute_wrapper(PandasTimestampType, 'year', 'year')
make_attribute_wrapper(PandasTimestampType, 'month', 'month')
make_attribute_wrapper(PandasTimestampType, 'day', 'day')
make_attribute_wrapper(PandasTimestampType, 'hour', 'hour')
make_attribute_wrapper(PandasTimestampType, 'minute', 'minute')
make_attribute_wrapper(PandasTimestampType, 'second', 'second')
make_attribute_wrapper(PandasTimestampType, 'microsecond', 'microsecond')
make_attribute_wrapper(PandasTimestampType, 'nanosecond', 'nanosecond')
make_attribute_wrapper(PandasTimestampType, 'value', 'value')


@unbox(PandasTimestampType)
def unbox_pandas_timestamp(typ, val, c):
    rjdq__hnzma = c.pyapi.object_getattr_string(val, 'year')
    bnknm__emxvy = c.pyapi.object_getattr_string(val, 'month')
    krldk__dajq = c.pyapi.object_getattr_string(val, 'day')
    wjib__kfnll = c.pyapi.object_getattr_string(val, 'hour')
    djf__srebq = c.pyapi.object_getattr_string(val, 'minute')
    zew__srn = c.pyapi.object_getattr_string(val, 'second')
    bkt__jnup = c.pyapi.object_getattr_string(val, 'microsecond')
    jrrv__euqmr = c.pyapi.object_getattr_string(val, 'nanosecond')
    uuk__bgv = c.pyapi.object_getattr_string(val, 'value')
    gmn__qtwx = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gmn__qtwx.year = c.pyapi.long_as_longlong(rjdq__hnzma)
    gmn__qtwx.month = c.pyapi.long_as_longlong(bnknm__emxvy)
    gmn__qtwx.day = c.pyapi.long_as_longlong(krldk__dajq)
    gmn__qtwx.hour = c.pyapi.long_as_longlong(wjib__kfnll)
    gmn__qtwx.minute = c.pyapi.long_as_longlong(djf__srebq)
    gmn__qtwx.second = c.pyapi.long_as_longlong(zew__srn)
    gmn__qtwx.microsecond = c.pyapi.long_as_longlong(bkt__jnup)
    gmn__qtwx.nanosecond = c.pyapi.long_as_longlong(jrrv__euqmr)
    gmn__qtwx.value = c.pyapi.long_as_longlong(uuk__bgv)
    c.pyapi.decref(rjdq__hnzma)
    c.pyapi.decref(bnknm__emxvy)
    c.pyapi.decref(krldk__dajq)
    c.pyapi.decref(wjib__kfnll)
    c.pyapi.decref(djf__srebq)
    c.pyapi.decref(zew__srn)
    c.pyapi.decref(bkt__jnup)
    c.pyapi.decref(jrrv__euqmr)
    c.pyapi.decref(uuk__bgv)
    otsb__pywr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gmn__qtwx._getvalue(), is_error=otsb__pywr)


@box(PandasTimestampType)
def box_pandas_timestamp(typ, val, c):
    vhiuk__puvg = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    rjdq__hnzma = c.pyapi.long_from_longlong(vhiuk__puvg.year)
    bnknm__emxvy = c.pyapi.long_from_longlong(vhiuk__puvg.month)
    krldk__dajq = c.pyapi.long_from_longlong(vhiuk__puvg.day)
    wjib__kfnll = c.pyapi.long_from_longlong(vhiuk__puvg.hour)
    djf__srebq = c.pyapi.long_from_longlong(vhiuk__puvg.minute)
    zew__srn = c.pyapi.long_from_longlong(vhiuk__puvg.second)
    yzyqq__qugii = c.pyapi.long_from_longlong(vhiuk__puvg.microsecond)
    yfxa__dgxtr = c.pyapi.long_from_longlong(vhiuk__puvg.nanosecond)
    vitp__yworz = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timestamp))
    if typ.tz is None:
        res = c.pyapi.call_function_objargs(vitp__yworz, (rjdq__hnzma,
            bnknm__emxvy, krldk__dajq, wjib__kfnll, djf__srebq, zew__srn,
            yzyqq__qugii, yfxa__dgxtr))
    else:
        if isinstance(typ.tz, int):
            jzyx__inxsg = c.pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), typ.tz))
        else:
            blt__lbxe = c.context.insert_const_string(c.builder.module, str
                (typ.tz))
            jzyx__inxsg = c.pyapi.string_from_string(blt__lbxe)
        args = c.pyapi.tuple_pack(())
        kwargs = c.pyapi.dict_pack([('year', rjdq__hnzma), ('month',
            bnknm__emxvy), ('day', krldk__dajq), ('hour', wjib__kfnll), (
            'minute', djf__srebq), ('second', zew__srn), ('microsecond',
            yzyqq__qugii), ('nanosecond', yfxa__dgxtr), ('tz', jzyx__inxsg)])
        res = c.pyapi.call(vitp__yworz, args, kwargs)
        c.pyapi.decref(args)
        c.pyapi.decref(kwargs)
        c.pyapi.decref(jzyx__inxsg)
    c.pyapi.decref(rjdq__hnzma)
    c.pyapi.decref(bnknm__emxvy)
    c.pyapi.decref(krldk__dajq)
    c.pyapi.decref(wjib__kfnll)
    c.pyapi.decref(djf__srebq)
    c.pyapi.decref(zew__srn)
    c.pyapi.decref(yzyqq__qugii)
    c.pyapi.decref(yfxa__dgxtr)
    return res


@intrinsic
def init_timestamp(typingctx, year, month, day, hour, minute, second,
    microsecond, nanosecond, value, tz):

    def codegen(context, builder, sig, args):
        (year, month, day, hour, minute, second, waxqd__nlc, kpuur__mtrw,
            value, bcb__jhr) = args
        ts = cgutils.create_struct_proxy(sig.return_type)(context, builder)
        ts.year = year
        ts.month = month
        ts.day = day
        ts.hour = hour
        ts.minute = minute
        ts.second = second
        ts.microsecond = waxqd__nlc
        ts.nanosecond = kpuur__mtrw
        ts.value = value
        return ts._getvalue()
    if is_overload_none(tz):
        typ = pd_timestamp_type
    elif is_overload_constant_str(tz):
        typ = PandasTimestampType(get_overload_const_str(tz))
    elif is_overload_constant_int(tz):
        typ = PandasTimestampType(get_overload_const_int(tz))
    else:
        raise_bodo_error('tz must be a constant string, int, or None')
    return typ(types.int64, types.int64, types.int64, types.int64, types.
        int64, types.int64, types.int64, types.int64, types.int64, tz), codegen


@numba.generated_jit
def zero_if_none(value):
    if value == types.none:
        return lambda value: 0
    return lambda value: value


@lower_constant(PandasTimestampType)
def constant_timestamp(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    nanosecond = context.get_constant(types.int64, pyval.nanosecond)
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct((year, month, day, hour, minute,
        second, microsecond, nanosecond, value))


@overload(pd.Timestamp, no_unliteral=True)
def overload_pd_timestamp(ts_input=_no_input, freq=None, tz=None, unit=None,
    year=None, month=None, day=None, hour=None, minute=None, second=None,
    microsecond=None, nanosecond=None, tzinfo=None):
    if not is_overload_none(tz) and is_overload_constant_str(tz
        ) and get_overload_const_str(tz) not in pytz.all_timezones_set:
        raise BodoError(
            "pandas.Timestamp(): 'tz', if provided, must be constant string found in pytz.all_timezones"
            )
    if ts_input == _no_input or getattr(ts_input, 'value', None) == _no_input:

        def impl_kw(ts_input=_no_input, freq=None, tz=None, unit=None, year
            =None, month=None, day=None, hour=None, minute=None, second=
            None, microsecond=None, nanosecond=None, tzinfo=None):
            value = npy_datetimestruct_to_datetime(year, month, day,
                zero_if_none(hour), zero_if_none(minute), zero_if_none(
                second), zero_if_none(microsecond))
            value += zero_if_none(nanosecond)
            return init_timestamp(year, month, day, zero_if_none(hour),
                zero_if_none(minute), zero_if_none(second), zero_if_none(
                microsecond), zero_if_none(nanosecond), value, tz)
        return impl_kw
    if isinstance(types.unliteral(freq), types.Integer):

        def impl_pos(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = npy_datetimestruct_to_datetime(ts_input, freq, tz,
                zero_if_none(unit), zero_if_none(year), zero_if_none(month),
                zero_if_none(day))
            value += zero_if_none(hour)
            return init_timestamp(ts_input, freq, tz, zero_if_none(unit),
                zero_if_none(year), zero_if_none(month), zero_if_none(day),
                zero_if_none(hour), value, None)
        return impl_pos
    if isinstance(ts_input, types.Number):
        if is_overload_none(unit):
            unit = 'ns'
        if not is_overload_constant_str(unit):
            raise BodoError(
                'pandas.Timedelta(): unit argument must be a constant str')
        unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
            get_overload_const_str(unit))
        bnt__iviuz, precision = pd._libs.tslibs.conversion.precision_from_unit(
            unit)
        if isinstance(ts_input, types.Integer):

            def impl_int(ts_input=_no_input, freq=None, tz=None, unit=None,
                year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, nanosecond=None, tzinfo=None):
                value = ts_input * bnt__iviuz
                return convert_val_to_timestamp(value, tz)
            return impl_int

        def impl_float(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            hzurv__penw = np.int64(ts_input)
            pyq__vuctf = ts_input - hzurv__penw
            if precision:
                pyq__vuctf = np.round(pyq__vuctf, precision)
            value = hzurv__penw * bnt__iviuz + np.int64(pyq__vuctf * bnt__iviuz
                )
            return convert_val_to_timestamp(value, tz)
        return impl_float
    if ts_input == bodo.string_type or is_overload_constant_str(ts_input):
        types.pd_timestamp_type = pd_timestamp_type
        if is_overload_none(tz):
            tz_val = None
        elif is_overload_constant_str(tz):
            tz_val = get_overload_const_str(tz)
        else:
            raise_bodo_error(
                'pandas.Timestamp(): tz argument must be a constant string or None'
                )
        typ = PandasTimestampType(tz_val)

        def impl_str(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            with numba.objmode(res=typ):
                res = pd.Timestamp(ts_input, tz=tz)
            return res
        return impl_str
    if ts_input == pd_timestamp_type:
        return (lambda ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None: ts_input)
    if ts_input == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:

        def impl_datetime(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            hour = ts_input.hour
            minute = ts_input.minute
            second = ts_input.second
            microsecond = ts_input.microsecond
            value = npy_datetimestruct_to_datetime(year, month, day,
                zero_if_none(hour), zero_if_none(minute), zero_if_none(
                second), zero_if_none(microsecond))
            value += zero_if_none(nanosecond)
            return init_timestamp(year, month, day, zero_if_none(hour),
                zero_if_none(minute), zero_if_none(second), zero_if_none(
                microsecond), zero_if_none(nanosecond), value, tz)
        return impl_datetime
    if ts_input == bodo.hiframes.datetime_date_ext.datetime_date_type:

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            value = npy_datetimestruct_to_datetime(year, month, day,
                zero_if_none(hour), zero_if_none(minute), zero_if_none(
                second), zero_if_none(microsecond))
            value += zero_if_none(nanosecond)
            return init_timestamp(year, month, day, zero_if_none(hour),
                zero_if_none(minute), zero_if_none(second), zero_if_none(
                microsecond), zero_if_none(nanosecond), value, None)
        return impl_date
    if isinstance(ts_input, numba.core.types.scalars.NPDatetime):
        bnt__iviuz, precision = pd._libs.tslibs.conversion.precision_from_unit(
            ts_input.unit)

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = np.int64(ts_input) * bnt__iviuz
            return convert_datetime64_to_timestamp(integer_to_dt64(value))
        return impl_date


@overload_attribute(PandasTimestampType, 'dayofyear')
@overload_attribute(PandasTimestampType, 'day_of_year')
def overload_pd_dayofyear(ptt):

    def pd_dayofyear(ptt):
        return get_day_of_year(ptt.year, ptt.month, ptt.day)
    return pd_dayofyear


@overload_method(PandasTimestampType, 'weekday')
@overload_attribute(PandasTimestampType, 'dayofweek')
@overload_attribute(PandasTimestampType, 'day_of_week')
def overload_pd_dayofweek(ptt):

    def pd_dayofweek(ptt):
        return get_day_of_week(ptt.year, ptt.month, ptt.day)
    return pd_dayofweek


@overload_attribute(PandasTimestampType, 'week')
@overload_attribute(PandasTimestampType, 'weekofyear')
def overload_week_number(ptt):

    def pd_week_number(ptt):
        bcb__jhr, hypbg__hfb, bcb__jhr = get_isocalendar(ptt.year, ptt.
            month, ptt.day)
        return hypbg__hfb
    return pd_week_number


@overload_method(PandasTimestampType, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(val.value)


@overload_attribute(PandasTimestampType, 'days_in_month')
@overload_attribute(PandasTimestampType, 'daysinmonth')
def overload_pd_daysinmonth(ptt):

    def pd_daysinmonth(ptt):
        return get_days_in_month(ptt.year, ptt.month)
    return pd_daysinmonth


@overload_attribute(PandasTimestampType, 'is_leap_year')
def overload_pd_is_leap_year(ptt):

    def pd_is_leap_year(ptt):
        return is_leap_year(ptt.year)
    return pd_is_leap_year


@overload_attribute(PandasTimestampType, 'is_month_start')
def overload_pd_is_month_start(ptt):

    def pd_is_month_start(ptt):
        return ptt.day == 1
    return pd_is_month_start


@overload_attribute(PandasTimestampType, 'is_month_end')
def overload_pd_is_month_end(ptt):

    def pd_is_month_end(ptt):
        return ptt.day == get_days_in_month(ptt.year, ptt.month)
    return pd_is_month_end


@overload_attribute(PandasTimestampType, 'is_quarter_start')
def overload_pd_is_quarter_start(ptt):

    def pd_is_quarter_start(ptt):
        return ptt.day == 1 and ptt.month % 3 == 1
    return pd_is_quarter_start


@overload_attribute(PandasTimestampType, 'is_quarter_end')
def overload_pd_is_quarter_end(ptt):

    def pd_is_quarter_end(ptt):
        return ptt.month % 3 == 0 and ptt.day == get_days_in_month(ptt.year,
            ptt.month)
    return pd_is_quarter_end


@overload_attribute(PandasTimestampType, 'is_year_start')
def overload_pd_is_year_start(ptt):

    def pd_is_year_start(ptt):
        return ptt.day == 1 and ptt.month == 1
    return pd_is_year_start


@overload_attribute(PandasTimestampType, 'is_year_end')
def overload_pd_is_year_end(ptt):

    def pd_is_year_end(ptt):
        return ptt.day == 31 and ptt.month == 12
    return pd_is_year_end


@overload_attribute(PandasTimestampType, 'quarter')
def overload_quarter(ptt):

    def quarter(ptt):
        return (ptt.month - 1) // 3 + 1
    return quarter


@overload_method(PandasTimestampType, 'date', no_unliteral=True)
def overload_pd_timestamp_date(ptt):

    def pd_timestamp_date_impl(ptt):
        return datetime.date(ptt.year, ptt.month, ptt.day)
    return pd_timestamp_date_impl


@overload_method(PandasTimestampType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(ptt):

    def impl(ptt):
        year, hypbg__hfb, qlese__ufs = get_isocalendar(ptt.year, ptt.month,
            ptt.day)
        return year, hypbg__hfb, qlese__ufs
    return impl


@overload_method(PandasTimestampType, 'isoformat', no_unliteral=True)
def overload_pd_timestamp_isoformat(ts, sep=None):
    if is_overload_none(sep):

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            gtem__hho = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + 'T' + gtem__hho
            return res
        return timestamp_isoformat_impl
    else:

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            gtem__hho = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + sep + gtem__hho
            return res
    return timestamp_isoformat_impl


@overload_method(PandasTimestampType, 'normalize', no_unliteral=True)
def overload_pd_timestamp_normalize(ptt):

    def impl(ptt):
        return pd.Timestamp(year=ptt.year, month=ptt.month, day=ptt.day)
    return impl


@overload_method(PandasTimestampType, 'day_name', no_unliteral=True)
def overload_pd_timestamp_day_name(ptt, locale=None):
    ufpbk__bpbpq = dict(locale=locale)
    gwqgs__caxg = dict(locale=None)
    check_unsupported_args('Timestamp.day_name', ufpbk__bpbpq, gwqgs__caxg,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        fmc__lvice = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday')
        bcb__jhr, bcb__jhr, xxn__owoby = ptt.isocalendar()
        return fmc__lvice[xxn__owoby - 1]
    return impl


@overload_method(PandasTimestampType, 'month_name', no_unliteral=True)
def overload_pd_timestamp_month_name(ptt, locale=None):
    ufpbk__bpbpq = dict(locale=locale)
    gwqgs__caxg = dict(locale=None)
    check_unsupported_args('Timestamp.month_name', ufpbk__bpbpq,
        gwqgs__caxg, package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        wqnuq__ops = ('January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October', 'November',
            'December')
        return wqnuq__ops[ptt.month - 1]
    return impl


@overload_method(PandasTimestampType, 'tz_convert', no_unliteral=True)
def overload_pd_timestamp_tz_convert(ptt, tz):
    if ptt.tz is None:
        raise BodoError(
            'Cannot convert tz-naive Timestamp, use tz_localize to localize')
    if is_overload_none(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value)
    elif is_overload_constant_str(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value, tz=tz)


@overload_method(PandasTimestampType, 'tz_localize', no_unliteral=True)
def overload_pd_timestamp_tz_localize(ptt, tz, ambiguous='raise',
    nonexistent='raise'):
    if ptt.tz is not None and not is_overload_none(tz):
        raise BodoError(
            'Cannot localize tz-aware Timestamp, use tz_convert for conversions'
            )
    ufpbk__bpbpq = dict(ambiguous=ambiguous, nonexistent=nonexistent)
    khwhn__rmx = dict(ambiguous='raise', nonexistent='raise')
    check_unsupported_args('Timestamp.tz_localize', ufpbk__bpbpq,
        khwhn__rmx, package_name='pandas', module_name='Timestamp')
    if is_overload_none(tz):
        return (lambda ptt, tz, ambiguous='raise', nonexistent='raise':
            convert_val_to_timestamp(ptt.value, is_convert=False))
    elif is_overload_constant_str(tz):
        return (lambda ptt, tz, ambiguous='raise', nonexistent='raise':
            convert_val_to_timestamp(ptt.value, tz=tz, is_convert=False))


@numba.njit
def str_2d(a):
    res = str(a)
    if len(res) == 1:
        return '0' + res
    return res


@overload(str, no_unliteral=True)
def ts_str_overload(a):
    if a == pd_timestamp_type:
        return lambda a: a.isoformat(' ')


@intrinsic
def extract_year_days(typingctx, dt64_t=None):
    assert dt64_t in (types.int64, types.NPDatetime('ns'))

    def codegen(context, builder, sig, args):
        sai__zeibd = cgutils.alloca_once(builder, lir.IntType(64))
        builder.store(args[0], sai__zeibd)
        year = cgutils.alloca_once(builder, lir.IntType(64))
        imzh__nhjeg = cgutils.alloca_once(builder, lir.IntType(64))
        emj__xepul = lir.FunctionType(lir.VoidType(), [lir.IntType(64).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        dcr__qnsf = cgutils.get_or_insert_function(builder.module,
            emj__xepul, name='extract_year_days')
        builder.call(dcr__qnsf, [sai__zeibd, year, imzh__nhjeg])
        return cgutils.pack_array(builder, [builder.load(sai__zeibd),
            builder.load(year), builder.load(imzh__nhjeg)])
    return types.Tuple([types.int64, types.int64, types.int64])(dt64_t
        ), codegen


@intrinsic
def get_month_day(typingctx, year_t, days_t=None):
    assert year_t == types.int64
    assert days_t == types.int64

    def codegen(context, builder, sig, args):
        month = cgutils.alloca_once(builder, lir.IntType(64))
        day = cgutils.alloca_once(builder, lir.IntType(64))
        emj__xepul = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir
            .IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        dcr__qnsf = cgutils.get_or_insert_function(builder.module,
            emj__xepul, name='get_month_day')
        builder.call(dcr__qnsf, [args[0], args[1], month, day])
        return cgutils.pack_array(builder, [builder.load(month), builder.
            load(day)])
    return types.Tuple([types.int64, types.int64])(types.int64, types.int64
        ), codegen


@register_jitable
def get_day_of_year(year, month, day):
    xixc__ygeh = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 
        365, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    jxer__znfaa = is_leap_year(year)
    tfo__yzs = xixc__ygeh[jxer__znfaa * 13 + month - 1]
    nhhk__oxogo = tfo__yzs + day
    return nhhk__oxogo


@register_jitable
def get_day_of_week(y, m, d):
    ohdul__uhrnb = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y -= m < 3
    day = (y + y // 4 - y // 100 + y // 400 + ohdul__uhrnb[m - 1] + d) % 7
    return (day + 6) % 7


@register_jitable
def get_days_in_month(year, month):
    is_leap_year = year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)
    kwdf__flc = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 29, 31,
        30, 31, 30, 31, 31, 30, 31, 30, 31]
    return kwdf__flc[12 * is_leap_year + month - 1]


@register_jitable
def is_leap_year(year):
    return year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)


@numba.generated_jit(nopython=True)
def convert_val_to_timestamp(ts_input, tz=None, is_convert=True):
    kdp__xwwm = uwnma__gcuu = np.array([])
    lujo__ktvf = '0'
    if is_overload_constant_str(tz):
        blt__lbxe = get_overload_const_str(tz)
        jzyx__inxsg = pytz.timezone(blt__lbxe)
        if isinstance(jzyx__inxsg, pytz.tzinfo.DstTzInfo):
            kdp__xwwm = np.array(jzyx__inxsg._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            uwnma__gcuu = np.array(jzyx__inxsg._transition_info)[:, 0]
            uwnma__gcuu = (pd.Series(uwnma__gcuu).dt.total_seconds() * 
                1000000000).astype(np.int64).values
            lujo__ktvf = (
                "deltas[np.searchsorted(trans, ts_input, side='right') - 1]")
        else:
            uwnma__gcuu = np.int64(jzyx__inxsg._utcoffset.total_seconds() *
                1000000000)
            lujo__ktvf = 'deltas'
    elif is_overload_constant_int(tz):
        zaxg__aekz = get_overload_const_int(tz)
        lujo__ktvf = str(zaxg__aekz)
    elif not is_overload_none(tz):
        raise_bodo_error(
            'convert_val_to_timestamp(): tz value must be a constant string or None'
            )
    is_convert = get_overload_const_bool(is_convert)
    if is_convert:
        duazi__yfhwj = 'tz_ts_input'
        udbsq__jxi = 'ts_input'
    else:
        duazi__yfhwj = 'ts_input'
        udbsq__jxi = 'tz_ts_input'
    gxpv__njuwj = 'def impl(ts_input, tz=None, is_convert=True):\n'
    gxpv__njuwj += f'  tz_ts_input = ts_input + {lujo__ktvf}\n'
    gxpv__njuwj += (
        f'  dt, year, days = extract_year_days(integer_to_dt64({duazi__yfhwj}))\n'
        )
    gxpv__njuwj += '  month, day = get_month_day(year, days)\n'
    gxpv__njuwj += '  return init_timestamp(\n'
    gxpv__njuwj += '    year=year,\n'
    gxpv__njuwj += '    month=month,\n'
    gxpv__njuwj += '    day=day,\n'
    gxpv__njuwj += '    hour=dt // (60 * 60 * 1_000_000_000),\n'
    gxpv__njuwj += '    minute=(dt // (60 * 1_000_000_000)) % 60,\n'
    gxpv__njuwj += '    second=(dt // 1_000_000_000) % 60,\n'
    gxpv__njuwj += '    microsecond=(dt // 1000) % 1_000_000,\n'
    gxpv__njuwj += '    nanosecond=dt % 1000,\n'
    gxpv__njuwj += f'    value={udbsq__jxi},\n'
    gxpv__njuwj += '    tz=tz,\n'
    gxpv__njuwj += '  )\n'
    ivdq__xxw = {}
    exec(gxpv__njuwj, {'np': np, 'pd': pd, 'trans': kdp__xwwm, 'deltas':
        uwnma__gcuu, 'integer_to_dt64': integer_to_dt64,
        'extract_year_days': extract_year_days, 'get_month_day':
        get_month_day, 'init_timestamp': init_timestamp, 'zero_if_none':
        zero_if_none}, ivdq__xxw)
    impl = ivdq__xxw['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def convert_datetime64_to_timestamp(dt64):
    sai__zeibd, year, imzh__nhjeg = extract_year_days(dt64)
    month, day = get_month_day(year, imzh__nhjeg)
    return init_timestamp(year=year, month=month, day=day, hour=sai__zeibd //
        (60 * 60 * 1000000000), minute=sai__zeibd // (60 * 1000000000) % 60,
        second=sai__zeibd // 1000000000 % 60, microsecond=sai__zeibd // 
        1000 % 1000000, nanosecond=sai__zeibd % 1000, value=dt64, tz=None)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_datetime_timedelta(dt64):
    tnxt__nmejc = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    yge__ykk = tnxt__nmejc // (86400 * 1000000000)
    qln__hfzx = tnxt__nmejc - yge__ykk * 86400 * 1000000000
    qoplp__mer = qln__hfzx // 1000000000
    edp__qsod = qln__hfzx - qoplp__mer * 1000000000
    kpeuf__gkex = edp__qsod // 1000
    return datetime.timedelta(yge__ykk, qoplp__mer, kpeuf__gkex)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_pd_timedelta(dt64):
    tnxt__nmejc = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    return pd.Timedelta(tnxt__nmejc)


@intrinsic
def integer_to_timedelta64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPTimedelta('ns')(val), codegen


@intrinsic
def integer_to_dt64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPDatetime('ns')(val), codegen


@intrinsic
def dt64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(types.NPDatetime('ns'), types.int64)
def cast_dt64_to_integer(context, builder, fromty, toty, val):
    return val


@overload_method(types.NPDatetime, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@overload_method(types.NPTimedelta, '__hash__', no_unliteral=True)
def td64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@intrinsic
def timedelta64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(bodo.timedelta64ns, types.int64)
def cast_td64_to_integer(context, builder, fromty, toty, val):
    return val


@numba.njit
def parse_datetime_str(val):
    with numba.objmode(res='int64'):
        res = pd.Timestamp(val).value
    return integer_to_dt64(res)


@numba.njit
def datetime_timedelta_to_timedelta64(val):
    with numba.objmode(res='NPTimedelta("ns")'):
        res = pd.to_timedelta(val)
        res = res.to_timedelta64()
    return res


@numba.njit
def series_str_dt64_astype(data):
    with numba.objmode(res="NPDatetime('ns')[::1]"):
        res = pd.Series(data).astype('datetime64[ns]').values
    return res


@numba.njit
def series_str_td64_astype(data):
    with numba.objmode(res="NPTimedelta('ns')[::1]"):
        res = data.astype('timedelta64[ns]')
    return res


@numba.njit
def datetime_datetime_to_dt64(val):
    with numba.objmode(res='NPDatetime("ns")'):
        res = np.datetime64(val).astype('datetime64[ns]')
    return res


@register_jitable
def datetime_date_arr_to_dt64_arr(arr):
    with numba.objmode(res='NPDatetime("ns")[::1]'):
        res = np.array(arr, dtype='datetime64[ns]')
    return res


types.pd_timestamp_type = pd_timestamp_type


@register_jitable
def to_datetime_scalar(a, errors='raise', dayfirst=False, yearfirst=False,
    utc=None, format=None, exact=True, unit=None, infer_datetime_format=
    False, origin='unix', cache=True):
    with numba.objmode(t='pd_timestamp_type'):
        t = pd.to_datetime(a, errors=errors, dayfirst=dayfirst, yearfirst=
            yearfirst, utc=utc, format=format, exact=exact, unit=unit,
            infer_datetime_format=infer_datetime_format, origin=origin,
            cache=cache)
    return t


@numba.njit
def pandas_string_array_to_datetime(arr, errors, dayfirst, yearfirst, utc,
    format, exact, unit, infer_datetime_format, origin, cache):
    with numba.objmode(result='datetime_index'):
        result = pd.to_datetime(arr, errors=errors, dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
    return result


@numba.njit
def pandas_dict_string_array_to_datetime(arr, errors, dayfirst, yearfirst,
    utc, format, exact, unit, infer_datetime_format, origin, cache):
    xjw__btur = len(arr)
    mttb__auxcv = np.empty(xjw__btur, 'datetime64[ns]')
    xmwd__cvhi = arr._indices
    dkzzt__gnyq = pandas_string_array_to_datetime(arr._data, errors,
        dayfirst, yearfirst, utc, format, exact, unit,
        infer_datetime_format, origin, cache).values
    for ifv__yywp in range(xjw__btur):
        if bodo.libs.array_kernels.isna(xmwd__cvhi, ifv__yywp):
            bodo.libs.array_kernels.setna(mttb__auxcv, ifv__yywp)
            continue
        mttb__auxcv[ifv__yywp] = dkzzt__gnyq[xmwd__cvhi[ifv__yywp]]
    return mttb__auxcv


@overload(pd.to_datetime, inline='always', no_unliteral=True)
def overload_to_datetime(arg_a, errors='raise', dayfirst=False, yearfirst=
    False, utc=None, format=None, exact=True, unit=None,
    infer_datetime_format=False, origin='unix', cache=True):
    if arg_a == bodo.string_type or is_overload_constant_str(arg_a
        ) or is_overload_constant_int(arg_a) or isinstance(arg_a, types.Integer
        ):

        def pd_to_datetime_impl(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return to_datetime_scalar(arg_a, errors=errors, dayfirst=
                dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                exact=exact, unit=unit, infer_datetime_format=
                infer_datetime_format, origin=origin, cache=cache)
        return pd_to_datetime_impl
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            jshhs__wjp = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            ckxoe__itik = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            wfyne__mzrn = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_datetime(arr, errors=errors, dayfirst=dayfirst,
                yearfirst=yearfirst, utc=utc, format=format, exact=exact,
                unit=unit, infer_datetime_format=infer_datetime_format,
                origin=origin, cache=cache))
            return bodo.hiframes.pd_series_ext.init_series(wfyne__mzrn,
                jshhs__wjp, ckxoe__itik)
        return impl_series
    if arg_a == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        mjpm__lxqoq = np.dtype('datetime64[ns]')
        iNaT = pd._libs.tslibs.iNaT

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            xjw__btur = len(arg_a)
            mttb__auxcv = np.empty(xjw__btur, mjpm__lxqoq)
            for ifv__yywp in numba.parfors.parfor.internal_prange(xjw__btur):
                val = iNaT
                if not bodo.libs.array_kernels.isna(arg_a, ifv__yywp):
                    data = arg_a[ifv__yywp]
                    val = (bodo.hiframes.pd_timestamp_ext.
                        npy_datetimestruct_to_datetime(data.year, data.
                        month, data.day, 0, 0, 0, 0))
                mttb__auxcv[ifv__yywp
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(mttb__auxcv,
                None)
        return impl_date_arr
    if arg_a == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return (lambda arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True: bodo.
            hiframes.pd_index_ext.init_datetime_index(arg_a, None))
    if arg_a == string_array_type:

        def impl_string_array(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return pandas_string_array_to_datetime(arg_a, errors, dayfirst,
                yearfirst, utc, format, exact, unit, infer_datetime_format,
                origin, cache)
        return impl_string_array
    if isinstance(arg_a, types.Array) and isinstance(arg_a.dtype, types.Integer
        ):
        mjpm__lxqoq = np.dtype('datetime64[ns]')

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            xjw__btur = len(arg_a)
            mttb__auxcv = np.empty(xjw__btur, mjpm__lxqoq)
            for ifv__yywp in numba.parfors.parfor.internal_prange(xjw__btur):
                data = arg_a[ifv__yywp]
                val = to_datetime_scalar(data, errors=errors, dayfirst=
                    dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                    exact=exact, unit=unit, infer_datetime_format=
                    infer_datetime_format, origin=origin, cache=cache)
                mttb__auxcv[ifv__yywp
                    ] = bodo.hiframes.pd_timestamp_ext.datetime_datetime_to_dt64(
                    val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(mttb__auxcv,
                None)
        return impl_date_arr
    if isinstance(arg_a, CategoricalArrayType
        ) and arg_a.dtype.elem_type == bodo.string_type:
        mjpm__lxqoq = np.dtype('datetime64[ns]')

        def impl_cat_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            xjw__btur = len(arg_a)
            mttb__auxcv = np.empty(xjw__btur, mjpm__lxqoq)
            qisjt__ykhf = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arg_a))
            dkzzt__gnyq = pandas_string_array_to_datetime(arg_a.dtype.
                categories.values, errors, dayfirst, yearfirst, utc, format,
                exact, unit, infer_datetime_format, origin, cache).values
            for ifv__yywp in numba.parfors.parfor.internal_prange(xjw__btur):
                c = qisjt__ykhf[ifv__yywp]
                if c == -1:
                    bodo.libs.array_kernels.setna(mttb__auxcv, ifv__yywp)
                    continue
                mttb__auxcv[ifv__yywp] = dkzzt__gnyq[c]
            return bodo.hiframes.pd_index_ext.init_datetime_index(mttb__auxcv,
                None)
        return impl_cat_arr
    if arg_a == bodo.dict_str_arr_type:

        def impl_dict_str_arr(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            mttb__auxcv = pandas_dict_string_array_to_datetime(arg_a,
                errors, dayfirst, yearfirst, utc, format, exact, unit,
                infer_datetime_format, origin, cache)
            return bodo.hiframes.pd_index_ext.init_datetime_index(mttb__auxcv,
                None)
        return impl_dict_str_arr
    if isinstance(arg_a, PandasTimestampType):

        def impl_timestamp(arg_a, errors='raise', dayfirst=False, yearfirst
            =False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return arg_a
        return impl_timestamp
    raise_bodo_error(f'pd.to_datetime(): cannot convert date type {arg_a}')


@overload(pd.to_timedelta, inline='always', no_unliteral=True)
def overload_to_timedelta(arg_a, unit='ns', errors='raise'):
    if not is_overload_constant_str(unit):
        raise BodoError(
            'pandas.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, unit='ns', errors='raise'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            jshhs__wjp = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            ckxoe__itik = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            wfyne__mzrn = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_timedelta(arr, unit, errors))
            return bodo.hiframes.pd_series_ext.init_series(wfyne__mzrn,
                jshhs__wjp, ckxoe__itik)
        return impl_series
    if is_overload_constant_str(arg_a) or arg_a in (pd_timedelta_type,
        datetime_timedelta_type, bodo.string_type):

        def impl_string(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a)
        return impl_string
    if isinstance(arg_a, types.Float):
        m, srdal__ubdk = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_float_scalar(arg_a, unit='ns', errors='raise'):
            val = float_to_timedelta_val(arg_a, srdal__ubdk, m)
            return pd.Timedelta(val)
        return impl_float_scalar
    if isinstance(arg_a, types.Integer):
        m, bcb__jhr = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_integer_scalar(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a * m)
        return impl_integer_scalar
    if is_iterable_type(arg_a) and not isinstance(arg_a, types.BaseTuple):
        m, srdal__ubdk = pd._libs.tslibs.conversion.precision_from_unit(unit)
        zvlie__rjkt = np.dtype('timedelta64[ns]')
        if isinstance(arg_a.dtype, types.Float):

            def impl_float(arg_a, unit='ns', errors='raise'):
                xjw__btur = len(arg_a)
                mttb__auxcv = np.empty(xjw__btur, zvlie__rjkt)
                for ifv__yywp in numba.parfors.parfor.internal_prange(xjw__btur
                    ):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, ifv__yywp):
                        val = float_to_timedelta_val(arg_a[ifv__yywp],
                            srdal__ubdk, m)
                    mttb__auxcv[ifv__yywp
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    mttb__auxcv, None)
            return impl_float
        if isinstance(arg_a.dtype, types.Integer):

            def impl_int(arg_a, unit='ns', errors='raise'):
                xjw__btur = len(arg_a)
                mttb__auxcv = np.empty(xjw__btur, zvlie__rjkt)
                for ifv__yywp in numba.parfors.parfor.internal_prange(xjw__btur
                    ):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, ifv__yywp):
                        val = arg_a[ifv__yywp] * m
                    mttb__auxcv[ifv__yywp
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    mttb__auxcv, None)
            return impl_int
        if arg_a.dtype == bodo.timedelta64ns:

            def impl_td64(arg_a, unit='ns', errors='raise'):
                arr = bodo.utils.conversion.coerce_to_ndarray(arg_a)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(arr,
                    None)
            return impl_td64
        if arg_a.dtype == bodo.string_type or isinstance(arg_a.dtype, types
            .UnicodeCharSeq):

            def impl_str(arg_a, unit='ns', errors='raise'):
                return pandas_string_array_to_timedelta(arg_a, unit, errors)
            return impl_str
        if arg_a.dtype == datetime_timedelta_type:

            def impl_datetime_timedelta(arg_a, unit='ns', errors='raise'):
                xjw__btur = len(arg_a)
                mttb__auxcv = np.empty(xjw__btur, zvlie__rjkt)
                for ifv__yywp in numba.parfors.parfor.internal_prange(xjw__btur
                    ):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, ifv__yywp):
                        wsip__erfpt = arg_a[ifv__yywp]
                        val = (wsip__erfpt.microseconds + 1000 * 1000 * (
                            wsip__erfpt.seconds + 24 * 60 * 60 *
                            wsip__erfpt.days)) * 1000
                    mttb__auxcv[ifv__yywp
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    mttb__auxcv, None)
            return impl_datetime_timedelta
    raise_bodo_error(
        f'pd.to_timedelta(): cannot convert date type {arg_a.dtype}')


@register_jitable
def float_to_timedelta_val(data, precision, multiplier):
    hzurv__penw = np.int64(data)
    pyq__vuctf = data - hzurv__penw
    if precision:
        pyq__vuctf = np.round(pyq__vuctf, precision)
    return hzurv__penw * multiplier + np.int64(pyq__vuctf * multiplier)


@numba.njit
def pandas_string_array_to_timedelta(arg_a, unit='ns', errors='raise'):
    with numba.objmode(result='timedelta_index'):
        result = pd.to_timedelta(arg_a, errors=errors)
    return result


def create_timestamp_cmp_op_overload(op):

    def overload_date_timestamp_cmp(lhs, rhs):
        if (lhs == pd_timestamp_type and rhs == bodo.hiframes.
            datetime_date_ext.datetime_date_type):
            return lambda lhs, rhs: op(lhs.value, bodo.hiframes.
                pd_timestamp_ext.npy_datetimestruct_to_datetime(rhs.year,
                rhs.month, rhs.day, 0, 0, 0, 0))
        if (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and 
            rhs == pd_timestamp_type):
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                npy_datetimestruct_to_datetime(lhs.year, lhs.month, lhs.day,
                0, 0, 0, 0), rhs.value)
        if lhs == pd_timestamp_type and rhs == pd_timestamp_type:
            return lambda lhs, rhs: op(lhs.value, rhs.value)
        if lhs == pd_timestamp_type and rhs == bodo.datetime64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(lhs.value), rhs)
        if lhs == bodo.datetime64ns and rhs == pd_timestamp_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(rhs.value))
    return overload_date_timestamp_cmp


@overload_method(PandasTimestampType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


def overload_freq_methods(method):

    def freq_overload(td, freq, ambiguous='raise', nonexistent='raise'):
        check_tz_aware_unsupported(td, f'Timestamp.{method}()')
        ufpbk__bpbpq = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        iwu__pbfwf = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Timestamp.{method}', ufpbk__bpbpq,
            iwu__pbfwf, package_name='pandas', module_name='Timestamp')
        ifl__llvkh = ["freq == 'D'", "freq == 'H'",
            "freq == 'min' or freq == 'T'", "freq == 'S'",
            "freq == 'ms' or freq == 'L'", "freq == 'U' or freq == 'us'",
            "freq == 'N'"]
        vvyl__dat = [24 * 60 * 60 * 1000000 * 1000, 60 * 60 * 1000000 * 
            1000, 60 * 1000000 * 1000, 1000000 * 1000, 1000 * 1000, 1000, 1]
        gxpv__njuwj = (
            "def impl(td, freq, ambiguous='raise', nonexistent='raise'):\n")
        for ifv__yywp, skleq__vpnr in enumerate(ifl__llvkh):
            giqe__jfn = 'if' if ifv__yywp == 0 else 'elif'
            gxpv__njuwj += '    {} {}:\n'.format(giqe__jfn, skleq__vpnr)
            gxpv__njuwj += '        unit_value = {}\n'.format(vvyl__dat[
                ifv__yywp])
        gxpv__njuwj += '    else:\n'
        gxpv__njuwj += (
            "        raise ValueError('Incorrect Frequency specification')\n")
        if td == pd_timedelta_type:
            gxpv__njuwj += (
                """    return pd.Timedelta(unit_value * np.int64(np.{}(td.value / unit_value)))
"""
                .format(method))
        elif td == pd_timestamp_type:
            if method == 'ceil':
                gxpv__njuwj += (
                    '    value = td.value + np.remainder(-td.value, unit_value)\n'
                    )
            if method == 'floor':
                gxpv__njuwj += (
                    '    value = td.value - np.remainder(td.value, unit_value)\n'
                    )
            if method == 'round':
                gxpv__njuwj += '    if unit_value == 1:\n'
                gxpv__njuwj += '        value = td.value\n'
                gxpv__njuwj += '    else:\n'
                gxpv__njuwj += (
                    '        quotient, remainder = np.divmod(td.value, unit_value)\n'
                    )
                gxpv__njuwj += """        mask = np.logical_or(remainder > (unit_value // 2), np.logical_and(remainder == (unit_value // 2), quotient % 2))
"""
                gxpv__njuwj += '        if mask:\n'
                gxpv__njuwj += '            quotient = quotient + 1\n'
                gxpv__njuwj += '        value = quotient * unit_value\n'
            gxpv__njuwj += '    return pd.Timestamp(value)\n'
        ivdq__xxw = {}
        exec(gxpv__njuwj, {'np': np, 'pd': pd}, ivdq__xxw)
        impl = ivdq__xxw['impl']
        return impl
    return freq_overload


def _install_freq_methods():
    pwtfy__mqn = ['ceil', 'floor', 'round']
    for method in pwtfy__mqn:
        lkzg__umu = overload_freq_methods(method)
        overload_method(PDTimeDeltaType, method, no_unliteral=True)(lkzg__umu)
        overload_method(PandasTimestampType, method, no_unliteral=True)(
            lkzg__umu)


_install_freq_methods()


@register_jitable
def compute_pd_timestamp(totmicrosec, nanosecond):
    microsecond = totmicrosec % 1000000
    dseop__isdt = totmicrosec // 1000000
    second = dseop__isdt % 60
    slkny__qxm = dseop__isdt // 60
    minute = slkny__qxm % 60
    lrq__ugxd = slkny__qxm // 60
    hour = lrq__ugxd % 24
    zah__asyce = lrq__ugxd // 24
    year, month, day = _ord2ymd(zah__asyce)
    value = npy_datetimestruct_to_datetime(year, month, day, hour, minute,
        second, microsecond)
    value += zero_if_none(nanosecond)
    return init_timestamp(year, month, day, hour, minute, second,
        microsecond, nanosecond, value, None)


def overload_sub_operator_timestamp(lhs, rhs):
    if lhs == pd_timestamp_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            nsn__guxc = lhs.toordinal()
            ksa__nts = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            dszl__snp = lhs.microsecond
            nanosecond = lhs.nanosecond
            amjas__xcoj = rhs.days
            kejyy__jvlyi = rhs.seconds
            zhx__mnnn = rhs.microseconds
            lxxpj__ugyd = nsn__guxc - amjas__xcoj
            bym__iym = ksa__nts - kejyy__jvlyi
            esgmj__mtj = dszl__snp - zhx__mnnn
            totmicrosec = 1000000 * (lxxpj__ugyd * 86400 + bym__iym
                ) + esgmj__mtj
            return compute_pd_timestamp(totmicrosec, nanosecond)
        return impl
    if lhs == pd_timestamp_type and rhs == pd_timestamp_type:

        def impl_timestamp(lhs, rhs):
            return convert_numpy_timedelta64_to_pd_timedelta(lhs.value -
                rhs.value)
        return impl_timestamp
    if lhs == pd_timestamp_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


def overload_add_operator_timestamp(lhs, rhs):
    if lhs == pd_timestamp_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            nsn__guxc = lhs.toordinal()
            ksa__nts = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            dszl__snp = lhs.microsecond
            nanosecond = lhs.nanosecond
            amjas__xcoj = rhs.days
            kejyy__jvlyi = rhs.seconds
            zhx__mnnn = rhs.microseconds
            lxxpj__ugyd = nsn__guxc + amjas__xcoj
            bym__iym = ksa__nts + kejyy__jvlyi
            esgmj__mtj = dszl__snp + zhx__mnnn
            totmicrosec = 1000000 * (lxxpj__ugyd * 86400 + bym__iym
                ) + esgmj__mtj
            return compute_pd_timestamp(totmicrosec, nanosecond)
        return impl
    if lhs == pd_timestamp_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            nsn__guxc = lhs.toordinal()
            ksa__nts = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            dszl__snp = lhs.microsecond
            iir__ter = lhs.nanosecond
            zhx__mnnn = rhs.value // 1000
            ocnqz__vrs = rhs.nanoseconds
            esgmj__mtj = dszl__snp + zhx__mnnn
            totmicrosec = 1000000 * (nsn__guxc * 86400 + ksa__nts) + esgmj__mtj
            ddv__odcw = iir__ter + ocnqz__vrs
            return compute_pd_timestamp(totmicrosec, ddv__odcw)
        return impl
    if (lhs == pd_timedelta_type and rhs == pd_timestamp_type or lhs ==
        datetime_timedelta_type and rhs == pd_timestamp_type):

        def impl(lhs, rhs):
            return rhs + lhs
        return impl


@overload(min, no_unliteral=True)
def timestamp_min(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.min()')
    check_tz_aware_unsupported(rhs, f'Timestamp.min()')
    if lhs == pd_timestamp_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def timestamp_max(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.max()')
    check_tz_aware_unsupported(rhs, f'Timestamp.max()')
    if lhs == pd_timestamp_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, 'strftime')
@overload_method(PandasTimestampType, 'strftime')
def strftime(ts, format):
    if isinstance(ts, DatetimeDateType):
        sotyh__nedcr = 'datetime.date'
    else:
        sotyh__nedcr = 'pandas.Timestamp'
    if types.unliteral(format) != types.unicode_type:
        raise BodoError(
            f"{sotyh__nedcr}.strftime(): 'strftime' argument must be a string")

    def impl(ts, format):
        with numba.objmode(res='unicode_type'):
            res = ts.strftime(format)
        return res
    return impl


@overload_method(PandasTimestampType, 'to_datetime64')
def to_datetime64(ts):

    def impl(ts):
        return integer_to_dt64(ts.value)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='pd_timestamp_type'):
        d = pd.Timestamp.now()
    return d


class CompDT64(ConcreteTemplate):
    cases = [signature(types.boolean, types.NPDatetime('ns'), types.
        NPDatetime('ns'))]


@infer_global(operator.lt)
class CmpOpLt(CompDT64):
    key = operator.lt


@infer_global(operator.le)
class CmpOpLe(CompDT64):
    key = operator.le


@infer_global(operator.gt)
class CmpOpGt(CompDT64):
    key = operator.gt


@infer_global(operator.ge)
class CmpOpGe(CompDT64):
    key = operator.ge


@infer_global(operator.eq)
class CmpOpEq(CompDT64):
    key = operator.eq


@infer_global(operator.ne)
class CmpOpNe(CompDT64):
    key = operator.ne


@typeof_impl.register(calendar._localized_month)
def typeof_python_calendar(val, c):
    return types.Tuple([types.StringLiteral(konrc__olwnt) for konrc__olwnt in
        val])


@overload(str)
def overload_datetime64_str(val):
    if val == bodo.datetime64ns:

        def impl(val):
            return (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(val).isoformat('T'))
        return impl


timestamp_unsupported_attrs = ['asm8', 'components', 'freqstr', 'tz',
    'fold', 'tzinfo', 'freq']
timestamp_unsupported_methods = ['astimezone', 'ctime', 'dst', 'isoweekday',
    'replace', 'strptime', 'time', 'timestamp', 'timetuple', 'timetz',
    'to_julian_date', 'to_numpy', 'to_period', 'to_pydatetime', 'tzname',
    'utcoffset', 'utctimetuple']


def _install_pd_timestamp_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for qoqsf__lhvf in timestamp_unsupported_attrs:
        rqhe__plckd = 'pandas.Timestamp.' + qoqsf__lhvf
        overload_attribute(PandasTimestampType, qoqsf__lhvf)(
            create_unsupported_overload(rqhe__plckd))
    for jao__vycn in timestamp_unsupported_methods:
        rqhe__plckd = 'pandas.Timestamp.' + jao__vycn
        overload_method(PandasTimestampType, jao__vycn)(
            create_unsupported_overload(rqhe__plckd + '()'))


_install_pd_timestamp_unsupported()


@lower_builtin(numba.core.types.functions.NumberClass, pd_timestamp_type,
    types.StringLiteral)
def datetime64_constructor(context, builder, sig, args):

    def datetime64_constructor_impl(a, b):
        return integer_to_dt64(a.value)
    return context.compile_internal(builder, datetime64_constructor_impl,
        sig, args)
