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
    qcam__adz = tuple(val.columns.to_list())
    ejd__oaofu = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        evlcj__lfb = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        evlcj__lfb = numba.typeof(val.index)
    szmpo__kjtwf = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    khbp__hsrlx = len(ejd__oaofu) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(ejd__oaofu, evlcj__lfb, qcam__adz, szmpo__kjtwf,
        is_table_format=khbp__hsrlx)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    szmpo__kjtwf = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        rtn__wiaxt = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        rtn__wiaxt = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    ttbfb__nkjmo = dtype_to_array_type(dtype)
    if _use_dict_str_type and ttbfb__nkjmo == string_array_type:
        ttbfb__nkjmo = bodo.dict_str_arr_type
    return SeriesType(dtype, data=ttbfb__nkjmo, index=rtn__wiaxt, name_typ=
        numba.typeof(val.name), dist=szmpo__kjtwf)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    fahh__pdhgs = c.pyapi.object_getattr_string(val, 'index')
    cdhqd__ggrch = c.pyapi.to_native_value(typ.index, fahh__pdhgs).value
    c.pyapi.decref(fahh__pdhgs)
    if typ.is_table_format:
        cst__gxkpg = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        cst__gxkpg.parent = val
        for kmtzp__wpipl, jlz__onldm in typ.table_type.type_to_blk.items():
            btpxq__arw = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[jlz__onldm]))
            nzvqw__byj, tiu__shf = ListInstance.allocate_ex(c.context, c.
                builder, types.List(kmtzp__wpipl), btpxq__arw)
            tiu__shf.size = btpxq__arw
            setattr(cst__gxkpg, f'block_{jlz__onldm}', tiu__shf.value)
        xnkj__pxgi = c.pyapi.call_method(val, '__len__', ())
        oarvq__gln = c.pyapi.long_as_longlong(xnkj__pxgi)
        c.pyapi.decref(xnkj__pxgi)
        cst__gxkpg.len = oarvq__gln
        ltq__kgxc = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [cst__gxkpg._getvalue()])
    else:
        azmxb__dpe = [c.context.get_constant_null(kmtzp__wpipl) for
            kmtzp__wpipl in typ.data]
        ltq__kgxc = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            azmxb__dpe)
    jcrh__ioro = construct_dataframe(c.context, c.builder, typ, ltq__kgxc,
        cdhqd__ggrch, val, None)
    return NativeValue(jcrh__ioro)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        jufjz__maiob = df._bodo_meta['type_metadata'][1]
    else:
        jufjz__maiob = [None] * len(df.columns)
    lynad__pbbb = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=jufjz__maiob[i])) for i in range(len(df.columns))]
    lynad__pbbb = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        kmtzp__wpipl == string_array_type else kmtzp__wpipl) for
        kmtzp__wpipl in lynad__pbbb]
    return tuple(lynad__pbbb)


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
    edo__vzj, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(edo__vzj) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {edo__vzj}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        lrxxx__ohgn, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return lrxxx__ohgn, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        lrxxx__ohgn, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return lrxxx__ohgn, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        gmh__sne = typ_enum_list[1]
        pgnbc__xwz = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(gmh__sne, pgnbc__xwz)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        auqk__nzds = typ_enum_list[1]
        pcmf__czol = tuple(typ_enum_list[2:2 + auqk__nzds])
        lxwv__hmah = typ_enum_list[2 + auqk__nzds:]
        mjn__jff = []
        for i in range(auqk__nzds):
            lxwv__hmah, moce__rafui = _dtype_from_type_enum_list_recursor(
                lxwv__hmah)
            mjn__jff.append(moce__rafui)
        return lxwv__hmah, StructType(tuple(mjn__jff), pcmf__czol)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        aic__tsr = typ_enum_list[1]
        lxwv__hmah = typ_enum_list[2:]
        return lxwv__hmah, aic__tsr
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        aic__tsr = typ_enum_list[1]
        lxwv__hmah = typ_enum_list[2:]
        return lxwv__hmah, numba.types.literal(aic__tsr)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        lxwv__hmah, idae__wkj = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        lxwv__hmah, rtlkd__fxqci = _dtype_from_type_enum_list_recursor(
            lxwv__hmah)
        lxwv__hmah, temm__ulrv = _dtype_from_type_enum_list_recursor(lxwv__hmah
            )
        lxwv__hmah, hyna__huef = _dtype_from_type_enum_list_recursor(lxwv__hmah
            )
        lxwv__hmah, mmzyf__yvb = _dtype_from_type_enum_list_recursor(lxwv__hmah
            )
        return lxwv__hmah, PDCategoricalDtype(idae__wkj, rtlkd__fxqci,
            temm__ulrv, hyna__huef, mmzyf__yvb)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        lxwv__hmah, ewxlp__pqwh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return lxwv__hmah, DatetimeIndexType(ewxlp__pqwh)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        lxwv__hmah, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        lxwv__hmah, ewxlp__pqwh = _dtype_from_type_enum_list_recursor(
            lxwv__hmah)
        lxwv__hmah, hyna__huef = _dtype_from_type_enum_list_recursor(lxwv__hmah
            )
        return lxwv__hmah, NumericIndexType(dtype, ewxlp__pqwh, hyna__huef)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        lxwv__hmah, mahgr__vqsnv = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        lxwv__hmah, ewxlp__pqwh = _dtype_from_type_enum_list_recursor(
            lxwv__hmah)
        return lxwv__hmah, PeriodIndexType(mahgr__vqsnv, ewxlp__pqwh)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        lxwv__hmah, hyna__huef = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        lxwv__hmah, ewxlp__pqwh = _dtype_from_type_enum_list_recursor(
            lxwv__hmah)
        return lxwv__hmah, CategoricalIndexType(hyna__huef, ewxlp__pqwh)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        lxwv__hmah, ewxlp__pqwh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return lxwv__hmah, RangeIndexType(ewxlp__pqwh)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        lxwv__hmah, ewxlp__pqwh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return lxwv__hmah, StringIndexType(ewxlp__pqwh)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        lxwv__hmah, ewxlp__pqwh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return lxwv__hmah, BinaryIndexType(ewxlp__pqwh)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        lxwv__hmah, ewxlp__pqwh = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return lxwv__hmah, TimedeltaIndexType(ewxlp__pqwh)
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
        afvol__ftl = get_overload_const_int(typ)
        if numba.types.maybe_literal(afvol__ftl) == typ:
            return [SeriesDtypeEnum.LiteralType.value, afvol__ftl]
    elif is_overload_constant_str(typ):
        afvol__ftl = get_overload_const_str(typ)
        if numba.types.maybe_literal(afvol__ftl) == typ:
            return [SeriesDtypeEnum.LiteralType.value, afvol__ftl]
    elif is_overload_constant_bool(typ):
        afvol__ftl = get_overload_const_bool(typ)
        if numba.types.maybe_literal(afvol__ftl) == typ:
            return [SeriesDtypeEnum.LiteralType.value, afvol__ftl]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        ettsa__ngr = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for jbya__mznmc in typ.names:
            ettsa__ngr.append(jbya__mznmc)
        for zqix__vjo in typ.data:
            ettsa__ngr += _dtype_to_type_enum_list_recursor(zqix__vjo)
        return ettsa__ngr
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        pwwou__nageo = _dtype_to_type_enum_list_recursor(typ.categories)
        avlb__chnrj = _dtype_to_type_enum_list_recursor(typ.elem_type)
        pkm__jdsdz = _dtype_to_type_enum_list_recursor(typ.ordered)
        kke__red = _dtype_to_type_enum_list_recursor(typ.data)
        tzb__spd = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + pwwou__nageo + avlb__chnrj + pkm__jdsdz + kke__red + tzb__spd
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                qax__ntgl = types.float64
                hxmga__pphw = types.Array(qax__ntgl, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                qax__ntgl = types.int64
                hxmga__pphw = types.Array(qax__ntgl, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                qax__ntgl = types.uint64
                hxmga__pphw = types.Array(qax__ntgl, 1, 'C')
            elif typ.dtype == types.bool_:
                qax__ntgl = typ.dtype
                hxmga__pphw = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(qax__ntgl
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(hxmga__pphw)
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
                qeu__ydlu = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(qeu__ydlu)
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
        jufs__btmc = S.dtype.unit
        if jufs__btmc != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        sby__akvqr = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.
            dtype.tz)
        return PandasDatetimeTZDtype(sby__akvqr)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    ktknf__aerav = cgutils.is_not_null(builder, parent_obj)
    rtxdp__fesim = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(ktknf__aerav):
        oeq__tvo = pyapi.object_getattr_string(parent_obj, 'columns')
        xnkj__pxgi = pyapi.call_method(oeq__tvo, '__len__', ())
        builder.store(pyapi.long_as_longlong(xnkj__pxgi), rtxdp__fesim)
        pyapi.decref(xnkj__pxgi)
        pyapi.decref(oeq__tvo)
    use_parent_obj = builder.and_(ktknf__aerav, builder.icmp_unsigned('==',
        builder.load(rtxdp__fesim), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        svwo__eepi = df_typ.runtime_colname_typ
        context.nrt.incref(builder, svwo__eepi, dataframe_payload.columns)
        return pyapi.from_native_value(svwo__eepi, dataframe_payload.
            columns, c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        obvdu__kpi = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        obvdu__kpi = pd.array(df_typ.columns, 'string')
    else:
        obvdu__kpi = df_typ.columns
    sij__ytkk = numba.typeof(obvdu__kpi)
    kbeq__yaddw = context.get_constant_generic(builder, sij__ytkk, obvdu__kpi)
    rbixo__krx = pyapi.from_native_value(sij__ytkk, kbeq__yaddw, c.env_manager)
    return rbixo__krx


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (kfkd__aylcs, wnf__dted):
        with kfkd__aylcs:
            pyapi.incref(obj)
            xmy__sfczb = context.insert_const_string(c.builder.module, 'numpy')
            cazxl__yhaaf = pyapi.import_module_noblock(xmy__sfczb)
            if df_typ.has_runtime_cols:
                zzui__cpyrg = 0
            else:
                zzui__cpyrg = len(df_typ.columns)
            ngr__ouo = pyapi.long_from_longlong(lir.Constant(lir.IntType(64
                ), zzui__cpyrg))
            xgj__nwxt = pyapi.call_method(cazxl__yhaaf, 'arange', (ngr__ouo,))
            pyapi.object_setattr_string(obj, 'columns', xgj__nwxt)
            pyapi.decref(cazxl__yhaaf)
            pyapi.decref(xgj__nwxt)
            pyapi.decref(ngr__ouo)
        with wnf__dted:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            esolg__hqpsg = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            xmy__sfczb = context.insert_const_string(c.builder.module, 'pandas'
                )
            cazxl__yhaaf = pyapi.import_module_noblock(xmy__sfczb)
            df_obj = pyapi.call_method(cazxl__yhaaf, 'DataFrame', (pyapi.
                borrow_none(), esolg__hqpsg))
            pyapi.decref(cazxl__yhaaf)
            pyapi.decref(esolg__hqpsg)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    wzdp__xdgg = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = wzdp__xdgg.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        jbxm__aknfa = typ.table_type
        cst__gxkpg = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, jbxm__aknfa, cst__gxkpg)
        fma__hgbi = box_table(jbxm__aknfa, cst__gxkpg, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (uzoqf__lpw, fvxgg__irf):
            with uzoqf__lpw:
                ynzwn__cwk = pyapi.object_getattr_string(fma__hgbi, 'arrays')
                cdcx__ibe = c.pyapi.make_none()
                if n_cols is None:
                    xnkj__pxgi = pyapi.call_method(ynzwn__cwk, '__len__', ())
                    btpxq__arw = pyapi.long_as_longlong(xnkj__pxgi)
                    pyapi.decref(xnkj__pxgi)
                else:
                    btpxq__arw = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, btpxq__arw) as twke__sswau:
                    i = twke__sswau.index
                    banpk__tukuj = pyapi.list_getitem(ynzwn__cwk, i)
                    sadj__rsv = c.builder.icmp_unsigned('!=', banpk__tukuj,
                        cdcx__ibe)
                    with builder.if_then(sadj__rsv):
                        bixt__dkli = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, bixt__dkli, banpk__tukuj)
                        pyapi.decref(bixt__dkli)
                pyapi.decref(ynzwn__cwk)
                pyapi.decref(cdcx__ibe)
            with fvxgg__irf:
                df_obj = builder.load(res)
                esolg__hqpsg = pyapi.object_getattr_string(df_obj, 'index')
                vram__ewpi = c.pyapi.call_method(fma__hgbi, 'to_pandas', (
                    esolg__hqpsg,))
                builder.store(vram__ewpi, res)
                pyapi.decref(df_obj)
                pyapi.decref(esolg__hqpsg)
        pyapi.decref(fma__hgbi)
    else:
        ybz__mgts = [builder.extract_value(dataframe_payload.data, i) for i in
            range(n_cols)]
        tinsk__kueue = typ.data
        for i, ddab__pjus, ttbfb__nkjmo in zip(range(n_cols), ybz__mgts,
            tinsk__kueue):
            nrle__inxjh = cgutils.alloca_once_value(builder, ddab__pjus)
            ecmhu__ulq = cgutils.alloca_once_value(builder, context.
                get_constant_null(ttbfb__nkjmo))
            sadj__rsv = builder.not_(is_ll_eq(builder, nrle__inxjh, ecmhu__ulq)
                )
            tfxhh__wrir = builder.or_(builder.not_(use_parent_obj), builder
                .and_(use_parent_obj, sadj__rsv))
            with builder.if_then(tfxhh__wrir):
                bixt__dkli = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, ttbfb__nkjmo, ddab__pjus)
                arr_obj = pyapi.from_native_value(ttbfb__nkjmo, ddab__pjus,
                    c.env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, bixt__dkli, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(bixt__dkli)
    df_obj = builder.load(res)
    rbixo__krx = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', rbixo__krx)
    pyapi.decref(rbixo__krx)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    cdcx__ibe = pyapi.borrow_none()
    usj__sxi = pyapi.unserialize(pyapi.serialize_object(slice))
    uucls__iebuu = pyapi.call_function_objargs(usj__sxi, [cdcx__ibe])
    qrv__qkp = pyapi.long_from_longlong(col_ind)
    rvzy__ueys = pyapi.tuple_pack([uucls__iebuu, qrv__qkp])
    wnq__rgxl = pyapi.object_getattr_string(df_obj, 'iloc')
    rtxg__nctr = pyapi.object_getitem(wnq__rgxl, rvzy__ueys)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        dtdoq__exng = pyapi.object_getattr_string(rtxg__nctr, 'array')
    else:
        dtdoq__exng = pyapi.object_getattr_string(rtxg__nctr, 'values')
    if isinstance(data_typ, types.Array):
        eon__lcz = context.insert_const_string(builder.module, 'numpy')
        ewfoi__xapt = pyapi.import_module_noblock(eon__lcz)
        arr_obj = pyapi.call_method(ewfoi__xapt, 'ascontiguousarray', (
            dtdoq__exng,))
        pyapi.decref(dtdoq__exng)
        pyapi.decref(ewfoi__xapt)
    else:
        arr_obj = dtdoq__exng
    pyapi.decref(usj__sxi)
    pyapi.decref(uucls__iebuu)
    pyapi.decref(qrv__qkp)
    pyapi.decref(rvzy__ueys)
    pyapi.decref(wnq__rgxl)
    pyapi.decref(rtxg__nctr)
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
        wzdp__xdgg = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            wzdp__xdgg.parent, args[1], data_typ)
        rfqx__slpiz = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            cst__gxkpg = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            jlz__onldm = df_typ.table_type.type_to_blk[data_typ]
            bjoy__bhatj = getattr(cst__gxkpg, f'block_{jlz__onldm}')
            ivsrs__fkits = ListInstance(c.context, c.builder, types.List(
                data_typ), bjoy__bhatj)
            bathu__jzczd = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            ivsrs__fkits.inititem(bathu__jzczd, rfqx__slpiz.value, incref=False
                )
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, rfqx__slpiz.value, col_ind)
        bqcmc__hrrd = DataFramePayloadType(df_typ)
        sdvmj__qccx = context.nrt.meminfo_data(builder, wzdp__xdgg.meminfo)
        lenbd__loooe = context.get_value_type(bqcmc__hrrd).as_pointer()
        sdvmj__qccx = builder.bitcast(sdvmj__qccx, lenbd__loooe)
        builder.store(dataframe_payload._getvalue(), sdvmj__qccx)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        dtdoq__exng = c.pyapi.object_getattr_string(val, 'array')
    else:
        dtdoq__exng = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        eon__lcz = c.context.insert_const_string(c.builder.module, 'numpy')
        ewfoi__xapt = c.pyapi.import_module_noblock(eon__lcz)
        arr_obj = c.pyapi.call_method(ewfoi__xapt, 'ascontiguousarray', (
            dtdoq__exng,))
        c.pyapi.decref(dtdoq__exng)
        c.pyapi.decref(ewfoi__xapt)
    else:
        arr_obj = dtdoq__exng
    kfx__voxm = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    esolg__hqpsg = c.pyapi.object_getattr_string(val, 'index')
    cdhqd__ggrch = c.pyapi.to_native_value(typ.index, esolg__hqpsg).value
    tdivz__rqnb = c.pyapi.object_getattr_string(val, 'name')
    sohaj__dnqvn = c.pyapi.to_native_value(typ.name_typ, tdivz__rqnb).value
    jddu__kvbea = bodo.hiframes.pd_series_ext.construct_series(c.context, c
        .builder, typ, kfx__voxm, cdhqd__ggrch, sohaj__dnqvn)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(esolg__hqpsg)
    c.pyapi.decref(tdivz__rqnb)
    return NativeValue(jddu__kvbea)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        eww__jll = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(eww__jll._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    xmy__sfczb = c.context.insert_const_string(c.builder.module, 'pandas')
    cblc__cebb = c.pyapi.import_module_noblock(xmy__sfczb)
    dnl__ifx = bodo.hiframes.pd_series_ext.get_series_payload(c.context, c.
        builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, dnl__ifx.data)
    c.context.nrt.incref(c.builder, typ.index, dnl__ifx.index)
    c.context.nrt.incref(c.builder, typ.name_typ, dnl__ifx.name)
    arr_obj = c.pyapi.from_native_value(typ.data, dnl__ifx.data, c.env_manager)
    esolg__hqpsg = c.pyapi.from_native_value(typ.index, dnl__ifx.index, c.
        env_manager)
    tdivz__rqnb = c.pyapi.from_native_value(typ.name_typ, dnl__ifx.name, c.
        env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(cblc__cebb, 'Series', (arr_obj, esolg__hqpsg,
        dtype, tdivz__rqnb))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(esolg__hqpsg)
    c.pyapi.decref(tdivz__rqnb)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(cblc__cebb)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    ilit__ezax = []
    for ryad__wlbnk in typ_list:
        if isinstance(ryad__wlbnk, int) and not isinstance(ryad__wlbnk, bool):
            mfdxn__owh = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), ryad__wlbnk))
        else:
            vuqll__oavhs = numba.typeof(ryad__wlbnk)
            zdlzu__veyqm = context.get_constant_generic(builder,
                vuqll__oavhs, ryad__wlbnk)
            mfdxn__owh = pyapi.from_native_value(vuqll__oavhs, zdlzu__veyqm,
                env_manager)
        ilit__ezax.append(mfdxn__owh)
    jsxbx__dnqm = pyapi.list_pack(ilit__ezax)
    for val in ilit__ezax:
        pyapi.decref(val)
    return jsxbx__dnqm


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    wnc__ibs = not typ.has_runtime_cols and (not typ.is_table_format or len
        (typ.columns) < TABLE_FORMAT_THRESHOLD)
    juz__bek = 2 if wnc__ibs else 1
    usbqj__qjbcq = pyapi.dict_new(juz__bek)
    btk__ltfm = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(usbqj__qjbcq, 'dist', btk__ltfm)
    pyapi.decref(btk__ltfm)
    if wnc__ibs:
        jkgd__slmjd = _dtype_to_type_enum_list(typ.index)
        if jkgd__slmjd != None:
            vdbiq__qgjap = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, jkgd__slmjd)
        else:
            vdbiq__qgjap = pyapi.make_none()
        demun__zije = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                jsxbx__dnqm = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                jsxbx__dnqm = pyapi.make_none()
            demun__zije.append(jsxbx__dnqm)
        wszhy__govv = pyapi.list_pack(demun__zije)
        tpple__lznl = pyapi.list_pack([vdbiq__qgjap, wszhy__govv])
        for val in demun__zije:
            pyapi.decref(val)
        pyapi.dict_setitem_string(usbqj__qjbcq, 'type_metadata', tpple__lznl)
    pyapi.object_setattr_string(obj, '_bodo_meta', usbqj__qjbcq)
    pyapi.decref(usbqj__qjbcq)


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
    usbqj__qjbcq = pyapi.dict_new(2)
    btk__ltfm = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    jkgd__slmjd = _dtype_to_type_enum_list(typ.index)
    if jkgd__slmjd != None:
        vdbiq__qgjap = type_enum_list_to_py_list_obj(pyapi, context,
            builder, c.env_manager, jkgd__slmjd)
    else:
        vdbiq__qgjap = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            rdcol__ven = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            rdcol__ven = pyapi.make_none()
    else:
        rdcol__ven = pyapi.make_none()
    ssods__lzpl = pyapi.list_pack([vdbiq__qgjap, rdcol__ven])
    pyapi.dict_setitem_string(usbqj__qjbcq, 'type_metadata', ssods__lzpl)
    pyapi.decref(ssods__lzpl)
    pyapi.dict_setitem_string(usbqj__qjbcq, 'dist', btk__ltfm)
    pyapi.object_setattr_string(obj, '_bodo_meta', usbqj__qjbcq)
    pyapi.decref(usbqj__qjbcq)
    pyapi.decref(btk__ltfm)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as btses__jjpa:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    sbv__ujams = numba.np.numpy_support.map_layout(val)
    hynt__bir = not val.flags.writeable
    return types.Array(dtype, val.ndim, sbv__ujams, readonly=hynt__bir)


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
    eexf__ewy = val[i]
    if isinstance(eexf__ewy, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(eexf__ewy, bytes):
        return binary_array_type
    elif isinstance(eexf__ewy, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(eexf__ewy, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(eexf__ewy))
    elif isinstance(eexf__ewy, (dict, Dict)) and all(isinstance(gkwu__lbibs,
        str) for gkwu__lbibs in eexf__ewy.keys()):
        pcmf__czol = tuple(eexf__ewy.keys())
        bngjm__mjdda = tuple(_get_struct_value_arr_type(v) for v in
            eexf__ewy.values())
        return StructArrayType(bngjm__mjdda, pcmf__czol)
    elif isinstance(eexf__ewy, (dict, Dict)):
        czzqj__jmpc = numba.typeof(_value_to_array(list(eexf__ewy.keys())))
        gcob__tnfjv = numba.typeof(_value_to_array(list(eexf__ewy.values())))
        czzqj__jmpc = to_str_arr_if_dict_array(czzqj__jmpc)
        gcob__tnfjv = to_str_arr_if_dict_array(gcob__tnfjv)
        return MapArrayType(czzqj__jmpc, gcob__tnfjv)
    elif isinstance(eexf__ewy, tuple):
        bngjm__mjdda = tuple(_get_struct_value_arr_type(v) for v in eexf__ewy)
        return TupleArrayType(bngjm__mjdda)
    if isinstance(eexf__ewy, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(eexf__ewy, list):
            eexf__ewy = _value_to_array(eexf__ewy)
        vxfx__eyfi = numba.typeof(eexf__ewy)
        vxfx__eyfi = to_str_arr_if_dict_array(vxfx__eyfi)
        return ArrayItemArrayType(vxfx__eyfi)
    if isinstance(eexf__ewy, datetime.date):
        return datetime_date_array_type
    if isinstance(eexf__ewy, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(eexf__ewy, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(f'Unsupported object array with first value: {eexf__ewy}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    hsxwg__kzpnp = val.copy()
    hsxwg__kzpnp.append(None)
    ddab__pjus = np.array(hsxwg__kzpnp, np.object_)
    if len(val) and isinstance(val[0], float):
        ddab__pjus = np.array(val, np.float64)
    return ddab__pjus


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
    ttbfb__nkjmo = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        ttbfb__nkjmo = to_nullable_type(ttbfb__nkjmo)
    return ttbfb__nkjmo
