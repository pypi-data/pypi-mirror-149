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
        ougc__jzpny = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({ougc__jzpny})\n'
            )
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    zohr__oyejj = 'def impl(df):\n'
    if df.has_runtime_cols:
        zohr__oyejj += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        qblf__xeefi = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        zohr__oyejj += f'  return {qblf__xeefi}'
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo}, zqs__jguwt)
    impl = zqs__jguwt['impl']
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
    anz__psfkl = len(df.columns)
    vfoaf__nlu = set(i for i in range(anz__psfkl) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in vfoaf__nlu else '') for i in
        range(anz__psfkl))
    zohr__oyejj = 'def f(df):\n'.format()
    zohr__oyejj += '    return np.stack(({},), 1)\n'.format(data_args)
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo, 'np': np}, zqs__jguwt)
    ywyl__chmer = zqs__jguwt['f']
    return ywyl__chmer


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
    whnxa__eap = {'dtype': dtype, 'na_value': na_value}
    voo__xbwir = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', whnxa__eap, voo__xbwir,
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
            xrni__boan = bodo.hiframes.table.compute_num_runtime_columns(t)
            return xrni__boan * len(t)
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
            xrni__boan = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), xrni__boan
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    zohr__oyejj = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    dvn__rev = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    zohr__oyejj += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{dvn__rev}), {index}, None)
"""
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo}, zqs__jguwt)
    impl = zqs__jguwt['impl']
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
    whnxa__eap = {'copy': copy, 'errors': errors}
    voo__xbwir = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', whnxa__eap, voo__xbwir,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        dag__qfd = _bodo_object_typeref.instance_type
        assert isinstance(dag__qfd, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        igvb__jxx = {}
        for i, name in enumerate(dag__qfd.columns):
            arr_typ = dag__qfd.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                vzw__mmw = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                vzw__mmw = boolean_dtype
            else:
                vzw__mmw = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = vzw__mmw
            igvb__jxx[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {igvb__jxx[hyxb__uivvt]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if hyxb__uivvt in igvb__jxx else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, hyxb__uivvt in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        labl__pgc = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(labl__pgc[hyxb__uivvt])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if hyxb__uivvt in labl__pgc else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, hyxb__uivvt in enumerate(df.columns))
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
    huh__revy = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(deep):
            huh__revy.append(arr + '.copy()')
        elif is_overload_false(deep):
            huh__revy.append(arr)
        else:
            huh__revy.append(f'{arr}.copy() if deep else {arr}')
    header = 'def impl(df, deep=True):\n'
    return _gen_init_df(header, df.columns, ', '.join(huh__revy))


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    whnxa__eap = {'index': index, 'level': level, 'errors': errors}
    voo__xbwir = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', whnxa__eap, voo__xbwir,
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
        pyj__lqf = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        pyj__lqf = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    jbvx__mufyp = [pyj__lqf.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))]
    huh__revy = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(copy):
            huh__revy.append(arr + '.copy()')
        elif is_overload_false(copy):
            huh__revy.append(arr)
        else:
            huh__revy.append(f'{arr}.copy() if copy else {arr}')
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    return _gen_init_df(header, jbvx__mufyp, ', '.join(huh__revy))


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    fflni__hlhim = not is_overload_none(items)
    dsl__kwkbp = not is_overload_none(like)
    ooknq__sfyba = not is_overload_none(regex)
    jyf__kzm = fflni__hlhim ^ dsl__kwkbp ^ ooknq__sfyba
    dky__xhxsu = not (fflni__hlhim or dsl__kwkbp or ooknq__sfyba)
    if dky__xhxsu:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not jyf__kzm:
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
        sbab__ggcc = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        sbab__ggcc = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert sbab__ggcc in {0, 1}
    zohr__oyejj = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if sbab__ggcc == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if sbab__ggcc == 1:
        fgwd__onee = []
        etp__mjs = []
        tbwx__pkoge = []
        if fflni__hlhim:
            if is_overload_constant_list(items):
                eiz__qiyxp = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if dsl__kwkbp:
            if is_overload_constant_str(like):
                jpba__sro = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if ooknq__sfyba:
            if is_overload_constant_str(regex):
                kkr__xlz = get_overload_const_str(regex)
                nhotr__dhyn = re.compile(kkr__xlz)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, hyxb__uivvt in enumerate(df.columns):
            if not is_overload_none(items
                ) and hyxb__uivvt in eiz__qiyxp or not is_overload_none(like
                ) and jpba__sro in str(hyxb__uivvt) or not is_overload_none(
                regex) and nhotr__dhyn.search(str(hyxb__uivvt)):
                etp__mjs.append(hyxb__uivvt)
                tbwx__pkoge.append(i)
        for i in tbwx__pkoge:
            var_name = f'data_{i}'
            fgwd__onee.append(var_name)
            zohr__oyejj += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(fgwd__onee)
        return _gen_init_df(zohr__oyejj, etp__mjs, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        tdu__dcd = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([tdu__dcd] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': tdu__dcd}
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
    net__mot = is_overload_none(include)
    tdf__nugch = is_overload_none(exclude)
    vyo__liu = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if net__mot and tdf__nugch:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not net__mot:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            efacv__mtnck = [dtype_to_array_type(parse_dtype(elem, vyo__liu)
                ) for elem in include]
        elif is_legal_input(include):
            efacv__mtnck = [dtype_to_array_type(parse_dtype(include, vyo__liu))
                ]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        efacv__mtnck = get_nullable_and_non_nullable_types(efacv__mtnck)
        murb__sonqm = tuple(hyxb__uivvt for i, hyxb__uivvt in enumerate(df.
            columns) if df.data[i] in efacv__mtnck)
    else:
        murb__sonqm = df.columns
    if not tdf__nugch:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            mneh__zit = [dtype_to_array_type(parse_dtype(elem, vyo__liu)) for
                elem in exclude]
        elif is_legal_input(exclude):
            mneh__zit = [dtype_to_array_type(parse_dtype(exclude, vyo__liu))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        mneh__zit = get_nullable_and_non_nullable_types(mneh__zit)
        murb__sonqm = tuple(hyxb__uivvt for hyxb__uivvt in murb__sonqm if 
            df.data[df.columns.index(hyxb__uivvt)] not in mneh__zit)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(hyxb__uivvt)})'
         for hyxb__uivvt in murb__sonqm)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, murb__sonqm, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        tdu__dcd = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([tdu__dcd] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': tdu__dcd}
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
    spgjw__mpqh = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in spgjw__mpqh:
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
    spgjw__mpqh = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in spgjw__mpqh:
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
    zohr__oyejj = 'def impl(df, values):\n'
    gfkgb__fyut = {}
    jrsy__webb = False
    if isinstance(values, DataFrameType):
        jrsy__webb = True
        for i, hyxb__uivvt in enumerate(df.columns):
            if hyxb__uivvt in values.columns:
                kjmzc__xsu = 'val{}'.format(i)
                zohr__oyejj += (
                    """  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {})
"""
                    .format(kjmzc__xsu, values.columns.index(hyxb__uivvt)))
                gfkgb__fyut[hyxb__uivvt] = kjmzc__xsu
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        gfkgb__fyut = {hyxb__uivvt: 'values' for hyxb__uivvt in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        kjmzc__xsu = 'data{}'.format(i)
        zohr__oyejj += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(kjmzc__xsu, i))
        data.append(kjmzc__xsu)
    yirn__budt = ['out{}'.format(i) for i in range(len(df.columns))]
    cqro__gmxo = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    nsqx__dyjb = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    ibb__ypr = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, zovv__qwsp) in enumerate(zip(df.columns, data)):
        if cname in gfkgb__fyut:
            iih__vqyxb = gfkgb__fyut[cname]
            if jrsy__webb:
                zohr__oyejj += cqro__gmxo.format(zovv__qwsp, iih__vqyxb,
                    yirn__budt[i])
            else:
                zohr__oyejj += nsqx__dyjb.format(zovv__qwsp, iih__vqyxb,
                    yirn__budt[i])
        else:
            zohr__oyejj += ibb__ypr.format(yirn__budt[i])
    return _gen_init_df(zohr__oyejj, df.columns, ','.join(yirn__budt))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    anz__psfkl = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(anz__psfkl))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    nwt__lbo = [hyxb__uivvt for hyxb__uivvt, dvpnx__unz in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(dvpnx__unz.
        dtype)]
    assert len(nwt__lbo) != 0
    wmtkm__stf = ''
    if not any(dvpnx__unz == types.float64 for dvpnx__unz in df.data):
        wmtkm__stf = '.astype(np.float64)'
    rock__qfrgh = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(hyxb__uivvt), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(hyxb__uivvt)], IntegerArrayType
        ) or df.data[df.columns.index(hyxb__uivvt)] == boolean_array else
        '') for hyxb__uivvt in nwt__lbo)
    fmj__dkad = 'np.stack(({},), 1){}'.format(rock__qfrgh, wmtkm__stf)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(nwt__lbo)))
    index = f'{generate_col_to_index_func_text(nwt__lbo)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(fmj__dkad)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, nwt__lbo, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    thscd__alidr = dict(ddof=ddof)
    bpi__tje = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    pteoo__ahtpc = '1' if is_overload_none(min_periods) else 'min_periods'
    nwt__lbo = [hyxb__uivvt for hyxb__uivvt, dvpnx__unz in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(dvpnx__unz.
        dtype)]
    if len(nwt__lbo) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    wmtkm__stf = ''
    if not any(dvpnx__unz == types.float64 for dvpnx__unz in df.data):
        wmtkm__stf = '.astype(np.float64)'
    rock__qfrgh = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(hyxb__uivvt), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(hyxb__uivvt)], IntegerArrayType
        ) or df.data[df.columns.index(hyxb__uivvt)] == boolean_array else
        '') for hyxb__uivvt in nwt__lbo)
    fmj__dkad = 'np.stack(({},), 1){}'.format(rock__qfrgh, wmtkm__stf)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(nwt__lbo)))
    index = f'pd.Index({nwt__lbo})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(fmj__dkad)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        pteoo__ahtpc)
    return _gen_init_df(header, nwt__lbo, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    thscd__alidr = dict(axis=axis, level=level, numeric_only=numeric_only)
    bpi__tje = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    zohr__oyejj = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    zohr__oyejj += '  data = np.array([{}])\n'.format(data_args)
    qblf__xeefi = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    zohr__oyejj += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {qblf__xeefi})\n'
        )
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo, 'np': np}, zqs__jguwt)
    impl = zqs__jguwt['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    thscd__alidr = dict(axis=axis)
    bpi__tje = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    zohr__oyejj = 'def impl(df, axis=0, dropna=True):\n'
    zohr__oyejj += '  data = np.asarray(({},))\n'.format(data_args)
    qblf__xeefi = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    zohr__oyejj += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {qblf__xeefi})\n'
        )
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo, 'np': np}, zqs__jguwt)
    impl = zqs__jguwt['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    thscd__alidr = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    bpi__tje = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    thscd__alidr = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    bpi__tje = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    thscd__alidr = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    bpi__tje = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    thscd__alidr = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    bpi__tje = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    thscd__alidr = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    bpi__tje = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    thscd__alidr = dict(skipna=skipna, level=level, ddof=ddof, numeric_only
        =numeric_only)
    bpi__tje = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    thscd__alidr = dict(skipna=skipna, level=level, ddof=ddof, numeric_only
        =numeric_only)
    bpi__tje = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    thscd__alidr = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    bpi__tje = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    thscd__alidr = dict(numeric_only=numeric_only, interpolation=interpolation)
    bpi__tje = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    thscd__alidr = dict(axis=axis, skipna=skipna)
    bpi__tje = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for isn__hsvlh in df.data:
        if not (bodo.utils.utils.is_np_array_typ(isn__hsvlh) and (
            isn__hsvlh.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(isn__hsvlh.dtype, (types.Number, types.Boolean))) or
            isinstance(isn__hsvlh, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or isn__hsvlh in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {isn__hsvlh} not supported.'
                )
        if isinstance(isn__hsvlh, bodo.CategoricalArrayType
            ) and not isn__hsvlh.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    thscd__alidr = dict(axis=axis, skipna=skipna)
    bpi__tje = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for isn__hsvlh in df.data:
        if not (bodo.utils.utils.is_np_array_typ(isn__hsvlh) and (
            isn__hsvlh.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(isn__hsvlh.dtype, (types.Number, types.Boolean))) or
            isinstance(isn__hsvlh, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or isn__hsvlh in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {isn__hsvlh} not supported.'
                )
        if isinstance(isn__hsvlh, bodo.CategoricalArrayType
            ) and not isn__hsvlh.dtype.ordered:
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
        nwt__lbo = tuple(hyxb__uivvt for hyxb__uivvt, dvpnx__unz in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (dvpnx__unz.dtype))
        out_colnames = nwt__lbo
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            ujqho__qkd = [numba.np.numpy_support.as_dtype(df.data[df.
                columns.index(hyxb__uivvt)].dtype) for hyxb__uivvt in
                out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(ujqho__qkd, []))
    except NotImplementedError as lsqbm__ptjz:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    usvf__mgbu = ''
    if func_name in ('sum', 'prod'):
        usvf__mgbu = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    zohr__oyejj = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, usvf__mgbu))
    if func_name == 'quantile':
        zohr__oyejj = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        zohr__oyejj = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        zohr__oyejj += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        zohr__oyejj += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        zqs__jguwt)
    impl = zqs__jguwt['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    gccf__paz = ''
    if func_name in ('min', 'max'):
        gccf__paz = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        gccf__paz = ', dtype=np.float32'
    fpspg__nakl = f'bodo.libs.array_ops.array_op_{func_name}'
    hurru__nej = ''
    if func_name in ['sum', 'prod']:
        hurru__nej = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        hurru__nej = 'index'
    elif func_name == 'quantile':
        hurru__nej = 'q'
    elif func_name in ['std', 'var']:
        hurru__nej = 'True, ddof'
    elif func_name == 'median':
        hurru__nej = 'True'
    data_args = ', '.join(
        f'{fpspg__nakl}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(hyxb__uivvt)}), {hurru__nej})'
         for hyxb__uivvt in out_colnames)
    zohr__oyejj = ''
    if func_name in ('idxmax', 'idxmin'):
        zohr__oyejj += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        zohr__oyejj += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        zohr__oyejj += '  data = np.asarray(({},){})\n'.format(data_args,
            gccf__paz)
    zohr__oyejj += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return zohr__oyejj


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    nat__xnem = [df_type.columns.index(hyxb__uivvt) for hyxb__uivvt in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in nat__xnem)
    ozg__sdgr = '\n        '.join(f'row[{i}] = arr_{nat__xnem[i]}[i]' for i in
        range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    lvw__jcphq = f'len(arr_{nat__xnem[0]})'
    ypa__hob = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum': 'np.nansum',
        'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in ypa__hob:
        xlxf__qtvri = ypa__hob[func_name]
        odv__qvqh = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        zohr__oyejj = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {lvw__jcphq}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{odv__qvqh})
    for i in numba.parfors.parfor.internal_prange(n):
        {ozg__sdgr}
        A[i] = {xlxf__qtvri}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return zohr__oyejj
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    thscd__alidr = dict(fill_method=fill_method, limit=limit, freq=freq)
    bpi__tje = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', thscd__alidr, bpi__tje,
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
    thscd__alidr = dict(axis=axis, skipna=skipna)
    bpi__tje = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', thscd__alidr, bpi__tje,
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
    thscd__alidr = dict(skipna=skipna)
    bpi__tje = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', thscd__alidr, bpi__tje,
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
    thscd__alidr = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    bpi__tje = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    nwt__lbo = [hyxb__uivvt for hyxb__uivvt, dvpnx__unz in zip(df.columns,
        df.data) if _is_describe_type(dvpnx__unz)]
    if len(nwt__lbo) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    yfkdw__tsj = sum(df.data[df.columns.index(hyxb__uivvt)].dtype == bodo.
        datetime64ns for hyxb__uivvt in nwt__lbo)

    def _get_describe(col_ind):
        bye__jqtum = df.data[col_ind].dtype == bodo.datetime64ns
        if yfkdw__tsj and yfkdw__tsj != len(nwt__lbo):
            if bye__jqtum:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for hyxb__uivvt in nwt__lbo:
        col_ind = df.columns.index(hyxb__uivvt)
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.columns.index(hyxb__uivvt)) for
        hyxb__uivvt in nwt__lbo)
    oxqh__cgi = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if yfkdw__tsj == len(nwt__lbo):
        oxqh__cgi = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif yfkdw__tsj:
        oxqh__cgi = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({oxqh__cgi})'
    return _gen_init_df(header, nwt__lbo, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    thscd__alidr = dict(axis=axis, convert=convert, is_copy=is_copy)
    bpi__tje = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', thscd__alidr, bpi__tje,
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
    thscd__alidr = dict(freq=freq, axis=axis, fill_value=fill_value)
    bpi__tje = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for vcmkl__pushq in df.data:
        if not is_supported_shift_array_type(vcmkl__pushq):
            raise BodoError(
                f'Dataframe.shift() column input type {vcmkl__pushq.dtype} not supported yet.'
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
    thscd__alidr = dict(axis=axis)
    bpi__tje = dict(axis=0)
    check_unsupported_args('DataFrame.diff', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for vcmkl__pushq in df.data:
        if not (isinstance(vcmkl__pushq, types.Array) and (isinstance(
            vcmkl__pushq.dtype, types.Number) or vcmkl__pushq.dtype == bodo
            .datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {vcmkl__pushq.dtype} not supported.'
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
    fcjwk__pfq = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(fcjwk__pfq)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        cfd__ont = get_overload_const_list(column)
    else:
        cfd__ont = [get_literal_value(column)]
    gmq__cefh = {hyxb__uivvt: i for i, hyxb__uivvt in enumerate(df.columns)}
    buwp__jfem = [gmq__cefh[hyxb__uivvt] for hyxb__uivvt in cfd__ont]
    for i in buwp__jfem:
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
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{buwp__jfem[0]})\n'
        )
    for i in range(n):
        if i in buwp__jfem:
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
    whnxa__eap = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    voo__xbwir = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', whnxa__eap, voo__xbwir,
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
    columns = tuple(hyxb__uivvt for hyxb__uivvt in df.columns if 
        hyxb__uivvt != col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    whnxa__eap = {'inplace': inplace}
    voo__xbwir = {'inplace': False}
    check_unsupported_args('query', whnxa__eap, voo__xbwir, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        zst__nde = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[zst__nde]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    whnxa__eap = {'subset': subset, 'keep': keep}
    voo__xbwir = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', whnxa__eap, voo__xbwir,
        package_name='pandas', module_name='DataFrame')
    anz__psfkl = len(df.columns)
    zohr__oyejj = "def impl(df, subset=None, keep='first'):\n"
    for i in range(anz__psfkl):
        zohr__oyejj += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    exgcx__bjq = ', '.join(f'data_{i}' for i in range(anz__psfkl))
    exgcx__bjq += ',' if anz__psfkl == 1 else ''
    zohr__oyejj += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({exgcx__bjq}))\n')
    zohr__oyejj += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    zohr__oyejj += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo}, zqs__jguwt)
    impl = zqs__jguwt['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    whnxa__eap = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    voo__xbwir = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    khy__wgu = []
    if is_overload_constant_list(subset):
        khy__wgu = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        khy__wgu = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        khy__wgu = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    cyc__chup = []
    for col_name in khy__wgu:
        if col_name not in df.columns:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        cyc__chup.append(df.columns.index(col_name))
    check_unsupported_args('DataFrame.drop_duplicates', whnxa__eap,
        voo__xbwir, package_name='pandas', module_name='DataFrame')
    jjb__yyuo = []
    if cyc__chup:
        for tshem__wrs in cyc__chup:
            if isinstance(df.data[tshem__wrs], bodo.MapArrayType):
                jjb__yyuo.append(df.columns[tshem__wrs])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                jjb__yyuo.append(col_name)
    if jjb__yyuo:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {jjb__yyuo} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    anz__psfkl = len(df.columns)
    tsnoi__sogo = ['data_{}'.format(i) for i in cyc__chup]
    axdbs__fdzoh = ['data_{}'.format(i) for i in range(anz__psfkl) if i not in
        cyc__chup]
    if tsnoi__sogo:
        ggby__mijzd = len(tsnoi__sogo)
    else:
        ggby__mijzd = anz__psfkl
    xktja__phwg = ', '.join(tsnoi__sogo + axdbs__fdzoh)
    data_args = ', '.join('data_{}'.format(i) for i in range(anz__psfkl))
    zohr__oyejj = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(anz__psfkl):
        zohr__oyejj += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    zohr__oyejj += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(xktja__phwg, index, ggby__mijzd))
    zohr__oyejj += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(zohr__oyejj, df.columns, data_args, 'index')


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
                zpgd__swa = {hyxb__uivvt: i for i, hyxb__uivvt in enumerate
                    (cond.columns)}

                def cond_str(i, gen_all_false):
                    if df.columns[i] in zpgd__swa:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {zpgd__swa[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            higbm__ipiwm = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                other_map = {hyxb__uivvt: i for i, hyxb__uivvt in enumerate
                    (other.columns)}
                higbm__ipiwm = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other_map[df.columns[i]]})'
                     if df.columns[i] in other_map else 'None')
            elif isinstance(other, types.Array):
                higbm__ipiwm = lambda i: f'other[:,{i}]'
        anz__psfkl = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {higbm__ipiwm(i)})'
             for i in range(anz__psfkl))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        fmnk__woeek = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(
            fmnk__woeek)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    thscd__alidr = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    bpi__tje = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', thscd__alidr, bpi__tje,
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
    anz__psfkl = len(df.columns)
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
        other_map = {hyxb__uivvt: i for i, hyxb__uivvt in enumerate(other.
            columns)}
        for i in range(anz__psfkl):
            if df.columns[i] in other_map:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other_map[df.columns[i]]]
                    )
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(anz__psfkl):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(anz__psfkl):
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
        kfwpy__japhh = 'out_df_type'
    else:
        kfwpy__japhh = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    zohr__oyejj = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {kfwpy__japhh})
"""
    zqs__jguwt = {}
    qfre__cqjtn = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    qfre__cqjtn.update(extra_globals)
    exec(zohr__oyejj, qfre__cqjtn, zqs__jguwt)
    impl = zqs__jguwt['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        rvkv__idqu = pd.Index(lhs.columns)
        tihlq__rvs = pd.Index(rhs.columns)
        xaoi__abpef, hsw__mgexj, pdd__ltcuz = rvkv__idqu.join(tihlq__rvs,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(xaoi__abpef), hsw__mgexj, pdd__ltcuz
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        xetu__dsfc = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        grlt__kms = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, xetu__dsfc)
        check_runtime_cols_unsupported(rhs, xetu__dsfc)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                xaoi__abpef, hsw__mgexj, pdd__ltcuz = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {qymec__ohbf}) {xetu__dsfc}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {xpfjn__soikk})'
                     if qymec__ohbf != -1 and xpfjn__soikk != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for qymec__ohbf, xpfjn__soikk in zip(hsw__mgexj,
                    pdd__ltcuz))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, xaoi__abpef, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            kniqr__ikkij = []
            msv__vfq = []
            if op in grlt__kms:
                for i, xhn__qqg in enumerate(lhs.data):
                    if is_common_scalar_dtype([xhn__qqg.dtype, rhs]):
                        kniqr__ikkij.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {xetu__dsfc} rhs'
                            )
                    else:
                        blj__ctpch = f'arr{i}'
                        msv__vfq.append(blj__ctpch)
                        kniqr__ikkij.append(blj__ctpch)
                data_args = ', '.join(kniqr__ikkij)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {xetu__dsfc} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(msv__vfq) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {blj__ctpch} = np.empty(n, dtype=np.bool_)\n' for
                    blj__ctpch in msv__vfq)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(blj__ctpch, 
                    op == operator.ne) for blj__ctpch in msv__vfq)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            kniqr__ikkij = []
            msv__vfq = []
            if op in grlt__kms:
                for i, xhn__qqg in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, xhn__qqg.dtype]):
                        kniqr__ikkij.append(
                            f'lhs {xetu__dsfc} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        blj__ctpch = f'arr{i}'
                        msv__vfq.append(blj__ctpch)
                        kniqr__ikkij.append(blj__ctpch)
                data_args = ', '.join(kniqr__ikkij)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, xetu__dsfc) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(msv__vfq) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(blj__ctpch) for blj__ctpch in msv__vfq)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(blj__ctpch, 
                    op == operator.ne) for blj__ctpch in msv__vfq)
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
        fmnk__woeek = create_binary_op_overload(op)
        overload(op)(fmnk__woeek)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        xetu__dsfc = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, xetu__dsfc)
        check_runtime_cols_unsupported(right, xetu__dsfc)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                xaoi__abpef, _, pdd__ltcuz = _get_binop_columns(left, right,
                    True)
                zohr__oyejj = 'def impl(left, right):\n'
                for i, xpfjn__soikk in enumerate(pdd__ltcuz):
                    if xpfjn__soikk == -1:
                        zohr__oyejj += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    zohr__oyejj += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    zohr__oyejj += f"""  df_arr{i} {xetu__dsfc} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {xpfjn__soikk})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    xaoi__abpef)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(zohr__oyejj, xaoi__abpef, data_args,
                    index, extra_globals={'float64_arr_type': types.Array(
                    types.float64, 1, 'C')})
            zohr__oyejj = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                zohr__oyejj += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                zohr__oyejj += '  df_arr{0} {1} right\n'.format(i, xetu__dsfc)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(zohr__oyejj, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        fmnk__woeek = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(fmnk__woeek)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            xetu__dsfc = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, xetu__dsfc)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, xetu__dsfc) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        fmnk__woeek = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(fmnk__woeek)


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
            weqpz__bsrhg = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                weqpz__bsrhg[i] = bodo.libs.array_kernels.isna(obj, i)
            return weqpz__bsrhg
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
            weqpz__bsrhg = np.empty(n, np.bool_)
            for i in range(n):
                weqpz__bsrhg[i] = pd.isna(obj[i])
            return weqpz__bsrhg
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
    whnxa__eap = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    voo__xbwir = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', whnxa__eap, voo__xbwir, package_name=
        'pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    vaunq__wnayv = str(expr_node)
    return vaunq__wnayv.startswith('left.') or vaunq__wnayv.startswith('right.'
        )


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    jhpbf__fzuf = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (jhpbf__fzuf,))
    lga__ydskb = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        xttc__yete = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        vbdzf__fdn = {('NOT_NA', lga__ydskb(xhn__qqg)): xhn__qqg for
            xhn__qqg in null_set}
        plcy__vla, _, _ = _parse_query_expr(xttc__yete, env, [], [], None,
            join_cleaned_cols=vbdzf__fdn)
        hxc__tfd = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            ztge__kvt = pd.core.computation.ops.BinOp('&', plcy__vla, expr_node
                )
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = hxc__tfd
        return ztge__kvt

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                nzulj__csu = set()
                licjj__nrbg = set()
                kypt__notrj = _insert_NA_cond_body(expr_node.lhs, nzulj__csu)
                gcvgx__upwj = _insert_NA_cond_body(expr_node.rhs, licjj__nrbg)
                mnb__ibk = nzulj__csu.intersection(licjj__nrbg)
                nzulj__csu.difference_update(mnb__ibk)
                licjj__nrbg.difference_update(mnb__ibk)
                null_set.update(mnb__ibk)
                expr_node.lhs = append_null_checks(kypt__notrj, nzulj__csu)
                expr_node.rhs = append_null_checks(gcvgx__upwj, licjj__nrbg)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            gtxhi__acatb = expr_node.name
            xsi__ccny, col_name = gtxhi__acatb.split('.')
            if xsi__ccny == 'left':
                tqre__avkqr = left_columns
                data = left_data
            else:
                tqre__avkqr = right_columns
                data = right_data
            qlyve__saejv = data[tqre__avkqr.index(col_name)]
            if bodo.utils.typing.is_nullable(qlyve__saejv):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    jeb__hjyps = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        aon__oumnm = str(expr_node.lhs)
        mvvgw__wbit = str(expr_node.rhs)
        if aon__oumnm.startswith('left.') and mvvgw__wbit.startswith('left.'
            ) or aon__oumnm.startswith('right.') and mvvgw__wbit.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [aon__oumnm.split('.')[1]]
        right_on = [mvvgw__wbit.split('.')[1]]
        if aon__oumnm.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        twshv__gznxf, scuya__eyux, twjt__kcwcp = _extract_equal_conds(expr_node
            .lhs)
        hws__aqhk, qjptf__hvj, jzvg__uaw = _extract_equal_conds(expr_node.rhs)
        left_on = twshv__gznxf + hws__aqhk
        right_on = scuya__eyux + qjptf__hvj
        if twjt__kcwcp is None:
            return left_on, right_on, jzvg__uaw
        if jzvg__uaw is None:
            return left_on, right_on, twjt__kcwcp
        expr_node.lhs = twjt__kcwcp
        expr_node.rhs = jzvg__uaw
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    jhpbf__fzuf = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (jhpbf__fzuf,))
    pyj__lqf = dict()
    lga__ydskb = pd.core.computation.parsing.clean_column_name
    for name, szplv__rnw in (('left', left_columns), ('right', right_columns)):
        for xhn__qqg in szplv__rnw:
            pgu__hjfav = lga__ydskb(xhn__qqg)
            kcrph__wkqg = name, pgu__hjfav
            if kcrph__wkqg in pyj__lqf:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{xhn__qqg}' and '{pyj__lqf[pgu__hjfav]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            pyj__lqf[kcrph__wkqg] = xhn__qqg
    amsi__qkn, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=pyj__lqf)
    left_on, right_on, azo__bsi = _extract_equal_conds(amsi__qkn.terms)
    return left_on, right_on, _insert_NA_cond(azo__bsi, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    thscd__alidr = dict(sort=sort, copy=copy, validate=validate)
    bpi__tje = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    llmah__tjze = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    ibfx__tbb = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in llmah__tjze and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, czaw__rnx = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if czaw__rnx is None:
                    ibfx__tbb = ''
                else:
                    ibfx__tbb = str(czaw__rnx)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = llmah__tjze
        right_keys = llmah__tjze
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
    tzb__fuwm = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        lfx__qdbj = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        lfx__qdbj = list(get_overload_const_list(suffixes))
    suffix_x = lfx__qdbj[0]
    suffix_y = lfx__qdbj[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    zohr__oyejj = (
        "def _impl(left, right, how='inner', on=None, left_on=None,\n")
    zohr__oyejj += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    zohr__oyejj += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    zohr__oyejj += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, tzb__fuwm, ibfx__tbb))
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo}, zqs__jguwt)
    _impl = zqs__jguwt['_impl']
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
    pgdhc__sfil = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    fxx__liti = {get_overload_const_str(owcf__zxsn) for owcf__zxsn in (
        left_on, right_on, on) if is_overload_constant_str(owcf__zxsn)}
    for df in (left, right):
        for i, xhn__qqg in enumerate(df.data):
            if not isinstance(xhn__qqg, valid_dataframe_column_types
                ) and xhn__qqg not in pgdhc__sfil:
                raise BodoError(
                    f'{name_func}(): use of column with {type(xhn__qqg)} in merge unsupported'
                    )
            if df.columns[i] in fxx__liti and isinstance(xhn__qqg, MapArrayType
                ):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        lfx__qdbj = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        lfx__qdbj = list(get_overload_const_list(suffixes))
    if len(lfx__qdbj) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    llmah__tjze = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        enaw__ysce = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            enaw__ysce = on_str not in llmah__tjze and ('left.' in on_str or
                'right.' in on_str)
        if len(llmah__tjze) == 0 and not enaw__ysce:
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
    oqr__gez = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            puci__esqld = left.index
            chkn__yey = isinstance(puci__esqld, StringIndexType)
            fyoj__submv = right.index
            ngp__feld = isinstance(fyoj__submv, StringIndexType)
        elif is_overload_true(left_index):
            puci__esqld = left.index
            chkn__yey = isinstance(puci__esqld, StringIndexType)
            fyoj__submv = right.data[right.columns.index(right_keys[0])]
            ngp__feld = fyoj__submv.dtype == string_type
        elif is_overload_true(right_index):
            puci__esqld = left.data[left.columns.index(left_keys[0])]
            chkn__yey = puci__esqld.dtype == string_type
            fyoj__submv = right.index
            ngp__feld = isinstance(fyoj__submv, StringIndexType)
        if chkn__yey and ngp__feld:
            return
        puci__esqld = puci__esqld.dtype
        fyoj__submv = fyoj__submv.dtype
        try:
            abw__ubgbg = oqr__gez.resolve_function_type(operator.eq, (
                puci__esqld, fyoj__submv), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=puci__esqld, rk_dtype=fyoj__submv))
    else:
        for ztkvx__kicxs, eurh__pdqzq in zip(left_keys, right_keys):
            puci__esqld = left.data[left.columns.index(ztkvx__kicxs)].dtype
            qjd__buev = left.data[left.columns.index(ztkvx__kicxs)]
            fyoj__submv = right.data[right.columns.index(eurh__pdqzq)].dtype
            xitfx__pxp = right.data[right.columns.index(eurh__pdqzq)]
            if qjd__buev == xitfx__pxp:
                continue
            hex__exgz = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=ztkvx__kicxs, lk_dtype=puci__esqld, rk=
                eurh__pdqzq, rk_dtype=fyoj__submv))
            puomj__fcxh = puci__esqld == string_type
            mpvd__iimy = fyoj__submv == string_type
            if puomj__fcxh ^ mpvd__iimy:
                raise_bodo_error(hex__exgz)
            try:
                abw__ubgbg = oqr__gez.resolve_function_type(operator.eq, (
                    puci__esqld, fyoj__submv), {})
            except:
                raise_bodo_error(hex__exgz)


def validate_keys(keys, df):
    nbjo__qxyau = set(keys).difference(set(df.columns))
    if len(nbjo__qxyau) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in nbjo__qxyau:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {nbjo__qxyau} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    thscd__alidr = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    bpi__tje = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', thscd__alidr, bpi__tje,
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
    zohr__oyejj = "def _impl(left, other, on=None, how='left',\n"
    zohr__oyejj += "    lsuffix='', rsuffix='', sort=False):\n"
    zohr__oyejj += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo}, zqs__jguwt)
    _impl = zqs__jguwt['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        obarp__zknj = get_overload_const_list(on)
        validate_keys(obarp__zknj, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    llmah__tjze = tuple(set(left.columns) & set(other.columns))
    if len(llmah__tjze) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=llmah__tjze))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    rvsvb__oqgb = set(left_keys) & set(right_keys)
    tmbc__btbnl = set(left_columns) & set(right_columns)
    sgul__chcyt = tmbc__btbnl - rvsvb__oqgb
    psc__lbp = set(left_columns) - tmbc__btbnl
    utrez__evb = set(right_columns) - tmbc__btbnl
    krupx__dmgok = {}

    def insertOutColumn(col_name):
        if col_name in krupx__dmgok:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        krupx__dmgok[col_name] = 0
    for evw__ilzfh in rvsvb__oqgb:
        insertOutColumn(evw__ilzfh)
    for evw__ilzfh in sgul__chcyt:
        cdld__omt = str(evw__ilzfh) + suffix_x
        atr__dpsu = str(evw__ilzfh) + suffix_y
        insertOutColumn(cdld__omt)
        insertOutColumn(atr__dpsu)
    for evw__ilzfh in psc__lbp:
        insertOutColumn(evw__ilzfh)
    for evw__ilzfh in utrez__evb:
        insertOutColumn(evw__ilzfh)
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
    llmah__tjze = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = llmah__tjze
        right_keys = llmah__tjze
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
        lfx__qdbj = suffixes
    if is_overload_constant_list(suffixes):
        lfx__qdbj = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        lfx__qdbj = suffixes.value
    suffix_x = lfx__qdbj[0]
    suffix_y = lfx__qdbj[1]
    zohr__oyejj = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    zohr__oyejj += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    zohr__oyejj += (
        "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n")
    zohr__oyejj += "    allow_exact_matches=True, direction='backward'):\n"
    zohr__oyejj += '  suffix_x = suffixes[0]\n'
    zohr__oyejj += '  suffix_y = suffixes[1]\n'
    zohr__oyejj += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo}, zqs__jguwt)
    _impl = zqs__jguwt['_impl']
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
    thscd__alidr = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    scct__rov = dict(sort=False, group_keys=True, squeeze=False, observed=True)
    check_unsupported_args('Dataframe.groupby', thscd__alidr, scct__rov,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    wtgqn__ecdl = func_name == 'DataFrame.pivot_table'
    if wtgqn__ecdl:
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
    wbdzi__fdkn = get_literal_value(columns)
    if isinstance(wbdzi__fdkn, (list, tuple)):
        if len(wbdzi__fdkn) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {wbdzi__fdkn}"
                )
        wbdzi__fdkn = wbdzi__fdkn[0]
    if wbdzi__fdkn not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {wbdzi__fdkn} not found in DataFrame {df}."
            )
    wvfsc__fov = {hyxb__uivvt: i for i, hyxb__uivvt in enumerate(df.columns)}
    croc__mfnd = wvfsc__fov[wbdzi__fdkn]
    if is_overload_none(index):
        vgc__djc = []
        hhf__tbzd = []
    else:
        hhf__tbzd = get_literal_value(index)
        if not isinstance(hhf__tbzd, (list, tuple)):
            hhf__tbzd = [hhf__tbzd]
        vgc__djc = []
        for index in hhf__tbzd:
            if index not in wvfsc__fov:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            vgc__djc.append(wvfsc__fov[index])
    if not (all(isinstance(hyxb__uivvt, int) for hyxb__uivvt in hhf__tbzd) or
        all(isinstance(hyxb__uivvt, str) for hyxb__uivvt in hhf__tbzd)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        rrzs__wxefm = []
        dyge__yxk = []
        csi__jxvx = vgc__djc + [croc__mfnd]
        for i, hyxb__uivvt in enumerate(df.columns):
            if i not in csi__jxvx:
                rrzs__wxefm.append(i)
                dyge__yxk.append(hyxb__uivvt)
    else:
        dyge__yxk = get_literal_value(values)
        if not isinstance(dyge__yxk, (list, tuple)):
            dyge__yxk = [dyge__yxk]
        rrzs__wxefm = []
        for val in dyge__yxk:
            if val not in wvfsc__fov:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            rrzs__wxefm.append(wvfsc__fov[val])
    if all(isinstance(hyxb__uivvt, int) for hyxb__uivvt in dyge__yxk):
        dyge__yxk = np.array(dyge__yxk, 'int64')
    elif all(isinstance(hyxb__uivvt, str) for hyxb__uivvt in dyge__yxk):
        dyge__yxk = pd.array(dyge__yxk, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    axegx__suy = set(rrzs__wxefm) | set(vgc__djc) | {croc__mfnd}
    if len(axegx__suy) != len(rrzs__wxefm) + len(vgc__djc) + 1:
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
    if len(vgc__djc) == 0:
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
        for sumy__chvwg in vgc__djc:
            index_column = df.data[sumy__chvwg]
            check_valid_index_typ(index_column)
    fcksi__bzww = df.data[croc__mfnd]
    if isinstance(fcksi__bzww, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(fcksi__bzww, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for woq__vehm in rrzs__wxefm:
        ipdtg__vbyca = df.data[woq__vehm]
        if isinstance(ipdtg__vbyca, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or ipdtg__vbyca == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return hhf__tbzd, wbdzi__fdkn, dyge__yxk, vgc__djc, croc__mfnd, rrzs__wxefm


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (hhf__tbzd, wbdzi__fdkn, dyge__yxk, sumy__chvwg, croc__mfnd, jozsk__ylgp
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(hhf__tbzd) == 0:
        if is_overload_none(data.index.name_typ):
            hhf__tbzd = [None]
        else:
            hhf__tbzd = [get_literal_value(data.index.name_typ)]
    if len(dyge__yxk) == 1:
        sxqlf__rla = None
    else:
        sxqlf__rla = dyge__yxk
    zohr__oyejj = 'def impl(data, index=None, columns=None, values=None):\n'
    zohr__oyejj += f'    pivot_values = data.iloc[:, {croc__mfnd}].unique()\n'
    zohr__oyejj += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(sumy__chvwg) == 0:
        zohr__oyejj += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        zohr__oyejj += '        (\n'
        for vhfqu__jnb in sumy__chvwg:
            zohr__oyejj += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {vhfqu__jnb}),
"""
        zohr__oyejj += '        ),\n'
    zohr__oyejj += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {croc__mfnd}),),
"""
    zohr__oyejj += '        (\n'
    for woq__vehm in jozsk__ylgp:
        zohr__oyejj += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {woq__vehm}),
"""
    zohr__oyejj += '        ),\n'
    zohr__oyejj += '        pivot_values,\n'
    zohr__oyejj += '        index_lit_tup,\n'
    zohr__oyejj += '        columns_lit,\n'
    zohr__oyejj += '        values_name_const,\n'
    zohr__oyejj += '    )\n'
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo, 'index_lit_tup': tuple(hhf__tbzd),
        'columns_lit': wbdzi__fdkn, 'values_name_const': sxqlf__rla},
        zqs__jguwt)
    impl = zqs__jguwt['impl']
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
    thscd__alidr = dict(fill_value=fill_value, margins=margins, dropna=
        dropna, margins_name=margins_name, observed=observed, sort=sort)
    bpi__tje = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (hhf__tbzd, wbdzi__fdkn, dyge__yxk, sumy__chvwg, croc__mfnd,
            jozsk__ylgp) = (pivot_error_checking(data, index, columns,
            values, 'DataFrame.pivot_table'))
        if len(dyge__yxk) == 1:
            sxqlf__rla = None
        else:
            sxqlf__rla = dyge__yxk
        zohr__oyejj = 'def impl(\n'
        zohr__oyejj += '    data,\n'
        zohr__oyejj += '    values=None,\n'
        zohr__oyejj += '    index=None,\n'
        zohr__oyejj += '    columns=None,\n'
        zohr__oyejj += '    aggfunc="mean",\n'
        zohr__oyejj += '    fill_value=None,\n'
        zohr__oyejj += '    margins=False,\n'
        zohr__oyejj += '    dropna=True,\n'
        zohr__oyejj += '    margins_name="All",\n'
        zohr__oyejj += '    observed=False,\n'
        zohr__oyejj += '    sort=True,\n'
        zohr__oyejj += '    _pivot_values=None,\n'
        zohr__oyejj += '):\n'
        xkg__jos = sumy__chvwg + [croc__mfnd] + jozsk__ylgp
        zohr__oyejj += f'    data = data.iloc[:, {xkg__jos}]\n'
        xthhs__utad = hhf__tbzd + [wbdzi__fdkn]
        zohr__oyejj += (
            f'    data = data.groupby({xthhs__utad!r}, as_index=False).agg(aggfunc)\n'
            )
        zohr__oyejj += (
            f'    pivot_values = data.iloc[:, {len(sumy__chvwg)}].unique()\n')
        zohr__oyejj += (
            '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n')
        zohr__oyejj += '        (\n'
        for i in range(0, len(sumy__chvwg)):
            zohr__oyejj += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        zohr__oyejj += '        ),\n'
        zohr__oyejj += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(sumy__chvwg)}),),
"""
        zohr__oyejj += '        (\n'
        for i in range(len(sumy__chvwg) + 1, len(jozsk__ylgp) + len(
            sumy__chvwg) + 1):
            zohr__oyejj += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        zohr__oyejj += '        ),\n'
        zohr__oyejj += '        pivot_values,\n'
        zohr__oyejj += '        index_lit_tup,\n'
        zohr__oyejj += '        columns_lit,\n'
        zohr__oyejj += '        values_name_const,\n'
        zohr__oyejj += '        check_duplicates=False,\n'
        zohr__oyejj += '    )\n'
        zqs__jguwt = {}
        exec(zohr__oyejj, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(hhf__tbzd), 'columns_lit': wbdzi__fdkn,
            'values_name_const': sxqlf__rla}, zqs__jguwt)
        impl = zqs__jguwt['impl']
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
    thscd__alidr = dict(var_name=var_name, value_name=value_name, col_level
        =col_level, ignore_index=ignore_index)
    bpi__tje = dict(var_name=None, value_name='value', col_level=None,
        ignore_index=True)
    check_unsupported_args('DataFrame.melt', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise BodoError(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise BodoError(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal")
    znd__ogbt = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(znd__ogbt, (list, tuple)):
        znd__ogbt = [znd__ogbt]
    for hyxb__uivvt in znd__ogbt:
        if hyxb__uivvt not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {hyxb__uivvt} not found in {frame}"
                )
    pyj__lqf = {hyxb__uivvt: i for i, hyxb__uivvt in enumerate(frame.columns)}
    pppz__mfkma = [pyj__lqf[i] for i in znd__ogbt]
    if is_overload_none(value_vars):
        set__aune = []
        ihc__yrnyf = []
        for i, hyxb__uivvt in enumerate(frame.columns):
            if i not in pppz__mfkma:
                set__aune.append(i)
                ihc__yrnyf.append(hyxb__uivvt)
    else:
        ihc__yrnyf = get_literal_value(value_vars)
        if not isinstance(ihc__yrnyf, (list, tuple)):
            ihc__yrnyf = [ihc__yrnyf]
        ihc__yrnyf = [v for v in ihc__yrnyf if v not in znd__ogbt]
        if not ihc__yrnyf:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        set__aune = []
        for val in ihc__yrnyf:
            if val not in pyj__lqf:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            set__aune.append(pyj__lqf[val])
    for hyxb__uivvt in ihc__yrnyf:
        if hyxb__uivvt not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {hyxb__uivvt} not found in {frame}"
                )
    if not (all(isinstance(hyxb__uivvt, int) for hyxb__uivvt in ihc__yrnyf) or
        all(isinstance(hyxb__uivvt, str) for hyxb__uivvt in ihc__yrnyf)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    tytv__nxq = frame.data[set__aune[0]]
    pqrg__evhhu = [frame.data[i].dtype for i in set__aune]
    set__aune = np.array(set__aune, dtype=np.int64)
    pppz__mfkma = np.array(pppz__mfkma, dtype=np.int64)
    _, ihz__zzt = bodo.utils.typing.get_common_scalar_dtype(pqrg__evhhu)
    if not ihz__zzt:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': ihc__yrnyf, 'val_type': tytv__nxq}
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
    if frame.is_table_format and all(v == tytv__nxq.dtype for v in pqrg__evhhu
        ):
        extra_globals['value_idxs'] = set__aune
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(ihc__yrnyf) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {set__aune[0]})
"""
    else:
        pqqma__ykrka = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in set__aune)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({pqqma__ykrka},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in pppz__mfkma:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(ihc__yrnyf)})\n'
            )
    mryi__dtkm = ', '.join(f'out_id{i}' for i in pppz__mfkma) + (', ' if 
        len(pppz__mfkma) > 0 else '')
    data_args = mryi__dtkm + 'var_col, val_col'
    columns = tuple(znd__ogbt + ['variable', 'value'])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(ihc__yrnyf)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    thscd__alidr = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    bpi__tje = dict(values=None, rownames=None, colnames=None, aggfunc=None,
        margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', thscd__alidr, bpi__tje,
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
    thscd__alidr = dict(ignore_index=ignore_index, key=key)
    bpi__tje = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
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
    rxlnr__epno = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        rxlnr__epno.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        djb__souw = [get_overload_const_tuple(by)]
    else:
        djb__souw = get_overload_const_list(by)
    djb__souw = set((k, '') if (k, '') in rxlnr__epno else k for k in djb__souw
        )
    if len(djb__souw.difference(rxlnr__epno)) > 0:
        mni__eojek = list(set(get_overload_const_list(by)).difference(
            rxlnr__epno))
        raise_bodo_error(f'sort_values(): invalid keys {mni__eojek} for by.')
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
        aufdn__lpuov = get_overload_const_list(na_position)
        for na_position in aufdn__lpuov:
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
    thscd__alidr = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    bpi__tje = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', thscd__alidr, bpi__tje,
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
    thscd__alidr = dict(limit=limit, downcast=downcast)
    bpi__tje = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    imdri__dvz = not is_overload_none(value)
    twkx__cvk = not is_overload_none(method)
    if imdri__dvz and twkx__cvk:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not imdri__dvz and not twkx__cvk:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if imdri__dvz:
        bnw__mal = 'value=value'
    else:
        bnw__mal = 'method=method'
    data_args = [(
        f"df['{hyxb__uivvt}'].fillna({bnw__mal}, inplace=inplace)" if
        isinstance(hyxb__uivvt, str) else
        f'df[{hyxb__uivvt}].fillna({bnw__mal}, inplace=inplace)') for
        hyxb__uivvt in df.columns]
    zohr__oyejj = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        zohr__oyejj += '  ' + '  \n'.join(data_args) + '\n'
        zqs__jguwt = {}
        exec(zohr__oyejj, {}, zqs__jguwt)
        impl = zqs__jguwt['impl']
        return impl
    else:
        return _gen_init_df(zohr__oyejj, df.columns, ', '.join(dvpnx__unz +
            '.values' for dvpnx__unz in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    thscd__alidr = dict(col_level=col_level, col_fill=col_fill)
    bpi__tje = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', thscd__alidr, bpi__tje,
        package_name='pandas', module_name='DataFrame')
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
    zohr__oyejj = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    zohr__oyejj += (
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
        rsu__zfk = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            rsu__zfk)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            zohr__oyejj += (
                '  m_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
                )
            jtec__yyyuy = ['m_index._data[{}]'.format(i) for i in range(df.
                index.nlevels)]
            data_args = jtec__yyyuy + data_args
        else:
            aqe__oyuw = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [aqe__oyuw] + data_args
    return _gen_init_df(zohr__oyejj, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    ywso__jzwkw = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and ywso__jzwkw == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(ywso__jzwkw))


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
        sxcdg__zuk = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        waxn__lzgz = get_overload_const_list(subset)
        sxcdg__zuk = []
        for wuz__bdpn in waxn__lzgz:
            if wuz__bdpn not in df.columns:
                raise_bodo_error(
                    f"df.dropna(): column '{wuz__bdpn}' not in data frame columns {df}"
                    )
            sxcdg__zuk.append(df.columns.index(wuz__bdpn))
    anz__psfkl = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(anz__psfkl))
    zohr__oyejj = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(anz__psfkl):
        zohr__oyejj += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    zohr__oyejj += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in sxcdg__zuk)))
    zohr__oyejj += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(zohr__oyejj, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    thscd__alidr = dict(index=index, level=level, errors=errors)
    bpi__tje = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', thscd__alidr, bpi__tje,
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
            uter__iye = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            uter__iye = get_overload_const_list(labels)
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
            uter__iye = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            uter__iye = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for hyxb__uivvt in uter__iye:
        if hyxb__uivvt not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(hyxb__uivvt, df.columns))
    if len(set(uter__iye)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    jbvx__mufyp = tuple(hyxb__uivvt for hyxb__uivvt in df.columns if 
        hyxb__uivvt not in uter__iye)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(hyxb__uivvt), '.copy()' if not inplace else
        '') for hyxb__uivvt in jbvx__mufyp)
    zohr__oyejj = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    zohr__oyejj += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(zohr__oyejj, jbvx__mufyp, data_args, index)


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
    thscd__alidr = dict(random_state=random_state, weights=weights, axis=
        axis, ignore_index=ignore_index)
    tdqwm__rloyd = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', thscd__alidr, tdqwm__rloyd,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    anz__psfkl = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(anz__psfkl))
    fsbk__jukhe = ', '.join('rhs_data_{}'.format(i) for i in range(anz__psfkl))
    zohr__oyejj = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    zohr__oyejj += '  if (frac == 1 or n == len(df)) and not replace:\n'
    zohr__oyejj += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(anz__psfkl):
        zohr__oyejj += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    zohr__oyejj += '  if frac is None:\n'
    zohr__oyejj += '    frac_d = -1.0\n'
    zohr__oyejj += '  else:\n'
    zohr__oyejj += '    frac_d = frac\n'
    zohr__oyejj += '  if n is None:\n'
    zohr__oyejj += '    n_i = 0\n'
    zohr__oyejj += '  else:\n'
    zohr__oyejj += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    zohr__oyejj += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({fsbk__jukhe},), {index}, n_i, frac_d, replace)
"""
    zohr__oyejj += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(zohr__oyejj, df.
        columns, data_args, 'index')


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
    whnxa__eap = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    voo__xbwir = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', whnxa__eap, voo__xbwir,
        package_name='pandas', module_name='DataFrame')
    narce__fbvd = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            tlu__nobhx = narce__fbvd + '\n'
            tlu__nobhx += 'Index: 0 entries\n'
            tlu__nobhx += 'Empty DataFrame'
            print(tlu__nobhx)
        return _info_impl
    else:
        zohr__oyejj = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        zohr__oyejj += '    ncols = df.shape[1]\n'
        zohr__oyejj += f'    lines = "{narce__fbvd}\\n"\n'
        zohr__oyejj += f'    lines += "{df.index}: "\n'
        zohr__oyejj += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            zohr__oyejj += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            zohr__oyejj += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            zohr__oyejj += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        zohr__oyejj += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        zohr__oyejj += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        zohr__oyejj += '    column_width = max(space, 7)\n'
        zohr__oyejj += '    column= "Column"\n'
        zohr__oyejj += '    underl= "------"\n'
        zohr__oyejj += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        zohr__oyejj += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        zohr__oyejj += '    mem_size = 0\n'
        zohr__oyejj += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        zohr__oyejj += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        zohr__oyejj += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        ayki__rgrm = dict()
        for i in range(len(df.columns)):
            zohr__oyejj += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            pwhzb__wlzu = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                pwhzb__wlzu = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                ikw__pmlrp = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                pwhzb__wlzu = f'{ikw__pmlrp[:-7]}'
            zohr__oyejj += f'    col_dtype[{i}] = "{pwhzb__wlzu}"\n'
            if pwhzb__wlzu in ayki__rgrm:
                ayki__rgrm[pwhzb__wlzu] += 1
            else:
                ayki__rgrm[pwhzb__wlzu] = 1
            zohr__oyejj += f'    col_name[{i}] = "{df.columns[i]}"\n'
            zohr__oyejj += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        zohr__oyejj += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        zohr__oyejj += '    for i in column_info:\n'
        zohr__oyejj += "        lines += f'{i}\\n'\n"
        aevex__ojpfq = ', '.join(f'{k}({ayki__rgrm[k]})' for k in sorted(
            ayki__rgrm))
        zohr__oyejj += f"    lines += 'dtypes: {aevex__ojpfq}\\n'\n"
        zohr__oyejj += '    mem_size += df.index.nbytes\n'
        zohr__oyejj += '    total_size = _sizeof_fmt(mem_size)\n'
        zohr__oyejj += "    lines += f'memory usage: {total_size}'\n"
        zohr__oyejj += '    print(lines)\n'
        zqs__jguwt = {}
        exec(zohr__oyejj, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, zqs__jguwt)
        _info_impl = zqs__jguwt['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    zohr__oyejj = 'def impl(df, index=True, deep=False):\n'
    chkd__hdjbq = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes')
    mpyk__wcawc = is_overload_true(index)
    columns = df.columns
    if mpyk__wcawc:
        columns = ('Index',) + columns
    if len(columns) == 0:
        twhvh__ynjov = ()
    elif all(isinstance(hyxb__uivvt, int) for hyxb__uivvt in columns):
        twhvh__ynjov = np.array(columns, 'int64')
    elif all(isinstance(hyxb__uivvt, str) for hyxb__uivvt in columns):
        twhvh__ynjov = pd.array(columns, 'string')
    else:
        twhvh__ynjov = columns
    if df.is_table_format:
        vztvt__xbd = int(mpyk__wcawc)
        xrni__boan = len(columns)
        zohr__oyejj += f'  nbytes_arr = np.empty({xrni__boan}, np.int64)\n'
        zohr__oyejj += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        zohr__oyejj += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {vztvt__xbd})
"""
        if mpyk__wcawc:
            zohr__oyejj += f'  nbytes_arr[0] = {chkd__hdjbq}\n'
        zohr__oyejj += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if mpyk__wcawc:
            data = f'{chkd__hdjbq},{data}'
        else:
            dvn__rev = ',' if len(columns) == 1 else ''
            data = f'{data}{dvn__rev}'
        zohr__oyejj += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        twhvh__ynjov}, zqs__jguwt)
    impl = zqs__jguwt['impl']
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
    zdn__nptsd = 'read_excel_df{}'.format(next_label())
    setattr(types, zdn__nptsd, df_type)
    rrg__lfg = False
    if is_overload_constant_list(parse_dates):
        rrg__lfg = get_overload_const_list(parse_dates)
    hroxx__ptgvt = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    zohr__oyejj = f"""
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
    with numba.objmode(df="{zdn__nptsd}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{hroxx__ptgvt}}},
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
            parse_dates={rrg__lfg},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    zqs__jguwt = {}
    exec(zohr__oyejj, globals(), zqs__jguwt)
    impl = zqs__jguwt['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as lsqbm__ptjz:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    zohr__oyejj = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    zohr__oyejj += (
        '    ylabel=None, title=None, legend=True, fontsize=None, \n')
    zohr__oyejj += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        zohr__oyejj += '   fig, ax = plt.subplots()\n'
    else:
        zohr__oyejj += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        zohr__oyejj += '   fig.set_figwidth(figsize[0])\n'
        zohr__oyejj += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        zohr__oyejj += '   xlabel = x\n'
    zohr__oyejj += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        zohr__oyejj += '   ylabel = y\n'
    else:
        zohr__oyejj += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        zohr__oyejj += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        zohr__oyejj += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    zohr__oyejj += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            zohr__oyejj += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            dyvs__sopt = get_overload_const_str(x)
            kek__kbyz = df.columns.index(dyvs__sopt)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if kek__kbyz != i:
                        zohr__oyejj += f"""   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])
"""
        else:
            zohr__oyejj += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        zohr__oyejj += '   ax.scatter(df[x], df[y], s=20)\n'
        zohr__oyejj += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        zohr__oyejj += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        zohr__oyejj += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        zohr__oyejj += '   ax.legend()\n'
    zohr__oyejj += '   return ax\n'
    zqs__jguwt = {}
    exec(zohr__oyejj, {'bodo': bodo, 'plt': plt}, zqs__jguwt)
    impl = zqs__jguwt['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for iwyy__slrrs in df_typ.data:
        if not (isinstance(iwyy__slrrs, IntegerArrayType) or isinstance(
            iwyy__slrrs.dtype, types.Number) or iwyy__slrrs.dtype in (bodo.
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
        puxv__kscw = args[0]
        yocy__wxf = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        vhocu__bqh = puxv__kscw
        check_runtime_cols_unsupported(puxv__kscw, 'set_df_col()')
        if isinstance(puxv__kscw, DataFrameType):
            index = puxv__kscw.index
            if len(puxv__kscw.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(puxv__kscw.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if yocy__wxf in puxv__kscw.columns:
                jbvx__mufyp = puxv__kscw.columns
                trddn__mopvy = puxv__kscw.columns.index(yocy__wxf)
                tjku__ank = list(puxv__kscw.data)
                tjku__ank[trddn__mopvy] = val
                tjku__ank = tuple(tjku__ank)
            else:
                jbvx__mufyp = puxv__kscw.columns + (yocy__wxf,)
                tjku__ank = puxv__kscw.data + (val,)
            vhocu__bqh = DataFrameType(tjku__ank, index, jbvx__mufyp,
                puxv__kscw.dist, puxv__kscw.is_table_format)
        return vhocu__bqh(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    cbch__snqe = {}

    def _rewrite_membership_op(self, node, left, right):
        pbdp__dfg = node.op
        op = self.visit(pbdp__dfg)
        return op, pbdp__dfg, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    hktie__zame = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in hktie__zame:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in hktie__zame:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        hiy__tnage = node.attr
        value = node.value
        flwz__vva = pd.core.computation.ops.LOCAL_TAG
        if hiy__tnage in ('str', 'dt'):
            try:
                mpwm__ovjv = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as kggjd__eeb:
                col_name = kggjd__eeb.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            mpwm__ovjv = str(self.visit(value))
        kcrph__wkqg = mpwm__ovjv, hiy__tnage
        if kcrph__wkqg in join_cleaned_cols:
            hiy__tnage = join_cleaned_cols[kcrph__wkqg]
        name = mpwm__ovjv + '.' + hiy__tnage
        if name.startswith(flwz__vva):
            name = name[len(flwz__vva):]
        if hiy__tnage in ('str', 'dt'):
            lku__yqa = columns[cleaned_columns.index(mpwm__ovjv)]
            cbch__snqe[lku__yqa] = mpwm__ovjv
            self.env.scope[name] = 0
            return self.term_type(flwz__vva + name, self.env)
        hktie__zame.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in hktie__zame:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        zxo__elhq = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        yocy__wxf = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(zxo__elhq), yocy__wxf))

    def op__str__(self):
        qyl__xgox = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            muyi__ihicb)) for muyi__ihicb in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(qyl__xgox)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(qyl__xgox)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(qyl__xgox))
    aisf__asmig = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    euzc__adv = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    szrku__hmiq = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    ybpf__juk = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    aql__xxefn = pd.core.computation.ops.Term.__str__
    icit__fhgu = pd.core.computation.ops.MathCall.__str__
    fcqi__yzg = pd.core.computation.ops.Op.__str__
    hxc__tfd = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
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
        amsi__qkn = pd.core.computation.expr.Expr(expr, env=env)
        xkwyk__fcked = str(amsi__qkn)
    except pd.core.computation.ops.UndefinedVariableError as kggjd__eeb:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == kggjd__eeb.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {kggjd__eeb}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            aisf__asmig)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            euzc__adv)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = szrku__hmiq
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = ybpf__juk
        pd.core.computation.ops.Term.__str__ = aql__xxefn
        pd.core.computation.ops.MathCall.__str__ = icit__fhgu
        pd.core.computation.ops.Op.__str__ = fcqi__yzg
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = hxc__tfd
    cpgc__zwl = pd.core.computation.parsing.clean_column_name
    cbch__snqe.update({hyxb__uivvt: cpgc__zwl(hyxb__uivvt) for hyxb__uivvt in
        columns if cpgc__zwl(hyxb__uivvt) in amsi__qkn.names})
    return amsi__qkn, xkwyk__fcked, cbch__snqe


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        wovc__cor = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(wovc__cor))
        fdi__xro = namedtuple('Pandas', col_names)
        dukd__ryyku = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], fdi__xro)
        super(DataFrameTupleIterator, self).__init__(name, dukd__ryyku)

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
        qxig__ybir = [if_series_to_array_type(a) for a in args[len(args) // 2:]
            ]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        qxig__ybir = [types.Array(types.int64, 1, 'C')] + qxig__ybir
        crdf__zeil = DataFrameTupleIterator(col_names, qxig__ybir)
        return crdf__zeil(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        iiavu__xabjs = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            iiavu__xabjs)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    btim__dxyk = args[len(args) // 2:]
    ypdy__tutm = sig.args[len(sig.args) // 2:]
    vew__zxwv = context.make_helper(builder, sig.return_type)
    ruf__isit = context.get_constant(types.intp, 0)
    llwwq__qtqi = cgutils.alloca_once_value(builder, ruf__isit)
    vew__zxwv.index = llwwq__qtqi
    for i, arr in enumerate(btim__dxyk):
        setattr(vew__zxwv, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(btim__dxyk, ypdy__tutm):
        context.nrt.incref(builder, arr_typ, arr)
    res = vew__zxwv._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    wsah__zuepp, = sig.args
    mzia__oeby, = args
    vew__zxwv = context.make_helper(builder, wsah__zuepp, value=mzia__oeby)
    ircf__qnbwa = signature(types.intp, wsah__zuepp.array_types[1])
    jsuk__umqn = context.compile_internal(builder, lambda a: len(a),
        ircf__qnbwa, [vew__zxwv.array0])
    index = builder.load(vew__zxwv.index)
    hvwyw__vgcfy = builder.icmp_signed('<', index, jsuk__umqn)
    result.set_valid(hvwyw__vgcfy)
    with builder.if_then(hvwyw__vgcfy):
        values = [index]
        for i, arr_typ in enumerate(wsah__zuepp.array_types[1:]):
            nga__aalfk = getattr(vew__zxwv, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                zjkeo__cfac = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    zjkeo__cfac, [nga__aalfk, index])
            else:
                zjkeo__cfac = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    zjkeo__cfac, [nga__aalfk, index])
            values.append(val)
        value = context.make_tuple(builder, wsah__zuepp.yield_type, values)
        result.yield_(value)
        mhcxt__tck = cgutils.increment_index(builder, index)
        builder.store(mhcxt__tck, vew__zxwv.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    hnexp__wjvjc = ir.Assign(rhs, lhs, expr.loc)
    rjm__mkxq = lhs
    kwylk__row = []
    cio__boybi = []
    zcnc__kfbfz = typ.count
    for i in range(zcnc__kfbfz):
        ujlc__xxgt = ir.Var(rjm__mkxq.scope, mk_unique_var('{}_size{}'.
            format(rjm__mkxq.name, i)), rjm__mkxq.loc)
        vrah__vme = ir.Expr.static_getitem(lhs, i, None, rjm__mkxq.loc)
        self.calltypes[vrah__vme] = None
        kwylk__row.append(ir.Assign(vrah__vme, ujlc__xxgt, rjm__mkxq.loc))
        self._define(equiv_set, ujlc__xxgt, types.intp, vrah__vme)
        cio__boybi.append(ujlc__xxgt)
    fgn__qph = tuple(cio__boybi)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        fgn__qph, pre=[hnexp__wjvjc] + kwylk__row)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
