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
        bukf__nhl = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, bukf__nhl)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    smp__yft = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    odhsv__mdn = c.pyapi.long_from_longlong(smp__yft.year)
    gblm__xnis = c.pyapi.long_from_longlong(smp__yft.month)
    udzdy__ttpg = c.pyapi.long_from_longlong(smp__yft.day)
    hdhxr__jqc = c.pyapi.long_from_longlong(smp__yft.hour)
    eltod__xxh = c.pyapi.long_from_longlong(smp__yft.minute)
    bmo__thjj = c.pyapi.long_from_longlong(smp__yft.second)
    ujlm__pzaom = c.pyapi.long_from_longlong(smp__yft.microsecond)
    ftkw__ytmj = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    pntyz__bbr = c.pyapi.call_function_objargs(ftkw__ytmj, (odhsv__mdn,
        gblm__xnis, udzdy__ttpg, hdhxr__jqc, eltod__xxh, bmo__thjj,
        ujlm__pzaom))
    c.pyapi.decref(odhsv__mdn)
    c.pyapi.decref(gblm__xnis)
    c.pyapi.decref(udzdy__ttpg)
    c.pyapi.decref(hdhxr__jqc)
    c.pyapi.decref(eltod__xxh)
    c.pyapi.decref(bmo__thjj)
    c.pyapi.decref(ujlm__pzaom)
    c.pyapi.decref(ftkw__ytmj)
    return pntyz__bbr


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    odhsv__mdn = c.pyapi.object_getattr_string(val, 'year')
    gblm__xnis = c.pyapi.object_getattr_string(val, 'month')
    udzdy__ttpg = c.pyapi.object_getattr_string(val, 'day')
    hdhxr__jqc = c.pyapi.object_getattr_string(val, 'hour')
    eltod__xxh = c.pyapi.object_getattr_string(val, 'minute')
    bmo__thjj = c.pyapi.object_getattr_string(val, 'second')
    ujlm__pzaom = c.pyapi.object_getattr_string(val, 'microsecond')
    smp__yft = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    smp__yft.year = c.pyapi.long_as_longlong(odhsv__mdn)
    smp__yft.month = c.pyapi.long_as_longlong(gblm__xnis)
    smp__yft.day = c.pyapi.long_as_longlong(udzdy__ttpg)
    smp__yft.hour = c.pyapi.long_as_longlong(hdhxr__jqc)
    smp__yft.minute = c.pyapi.long_as_longlong(eltod__xxh)
    smp__yft.second = c.pyapi.long_as_longlong(bmo__thjj)
    smp__yft.microsecond = c.pyapi.long_as_longlong(ujlm__pzaom)
    c.pyapi.decref(odhsv__mdn)
    c.pyapi.decref(gblm__xnis)
    c.pyapi.decref(udzdy__ttpg)
    c.pyapi.decref(hdhxr__jqc)
    c.pyapi.decref(eltod__xxh)
    c.pyapi.decref(bmo__thjj)
    c.pyapi.decref(ujlm__pzaom)
    dqv__mnk = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(smp__yft._getvalue(), is_error=dqv__mnk)


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
        smp__yft = cgutils.create_struct_proxy(typ)(context, builder)
        smp__yft.year = args[0]
        smp__yft.month = args[1]
        smp__yft.day = args[2]
        smp__yft.hour = args[3]
        smp__yft.minute = args[4]
        smp__yft.second = args[5]
        smp__yft.microsecond = args[6]
        return smp__yft._getvalue()
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
                y, tuhvf__blf = lhs.year, rhs.year
                idi__dedc, ljfys__huf = lhs.month, rhs.month
                d, hfly__ceyto = lhs.day, rhs.day
                eba__dynm, nnqqj__qpk = lhs.hour, rhs.hour
                lkq__zgln, ujz__jrmh = lhs.minute, rhs.minute
                uuo__bcb, jpjug__gid = lhs.second, rhs.second
                zspl__dclb, bjpu__dnns = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, idi__dedc, d, eba__dynm, lkq__zgln,
                    uuo__bcb, zspl__dclb), (tuhvf__blf, ljfys__huf,
                    hfly__ceyto, nnqqj__qpk, ujz__jrmh, jpjug__gid,
                    bjpu__dnns)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            jblt__tjkpe = lhs.toordinal()
            cgbml__thzsd = rhs.toordinal()
            eedy__ubhy = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            cle__pqvnz = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            jsyj__hfa = datetime.timedelta(jblt__tjkpe - cgbml__thzsd, 
                eedy__ubhy - cle__pqvnz, lhs.microsecond - rhs.microsecond)
            return jsyj__hfa
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    cgpgx__msrir = context.make_helper(builder, fromty, value=val)
    qopjs__ufea = cgutils.as_bool_bit(builder, cgpgx__msrir.valid)
    with builder.if_else(qopjs__ufea) as (kft__aau, ash__vgg):
        with kft__aau:
            amf__xstdu = context.cast(builder, cgpgx__msrir.data, fromty.
                type, toty)
            ovqlj__pljgv = builder.block
        with ash__vgg:
            gxmv__qepkn = numba.np.npdatetime.NAT
            ysw__uaang = builder.block
    pntyz__bbr = builder.phi(amf__xstdu.type)
    pntyz__bbr.add_incoming(amf__xstdu, ovqlj__pljgv)
    pntyz__bbr.add_incoming(gxmv__qepkn, ysw__uaang)
    return pntyz__bbr
