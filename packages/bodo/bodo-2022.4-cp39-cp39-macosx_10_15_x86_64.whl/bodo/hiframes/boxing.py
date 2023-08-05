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
    ubix__jwbd = tuple(val.columns.to_list())
    euo__mnpvt = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        cnba__psky = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        cnba__psky = numba.typeof(val.index)
    qgv__tikti = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    mfr__rnp = len(euo__mnpvt) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(euo__mnpvt, cnba__psky, ubix__jwbd, qgv__tikti,
        is_table_format=mfr__rnp)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    qgv__tikti = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        anla__lde = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        anla__lde = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    dvbb__shacq = dtype_to_array_type(dtype)
    if _use_dict_str_type and dvbb__shacq == string_array_type:
        dvbb__shacq = bodo.dict_str_arr_type
    return SeriesType(dtype, data=dvbb__shacq, index=anla__lde, name_typ=
        numba.typeof(val.name), dist=qgv__tikti)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    xwj__tdj = c.pyapi.object_getattr_string(val, 'index')
    mifza__rzkhm = c.pyapi.to_native_value(typ.index, xwj__tdj).value
    c.pyapi.decref(xwj__tdj)
    if typ.is_table_format:
        waxyq__ijs = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        waxyq__ijs.parent = val
        for kcsst__tru, fgn__iim in typ.table_type.type_to_blk.items():
            xtxkn__rxc = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[fgn__iim]))
            jer__ozu, lhi__zmghd = ListInstance.allocate_ex(c.context, c.
                builder, types.List(kcsst__tru), xtxkn__rxc)
            lhi__zmghd.size = xtxkn__rxc
            setattr(waxyq__ijs, f'block_{fgn__iim}', lhi__zmghd.value)
        drv__ytucx = c.pyapi.call_method(val, '__len__', ())
        rtpfv__lwr = c.pyapi.long_as_longlong(drv__ytucx)
        c.pyapi.decref(drv__ytucx)
        waxyq__ijs.len = rtpfv__lwr
        tjrz__qjan = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [waxyq__ijs._getvalue()])
    else:
        ugi__szsxl = [c.context.get_constant_null(kcsst__tru) for
            kcsst__tru in typ.data]
        tjrz__qjan = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            ugi__szsxl)
    ngzgi__uway = construct_dataframe(c.context, c.builder, typ, tjrz__qjan,
        mifza__rzkhm, val, None)
    return NativeValue(ngzgi__uway)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        yjb__zebf = df._bodo_meta['type_metadata'][1]
    else:
        yjb__zebf = [None] * len(df.columns)
    akla__iki = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=yjb__zebf[i])) for i in range(len(df.columns))]
    akla__iki = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        kcsst__tru == string_array_type else kcsst__tru) for kcsst__tru in
        akla__iki]
    return tuple(akla__iki)


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
    vak__xhqb, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(vak__xhqb) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {vak__xhqb}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        tfdkg__jjua, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return tfdkg__jjua, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        tfdkg__jjua, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return tfdkg__jjua, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        bslpu__gfr = typ_enum_list[1]
        vxp__cmku = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(bslpu__gfr, vxp__cmku)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        ska__ghl = typ_enum_list[1]
        iqeos__cega = tuple(typ_enum_list[2:2 + ska__ghl])
        qmxux__uqwye = typ_enum_list[2 + ska__ghl:]
        oilns__lhkc = []
        for i in range(ska__ghl):
            qmxux__uqwye, ipj__rjz = _dtype_from_type_enum_list_recursor(
                qmxux__uqwye)
            oilns__lhkc.append(ipj__rjz)
        return qmxux__uqwye, StructType(tuple(oilns__lhkc), iqeos__cega)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        tqr__vakm = typ_enum_list[1]
        qmxux__uqwye = typ_enum_list[2:]
        return qmxux__uqwye, tqr__vakm
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        tqr__vakm = typ_enum_list[1]
        qmxux__uqwye = typ_enum_list[2:]
        return qmxux__uqwye, numba.types.literal(tqr__vakm)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        qmxux__uqwye, cqr__uao = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        qmxux__uqwye, osreg__paaqp = _dtype_from_type_enum_list_recursor(
            qmxux__uqwye)
        qmxux__uqwye, nco__oadyo = _dtype_from_type_enum_list_recursor(
            qmxux__uqwye)
        qmxux__uqwye, lrkg__prakg = _dtype_from_type_enum_list_recursor(
            qmxux__uqwye)
        qmxux__uqwye, ecd__peuv = _dtype_from_type_enum_list_recursor(
            qmxux__uqwye)
        return qmxux__uqwye, PDCategoricalDtype(cqr__uao, osreg__paaqp,
            nco__oadyo, lrkg__prakg, ecd__peuv)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        qmxux__uqwye, kwetb__tfiyi = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return qmxux__uqwye, DatetimeIndexType(kwetb__tfiyi)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        qmxux__uqwye, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        qmxux__uqwye, kwetb__tfiyi = _dtype_from_type_enum_list_recursor(
            qmxux__uqwye)
        qmxux__uqwye, lrkg__prakg = _dtype_from_type_enum_list_recursor(
            qmxux__uqwye)
        return qmxux__uqwye, NumericIndexType(dtype, kwetb__tfiyi, lrkg__prakg)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        qmxux__uqwye, stf__kqtxo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        qmxux__uqwye, kwetb__tfiyi = _dtype_from_type_enum_list_recursor(
            qmxux__uqwye)
        return qmxux__uqwye, PeriodIndexType(stf__kqtxo, kwetb__tfiyi)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        qmxux__uqwye, lrkg__prakg = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        qmxux__uqwye, kwetb__tfiyi = _dtype_from_type_enum_list_recursor(
            qmxux__uqwye)
        return qmxux__uqwye, CategoricalIndexType(lrkg__prakg, kwetb__tfiyi)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        qmxux__uqwye, kwetb__tfiyi = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return qmxux__uqwye, RangeIndexType(kwetb__tfiyi)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        qmxux__uqwye, kwetb__tfiyi = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return qmxux__uqwye, StringIndexType(kwetb__tfiyi)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        qmxux__uqwye, kwetb__tfiyi = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return qmxux__uqwye, BinaryIndexType(kwetb__tfiyi)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        qmxux__uqwye, kwetb__tfiyi = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return qmxux__uqwye, TimedeltaIndexType(kwetb__tfiyi)
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
        edmri__kkdz = get_overload_const_int(typ)
        if numba.types.maybe_literal(edmri__kkdz) == typ:
            return [SeriesDtypeEnum.LiteralType.value, edmri__kkdz]
    elif is_overload_constant_str(typ):
        edmri__kkdz = get_overload_const_str(typ)
        if numba.types.maybe_literal(edmri__kkdz) == typ:
            return [SeriesDtypeEnum.LiteralType.value, edmri__kkdz]
    elif is_overload_constant_bool(typ):
        edmri__kkdz = get_overload_const_bool(typ)
        if numba.types.maybe_literal(edmri__kkdz) == typ:
            return [SeriesDtypeEnum.LiteralType.value, edmri__kkdz]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        uxao__wbyb = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for dqre__wpfny in typ.names:
            uxao__wbyb.append(dqre__wpfny)
        for ivi__xdx in typ.data:
            uxao__wbyb += _dtype_to_type_enum_list_recursor(ivi__xdx)
        return uxao__wbyb
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        cpu__crhlt = _dtype_to_type_enum_list_recursor(typ.categories)
        aun__lhusy = _dtype_to_type_enum_list_recursor(typ.elem_type)
        dzfen__qunoj = _dtype_to_type_enum_list_recursor(typ.ordered)
        ude__jpuuc = _dtype_to_type_enum_list_recursor(typ.data)
        nrt__oqvos = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + cpu__crhlt + aun__lhusy + dzfen__qunoj + ude__jpuuc + nrt__oqvos
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                kzdo__ctw = types.float64
                ziriv__ugho = types.Array(kzdo__ctw, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                kzdo__ctw = types.int64
                ziriv__ugho = types.Array(kzdo__ctw, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                kzdo__ctw = types.uint64
                ziriv__ugho = types.Array(kzdo__ctw, 1, 'C')
            elif typ.dtype == types.bool_:
                kzdo__ctw = typ.dtype
                ziriv__ugho = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(kzdo__ctw
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(ziriv__ugho)
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
                anvc__rir = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(anvc__rir)
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
        qfaq__tsni = S.dtype.unit
        if qfaq__tsni != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        rqmd__yxi = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.dtype.tz
            )
        return PandasDatetimeTZDtype(rqmd__yxi)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    apiz__sph = cgutils.is_not_null(builder, parent_obj)
    bkayh__jdbtb = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(apiz__sph):
        bupgm__bqaao = pyapi.object_getattr_string(parent_obj, 'columns')
        drv__ytucx = pyapi.call_method(bupgm__bqaao, '__len__', ())
        builder.store(pyapi.long_as_longlong(drv__ytucx), bkayh__jdbtb)
        pyapi.decref(drv__ytucx)
        pyapi.decref(bupgm__bqaao)
    use_parent_obj = builder.and_(apiz__sph, builder.icmp_unsigned('==',
        builder.load(bkayh__jdbtb), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        kvx__tok = df_typ.runtime_colname_typ
        context.nrt.incref(builder, kvx__tok, dataframe_payload.columns)
        return pyapi.from_native_value(kvx__tok, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        zwa__oucg = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        zwa__oucg = pd.array(df_typ.columns, 'string')
    else:
        zwa__oucg = df_typ.columns
    tphep__ojy = numba.typeof(zwa__oucg)
    pgo__qja = context.get_constant_generic(builder, tphep__ojy, zwa__oucg)
    mqw__vxbpt = pyapi.from_native_value(tphep__ojy, pgo__qja, c.env_manager)
    return mqw__vxbpt


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (vkqsy__wtcne, kix__mhm):
        with vkqsy__wtcne:
            pyapi.incref(obj)
            pmxi__pbyw = context.insert_const_string(c.builder.module, 'numpy')
            waab__iefc = pyapi.import_module_noblock(pmxi__pbyw)
            if df_typ.has_runtime_cols:
                kor__dshb = 0
            else:
                kor__dshb = len(df_typ.columns)
            sdo__iyxd = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), kor__dshb))
            hglr__aelpk = pyapi.call_method(waab__iefc, 'arange', (sdo__iyxd,))
            pyapi.object_setattr_string(obj, 'columns', hglr__aelpk)
            pyapi.decref(waab__iefc)
            pyapi.decref(hglr__aelpk)
            pyapi.decref(sdo__iyxd)
        with kix__mhm:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            uirmo__bwbqr = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            pmxi__pbyw = context.insert_const_string(c.builder.module, 'pandas'
                )
            waab__iefc = pyapi.import_module_noblock(pmxi__pbyw)
            df_obj = pyapi.call_method(waab__iefc, 'DataFrame', (pyapi.
                borrow_none(), uirmo__bwbqr))
            pyapi.decref(waab__iefc)
            pyapi.decref(uirmo__bwbqr)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    fxjej__vkg = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = fxjej__vkg.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        eps__vbgii = typ.table_type
        waxyq__ijs = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, eps__vbgii, waxyq__ijs)
        fnwk__wshw = box_table(eps__vbgii, waxyq__ijs, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (lqjzb__xgn, kib__wfej):
            with lqjzb__xgn:
                gkku__zhbzk = pyapi.object_getattr_string(fnwk__wshw, 'arrays')
                emyv__cgl = c.pyapi.make_none()
                if n_cols is None:
                    drv__ytucx = pyapi.call_method(gkku__zhbzk, '__len__', ())
                    xtxkn__rxc = pyapi.long_as_longlong(drv__ytucx)
                    pyapi.decref(drv__ytucx)
                else:
                    xtxkn__rxc = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, xtxkn__rxc) as luew__xqjya:
                    i = luew__xqjya.index
                    ahnco__lrxe = pyapi.list_getitem(gkku__zhbzk, i)
                    izta__bbo = c.builder.icmp_unsigned('!=', ahnco__lrxe,
                        emyv__cgl)
                    with builder.if_then(izta__bbo):
                        ofqyl__wzkod = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, ofqyl__wzkod, ahnco__lrxe)
                        pyapi.decref(ofqyl__wzkod)
                pyapi.decref(gkku__zhbzk)
                pyapi.decref(emyv__cgl)
            with kib__wfej:
                df_obj = builder.load(res)
                uirmo__bwbqr = pyapi.object_getattr_string(df_obj, 'index')
                smwim__dfty = c.pyapi.call_method(fnwk__wshw, 'to_pandas',
                    (uirmo__bwbqr,))
                builder.store(smwim__dfty, res)
                pyapi.decref(df_obj)
                pyapi.decref(uirmo__bwbqr)
        pyapi.decref(fnwk__wshw)
    else:
        ibd__vcyz = [builder.extract_value(dataframe_payload.data, i) for i in
            range(n_cols)]
        ysrrn__omsq = typ.data
        for i, xyv__prz, dvbb__shacq in zip(range(n_cols), ibd__vcyz,
            ysrrn__omsq):
            ygyv__offzf = cgutils.alloca_once_value(builder, xyv__prz)
            dcelg__mjeyb = cgutils.alloca_once_value(builder, context.
                get_constant_null(dvbb__shacq))
            izta__bbo = builder.not_(is_ll_eq(builder, ygyv__offzf,
                dcelg__mjeyb))
            bbrqq__aiii = builder.or_(builder.not_(use_parent_obj), builder
                .and_(use_parent_obj, izta__bbo))
            with builder.if_then(bbrqq__aiii):
                ofqyl__wzkod = pyapi.long_from_longlong(context.
                    get_constant(types.int64, i))
                context.nrt.incref(builder, dvbb__shacq, xyv__prz)
                arr_obj = pyapi.from_native_value(dvbb__shacq, xyv__prz, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, ofqyl__wzkod, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(ofqyl__wzkod)
    df_obj = builder.load(res)
    mqw__vxbpt = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', mqw__vxbpt)
    pyapi.decref(mqw__vxbpt)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    emyv__cgl = pyapi.borrow_none()
    frnl__pnssb = pyapi.unserialize(pyapi.serialize_object(slice))
    bie__fod = pyapi.call_function_objargs(frnl__pnssb, [emyv__cgl])
    zofg__wqi = pyapi.long_from_longlong(col_ind)
    miv__bcz = pyapi.tuple_pack([bie__fod, zofg__wqi])
    rxlip__xdgt = pyapi.object_getattr_string(df_obj, 'iloc')
    hnsx__pnuvb = pyapi.object_getitem(rxlip__xdgt, miv__bcz)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        sur__gbsp = pyapi.object_getattr_string(hnsx__pnuvb, 'array')
    else:
        sur__gbsp = pyapi.object_getattr_string(hnsx__pnuvb, 'values')
    if isinstance(data_typ, types.Array):
        nedsz__aqzeq = context.insert_const_string(builder.module, 'numpy')
        edpqb__kyhf = pyapi.import_module_noblock(nedsz__aqzeq)
        arr_obj = pyapi.call_method(edpqb__kyhf, 'ascontiguousarray', (
            sur__gbsp,))
        pyapi.decref(sur__gbsp)
        pyapi.decref(edpqb__kyhf)
    else:
        arr_obj = sur__gbsp
    pyapi.decref(frnl__pnssb)
    pyapi.decref(bie__fod)
    pyapi.decref(zofg__wqi)
    pyapi.decref(miv__bcz)
    pyapi.decref(rxlip__xdgt)
    pyapi.decref(hnsx__pnuvb)
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
        fxjej__vkg = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            fxjej__vkg.parent, args[1], data_typ)
        dhd__xctr = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            waxyq__ijs = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            fgn__iim = df_typ.table_type.type_to_blk[data_typ]
            smci__mqz = getattr(waxyq__ijs, f'block_{fgn__iim}')
            mukzk__iclcy = ListInstance(c.context, c.builder, types.List(
                data_typ), smci__mqz)
            wbrm__uslqw = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            mukzk__iclcy.inititem(wbrm__uslqw, dhd__xctr.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, dhd__xctr.value, col_ind)
        glvv__ewge = DataFramePayloadType(df_typ)
        pig__sie = context.nrt.meminfo_data(builder, fxjej__vkg.meminfo)
        mzo__whx = context.get_value_type(glvv__ewge).as_pointer()
        pig__sie = builder.bitcast(pig__sie, mzo__whx)
        builder.store(dataframe_payload._getvalue(), pig__sie)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        sur__gbsp = c.pyapi.object_getattr_string(val, 'array')
    else:
        sur__gbsp = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        nedsz__aqzeq = c.context.insert_const_string(c.builder.module, 'numpy')
        edpqb__kyhf = c.pyapi.import_module_noblock(nedsz__aqzeq)
        arr_obj = c.pyapi.call_method(edpqb__kyhf, 'ascontiguousarray', (
            sur__gbsp,))
        c.pyapi.decref(sur__gbsp)
        c.pyapi.decref(edpqb__kyhf)
    else:
        arr_obj = sur__gbsp
    map__ihpa = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    uirmo__bwbqr = c.pyapi.object_getattr_string(val, 'index')
    mifza__rzkhm = c.pyapi.to_native_value(typ.index, uirmo__bwbqr).value
    kqyl__guvw = c.pyapi.object_getattr_string(val, 'name')
    ogxd__ooivc = c.pyapi.to_native_value(typ.name_typ, kqyl__guvw).value
    smnsf__zxpt = bodo.hiframes.pd_series_ext.construct_series(c.context, c
        .builder, typ, map__ihpa, mifza__rzkhm, ogxd__ooivc)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(uirmo__bwbqr)
    c.pyapi.decref(kqyl__guvw)
    return NativeValue(smnsf__zxpt)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        ksv__dbdhn = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(ksv__dbdhn._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    pmxi__pbyw = c.context.insert_const_string(c.builder.module, 'pandas')
    bjqmc__ekl = c.pyapi.import_module_noblock(pmxi__pbyw)
    pgqex__gpnyg = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, pgqex__gpnyg.data)
    c.context.nrt.incref(c.builder, typ.index, pgqex__gpnyg.index)
    c.context.nrt.incref(c.builder, typ.name_typ, pgqex__gpnyg.name)
    arr_obj = c.pyapi.from_native_value(typ.data, pgqex__gpnyg.data, c.
        env_manager)
    uirmo__bwbqr = c.pyapi.from_native_value(typ.index, pgqex__gpnyg.index,
        c.env_manager)
    kqyl__guvw = c.pyapi.from_native_value(typ.name_typ, pgqex__gpnyg.name,
        c.env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(bjqmc__ekl, 'Series', (arr_obj, uirmo__bwbqr,
        dtype, kqyl__guvw))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(uirmo__bwbqr)
    c.pyapi.decref(kqyl__guvw)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(bjqmc__ekl)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    jnr__ywv = []
    for ukua__umd in typ_list:
        if isinstance(ukua__umd, int) and not isinstance(ukua__umd, bool):
            ebxhm__lfyh = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), ukua__umd))
        else:
            bnttg__lca = numba.typeof(ukua__umd)
            jcrn__kon = context.get_constant_generic(builder, bnttg__lca,
                ukua__umd)
            ebxhm__lfyh = pyapi.from_native_value(bnttg__lca, jcrn__kon,
                env_manager)
        jnr__ywv.append(ebxhm__lfyh)
    hdvrj__sjpuc = pyapi.list_pack(jnr__ywv)
    for val in jnr__ywv:
        pyapi.decref(val)
    return hdvrj__sjpuc


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    zmh__rgdko = not typ.has_runtime_cols and (not typ.is_table_format or 
        len(typ.columns) < TABLE_FORMAT_THRESHOLD)
    tjyo__mplte = 2 if zmh__rgdko else 1
    dlr__dlq = pyapi.dict_new(tjyo__mplte)
    brko__bmzt = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    pyapi.dict_setitem_string(dlr__dlq, 'dist', brko__bmzt)
    pyapi.decref(brko__bmzt)
    if zmh__rgdko:
        jane__mjes = _dtype_to_type_enum_list(typ.index)
        if jane__mjes != None:
            ebccp__fudqu = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, jane__mjes)
        else:
            ebccp__fudqu = pyapi.make_none()
        zob__kji = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                hdvrj__sjpuc = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                hdvrj__sjpuc = pyapi.make_none()
            zob__kji.append(hdvrj__sjpuc)
        dzj__nlnf = pyapi.list_pack(zob__kji)
        isk__hjvpw = pyapi.list_pack([ebccp__fudqu, dzj__nlnf])
        for val in zob__kji:
            pyapi.decref(val)
        pyapi.dict_setitem_string(dlr__dlq, 'type_metadata', isk__hjvpw)
    pyapi.object_setattr_string(obj, '_bodo_meta', dlr__dlq)
    pyapi.decref(dlr__dlq)


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
    dlr__dlq = pyapi.dict_new(2)
    brko__bmzt = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    jane__mjes = _dtype_to_type_enum_list(typ.index)
    if jane__mjes != None:
        ebccp__fudqu = type_enum_list_to_py_list_obj(pyapi, context,
            builder, c.env_manager, jane__mjes)
    else:
        ebccp__fudqu = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            ugtm__jyn = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            ugtm__jyn = pyapi.make_none()
    else:
        ugtm__jyn = pyapi.make_none()
    ekeo__bhm = pyapi.list_pack([ebccp__fudqu, ugtm__jyn])
    pyapi.dict_setitem_string(dlr__dlq, 'type_metadata', ekeo__bhm)
    pyapi.decref(ekeo__bhm)
    pyapi.dict_setitem_string(dlr__dlq, 'dist', brko__bmzt)
    pyapi.object_setattr_string(obj, '_bodo_meta', dlr__dlq)
    pyapi.decref(dlr__dlq)
    pyapi.decref(brko__bmzt)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as eibrt__seazn:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    rdxzz__aglhb = numba.np.numpy_support.map_layout(val)
    tkcb__wjvv = not val.flags.writeable
    return types.Array(dtype, val.ndim, rdxzz__aglhb, readonly=tkcb__wjvv)


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
    sbnoo__pac = val[i]
    if isinstance(sbnoo__pac, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(sbnoo__pac, bytes):
        return binary_array_type
    elif isinstance(sbnoo__pac, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(sbnoo__pac, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(sbnoo__pac))
    elif isinstance(sbnoo__pac, (dict, Dict)) and all(isinstance(mtij__tfc,
        str) for mtij__tfc in sbnoo__pac.keys()):
        iqeos__cega = tuple(sbnoo__pac.keys())
        owlqs__trv = tuple(_get_struct_value_arr_type(v) for v in
            sbnoo__pac.values())
        return StructArrayType(owlqs__trv, iqeos__cega)
    elif isinstance(sbnoo__pac, (dict, Dict)):
        rian__ukkut = numba.typeof(_value_to_array(list(sbnoo__pac.keys())))
        mhn__jwe = numba.typeof(_value_to_array(list(sbnoo__pac.values())))
        rian__ukkut = to_str_arr_if_dict_array(rian__ukkut)
        mhn__jwe = to_str_arr_if_dict_array(mhn__jwe)
        return MapArrayType(rian__ukkut, mhn__jwe)
    elif isinstance(sbnoo__pac, tuple):
        owlqs__trv = tuple(_get_struct_value_arr_type(v) for v in sbnoo__pac)
        return TupleArrayType(owlqs__trv)
    if isinstance(sbnoo__pac, (list, np.ndarray, pd.arrays.BooleanArray, pd
        .arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(sbnoo__pac, list):
            sbnoo__pac = _value_to_array(sbnoo__pac)
        egt__uahzf = numba.typeof(sbnoo__pac)
        egt__uahzf = to_str_arr_if_dict_array(egt__uahzf)
        return ArrayItemArrayType(egt__uahzf)
    if isinstance(sbnoo__pac, datetime.date):
        return datetime_date_array_type
    if isinstance(sbnoo__pac, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(sbnoo__pac, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(f'Unsupported object array with first value: {sbnoo__pac}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    bas__pqjyp = val.copy()
    bas__pqjyp.append(None)
    xyv__prz = np.array(bas__pqjyp, np.object_)
    if len(val) and isinstance(val[0], float):
        xyv__prz = np.array(val, np.float64)
    return xyv__prz


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
    dvbb__shacq = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        dvbb__shacq = to_nullable_type(dvbb__shacq)
    return dvbb__shacq
