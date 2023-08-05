"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
from typing import Tuple
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_getattr, models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import _no_input, datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import DatetimeIndexType, RangeIndexType, StringIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array, boolean_dtype
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_index_data_arr_types, get_index_names, get_literal_value, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, parse_dtype, raise_bodo_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names: Tuple):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        utt__syv = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({utt__syv})\n')
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    zuwt__foby = 'def impl(df):\n'
    if df.has_runtime_cols:
        zuwt__foby += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        qvd__rwisw = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        zuwt__foby += f'  return {qvd__rwisw}'
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo}, lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    check_runtime_cols_unsupported(df, 'DataFrame.values')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.values')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.values: only supported for dataframes containing numeric values'
            )
    ona__salxe = len(df.columns)
    tfge__rdsvb = set(i for i in range(ona__salxe) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in tfge__rdsvb else '') for i in
        range(ona__salxe))
    zuwt__foby = 'def f(df):\n'.format()
    zuwt__foby += '    return np.stack(({},), 1)\n'.format(data_args)
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo, 'np': np}, lrc__hdl)
    fuyvn__ytrh = lrc__hdl['f']
    return fuyvn__ytrh


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False, na_value=_no_input
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.to_numpy()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.to_numpy()')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.to_numpy(): only supported for dataframes containing numeric values'
            )
    vabyk__txgl = {'dtype': dtype, 'na_value': na_value}
    oci__mue = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', vabyk__txgl, oci__mue,
        package_name='pandas', module_name='DataFrame')

    def impl(df, dtype=None, copy=False, na_value=_no_input):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            het__glnih = bodo.hiframes.table.compute_num_runtime_columns(t)
            return het__glnih * len(t)
        return impl
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@lower_getattr(DataFrameType, 'shape')
def lower_dataframe_shape(context, builder, typ, val):
    impl = overload_dataframe_shape(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def overload_dataframe_shape(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            het__glnih = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), het__glnih
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    zuwt__foby = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    uxpb__slsoj = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    zuwt__foby += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{uxpb__slsoj}), {index}, None)
"""
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo}, lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    check_runtime_cols_unsupported(df, 'DataFrame.empty')
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    check_runtime_cols_unsupported(df, 'DataFrame.assign()')
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    check_runtime_cols_unsupported(df, 'DataFrame.insert()')
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if isinstance(dtype, types.PyObject) or dtype in (object, 'object'):
        return "'object'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True, _bodo_object_typeref=None):
    check_runtime_cols_unsupported(df, 'DataFrame.astype()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.astype()')
    vabyk__txgl = {'copy': copy, 'errors': errors}
    oci__mue = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', vabyk__txgl, oci__mue, package_name
        ='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        fjzz__wuyv = _bodo_object_typeref.instance_type
        assert isinstance(fjzz__wuyv, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        arq__bibq = {}
        for i, name in enumerate(fjzz__wuyv.columns):
            arr_typ = fjzz__wuyv.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                pcmew__qtpy = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                pcmew__qtpy = boolean_dtype
            else:
                pcmew__qtpy = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = pcmew__qtpy
            arq__bibq[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {arq__bibq[bjo__ykb]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if bjo__ykb in arq__bibq else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, bjo__ykb in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        vpa__opt = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(vpa__opt[bjo__ykb])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if bjo__ykb in vpa__opt else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, bjo__ykb in enumerate(df.columns))
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    header = """def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True, _bodo_object_typeref=None):
"""
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    check_runtime_cols_unsupported(df, 'DataFrame.copy()')
    vhbpc__uwwo = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(deep):
            vhbpc__uwwo.append(arr + '.copy()')
        elif is_overload_false(deep):
            vhbpc__uwwo.append(arr)
        else:
            vhbpc__uwwo.append(f'{arr}.copy() if deep else {arr}')
    header = 'def impl(df, deep=True):\n'
    return _gen_init_df(header, df.columns, ', '.join(vhbpc__uwwo))


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    vabyk__txgl = {'index': index, 'level': level, 'errors': errors}
    oci__mue = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', vabyk__txgl, oci__mue,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        qmfyt__qsh = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        qmfyt__qsh = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    uow__tkb = [qmfyt__qsh.get(df.columns[i], df.columns[i]) for i in range
        (len(df.columns))]
    vhbpc__uwwo = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(copy):
            vhbpc__uwwo.append(arr + '.copy()')
        elif is_overload_false(copy):
            vhbpc__uwwo.append(arr)
        else:
            vhbpc__uwwo.append(f'{arr}.copy() if copy else {arr}')
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    return _gen_init_df(header, uow__tkb, ', '.join(vhbpc__uwwo))


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    ulc__uvnkg = not is_overload_none(items)
    zja__ydom = not is_overload_none(like)
    aygn__nqx = not is_overload_none(regex)
    mpp__yovo = ulc__uvnkg ^ zja__ydom ^ aygn__nqx
    icm__aenxg = not (ulc__uvnkg or zja__ydom or aygn__nqx)
    if icm__aenxg:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not mpp__yovo:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        if axis not in {'index', 'columns'}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either "index" or "columns" if string'
                )
        fsn__zmby = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        fsn__zmby = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert fsn__zmby in {0, 1}
    zuwt__foby = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if fsn__zmby == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if fsn__zmby == 1:
        hpcc__ecy = []
        rtf__bgw = []
        rfvu__hdaj = []
        if ulc__uvnkg:
            if is_overload_constant_list(items):
                zmd__fcs = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if zja__ydom:
            if is_overload_constant_str(like):
                lcck__azp = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if aygn__nqx:
            if is_overload_constant_str(regex):
                gpep__dfvu = get_overload_const_str(regex)
                groh__mqywo = re.compile(gpep__dfvu)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, bjo__ykb in enumerate(df.columns):
            if not is_overload_none(items
                ) and bjo__ykb in zmd__fcs or not is_overload_none(like
                ) and lcck__azp in str(bjo__ykb) or not is_overload_none(regex
                ) and groh__mqywo.search(str(bjo__ykb)):
                rtf__bgw.append(bjo__ykb)
                rfvu__hdaj.append(i)
        for i in rfvu__hdaj:
            var_name = f'data_{i}'
            hpcc__ecy.append(var_name)
            zuwt__foby += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(hpcc__ecy)
        return _gen_init_df(zuwt__foby, rtf__bgw, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        uqh__dmy = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([uqh__dmy] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': uqh__dmy}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    check_runtime_cols_unsupported(df, 'DataFrame.select_dtypes')
    qbv__dmhm = is_overload_none(include)
    qph__yyunc = is_overload_none(exclude)
    djvvh__aako = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if qbv__dmhm and qph__yyunc:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not qbv__dmhm:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            ktp__qzw = [dtype_to_array_type(parse_dtype(elem, djvvh__aako)) for
                elem in include]
        elif is_legal_input(include):
            ktp__qzw = [dtype_to_array_type(parse_dtype(include, djvvh__aako))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        ktp__qzw = get_nullable_and_non_nullable_types(ktp__qzw)
        saby__gnnhz = tuple(bjo__ykb for i, bjo__ykb in enumerate(df.
            columns) if df.data[i] in ktp__qzw)
    else:
        saby__gnnhz = df.columns
    if not qph__yyunc:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            kfpzd__qkhr = [dtype_to_array_type(parse_dtype(elem,
                djvvh__aako)) for elem in exclude]
        elif is_legal_input(exclude):
            kfpzd__qkhr = [dtype_to_array_type(parse_dtype(exclude,
                djvvh__aako))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        kfpzd__qkhr = get_nullable_and_non_nullable_types(kfpzd__qkhr)
        saby__gnnhz = tuple(bjo__ykb for bjo__ykb in saby__gnnhz if df.data
            [df.columns.index(bjo__ykb)] not in kfpzd__qkhr)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(bjo__ykb)})'
         for bjo__ykb in saby__gnnhz)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, saby__gnnhz, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        uqh__dmy = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([uqh__dmy] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': uqh__dmy}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'~bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


def overload_dataframe_head(df, n=5):
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    check_runtime_cols_unsupported(df, 'DataFrame.tail()')
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'first', inline='always', no_unliteral=True)
def overload_dataframe_first(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.first()')
    xiy__pjal = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in xiy__pjal:
        raise BodoError(
            "DataFrame.first(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.first()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:valid_entries]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:valid_entries]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    start_date = df_index[0]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, start_date, False)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'last', inline='always', no_unliteral=True)
def overload_dataframe_last(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.last()')
    xiy__pjal = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in xiy__pjal:
        raise BodoError(
            "DataFrame.last(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.last()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[len(df)-valid_entries:]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[len(df)-valid_entries:]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    final_date = df_index[-1]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, final_date, True)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_string()')

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    check_runtime_cols_unsupported(df, 'DataFrame.isin()')
    from bodo.utils.typing import is_iterable_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.isin()')
    zuwt__foby = 'def impl(df, values):\n'
    gft__hwan = {}
    efw__rnoi = False
    if isinstance(values, DataFrameType):
        efw__rnoi = True
        for i, bjo__ykb in enumerate(df.columns):
            if bjo__ykb in values.columns:
                qze__pedh = 'val{}'.format(i)
                zuwt__foby += (
                    """  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {})
"""
                    .format(qze__pedh, values.columns.index(bjo__ykb)))
                gft__hwan[bjo__ykb] = qze__pedh
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        gft__hwan = {bjo__ykb: 'values' for bjo__ykb in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        qze__pedh = 'data{}'.format(i)
        zuwt__foby += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(qze__pedh, i))
        data.append(qze__pedh)
    qkhoi__focgt = ['out{}'.format(i) for i in range(len(df.columns))]
    zdggr__byio = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    aab__jgc = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    lbqi__cozq = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, mxwds__bos) in enumerate(zip(df.columns, data)):
        if cname in gft__hwan:
            qznms__jdgyb = gft__hwan[cname]
            if efw__rnoi:
                zuwt__foby += zdggr__byio.format(mxwds__bos, qznms__jdgyb,
                    qkhoi__focgt[i])
            else:
                zuwt__foby += aab__jgc.format(mxwds__bos, qznms__jdgyb,
                    qkhoi__focgt[i])
        else:
            zuwt__foby += lbqi__cozq.format(qkhoi__focgt[i])
    return _gen_init_df(zuwt__foby, df.columns, ','.join(qkhoi__focgt))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    ona__salxe = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(ona__salxe))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    fqvwd__ymxpr = [bjo__ykb for bjo__ykb, ycm__nqpk in zip(df.columns, df.
        data) if bodo.utils.typing._is_pandas_numeric_dtype(ycm__nqpk.dtype)]
    assert len(fqvwd__ymxpr) != 0
    wryuu__dvge = ''
    if not any(ycm__nqpk == types.float64 for ycm__nqpk in df.data):
        wryuu__dvge = '.astype(np.float64)'
    jtxog__ciczf = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(bjo__ykb), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(bjo__ykb)], IntegerArrayType) or
        df.data[df.columns.index(bjo__ykb)] == boolean_array else '') for
        bjo__ykb in fqvwd__ymxpr)
    psjb__xvj = 'np.stack(({},), 1){}'.format(jtxog__ciczf, wryuu__dvge)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        fqvwd__ymxpr)))
    index = f'{generate_col_to_index_func_text(fqvwd__ymxpr)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(psjb__xvj)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, fqvwd__ymxpr, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    vtgbb__kpod = dict(ddof=ddof)
    linof__dtsm = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    cbigy__wdq = '1' if is_overload_none(min_periods) else 'min_periods'
    fqvwd__ymxpr = [bjo__ykb for bjo__ykb, ycm__nqpk in zip(df.columns, df.
        data) if bodo.utils.typing._is_pandas_numeric_dtype(ycm__nqpk.dtype)]
    if len(fqvwd__ymxpr) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    wryuu__dvge = ''
    if not any(ycm__nqpk == types.float64 for ycm__nqpk in df.data):
        wryuu__dvge = '.astype(np.float64)'
    jtxog__ciczf = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(bjo__ykb), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(bjo__ykb)], IntegerArrayType) or
        df.data[df.columns.index(bjo__ykb)] == boolean_array else '') for
        bjo__ykb in fqvwd__ymxpr)
    psjb__xvj = 'np.stack(({},), 1){}'.format(jtxog__ciczf, wryuu__dvge)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        fqvwd__ymxpr)))
    index = f'pd.Index({fqvwd__ymxpr})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(psjb__xvj)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        cbigy__wdq)
    return _gen_init_df(header, fqvwd__ymxpr, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    vtgbb__kpod = dict(axis=axis, level=level, numeric_only=numeric_only)
    linof__dtsm = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    zuwt__foby = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    zuwt__foby += '  data = np.array([{}])\n'.format(data_args)
    qvd__rwisw = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    zuwt__foby += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {qvd__rwisw})\n'
        )
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo, 'np': np}, lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    vtgbb__kpod = dict(axis=axis)
    linof__dtsm = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    zuwt__foby = 'def impl(df, axis=0, dropna=True):\n'
    zuwt__foby += '  data = np.asarray(({},))\n'.format(data_args)
    qvd__rwisw = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    zuwt__foby += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {qvd__rwisw})\n'
        )
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo, 'np': np}, lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    vtgbb__kpod = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    linof__dtsm = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    vtgbb__kpod = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    linof__dtsm = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    vtgbb__kpod = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    linof__dtsm = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    vtgbb__kpod = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    linof__dtsm = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    vtgbb__kpod = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    linof__dtsm = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    vtgbb__kpod = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    linof__dtsm = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    vtgbb__kpod = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    linof__dtsm = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    vtgbb__kpod = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    linof__dtsm = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    vtgbb__kpod = dict(numeric_only=numeric_only, interpolation=interpolation)
    linof__dtsm = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    vtgbb__kpod = dict(axis=axis, skipna=skipna)
    linof__dtsm = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for akate__emgxp in df.data:
        if not (bodo.utils.utils.is_np_array_typ(akate__emgxp) and (
            akate__emgxp.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(akate__emgxp.dtype, (types.Number, types.Boolean))) or
            isinstance(akate__emgxp, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or akate__emgxp in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {akate__emgxp} not supported.'
                )
        if isinstance(akate__emgxp, bodo.CategoricalArrayType
            ) and not akate__emgxp.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    vtgbb__kpod = dict(axis=axis, skipna=skipna)
    linof__dtsm = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for akate__emgxp in df.data:
        if not (bodo.utils.utils.is_np_array_typ(akate__emgxp) and (
            akate__emgxp.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(akate__emgxp.dtype, (types.Number, types.Boolean))) or
            isinstance(akate__emgxp, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or akate__emgxp in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {akate__emgxp} not supported.'
                )
        if isinstance(akate__emgxp, bodo.CategoricalArrayType
            ) and not akate__emgxp.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


@overload_method(DataFrameType, 'infer_objects', inline='always')
def overload_dataframe_infer_objects(df):
    check_runtime_cols_unsupported(df, 'DataFrame.infer_objects()')
    return lambda df: df.copy()


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
    else:
        raise_bodo_error(
            f'DataFrame.{func_name}: axis must be a constant Integer')
    assert axis in (0, 1), f'invalid axis argument for DataFrame.{func_name}'
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        fqvwd__ymxpr = tuple(bjo__ykb for bjo__ykb, ycm__nqpk in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (ycm__nqpk.dtype))
        out_colnames = fqvwd__ymxpr
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            ebmvs__xwuec = [numba.np.numpy_support.as_dtype(df.data[df.
                columns.index(bjo__ykb)].dtype) for bjo__ykb in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(ebmvs__xwuec, []))
    except NotImplementedError as dynxd__cuv:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    memdx__axr = ''
    if func_name in ('sum', 'prod'):
        memdx__axr = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    zuwt__foby = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, memdx__axr))
    if func_name == 'quantile':
        zuwt__foby = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        zuwt__foby = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        zuwt__foby += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        zuwt__foby += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    uryrq__hst = ''
    if func_name in ('min', 'max'):
        uryrq__hst = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        uryrq__hst = ', dtype=np.float32'
    xmowy__fzd = f'bodo.libs.array_ops.array_op_{func_name}'
    lihny__ffpe = ''
    if func_name in ['sum', 'prod']:
        lihny__ffpe = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        lihny__ffpe = 'index'
    elif func_name == 'quantile':
        lihny__ffpe = 'q'
    elif func_name in ['std', 'var']:
        lihny__ffpe = 'True, ddof'
    elif func_name == 'median':
        lihny__ffpe = 'True'
    data_args = ', '.join(
        f'{xmowy__fzd}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(bjo__ykb)}), {lihny__ffpe})'
         for bjo__ykb in out_colnames)
    zuwt__foby = ''
    if func_name in ('idxmax', 'idxmin'):
        zuwt__foby += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        zuwt__foby += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        zuwt__foby += '  data = np.asarray(({},){})\n'.format(data_args,
            uryrq__hst)
    zuwt__foby += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return zuwt__foby


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    epx__bli = [df_type.columns.index(bjo__ykb) for bjo__ykb in out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in epx__bli)
    xgmb__cqsda = '\n        '.join(f'row[{i}] = arr_{epx__bli[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    veva__iuha = f'len(arr_{epx__bli[0]})'
    gns__rbms = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum': 'np.nansum',
        'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in gns__rbms:
        xkrqz__xwta = gns__rbms[func_name]
        kee__gpect = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        zuwt__foby = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {veva__iuha}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{kee__gpect})
    for i in numba.parfors.parfor.internal_prange(n):
        {xgmb__cqsda}
        A[i] = {xkrqz__xwta}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return zuwt__foby
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    vtgbb__kpod = dict(fill_method=fill_method, limit=limit, freq=freq)
    linof__dtsm = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.pct_change()')
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumprod()')
    vtgbb__kpod = dict(axis=axis, skipna=skipna)
    linof__dtsm = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumprod()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumsum()')
    vtgbb__kpod = dict(skipna=skipna)
    linof__dtsm = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumsum()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, IntegerArrayType) or isinstance(data, types.Array
        ) and isinstance(data.dtype, types.Number
        ) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    check_runtime_cols_unsupported(df, 'DataFrame.describe()')
    vtgbb__kpod = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    linof__dtsm = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    fqvwd__ymxpr = [bjo__ykb for bjo__ykb, ycm__nqpk in zip(df.columns, df.
        data) if _is_describe_type(ycm__nqpk)]
    if len(fqvwd__ymxpr) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    xwgpr__zlz = sum(df.data[df.columns.index(bjo__ykb)].dtype == bodo.
        datetime64ns for bjo__ykb in fqvwd__ymxpr)

    def _get_describe(col_ind):
        zuee__hdt = df.data[col_ind].dtype == bodo.datetime64ns
        if xwgpr__zlz and xwgpr__zlz != len(fqvwd__ymxpr):
            if zuee__hdt:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for bjo__ykb in fqvwd__ymxpr:
        col_ind = df.columns.index(bjo__ykb)
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.columns.index(bjo__ykb)) for
        bjo__ykb in fqvwd__ymxpr)
    xzrr__iosnq = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if xwgpr__zlz == len(fqvwd__ymxpr):
        xzrr__iosnq = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif xwgpr__zlz:
        xzrr__iosnq = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({xzrr__iosnq})'
    return _gen_init_df(header, fqvwd__ymxpr, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    vtgbb__kpod = dict(axis=axis, convert=convert, is_copy=is_copy)
    linof__dtsm = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.shift()')
    vtgbb__kpod = dict(freq=freq, axis=axis, fill_value=fill_value)
    linof__dtsm = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for iply__sobsc in df.data:
        if not is_supported_shift_array_type(iply__sobsc):
            raise BodoError(
                f'Dataframe.shift() column input type {iply__sobsc.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    check_runtime_cols_unsupported(df, 'DataFrame.diff()')
    vtgbb__kpod = dict(axis=axis)
    linof__dtsm = dict(axis=0)
    check_unsupported_args('DataFrame.diff', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for iply__sobsc in df.data:
        if not (isinstance(iply__sobsc, types.Array) and (isinstance(
            iply__sobsc.dtype, types.Number) or iply__sobsc.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {iply__sobsc.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'explode', inline='always', no_unliteral=True)
def overload_dataframe_explode(df, column, ignore_index=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.explode()')
    xlibx__clkxt = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(xlibx__clkxt)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        krdk__vaun = get_overload_const_list(column)
    else:
        krdk__vaun = [get_literal_value(column)]
    ohfe__gqb = {bjo__ykb: i for i, bjo__ykb in enumerate(df.columns)}
    bbts__zds = [ohfe__gqb[bjo__ykb] for bjo__ykb in krdk__vaun]
    for i in bbts__zds:
        if not isinstance(df.data[i], ArrayItemArrayType) and df.data[i
            ].dtype != string_array_split_view_type:
            raise BodoError(
                f'DataFrame.explode(): columns must have array-like entries')
    n = len(df.columns)
    header = 'def impl(df, column, ignore_index=False):\n'
    header += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    header += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    for i in range(n):
        header += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    header += (
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{bbts__zds[0]})\n'
        )
    for i in range(n):
        if i in bbts__zds:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.explode_no_index(data{i}, counts)\n'
                )
        else:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.repeat_kernel(data{i}, counts)\n'
                )
    header += (
        '  new_index = bodo.libs.array_kernels.repeat_kernel(index_arr, counts)\n'
        )
    data_args = ', '.join(f'out_data{i}' for i in range(n))
    index = 'bodo.utils.conversion.convert_to_index(new_index)'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    check_runtime_cols_unsupported(df, 'DataFrame.set_index()')
    vabyk__txgl = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    oci__mue = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', vabyk__txgl, oci__mue,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    columns = tuple(bjo__ykb for bjo__ykb in df.columns if bjo__ykb != col_name
        )
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    vabyk__txgl = {'inplace': inplace}
    oci__mue = {'inplace': False}
    check_unsupported_args('query', vabyk__txgl, oci__mue, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        bcbyn__osqh = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[bcbyn__osqh]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    vabyk__txgl = {'subset': subset, 'keep': keep}
    oci__mue = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', vabyk__txgl, oci__mue,
        package_name='pandas', module_name='DataFrame')
    ona__salxe = len(df.columns)
    zuwt__foby = "def impl(df, subset=None, keep='first'):\n"
    for i in range(ona__salxe):
        zuwt__foby += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    nfjvb__eiu = ', '.join(f'data_{i}' for i in range(ona__salxe))
    nfjvb__eiu += ',' if ona__salxe == 1 else ''
    zuwt__foby += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({nfjvb__eiu}))\n')
    zuwt__foby += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    zuwt__foby += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo}, lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    vabyk__txgl = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    oci__mue = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    jtb__mrdo = []
    if is_overload_constant_list(subset):
        jtb__mrdo = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        jtb__mrdo = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        jtb__mrdo = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    fcn__tjw = []
    for col_name in jtb__mrdo:
        if col_name not in df.columns:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        fcn__tjw.append(df.columns.index(col_name))
    check_unsupported_args('DataFrame.drop_duplicates', vabyk__txgl,
        oci__mue, package_name='pandas', module_name='DataFrame')
    rxop__cmgnx = []
    if fcn__tjw:
        for jruho__dquto in fcn__tjw:
            if isinstance(df.data[jruho__dquto], bodo.MapArrayType):
                rxop__cmgnx.append(df.columns[jruho__dquto])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                rxop__cmgnx.append(col_name)
    if rxop__cmgnx:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {rxop__cmgnx} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    ona__salxe = len(df.columns)
    arzw__pdb = ['data_{}'.format(i) for i in fcn__tjw]
    wlty__azvp = ['data_{}'.format(i) for i in range(ona__salxe) if i not in
        fcn__tjw]
    if arzw__pdb:
        ebwkw__qrmo = len(arzw__pdb)
    else:
        ebwkw__qrmo = ona__salxe
    sbfpt__cadj = ', '.join(arzw__pdb + wlty__azvp)
    data_args = ', '.join('data_{}'.format(i) for i in range(ona__salxe))
    zuwt__foby = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(ona__salxe):
        zuwt__foby += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    zuwt__foby += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(sbfpt__cadj, index, ebwkw__qrmo))
    zuwt__foby += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(zuwt__foby, df.columns, data_args, 'index')


def create_dataframe_mask_where_overload(func_name):

    def overload_dataframe_mask_where(df, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
            f'DataFrame.{func_name}()')
        _validate_arguments_mask_where(f'DataFrame.{func_name}', df, cond,
            other, inplace, axis, level, errors, try_cast)
        header = """def impl(df, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False):
"""
        if func_name == 'mask':
            header += '  cond = ~cond\n'
        gen_all_false = [False]
        if cond.ndim == 1:
            cond_str = lambda i, _: 'cond'
        elif cond.ndim == 2:
            if isinstance(cond, DataFrameType):
                vcjs__eknsd = {bjo__ykb: i for i, bjo__ykb in enumerate(
                    cond.columns)}

                def cond_str(i, gen_all_false):
                    if df.columns[i] in vcjs__eknsd:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {vcjs__eknsd[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            hkgt__kxhfv = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                other_map = {bjo__ykb: i for i, bjo__ykb in enumerate(other
                    .columns)}
                hkgt__kxhfv = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other_map[df.columns[i]]})'
                     if df.columns[i] in other_map else 'None')
            elif isinstance(other, types.Array):
                hkgt__kxhfv = lambda i: f'other[:,{i}]'
        ona__salxe = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {hkgt__kxhfv(i)})'
             for i in range(ona__salxe))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        lox__ikc = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(lox__ikc)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    vtgbb__kpod = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    linof__dtsm = dict(inplace=False, level=None, errors='raise', try_cast=
        False)
    check_unsupported_args(f'{func_name}', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        (cond.ndim == 1 or cond.ndim == 2) and cond.dtype == types.bool_
        ) and not (isinstance(cond, DataFrameType) and cond.ndim == 2 and
        all(cond.data[i].dtype == types.bool_ for i in range(len(df.columns)))
        ):
        raise BodoError(
            f"{func_name}(): 'cond' argument must be a DataFrame, Series, 1- or 2-dimensional array of booleans"
            )
    ona__salxe = len(df.columns)
    if hasattr(other, 'ndim') and (other.ndim != 1 or other.ndim != 2):
        if other.ndim == 2:
            if not isinstance(other, (DataFrameType, types.Array)):
                raise BodoError(
                    f"{func_name}(): 'other', if 2-dimensional, must be a DataFrame or array."
                    )
        elif other.ndim != 1:
            raise BodoError(
                f"{func_name}(): 'other' must be either 1 or 2-dimensional")
    if isinstance(other, DataFrameType):
        other_map = {bjo__ykb: i for i, bjo__ykb in enumerate(other.columns)}
        for i in range(ona__salxe):
            if df.columns[i] in other_map:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other_map[df.columns[i]]]
                    )
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(ona__salxe):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(ona__salxe):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other, max_ndim=2)


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None,
    out_df_type=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    if out_df_type is not None:
        extra_globals['out_df_type'] = out_df_type
        ubt__kvl = 'out_df_type'
    else:
        ubt__kvl = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    zuwt__foby = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {ubt__kvl})
"""
    lrc__hdl = {}
    irh__lvqyg = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    irh__lvqyg.update(extra_globals)
    exec(zuwt__foby, irh__lvqyg, lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        eft__wlt = pd.Index(lhs.columns)
        mgm__mkksy = pd.Index(rhs.columns)
        ftyid__pca, ysm__bqej, qyz__qqh = eft__wlt.join(mgm__mkksy, how=
            'left' if is_inplace else 'outer', level=None, return_indexers=True
            )
        return tuple(ftyid__pca), ysm__bqej, qyz__qqh
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        ggogc__spg = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        dvyf__lwt = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, ggogc__spg)
        check_runtime_cols_unsupported(rhs, ggogc__spg)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                ftyid__pca, ysm__bqej, qyz__qqh = _get_binop_columns(lhs, rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {ipe__bbevw}) {ggogc__spg}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {owm__cbwiv})'
                     if ipe__bbevw != -1 and owm__cbwiv != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for ipe__bbevw, owm__cbwiv in zip(ysm__bqej, qyz__qqh))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, ftyid__pca, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            jjyv__syqm = []
            xxswr__wcvts = []
            if op in dvyf__lwt:
                for i, hkd__xpqhq in enumerate(lhs.data):
                    if is_common_scalar_dtype([hkd__xpqhq.dtype, rhs]):
                        jjyv__syqm.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {ggogc__spg} rhs'
                            )
                    else:
                        hsy__dfon = f'arr{i}'
                        xxswr__wcvts.append(hsy__dfon)
                        jjyv__syqm.append(hsy__dfon)
                data_args = ', '.join(jjyv__syqm)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {ggogc__spg} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(xxswr__wcvts) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {hsy__dfon} = np.empty(n, dtype=np.bool_)\n' for
                    hsy__dfon in xxswr__wcvts)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(hsy__dfon, op ==
                    operator.ne) for hsy__dfon in xxswr__wcvts)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            jjyv__syqm = []
            xxswr__wcvts = []
            if op in dvyf__lwt:
                for i, hkd__xpqhq in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, hkd__xpqhq.dtype]):
                        jjyv__syqm.append(
                            f'lhs {ggogc__spg} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        hsy__dfon = f'arr{i}'
                        xxswr__wcvts.append(hsy__dfon)
                        jjyv__syqm.append(hsy__dfon)
                data_args = ', '.join(jjyv__syqm)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, ggogc__spg) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(xxswr__wcvts) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(hsy__dfon) for hsy__dfon in xxswr__wcvts)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(hsy__dfon, op ==
                    operator.ne) for hsy__dfon in xxswr__wcvts)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        lox__ikc = create_binary_op_overload(op)
        overload(op)(lox__ikc)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        ggogc__spg = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, ggogc__spg)
        check_runtime_cols_unsupported(right, ggogc__spg)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                ftyid__pca, _, qyz__qqh = _get_binop_columns(left, right, True)
                zuwt__foby = 'def impl(left, right):\n'
                for i, owm__cbwiv in enumerate(qyz__qqh):
                    if owm__cbwiv == -1:
                        zuwt__foby += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    zuwt__foby += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    zuwt__foby += f"""  df_arr{i} {ggogc__spg} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {owm__cbwiv})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    ftyid__pca)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(zuwt__foby, ftyid__pca, data_args,
                    index, extra_globals={'float64_arr_type': types.Array(
                    types.float64, 1, 'C')})
            zuwt__foby = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                zuwt__foby += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                zuwt__foby += '  df_arr{0} {1} right\n'.format(i, ggogc__spg)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(zuwt__foby, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        lox__ikc = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(lox__ikc)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            ggogc__spg = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, ggogc__spg)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, ggogc__spg) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        lox__ikc = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(lox__ikc)


_install_unary_ops()


def overload_isna(obj):
    check_runtime_cols_unsupported(obj, 'pd.isna()')
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            lrix__ywoic = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                lrix__ywoic[i] = bodo.libs.array_kernels.isna(obj, i)
            return lrix__ywoic
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            lrix__ywoic = np.empty(n, np.bool_)
            for i in range(n):
                lrix__ywoic[i] = pd.isna(obj[i])
            return lrix__ywoic
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if isinstance(obj, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    check_runtime_cols_unsupported(obj, 'pd.notna()')
    if isinstance(obj, (DataFrameType, SeriesType)):
        return lambda obj: obj.notna()
    if isinstance(obj, (types.List, types.UniTuple)) or is_array_typ(obj,
        include_index_series=True):
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    check_runtime_cols_unsupported(df, 'DataFrame.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.replace()')
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    vabyk__txgl = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    oci__mue = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', vabyk__txgl, oci__mue, package_name=
        'pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    rzw__kwsdv = str(expr_node)
    return rzw__kwsdv.startswith('left.') or rzw__kwsdv.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    jzu__lyb = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (jzu__lyb,))
    vmw__ofn = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        xfnlf__dxecw = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        hmtua__yubdx = {('NOT_NA', vmw__ofn(hkd__xpqhq)): hkd__xpqhq for
            hkd__xpqhq in null_set}
        jqt__szua, _, _ = _parse_query_expr(xfnlf__dxecw, env, [], [], None,
            join_cleaned_cols=hmtua__yubdx)
        tszbr__gnr = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            nwl__thomt = pd.core.computation.ops.BinOp('&', jqt__szua,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = tszbr__gnr
        return nwl__thomt

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                okdbt__pnlez = set()
                wvwu__kymvq = set()
                tat__dhxen = _insert_NA_cond_body(expr_node.lhs, okdbt__pnlez)
                bmpuh__jeo = _insert_NA_cond_body(expr_node.rhs, wvwu__kymvq)
                rrco__dpxcz = okdbt__pnlez.intersection(wvwu__kymvq)
                okdbt__pnlez.difference_update(rrco__dpxcz)
                wvwu__kymvq.difference_update(rrco__dpxcz)
                null_set.update(rrco__dpxcz)
                expr_node.lhs = append_null_checks(tat__dhxen, okdbt__pnlez)
                expr_node.rhs = append_null_checks(bmpuh__jeo, wvwu__kymvq)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            zle__ppzab = expr_node.name
            wkvm__zqhob, col_name = zle__ppzab.split('.')
            if wkvm__zqhob == 'left':
                vihz__gli = left_columns
                data = left_data
            else:
                vihz__gli = right_columns
                data = right_data
            gxod__pexlu = data[vihz__gli.index(col_name)]
            if bodo.utils.typing.is_nullable(gxod__pexlu):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    bqic__mmx = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        qic__szciy = str(expr_node.lhs)
        csxe__ltk = str(expr_node.rhs)
        if qic__szciy.startswith('left.') and csxe__ltk.startswith('left.'
            ) or qic__szciy.startswith('right.') and csxe__ltk.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [qic__szciy.split('.')[1]]
        right_on = [csxe__ltk.split('.')[1]]
        if qic__szciy.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        tdkc__hvmp, yfgvm__bqjx, mov__svfu = _extract_equal_conds(expr_node.lhs
            )
        nrelw__kzeco, nlt__btmbm, aqx__elq = _extract_equal_conds(expr_node.rhs
            )
        left_on = tdkc__hvmp + nrelw__kzeco
        right_on = yfgvm__bqjx + nlt__btmbm
        if mov__svfu is None:
            return left_on, right_on, aqx__elq
        if aqx__elq is None:
            return left_on, right_on, mov__svfu
        expr_node.lhs = mov__svfu
        expr_node.rhs = aqx__elq
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    jzu__lyb = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (jzu__lyb,))
    qmfyt__qsh = dict()
    vmw__ofn = pd.core.computation.parsing.clean_column_name
    for name, xchrg__lgk in (('left', left_columns), ('right', right_columns)):
        for hkd__xpqhq in xchrg__lgk:
            qhgcm__ondh = vmw__ofn(hkd__xpqhq)
            fkjx__wzufb = name, qhgcm__ondh
            if fkjx__wzufb in qmfyt__qsh:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{hkd__xpqhq}' and '{qmfyt__qsh[qhgcm__ondh]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            qmfyt__qsh[fkjx__wzufb] = hkd__xpqhq
    tdr__kmg, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=qmfyt__qsh)
    left_on, right_on, ijih__keaf = _extract_equal_conds(tdr__kmg.terms)
    return left_on, right_on, _insert_NA_cond(ijih__keaf, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    vtgbb__kpod = dict(sort=sort, copy=copy, validate=validate)
    linof__dtsm = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    vdb__qnd = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    ftm__cyr = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in vdb__qnd and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, pbj__gezw = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if pbj__gezw is None:
                    ftm__cyr = ''
                else:
                    ftm__cyr = str(pbj__gezw)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = vdb__qnd
        right_keys = vdb__qnd
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    if (not left_on or not right_on) and not is_overload_none(on):
        raise BodoError(
            f"DataFrame.merge(): Merge condition '{get_overload_const_str(on)}' requires a cross join to implement, but cross join is not supported."
            )
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    tbqnh__tul = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        ipqvk__qxjuz = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        ipqvk__qxjuz = list(get_overload_const_list(suffixes))
    suffix_x = ipqvk__qxjuz[0]
    suffix_y = ipqvk__qxjuz[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    zuwt__foby = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    zuwt__foby += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    zuwt__foby += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    zuwt__foby += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, tbqnh__tul, ftm__cyr))
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo}, lrc__hdl)
    _impl = lrc__hdl['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    valid_dataframe_column_types = (ArrayItemArrayType, MapArrayType,
        StructArrayType, CategoricalArrayType, types.Array,
        IntegerArrayType, DecimalArrayType, IntervalArrayType, bodo.
        DatetimeArrayType)
    bvq__vgdps = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    dhfdi__diuyx = {get_overload_const_str(viqe__qee) for viqe__qee in (
        left_on, right_on, on) if is_overload_constant_str(viqe__qee)}
    for df in (left, right):
        for i, hkd__xpqhq in enumerate(df.data):
            if not isinstance(hkd__xpqhq, valid_dataframe_column_types
                ) and hkd__xpqhq not in bvq__vgdps:
                raise BodoError(
                    f'{name_func}(): use of column with {type(hkd__xpqhq)} in merge unsupported'
                    )
            if df.columns[i] in dhfdi__diuyx and isinstance(hkd__xpqhq,
                MapArrayType):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        ipqvk__qxjuz = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        ipqvk__qxjuz = list(get_overload_const_list(suffixes))
    if len(ipqvk__qxjuz) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    vdb__qnd = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        uksxc__etiri = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            uksxc__etiri = on_str not in vdb__qnd and ('left.' in on_str or
                'right.' in on_str)
        if len(vdb__qnd) == 0 and not uksxc__etiri:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    wcv__dpmh = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            pqitg__rgi = left.index
            apdon__rgiv = isinstance(pqitg__rgi, StringIndexType)
            umo__kby = right.index
            rrc__tamf = isinstance(umo__kby, StringIndexType)
        elif is_overload_true(left_index):
            pqitg__rgi = left.index
            apdon__rgiv = isinstance(pqitg__rgi, StringIndexType)
            umo__kby = right.data[right.columns.index(right_keys[0])]
            rrc__tamf = umo__kby.dtype == string_type
        elif is_overload_true(right_index):
            pqitg__rgi = left.data[left.columns.index(left_keys[0])]
            apdon__rgiv = pqitg__rgi.dtype == string_type
            umo__kby = right.index
            rrc__tamf = isinstance(umo__kby, StringIndexType)
        if apdon__rgiv and rrc__tamf:
            return
        pqitg__rgi = pqitg__rgi.dtype
        umo__kby = umo__kby.dtype
        try:
            qgqfc__kykp = wcv__dpmh.resolve_function_type(operator.eq, (
                pqitg__rgi, umo__kby), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=pqitg__rgi, rk_dtype=umo__kby))
    else:
        for lemas__exlz, lwwq__beur in zip(left_keys, right_keys):
            pqitg__rgi = left.data[left.columns.index(lemas__exlz)].dtype
            taeu__hvtkh = left.data[left.columns.index(lemas__exlz)]
            umo__kby = right.data[right.columns.index(lwwq__beur)].dtype
            jcb__lzb = right.data[right.columns.index(lwwq__beur)]
            if taeu__hvtkh == jcb__lzb:
                continue
            vfj__xst = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=lemas__exlz, lk_dtype=pqitg__rgi, rk=lwwq__beur,
                rk_dtype=umo__kby))
            cxu__jpiz = pqitg__rgi == string_type
            arkro__giwu = umo__kby == string_type
            if cxu__jpiz ^ arkro__giwu:
                raise_bodo_error(vfj__xst)
            try:
                qgqfc__kykp = wcv__dpmh.resolve_function_type(operator.eq,
                    (pqitg__rgi, umo__kby), {})
            except:
                raise_bodo_error(vfj__xst)


def validate_keys(keys, df):
    dyo__lgoy = set(keys).difference(set(df.columns))
    if len(dyo__lgoy) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in dyo__lgoy:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {dyo__lgoy} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    vtgbb__kpod = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    linof__dtsm = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    zuwt__foby = "def _impl(left, other, on=None, how='left',\n"
    zuwt__foby += "    lsuffix='', rsuffix='', sort=False):\n"
    zuwt__foby += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo}, lrc__hdl)
    _impl = lrc__hdl['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        wzrx__rnjr = get_overload_const_list(on)
        validate_keys(wzrx__rnjr, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    vdb__qnd = tuple(set(left.columns) & set(other.columns))
    if len(vdb__qnd) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=vdb__qnd))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    osiow__nzgni = set(left_keys) & set(right_keys)
    qlr__nqos = set(left_columns) & set(right_columns)
    ygyoh__ihvmb = qlr__nqos - osiow__nzgni
    wko__nafv = set(left_columns) - qlr__nqos
    aueqn__sunx = set(right_columns) - qlr__nqos
    scye__xab = {}

    def insertOutColumn(col_name):
        if col_name in scye__xab:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        scye__xab[col_name] = 0
    for pkjw__qvagq in osiow__nzgni:
        insertOutColumn(pkjw__qvagq)
    for pkjw__qvagq in ygyoh__ihvmb:
        gnko__bhn = str(pkjw__qvagq) + suffix_x
        jev__dnpy = str(pkjw__qvagq) + suffix_y
        insertOutColumn(gnko__bhn)
        insertOutColumn(jev__dnpy)
    for pkjw__qvagq in wko__nafv:
        insertOutColumn(pkjw__qvagq)
    for pkjw__qvagq in aueqn__sunx:
        insertOutColumn(pkjw__qvagq)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    vdb__qnd = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = vdb__qnd
        right_keys = vdb__qnd
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        ipqvk__qxjuz = suffixes
    if is_overload_constant_list(suffixes):
        ipqvk__qxjuz = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        ipqvk__qxjuz = suffixes.value
    suffix_x = ipqvk__qxjuz[0]
    suffix_y = ipqvk__qxjuz[1]
    zuwt__foby = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    zuwt__foby += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    zuwt__foby += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    zuwt__foby += "    allow_exact_matches=True, direction='backward'):\n"
    zuwt__foby += '  suffix_x = suffixes[0]\n'
    zuwt__foby += '  suffix_y = suffixes[1]\n'
    zuwt__foby += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo}, lrc__hdl)
    _impl = lrc__hdl['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True):
    check_runtime_cols_unsupported(df, 'DataFrame.groupby()')
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_bodo_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_bodo_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_bodo_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_bodo_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    vtgbb__kpod = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    tvjza__nsvsb = dict(sort=False, group_keys=True, squeeze=False,
        observed=True)
    check_unsupported_args('Dataframe.groupby', vtgbb__kpod, tvjza__nsvsb,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    ommko__tip = func_name == 'DataFrame.pivot_table'
    if ommko__tip:
        if is_overload_none(index) or not is_literal_type(index):
            raise_bodo_error(
                f"DataFrame.pivot_table(): 'index' argument is required and must be constant column labels"
                )
    elif not is_overload_none(index) and not is_literal_type(index):
        raise_bodo_error(
            f"{func_name}(): if 'index' argument is provided it must be constant column labels"
            )
    if is_overload_none(columns) or not is_literal_type(columns):
        raise_bodo_error(
            f"{func_name}(): 'columns' argument is required and must be a constant column label"
            )
    if not is_overload_none(values) and not is_literal_type(values):
        raise_bodo_error(
            f"{func_name}(): if 'values' argument is provided it must be constant column labels"
            )
    bnqa__pypm = get_literal_value(columns)
    if isinstance(bnqa__pypm, (list, tuple)):
        if len(bnqa__pypm) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {bnqa__pypm}"
                )
        bnqa__pypm = bnqa__pypm[0]
    if bnqa__pypm not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {bnqa__pypm} not found in DataFrame {df}."
            )
    ikivi__ikfz = {bjo__ykb: i for i, bjo__ykb in enumerate(df.columns)}
    evs__gllg = ikivi__ikfz[bnqa__pypm]
    if is_overload_none(index):
        qpiw__hrfm = []
        zabz__updzj = []
    else:
        zabz__updzj = get_literal_value(index)
        if not isinstance(zabz__updzj, (list, tuple)):
            zabz__updzj = [zabz__updzj]
        qpiw__hrfm = []
        for index in zabz__updzj:
            if index not in ikivi__ikfz:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            qpiw__hrfm.append(ikivi__ikfz[index])
    if not (all(isinstance(bjo__ykb, int) for bjo__ykb in zabz__updzj) or
        all(isinstance(bjo__ykb, str) for bjo__ykb in zabz__updzj)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        tip__lkgw = []
        oopq__qvd = []
        uim__tjl = qpiw__hrfm + [evs__gllg]
        for i, bjo__ykb in enumerate(df.columns):
            if i not in uim__tjl:
                tip__lkgw.append(i)
                oopq__qvd.append(bjo__ykb)
    else:
        oopq__qvd = get_literal_value(values)
        if not isinstance(oopq__qvd, (list, tuple)):
            oopq__qvd = [oopq__qvd]
        tip__lkgw = []
        for val in oopq__qvd:
            if val not in ikivi__ikfz:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            tip__lkgw.append(ikivi__ikfz[val])
    if all(isinstance(bjo__ykb, int) for bjo__ykb in oopq__qvd):
        oopq__qvd = np.array(oopq__qvd, 'int64')
    elif all(isinstance(bjo__ykb, str) for bjo__ykb in oopq__qvd):
        oopq__qvd = pd.array(oopq__qvd, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    ytvpm__szgdl = set(tip__lkgw) | set(qpiw__hrfm) | {evs__gllg}
    if len(ytvpm__szgdl) != len(tip__lkgw) + len(qpiw__hrfm) + 1:
        raise BodoError(
            f"{func_name}(): 'index', 'columns', and 'values' must all refer to different columns"
            )

    def check_valid_index_typ(index_column):
        if isinstance(index_column, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType, bodo.
            IntervalArrayType)):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column must have scalar rows"
                )
        if isinstance(index_column, bodo.CategoricalArrayType):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column does not support categorical data"
                )
    if len(qpiw__hrfm) == 0:
        index = df.index
        if isinstance(index, MultiIndexType):
            raise BodoError(
                f"{func_name}(): 'index' cannot be None with a DataFrame with a multi-index"
                )
        if not isinstance(index, RangeIndexType):
            check_valid_index_typ(index.data)
        if not is_literal_type(df.index.name_typ):
            raise BodoError(
                f"{func_name}(): If 'index' is None, the name of the DataFrame's Index must be constant at compile-time"
                )
    else:
        for qxo__nsjx in qpiw__hrfm:
            index_column = df.data[qxo__nsjx]
            check_valid_index_typ(index_column)
    eppy__llale = df.data[evs__gllg]
    if isinstance(eppy__llale, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(eppy__llale, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for xtg__aehs in tip__lkgw:
        mwxfj__fxyz = df.data[xtg__aehs]
        if isinstance(mwxfj__fxyz, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or mwxfj__fxyz == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return zabz__updzj, bnqa__pypm, oopq__qvd, qpiw__hrfm, evs__gllg, tip__lkgw


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    zabz__updzj, bnqa__pypm, oopq__qvd, qxo__nsjx, evs__gllg, wjp__eydp = (
        pivot_error_checking(data, index, columns, values, 'DataFrame.pivot'))
    if len(zabz__updzj) == 0:
        if is_overload_none(data.index.name_typ):
            zabz__updzj = [None]
        else:
            zabz__updzj = [get_literal_value(data.index.name_typ)]
    if len(oopq__qvd) == 1:
        pphdu__bedud = None
    else:
        pphdu__bedud = oopq__qvd
    zuwt__foby = 'def impl(data, index=None, columns=None, values=None):\n'
    zuwt__foby += f'    pivot_values = data.iloc[:, {evs__gllg}].unique()\n'
    zuwt__foby += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(qxo__nsjx) == 0:
        zuwt__foby += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        zuwt__foby += '        (\n'
        for abouh__fljt in qxo__nsjx:
            zuwt__foby += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {abouh__fljt}),
"""
        zuwt__foby += '        ),\n'
    zuwt__foby += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {evs__gllg}),),
"""
    zuwt__foby += '        (\n'
    for xtg__aehs in wjp__eydp:
        zuwt__foby += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {xtg__aehs}),
"""
    zuwt__foby += '        ),\n'
    zuwt__foby += '        pivot_values,\n'
    zuwt__foby += '        index_lit_tup,\n'
    zuwt__foby += '        columns_lit,\n'
    zuwt__foby += '        values_name_const,\n'
    zuwt__foby += '    )\n'
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo, 'index_lit_tup': tuple(zabz__updzj),
        'columns_lit': bnqa__pypm, 'values_name_const': pphdu__bedud}, lrc__hdl
        )
    impl = lrc__hdl['impl']
    return impl


@overload(pd.pivot_table, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(data, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=False, sort=True, _pivot_values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot_table()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot_table()')
    vtgbb__kpod = dict(fill_value=fill_value, margins=margins, dropna=
        dropna, margins_name=margins_name, observed=observed, sort=sort)
    linof__dtsm = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', vtgbb__kpod,
        linof__dtsm, package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (zabz__updzj, bnqa__pypm, oopq__qvd, qxo__nsjx, evs__gllg, wjp__eydp
            ) = (pivot_error_checking(data, index, columns, values,
            'DataFrame.pivot_table'))
        if len(oopq__qvd) == 1:
            pphdu__bedud = None
        else:
            pphdu__bedud = oopq__qvd
        zuwt__foby = 'def impl(\n'
        zuwt__foby += '    data,\n'
        zuwt__foby += '    values=None,\n'
        zuwt__foby += '    index=None,\n'
        zuwt__foby += '    columns=None,\n'
        zuwt__foby += '    aggfunc="mean",\n'
        zuwt__foby += '    fill_value=None,\n'
        zuwt__foby += '    margins=False,\n'
        zuwt__foby += '    dropna=True,\n'
        zuwt__foby += '    margins_name="All",\n'
        zuwt__foby += '    observed=False,\n'
        zuwt__foby += '    sort=True,\n'
        zuwt__foby += '    _pivot_values=None,\n'
        zuwt__foby += '):\n'
        uan__mgscc = qxo__nsjx + [evs__gllg] + wjp__eydp
        zuwt__foby += f'    data = data.iloc[:, {uan__mgscc}]\n'
        tzy__rtr = zabz__updzj + [bnqa__pypm]
        zuwt__foby += (
            f'    data = data.groupby({tzy__rtr!r}, as_index=False).agg(aggfunc)\n'
            )
        zuwt__foby += (
            f'    pivot_values = data.iloc[:, {len(qxo__nsjx)}].unique()\n')
        zuwt__foby += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
        zuwt__foby += '        (\n'
        for i in range(0, len(qxo__nsjx)):
            zuwt__foby += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        zuwt__foby += '        ),\n'
        zuwt__foby += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(qxo__nsjx)}),),
"""
        zuwt__foby += '        (\n'
        for i in range(len(qxo__nsjx) + 1, len(wjp__eydp) + len(qxo__nsjx) + 1
            ):
            zuwt__foby += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        zuwt__foby += '        ),\n'
        zuwt__foby += '        pivot_values,\n'
        zuwt__foby += '        index_lit_tup,\n'
        zuwt__foby += '        columns_lit,\n'
        zuwt__foby += '        values_name_const,\n'
        zuwt__foby += '        check_duplicates=False,\n'
        zuwt__foby += '    )\n'
        lrc__hdl = {}
        exec(zuwt__foby, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(zabz__updzj), 'columns_lit': bnqa__pypm,
            'values_name_const': pphdu__bedud}, lrc__hdl)
        impl = lrc__hdl['impl']
        return impl
    if aggfunc == 'mean':

        def _impl(data, values=None, index=None, columns=None, aggfunc=
            'mean', fill_value=None, margins=False, dropna=True,
            margins_name='All', observed=False, sort=True, _pivot_values=None):
            return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(data,
                values, index, columns, 'mean', _pivot_values)
        return _impl

    def _impl(data, values=None, index=None, columns=None, aggfunc='mean',
        fill_value=None, margins=False, dropna=True, margins_name='All',
        observed=False, sort=True, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(data, values,
            index, columns, aggfunc, _pivot_values)
    return _impl


@overload(pd.melt, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'melt', inline='always', no_unliteral=True)
def overload_dataframe_melt(frame, id_vars=None, value_vars=None, var_name=
    None, value_name='value', col_level=None, ignore_index=True):
    vtgbb__kpod = dict(var_name=var_name, value_name=value_name, col_level=
        col_level, ignore_index=ignore_index)
    linof__dtsm = dict(var_name=None, value_name='value', col_level=None,
        ignore_index=True)
    check_unsupported_args('DataFrame.melt', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise BodoError(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise BodoError(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal")
    rmwnf__umdjx = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(rmwnf__umdjx, (list, tuple)):
        rmwnf__umdjx = [rmwnf__umdjx]
    for bjo__ykb in rmwnf__umdjx:
        if bjo__ykb not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {bjo__ykb} not found in {frame}"
                )
    qmfyt__qsh = {bjo__ykb: i for i, bjo__ykb in enumerate(frame.columns)}
    ozt__xtali = [qmfyt__qsh[i] for i in rmwnf__umdjx]
    if is_overload_none(value_vars):
        ndn__fyy = []
        okk__vcn = []
        for i, bjo__ykb in enumerate(frame.columns):
            if i not in ozt__xtali:
                ndn__fyy.append(i)
                okk__vcn.append(bjo__ykb)
    else:
        okk__vcn = get_literal_value(value_vars)
        if not isinstance(okk__vcn, (list, tuple)):
            okk__vcn = [okk__vcn]
        okk__vcn = [v for v in okk__vcn if v not in rmwnf__umdjx]
        if not okk__vcn:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        ndn__fyy = []
        for val in okk__vcn:
            if val not in qmfyt__qsh:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            ndn__fyy.append(qmfyt__qsh[val])
    for bjo__ykb in okk__vcn:
        if bjo__ykb not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {bjo__ykb} not found in {frame}"
                )
    if not (all(isinstance(bjo__ykb, int) for bjo__ykb in okk__vcn) or all(
        isinstance(bjo__ykb, str) for bjo__ykb in okk__vcn)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    evqgp__vqds = frame.data[ndn__fyy[0]]
    urxp__dwrgq = [frame.data[i].dtype for i in ndn__fyy]
    ndn__fyy = np.array(ndn__fyy, dtype=np.int64)
    ozt__xtali = np.array(ozt__xtali, dtype=np.int64)
    _, gqcp__its = bodo.utils.typing.get_common_scalar_dtype(urxp__dwrgq)
    if not gqcp__its:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': okk__vcn, 'val_type': evqgp__vqds}
    header = 'def impl(\n'
    header += '  frame,\n'
    header += '  id_vars=None,\n'
    header += '  value_vars=None,\n'
    header += '  var_name=None,\n'
    header += "  value_name='value',\n"
    header += '  col_level=None,\n'
    header += '  ignore_index=True,\n'
    header += '):\n'
    header += (
        '  dummy_id = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, 0)\n'
        )
    if frame.is_table_format and all(v == evqgp__vqds.dtype for v in
        urxp__dwrgq):
        extra_globals['value_idxs'] = ndn__fyy
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(okk__vcn) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {ndn__fyy[0]})
"""
    else:
        zgu__xdf = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in ndn__fyy)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({zgu__xdf},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in ozt__xtali:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(okk__vcn)})\n'
            )
    ukwbx__vmyty = ', '.join(f'out_id{i}' for i in ozt__xtali) + (', ' if 
        len(ozt__xtali) > 0 else '')
    data_args = ukwbx__vmyty + 'var_col, val_col'
    columns = tuple(rmwnf__umdjx + ['variable', 'value'])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(okk__vcn)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    vtgbb__kpod = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    linof__dtsm = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(index,
        'pandas.crosstab()')
    if not isinstance(index, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'index' argument only supported for Series types, found {index}"
            )
    if not isinstance(columns, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'columns' argument only supported for Series types, found {columns}"
            )

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_values()')
    vtgbb__kpod = dict(ignore_index=ignore_index, key=key)
    linof__dtsm = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', vtgbb__kpod,
        linof__dtsm, package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_bodo_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    ydx__hsh = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        ydx__hsh.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        xtbgx__jazf = [get_overload_const_tuple(by)]
    else:
        xtbgx__jazf = get_overload_const_list(by)
    xtbgx__jazf = set((k, '') if (k, '') in ydx__hsh else k for k in
        xtbgx__jazf)
    if len(xtbgx__jazf.difference(ydx__hsh)) > 0:
        vsp__ael = list(set(get_overload_const_list(by)).difference(ydx__hsh))
        raise_bodo_error(f'sort_values(): invalid keys {vsp__ael} for by.')
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        eufse__iel = get_overload_const_list(na_position)
        for na_position in eufse__iel:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_bodo_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_index()')
    vtgbb__kpod = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    linof__dtsm = dict(axis=0, level=None, kind='quicksort', sort_remaining
        =True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_bool(ascending):
        raise BodoError(
            "DataFrame.sort_index(): 'ascending' parameter must be of type bool"
            )
    if not is_overload_bool(inplace):
        raise BodoError(
            "DataFrame.sort_index(): 'inplace' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "DataFrame.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position)
    return _impl


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    vtgbb__kpod = dict(limit=limit, downcast=downcast)
    linof__dtsm = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    zuxk__csyex = not is_overload_none(value)
    kwsg__mdtb = not is_overload_none(method)
    if zuxk__csyex and kwsg__mdtb:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not zuxk__csyex and not kwsg__mdtb:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if zuxk__csyex:
        yqlfe__dygx = 'value=value'
    else:
        yqlfe__dygx = 'method=method'
    data_args = [(
        f"df['{bjo__ykb}'].fillna({yqlfe__dygx}, inplace=inplace)" if
        isinstance(bjo__ykb, str) else
        f'df[{bjo__ykb}].fillna({yqlfe__dygx}, inplace=inplace)') for
        bjo__ykb in df.columns]
    zuwt__foby = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        zuwt__foby += '  ' + '  \n'.join(data_args) + '\n'
        lrc__hdl = {}
        exec(zuwt__foby, {}, lrc__hdl)
        impl = lrc__hdl['impl']
        return impl
    else:
        return _gen_init_df(zuwt__foby, df.columns, ', '.join(ycm__nqpk +
            '.values' for ycm__nqpk in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    vtgbb__kpod = dict(col_level=col_level, col_fill=col_fill)
    linof__dtsm = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', vtgbb__kpod,
        linof__dtsm, package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    zuwt__foby = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    zuwt__foby += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        eeoc__bwu = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            eeoc__bwu)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            zuwt__foby += (
                '  m_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
                )
            bkrs__tnaja = ['m_index._data[{}]'.format(i) for i in range(df.
                index.nlevels)]
            data_args = bkrs__tnaja + data_args
        else:
            ebcro__uckc = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [ebcro__uckc] + data_args
    return _gen_init_df(zuwt__foby, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    qojz__bpwg = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and qojz__bpwg == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(qojz__bpwg))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.dropna()')
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        lauh__lafau = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        hmzdj__vpv = get_overload_const_list(subset)
        lauh__lafau = []
        for krrt__xshbx in hmzdj__vpv:
            if krrt__xshbx not in df.columns:
                raise_bodo_error(
                    f"df.dropna(): column '{krrt__xshbx}' not in data frame columns {df}"
                    )
            lauh__lafau.append(df.columns.index(krrt__xshbx))
    ona__salxe = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(ona__salxe))
    zuwt__foby = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(ona__salxe):
        zuwt__foby += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    zuwt__foby += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in lauh__lafau)))
    zuwt__foby += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(zuwt__foby, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    vtgbb__kpod = dict(index=index, level=level, errors=errors)
    linof__dtsm = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', vtgbb__kpod, linof__dtsm,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            ypd__axxd = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            ypd__axxd = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            ypd__axxd = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            ypd__axxd = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for bjo__ykb in ypd__axxd:
        if bjo__ykb not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(bjo__ykb, df.columns))
    if len(set(ypd__axxd)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    uow__tkb = tuple(bjo__ykb for bjo__ykb in df.columns if bjo__ykb not in
        ypd__axxd)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(bjo__ykb), '.copy()' if not inplace else ''
        ) for bjo__ykb in uow__tkb)
    zuwt__foby = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    zuwt__foby += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(zuwt__foby, uow__tkb, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    check_runtime_cols_unsupported(df, 'DataFrame.append()')
    check_runtime_cols_unsupported(other, 'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'DataFrame.append()')
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sample()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sample()')
    vtgbb__kpod = dict(random_state=random_state, weights=weights, axis=
        axis, ignore_index=ignore_index)
    rucix__muuac = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', vtgbb__kpod, rucix__muuac,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    ona__salxe = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(ona__salxe))
    deqw__cixmd = ', '.join('rhs_data_{}'.format(i) for i in range(ona__salxe))
    zuwt__foby = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    zuwt__foby += '  if (frac == 1 or n == len(df)) and not replace:\n'
    zuwt__foby += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(ona__salxe):
        zuwt__foby += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    zuwt__foby += '  if frac is None:\n'
    zuwt__foby += '    frac_d = -1.0\n'
    zuwt__foby += '  else:\n'
    zuwt__foby += '    frac_d = frac\n'
    zuwt__foby += '  if n is None:\n'
    zuwt__foby += '    n_i = 0\n'
    zuwt__foby += '  else:\n'
    zuwt__foby += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    zuwt__foby += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({deqw__cixmd},), {index}, n_i, frac_d, replace)
"""
    zuwt__foby += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(zuwt__foby, df.columns,
        data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {x}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    check_runtime_cols_unsupported(df, 'DataFrame.info()')
    vabyk__txgl = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    oci__mue = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', vabyk__txgl, oci__mue,
        package_name='pandas', module_name='DataFrame')
    vkim__ebvdf = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            tjyy__bfhj = vkim__ebvdf + '\n'
            tjyy__bfhj += 'Index: 0 entries\n'
            tjyy__bfhj += 'Empty DataFrame'
            print(tjyy__bfhj)
        return _info_impl
    else:
        zuwt__foby = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        zuwt__foby += '    ncols = df.shape[1]\n'
        zuwt__foby += f'    lines = "{vkim__ebvdf}\\n"\n'
        zuwt__foby += f'    lines += "{df.index}: "\n'
        zuwt__foby += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            zuwt__foby += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            zuwt__foby += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            zuwt__foby += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        zuwt__foby += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        zuwt__foby += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        zuwt__foby += '    column_width = max(space, 7)\n'
        zuwt__foby += '    column= "Column"\n'
        zuwt__foby += '    underl= "------"\n'
        zuwt__foby += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        zuwt__foby += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        zuwt__foby += '    mem_size = 0\n'
        zuwt__foby += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        zuwt__foby += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        zuwt__foby += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        uijtw__rwbe = dict()
        for i in range(len(df.columns)):
            zuwt__foby += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            anq__hab = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                anq__hab = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                mptvi__vfi = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                anq__hab = f'{mptvi__vfi[:-7]}'
            zuwt__foby += f'    col_dtype[{i}] = "{anq__hab}"\n'
            if anq__hab in uijtw__rwbe:
                uijtw__rwbe[anq__hab] += 1
            else:
                uijtw__rwbe[anq__hab] = 1
            zuwt__foby += f'    col_name[{i}] = "{df.columns[i]}"\n'
            zuwt__foby += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        zuwt__foby += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        zuwt__foby += '    for i in column_info:\n'
        zuwt__foby += "        lines += f'{i}\\n'\n"
        sltg__rgpgz = ', '.join(f'{k}({uijtw__rwbe[k]})' for k in sorted(
            uijtw__rwbe))
        zuwt__foby += f"    lines += 'dtypes: {sltg__rgpgz}\\n'\n"
        zuwt__foby += '    mem_size += df.index.nbytes\n'
        zuwt__foby += '    total_size = _sizeof_fmt(mem_size)\n'
        zuwt__foby += "    lines += f'memory usage: {total_size}'\n"
        zuwt__foby += '    print(lines)\n'
        lrc__hdl = {}
        exec(zuwt__foby, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, lrc__hdl)
        _info_impl = lrc__hdl['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    zuwt__foby = 'def impl(df, index=True, deep=False):\n'
    bulzz__hfg = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes')
    hrd__zwm = is_overload_true(index)
    columns = df.columns
    if hrd__zwm:
        columns = ('Index',) + columns
    if len(columns) == 0:
        qdmp__hexab = ()
    elif all(isinstance(bjo__ykb, int) for bjo__ykb in columns):
        qdmp__hexab = np.array(columns, 'int64')
    elif all(isinstance(bjo__ykb, str) for bjo__ykb in columns):
        qdmp__hexab = pd.array(columns, 'string')
    else:
        qdmp__hexab = columns
    if df.is_table_format:
        keyfm__mayzu = int(hrd__zwm)
        het__glnih = len(columns)
        zuwt__foby += f'  nbytes_arr = np.empty({het__glnih}, np.int64)\n'
        zuwt__foby += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        zuwt__foby += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {keyfm__mayzu})
"""
        if hrd__zwm:
            zuwt__foby += f'  nbytes_arr[0] = {bulzz__hfg}\n'
        zuwt__foby += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if hrd__zwm:
            data = f'{bulzz__hfg},{data}'
        else:
            uxpb__slsoj = ',' if len(columns) == 1 else ''
            data = f'{data}{uxpb__slsoj}'
        zuwt__foby += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        qdmp__hexab}, lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    dot__ujbc = 'read_excel_df{}'.format(next_label())
    setattr(types, dot__ujbc, df_type)
    vljw__kaoh = False
    if is_overload_constant_list(parse_dates):
        vljw__kaoh = get_overload_const_list(parse_dates)
    pog__bld = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    zuwt__foby = f"""
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{dot__ujbc}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{pog__bld}}},
            engine=engine,
            converters=converters,
            true_values=true_values,
            false_values=false_values,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            keep_default_na=keep_default_na,
            na_filter=na_filter,
            verbose=verbose,
            parse_dates={vljw__kaoh},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    lrc__hdl = {}
    exec(zuwt__foby, globals(), lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as dynxd__cuv:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    zuwt__foby = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    zuwt__foby += '    ylabel=None, title=None, legend=True, fontsize=None, \n'
    zuwt__foby += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        zuwt__foby += '   fig, ax = plt.subplots()\n'
    else:
        zuwt__foby += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        zuwt__foby += '   fig.set_figwidth(figsize[0])\n'
        zuwt__foby += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        zuwt__foby += '   xlabel = x\n'
    zuwt__foby += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        zuwt__foby += '   ylabel = y\n'
    else:
        zuwt__foby += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        zuwt__foby += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        zuwt__foby += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    zuwt__foby += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            zuwt__foby += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            otua__ode = get_overload_const_str(x)
            vkhv__skf = df.columns.index(otua__ode)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if vkhv__skf != i:
                        zuwt__foby += (
                            f'   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])\n'
                            )
        else:
            zuwt__foby += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        zuwt__foby += '   ax.scatter(df[x], df[y], s=20)\n'
        zuwt__foby += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        zuwt__foby += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        zuwt__foby += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        zuwt__foby += '   ax.legend()\n'
    zuwt__foby += '   return ax\n'
    lrc__hdl = {}
    exec(zuwt__foby, {'bodo': bodo, 'plt': plt}, lrc__hdl)
    impl = lrc__hdl['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for zpfzz__qei in df_typ.data:
        if not (isinstance(zpfzz__qei, IntegerArrayType) or isinstance(
            zpfzz__qei.dtype, types.Number) or zpfzz__qei.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns)):
            return False
    return True


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        qenmf__ilhn = args[0]
        yjx__ylcyi = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        mhj__qeqj = qenmf__ilhn
        check_runtime_cols_unsupported(qenmf__ilhn, 'set_df_col()')
        if isinstance(qenmf__ilhn, DataFrameType):
            index = qenmf__ilhn.index
            if len(qenmf__ilhn.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(qenmf__ilhn.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if yjx__ylcyi in qenmf__ilhn.columns:
                uow__tkb = qenmf__ilhn.columns
                uobi__zqcw = qenmf__ilhn.columns.index(yjx__ylcyi)
                vrxt__mjq = list(qenmf__ilhn.data)
                vrxt__mjq[uobi__zqcw] = val
                vrxt__mjq = tuple(vrxt__mjq)
            else:
                uow__tkb = qenmf__ilhn.columns + (yjx__ylcyi,)
                vrxt__mjq = qenmf__ilhn.data + (val,)
            mhj__qeqj = DataFrameType(vrxt__mjq, index, uow__tkb,
                qenmf__ilhn.dist, qenmf__ilhn.is_table_format)
        return mhj__qeqj(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    qsw__qrcl = {}

    def _rewrite_membership_op(self, node, left, right):
        nmrc__lhzxo = node.op
        op = self.visit(nmrc__lhzxo)
        return op, nmrc__lhzxo, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    xxlmh__hcak = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in xxlmh__hcak:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in xxlmh__hcak:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        vovx__nsq = node.attr
        value = node.value
        cjyjj__vgw = pd.core.computation.ops.LOCAL_TAG
        if vovx__nsq in ('str', 'dt'):
            try:
                cxhfr__mqti = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as tzkau__tkh:
                col_name = tzkau__tkh.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            cxhfr__mqti = str(self.visit(value))
        fkjx__wzufb = cxhfr__mqti, vovx__nsq
        if fkjx__wzufb in join_cleaned_cols:
            vovx__nsq = join_cleaned_cols[fkjx__wzufb]
        name = cxhfr__mqti + '.' + vovx__nsq
        if name.startswith(cjyjj__vgw):
            name = name[len(cjyjj__vgw):]
        if vovx__nsq in ('str', 'dt'):
            yidu__qvjk = columns[cleaned_columns.index(cxhfr__mqti)]
            qsw__qrcl[yidu__qvjk] = cxhfr__mqti
            self.env.scope[name] = 0
            return self.term_type(cjyjj__vgw + name, self.env)
        xxlmh__hcak.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in xxlmh__hcak:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        nahxx__kdt = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        yjx__ylcyi = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(nahxx__kdt), yjx__ylcyi))

    def op__str__(self):
        jwl__cdhv = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            whc__uwmgh)) for whc__uwmgh in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(jwl__cdhv)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(jwl__cdhv)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(jwl__cdhv))
    poypc__rfkv = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    vtbw__nvv = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    zrb__cmi = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    pae__jma = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    xyx__zfxao = pd.core.computation.ops.Term.__str__
    ixbs__gppm = pd.core.computation.ops.MathCall.__str__
    wur__drr = pd.core.computation.ops.Op.__str__
    tszbr__gnr = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        tdr__kmg = pd.core.computation.expr.Expr(expr, env=env)
        zejq__lflaa = str(tdr__kmg)
    except pd.core.computation.ops.UndefinedVariableError as tzkau__tkh:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == tzkau__tkh.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {tzkau__tkh}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            poypc__rfkv)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            vtbw__nvv)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = zrb__cmi
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = pae__jma
        pd.core.computation.ops.Term.__str__ = xyx__zfxao
        pd.core.computation.ops.MathCall.__str__ = ixbs__gppm
        pd.core.computation.ops.Op.__str__ = wur__drr
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            tszbr__gnr)
    byq__utg = pd.core.computation.parsing.clean_column_name
    qsw__qrcl.update({bjo__ykb: byq__utg(bjo__ykb) for bjo__ykb in columns if
        byq__utg(bjo__ykb) in tdr__kmg.names})
    return tdr__kmg, zejq__lflaa, qsw__qrcl


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        sic__vsxu = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(sic__vsxu))
        rtape__pyr = namedtuple('Pandas', col_names)
        hlawb__zmxkg = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], rtape__pyr)
        super(DataFrameTupleIterator, self).__init__(name, hlawb__zmxkg)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        zfw__fxvxk = [if_series_to_array_type(a) for a in args[len(args) // 2:]
            ]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        zfw__fxvxk = [types.Array(types.int64, 1, 'C')] + zfw__fxvxk
        uvxi__uouj = DataFrameTupleIterator(col_names, zfw__fxvxk)
        return uvxi__uouj(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mfmja__edzw = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            mfmja__edzw)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    zkw__cgkzc = args[len(args) // 2:]
    uwa__xniml = sig.args[len(sig.args) // 2:]
    tnr__tuiuw = context.make_helper(builder, sig.return_type)
    uedha__ezcqe = context.get_constant(types.intp, 0)
    hfo__pdcd = cgutils.alloca_once_value(builder, uedha__ezcqe)
    tnr__tuiuw.index = hfo__pdcd
    for i, arr in enumerate(zkw__cgkzc):
        setattr(tnr__tuiuw, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(zkw__cgkzc, uwa__xniml):
        context.nrt.incref(builder, arr_typ, arr)
    res = tnr__tuiuw._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    rphmk__rfzrt, = sig.args
    fwwzs__xsu, = args
    tnr__tuiuw = context.make_helper(builder, rphmk__rfzrt, value=fwwzs__xsu)
    fjlbf__byk = signature(types.intp, rphmk__rfzrt.array_types[1])
    ypaix__hzk = context.compile_internal(builder, lambda a: len(a),
        fjlbf__byk, [tnr__tuiuw.array0])
    index = builder.load(tnr__tuiuw.index)
    ozb__kqy = builder.icmp_signed('<', index, ypaix__hzk)
    result.set_valid(ozb__kqy)
    with builder.if_then(ozb__kqy):
        values = [index]
        for i, arr_typ in enumerate(rphmk__rfzrt.array_types[1:]):
            excj__fkosq = getattr(tnr__tuiuw, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                qhj__kmg = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    qhj__kmg, [excj__fkosq, index])
            else:
                qhj__kmg = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    qhj__kmg, [excj__fkosq, index])
            values.append(val)
        value = context.make_tuple(builder, rphmk__rfzrt.yield_type, values)
        result.yield_(value)
        qzx__pzuf = cgutils.increment_index(builder, index)
        builder.store(qzx__pzuf, tnr__tuiuw.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    wonj__rdoxa = ir.Assign(rhs, lhs, expr.loc)
    xsyj__nypfc = lhs
    ttw__vklt = []
    zqppy__hmg = []
    gay__glus = typ.count
    for i in range(gay__glus):
        xwfpz__cvhd = ir.Var(xsyj__nypfc.scope, mk_unique_var('{}_size{}'.
            format(xsyj__nypfc.name, i)), xsyj__nypfc.loc)
        siyhh__ldcmb = ir.Expr.static_getitem(lhs, i, None, xsyj__nypfc.loc)
        self.calltypes[siyhh__ldcmb] = None
        ttw__vklt.append(ir.Assign(siyhh__ldcmb, xwfpz__cvhd, xsyj__nypfc.loc))
        self._define(equiv_set, xwfpz__cvhd, types.intp, siyhh__ldcmb)
        zqppy__hmg.append(xwfpz__cvhd)
    zxr__arqc = tuple(zqppy__hmg)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        zxr__arqc, pre=[wonj__rdoxa] + ttw__vklt)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
