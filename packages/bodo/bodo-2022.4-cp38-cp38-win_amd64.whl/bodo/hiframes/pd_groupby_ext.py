"""Support for Pandas Groupby operations
"""
import operator
from enum import Enum
import numba
import numpy as np
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, get_groupby_labels, get_null_shuffle_info, get_shuffle_info, info_from_table, info_to_array, reverse_shuffle_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import gen_const_tup, get_call_expr_arg, get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_index_name_types, get_literal_value, get_overload_const_bool, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, get_udf_error_msg, get_udf_out_arr_type, is_dtype_nullable, is_literal_type, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, list_cumulative, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import dt_err, is_expr


class DataFrameGroupByType(types.Type):

    def __init__(self, df_type, keys, selection, as_index, dropna=True,
        explicit_select=False, series_select=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df_type,
            'pandas.groupby()')
        self.df_type = df_type
        self.keys = keys
        self.selection = selection
        self.as_index = as_index
        self.dropna = dropna
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(DataFrameGroupByType, self).__init__(name=
            f'DataFrameGroupBy({df_type}, {keys}, {selection}, {as_index}, {dropna}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return DataFrameGroupByType(self.df_type, self.keys, self.selection,
            self.as_index, self.dropna, self.explicit_select, self.
            series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFrameGroupByType)
class GroupbyModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hyvu__ver = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, hyvu__ver)


make_attribute_wrapper(DataFrameGroupByType, 'obj', 'obj')


def validate_udf(func_name, func):
    if not isinstance(func, (types.functions.MakeFunctionLiteral, bodo.
        utils.typing.FunctionLiteral, types.Dispatcher, CPUDispatcher)):
        raise_bodo_error(
            f"Groupby.{func_name}: 'func' must be user defined function")


@intrinsic
def init_groupby(typingctx, obj_type, by_type, as_index_type=None,
    dropna_type=None):

    def codegen(context, builder, signature, args):
        qqgys__mkd = args[0]
        fwkk__dklis = signature.return_type
        plhxa__yzfv = cgutils.create_struct_proxy(fwkk__dklis)(context, builder
            )
        plhxa__yzfv.obj = qqgys__mkd
        context.nrt.incref(builder, signature.args[0], qqgys__mkd)
        return plhxa__yzfv._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for bvcxi__czkg in keys:
        selection.remove(bvcxi__czkg)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    fwkk__dklis = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return fwkk__dklis(obj_type, by_type, as_index_type, dropna_type), codegen


@lower_builtin('groupby.count', types.VarArg(types.Any))
@lower_builtin('groupby.size', types.VarArg(types.Any))
@lower_builtin('groupby.apply', types.VarArg(types.Any))
@lower_builtin('groupby.agg', types.VarArg(types.Any))
def lower_groupby_count_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@infer
class StaticGetItemDataFrameGroupBy(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        grpby, fsi__qwan = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(fsi__qwan, (tuple, list)):
                if len(set(fsi__qwan).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(fsi__qwan).difference(set(grpby.df_type
                        .columns))))
                selection = fsi__qwan
            else:
                if fsi__qwan not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(fsi__qwan))
                selection = fsi__qwan,
                series_select = True
            dzc__wpo = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(dzc__wpo, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, fsi__qwan = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            fsi__qwan):
            dzc__wpo = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(fsi__qwan)), {}).return_type
            return signature(dzc__wpo, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    bgxzh__qhr = arr_type == ArrayItemArrayType(string_array_type)
    hqhd__lto = arr_type.dtype
    if isinstance(hqhd__lto, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {hqhd__lto} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(hqhd__lto, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {hqhd__lto} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(hqhd__lto,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(hqhd__lto, (types.Integer, types.Float, types.Boolean)):
        if bgxzh__qhr or hqhd__lto == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(hqhd__lto, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not hqhd__lto.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {hqhd__lto} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(hqhd__lto, types.Boolean) and func_name in {'cumsum',
        'sum', 'mean', 'std', 'var'}:
        return (None,
            f'groupby built-in functions {func_name} does not support boolean column'
            )
    if func_name in {'idxmin', 'idxmax'}:
        return dtype_to_array_type(get_index_data_arr_types(index_type)[0].
            dtype), 'ok'
    if func_name in {'count', 'nunique'}:
        return dtype_to_array_type(types.int64), 'ok'
    else:
        return arr_type, 'ok'


def get_pivot_output_dtype(arr_type, func_name, index_type=None):
    hqhd__lto = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(hqhd__lto, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(hqhd__lto, types.Integer):
            return IntDtype(hqhd__lto)
        return hqhd__lto
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        mht__copq = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{mht__copq}'."
            )
    elif len(args) > len_args:
        raise BodoError(
            f'Groupby.{func_name}() takes {len_args + 1} positional argument but {len(args)} were given.'
            )


class ColumnType(Enum):
    KeyColumn = 0
    NumericalColumn = 1
    NonNumericalColumn = 2


def get_keys_not_as_index(grp, out_columns, out_data, out_column_type,
    multi_level_names=False):
    for bvcxi__czkg in grp.keys:
        if multi_level_names:
            kmz__oxfvx = bvcxi__czkg, ''
        else:
            kmz__oxfvx = bvcxi__czkg
        cqzor__daf = grp.df_type.columns.index(bvcxi__czkg)
        data = to_str_arr_if_dict_array(grp.df_type.data[cqzor__daf])
        out_columns.append(kmz__oxfvx)
        out_data.append(data)
        out_column_type.append(ColumnType.KeyColumn.value)


def get_agg_typ(grp, args, func_name, typing_context, target_context, func=
    None, kws=None):
    index = RangeIndexType(types.none)
    out_data = []
    out_columns = []
    out_column_type = []
    if func_name == 'head':
        grp.as_index = True
    if not grp.as_index:
        get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
    elif func_name == 'head':
        if grp.df_type.index == index:
            index = NumericIndexType(types.int64, types.none)
        else:
            index = grp.df_type.index
    elif len(grp.keys) > 1:
        lru__txal = tuple(grp.df_type.columns.index(grp.keys[vagq__dpc]) for
            vagq__dpc in range(len(grp.keys)))
        nppho__ouk = tuple(grp.df_type.data[cqzor__daf] for cqzor__daf in
            lru__txal)
        nppho__ouk = tuple(to_str_arr_if_dict_array(bnj__uktqo) for
            bnj__uktqo in nppho__ouk)
        index = MultiIndexType(nppho__ouk, tuple(types.StringLiteral(
            bvcxi__czkg) for bvcxi__czkg in grp.keys))
    else:
        cqzor__daf = grp.df_type.columns.index(grp.keys[0])
        nqki__qdgkm = to_str_arr_if_dict_array(grp.df_type.data[cqzor__daf])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(nqki__qdgkm,
            types.StringLiteral(grp.keys[0]))
    nwtg__kjfj = {}
    cgwp__yptoi = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        nwtg__kjfj[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for gza__kgcy in columns:
            cqzor__daf = grp.df_type.columns.index(gza__kgcy)
            data = grp.df_type.data[cqzor__daf]
            data = to_str_arr_if_dict_array(data)
            qbfyn__bqlup = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                qbfyn__bqlup = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    efurx__gtjco = SeriesType(data.dtype, data, None,
                        string_type)
                    koc__rdtik = get_const_func_output_type(func, (
                        efurx__gtjco,), {}, typing_context, target_context)
                    if koc__rdtik != ArrayItemArrayType(string_array_type):
                        koc__rdtik = dtype_to_array_type(koc__rdtik)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=gza__kgcy, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    fde__zikzt = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    gnkol__ufiz = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    lte__xho = dict(numeric_only=fde__zikzt, min_count=
                        gnkol__ufiz)
                    jks__rhgpm = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}', lte__xho,
                        jks__rhgpm, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    fde__zikzt = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    gnkol__ufiz = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    lte__xho = dict(numeric_only=fde__zikzt, min_count=
                        gnkol__ufiz)
                    jks__rhgpm = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}', lte__xho,
                        jks__rhgpm, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    fde__zikzt = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    lte__xho = dict(numeric_only=fde__zikzt)
                    jks__rhgpm = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}', lte__xho,
                        jks__rhgpm, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    vsz__epgiy = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    quz__wauo = args[1] if len(args) > 1 else kws.pop('skipna',
                        True)
                    lte__xho = dict(axis=vsz__epgiy, skipna=quz__wauo)
                    jks__rhgpm = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}', lte__xho,
                        jks__rhgpm, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    cpmou__utqq = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    lte__xho = dict(ddof=cpmou__utqq)
                    jks__rhgpm = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}', lte__xho,
                        jks__rhgpm, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                koc__rdtik, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                fygfz__mljsf = to_str_arr_if_dict_array(koc__rdtik)
                out_data.append(fygfz__mljsf)
                out_columns.append(gza__kgcy)
                if func_name == 'agg':
                    ptj__qmf = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    nwtg__kjfj[gza__kgcy, ptj__qmf] = gza__kgcy
                else:
                    nwtg__kjfj[gza__kgcy, func_name] = gza__kgcy
                out_column_type.append(qbfyn__bqlup)
            else:
                cgwp__yptoi.append(err_msg)
    if func_name == 'sum':
        ivaej__yeyj = any([(qyk__wwdhq == ColumnType.NumericalColumn.value) for
            qyk__wwdhq in out_column_type])
        if ivaej__yeyj:
            out_data = [qyk__wwdhq for qyk__wwdhq, tviq__ehuxk in zip(
                out_data, out_column_type) if tviq__ehuxk != ColumnType.
                NonNumericalColumn.value]
            out_columns = [qyk__wwdhq for qyk__wwdhq, tviq__ehuxk in zip(
                out_columns, out_column_type) if tviq__ehuxk != ColumnType.
                NonNumericalColumn.value]
            nwtg__kjfj = {}
            for gza__kgcy in out_columns:
                if grp.as_index is False and gza__kgcy in grp.keys:
                    continue
                nwtg__kjfj[gza__kgcy, func_name] = gza__kgcy
    rhhjz__jjf = len(cgwp__yptoi)
    if len(out_data) == 0:
        if rhhjz__jjf == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(rhhjz__jjf, ' was' if rhhjz__jjf == 1 else 's were',
                ','.join(cgwp__yptoi)))
    tqbls__fkm = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            ntsm__bbiib = IntDtype(out_data[0].dtype)
        else:
            ntsm__bbiib = out_data[0].dtype
        udv__hdkjz = (types.none if func_name == 'size' else types.
            StringLiteral(grp.selection[0]))
        tqbls__fkm = SeriesType(ntsm__bbiib, index=index, name_typ=udv__hdkjz)
    return signature(tqbls__fkm, *args), nwtg__kjfj


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    bfgd__annzq = True
    if isinstance(f_val, str):
        bfgd__annzq = False
        zujf__ofwwo = f_val
    elif is_overload_constant_str(f_val):
        bfgd__annzq = False
        zujf__ofwwo = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        bfgd__annzq = False
        zujf__ofwwo = bodo.utils.typing.get_builtin_function_name(f_val)
    if not bfgd__annzq:
        if zujf__ofwwo not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {zujf__ofwwo}')
        dzc__wpo = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp.
            as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(dzc__wpo, (), zujf__ofwwo, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            ecmg__caje = types.functions.MakeFunctionLiteral(f_val)
        else:
            ecmg__caje = f_val
        validate_udf('agg', ecmg__caje)
        func = get_overload_const_func(ecmg__caje, None)
        ozg__ecla = func.code if hasattr(func, 'code') else func.__code__
        zujf__ofwwo = ozg__ecla.co_name
        dzc__wpo = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp.
            as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(dzc__wpo, (), 'agg', typing_context,
            target_context, ecmg__caje)[0].return_type
    return zujf__ofwwo, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    eboq__kbknz = kws and all(isinstance(mdx__xmq, types.Tuple) and len(
        mdx__xmq) == 2 for mdx__xmq in kws.values())
    if is_overload_none(func) and not eboq__kbknz:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not eboq__kbknz:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    wtt__zcrg = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if eboq__kbknz or is_overload_constant_dict(func):
        if eboq__kbknz:
            hjppj__new = [get_literal_value(lbhda__eczza) for lbhda__eczza,
                vrv__atog in kws.values()]
            jrqo__rygqg = [get_literal_value(nnnth__kshbd) for vrv__atog,
                nnnth__kshbd in kws.values()]
        else:
            uhw__pagy = get_overload_constant_dict(func)
            hjppj__new = tuple(uhw__pagy.keys())
            jrqo__rygqg = tuple(uhw__pagy.values())
        if 'head' in jrqo__rygqg:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(gza__kgcy not in grp.selection and gza__kgcy not in grp.keys for
            gza__kgcy in hjppj__new):
            raise_bodo_error(
                f'Selected column names {hjppj__new} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            jrqo__rygqg)
        if eboq__kbknz and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        nwtg__kjfj = {}
        out_columns = []
        out_data = []
        out_column_type = []
        luhm__wqusz = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for yhnd__dst, f_val in zip(hjppj__new, jrqo__rygqg):
            if isinstance(f_val, (tuple, list)):
                nnbo__fra = 0
                for ecmg__caje in f_val:
                    zujf__ofwwo, out_tp = get_agg_funcname_and_outtyp(grp,
                        yhnd__dst, ecmg__caje, typing_context, target_context)
                    wtt__zcrg = zujf__ofwwo in list_cumulative
                    if zujf__ofwwo == '<lambda>' and len(f_val) > 1:
                        zujf__ofwwo = '<lambda_' + str(nnbo__fra) + '>'
                        nnbo__fra += 1
                    out_columns.append((yhnd__dst, zujf__ofwwo))
                    nwtg__kjfj[yhnd__dst, zujf__ofwwo] = yhnd__dst, zujf__ofwwo
                    _append_out_type(grp, out_data, out_tp)
            else:
                zujf__ofwwo, out_tp = get_agg_funcname_and_outtyp(grp,
                    yhnd__dst, f_val, typing_context, target_context)
                wtt__zcrg = zujf__ofwwo in list_cumulative
                if multi_level_names:
                    out_columns.append((yhnd__dst, zujf__ofwwo))
                    nwtg__kjfj[yhnd__dst, zujf__ofwwo] = yhnd__dst, zujf__ofwwo
                elif not eboq__kbknz:
                    out_columns.append(yhnd__dst)
                    nwtg__kjfj[yhnd__dst, zujf__ofwwo] = yhnd__dst
                elif eboq__kbknz:
                    luhm__wqusz.append(zujf__ofwwo)
                _append_out_type(grp, out_data, out_tp)
        if eboq__kbknz:
            for vagq__dpc, ruxed__nbbv in enumerate(kws.keys()):
                out_columns.append(ruxed__nbbv)
                nwtg__kjfj[hjppj__new[vagq__dpc], luhm__wqusz[vagq__dpc]
                    ] = ruxed__nbbv
        if wtt__zcrg:
            index = grp.df_type.index
        else:
            index = out_tp.index
        tqbls__fkm = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(tqbls__fkm, *args), nwtg__kjfj
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one functions supplied'
                )
        assert len(func) > 0
        out_data = []
        out_columns = []
        out_column_type = []
        nnbo__fra = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        nwtg__kjfj = {}
        cpxhe__nqeje = grp.selection[0]
        for f_val in func.types:
            zujf__ofwwo, out_tp = get_agg_funcname_and_outtyp(grp,
                cpxhe__nqeje, f_val, typing_context, target_context)
            wtt__zcrg = zujf__ofwwo in list_cumulative
            if zujf__ofwwo == '<lambda>':
                zujf__ofwwo = '<lambda_' + str(nnbo__fra) + '>'
                nnbo__fra += 1
            out_columns.append(zujf__ofwwo)
            nwtg__kjfj[cpxhe__nqeje, zujf__ofwwo] = zujf__ofwwo
            _append_out_type(grp, out_data, out_tp)
        if wtt__zcrg:
            index = grp.df_type.index
        else:
            index = out_tp.index
        tqbls__fkm = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(tqbls__fkm, *args), nwtg__kjfj
    zujf__ofwwo = ''
    if types.unliteral(func) == types.unicode_type:
        zujf__ofwwo = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        zujf__ofwwo = bodo.utils.typing.get_builtin_function_name(func)
    if zujf__ofwwo:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, zujf__ofwwo, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        vsz__epgiy = args[0] if len(args) > 0 else kws.pop('axis', 0)
        fde__zikzt = args[1] if len(args) > 1 else kws.pop('numeric_only', 
            False)
        quz__wauo = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        lte__xho = dict(axis=vsz__epgiy, numeric_only=fde__zikzt)
        jks__rhgpm = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', lte__xho,
            jks__rhgpm, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        ttrhl__oqy = args[0] if len(args) > 0 else kws.pop('periods', 1)
        hcmpn__rmfoo = args[1] if len(args) > 1 else kws.pop('freq', None)
        vsz__epgiy = args[2] if len(args) > 2 else kws.pop('axis', 0)
        mug__klw = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        lte__xho = dict(freq=hcmpn__rmfoo, axis=vsz__epgiy, fill_value=mug__klw
            )
        jks__rhgpm = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', lte__xho,
            jks__rhgpm, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        put__hihk = args[0] if len(args) > 0 else kws.pop('func', None)
        lcp__ochq = kws.pop('engine', None)
        edp__eeojf = kws.pop('engine_kwargs', None)
        lte__xho = dict(engine=lcp__ochq, engine_kwargs=edp__eeojf)
        jks__rhgpm = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', lte__xho, jks__rhgpm,
            package_name='pandas', module_name='GroupBy')
    nwtg__kjfj = {}
    for gza__kgcy in grp.selection:
        out_columns.append(gza__kgcy)
        nwtg__kjfj[gza__kgcy, name_operation] = gza__kgcy
        cqzor__daf = grp.df_type.columns.index(gza__kgcy)
        data = grp.df_type.data[cqzor__daf]
        data = to_str_arr_if_dict_array(data)
        if name_operation == 'cumprod':
            if not isinstance(data.dtype, (types.Integer, types.Float)):
                raise BodoError(msg)
        if name_operation == 'cumsum':
            if data.dtype != types.unicode_type and data != ArrayItemArrayType(
                string_array_type) and not isinstance(data.dtype, (types.
                Integer, types.Float)):
                raise BodoError(msg)
        if name_operation in ('cummin', 'cummax'):
            if not isinstance(data.dtype, types.Integer
                ) and not is_dtype_nullable(data.dtype):
                raise BodoError(msg)
        if name_operation == 'shift':
            if isinstance(data, (TupleArrayType, ArrayItemArrayType)):
                raise BodoError(msg)
            if isinstance(data.dtype, bodo.hiframes.datetime_timedelta_ext.
                DatetimeTimeDeltaType):
                raise BodoError(
                    f"""column type of {data.dtype} is not supported in groupby built-in function shift.
{dt_err}"""
                    )
        if name_operation == 'transform':
            koc__rdtik, err_msg = get_groupby_output_dtype(data,
                get_literal_value(put__hihk), grp.df_type.index)
            if err_msg == 'ok':
                data = koc__rdtik
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    tqbls__fkm = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        tqbls__fkm = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(tqbls__fkm, *args), nwtg__kjfj


def resolve_gb(grp, args, kws, func_name, typing_context, target_context,
    err_msg=''):
    if func_name in set(list_cumulative) | {'shift', 'transform'}:
        return resolve_transformative(grp, args, kws, err_msg, func_name)
    elif func_name in {'agg', 'aggregate'}:
        return resolve_agg(grp, args, kws, typing_context, target_context)
    else:
        return get_agg_typ(grp, args, func_name, typing_context,
            target_context, kws=kws)


@infer_getattr
class DataframeGroupByAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameGroupByType
    _attr_set = None

    @bound_function('groupby.agg', no_unliteral=True)
    def resolve_agg(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.aggregate', no_unliteral=True)
    def resolve_aggregate(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.sum', no_unliteral=True)
    def resolve_sum(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'sum', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.count', no_unliteral=True)
    def resolve_count(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'count', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.nunique', no_unliteral=True)
    def resolve_nunique(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'nunique', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.median', no_unliteral=True)
    def resolve_median(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'median', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.mean', no_unliteral=True)
    def resolve_mean(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'mean', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.min', no_unliteral=True)
    def resolve_min(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'min', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.max', no_unliteral=True)
    def resolve_max(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'max', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.prod', no_unliteral=True)
    def resolve_prod(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'prod', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.var', no_unliteral=True)
    def resolve_var(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'var', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.std', no_unliteral=True)
    def resolve_std(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'std', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.first', no_unliteral=True)
    def resolve_first(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'first', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.last', no_unliteral=True)
    def resolve_last(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'last', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmin', no_unliteral=True)
    def resolve_idxmin(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmin', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmax', no_unliteral=True)
    def resolve_idxmax(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmax', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.size', no_unliteral=True)
    def resolve_size(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'size', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.cumsum', no_unliteral=True)
    def resolve_cumsum(self, grp, args, kws):
        msg = (
            'Groupby.cumsum() only supports columns of types integer, float, string or liststring'
            )
        return resolve_gb(grp, args, kws, 'cumsum', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cumprod', no_unliteral=True)
    def resolve_cumprod(self, grp, args, kws):
        msg = (
            'Groupby.cumprod() only supports columns of types integer and float'
            )
        return resolve_gb(grp, args, kws, 'cumprod', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummin', no_unliteral=True)
    def resolve_cummin(self, grp, args, kws):
        msg = (
            'Groupby.cummin() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummin', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummax', no_unliteral=True)
    def resolve_cummax(self, grp, args, kws):
        msg = (
            'Groupby.cummax() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummax', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.shift', no_unliteral=True)
    def resolve_shift(self, grp, args, kws):
        msg = (
            'Column type of list/tuple is not supported in groupby built-in function shift'
            )
        return resolve_gb(grp, args, kws, 'shift', self.context, numba.core
            .registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.pipe', no_unliteral=True)
    def resolve_pipe(self, grp, args, kws):
        return resolve_obj_pipe(self, grp, args, kws, 'GroupBy')

    @bound_function('groupby.transform', no_unliteral=True)
    def resolve_transform(self, grp, args, kws):
        msg = (
            'Groupby.transform() only supports sum, count, min, max, mean, and std operations'
            )
        return resolve_gb(grp, args, kws, 'transform', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.head', no_unliteral=True)
    def resolve_head(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'head', self.context, numba.core.
            registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.apply', no_unliteral=True)
    def resolve_apply(self, grp, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws.pop('func', None)
        f_args = tuple(args[1:]) if len(args) > 0 else ()
        nlz__zkj = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        soqe__icnnx = isinstance(nlz__zkj, (SeriesType,
            HeterogeneousSeriesType)
            ) and nlz__zkj.const_info is not None or not isinstance(nlz__zkj,
            (SeriesType, DataFrameType))
        if soqe__icnnx:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                syygg__gpzm = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                lru__txal = tuple(grp.df_type.columns.index(grp.keys[
                    vagq__dpc]) for vagq__dpc in range(len(grp.keys)))
                nppho__ouk = tuple(grp.df_type.data[cqzor__daf] for
                    cqzor__daf in lru__txal)
                nppho__ouk = tuple(to_str_arr_if_dict_array(bnj__uktqo) for
                    bnj__uktqo in nppho__ouk)
                syygg__gpzm = MultiIndexType(nppho__ouk, tuple(types.
                    literal(bvcxi__czkg) for bvcxi__czkg in grp.keys))
            else:
                cqzor__daf = grp.df_type.columns.index(grp.keys[0])
                nqki__qdgkm = grp.df_type.data[cqzor__daf]
                nqki__qdgkm = to_str_arr_if_dict_array(nqki__qdgkm)
                syygg__gpzm = bodo.hiframes.pd_index_ext.array_type_to_index(
                    nqki__qdgkm, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            lhsa__yyut = tuple(grp.df_type.data[grp.df_type.columns.index(
                gza__kgcy)] for gza__kgcy in grp.keys)
            lhsa__yyut = tuple(to_str_arr_if_dict_array(bnj__uktqo) for
                bnj__uktqo in lhsa__yyut)
            wli__bqy = tuple(types.literal(mdx__xmq) for mdx__xmq in grp.keys
                ) + get_index_name_types(nlz__zkj.index)
            if not grp.as_index:
                lhsa__yyut = types.Array(types.int64, 1, 'C'),
                wli__bqy = (types.none,) + get_index_name_types(nlz__zkj.index)
            syygg__gpzm = MultiIndexType(lhsa__yyut +
                get_index_data_arr_types(nlz__zkj.index), wli__bqy)
        if soqe__icnnx:
            if isinstance(nlz__zkj, HeterogeneousSeriesType):
                vrv__atog, nmto__cjfw = nlz__zkj.const_info
                if isinstance(nlz__zkj.data, bodo.libs.nullable_tuple_ext.
                    NullableTupleType):
                    dik__wqype = nlz__zkj.data.tuple_typ.types
                elif isinstance(nlz__zkj.data, types.Tuple):
                    dik__wqype = nlz__zkj.data.types
                rvskp__cfq = tuple(to_nullable_type(dtype_to_array_type(
                    bnj__uktqo)) for bnj__uktqo in dik__wqype)
                sgu__jcwhv = DataFrameType(out_data + rvskp__cfq,
                    syygg__gpzm, out_columns + nmto__cjfw)
            elif isinstance(nlz__zkj, SeriesType):
                eyo__oqof, nmto__cjfw = nlz__zkj.const_info
                rvskp__cfq = tuple(to_nullable_type(dtype_to_array_type(
                    nlz__zkj.dtype)) for vrv__atog in range(eyo__oqof))
                sgu__jcwhv = DataFrameType(out_data + rvskp__cfq,
                    syygg__gpzm, out_columns + nmto__cjfw)
            else:
                mcc__jwxi = get_udf_out_arr_type(nlz__zkj)
                if not grp.as_index:
                    sgu__jcwhv = DataFrameType(out_data + (mcc__jwxi,),
                        syygg__gpzm, out_columns + ('',))
                else:
                    sgu__jcwhv = SeriesType(mcc__jwxi.dtype, mcc__jwxi,
                        syygg__gpzm, None)
        elif isinstance(nlz__zkj, SeriesType):
            sgu__jcwhv = SeriesType(nlz__zkj.dtype, nlz__zkj.data,
                syygg__gpzm, nlz__zkj.name_typ)
        else:
            sgu__jcwhv = DataFrameType(nlz__zkj.data, syygg__gpzm, nlz__zkj
                .columns)
        hgsp__oixm = gen_apply_pysig(len(f_args), kws.keys())
        ztj__hzmhz = (func, *f_args) + tuple(kws.values())
        return signature(sgu__jcwhv, *ztj__hzmhz).replace(pysig=hgsp__oixm)

    def generic_resolve(self, grpby, attr):
        if self._is_existing_attr(attr):
            return
        if attr not in grpby.df_type.columns:
            raise_bodo_error(
                f'groupby: invalid attribute {attr} (column not found in dataframe or unsupported function)'
                )
        return DataFrameGroupByType(grpby.df_type, grpby.keys, (attr,),
            grpby.as_index, grpby.dropna, True, True)


def _get_groupby_apply_udf_out_type(func, grp, f_args, kws, typing_context,
    target_context):
    atse__nbi = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            yhnd__dst = grp.selection[0]
            mcc__jwxi = atse__nbi.data[atse__nbi.columns.index(yhnd__dst)]
            mcc__jwxi = to_str_arr_if_dict_array(mcc__jwxi)
            kycs__gxemd = SeriesType(mcc__jwxi.dtype, mcc__jwxi, atse__nbi.
                index, types.literal(yhnd__dst))
        else:
            lvtr__xewcf = tuple(atse__nbi.data[atse__nbi.columns.index(
                gza__kgcy)] for gza__kgcy in grp.selection)
            lvtr__xewcf = tuple(to_str_arr_if_dict_array(bnj__uktqo) for
                bnj__uktqo in lvtr__xewcf)
            kycs__gxemd = DataFrameType(lvtr__xewcf, atse__nbi.index, tuple
                (grp.selection))
    else:
        kycs__gxemd = atse__nbi
    rlqr__pxk = kycs__gxemd,
    rlqr__pxk += tuple(f_args)
    try:
        nlz__zkj = get_const_func_output_type(func, rlqr__pxk, kws,
            typing_context, target_context)
    except Exception as gxiwa__bsgfh:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', gxiwa__bsgfh),
            getattr(gxiwa__bsgfh, 'loc', None))
    return nlz__zkj


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    rlqr__pxk = (grp,) + f_args
    try:
        nlz__zkj = get_const_func_output_type(func, rlqr__pxk, kws, self.
            context, numba.core.registry.cpu_target.target_context, False)
    except Exception as gxiwa__bsgfh:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()',
            gxiwa__bsgfh), getattr(gxiwa__bsgfh, 'loc', None))
    hgsp__oixm = gen_apply_pysig(len(f_args), kws.keys())
    ztj__hzmhz = (func, *f_args) + tuple(kws.values())
    return signature(nlz__zkj, *ztj__hzmhz).replace(pysig=hgsp__oixm)


def gen_apply_pysig(n_args, kws):
    gzmx__lfgay = ', '.join(f'arg{vagq__dpc}' for vagq__dpc in range(n_args))
    gzmx__lfgay = gzmx__lfgay + ', ' if gzmx__lfgay else ''
    bvzx__wrms = ', '.join(f"{lrkt__kjqy} = ''" for lrkt__kjqy in kws)
    fbpbc__csdj = f'def apply_stub(func, {gzmx__lfgay}{bvzx__wrms}):\n'
    fbpbc__csdj += '    pass\n'
    pxac__pejyd = {}
    exec(fbpbc__csdj, {}, pxac__pejyd)
    eeigm__oayu = pxac__pejyd['apply_stub']
    return numba.core.utils.pysignature(eeigm__oayu)


def pivot_table_dummy(df, values, index, columns, aggfunc, _pivot_values):
    return 0


@infer_global(pivot_table_dummy)
class PivotTableTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, values, index, columns, aggfunc, _pivot_values = args
        if not (is_overload_constant_str(values) and
            is_overload_constant_str(index) and is_overload_constant_str(
            columns)):
            raise BodoError(
                "pivot_table() only support string constants for 'values', 'index' and 'columns' arguments"
                )
        values = values.literal_value
        index = index.literal_value
        columns = columns.literal_value
        data = df.data[df.columns.index(values)]
        data = to_str_arr_if_dict_array(data)
        koc__rdtik = get_pivot_output_dtype(data, aggfunc.literal_value)
        wgfwv__upqo = dtype_to_array_type(koc__rdtik)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/pandas.html'
                )
        wbph__sdkin = _pivot_values.meta
        rfq__yqyk = len(wbph__sdkin)
        cqzor__daf = df.columns.index(index)
        nqki__qdgkm = df.data[cqzor__daf]
        nqki__qdgkm = to_str_arr_if_dict_array(nqki__qdgkm)
        pafl__vvrbi = bodo.hiframes.pd_index_ext.array_type_to_index(
            nqki__qdgkm, types.StringLiteral(index))
        nnf__gjz = DataFrameType((wgfwv__upqo,) * rfq__yqyk, pafl__vvrbi,
            tuple(wbph__sdkin))
        return signature(nnf__gjz, *args)


PivotTableTyper._no_unliteral = True


@lower_builtin(pivot_table_dummy, types.VarArg(types.Any))
def lower_pivot_table_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        wgfwv__upqo = types.Array(types.int64, 1, 'C')
        wbph__sdkin = _pivot_values.meta
        rfq__yqyk = len(wbph__sdkin)
        pafl__vvrbi = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        nnf__gjz = DataFrameType((wgfwv__upqo,) * rfq__yqyk, pafl__vvrbi,
            tuple(wbph__sdkin))
        return signature(nnf__gjz, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    fbpbc__csdj = 'def impl(keys, dropna, _is_parallel):\n'
    fbpbc__csdj += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    fbpbc__csdj += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{vagq__dpc}])' for vagq__dpc in range(len(keys
        .types))))
    fbpbc__csdj += '    table = arr_info_list_to_table(info_list)\n'
    fbpbc__csdj += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    fbpbc__csdj += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    fbpbc__csdj += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    fbpbc__csdj += '    delete_table_decref_arrays(table)\n'
    fbpbc__csdj += '    ev.finalize()\n'
    fbpbc__csdj += '    return sort_idx, group_labels, ngroups\n'
    pxac__pejyd = {}
    exec(fbpbc__csdj, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, pxac__pejyd)
    supwc__nbmp = pxac__pejyd['impl']
    return supwc__nbmp


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    obxq__vozsz = len(labels)
    yomyt__njhcm = np.zeros(ngroups, dtype=np.int64)
    zhr__ypzh = np.zeros(ngroups, dtype=np.int64)
    vff__ybp = 0
    oflst__dwr = 0
    for vagq__dpc in range(obxq__vozsz):
        ygkl__aiih = labels[vagq__dpc]
        if ygkl__aiih < 0:
            vff__ybp += 1
        else:
            oflst__dwr += 1
            if vagq__dpc == obxq__vozsz - 1 or ygkl__aiih != labels[
                vagq__dpc + 1]:
                yomyt__njhcm[ygkl__aiih] = vff__ybp
                zhr__ypzh[ygkl__aiih] = vff__ybp + oflst__dwr
                vff__ybp += oflst__dwr
                oflst__dwr = 0
    return yomyt__njhcm, zhr__ypzh


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    supwc__nbmp, vrv__atog = gen_shuffle_dataframe(df, keys, _is_parallel)
    return supwc__nbmp


def gen_shuffle_dataframe(df, keys, _is_parallel):
    eyo__oqof = len(df.columns)
    lkop__uuzb = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    fbpbc__csdj = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        fbpbc__csdj += '  return df, keys, get_null_shuffle_info()\n'
        pxac__pejyd = {}
        exec(fbpbc__csdj, {'get_null_shuffle_info': get_null_shuffle_info},
            pxac__pejyd)
        supwc__nbmp = pxac__pejyd['impl']
        return supwc__nbmp
    for vagq__dpc in range(eyo__oqof):
        fbpbc__csdj += f"""  in_arr{vagq__dpc} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {vagq__dpc})
"""
    fbpbc__csdj += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    fbpbc__csdj += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{vagq__dpc}])' for vagq__dpc in range(
        lkop__uuzb)), ', '.join(f'array_to_info(in_arr{vagq__dpc})' for
        vagq__dpc in range(eyo__oqof)), 'array_to_info(in_index_arr)')
    fbpbc__csdj += '  table = arr_info_list_to_table(info_list)\n'
    fbpbc__csdj += (
        f'  out_table = shuffle_table(table, {lkop__uuzb}, _is_parallel, 1)\n')
    for vagq__dpc in range(lkop__uuzb):
        fbpbc__csdj += f"""  out_key{vagq__dpc} = info_to_array(info_from_table(out_table, {vagq__dpc}), keys{vagq__dpc}_typ)
"""
    for vagq__dpc in range(eyo__oqof):
        fbpbc__csdj += f"""  out_arr{vagq__dpc} = info_to_array(info_from_table(out_table, {vagq__dpc + lkop__uuzb}), in_arr{vagq__dpc}_typ)
"""
    fbpbc__csdj += f"""  out_arr_index = info_to_array(info_from_table(out_table, {lkop__uuzb + eyo__oqof}), ind_arr_typ)
"""
    fbpbc__csdj += '  shuffle_info = get_shuffle_info(out_table)\n'
    fbpbc__csdj += '  delete_table(out_table)\n'
    fbpbc__csdj += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{vagq__dpc}' for vagq__dpc in range(
        eyo__oqof))
    fbpbc__csdj += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    fbpbc__csdj += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    fbpbc__csdj += '  return out_df, ({},), shuffle_info\n'.format(', '.
        join(f'out_key{vagq__dpc}' for vagq__dpc in range(lkop__uuzb)))
    azssa__qlr = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    azssa__qlr.update({f'keys{vagq__dpc}_typ': keys.types[vagq__dpc] for
        vagq__dpc in range(lkop__uuzb)})
    azssa__qlr.update({f'in_arr{vagq__dpc}_typ': df.data[vagq__dpc] for
        vagq__dpc in range(eyo__oqof)})
    pxac__pejyd = {}
    exec(fbpbc__csdj, azssa__qlr, pxac__pejyd)
    supwc__nbmp = pxac__pejyd['impl']
    return supwc__nbmp, azssa__qlr


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        xtln__ybxmb = len(data.array_types)
        fbpbc__csdj = 'def impl(data, shuffle_info):\n'
        fbpbc__csdj += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{vagq__dpc}])' for vagq__dpc in
            range(xtln__ybxmb)))
        fbpbc__csdj += '  table = arr_info_list_to_table(info_list)\n'
        fbpbc__csdj += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for vagq__dpc in range(xtln__ybxmb):
            fbpbc__csdj += f"""  out_arr{vagq__dpc} = info_to_array(info_from_table(out_table, {vagq__dpc}), data._data[{vagq__dpc}])
"""
        fbpbc__csdj += '  delete_table(out_table)\n'
        fbpbc__csdj += '  delete_table(table)\n'
        fbpbc__csdj += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{vagq__dpc}' for vagq__dpc in range(
            xtln__ybxmb))))
        pxac__pejyd = {}
        exec(fbpbc__csdj, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, pxac__pejyd)
        supwc__nbmp = pxac__pejyd['impl']
        return supwc__nbmp
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            ggcr__wbvdr = bodo.utils.conversion.index_to_array(data)
            fygfz__mljsf = reverse_shuffle(ggcr__wbvdr, shuffle_info)
            return bodo.utils.conversion.index_from_array(fygfz__mljsf)
        return impl_index

    def impl_arr(data, shuffle_info):
        vzsfa__ujq = [array_to_info(data)]
        brblk__hljh = arr_info_list_to_table(vzsfa__ujq)
        aitq__jbrf = reverse_shuffle_table(brblk__hljh, shuffle_info)
        fygfz__mljsf = info_to_array(info_from_table(aitq__jbrf, 0), data)
        delete_table(aitq__jbrf)
        delete_table(brblk__hljh)
        return fygfz__mljsf
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    lte__xho = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    jks__rhgpm = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', lte__xho, jks__rhgpm,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    rxyir__qemut = get_overload_const_bool(ascending)
    vsuw__rlro = grp.selection[0]
    fbpbc__csdj = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    onmh__pjru = (
        f"lambda S: S.value_counts(ascending={rxyir__qemut}, _index_name='{vsuw__rlro}')"
        )
    fbpbc__csdj += f'    return grp.apply({onmh__pjru})\n'
    pxac__pejyd = {}
    exec(fbpbc__csdj, {'bodo': bodo}, pxac__pejyd)
    supwc__nbmp = pxac__pejyd['impl']
    return supwc__nbmp


groupby_unsupported_attr = {'groups', 'indices'}
groupby_unsupported = {'__iter__', 'get_group', 'all', 'any', 'bfill',
    'backfill', 'cumcount', 'cummax', 'cummin', 'cumprod', 'ffill',
    'ngroup', 'nth', 'ohlc', 'pad', 'rank', 'pct_change', 'sem', 'tail',
    'corr', 'cov', 'describe', 'diff', 'fillna', 'filter', 'hist', 'mad',
    'plot', 'quantile', 'resample', 'sample', 'skew', 'take', 'tshift'}
series_only_unsupported_attrs = {'is_monotonic_increasing',
    'is_monotonic_decreasing'}
series_only_unsupported = {'nlargest', 'nsmallest', 'unique'}
dataframe_only_unsupported = {'corrwith', 'boxplot'}


def _install_groupby_unsupported():
    for ydpz__ecpo in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, ydpz__ecpo, no_unliteral=True
            )(create_unsupported_overload(f'DataFrameGroupBy.{ydpz__ecpo}'))
    for ydpz__ecpo in groupby_unsupported:
        overload_method(DataFrameGroupByType, ydpz__ecpo, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{ydpz__ecpo}'))
    for ydpz__ecpo in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, ydpz__ecpo, no_unliteral=True
            )(create_unsupported_overload(f'SeriesGroupBy.{ydpz__ecpo}'))
    for ydpz__ecpo in series_only_unsupported:
        overload_method(DataFrameGroupByType, ydpz__ecpo, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{ydpz__ecpo}'))
    for ydpz__ecpo in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, ydpz__ecpo, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{ydpz__ecpo}'))


_install_groupby_unsupported()
