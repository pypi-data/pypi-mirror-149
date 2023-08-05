"""
Utility functions for conversion of data such as list to array.
Need to be inlined for better optimization.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_dtype
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.nullable_tuple_ext import NullableTupleType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, decode_if_dict_array, dtype_to_array_type, get_overload_const_list, get_overload_const_str, is_heterogeneous_tuple_type, is_np_arr_typ, is_overload_constant_list, is_overload_constant_str, is_overload_none, is_overload_true, is_str_arr_type, to_nullable_type
NS_DTYPE = np.dtype('M8[ns]')
TD_DTYPE = np.dtype('m8[ns]')


def coerce_to_ndarray(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_ndarray)
def overload_coerce_to_ndarray(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, RangeIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType
        ) and not is_overload_none(use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.int_arr_ext.
            get_int_arr_data(data))
    if data == bodo.libs.bool_arr_ext.boolean_array and not is_overload_none(
        use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.bool_arr_ext.
            get_bool_arr_data(data))
    if isinstance(data, types.Array):
        if not is_overload_none(use_nullable_array) and isinstance(data.
            dtype, (types.Boolean, types.Integer)):
            if data.dtype == types.bool_:
                if data.layout != 'C':
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(np.
                        ascontiguousarray(data), np.full(len(data) + 7 >> 3,
                        255, np.uint8)))
                else:
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(data, np.
                        full(len(data) + 7 >> 3, 255, np.uint8)))
            elif data.layout != 'C':
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(np.
                    ascontiguousarray(data), np.full(len(data) + 7 >> 3, 
                    255, np.uint8)))
            else:
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(data, np.full(len(
                    data) + 7 >> 3, 255, np.uint8)))
        if data.layout != 'C':
            return (lambda data, error_on_nonarray=True, use_nullable_array
                =None, scalar_to_arr_len=None: np.ascontiguousarray(data))
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)):
        djlc__graxf = data.dtype
        if isinstance(djlc__graxf, types.Optional):
            djlc__graxf = djlc__graxf.type
            if bodo.utils.typing.is_scalar_type(djlc__graxf):
                use_nullable_array = True
        if isinstance(djlc__graxf, (types.Boolean, types.Integer,
            Decimal128Type)) or djlc__graxf in [bodo.hiframes.
            pd_timestamp_ext.pd_timestamp_type, bodo.hiframes.
            datetime_date_ext.datetime_date_type, bodo.hiframes.
            datetime_timedelta_ext.datetime_timedelta_type]:
            eci__arxwf = dtype_to_array_type(djlc__graxf)
            if not is_overload_none(use_nullable_array):
                eci__arxwf = to_nullable_type(eci__arxwf)

            def impl(data, error_on_nonarray=True, use_nullable_array=None,
                scalar_to_arr_len=None):
                ozt__ney = len(data)
                A = bodo.utils.utils.alloc_type(ozt__ney, eci__arxwf, (-1,))
                bodo.utils.utils.tuple_list_to_array(A, data, djlc__graxf)
                return A
            return impl
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.asarray(data))
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, RangeIndexType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data._start, data._stop,
            data._step))
    if isinstance(data, types.RangeType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data.start, data.stop,
            data.step))
    if not is_overload_none(scalar_to_arr_len):
        if isinstance(data, Decimal128Type):
            hakc__eyfg = data.precision
            xcikj__ksc = data.scale

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                ozt__ney = scalar_to_arr_len
                A = bodo.libs.decimal_arr_ext.alloc_decimal_array(ozt__ney,
                    hakc__eyfg, xcikj__ksc)
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    A[edjw__otdr] = data
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
            rheh__gah = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                ozt__ney = scalar_to_arr_len
                A = np.empty(ozt__ney, rheh__gah)
                zhea__fhgar = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(data))
                wwxw__kxbz = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    zhea__fhgar)
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    A[edjw__otdr] = wwxw__kxbz
                return A
            return impl_ts
        if (data == bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type):
            qvix__mxfcb = np.dtype('timedelta64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                ozt__ney = scalar_to_arr_len
                A = np.empty(ozt__ney, qvix__mxfcb)
                lnmfi__lwta = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(data))
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    A[edjw__otdr] = lnmfi__lwta
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_date_ext.datetime_date_type:

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                ozt__ney = scalar_to_arr_len
                A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                    ozt__ney)
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    A[edjw__otdr] = data
                return A
            return impl_ts
        if data == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            rheh__gah = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                ozt__ney = scalar_to_arr_len
                A = np.empty(scalar_to_arr_len, rheh__gah)
                zhea__fhgar = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data.value)
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    A[edjw__otdr] = zhea__fhgar
                return A
            return impl_ts
        dtype = types.unliteral(data)
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Integer):

            def impl_null_integer(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                ozt__ney = scalar_to_arr_len
                biktd__fsb = bodo.libs.int_arr_ext.alloc_int_array(ozt__ney,
                    dtype)
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    biktd__fsb[edjw__otdr] = data
                return biktd__fsb
            return impl_null_integer
        if not is_overload_none(use_nullable_array) and dtype == types.bool_:

            def impl_null_bool(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                ozt__ney = scalar_to_arr_len
                biktd__fsb = bodo.libs.bool_arr_ext.alloc_bool_array(ozt__ney)
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    biktd__fsb[edjw__otdr] = data
                return biktd__fsb
            return impl_null_bool

        def impl_num(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            numba.parfors.parfor.init_prange()
            ozt__ney = scalar_to_arr_len
            biktd__fsb = np.empty(ozt__ney, dtype)
            for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney):
                biktd__fsb[edjw__otdr] = data
            return biktd__fsb
        return impl_num
    if isinstance(data, types.BaseTuple) and all(isinstance(isoe__ckdj, (
        types.Float, types.Integer)) for isoe__ckdj in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.array(data))
    if bodo.utils.utils.is_array_typ(data, False):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if is_overload_true(error_on_nonarray):
        raise BodoError(f'cannot coerce {data} to array')
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: data)


def coerce_to_array(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_array, no_unliteral=True)
def overload_coerce_to_array(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, StringIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (StringIndexType, BinaryIndexType,
        CategoricalIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, types.List) and data.dtype in (bodo.string_type,
        bodo.bytes_type):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if isinstance(data, types.BaseTuple) and data.count == 0:
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            empty_str_arr(data))
    if isinstance(data, types.UniTuple) and isinstance(data.dtype, (types.
        UnicodeType, types.StringLiteral)) or isinstance(data, types.BaseTuple
        ) and all(isinstance(isoe__ckdj, types.StringLiteral) for
        isoe__ckdj in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if data in (bodo.string_array_type, bodo.dict_str_arr_type, bodo.
        binary_array_type, bodo.libs.bool_arr_ext.boolean_array, bodo.
        hiframes.datetime_date_ext.datetime_date_array_type, bodo.hiframes.
        datetime_timedelta_ext.datetime_timedelta_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type) or isinstance(data, (bodo
        .libs.int_arr_ext.IntegerArrayType, DecimalArrayType, bodo.libs.
        interval_arr_ext.IntervalArrayType, bodo.libs.tuple_arr_ext.
        TupleArrayType, bodo.libs.struct_arr_ext.StructArrayType, bodo.
        hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        csr_matrix_ext.CSRMatrixType, bodo.DatetimeArrayType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)) and isinstance(data.
        dtype, types.BaseTuple):
        skixx__qpgu = tuple(dtype_to_array_type(isoe__ckdj) for isoe__ckdj in
            data.dtype.types)

        def impl_tuple_list(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            ozt__ney = len(data)
            arr = bodo.libs.tuple_arr_ext.pre_alloc_tuple_array(ozt__ney, (
                -1,), skixx__qpgu)
            for edjw__otdr in range(ozt__ney):
                arr[edjw__otdr] = data[edjw__otdr]
            return arr
        return impl_tuple_list
    if isinstance(data, types.List) and (bodo.utils.utils.is_array_typ(data
        .dtype, False) or isinstance(data.dtype, types.List)):
        tstf__nyl = dtype_to_array_type(data.dtype.dtype)

        def impl_array_item_arr(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            ozt__ney = len(data)
            tkxfd__ekyri = init_nested_counts(tstf__nyl)
            for edjw__otdr in range(ozt__ney):
                vide__rot = bodo.utils.conversion.coerce_to_array(data[
                    edjw__otdr], use_nullable_array=True)
                tkxfd__ekyri = add_nested_counts(tkxfd__ekyri, vide__rot)
            biktd__fsb = (bodo.libs.array_item_arr_ext.
                pre_alloc_array_item_array(ozt__ney, tkxfd__ekyri, tstf__nyl))
            ark__ywui = bodo.libs.array_item_arr_ext.get_null_bitmap(biktd__fsb
                )
            for fgely__thho in range(ozt__ney):
                vide__rot = bodo.utils.conversion.coerce_to_array(data[
                    fgely__thho], use_nullable_array=True)
                biktd__fsb[fgely__thho] = vide__rot
                bodo.libs.int_arr_ext.set_bit_to_arr(ark__ywui, fgely__thho, 1)
            return biktd__fsb
        return impl_array_item_arr
    if not is_overload_none(scalar_to_arr_len) and isinstance(data, (types.
        UnicodeType, types.StringLiteral)):

        def impl_str(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            ozt__ney = scalar_to_arr_len
            A = bodo.libs.str_arr_ext.pre_alloc_string_array(ozt__ney, -1)
            for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney):
                A[edjw__otdr] = data
            return A
        return impl_str
    if isinstance(data, types.List) and isinstance(data.dtype, bodo.
        hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')

        def impl_list_timestamp(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            ozt__ney = len(data)
            A = np.empty(ozt__ney, np.dtype('datetime64[ns]'))
            for edjw__otdr in range(ozt__ney):
                A[edjw__otdr] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data[edjw__otdr].value)
            return A
        return impl_list_timestamp
    if isinstance(data, types.List) and data.dtype == bodo.pd_timedelta_type:

        def impl_list_timedelta(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            ozt__ney = len(data)
            A = np.empty(ozt__ney, np.dtype('timedelta64[ns]'))
            for edjw__otdr in range(ozt__ney):
                A[edjw__otdr
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    data[edjw__otdr].value)
            return A
        return impl_list_timedelta
    if isinstance(data, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')
    if not is_overload_none(scalar_to_arr_len) and data in [bodo.
        pd_timestamp_type, bodo.pd_timedelta_type]:
        cxfa__gbnii = ('datetime64[ns]' if data == bodo.pd_timestamp_type else
            'timedelta64[ns]')

        def impl_timestamp(data, error_on_nonarray=True, use_nullable_array
            =None, scalar_to_arr_len=None):
            ozt__ney = scalar_to_arr_len
            A = np.empty(ozt__ney, cxfa__gbnii)
            data = bodo.utils.conversion.unbox_if_timestamp(data)
            for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney):
                A[edjw__otdr] = data
            return A
        return impl_timestamp
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: bodo.utils.conversion.coerce_to_ndarray(
        data, error_on_nonarray, use_nullable_array, scalar_to_arr_len))


def _is_str_dtype(dtype):
    return isinstance(dtype, bodo.libs.str_arr_ext.StringDtype) or isinstance(
        dtype, types.Function) and dtype.key[0
        ] == str or is_overload_constant_str(dtype) and get_overload_const_str(
        dtype) == 'str' or isinstance(dtype, types.TypeRef
        ) and dtype.instance_type == types.unicode_type


def fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True, from_series=
    False):
    return data


@overload(fix_arr_dtype, no_unliteral=True)
def overload_fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True,
    from_series=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'fix_arr_dtype()')
    wsqu__gbnmh = is_overload_true(copy)
    wfnlf__ged = is_overload_constant_str(new_dtype
        ) and get_overload_const_str(new_dtype) == 'object'
    if is_overload_none(new_dtype) or wfnlf__ged:
        if wsqu__gbnmh:
            return (lambda data, new_dtype, copy=None, nan_to_str=True,
                from_series=False: data.copy())
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(data, NullableTupleType):
        nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
        if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
            nb_dtype = nb_dtype.dtype
        jzxde__olvsc = {types.unicode_type: '', boolean_dtype: False, types
            .bool_: False, types.int8: np.int8(0), types.int16: np.int16(0),
            types.int32: np.int32(0), types.int64: np.int64(0), types.uint8:
            np.uint8(0), types.uint16: np.uint16(0), types.uint32: np.
            uint32(0), types.uint64: np.uint64(0), types.float32: np.
            float32(0), types.float64: np.float64(0), bodo.datetime64ns: pd
            .Timestamp(0), bodo.timedelta64ns: pd.Timedelta(0)}
        zas__qwtud = {types.unicode_type: str, types.bool_: bool,
            boolean_dtype: bool, types.int8: np.int8, types.int16: np.int16,
            types.int32: np.int32, types.int64: np.int64, types.uint8: np.
            uint8, types.uint16: np.uint16, types.uint32: np.uint32, types.
            uint64: np.uint64, types.float32: np.float32, types.float64: np
            .float64, bodo.datetime64ns: pd.to_datetime, bodo.timedelta64ns:
            pd.to_timedelta}
        kzfl__ssopl = jzxde__olvsc.keys()
        vam__fkirz = list(data._tuple_typ.types)
        if nb_dtype not in kzfl__ssopl:
            raise BodoError(f'type conversion to {nb_dtype} types unsupported.'
                )
        for crfad__lfw in vam__fkirz:
            if crfad__lfw == bodo.datetime64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.datetime64ns):
                    raise BodoError(
                        f'invalid type conversion from {crfad__lfw} to {nb_dtype}.'
                        )
            elif crfad__lfw == bodo.timedelta64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.timedelta64ns):
                    raise BodoError(
                        f'invalid type conversion from {crfad__lfw} to {nb_dtype}.'
                        )
        gkuc__gvh = (
            'def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False):\n'
            )
        gkuc__gvh += '  data_tup = data._data\n'
        gkuc__gvh += '  null_tup = data._null_values\n'
        for edjw__otdr in range(len(vam__fkirz)):
            gkuc__gvh += f'  val_{edjw__otdr} = convert_func(default_value)\n'
            gkuc__gvh += f'  if not null_tup[{edjw__otdr}]:\n'
            gkuc__gvh += (
                f'    val_{edjw__otdr} = convert_func(data_tup[{edjw__otdr}])\n'
                )
        golj__wcy = ', '.join(f'val_{edjw__otdr}' for edjw__otdr in range(
            len(vam__fkirz)))
        gkuc__gvh += f'  vals_tup = ({golj__wcy},)\n'
        gkuc__gvh += """  res_tup = bodo.libs.nullable_tuple_ext.build_nullable_tuple(vals_tup, null_tup)
"""
        gkuc__gvh += '  return res_tup\n'
        hjl__cgoh = {}
        lsjb__mix = zas__qwtud[nb_dtype]
        tffoh__jvtt = jzxde__olvsc[nb_dtype]
        exec(gkuc__gvh, {'bodo': bodo, 'np': np, 'pd': pd, 'default_value':
            tffoh__jvtt, 'convert_func': lsjb__mix}, hjl__cgoh)
        impl = hjl__cgoh['impl']
        return impl
    if _is_str_dtype(new_dtype):
        if isinstance(data.dtype, types.Integer):

            def impl_int_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                ozt__ney = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(ozt__ney, -1)
                for dbf__airn in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    if bodo.libs.array_kernels.isna(data, dbf__airn):
                        if nan_to_str:
                            bodo.libs.str_arr_ext.str_arr_setitem_NA_str(A,
                                dbf__airn)
                        else:
                            bodo.libs.array_kernels.setna(A, dbf__airn)
                    else:
                        bodo.libs.str_arr_ext.str_arr_setitem_int_to_str(A,
                            dbf__airn, data[dbf__airn])
                return A
            return impl_int_str
        if data.dtype == bytes_type:

            def impl_binary(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                ozt__ney = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(ozt__ney, -1)
                for dbf__airn in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    if bodo.libs.array_kernels.isna(data, dbf__airn):
                        bodo.libs.array_kernels.setna(A, dbf__airn)
                    else:
                        A[dbf__airn] = ''.join([chr(mferk__phzg) for
                            mferk__phzg in data[dbf__airn]])
                return A
            return impl_binary
        if is_overload_true(from_series) and data.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns):

            def impl_str_dt_series(data, new_dtype, copy=None, nan_to_str=
                True, from_series=False):
                numba.parfors.parfor.init_prange()
                ozt__ney = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(ozt__ney, -1)
                for dbf__airn in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    if bodo.libs.array_kernels.isna(data, dbf__airn):
                        if nan_to_str:
                            A[dbf__airn] = 'NaT'
                        else:
                            bodo.libs.array_kernels.setna(A, dbf__airn)
                        continue
                    A[dbf__airn] = str(box_if_dt64(data[dbf__airn]))
                return A
            return impl_str_dt_series
        else:

            def impl_str_array(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                ozt__ney = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(ozt__ney, -1)
                for dbf__airn in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    if bodo.libs.array_kernels.isna(data, dbf__airn):
                        if nan_to_str:
                            A[dbf__airn] = 'nan'
                        else:
                            bodo.libs.array_kernels.setna(A, dbf__airn)
                        continue
                    A[dbf__airn] = str(data[dbf__airn])
                return A
            return impl_str_array
    if isinstance(new_dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):

        def impl_cat_dtype(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            ozt__ney = len(data)
            numba.parfors.parfor.init_prange()
            kttvv__wvo = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories(new_dtype.categories.values))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                ozt__ney, new_dtype)
            drtqo__vpuch = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney):
                if bodo.libs.array_kernels.isna(data, edjw__otdr):
                    bodo.libs.array_kernels.setna(A, edjw__otdr)
                    continue
                val = data[edjw__otdr]
                if val not in kttvv__wvo:
                    bodo.libs.array_kernels.setna(A, edjw__otdr)
                    continue
                drtqo__vpuch[edjw__otdr] = kttvv__wvo[val]
            return A
        return impl_cat_dtype
    if is_overload_constant_str(new_dtype) and get_overload_const_str(new_dtype
        ) == 'category':

        def impl_category(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            ygyrp__psa = bodo.libs.array_kernels.unique(data, dropna=True)
            ygyrp__psa = pd.Series(ygyrp__psa).sort_values().values
            ygyrp__psa = bodo.allgatherv(ygyrp__psa, False)
            vdxj__psrm = bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo
                .utils.conversion.index_from_array(ygyrp__psa, None), False,
                None, None)
            ozt__ney = len(data)
            numba.parfors.parfor.init_prange()
            kttvv__wvo = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories_no_duplicates(ygyrp__psa))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                ozt__ney, vdxj__psrm)
            drtqo__vpuch = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney):
                if bodo.libs.array_kernels.isna(data, edjw__otdr):
                    bodo.libs.array_kernels.setna(A, edjw__otdr)
                    continue
                val = data[edjw__otdr]
                drtqo__vpuch[edjw__otdr] = kttvv__wvo[val]
            return A
        return impl_category
    nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType):
        licg__jqrr = isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype
            ) and data.dtype == nb_dtype.dtype
    else:
        licg__jqrr = data.dtype == nb_dtype
    if wsqu__gbnmh and licg__jqrr:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.copy())
    if licg__jqrr:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
        if isinstance(nb_dtype, types.Integer):
            cxfa__gbnii = nb_dtype
        else:
            cxfa__gbnii = nb_dtype.dtype
        if isinstance(data.dtype, types.Float):

            def impl_float(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                ozt__ney = len(data)
                numba.parfors.parfor.init_prange()
                mgqkr__btjb = bodo.libs.int_arr_ext.alloc_int_array(ozt__ney,
                    cxfa__gbnii)
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    if bodo.libs.array_kernels.isna(data, edjw__otdr):
                        bodo.libs.array_kernels.setna(mgqkr__btjb, edjw__otdr)
                    else:
                        mgqkr__btjb[edjw__otdr] = int(data[edjw__otdr])
                return mgqkr__btjb
            return impl_float
        else:
            if data == bodo.dict_str_arr_type:

                def impl_dict(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    return bodo.libs.dict_arr_ext.convert_dict_arr_to_int(data,
                        cxfa__gbnii)
                return impl_dict

            def impl(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                ozt__ney = len(data)
                numba.parfors.parfor.init_prange()
                mgqkr__btjb = bodo.libs.int_arr_ext.alloc_int_array(ozt__ney,
                    cxfa__gbnii)
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    if bodo.libs.array_kernels.isna(data, edjw__otdr):
                        bodo.libs.array_kernels.setna(mgqkr__btjb, edjw__otdr)
                    else:
                        mgqkr__btjb[edjw__otdr] = np.int64(data[edjw__otdr])
                return mgqkr__btjb
            return impl
    if isinstance(nb_dtype, types.Integer) and isinstance(data.dtype, types
        .Integer):

        def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False
            ):
            return data.astype(nb_dtype)
        return impl
    if nb_dtype == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            ozt__ney = len(data)
            numba.parfors.parfor.init_prange()
            mgqkr__btjb = bodo.libs.bool_arr_ext.alloc_bool_array(ozt__ney)
            for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney):
                if bodo.libs.array_kernels.isna(data, edjw__otdr):
                    bodo.libs.array_kernels.setna(mgqkr__btjb, edjw__otdr)
                else:
                    mgqkr__btjb[edjw__otdr] = bool(data[edjw__otdr])
            return mgqkr__btjb
        return impl_bool
    if nb_dtype == bodo.datetime_date_type:
        if data.dtype == bodo.datetime64ns:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                ozt__ney = len(data)
                biktd__fsb = (bodo.hiframes.datetime_date_ext.
                    alloc_datetime_date_array(ozt__ney))
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    if bodo.libs.array_kernels.isna(data, edjw__otdr):
                        bodo.libs.array_kernels.setna(biktd__fsb, edjw__otdr)
                    else:
                        biktd__fsb[edjw__otdr
                            ] = bodo.utils.conversion.box_if_dt64(data[
                            edjw__otdr]).date()
                return biktd__fsb
            return impl_date
    if nb_dtype == bodo.datetime64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_dt64_astype(
                    data)
            return impl_str
        if data == bodo.datetime_date_array_type:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return (bodo.hiframes.pd_timestamp_ext.
                    datetime_date_arr_to_dt64_arr(data))
            return impl_date
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            timedelta64ns, types.bool_]:

            def impl_numeric(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                ozt__ney = len(data)
                numba.parfors.parfor.init_prange()
                biktd__fsb = np.empty(ozt__ney, dtype=np.dtype(
                    'datetime64[ns]'))
                for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney
                    ):
                    if bodo.libs.array_kernels.isna(data, edjw__otdr):
                        bodo.libs.array_kernels.setna(biktd__fsb, edjw__otdr)
                    else:
                        biktd__fsb[edjw__otdr
                            ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                            np.int64(data[edjw__otdr]))
                return biktd__fsb
            return impl_numeric
    if nb_dtype == bodo.timedelta64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_td64_astype(
                    data)
            return impl_str
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            datetime64ns, types.bool_]:
            if wsqu__gbnmh:

                def impl_numeric(data, new_dtype, copy=None, nan_to_str=
                    True, from_series=False):
                    ozt__ney = len(data)
                    numba.parfors.parfor.init_prange()
                    biktd__fsb = np.empty(ozt__ney, dtype=np.dtype(
                        'timedelta64[ns]'))
                    for edjw__otdr in numba.parfors.parfor.internal_prange(
                        ozt__ney):
                        if bodo.libs.array_kernels.isna(data, edjw__otdr):
                            bodo.libs.array_kernels.setna(biktd__fsb,
                                edjw__otdr)
                        else:
                            biktd__fsb[edjw__otdr] = (bodo.hiframes.
                                pd_timestamp_ext.integer_to_timedelta64(np.
                                int64(data[edjw__otdr])))
                    return biktd__fsb
                return impl_numeric
            else:
                return (lambda data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False: data.view('int64'))
    if nb_dtype == types.int64 and data.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]:

        def impl_datelike_to_integer(data, new_dtype, copy=None, nan_to_str
            =True, from_series=False):
            ozt__ney = len(data)
            numba.parfors.parfor.init_prange()
            A = np.empty(ozt__ney, types.int64)
            for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney):
                if bodo.libs.array_kernels.isna(data, edjw__otdr):
                    bodo.libs.array_kernels.setna(A, edjw__otdr)
                else:
                    A[edjw__otdr] = np.int64(data[edjw__otdr])
            return A
        return impl_datelike_to_integer
    if data.dtype != nb_dtype:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.astype(nb_dtype))
    raise BodoError(f'Conversion from {data} to {new_dtype} not supported yet')


def array_type_from_dtype(dtype):
    return dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))


@overload(array_type_from_dtype)
def overload_array_type_from_dtype(dtype):
    arr_type = dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))
    return lambda dtype: arr_type


@numba.jit
def flatten_array(A):
    sfjcu__ixb = []
    ozt__ney = len(A)
    for edjw__otdr in range(ozt__ney):
        gpjz__gwei = A[edjw__otdr]
        for gwrti__fsvj in gpjz__gwei:
            sfjcu__ixb.append(gwrti__fsvj)
    return bodo.utils.conversion.coerce_to_array(sfjcu__ixb)


def parse_datetimes_from_strings(data):
    return data


@overload(parse_datetimes_from_strings, no_unliteral=True)
def overload_parse_datetimes_from_strings(data):
    assert is_str_arr_type(data
        ), 'parse_datetimes_from_strings: string array expected'

    def parse_impl(data):
        numba.parfors.parfor.init_prange()
        ozt__ney = len(data)
        mrub__cxt = np.empty(ozt__ney, bodo.utils.conversion.NS_DTYPE)
        for edjw__otdr in numba.parfors.parfor.internal_prange(ozt__ney):
            mrub__cxt[edjw__otdr
                ] = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(data[
                edjw__otdr])
        return mrub__cxt
    return parse_impl


def convert_to_dt64ns(data):
    return data


@overload(convert_to_dt64ns, no_unliteral=True)
def overload_convert_to_dt64ns(data):
    if data == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        return (lambda data: bodo.hiframes.pd_timestamp_ext.
            datetime_date_arr_to_dt64_arr(data))
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.NS_DTYPE)
    if is_np_arr_typ(data, types.NPDatetime('ns')):
        return lambda data: data
    if is_str_arr_type(data):
        return lambda data: bodo.utils.conversion.parse_datetimes_from_strings(
            data)
    raise BodoError(f'invalid data type {data} for dt64 conversion')


def convert_to_td64ns(data):
    return data


@overload(convert_to_td64ns, no_unliteral=True)
def overload_convert_to_td64ns(data):
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.TD_DTYPE)
    if is_np_arr_typ(data, types.NPTimedelta('ns')):
        return lambda data: data
    if is_str_arr_type(data):
        raise BodoError('conversion to timedelta from string not supported yet'
            )
    raise BodoError(f'invalid data type {data} for timedelta64 conversion')


def convert_to_index(data, name=None):
    return data


@overload(convert_to_index, no_unliteral=True)
def overload_convert_to_index(data, name=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
    if isinstance(data, (RangeIndexType, NumericIndexType,
        DatetimeIndexType, TimedeltaIndexType, StringIndexType,
        BinaryIndexType, CategoricalIndexType, PeriodIndexType, types.NoneType)
        ):
        return lambda data, name=None: data

    def impl(data, name=None):
        ntsg__mfex = bodo.utils.conversion.coerce_to_array(data)
        return bodo.utils.conversion.index_from_array(ntsg__mfex, name)
    return impl


def force_convert_index(I1, I2):
    return I2


@overload(force_convert_index, no_unliteral=True)
def overload_force_convert_index(I1, I2):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I2, RangeIndexType):
        return lambda I1, I2: pd.RangeIndex(len(I1._data))
    return lambda I1, I2: I1


def index_from_array(data, name=None):
    return data


@overload(index_from_array, no_unliteral=True)
def overload_index_from_array(data, name=None):
    if data in [bodo.string_array_type, bodo.binary_array_type]:
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_binary_str_index(data, name))
    if data == bodo.dict_str_arr_type:
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_binary_str_index(decode_if_dict_array(data), name))
    if (data == bodo.hiframes.datetime_date_ext.datetime_date_array_type or
        data.dtype == types.NPDatetime('ns')):
        return lambda data, name=None: pd.DatetimeIndex(data, name=name)
    if data.dtype == types.NPTimedelta('ns'):
        return lambda data, name=None: pd.TimedeltaIndex(data, name=name)
    if isinstance(data.dtype, (types.Integer, types.Float, types.Boolean)):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_numeric_index(data, name))
    if isinstance(data, bodo.libs.interval_arr_ext.IntervalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_interval_index(data, name))
    if isinstance(data, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_categorical_index(data, name))
    if isinstance(data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_datetime_index(data, name))
    raise BodoError(f'cannot convert {data} to Index')


def index_to_array(data):
    return data


@overload(index_to_array, no_unliteral=True)
def overload_index_to_array(I):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I, RangeIndexType):
        return lambda I: np.arange(I._start, I._stop, I._step)
    return lambda I: bodo.hiframes.pd_index_ext.get_index_data(I)


def false_if_none(val):
    return False if val is None else val


@overload(false_if_none, no_unliteral=True)
def overload_false_if_none(val):
    if is_overload_none(val):
        return lambda val: False
    return lambda val: val


def extract_name_if_none(data, name):
    return name


@overload(extract_name_if_none, no_unliteral=True)
def overload_extract_name_if_none(data, name):
    from bodo.hiframes.pd_index_ext import CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(name):
        return lambda data, name: name
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, PeriodIndexType, CategoricalIndexType)):
        return lambda data, name: bodo.hiframes.pd_index_ext.get_index_name(
            data)
    if isinstance(data, SeriesType):
        return lambda data, name: bodo.hiframes.pd_series_ext.get_series_name(
            data)
    return lambda data, name: name


def extract_index_if_none(data, index):
    return index


@overload(extract_index_if_none, no_unliteral=True)
def overload_extract_index_if_none(data, index):
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(index):
        return lambda data, index: index
    if isinstance(data, SeriesType):
        return (lambda data, index: bodo.hiframes.pd_series_ext.
            get_series_index(data))
    return lambda data, index: bodo.hiframes.pd_index_ext.init_range_index(
        0, len(data), 1, None)


def box_if_dt64(val):
    return val


@overload(box_if_dt64, no_unliteral=True)
def overload_box_if_dt64(val):
    if val == types.NPDatetime('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_datetime64_to_timestamp(val))
    if val == types.NPTimedelta('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_numpy_timedelta64_to_pd_timedelta(val))
    return lambda val: val


def unbox_if_timestamp(val):
    return val


@overload(unbox_if_timestamp, no_unliteral=True)
def overload_unbox_if_timestamp(val):
    if val == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val
            .value)
    if val == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(pd
            .Timestamp(val).value)
    if val == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(val.value))
    if val == types.Optional(bodo.hiframes.pd_timestamp_ext.pd_timestamp_type):

        def impl_optional(val):
            if val is None:
                znfeh__xei = None
            else:
                znfeh__xei = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    bodo.utils.indexing.unoptional(val).value)
            return znfeh__xei
        return impl_optional
    if val == types.Optional(bodo.hiframes.datetime_timedelta_ext.
        pd_timedelta_type):

        def impl_optional_td(val):
            if val is None:
                znfeh__xei = None
            else:
                znfeh__xei = (bodo.hiframes.pd_timestamp_ext.
                    integer_to_timedelta64(bodo.utils.indexing.unoptional(
                    val).value))
            return znfeh__xei
        return impl_optional_td
    return lambda val: val


def to_tuple(val):
    return val


@overload(to_tuple, no_unliteral=True)
def overload_to_tuple(val):
    if not isinstance(val, types.BaseTuple) and is_overload_constant_list(val):
        usmxu__byh = len(val.types if isinstance(val, types.LiteralList) else
            get_overload_const_list(val))
        gkuc__gvh = 'def f(val):\n'
        zjij__pdzdq = ','.join(f'val[{edjw__otdr}]' for edjw__otdr in range
            (usmxu__byh))
        gkuc__gvh += f'  return ({zjij__pdzdq},)\n'
        hjl__cgoh = {}
        exec(gkuc__gvh, {}, hjl__cgoh)
        impl = hjl__cgoh['f']
        return impl
    assert isinstance(val, types.BaseTuple), 'tuple type expected'
    return lambda val: val


def get_array_if_series_or_index(data):
    return data


@overload(get_array_if_series_or_index)
def overload_get_array_if_series_or_index(data):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(data, SeriesType):
        return lambda data: bodo.hiframes.pd_series_ext.get_series_data(data)
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        return lambda data: bodo.utils.conversion.coerce_to_array(data)
    if isinstance(data, bodo.hiframes.pd_index_ext.HeterogeneousIndexType):
        if not is_heterogeneous_tuple_type(data.data):

            def impl(data):
                uppm__wtwsd = bodo.hiframes.pd_index_ext.get_index_data(data)
                return bodo.utils.conversion.coerce_to_array(uppm__wtwsd)
            return impl

        def impl(data):
            return bodo.hiframes.pd_index_ext.get_index_data(data)
        return impl
    return lambda data: data


def extract_index_array(A):
    return np.arange(len(A))


@overload(extract_index_array, no_unliteral=True)
def overload_extract_index_array(A):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(A, SeriesType):

        def impl(A):
            index = bodo.hiframes.pd_series_ext.get_series_index(A)
            vxwhs__bckjb = bodo.utils.conversion.coerce_to_array(index)
            return vxwhs__bckjb
        return impl
    return lambda A: np.arange(len(A))


def ensure_contig_if_np(arr):
    return np.ascontiguousarray(arr)


@overload(ensure_contig_if_np, no_unliteral=True)
def overload_ensure_contig_if_np(arr):
    if isinstance(arr, types.Array):
        return lambda arr: np.ascontiguousarray(arr)
    return lambda arr: arr


def struct_if_heter_dict(values, names):
    return {txunz__nftdu: zhea__fhgar for txunz__nftdu, zhea__fhgar in zip(
        names, values)}


@overload(struct_if_heter_dict, no_unliteral=True)
def overload_struct_if_heter_dict(values, names):
    if not types.is_homogeneous(*values.types):
        return lambda values, names: bodo.libs.struct_arr_ext.init_struct(
            values, names)
    evfr__rto = len(values.types)
    gkuc__gvh = 'def f(values, names):\n'
    zjij__pdzdq = ','.join("'{}': values[{}]".format(get_overload_const_str
        (names.types[edjw__otdr]), edjw__otdr) for edjw__otdr in range(
        evfr__rto))
    gkuc__gvh += '  return {{{}}}\n'.format(zjij__pdzdq)
    hjl__cgoh = {}
    exec(gkuc__gvh, {}, hjl__cgoh)
    impl = hjl__cgoh['f']
    return impl
