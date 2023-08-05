"""
Support for Series.dt attributes and methods
"""
import datetime
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_series_ext import SeriesType, get_series_data, get_series_index, get_series_name, init_series
from bodo.libs.pd_datetime_arr_ext import PandasDatetimeTZDtype
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, raise_bodo_error
dt64_dtype = np.dtype('datetime64[ns]')
timedelta64_dtype = np.dtype('timedelta64[ns]')


class SeriesDatetimePropertiesType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        bedw__wry = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(bedw__wry)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kpg__xcx = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, kpg__xcx)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        mengu__iyimy, = args
        nuw__qxkk = signature.return_type
        bbxt__sajv = cgutils.create_struct_proxy(nuw__qxkk)(context, builder)
        bbxt__sajv.obj = mengu__iyimy
        context.nrt.incref(builder, signature.args[0], mengu__iyimy)
        return bbxt__sajv._getvalue()
    return SeriesDatetimePropertiesType(obj)(obj), codegen


@overload_attribute(SeriesType, 'dt')
def overload_series_dt(s):
    if not (bodo.hiframes.pd_series_ext.is_dt64_series_typ(s) or bodo.
        hiframes.pd_series_ext.is_timedelta64_series_typ(s)):
        raise_bodo_error('Can only use .dt accessor with datetimelike values.')
    return lambda s: bodo.hiframes.series_dt_impl.init_series_dt_properties(s)


def create_date_field_overload(field):

    def overload_field(S_dt):
        if S_dt.stype.dtype != types.NPDatetime('ns') and not isinstance(S_dt
            .stype.dtype, PandasDatetimeTZDtype):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{field}')
        rfz__bcx = 'def impl(S_dt):\n'
        rfz__bcx += '    S = S_dt._obj\n'
        rfz__bcx += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        rfz__bcx += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rfz__bcx += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        rfz__bcx += '    numba.parfors.parfor.init_prange()\n'
        rfz__bcx += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            rfz__bcx += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            rfz__bcx += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        rfz__bcx += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rfz__bcx += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        rfz__bcx += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        rfz__bcx += '            continue\n'
        rfz__bcx += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            rfz__bcx += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                rfz__bcx += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            rfz__bcx += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            elsq__hqn = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            rfz__bcx += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            rfz__bcx += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            rfz__bcx += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(elsq__hqn[field]))
        elif field == 'is_leap_year':
            rfz__bcx += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            rfz__bcx += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)\n'
                )
        elif field in ('daysinmonth', 'days_in_month'):
            elsq__hqn = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            rfz__bcx += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            rfz__bcx += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            rfz__bcx += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(elsq__hqn[field]))
        else:
            rfz__bcx += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            rfz__bcx += '        out_arr[i] = ts.' + field + '\n'
        rfz__bcx += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        zomut__socux = {}
        exec(rfz__bcx, {'bodo': bodo, 'numba': numba, 'np': np}, zomut__socux)
        impl = zomut__socux['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        mhjdi__pxrb = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(mhjdi__pxrb)


_install_date_fields()


def create_date_method_overload(method):
    afj__eynej = method in ['day_name', 'month_name']
    if afj__eynej:
        rfz__bcx = 'def overload_method(S_dt, locale=None):\n'
        rfz__bcx += '    unsupported_args = dict(locale=locale)\n'
        rfz__bcx += '    arg_defaults = dict(locale=None)\n'
        rfz__bcx += '    bodo.utils.typing.check_unsupported_args(\n'
        rfz__bcx += f"        'Series.dt.{method}',\n"
        rfz__bcx += '        unsupported_args,\n'
        rfz__bcx += '        arg_defaults,\n'
        rfz__bcx += "        package_name='pandas',\n"
        rfz__bcx += "        module_name='Series',\n"
        rfz__bcx += '    )\n'
    else:
        rfz__bcx = 'def overload_method(S_dt):\n'
        rfz__bcx += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    rfz__bcx += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    rfz__bcx += '        return\n'
    if afj__eynej:
        rfz__bcx += '    def impl(S_dt, locale=None):\n'
    else:
        rfz__bcx += '    def impl(S_dt):\n'
    rfz__bcx += '        S = S_dt._obj\n'
    rfz__bcx += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    rfz__bcx += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    rfz__bcx += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    rfz__bcx += '        numba.parfors.parfor.init_prange()\n'
    rfz__bcx += '        n = len(arr)\n'
    if afj__eynej:
        rfz__bcx += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        rfz__bcx += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    rfz__bcx += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    rfz__bcx += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    rfz__bcx += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    rfz__bcx += '                continue\n'
    rfz__bcx += '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n'
    rfz__bcx += f'            method_val = ts.{method}()\n'
    if afj__eynej:
        rfz__bcx += '            out_arr[i] = method_val\n'
    else:
        rfz__bcx += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    rfz__bcx += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    rfz__bcx += '    return impl\n'
    zomut__socux = {}
    exec(rfz__bcx, {'bodo': bodo, 'numba': numba, 'np': np}, zomut__socux)
    overload_method = zomut__socux['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        mhjdi__pxrb = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            mhjdi__pxrb)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        aoze__kwhru = S_dt._obj
        zsih__txmrf = bodo.hiframes.pd_series_ext.get_series_data(aoze__kwhru)
        uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(aoze__kwhru)
        bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(aoze__kwhru)
        numba.parfors.parfor.init_prange()
        klyb__jfve = len(zsih__txmrf)
        kzgv__omg = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            klyb__jfve)
        for rubdl__wgcex in numba.parfors.parfor.internal_prange(klyb__jfve):
            ipci__cfsm = zsih__txmrf[rubdl__wgcex]
            mvw__fszg = bodo.utils.conversion.box_if_dt64(ipci__cfsm)
            kzgv__omg[rubdl__wgcex] = datetime.date(mvw__fszg.year,
                mvw__fszg.month, mvw__fszg.day)
        return bodo.hiframes.pd_series_ext.init_series(kzgv__omg,
            uhohz__itqp, bedw__wry)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{attr}')
        if attr == 'components':
            aazwu__jda = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            vixps__jdz = 'convert_numpy_timedelta64_to_pd_timedelta'
            fdf__cquf = 'np.empty(n, np.int64)'
            ojpj__mmvv = attr
        elif attr == 'isocalendar':
            aazwu__jda = ['year', 'week', 'day']
            vixps__jdz = 'convert_datetime64_to_timestamp'
            fdf__cquf = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            ojpj__mmvv = attr + '()'
        rfz__bcx = 'def impl(S_dt):\n'
        rfz__bcx += '    S = S_dt._obj\n'
        rfz__bcx += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        rfz__bcx += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rfz__bcx += '    numba.parfors.parfor.init_prange()\n'
        rfz__bcx += '    n = len(arr)\n'
        for field in aazwu__jda:
            rfz__bcx += '    {} = {}\n'.format(field, fdf__cquf)
        rfz__bcx += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rfz__bcx += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in aazwu__jda:
            rfz__bcx += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        rfz__bcx += '            continue\n'
        coaqv__ogy = '(' + '[i], '.join(aazwu__jda) + '[i])'
        rfz__bcx += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(coaqv__ogy, vixps__jdz, ojpj__mmvv))
        nujzl__ixdw = '(' + ', '.join(aazwu__jda) + ')'
        akhl__bdh = "('" + "', '".join(aazwu__jda) + "')"
        rfz__bcx += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(nujzl__ixdw, akhl__bdh))
        zomut__socux = {}
        exec(rfz__bcx, {'bodo': bodo, 'numba': numba, 'np': np}, zomut__socux)
        impl = zomut__socux['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    niryd__ykhll = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, lkbct__zvuq in niryd__ykhll:
        mhjdi__pxrb = create_series_dt_df_output_overload(attr)
        lkbct__zvuq(SeriesDatetimePropertiesType, attr, inline='always')(
            mhjdi__pxrb)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        rfz__bcx = 'def impl(S_dt):\n'
        rfz__bcx += '    S = S_dt._obj\n'
        rfz__bcx += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        rfz__bcx += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rfz__bcx += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        rfz__bcx += '    numba.parfors.parfor.init_prange()\n'
        rfz__bcx += '    n = len(A)\n'
        rfz__bcx += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        rfz__bcx += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rfz__bcx += '        if bodo.libs.array_kernels.isna(A, i):\n'
        rfz__bcx += '            bodo.libs.array_kernels.setna(B, i)\n'
        rfz__bcx += '            continue\n'
        rfz__bcx += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if field == 'nanoseconds':
            rfz__bcx += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            rfz__bcx += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            rfz__bcx += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            rfz__bcx += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        rfz__bcx += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        zomut__socux = {}
        exec(rfz__bcx, {'numba': numba, 'np': np, 'bodo': bodo}, zomut__socux)
        impl = zomut__socux['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        rfz__bcx = 'def impl(S_dt):\n'
        rfz__bcx += '    S = S_dt._obj\n'
        rfz__bcx += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        rfz__bcx += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rfz__bcx += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        rfz__bcx += '    numba.parfors.parfor.init_prange()\n'
        rfz__bcx += '    n = len(A)\n'
        if method == 'total_seconds':
            rfz__bcx += '    B = np.empty(n, np.float64)\n'
        else:
            rfz__bcx += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        rfz__bcx += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rfz__bcx += '        if bodo.libs.array_kernels.isna(A, i):\n'
        rfz__bcx += '            bodo.libs.array_kernels.setna(B, i)\n'
        rfz__bcx += '            continue\n'
        rfz__bcx += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if method == 'total_seconds':
            rfz__bcx += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            rfz__bcx += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            rfz__bcx += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            rfz__bcx += '    return B\n'
        zomut__socux = {}
        exec(rfz__bcx, {'numba': numba, 'np': np, 'bodo': bodo, 'datetime':
            datetime}, zomut__socux)
        impl = zomut__socux['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        mhjdi__pxrb = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(mhjdi__pxrb)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        mhjdi__pxrb = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            mhjdi__pxrb)


_install_S_dt_timedelta_methods()


@overload_method(SeriesDatetimePropertiesType, 'strftime', inline='always',
    no_unliteral=True)
def dt_strftime(S_dt, date_format):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return
    if types.unliteral(date_format) != types.unicode_type:
        raise BodoError(
            "Series.str.strftime(): 'date_format' argument must be a string")

    def impl(S_dt, date_format):
        aoze__kwhru = S_dt._obj
        emgiv__bsmse = bodo.hiframes.pd_series_ext.get_series_data(aoze__kwhru)
        uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(aoze__kwhru)
        bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(aoze__kwhru)
        numba.parfors.parfor.init_prange()
        klyb__jfve = len(emgiv__bsmse)
        eqfbj__rjc = bodo.libs.str_arr_ext.pre_alloc_string_array(klyb__jfve,
            -1)
        for jpipt__hhvck in numba.parfors.parfor.internal_prange(klyb__jfve):
            if bodo.libs.array_kernels.isna(emgiv__bsmse, jpipt__hhvck):
                bodo.libs.array_kernels.setna(eqfbj__rjc, jpipt__hhvck)
                continue
            eqfbj__rjc[jpipt__hhvck] = bodo.utils.conversion.box_if_dt64(
                emgiv__bsmse[jpipt__hhvck]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(eqfbj__rjc,
            uhohz__itqp, bedw__wry)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        aoze__kwhru = S_dt._obj
        swjkw__znhy = get_series_data(aoze__kwhru).tz_convert(tz)
        uhohz__itqp = get_series_index(aoze__kwhru)
        bedw__wry = get_series_name(aoze__kwhru)
        return init_series(swjkw__znhy, uhohz__itqp, bedw__wry)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{method}()')
        zregi__ojl = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        wqou__ctyb = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', zregi__ojl,
            wqou__ctyb, package_name='pandas', module_name='Series')
        rfz__bcx = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        rfz__bcx += '    S = S_dt._obj\n'
        rfz__bcx += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        rfz__bcx += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rfz__bcx += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        rfz__bcx += '    numba.parfors.parfor.init_prange()\n'
        rfz__bcx += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            rfz__bcx += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            rfz__bcx += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        rfz__bcx += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rfz__bcx += '        if bodo.libs.array_kernels.isna(A, i):\n'
        rfz__bcx += '            bodo.libs.array_kernels.setna(B, i)\n'
        rfz__bcx += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            cuknu__ehbir = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            xqj__lazv = 'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64'
        else:
            cuknu__ehbir = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            xqj__lazv = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        rfz__bcx += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            xqj__lazv, cuknu__ehbir, method)
        rfz__bcx += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        zomut__socux = {}
        exec(rfz__bcx, {'numba': numba, 'np': np, 'bodo': bodo}, zomut__socux)
        impl = zomut__socux['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    trt__rot = ['ceil', 'floor', 'round']
    for method in trt__rot:
        mhjdi__pxrb = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            mhjdi__pxrb)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jzgb__yls = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                rgzf__ijl = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jzgb__yls)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                obgr__foigk = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                boxs__ytc = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    obgr__foigk)
                klyb__jfve = len(rgzf__ijl)
                aoze__kwhru = np.empty(klyb__jfve, timedelta64_dtype)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    qisdl__wvfq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(rgzf__ijl[rubdl__wgcex]))
                    iitw__erq = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        boxs__ytc[rubdl__wgcex])
                    if qisdl__wvfq == msiw__fgzwl or iitw__erq == msiw__fgzwl:
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(qisdl__wvfq, iitw__erq)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                boxs__ytc = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, dt64_dtype)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    tfve__emao = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    bcv__nulog = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(boxs__ytc[rubdl__wgcex]))
                    if tfve__emao == msiw__fgzwl or bcv__nulog == msiw__fgzwl:
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(tfve__emao, bcv__nulog)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                boxs__ytc = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, dt64_dtype)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    tfve__emao = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    bcv__nulog = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(boxs__ytc[rubdl__wgcex]))
                    if tfve__emao == msiw__fgzwl or bcv__nulog == msiw__fgzwl:
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(tfve__emao, bcv__nulog)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, timedelta64_dtype)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                ljiqb__rah = rhs.value
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    tfve__emao = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if tfve__emao == msiw__fgzwl or ljiqb__rah == msiw__fgzwl:
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(tfve__emao, ljiqb__rah)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, timedelta64_dtype)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                ljiqb__rah = lhs.value
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    tfve__emao = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if ljiqb__rah == msiw__fgzwl or tfve__emao == msiw__fgzwl:
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(ljiqb__rah, tfve__emao)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, dt64_dtype)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                pxpuv__vjduw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                bcv__nulog = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pxpuv__vjduw))
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    tfve__emao = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if tfve__emao == msiw__fgzwl or bcv__nulog == msiw__fgzwl:
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(tfve__emao, bcv__nulog)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, dt64_dtype)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                pxpuv__vjduw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                bcv__nulog = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pxpuv__vjduw))
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    tfve__emao = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if tfve__emao == msiw__fgzwl or bcv__nulog == msiw__fgzwl:
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(tfve__emao, bcv__nulog)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, timedelta64_dtype)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                aydmi__adxz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                tfve__emao = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    aydmi__adxz)
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    vekwy__seq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if vekwy__seq == msiw__fgzwl or tfve__emao == msiw__fgzwl:
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(vekwy__seq, tfve__emao)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, timedelta64_dtype)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                aydmi__adxz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                tfve__emao = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    aydmi__adxz)
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    vekwy__seq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if tfve__emao == msiw__fgzwl or vekwy__seq == msiw__fgzwl:
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(tfve__emao, vekwy__seq)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            txcm__xqw = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zsih__txmrf = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, timedelta64_dtype)
                msiw__fgzwl = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(txcm__xqw))
                pxpuv__vjduw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                bcv__nulog = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pxpuv__vjduw))
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    ykqox__wbkkm = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if (bcv__nulog == msiw__fgzwl or ykqox__wbkkm ==
                        msiw__fgzwl):
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(ykqox__wbkkm, bcv__nulog)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            txcm__xqw = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zsih__txmrf = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                klyb__jfve = len(zsih__txmrf)
                aoze__kwhru = np.empty(klyb__jfve, timedelta64_dtype)
                msiw__fgzwl = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(txcm__xqw))
                pxpuv__vjduw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                bcv__nulog = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(pxpuv__vjduw))
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    ykqox__wbkkm = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if (bcv__nulog == msiw__fgzwl or ykqox__wbkkm ==
                        msiw__fgzwl):
                        eyfc__prw = msiw__fgzwl
                    else:
                        eyfc__prw = op(bcv__nulog, ykqox__wbkkm)
                    aoze__kwhru[rubdl__wgcex
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        eyfc__prw)
                return bodo.hiframes.pd_series_ext.init_series(aoze__kwhru,
                    uhohz__itqp, bedw__wry)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            elej__mpnjj = True
        else:
            elej__mpnjj = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            txcm__xqw = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zsih__txmrf = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                klyb__jfve = len(zsih__txmrf)
                kzgv__omg = bodo.libs.bool_arr_ext.alloc_bool_array(klyb__jfve)
                msiw__fgzwl = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(txcm__xqw))
                asx__cqsk = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                ufn__riiu = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(asx__cqsk))
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    utg__cml = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if utg__cml == msiw__fgzwl or ufn__riiu == msiw__fgzwl:
                        eyfc__prw = elej__mpnjj
                    else:
                        eyfc__prw = op(utg__cml, ufn__riiu)
                    kzgv__omg[rubdl__wgcex] = eyfc__prw
                return bodo.hiframes.pd_series_ext.init_series(kzgv__omg,
                    uhohz__itqp, bedw__wry)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            txcm__xqw = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zsih__txmrf = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                klyb__jfve = len(zsih__txmrf)
                kzgv__omg = bodo.libs.bool_arr_ext.alloc_bool_array(klyb__jfve)
                msiw__fgzwl = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(txcm__xqw))
                ofwul__wnz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                utg__cml = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ofwul__wnz))
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    ufn__riiu = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if utg__cml == msiw__fgzwl or ufn__riiu == msiw__fgzwl:
                        eyfc__prw = elej__mpnjj
                    else:
                        eyfc__prw = op(utg__cml, ufn__riiu)
                    kzgv__omg[rubdl__wgcex] = eyfc__prw
                return bodo.hiframes.pd_series_ext.init_series(kzgv__omg,
                    uhohz__itqp, bedw__wry)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                klyb__jfve = len(zsih__txmrf)
                kzgv__omg = bodo.libs.bool_arr_ext.alloc_bool_array(klyb__jfve)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    utg__cml = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zsih__txmrf[rubdl__wgcex])
                    if utg__cml == msiw__fgzwl or rhs.value == msiw__fgzwl:
                        eyfc__prw = elej__mpnjj
                    else:
                        eyfc__prw = op(utg__cml, rhs.value)
                    kzgv__omg[rubdl__wgcex] = eyfc__prw
                return bodo.hiframes.pd_series_ext.init_series(kzgv__omg,
                    uhohz__itqp, bedw__wry)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                klyb__jfve = len(zsih__txmrf)
                kzgv__omg = bodo.libs.bool_arr_ext.alloc_bool_array(klyb__jfve)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    ufn__riiu = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zsih__txmrf[rubdl__wgcex])
                    if ufn__riiu == msiw__fgzwl or lhs.value == msiw__fgzwl:
                        eyfc__prw = elej__mpnjj
                    else:
                        eyfc__prw = op(lhs.value, ufn__riiu)
                    kzgv__omg[rubdl__wgcex] = eyfc__prw
                return bodo.hiframes.pd_series_ext.init_series(kzgv__omg,
                    uhohz__itqp, bedw__wry)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                klyb__jfve = len(zsih__txmrf)
                kzgv__omg = bodo.libs.bool_arr_ext.alloc_bool_array(klyb__jfve)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                zcv__lxd = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                dsn__gdiyh = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zcv__lxd)
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    utg__cml = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zsih__txmrf[rubdl__wgcex])
                    if utg__cml == msiw__fgzwl or dsn__gdiyh == msiw__fgzwl:
                        eyfc__prw = elej__mpnjj
                    else:
                        eyfc__prw = op(utg__cml, dsn__gdiyh)
                    kzgv__omg[rubdl__wgcex] = eyfc__prw
                return bodo.hiframes.pd_series_ext.init_series(kzgv__omg,
                    uhohz__itqp, bedw__wry)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            txcm__xqw = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                agaqn__shabm = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zsih__txmrf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    agaqn__shabm)
                uhohz__itqp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                bedw__wry = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                klyb__jfve = len(zsih__txmrf)
                kzgv__omg = bodo.libs.bool_arr_ext.alloc_bool_array(klyb__jfve)
                msiw__fgzwl = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    txcm__xqw)
                zcv__lxd = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                dsn__gdiyh = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zcv__lxd)
                for rubdl__wgcex in numba.parfors.parfor.internal_prange(
                    klyb__jfve):
                    aydmi__adxz = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zsih__txmrf[rubdl__wgcex]))
                    if aydmi__adxz == msiw__fgzwl or dsn__gdiyh == msiw__fgzwl:
                        eyfc__prw = elej__mpnjj
                    else:
                        eyfc__prw = op(dsn__gdiyh, aydmi__adxz)
                    kzgv__omg[rubdl__wgcex] = eyfc__prw
                return bodo.hiframes.pd_series_ext.init_series(kzgv__omg,
                    uhohz__itqp, bedw__wry)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for degc__qea in series_dt_unsupported_attrs:
        fdn__kqqxp = 'Series.dt.' + degc__qea
        overload_attribute(SeriesDatetimePropertiesType, degc__qea)(
            create_unsupported_overload(fdn__kqqxp))
    for hjnow__viwxm in series_dt_unsupported_methods:
        fdn__kqqxp = 'Series.dt.' + hjnow__viwxm
        overload_method(SeriesDatetimePropertiesType, hjnow__viwxm,
            no_unliteral=True)(create_unsupported_overload(fdn__kqqxp))


_install_series_dt_unsupported()
