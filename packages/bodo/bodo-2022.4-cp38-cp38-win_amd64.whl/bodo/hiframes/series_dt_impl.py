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
        tpwu__ngueo = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(tpwu__ngueo)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jxvs__xey = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, jxvs__xey)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        lxhn__lraii, = args
        azox__dpean = signature.return_type
        cmhv__pyxjp = cgutils.create_struct_proxy(azox__dpean)(context, builder
            )
        cmhv__pyxjp.obj = lxhn__lraii
        context.nrt.incref(builder, signature.args[0], lxhn__lraii)
        return cmhv__pyxjp._getvalue()
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
        myhm__vrc = 'def impl(S_dt):\n'
        myhm__vrc += '    S = S_dt._obj\n'
        myhm__vrc += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        myhm__vrc += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        myhm__vrc += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        myhm__vrc += '    numba.parfors.parfor.init_prange()\n'
        myhm__vrc += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            myhm__vrc += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            myhm__vrc += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        myhm__vrc += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        myhm__vrc += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        myhm__vrc += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        myhm__vrc += '            continue\n'
        myhm__vrc += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            myhm__vrc += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                myhm__vrc += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            myhm__vrc += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            ayjg__wem = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            myhm__vrc += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            myhm__vrc += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            myhm__vrc += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(ayjg__wem[field]))
        elif field == 'is_leap_year':
            myhm__vrc += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            myhm__vrc += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)\n'
                )
        elif field in ('daysinmonth', 'days_in_month'):
            ayjg__wem = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            myhm__vrc += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            myhm__vrc += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            myhm__vrc += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(ayjg__wem[field]))
        else:
            myhm__vrc += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            myhm__vrc += '        out_arr[i] = ts.' + field + '\n'
        myhm__vrc += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        etdvo__hrxbp = {}
        exec(myhm__vrc, {'bodo': bodo, 'numba': numba, 'np': np}, etdvo__hrxbp)
        impl = etdvo__hrxbp['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        rtqhv__ikmw = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(rtqhv__ikmw)


_install_date_fields()


def create_date_method_overload(method):
    ysnve__klc = method in ['day_name', 'month_name']
    if ysnve__klc:
        myhm__vrc = 'def overload_method(S_dt, locale=None):\n'
        myhm__vrc += '    unsupported_args = dict(locale=locale)\n'
        myhm__vrc += '    arg_defaults = dict(locale=None)\n'
        myhm__vrc += '    bodo.utils.typing.check_unsupported_args(\n'
        myhm__vrc += f"        'Series.dt.{method}',\n"
        myhm__vrc += '        unsupported_args,\n'
        myhm__vrc += '        arg_defaults,\n'
        myhm__vrc += "        package_name='pandas',\n"
        myhm__vrc += "        module_name='Series',\n"
        myhm__vrc += '    )\n'
    else:
        myhm__vrc = 'def overload_method(S_dt):\n'
        myhm__vrc += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    myhm__vrc += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    myhm__vrc += '        return\n'
    if ysnve__klc:
        myhm__vrc += '    def impl(S_dt, locale=None):\n'
    else:
        myhm__vrc += '    def impl(S_dt):\n'
    myhm__vrc += '        S = S_dt._obj\n'
    myhm__vrc += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    myhm__vrc += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    myhm__vrc += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    myhm__vrc += '        numba.parfors.parfor.init_prange()\n'
    myhm__vrc += '        n = len(arr)\n'
    if ysnve__klc:
        myhm__vrc += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        myhm__vrc += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    myhm__vrc += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    myhm__vrc += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    myhm__vrc += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    myhm__vrc += '                continue\n'
    myhm__vrc += '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n'
    myhm__vrc += f'            method_val = ts.{method}()\n'
    if ysnve__klc:
        myhm__vrc += '            out_arr[i] = method_val\n'
    else:
        myhm__vrc += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    myhm__vrc += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    myhm__vrc += '    return impl\n'
    etdvo__hrxbp = {}
    exec(myhm__vrc, {'bodo': bodo, 'numba': numba, 'np': np}, etdvo__hrxbp)
    overload_method = etdvo__hrxbp['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        rtqhv__ikmw = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            rtqhv__ikmw)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        qne__ktu = S_dt._obj
        ngpg__srh = bodo.hiframes.pd_series_ext.get_series_data(qne__ktu)
        osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(qne__ktu)
        tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(qne__ktu)
        numba.parfors.parfor.init_prange()
        vmx__qkbcg = len(ngpg__srh)
        wudw__tgzsp = (bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(vmx__qkbcg))
        for siprq__aheo in numba.parfors.parfor.internal_prange(vmx__qkbcg):
            gjnxg__buez = ngpg__srh[siprq__aheo]
            ldqp__pfg = bodo.utils.conversion.box_if_dt64(gjnxg__buez)
            wudw__tgzsp[siprq__aheo] = datetime.date(ldqp__pfg.year,
                ldqp__pfg.month, ldqp__pfg.day)
        return bodo.hiframes.pd_series_ext.init_series(wudw__tgzsp,
            osqbi__plp, tpwu__ngueo)
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
            led__ouflm = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            ovyfy__mjrh = 'convert_numpy_timedelta64_to_pd_timedelta'
            rnmki__ogmxt = 'np.empty(n, np.int64)'
            bya__wlx = attr
        elif attr == 'isocalendar':
            led__ouflm = ['year', 'week', 'day']
            ovyfy__mjrh = 'convert_datetime64_to_timestamp'
            rnmki__ogmxt = (
                'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)')
            bya__wlx = attr + '()'
        myhm__vrc = 'def impl(S_dt):\n'
        myhm__vrc += '    S = S_dt._obj\n'
        myhm__vrc += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        myhm__vrc += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        myhm__vrc += '    numba.parfors.parfor.init_prange()\n'
        myhm__vrc += '    n = len(arr)\n'
        for field in led__ouflm:
            myhm__vrc += '    {} = {}\n'.format(field, rnmki__ogmxt)
        myhm__vrc += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        myhm__vrc += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in led__ouflm:
            myhm__vrc += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        myhm__vrc += '            continue\n'
        apt__eyi = '(' + '[i], '.join(led__ouflm) + '[i])'
        myhm__vrc += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(apt__eyi, ovyfy__mjrh, bya__wlx))
        xaixh__inujz = '(' + ', '.join(led__ouflm) + ')'
        isvex__iav = "('" + "', '".join(led__ouflm) + "')"
        myhm__vrc += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(xaixh__inujz, isvex__iav))
        etdvo__hrxbp = {}
        exec(myhm__vrc, {'bodo': bodo, 'numba': numba, 'np': np}, etdvo__hrxbp)
        impl = etdvo__hrxbp['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    xxhg__jgrti = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, dqvw__map in xxhg__jgrti:
        rtqhv__ikmw = create_series_dt_df_output_overload(attr)
        dqvw__map(SeriesDatetimePropertiesType, attr, inline='always')(
            rtqhv__ikmw)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        myhm__vrc = 'def impl(S_dt):\n'
        myhm__vrc += '    S = S_dt._obj\n'
        myhm__vrc += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        myhm__vrc += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        myhm__vrc += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        myhm__vrc += '    numba.parfors.parfor.init_prange()\n'
        myhm__vrc += '    n = len(A)\n'
        myhm__vrc += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        myhm__vrc += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        myhm__vrc += '        if bodo.libs.array_kernels.isna(A, i):\n'
        myhm__vrc += '            bodo.libs.array_kernels.setna(B, i)\n'
        myhm__vrc += '            continue\n'
        myhm__vrc += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if field == 'nanoseconds':
            myhm__vrc += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            myhm__vrc += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            myhm__vrc += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            myhm__vrc += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        myhm__vrc += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        etdvo__hrxbp = {}
        exec(myhm__vrc, {'numba': numba, 'np': np, 'bodo': bodo}, etdvo__hrxbp)
        impl = etdvo__hrxbp['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        myhm__vrc = 'def impl(S_dt):\n'
        myhm__vrc += '    S = S_dt._obj\n'
        myhm__vrc += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        myhm__vrc += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        myhm__vrc += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        myhm__vrc += '    numba.parfors.parfor.init_prange()\n'
        myhm__vrc += '    n = len(A)\n'
        if method == 'total_seconds':
            myhm__vrc += '    B = np.empty(n, np.float64)\n'
        else:
            myhm__vrc += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        myhm__vrc += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        myhm__vrc += '        if bodo.libs.array_kernels.isna(A, i):\n'
        myhm__vrc += '            bodo.libs.array_kernels.setna(B, i)\n'
        myhm__vrc += '            continue\n'
        myhm__vrc += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if method == 'total_seconds':
            myhm__vrc += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            myhm__vrc += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            myhm__vrc += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            myhm__vrc += '    return B\n'
        etdvo__hrxbp = {}
        exec(myhm__vrc, {'numba': numba, 'np': np, 'bodo': bodo, 'datetime':
            datetime}, etdvo__hrxbp)
        impl = etdvo__hrxbp['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        rtqhv__ikmw = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(rtqhv__ikmw)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        rtqhv__ikmw = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            rtqhv__ikmw)


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
        qne__ktu = S_dt._obj
        bgfz__edman = bodo.hiframes.pd_series_ext.get_series_data(qne__ktu)
        osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(qne__ktu)
        tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(qne__ktu)
        numba.parfors.parfor.init_prange()
        vmx__qkbcg = len(bgfz__edman)
        wftgi__rxai = bodo.libs.str_arr_ext.pre_alloc_string_array(vmx__qkbcg,
            -1)
        for phrv__bybsl in numba.parfors.parfor.internal_prange(vmx__qkbcg):
            if bodo.libs.array_kernels.isna(bgfz__edman, phrv__bybsl):
                bodo.libs.array_kernels.setna(wftgi__rxai, phrv__bybsl)
                continue
            wftgi__rxai[phrv__bybsl] = bodo.utils.conversion.box_if_dt64(
                bgfz__edman[phrv__bybsl]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(wftgi__rxai,
            osqbi__plp, tpwu__ngueo)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        qne__ktu = S_dt._obj
        yzqw__zoj = get_series_data(qne__ktu).tz_convert(tz)
        osqbi__plp = get_series_index(qne__ktu)
        tpwu__ngueo = get_series_name(qne__ktu)
        return init_series(yzqw__zoj, osqbi__plp, tpwu__ngueo)
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
        aecs__cjdt = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        jwg__rgra = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', aecs__cjdt, jwg__rgra,
            package_name='pandas', module_name='Series')
        myhm__vrc = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        myhm__vrc += '    S = S_dt._obj\n'
        myhm__vrc += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        myhm__vrc += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        myhm__vrc += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        myhm__vrc += '    numba.parfors.parfor.init_prange()\n'
        myhm__vrc += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            myhm__vrc += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            myhm__vrc += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        myhm__vrc += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        myhm__vrc += '        if bodo.libs.array_kernels.isna(A, i):\n'
        myhm__vrc += '            bodo.libs.array_kernels.setna(B, i)\n'
        myhm__vrc += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            bisu__cfe = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            fohc__waiec = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            bisu__cfe = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            fohc__waiec = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        myhm__vrc += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            fohc__waiec, bisu__cfe, method)
        myhm__vrc += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        etdvo__hrxbp = {}
        exec(myhm__vrc, {'numba': numba, 'np': np, 'bodo': bodo}, etdvo__hrxbp)
        impl = etdvo__hrxbp['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    ldme__dttf = ['ceil', 'floor', 'round']
    for method in ldme__dttf:
        rtqhv__ikmw = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            rtqhv__ikmw)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jej__gujzj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                hef__dht = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jej__gujzj)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                olyrx__fyx = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                nxe__dmiue = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    olyrx__fyx)
                vmx__qkbcg = len(hef__dht)
                qne__ktu = np.empty(vmx__qkbcg, timedelta64_dtype)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    bie__rutqd = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(hef__dht[siprq__aheo]))
                    gbyi__mbtn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(nxe__dmiue[siprq__aheo]))
                    if bie__rutqd == grxb__mtnv or gbyi__mbtn == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(bie__rutqd, gbyi__mbtn)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                nxe__dmiue = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, dt64_dtype)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    bvyj__ebssn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ngpg__srh[siprq__aheo]))
                    gmylr__vur = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(nxe__dmiue[siprq__aheo]))
                    if bvyj__ebssn == grxb__mtnv or gmylr__vur == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(bvyj__ebssn, gmylr__vur)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                nxe__dmiue = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, dt64_dtype)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    bvyj__ebssn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ngpg__srh[siprq__aheo]))
                    gmylr__vur = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(nxe__dmiue[siprq__aheo]))
                    if bvyj__ebssn == grxb__mtnv or gmylr__vur == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(bvyj__ebssn, gmylr__vur)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, timedelta64_dtype)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                wmxb__ktaas = rhs.value
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    bvyj__ebssn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ngpg__srh[siprq__aheo]))
                    if bvyj__ebssn == grxb__mtnv or wmxb__ktaas == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(bvyj__ebssn, wmxb__ktaas)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, timedelta64_dtype)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                wmxb__ktaas = lhs.value
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    bvyj__ebssn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ngpg__srh[siprq__aheo]))
                    if wmxb__ktaas == grxb__mtnv or bvyj__ebssn == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(wmxb__ktaas, bvyj__ebssn)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, dt64_dtype)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                xsxu__fclpq = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                gmylr__vur = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xsxu__fclpq))
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    bvyj__ebssn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ngpg__srh[siprq__aheo]))
                    if bvyj__ebssn == grxb__mtnv or gmylr__vur == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(bvyj__ebssn, gmylr__vur)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, dt64_dtype)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                xsxu__fclpq = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                gmylr__vur = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xsxu__fclpq))
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    bvyj__ebssn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ngpg__srh[siprq__aheo]))
                    if bvyj__ebssn == grxb__mtnv or gmylr__vur == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(bvyj__ebssn, gmylr__vur)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, timedelta64_dtype)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                kkw__ybqa = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                bvyj__ebssn = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    kkw__ybqa)
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    znbl__obcbe = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ngpg__srh[siprq__aheo]))
                    if znbl__obcbe == grxb__mtnv or bvyj__ebssn == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(znbl__obcbe, bvyj__ebssn)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, timedelta64_dtype)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                kkw__ybqa = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                bvyj__ebssn = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    kkw__ybqa)
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    znbl__obcbe = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ngpg__srh[siprq__aheo]))
                    if bvyj__ebssn == grxb__mtnv or znbl__obcbe == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(bvyj__ebssn, znbl__obcbe)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            flmb__ytqpl = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ngpg__srh = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, timedelta64_dtype)
                grxb__mtnv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(flmb__ytqpl))
                xsxu__fclpq = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                gmylr__vur = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xsxu__fclpq))
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    jmn__sajmu = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(ngpg__srh[siprq__aheo]))
                    if gmylr__vur == grxb__mtnv or jmn__sajmu == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(jmn__sajmu, gmylr__vur)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            flmb__ytqpl = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ngpg__srh = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                vmx__qkbcg = len(ngpg__srh)
                qne__ktu = np.empty(vmx__qkbcg, timedelta64_dtype)
                grxb__mtnv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(flmb__ytqpl))
                xsxu__fclpq = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                gmylr__vur = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xsxu__fclpq))
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    jmn__sajmu = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(ngpg__srh[siprq__aheo]))
                    if gmylr__vur == grxb__mtnv or jmn__sajmu == grxb__mtnv:
                        dhrq__mhaq = grxb__mtnv
                    else:
                        dhrq__mhaq = op(gmylr__vur, jmn__sajmu)
                    qne__ktu[siprq__aheo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        dhrq__mhaq)
                return bodo.hiframes.pd_series_ext.init_series(qne__ktu,
                    osqbi__plp, tpwu__ngueo)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            arq__hhiv = True
        else:
            arq__hhiv = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            flmb__ytqpl = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ngpg__srh = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vmx__qkbcg = len(ngpg__srh)
                wudw__tgzsp = bodo.libs.bool_arr_ext.alloc_bool_array(
                    vmx__qkbcg)
                grxb__mtnv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(flmb__ytqpl))
                kqgli__qbd = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                lwt__ghv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(kqgli__qbd))
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    kppw__buo = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(ngpg__srh[siprq__aheo]))
                    if kppw__buo == grxb__mtnv or lwt__ghv == grxb__mtnv:
                        dhrq__mhaq = arq__hhiv
                    else:
                        dhrq__mhaq = op(kppw__buo, lwt__ghv)
                    wudw__tgzsp[siprq__aheo] = dhrq__mhaq
                return bodo.hiframes.pd_series_ext.init_series(wudw__tgzsp,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            flmb__ytqpl = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ngpg__srh = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                vmx__qkbcg = len(ngpg__srh)
                wudw__tgzsp = bodo.libs.bool_arr_ext.alloc_bool_array(
                    vmx__qkbcg)
                grxb__mtnv = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(flmb__ytqpl))
                hrlbe__vkej = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                kppw__buo = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(hrlbe__vkej))
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    lwt__ghv = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(ngpg__srh[siprq__aheo]))
                    if kppw__buo == grxb__mtnv or lwt__ghv == grxb__mtnv:
                        dhrq__mhaq = arq__hhiv
                    else:
                        dhrq__mhaq = op(kppw__buo, lwt__ghv)
                    wudw__tgzsp[siprq__aheo] = dhrq__mhaq
                return bodo.hiframes.pd_series_ext.init_series(wudw__tgzsp,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                vmx__qkbcg = len(ngpg__srh)
                wudw__tgzsp = bodo.libs.bool_arr_ext.alloc_bool_array(
                    vmx__qkbcg)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    kppw__buo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        ngpg__srh[siprq__aheo])
                    if kppw__buo == grxb__mtnv or rhs.value == grxb__mtnv:
                        dhrq__mhaq = arq__hhiv
                    else:
                        dhrq__mhaq = op(kppw__buo, rhs.value)
                    wudw__tgzsp[siprq__aheo] = dhrq__mhaq
                return bodo.hiframes.pd_series_ext.init_series(wudw__tgzsp,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                vmx__qkbcg = len(ngpg__srh)
                wudw__tgzsp = bodo.libs.bool_arr_ext.alloc_bool_array(
                    vmx__qkbcg)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    lwt__ghv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        ngpg__srh[siprq__aheo])
                    if lwt__ghv == grxb__mtnv or lhs.value == grxb__mtnv:
                        dhrq__mhaq = arq__hhiv
                    else:
                        dhrq__mhaq = op(lhs.value, lwt__ghv)
                    wudw__tgzsp[siprq__aheo] = dhrq__mhaq
                return bodo.hiframes.pd_series_ext.init_series(wudw__tgzsp,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                vmx__qkbcg = len(ngpg__srh)
                wudw__tgzsp = bodo.libs.bool_arr_ext.alloc_bool_array(
                    vmx__qkbcg)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                rhu__nmu = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                zgyh__qug = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    rhu__nmu)
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    kppw__buo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        ngpg__srh[siprq__aheo])
                    if kppw__buo == grxb__mtnv or zgyh__qug == grxb__mtnv:
                        dhrq__mhaq = arq__hhiv
                    else:
                        dhrq__mhaq = op(kppw__buo, zgyh__qug)
                    wudw__tgzsp[siprq__aheo] = dhrq__mhaq
                return bodo.hiframes.pd_series_ext.init_series(wudw__tgzsp,
                    osqbi__plp, tpwu__ngueo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            flmb__ytqpl = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                alsnd__yiuq = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ngpg__srh = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    alsnd__yiuq)
                osqbi__plp = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                tpwu__ngueo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                vmx__qkbcg = len(ngpg__srh)
                wudw__tgzsp = bodo.libs.bool_arr_ext.alloc_bool_array(
                    vmx__qkbcg)
                grxb__mtnv = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    flmb__ytqpl)
                rhu__nmu = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                zgyh__qug = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    rhu__nmu)
                for siprq__aheo in numba.parfors.parfor.internal_prange(
                    vmx__qkbcg):
                    kkw__ybqa = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        ngpg__srh[siprq__aheo])
                    if kkw__ybqa == grxb__mtnv or zgyh__qug == grxb__mtnv:
                        dhrq__mhaq = arq__hhiv
                    else:
                        dhrq__mhaq = op(zgyh__qug, kkw__ybqa)
                    wudw__tgzsp[siprq__aheo] = dhrq__mhaq
                return bodo.hiframes.pd_series_ext.init_series(wudw__tgzsp,
                    osqbi__plp, tpwu__ngueo)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for bdnrx__zwdi in series_dt_unsupported_attrs:
        ime__jgc = 'Series.dt.' + bdnrx__zwdi
        overload_attribute(SeriesDatetimePropertiesType, bdnrx__zwdi)(
            create_unsupported_overload(ime__jgc))
    for cca__krdw in series_dt_unsupported_methods:
        ime__jgc = 'Series.dt.' + cca__krdw
        overload_method(SeriesDatetimePropertiesType, cca__krdw,
            no_unliteral=True)(create_unsupported_overload(ime__jgc))


_install_series_dt_unsupported()
