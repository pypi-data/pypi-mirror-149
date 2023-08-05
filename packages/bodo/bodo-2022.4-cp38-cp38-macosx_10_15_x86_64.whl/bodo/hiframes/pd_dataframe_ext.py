"""
Implement pd.DataFrame typing and data model handling.
"""
import json
import operator
from urllib.parse import urlparse, quote
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.cpython.listobj import ListInstance
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.series_indexing import SeriesIlocType
from bodo.hiframes.table import Table, TableType, decode_if_dict_table, get_table_data, set_table_data_codegen
from bodo.io import json_cpp
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_table_to_cpp_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.distributed_api import bcast_scalar
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_from_sequence
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.conversion import fix_arr_dtype, index_to_array
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import gen_const_tup, get_const_func_output_type, get_const_tup_vals
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, create_unsupported_overload, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_iterable_type, is_literal_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_str_arr_type, is_tuple_like_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import is_null_pointer
_json_write = types.ExternalFunction('json_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.bool_,
    types.voidptr))
ll.add_symbol('json_write', json_cpp.json_write)


class DataFrameType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, data=None, index=None, columns=None, dist=None,
        is_table_format=False):
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        if index is None:
            index = RangeIndexType(types.none)
        self.index = index
        self.columns = columns
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        self.is_table_format = is_table_format
        if columns is None:
            assert is_table_format, 'Determining columns at runtime is only supported for DataFrame with table format'
            self.table_type = TableType(tuple(data[:-1]), True)
        else:
            self.table_type = TableType(data) if is_table_format else None
        super(DataFrameType, self).__init__(name=
            f'dataframe({data}, {index}, {columns}, {dist}, {is_table_format})'
            )

    def __str__(self):
        if not self.has_runtime_cols and len(self.columns) > 20:
            jrdiw__huz = f'{len(self.data)} columns of types {set(self.data)}'
            wmwqt__tdy = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({jrdiw__huz}, {self.index}, {wmwqt__tdy}, {self.dist}, {self.is_table_format})'
                )
        return super().__str__()

    def copy(self, data=None, index=None, columns=None, dist=None,
        is_table_format=None):
        if data is None:
            data = self.data
        if columns is None:
            columns = self.columns
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if is_table_format is None:
            is_table_format = self.is_table_format
        return DataFrameType(data, index, columns, dist, is_table_format)

    @property
    def has_runtime_cols(self):
        return self.columns is None

    @property
    def runtime_colname_typ(self):
        return self.data[-1] if self.has_runtime_cols else None

    @property
    def runtime_data_types(self):
        return self.data[:-1] if self.has_runtime_cols else self.data

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return (self.data, self.index, self.columns, self.dist, self.
            is_table_format)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if (isinstance(other, DataFrameType) and len(other.data) == len(
            self.data) and other.columns == self.columns and other.
            has_runtime_cols == self.has_runtime_cols):
            unh__fnt = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(lgi__wldut.unify(typingctx, kjj__yvuz) if 
                lgi__wldut != kjj__yvuz else lgi__wldut for lgi__wldut,
                kjj__yvuz in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if unh__fnt is not None and None not in data:
                return DataFrameType(data, unh__fnt, self.columns, dist,
                    self.is_table_format)
        if isinstance(other, DataFrameType) and len(self.data
            ) == 0 and not self.has_runtime_cols:
            return other

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, DataFrameType) and self.data == other.data and
            self.index == other.index and self.columns == other.columns and
            self.dist != other.dist and self.has_runtime_cols == other.
            has_runtime_cols):
            return Conversion.safe

    def is_precise(self):
        return all(lgi__wldut.is_precise() for lgi__wldut in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        napy__qaepi = self.columns.index(col_name)
        rxf__meuh = tuple(list(self.data[:napy__qaepi]) + [new_type] + list
            (self.data[napy__qaepi + 1:]))
        return DataFrameType(rxf__meuh, self.index, self.columns, self.dist,
            self.is_table_format)


def check_runtime_cols_unsupported(df, func_name):
    if isinstance(df, DataFrameType) and df.has_runtime_cols:
        raise BodoError(
            f'{func_name} on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information.'
            )


class DataFramePayloadType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        super(DataFramePayloadType, self).__init__(name=
            f'DataFramePayloadType({df_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFramePayloadType)
class DataFramePayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        data_typ = types.Tuple(fe_type.df_type.data)
        if fe_type.df_type.is_table_format:
            data_typ = types.Tuple([fe_type.df_type.table_type])
        eyb__xvbbd = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            eyb__xvbbd.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, eyb__xvbbd)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        eyb__xvbbd = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, eyb__xvbbd)


make_attribute_wrapper(DataFrameType, 'meminfo', '_meminfo')


@infer_getattr
class DataFrameAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])

    @bound_function('df.head')
    def resolve_head(self, df, args, kws):
        func_name = 'DataFrame.head'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        eyap__ogmym = 'n',
        cpbkf__itu = {'n': 5}
        nhhtq__cnj, yxwx__cfpd = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, eyap__ogmym, cpbkf__itu)
        har__utid = yxwx__cfpd[0]
        if not is_overload_int(har__utid):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        timmz__axp = df.copy(is_table_format=False)
        return timmz__axp(*yxwx__cfpd).replace(pysig=nhhtq__cnj)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        gaqek__epeja = (df,) + args
        eyap__ogmym = 'df', 'method', 'min_periods'
        cpbkf__itu = {'method': 'pearson', 'min_periods': 1}
        hunn__wde = 'method',
        nhhtq__cnj, yxwx__cfpd = bodo.utils.typing.fold_typing_args(func_name,
            gaqek__epeja, kws, eyap__ogmym, cpbkf__itu, hunn__wde)
        nsry__bmi = yxwx__cfpd[2]
        if not is_overload_int(nsry__bmi):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        npwh__affq = []
        iuk__ypw = []
        for urtbw__als, ovmwi__afnun in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(ovmwi__afnun.dtype):
                npwh__affq.append(urtbw__als)
                iuk__ypw.append(types.Array(types.float64, 1, 'A'))
        if len(npwh__affq) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        iuk__ypw = tuple(iuk__ypw)
        npwh__affq = tuple(npwh__affq)
        index_typ = bodo.utils.typing.type_col_to_index(npwh__affq)
        timmz__axp = DataFrameType(iuk__ypw, index_typ, npwh__affq)
        return timmz__axp(*yxwx__cfpd).replace(pysig=nhhtq__cnj)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        mavbc__cpty = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        pyig__xzmp = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        bktq__kracz = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        zjdia__jdtf = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        hjf__lro = dict(raw=pyig__xzmp, result_type=bktq__kracz)
        hgwop__pec = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', hjf__lro, hgwop__pec,
            package_name='pandas', module_name='DataFrame')
        wvv__qdvsh = True
        if types.unliteral(mavbc__cpty) == types.unicode_type:
            if not is_overload_constant_str(mavbc__cpty):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            wvv__qdvsh = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        rwr__xkj = get_overload_const_int(axis)
        if wvv__qdvsh and rwr__xkj != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif rwr__xkj not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        fsw__nrosc = []
        for arr_typ in df.data:
            qroh__dsdh = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            hmiw__xpubs = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(qroh__dsdh), types.int64), {}
                ).return_type
            fsw__nrosc.append(hmiw__xpubs)
        odzu__lnm = types.none
        wgktw__mxl = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(urtbw__als) for urtbw__als in df.columns)),
            None)
        ldzz__lyjbn = types.BaseTuple.from_types(fsw__nrosc)
        txtza__bsdqf = types.Tuple([types.bool_] * len(ldzz__lyjbn))
        kohn__wzuxx = bodo.NullableTupleType(ldzz__lyjbn, txtza__bsdqf)
        xfo__nwk = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if xfo__nwk == types.NPDatetime('ns'):
            xfo__nwk = bodo.pd_timestamp_type
        if xfo__nwk == types.NPTimedelta('ns'):
            xfo__nwk = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(ldzz__lyjbn):
            rdasr__khqyj = HeterogeneousSeriesType(kohn__wzuxx, wgktw__mxl,
                xfo__nwk)
        else:
            rdasr__khqyj = SeriesType(ldzz__lyjbn.dtype, kohn__wzuxx,
                wgktw__mxl, xfo__nwk)
        ggqmd__vptn = rdasr__khqyj,
        if zjdia__jdtf is not None:
            ggqmd__vptn += tuple(zjdia__jdtf.types)
        try:
            if not wvv__qdvsh:
                kfrgx__ydetg = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(mavbc__cpty), self.context,
                    'DataFrame.apply', axis if rwr__xkj == 1 else None)
            else:
                kfrgx__ydetg = get_const_func_output_type(mavbc__cpty,
                    ggqmd__vptn, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as dsrz__aamzs:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                dsrz__aamzs))
        if wvv__qdvsh:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(kfrgx__ydetg, (SeriesType, HeterogeneousSeriesType)
                ) and kfrgx__ydetg.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(kfrgx__ydetg, HeterogeneousSeriesType):
                ogkxd__rkdn, sgxo__eoajk = kfrgx__ydetg.const_info
                if isinstance(kfrgx__ydetg.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    kidi__rwcqp = kfrgx__ydetg.data.tuple_typ.types
                elif isinstance(kfrgx__ydetg.data, types.Tuple):
                    kidi__rwcqp = kfrgx__ydetg.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                bjvk__arwm = tuple(to_nullable_type(dtype_to_array_type(
                    rfp__nccjk)) for rfp__nccjk in kidi__rwcqp)
                qxz__xwz = DataFrameType(bjvk__arwm, df.index, sgxo__eoajk)
            elif isinstance(kfrgx__ydetg, SeriesType):
                ykywm__nkef, sgxo__eoajk = kfrgx__ydetg.const_info
                bjvk__arwm = tuple(to_nullable_type(dtype_to_array_type(
                    kfrgx__ydetg.dtype)) for ogkxd__rkdn in range(ykywm__nkef))
                qxz__xwz = DataFrameType(bjvk__arwm, df.index, sgxo__eoajk)
            else:
                mat__fhdif = get_udf_out_arr_type(kfrgx__ydetg)
                qxz__xwz = SeriesType(mat__fhdif.dtype, mat__fhdif, df.
                    index, None)
        else:
            qxz__xwz = kfrgx__ydetg
        qbvv__jaqc = ', '.join("{} = ''".format(lgi__wldut) for lgi__wldut in
            kws.keys())
        azjs__tmyln = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {qbvv__jaqc}):
"""
        azjs__tmyln += '    pass\n'
        zxosd__hxatb = {}
        exec(azjs__tmyln, {}, zxosd__hxatb)
        cbfnq__fcxsc = zxosd__hxatb['apply_stub']
        nhhtq__cnj = numba.core.utils.pysignature(cbfnq__fcxsc)
        hns__cwhgr = (mavbc__cpty, axis, pyig__xzmp, bktq__kracz, zjdia__jdtf
            ) + tuple(kws.values())
        return signature(qxz__xwz, *hns__cwhgr).replace(pysig=nhhtq__cnj)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        eyap__ogmym = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        cpbkf__itu = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        hunn__wde = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        nhhtq__cnj, yxwx__cfpd = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, eyap__ogmym, cpbkf__itu, hunn__wde)
        flnb__cbctm = yxwx__cfpd[2]
        if not is_overload_constant_str(flnb__cbctm):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        wysph__esh = yxwx__cfpd[0]
        if not is_overload_none(wysph__esh) and not (is_overload_int(
            wysph__esh) or is_overload_constant_str(wysph__esh)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(wysph__esh):
            meym__muwe = get_overload_const_str(wysph__esh)
            if meym__muwe not in df.columns:
                raise BodoError(f'{func_name}: {meym__muwe} column not found.')
        elif is_overload_int(wysph__esh):
            smaaj__xtlat = get_overload_const_int(wysph__esh)
            if smaaj__xtlat > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {smaaj__xtlat} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            wysph__esh = df.columns[wysph__esh]
        wti__znnmm = yxwx__cfpd[1]
        if not is_overload_none(wti__znnmm) and not (is_overload_int(
            wti__znnmm) or is_overload_constant_str(wti__znnmm)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(wti__znnmm):
            hcing__ivu = get_overload_const_str(wti__znnmm)
            if hcing__ivu not in df.columns:
                raise BodoError(f'{func_name}: {hcing__ivu} column not found.')
        elif is_overload_int(wti__znnmm):
            ademw__nbid = get_overload_const_int(wti__znnmm)
            if ademw__nbid > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {ademw__nbid} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            wti__znnmm = df.columns[wti__znnmm]
        rpgnw__vpjff = yxwx__cfpd[3]
        if not is_overload_none(rpgnw__vpjff) and not is_tuple_like_type(
            rpgnw__vpjff):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        ipfc__aan = yxwx__cfpd[10]
        if not is_overload_none(ipfc__aan) and not is_overload_constant_str(
            ipfc__aan):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        kzhod__krt = yxwx__cfpd[12]
        if not is_overload_bool(kzhod__krt):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        icr__xow = yxwx__cfpd[17]
        if not is_overload_none(icr__xow) and not is_tuple_like_type(icr__xow):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        ggqdf__mcw = yxwx__cfpd[18]
        if not is_overload_none(ggqdf__mcw) and not is_tuple_like_type(
            ggqdf__mcw):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        nvk__oodlg = yxwx__cfpd[22]
        if not is_overload_none(nvk__oodlg) and not is_overload_int(nvk__oodlg
            ):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        bpnx__yshnk = yxwx__cfpd[29]
        if not is_overload_none(bpnx__yshnk) and not is_overload_constant_str(
            bpnx__yshnk):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        kfyyx__uldq = yxwx__cfpd[30]
        if not is_overload_none(kfyyx__uldq) and not is_overload_constant_str(
            kfyyx__uldq):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        plzh__nuiz = types.List(types.mpl_line_2d_type)
        flnb__cbctm = get_overload_const_str(flnb__cbctm)
        if flnb__cbctm == 'scatter':
            if is_overload_none(wysph__esh) and is_overload_none(wti__znnmm):
                raise BodoError(
                    f'{func_name}: {flnb__cbctm} requires an x and y column.')
            elif is_overload_none(wysph__esh):
                raise BodoError(
                    f'{func_name}: {flnb__cbctm} x column is missing.')
            elif is_overload_none(wti__znnmm):
                raise BodoError(
                    f'{func_name}: {flnb__cbctm} y column is missing.')
            plzh__nuiz = types.mpl_path_collection_type
        elif flnb__cbctm != 'line':
            raise BodoError(
                f'{func_name}: {flnb__cbctm} plot is not supported.')
        return signature(plzh__nuiz, *yxwx__cfpd).replace(pysig=nhhtq__cnj)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            umg__ypjsn = df.columns.index(attr)
            arr_typ = df.data[umg__ypjsn]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            jdx__vul = []
            rxf__meuh = []
            mub__zzowb = False
            for i, mpdjc__pwtp in enumerate(df.columns):
                if mpdjc__pwtp[0] != attr:
                    continue
                mub__zzowb = True
                jdx__vul.append(mpdjc__pwtp[1] if len(mpdjc__pwtp) == 2 else
                    mpdjc__pwtp[1:])
                rxf__meuh.append(df.data[i])
            if mub__zzowb:
                return DataFrameType(tuple(rxf__meuh), df.index, tuple(
                    jdx__vul))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        ywgqe__sjv = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(ywgqe__sjv)
        return lambda tup, idx: tup[val_ind]


def decref_df_data(context, builder, payload, df_type):
    if df_type.is_table_format:
        context.nrt.decref(builder, df_type.table_type, builder.
            extract_value(payload.data, 0))
        context.nrt.decref(builder, df_type.index, payload.index)
        if df_type.has_runtime_cols:
            context.nrt.decref(builder, df_type.data[-1], payload.columns)
        return
    for i in range(len(df_type.data)):
        gdxtt__ikod = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], gdxtt__ikod)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    asbt__xofcm = builder.module
    ufv__ugnqy = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    jqisd__lmyto = cgutils.get_or_insert_function(asbt__xofcm, ufv__ugnqy,
        name='.dtor.df.{}'.format(df_type))
    if not jqisd__lmyto.is_declaration:
        return jqisd__lmyto
    jqisd__lmyto.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(jqisd__lmyto.append_basic_block())
    bhvm__nvl = jqisd__lmyto.args[0]
    jppl__uhz = context.get_value_type(payload_type).as_pointer()
    mlr__urziq = builder.bitcast(bhvm__nvl, jppl__uhz)
    payload = context.make_helper(builder, payload_type, ref=mlr__urziq)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        qtakh__thk = context.get_python_api(builder)
        pbs__sbzgy = qtakh__thk.gil_ensure()
        qtakh__thk.decref(payload.parent)
        qtakh__thk.gil_release(pbs__sbzgy)
    builder.ret_void()
    return jqisd__lmyto


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    rgakg__kpwq = cgutils.create_struct_proxy(payload_type)(context, builder)
    rgakg__kpwq.data = data_tup
    rgakg__kpwq.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        rgakg__kpwq.columns = colnames
    wfhf__kucmk = context.get_value_type(payload_type)
    bdcl__rhvae = context.get_abi_sizeof(wfhf__kucmk)
    zjtlk__wvvc = define_df_dtor(context, builder, df_type, payload_type)
    ynkb__mmfbn = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, bdcl__rhvae), zjtlk__wvvc)
    bnnmk__icrc = context.nrt.meminfo_data(builder, ynkb__mmfbn)
    qgxw__aims = builder.bitcast(bnnmk__icrc, wfhf__kucmk.as_pointer())
    avxkt__kbi = cgutils.create_struct_proxy(df_type)(context, builder)
    avxkt__kbi.meminfo = ynkb__mmfbn
    if parent is None:
        avxkt__kbi.parent = cgutils.get_null_value(avxkt__kbi.parent.type)
    else:
        avxkt__kbi.parent = parent
        rgakg__kpwq.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            qtakh__thk = context.get_python_api(builder)
            pbs__sbzgy = qtakh__thk.gil_ensure()
            qtakh__thk.incref(parent)
            qtakh__thk.gil_release(pbs__sbzgy)
    builder.store(rgakg__kpwq._getvalue(), qgxw__aims)
    return avxkt__kbi._getvalue()


@intrinsic
def init_runtime_cols_dataframe(typingctx, data_typ, index_typ,
    colnames_index_typ=None):
    assert isinstance(data_typ, types.BaseTuple) and isinstance(data_typ.
        dtype, TableType
        ) and data_typ.dtype.has_runtime_cols, 'init_runtime_cols_dataframe must be called with a table that determines columns at runtime.'
    assert bodo.hiframes.pd_index_ext.is_pd_index_type(colnames_index_typ
        ) or isinstance(colnames_index_typ, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType), 'Column names must be an index'
    if isinstance(data_typ.dtype.arr_types, types.UniTuple):
        addie__pjw = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype.
            arr_types)
    else:
        addie__pjw = [rfp__nccjk for rfp__nccjk in data_typ.dtype.arr_types]
    igc__uxyv = DataFrameType(tuple(addie__pjw + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        uja__luie = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return uja__luie
    sig = signature(igc__uxyv, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    ykywm__nkef = len(data_tup_typ.types)
    if ykywm__nkef == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if ykywm__nkef == 1 and isinstance(data_tup_typ.types[0], TableType):
        ykywm__nkef = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == ykywm__nkef, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    nkvib__vugmi = data_tup_typ.types
    if ykywm__nkef != 0 and isinstance(data_tup_typ.types[0], TableType):
        nkvib__vugmi = data_tup_typ.types[0].arr_types
        is_table_format = True
    igc__uxyv = DataFrameType(nkvib__vugmi, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            otl__mcf = cgutils.create_struct_proxy(igc__uxyv.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = otl__mcf.parent
        uja__luie = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return uja__luie
    sig = signature(igc__uxyv, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        avxkt__kbi = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, avxkt__kbi.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        rgakg__kpwq = get_dataframe_payload(context, builder, df_typ, args[0])
        dvv__tkxsm = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[dvv__tkxsm]
        if df_typ.is_table_format:
            otl__mcf = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(rgakg__kpwq.data, 0))
            bdgx__jdu = df_typ.table_type.type_to_blk[arr_typ]
            kmd__fbkja = getattr(otl__mcf, f'block_{bdgx__jdu}')
            dcy__wbqz = ListInstance(context, builder, types.List(arr_typ),
                kmd__fbkja)
            lzd__zkem = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[dvv__tkxsm])
            gdxtt__ikod = dcy__wbqz.getitem(lzd__zkem)
        else:
            gdxtt__ikod = builder.extract_value(rgakg__kpwq.data, dvv__tkxsm)
        try__jfjs = cgutils.alloca_once_value(builder, gdxtt__ikod)
        nefju__tyfr = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, try__jfjs, nefju__tyfr)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    ynkb__mmfbn = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, ynkb__mmfbn)
    jppl__uhz = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, jppl__uhz)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    igc__uxyv = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        igc__uxyv = types.Tuple([TableType(df_typ.data)])
    sig = signature(igc__uxyv, df_typ)

    def codegen(context, builder, signature, args):
        rgakg__kpwq = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            rgakg__kpwq.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        rgakg__kpwq = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index,
            rgakg__kpwq.index)
    igc__uxyv = df_typ.index
    sig = signature(igc__uxyv, df_typ)
    return sig, codegen


def get_dataframe_data(df, i):
    return df[i]


@infer_global(get_dataframe_data)
class GetDataFrameDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        if not is_overload_constant_int(args[1]):
            raise_bodo_error(
                'Selecting a DataFrame column requires a constant column label'
                )
        df = args[0]
        check_runtime_cols_unsupported(df, 'get_dataframe_data')
        i = get_overload_const_int(args[1])
        timmz__axp = df.data[i]
        return timmz__axp(*args)


GetDataFrameDataInfer.prefer_literal = True


def get_dataframe_data_impl(df, i):
    if df.is_table_format:

        def _impl(df, i):
            if has_parent(df) and _column_needs_unboxing(df, i):
                bodo.hiframes.boxing.unbox_dataframe_column(df, i)
            return get_table_data(_get_dataframe_data(df)[0], i)
        return _impl

    def _impl(df, i):
        if has_parent(df) and _column_needs_unboxing(df, i):
            bodo.hiframes.boxing.unbox_dataframe_column(df, i)
        return _get_dataframe_data(df)[i]
    return _impl


@intrinsic
def get_dataframe_table(typingctx, df_typ=None):
    assert df_typ.is_table_format, 'get_dataframe_table() expects table format'

    def codegen(context, builder, signature, args):
        rgakg__kpwq = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(rgakg__kpwq.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        rgakg__kpwq = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, rgakg__kpwq.columns)
    return df_typ.runtime_colname_typ(df_typ), codegen


@lower_builtin(get_dataframe_data, DataFrameType, types.IntegerLiteral)
def lower_get_dataframe_data(context, builder, sig, args):
    impl = get_dataframe_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_dataframe_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_index',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_table',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func


def alias_ext_init_dataframe(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 3
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_dataframe',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_init_dataframe


def init_dataframe_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 3 and not kws
    data_tup = args[0]
    index = args[1]
    ldzz__lyjbn = self.typemap[data_tup.name]
    if any(is_tuple_like_type(rfp__nccjk) for rfp__nccjk in ldzz__lyjbn.types):
        return None
    if equiv_set.has_shape(data_tup):
        ntiue__rkf = equiv_set.get_shape(data_tup)
        if len(ntiue__rkf) > 1:
            equiv_set.insert_equiv(*ntiue__rkf)
        if len(ntiue__rkf) > 0:
            wgktw__mxl = self.typemap[index.name]
            if not isinstance(wgktw__mxl, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(ntiue__rkf[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(ntiue__rkf[0], len(
                ntiue__rkf)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    bwlbk__qfsdp = args[0]
    data_types = self.typemap[bwlbk__qfsdp.name].data
    if any(is_tuple_like_type(rfp__nccjk) for rfp__nccjk in data_types):
        return None
    if equiv_set.has_shape(bwlbk__qfsdp):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            bwlbk__qfsdp)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    bwlbk__qfsdp = args[0]
    wgktw__mxl = self.typemap[bwlbk__qfsdp.name].index
    if isinstance(wgktw__mxl, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(bwlbk__qfsdp):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            bwlbk__qfsdp)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    bwlbk__qfsdp = args[0]
    if equiv_set.has_shape(bwlbk__qfsdp):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            bwlbk__qfsdp), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    bwlbk__qfsdp = args[0]
    if equiv_set.has_shape(bwlbk__qfsdp):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            bwlbk__qfsdp)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    dvv__tkxsm = get_overload_const_int(c_ind_typ)
    if df_typ.data[dvv__tkxsm] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        ayc__dolw, ogkxd__rkdn, qnato__eca = args
        rgakg__kpwq = get_dataframe_payload(context, builder, df_typ, ayc__dolw
            )
        if df_typ.is_table_format:
            otl__mcf = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(rgakg__kpwq.data, 0))
            bdgx__jdu = df_typ.table_type.type_to_blk[arr_typ]
            kmd__fbkja = getattr(otl__mcf, f'block_{bdgx__jdu}')
            dcy__wbqz = ListInstance(context, builder, types.List(arr_typ),
                kmd__fbkja)
            lzd__zkem = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[dvv__tkxsm])
            dcy__wbqz.setitem(lzd__zkem, qnato__eca, True)
        else:
            gdxtt__ikod = builder.extract_value(rgakg__kpwq.data, dvv__tkxsm)
            context.nrt.decref(builder, df_typ.data[dvv__tkxsm], gdxtt__ikod)
            rgakg__kpwq.data = builder.insert_value(rgakg__kpwq.data,
                qnato__eca, dvv__tkxsm)
            context.nrt.incref(builder, arr_typ, qnato__eca)
        avxkt__kbi = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=ayc__dolw)
        payload_type = DataFramePayloadType(df_typ)
        mlr__urziq = context.nrt.meminfo_data(builder, avxkt__kbi.meminfo)
        jppl__uhz = context.get_value_type(payload_type).as_pointer()
        mlr__urziq = builder.bitcast(mlr__urziq, jppl__uhz)
        builder.store(rgakg__kpwq._getvalue(), mlr__urziq)
        return impl_ret_borrowed(context, builder, df_typ, ayc__dolw)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        jxny__bpubc = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        xsyk__wnl = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=jxny__bpubc)
        qqr__jxxn = get_dataframe_payload(context, builder, df_typ, jxny__bpubc
            )
        avxkt__kbi = construct_dataframe(context, builder, signature.
            return_type, qqr__jxxn.data, index_val, xsyk__wnl.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), qqr__jxxn.data)
        return avxkt__kbi
    igc__uxyv = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(igc__uxyv, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    ykywm__nkef = len(df_type.columns)
    mihx__obsu = ykywm__nkef
    szp__gav = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    ujpt__ndgl = col_name not in df_type.columns
    dvv__tkxsm = ykywm__nkef
    if ujpt__ndgl:
        szp__gav += arr_type,
        column_names += col_name,
        mihx__obsu += 1
    else:
        dvv__tkxsm = df_type.columns.index(col_name)
        szp__gav = tuple(arr_type if i == dvv__tkxsm else szp__gav[i] for i in
            range(ykywm__nkef))

    def codegen(context, builder, signature, args):
        ayc__dolw, ogkxd__rkdn, qnato__eca = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, ayc__dolw)
        zdlra__utbu = cgutils.create_struct_proxy(df_type)(context, builder,
            value=ayc__dolw)
        if df_type.is_table_format:
            uylhy__rhc = df_type.table_type
            xpdm__gzva = builder.extract_value(in_dataframe_payload.data, 0)
            zdwn__feqb = TableType(szp__gav)
            hct__ywbzf = set_table_data_codegen(context, builder,
                uylhy__rhc, xpdm__gzva, zdwn__feqb, arr_type, qnato__eca,
                dvv__tkxsm, ujpt__ndgl)
            data_tup = context.make_tuple(builder, types.Tuple([zdwn__feqb]
                ), [hct__ywbzf])
        else:
            nkvib__vugmi = [(builder.extract_value(in_dataframe_payload.
                data, i) if i != dvv__tkxsm else qnato__eca) for i in range
                (ykywm__nkef)]
            if ujpt__ndgl:
                nkvib__vugmi.append(qnato__eca)
            for bwlbk__qfsdp, bds__izivj in zip(nkvib__vugmi, szp__gav):
                context.nrt.incref(builder, bds__izivj, bwlbk__qfsdp)
            data_tup = context.make_tuple(builder, types.Tuple(szp__gav),
                nkvib__vugmi)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        ffm__fozyd = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, zdlra__utbu.parent, None)
        if not ujpt__ndgl and arr_type == df_type.data[dvv__tkxsm]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            mlr__urziq = context.nrt.meminfo_data(builder, zdlra__utbu.meminfo)
            jppl__uhz = context.get_value_type(payload_type).as_pointer()
            mlr__urziq = builder.bitcast(mlr__urziq, jppl__uhz)
            zrs__gcjcw = get_dataframe_payload(context, builder, df_type,
                ffm__fozyd)
            builder.store(zrs__gcjcw._getvalue(), mlr__urziq)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, zdwn__feqb, builder.
                    extract_value(data_tup, 0))
            else:
                for bwlbk__qfsdp, bds__izivj in zip(nkvib__vugmi, szp__gav):
                    context.nrt.incref(builder, bds__izivj, bwlbk__qfsdp)
        has_parent = cgutils.is_not_null(builder, zdlra__utbu.parent)
        with builder.if_then(has_parent):
            qtakh__thk = context.get_python_api(builder)
            pbs__sbzgy = qtakh__thk.gil_ensure()
            iew__ocitk = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, qnato__eca)
            urtbw__als = numba.core.pythonapi._BoxContext(context, builder,
                qtakh__thk, iew__ocitk)
            pah__kirln = urtbw__als.pyapi.from_native_value(arr_type,
                qnato__eca, urtbw__als.env_manager)
            if isinstance(col_name, str):
                ggs__fyac = context.insert_const_string(builder.module,
                    col_name)
                gszg__zxkat = qtakh__thk.string_from_string(ggs__fyac)
            else:
                assert isinstance(col_name, int)
                gszg__zxkat = qtakh__thk.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            qtakh__thk.object_setitem(zdlra__utbu.parent, gszg__zxkat,
                pah__kirln)
            qtakh__thk.decref(pah__kirln)
            qtakh__thk.decref(gszg__zxkat)
            qtakh__thk.gil_release(pbs__sbzgy)
        return ffm__fozyd
    igc__uxyv = DataFrameType(szp__gav, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(igc__uxyv, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    ykywm__nkef = len(pyval.columns)
    nkvib__vugmi = []
    for i in range(ykywm__nkef):
        imzx__oqwla = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            pah__kirln = imzx__oqwla.array
        else:
            pah__kirln = imzx__oqwla.values
        nkvib__vugmi.append(pah__kirln)
    nkvib__vugmi = tuple(nkvib__vugmi)
    if df_type.is_table_format:
        otl__mcf = context.get_constant_generic(builder, df_type.table_type,
            Table(nkvib__vugmi))
        data_tup = lir.Constant.literal_struct([otl__mcf])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], mpdjc__pwtp) for
            i, mpdjc__pwtp in enumerate(nkvib__vugmi)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    gxoc__nfu = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, gxoc__nfu])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    ghwwo__jldoq = context.get_constant(types.int64, -1)
    oild__qak = context.get_constant_null(types.voidptr)
    ynkb__mmfbn = lir.Constant.literal_struct([ghwwo__jldoq, oild__qak,
        oild__qak, payload, ghwwo__jldoq])
    ynkb__mmfbn = cgutils.global_constant(builder, '.const.meminfo',
        ynkb__mmfbn).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([ynkb__mmfbn, gxoc__nfu])


@lower_cast(DataFrameType, DataFrameType)
def cast_df_to_df(context, builder, fromty, toty, val):
    if (fromty.data == toty.data and fromty.index == toty.index and fromty.
        columns == toty.columns and fromty.is_table_format == toty.
        is_table_format and fromty.dist != toty.dist and fromty.
        has_runtime_cols == toty.has_runtime_cols):
        return val
    if not fromty.has_runtime_cols and not toty.has_runtime_cols and len(fromty
        .data) == 0 and len(toty.columns):
        return _cast_empty_df(context, builder, toty)
    if len(fromty.data) != len(toty.data) or fromty.data != toty.data and any(
        context.typing_context.unify_pairs(fromty.data[i], toty.data[i]) is
        None for i in range(len(fromty.data))
        ) or fromty.has_runtime_cols != toty.has_runtime_cols:
        raise BodoError(f'Invalid dataframe cast from {fromty} to {toty}')
    in_dataframe_payload = get_dataframe_payload(context, builder, fromty, val)
    if isinstance(fromty.index, RangeIndexType) and isinstance(toty.index,
        NumericIndexType):
        unh__fnt = context.cast(builder, in_dataframe_payload.index, fromty
            .index, toty.index)
    else:
        unh__fnt = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, unh__fnt)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        rxf__meuh = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                rxf__meuh)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), rxf__meuh)
    elif not fromty.is_table_format and toty.is_table_format:
        rxf__meuh = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        rxf__meuh = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        rxf__meuh = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        rxf__meuh = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, rxf__meuh, unh__fnt,
        in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    kxohj__uknx = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        nolcw__qjt = get_index_data_arr_types(toty.index)[0]
        okxfb__brj = bodo.utils.transform.get_type_alloc_counts(nolcw__qjt) - 1
        xgbpe__czjo = ', '.join('0' for ogkxd__rkdn in range(okxfb__brj))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(xgbpe__czjo, ', ' if okxfb__brj == 1 else ''))
        kxohj__uknx['index_arr_type'] = nolcw__qjt
    ubpxx__vnjp = []
    for i, arr_typ in enumerate(toty.data):
        okxfb__brj = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        xgbpe__czjo = ', '.join('0' for ogkxd__rkdn in range(okxfb__brj))
        vhe__hmcu = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, xgbpe__czjo, ', ' if okxfb__brj == 1 else ''))
        ubpxx__vnjp.append(vhe__hmcu)
        kxohj__uknx[f'arr_type{i}'] = arr_typ
    ubpxx__vnjp = ', '.join(ubpxx__vnjp)
    azjs__tmyln = 'def impl():\n'
    shpue__ipghf = bodo.hiframes.dataframe_impl._gen_init_df(azjs__tmyln,
        toty.columns, ubpxx__vnjp, index, kxohj__uknx)
    df = context.compile_internal(builder, shpue__ipghf, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    atye__pejkx = toty.table_type
    otl__mcf = cgutils.create_struct_proxy(atye__pejkx)(context, builder)
    otl__mcf.parent = in_dataframe_payload.parent
    for rfp__nccjk, bdgx__jdu in atye__pejkx.type_to_blk.items():
        nqdz__aznbo = context.get_constant(types.int64, len(atye__pejkx.
            block_to_arr_ind[bdgx__jdu]))
        ogkxd__rkdn, ratxy__tmg = ListInstance.allocate_ex(context, builder,
            types.List(rfp__nccjk), nqdz__aznbo)
        ratxy__tmg.size = nqdz__aznbo
        setattr(otl__mcf, f'block_{bdgx__jdu}', ratxy__tmg.value)
    for i, rfp__nccjk in enumerate(fromty.data):
        aoyx__ljeaa = toty.data[i]
        if rfp__nccjk != aoyx__ljeaa:
            kyodx__jxnw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*kyodx__jxnw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        gdxtt__ikod = builder.extract_value(in_dataframe_payload.data, i)
        if rfp__nccjk != aoyx__ljeaa:
            irr__snp = context.cast(builder, gdxtt__ikod, rfp__nccjk,
                aoyx__ljeaa)
            iqpp__nkpz = False
        else:
            irr__snp = gdxtt__ikod
            iqpp__nkpz = True
        bdgx__jdu = atye__pejkx.type_to_blk[rfp__nccjk]
        kmd__fbkja = getattr(otl__mcf, f'block_{bdgx__jdu}')
        dcy__wbqz = ListInstance(context, builder, types.List(rfp__nccjk),
            kmd__fbkja)
        lzd__zkem = context.get_constant(types.int64, atye__pejkx.
            block_offsets[i])
        dcy__wbqz.setitem(lzd__zkem, irr__snp, iqpp__nkpz)
    data_tup = context.make_tuple(builder, types.Tuple([atye__pejkx]), [
        otl__mcf._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    nkvib__vugmi = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            kyodx__jxnw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*kyodx__jxnw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            gdxtt__ikod = builder.extract_value(in_dataframe_payload.data, i)
            irr__snp = context.cast(builder, gdxtt__ikod, fromty.data[i],
                toty.data[i])
            iqpp__nkpz = False
        else:
            irr__snp = builder.extract_value(in_dataframe_payload.data, i)
            iqpp__nkpz = True
        if iqpp__nkpz:
            context.nrt.incref(builder, toty.data[i], irr__snp)
        nkvib__vugmi.append(irr__snp)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), nkvib__vugmi
        )
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    uylhy__rhc = fromty.table_type
    xpdm__gzva = cgutils.create_struct_proxy(uylhy__rhc)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    zdwn__feqb = toty.table_type
    hct__ywbzf = cgutils.create_struct_proxy(zdwn__feqb)(context, builder)
    hct__ywbzf.parent = in_dataframe_payload.parent
    for rfp__nccjk, bdgx__jdu in zdwn__feqb.type_to_blk.items():
        nqdz__aznbo = context.get_constant(types.int64, len(zdwn__feqb.
            block_to_arr_ind[bdgx__jdu]))
        ogkxd__rkdn, ratxy__tmg = ListInstance.allocate_ex(context, builder,
            types.List(rfp__nccjk), nqdz__aznbo)
        ratxy__tmg.size = nqdz__aznbo
        setattr(hct__ywbzf, f'block_{bdgx__jdu}', ratxy__tmg.value)
    for i in range(len(fromty.data)):
        xmr__cons = fromty.data[i]
        aoyx__ljeaa = toty.data[i]
        if xmr__cons != aoyx__ljeaa:
            kyodx__jxnw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*kyodx__jxnw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        obhwr__imum = uylhy__rhc.type_to_blk[xmr__cons]
        vyd__nzt = getattr(xpdm__gzva, f'block_{obhwr__imum}')
        dweda__qybfl = ListInstance(context, builder, types.List(xmr__cons),
            vyd__nzt)
        yqm__ppo = context.get_constant(types.int64, uylhy__rhc.
            block_offsets[i])
        gdxtt__ikod = dweda__qybfl.getitem(yqm__ppo)
        if xmr__cons != aoyx__ljeaa:
            irr__snp = context.cast(builder, gdxtt__ikod, xmr__cons,
                aoyx__ljeaa)
            iqpp__nkpz = False
        else:
            irr__snp = gdxtt__ikod
            iqpp__nkpz = True
        mon__xzga = zdwn__feqb.type_to_blk[rfp__nccjk]
        ratxy__tmg = getattr(hct__ywbzf, f'block_{mon__xzga}')
        nyfx__yoh = ListInstance(context, builder, types.List(aoyx__ljeaa),
            ratxy__tmg)
        qorhr__wyi = context.get_constant(types.int64, zdwn__feqb.
            block_offsets[i])
        nyfx__yoh.setitem(qorhr__wyi, irr__snp, iqpp__nkpz)
    data_tup = context.make_tuple(builder, types.Tuple([zdwn__feqb]), [
        hct__ywbzf._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    atye__pejkx = fromty.table_type
    otl__mcf = cgutils.create_struct_proxy(atye__pejkx)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    nkvib__vugmi = []
    for i, rfp__nccjk in enumerate(toty.data):
        xmr__cons = fromty.data[i]
        if rfp__nccjk != xmr__cons:
            kyodx__jxnw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*kyodx__jxnw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        bdgx__jdu = atye__pejkx.type_to_blk[rfp__nccjk]
        kmd__fbkja = getattr(otl__mcf, f'block_{bdgx__jdu}')
        dcy__wbqz = ListInstance(context, builder, types.List(rfp__nccjk),
            kmd__fbkja)
        lzd__zkem = context.get_constant(types.int64, atye__pejkx.
            block_offsets[i])
        gdxtt__ikod = dcy__wbqz.getitem(lzd__zkem)
        if rfp__nccjk != xmr__cons:
            irr__snp = context.cast(builder, gdxtt__ikod, xmr__cons, rfp__nccjk
                )
            iqpp__nkpz = False
        else:
            irr__snp = gdxtt__ikod
            iqpp__nkpz = True
        if iqpp__nkpz:
            context.nrt.incref(builder, rfp__nccjk, irr__snp)
        nkvib__vugmi.append(irr__snp)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), nkvib__vugmi
        )
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    ebpj__aljog, ubpxx__vnjp, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    gjdk__ofht = gen_const_tup(ebpj__aljog)
    azjs__tmyln = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    azjs__tmyln += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(ubpxx__vnjp, index_arg, gjdk__ofht))
    zxosd__hxatb = {}
    exec(azjs__tmyln, {'bodo': bodo, 'np': np}, zxosd__hxatb)
    fvniv__mzw = zxosd__hxatb['_init_df']
    return fvniv__mzw


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    igc__uxyv = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ
        .index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(igc__uxyv, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    igc__uxyv = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ
        .index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(igc__uxyv, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    toa__hxu = ''
    if not is_overload_none(dtype):
        toa__hxu = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        ykywm__nkef = (len(data.types) - 1) // 2
        bryzr__tasre = [rfp__nccjk.literal_value for rfp__nccjk in data.
            types[1:ykywm__nkef + 1]]
        data_val_types = dict(zip(bryzr__tasre, data.types[ykywm__nkef + 1:]))
        nkvib__vugmi = ['data[{}]'.format(i) for i in range(ykywm__nkef + 1,
            2 * ykywm__nkef + 1)]
        data_dict = dict(zip(bryzr__tasre, nkvib__vugmi))
        if is_overload_none(index):
            for i, rfp__nccjk in enumerate(data.types[ykywm__nkef + 1:]):
                if isinstance(rfp__nccjk, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(ykywm__nkef + 1 + i))
                    index_is_none = False
                    break
    elif is_overload_none(data):
        data_dict = {}
        data_val_types = {}
    else:
        if not (isinstance(data, types.Array) and data.ndim == 2):
            raise BodoError(
                'pd.DataFrame() only supports constant dictionary and array input'
                )
        if is_overload_none(columns):
            raise BodoError(
                "pd.DataFrame() 'columns' argument is required when an array is passed as data"
                )
        zdlq__utzc = '.copy()' if copy else ''
        tho__jcskt = get_overload_const_list(columns)
        ykywm__nkef = len(tho__jcskt)
        data_val_types = {urtbw__als: data.copy(ndim=1) for urtbw__als in
            tho__jcskt}
        nkvib__vugmi = ['data[:,{}]{}'.format(i, zdlq__utzc) for i in range
            (ykywm__nkef)]
        data_dict = dict(zip(tho__jcskt, nkvib__vugmi))
    if is_overload_none(columns):
        col_names = data_dict.keys()
    else:
        col_names = get_overload_const_list(columns)
    df_len = _get_df_len_from_info(data_dict, data_val_types, col_names,
        index_is_none, index_arg)
    _fill_null_arrays(data_dict, col_names, df_len, dtype)
    if index_is_none:
        if is_overload_none(data):
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_binary_str_index(bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0))'
                )
        else:
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, {}, 1, None)'
                .format(df_len))
    ubpxx__vnjp = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[urtbw__als], df_len, toa__hxu) for urtbw__als in
        col_names))
    if len(col_names) == 0:
        ubpxx__vnjp = '()'
    return col_names, ubpxx__vnjp, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for urtbw__als in col_names:
        if urtbw__als in data_dict and is_iterable_type(data_val_types[
            urtbw__als]):
            df_len = 'len({})'.format(data_dict[urtbw__als])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(urtbw__als in data_dict for urtbw__als in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    fzn__yzuh = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for urtbw__als in col_names:
        if urtbw__als not in data_dict:
            data_dict[urtbw__als] = fzn__yzuh


@infer_global(len)
class LenTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        if isinstance(args[0], (DataFrameType, bodo.TableType)):
            return types.int64(*args)


@lower_builtin(len, DataFrameType)
def table_len_lower(context, builder, sig, args):
    impl = df_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_len_overload(df):
    if not isinstance(df, DataFrameType):
        return
    if df.has_runtime_cols:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            rfp__nccjk = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(rfp__nccjk)
        return impl
    if len(df.columns) == 0:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
        return impl

    def impl(df):
        if is_null_pointer(df._meminfo):
            return 0
        return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0))
    return impl


@infer_global(operator.getitem)
class GetItemTuple(AbstractTemplate):
    key = operator.getitem

    def generic(self, args, kws):
        tup, idx = args
        if not isinstance(tup, types.BaseTuple) or not isinstance(idx,
            types.IntegerLiteral):
            return
        giew__brmt = idx.literal_value
        if isinstance(giew__brmt, int):
            timmz__axp = tup.types[giew__brmt]
        elif isinstance(giew__brmt, slice):
            timmz__axp = types.BaseTuple.from_types(tup.types[giew__brmt])
        return signature(timmz__axp, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    sya__lrret, idx = sig.args
    idx = idx.literal_value
    tup, ogkxd__rkdn = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(sya__lrret)
        if not 0 <= idx < len(sya__lrret):
            raise IndexError('cannot index at %d in %s' % (idx, sya__lrret))
        pfbf__hdz = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        kdsek__iszzr = cgutils.unpack_tuple(builder, tup)[idx]
        pfbf__hdz = context.make_tuple(builder, sig.return_type, kdsek__iszzr)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, pfbf__hdz)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, cusdk__bsi, suffix_x,
            suffix_y, is_join, indicator, _bodo_na_equal, uwj__bpz) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        mmr__ztljh = set(left_on) & set(right_on)
        ukv__dgoyt = set(left_df.columns) & set(right_df.columns)
        wzbwf__zpl = ukv__dgoyt - mmr__ztljh
        ndpvz__fktfu = '$_bodo_index_' in left_on
        tpm__qcgv = '$_bodo_index_' in right_on
        how = get_overload_const_str(cusdk__bsi)
        usxzy__mipbs = how in {'left', 'outer'}
        tyt__vftsi = how in {'right', 'outer'}
        columns = []
        data = []
        if ndpvz__fktfu:
            amz__xokjd = bodo.utils.typing.get_index_data_arr_types(left_df
                .index)[0]
        else:
            amz__xokjd = left_df.data[left_df.columns.index(left_on[0])]
        if tpm__qcgv:
            lgj__xns = bodo.utils.typing.get_index_data_arr_types(right_df.
                index)[0]
        else:
            lgj__xns = right_df.data[right_df.columns.index(right_on[0])]
        if ndpvz__fktfu and not tpm__qcgv and not is_join.literal_value:
            efxwo__ehzm = right_on[0]
            if efxwo__ehzm in left_df.columns:
                columns.append(efxwo__ehzm)
                if (lgj__xns == bodo.dict_str_arr_type and amz__xokjd ==
                    bodo.string_array_type):
                    ywc__cce = bodo.string_array_type
                else:
                    ywc__cce = lgj__xns
                data.append(ywc__cce)
        if tpm__qcgv and not ndpvz__fktfu and not is_join.literal_value:
            hypg__tsyss = left_on[0]
            if hypg__tsyss in right_df.columns:
                columns.append(hypg__tsyss)
                if (amz__xokjd == bodo.dict_str_arr_type and lgj__xns ==
                    bodo.string_array_type):
                    ywc__cce = bodo.string_array_type
                else:
                    ywc__cce = amz__xokjd
                data.append(ywc__cce)
        for xmr__cons, imzx__oqwla in zip(left_df.data, left_df.columns):
            columns.append(str(imzx__oqwla) + suffix_x.literal_value if 
                imzx__oqwla in wzbwf__zpl else imzx__oqwla)
            if imzx__oqwla in mmr__ztljh:
                if xmr__cons == bodo.dict_str_arr_type:
                    xmr__cons = right_df.data[right_df.columns.index(
                        imzx__oqwla)]
                data.append(xmr__cons)
            else:
                if (xmr__cons == bodo.dict_str_arr_type and imzx__oqwla in
                    left_on):
                    if tpm__qcgv:
                        xmr__cons = lgj__xns
                    else:
                        igqa__mlm = left_on.index(imzx__oqwla)
                        vhq__wjz = right_on[igqa__mlm]
                        xmr__cons = right_df.data[right_df.columns.index(
                            vhq__wjz)]
                if tyt__vftsi:
                    xmr__cons = to_nullable_type(xmr__cons)
                data.append(xmr__cons)
        for xmr__cons, imzx__oqwla in zip(right_df.data, right_df.columns):
            if imzx__oqwla not in mmr__ztljh:
                columns.append(str(imzx__oqwla) + suffix_y.literal_value if
                    imzx__oqwla in wzbwf__zpl else imzx__oqwla)
                if (xmr__cons == bodo.dict_str_arr_type and imzx__oqwla in
                    right_on):
                    if ndpvz__fktfu:
                        xmr__cons = amz__xokjd
                    else:
                        igqa__mlm = right_on.index(imzx__oqwla)
                        hyqr__hvg = left_on[igqa__mlm]
                        xmr__cons = left_df.data[left_df.columns.index(
                            hyqr__hvg)]
                if usxzy__mipbs:
                    xmr__cons = to_nullable_type(xmr__cons)
                data.append(xmr__cons)
        xqrra__nkfcg = get_overload_const_bool(indicator)
        if xqrra__nkfcg:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        if ndpvz__fktfu and tpm__qcgv and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif ndpvz__fktfu and not tpm__qcgv:
            index_typ = right_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif tpm__qcgv and not ndpvz__fktfu:
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        mcg__hhf = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(mcg__hhf, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    avxkt__kbi = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return avxkt__kbi._getvalue()


@overload(pd.concat, inline='always', no_unliteral=True)
def concat_overload(objs, axis=0, join='outer', join_axes=None,
    ignore_index=False, keys=None, levels=None, names=None,
    verify_integrity=False, sort=None, copy=True):
    if not is_overload_constant_int(axis):
        raise BodoError("pd.concat(): 'axis' should be a constant integer")
    if not is_overload_constant_bool(ignore_index):
        raise BodoError(
            "pd.concat(): 'ignore_index' should be a constant boolean")
    axis = get_overload_const_int(axis)
    ignore_index = is_overload_true(ignore_index)
    hjf__lro = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    cpbkf__itu = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', hjf__lro, cpbkf__itu,
        package_name='pandas', module_name='General')
    azjs__tmyln = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        vfkk__kpata = 0
        ubpxx__vnjp = []
        names = []
        for i, aplp__qijwz in enumerate(objs.types):
            assert isinstance(aplp__qijwz, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(aplp__qijwz, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                aplp__qijwz, 'pandas.concat()')
            if isinstance(aplp__qijwz, SeriesType):
                names.append(str(vfkk__kpata))
                vfkk__kpata += 1
                ubpxx__vnjp.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(aplp__qijwz.columns)
                for iufes__rboui in range(len(aplp__qijwz.data)):
                    ubpxx__vnjp.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, iufes__rboui))
        return bodo.hiframes.dataframe_impl._gen_init_df(azjs__tmyln, names,
            ', '.join(ubpxx__vnjp), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(rfp__nccjk, DataFrameType) for rfp__nccjk in
            objs.types)
        ajed__szk = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            ajed__szk.extend(df.columns)
        ajed__szk = list(dict.fromkeys(ajed__szk).keys())
        addie__pjw = {}
        for vfkk__kpata, urtbw__als in enumerate(ajed__szk):
            for df in objs.types:
                if urtbw__als in df.columns:
                    addie__pjw['arr_typ{}'.format(vfkk__kpata)] = df.data[df
                        .columns.index(urtbw__als)]
                    break
        assert len(addie__pjw) == len(ajed__szk)
        bmt__lywe = []
        for vfkk__kpata, urtbw__als in enumerate(ajed__szk):
            args = []
            for i, df in enumerate(objs.types):
                if urtbw__als in df.columns:
                    dvv__tkxsm = df.columns.index(urtbw__als)
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, dvv__tkxsm))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, vfkk__kpata))
            azjs__tmyln += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(vfkk__kpata, ', '.join(args)))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(A0), 1, None)'
                )
        else:
            index = (
                """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)) if len(objs[i].
                columns) > 0)))
        return bodo.hiframes.dataframe_impl._gen_init_df(azjs__tmyln,
            ajed__szk, ', '.join('A{}'.format(i) for i in range(len(
            ajed__szk))), index, addie__pjw)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(rfp__nccjk, SeriesType) for rfp__nccjk in
            objs.types)
        azjs__tmyln += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            azjs__tmyln += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            azjs__tmyln += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        azjs__tmyln += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        zxosd__hxatb = {}
        exec(azjs__tmyln, {'bodo': bodo, 'np': np, 'numba': numba},
            zxosd__hxatb)
        return zxosd__hxatb['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for vfkk__kpata, urtbw__als in enumerate(df_type.columns):
            azjs__tmyln += '  arrs{} = []\n'.format(vfkk__kpata)
            azjs__tmyln += '  for i in range(len(objs)):\n'
            azjs__tmyln += '    df = objs[i]\n'
            azjs__tmyln += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(vfkk__kpata))
            azjs__tmyln += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(vfkk__kpata))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            azjs__tmyln += '  arrs_index = []\n'
            azjs__tmyln += '  for i in range(len(objs)):\n'
            azjs__tmyln += '    df = objs[i]\n'
            azjs__tmyln += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(azjs__tmyln,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        azjs__tmyln += '  arrs = []\n'
        azjs__tmyln += '  for i in range(len(objs)):\n'
        azjs__tmyln += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        azjs__tmyln += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            azjs__tmyln += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            azjs__tmyln += '  arrs_index = []\n'
            azjs__tmyln += '  for i in range(len(objs)):\n'
            azjs__tmyln += '    S = objs[i]\n'
            azjs__tmyln += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            azjs__tmyln += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        azjs__tmyln += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        zxosd__hxatb = {}
        exec(azjs__tmyln, {'bodo': bodo, 'np': np, 'numba': numba},
            zxosd__hxatb)
        return zxosd__hxatb['impl']
    raise BodoError('pd.concat(): input type {} not supported yet'.format(objs)
        )


def sort_values_dummy(df, by, ascending, inplace, na_position):
    return df.sort_values(by, ascending=ascending, inplace=inplace,
        na_position=na_position)


@infer_global(sort_values_dummy)
class SortDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, by, ascending, inplace, na_position = args
        index = df.index
        if isinstance(index, bodo.hiframes.pd_index_ext.RangeIndexType):
            index = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64)
        igc__uxyv = df.copy(index=index, is_table_format=False)
        return signature(igc__uxyv, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    pecx__eyct = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return pecx__eyct._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    hjf__lro = dict(index=index, name=name)
    cpbkf__itu = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', hjf__lro, cpbkf__itu,
        package_name='pandas', module_name='DataFrame')

    def _impl(df, index=True, name='Pandas'):
        return bodo.hiframes.pd_dataframe_ext.itertuples_dummy(df)
    return _impl


def itertuples_dummy(df):
    return df


@infer_global(itertuples_dummy)
class ItertuplesDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        assert 'Index' not in df.columns
        columns = ('Index',) + df.columns
        addie__pjw = (types.Array(types.int64, 1, 'C'),) + df.data
        uhob__rhwpa = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, addie__pjw)
        return signature(uhob__rhwpa, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    pecx__eyct = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return pecx__eyct._getvalue()


def query_dummy(df, expr):
    return df.eval(expr)


@infer_global(query_dummy)
class QueryDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=RangeIndexType(types
            .none)), *args)


@lower_builtin(query_dummy, types.VarArg(types.Any))
def lower_query_dummy(context, builder, sig, args):
    pecx__eyct = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return pecx__eyct._getvalue()


def val_isin_dummy(S, vals):
    return S in vals


def val_notin_dummy(S, vals):
    return S not in vals


@infer_global(val_isin_dummy)
@infer_global(val_notin_dummy)
class ValIsinTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=args[0].index), *args)


@lower_builtin(val_isin_dummy, types.VarArg(types.Any))
@lower_builtin(val_notin_dummy, types.VarArg(types.Any))
def lower_val_isin_dummy(context, builder, sig, args):
    pecx__eyct = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return pecx__eyct._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    cpacr__yos = get_overload_const_bool(check_duplicates)
    jko__vnj = not is_overload_none(value_names)
    zup__zwlf = isinstance(values_tup, types.UniTuple)
    if zup__zwlf:
        yykd__drf = [to_nullable_type(values_tup.dtype)]
    else:
        yykd__drf = [to_nullable_type(bds__izivj) for bds__izivj in values_tup]
    azjs__tmyln = 'def impl(\n'
    azjs__tmyln += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    azjs__tmyln += '):\n'
    azjs__tmyln += '    if parallel:\n'
    xvh__jsne = ', '.join([f'array_to_info(index_tup[{i}])' for i in range(
        len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    azjs__tmyln += f'        info_list = [{xvh__jsne}]\n'
    azjs__tmyln += '        cpp_table = arr_info_list_to_table(info_list)\n'
    azjs__tmyln += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
    fln__dcktf = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    cvy__mrsc = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    zexx__fhg = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    azjs__tmyln += f'        index_tup = ({fln__dcktf},)\n'
    azjs__tmyln += f'        columns_tup = ({cvy__mrsc},)\n'
    azjs__tmyln += f'        values_tup = ({zexx__fhg},)\n'
    azjs__tmyln += '        delete_table(cpp_table)\n'
    azjs__tmyln += '        delete_table(out_cpp_table)\n'
    azjs__tmyln += '    columns_arr = columns_tup[0]\n'
    if zup__zwlf:
        azjs__tmyln += '    values_arrs = [arr for arr in values_tup]\n'
    azjs__tmyln += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    azjs__tmyln += '        index_tup\n'
    azjs__tmyln += '    )\n'
    azjs__tmyln += '    n_rows = len(unique_index_arr_tup[0])\n'
    azjs__tmyln += '    num_values_arrays = len(values_tup)\n'
    azjs__tmyln += '    n_unique_pivots = len(pivot_values)\n'
    if zup__zwlf:
        azjs__tmyln += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        azjs__tmyln += '    n_cols = n_unique_pivots\n'
    azjs__tmyln += '    col_map = {}\n'
    azjs__tmyln += '    for i in range(n_unique_pivots):\n'
    azjs__tmyln += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    azjs__tmyln += '            raise ValueError(\n'
    azjs__tmyln += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    azjs__tmyln += '            )\n'
    azjs__tmyln += '        col_map[pivot_values[i]] = i\n'
    mgwf__vqqpw = False
    for i, rbecn__fba in enumerate(yykd__drf):
        if is_str_arr_type(rbecn__fba):
            mgwf__vqqpw = True
            azjs__tmyln += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            azjs__tmyln += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if mgwf__vqqpw:
        if cpacr__yos:
            azjs__tmyln += '    nbytes = (n_rows + 7) >> 3\n'
            azjs__tmyln += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        azjs__tmyln += '    for i in range(len(columns_arr)):\n'
        azjs__tmyln += '        col_name = columns_arr[i]\n'
        azjs__tmyln += '        pivot_idx = col_map[col_name]\n'
        azjs__tmyln += '        row_idx = row_vector[i]\n'
        if cpacr__yos:
            azjs__tmyln += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            azjs__tmyln += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            azjs__tmyln += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            azjs__tmyln += '        else:\n'
            azjs__tmyln += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if zup__zwlf:
            azjs__tmyln += '        for j in range(num_values_arrays):\n'
            azjs__tmyln += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            azjs__tmyln += '            len_arr = len_arrs_0[col_idx]\n'
            azjs__tmyln += '            values_arr = values_arrs[j]\n'
            azjs__tmyln += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            azjs__tmyln += (
                '                len_arr[row_idx] = len(values_arr[i])\n')
            azjs__tmyln += (
                '                total_lens_0[col_idx] += len(values_arr[i])\n'
                )
        else:
            for i, rbecn__fba in enumerate(yykd__drf):
                if is_str_arr_type(rbecn__fba):
                    azjs__tmyln += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    azjs__tmyln += f"""            len_arrs_{i}[pivot_idx][row_idx] = len(values_tup[{i}][i])
"""
                    azjs__tmyln += f"""            total_lens_{i}[pivot_idx] += len(values_tup[{i}][i])
"""
    for i, rbecn__fba in enumerate(yykd__drf):
        if is_str_arr_type(rbecn__fba):
            azjs__tmyln += f'    data_arrs_{i} = [\n'
            azjs__tmyln += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            azjs__tmyln += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            azjs__tmyln += '        )\n'
            azjs__tmyln += '        for i in range(n_cols)\n'
            azjs__tmyln += '    ]\n'
        else:
            azjs__tmyln += f'    data_arrs_{i} = [\n'
            azjs__tmyln += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            azjs__tmyln += '        for _ in range(n_cols)\n'
            azjs__tmyln += '    ]\n'
    if not mgwf__vqqpw and cpacr__yos:
        azjs__tmyln += '    nbytes = (n_rows + 7) >> 3\n'
        azjs__tmyln += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    azjs__tmyln += '    for i in range(len(columns_arr)):\n'
    azjs__tmyln += '        col_name = columns_arr[i]\n'
    azjs__tmyln += '        pivot_idx = col_map[col_name]\n'
    azjs__tmyln += '        row_idx = row_vector[i]\n'
    if not mgwf__vqqpw and cpacr__yos:
        azjs__tmyln += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        azjs__tmyln += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        azjs__tmyln += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        azjs__tmyln += '        else:\n'
        azjs__tmyln += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if zup__zwlf:
        azjs__tmyln += '        for j in range(num_values_arrays):\n'
        azjs__tmyln += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        azjs__tmyln += '            col_arr = data_arrs_0[col_idx]\n'
        azjs__tmyln += '            values_arr = values_arrs[j]\n'
        azjs__tmyln += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        azjs__tmyln += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        azjs__tmyln += '            else:\n'
        azjs__tmyln += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, rbecn__fba in enumerate(yykd__drf):
            azjs__tmyln += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            azjs__tmyln += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            azjs__tmyln += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            azjs__tmyln += f'        else:\n'
            azjs__tmyln += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        azjs__tmyln += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        azjs__tmyln += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if jko__vnj:
        azjs__tmyln += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            azjs__tmyln += '    total_chars = 0\n'
            azjs__tmyln += '    for i in range(len(value_names)):\n'
            azjs__tmyln += '        total_chars += len(value_names[i])\n'
            azjs__tmyln += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            azjs__tmyln += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            azjs__tmyln += '    total_chars = 0\n'
            azjs__tmyln += '    for i in range(len(pivot_values)):\n'
            azjs__tmyln += '        total_chars += len(pivot_values[i])\n'
            azjs__tmyln += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            azjs__tmyln += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        azjs__tmyln += '    for i in range(len(value_names)):\n'
        azjs__tmyln += '        for j in range(len(pivot_values)):\n'
        azjs__tmyln += """            new_value_names[(i * len(pivot_values)) + j] = value_names[i]
"""
        azjs__tmyln += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        azjs__tmyln += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        azjs__tmyln += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    bog__tnjx = ', '.join(f'data_arrs_{i}' for i in range(len(yykd__drf)))
    azjs__tmyln += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({bog__tnjx},), n_rows)
"""
    azjs__tmyln += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    azjs__tmyln += '        (table,), index, column_index\n'
    azjs__tmyln += '    )\n'
    zxosd__hxatb = {}
    iop__lpsea = {f'data_arr_typ_{i}': rbecn__fba for i, rbecn__fba in
        enumerate(yykd__drf)}
    fwej__hdvu = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **iop__lpsea}
    exec(azjs__tmyln, fwej__hdvu, zxosd__hxatb)
    impl = zxosd__hxatb['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    frysu__xgeu = {}
    frysu__xgeu['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, wasp__xxoit in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        vfqwj__kaphs = None
        if isinstance(wasp__xxoit, bodo.DatetimeArrayType):
            raf__fhxoq = 'datetimetz'
            usphi__yklol = 'datetime64[ns]'
            if isinstance(wasp__xxoit.tz, int):
                zzi__gyrgv = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(wasp__xxoit.tz))
            else:
                zzi__gyrgv = pd.DatetimeTZDtype(tz=wasp__xxoit.tz).tz
            vfqwj__kaphs = {'timezone': pa.lib.tzinfo_to_string(zzi__gyrgv)}
        elif isinstance(wasp__xxoit, types.Array
            ) or wasp__xxoit == boolean_array:
            raf__fhxoq = usphi__yklol = wasp__xxoit.dtype.name
            if usphi__yklol.startswith('datetime'):
                raf__fhxoq = 'datetime'
        elif is_str_arr_type(wasp__xxoit):
            raf__fhxoq = 'unicode'
            usphi__yklol = 'object'
        elif wasp__xxoit == binary_array_type:
            raf__fhxoq = 'bytes'
            usphi__yklol = 'object'
        elif isinstance(wasp__xxoit, DecimalArrayType):
            raf__fhxoq = usphi__yklol = 'object'
        elif isinstance(wasp__xxoit, IntegerArrayType):
            bbq__ceya = wasp__xxoit.dtype.name
            if bbq__ceya.startswith('int'):
                raf__fhxoq = 'Int' + bbq__ceya[3:]
            elif bbq__ceya.startswith('uint'):
                raf__fhxoq = 'UInt' + bbq__ceya[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, wasp__xxoit))
            usphi__yklol = wasp__xxoit.dtype.name
        elif wasp__xxoit == datetime_date_array_type:
            raf__fhxoq = 'datetime'
            usphi__yklol = 'object'
        elif isinstance(wasp__xxoit, (StructArrayType, ArrayItemArrayType)):
            raf__fhxoq = 'object'
            usphi__yklol = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, wasp__xxoit))
        bcrt__nfe = {'name': col_name, 'field_name': col_name,
            'pandas_type': raf__fhxoq, 'numpy_type': usphi__yklol,
            'metadata': vfqwj__kaphs}
        frysu__xgeu['columns'].append(bcrt__nfe)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            izp__ajt = '__index_level_0__'
            pqv__ojal = None
        else:
            izp__ajt = '%s'
            pqv__ojal = '%s'
        frysu__xgeu['index_columns'] = [izp__ajt]
        frysu__xgeu['columns'].append({'name': pqv__ojal, 'field_name':
            izp__ajt, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        frysu__xgeu['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        frysu__xgeu['index_columns'] = []
    frysu__xgeu['pandas_version'] = pd.__version__
    return frysu__xgeu


@overload_method(DataFrameType, 'to_parquet', no_unliteral=True)
def to_parquet_overload(df, path, engine='auto', compression='snappy',
    index=None, partition_cols=None, storage_options=None, row_group_size=-
    1, _is_parallel=False):
    check_unsupported_args('DataFrame.to_parquet', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if df.has_runtime_cols and not is_overload_none(partition_cols):
        raise BodoError(
            f"DataFrame.to_parquet(): Providing 'partition_cols' on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information."
            )
    if not is_overload_none(engine) and get_overload_const_str(engine) not in (
        'auto', 'pyarrow'):
        raise BodoError('DataFrame.to_parquet(): only pyarrow engine supported'
            )
    if not is_overload_none(compression) and get_overload_const_str(compression
        ) not in {'snappy', 'gzip', 'brotli'}:
        raise BodoError('to_parquet(): Unsupported compression: ' + str(
            get_overload_const_str(compression)))
    if not is_overload_none(partition_cols):
        partition_cols = get_overload_const_list(partition_cols)
        afjl__yrfhs = []
        for dxyj__taw in partition_cols:
            try:
                idx = df.columns.index(dxyj__taw)
            except ValueError as oxto__vdj:
                raise BodoError(
                    f'Partition column {dxyj__taw} is not in dataframe')
            afjl__yrfhs.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    jitl__kgg = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType)
    nbmmt__qvtcn = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not jitl__kgg)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not jitl__kgg or is_overload_true
        (_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and jitl__kgg and not is_overload_true(_is_parallel)
    if df.has_runtime_cols:
        if isinstance(df.runtime_colname_typ, MultiIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): Not supported with MultiIndex runtime column names. Please return the DataFrame to regular Python to update typing information.'
                )
        if not isinstance(df.runtime_colname_typ, bodo.hiframes.
            pd_index_ext.StringIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): parquet must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
        pahb__skn = df.runtime_data_types
        thbd__omcd = len(pahb__skn)
        vfqwj__kaphs = gen_pandas_parquet_metadata([''] * thbd__omcd,
            pahb__skn, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        tuvm__tefip = vfqwj__kaphs['columns'][:thbd__omcd]
        vfqwj__kaphs['columns'] = vfqwj__kaphs['columns'][thbd__omcd:]
        tuvm__tefip = [json.dumps(wysph__esh).replace('""', '{0}') for
            wysph__esh in tuvm__tefip]
        hiyoh__kvmrj = json.dumps(vfqwj__kaphs)
        trjvh__fwu = '"columns": ['
        nvyrl__pll = hiyoh__kvmrj.find(trjvh__fwu)
        if nvyrl__pll == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        itpl__ccvc = nvyrl__pll + len(trjvh__fwu)
        ptj__hre = hiyoh__kvmrj[:itpl__ccvc]
        hiyoh__kvmrj = hiyoh__kvmrj[itpl__ccvc:]
        rubb__uxfwc = len(vfqwj__kaphs['columns'])
    else:
        hiyoh__kvmrj = json.dumps(gen_pandas_parquet_metadata(df.columns,
            df.data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and jitl__kgg:
        hiyoh__kvmrj = hiyoh__kvmrj.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            hiyoh__kvmrj = hiyoh__kvmrj.replace('"%s"', '%s')
    if not df.is_table_format:
        ubpxx__vnjp = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    azjs__tmyln = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        azjs__tmyln += '    py_table = get_dataframe_table(df)\n'
        azjs__tmyln += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        azjs__tmyln += '    info_list = [{}]\n'.format(ubpxx__vnjp)
        azjs__tmyln += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        azjs__tmyln += '    columns_index = get_dataframe_column_names(df)\n'
        azjs__tmyln += '    names_arr = index_to_array(columns_index)\n'
        azjs__tmyln += '    col_names = array_to_info(names_arr)\n'
    else:
        azjs__tmyln += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and nbmmt__qvtcn:
        azjs__tmyln += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        ywf__hiq = True
    else:
        azjs__tmyln += '    index_col = array_to_info(np.empty(0))\n'
        ywf__hiq = False
    if df.has_runtime_cols:
        azjs__tmyln += '    columns_lst = []\n'
        azjs__tmyln += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            azjs__tmyln += f'    for _ in range(len(py_table.block_{i})):\n'
            azjs__tmyln += f"""        columns_lst.append({tuvm__tefip[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            azjs__tmyln += '        num_cols += 1\n'
        if rubb__uxfwc:
            azjs__tmyln += "    columns_lst.append('')\n"
        azjs__tmyln += '    columns_str = ", ".join(columns_lst)\n'
        azjs__tmyln += ('    metadata = """' + ptj__hre +
            '""" + columns_str + """' + hiyoh__kvmrj + '"""\n')
    else:
        azjs__tmyln += '    metadata = """' + hiyoh__kvmrj + '"""\n'
    azjs__tmyln += '    if compression is None:\n'
    azjs__tmyln += "        compression = 'none'\n"
    azjs__tmyln += '    if df.index.name is not None:\n'
    azjs__tmyln += '        name_ptr = df.index.name\n'
    azjs__tmyln += '    else:\n'
    azjs__tmyln += "        name_ptr = 'null'\n"
    azjs__tmyln += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    wngc__kyr = None
    if partition_cols:
        wngc__kyr = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        dhmfj__xauj = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in afjl__yrfhs)
        if dhmfj__xauj:
            azjs__tmyln += '    cat_info_list = [{}]\n'.format(dhmfj__xauj)
            azjs__tmyln += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            azjs__tmyln += '    cat_table = table\n'
        azjs__tmyln += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        azjs__tmyln += (
            f'    part_cols_idxs = np.array({afjl__yrfhs}, dtype=np.int32)\n')
        azjs__tmyln += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        azjs__tmyln += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        azjs__tmyln += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        azjs__tmyln += (
            '                            unicode_to_utf8(compression),\n')
        azjs__tmyln += '                            _is_parallel,\n'
        azjs__tmyln += (
            '                            unicode_to_utf8(bucket_region),\n')
        azjs__tmyln += '                            row_group_size)\n'
        azjs__tmyln += '    delete_table_decref_arrays(table)\n'
        azjs__tmyln += '    delete_info_decref_array(index_col)\n'
        azjs__tmyln += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        azjs__tmyln += '    delete_info_decref_array(col_names)\n'
        if dhmfj__xauj:
            azjs__tmyln += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        azjs__tmyln += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        azjs__tmyln += (
            '                            table, col_names, index_col,\n')
        azjs__tmyln += '                            ' + str(ywf__hiq) + ',\n'
        azjs__tmyln += (
            '                            unicode_to_utf8(metadata),\n')
        azjs__tmyln += (
            '                            unicode_to_utf8(compression),\n')
        azjs__tmyln += (
            '                            _is_parallel, 1, df.index.start,\n')
        azjs__tmyln += (
            '                            df.index.stop, df.index.step,\n')
        azjs__tmyln += (
            '                            unicode_to_utf8(name_ptr),\n')
        azjs__tmyln += (
            '                            unicode_to_utf8(bucket_region),\n')
        azjs__tmyln += '                            row_group_size)\n'
        azjs__tmyln += '    delete_table_decref_arrays(table)\n'
        azjs__tmyln += '    delete_info_decref_array(index_col)\n'
        azjs__tmyln += '    delete_info_decref_array(col_names)\n'
    else:
        azjs__tmyln += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        azjs__tmyln += (
            '                            table, col_names, index_col,\n')
        azjs__tmyln += '                            ' + str(ywf__hiq) + ',\n'
        azjs__tmyln += (
            '                            unicode_to_utf8(metadata),\n')
        azjs__tmyln += (
            '                            unicode_to_utf8(compression),\n')
        azjs__tmyln += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        azjs__tmyln += (
            '                            unicode_to_utf8(name_ptr),\n')
        azjs__tmyln += (
            '                            unicode_to_utf8(bucket_region),\n')
        azjs__tmyln += '                            row_group_size)\n'
        azjs__tmyln += '    delete_table_decref_arrays(table)\n'
        azjs__tmyln += '    delete_info_decref_array(index_col)\n'
        azjs__tmyln += '    delete_info_decref_array(col_names)\n'
    zxosd__hxatb = {}
    if df.has_runtime_cols:
        oya__ude = None
    else:
        for imzx__oqwla in df.columns:
            if not isinstance(imzx__oqwla, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        oya__ude = pd.array(df.columns)
    exec(azjs__tmyln, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': oya__ude,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': wngc__kyr, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, zxosd__hxatb)
    xfk__gobed = zxosd__hxatb['df_to_parquet']
    return xfk__gobed


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    bto__xah = 'all_ok'
    uzycq__tqjnr = urlparse(con)
    ocek__nzj = uzycq__tqjnr.scheme
    if _is_parallel and bodo.get_rank() == 0:
        skp__fcnns = 100
        if chunksize is None:
            mfw__ohns = skp__fcnns
        else:
            mfw__ohns = min(chunksize, skp__fcnns)
        if _is_table_create:
            df = df.iloc[:mfw__ohns, :]
        else:
            df = df.iloc[mfw__ohns:, :]
            if len(df) == 0:
                return bto__xah
    raia__ytiv = df.columns
    try:
        if ocek__nzj == 'snowflake':
            rpfu__wxgvd = uzycq__tqjnr.password
            if rpfu__wxgvd and con.count(rpfu__wxgvd) == 1:
                con = con.replace(rpfu__wxgvd, quote(rpfu__wxgvd))
            try:
                from snowflake.connector.pandas_tools import pd_writer
                from bodo import snowflake_sqlalchemy_compat
                if method is not None and _is_table_create and bodo.get_rank(
                    ) == 0:
                    import warnings
                    from bodo.utils.typing import BodoWarning
                    warnings.warn(BodoWarning(
                        'DataFrame.to_sql(): method argument is not supported with Snowflake. Bodo always uses snowflake.connector.pandas_tools.pd_writer to write data.'
                        ))
                method = pd_writer
                df.columns = [(urtbw__als.upper() if urtbw__als.islower() else
                    urtbw__als) for urtbw__als in df.columns]
            except ImportError as oxto__vdj:
                bto__xah = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return bto__xah
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as dsrz__aamzs:
            bto__xah = dsrz__aamzs.args[0]
        return bto__xah
    finally:
        df.columns = raia__ytiv


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    with numba.objmode(out='unicode_type'):
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
    return out


@overload_method(DataFrameType, 'to_sql')
def to_sql_overload(df, name, con, schema=None, if_exists='fail', index=
    True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_parallel=False):
    check_runtime_cols_unsupported(df, 'DataFrame.to_sql()')
    if is_overload_none(schema):
        if bodo.get_rank() == 0:
            import warnings
            warnings.warn(BodoWarning(
                f'DataFrame.to_sql(): schema argument is recommended to avoid permission issues when writing the table.'
                ))
    if not (is_overload_none(chunksize) or isinstance(chunksize, types.Integer)
        ):
        raise BodoError(
            "DataFrame.to_sql(): 'chunksize' argument must be an integer if provided."
            )

    def _impl(df, name, con, schema=None, if_exists='fail', index=True,
        index_label=None, chunksize=None, dtype=None, method=None,
        _is_parallel=False):
        qwly__ftz = bodo.libs.distributed_api.get_rank()
        bto__xah = 'unset'
        if qwly__ftz != 0:
            bto__xah = bcast_scalar(bto__xah)
        elif qwly__ftz == 0:
            bto__xah = to_sql_exception_guard_encaps(df, name, con, schema,
                if_exists, index, index_label, chunksize, dtype, method, 
                True, _is_parallel)
            bto__xah = bcast_scalar(bto__xah)
        if_exists = 'append'
        if _is_parallel and bto__xah == 'all_ok':
            bto__xah = to_sql_exception_guard_encaps(df, name, con, schema,
                if_exists, index, index_label, chunksize, dtype, method, 
                False, _is_parallel)
        if bto__xah != 'all_ok':
            print('err_msg=', bto__xah)
            raise ValueError('error in to_sql() operation')
    return _impl


@overload_method(DataFrameType, 'to_csv', no_unliteral=True)
def to_csv_overload(df, path_or_buf=None, sep=',', na_rep='', float_format=
    None, columns=None, header=True, index=True, index_label=None, mode='w',
    encoding=None, compression=None, quoting=None, quotechar='"',
    line_terminator=None, chunksize=None, date_format=None, doublequote=
    True, escapechar=None, decimal='.', errors='strict', storage_options=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_csv()')
    check_unsupported_args('DataFrame.to_csv', {'encoding': encoding,
        'mode': mode, 'errors': errors, 'storage_options': storage_options},
        {'encoding': None, 'mode': 'w', 'errors': 'strict',
        'storage_options': None}, package_name='pandas', module_name='IO')
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "DataFrame.to_csv(): 'path_or_buf' argument should be None or string"
            )
    if not is_overload_none(compression):
        raise BodoError(
            "DataFrame.to_csv(): 'compression' argument supports only None, which is the default in JIT code."
            )
    if is_overload_constant_str(path_or_buf):
        scxgo__vnh = get_overload_const_str(path_or_buf)
        if scxgo__vnh.endswith(('.gz', '.bz2', '.zip', '.xz')):
            import warnings
            from bodo.utils.typing import BodoWarning
            warnings.warn(BodoWarning(
                "DataFrame.to_csv(): 'compression' argument defaults to None in JIT code, which is the only supported value."
                ))
    if not (is_overload_none(columns) or isinstance(columns, (types.List,
        types.Tuple))):
        raise BodoError(
            "DataFrame.to_csv(): 'columns' argument must be list a or tuple type."
            )
    if is_overload_none(path_or_buf):

        def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=
            None, columns=None, header=True, index=True, index_label=None,
            mode='w', encoding=None, compression=None, quoting=None,
            quotechar='"', line_terminator=None, chunksize=None,
            date_format=None, doublequote=True, escapechar=None, decimal=
            '.', errors='strict', storage_options=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_csv(path_or_buf, sep, na_rep, float_format,
                    columns, header, index, index_label, mode, encoding,
                    compression, quoting, quotechar, line_terminator,
                    chunksize, date_format, doublequote, escapechar,
                    decimal, errors, storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=None,
        columns=None, header=True, index=True, index_label=None, mode='w',
        encoding=None, compression=None, quoting=None, quotechar='"',
        line_terminator=None, chunksize=None, date_format=None, doublequote
        =True, escapechar=None, decimal='.', errors='strict',
        storage_options=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_csv(None, sep, na_rep, float_format, columns, header,
                index, index_label, mode, encoding, compression, quoting,
                quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors, storage_options)
        bodo.io.fs_io.csv_write(path_or_buf, D)
    return _impl


@overload_method(DataFrameType, 'to_json', no_unliteral=True)
def to_json_overload(df, path_or_buf=None, orient='records', date_format=
    None, double_precision=10, force_ascii=True, date_unit='ms',
    default_handler=None, lines=True, compression='infer', index=True,
    indent=None, storage_options=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_json()')
    check_unsupported_args('DataFrame.to_json', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if path_or_buf is None or path_or_buf == types.none:

        def _impl(df, path_or_buf=None, orient='records', date_format=None,
            double_precision=10, force_ascii=True, date_unit='ms',
            default_handler=None, lines=True, compression='infer', index=
            True, indent=None, storage_options=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_json(path_or_buf, orient, date_format,
                    double_precision, force_ascii, date_unit,
                    default_handler, lines, compression, index, indent,
                    storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, orient='records', date_format=None,
        double_precision=10, force_ascii=True, date_unit='ms',
        default_handler=None, lines=True, compression='infer', index=True,
        indent=None, storage_options=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_json(None, orient, date_format, double_precision,
                force_ascii, date_unit, default_handler, lines, compression,
                index, indent, storage_options)
        zydyf__cpjnw = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(zydyf__cpjnw))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(zydyf__cpjnw))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    hng__akurv = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    qdha__djwco = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', hng__akurv, qdha__djwco,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    azjs__tmyln = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        iud__srlq = data.data.dtype.categories
        azjs__tmyln += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        iud__srlq = data.dtype.categories
        azjs__tmyln += '  data_values = data\n'
    ykywm__nkef = len(iud__srlq)
    azjs__tmyln += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    azjs__tmyln += '  numba.parfors.parfor.init_prange()\n'
    azjs__tmyln += '  n = len(data_values)\n'
    for i in range(ykywm__nkef):
        azjs__tmyln += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    azjs__tmyln += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    azjs__tmyln += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for iufes__rboui in range(ykywm__nkef):
        azjs__tmyln += '          data_arr_{}[i] = 0\n'.format(iufes__rboui)
    azjs__tmyln += '      else:\n'
    for leh__rdzum in range(ykywm__nkef):
        azjs__tmyln += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            leh__rdzum)
    ubpxx__vnjp = ', '.join(f'data_arr_{i}' for i in range(ykywm__nkef))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(iud__srlq[0], np.datetime64):
        iud__srlq = tuple(pd.Timestamp(urtbw__als) for urtbw__als in iud__srlq)
    elif isinstance(iud__srlq[0], np.timedelta64):
        iud__srlq = tuple(pd.Timedelta(urtbw__als) for urtbw__als in iud__srlq)
    return bodo.hiframes.dataframe_impl._gen_init_df(azjs__tmyln, iud__srlq,
        ubpxx__vnjp, index)


def categorical_can_construct_dataframe(val):
    if isinstance(val, CategoricalArrayType):
        return val.dtype.categories is not None
    elif isinstance(val, SeriesType) and isinstance(val.data,
        CategoricalArrayType):
        return val.data.dtype.categories is not None
    return False


def handle_inplace_df_type_change(inplace, _bodo_transformed, func_name):
    if is_overload_false(_bodo_transformed
        ) and bodo.transforms.typing_pass.in_partial_typing and (
        is_overload_true(inplace) or not is_overload_constant_bool(inplace)):
        bodo.transforms.typing_pass.typing_transform_required = True
        raise Exception('DataFrame.{}(): transform necessary for inplace'.
            format(func_name))


pd_unsupported = (pd.read_pickle, pd.read_table, pd.read_fwf, pd.
    read_clipboard, pd.ExcelFile, pd.read_html, pd.read_xml, pd.read_hdf,
    pd.read_feather, pd.read_orc, pd.read_sas, pd.read_spss, pd.
    read_sql_table, pd.read_sql_query, pd.read_gbq, pd.read_stata, pd.
    ExcelWriter, pd.json_normalize, pd.merge_ordered, pd.factorize, pd.
    wide_to_long, pd.bdate_range, pd.period_range, pd.infer_freq, pd.
    interval_range, pd.eval, pd.test, pd.Grouper)
pd_util_unsupported = pd.util.hash_array, pd.util.hash_pandas_object
dataframe_unsupported = ['set_flags', 'convert_dtypes', 'bool', '__iter__',
    'items', 'iteritems', 'keys', 'iterrows', 'lookup', 'pop', 'xs', 'get',
    'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'pow', 'dot',
    'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rpow',
    'lt', 'gt', 'le', 'ge', 'ne', 'eq', 'combine', 'combine_first',
    'subtract', 'divide', 'multiply', 'applymap', 'agg', 'aggregate',
    'transform', 'expanding', 'ewm', 'all', 'any', 'clip', 'corrwith',
    'cummax', 'cummin', 'eval', 'kurt', 'kurtosis', 'mad', 'mode', 'rank',
    'round', 'sem', 'skew', 'value_counts', 'add_prefix', 'add_suffix',
    'align', 'at_time', 'between_time', 'equals', 'reindex', 'reindex_like',
    'rename_axis', 'set_axis', 'truncate', 'backfill', 'bfill', 'ffill',
    'interpolate', 'pad', 'droplevel', 'reorder_levels', 'nlargest',
    'nsmallest', 'swaplevel', 'stack', 'unstack', 'swapaxes', 'squeeze',
    'to_xarray', 'T', 'transpose', 'compare', 'update', 'asfreq', 'asof',
    'slice_shift', 'tshift', 'first_valid_index', 'last_valid_index',
    'resample', 'to_period', 'to_timestamp', 'tz_convert', 'tz_localize',
    'boxplot', 'hist', 'from_dict', 'from_records', 'to_pickle', 'to_hdf',
    'to_dict', 'to_excel', 'to_html', 'to_feather', 'to_latex', 'to_stata',
    'to_gbq', 'to_records', 'to_clipboard', 'to_markdown', 'to_xml']
dataframe_unsupported_attrs = ['at', 'attrs', 'axes', 'flags', 'style',
    'sparse']


def _install_pd_unsupported(mod_name, pd_unsupported):
    for btoc__bvng in pd_unsupported:
        xdq__ejmyj = mod_name + '.' + btoc__bvng.__name__
        overload(btoc__bvng, no_unliteral=True)(create_unsupported_overload
            (xdq__ejmyj))


def _install_dataframe_unsupported():
    for egk__smyf in dataframe_unsupported_attrs:
        zpu__zpg = 'DataFrame.' + egk__smyf
        overload_attribute(DataFrameType, egk__smyf)(
            create_unsupported_overload(zpu__zpg))
    for xdq__ejmyj in dataframe_unsupported:
        zpu__zpg = 'DataFrame.' + xdq__ejmyj + '()'
        overload_method(DataFrameType, xdq__ejmyj)(create_unsupported_overload
            (zpu__zpg))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
