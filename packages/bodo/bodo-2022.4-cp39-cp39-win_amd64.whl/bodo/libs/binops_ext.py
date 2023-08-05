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
        kyasr__qsmb = lhs.data if isinstance(lhs, SeriesType) else lhs
        vtcv__rjn = rhs.data if isinstance(rhs, SeriesType) else rhs
        if kyasr__qsmb in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and vtcv__rjn.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            kyasr__qsmb = vtcv__rjn.dtype
        elif vtcv__rjn in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and kyasr__qsmb.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            vtcv__rjn = kyasr__qsmb.dtype
        sqiq__oaltr = kyasr__qsmb, vtcv__rjn
        xul__igynw = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            avm__lurf = self.context.resolve_function_type(self.key,
                sqiq__oaltr, {}).return_type
        except Exception as slab__mplz:
            raise BodoError(xul__igynw)
        if is_overload_bool(avm__lurf):
            raise BodoError(xul__igynw)
        imlc__sklec = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ohnqp__eriy = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        zkr__pgqde = types.bool_
        zerd__gvsyj = SeriesType(zkr__pgqde, avm__lurf, imlc__sklec,
            ohnqp__eriy)
        return zerd__gvsyj(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        wfd__ays = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if wfd__ays is None:
            wfd__ays = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, wfd__ays, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        kyasr__qsmb = lhs.data if isinstance(lhs, SeriesType) else lhs
        vtcv__rjn = rhs.data if isinstance(rhs, SeriesType) else rhs
        sqiq__oaltr = kyasr__qsmb, vtcv__rjn
        xul__igynw = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            avm__lurf = self.context.resolve_function_type(self.key,
                sqiq__oaltr, {}).return_type
        except Exception as yaqck__ssqh:
            raise BodoError(xul__igynw)
        imlc__sklec = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ohnqp__eriy = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        zkr__pgqde = avm__lurf.dtype
        zerd__gvsyj = SeriesType(zkr__pgqde, avm__lurf, imlc__sklec,
            ohnqp__eriy)
        return zerd__gvsyj(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        wfd__ays = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if wfd__ays is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                wfd__ays = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, wfd__ays, sig, args)
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
            wfd__ays = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return wfd__ays(lhs, rhs)
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
            wfd__ays = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return wfd__ays(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    epa__pdd = lhs == datetime_timedelta_type and rhs == datetime_date_type
    soc__cljd = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return epa__pdd or soc__cljd


def add_timestamp(lhs, rhs):
    lwzdt__pkg = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    bjbg__zjg = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return lwzdt__pkg or bjbg__zjg


def add_datetime_and_timedeltas(lhs, rhs):
    mpa__apg = [datetime_timedelta_type, pd_timedelta_type]
    caz__ckid = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    xipcb__uuvp = lhs in mpa__apg and rhs in mpa__apg
    dirm__xpuj = (lhs == datetime_datetime_type and rhs in mpa__apg or rhs ==
        datetime_datetime_type and lhs in mpa__apg)
    return xipcb__uuvp or dirm__xpuj


def mul_string_arr_and_int(lhs, rhs):
    vtcv__rjn = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    kyasr__qsmb = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return vtcv__rjn or kyasr__qsmb


def mul_timedelta_and_int(lhs, rhs):
    epa__pdd = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    soc__cljd = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return epa__pdd or soc__cljd


def mul_date_offset_and_int(lhs, rhs):
    aveck__coudh = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    rgecb__pgwq = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return aveck__coudh or rgecb__pgwq


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    ggta__wqzjw = [datetime_datetime_type, pd_timestamp_type,
        datetime_date_type]
    ier__aih = [date_offset_type, month_begin_type, month_end_type, week_type]
    return rhs in ier__aih and lhs in ggta__wqzjw


def sub_dt_index_and_timestamp(lhs, rhs):
    ctek__ndg = isinstance(lhs, DatetimeIndexType) and rhs == pd_timestamp_type
    cegg__oxsyi = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return ctek__ndg or cegg__oxsyi


def sub_dt_or_td(lhs, rhs):
    lgg__kco = lhs == datetime_date_type and rhs == datetime_timedelta_type
    dqj__iary = lhs == datetime_date_type and rhs == datetime_date_type
    szu__yjoyj = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return lgg__kco or dqj__iary or szu__yjoyj


def sub_datetime_and_timedeltas(lhs, rhs):
    rmryq__azg = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    kzfjk__dxif = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return rmryq__azg or kzfjk__dxif


def div_timedelta_and_int(lhs, rhs):
    xipcb__uuvp = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    ygkq__acfl = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return xipcb__uuvp or ygkq__acfl


def div_datetime_timedelta(lhs, rhs):
    xipcb__uuvp = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    ygkq__acfl = lhs == datetime_timedelta_type and rhs == types.int64
    return xipcb__uuvp or ygkq__acfl


def mod_timedeltas(lhs, rhs):
    pag__saur = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    rotfp__yryjt = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return pag__saur or rotfp__yryjt


def cmp_dt_index_to_string(lhs, rhs):
    ctek__ndg = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    cegg__oxsyi = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return ctek__ndg or cegg__oxsyi


def cmp_timestamp_or_date(lhs, rhs):
    qvtqb__mboxl = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    cwn__cnb = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        rhs == pd_timestamp_type)
    bnzk__pdnu = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    mge__upa = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    cyh__bew = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return qvtqb__mboxl or cwn__cnb or bnzk__pdnu or mge__upa or cyh__bew


def cmp_timeseries(lhs, rhs):
    woswe__jkd = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    hwf__oyo = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    ypwg__zndy = woswe__jkd or hwf__oyo
    drtwv__hehk = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    urxlm__sgdw = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    nws__nrul = drtwv__hehk or urxlm__sgdw
    return ypwg__zndy or nws__nrul


def cmp_timedeltas(lhs, rhs):
    xipcb__uuvp = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in xipcb__uuvp and rhs in xipcb__uuvp


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    ijvmj__rgcr = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return ijvmj__rgcr


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    vprfs__sstu = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    webo__zxiw = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    hngd__abyj = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    dunu__noj = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return vprfs__sstu or webo__zxiw or hngd__abyj or dunu__noj


def args_td_and_int_array(lhs, rhs):
    wlniq__rzw = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    virqz__hxl = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return wlniq__rzw and virqz__hxl


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        soc__cljd = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        epa__pdd = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        keq__qsppy = soc__cljd or epa__pdd
        vmggl__cub = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        mawx__gjmu = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        axabh__ygoyd = vmggl__cub or mawx__gjmu
        plobs__brtcu = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        gulk__ghhtc = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        elfi__gkzj = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        fhvm__okj = plobs__brtcu or gulk__ghhtc or elfi__gkzj
        palt__ffwy = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        wlrd__mtmi = isinstance(lhs, tys) or isinstance(rhs, tys)
        itzs__fahp = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (keq__qsppy or axabh__ygoyd or fhvm__okj or palt__ffwy or
            wlrd__mtmi or itzs__fahp)
    if op == operator.pow:
        wgtdo__ekmw = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        ozzug__yuo = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        elfi__gkzj = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        itzs__fahp = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return wgtdo__ekmw or ozzug__yuo or elfi__gkzj or itzs__fahp
    if op == operator.floordiv:
        gulk__ghhtc = lhs in types.real_domain and rhs in types.real_domain
        plobs__brtcu = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        bsqa__omyi = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        xipcb__uuvp = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        itzs__fahp = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (gulk__ghhtc or plobs__brtcu or bsqa__omyi or xipcb__uuvp or
            itzs__fahp)
    if op == operator.truediv:
        qcyy__gfdzo = lhs in machine_ints and rhs in machine_ints
        gulk__ghhtc = lhs in types.real_domain and rhs in types.real_domain
        elfi__gkzj = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        plobs__brtcu = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        bsqa__omyi = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        ktdhn__nofqm = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        xipcb__uuvp = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        itzs__fahp = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (qcyy__gfdzo or gulk__ghhtc or elfi__gkzj or plobs__brtcu or
            bsqa__omyi or ktdhn__nofqm or xipcb__uuvp or itzs__fahp)
    if op == operator.mod:
        qcyy__gfdzo = lhs in machine_ints and rhs in machine_ints
        gulk__ghhtc = lhs in types.real_domain and rhs in types.real_domain
        plobs__brtcu = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        bsqa__omyi = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        itzs__fahp = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (qcyy__gfdzo or gulk__ghhtc or plobs__brtcu or bsqa__omyi or
            itzs__fahp)
    if op == operator.add or op == operator.sub:
        keq__qsppy = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        jjr__geumn = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        mbbt__rxpwg = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        fnwpc__edqvx = isinstance(lhs, types.Set) and isinstance(rhs, types.Set
            )
        plobs__brtcu = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        gulk__ghhtc = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        elfi__gkzj = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        fhvm__okj = plobs__brtcu or gulk__ghhtc or elfi__gkzj
        itzs__fahp = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        gywj__teppt = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        palt__ffwy = isinstance(lhs, types.List) and isinstance(rhs, types.List
            )
        aki__bfz = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        kfx__odsg = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        yjswx__elboq = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs
            , types.UnicodeCharSeq)
        jjq__pjf = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        cdfqc__tkxt = aki__bfz or kfx__odsg or yjswx__elboq or jjq__pjf
        axabh__ygoyd = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        ocrrl__mboyo = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        mgqnt__latkw = axabh__ygoyd or ocrrl__mboyo
        npvn__kvmj = lhs == types.NPTimedelta and rhs == types.NPDatetime
        hijf__ljbw = (gywj__teppt or palt__ffwy or cdfqc__tkxt or
            mgqnt__latkw or npvn__kvmj)
        dopx__kzzzc = op == operator.add and hijf__ljbw
        return (keq__qsppy or jjr__geumn or mbbt__rxpwg or fnwpc__edqvx or
            fhvm__okj or itzs__fahp or dopx__kzzzc)


def cmp_op_supported_by_numba(lhs, rhs):
    itzs__fahp = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    palt__ffwy = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    keq__qsppy = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    bay__efm = isinstance(lhs, types.NPDatetime) and isinstance(rhs, types.
        NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    axabh__ygoyd = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    gywj__teppt = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    fnwpc__edqvx = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    fhvm__okj = isinstance(lhs, types.Number) and isinstance(rhs, types.Number)
    lssh__gbbo = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    ohiqy__mzdzl = isinstance(lhs, types.NoneType) or isinstance(rhs, types
        .NoneType)
    gowu__lbs = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    qtlx__zdg = isinstance(lhs, types.EnumMember) and isinstance(rhs, types
        .EnumMember)
    nojha__lskm = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (palt__ffwy or keq__qsppy or bay__efm or axabh__ygoyd or
        gywj__teppt or fnwpc__edqvx or fhvm__okj or lssh__gbbo or
        ohiqy__mzdzl or gowu__lbs or itzs__fahp or qtlx__zdg or nojha__lskm)


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
        vlyab__mcfk = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(vlyab__mcfk)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        vlyab__mcfk = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(vlyab__mcfk)


install_arith_ops()
