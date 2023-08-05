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
        lrqg__fqjyx = lhs.data if isinstance(lhs, SeriesType) else lhs
        lga__wex = rhs.data if isinstance(rhs, SeriesType) else rhs
        if lrqg__fqjyx in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and lga__wex.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            lrqg__fqjyx = lga__wex.dtype
        elif lga__wex in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and lrqg__fqjyx.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            lga__wex = lrqg__fqjyx.dtype
        vxp__iox = lrqg__fqjyx, lga__wex
        bnnvq__jdg = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            dqtdp__cfbs = self.context.resolve_function_type(self.key,
                vxp__iox, {}).return_type
        except Exception as tgtmg__wqrfa:
            raise BodoError(bnnvq__jdg)
        if is_overload_bool(dqtdp__cfbs):
            raise BodoError(bnnvq__jdg)
        tvfm__uyvg = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        sglc__dnwb = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        ihzpw__abn = types.bool_
        dpky__zzs = SeriesType(ihzpw__abn, dqtdp__cfbs, tvfm__uyvg, sglc__dnwb)
        return dpky__zzs(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        qfmf__kwo = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if qfmf__kwo is None:
            qfmf__kwo = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, qfmf__kwo, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        lrqg__fqjyx = lhs.data if isinstance(lhs, SeriesType) else lhs
        lga__wex = rhs.data if isinstance(rhs, SeriesType) else rhs
        vxp__iox = lrqg__fqjyx, lga__wex
        bnnvq__jdg = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            dqtdp__cfbs = self.context.resolve_function_type(self.key,
                vxp__iox, {}).return_type
        except Exception as riq__ovpyy:
            raise BodoError(bnnvq__jdg)
        tvfm__uyvg = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        sglc__dnwb = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        ihzpw__abn = dqtdp__cfbs.dtype
        dpky__zzs = SeriesType(ihzpw__abn, dqtdp__cfbs, tvfm__uyvg, sglc__dnwb)
        return dpky__zzs(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        qfmf__kwo = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if qfmf__kwo is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                qfmf__kwo = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, qfmf__kwo, sig, args)
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
            qfmf__kwo = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return qfmf__kwo(lhs, rhs)
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
            qfmf__kwo = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return qfmf__kwo(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    ulgi__zmw = lhs == datetime_timedelta_type and rhs == datetime_date_type
    jbmkv__nyaq = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return ulgi__zmw or jbmkv__nyaq


def add_timestamp(lhs, rhs):
    hcrl__fnx = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    jyxgo__lvfm = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return hcrl__fnx or jyxgo__lvfm


def add_datetime_and_timedeltas(lhs, rhs):
    waui__sev = [datetime_timedelta_type, pd_timedelta_type]
    vmkwp__jibw = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    cwqy__npx = lhs in waui__sev and rhs in waui__sev
    upg__vwtx = (lhs == datetime_datetime_type and rhs in waui__sev or rhs ==
        datetime_datetime_type and lhs in waui__sev)
    return cwqy__npx or upg__vwtx


def mul_string_arr_and_int(lhs, rhs):
    lga__wex = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    lrqg__fqjyx = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return lga__wex or lrqg__fqjyx


def mul_timedelta_and_int(lhs, rhs):
    ulgi__zmw = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    jbmkv__nyaq = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return ulgi__zmw or jbmkv__nyaq


def mul_date_offset_and_int(lhs, rhs):
    ktak__zmg = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    btl__sub = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return ktak__zmg or btl__sub


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    orxja__llcs = [datetime_datetime_type, pd_timestamp_type,
        datetime_date_type]
    jixyq__bww = [date_offset_type, month_begin_type, month_end_type, week_type
        ]
    return rhs in jixyq__bww and lhs in orxja__llcs


def sub_dt_index_and_timestamp(lhs, rhs):
    khxbb__esgmy = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    dzcwr__glui = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return khxbb__esgmy or dzcwr__glui


def sub_dt_or_td(lhs, rhs):
    gxzbf__jjz = lhs == datetime_date_type and rhs == datetime_timedelta_type
    pigz__vhn = lhs == datetime_date_type and rhs == datetime_date_type
    bcnvf__xyv = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return gxzbf__jjz or pigz__vhn or bcnvf__xyv


def sub_datetime_and_timedeltas(lhs, rhs):
    hfsts__ifmid = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    euacg__saspy = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return hfsts__ifmid or euacg__saspy


def div_timedelta_and_int(lhs, rhs):
    cwqy__npx = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    jzc__hzwrd = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return cwqy__npx or jzc__hzwrd


def div_datetime_timedelta(lhs, rhs):
    cwqy__npx = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    jzc__hzwrd = lhs == datetime_timedelta_type and rhs == types.int64
    return cwqy__npx or jzc__hzwrd


def mod_timedeltas(lhs, rhs):
    kjemp__jtk = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    rdqqv__nwu = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return kjemp__jtk or rdqqv__nwu


def cmp_dt_index_to_string(lhs, rhs):
    khxbb__esgmy = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    dzcwr__glui = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return khxbb__esgmy or dzcwr__glui


def cmp_timestamp_or_date(lhs, rhs):
    mds__qzio = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    fufis__fnl = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        rhs == pd_timestamp_type)
    mrxsc__krcl = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    zad__drpzm = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    mbueg__pexpw = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return mds__qzio or fufis__fnl or mrxsc__krcl or zad__drpzm or mbueg__pexpw


def cmp_timeseries(lhs, rhs):
    ajojv__qrb = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    fcjrz__pmmkk = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (
        bodo.utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs
        .str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    kmd__axk = ajojv__qrb or fcjrz__pmmkk
    tvlpy__asi = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    jqqzo__ves = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    olnc__eaafb = tvlpy__asi or jqqzo__ves
    return kmd__axk or olnc__eaafb


def cmp_timedeltas(lhs, rhs):
    cwqy__npx = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in cwqy__npx and rhs in cwqy__npx


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    dnkwq__zwtj = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return dnkwq__zwtj


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    vzq__trkpb = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    fdxl__gzec = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    rrm__ponfl = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    dins__jvf = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return vzq__trkpb or fdxl__gzec or rrm__ponfl or dins__jvf


def args_td_and_int_array(lhs, rhs):
    gneu__nutoi = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    snqw__xmh = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return gneu__nutoi and snqw__xmh


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        jbmkv__nyaq = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        ulgi__zmw = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        cngo__zol = jbmkv__nyaq or ulgi__zmw
        itnb__ksz = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        iin__imhe = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        tng__ljhl = itnb__ksz or iin__imhe
        zqspn__ojki = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        dji__cfzb = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        bqkvt__lfde = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        bqti__hknr = zqspn__ojki or dji__cfzb or bqkvt__lfde
        qss__rhnu = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        xea__cwjqu = isinstance(lhs, tys) or isinstance(rhs, tys)
        hlcku__ywn = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (cngo__zol or tng__ljhl or bqti__hknr or qss__rhnu or
            xea__cwjqu or hlcku__ywn)
    if op == operator.pow:
        qiz__hrq = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        mncyx__rtp = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        bqkvt__lfde = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        hlcku__ywn = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return qiz__hrq or mncyx__rtp or bqkvt__lfde or hlcku__ywn
    if op == operator.floordiv:
        dji__cfzb = lhs in types.real_domain and rhs in types.real_domain
        zqspn__ojki = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        elni__bvdk = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        cwqy__npx = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        hlcku__ywn = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (dji__cfzb or zqspn__ojki or elni__bvdk or cwqy__npx or
            hlcku__ywn)
    if op == operator.truediv:
        hlh__xlnvf = lhs in machine_ints and rhs in machine_ints
        dji__cfzb = lhs in types.real_domain and rhs in types.real_domain
        bqkvt__lfde = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        zqspn__ojki = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        elni__bvdk = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        tbsf__oovrv = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        cwqy__npx = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        hlcku__ywn = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (hlh__xlnvf or dji__cfzb or bqkvt__lfde or zqspn__ojki or
            elni__bvdk or tbsf__oovrv or cwqy__npx or hlcku__ywn)
    if op == operator.mod:
        hlh__xlnvf = lhs in machine_ints and rhs in machine_ints
        dji__cfzb = lhs in types.real_domain and rhs in types.real_domain
        zqspn__ojki = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        elni__bvdk = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        hlcku__ywn = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (hlh__xlnvf or dji__cfzb or zqspn__ojki or elni__bvdk or
            hlcku__ywn)
    if op == operator.add or op == operator.sub:
        cngo__zol = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        aehnj__mvwm = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        gmr__ysjo = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        yidt__kdmly = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        zqspn__ojki = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        dji__cfzb = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        bqkvt__lfde = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        bqti__hknr = zqspn__ojki or dji__cfzb or bqkvt__lfde
        hlcku__ywn = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        lvagu__xvu = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        qss__rhnu = isinstance(lhs, types.List) and isinstance(rhs, types.List)
        dkyb__faba = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        jbh__moo = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        xqrqp__fgst = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        ece__gyz = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        atxs__hgn = dkyb__faba or jbh__moo or xqrqp__fgst or ece__gyz
        tng__ljhl = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        gxo__xdkwf = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        wwxp__wtcc = tng__ljhl or gxo__xdkwf
        waodl__hlapy = lhs == types.NPTimedelta and rhs == types.NPDatetime
        zci__vfnp = (lvagu__xvu or qss__rhnu or atxs__hgn or wwxp__wtcc or
            waodl__hlapy)
        hhz__ekh = op == operator.add and zci__vfnp
        return (cngo__zol or aehnj__mvwm or gmr__ysjo or yidt__kdmly or
            bqti__hknr or hlcku__ywn or hhz__ekh)


def cmp_op_supported_by_numba(lhs, rhs):
    hlcku__ywn = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    qss__rhnu = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    cngo__zol = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    ash__akfho = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    tng__ljhl = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    lvagu__xvu = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types
        .BaseTuple)
    yidt__kdmly = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    bqti__hknr = isinstance(lhs, types.Number) and isinstance(rhs, types.Number
        )
    fnk__glc = isinstance(lhs, types.Boolean) and isinstance(rhs, types.Boolean
        )
    gvc__ljfcc = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    djsnl__krztk = isinstance(lhs, types.DictType) and isinstance(rhs,
        types.DictType)
    vrqi__otro = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    buhy__ebyvn = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (qss__rhnu or cngo__zol or ash__akfho or tng__ljhl or lvagu__xvu or
        yidt__kdmly or bqti__hknr or fnk__glc or gvc__ljfcc or djsnl__krztk or
        hlcku__ywn or vrqi__otro or buhy__ebyvn)


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
        avpq__gpwh = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(avpq__gpwh)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        avpq__gpwh = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(avpq__gpwh)


install_arith_ops()
