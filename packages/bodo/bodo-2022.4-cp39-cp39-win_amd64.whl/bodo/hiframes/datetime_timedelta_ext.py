"""Numba extension support for datetime.timedelta objects and their arrays.
"""
import datetime
import operator
from collections import namedtuple
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import get_new_null_mask_bool_index, get_new_null_mask_int_index, get_new_null_mask_slice_index, setitem_slice_index_null_bits
from bodo.utils.typing import BodoError, get_overload_const_str, is_iterable_type, is_list_like_index_type, is_overload_constant_str
ll.add_symbol('box_datetime_timedelta_array', hdatetime_ext.
    box_datetime_timedelta_array)
ll.add_symbol('unbox_datetime_timedelta_array', hdatetime_ext.
    unbox_datetime_timedelta_array)


class NoInput:
    pass


_no_input = NoInput()


class NoInputType(types.Type):

    def __init__(self):
        super(NoInputType, self).__init__(name='NoInput')


register_model(NoInputType)(models.OpaqueModel)


@typeof_impl.register(NoInput)
def _typ_no_input(val, c):
    return NoInputType()


@lower_constant(NoInputType)
def constant_no_input(context, builder, ty, pyval):
    return context.get_dummy_value()


class PDTimeDeltaType(types.Type):

    def __init__(self):
        super(PDTimeDeltaType, self).__init__(name='PDTimeDeltaType()')


pd_timedelta_type = PDTimeDeltaType()
types.pd_timedelta_type = pd_timedelta_type


@typeof_impl.register(pd.Timedelta)
def typeof_pd_timedelta(val, c):
    return pd_timedelta_type


@register_model(PDTimeDeltaType)
class PDTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ebme__iebbw = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, ebme__iebbw)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    vcpgb__xglpb = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    vvn__cce = c.pyapi.long_from_longlong(vcpgb__xglpb.value)
    yqyoj__phly = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(yqyoj__phly, (vvn__cce,))
    c.pyapi.decref(vvn__cce)
    c.pyapi.decref(yqyoj__phly)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    vvn__cce = c.pyapi.object_getattr_string(val, 'value')
    nxzzg__ecajp = c.pyapi.long_as_longlong(vvn__cce)
    vcpgb__xglpb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vcpgb__xglpb.value = nxzzg__ecajp
    c.pyapi.decref(vvn__cce)
    bueh__jkv = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(vcpgb__xglpb._getvalue(), is_error=bueh__jkv)


@lower_constant(PDTimeDeltaType)
def lower_constant_pd_timedelta(context, builder, ty, pyval):
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct([value])


@overload(pd.Timedelta, no_unliteral=True)
def pd_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
    microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    if value == _no_input:

        def impl_timedelta_kw(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            days += weeks * 7
            hours += days * 24
            minutes += 60 * hours
            seconds += 60 * minutes
            milliseconds += 1000 * seconds
            microseconds += 1000 * milliseconds
            ngo__aqc = 1000 * microseconds
            return init_pd_timedelta(ngo__aqc)
        return impl_timedelta_kw
    if value == bodo.string_type or is_overload_constant_str(value):

        def impl_str(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            with numba.objmode(res='pd_timedelta_type'):
                res = pd.Timedelta(value)
            return res
        return impl_str
    if value == pd_timedelta_type:
        return (lambda value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0: value)
    if value == datetime_timedelta_type:

        def impl_timedelta_datetime(value=_no_input, unit='ns', days=0,
            seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
            weeks=0):
            days = value.days
            seconds = 60 * 60 * 24 * days + value.seconds
            microseconds = 1000 * 1000 * seconds + value.microseconds
            ngo__aqc = 1000 * microseconds
            return init_pd_timedelta(ngo__aqc)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    dohy__lpet, arx__smhs = pd._libs.tslibs.conversion.precision_from_unit(unit
        )

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * dohy__lpet)
    return impl_timedelta


@intrinsic
def init_pd_timedelta(typingctx, value):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.value = args[0]
        return timedelta._getvalue()
    return PDTimeDeltaType()(value), codegen


make_attribute_wrapper(PDTimeDeltaType, 'value', '_value')


@overload_attribute(PDTimeDeltaType, 'value')
@overload_attribute(PDTimeDeltaType, 'delta')
def pd_timedelta_get_value(td):

    def impl(td):
        return td._value
    return impl


@overload_attribute(PDTimeDeltaType, 'days')
def pd_timedelta_get_days(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000 * 60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'seconds')
def pd_timedelta_get_seconds(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000) % (60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'microseconds')
def pd_timedelta_get_microseconds(td):

    def impl(td):
        return td._value // 1000 % 1000000
    return impl


@overload_attribute(PDTimeDeltaType, 'nanoseconds')
def pd_timedelta_get_nanoseconds(td):

    def impl(td):
        return td._value % 1000
    return impl


@register_jitable
def _to_hours_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60 * 60) % 24


@register_jitable
def _to_minutes_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60) % 60


@register_jitable
def _to_seconds_pd_td(td):
    return td._value // (1000 * 1000 * 1000) % 60


@register_jitable
def _to_milliseconds_pd_td(td):
    return td._value // (1000 * 1000) % 1000


@register_jitable
def _to_microseconds_pd_td(td):
    return td._value // 1000 % 1000


Components = namedtuple('Components', ['days', 'hours', 'minutes',
    'seconds', 'milliseconds', 'microseconds', 'nanoseconds'], defaults=[0,
    0, 0, 0, 0, 0, 0])


@overload_attribute(PDTimeDeltaType, 'components', no_unliteral=True)
def pd_timedelta_get_components(td):

    def impl(td):
        a = Components(td.days, _to_hours_pd_td(td), _to_minutes_pd_td(td),
            _to_seconds_pd_td(td), _to_milliseconds_pd_td(td),
            _to_microseconds_pd_td(td), td.nanoseconds)
        return a
    return impl


@overload_method(PDTimeDeltaType, '__hash__', no_unliteral=True)
def pd_td___hash__(td):

    def impl(td):
        return hash(td._value)
    return impl


@overload_method(PDTimeDeltaType, 'to_numpy', no_unliteral=True)
@overload_method(PDTimeDeltaType, 'to_timedelta64', no_unliteral=True)
def pd_td_to_numpy(td):
    from bodo.hiframes.pd_timestamp_ext import integer_to_timedelta64

    def impl(td):
        return integer_to_timedelta64(td.value)
    return impl


@overload_method(PDTimeDeltaType, 'to_pytimedelta', no_unliteral=True)
def pd_td_to_pytimedelta(td):

    def impl(td):
        return datetime.timedelta(microseconds=np.int64(td._value / 1000))
    return impl


@overload_method(PDTimeDeltaType, 'total_seconds', no_unliteral=True)
def pd_td_total_seconds(td):

    def impl(td):
        return td._value // 1000 / 10 ** 6
    return impl


def overload_add_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            val = lhs.value + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            igryn__ifd = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + igryn__ifd
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            iirdy__lxp = (lhs.microseconds + (lhs.seconds + lhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = iirdy__lxp + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            hale__nhfi = rhs.toordinal()
            msqq__bjmt = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            clph__amzq = rhs.microsecond
            jdlqa__xrf = lhs.value // 1000
            fihcf__rpaf = lhs.nanoseconds
            rgav__trt = clph__amzq + jdlqa__xrf
            evdz__rygpu = 1000000 * (hale__nhfi * 86400 + msqq__bjmt
                ) + rgav__trt
            kfr__halvj = fihcf__rpaf
            return compute_pd_timestamp(evdz__rygpu, kfr__halvj)
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + rhs.to_pytimedelta()
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days + rhs.days
            s = lhs.seconds + rhs.seconds
            us = lhs.microseconds + rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            sdyya__lub = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            sdyya__lub = sdyya__lub + lhs
            msno__lwbm, nfy__ytby = divmod(sdyya__lub.seconds, 3600)
            mqg__vjdtz, srbvp__jehof = divmod(nfy__ytby, 60)
            if 0 < sdyya__lub.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(sdyya__lub
                    .days)
                return datetime.datetime(d.year, d.month, d.day, msno__lwbm,
                    mqg__vjdtz, srbvp__jehof, sdyya__lub.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            sdyya__lub = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            sdyya__lub = sdyya__lub + rhs
            msno__lwbm, nfy__ytby = divmod(sdyya__lub.seconds, 3600)
            mqg__vjdtz, srbvp__jehof = divmod(nfy__ytby, 60)
            if 0 < sdyya__lub.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(sdyya__lub
                    .days)
                return datetime.datetime(d.year, d.month, d.day, msno__lwbm,
                    mqg__vjdtz, srbvp__jehof, sdyya__lub.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            qdeek__avff = lhs.value - rhs.value
            return pd.Timedelta(qdeek__avff)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days - rhs.days
            s = lhs.seconds - rhs.seconds
            us = lhs.microseconds - rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            lwdw__nfod = lhs
            numba.parfors.parfor.init_prange()
            n = len(lwdw__nfod)
            A = alloc_datetime_timedelta_array(n)
            for unn__twuuh in numba.parfors.parfor.internal_prange(n):
                A[unn__twuuh] = lwdw__nfod[unn__twuuh] - rhs
            return A
        return impl


def overload_mul_operator_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value * rhs)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(rhs.value * lhs)
        return impl
    if lhs == datetime_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            d = lhs.days * rhs
            s = lhs.seconds * rhs
            us = lhs.microseconds * rhs
            return datetime.timedelta(d, s, us)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs * rhs.days
            s = lhs * rhs.seconds
            us = lhs * rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl


def overload_floordiv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value // rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value // rhs)
        return impl


def overload_truediv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value / rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(int(lhs.value / rhs))
        return impl


def overload_mod_operator_timedeltas(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value % rhs.value)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            jrs__makdi = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, jrs__makdi)
        return impl


def pd_create_cmp_op_overload(op):

    def overload_pd_timedelta_cmp(lhs, rhs):
        if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

            def impl(lhs, rhs):
                return op(lhs.value, rhs.value)
            return impl
        if lhs == pd_timedelta_type and rhs == bodo.timedelta64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(lhs.value), rhs)
        if lhs == bodo.timedelta64ns and rhs == pd_timedelta_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(rhs.value))
    return overload_pd_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def pd_timedelta_neg(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return pd.Timedelta(-lhs.value)
        return impl


@overload(operator.pos, no_unliteral=True)
def pd_timedelta_pos(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def pd_timedelta_divmod(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            schdh__zpb, jrs__makdi = divmod(lhs.value, rhs.value)
            return schdh__zpb, pd.Timedelta(jrs__makdi)
        return impl


@overload(abs, no_unliteral=True)
def pd_timedelta_abs(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            if lhs.value < 0:
                return -lhs
            else:
                return lhs
        return impl


class DatetimeTimeDeltaType(types.Type):

    def __init__(self):
        super(DatetimeTimeDeltaType, self).__init__(name=
            'DatetimeTimeDeltaType()')


datetime_timedelta_type = DatetimeTimeDeltaType()


@typeof_impl.register(datetime.timedelta)
def typeof_datetime_timedelta(val, c):
    return datetime_timedelta_type


@register_model(DatetimeTimeDeltaType)
class DatetimeTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ebme__iebbw = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, ebme__iebbw)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    vcpgb__xglpb = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    cqpwl__lkft = c.pyapi.long_from_longlong(vcpgb__xglpb.days)
    axdc__ilno = c.pyapi.long_from_longlong(vcpgb__xglpb.seconds)
    vtfef__hfzyp = c.pyapi.long_from_longlong(vcpgb__xglpb.microseconds)
    yqyoj__phly = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(yqyoj__phly, (cqpwl__lkft,
        axdc__ilno, vtfef__hfzyp))
    c.pyapi.decref(cqpwl__lkft)
    c.pyapi.decref(axdc__ilno)
    c.pyapi.decref(vtfef__hfzyp)
    c.pyapi.decref(yqyoj__phly)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    cqpwl__lkft = c.pyapi.object_getattr_string(val, 'days')
    axdc__ilno = c.pyapi.object_getattr_string(val, 'seconds')
    vtfef__hfzyp = c.pyapi.object_getattr_string(val, 'microseconds')
    tduhb__wziav = c.pyapi.long_as_longlong(cqpwl__lkft)
    hdl__uigv = c.pyapi.long_as_longlong(axdc__ilno)
    zrrc__tdu = c.pyapi.long_as_longlong(vtfef__hfzyp)
    vcpgb__xglpb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vcpgb__xglpb.days = tduhb__wziav
    vcpgb__xglpb.seconds = hdl__uigv
    vcpgb__xglpb.microseconds = zrrc__tdu
    c.pyapi.decref(cqpwl__lkft)
    c.pyapi.decref(axdc__ilno)
    c.pyapi.decref(vtfef__hfzyp)
    bueh__jkv = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(vcpgb__xglpb._getvalue(), is_error=bueh__jkv)


@lower_constant(DatetimeTimeDeltaType)
def lower_constant_datetime_timedelta(context, builder, ty, pyval):
    days = context.get_constant(types.int64, pyval.days)
    seconds = context.get_constant(types.int64, pyval.seconds)
    microseconds = context.get_constant(types.int64, pyval.microseconds)
    return lir.Constant.literal_struct([days, seconds, microseconds])


@overload(datetime.timedelta, no_unliteral=True)
def datetime_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0):

    def impl_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
        minutes=0, hours=0, weeks=0):
        d = s = us = 0
        days += weeks * 7
        seconds += minutes * 60 + hours * 3600
        microseconds += milliseconds * 1000
        d = days
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += int(seconds)
        seconds, us = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += seconds
        return init_timedelta(d, s, us)
    return impl_timedelta


@intrinsic
def init_timedelta(typingctx, d, s, us):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.days = args[0]
        timedelta.seconds = args[1]
        timedelta.microseconds = args[2]
        return timedelta._getvalue()
    return DatetimeTimeDeltaType()(d, s, us), codegen


make_attribute_wrapper(DatetimeTimeDeltaType, 'days', '_days')
make_attribute_wrapper(DatetimeTimeDeltaType, 'seconds', '_seconds')
make_attribute_wrapper(DatetimeTimeDeltaType, 'microseconds', '_microseconds')


@overload_attribute(DatetimeTimeDeltaType, 'days')
def timedelta_get_days(td):

    def impl(td):
        return td._days
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'seconds')
def timedelta_get_seconds(td):

    def impl(td):
        return td._seconds
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'microseconds')
def timedelta_get_microseconds(td):

    def impl(td):
        return td._microseconds
    return impl


@overload_method(DatetimeTimeDeltaType, 'total_seconds', no_unliteral=True)
def total_seconds(td):

    def impl(td):
        return ((td._days * 86400 + td._seconds) * 10 ** 6 + td._microseconds
            ) / 10 ** 6
    return impl


@overload_method(DatetimeTimeDeltaType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        return hash((td._days, td._seconds, td._microseconds))
    return impl


@register_jitable
def _to_nanoseconds(td):
    return np.int64(((td._days * 86400 + td._seconds) * 1000000 + td.
        _microseconds) * 1000)


@register_jitable
def _to_microseconds(td):
    return (td._days * (24 * 3600) + td._seconds) * 1000000 + td._microseconds


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@register_jitable
def _getstate(td):
    return td._days, td._seconds, td._microseconds


@register_jitable
def _divide_and_round(a, b):
    schdh__zpb, jrs__makdi = divmod(a, b)
    jrs__makdi *= 2
    yno__ipuhi = jrs__makdi > b if b > 0 else jrs__makdi < b
    if yno__ipuhi or jrs__makdi == b and schdh__zpb % 2 == 1:
        schdh__zpb += 1
    return schdh__zpb


_MAXORDINAL = 3652059


def overload_floordiv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us // _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, us // rhs)
        return impl


def overload_truediv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us / _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, _divide_and_round(us, rhs))
        return impl


def create_cmp_op_overload(op):

    def overload_timedelta_cmp(lhs, rhs):
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

            def impl(lhs, rhs):
                hpwd__mctr = _cmp(_getstate(lhs), _getstate(rhs))
                return op(hpwd__mctr, 0)
            return impl
    return overload_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def timedelta_neg(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return datetime.timedelta(-lhs.days, -lhs.seconds, -lhs.
                microseconds)
        return impl


@overload(operator.pos, no_unliteral=True)
def timedelta_pos(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def timedelta_divmod(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            schdh__zpb, jrs__makdi = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return schdh__zpb, datetime.timedelta(0, 0, jrs__makdi)
        return impl


@overload(abs, no_unliteral=True)
def timedelta_abs(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            if lhs.days < 0:
                return -lhs
            else:
                return lhs
        return impl


@intrinsic
def cast_numpy_timedelta_to_int(typingctx, val=None):
    assert val in (types.NPTimedelta('ns'), types.int64)

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


@overload(bool, no_unliteral=True)
def timedelta_to_bool(timedelta):
    if timedelta != datetime_timedelta_type:
        return
    nbcno__kwo = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != nbcno__kwo
    return impl


class DatetimeTimeDeltaArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeTimeDeltaArrayType, self).__init__(name=
            'DatetimeTimeDeltaArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_timedelta_type

    def copy(self):
        return DatetimeTimeDeltaArrayType()


datetime_timedelta_array_type = DatetimeTimeDeltaArrayType()
types.datetime_timedelta_array_type = datetime_timedelta_array_type
days_data_type = types.Array(types.int64, 1, 'C')
seconds_data_type = types.Array(types.int64, 1, 'C')
microseconds_data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeTimeDeltaArrayType)
class DatetimeTimeDeltaArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ebme__iebbw = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, ebme__iebbw)


make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'days_data', '_days_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'seconds_data',
    '_seconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'microseconds_data',
    '_microseconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'null_bitmap',
    '_null_bitmap')


@overload_method(DatetimeTimeDeltaArrayType, 'copy', no_unliteral=True)
def overload_datetime_timedelta_arr_copy(A):
    return (lambda A: bodo.hiframes.datetime_timedelta_ext.
        init_datetime_timedelta_array(A._days_data.copy(), A._seconds_data.
        copy(), A._microseconds_data.copy(), A._null_bitmap.copy()))


@unbox(DatetimeTimeDeltaArrayType)
def unbox_datetime_timedelta_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    lmc__izafu = types.Array(types.intp, 1, 'C')
    plj__dqmce = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        lmc__izafu, [n])
    qpqzc__xba = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        lmc__izafu, [n])
    mppe__mvych = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        lmc__izafu, [n])
    vwqcc__gedf = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    fbbix__gcznh = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [vwqcc__gedf])
    tpew__ycdpv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    lzsfs__jnd = cgutils.get_or_insert_function(c.builder.module,
        tpew__ycdpv, name='unbox_datetime_timedelta_array')
    c.builder.call(lzsfs__jnd, [val, n, plj__dqmce.data, qpqzc__xba.data,
        mppe__mvych.data, fbbix__gcznh.data])
    ssj__zusu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ssj__zusu.days_data = plj__dqmce._getvalue()
    ssj__zusu.seconds_data = qpqzc__xba._getvalue()
    ssj__zusu.microseconds_data = mppe__mvych._getvalue()
    ssj__zusu.null_bitmap = fbbix__gcznh._getvalue()
    bueh__jkv = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ssj__zusu._getvalue(), is_error=bueh__jkv)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    lwdw__nfod = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    plj__dqmce = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, lwdw__nfod.days_data)
    qpqzc__xba = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, lwdw__nfod.seconds_data).data
    mppe__mvych = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, lwdw__nfod.microseconds_data).data
    crswq__ozyxb = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, lwdw__nfod.null_bitmap).data
    n = c.builder.extract_value(plj__dqmce.shape, 0)
    tpew__ycdpv = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    yeyal__ashsd = cgutils.get_or_insert_function(c.builder.module,
        tpew__ycdpv, name='box_datetime_timedelta_array')
    szh__zstvz = c.builder.call(yeyal__ashsd, [n, plj__dqmce.data,
        qpqzc__xba, mppe__mvych, crswq__ozyxb])
    c.context.nrt.decref(c.builder, typ, val)
    return szh__zstvz


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        syi__vwr, vbnl__pykd, fmulz__sdd, ifw__oljn = args
        ykunb__kmjzf = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ykunb__kmjzf.days_data = syi__vwr
        ykunb__kmjzf.seconds_data = vbnl__pykd
        ykunb__kmjzf.microseconds_data = fmulz__sdd
        ykunb__kmjzf.null_bitmap = ifw__oljn
        context.nrt.incref(builder, signature.args[0], syi__vwr)
        context.nrt.incref(builder, signature.args[1], vbnl__pykd)
        context.nrt.incref(builder, signature.args[2], fmulz__sdd)
        context.nrt.incref(builder, signature.args[3], ifw__oljn)
        return ykunb__kmjzf._getvalue()
    gzxnx__ney = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return gzxnx__ney, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    plj__dqmce = np.empty(n, np.int64)
    qpqzc__xba = np.empty(n, np.int64)
    mppe__mvych = np.empty(n, np.int64)
    vct__nbr = np.empty(n + 7 >> 3, np.uint8)
    for unn__twuuh, s in enumerate(pyval):
        fkcvy__btj = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(vct__nbr, unn__twuuh, int(not
            fkcvy__btj))
        if not fkcvy__btj:
            plj__dqmce[unn__twuuh] = s.days
            qpqzc__xba[unn__twuuh] = s.seconds
            mppe__mvych[unn__twuuh] = s.microseconds
    hjevr__yftab = context.get_constant_generic(builder, days_data_type,
        plj__dqmce)
    twd__wkit = context.get_constant_generic(builder, seconds_data_type,
        qpqzc__xba)
    ixtn__ups = context.get_constant_generic(builder,
        microseconds_data_type, mppe__mvych)
    pzckc__klbj = context.get_constant_generic(builder, nulls_type, vct__nbr)
    return lir.Constant.literal_struct([hjevr__yftab, twd__wkit, ixtn__ups,
        pzckc__klbj])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    plj__dqmce = np.empty(n, dtype=np.int64)
    qpqzc__xba = np.empty(n, dtype=np.int64)
    mppe__mvych = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(plj__dqmce, qpqzc__xba,
        mppe__mvych, nulls)


def alloc_datetime_timedelta_array_equiv(self, scope, equiv_set, loc, args, kws
    ):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_timedelta_ext_alloc_datetime_timedelta_array
    ) = alloc_datetime_timedelta_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_timedelta_arr_getitem(A, ind):
    if A != datetime_timedelta_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl_int(A, ind):
            return datetime.timedelta(days=A._days_data[ind], seconds=A.
                _seconds_data[ind], microseconds=A._microseconds_data[ind])
        return impl_int
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            bgor__wiy = bodo.utils.conversion.coerce_to_ndarray(ind)
            ohvpb__xuugl = A._null_bitmap
            qludf__zcb = A._days_data[bgor__wiy]
            rzsry__mnut = A._seconds_data[bgor__wiy]
            vzjn__hojpr = A._microseconds_data[bgor__wiy]
            n = len(qludf__zcb)
            gwdtr__ggflu = get_new_null_mask_bool_index(ohvpb__xuugl, ind, n)
            return init_datetime_timedelta_array(qludf__zcb, rzsry__mnut,
                vzjn__hojpr, gwdtr__ggflu)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            bgor__wiy = bodo.utils.conversion.coerce_to_ndarray(ind)
            ohvpb__xuugl = A._null_bitmap
            qludf__zcb = A._days_data[bgor__wiy]
            rzsry__mnut = A._seconds_data[bgor__wiy]
            vzjn__hojpr = A._microseconds_data[bgor__wiy]
            n = len(qludf__zcb)
            gwdtr__ggflu = get_new_null_mask_int_index(ohvpb__xuugl,
                bgor__wiy, n)
            return init_datetime_timedelta_array(qludf__zcb, rzsry__mnut,
                vzjn__hojpr, gwdtr__ggflu)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            ohvpb__xuugl = A._null_bitmap
            qludf__zcb = np.ascontiguousarray(A._days_data[ind])
            rzsry__mnut = np.ascontiguousarray(A._seconds_data[ind])
            vzjn__hojpr = np.ascontiguousarray(A._microseconds_data[ind])
            gwdtr__ggflu = get_new_null_mask_slice_index(ohvpb__xuugl, ind, n)
            return init_datetime_timedelta_array(qludf__zcb, rzsry__mnut,
                vzjn__hojpr, gwdtr__ggflu)
        return impl_slice
    raise BodoError(
        f'getitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(operator.setitem, no_unliteral=True)
def dt_timedelta_arr_setitem(A, ind, val):
    if A != datetime_timedelta_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    broc__ftbvd = (
        f"setitem for DatetimeTimedeltaArray with indexing type {ind} received an incorrect 'value' type {val}."
        )
    if isinstance(ind, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl(A, ind, val):
                A._days_data[ind] = val._days
                A._seconds_data[ind] = val._seconds
                A._microseconds_data[ind] = val._microseconds
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, ind, 1)
            return impl
        else:
            raise BodoError(broc__ftbvd)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(broc__ftbvd)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for unn__twuuh in range(n):
                    A._days_data[ind[unn__twuuh]] = val._days
                    A._seconds_data[ind[unn__twuuh]] = val._seconds
                    A._microseconds_data[ind[unn__twuuh]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[unn__twuuh], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for unn__twuuh in range(n):
                    A._days_data[ind[unn__twuuh]] = val._days_data[unn__twuuh]
                    A._seconds_data[ind[unn__twuuh]] = val._seconds_data[
                        unn__twuuh]
                    A._microseconds_data[ind[unn__twuuh]
                        ] = val._microseconds_data[unn__twuuh]
                    nqqg__sepsc = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, unn__twuuh)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[unn__twuuh], nqqg__sepsc)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for unn__twuuh in range(n):
                    if not bodo.libs.array_kernels.isna(ind, unn__twuuh
                        ) and ind[unn__twuuh]:
                        A._days_data[unn__twuuh] = val._days
                        A._seconds_data[unn__twuuh] = val._seconds
                        A._microseconds_data[unn__twuuh] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            unn__twuuh, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                llm__dfaqm = 0
                for unn__twuuh in range(n):
                    if not bodo.libs.array_kernels.isna(ind, unn__twuuh
                        ) and ind[unn__twuuh]:
                        A._days_data[unn__twuuh] = val._days_data[llm__dfaqm]
                        A._seconds_data[unn__twuuh] = val._seconds_data[
                            llm__dfaqm]
                        A._microseconds_data[unn__twuuh
                            ] = val._microseconds_data[llm__dfaqm]
                        nqqg__sepsc = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, llm__dfaqm)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            unn__twuuh, nqqg__sepsc)
                        llm__dfaqm += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                hae__ljd = numba.cpython.unicode._normalize_slice(ind, len(A))
                for unn__twuuh in range(hae__ljd.start, hae__ljd.stop,
                    hae__ljd.step):
                    A._days_data[unn__twuuh] = val._days
                    A._seconds_data[unn__twuuh] = val._seconds
                    A._microseconds_data[unn__twuuh] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        unn__twuuh, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                fjqb__nxxho = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, fjqb__nxxho,
                    ind, n)
            return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_timedelta_arr(A):
    if A == datetime_timedelta_array_type:
        return lambda A: len(A._days_data)


@overload_attribute(DatetimeTimeDeltaArrayType, 'shape')
def overload_datetime_timedelta_arr_shape(A):
    return lambda A: (len(A._days_data),)


@overload_attribute(DatetimeTimeDeltaArrayType, 'nbytes')
def timedelta_arr_nbytes_overload(A):
    return (lambda A: A._days_data.nbytes + A._seconds_data.nbytes + A.
        _microseconds_data.nbytes + A._null_bitmap.nbytes)


def overload_datetime_timedelta_arr_sub(arg1, arg2):
    if (arg1 == datetime_timedelta_array_type and arg2 ==
        datetime_timedelta_type):

        def impl(arg1, arg2):
            lwdw__nfod = arg1
            numba.parfors.parfor.init_prange()
            n = len(lwdw__nfod)
            A = alloc_datetime_timedelta_array(n)
            for unn__twuuh in numba.parfors.parfor.internal_prange(n):
                A[unn__twuuh] = lwdw__nfod[unn__twuuh] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            bgqpu__jijh = True
        else:
            bgqpu__jijh = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                vwyc__aldh = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for unn__twuuh in numba.parfors.parfor.internal_prange(n):
                    njnx__fbefe = bodo.libs.array_kernels.isna(lhs, unn__twuuh)
                    zjnvq__bhsl = bodo.libs.array_kernels.isna(rhs, unn__twuuh)
                    if njnx__fbefe or zjnvq__bhsl:
                        irbt__qqiv = bgqpu__jijh
                    else:
                        irbt__qqiv = op(lhs[unn__twuuh], rhs[unn__twuuh])
                    vwyc__aldh[unn__twuuh] = irbt__qqiv
                return vwyc__aldh
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                vwyc__aldh = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for unn__twuuh in numba.parfors.parfor.internal_prange(n):
                    nqqg__sepsc = bodo.libs.array_kernels.isna(lhs, unn__twuuh)
                    if nqqg__sepsc:
                        irbt__qqiv = bgqpu__jijh
                    else:
                        irbt__qqiv = op(lhs[unn__twuuh], rhs)
                    vwyc__aldh[unn__twuuh] = irbt__qqiv
                return vwyc__aldh
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                vwyc__aldh = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for unn__twuuh in numba.parfors.parfor.internal_prange(n):
                    nqqg__sepsc = bodo.libs.array_kernels.isna(rhs, unn__twuuh)
                    if nqqg__sepsc:
                        irbt__qqiv = bgqpu__jijh
                    else:
                        irbt__qqiv = op(lhs, rhs[unn__twuuh])
                    vwyc__aldh[unn__twuuh] = irbt__qqiv
                return vwyc__aldh
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for jfrxg__zlh in timedelta_unsupported_attrs:
        hhla__lxsn = 'pandas.Timedelta.' + jfrxg__zlh
        overload_attribute(PDTimeDeltaType, jfrxg__zlh)(
            create_unsupported_overload(hhla__lxsn))
    for xbbr__noa in timedelta_unsupported_methods:
        hhla__lxsn = 'pandas.Timedelta.' + xbbr__noa
        overload_method(PDTimeDeltaType, xbbr__noa)(create_unsupported_overload
            (hhla__lxsn + '()'))


_intstall_pd_timedelta_unsupported()
