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
        zubx__jwhrr = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, zubx__jwhrr)


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
        bzxf__zysui = args[0]
        phg__iuek = signature.return_type
        lnf__wrp = cgutils.create_struct_proxy(phg__iuek)(context, builder)
        lnf__wrp.obj = bzxf__zysui
        context.nrt.incref(builder, signature.args[0], bzxf__zysui)
        return lnf__wrp._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for podtk__kosxa in keys:
        selection.remove(podtk__kosxa)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    phg__iuek = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return phg__iuek(obj_type, by_type, as_index_type, dropna_type), codegen


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
        grpby, kjf__mghkd = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(kjf__mghkd, (tuple, list)):
                if len(set(kjf__mghkd).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(kjf__mghkd).difference(set(grpby.
                        df_type.columns))))
                selection = kjf__mghkd
            else:
                if kjf__mghkd not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(kjf__mghkd))
                selection = kjf__mghkd,
                series_select = True
            ebvz__hlf = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(ebvz__hlf, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, kjf__mghkd = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            kjf__mghkd):
            ebvz__hlf = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(kjf__mghkd)), {}).return_type
            return signature(ebvz__hlf, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    xtjv__wera = arr_type == ArrayItemArrayType(string_array_type)
    lnk__jcj = arr_type.dtype
    if isinstance(lnk__jcj, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {lnk__jcj} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(lnk__jcj, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {lnk__jcj} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(lnk__jcj,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(lnk__jcj, (types.Integer, types.Float, types.Boolean)):
        if xtjv__wera or lnk__jcj == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(lnk__jcj, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not lnk__jcj.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {lnk__jcj} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(lnk__jcj, types.Boolean) and func_name in {'cumsum',
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
    lnk__jcj = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(lnk__jcj, (types
            .Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(lnk__jcj, types.Integer):
            return IntDtype(lnk__jcj)
        return lnk__jcj
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        lbql__qoafa = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{lbql__qoafa}'."
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
    for podtk__kosxa in grp.keys:
        if multi_level_names:
            wfd__bnoh = podtk__kosxa, ''
        else:
            wfd__bnoh = podtk__kosxa
        yvbty__kcbj = grp.df_type.columns.index(podtk__kosxa)
        data = to_str_arr_if_dict_array(grp.df_type.data[yvbty__kcbj])
        out_columns.append(wfd__bnoh)
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
        racrb__gqusp = tuple(grp.df_type.columns.index(grp.keys[
            goran__kkiow]) for goran__kkiow in range(len(grp.keys)))
        jrhgj__yvqp = tuple(grp.df_type.data[yvbty__kcbj] for yvbty__kcbj in
            racrb__gqusp)
        jrhgj__yvqp = tuple(to_str_arr_if_dict_array(bre__puaz) for
            bre__puaz in jrhgj__yvqp)
        index = MultiIndexType(jrhgj__yvqp, tuple(types.StringLiteral(
            podtk__kosxa) for podtk__kosxa in grp.keys))
    else:
        yvbty__kcbj = grp.df_type.columns.index(grp.keys[0])
        kldh__zffh = to_str_arr_if_dict_array(grp.df_type.data[yvbty__kcbj])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(kldh__zffh,
            types.StringLiteral(grp.keys[0]))
    upw__aijim = {}
    lknl__ibspi = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        upw__aijim[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for bmf__icwq in columns:
            yvbty__kcbj = grp.df_type.columns.index(bmf__icwq)
            data = grp.df_type.data[yvbty__kcbj]
            data = to_str_arr_if_dict_array(data)
            jcv__jlrg = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                jcv__jlrg = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    fob__llz = SeriesType(data.dtype, data, None, string_type)
                    vuxu__kvz = get_const_func_output_type(func, (fob__llz,
                        ), {}, typing_context, target_context)
                    if vuxu__kvz != ArrayItemArrayType(string_array_type):
                        vuxu__kvz = dtype_to_array_type(vuxu__kvz)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=bmf__icwq, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    cgpl__qcjd = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    pden__ehkl = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    qlbr__tnrth = dict(numeric_only=cgpl__qcjd, min_count=
                        pden__ehkl)
                    rvc__bqieh = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        qlbr__tnrth, rvc__bqieh, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    cgpl__qcjd = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    pden__ehkl = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    qlbr__tnrth = dict(numeric_only=cgpl__qcjd, min_count=
                        pden__ehkl)
                    rvc__bqieh = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        qlbr__tnrth, rvc__bqieh, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    cgpl__qcjd = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    qlbr__tnrth = dict(numeric_only=cgpl__qcjd)
                    rvc__bqieh = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        qlbr__tnrth, rvc__bqieh, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    zwy__mgmbv = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    nhrtl__fdzkl = args[1] if len(args) > 1 else kws.pop(
                        'skipna', True)
                    qlbr__tnrth = dict(axis=zwy__mgmbv, skipna=nhrtl__fdzkl)
                    rvc__bqieh = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        qlbr__tnrth, rvc__bqieh, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    xfg__jeajr = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    qlbr__tnrth = dict(ddof=xfg__jeajr)
                    rvc__bqieh = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        qlbr__tnrth, rvc__bqieh, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                vuxu__kvz, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                fwlq__xof = to_str_arr_if_dict_array(vuxu__kvz)
                out_data.append(fwlq__xof)
                out_columns.append(bmf__icwq)
                if func_name == 'agg':
                    xmfxi__gesn = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    upw__aijim[bmf__icwq, xmfxi__gesn] = bmf__icwq
                else:
                    upw__aijim[bmf__icwq, func_name] = bmf__icwq
                out_column_type.append(jcv__jlrg)
            else:
                lknl__ibspi.append(err_msg)
    if func_name == 'sum':
        onv__glhd = any([(irg__gokb == ColumnType.NumericalColumn.value) for
            irg__gokb in out_column_type])
        if onv__glhd:
            out_data = [irg__gokb for irg__gokb, ouix__xhmzp in zip(
                out_data, out_column_type) if ouix__xhmzp != ColumnType.
                NonNumericalColumn.value]
            out_columns = [irg__gokb for irg__gokb, ouix__xhmzp in zip(
                out_columns, out_column_type) if ouix__xhmzp != ColumnType.
                NonNumericalColumn.value]
            upw__aijim = {}
            for bmf__icwq in out_columns:
                if grp.as_index is False and bmf__icwq in grp.keys:
                    continue
                upw__aijim[bmf__icwq, func_name] = bmf__icwq
    krrpn__bvzi = len(lknl__ibspi)
    if len(out_data) == 0:
        if krrpn__bvzi == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(krrpn__bvzi, ' was' if krrpn__bvzi == 1 else
                's were', ','.join(lknl__ibspi)))
    ytshn__yfz = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            cmp__pjwv = IntDtype(out_data[0].dtype)
        else:
            cmp__pjwv = out_data[0].dtype
        ulp__fzpa = types.none if func_name == 'size' else types.StringLiteral(
            grp.selection[0])
        ytshn__yfz = SeriesType(cmp__pjwv, index=index, name_typ=ulp__fzpa)
    return signature(ytshn__yfz, *args), upw__aijim


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    oyjyc__gltks = True
    if isinstance(f_val, str):
        oyjyc__gltks = False
        oqz__eks = f_val
    elif is_overload_constant_str(f_val):
        oyjyc__gltks = False
        oqz__eks = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        oyjyc__gltks = False
        oqz__eks = bodo.utils.typing.get_builtin_function_name(f_val)
    if not oyjyc__gltks:
        if oqz__eks not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {oqz__eks}')
        ebvz__hlf = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(ebvz__hlf, (), oqz__eks, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            nigb__odvg = types.functions.MakeFunctionLiteral(f_val)
        else:
            nigb__odvg = f_val
        validate_udf('agg', nigb__odvg)
        func = get_overload_const_func(nigb__odvg, None)
        hggem__abpe = func.code if hasattr(func, 'code') else func.__code__
        oqz__eks = hggem__abpe.co_name
        ebvz__hlf = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(ebvz__hlf, (), 'agg', typing_context,
            target_context, nigb__odvg)[0].return_type
    return oqz__eks, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    nex__wvox = kws and all(isinstance(sxtil__grfi, types.Tuple) and len(
        sxtil__grfi) == 2 for sxtil__grfi in kws.values())
    if is_overload_none(func) and not nex__wvox:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not nex__wvox:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    avwm__fpej = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if nex__wvox or is_overload_constant_dict(func):
        if nex__wvox:
            itj__aij = [get_literal_value(ovap__mnhww) for ovap__mnhww,
                joeu__afi in kws.values()]
            vigz__egi = [get_literal_value(jjw__qgr) for joeu__afi,
                jjw__qgr in kws.values()]
        else:
            gwo__cxh = get_overload_constant_dict(func)
            itj__aij = tuple(gwo__cxh.keys())
            vigz__egi = tuple(gwo__cxh.values())
        if 'head' in vigz__egi:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(bmf__icwq not in grp.selection and bmf__icwq not in grp.keys for
            bmf__icwq in itj__aij):
            raise_bodo_error(
                f'Selected column names {itj__aij} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            vigz__egi)
        if nex__wvox and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        upw__aijim = {}
        out_columns = []
        out_data = []
        out_column_type = []
        vjq__arogh = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for mhyp__itnv, f_val in zip(itj__aij, vigz__egi):
            if isinstance(f_val, (tuple, list)):
                wzas__kdj = 0
                for nigb__odvg in f_val:
                    oqz__eks, out_tp = get_agg_funcname_and_outtyp(grp,
                        mhyp__itnv, nigb__odvg, typing_context, target_context)
                    avwm__fpej = oqz__eks in list_cumulative
                    if oqz__eks == '<lambda>' and len(f_val) > 1:
                        oqz__eks = '<lambda_' + str(wzas__kdj) + '>'
                        wzas__kdj += 1
                    out_columns.append((mhyp__itnv, oqz__eks))
                    upw__aijim[mhyp__itnv, oqz__eks] = mhyp__itnv, oqz__eks
                    _append_out_type(grp, out_data, out_tp)
            else:
                oqz__eks, out_tp = get_agg_funcname_and_outtyp(grp,
                    mhyp__itnv, f_val, typing_context, target_context)
                avwm__fpej = oqz__eks in list_cumulative
                if multi_level_names:
                    out_columns.append((mhyp__itnv, oqz__eks))
                    upw__aijim[mhyp__itnv, oqz__eks] = mhyp__itnv, oqz__eks
                elif not nex__wvox:
                    out_columns.append(mhyp__itnv)
                    upw__aijim[mhyp__itnv, oqz__eks] = mhyp__itnv
                elif nex__wvox:
                    vjq__arogh.append(oqz__eks)
                _append_out_type(grp, out_data, out_tp)
        if nex__wvox:
            for goran__kkiow, ykz__cttm in enumerate(kws.keys()):
                out_columns.append(ykz__cttm)
                upw__aijim[itj__aij[goran__kkiow], vjq__arogh[goran__kkiow]
                    ] = ykz__cttm
        if avwm__fpej:
            index = grp.df_type.index
        else:
            index = out_tp.index
        ytshn__yfz = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(ytshn__yfz, *args), upw__aijim
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
        wzas__kdj = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        upw__aijim = {}
        yzq__siywb = grp.selection[0]
        for f_val in func.types:
            oqz__eks, out_tp = get_agg_funcname_and_outtyp(grp, yzq__siywb,
                f_val, typing_context, target_context)
            avwm__fpej = oqz__eks in list_cumulative
            if oqz__eks == '<lambda>':
                oqz__eks = '<lambda_' + str(wzas__kdj) + '>'
                wzas__kdj += 1
            out_columns.append(oqz__eks)
            upw__aijim[yzq__siywb, oqz__eks] = oqz__eks
            _append_out_type(grp, out_data, out_tp)
        if avwm__fpej:
            index = grp.df_type.index
        else:
            index = out_tp.index
        ytshn__yfz = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(ytshn__yfz, *args), upw__aijim
    oqz__eks = ''
    if types.unliteral(func) == types.unicode_type:
        oqz__eks = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        oqz__eks = bodo.utils.typing.get_builtin_function_name(func)
    if oqz__eks:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, oqz__eks, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        zwy__mgmbv = args[0] if len(args) > 0 else kws.pop('axis', 0)
        cgpl__qcjd = args[1] if len(args) > 1 else kws.pop('numeric_only', 
            False)
        nhrtl__fdzkl = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        qlbr__tnrth = dict(axis=zwy__mgmbv, numeric_only=cgpl__qcjd)
        rvc__bqieh = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', qlbr__tnrth,
            rvc__bqieh, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        jihx__hdfbx = args[0] if len(args) > 0 else kws.pop('periods', 1)
        chixt__zycl = args[1] if len(args) > 1 else kws.pop('freq', None)
        zwy__mgmbv = args[2] if len(args) > 2 else kws.pop('axis', 0)
        jwoq__zjwb = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        qlbr__tnrth = dict(freq=chixt__zycl, axis=zwy__mgmbv, fill_value=
            jwoq__zjwb)
        rvc__bqieh = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', qlbr__tnrth,
            rvc__bqieh, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        bwplb__vclyz = args[0] if len(args) > 0 else kws.pop('func', None)
        zqzdl__eaiy = kws.pop('engine', None)
        gjy__wjh = kws.pop('engine_kwargs', None)
        qlbr__tnrth = dict(engine=zqzdl__eaiy, engine_kwargs=gjy__wjh)
        rvc__bqieh = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', qlbr__tnrth,
            rvc__bqieh, package_name='pandas', module_name='GroupBy')
    upw__aijim = {}
    for bmf__icwq in grp.selection:
        out_columns.append(bmf__icwq)
        upw__aijim[bmf__icwq, name_operation] = bmf__icwq
        yvbty__kcbj = grp.df_type.columns.index(bmf__icwq)
        data = grp.df_type.data[yvbty__kcbj]
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
            vuxu__kvz, err_msg = get_groupby_output_dtype(data,
                get_literal_value(bwplb__vclyz), grp.df_type.index)
            if err_msg == 'ok':
                data = vuxu__kvz
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    ytshn__yfz = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        ytshn__yfz = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(ytshn__yfz, *args), upw__aijim


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
        vlgpu__hrvz = _get_groupby_apply_udf_out_type(func, grp, f_args,
            kws, self.context, numba.core.registry.cpu_target.target_context)
        cnudt__oneld = isinstance(vlgpu__hrvz, (SeriesType,
            HeterogeneousSeriesType)
            ) and vlgpu__hrvz.const_info is not None or not isinstance(
            vlgpu__hrvz, (SeriesType, DataFrameType))
        if cnudt__oneld:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                mgp__wbatf = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                racrb__gqusp = tuple(grp.df_type.columns.index(grp.keys[
                    goran__kkiow]) for goran__kkiow in range(len(grp.keys)))
                jrhgj__yvqp = tuple(grp.df_type.data[yvbty__kcbj] for
                    yvbty__kcbj in racrb__gqusp)
                jrhgj__yvqp = tuple(to_str_arr_if_dict_array(bre__puaz) for
                    bre__puaz in jrhgj__yvqp)
                mgp__wbatf = MultiIndexType(jrhgj__yvqp, tuple(types.
                    literal(podtk__kosxa) for podtk__kosxa in grp.keys))
            else:
                yvbty__kcbj = grp.df_type.columns.index(grp.keys[0])
                kldh__zffh = grp.df_type.data[yvbty__kcbj]
                kldh__zffh = to_str_arr_if_dict_array(kldh__zffh)
                mgp__wbatf = bodo.hiframes.pd_index_ext.array_type_to_index(
                    kldh__zffh, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            uvpft__alpi = tuple(grp.df_type.data[grp.df_type.columns.index(
                bmf__icwq)] for bmf__icwq in grp.keys)
            uvpft__alpi = tuple(to_str_arr_if_dict_array(bre__puaz) for
                bre__puaz in uvpft__alpi)
            ylv__bqgbp = tuple(types.literal(sxtil__grfi) for sxtil__grfi in
                grp.keys) + get_index_name_types(vlgpu__hrvz.index)
            if not grp.as_index:
                uvpft__alpi = types.Array(types.int64, 1, 'C'),
                ylv__bqgbp = (types.none,) + get_index_name_types(vlgpu__hrvz
                    .index)
            mgp__wbatf = MultiIndexType(uvpft__alpi +
                get_index_data_arr_types(vlgpu__hrvz.index), ylv__bqgbp)
        if cnudt__oneld:
            if isinstance(vlgpu__hrvz, HeterogeneousSeriesType):
                joeu__afi, xlvwd__ddmg = vlgpu__hrvz.const_info
                if isinstance(vlgpu__hrvz.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    aatb__epzac = vlgpu__hrvz.data.tuple_typ.types
                elif isinstance(vlgpu__hrvz.data, types.Tuple):
                    aatb__epzac = vlgpu__hrvz.data.types
                dsbhp__icvai = tuple(to_nullable_type(dtype_to_array_type(
                    bre__puaz)) for bre__puaz in aatb__epzac)
                guqm__cky = DataFrameType(out_data + dsbhp__icvai,
                    mgp__wbatf, out_columns + xlvwd__ddmg)
            elif isinstance(vlgpu__hrvz, SeriesType):
                jklgr__fjb, xlvwd__ddmg = vlgpu__hrvz.const_info
                dsbhp__icvai = tuple(to_nullable_type(dtype_to_array_type(
                    vlgpu__hrvz.dtype)) for joeu__afi in range(jklgr__fjb))
                guqm__cky = DataFrameType(out_data + dsbhp__icvai,
                    mgp__wbatf, out_columns + xlvwd__ddmg)
            else:
                kmzyu__pknn = get_udf_out_arr_type(vlgpu__hrvz)
                if not grp.as_index:
                    guqm__cky = DataFrameType(out_data + (kmzyu__pknn,),
                        mgp__wbatf, out_columns + ('',))
                else:
                    guqm__cky = SeriesType(kmzyu__pknn.dtype, kmzyu__pknn,
                        mgp__wbatf, None)
        elif isinstance(vlgpu__hrvz, SeriesType):
            guqm__cky = SeriesType(vlgpu__hrvz.dtype, vlgpu__hrvz.data,
                mgp__wbatf, vlgpu__hrvz.name_typ)
        else:
            guqm__cky = DataFrameType(vlgpu__hrvz.data, mgp__wbatf,
                vlgpu__hrvz.columns)
        iqemq__etrb = gen_apply_pysig(len(f_args), kws.keys())
        elov__rtnsx = (func, *f_args) + tuple(kws.values())
        return signature(guqm__cky, *elov__rtnsx).replace(pysig=iqemq__etrb)

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
    wrfma__ctrqw = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            mhyp__itnv = grp.selection[0]
            kmzyu__pknn = wrfma__ctrqw.data[wrfma__ctrqw.columns.index(
                mhyp__itnv)]
            kmzyu__pknn = to_str_arr_if_dict_array(kmzyu__pknn)
            owsnb__hgbr = SeriesType(kmzyu__pknn.dtype, kmzyu__pknn,
                wrfma__ctrqw.index, types.literal(mhyp__itnv))
        else:
            owhn__zswlk = tuple(wrfma__ctrqw.data[wrfma__ctrqw.columns.
                index(bmf__icwq)] for bmf__icwq in grp.selection)
            owhn__zswlk = tuple(to_str_arr_if_dict_array(bre__puaz) for
                bre__puaz in owhn__zswlk)
            owsnb__hgbr = DataFrameType(owhn__zswlk, wrfma__ctrqw.index,
                tuple(grp.selection))
    else:
        owsnb__hgbr = wrfma__ctrqw
    aplyp__hrju = owsnb__hgbr,
    aplyp__hrju += tuple(f_args)
    try:
        vlgpu__hrvz = get_const_func_output_type(func, aplyp__hrju, kws,
            typing_context, target_context)
    except Exception as tox__htza:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', tox__htza),
            getattr(tox__htza, 'loc', None))
    return vlgpu__hrvz


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    aplyp__hrju = (grp,) + f_args
    try:
        vlgpu__hrvz = get_const_func_output_type(func, aplyp__hrju, kws,
            self.context, numba.core.registry.cpu_target.target_context, False)
    except Exception as tox__htza:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', tox__htza),
            getattr(tox__htza, 'loc', None))
    iqemq__etrb = gen_apply_pysig(len(f_args), kws.keys())
    elov__rtnsx = (func, *f_args) + tuple(kws.values())
    return signature(vlgpu__hrvz, *elov__rtnsx).replace(pysig=iqemq__etrb)


def gen_apply_pysig(n_args, kws):
    kjfp__afynb = ', '.join(f'arg{goran__kkiow}' for goran__kkiow in range(
        n_args))
    kjfp__afynb = kjfp__afynb + ', ' if kjfp__afynb else ''
    xsil__hsh = ', '.join(f"{kszzs__dbngt} = ''" for kszzs__dbngt in kws)
    siadg__zvb = f'def apply_stub(func, {kjfp__afynb}{xsil__hsh}):\n'
    siadg__zvb += '    pass\n'
    dnp__awpp = {}
    exec(siadg__zvb, {}, dnp__awpp)
    vfdt__pldxc = dnp__awpp['apply_stub']
    return numba.core.utils.pysignature(vfdt__pldxc)


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
        vuxu__kvz = get_pivot_output_dtype(data, aggfunc.literal_value)
        lcvl__etrh = dtype_to_array_type(vuxu__kvz)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/pandas.html'
                )
        aso__pqou = _pivot_values.meta
        ceuz__mwn = len(aso__pqou)
        yvbty__kcbj = df.columns.index(index)
        kldh__zffh = df.data[yvbty__kcbj]
        kldh__zffh = to_str_arr_if_dict_array(kldh__zffh)
        ldqb__ycgd = bodo.hiframes.pd_index_ext.array_type_to_index(kldh__zffh,
            types.StringLiteral(index))
        bqnb__uhkh = DataFrameType((lcvl__etrh,) * ceuz__mwn, ldqb__ycgd,
            tuple(aso__pqou))
        return signature(bqnb__uhkh, *args)


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
        lcvl__etrh = types.Array(types.int64, 1, 'C')
        aso__pqou = _pivot_values.meta
        ceuz__mwn = len(aso__pqou)
        ldqb__ycgd = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        bqnb__uhkh = DataFrameType((lcvl__etrh,) * ceuz__mwn, ldqb__ycgd,
            tuple(aso__pqou))
        return signature(bqnb__uhkh, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    siadg__zvb = 'def impl(keys, dropna, _is_parallel):\n'
    siadg__zvb += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    siadg__zvb += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{goran__kkiow}])' for goran__kkiow in range(
        len(keys.types))))
    siadg__zvb += '    table = arr_info_list_to_table(info_list)\n'
    siadg__zvb += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    siadg__zvb += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    siadg__zvb += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    siadg__zvb += '    delete_table_decref_arrays(table)\n'
    siadg__zvb += '    ev.finalize()\n'
    siadg__zvb += '    return sort_idx, group_labels, ngroups\n'
    dnp__awpp = {}
    exec(siadg__zvb, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, dnp__awpp)
    vwlyy__vmrqd = dnp__awpp['impl']
    return vwlyy__vmrqd


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    nnsgg__ojuf = len(labels)
    qvm__lgs = np.zeros(ngroups, dtype=np.int64)
    huwbc__wkl = np.zeros(ngroups, dtype=np.int64)
    xpji__xnn = 0
    kwmcq__gnjpw = 0
    for goran__kkiow in range(nnsgg__ojuf):
        mof__ltv = labels[goran__kkiow]
        if mof__ltv < 0:
            xpji__xnn += 1
        else:
            kwmcq__gnjpw += 1
            if goran__kkiow == nnsgg__ojuf - 1 or mof__ltv != labels[
                goran__kkiow + 1]:
                qvm__lgs[mof__ltv] = xpji__xnn
                huwbc__wkl[mof__ltv] = xpji__xnn + kwmcq__gnjpw
                xpji__xnn += kwmcq__gnjpw
                kwmcq__gnjpw = 0
    return qvm__lgs, huwbc__wkl


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    vwlyy__vmrqd, joeu__afi = gen_shuffle_dataframe(df, keys, _is_parallel)
    return vwlyy__vmrqd


def gen_shuffle_dataframe(df, keys, _is_parallel):
    jklgr__fjb = len(df.columns)
    fdc__oisce = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    siadg__zvb = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        siadg__zvb += '  return df, keys, get_null_shuffle_info()\n'
        dnp__awpp = {}
        exec(siadg__zvb, {'get_null_shuffle_info': get_null_shuffle_info},
            dnp__awpp)
        vwlyy__vmrqd = dnp__awpp['impl']
        return vwlyy__vmrqd
    for goran__kkiow in range(jklgr__fjb):
        siadg__zvb += f"""  in_arr{goran__kkiow} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {goran__kkiow})
"""
    siadg__zvb += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    siadg__zvb += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{goran__kkiow}])' for goran__kkiow in range(
        fdc__oisce)), ', '.join(f'array_to_info(in_arr{goran__kkiow})' for
        goran__kkiow in range(jklgr__fjb)), 'array_to_info(in_index_arr)')
    siadg__zvb += '  table = arr_info_list_to_table(info_list)\n'
    siadg__zvb += (
        f'  out_table = shuffle_table(table, {fdc__oisce}, _is_parallel, 1)\n')
    for goran__kkiow in range(fdc__oisce):
        siadg__zvb += f"""  out_key{goran__kkiow} = info_to_array(info_from_table(out_table, {goran__kkiow}), keys{goran__kkiow}_typ)
"""
    for goran__kkiow in range(jklgr__fjb):
        siadg__zvb += f"""  out_arr{goran__kkiow} = info_to_array(info_from_table(out_table, {goran__kkiow + fdc__oisce}), in_arr{goran__kkiow}_typ)
"""
    siadg__zvb += f"""  out_arr_index = info_to_array(info_from_table(out_table, {fdc__oisce + jklgr__fjb}), ind_arr_typ)
"""
    siadg__zvb += '  shuffle_info = get_shuffle_info(out_table)\n'
    siadg__zvb += '  delete_table(out_table)\n'
    siadg__zvb += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{goran__kkiow}' for goran__kkiow in range
        (jklgr__fjb))
    siadg__zvb += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    siadg__zvb += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    siadg__zvb += '  return out_df, ({},), shuffle_info\n'.format(', '.join
        (f'out_key{goran__kkiow}' for goran__kkiow in range(fdc__oisce)))
    ojh__wjm = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    ojh__wjm.update({f'keys{goran__kkiow}_typ': keys.types[goran__kkiow] for
        goran__kkiow in range(fdc__oisce)})
    ojh__wjm.update({f'in_arr{goran__kkiow}_typ': df.data[goran__kkiow] for
        goran__kkiow in range(jklgr__fjb)})
    dnp__awpp = {}
    exec(siadg__zvb, ojh__wjm, dnp__awpp)
    vwlyy__vmrqd = dnp__awpp['impl']
    return vwlyy__vmrqd, ojh__wjm


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        bhmns__bjt = len(data.array_types)
        siadg__zvb = 'def impl(data, shuffle_info):\n'
        siadg__zvb += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{goran__kkiow}])' for goran__kkiow in
            range(bhmns__bjt)))
        siadg__zvb += '  table = arr_info_list_to_table(info_list)\n'
        siadg__zvb += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for goran__kkiow in range(bhmns__bjt):
            siadg__zvb += f"""  out_arr{goran__kkiow} = info_to_array(info_from_table(out_table, {goran__kkiow}), data._data[{goran__kkiow}])
"""
        siadg__zvb += '  delete_table(out_table)\n'
        siadg__zvb += '  delete_table(table)\n'
        siadg__zvb += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{goran__kkiow}' for goran__kkiow in
            range(bhmns__bjt))))
        dnp__awpp = {}
        exec(siadg__zvb, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, dnp__awpp)
        vwlyy__vmrqd = dnp__awpp['impl']
        return vwlyy__vmrqd
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            yjkbc__qrqb = bodo.utils.conversion.index_to_array(data)
            fwlq__xof = reverse_shuffle(yjkbc__qrqb, shuffle_info)
            return bodo.utils.conversion.index_from_array(fwlq__xof)
        return impl_index

    def impl_arr(data, shuffle_info):
        njn__ntm = [array_to_info(data)]
        noru__oue = arr_info_list_to_table(njn__ntm)
        hkc__mfqz = reverse_shuffle_table(noru__oue, shuffle_info)
        fwlq__xof = info_to_array(info_from_table(hkc__mfqz, 0), data)
        delete_table(hkc__mfqz)
        delete_table(noru__oue)
        return fwlq__xof
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    qlbr__tnrth = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna
        )
    rvc__bqieh = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', qlbr__tnrth, rvc__bqieh,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    ptfvy__bgpsp = get_overload_const_bool(ascending)
    ybc__mvl = grp.selection[0]
    siadg__zvb = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    crh__lss = (
        f"lambda S: S.value_counts(ascending={ptfvy__bgpsp}, _index_name='{ybc__mvl}')"
        )
    siadg__zvb += f'    return grp.apply({crh__lss})\n'
    dnp__awpp = {}
    exec(siadg__zvb, {'bodo': bodo}, dnp__awpp)
    vwlyy__vmrqd = dnp__awpp['impl']
    return vwlyy__vmrqd


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
    for nivnn__ogx in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, nivnn__ogx, no_unliteral=True
            )(create_unsupported_overload(f'DataFrameGroupBy.{nivnn__ogx}'))
    for nivnn__ogx in groupby_unsupported:
        overload_method(DataFrameGroupByType, nivnn__ogx, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{nivnn__ogx}'))
    for nivnn__ogx in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, nivnn__ogx, no_unliteral=True
            )(create_unsupported_overload(f'SeriesGroupBy.{nivnn__ogx}'))
    for nivnn__ogx in series_only_unsupported:
        overload_method(DataFrameGroupByType, nivnn__ogx, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{nivnn__ogx}'))
    for nivnn__ogx in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, nivnn__ogx, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{nivnn__ogx}'))


_install_groupby_unsupported()
