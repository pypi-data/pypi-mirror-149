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
        ioqys__pbb = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(ioqys__pbb)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bittu__noz = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, bittu__noz)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        gpmi__lcsu, = args
        cav__hlq = signature.return_type
        rvram__emd = cgutils.create_struct_proxy(cav__hlq)(context, builder)
        rvram__emd.obj = gpmi__lcsu
        context.nrt.incref(builder, signature.args[0], gpmi__lcsu)
        return rvram__emd._getvalue()
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
        rzaz__mnkq = 'def impl(S_dt):\n'
        rzaz__mnkq += '    S = S_dt._obj\n'
        rzaz__mnkq += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        rzaz__mnkq += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rzaz__mnkq += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        rzaz__mnkq += '    numba.parfors.parfor.init_prange()\n'
        rzaz__mnkq += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            rzaz__mnkq += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            rzaz__mnkq += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        rzaz__mnkq += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rzaz__mnkq += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        rzaz__mnkq += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        rzaz__mnkq += '            continue\n'
        rzaz__mnkq += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            rzaz__mnkq += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                rzaz__mnkq += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            rzaz__mnkq += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            zmn__biywz = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            rzaz__mnkq += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            rzaz__mnkq += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            rzaz__mnkq += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(zmn__biywz[field]))
        elif field == 'is_leap_year':
            rzaz__mnkq += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            rzaz__mnkq += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)
"""
        elif field in ('daysinmonth', 'days_in_month'):
            zmn__biywz = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            rzaz__mnkq += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            rzaz__mnkq += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            rzaz__mnkq += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(zmn__biywz[field]))
        else:
            rzaz__mnkq += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            rzaz__mnkq += '        out_arr[i] = ts.' + field + '\n'
        rzaz__mnkq += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        nzwpk__lpz = {}
        exec(rzaz__mnkq, {'bodo': bodo, 'numba': numba, 'np': np}, nzwpk__lpz)
        impl = nzwpk__lpz['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        cuygi__dmg = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(cuygi__dmg)


_install_date_fields()


def create_date_method_overload(method):
    viei__atnbg = method in ['day_name', 'month_name']
    if viei__atnbg:
        rzaz__mnkq = 'def overload_method(S_dt, locale=None):\n'
        rzaz__mnkq += '    unsupported_args = dict(locale=locale)\n'
        rzaz__mnkq += '    arg_defaults = dict(locale=None)\n'
        rzaz__mnkq += '    bodo.utils.typing.check_unsupported_args(\n'
        rzaz__mnkq += f"        'Series.dt.{method}',\n"
        rzaz__mnkq += '        unsupported_args,\n'
        rzaz__mnkq += '        arg_defaults,\n'
        rzaz__mnkq += "        package_name='pandas',\n"
        rzaz__mnkq += "        module_name='Series',\n"
        rzaz__mnkq += '    )\n'
    else:
        rzaz__mnkq = 'def overload_method(S_dt):\n'
        rzaz__mnkq += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    rzaz__mnkq += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    rzaz__mnkq += '        return\n'
    if viei__atnbg:
        rzaz__mnkq += '    def impl(S_dt, locale=None):\n'
    else:
        rzaz__mnkq += '    def impl(S_dt):\n'
    rzaz__mnkq += '        S = S_dt._obj\n'
    rzaz__mnkq += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    rzaz__mnkq += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    rzaz__mnkq += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    rzaz__mnkq += '        numba.parfors.parfor.init_prange()\n'
    rzaz__mnkq += '        n = len(arr)\n'
    if viei__atnbg:
        rzaz__mnkq += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        rzaz__mnkq += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    rzaz__mnkq += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    rzaz__mnkq += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    rzaz__mnkq += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    rzaz__mnkq += '                continue\n'
    rzaz__mnkq += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    rzaz__mnkq += f'            method_val = ts.{method}()\n'
    if viei__atnbg:
        rzaz__mnkq += '            out_arr[i] = method_val\n'
    else:
        rzaz__mnkq += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    rzaz__mnkq += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    rzaz__mnkq += '    return impl\n'
    nzwpk__lpz = {}
    exec(rzaz__mnkq, {'bodo': bodo, 'numba': numba, 'np': np}, nzwpk__lpz)
    overload_method = nzwpk__lpz['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        cuygi__dmg = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            cuygi__dmg)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        smz__vgf = S_dt._obj
        csvfi__maib = bodo.hiframes.pd_series_ext.get_series_data(smz__vgf)
        jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(smz__vgf)
        ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(smz__vgf)
        numba.parfors.parfor.init_prange()
        yagn__bybm = len(csvfi__maib)
        isihd__xzd = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            yagn__bybm)
        for ojkp__rnsc in numba.parfors.parfor.internal_prange(yagn__bybm):
            qmy__tvx = csvfi__maib[ojkp__rnsc]
            vvl__wowsm = bodo.utils.conversion.box_if_dt64(qmy__tvx)
            isihd__xzd[ojkp__rnsc] = datetime.date(vvl__wowsm.year,
                vvl__wowsm.month, vvl__wowsm.day)
        return bodo.hiframes.pd_series_ext.init_series(isihd__xzd,
            jdi__tlrck, ioqys__pbb)
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
            foy__zzxm = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            vab__gsx = 'convert_numpy_timedelta64_to_pd_timedelta'
            qojd__ave = 'np.empty(n, np.int64)'
            kknr__jdql = attr
        elif attr == 'isocalendar':
            foy__zzxm = ['year', 'week', 'day']
            vab__gsx = 'convert_datetime64_to_timestamp'
            qojd__ave = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            kknr__jdql = attr + '()'
        rzaz__mnkq = 'def impl(S_dt):\n'
        rzaz__mnkq += '    S = S_dt._obj\n'
        rzaz__mnkq += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        rzaz__mnkq += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rzaz__mnkq += '    numba.parfors.parfor.init_prange()\n'
        rzaz__mnkq += '    n = len(arr)\n'
        for field in foy__zzxm:
            rzaz__mnkq += '    {} = {}\n'.format(field, qojd__ave)
        rzaz__mnkq += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rzaz__mnkq += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in foy__zzxm:
            rzaz__mnkq += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        rzaz__mnkq += '            continue\n'
        gkqd__ape = '(' + '[i], '.join(foy__zzxm) + '[i])'
        rzaz__mnkq += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(gkqd__ape, vab__gsx, kknr__jdql))
        penir__hixic = '(' + ', '.join(foy__zzxm) + ')'
        yll__kfyho = "('" + "', '".join(foy__zzxm) + "')"
        rzaz__mnkq += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(penir__hixic, yll__kfyho))
        nzwpk__lpz = {}
        exec(rzaz__mnkq, {'bodo': bodo, 'numba': numba, 'np': np}, nzwpk__lpz)
        impl = nzwpk__lpz['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    jzcj__yavqu = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, zbyo__rvfn in jzcj__yavqu:
        cuygi__dmg = create_series_dt_df_output_overload(attr)
        zbyo__rvfn(SeriesDatetimePropertiesType, attr, inline='always')(
            cuygi__dmg)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        rzaz__mnkq = 'def impl(S_dt):\n'
        rzaz__mnkq += '    S = S_dt._obj\n'
        rzaz__mnkq += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        rzaz__mnkq += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rzaz__mnkq += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        rzaz__mnkq += '    numba.parfors.parfor.init_prange()\n'
        rzaz__mnkq += '    n = len(A)\n'
        rzaz__mnkq += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        rzaz__mnkq += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rzaz__mnkq += '        if bodo.libs.array_kernels.isna(A, i):\n'
        rzaz__mnkq += '            bodo.libs.array_kernels.setna(B, i)\n'
        rzaz__mnkq += '            continue\n'
        rzaz__mnkq += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            rzaz__mnkq += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            rzaz__mnkq += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            rzaz__mnkq += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            rzaz__mnkq += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        rzaz__mnkq += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        nzwpk__lpz = {}
        exec(rzaz__mnkq, {'numba': numba, 'np': np, 'bodo': bodo}, nzwpk__lpz)
        impl = nzwpk__lpz['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        rzaz__mnkq = 'def impl(S_dt):\n'
        rzaz__mnkq += '    S = S_dt._obj\n'
        rzaz__mnkq += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        rzaz__mnkq += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rzaz__mnkq += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        rzaz__mnkq += '    numba.parfors.parfor.init_prange()\n'
        rzaz__mnkq += '    n = len(A)\n'
        if method == 'total_seconds':
            rzaz__mnkq += '    B = np.empty(n, np.float64)\n'
        else:
            rzaz__mnkq += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        rzaz__mnkq += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rzaz__mnkq += '        if bodo.libs.array_kernels.isna(A, i):\n'
        rzaz__mnkq += '            bodo.libs.array_kernels.setna(B, i)\n'
        rzaz__mnkq += '            continue\n'
        rzaz__mnkq += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            rzaz__mnkq += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            rzaz__mnkq += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            rzaz__mnkq += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            rzaz__mnkq += '    return B\n'
        nzwpk__lpz = {}
        exec(rzaz__mnkq, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, nzwpk__lpz)
        impl = nzwpk__lpz['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        cuygi__dmg = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(cuygi__dmg)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        cuygi__dmg = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            cuygi__dmg)


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
        smz__vgf = S_dt._obj
        jzggh__dvps = bodo.hiframes.pd_series_ext.get_series_data(smz__vgf)
        jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(smz__vgf)
        ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(smz__vgf)
        numba.parfors.parfor.init_prange()
        yagn__bybm = len(jzggh__dvps)
        ofivj__exdn = bodo.libs.str_arr_ext.pre_alloc_string_array(yagn__bybm,
            -1)
        for kzur__enr in numba.parfors.parfor.internal_prange(yagn__bybm):
            if bodo.libs.array_kernels.isna(jzggh__dvps, kzur__enr):
                bodo.libs.array_kernels.setna(ofivj__exdn, kzur__enr)
                continue
            ofivj__exdn[kzur__enr] = bodo.utils.conversion.box_if_dt64(
                jzggh__dvps[kzur__enr]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(ofivj__exdn,
            jdi__tlrck, ioqys__pbb)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        smz__vgf = S_dt._obj
        sad__rskss = get_series_data(smz__vgf).tz_convert(tz)
        jdi__tlrck = get_series_index(smz__vgf)
        ioqys__pbb = get_series_name(smz__vgf)
        return init_series(sad__rskss, jdi__tlrck, ioqys__pbb)
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
        rmk__wnx = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        gas__qxq = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', rmk__wnx, gas__qxq,
            package_name='pandas', module_name='Series')
        rzaz__mnkq = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        rzaz__mnkq += '    S = S_dt._obj\n'
        rzaz__mnkq += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        rzaz__mnkq += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        rzaz__mnkq += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        rzaz__mnkq += '    numba.parfors.parfor.init_prange()\n'
        rzaz__mnkq += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            rzaz__mnkq += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            rzaz__mnkq += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        rzaz__mnkq += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        rzaz__mnkq += '        if bodo.libs.array_kernels.isna(A, i):\n'
        rzaz__mnkq += '            bodo.libs.array_kernels.setna(B, i)\n'
        rzaz__mnkq += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            aeuju__qbs = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            kzud__kaj = 'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64'
        else:
            aeuju__qbs = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            kzud__kaj = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        rzaz__mnkq += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            kzud__kaj, aeuju__qbs, method)
        rzaz__mnkq += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        nzwpk__lpz = {}
        exec(rzaz__mnkq, {'numba': numba, 'np': np, 'bodo': bodo}, nzwpk__lpz)
        impl = nzwpk__lpz['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    tau__zyblz = ['ceil', 'floor', 'round']
    for method in tau__zyblz:
        cuygi__dmg = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            cuygi__dmg)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                apner__djll = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                dvs__vij = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    apner__djll)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                zkgpd__swtl = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                svojh__kyilr = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    zkgpd__swtl)
                yagn__bybm = len(dvs__vij)
                smz__vgf = np.empty(yagn__bybm, timedelta64_dtype)
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    xbi__ygdo = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        dvs__vij[ojkp__rnsc])
                    yet__btyu = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        svojh__kyilr[ojkp__rnsc])
                    if xbi__ygdo == wsqip__mjba or yet__btyu == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(xbi__ygdo, yet__btyu)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                svojh__kyilr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, dt64_dtype)
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    fmp__hlz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        csvfi__maib[ojkp__rnsc])
                    gmn__myjg = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(svojh__kyilr[ojkp__rnsc]))
                    if fmp__hlz == wsqip__mjba or gmn__myjg == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(fmp__hlz, gmn__myjg)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                svojh__kyilr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, dt64_dtype)
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    fmp__hlz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        csvfi__maib[ojkp__rnsc])
                    gmn__myjg = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(svojh__kyilr[ojkp__rnsc]))
                    if fmp__hlz == wsqip__mjba or gmn__myjg == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(fmp__hlz, gmn__myjg)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, timedelta64_dtype)
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                axi__wbnsj = rhs.value
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    fmp__hlz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        csvfi__maib[ojkp__rnsc])
                    if fmp__hlz == wsqip__mjba or axi__wbnsj == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(fmp__hlz, axi__wbnsj)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, timedelta64_dtype)
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                axi__wbnsj = lhs.value
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    fmp__hlz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        csvfi__maib[ojkp__rnsc])
                    if axi__wbnsj == wsqip__mjba or fmp__hlz == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(axi__wbnsj, fmp__hlz)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, dt64_dtype)
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                plow__ddptr = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                gmn__myjg = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(plow__ddptr))
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    fmp__hlz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        csvfi__maib[ojkp__rnsc])
                    if fmp__hlz == wsqip__mjba or gmn__myjg == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(fmp__hlz, gmn__myjg)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, dt64_dtype)
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                plow__ddptr = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                gmn__myjg = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(plow__ddptr))
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    fmp__hlz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        csvfi__maib[ojkp__rnsc])
                    if fmp__hlz == wsqip__mjba or gmn__myjg == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(fmp__hlz, gmn__myjg)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, timedelta64_dtype)
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                wll__ifsbb = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                fmp__hlz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wll__ifsbb)
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    alzoi__kwwdv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if alzoi__kwwdv == wsqip__mjba or fmp__hlz == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(alzoi__kwwdv, fmp__hlz)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, timedelta64_dtype)
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                wll__ifsbb = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                fmp__hlz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    wll__ifsbb)
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    alzoi__kwwdv = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if fmp__hlz == wsqip__mjba or alzoi__kwwdv == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(fmp__hlz, alzoi__kwwdv)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ujet__zvalr = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                csvfi__maib = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, timedelta64_dtype)
                wsqip__mjba = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ujet__zvalr))
                plow__ddptr = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                gmn__myjg = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(plow__ddptr))
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    pnoq__rec = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if gmn__myjg == wsqip__mjba or pnoq__rec == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(pnoq__rec, gmn__myjg)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ujet__zvalr = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                csvfi__maib = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yagn__bybm = len(csvfi__maib)
                smz__vgf = np.empty(yagn__bybm, timedelta64_dtype)
                wsqip__mjba = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ujet__zvalr))
                plow__ddptr = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                gmn__myjg = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(plow__ddptr))
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    pnoq__rec = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if gmn__myjg == wsqip__mjba or pnoq__rec == wsqip__mjba:
                        jdq__zuh = wsqip__mjba
                    else:
                        jdq__zuh = op(gmn__myjg, pnoq__rec)
                    smz__vgf[ojkp__rnsc
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        jdq__zuh)
                return bodo.hiframes.pd_series_ext.init_series(smz__vgf,
                    jdi__tlrck, ioqys__pbb)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            uckob__ojcl = True
        else:
            uckob__ojcl = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ujet__zvalr = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                csvfi__maib = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yagn__bybm = len(csvfi__maib)
                isihd__xzd = bodo.libs.bool_arr_ext.alloc_bool_array(yagn__bybm
                    )
                wsqip__mjba = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ujet__zvalr))
                ovzza__otsp = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                ewyi__xmtdk = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ovzza__otsp))
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    jcg__ocxwr = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if jcg__ocxwr == wsqip__mjba or ewyi__xmtdk == wsqip__mjba:
                        jdq__zuh = uckob__ojcl
                    else:
                        jdq__zuh = op(jcg__ocxwr, ewyi__xmtdk)
                    isihd__xzd[ojkp__rnsc] = jdq__zuh
                return bodo.hiframes.pd_series_ext.init_series(isihd__xzd,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            ujet__zvalr = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                csvfi__maib = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yagn__bybm = len(csvfi__maib)
                isihd__xzd = bodo.libs.bool_arr_ext.alloc_bool_array(yagn__bybm
                    )
                wsqip__mjba = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ujet__zvalr))
                gfdf__pfy = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                jcg__ocxwr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(gfdf__pfy))
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    ewyi__xmtdk = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if jcg__ocxwr == wsqip__mjba or ewyi__xmtdk == wsqip__mjba:
                        jdq__zuh = uckob__ojcl
                    else:
                        jdq__zuh = op(jcg__ocxwr, ewyi__xmtdk)
                    isihd__xzd[ojkp__rnsc] = jdq__zuh
                return bodo.hiframes.pd_series_ext.init_series(isihd__xzd,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yagn__bybm = len(csvfi__maib)
                isihd__xzd = bodo.libs.bool_arr_ext.alloc_bool_array(yagn__bybm
                    )
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    jcg__ocxwr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if jcg__ocxwr == wsqip__mjba or rhs.value == wsqip__mjba:
                        jdq__zuh = uckob__ojcl
                    else:
                        jdq__zuh = op(jcg__ocxwr, rhs.value)
                    isihd__xzd[ojkp__rnsc] = jdq__zuh
                return bodo.hiframes.pd_series_ext.init_series(isihd__xzd,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                yagn__bybm = len(csvfi__maib)
                isihd__xzd = bodo.libs.bool_arr_ext.alloc_bool_array(yagn__bybm
                    )
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    ewyi__xmtdk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if ewyi__xmtdk == wsqip__mjba or lhs.value == wsqip__mjba:
                        jdq__zuh = uckob__ojcl
                    else:
                        jdq__zuh = op(lhs.value, ewyi__xmtdk)
                    isihd__xzd[ojkp__rnsc] = jdq__zuh
                return bodo.hiframes.pd_series_ext.init_series(isihd__xzd,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                yagn__bybm = len(csvfi__maib)
                isihd__xzd = bodo.libs.bool_arr_ext.alloc_bool_array(yagn__bybm
                    )
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                xnrds__dlevz = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(rhs))
                fojon__nhlxz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    xnrds__dlevz)
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    jcg__ocxwr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if (jcg__ocxwr == wsqip__mjba or fojon__nhlxz ==
                        wsqip__mjba):
                        jdq__zuh = uckob__ojcl
                    else:
                        jdq__zuh = op(jcg__ocxwr, fojon__nhlxz)
                    isihd__xzd[ojkp__rnsc] = jdq__zuh
                return bodo.hiframes.pd_series_ext.init_series(isihd__xzd,
                    jdi__tlrck, ioqys__pbb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            ujet__zvalr = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                wfwu__sdgjr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                csvfi__maib = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    wfwu__sdgjr)
                jdi__tlrck = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ioqys__pbb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                yagn__bybm = len(csvfi__maib)
                isihd__xzd = bodo.libs.bool_arr_ext.alloc_bool_array(yagn__bybm
                    )
                wsqip__mjba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ujet__zvalr)
                xnrds__dlevz = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(lhs))
                fojon__nhlxz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    xnrds__dlevz)
                for ojkp__rnsc in numba.parfors.parfor.internal_prange(
                    yagn__bybm):
                    wll__ifsbb = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(csvfi__maib[ojkp__rnsc]))
                    if (wll__ifsbb == wsqip__mjba or fojon__nhlxz ==
                        wsqip__mjba):
                        jdq__zuh = uckob__ojcl
                    else:
                        jdq__zuh = op(fojon__nhlxz, wll__ifsbb)
                    isihd__xzd[ojkp__rnsc] = jdq__zuh
                return bodo.hiframes.pd_series_ext.init_series(isihd__xzd,
                    jdi__tlrck, ioqys__pbb)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for acgyu__zgj in series_dt_unsupported_attrs:
        xrkxx__mhmi = 'Series.dt.' + acgyu__zgj
        overload_attribute(SeriesDatetimePropertiesType, acgyu__zgj)(
            create_unsupported_overload(xrkxx__mhmi))
    for fdm__hzyf in series_dt_unsupported_methods:
        xrkxx__mhmi = 'Series.dt.' + fdm__hzyf
        overload_method(SeriesDatetimePropertiesType, fdm__hzyf,
            no_unliteral=True)(create_unsupported_overload(xrkxx__mhmi))


_install_series_dt_unsupported()
