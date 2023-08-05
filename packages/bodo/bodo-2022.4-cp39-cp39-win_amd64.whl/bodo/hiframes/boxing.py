"""
Boxing and unboxing support for DataFrame, Series, etc.
"""
import datetime
import decimal
import warnings
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.ir_utils import GuardException, guard
from numba.core.typing import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, intrinsic, typeof_impl, unbox
from numba.np import numpy_support
from numba.typed.typeddict import Dict
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFramePayloadType, DataFrameType, check_runtime_cols_unsupported, construct_dataframe
from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType, typeof_pd_int_dtype
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType, PandasDatetimeTZDtype
from bodo.libs.str_arr_ext import string_array_type, string_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import BodoError, BodoWarning, dtype_to_array_type, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
ll.add_symbol('is_np_array', hstr_ext.is_np_array)
ll.add_symbol('array_size', hstr_ext.array_size)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
TABLE_FORMAT_THRESHOLD = 20
_use_dict_str_type = False


def _set_bodo_meta_in_pandas():
    if '_bodo_meta' not in pd.Series._metadata:
        pd.Series._metadata.append('_bodo_meta')
    if '_bodo_meta' not in pd.DataFrame._metadata:
        pd.DataFrame._metadata.append('_bodo_meta')


_set_bodo_meta_in_pandas()


@typeof_impl.register(pd.DataFrame)
def typeof_pd_dataframe(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    yjawy__prwvn = tuple(val.columns.to_list())
    dteg__ewt = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        jrmn__omnwo = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        jrmn__omnwo = numba.typeof(val.index)
    fdcag__kozbo = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    himul__fwig = len(dteg__ewt) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(dteg__ewt, jrmn__omnwo, yjawy__prwvn, fdcag__kozbo,
        is_table_format=himul__fwig)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    fdcag__kozbo = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        fdbvf__yxqsw = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        fdbvf__yxqsw = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    yac__dbkk = dtype_to_array_type(dtype)
    if _use_dict_str_type and yac__dbkk == string_array_type:
        yac__dbkk = bodo.dict_str_arr_type
    return SeriesType(dtype, data=yac__dbkk, index=fdbvf__yxqsw, name_typ=
        numba.typeof(val.name), dist=fdcag__kozbo)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    emvgz__jikmn = c.pyapi.object_getattr_string(val, 'index')
    oolig__fwuo = c.pyapi.to_native_value(typ.index, emvgz__jikmn).value
    c.pyapi.decref(emvgz__jikmn)
    if typ.is_table_format:
        ztn__nmex = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        ztn__nmex.parent = val
        for oldnv__lpbe, qzc__oid in typ.table_type.type_to_blk.items():
            uukm__syi = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[qzc__oid]))
            nalz__fgvzr, qatq__apqjh = ListInstance.allocate_ex(c.context,
                c.builder, types.List(oldnv__lpbe), uukm__syi)
            qatq__apqjh.size = uukm__syi
            setattr(ztn__nmex, f'block_{qzc__oid}', qatq__apqjh.value)
        alnvl__dqjj = c.pyapi.call_method(val, '__len__', ())
        sibx__ken = c.pyapi.long_as_longlong(alnvl__dqjj)
        c.pyapi.decref(alnvl__dqjj)
        ztn__nmex.len = sibx__ken
        ovp__rtqq = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [ztn__nmex._getvalue()])
    else:
        vor__zyf = [c.context.get_constant_null(oldnv__lpbe) for
            oldnv__lpbe in typ.data]
        ovp__rtqq = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            vor__zyf)
    ccp__rkitd = construct_dataframe(c.context, c.builder, typ, ovp__rtqq,
        oolig__fwuo, val, None)
    return NativeValue(ccp__rkitd)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        nkvtz__xilao = df._bodo_meta['type_metadata'][1]
    else:
        nkvtz__xilao = [None] * len(df.columns)
    frem__ibs = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=nkvtz__xilao[i])) for i in range(len(df.columns))]
    frem__ibs = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        oldnv__lpbe == string_array_type else oldnv__lpbe) for oldnv__lpbe in
        frem__ibs]
    return tuple(frem__ibs)


class SeriesDtypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Datime_Date = 13
    NP_Datetime64ns = 14
    NP_Timedelta64ns = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 21
    ARRAY = 22
    PD_nullable_Int8 = 23
    PD_nullable_UInt8 = 24
    PD_nullable_Int16 = 25
    PD_nullable_UInt16 = 26
    PD_nullable_Int32 = 27
    PD_nullable_UInt32 = 28
    PD_nullable_Int64 = 29
    PD_nullable_UInt64 = 30
    PD_nullable_bool = 31
    CategoricalType = 32
    NoneType = 33
    Literal = 34
    IntegerArray = 35
    RangeIndexType = 36
    DatetimeIndexType = 37
    NumericIndexType = 38
    PeriodIndexType = 39
    IntervalIndexType = 40
    CategoricalIndexType = 41
    StringIndexType = 42
    BinaryIndexType = 43
    TimedeltaIndexType = 44
    LiteralType = 45


_one_to_one_type_to_enum_map = {types.int8: SeriesDtypeEnum.Int8.value,
    types.uint8: SeriesDtypeEnum.UInt8.value, types.int32: SeriesDtypeEnum.
    Int32.value, types.uint32: SeriesDtypeEnum.UInt32.value, types.int64:
    SeriesDtypeEnum.Int64.value, types.uint64: SeriesDtypeEnum.UInt64.value,
    types.float32: SeriesDtypeEnum.Float32.value, types.float64:
    SeriesDtypeEnum.Float64.value, types.NPDatetime('ns'): SeriesDtypeEnum.
    NP_Datetime64ns.value, types.NPTimedelta('ns'): SeriesDtypeEnum.
    NP_Timedelta64ns.value, types.bool_: SeriesDtypeEnum.Bool.value, types.
    int16: SeriesDtypeEnum.Int16.value, types.uint16: SeriesDtypeEnum.
    UInt16.value, types.Integer('int128', 128): SeriesDtypeEnum.Int128.
    value, bodo.hiframes.datetime_date_ext.datetime_date_type:
    SeriesDtypeEnum.Datime_Date.value, IntDtype(types.int8):
    SeriesDtypeEnum.PD_nullable_Int8.value, IntDtype(types.uint8):
    SeriesDtypeEnum.PD_nullable_UInt8.value, IntDtype(types.int16):
    SeriesDtypeEnum.PD_nullable_Int16.value, IntDtype(types.uint16):
    SeriesDtypeEnum.PD_nullable_UInt16.value, IntDtype(types.int32):
    SeriesDtypeEnum.PD_nullable_Int32.value, IntDtype(types.uint32):
    SeriesDtypeEnum.PD_nullable_UInt32.value, IntDtype(types.int64):
    SeriesDtypeEnum.PD_nullable_Int64.value, IntDtype(types.uint64):
    SeriesDtypeEnum.PD_nullable_UInt64.value, bytes_type: SeriesDtypeEnum.
    BINARY.value, string_type: SeriesDtypeEnum.STRING.value, bodo.bool_:
    SeriesDtypeEnum.Bool.value, types.none: SeriesDtypeEnum.NoneType.value}
_one_to_one_enum_to_type_map = {SeriesDtypeEnum.Int8.value: types.int8,
    SeriesDtypeEnum.UInt8.value: types.uint8, SeriesDtypeEnum.Int32.value:
    types.int32, SeriesDtypeEnum.UInt32.value: types.uint32,
    SeriesDtypeEnum.Int64.value: types.int64, SeriesDtypeEnum.UInt64.value:
    types.uint64, SeriesDtypeEnum.Float32.value: types.float32,
    SeriesDtypeEnum.Float64.value: types.float64, SeriesDtypeEnum.
    NP_Datetime64ns.value: types.NPDatetime('ns'), SeriesDtypeEnum.
    NP_Timedelta64ns.value: types.NPTimedelta('ns'), SeriesDtypeEnum.Int16.
    value: types.int16, SeriesDtypeEnum.UInt16.value: types.uint16,
    SeriesDtypeEnum.Int128.value: types.Integer('int128', 128),
    SeriesDtypeEnum.Datime_Date.value: bodo.hiframes.datetime_date_ext.
    datetime_date_type, SeriesDtypeEnum.PD_nullable_Int8.value: IntDtype(
    types.int8), SeriesDtypeEnum.PD_nullable_UInt8.value: IntDtype(types.
    uint8), SeriesDtypeEnum.PD_nullable_Int16.value: IntDtype(types.int16),
    SeriesDtypeEnum.PD_nullable_UInt16.value: IntDtype(types.uint16),
    SeriesDtypeEnum.PD_nullable_Int32.value: IntDtype(types.int32),
    SeriesDtypeEnum.PD_nullable_UInt32.value: IntDtype(types.uint32),
    SeriesDtypeEnum.PD_nullable_Int64.value: IntDtype(types.int64),
    SeriesDtypeEnum.PD_nullable_UInt64.value: IntDtype(types.uint64),
    SeriesDtypeEnum.BINARY.value: bytes_type, SeriesDtypeEnum.STRING.value:
    string_type, SeriesDtypeEnum.Bool.value: bodo.bool_, SeriesDtypeEnum.
    NoneType.value: types.none}


def _dtype_from_type_enum_list(typ_enum_list):
    jyn__pxxmm, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(jyn__pxxmm) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {jyn__pxxmm}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        fmr__dmsh, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return fmr__dmsh, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        fmr__dmsh, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return fmr__dmsh, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        cjrbn__gjz = typ_enum_list[1]
        ywk__zzqmy = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(cjrbn__gjz, ywk__zzqmy)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        ncnbx__zgwxd = typ_enum_list[1]
        tvy__akof = tuple(typ_enum_list[2:2 + ncnbx__zgwxd])
        eiemv__clnz = typ_enum_list[2 + ncnbx__zgwxd:]
        mkbsf__xgzm = []
        for i in range(ncnbx__zgwxd):
            eiemv__clnz, fpr__nfqo = _dtype_from_type_enum_list_recursor(
                eiemv__clnz)
            mkbsf__xgzm.append(fpr__nfqo)
        return eiemv__clnz, StructType(tuple(mkbsf__xgzm), tvy__akof)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        zirx__nmxfq = typ_enum_list[1]
        eiemv__clnz = typ_enum_list[2:]
        return eiemv__clnz, zirx__nmxfq
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        zirx__nmxfq = typ_enum_list[1]
        eiemv__clnz = typ_enum_list[2:]
        return eiemv__clnz, numba.types.literal(zirx__nmxfq)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        eiemv__clnz, ucl__hhhv = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        eiemv__clnz, onple__cmwxi = _dtype_from_type_enum_list_recursor(
            eiemv__clnz)
        eiemv__clnz, jhr__gaux = _dtype_from_type_enum_list_recursor(
            eiemv__clnz)
        eiemv__clnz, prwmu__artd = _dtype_from_type_enum_list_recursor(
            eiemv__clnz)
        eiemv__clnz, vgiv__zvhkx = _dtype_from_type_enum_list_recursor(
            eiemv__clnz)
        return eiemv__clnz, PDCategoricalDtype(ucl__hhhv, onple__cmwxi,
            jhr__gaux, prwmu__artd, vgiv__zvhkx)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        eiemv__clnz, vyp__zwkza = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return eiemv__clnz, DatetimeIndexType(vyp__zwkza)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        eiemv__clnz, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        eiemv__clnz, vyp__zwkza = _dtype_from_type_enum_list_recursor(
            eiemv__clnz)
        eiemv__clnz, prwmu__artd = _dtype_from_type_enum_list_recursor(
            eiemv__clnz)
        return eiemv__clnz, NumericIndexType(dtype, vyp__zwkza, prwmu__artd)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        eiemv__clnz, bsmi__oyhd = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        eiemv__clnz, vyp__zwkza = _dtype_from_type_enum_list_recursor(
            eiemv__clnz)
        return eiemv__clnz, PeriodIndexType(bsmi__oyhd, vyp__zwkza)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        eiemv__clnz, prwmu__artd = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        eiemv__clnz, vyp__zwkza = _dtype_from_type_enum_list_recursor(
            eiemv__clnz)
        return eiemv__clnz, CategoricalIndexType(prwmu__artd, vyp__zwkza)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        eiemv__clnz, vyp__zwkza = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return eiemv__clnz, RangeIndexType(vyp__zwkza)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        eiemv__clnz, vyp__zwkza = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return eiemv__clnz, StringIndexType(vyp__zwkza)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        eiemv__clnz, vyp__zwkza = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return eiemv__clnz, BinaryIndexType(vyp__zwkza)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        eiemv__clnz, vyp__zwkza = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return eiemv__clnz, TimedeltaIndexType(vyp__zwkza)
    else:
        raise_bodo_error(
            f'Unexpected Internal Error while converting typing metadata: unable to infer dtype for type enum {typ_enum_list[0]}. Please file the error here: https://github.com/Bodo-inc/Feedback'
            )


def _dtype_to_type_enum_list(typ):
    return guard(_dtype_to_type_enum_list_recursor, typ)


def _dtype_to_type_enum_list_recursor(typ, upcast_numeric_index=True):
    if typ.__hash__ and typ in _one_to_one_type_to_enum_map:
        return [_one_to_one_type_to_enum_map[typ]]
    if isinstance(typ, (dict, int, list, tuple, str, bool, bytes, float)):
        return [SeriesDtypeEnum.Literal.value, typ]
    elif typ is None:
        return [SeriesDtypeEnum.Literal.value, typ]
    elif is_overload_constant_int(typ):
        elru__bjesk = get_overload_const_int(typ)
        if numba.types.maybe_literal(elru__bjesk) == typ:
            return [SeriesDtypeEnum.LiteralType.value, elru__bjesk]
    elif is_overload_constant_str(typ):
        elru__bjesk = get_overload_const_str(typ)
        if numba.types.maybe_literal(elru__bjesk) == typ:
            return [SeriesDtypeEnum.LiteralType.value, elru__bjesk]
    elif is_overload_constant_bool(typ):
        elru__bjesk = get_overload_const_bool(typ)
        if numba.types.maybe_literal(elru__bjesk) == typ:
            return [SeriesDtypeEnum.LiteralType.value, elru__bjesk]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        oea__vwajv = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for ezg__jjj in typ.names:
            oea__vwajv.append(ezg__jjj)
        for ccys__eduly in typ.data:
            oea__vwajv += _dtype_to_type_enum_list_recursor(ccys__eduly)
        return oea__vwajv
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        bdoad__qlcp = _dtype_to_type_enum_list_recursor(typ.categories)
        dcdix__eaxp = _dtype_to_type_enum_list_recursor(typ.elem_type)
        pvmci__gluhh = _dtype_to_type_enum_list_recursor(typ.ordered)
        iwko__bdk = _dtype_to_type_enum_list_recursor(typ.data)
        vzk__ojr = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + bdoad__qlcp + dcdix__eaxp + pvmci__gluhh + iwko__bdk + vzk__ojr
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                lsjbh__nod = types.float64
                xdpu__jypl = types.Array(lsjbh__nod, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                lsjbh__nod = types.int64
                xdpu__jypl = types.Array(lsjbh__nod, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                lsjbh__nod = types.uint64
                xdpu__jypl = types.Array(lsjbh__nod, 1, 'C')
            elif typ.dtype == types.bool_:
                lsjbh__nod = typ.dtype
                xdpu__jypl = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(lsjbh__nod
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(xdpu__jypl)
        else:
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(typ.dtype
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(typ.data)
    elif isinstance(typ, PeriodIndexType):
        return [SeriesDtypeEnum.PeriodIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.freq
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, CategoricalIndexType):
        return [SeriesDtypeEnum.CategoricalIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.data
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, RangeIndexType):
        return [SeriesDtypeEnum.RangeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, StringIndexType):
        return [SeriesDtypeEnum.StringIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, BinaryIndexType):
        return [SeriesDtypeEnum.BinaryIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, TimedeltaIndexType):
        return [SeriesDtypeEnum.TimedeltaIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    else:
        raise GuardException('Unable to convert type')


def _infer_series_dtype(S, array_metadata=None):
    if S.dtype == np.dtype('O'):
        if len(S.values) == 0:
            if (hasattr(S, '_bodo_meta') and S._bodo_meta is not None and 
                'type_metadata' in S._bodo_meta and S._bodo_meta[
                'type_metadata'][1] is not None):
                yzad__rpu = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(yzad__rpu)
            elif array_metadata != None:
                return _dtype_from_type_enum_list(array_metadata).dtype
        return numba.typeof(S.values).dtype
    if isinstance(S.dtype, pd.core.arrays.integer._IntegerDtype):
        return typeof_pd_int_dtype(S.dtype, None)
    elif isinstance(S.dtype, pd.CategoricalDtype):
        return bodo.typeof(S.dtype)
    elif isinstance(S.dtype, pd.StringDtype):
        return string_type
    elif isinstance(S.dtype, pd.BooleanDtype):
        return types.bool_
    if isinstance(S.dtype, pd.DatetimeTZDtype):
        regii__mwzny = S.dtype.unit
        if regii__mwzny != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        bhbg__pxljv = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.
            dtype.tz)
        return PandasDatetimeTZDtype(bhbg__pxljv)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    tyfj__rwlt = cgutils.is_not_null(builder, parent_obj)
    xuyn__zqz = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(tyfj__rwlt):
        qayyh__lvpbg = pyapi.object_getattr_string(parent_obj, 'columns')
        alnvl__dqjj = pyapi.call_method(qayyh__lvpbg, '__len__', ())
        builder.store(pyapi.long_as_longlong(alnvl__dqjj), xuyn__zqz)
        pyapi.decref(alnvl__dqjj)
        pyapi.decref(qayyh__lvpbg)
    use_parent_obj = builder.and_(tyfj__rwlt, builder.icmp_unsigned('==',
        builder.load(xuyn__zqz), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        qzq__bfh = df_typ.runtime_colname_typ
        context.nrt.incref(builder, qzq__bfh, dataframe_payload.columns)
        return pyapi.from_native_value(qzq__bfh, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        pwski__ems = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        pwski__ems = pd.array(df_typ.columns, 'string')
    else:
        pwski__ems = df_typ.columns
    esle__ktjkv = numba.typeof(pwski__ems)
    zgv__xnlkq = context.get_constant_generic(builder, esle__ktjkv, pwski__ems)
    qqc__pyx = pyapi.from_native_value(esle__ktjkv, zgv__xnlkq, c.env_manager)
    return qqc__pyx


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (ggb__svyr, yjxnz__witb):
        with ggb__svyr:
            pyapi.incref(obj)
            lrrqu__owjiu = context.insert_const_string(c.builder.module,
                'numpy')
            otpfc__aoh = pyapi.import_module_noblock(lrrqu__owjiu)
            if df_typ.has_runtime_cols:
                whin__fmo = 0
            else:
                whin__fmo = len(df_typ.columns)
            kwcws__bwgsw = pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), whin__fmo))
            fwtp__cto = pyapi.call_method(otpfc__aoh, 'arange', (kwcws__bwgsw,)
                )
            pyapi.object_setattr_string(obj, 'columns', fwtp__cto)
            pyapi.decref(otpfc__aoh)
            pyapi.decref(fwtp__cto)
            pyapi.decref(kwcws__bwgsw)
        with yjxnz__witb:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            off__evv = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            lrrqu__owjiu = context.insert_const_string(c.builder.module,
                'pandas')
            otpfc__aoh = pyapi.import_module_noblock(lrrqu__owjiu)
            df_obj = pyapi.call_method(otpfc__aoh, 'DataFrame', (pyapi.
                borrow_none(), off__evv))
            pyapi.decref(otpfc__aoh)
            pyapi.decref(off__evv)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    tzxt__fknl = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = tzxt__fknl.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        xrq__zww = typ.table_type
        ztn__nmex = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, xrq__zww, ztn__nmex)
        bvd__lryas = box_table(xrq__zww, ztn__nmex, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (jxmyp__xaj, aff__eotz):
            with jxmyp__xaj:
                pixpa__auhlu = pyapi.object_getattr_string(bvd__lryas, 'arrays'
                    )
                dqq__jpj = c.pyapi.make_none()
                if n_cols is None:
                    alnvl__dqjj = pyapi.call_method(pixpa__auhlu, '__len__', ()
                        )
                    uukm__syi = pyapi.long_as_longlong(alnvl__dqjj)
                    pyapi.decref(alnvl__dqjj)
                else:
                    uukm__syi = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, uukm__syi) as eae__vxi:
                    i = eae__vxi.index
                    lhpih__zqtyx = pyapi.list_getitem(pixpa__auhlu, i)
                    oyqv__jhr = c.builder.icmp_unsigned('!=', lhpih__zqtyx,
                        dqq__jpj)
                    with builder.if_then(oyqv__jhr):
                        zwyr__bbrfu = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, zwyr__bbrfu, lhpih__zqtyx)
                        pyapi.decref(zwyr__bbrfu)
                pyapi.decref(pixpa__auhlu)
                pyapi.decref(dqq__jpj)
            with aff__eotz:
                df_obj = builder.load(res)
                off__evv = pyapi.object_getattr_string(df_obj, 'index')
                jops__rymac = c.pyapi.call_method(bvd__lryas, 'to_pandas',
                    (off__evv,))
                builder.store(jops__rymac, res)
                pyapi.decref(df_obj)
                pyapi.decref(off__evv)
        pyapi.decref(bvd__lryas)
    else:
        fosop__iuop = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        jiynb__rmef = typ.data
        for i, fqwp__fxm, yac__dbkk in zip(range(n_cols), fosop__iuop,
            jiynb__rmef):
            ubdxc__dxjr = cgutils.alloca_once_value(builder, fqwp__fxm)
            pdya__xvh = cgutils.alloca_once_value(builder, context.
                get_constant_null(yac__dbkk))
            oyqv__jhr = builder.not_(is_ll_eq(builder, ubdxc__dxjr, pdya__xvh))
            hnk__lpqa = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, oyqv__jhr))
            with builder.if_then(hnk__lpqa):
                zwyr__bbrfu = pyapi.long_from_longlong(context.get_constant
                    (types.int64, i))
                context.nrt.incref(builder, yac__dbkk, fqwp__fxm)
                arr_obj = pyapi.from_native_value(yac__dbkk, fqwp__fxm, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, zwyr__bbrfu, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(zwyr__bbrfu)
    df_obj = builder.load(res)
    qqc__pyx = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', qqc__pyx)
    pyapi.decref(qqc__pyx)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    dqq__jpj = pyapi.borrow_none()
    yvwpq__gvon = pyapi.unserialize(pyapi.serialize_object(slice))
    swbvs__pvue = pyapi.call_function_objargs(yvwpq__gvon, [dqq__jpj])
    nze__hxhwp = pyapi.long_from_longlong(col_ind)
    mcl__ivm = pyapi.tuple_pack([swbvs__pvue, nze__hxhwp])
    ioq__jflge = pyapi.object_getattr_string(df_obj, 'iloc')
    zdlsp__qif = pyapi.object_getitem(ioq__jflge, mcl__ivm)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        ercl__gmza = pyapi.object_getattr_string(zdlsp__qif, 'array')
    else:
        ercl__gmza = pyapi.object_getattr_string(zdlsp__qif, 'values')
    if isinstance(data_typ, types.Array):
        jztkj__mdcp = context.insert_const_string(builder.module, 'numpy')
        spgnx__hbvhr = pyapi.import_module_noblock(jztkj__mdcp)
        arr_obj = pyapi.call_method(spgnx__hbvhr, 'ascontiguousarray', (
            ercl__gmza,))
        pyapi.decref(ercl__gmza)
        pyapi.decref(spgnx__hbvhr)
    else:
        arr_obj = ercl__gmza
    pyapi.decref(yvwpq__gvon)
    pyapi.decref(swbvs__pvue)
    pyapi.decref(nze__hxhwp)
    pyapi.decref(mcl__ivm)
    pyapi.decref(ioq__jflge)
    pyapi.decref(zdlsp__qif)
    return arr_obj


@intrinsic
def unbox_dataframe_column(typingctx, df, i=None):
    assert isinstance(df, DataFrameType) and is_overload_constant_int(i)

    def codegen(context, builder, sig, args):
        pyapi = context.get_python_api(builder)
        c = numba.core.pythonapi._UnboxContext(context, builder, pyapi)
        df_typ = sig.args[0]
        col_ind = get_overload_const_int(sig.args[1])
        data_typ = df_typ.data[col_ind]
        tzxt__fknl = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            tzxt__fknl.parent, args[1], data_typ)
        ygh__bunw = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            ztn__nmex = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            qzc__oid = df_typ.table_type.type_to_blk[data_typ]
            fmz__wsr = getattr(ztn__nmex, f'block_{qzc__oid}')
            rckal__xncu = ListInstance(c.context, c.builder, types.List(
                data_typ), fmz__wsr)
            qjw__tezay = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            rckal__xncu.inititem(qjw__tezay, ygh__bunw.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, ygh__bunw.value, col_ind)
        rojpl__fsz = DataFramePayloadType(df_typ)
        qbku__ppcv = context.nrt.meminfo_data(builder, tzxt__fknl.meminfo)
        jiau__lap = context.get_value_type(rojpl__fsz).as_pointer()
        qbku__ppcv = builder.bitcast(qbku__ppcv, jiau__lap)
        builder.store(dataframe_payload._getvalue(), qbku__ppcv)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        ercl__gmza = c.pyapi.object_getattr_string(val, 'array')
    else:
        ercl__gmza = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        jztkj__mdcp = c.context.insert_const_string(c.builder.module, 'numpy')
        spgnx__hbvhr = c.pyapi.import_module_noblock(jztkj__mdcp)
        arr_obj = c.pyapi.call_method(spgnx__hbvhr, 'ascontiguousarray', (
            ercl__gmza,))
        c.pyapi.decref(ercl__gmza)
        c.pyapi.decref(spgnx__hbvhr)
    else:
        arr_obj = ercl__gmza
    furjs__hddrn = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    off__evv = c.pyapi.object_getattr_string(val, 'index')
    oolig__fwuo = c.pyapi.to_native_value(typ.index, off__evv).value
    uzq__oeqkf = c.pyapi.object_getattr_string(val, 'name')
    zmrfe__sphc = c.pyapi.to_native_value(typ.name_typ, uzq__oeqkf).value
    xhwm__naxw = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, furjs__hddrn, oolig__fwuo, zmrfe__sphc)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(off__evv)
    c.pyapi.decref(uzq__oeqkf)
    return NativeValue(xhwm__naxw)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        hpygs__nbut = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(hpygs__nbut._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    lrrqu__owjiu = c.context.insert_const_string(c.builder.module, 'pandas')
    lnixn__mpl = c.pyapi.import_module_noblock(lrrqu__owjiu)
    wtjw__ppll = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, wtjw__ppll.data)
    c.context.nrt.incref(c.builder, typ.index, wtjw__ppll.index)
    c.context.nrt.incref(c.builder, typ.name_typ, wtjw__ppll.name)
    arr_obj = c.pyapi.from_native_value(typ.data, wtjw__ppll.data, c.
        env_manager)
    off__evv = c.pyapi.from_native_value(typ.index, wtjw__ppll.index, c.
        env_manager)
    uzq__oeqkf = c.pyapi.from_native_value(typ.name_typ, wtjw__ppll.name, c
        .env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(lnixn__mpl, 'Series', (arr_obj, off__evv,
        dtype, uzq__oeqkf))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(off__evv)
    c.pyapi.decref(uzq__oeqkf)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(lnixn__mpl)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    shtbd__ygm = []
    for ihs__cauzd in typ_list:
        if isinstance(ihs__cauzd, int) and not isinstance(ihs__cauzd, bool):
            emc__vcibz = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), ihs__cauzd))
        else:
            cti__uxfrs = numba.typeof(ihs__cauzd)
            zzr__dwnb = context.get_constant_generic(builder, cti__uxfrs,
                ihs__cauzd)
            emc__vcibz = pyapi.from_native_value(cti__uxfrs, zzr__dwnb,
                env_manager)
        shtbd__ygm.append(emc__vcibz)
    famw__uzfy = pyapi.list_pack(shtbd__ygm)
    for val in shtbd__ygm:
        pyapi.decref(val)
    return famw__uzfy


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    buj__bao = not typ.has_runtime_cols and (not typ.is_table_format or len
        (typ.columns) < TABLE_FORMAT_THRESHOLD)
    fzhu__eza = 2 if buj__bao else 1
    jlpt__alm = pyapi.dict_new(fzhu__eza)
    ibiy__mrswp = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    pyapi.dict_setitem_string(jlpt__alm, 'dist', ibiy__mrswp)
    pyapi.decref(ibiy__mrswp)
    if buj__bao:
        yqx__novp = _dtype_to_type_enum_list(typ.index)
        if yqx__novp != None:
            miool__drkr = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, yqx__novp)
        else:
            miool__drkr = pyapi.make_none()
        iugmn__lqls = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                famw__uzfy = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                famw__uzfy = pyapi.make_none()
            iugmn__lqls.append(famw__uzfy)
        hrrk__eipe = pyapi.list_pack(iugmn__lqls)
        aajlm__zda = pyapi.list_pack([miool__drkr, hrrk__eipe])
        for val in iugmn__lqls:
            pyapi.decref(val)
        pyapi.dict_setitem_string(jlpt__alm, 'type_metadata', aajlm__zda)
    pyapi.object_setattr_string(obj, '_bodo_meta', jlpt__alm)
    pyapi.decref(jlpt__alm)


def get_series_dtype_handle_null_int_and_hetrogenous(series_typ):
    if isinstance(series_typ, HeterogeneousSeriesType):
        return None
    if isinstance(series_typ.dtype, types.Number) and isinstance(series_typ
        .data, IntegerArrayType):
        return IntDtype(series_typ.dtype)
    return series_typ.dtype


def _set_bodo_meta_series(obj, c, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    jlpt__alm = pyapi.dict_new(2)
    ibiy__mrswp = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    yqx__novp = _dtype_to_type_enum_list(typ.index)
    if yqx__novp != None:
        miool__drkr = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, yqx__novp)
    else:
        miool__drkr = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            bkc__gijya = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            bkc__gijya = pyapi.make_none()
    else:
        bkc__gijya = pyapi.make_none()
    vpzix__zmitj = pyapi.list_pack([miool__drkr, bkc__gijya])
    pyapi.dict_setitem_string(jlpt__alm, 'type_metadata', vpzix__zmitj)
    pyapi.decref(vpzix__zmitj)
    pyapi.dict_setitem_string(jlpt__alm, 'dist', ibiy__mrswp)
    pyapi.object_setattr_string(obj, '_bodo_meta', jlpt__alm)
    pyapi.decref(jlpt__alm)
    pyapi.decref(ibiy__mrswp)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as qjk__ucp:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    iqni__tgrry = numba.np.numpy_support.map_layout(val)
    glo__lyi = not val.flags.writeable
    return types.Array(dtype, val.ndim, iqni__tgrry, readonly=glo__lyi)


def _infer_ndarray_obj_dtype(val):
    if not val.dtype == np.dtype('O'):
        raise BodoError('Unsupported array dtype: {}'.format(val.dtype))
    i = 0
    while i < len(val) and (pd.api.types.is_scalar(val[i]) and pd.isna(val[
        i]) or not pd.api.types.is_scalar(val[i]) and len(val[i]) == 0):
        i += 1
    if i == len(val):
        warnings.warn(BodoWarning(
            'Empty object array passed to Bodo, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    qgxi__gczly = val[i]
    if isinstance(qgxi__gczly, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(qgxi__gczly, bytes):
        return binary_array_type
    elif isinstance(qgxi__gczly, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(qgxi__gczly, (int, np.int8, np.int16, np.int32, np.
        int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(qgxi__gczly)
            )
    elif isinstance(qgxi__gczly, (dict, Dict)) and all(isinstance(agzr__unr,
        str) for agzr__unr in qgxi__gczly.keys()):
        tvy__akof = tuple(qgxi__gczly.keys())
        drdjw__wygzc = tuple(_get_struct_value_arr_type(v) for v in
            qgxi__gczly.values())
        return StructArrayType(drdjw__wygzc, tvy__akof)
    elif isinstance(qgxi__gczly, (dict, Dict)):
        gblnz__ndnl = numba.typeof(_value_to_array(list(qgxi__gczly.keys())))
        wbht__aiz = numba.typeof(_value_to_array(list(qgxi__gczly.values())))
        gblnz__ndnl = to_str_arr_if_dict_array(gblnz__ndnl)
        wbht__aiz = to_str_arr_if_dict_array(wbht__aiz)
        return MapArrayType(gblnz__ndnl, wbht__aiz)
    elif isinstance(qgxi__gczly, tuple):
        drdjw__wygzc = tuple(_get_struct_value_arr_type(v) for v in qgxi__gczly
            )
        return TupleArrayType(drdjw__wygzc)
    if isinstance(qgxi__gczly, (list, np.ndarray, pd.arrays.BooleanArray,
        pd.arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(qgxi__gczly, list):
            qgxi__gczly = _value_to_array(qgxi__gczly)
        ddmjg__izy = numba.typeof(qgxi__gczly)
        ddmjg__izy = to_str_arr_if_dict_array(ddmjg__izy)
        return ArrayItemArrayType(ddmjg__izy)
    if isinstance(qgxi__gczly, datetime.date):
        return datetime_date_array_type
    if isinstance(qgxi__gczly, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(qgxi__gczly, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(f'Unsupported object array with first value: {qgxi__gczly}'
        )


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    uehg__hdu = val.copy()
    uehg__hdu.append(None)
    fqwp__fxm = np.array(uehg__hdu, np.object_)
    if len(val) and isinstance(val[0], float):
        fqwp__fxm = np.array(val, np.float64)
    return fqwp__fxm


def _get_struct_value_arr_type(v):
    if isinstance(v, (dict, Dict)):
        return numba.typeof(_value_to_array(v))
    if isinstance(v, list):
        return dtype_to_array_type(numba.typeof(_value_to_array(v)))
    if pd.api.types.is_scalar(v) and pd.isna(v):
        warnings.warn(BodoWarning(
            'Field value in struct array is NA, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    yac__dbkk = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        yac__dbkk = to_nullable_type(yac__dbkk)
    return yac__dbkk
