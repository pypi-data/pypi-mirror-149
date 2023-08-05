import datetime
import numba
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
"""
Implementation is based on
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""


class DatetimeDatetimeType(types.Type):

    def __init__(self):
        super(DatetimeDatetimeType, self).__init__(name=
            'DatetimeDatetimeType()')


datetime_datetime_type = DatetimeDatetimeType()
types.datetime_datetime_type = datetime_datetime_type


@typeof_impl.register(datetime.datetime)
def typeof_datetime_datetime(val, c):
    return datetime_datetime_type


@register_model(DatetimeDatetimeType)
class DatetimeDateTimeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qfgqp__whpc = [('year', types.int64), ('month', types.int64), (
            'day', types.int64), ('hour', types.int64), ('minute', types.
            int64), ('second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, qfgqp__whpc)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    aoxuk__mbif = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    zmi__zyav = c.pyapi.long_from_longlong(aoxuk__mbif.year)
    nyfdx__lgwex = c.pyapi.long_from_longlong(aoxuk__mbif.month)
    nbhd__mhmt = c.pyapi.long_from_longlong(aoxuk__mbif.day)
    tclrl__khmr = c.pyapi.long_from_longlong(aoxuk__mbif.hour)
    vobrr__jma = c.pyapi.long_from_longlong(aoxuk__mbif.minute)
    llcfi__ovcej = c.pyapi.long_from_longlong(aoxuk__mbif.second)
    apdx__wllnj = c.pyapi.long_from_longlong(aoxuk__mbif.microsecond)
    jhr__fie = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime))
    lmv__vstk = c.pyapi.call_function_objargs(jhr__fie, (zmi__zyav,
        nyfdx__lgwex, nbhd__mhmt, tclrl__khmr, vobrr__jma, llcfi__ovcej,
        apdx__wllnj))
    c.pyapi.decref(zmi__zyav)
    c.pyapi.decref(nyfdx__lgwex)
    c.pyapi.decref(nbhd__mhmt)
    c.pyapi.decref(tclrl__khmr)
    c.pyapi.decref(vobrr__jma)
    c.pyapi.decref(llcfi__ovcej)
    c.pyapi.decref(apdx__wllnj)
    c.pyapi.decref(jhr__fie)
    return lmv__vstk


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    zmi__zyav = c.pyapi.object_getattr_string(val, 'year')
    nyfdx__lgwex = c.pyapi.object_getattr_string(val, 'month')
    nbhd__mhmt = c.pyapi.object_getattr_string(val, 'day')
    tclrl__khmr = c.pyapi.object_getattr_string(val, 'hour')
    vobrr__jma = c.pyapi.object_getattr_string(val, 'minute')
    llcfi__ovcej = c.pyapi.object_getattr_string(val, 'second')
    apdx__wllnj = c.pyapi.object_getattr_string(val, 'microsecond')
    aoxuk__mbif = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    aoxuk__mbif.year = c.pyapi.long_as_longlong(zmi__zyav)
    aoxuk__mbif.month = c.pyapi.long_as_longlong(nyfdx__lgwex)
    aoxuk__mbif.day = c.pyapi.long_as_longlong(nbhd__mhmt)
    aoxuk__mbif.hour = c.pyapi.long_as_longlong(tclrl__khmr)
    aoxuk__mbif.minute = c.pyapi.long_as_longlong(vobrr__jma)
    aoxuk__mbif.second = c.pyapi.long_as_longlong(llcfi__ovcej)
    aoxuk__mbif.microsecond = c.pyapi.long_as_longlong(apdx__wllnj)
    c.pyapi.decref(zmi__zyav)
    c.pyapi.decref(nyfdx__lgwex)
    c.pyapi.decref(nbhd__mhmt)
    c.pyapi.decref(tclrl__khmr)
    c.pyapi.decref(vobrr__jma)
    c.pyapi.decref(llcfi__ovcej)
    c.pyapi.decref(apdx__wllnj)
    gttjg__qrf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(aoxuk__mbif._getvalue(), is_error=gttjg__qrf)


@lower_constant(DatetimeDatetimeType)
def constant_datetime(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    return lir.Constant.literal_struct([year, month, day, hour, minute,
        second, microsecond])


@overload(datetime.datetime, no_unliteral=True)
def datetime_datetime(year, month, day, hour=0, minute=0, second=0,
    microsecond=0):

    def impl_datetime(year, month, day, hour=0, minute=0, second=0,
        microsecond=0):
        return init_datetime(year, month, day, hour, minute, second,
            microsecond)
    return impl_datetime


@intrinsic
def init_datetime(typingctx, year, month, day, hour, minute, second,
    microsecond):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        aoxuk__mbif = cgutils.create_struct_proxy(typ)(context, builder)
        aoxuk__mbif.year = args[0]
        aoxuk__mbif.month = args[1]
        aoxuk__mbif.day = args[2]
        aoxuk__mbif.hour = args[3]
        aoxuk__mbif.minute = args[4]
        aoxuk__mbif.second = args[5]
        aoxuk__mbif.microsecond = args[6]
        return aoxuk__mbif._getvalue()
    return DatetimeDatetimeType()(year, month, day, hour, minute, second,
        microsecond), codegen


make_attribute_wrapper(DatetimeDatetimeType, 'year', '_year')
make_attribute_wrapper(DatetimeDatetimeType, 'month', '_month')
make_attribute_wrapper(DatetimeDatetimeType, 'day', '_day')
make_attribute_wrapper(DatetimeDatetimeType, 'hour', '_hour')
make_attribute_wrapper(DatetimeDatetimeType, 'minute', '_minute')
make_attribute_wrapper(DatetimeDatetimeType, 'second', '_second')
make_attribute_wrapper(DatetimeDatetimeType, 'microsecond', '_microsecond')


@overload_attribute(DatetimeDatetimeType, 'year')
def datetime_get_year(dt):

    def impl(dt):
        return dt._year
    return impl


@overload_attribute(DatetimeDatetimeType, 'month')
def datetime_get_month(dt):

    def impl(dt):
        return dt._month
    return impl


@overload_attribute(DatetimeDatetimeType, 'day')
def datetime_get_day(dt):

    def impl(dt):
        return dt._day
    return impl


@overload_attribute(DatetimeDatetimeType, 'hour')
def datetime_get_hour(dt):

    def impl(dt):
        return dt._hour
    return impl


@overload_attribute(DatetimeDatetimeType, 'minute')
def datetime_get_minute(dt):

    def impl(dt):
        return dt._minute
    return impl


@overload_attribute(DatetimeDatetimeType, 'second')
def datetime_get_second(dt):

    def impl(dt):
        return dt._second
    return impl


@overload_attribute(DatetimeDatetimeType, 'microsecond')
def datetime_get_microsecond(dt):

    def impl(dt):
        return dt._microsecond
    return impl


@overload_method(DatetimeDatetimeType, 'date', no_unliteral=True)
def date(dt):

    def impl(dt):
        return datetime.date(dt.year, dt.month, dt.day)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.now()
    return d


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.today()
    return d


@register_jitable
def strptime_impl(date_string, dtformat):
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.strptime(date_string, dtformat)
    return d


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def create_cmp_op_overload(op):

    def overload_datetime_cmp(lhs, rhs):
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

            def impl(lhs, rhs):
                y, ukes__aat = lhs.year, rhs.year
                xqod__pyjlb, rrrq__vxei = lhs.month, rhs.month
                d, qfzh__knxvf = lhs.day, rhs.day
                amca__cmgw, vctg__cwz = lhs.hour, rhs.hour
                tzwo__avs, enmir__xsib = lhs.minute, rhs.minute
                xij__asba, nww__jpfdd = lhs.second, rhs.second
                dchot__btomj, xdat__pcjo = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, xqod__pyjlb, d, amca__cmgw, tzwo__avs,
                    xij__asba, dchot__btomj), (ukes__aat, rrrq__vxei,
                    qfzh__knxvf, vctg__cwz, enmir__xsib, nww__jpfdd,
                    xdat__pcjo)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            jpiy__oub = lhs.toordinal()
            wnnn__ybm = rhs.toordinal()
            pbhd__wfy = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            znts__rypp = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            bow__jne = datetime.timedelta(jpiy__oub - wnnn__ybm, pbhd__wfy -
                znts__rypp, lhs.microsecond - rhs.microsecond)
            return bow__jne
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    izj__tqq = context.make_helper(builder, fromty, value=val)
    myvpi__uua = cgutils.as_bool_bit(builder, izj__tqq.valid)
    with builder.if_else(myvpi__uua) as (jrh__fkgj, bjnt__fwyb):
        with jrh__fkgj:
            ytibz__imp = context.cast(builder, izj__tqq.data, fromty.type, toty
                )
            cmw__zsenp = builder.block
        with bjnt__fwyb:
            hbfs__ylr = numba.np.npdatetime.NAT
            xlewv__zljfl = builder.block
    lmv__vstk = builder.phi(ytibz__imp.type)
    lmv__vstk.add_incoming(ytibz__imp, cmw__zsenp)
    lmv__vstk.add_incoming(hbfs__ylr, xlewv__zljfl)
    return lmv__vstk
