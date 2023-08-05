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
        dpaz__xzruf = [('year', types.int64), ('month', types.int64), (
            'day', types.int64), ('hour', types.int64), ('minute', types.
            int64), ('second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, dpaz__xzruf)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    veyim__fmnuf = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    cygz__vxw = c.pyapi.long_from_longlong(veyim__fmnuf.year)
    jph__lftb = c.pyapi.long_from_longlong(veyim__fmnuf.month)
    vvfcw__pgw = c.pyapi.long_from_longlong(veyim__fmnuf.day)
    hghnk__dvqws = c.pyapi.long_from_longlong(veyim__fmnuf.hour)
    qop__jncmd = c.pyapi.long_from_longlong(veyim__fmnuf.minute)
    mej__htmgm = c.pyapi.long_from_longlong(veyim__fmnuf.second)
    zrrv__dmwe = c.pyapi.long_from_longlong(veyim__fmnuf.microsecond)
    nvzy__fnsmy = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    obh__zjsto = c.pyapi.call_function_objargs(nvzy__fnsmy, (cygz__vxw,
        jph__lftb, vvfcw__pgw, hghnk__dvqws, qop__jncmd, mej__htmgm,
        zrrv__dmwe))
    c.pyapi.decref(cygz__vxw)
    c.pyapi.decref(jph__lftb)
    c.pyapi.decref(vvfcw__pgw)
    c.pyapi.decref(hghnk__dvqws)
    c.pyapi.decref(qop__jncmd)
    c.pyapi.decref(mej__htmgm)
    c.pyapi.decref(zrrv__dmwe)
    c.pyapi.decref(nvzy__fnsmy)
    return obh__zjsto


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    cygz__vxw = c.pyapi.object_getattr_string(val, 'year')
    jph__lftb = c.pyapi.object_getattr_string(val, 'month')
    vvfcw__pgw = c.pyapi.object_getattr_string(val, 'day')
    hghnk__dvqws = c.pyapi.object_getattr_string(val, 'hour')
    qop__jncmd = c.pyapi.object_getattr_string(val, 'minute')
    mej__htmgm = c.pyapi.object_getattr_string(val, 'second')
    zrrv__dmwe = c.pyapi.object_getattr_string(val, 'microsecond')
    veyim__fmnuf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    veyim__fmnuf.year = c.pyapi.long_as_longlong(cygz__vxw)
    veyim__fmnuf.month = c.pyapi.long_as_longlong(jph__lftb)
    veyim__fmnuf.day = c.pyapi.long_as_longlong(vvfcw__pgw)
    veyim__fmnuf.hour = c.pyapi.long_as_longlong(hghnk__dvqws)
    veyim__fmnuf.minute = c.pyapi.long_as_longlong(qop__jncmd)
    veyim__fmnuf.second = c.pyapi.long_as_longlong(mej__htmgm)
    veyim__fmnuf.microsecond = c.pyapi.long_as_longlong(zrrv__dmwe)
    c.pyapi.decref(cygz__vxw)
    c.pyapi.decref(jph__lftb)
    c.pyapi.decref(vvfcw__pgw)
    c.pyapi.decref(hghnk__dvqws)
    c.pyapi.decref(qop__jncmd)
    c.pyapi.decref(mej__htmgm)
    c.pyapi.decref(zrrv__dmwe)
    mkfn__mkd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(veyim__fmnuf._getvalue(), is_error=mkfn__mkd)


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
        veyim__fmnuf = cgutils.create_struct_proxy(typ)(context, builder)
        veyim__fmnuf.year = args[0]
        veyim__fmnuf.month = args[1]
        veyim__fmnuf.day = args[2]
        veyim__fmnuf.hour = args[3]
        veyim__fmnuf.minute = args[4]
        veyim__fmnuf.second = args[5]
        veyim__fmnuf.microsecond = args[6]
        return veyim__fmnuf._getvalue()
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
                y, yesls__ydho = lhs.year, rhs.year
                khbq__alaj, qins__xqmn = lhs.month, rhs.month
                d, mzuwl__uzb = lhs.day, rhs.day
                keo__hyxa, dmfyo__cnzt = lhs.hour, rhs.hour
                sijvx__cjw, xeys__owbsr = lhs.minute, rhs.minute
                ztny__fkhco, ldq__usaj = lhs.second, rhs.second
                phs__zuk, ctzzd__nbj = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, khbq__alaj, d, keo__hyxa, sijvx__cjw,
                    ztny__fkhco, phs__zuk), (yesls__ydho, qins__xqmn,
                    mzuwl__uzb, dmfyo__cnzt, xeys__owbsr, ldq__usaj,
                    ctzzd__nbj)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            grku__exwng = lhs.toordinal()
            nen__cshyl = rhs.toordinal()
            omr__pmzhe = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            nwpco__bfj = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            dvn__www = datetime.timedelta(grku__exwng - nen__cshyl, 
                omr__pmzhe - nwpco__bfj, lhs.microsecond - rhs.microsecond)
            return dvn__www
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    rtfwg__ozsqv = context.make_helper(builder, fromty, value=val)
    lrkp__ryp = cgutils.as_bool_bit(builder, rtfwg__ozsqv.valid)
    with builder.if_else(lrkp__ryp) as (jezme__xjmu, mvb__csbmu):
        with jezme__xjmu:
            jabkw__fnsgy = context.cast(builder, rtfwg__ozsqv.data, fromty.
                type, toty)
            apj__tmkv = builder.block
        with mvb__csbmu:
            yzs__wsjqr = numba.np.npdatetime.NAT
            vuya__tdby = builder.block
    obh__zjsto = builder.phi(jabkw__fnsgy.type)
    obh__zjsto.add_incoming(jabkw__fnsgy, apj__tmkv)
    obh__zjsto.add_incoming(yzs__wsjqr, vuya__tdby)
    return obh__zjsto
