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
            qmbs__wiax = f'{len(self.data)} columns of types {set(self.data)}'
            ahldp__cnomw = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({qmbs__wiax}, {self.index}, {ahldp__cnomw}, {self.dist}, {self.is_table_format})'
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
            qkei__jda = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(cihp__wcps.unify(typingctx, uvlft__dzhzt) if 
                cihp__wcps != uvlft__dzhzt else cihp__wcps for cihp__wcps,
                uvlft__dzhzt in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if qkei__jda is not None and None not in data:
                return DataFrameType(data, qkei__jda, self.columns, dist,
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
        return all(cihp__wcps.is_precise() for cihp__wcps in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        yomu__yiooi = self.columns.index(col_name)
        clh__tir = tuple(list(self.data[:yomu__yiooi]) + [new_type] + list(
            self.data[yomu__yiooi + 1:]))
        return DataFrameType(clh__tir, self.index, self.columns, self.dist,
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
        elzm__kgvm = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            elzm__kgvm.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, elzm__kgvm)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        elzm__kgvm = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, elzm__kgvm)


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
        gvi__bzjt = 'n',
        zagsu__aont = {'n': 5}
        cml__jmk, fvbh__azt = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, gvi__bzjt, zagsu__aont)
        mth__rvb = fvbh__azt[0]
        if not is_overload_int(mth__rvb):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        pwcsn__xpt = df.copy(is_table_format=False)
        return pwcsn__xpt(*fvbh__azt).replace(pysig=cml__jmk)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        hqsd__wzl = (df,) + args
        gvi__bzjt = 'df', 'method', 'min_periods'
        zagsu__aont = {'method': 'pearson', 'min_periods': 1}
        ema__cejji = 'method',
        cml__jmk, fvbh__azt = bodo.utils.typing.fold_typing_args(func_name,
            hqsd__wzl, kws, gvi__bzjt, zagsu__aont, ema__cejji)
        htsoo__vmvo = fvbh__azt[2]
        if not is_overload_int(htsoo__vmvo):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        nhqe__xmz = []
        edrlv__xbdzg = []
        for wbbk__qatve, tkkdh__szdep in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(tkkdh__szdep.dtype):
                nhqe__xmz.append(wbbk__qatve)
                edrlv__xbdzg.append(types.Array(types.float64, 1, 'A'))
        if len(nhqe__xmz) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        edrlv__xbdzg = tuple(edrlv__xbdzg)
        nhqe__xmz = tuple(nhqe__xmz)
        index_typ = bodo.utils.typing.type_col_to_index(nhqe__xmz)
        pwcsn__xpt = DataFrameType(edrlv__xbdzg, index_typ, nhqe__xmz)
        return pwcsn__xpt(*fvbh__azt).replace(pysig=cml__jmk)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        snp__wglnl = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        brfc__aco = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        rkumn__ddby = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        srpc__arhvi = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        sjfa__ewy = dict(raw=brfc__aco, result_type=rkumn__ddby)
        wezg__vflru = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', sjfa__ewy, wezg__vflru,
            package_name='pandas', module_name='DataFrame')
        iuy__neefn = True
        if types.unliteral(snp__wglnl) == types.unicode_type:
            if not is_overload_constant_str(snp__wglnl):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            iuy__neefn = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        umzwa__qswl = get_overload_const_int(axis)
        if iuy__neefn and umzwa__qswl != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif umzwa__qswl not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        wexv__zrnzj = []
        for arr_typ in df.data:
            rxxny__amf = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            xdul__moyq = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(rxxny__amf), types.int64), {}
                ).return_type
            wexv__zrnzj.append(xdul__moyq)
        gwt__lfgpl = types.none
        jhqn__kmc = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(wbbk__qatve) for wbbk__qatve in df.columns)), None)
        mhrj__ekjk = types.BaseTuple.from_types(wexv__zrnzj)
        csqa__pamnz = types.Tuple([types.bool_] * len(mhrj__ekjk))
        jvtxo__slxke = bodo.NullableTupleType(mhrj__ekjk, csqa__pamnz)
        htedc__wul = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if htedc__wul == types.NPDatetime('ns'):
            htedc__wul = bodo.pd_timestamp_type
        if htedc__wul == types.NPTimedelta('ns'):
            htedc__wul = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(mhrj__ekjk):
            cygu__pcta = HeterogeneousSeriesType(jvtxo__slxke, jhqn__kmc,
                htedc__wul)
        else:
            cygu__pcta = SeriesType(mhrj__ekjk.dtype, jvtxo__slxke,
                jhqn__kmc, htedc__wul)
        nhxm__wnpi = cygu__pcta,
        if srpc__arhvi is not None:
            nhxm__wnpi += tuple(srpc__arhvi.types)
        try:
            if not iuy__neefn:
                wykqn__sfb = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(snp__wglnl), self.context,
                    'DataFrame.apply', axis if umzwa__qswl == 1 else None)
            else:
                wykqn__sfb = get_const_func_output_type(snp__wglnl,
                    nhxm__wnpi, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as jqb__beam:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()', jqb__beam))
        if iuy__neefn:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(wykqn__sfb, (SeriesType, HeterogeneousSeriesType)
                ) and wykqn__sfb.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(wykqn__sfb, HeterogeneousSeriesType):
                bffpj__yntsk, atirg__hgyhc = wykqn__sfb.const_info
                if isinstance(wykqn__sfb.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    kit__tqx = wykqn__sfb.data.tuple_typ.types
                elif isinstance(wykqn__sfb.data, types.Tuple):
                    kit__tqx = wykqn__sfb.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                xej__asb = tuple(to_nullable_type(dtype_to_array_type(
                    yqs__nxaqn)) for yqs__nxaqn in kit__tqx)
                dyfz__qyoti = DataFrameType(xej__asb, df.index, atirg__hgyhc)
            elif isinstance(wykqn__sfb, SeriesType):
                aqr__xxeut, atirg__hgyhc = wykqn__sfb.const_info
                xej__asb = tuple(to_nullable_type(dtype_to_array_type(
                    wykqn__sfb.dtype)) for bffpj__yntsk in range(aqr__xxeut))
                dyfz__qyoti = DataFrameType(xej__asb, df.index, atirg__hgyhc)
            else:
                umpal__eivp = get_udf_out_arr_type(wykqn__sfb)
                dyfz__qyoti = SeriesType(umpal__eivp.dtype, umpal__eivp, df
                    .index, None)
        else:
            dyfz__qyoti = wykqn__sfb
        atuy__ftuam = ', '.join("{} = ''".format(cihp__wcps) for cihp__wcps in
            kws.keys())
        zplp__wiesi = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {atuy__ftuam}):
"""
        zplp__wiesi += '    pass\n'
        gom__ngvx = {}
        exec(zplp__wiesi, {}, gom__ngvx)
        ydpuk__auci = gom__ngvx['apply_stub']
        cml__jmk = numba.core.utils.pysignature(ydpuk__auci)
        dunjk__cvpu = (snp__wglnl, axis, brfc__aco, rkumn__ddby, srpc__arhvi
            ) + tuple(kws.values())
        return signature(dyfz__qyoti, *dunjk__cvpu).replace(pysig=cml__jmk)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        gvi__bzjt = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        zagsu__aont = {'x': None, 'y': None, 'kind': 'line', 'figsize':
            None, 'ax': None, 'subplots': False, 'sharex': None, 'sharey': 
            False, 'layout': None, 'use_index': True, 'title': None, 'grid':
            None, 'legend': True, 'style': None, 'logx': False, 'logy': 
            False, 'loglog': False, 'xticks': None, 'yticks': None, 'xlim':
            None, 'ylim': None, 'rot': None, 'fontsize': None, 'colormap':
            None, 'table': False, 'yerr': None, 'xerr': None, 'secondary_y':
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        ema__cejji = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        cml__jmk, fvbh__azt = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, gvi__bzjt, zagsu__aont, ema__cejji)
        gsun__gdt = fvbh__azt[2]
        if not is_overload_constant_str(gsun__gdt):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        etlpy__njogs = fvbh__azt[0]
        if not is_overload_none(etlpy__njogs) and not (is_overload_int(
            etlpy__njogs) or is_overload_constant_str(etlpy__njogs)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(etlpy__njogs):
            wyhf__grptv = get_overload_const_str(etlpy__njogs)
            if wyhf__grptv not in df.columns:
                raise BodoError(f'{func_name}: {wyhf__grptv} column not found.'
                    )
        elif is_overload_int(etlpy__njogs):
            jpiu__pwvgh = get_overload_const_int(etlpy__njogs)
            if jpiu__pwvgh > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {jpiu__pwvgh} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            etlpy__njogs = df.columns[etlpy__njogs]
        ulqy__pdpqn = fvbh__azt[1]
        if not is_overload_none(ulqy__pdpqn) and not (is_overload_int(
            ulqy__pdpqn) or is_overload_constant_str(ulqy__pdpqn)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(ulqy__pdpqn):
            uxhow__wiifg = get_overload_const_str(ulqy__pdpqn)
            if uxhow__wiifg not in df.columns:
                raise BodoError(
                    f'{func_name}: {uxhow__wiifg} column not found.')
        elif is_overload_int(ulqy__pdpqn):
            mvrg__ppuem = get_overload_const_int(ulqy__pdpqn)
            if mvrg__ppuem > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {mvrg__ppuem} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            ulqy__pdpqn = df.columns[ulqy__pdpqn]
        zpe__zmhx = fvbh__azt[3]
        if not is_overload_none(zpe__zmhx) and not is_tuple_like_type(zpe__zmhx
            ):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        ahin__slsaj = fvbh__azt[10]
        if not is_overload_none(ahin__slsaj) and not is_overload_constant_str(
            ahin__slsaj):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        rahrj__hahb = fvbh__azt[12]
        if not is_overload_bool(rahrj__hahb):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        ywn__skj = fvbh__azt[17]
        if not is_overload_none(ywn__skj) and not is_tuple_like_type(ywn__skj):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        tue__jgzhq = fvbh__azt[18]
        if not is_overload_none(tue__jgzhq) and not is_tuple_like_type(
            tue__jgzhq):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        fwgpi__hvi = fvbh__azt[22]
        if not is_overload_none(fwgpi__hvi) and not is_overload_int(fwgpi__hvi
            ):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        oike__mfem = fvbh__azt[29]
        if not is_overload_none(oike__mfem) and not is_overload_constant_str(
            oike__mfem):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        nyoj__ave = fvbh__azt[30]
        if not is_overload_none(nyoj__ave) and not is_overload_constant_str(
            nyoj__ave):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        zvupy__wio = types.List(types.mpl_line_2d_type)
        gsun__gdt = get_overload_const_str(gsun__gdt)
        if gsun__gdt == 'scatter':
            if is_overload_none(etlpy__njogs) and is_overload_none(ulqy__pdpqn
                ):
                raise BodoError(
                    f'{func_name}: {gsun__gdt} requires an x and y column.')
            elif is_overload_none(etlpy__njogs):
                raise BodoError(
                    f'{func_name}: {gsun__gdt} x column is missing.')
            elif is_overload_none(ulqy__pdpqn):
                raise BodoError(
                    f'{func_name}: {gsun__gdt} y column is missing.')
            zvupy__wio = types.mpl_path_collection_type
        elif gsun__gdt != 'line':
            raise BodoError(f'{func_name}: {gsun__gdt} plot is not supported.')
        return signature(zvupy__wio, *fvbh__azt).replace(pysig=cml__jmk)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            scho__lyvt = df.columns.index(attr)
            arr_typ = df.data[scho__lyvt]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            myoj__btnj = []
            clh__tir = []
            uwvcf__wmowp = False
            for i, ayfl__blbx in enumerate(df.columns):
                if ayfl__blbx[0] != attr:
                    continue
                uwvcf__wmowp = True
                myoj__btnj.append(ayfl__blbx[1] if len(ayfl__blbx) == 2 else
                    ayfl__blbx[1:])
                clh__tir.append(df.data[i])
            if uwvcf__wmowp:
                return DataFrameType(tuple(clh__tir), df.index, tuple(
                    myoj__btnj))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        xou__orqje = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(xou__orqje)
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
        cejue__ahjms = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], cejue__ahjms)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    gnb__btg = builder.module
    lvfj__wln = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    cge__rsesc = cgutils.get_or_insert_function(gnb__btg, lvfj__wln, name=
        '.dtor.df.{}'.format(df_type))
    if not cge__rsesc.is_declaration:
        return cge__rsesc
    cge__rsesc.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(cge__rsesc.append_basic_block())
    pexdm__taf = cge__rsesc.args[0]
    iooke__djpw = context.get_value_type(payload_type).as_pointer()
    hsxgt__gowsi = builder.bitcast(pexdm__taf, iooke__djpw)
    payload = context.make_helper(builder, payload_type, ref=hsxgt__gowsi)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        oqtrg__gccsw = context.get_python_api(builder)
        aeww__ksnxl = oqtrg__gccsw.gil_ensure()
        oqtrg__gccsw.decref(payload.parent)
        oqtrg__gccsw.gil_release(aeww__ksnxl)
    builder.ret_void()
    return cge__rsesc


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    azf__kftcy = cgutils.create_struct_proxy(payload_type)(context, builder)
    azf__kftcy.data = data_tup
    azf__kftcy.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        azf__kftcy.columns = colnames
    vuhc__xgxmb = context.get_value_type(payload_type)
    ijvc__lztwo = context.get_abi_sizeof(vuhc__xgxmb)
    ptvf__ygedd = define_df_dtor(context, builder, df_type, payload_type)
    cybk__nyejq = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ijvc__lztwo), ptvf__ygedd)
    jsfkh__soh = context.nrt.meminfo_data(builder, cybk__nyejq)
    gyppq__fuwie = builder.bitcast(jsfkh__soh, vuhc__xgxmb.as_pointer())
    ceei__act = cgutils.create_struct_proxy(df_type)(context, builder)
    ceei__act.meminfo = cybk__nyejq
    if parent is None:
        ceei__act.parent = cgutils.get_null_value(ceei__act.parent.type)
    else:
        ceei__act.parent = parent
        azf__kftcy.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            oqtrg__gccsw = context.get_python_api(builder)
            aeww__ksnxl = oqtrg__gccsw.gil_ensure()
            oqtrg__gccsw.incref(parent)
            oqtrg__gccsw.gil_release(aeww__ksnxl)
    builder.store(azf__kftcy._getvalue(), gyppq__fuwie)
    return ceei__act._getvalue()


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
        taul__bis = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype.
            arr_types)
    else:
        taul__bis = [yqs__nxaqn for yqs__nxaqn in data_typ.dtype.arr_types]
    xgzig__jdw = DataFrameType(tuple(taul__bis + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        rvrko__ftgtn = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return rvrko__ftgtn
    sig = signature(xgzig__jdw, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    aqr__xxeut = len(data_tup_typ.types)
    if aqr__xxeut == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if aqr__xxeut == 1 and isinstance(data_tup_typ.types[0], TableType):
        aqr__xxeut = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == aqr__xxeut, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    smwx__avfq = data_tup_typ.types
    if aqr__xxeut != 0 and isinstance(data_tup_typ.types[0], TableType):
        smwx__avfq = data_tup_typ.types[0].arr_types
        is_table_format = True
    xgzig__jdw = DataFrameType(smwx__avfq, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            unlk__dpn = cgutils.create_struct_proxy(xgzig__jdw.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = unlk__dpn.parent
        rvrko__ftgtn = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return rvrko__ftgtn
    sig = signature(xgzig__jdw, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        ceei__act = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, ceei__act.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        azf__kftcy = get_dataframe_payload(context, builder, df_typ, args[0])
        fvq__tieg = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[fvq__tieg]
        if df_typ.is_table_format:
            unlk__dpn = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(azf__kftcy.data, 0))
            ubbij__usl = df_typ.table_type.type_to_blk[arr_typ]
            cnflf__rfj = getattr(unlk__dpn, f'block_{ubbij__usl}')
            zhqq__vmu = ListInstance(context, builder, types.List(arr_typ),
                cnflf__rfj)
            oimax__kewb = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[fvq__tieg])
            cejue__ahjms = zhqq__vmu.getitem(oimax__kewb)
        else:
            cejue__ahjms = builder.extract_value(azf__kftcy.data, fvq__tieg)
        afplj__grno = cgutils.alloca_once_value(builder, cejue__ahjms)
        xiq__blfp = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, afplj__grno, xiq__blfp)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    cybk__nyejq = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, cybk__nyejq)
    iooke__djpw = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, iooke__djpw)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    xgzig__jdw = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        xgzig__jdw = types.Tuple([TableType(df_typ.data)])
    sig = signature(xgzig__jdw, df_typ)

    def codegen(context, builder, signature, args):
        azf__kftcy = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            azf__kftcy.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        azf__kftcy = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, azf__kftcy
            .index)
    xgzig__jdw = df_typ.index
    sig = signature(xgzig__jdw, df_typ)
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
        pwcsn__xpt = df.data[i]
        return pwcsn__xpt(*args)


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
        azf__kftcy = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(azf__kftcy.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        azf__kftcy = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, azf__kftcy.columns)
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
    mhrj__ekjk = self.typemap[data_tup.name]
    if any(is_tuple_like_type(yqs__nxaqn) for yqs__nxaqn in mhrj__ekjk.types):
        return None
    if equiv_set.has_shape(data_tup):
        vrbvv__cgge = equiv_set.get_shape(data_tup)
        if len(vrbvv__cgge) > 1:
            equiv_set.insert_equiv(*vrbvv__cgge)
        if len(vrbvv__cgge) > 0:
            jhqn__kmc = self.typemap[index.name]
            if not isinstance(jhqn__kmc, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(vrbvv__cgge[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(vrbvv__cgge[0], len(
                vrbvv__cgge)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    kmjw__osmjm = args[0]
    data_types = self.typemap[kmjw__osmjm.name].data
    if any(is_tuple_like_type(yqs__nxaqn) for yqs__nxaqn in data_types):
        return None
    if equiv_set.has_shape(kmjw__osmjm):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            kmjw__osmjm)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    kmjw__osmjm = args[0]
    jhqn__kmc = self.typemap[kmjw__osmjm.name].index
    if isinstance(jhqn__kmc, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(kmjw__osmjm):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            kmjw__osmjm)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    kmjw__osmjm = args[0]
    if equiv_set.has_shape(kmjw__osmjm):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            kmjw__osmjm), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    kmjw__osmjm = args[0]
    if equiv_set.has_shape(kmjw__osmjm):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            kmjw__osmjm)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    fvq__tieg = get_overload_const_int(c_ind_typ)
    if df_typ.data[fvq__tieg] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        ocx__lxi, bffpj__yntsk, vzitg__yuyyh = args
        azf__kftcy = get_dataframe_payload(context, builder, df_typ, ocx__lxi)
        if df_typ.is_table_format:
            unlk__dpn = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(azf__kftcy.data, 0))
            ubbij__usl = df_typ.table_type.type_to_blk[arr_typ]
            cnflf__rfj = getattr(unlk__dpn, f'block_{ubbij__usl}')
            zhqq__vmu = ListInstance(context, builder, types.List(arr_typ),
                cnflf__rfj)
            oimax__kewb = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[fvq__tieg])
            zhqq__vmu.setitem(oimax__kewb, vzitg__yuyyh, True)
        else:
            cejue__ahjms = builder.extract_value(azf__kftcy.data, fvq__tieg)
            context.nrt.decref(builder, df_typ.data[fvq__tieg], cejue__ahjms)
            azf__kftcy.data = builder.insert_value(azf__kftcy.data,
                vzitg__yuyyh, fvq__tieg)
            context.nrt.incref(builder, arr_typ, vzitg__yuyyh)
        ceei__act = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=ocx__lxi)
        payload_type = DataFramePayloadType(df_typ)
        hsxgt__gowsi = context.nrt.meminfo_data(builder, ceei__act.meminfo)
        iooke__djpw = context.get_value_type(payload_type).as_pointer()
        hsxgt__gowsi = builder.bitcast(hsxgt__gowsi, iooke__djpw)
        builder.store(azf__kftcy._getvalue(), hsxgt__gowsi)
        return impl_ret_borrowed(context, builder, df_typ, ocx__lxi)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        fth__ftwty = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        gey__qaxzs = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=fth__ftwty)
        wznh__lib = get_dataframe_payload(context, builder, df_typ, fth__ftwty)
        ceei__act = construct_dataframe(context, builder, signature.
            return_type, wznh__lib.data, index_val, gey__qaxzs.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), wznh__lib.data)
        return ceei__act
    xgzig__jdw = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(xgzig__jdw, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    aqr__xxeut = len(df_type.columns)
    qklbe__vyfko = aqr__xxeut
    qhgdj__zbsqi = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    xixxd__kzbh = col_name not in df_type.columns
    fvq__tieg = aqr__xxeut
    if xixxd__kzbh:
        qhgdj__zbsqi += arr_type,
        column_names += col_name,
        qklbe__vyfko += 1
    else:
        fvq__tieg = df_type.columns.index(col_name)
        qhgdj__zbsqi = tuple(arr_type if i == fvq__tieg else qhgdj__zbsqi[i
            ] for i in range(aqr__xxeut))

    def codegen(context, builder, signature, args):
        ocx__lxi, bffpj__yntsk, vzitg__yuyyh = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, ocx__lxi)
        jug__qjh = cgutils.create_struct_proxy(df_type)(context, builder,
            value=ocx__lxi)
        if df_type.is_table_format:
            aibf__zry = df_type.table_type
            kzq__jkcnt = builder.extract_value(in_dataframe_payload.data, 0)
            tcf__uckk = TableType(qhgdj__zbsqi)
            hpdso__hcll = set_table_data_codegen(context, builder,
                aibf__zry, kzq__jkcnt, tcf__uckk, arr_type, vzitg__yuyyh,
                fvq__tieg, xixxd__kzbh)
            data_tup = context.make_tuple(builder, types.Tuple([tcf__uckk]),
                [hpdso__hcll])
        else:
            smwx__avfq = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != fvq__tieg else vzitg__yuyyh) for i in range(
                aqr__xxeut)]
            if xixxd__kzbh:
                smwx__avfq.append(vzitg__yuyyh)
            for kmjw__osmjm, idhk__puc in zip(smwx__avfq, qhgdj__zbsqi):
                context.nrt.incref(builder, idhk__puc, kmjw__osmjm)
            data_tup = context.make_tuple(builder, types.Tuple(qhgdj__zbsqi
                ), smwx__avfq)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        zgwb__vtfea = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, jug__qjh.parent, None)
        if not xixxd__kzbh and arr_type == df_type.data[fvq__tieg]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            hsxgt__gowsi = context.nrt.meminfo_data(builder, jug__qjh.meminfo)
            iooke__djpw = context.get_value_type(payload_type).as_pointer()
            hsxgt__gowsi = builder.bitcast(hsxgt__gowsi, iooke__djpw)
            erwq__sjc = get_dataframe_payload(context, builder, df_type,
                zgwb__vtfea)
            builder.store(erwq__sjc._getvalue(), hsxgt__gowsi)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, tcf__uckk, builder.
                    extract_value(data_tup, 0))
            else:
                for kmjw__osmjm, idhk__puc in zip(smwx__avfq, qhgdj__zbsqi):
                    context.nrt.incref(builder, idhk__puc, kmjw__osmjm)
        has_parent = cgutils.is_not_null(builder, jug__qjh.parent)
        with builder.if_then(has_parent):
            oqtrg__gccsw = context.get_python_api(builder)
            aeww__ksnxl = oqtrg__gccsw.gil_ensure()
            epjj__spa = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, vzitg__yuyyh)
            wbbk__qatve = numba.core.pythonapi._BoxContext(context, builder,
                oqtrg__gccsw, epjj__spa)
            rwp__elgex = wbbk__qatve.pyapi.from_native_value(arr_type,
                vzitg__yuyyh, wbbk__qatve.env_manager)
            if isinstance(col_name, str):
                aymss__wfnm = context.insert_const_string(builder.module,
                    col_name)
                uvutg__nuwb = oqtrg__gccsw.string_from_string(aymss__wfnm)
            else:
                assert isinstance(col_name, int)
                uvutg__nuwb = oqtrg__gccsw.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            oqtrg__gccsw.object_setitem(jug__qjh.parent, uvutg__nuwb,
                rwp__elgex)
            oqtrg__gccsw.decref(rwp__elgex)
            oqtrg__gccsw.decref(uvutg__nuwb)
            oqtrg__gccsw.gil_release(aeww__ksnxl)
        return zgwb__vtfea
    xgzig__jdw = DataFrameType(qhgdj__zbsqi, index_typ, column_names,
        df_type.dist, df_type.is_table_format)
    sig = signature(xgzig__jdw, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    aqr__xxeut = len(pyval.columns)
    smwx__avfq = []
    for i in range(aqr__xxeut):
        agj__qiqsz = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            rwp__elgex = agj__qiqsz.array
        else:
            rwp__elgex = agj__qiqsz.values
        smwx__avfq.append(rwp__elgex)
    smwx__avfq = tuple(smwx__avfq)
    if df_type.is_table_format:
        unlk__dpn = context.get_constant_generic(builder, df_type.
            table_type, Table(smwx__avfq))
        data_tup = lir.Constant.literal_struct([unlk__dpn])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], ayfl__blbx) for 
            i, ayfl__blbx in enumerate(smwx__avfq)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    ziu__lyyo = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, ziu__lyyo])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    ywitc__asu = context.get_constant(types.int64, -1)
    eyf__oor = context.get_constant_null(types.voidptr)
    cybk__nyejq = lir.Constant.literal_struct([ywitc__asu, eyf__oor,
        eyf__oor, payload, ywitc__asu])
    cybk__nyejq = cgutils.global_constant(builder, '.const.meminfo',
        cybk__nyejq).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([cybk__nyejq, ziu__lyyo])


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
        qkei__jda = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        qkei__jda = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, qkei__jda)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        clh__tir = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                clh__tir)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), clh__tir)
    elif not fromty.is_table_format and toty.is_table_format:
        clh__tir = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        clh__tir = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        clh__tir = _cast_df_data_keep_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    else:
        clh__tir = _cast_df_data_keep_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, clh__tir, qkei__jda,
        in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    bpxp__nmxc = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        tgb__cus = get_index_data_arr_types(toty.index)[0]
        gpjs__amf = bodo.utils.transform.get_type_alloc_counts(tgb__cus) - 1
        ixe__cog = ', '.join('0' for bffpj__yntsk in range(gpjs__amf))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(ixe__cog, ', ' if gpjs__amf == 1 else ''))
        bpxp__nmxc['index_arr_type'] = tgb__cus
    dwj__mqu = []
    for i, arr_typ in enumerate(toty.data):
        gpjs__amf = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        ixe__cog = ', '.join('0' for bffpj__yntsk in range(gpjs__amf))
        mblk__hfz = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, ixe__cog, ', ' if gpjs__amf == 1 else ''))
        dwj__mqu.append(mblk__hfz)
        bpxp__nmxc[f'arr_type{i}'] = arr_typ
    dwj__mqu = ', '.join(dwj__mqu)
    zplp__wiesi = 'def impl():\n'
    aclcx__iilrc = bodo.hiframes.dataframe_impl._gen_init_df(zplp__wiesi,
        toty.columns, dwj__mqu, index, bpxp__nmxc)
    df = context.compile_internal(builder, aclcx__iilrc, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    wjhy__xiwuy = toty.table_type
    unlk__dpn = cgutils.create_struct_proxy(wjhy__xiwuy)(context, builder)
    unlk__dpn.parent = in_dataframe_payload.parent
    for yqs__nxaqn, ubbij__usl in wjhy__xiwuy.type_to_blk.items():
        yttzk__lni = context.get_constant(types.int64, len(wjhy__xiwuy.
            block_to_arr_ind[ubbij__usl]))
        bffpj__yntsk, hke__rsp = ListInstance.allocate_ex(context, builder,
            types.List(yqs__nxaqn), yttzk__lni)
        hke__rsp.size = yttzk__lni
        setattr(unlk__dpn, f'block_{ubbij__usl}', hke__rsp.value)
    for i, yqs__nxaqn in enumerate(fromty.data):
        naes__czkql = toty.data[i]
        if yqs__nxaqn != naes__czkql:
            vwfkd__hknw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*vwfkd__hknw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        cejue__ahjms = builder.extract_value(in_dataframe_payload.data, i)
        if yqs__nxaqn != naes__czkql:
            tnjpw__scvg = context.cast(builder, cejue__ahjms, yqs__nxaqn,
                naes__czkql)
            eaksn__wxs = False
        else:
            tnjpw__scvg = cejue__ahjms
            eaksn__wxs = True
        ubbij__usl = wjhy__xiwuy.type_to_blk[yqs__nxaqn]
        cnflf__rfj = getattr(unlk__dpn, f'block_{ubbij__usl}')
        zhqq__vmu = ListInstance(context, builder, types.List(yqs__nxaqn),
            cnflf__rfj)
        oimax__kewb = context.get_constant(types.int64, wjhy__xiwuy.
            block_offsets[i])
        zhqq__vmu.setitem(oimax__kewb, tnjpw__scvg, eaksn__wxs)
    data_tup = context.make_tuple(builder, types.Tuple([wjhy__xiwuy]), [
        unlk__dpn._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    smwx__avfq = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            vwfkd__hknw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*vwfkd__hknw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            cejue__ahjms = builder.extract_value(in_dataframe_payload.data, i)
            tnjpw__scvg = context.cast(builder, cejue__ahjms, fromty.data[i
                ], toty.data[i])
            eaksn__wxs = False
        else:
            tnjpw__scvg = builder.extract_value(in_dataframe_payload.data, i)
            eaksn__wxs = True
        if eaksn__wxs:
            context.nrt.incref(builder, toty.data[i], tnjpw__scvg)
        smwx__avfq.append(tnjpw__scvg)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), smwx__avfq)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    aibf__zry = fromty.table_type
    kzq__jkcnt = cgutils.create_struct_proxy(aibf__zry)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    tcf__uckk = toty.table_type
    hpdso__hcll = cgutils.create_struct_proxy(tcf__uckk)(context, builder)
    hpdso__hcll.parent = in_dataframe_payload.parent
    for yqs__nxaqn, ubbij__usl in tcf__uckk.type_to_blk.items():
        yttzk__lni = context.get_constant(types.int64, len(tcf__uckk.
            block_to_arr_ind[ubbij__usl]))
        bffpj__yntsk, hke__rsp = ListInstance.allocate_ex(context, builder,
            types.List(yqs__nxaqn), yttzk__lni)
        hke__rsp.size = yttzk__lni
        setattr(hpdso__hcll, f'block_{ubbij__usl}', hke__rsp.value)
    for i in range(len(fromty.data)):
        ilsev__oag = fromty.data[i]
        naes__czkql = toty.data[i]
        if ilsev__oag != naes__czkql:
            vwfkd__hknw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*vwfkd__hknw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ebnvm__qrfc = aibf__zry.type_to_blk[ilsev__oag]
        gqmj__nco = getattr(kzq__jkcnt, f'block_{ebnvm__qrfc}')
        lnf__xskp = ListInstance(context, builder, types.List(ilsev__oag),
            gqmj__nco)
        odgij__edgz = context.get_constant(types.int64, aibf__zry.
            block_offsets[i])
        cejue__ahjms = lnf__xskp.getitem(odgij__edgz)
        if ilsev__oag != naes__czkql:
            tnjpw__scvg = context.cast(builder, cejue__ahjms, ilsev__oag,
                naes__czkql)
            eaksn__wxs = False
        else:
            tnjpw__scvg = cejue__ahjms
            eaksn__wxs = True
        dwi__cai = tcf__uckk.type_to_blk[yqs__nxaqn]
        hke__rsp = getattr(hpdso__hcll, f'block_{dwi__cai}')
        xwv__afvn = ListInstance(context, builder, types.List(naes__czkql),
            hke__rsp)
        jcmfx__xlara = context.get_constant(types.int64, tcf__uckk.
            block_offsets[i])
        xwv__afvn.setitem(jcmfx__xlara, tnjpw__scvg, eaksn__wxs)
    data_tup = context.make_tuple(builder, types.Tuple([tcf__uckk]), [
        hpdso__hcll._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    wjhy__xiwuy = fromty.table_type
    unlk__dpn = cgutils.create_struct_proxy(wjhy__xiwuy)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    smwx__avfq = []
    for i, yqs__nxaqn in enumerate(toty.data):
        ilsev__oag = fromty.data[i]
        if yqs__nxaqn != ilsev__oag:
            vwfkd__hknw = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*vwfkd__hknw)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ubbij__usl = wjhy__xiwuy.type_to_blk[yqs__nxaqn]
        cnflf__rfj = getattr(unlk__dpn, f'block_{ubbij__usl}')
        zhqq__vmu = ListInstance(context, builder, types.List(yqs__nxaqn),
            cnflf__rfj)
        oimax__kewb = context.get_constant(types.int64, wjhy__xiwuy.
            block_offsets[i])
        cejue__ahjms = zhqq__vmu.getitem(oimax__kewb)
        if yqs__nxaqn != ilsev__oag:
            tnjpw__scvg = context.cast(builder, cejue__ahjms, ilsev__oag,
                yqs__nxaqn)
            eaksn__wxs = False
        else:
            tnjpw__scvg = cejue__ahjms
            eaksn__wxs = True
        if eaksn__wxs:
            context.nrt.incref(builder, yqs__nxaqn, tnjpw__scvg)
        smwx__avfq.append(tnjpw__scvg)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), smwx__avfq)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    psk__jwhiq, dwj__mqu, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    kbnm__ybgov = gen_const_tup(psk__jwhiq)
    zplp__wiesi = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    zplp__wiesi += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(dwj__mqu, index_arg, kbnm__ybgov))
    gom__ngvx = {}
    exec(zplp__wiesi, {'bodo': bodo, 'np': np}, gom__ngvx)
    rzj__rrudm = gom__ngvx['_init_df']
    return rzj__rrudm


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    xgzig__jdw = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(xgzig__jdw, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    xgzig__jdw = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(xgzig__jdw, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    dpra__gvzjr = ''
    if not is_overload_none(dtype):
        dpra__gvzjr = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        aqr__xxeut = (len(data.types) - 1) // 2
        obxsf__sqctf = [yqs__nxaqn.literal_value for yqs__nxaqn in data.
            types[1:aqr__xxeut + 1]]
        data_val_types = dict(zip(obxsf__sqctf, data.types[aqr__xxeut + 1:]))
        smwx__avfq = ['data[{}]'.format(i) for i in range(aqr__xxeut + 1, 2 *
            aqr__xxeut + 1)]
        data_dict = dict(zip(obxsf__sqctf, smwx__avfq))
        if is_overload_none(index):
            for i, yqs__nxaqn in enumerate(data.types[aqr__xxeut + 1:]):
                if isinstance(yqs__nxaqn, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(aqr__xxeut + 1 + i))
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
        rcnm__czblx = '.copy()' if copy else ''
        qtbu__rlda = get_overload_const_list(columns)
        aqr__xxeut = len(qtbu__rlda)
        data_val_types = {wbbk__qatve: data.copy(ndim=1) for wbbk__qatve in
            qtbu__rlda}
        smwx__avfq = ['data[:,{}]{}'.format(i, rcnm__czblx) for i in range(
            aqr__xxeut)]
        data_dict = dict(zip(qtbu__rlda, smwx__avfq))
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
    dwj__mqu = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[wbbk__qatve], df_len, dpra__gvzjr) for
        wbbk__qatve in col_names))
    if len(col_names) == 0:
        dwj__mqu = '()'
    return col_names, dwj__mqu, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for wbbk__qatve in col_names:
        if wbbk__qatve in data_dict and is_iterable_type(data_val_types[
            wbbk__qatve]):
            df_len = 'len({})'.format(data_dict[wbbk__qatve])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(wbbk__qatve in data_dict for wbbk__qatve in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    oryj__bir = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for wbbk__qatve in col_names:
        if wbbk__qatve not in data_dict:
            data_dict[wbbk__qatve] = oryj__bir


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
            yqs__nxaqn = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(yqs__nxaqn)
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
        hbhzf__yrcw = idx.literal_value
        if isinstance(hbhzf__yrcw, int):
            pwcsn__xpt = tup.types[hbhzf__yrcw]
        elif isinstance(hbhzf__yrcw, slice):
            pwcsn__xpt = types.BaseTuple.from_types(tup.types[hbhzf__yrcw])
        return signature(pwcsn__xpt, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    pysp__aeuv, idx = sig.args
    idx = idx.literal_value
    tup, bffpj__yntsk = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(pysp__aeuv)
        if not 0 <= idx < len(pysp__aeuv):
            raise IndexError('cannot index at %d in %s' % (idx, pysp__aeuv))
        qoiu__mnw = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        aaktm__pifdo = cgutils.unpack_tuple(builder, tup)[idx]
        qoiu__mnw = context.make_tuple(builder, sig.return_type, aaktm__pifdo)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, qoiu__mnw)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, opa__auu, suffix_x, suffix_y,
            is_join, indicator, _bodo_na_equal, ielt__dbz) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        apvo__xvjxh = set(left_on) & set(right_on)
        gvu__cbv = set(left_df.columns) & set(right_df.columns)
        pkm__tbn = gvu__cbv - apvo__xvjxh
        vyyq__rfpi = '$_bodo_index_' in left_on
        kcud__nthi = '$_bodo_index_' in right_on
        how = get_overload_const_str(opa__auu)
        erx__laqm = how in {'left', 'outer'}
        aaf__qxk = how in {'right', 'outer'}
        columns = []
        data = []
        if vyyq__rfpi:
            ttpyp__nhwxi = bodo.utils.typing.get_index_data_arr_types(left_df
                .index)[0]
        else:
            ttpyp__nhwxi = left_df.data[left_df.columns.index(left_on[0])]
        if kcud__nthi:
            pjkoy__oxgyw = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            pjkoy__oxgyw = right_df.data[right_df.columns.index(right_on[0])]
        if vyyq__rfpi and not kcud__nthi and not is_join.literal_value:
            zaeem__aeb = right_on[0]
            if zaeem__aeb in left_df.columns:
                columns.append(zaeem__aeb)
                if (pjkoy__oxgyw == bodo.dict_str_arr_type and ttpyp__nhwxi ==
                    bodo.string_array_type):
                    tsljj__zhng = bodo.string_array_type
                else:
                    tsljj__zhng = pjkoy__oxgyw
                data.append(tsljj__zhng)
        if kcud__nthi and not vyyq__rfpi and not is_join.literal_value:
            lpflj__gdrx = left_on[0]
            if lpflj__gdrx in right_df.columns:
                columns.append(lpflj__gdrx)
                if (ttpyp__nhwxi == bodo.dict_str_arr_type and pjkoy__oxgyw ==
                    bodo.string_array_type):
                    tsljj__zhng = bodo.string_array_type
                else:
                    tsljj__zhng = ttpyp__nhwxi
                data.append(tsljj__zhng)
        for ilsev__oag, agj__qiqsz in zip(left_df.data, left_df.columns):
            columns.append(str(agj__qiqsz) + suffix_x.literal_value if 
                agj__qiqsz in pkm__tbn else agj__qiqsz)
            if agj__qiqsz in apvo__xvjxh:
                if ilsev__oag == bodo.dict_str_arr_type:
                    ilsev__oag = right_df.data[right_df.columns.index(
                        agj__qiqsz)]
                data.append(ilsev__oag)
            else:
                if (ilsev__oag == bodo.dict_str_arr_type and agj__qiqsz in
                    left_on):
                    if kcud__nthi:
                        ilsev__oag = pjkoy__oxgyw
                    else:
                        jjxz__hdl = left_on.index(agj__qiqsz)
                        try__iwp = right_on[jjxz__hdl]
                        ilsev__oag = right_df.data[right_df.columns.index(
                            try__iwp)]
                if aaf__qxk:
                    ilsev__oag = to_nullable_type(ilsev__oag)
                data.append(ilsev__oag)
        for ilsev__oag, agj__qiqsz in zip(right_df.data, right_df.columns):
            if agj__qiqsz not in apvo__xvjxh:
                columns.append(str(agj__qiqsz) + suffix_y.literal_value if 
                    agj__qiqsz in pkm__tbn else agj__qiqsz)
                if (ilsev__oag == bodo.dict_str_arr_type and agj__qiqsz in
                    right_on):
                    if vyyq__rfpi:
                        ilsev__oag = ttpyp__nhwxi
                    else:
                        jjxz__hdl = right_on.index(agj__qiqsz)
                        lckdt__zdr = left_on[jjxz__hdl]
                        ilsev__oag = left_df.data[left_df.columns.index(
                            lckdt__zdr)]
                if erx__laqm:
                    ilsev__oag = to_nullable_type(ilsev__oag)
                data.append(ilsev__oag)
        eubs__psb = get_overload_const_bool(indicator)
        if eubs__psb:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        if vyyq__rfpi and kcud__nthi and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif vyyq__rfpi and not kcud__nthi:
            index_typ = right_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif kcud__nthi and not vyyq__rfpi:
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        qlh__fgqcu = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(qlh__fgqcu, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    ceei__act = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return ceei__act._getvalue()


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
    sjfa__ewy = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    zagsu__aont = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', sjfa__ewy, zagsu__aont,
        package_name='pandas', module_name='General')
    zplp__wiesi = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        lvni__gpu = 0
        dwj__mqu = []
        names = []
        for i, rzo__lhxe in enumerate(objs.types):
            assert isinstance(rzo__lhxe, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(rzo__lhxe, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rzo__lhxe
                , 'pandas.concat()')
            if isinstance(rzo__lhxe, SeriesType):
                names.append(str(lvni__gpu))
                lvni__gpu += 1
                dwj__mqu.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(rzo__lhxe.columns)
                for gvfp__rdsma in range(len(rzo__lhxe.data)):
                    dwj__mqu.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, gvfp__rdsma))
        return bodo.hiframes.dataframe_impl._gen_init_df(zplp__wiesi, names,
            ', '.join(dwj__mqu), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(yqs__nxaqn, DataFrameType) for yqs__nxaqn in
            objs.types)
        iqvwf__ktr = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            iqvwf__ktr.extend(df.columns)
        iqvwf__ktr = list(dict.fromkeys(iqvwf__ktr).keys())
        taul__bis = {}
        for lvni__gpu, wbbk__qatve in enumerate(iqvwf__ktr):
            for df in objs.types:
                if wbbk__qatve in df.columns:
                    taul__bis['arr_typ{}'.format(lvni__gpu)] = df.data[df.
                        columns.index(wbbk__qatve)]
                    break
        assert len(taul__bis) == len(iqvwf__ktr)
        hzcft__ayrvz = []
        for lvni__gpu, wbbk__qatve in enumerate(iqvwf__ktr):
            args = []
            for i, df in enumerate(objs.types):
                if wbbk__qatve in df.columns:
                    fvq__tieg = df.columns.index(wbbk__qatve)
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, fvq__tieg))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, lvni__gpu))
            zplp__wiesi += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(lvni__gpu, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(zplp__wiesi,
            iqvwf__ktr, ', '.join('A{}'.format(i) for i in range(len(
            iqvwf__ktr))), index, taul__bis)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(yqs__nxaqn, SeriesType) for yqs__nxaqn in
            objs.types)
        zplp__wiesi += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            zplp__wiesi += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            zplp__wiesi += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        zplp__wiesi += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        gom__ngvx = {}
        exec(zplp__wiesi, {'bodo': bodo, 'np': np, 'numba': numba}, gom__ngvx)
        return gom__ngvx['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for lvni__gpu, wbbk__qatve in enumerate(df_type.columns):
            zplp__wiesi += '  arrs{} = []\n'.format(lvni__gpu)
            zplp__wiesi += '  for i in range(len(objs)):\n'
            zplp__wiesi += '    df = objs[i]\n'
            zplp__wiesi += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(lvni__gpu))
            zplp__wiesi += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(lvni__gpu))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            zplp__wiesi += '  arrs_index = []\n'
            zplp__wiesi += '  for i in range(len(objs)):\n'
            zplp__wiesi += '    df = objs[i]\n'
            zplp__wiesi += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(zplp__wiesi,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        zplp__wiesi += '  arrs = []\n'
        zplp__wiesi += '  for i in range(len(objs)):\n'
        zplp__wiesi += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        zplp__wiesi += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            zplp__wiesi += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            zplp__wiesi += '  arrs_index = []\n'
            zplp__wiesi += '  for i in range(len(objs)):\n'
            zplp__wiesi += '    S = objs[i]\n'
            zplp__wiesi += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            zplp__wiesi += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        zplp__wiesi += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        gom__ngvx = {}
        exec(zplp__wiesi, {'bodo': bodo, 'np': np, 'numba': numba}, gom__ngvx)
        return gom__ngvx['impl']
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
        xgzig__jdw = df.copy(index=index, is_table_format=False)
        return signature(xgzig__jdw, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    vdjff__ldfqz = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return vdjff__ldfqz._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    sjfa__ewy = dict(index=index, name=name)
    zagsu__aont = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', sjfa__ewy, zagsu__aont,
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
        taul__bis = (types.Array(types.int64, 1, 'C'),) + df.data
        pavql__nzp = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, taul__bis)
        return signature(pavql__nzp, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    vdjff__ldfqz = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return vdjff__ldfqz._getvalue()


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
    vdjff__ldfqz = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return vdjff__ldfqz._getvalue()


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
    vdjff__ldfqz = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return vdjff__ldfqz._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    ava__fsvs = get_overload_const_bool(check_duplicates)
    netmz__dwkbc = not is_overload_none(value_names)
    tntby__abczn = isinstance(values_tup, types.UniTuple)
    if tntby__abczn:
        fux__qilyu = [to_nullable_type(values_tup.dtype)]
    else:
        fux__qilyu = [to_nullable_type(idhk__puc) for idhk__puc in values_tup]
    zplp__wiesi = 'def impl(\n'
    zplp__wiesi += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    zplp__wiesi += '):\n'
    zplp__wiesi += '    if parallel:\n'
    uxc__iij = ', '.join([f'array_to_info(index_tup[{i}])' for i in range(
        len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    zplp__wiesi += f'        info_list = [{uxc__iij}]\n'
    zplp__wiesi += '        cpp_table = arr_info_list_to_table(info_list)\n'
    zplp__wiesi += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
    tilr__obme = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    ojn__yxgq = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    byqh__dndal = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    zplp__wiesi += f'        index_tup = ({tilr__obme},)\n'
    zplp__wiesi += f'        columns_tup = ({ojn__yxgq},)\n'
    zplp__wiesi += f'        values_tup = ({byqh__dndal},)\n'
    zplp__wiesi += '        delete_table(cpp_table)\n'
    zplp__wiesi += '        delete_table(out_cpp_table)\n'
    zplp__wiesi += '    columns_arr = columns_tup[0]\n'
    if tntby__abczn:
        zplp__wiesi += '    values_arrs = [arr for arr in values_tup]\n'
    zplp__wiesi += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    zplp__wiesi += '        index_tup\n'
    zplp__wiesi += '    )\n'
    zplp__wiesi += '    n_rows = len(unique_index_arr_tup[0])\n'
    zplp__wiesi += '    num_values_arrays = len(values_tup)\n'
    zplp__wiesi += '    n_unique_pivots = len(pivot_values)\n'
    if tntby__abczn:
        zplp__wiesi += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        zplp__wiesi += '    n_cols = n_unique_pivots\n'
    zplp__wiesi += '    col_map = {}\n'
    zplp__wiesi += '    for i in range(n_unique_pivots):\n'
    zplp__wiesi += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    zplp__wiesi += '            raise ValueError(\n'
    zplp__wiesi += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    zplp__wiesi += '            )\n'
    zplp__wiesi += '        col_map[pivot_values[i]] = i\n'
    roznu__kaw = False
    for i, ggxh__vrsf in enumerate(fux__qilyu):
        if is_str_arr_type(ggxh__vrsf):
            roznu__kaw = True
            zplp__wiesi += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            zplp__wiesi += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if roznu__kaw:
        if ava__fsvs:
            zplp__wiesi += '    nbytes = (n_rows + 7) >> 3\n'
            zplp__wiesi += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        zplp__wiesi += '    for i in range(len(columns_arr)):\n'
        zplp__wiesi += '        col_name = columns_arr[i]\n'
        zplp__wiesi += '        pivot_idx = col_map[col_name]\n'
        zplp__wiesi += '        row_idx = row_vector[i]\n'
        if ava__fsvs:
            zplp__wiesi += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            zplp__wiesi += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            zplp__wiesi += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            zplp__wiesi += '        else:\n'
            zplp__wiesi += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if tntby__abczn:
            zplp__wiesi += '        for j in range(num_values_arrays):\n'
            zplp__wiesi += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            zplp__wiesi += '            len_arr = len_arrs_0[col_idx]\n'
            zplp__wiesi += '            values_arr = values_arrs[j]\n'
            zplp__wiesi += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            zplp__wiesi += (
                '                len_arr[row_idx] = len(values_arr[i])\n')
            zplp__wiesi += (
                '                total_lens_0[col_idx] += len(values_arr[i])\n'
                )
        else:
            for i, ggxh__vrsf in enumerate(fux__qilyu):
                if is_str_arr_type(ggxh__vrsf):
                    zplp__wiesi += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    zplp__wiesi += f"""            len_arrs_{i}[pivot_idx][row_idx] = len(values_tup[{i}][i])
"""
                    zplp__wiesi += f"""            total_lens_{i}[pivot_idx] += len(values_tup[{i}][i])
"""
    for i, ggxh__vrsf in enumerate(fux__qilyu):
        if is_str_arr_type(ggxh__vrsf):
            zplp__wiesi += f'    data_arrs_{i} = [\n'
            zplp__wiesi += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            zplp__wiesi += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            zplp__wiesi += '        )\n'
            zplp__wiesi += '        for i in range(n_cols)\n'
            zplp__wiesi += '    ]\n'
        else:
            zplp__wiesi += f'    data_arrs_{i} = [\n'
            zplp__wiesi += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            zplp__wiesi += '        for _ in range(n_cols)\n'
            zplp__wiesi += '    ]\n'
    if not roznu__kaw and ava__fsvs:
        zplp__wiesi += '    nbytes = (n_rows + 7) >> 3\n'
        zplp__wiesi += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    zplp__wiesi += '    for i in range(len(columns_arr)):\n'
    zplp__wiesi += '        col_name = columns_arr[i]\n'
    zplp__wiesi += '        pivot_idx = col_map[col_name]\n'
    zplp__wiesi += '        row_idx = row_vector[i]\n'
    if not roznu__kaw and ava__fsvs:
        zplp__wiesi += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        zplp__wiesi += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        zplp__wiesi += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        zplp__wiesi += '        else:\n'
        zplp__wiesi += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if tntby__abczn:
        zplp__wiesi += '        for j in range(num_values_arrays):\n'
        zplp__wiesi += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        zplp__wiesi += '            col_arr = data_arrs_0[col_idx]\n'
        zplp__wiesi += '            values_arr = values_arrs[j]\n'
        zplp__wiesi += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        zplp__wiesi += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        zplp__wiesi += '            else:\n'
        zplp__wiesi += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, ggxh__vrsf in enumerate(fux__qilyu):
            zplp__wiesi += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            zplp__wiesi += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            zplp__wiesi += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            zplp__wiesi += f'        else:\n'
            zplp__wiesi += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        zplp__wiesi += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        zplp__wiesi += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if netmz__dwkbc:
        zplp__wiesi += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            zplp__wiesi += '    total_chars = 0\n'
            zplp__wiesi += '    for i in range(len(value_names)):\n'
            zplp__wiesi += '        total_chars += len(value_names[i])\n'
            zplp__wiesi += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            zplp__wiesi += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            zplp__wiesi += '    total_chars = 0\n'
            zplp__wiesi += '    for i in range(len(pivot_values)):\n'
            zplp__wiesi += '        total_chars += len(pivot_values[i])\n'
            zplp__wiesi += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            zplp__wiesi += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        zplp__wiesi += '    for i in range(len(value_names)):\n'
        zplp__wiesi += '        for j in range(len(pivot_values)):\n'
        zplp__wiesi += """            new_value_names[(i * len(pivot_values)) + j] = value_names[i]
"""
        zplp__wiesi += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        zplp__wiesi += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        zplp__wiesi += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    mwm__uom = ', '.join(f'data_arrs_{i}' for i in range(len(fux__qilyu)))
    zplp__wiesi += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({mwm__uom},), n_rows)
"""
    zplp__wiesi += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    zplp__wiesi += '        (table,), index, column_index\n'
    zplp__wiesi += '    )\n'
    gom__ngvx = {}
    izzlm__aimws = {f'data_arr_typ_{i}': ggxh__vrsf for i, ggxh__vrsf in
        enumerate(fux__qilyu)}
    oiq__mmzvu = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **izzlm__aimws}
    exec(zplp__wiesi, oiq__mmzvu, gom__ngvx)
    impl = gom__ngvx['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    bhccs__xqz = {}
    bhccs__xqz['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, cil__eadq in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        bqkic__jblk = None
        if isinstance(cil__eadq, bodo.DatetimeArrayType):
            szon__cmv = 'datetimetz'
            yfhmu__qpxy = 'datetime64[ns]'
            if isinstance(cil__eadq.tz, int):
                klsks__mew = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(cil__eadq.tz))
            else:
                klsks__mew = pd.DatetimeTZDtype(tz=cil__eadq.tz).tz
            bqkic__jblk = {'timezone': pa.lib.tzinfo_to_string(klsks__mew)}
        elif isinstance(cil__eadq, types.Array) or cil__eadq == boolean_array:
            szon__cmv = yfhmu__qpxy = cil__eadq.dtype.name
            if yfhmu__qpxy.startswith('datetime'):
                szon__cmv = 'datetime'
        elif is_str_arr_type(cil__eadq):
            szon__cmv = 'unicode'
            yfhmu__qpxy = 'object'
        elif cil__eadq == binary_array_type:
            szon__cmv = 'bytes'
            yfhmu__qpxy = 'object'
        elif isinstance(cil__eadq, DecimalArrayType):
            szon__cmv = yfhmu__qpxy = 'object'
        elif isinstance(cil__eadq, IntegerArrayType):
            tayfq__migby = cil__eadq.dtype.name
            if tayfq__migby.startswith('int'):
                szon__cmv = 'Int' + tayfq__migby[3:]
            elif tayfq__migby.startswith('uint'):
                szon__cmv = 'UInt' + tayfq__migby[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, cil__eadq))
            yfhmu__qpxy = cil__eadq.dtype.name
        elif cil__eadq == datetime_date_array_type:
            szon__cmv = 'datetime'
            yfhmu__qpxy = 'object'
        elif isinstance(cil__eadq, (StructArrayType, ArrayItemArrayType)):
            szon__cmv = 'object'
            yfhmu__qpxy = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, cil__eadq))
        lxowz__jnxc = {'name': col_name, 'field_name': col_name,
            'pandas_type': szon__cmv, 'numpy_type': yfhmu__qpxy, 'metadata':
            bqkic__jblk}
        bhccs__xqz['columns'].append(lxowz__jnxc)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            dvlmc__gdd = '__index_level_0__'
            tixj__uhvu = None
        else:
            dvlmc__gdd = '%s'
            tixj__uhvu = '%s'
        bhccs__xqz['index_columns'] = [dvlmc__gdd]
        bhccs__xqz['columns'].append({'name': tixj__uhvu, 'field_name':
            dvlmc__gdd, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        bhccs__xqz['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        bhccs__xqz['index_columns'] = []
    bhccs__xqz['pandas_version'] = pd.__version__
    return bhccs__xqz


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
        rhkw__mkffq = []
        for phr__zep in partition_cols:
            try:
                idx = df.columns.index(phr__zep)
            except ValueError as nevzx__beitq:
                raise BodoError(
                    f'Partition column {phr__zep} is not in dataframe')
            rhkw__mkffq.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    qptj__dhrea = isinstance(df.index, bodo.hiframes.pd_index_ext.
        RangeIndexType)
    jnvqp__fizje = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not qptj__dhrea)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not qptj__dhrea or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and qptj__dhrea and not is_overload_true(_is_parallel)
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
        vbkf__otm = df.runtime_data_types
        eoj__xry = len(vbkf__otm)
        bqkic__jblk = gen_pandas_parquet_metadata([''] * eoj__xry,
            vbkf__otm, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        ksi__cqbcu = bqkic__jblk['columns'][:eoj__xry]
        bqkic__jblk['columns'] = bqkic__jblk['columns'][eoj__xry:]
        ksi__cqbcu = [json.dumps(etlpy__njogs).replace('""', '{0}') for
            etlpy__njogs in ksi__cqbcu]
        psklx__qhvc = json.dumps(bqkic__jblk)
        zot__izh = '"columns": ['
        afpgi__dqirx = psklx__qhvc.find(zot__izh)
        if afpgi__dqirx == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        trskb__zww = afpgi__dqirx + len(zot__izh)
        jjy__wkfrt = psklx__qhvc[:trskb__zww]
        psklx__qhvc = psklx__qhvc[trskb__zww:]
        pxn__oeql = len(bqkic__jblk['columns'])
    else:
        psklx__qhvc = json.dumps(gen_pandas_parquet_metadata(df.columns, df
            .data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and qptj__dhrea:
        psklx__qhvc = psklx__qhvc.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            psklx__qhvc = psklx__qhvc.replace('"%s"', '%s')
    if not df.is_table_format:
        dwj__mqu = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    zplp__wiesi = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        zplp__wiesi += '    py_table = get_dataframe_table(df)\n'
        zplp__wiesi += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        zplp__wiesi += '    info_list = [{}]\n'.format(dwj__mqu)
        zplp__wiesi += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        zplp__wiesi += '    columns_index = get_dataframe_column_names(df)\n'
        zplp__wiesi += '    names_arr = index_to_array(columns_index)\n'
        zplp__wiesi += '    col_names = array_to_info(names_arr)\n'
    else:
        zplp__wiesi += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and jnvqp__fizje:
        zplp__wiesi += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        lgpny__ttyqd = True
    else:
        zplp__wiesi += '    index_col = array_to_info(np.empty(0))\n'
        lgpny__ttyqd = False
    if df.has_runtime_cols:
        zplp__wiesi += '    columns_lst = []\n'
        zplp__wiesi += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            zplp__wiesi += f'    for _ in range(len(py_table.block_{i})):\n'
            zplp__wiesi += f"""        columns_lst.append({ksi__cqbcu[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            zplp__wiesi += '        num_cols += 1\n'
        if pxn__oeql:
            zplp__wiesi += "    columns_lst.append('')\n"
        zplp__wiesi += '    columns_str = ", ".join(columns_lst)\n'
        zplp__wiesi += ('    metadata = """' + jjy__wkfrt +
            '""" + columns_str + """' + psklx__qhvc + '"""\n')
    else:
        zplp__wiesi += '    metadata = """' + psklx__qhvc + '"""\n'
    zplp__wiesi += '    if compression is None:\n'
    zplp__wiesi += "        compression = 'none'\n"
    zplp__wiesi += '    if df.index.name is not None:\n'
    zplp__wiesi += '        name_ptr = df.index.name\n'
    zplp__wiesi += '    else:\n'
    zplp__wiesi += "        name_ptr = 'null'\n"
    zplp__wiesi += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    hndj__gie = None
    if partition_cols:
        hndj__gie = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        zztgp__vkos = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in rhkw__mkffq)
        if zztgp__vkos:
            zplp__wiesi += '    cat_info_list = [{}]\n'.format(zztgp__vkos)
            zplp__wiesi += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            zplp__wiesi += '    cat_table = table\n'
        zplp__wiesi += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        zplp__wiesi += (
            f'    part_cols_idxs = np.array({rhkw__mkffq}, dtype=np.int32)\n')
        zplp__wiesi += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        zplp__wiesi += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        zplp__wiesi += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        zplp__wiesi += (
            '                            unicode_to_utf8(compression),\n')
        zplp__wiesi += '                            _is_parallel,\n'
        zplp__wiesi += (
            '                            unicode_to_utf8(bucket_region),\n')
        zplp__wiesi += '                            row_group_size)\n'
        zplp__wiesi += '    delete_table_decref_arrays(table)\n'
        zplp__wiesi += '    delete_info_decref_array(index_col)\n'
        zplp__wiesi += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        zplp__wiesi += '    delete_info_decref_array(col_names)\n'
        if zztgp__vkos:
            zplp__wiesi += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        zplp__wiesi += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        zplp__wiesi += (
            '                            table, col_names, index_col,\n')
        zplp__wiesi += '                            ' + str(lgpny__ttyqd
            ) + ',\n'
        zplp__wiesi += (
            '                            unicode_to_utf8(metadata),\n')
        zplp__wiesi += (
            '                            unicode_to_utf8(compression),\n')
        zplp__wiesi += (
            '                            _is_parallel, 1, df.index.start,\n')
        zplp__wiesi += (
            '                            df.index.stop, df.index.step,\n')
        zplp__wiesi += (
            '                            unicode_to_utf8(name_ptr),\n')
        zplp__wiesi += (
            '                            unicode_to_utf8(bucket_region),\n')
        zplp__wiesi += '                            row_group_size)\n'
        zplp__wiesi += '    delete_table_decref_arrays(table)\n'
        zplp__wiesi += '    delete_info_decref_array(index_col)\n'
        zplp__wiesi += '    delete_info_decref_array(col_names)\n'
    else:
        zplp__wiesi += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        zplp__wiesi += (
            '                            table, col_names, index_col,\n')
        zplp__wiesi += '                            ' + str(lgpny__ttyqd
            ) + ',\n'
        zplp__wiesi += (
            '                            unicode_to_utf8(metadata),\n')
        zplp__wiesi += (
            '                            unicode_to_utf8(compression),\n')
        zplp__wiesi += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        zplp__wiesi += (
            '                            unicode_to_utf8(name_ptr),\n')
        zplp__wiesi += (
            '                            unicode_to_utf8(bucket_region),\n')
        zplp__wiesi += '                            row_group_size)\n'
        zplp__wiesi += '    delete_table_decref_arrays(table)\n'
        zplp__wiesi += '    delete_info_decref_array(index_col)\n'
        zplp__wiesi += '    delete_info_decref_array(col_names)\n'
    gom__ngvx = {}
    if df.has_runtime_cols:
        hzkc__motaw = None
    else:
        for agj__qiqsz in df.columns:
            if not isinstance(agj__qiqsz, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        hzkc__motaw = pd.array(df.columns)
    exec(zplp__wiesi, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': hzkc__motaw,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': hndj__gie, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, gom__ngvx)
    qvkhp__tmvq = gom__ngvx['df_to_parquet']
    return qvkhp__tmvq


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    zwohu__rku = 'all_ok'
    vexqw__wpc = urlparse(con)
    dhd__nxwm = vexqw__wpc.scheme
    if _is_parallel and bodo.get_rank() == 0:
        roj__wkk = 100
        if chunksize is None:
            azqmv__jdbjf = roj__wkk
        else:
            azqmv__jdbjf = min(chunksize, roj__wkk)
        if _is_table_create:
            df = df.iloc[:azqmv__jdbjf, :]
        else:
            df = df.iloc[azqmv__jdbjf:, :]
            if len(df) == 0:
                return zwohu__rku
    zwba__izgd = df.columns
    try:
        if dhd__nxwm == 'snowflake':
            oeonz__nrycx = vexqw__wpc.password
            if oeonz__nrycx and con.count(oeonz__nrycx) == 1:
                con = con.replace(oeonz__nrycx, quote(oeonz__nrycx))
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
                df.columns = [(wbbk__qatve.upper() if wbbk__qatve.islower()
                     else wbbk__qatve) for wbbk__qatve in df.columns]
            except ImportError as nevzx__beitq:
                zwohu__rku = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return zwohu__rku
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as jqb__beam:
            zwohu__rku = jqb__beam.args[0]
        return zwohu__rku
    finally:
        df.columns = zwba__izgd


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
        ksjb__lzzbb = bodo.libs.distributed_api.get_rank()
        zwohu__rku = 'unset'
        if ksjb__lzzbb != 0:
            zwohu__rku = bcast_scalar(zwohu__rku)
        elif ksjb__lzzbb == 0:
            zwohu__rku = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, True, _is_parallel)
            zwohu__rku = bcast_scalar(zwohu__rku)
        if_exists = 'append'
        if _is_parallel and zwohu__rku == 'all_ok':
            zwohu__rku = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, False, _is_parallel)
        if zwohu__rku != 'all_ok':
            print('err_msg=', zwohu__rku)
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
        tly__egdsu = get_overload_const_str(path_or_buf)
        if tly__egdsu.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        xqv__cmog = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(xqv__cmog))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(xqv__cmog))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    zpgx__ndydh = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    bler__wlrba = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', zpgx__ndydh, bler__wlrba,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    zplp__wiesi = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        dwtj__ahgdc = data.data.dtype.categories
        zplp__wiesi += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        dwtj__ahgdc = data.dtype.categories
        zplp__wiesi += '  data_values = data\n'
    aqr__xxeut = len(dwtj__ahgdc)
    zplp__wiesi += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    zplp__wiesi += '  numba.parfors.parfor.init_prange()\n'
    zplp__wiesi += '  n = len(data_values)\n'
    for i in range(aqr__xxeut):
        zplp__wiesi += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    zplp__wiesi += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    zplp__wiesi += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for gvfp__rdsma in range(aqr__xxeut):
        zplp__wiesi += '          data_arr_{}[i] = 0\n'.format(gvfp__rdsma)
    zplp__wiesi += '      else:\n'
    for iezho__rsb in range(aqr__xxeut):
        zplp__wiesi += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            iezho__rsb)
    dwj__mqu = ', '.join(f'data_arr_{i}' for i in range(aqr__xxeut))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(dwtj__ahgdc[0], np.datetime64):
        dwtj__ahgdc = tuple(pd.Timestamp(wbbk__qatve) for wbbk__qatve in
            dwtj__ahgdc)
    elif isinstance(dwtj__ahgdc[0], np.timedelta64):
        dwtj__ahgdc = tuple(pd.Timedelta(wbbk__qatve) for wbbk__qatve in
            dwtj__ahgdc)
    return bodo.hiframes.dataframe_impl._gen_init_df(zplp__wiesi,
        dwtj__ahgdc, dwj__mqu, index)


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
    for tboy__uhr in pd_unsupported:
        oxi__rnrzz = mod_name + '.' + tboy__uhr.__name__
        overload(tboy__uhr, no_unliteral=True)(create_unsupported_overload(
            oxi__rnrzz))


def _install_dataframe_unsupported():
    for gfii__ylg in dataframe_unsupported_attrs:
        osxi__mbldv = 'DataFrame.' + gfii__ylg
        overload_attribute(DataFrameType, gfii__ylg)(
            create_unsupported_overload(osxi__mbldv))
    for oxi__rnrzz in dataframe_unsupported:
        osxi__mbldv = 'DataFrame.' + oxi__rnrzz + '()'
        overload_method(DataFrameType, oxi__rnrzz)(create_unsupported_overload
            (osxi__mbldv))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
