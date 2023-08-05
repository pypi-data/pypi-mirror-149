""" Implementation of binary operators for the different types.
    Currently implemented operators:
        arith: add, sub, mul, truediv, floordiv, mod, pow
        cmp: lt, le, eq, ne, ge, gt
"""
import operator
import numba
from numba.core import types
from numba.core.imputils import lower_builtin
from numba.core.typing.builtins import machine_ints
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type, datetime_timedelta_type
from bodo.hiframes.datetime_timedelta_ext import datetime_datetime_type, datetime_timedelta_array_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import DatetimeIndexType, HeterogeneousIndexType, is_index_type
from bodo.hiframes.pd_offsets_ext import date_offset_type, month_begin_type, month_end_type, week_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.series_impl import SeriesType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.typing import BodoError, is_overload_bool, is_str_arr_type, is_timedelta_type


class SeriesCmpOpTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lhs, rhs = args
        if cmp_timeseries(lhs, rhs) or (isinstance(lhs, DataFrameType) or
            isinstance(rhs, DataFrameType)) or not (isinstance(lhs,
            SeriesType) or isinstance(rhs, SeriesType)):
            return
        lizti__eynrf = lhs.data if isinstance(lhs, SeriesType) else lhs
        yygrd__efqd = rhs.data if isinstance(rhs, SeriesType) else rhs
        if lizti__eynrf in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and yygrd__efqd.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            lizti__eynrf = yygrd__efqd.dtype
        elif yygrd__efqd in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and lizti__eynrf.dtype in (bodo.datetime64ns, bodo.timedelta64ns
            ):
            yygrd__efqd = lizti__eynrf.dtype
        nnay__qwpa = lizti__eynrf, yygrd__efqd
        gjo__kng = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            fzq__vzv = self.context.resolve_function_type(self.key,
                nnay__qwpa, {}).return_type
        except Exception as wbb__ujf:
            raise BodoError(gjo__kng)
        if is_overload_bool(fzq__vzv):
            raise BodoError(gjo__kng)
        efc__friv = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ckxjv__fowo = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        zso__axery = types.bool_
        fluz__lbi = SeriesType(zso__axery, fzq__vzv, efc__friv, ckxjv__fowo)
        return fluz__lbi(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        eygd__fqi = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if eygd__fqi is None:
            eygd__fqi = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, eygd__fqi, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        lizti__eynrf = lhs.data if isinstance(lhs, SeriesType) else lhs
        yygrd__efqd = rhs.data if isinstance(rhs, SeriesType) else rhs
        nnay__qwpa = lizti__eynrf, yygrd__efqd
        gjo__kng = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            fzq__vzv = self.context.resolve_function_type(self.key,
                nnay__qwpa, {}).return_type
        except Exception as inele__ckei:
            raise BodoError(gjo__kng)
        efc__friv = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ckxjv__fowo = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        zso__axery = fzq__vzv.dtype
        fluz__lbi = SeriesType(zso__axery, fzq__vzv, efc__friv, ckxjv__fowo)
        return fluz__lbi(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        eygd__fqi = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if eygd__fqi is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                eygd__fqi = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, eygd__fqi, sig, args)
    return lower_and_or_impl


def overload_add_operator_scalars(lhs, rhs):
    if lhs == week_type or rhs == week_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_week_offset_type(lhs, rhs))
    if lhs == month_begin_type or rhs == month_begin_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_begin_offset_type(lhs, rhs))
    if lhs == month_end_type or rhs == month_end_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_end_offset_type(lhs, rhs))
    if lhs == date_offset_type or rhs == date_offset_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_date_offset_type(lhs, rhs))
    if add_timestamp(lhs, rhs):
        return bodo.hiframes.pd_timestamp_ext.overload_add_operator_timestamp(
            lhs, rhs)
    if add_dt_td_and_dt_date(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_add_operator_datetime_date(lhs, rhs))
    if add_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_add_operator_datetime_timedelta(lhs, rhs))
    raise_error_if_not_numba_supported(operator.add, lhs, rhs)


def overload_sub_operator_scalars(lhs, rhs):
    if sub_offset_to_datetime_or_timestamp(lhs, rhs):
        return bodo.hiframes.pd_offsets_ext.overload_sub_operator_offsets(lhs,
            rhs)
    if lhs == pd_timestamp_type and rhs in [pd_timestamp_type,
        datetime_timedelta_type, pd_timedelta_type]:
        return bodo.hiframes.pd_timestamp_ext.overload_sub_operator_timestamp(
            lhs, rhs)
    if sub_dt_or_td(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_sub_operator_datetime_date(lhs, rhs))
    if sub_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_sub_operator_datetime_timedelta(lhs, rhs))
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
        return (bodo.hiframes.datetime_datetime_ext.
            overload_sub_operator_datetime_datetime(lhs, rhs))
    raise_error_if_not_numba_supported(operator.sub, lhs, rhs)


def create_overload_arith_op(op):

    def overload_arith_operator(lhs, rhs):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
            f'{op} operator')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
            f'{op} operator')
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if time_series_operation(lhs, rhs) and op in [operator.add,
            operator.sub]:
            return bodo.hiframes.series_dt_impl.create_bin_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return bodo.hiframes.series_impl.create_binary_op_overload(op)(lhs,
                rhs)
        if sub_dt_index_and_timestamp(lhs, rhs) and op == operator.sub:
            return (bodo.hiframes.pd_index_ext.
                overload_sub_operator_datetime_index(lhs, rhs))
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if args_td_and_int_array(lhs, rhs):
            return bodo.libs.int_arr_ext.get_int_array_op_pd_td(op)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if op == operator.add and (is_str_arr_type(lhs) or types.unliteral(
            lhs) == string_type):
            return bodo.libs.str_arr_ext.overload_add_operator_string_array(lhs
                , rhs)
        if op == operator.add:
            return overload_add_operator_scalars(lhs, rhs)
        if op == operator.sub:
            return overload_sub_operator_scalars(lhs, rhs)
        if op == operator.mul:
            if mul_timedelta_and_int(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mul_operator_timedelta(lhs, rhs))
            if mul_string_arr_and_int(lhs, rhs):
                return bodo.libs.str_arr_ext.overload_mul_operator_str_arr(lhs,
                    rhs)
            if mul_date_offset_and_int(lhs, rhs):
                return (bodo.hiframes.pd_offsets_ext.
                    overload_mul_date_offset_types(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op in [operator.truediv, operator.floordiv]:
            if div_timedelta_and_int(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_pd_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_pd_timedelta(lhs, rhs))
            if div_datetime_timedelta(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_dt_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_dt_timedelta(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.mod:
            if mod_timedeltas(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mod_operator_timedeltas(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.pow:
            raise_error_if_not_numba_supported(op, lhs, rhs)
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_arith_operator


def create_overload_cmp_operator(op):

    def overload_cmp_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if cmp_timeseries(lhs, rhs):
            return bodo.hiframes.series_dt_impl.create_cmp_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
            f'{op} operator')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
            f'{op} operator')
        if lhs == datetime_date_array_type or rhs == datetime_date_array_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload_arr(
                op)(lhs, rhs)
        if (lhs == datetime_timedelta_array_type or rhs ==
            datetime_timedelta_array_type):
            eygd__fqi = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return eygd__fqi(lhs, rhs)
        if is_str_arr_type(lhs) or is_str_arr_type(rhs):
            return bodo.libs.str_arr_ext.create_binary_op_overload(op)(lhs, rhs
                )
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            return bodo.libs.decimal_arr_ext.decimal_create_cmp_op_overload(op
                )(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if binary_array_cmp(lhs, rhs):
            return bodo.libs.binary_arr_ext.create_binary_cmp_op_overload(op)(
                lhs, rhs)
        if cmp_dt_index_to_string(lhs, rhs):
            return bodo.hiframes.pd_index_ext.overload_binop_dti_str(op)(lhs,
                rhs)
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if lhs == datetime_date_type and rhs == datetime_date_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload(op)(
                lhs, rhs)
        if can_cmp_date_datetime(lhs, rhs, op):
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
            return bodo.hiframes.datetime_datetime_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:
            return bodo.hiframes.datetime_timedelta_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if cmp_timedeltas(lhs, rhs):
            eygd__fqi = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return eygd__fqi(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    plme__redaz = lhs == datetime_timedelta_type and rhs == datetime_date_type
    frxzh__jfq = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return plme__redaz or frxzh__jfq


def add_timestamp(lhs, rhs):
    luy__obd = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    eddgi__yss = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return luy__obd or eddgi__yss


def add_datetime_and_timedeltas(lhs, rhs):
    xzxn__pjl = [datetime_timedelta_type, pd_timedelta_type]
    umtj__arsw = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    zpd__lqyo = lhs in xzxn__pjl and rhs in xzxn__pjl
    snj__kzggg = (lhs == datetime_datetime_type and rhs in xzxn__pjl or rhs ==
        datetime_datetime_type and lhs in xzxn__pjl)
    return zpd__lqyo or snj__kzggg


def mul_string_arr_and_int(lhs, rhs):
    yygrd__efqd = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    lizti__eynrf = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return yygrd__efqd or lizti__eynrf


def mul_timedelta_and_int(lhs, rhs):
    plme__redaz = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    frxzh__jfq = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return plme__redaz or frxzh__jfq


def mul_date_offset_and_int(lhs, rhs):
    fvv__fpv = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    akdj__dae = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return fvv__fpv or akdj__dae


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    thpyu__vdft = [datetime_datetime_type, pd_timestamp_type,
        datetime_date_type]
    uhq__uzf = [date_offset_type, month_begin_type, month_end_type, week_type]
    return rhs in uhq__uzf and lhs in thpyu__vdft


def sub_dt_index_and_timestamp(lhs, rhs):
    srgxj__orhui = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    dkzr__zxu = isinstance(rhs, DatetimeIndexType) and lhs == pd_timestamp_type
    return srgxj__orhui or dkzr__zxu


def sub_dt_or_td(lhs, rhs):
    icaj__jwy = lhs == datetime_date_type and rhs == datetime_timedelta_type
    zhvd__phrb = lhs == datetime_date_type and rhs == datetime_date_type
    kbg__ywf = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return icaj__jwy or zhvd__phrb or kbg__ywf


def sub_datetime_and_timedeltas(lhs, rhs):
    jidg__lpw = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    vjo__zeaa = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return jidg__lpw or vjo__zeaa


def div_timedelta_and_int(lhs, rhs):
    zpd__lqyo = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    ufq__hxvn = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return zpd__lqyo or ufq__hxvn


def div_datetime_timedelta(lhs, rhs):
    zpd__lqyo = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    ufq__hxvn = lhs == datetime_timedelta_type and rhs == types.int64
    return zpd__lqyo or ufq__hxvn


def mod_timedeltas(lhs, rhs):
    kni__mnf = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    mgpvr__wqvgh = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return kni__mnf or mgpvr__wqvgh


def cmp_dt_index_to_string(lhs, rhs):
    srgxj__orhui = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    dkzr__zxu = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return srgxj__orhui or dkzr__zxu


def cmp_timestamp_or_date(lhs, rhs):
    taebd__lrix = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    cxra__dyhb = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        rhs == pd_timestamp_type)
    cuh__arae = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    dzaav__hnoyz = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    xvxn__sfl = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return taebd__lrix or cxra__dyhb or cuh__arae or dzaav__hnoyz or xvxn__sfl


def cmp_timeseries(lhs, rhs):
    bulhq__tgiub = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (
        bodo.utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs
        .str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    xkb__qfeog = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    xock__eho = bulhq__tgiub or xkb__qfeog
    gbn__ygzc = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    bhz__trux = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    jipva__efy = gbn__ygzc or bhz__trux
    return xock__eho or jipva__efy


def cmp_timedeltas(lhs, rhs):
    zpd__lqyo = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in zpd__lqyo and rhs in zpd__lqyo


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    zdpe__brvsf = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return zdpe__brvsf


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    kykpe__mbzxl = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    zhm__nufd = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    teobu__ycptw = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    nfon__inthe = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return kykpe__mbzxl or zhm__nufd or teobu__ycptw or nfon__inthe


def args_td_and_int_array(lhs, rhs):
    dxg__plznu = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    ttqr__bpof = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return dxg__plznu and ttqr__bpof


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        frxzh__jfq = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        plme__redaz = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        pinpf__tnbl = frxzh__jfq or plme__redaz
        vtnh__nutl = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        yhv__pty = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        brej__ltstt = vtnh__nutl or yhv__pty
        febc__uqam = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        zmp__omk = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        ywnha__rlanf = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        dvtan__ota = febc__uqam or zmp__omk or ywnha__rlanf
        yydj__ort = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        oja__pnywv = isinstance(lhs, tys) or isinstance(rhs, tys)
        aqv__kggi = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return (pinpf__tnbl or brej__ltstt or dvtan__ota or yydj__ort or
            oja__pnywv or aqv__kggi)
    if op == operator.pow:
        fizg__wglri = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        jckjd__dmvci = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        ywnha__rlanf = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        aqv__kggi = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return fizg__wglri or jckjd__dmvci or ywnha__rlanf or aqv__kggi
    if op == operator.floordiv:
        zmp__omk = lhs in types.real_domain and rhs in types.real_domain
        febc__uqam = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        darnm__tlzp = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        zpd__lqyo = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        aqv__kggi = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return zmp__omk or febc__uqam or darnm__tlzp or zpd__lqyo or aqv__kggi
    if op == operator.truediv:
        bxkz__xjh = lhs in machine_ints and rhs in machine_ints
        zmp__omk = lhs in types.real_domain and rhs in types.real_domain
        ywnha__rlanf = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        febc__uqam = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        darnm__tlzp = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        qphv__ydj = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        zpd__lqyo = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        aqv__kggi = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return (bxkz__xjh or zmp__omk or ywnha__rlanf or febc__uqam or
            darnm__tlzp or qphv__ydj or zpd__lqyo or aqv__kggi)
    if op == operator.mod:
        bxkz__xjh = lhs in machine_ints and rhs in machine_ints
        zmp__omk = lhs in types.real_domain and rhs in types.real_domain
        febc__uqam = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        darnm__tlzp = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        aqv__kggi = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return bxkz__xjh or zmp__omk or febc__uqam or darnm__tlzp or aqv__kggi
    if op == operator.add or op == operator.sub:
        pinpf__tnbl = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        wpyt__wibqp = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        fby__vcq = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        makic__ymicb = isinstance(lhs, types.Set) and isinstance(rhs, types.Set
            )
        febc__uqam = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        zmp__omk = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        ywnha__rlanf = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        dvtan__ota = febc__uqam or zmp__omk or ywnha__rlanf
        aqv__kggi = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        yjieg__vpaqz = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        yydj__ort = isinstance(lhs, types.List) and isinstance(rhs, types.List)
        qruy__womyq = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        ffgl__ajgb = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        veaz__gdxey = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        pkxmw__casac = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        tkz__uccj = qruy__womyq or ffgl__ajgb or veaz__gdxey or pkxmw__casac
        brej__ltstt = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        xjtsk__kdcsm = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        adgil__rdgn = brej__ltstt or xjtsk__kdcsm
        qqcxa__jfbh = lhs == types.NPTimedelta and rhs == types.NPDatetime
        hrj__wpy = (yjieg__vpaqz or yydj__ort or tkz__uccj or adgil__rdgn or
            qqcxa__jfbh)
        zkabq__mwimg = op == operator.add and hrj__wpy
        return (pinpf__tnbl or wpyt__wibqp or fby__vcq or makic__ymicb or
            dvtan__ota or aqv__kggi or zkabq__mwimg)


def cmp_op_supported_by_numba(lhs, rhs):
    aqv__kggi = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    yydj__ort = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    pinpf__tnbl = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    gyn__vdv = isinstance(lhs, types.NPDatetime) and isinstance(rhs, types.
        NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    brej__ltstt = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    yjieg__vpaqz = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    makic__ymicb = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    dvtan__ota = isinstance(lhs, types.Number) and isinstance(rhs, types.Number
        )
    kvn__llkee = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    qhib__sknu = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    jhufa__egjqk = isinstance(lhs, types.DictType) and isinstance(rhs,
        types.DictType)
    nntm__jggx = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    qmjbp__pratn = isinstance(lhs, types.Literal) and isinstance(rhs, types
        .Literal)
    return (yydj__ort or pinpf__tnbl or gyn__vdv or brej__ltstt or
        yjieg__vpaqz or makic__ymicb or dvtan__ota or kvn__llkee or
        qhib__sknu or jhufa__egjqk or aqv__kggi or nntm__jggx or qmjbp__pratn)


def raise_error_if_not_numba_supported(op, lhs, rhs):
    if arith_op_supported_by_numba(op, lhs, rhs):
        return
    raise BodoError(
        f'{op} operator not supported for data types {lhs} and {rhs}.')


def _install_series_and_or():
    for op in (operator.or_, operator.and_):
        infer_global(op)(SeriesAndOrTyper)
        lower_impl = lower_series_and_or(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)


_install_series_and_or()


def _install_cmp_ops():
    for op in (operator.lt, operator.eq, operator.ne, operator.ge, operator
        .gt, operator.le):
        infer_global(op)(SeriesCmpOpTemplate)
        lower_impl = series_cmp_op_lower(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)
        bna__kwdgs = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(bna__kwdgs)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        bna__kwdgs = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(bna__kwdgs)


install_arith_ops()
