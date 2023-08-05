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
        dltu__ejn = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, dltu__ejn)


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
        fvi__qxy = args[0]
        dpgm__crd = signature.return_type
        rfd__jxq = cgutils.create_struct_proxy(dpgm__crd)(context, builder)
        rfd__jxq.obj = fvi__qxy
        context.nrt.incref(builder, signature.args[0], fvi__qxy)
        return rfd__jxq._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for azgkr__lbb in keys:
        selection.remove(azgkr__lbb)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    dpgm__crd = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return dpgm__crd(obj_type, by_type, as_index_type, dropna_type), codegen


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
        grpby, lwrte__zqqg = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(lwrte__zqqg, (tuple, list)):
                if len(set(lwrte__zqqg).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(lwrte__zqqg).difference(set(grpby.
                        df_type.columns))))
                selection = lwrte__zqqg
            else:
                if lwrte__zqqg not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(lwrte__zqqg))
                selection = lwrte__zqqg,
                series_select = True
            jwhtp__qhe = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(jwhtp__qhe, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, lwrte__zqqg = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            lwrte__zqqg):
            jwhtp__qhe = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(lwrte__zqqg)), {}).return_type
            return signature(jwhtp__qhe, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    fxbn__iauy = arr_type == ArrayItemArrayType(string_array_type)
    ehts__jbv = arr_type.dtype
    if isinstance(ehts__jbv, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {ehts__jbv} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(ehts__jbv, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {ehts__jbv} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(ehts__jbv,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(ehts__jbv, (types.Integer, types.Float, types.Boolean)):
        if fxbn__iauy or ehts__jbv == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(ehts__jbv, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not ehts__jbv.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {ehts__jbv} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(ehts__jbv, types.Boolean) and func_name in {'cumsum',
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
    ehts__jbv = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(ehts__jbv, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(ehts__jbv, types.Integer):
            return IntDtype(ehts__jbv)
        return ehts__jbv
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        chu__auf = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{chu__auf}'."
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
    for azgkr__lbb in grp.keys:
        if multi_level_names:
            lvxw__gvp = azgkr__lbb, ''
        else:
            lvxw__gvp = azgkr__lbb
        wcdbe__tsgbh = grp.df_type.columns.index(azgkr__lbb)
        data = to_str_arr_if_dict_array(grp.df_type.data[wcdbe__tsgbh])
        out_columns.append(lvxw__gvp)
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
        toj__wap = tuple(grp.df_type.columns.index(grp.keys[dphva__yat]) for
            dphva__yat in range(len(grp.keys)))
        qpcu__uzda = tuple(grp.df_type.data[wcdbe__tsgbh] for wcdbe__tsgbh in
            toj__wap)
        qpcu__uzda = tuple(to_str_arr_if_dict_array(sed__kwz) for sed__kwz in
            qpcu__uzda)
        index = MultiIndexType(qpcu__uzda, tuple(types.StringLiteral(
            azgkr__lbb) for azgkr__lbb in grp.keys))
    else:
        wcdbe__tsgbh = grp.df_type.columns.index(grp.keys[0])
        chp__omh = to_str_arr_if_dict_array(grp.df_type.data[wcdbe__tsgbh])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(chp__omh,
            types.StringLiteral(grp.keys[0]))
    ejlb__iigzm = {}
    zmy__chrla = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        ejlb__iigzm[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for bumvk__vxiwm in columns:
            wcdbe__tsgbh = grp.df_type.columns.index(bumvk__vxiwm)
            data = grp.df_type.data[wcdbe__tsgbh]
            data = to_str_arr_if_dict_array(data)
            pumv__mkft = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                pumv__mkft = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    nvw__oxtni = SeriesType(data.dtype, data, None, string_type
                        )
                    lzhvc__eebx = get_const_func_output_type(func, (
                        nvw__oxtni,), {}, typing_context, target_context)
                    if lzhvc__eebx != ArrayItemArrayType(string_array_type):
                        lzhvc__eebx = dtype_to_array_type(lzhvc__eebx)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=bumvk__vxiwm, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    lsw__xbod = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    lepx__jslrc = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    vgex__lehki = dict(numeric_only=lsw__xbod, min_count=
                        lepx__jslrc)
                    tzgad__fes = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vgex__lehki, tzgad__fes, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    lsw__xbod = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    lepx__jslrc = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    vgex__lehki = dict(numeric_only=lsw__xbod, min_count=
                        lepx__jslrc)
                    tzgad__fes = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vgex__lehki, tzgad__fes, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    lsw__xbod = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    vgex__lehki = dict(numeric_only=lsw__xbod)
                    tzgad__fes = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vgex__lehki, tzgad__fes, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    vfbrf__uvbx = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    ont__laje = args[1] if len(args) > 1 else kws.pop('skipna',
                        True)
                    vgex__lehki = dict(axis=vfbrf__uvbx, skipna=ont__laje)
                    tzgad__fes = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vgex__lehki, tzgad__fes, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    hyb__izwx = args[0] if len(args) > 0 else kws.pop('ddof', 1
                        )
                    vgex__lehki = dict(ddof=hyb__izwx)
                    tzgad__fes = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        vgex__lehki, tzgad__fes, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                lzhvc__eebx, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                qyvc__vgzdu = to_str_arr_if_dict_array(lzhvc__eebx)
                out_data.append(qyvc__vgzdu)
                out_columns.append(bumvk__vxiwm)
                if func_name == 'agg':
                    awau__endoa = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    ejlb__iigzm[bumvk__vxiwm, awau__endoa] = bumvk__vxiwm
                else:
                    ejlb__iigzm[bumvk__vxiwm, func_name] = bumvk__vxiwm
                out_column_type.append(pumv__mkft)
            else:
                zmy__chrla.append(err_msg)
    if func_name == 'sum':
        ojzdj__yxs = any([(grrsl__baj == ColumnType.NumericalColumn.value) for
            grrsl__baj in out_column_type])
        if ojzdj__yxs:
            out_data = [grrsl__baj for grrsl__baj, hjxr__ppp in zip(
                out_data, out_column_type) if hjxr__ppp != ColumnType.
                NonNumericalColumn.value]
            out_columns = [grrsl__baj for grrsl__baj, hjxr__ppp in zip(
                out_columns, out_column_type) if hjxr__ppp != ColumnType.
                NonNumericalColumn.value]
            ejlb__iigzm = {}
            for bumvk__vxiwm in out_columns:
                if grp.as_index is False and bumvk__vxiwm in grp.keys:
                    continue
                ejlb__iigzm[bumvk__vxiwm, func_name] = bumvk__vxiwm
    lbhrx__wvpa = len(zmy__chrla)
    if len(out_data) == 0:
        if lbhrx__wvpa == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(lbhrx__wvpa, ' was' if lbhrx__wvpa == 1 else
                's were', ','.join(zmy__chrla)))
    phsr__eccx = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            nmlb__rkpk = IntDtype(out_data[0].dtype)
        else:
            nmlb__rkpk = out_data[0].dtype
        ayvbn__iar = (types.none if func_name == 'size' else types.
            StringLiteral(grp.selection[0]))
        phsr__eccx = SeriesType(nmlb__rkpk, index=index, name_typ=ayvbn__iar)
    return signature(phsr__eccx, *args), ejlb__iigzm


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    doqwd__mbulb = True
    if isinstance(f_val, str):
        doqwd__mbulb = False
        wrj__oyz = f_val
    elif is_overload_constant_str(f_val):
        doqwd__mbulb = False
        wrj__oyz = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        doqwd__mbulb = False
        wrj__oyz = bodo.utils.typing.get_builtin_function_name(f_val)
    if not doqwd__mbulb:
        if wrj__oyz not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {wrj__oyz}')
        jwhtp__qhe = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(jwhtp__qhe, (), wrj__oyz, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            tozhm__fhib = types.functions.MakeFunctionLiteral(f_val)
        else:
            tozhm__fhib = f_val
        validate_udf('agg', tozhm__fhib)
        func = get_overload_const_func(tozhm__fhib, None)
        stdlk__hagk = func.code if hasattr(func, 'code') else func.__code__
        wrj__oyz = stdlk__hagk.co_name
        jwhtp__qhe = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(jwhtp__qhe, (), 'agg', typing_context,
            target_context, tozhm__fhib)[0].return_type
    return wrj__oyz, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    rxesj__dvw = kws and all(isinstance(zxlg__iudac, types.Tuple) and len(
        zxlg__iudac) == 2 for zxlg__iudac in kws.values())
    if is_overload_none(func) and not rxesj__dvw:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not rxesj__dvw:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    mujaa__jdtaf = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if rxesj__dvw or is_overload_constant_dict(func):
        if rxesj__dvw:
            sbqe__wme = [get_literal_value(eqwhe__vktvc) for eqwhe__vktvc,
                pgs__ffi in kws.values()]
            bnf__jjebw = [get_literal_value(byan__gitl) for pgs__ffi,
                byan__gitl in kws.values()]
        else:
            dqfee__iqvlg = get_overload_constant_dict(func)
            sbqe__wme = tuple(dqfee__iqvlg.keys())
            bnf__jjebw = tuple(dqfee__iqvlg.values())
        if 'head' in bnf__jjebw:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(bumvk__vxiwm not in grp.selection and bumvk__vxiwm not in
            grp.keys for bumvk__vxiwm in sbqe__wme):
            raise_bodo_error(
                f'Selected column names {sbqe__wme} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            bnf__jjebw)
        if rxesj__dvw and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        ejlb__iigzm = {}
        out_columns = []
        out_data = []
        out_column_type = []
        lxwx__wvzv = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for ijxm__zjn, f_val in zip(sbqe__wme, bnf__jjebw):
            if isinstance(f_val, (tuple, list)):
                ryp__kpvms = 0
                for tozhm__fhib in f_val:
                    wrj__oyz, out_tp = get_agg_funcname_and_outtyp(grp,
                        ijxm__zjn, tozhm__fhib, typing_context, target_context)
                    mujaa__jdtaf = wrj__oyz in list_cumulative
                    if wrj__oyz == '<lambda>' and len(f_val) > 1:
                        wrj__oyz = '<lambda_' + str(ryp__kpvms) + '>'
                        ryp__kpvms += 1
                    out_columns.append((ijxm__zjn, wrj__oyz))
                    ejlb__iigzm[ijxm__zjn, wrj__oyz] = ijxm__zjn, wrj__oyz
                    _append_out_type(grp, out_data, out_tp)
            else:
                wrj__oyz, out_tp = get_agg_funcname_and_outtyp(grp,
                    ijxm__zjn, f_val, typing_context, target_context)
                mujaa__jdtaf = wrj__oyz in list_cumulative
                if multi_level_names:
                    out_columns.append((ijxm__zjn, wrj__oyz))
                    ejlb__iigzm[ijxm__zjn, wrj__oyz] = ijxm__zjn, wrj__oyz
                elif not rxesj__dvw:
                    out_columns.append(ijxm__zjn)
                    ejlb__iigzm[ijxm__zjn, wrj__oyz] = ijxm__zjn
                elif rxesj__dvw:
                    lxwx__wvzv.append(wrj__oyz)
                _append_out_type(grp, out_data, out_tp)
        if rxesj__dvw:
            for dphva__yat, knvv__hpf in enumerate(kws.keys()):
                out_columns.append(knvv__hpf)
                ejlb__iigzm[sbqe__wme[dphva__yat], lxwx__wvzv[dphva__yat]
                    ] = knvv__hpf
        if mujaa__jdtaf:
            index = grp.df_type.index
        else:
            index = out_tp.index
        phsr__eccx = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(phsr__eccx, *args), ejlb__iigzm
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
        ryp__kpvms = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        ejlb__iigzm = {}
        xyurb__ypik = grp.selection[0]
        for f_val in func.types:
            wrj__oyz, out_tp = get_agg_funcname_and_outtyp(grp, xyurb__ypik,
                f_val, typing_context, target_context)
            mujaa__jdtaf = wrj__oyz in list_cumulative
            if wrj__oyz == '<lambda>':
                wrj__oyz = '<lambda_' + str(ryp__kpvms) + '>'
                ryp__kpvms += 1
            out_columns.append(wrj__oyz)
            ejlb__iigzm[xyurb__ypik, wrj__oyz] = wrj__oyz
            _append_out_type(grp, out_data, out_tp)
        if mujaa__jdtaf:
            index = grp.df_type.index
        else:
            index = out_tp.index
        phsr__eccx = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(phsr__eccx, *args), ejlb__iigzm
    wrj__oyz = ''
    if types.unliteral(func) == types.unicode_type:
        wrj__oyz = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        wrj__oyz = bodo.utils.typing.get_builtin_function_name(func)
    if wrj__oyz:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, wrj__oyz, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        vfbrf__uvbx = args[0] if len(args) > 0 else kws.pop('axis', 0)
        lsw__xbod = args[1] if len(args) > 1 else kws.pop('numeric_only', False
            )
        ont__laje = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        vgex__lehki = dict(axis=vfbrf__uvbx, numeric_only=lsw__xbod)
        tzgad__fes = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', vgex__lehki,
            tzgad__fes, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        hiyhg__esv = args[0] if len(args) > 0 else kws.pop('periods', 1)
        ack__uli = args[1] if len(args) > 1 else kws.pop('freq', None)
        vfbrf__uvbx = args[2] if len(args) > 2 else kws.pop('axis', 0)
        lxdcr__wvhwx = args[3] if len(args) > 3 else kws.pop('fill_value', None
            )
        vgex__lehki = dict(freq=ack__uli, axis=vfbrf__uvbx, fill_value=
            lxdcr__wvhwx)
        tzgad__fes = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', vgex__lehki,
            tzgad__fes, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        ilfaw__dgxn = args[0] if len(args) > 0 else kws.pop('func', None)
        wwoy__wbtl = kws.pop('engine', None)
        bjex__sgvng = kws.pop('engine_kwargs', None)
        vgex__lehki = dict(engine=wwoy__wbtl, engine_kwargs=bjex__sgvng)
        tzgad__fes = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', vgex__lehki,
            tzgad__fes, package_name='pandas', module_name='GroupBy')
    ejlb__iigzm = {}
    for bumvk__vxiwm in grp.selection:
        out_columns.append(bumvk__vxiwm)
        ejlb__iigzm[bumvk__vxiwm, name_operation] = bumvk__vxiwm
        wcdbe__tsgbh = grp.df_type.columns.index(bumvk__vxiwm)
        data = grp.df_type.data[wcdbe__tsgbh]
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
            lzhvc__eebx, err_msg = get_groupby_output_dtype(data,
                get_literal_value(ilfaw__dgxn), grp.df_type.index)
            if err_msg == 'ok':
                data = lzhvc__eebx
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    phsr__eccx = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        phsr__eccx = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(phsr__eccx, *args), ejlb__iigzm


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
        hfbe__gsl = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        ixe__yqpcl = isinstance(hfbe__gsl, (SeriesType,
            HeterogeneousSeriesType)
            ) and hfbe__gsl.const_info is not None or not isinstance(hfbe__gsl,
            (SeriesType, DataFrameType))
        if ixe__yqpcl:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                nww__xkj = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                toj__wap = tuple(grp.df_type.columns.index(grp.keys[
                    dphva__yat]) for dphva__yat in range(len(grp.keys)))
                qpcu__uzda = tuple(grp.df_type.data[wcdbe__tsgbh] for
                    wcdbe__tsgbh in toj__wap)
                qpcu__uzda = tuple(to_str_arr_if_dict_array(sed__kwz) for
                    sed__kwz in qpcu__uzda)
                nww__xkj = MultiIndexType(qpcu__uzda, tuple(types.literal(
                    azgkr__lbb) for azgkr__lbb in grp.keys))
            else:
                wcdbe__tsgbh = grp.df_type.columns.index(grp.keys[0])
                chp__omh = grp.df_type.data[wcdbe__tsgbh]
                chp__omh = to_str_arr_if_dict_array(chp__omh)
                nww__xkj = bodo.hiframes.pd_index_ext.array_type_to_index(
                    chp__omh, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            tpxy__syx = tuple(grp.df_type.data[grp.df_type.columns.index(
                bumvk__vxiwm)] for bumvk__vxiwm in grp.keys)
            tpxy__syx = tuple(to_str_arr_if_dict_array(sed__kwz) for
                sed__kwz in tpxy__syx)
            taz__pnl = tuple(types.literal(zxlg__iudac) for zxlg__iudac in
                grp.keys) + get_index_name_types(hfbe__gsl.index)
            if not grp.as_index:
                tpxy__syx = types.Array(types.int64, 1, 'C'),
                taz__pnl = (types.none,) + get_index_name_types(hfbe__gsl.index
                    )
            nww__xkj = MultiIndexType(tpxy__syx + get_index_data_arr_types(
                hfbe__gsl.index), taz__pnl)
        if ixe__yqpcl:
            if isinstance(hfbe__gsl, HeterogeneousSeriesType):
                pgs__ffi, hziy__pwejr = hfbe__gsl.const_info
                if isinstance(hfbe__gsl.data, bodo.libs.nullable_tuple_ext.
                    NullableTupleType):
                    kxmdj__pvq = hfbe__gsl.data.tuple_typ.types
                elif isinstance(hfbe__gsl.data, types.Tuple):
                    kxmdj__pvq = hfbe__gsl.data.types
                kfn__rpx = tuple(to_nullable_type(dtype_to_array_type(
                    sed__kwz)) for sed__kwz in kxmdj__pvq)
                atxh__olgak = DataFrameType(out_data + kfn__rpx, nww__xkj, 
                    out_columns + hziy__pwejr)
            elif isinstance(hfbe__gsl, SeriesType):
                chaqq__nbbv, hziy__pwejr = hfbe__gsl.const_info
                kfn__rpx = tuple(to_nullable_type(dtype_to_array_type(
                    hfbe__gsl.dtype)) for pgs__ffi in range(chaqq__nbbv))
                atxh__olgak = DataFrameType(out_data + kfn__rpx, nww__xkj, 
                    out_columns + hziy__pwejr)
            else:
                qus__udl = get_udf_out_arr_type(hfbe__gsl)
                if not grp.as_index:
                    atxh__olgak = DataFrameType(out_data + (qus__udl,),
                        nww__xkj, out_columns + ('',))
                else:
                    atxh__olgak = SeriesType(qus__udl.dtype, qus__udl,
                        nww__xkj, None)
        elif isinstance(hfbe__gsl, SeriesType):
            atxh__olgak = SeriesType(hfbe__gsl.dtype, hfbe__gsl.data,
                nww__xkj, hfbe__gsl.name_typ)
        else:
            atxh__olgak = DataFrameType(hfbe__gsl.data, nww__xkj, hfbe__gsl
                .columns)
        tjc__qxgt = gen_apply_pysig(len(f_args), kws.keys())
        fqm__fmmr = (func, *f_args) + tuple(kws.values())
        return signature(atxh__olgak, *fqm__fmmr).replace(pysig=tjc__qxgt)

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
    eqehz__brrxp = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            ijxm__zjn = grp.selection[0]
            qus__udl = eqehz__brrxp.data[eqehz__brrxp.columns.index(ijxm__zjn)]
            qus__udl = to_str_arr_if_dict_array(qus__udl)
            udzx__forz = SeriesType(qus__udl.dtype, qus__udl, eqehz__brrxp.
                index, types.literal(ijxm__zjn))
        else:
            duhv__twf = tuple(eqehz__brrxp.data[eqehz__brrxp.columns.index(
                bumvk__vxiwm)] for bumvk__vxiwm in grp.selection)
            duhv__twf = tuple(to_str_arr_if_dict_array(sed__kwz) for
                sed__kwz in duhv__twf)
            udzx__forz = DataFrameType(duhv__twf, eqehz__brrxp.index, tuple
                (grp.selection))
    else:
        udzx__forz = eqehz__brrxp
    ztphx__nxpia = udzx__forz,
    ztphx__nxpia += tuple(f_args)
    try:
        hfbe__gsl = get_const_func_output_type(func, ztphx__nxpia, kws,
            typing_context, target_context)
    except Exception as akr__vdk:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', akr__vdk),
            getattr(akr__vdk, 'loc', None))
    return hfbe__gsl


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    ztphx__nxpia = (grp,) + f_args
    try:
        hfbe__gsl = get_const_func_output_type(func, ztphx__nxpia, kws,
            self.context, numba.core.registry.cpu_target.target_context, False)
    except Exception as akr__vdk:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', akr__vdk),
            getattr(akr__vdk, 'loc', None))
    tjc__qxgt = gen_apply_pysig(len(f_args), kws.keys())
    fqm__fmmr = (func, *f_args) + tuple(kws.values())
    return signature(hfbe__gsl, *fqm__fmmr).replace(pysig=tjc__qxgt)


def gen_apply_pysig(n_args, kws):
    meni__zzfvb = ', '.join(f'arg{dphva__yat}' for dphva__yat in range(n_args))
    meni__zzfvb = meni__zzfvb + ', ' if meni__zzfvb else ''
    eqskl__dgs = ', '.join(f"{caova__ztlq} = ''" for caova__ztlq in kws)
    dkq__tiy = f'def apply_stub(func, {meni__zzfvb}{eqskl__dgs}):\n'
    dkq__tiy += '    pass\n'
    lyvo__piyxk = {}
    exec(dkq__tiy, {}, lyvo__piyxk)
    bqp__ghjv = lyvo__piyxk['apply_stub']
    return numba.core.utils.pysignature(bqp__ghjv)


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
        lzhvc__eebx = get_pivot_output_dtype(data, aggfunc.literal_value)
        zpu__sga = dtype_to_array_type(lzhvc__eebx)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/pandas.html'
                )
        sbg__mgxur = _pivot_values.meta
        jyp__tkjsv = len(sbg__mgxur)
        wcdbe__tsgbh = df.columns.index(index)
        chp__omh = df.data[wcdbe__tsgbh]
        chp__omh = to_str_arr_if_dict_array(chp__omh)
        rfum__ehehx = bodo.hiframes.pd_index_ext.array_type_to_index(chp__omh,
            types.StringLiteral(index))
        eiu__pyxis = DataFrameType((zpu__sga,) * jyp__tkjsv, rfum__ehehx,
            tuple(sbg__mgxur))
        return signature(eiu__pyxis, *args)


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
        zpu__sga = types.Array(types.int64, 1, 'C')
        sbg__mgxur = _pivot_values.meta
        jyp__tkjsv = len(sbg__mgxur)
        rfum__ehehx = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        eiu__pyxis = DataFrameType((zpu__sga,) * jyp__tkjsv, rfum__ehehx,
            tuple(sbg__mgxur))
        return signature(eiu__pyxis, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    dkq__tiy = 'def impl(keys, dropna, _is_parallel):\n'
    dkq__tiy += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    dkq__tiy += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{dphva__yat}])' for dphva__yat in range(len(
        keys.types))))
    dkq__tiy += '    table = arr_info_list_to_table(info_list)\n'
    dkq__tiy += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    dkq__tiy += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    dkq__tiy += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    dkq__tiy += '    delete_table_decref_arrays(table)\n'
    dkq__tiy += '    ev.finalize()\n'
    dkq__tiy += '    return sort_idx, group_labels, ngroups\n'
    lyvo__piyxk = {}
    exec(dkq__tiy, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, lyvo__piyxk)
    rod__crix = lyvo__piyxk['impl']
    return rod__crix


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    hpfck__lwwf = len(labels)
    rrfn__qwo = np.zeros(ngroups, dtype=np.int64)
    ymkq__uhb = np.zeros(ngroups, dtype=np.int64)
    azx__cicnj = 0
    yvo__ppud = 0
    for dphva__yat in range(hpfck__lwwf):
        rvivl__zfr = labels[dphva__yat]
        if rvivl__zfr < 0:
            azx__cicnj += 1
        else:
            yvo__ppud += 1
            if dphva__yat == hpfck__lwwf - 1 or rvivl__zfr != labels[
                dphva__yat + 1]:
                rrfn__qwo[rvivl__zfr] = azx__cicnj
                ymkq__uhb[rvivl__zfr] = azx__cicnj + yvo__ppud
                azx__cicnj += yvo__ppud
                yvo__ppud = 0
    return rrfn__qwo, ymkq__uhb


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    rod__crix, pgs__ffi = gen_shuffle_dataframe(df, keys, _is_parallel)
    return rod__crix


def gen_shuffle_dataframe(df, keys, _is_parallel):
    chaqq__nbbv = len(df.columns)
    lrpnw__jbu = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    dkq__tiy = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        dkq__tiy += '  return df, keys, get_null_shuffle_info()\n'
        lyvo__piyxk = {}
        exec(dkq__tiy, {'get_null_shuffle_info': get_null_shuffle_info},
            lyvo__piyxk)
        rod__crix = lyvo__piyxk['impl']
        return rod__crix
    for dphva__yat in range(chaqq__nbbv):
        dkq__tiy += f"""  in_arr{dphva__yat} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {dphva__yat})
"""
    dkq__tiy += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    dkq__tiy += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{dphva__yat}])' for dphva__yat in range(
        lrpnw__jbu)), ', '.join(f'array_to_info(in_arr{dphva__yat})' for
        dphva__yat in range(chaqq__nbbv)), 'array_to_info(in_index_arr)')
    dkq__tiy += '  table = arr_info_list_to_table(info_list)\n'
    dkq__tiy += (
        f'  out_table = shuffle_table(table, {lrpnw__jbu}, _is_parallel, 1)\n')
    for dphva__yat in range(lrpnw__jbu):
        dkq__tiy += f"""  out_key{dphva__yat} = info_to_array(info_from_table(out_table, {dphva__yat}), keys{dphva__yat}_typ)
"""
    for dphva__yat in range(chaqq__nbbv):
        dkq__tiy += f"""  out_arr{dphva__yat} = info_to_array(info_from_table(out_table, {dphva__yat + lrpnw__jbu}), in_arr{dphva__yat}_typ)
"""
    dkq__tiy += f"""  out_arr_index = info_to_array(info_from_table(out_table, {lrpnw__jbu + chaqq__nbbv}), ind_arr_typ)
"""
    dkq__tiy += '  shuffle_info = get_shuffle_info(out_table)\n'
    dkq__tiy += '  delete_table(out_table)\n'
    dkq__tiy += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{dphva__yat}' for dphva__yat in range(
        chaqq__nbbv))
    dkq__tiy += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    dkq__tiy += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    dkq__tiy += '  return out_df, ({},), shuffle_info\n'.format(', '.join(
        f'out_key{dphva__yat}' for dphva__yat in range(lrpnw__jbu)))
    plqlx__vrgi = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    plqlx__vrgi.update({f'keys{dphva__yat}_typ': keys.types[dphva__yat] for
        dphva__yat in range(lrpnw__jbu)})
    plqlx__vrgi.update({f'in_arr{dphva__yat}_typ': df.data[dphva__yat] for
        dphva__yat in range(chaqq__nbbv)})
    lyvo__piyxk = {}
    exec(dkq__tiy, plqlx__vrgi, lyvo__piyxk)
    rod__crix = lyvo__piyxk['impl']
    return rod__crix, plqlx__vrgi


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        etg__xtk = len(data.array_types)
        dkq__tiy = 'def impl(data, shuffle_info):\n'
        dkq__tiy += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{dphva__yat}])' for dphva__yat in
            range(etg__xtk)))
        dkq__tiy += '  table = arr_info_list_to_table(info_list)\n'
        dkq__tiy += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for dphva__yat in range(etg__xtk):
            dkq__tiy += f"""  out_arr{dphva__yat} = info_to_array(info_from_table(out_table, {dphva__yat}), data._data[{dphva__yat}])
"""
        dkq__tiy += '  delete_table(out_table)\n'
        dkq__tiy += '  delete_table(table)\n'
        dkq__tiy += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{dphva__yat}' for dphva__yat in range
            (etg__xtk))))
        lyvo__piyxk = {}
        exec(dkq__tiy, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, lyvo__piyxk)
        rod__crix = lyvo__piyxk['impl']
        return rod__crix
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            ttqc__hupux = bodo.utils.conversion.index_to_array(data)
            qyvc__vgzdu = reverse_shuffle(ttqc__hupux, shuffle_info)
            return bodo.utils.conversion.index_from_array(qyvc__vgzdu)
        return impl_index

    def impl_arr(data, shuffle_info):
        poy__jeg = [array_to_info(data)]
        jdfp__hfr = arr_info_list_to_table(poy__jeg)
        usfe__txe = reverse_shuffle_table(jdfp__hfr, shuffle_info)
        qyvc__vgzdu = info_to_array(info_from_table(usfe__txe, 0), data)
        delete_table(usfe__txe)
        delete_table(jdfp__hfr)
        return qyvc__vgzdu
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    vgex__lehki = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna
        )
    tzgad__fes = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', vgex__lehki, tzgad__fes,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    novkb__rks = get_overload_const_bool(ascending)
    anc__lvoq = grp.selection[0]
    dkq__tiy = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    vxmi__mjqvm = (
        f"lambda S: S.value_counts(ascending={novkb__rks}, _index_name='{anc__lvoq}')"
        )
    dkq__tiy += f'    return grp.apply({vxmi__mjqvm})\n'
    lyvo__piyxk = {}
    exec(dkq__tiy, {'bodo': bodo}, lyvo__piyxk)
    rod__crix = lyvo__piyxk['impl']
    return rod__crix


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
    for qrd__xlfcc in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, qrd__xlfcc, no_unliteral=True
            )(create_unsupported_overload(f'DataFrameGroupBy.{qrd__xlfcc}'))
    for qrd__xlfcc in groupby_unsupported:
        overload_method(DataFrameGroupByType, qrd__xlfcc, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{qrd__xlfcc}'))
    for qrd__xlfcc in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, qrd__xlfcc, no_unliteral=True
            )(create_unsupported_overload(f'SeriesGroupBy.{qrd__xlfcc}'))
    for qrd__xlfcc in series_only_unsupported:
        overload_method(DataFrameGroupByType, qrd__xlfcc, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{qrd__xlfcc}'))
    for qrd__xlfcc in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, qrd__xlfcc, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{qrd__xlfcc}'))


_install_groupby_unsupported()
