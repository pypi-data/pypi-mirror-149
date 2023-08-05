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
            ttvhf__bdq = f'{len(self.data)} columns of types {set(self.data)}'
            fcr__hqf = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({ttvhf__bdq}, {self.index}, {fcr__hqf}, {self.dist}, {self.is_table_format})'
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
            fhksl__qhyt = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            data = tuple(bvjwi__oswh.unify(typingctx, pulls__tuyp) if 
                bvjwi__oswh != pulls__tuyp else bvjwi__oswh for bvjwi__oswh,
                pulls__tuyp in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if fhksl__qhyt is not None and None not in data:
                return DataFrameType(data, fhksl__qhyt, self.columns, dist,
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
        return all(bvjwi__oswh.is_precise() for bvjwi__oswh in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        ogw__crop = self.columns.index(col_name)
        xct__ysfob = tuple(list(self.data[:ogw__crop]) + [new_type] + list(
            self.data[ogw__crop + 1:]))
        return DataFrameType(xct__ysfob, self.index, self.columns, self.
            dist, self.is_table_format)


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
        rkyf__qzdz = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            rkyf__qzdz.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, rkyf__qzdz)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        rkyf__qzdz = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, rkyf__qzdz)


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
        whceh__sqv = 'n',
        seq__enekw = {'n': 5}
        xpc__gbavy, indtd__xvce = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, whceh__sqv, seq__enekw)
        zgems__qersq = indtd__xvce[0]
        if not is_overload_int(zgems__qersq):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        myn__uhdza = df.copy(is_table_format=False)
        return myn__uhdza(*indtd__xvce).replace(pysig=xpc__gbavy)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        jvdf__wjcac = (df,) + args
        whceh__sqv = 'df', 'method', 'min_periods'
        seq__enekw = {'method': 'pearson', 'min_periods': 1}
        xnv__ozuow = 'method',
        xpc__gbavy, indtd__xvce = bodo.utils.typing.fold_typing_args(func_name,
            jvdf__wjcac, kws, whceh__sqv, seq__enekw, xnv__ozuow)
        zxwrp__nnyhl = indtd__xvce[2]
        if not is_overload_int(zxwrp__nnyhl):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        whjcb__fnkl = []
        whn__uawm = []
        for ylva__vjlc, pho__yhpl in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(pho__yhpl.dtype):
                whjcb__fnkl.append(ylva__vjlc)
                whn__uawm.append(types.Array(types.float64, 1, 'A'))
        if len(whjcb__fnkl) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        whn__uawm = tuple(whn__uawm)
        whjcb__fnkl = tuple(whjcb__fnkl)
        index_typ = bodo.utils.typing.type_col_to_index(whjcb__fnkl)
        myn__uhdza = DataFrameType(whn__uawm, index_typ, whjcb__fnkl)
        return myn__uhdza(*indtd__xvce).replace(pysig=xpc__gbavy)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        qvyod__ric = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        ufcob__skblf = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        qswox__zltn = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        hzkj__kqmoo = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        nlwy__kcbw = dict(raw=ufcob__skblf, result_type=qswox__zltn)
        rvxgq__ryb = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', nlwy__kcbw, rvxgq__ryb,
            package_name='pandas', module_name='DataFrame')
        omdj__dzv = True
        if types.unliteral(qvyod__ric) == types.unicode_type:
            if not is_overload_constant_str(qvyod__ric):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            omdj__dzv = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        fdaix__say = get_overload_const_int(axis)
        if omdj__dzv and fdaix__say != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif fdaix__say not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        ynst__vnl = []
        for arr_typ in df.data:
            dyf__mmd = SeriesType(arr_typ.dtype, arr_typ, df.index, string_type
                )
            eumz__tqtkh = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(dyf__mmd), types.int64), {}
                ).return_type
            ynst__vnl.append(eumz__tqtkh)
        lhbze__zyn = types.none
        jpy__snwo = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(ylva__vjlc) for ylva__vjlc in df.columns)), None)
        dnb__hllb = types.BaseTuple.from_types(ynst__vnl)
        cup__zmkob = types.Tuple([types.bool_] * len(dnb__hllb))
        omfc__hjgx = bodo.NullableTupleType(dnb__hllb, cup__zmkob)
        ysvw__tcyg = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if ysvw__tcyg == types.NPDatetime('ns'):
            ysvw__tcyg = bodo.pd_timestamp_type
        if ysvw__tcyg == types.NPTimedelta('ns'):
            ysvw__tcyg = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(dnb__hllb):
            ltj__okoi = HeterogeneousSeriesType(omfc__hjgx, jpy__snwo,
                ysvw__tcyg)
        else:
            ltj__okoi = SeriesType(dnb__hllb.dtype, omfc__hjgx, jpy__snwo,
                ysvw__tcyg)
        zqcpw__kjo = ltj__okoi,
        if hzkj__kqmoo is not None:
            zqcpw__kjo += tuple(hzkj__kqmoo.types)
        try:
            if not omdj__dzv:
                xhtov__ttp = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(qvyod__ric), self.context,
                    'DataFrame.apply', axis if fdaix__say == 1 else None)
            else:
                xhtov__ttp = get_const_func_output_type(qvyod__ric,
                    zqcpw__kjo, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as hre__vyyle:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()', hre__vyyle)
                )
        if omdj__dzv:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(xhtov__ttp, (SeriesType, HeterogeneousSeriesType)
                ) and xhtov__ttp.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(xhtov__ttp, HeterogeneousSeriesType):
                nxjfp__vaa, pwzsb__vbijj = xhtov__ttp.const_info
                if isinstance(xhtov__ttp.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    xens__wjio = xhtov__ttp.data.tuple_typ.types
                elif isinstance(xhtov__ttp.data, types.Tuple):
                    xens__wjio = xhtov__ttp.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                zwdwg__uhne = tuple(to_nullable_type(dtype_to_array_type(
                    ozp__gmt)) for ozp__gmt in xens__wjio)
                gzs__hbfc = DataFrameType(zwdwg__uhne, df.index, pwzsb__vbijj)
            elif isinstance(xhtov__ttp, SeriesType):
                zorit__zexiy, pwzsb__vbijj = xhtov__ttp.const_info
                zwdwg__uhne = tuple(to_nullable_type(dtype_to_array_type(
                    xhtov__ttp.dtype)) for nxjfp__vaa in range(zorit__zexiy))
                gzs__hbfc = DataFrameType(zwdwg__uhne, df.index, pwzsb__vbijj)
            else:
                tytax__rzy = get_udf_out_arr_type(xhtov__ttp)
                gzs__hbfc = SeriesType(tytax__rzy.dtype, tytax__rzy, df.
                    index, None)
        else:
            gzs__hbfc = xhtov__ttp
        usu__xkeic = ', '.join("{} = ''".format(bvjwi__oswh) for
            bvjwi__oswh in kws.keys())
        thr__urxa = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {usu__xkeic}):
"""
        thr__urxa += '    pass\n'
        ytg__sonj = {}
        exec(thr__urxa, {}, ytg__sonj)
        pfifl__azqjh = ytg__sonj['apply_stub']
        xpc__gbavy = numba.core.utils.pysignature(pfifl__azqjh)
        gav__lfxg = (qvyod__ric, axis, ufcob__skblf, qswox__zltn, hzkj__kqmoo
            ) + tuple(kws.values())
        return signature(gzs__hbfc, *gav__lfxg).replace(pysig=xpc__gbavy)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        whceh__sqv = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        seq__enekw = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        xnv__ozuow = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        xpc__gbavy, indtd__xvce = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, whceh__sqv, seq__enekw, xnv__ozuow)
        niuzy__vyqmz = indtd__xvce[2]
        if not is_overload_constant_str(niuzy__vyqmz):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        zwpq__yzwyw = indtd__xvce[0]
        if not is_overload_none(zwpq__yzwyw) and not (is_overload_int(
            zwpq__yzwyw) or is_overload_constant_str(zwpq__yzwyw)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(zwpq__yzwyw):
            rgic__gmq = get_overload_const_str(zwpq__yzwyw)
            if rgic__gmq not in df.columns:
                raise BodoError(f'{func_name}: {rgic__gmq} column not found.')
        elif is_overload_int(zwpq__yzwyw):
            lhuzc__wmri = get_overload_const_int(zwpq__yzwyw)
            if lhuzc__wmri > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {lhuzc__wmri} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            zwpq__yzwyw = df.columns[zwpq__yzwyw]
        gqcn__yoo = indtd__xvce[1]
        if not is_overload_none(gqcn__yoo) and not (is_overload_int(
            gqcn__yoo) or is_overload_constant_str(gqcn__yoo)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(gqcn__yoo):
            cnp__lwuam = get_overload_const_str(gqcn__yoo)
            if cnp__lwuam not in df.columns:
                raise BodoError(f'{func_name}: {cnp__lwuam} column not found.')
        elif is_overload_int(gqcn__yoo):
            rxfx__ycfv = get_overload_const_int(gqcn__yoo)
            if rxfx__ycfv > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {rxfx__ycfv} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            gqcn__yoo = df.columns[gqcn__yoo]
        guj__uay = indtd__xvce[3]
        if not is_overload_none(guj__uay) and not is_tuple_like_type(guj__uay):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        alqjb__hpg = indtd__xvce[10]
        if not is_overload_none(alqjb__hpg) and not is_overload_constant_str(
            alqjb__hpg):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        dezrk__msgff = indtd__xvce[12]
        if not is_overload_bool(dezrk__msgff):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        upbg__sum = indtd__xvce[17]
        if not is_overload_none(upbg__sum) and not is_tuple_like_type(upbg__sum
            ):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        nsnz__qzdb = indtd__xvce[18]
        if not is_overload_none(nsnz__qzdb) and not is_tuple_like_type(
            nsnz__qzdb):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        ibha__qzcw = indtd__xvce[22]
        if not is_overload_none(ibha__qzcw) and not is_overload_int(ibha__qzcw
            ):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        irdb__zsbzn = indtd__xvce[29]
        if not is_overload_none(irdb__zsbzn) and not is_overload_constant_str(
            irdb__zsbzn):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        qzl__mmif = indtd__xvce[30]
        if not is_overload_none(qzl__mmif) and not is_overload_constant_str(
            qzl__mmif):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        pwij__iens = types.List(types.mpl_line_2d_type)
        niuzy__vyqmz = get_overload_const_str(niuzy__vyqmz)
        if niuzy__vyqmz == 'scatter':
            if is_overload_none(zwpq__yzwyw) and is_overload_none(gqcn__yoo):
                raise BodoError(
                    f'{func_name}: {niuzy__vyqmz} requires an x and y column.')
            elif is_overload_none(zwpq__yzwyw):
                raise BodoError(
                    f'{func_name}: {niuzy__vyqmz} x column is missing.')
            elif is_overload_none(gqcn__yoo):
                raise BodoError(
                    f'{func_name}: {niuzy__vyqmz} y column is missing.')
            pwij__iens = types.mpl_path_collection_type
        elif niuzy__vyqmz != 'line':
            raise BodoError(
                f'{func_name}: {niuzy__vyqmz} plot is not supported.')
        return signature(pwij__iens, *indtd__xvce).replace(pysig=xpc__gbavy)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            iyjg__kerr = df.columns.index(attr)
            arr_typ = df.data[iyjg__kerr]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            jty__fkvxa = []
            xct__ysfob = []
            dkct__mgn = False
            for i, jjs__leh in enumerate(df.columns):
                if jjs__leh[0] != attr:
                    continue
                dkct__mgn = True
                jty__fkvxa.append(jjs__leh[1] if len(jjs__leh) == 2 else
                    jjs__leh[1:])
                xct__ysfob.append(df.data[i])
            if dkct__mgn:
                return DataFrameType(tuple(xct__ysfob), df.index, tuple(
                    jty__fkvxa))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        cqbqo__fudal = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(cqbqo__fudal)
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
        cfr__cfrjs = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], cfr__cfrjs)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    xrigj__wiw = builder.module
    itftv__ilde = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    mpuez__qyhsj = cgutils.get_or_insert_function(xrigj__wiw, itftv__ilde,
        name='.dtor.df.{}'.format(df_type))
    if not mpuez__qyhsj.is_declaration:
        return mpuez__qyhsj
    mpuez__qyhsj.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(mpuez__qyhsj.append_basic_block())
    tkqz__ccv = mpuez__qyhsj.args[0]
    mjdu__jeihx = context.get_value_type(payload_type).as_pointer()
    uropz__hvbt = builder.bitcast(tkqz__ccv, mjdu__jeihx)
    payload = context.make_helper(builder, payload_type, ref=uropz__hvbt)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        dngp__pgj = context.get_python_api(builder)
        xttcw__znlr = dngp__pgj.gil_ensure()
        dngp__pgj.decref(payload.parent)
        dngp__pgj.gil_release(xttcw__znlr)
    builder.ret_void()
    return mpuez__qyhsj


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    nmhmr__bkjn = cgutils.create_struct_proxy(payload_type)(context, builder)
    nmhmr__bkjn.data = data_tup
    nmhmr__bkjn.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        nmhmr__bkjn.columns = colnames
    psffa__htm = context.get_value_type(payload_type)
    jqn__ehsfb = context.get_abi_sizeof(psffa__htm)
    ultkz__jaxba = define_df_dtor(context, builder, df_type, payload_type)
    vqk__qma = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, jqn__ehsfb), ultkz__jaxba)
    gkq__kyg = context.nrt.meminfo_data(builder, vqk__qma)
    spp__zbmf = builder.bitcast(gkq__kyg, psffa__htm.as_pointer())
    eqmef__ufk = cgutils.create_struct_proxy(df_type)(context, builder)
    eqmef__ufk.meminfo = vqk__qma
    if parent is None:
        eqmef__ufk.parent = cgutils.get_null_value(eqmef__ufk.parent.type)
    else:
        eqmef__ufk.parent = parent
        nmhmr__bkjn.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            dngp__pgj = context.get_python_api(builder)
            xttcw__znlr = dngp__pgj.gil_ensure()
            dngp__pgj.incref(parent)
            dngp__pgj.gil_release(xttcw__znlr)
    builder.store(nmhmr__bkjn._getvalue(), spp__zbmf)
    return eqmef__ufk._getvalue()


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
        zjqw__mgnbd = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype
            .arr_types)
    else:
        zjqw__mgnbd = [ozp__gmt for ozp__gmt in data_typ.dtype.arr_types]
    apyf__fmob = DataFrameType(tuple(zjqw__mgnbd + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        cow__bkl = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return cow__bkl
    sig = signature(apyf__fmob, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    zorit__zexiy = len(data_tup_typ.types)
    if zorit__zexiy == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if zorit__zexiy == 1 and isinstance(data_tup_typ.types[0], TableType):
        zorit__zexiy = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == zorit__zexiy, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    dyf__jzobt = data_tup_typ.types
    if zorit__zexiy != 0 and isinstance(data_tup_typ.types[0], TableType):
        dyf__jzobt = data_tup_typ.types[0].arr_types
        is_table_format = True
    apyf__fmob = DataFrameType(dyf__jzobt, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            ruvs__cihak = cgutils.create_struct_proxy(apyf__fmob.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = ruvs__cihak.parent
        cow__bkl = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return cow__bkl
    sig = signature(apyf__fmob, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        eqmef__ufk = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, eqmef__ufk.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        nmhmr__bkjn = get_dataframe_payload(context, builder, df_typ, args[0])
        fjxdm__pja = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[fjxdm__pja]
        if df_typ.is_table_format:
            ruvs__cihak = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(nmhmr__bkjn.data, 0))
            mhpbx__dlhu = df_typ.table_type.type_to_blk[arr_typ]
            xlbc__kpl = getattr(ruvs__cihak, f'block_{mhpbx__dlhu}')
            gpufq__aob = ListInstance(context, builder, types.List(arr_typ),
                xlbc__kpl)
            yhas__ofn = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[fjxdm__pja])
            cfr__cfrjs = gpufq__aob.getitem(yhas__ofn)
        else:
            cfr__cfrjs = builder.extract_value(nmhmr__bkjn.data, fjxdm__pja)
        prbv__srxf = cgutils.alloca_once_value(builder, cfr__cfrjs)
        oqjv__cspj = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, prbv__srxf, oqjv__cspj)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    vqk__qma = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, vqk__qma)
    mjdu__jeihx = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, mjdu__jeihx)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    apyf__fmob = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        apyf__fmob = types.Tuple([TableType(df_typ.data)])
    sig = signature(apyf__fmob, df_typ)

    def codegen(context, builder, signature, args):
        nmhmr__bkjn = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            nmhmr__bkjn.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        nmhmr__bkjn = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index,
            nmhmr__bkjn.index)
    apyf__fmob = df_typ.index
    sig = signature(apyf__fmob, df_typ)
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
        myn__uhdza = df.data[i]
        return myn__uhdza(*args)


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
        nmhmr__bkjn = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(nmhmr__bkjn.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        nmhmr__bkjn = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, nmhmr__bkjn.columns)
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
    dnb__hllb = self.typemap[data_tup.name]
    if any(is_tuple_like_type(ozp__gmt) for ozp__gmt in dnb__hllb.types):
        return None
    if equiv_set.has_shape(data_tup):
        lrdzq__bps = equiv_set.get_shape(data_tup)
        if len(lrdzq__bps) > 1:
            equiv_set.insert_equiv(*lrdzq__bps)
        if len(lrdzq__bps) > 0:
            jpy__snwo = self.typemap[index.name]
            if not isinstance(jpy__snwo, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(lrdzq__bps[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(lrdzq__bps[0], len(
                lrdzq__bps)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    bya__viqbh = args[0]
    data_types = self.typemap[bya__viqbh.name].data
    if any(is_tuple_like_type(ozp__gmt) for ozp__gmt in data_types):
        return None
    if equiv_set.has_shape(bya__viqbh):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            bya__viqbh)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    bya__viqbh = args[0]
    jpy__snwo = self.typemap[bya__viqbh.name].index
    if isinstance(jpy__snwo, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(bya__viqbh):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            bya__viqbh)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    bya__viqbh = args[0]
    if equiv_set.has_shape(bya__viqbh):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            bya__viqbh), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    bya__viqbh = args[0]
    if equiv_set.has_shape(bya__viqbh):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            bya__viqbh)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    fjxdm__pja = get_overload_const_int(c_ind_typ)
    if df_typ.data[fjxdm__pja] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        tbta__aevz, nxjfp__vaa, bua__oth = args
        nmhmr__bkjn = get_dataframe_payload(context, builder, df_typ,
            tbta__aevz)
        if df_typ.is_table_format:
            ruvs__cihak = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(nmhmr__bkjn.data, 0))
            mhpbx__dlhu = df_typ.table_type.type_to_blk[arr_typ]
            xlbc__kpl = getattr(ruvs__cihak, f'block_{mhpbx__dlhu}')
            gpufq__aob = ListInstance(context, builder, types.List(arr_typ),
                xlbc__kpl)
            yhas__ofn = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[fjxdm__pja])
            gpufq__aob.setitem(yhas__ofn, bua__oth, True)
        else:
            cfr__cfrjs = builder.extract_value(nmhmr__bkjn.data, fjxdm__pja)
            context.nrt.decref(builder, df_typ.data[fjxdm__pja], cfr__cfrjs)
            nmhmr__bkjn.data = builder.insert_value(nmhmr__bkjn.data,
                bua__oth, fjxdm__pja)
            context.nrt.incref(builder, arr_typ, bua__oth)
        eqmef__ufk = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=tbta__aevz)
        payload_type = DataFramePayloadType(df_typ)
        uropz__hvbt = context.nrt.meminfo_data(builder, eqmef__ufk.meminfo)
        mjdu__jeihx = context.get_value_type(payload_type).as_pointer()
        uropz__hvbt = builder.bitcast(uropz__hvbt, mjdu__jeihx)
        builder.store(nmhmr__bkjn._getvalue(), uropz__hvbt)
        return impl_ret_borrowed(context, builder, df_typ, tbta__aevz)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        cmg__fboad = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        enw__djjyi = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=cmg__fboad)
        tnhk__yhjfq = get_dataframe_payload(context, builder, df_typ,
            cmg__fboad)
        eqmef__ufk = construct_dataframe(context, builder, signature.
            return_type, tnhk__yhjfq.data, index_val, enw__djjyi.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), tnhk__yhjfq.data)
        return eqmef__ufk
    apyf__fmob = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(apyf__fmob, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    zorit__zexiy = len(df_type.columns)
    mxd__fsr = zorit__zexiy
    shnnu__ilwx = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    blyl__zlf = col_name not in df_type.columns
    fjxdm__pja = zorit__zexiy
    if blyl__zlf:
        shnnu__ilwx += arr_type,
        column_names += col_name,
        mxd__fsr += 1
    else:
        fjxdm__pja = df_type.columns.index(col_name)
        shnnu__ilwx = tuple(arr_type if i == fjxdm__pja else shnnu__ilwx[i] for
            i in range(zorit__zexiy))

    def codegen(context, builder, signature, args):
        tbta__aevz, nxjfp__vaa, bua__oth = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, tbta__aevz)
        aqeb__jvc = cgutils.create_struct_proxy(df_type)(context, builder,
            value=tbta__aevz)
        if df_type.is_table_format:
            ggze__bpusc = df_type.table_type
            hwtfh__yts = builder.extract_value(in_dataframe_payload.data, 0)
            izf__ogd = TableType(shnnu__ilwx)
            gsmc__ntz = set_table_data_codegen(context, builder,
                ggze__bpusc, hwtfh__yts, izf__ogd, arr_type, bua__oth,
                fjxdm__pja, blyl__zlf)
            data_tup = context.make_tuple(builder, types.Tuple([izf__ogd]),
                [gsmc__ntz])
        else:
            dyf__jzobt = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != fjxdm__pja else bua__oth) for i in range(
                zorit__zexiy)]
            if blyl__zlf:
                dyf__jzobt.append(bua__oth)
            for bya__viqbh, uybel__cpps in zip(dyf__jzobt, shnnu__ilwx):
                context.nrt.incref(builder, uybel__cpps, bya__viqbh)
            data_tup = context.make_tuple(builder, types.Tuple(shnnu__ilwx),
                dyf__jzobt)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        zrn__tzoaf = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, aqeb__jvc.parent, None)
        if not blyl__zlf and arr_type == df_type.data[fjxdm__pja]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            uropz__hvbt = context.nrt.meminfo_data(builder, aqeb__jvc.meminfo)
            mjdu__jeihx = context.get_value_type(payload_type).as_pointer()
            uropz__hvbt = builder.bitcast(uropz__hvbt, mjdu__jeihx)
            xhilw__lflk = get_dataframe_payload(context, builder, df_type,
                zrn__tzoaf)
            builder.store(xhilw__lflk._getvalue(), uropz__hvbt)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, izf__ogd, builder.extract_value
                    (data_tup, 0))
            else:
                for bya__viqbh, uybel__cpps in zip(dyf__jzobt, shnnu__ilwx):
                    context.nrt.incref(builder, uybel__cpps, bya__viqbh)
        has_parent = cgutils.is_not_null(builder, aqeb__jvc.parent)
        with builder.if_then(has_parent):
            dngp__pgj = context.get_python_api(builder)
            xttcw__znlr = dngp__pgj.gil_ensure()
            pdyrt__sgehe = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, bua__oth)
            ylva__vjlc = numba.core.pythonapi._BoxContext(context, builder,
                dngp__pgj, pdyrt__sgehe)
            vawp__zsw = ylva__vjlc.pyapi.from_native_value(arr_type,
                bua__oth, ylva__vjlc.env_manager)
            if isinstance(col_name, str):
                bdzh__mhf = context.insert_const_string(builder.module,
                    col_name)
                qaelz__zhsz = dngp__pgj.string_from_string(bdzh__mhf)
            else:
                assert isinstance(col_name, int)
                qaelz__zhsz = dngp__pgj.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            dngp__pgj.object_setitem(aqeb__jvc.parent, qaelz__zhsz, vawp__zsw)
            dngp__pgj.decref(vawp__zsw)
            dngp__pgj.decref(qaelz__zhsz)
            dngp__pgj.gil_release(xttcw__znlr)
        return zrn__tzoaf
    apyf__fmob = DataFrameType(shnnu__ilwx, index_typ, column_names,
        df_type.dist, df_type.is_table_format)
    sig = signature(apyf__fmob, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    zorit__zexiy = len(pyval.columns)
    dyf__jzobt = []
    for i in range(zorit__zexiy):
        gooq__mydr = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            vawp__zsw = gooq__mydr.array
        else:
            vawp__zsw = gooq__mydr.values
        dyf__jzobt.append(vawp__zsw)
    dyf__jzobt = tuple(dyf__jzobt)
    if df_type.is_table_format:
        ruvs__cihak = context.get_constant_generic(builder, df_type.
            table_type, Table(dyf__jzobt))
        data_tup = lir.Constant.literal_struct([ruvs__cihak])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], jjs__leh) for i,
            jjs__leh in enumerate(dyf__jzobt)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    ndgzm__wzk = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, ndgzm__wzk])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    kjye__xklp = context.get_constant(types.int64, -1)
    hsb__dwkbm = context.get_constant_null(types.voidptr)
    vqk__qma = lir.Constant.literal_struct([kjye__xklp, hsb__dwkbm,
        hsb__dwkbm, payload, kjye__xklp])
    vqk__qma = cgutils.global_constant(builder, '.const.meminfo', vqk__qma
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([vqk__qma, ndgzm__wzk])


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
        fhksl__qhyt = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        fhksl__qhyt = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, fhksl__qhyt)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        xct__ysfob = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                xct__ysfob)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), xct__ysfob)
    elif not fromty.is_table_format and toty.is_table_format:
        xct__ysfob = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        xct__ysfob = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        xct__ysfob = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        xct__ysfob = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, xct__ysfob,
        fhksl__qhyt, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    liu__samu = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        hhy__qaj = get_index_data_arr_types(toty.index)[0]
        kts__hakc = bodo.utils.transform.get_type_alloc_counts(hhy__qaj) - 1
        lsvio__yho = ', '.join('0' for nxjfp__vaa in range(kts__hakc))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(lsvio__yho, ', ' if kts__hakc == 1 else ''))
        liu__samu['index_arr_type'] = hhy__qaj
    hpjf__iukyb = []
    for i, arr_typ in enumerate(toty.data):
        kts__hakc = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        lsvio__yho = ', '.join('0' for nxjfp__vaa in range(kts__hakc))
        tfry__bgyx = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, lsvio__yho, ', ' if kts__hakc == 1 else ''))
        hpjf__iukyb.append(tfry__bgyx)
        liu__samu[f'arr_type{i}'] = arr_typ
    hpjf__iukyb = ', '.join(hpjf__iukyb)
    thr__urxa = 'def impl():\n'
    ncilu__webw = bodo.hiframes.dataframe_impl._gen_init_df(thr__urxa, toty
        .columns, hpjf__iukyb, index, liu__samu)
    df = context.compile_internal(builder, ncilu__webw, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    nae__pxt = toty.table_type
    ruvs__cihak = cgutils.create_struct_proxy(nae__pxt)(context, builder)
    ruvs__cihak.parent = in_dataframe_payload.parent
    for ozp__gmt, mhpbx__dlhu in nae__pxt.type_to_blk.items():
        ogqu__kabdt = context.get_constant(types.int64, len(nae__pxt.
            block_to_arr_ind[mhpbx__dlhu]))
        nxjfp__vaa, adrvp__vvv = ListInstance.allocate_ex(context, builder,
            types.List(ozp__gmt), ogqu__kabdt)
        adrvp__vvv.size = ogqu__kabdt
        setattr(ruvs__cihak, f'block_{mhpbx__dlhu}', adrvp__vvv.value)
    for i, ozp__gmt in enumerate(fromty.data):
        qowk__bbdxm = toty.data[i]
        if ozp__gmt != qowk__bbdxm:
            kqr__eocl = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*kqr__eocl)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        cfr__cfrjs = builder.extract_value(in_dataframe_payload.data, i)
        if ozp__gmt != qowk__bbdxm:
            jqdfn__wusc = context.cast(builder, cfr__cfrjs, ozp__gmt,
                qowk__bbdxm)
            iedea__cmmn = False
        else:
            jqdfn__wusc = cfr__cfrjs
            iedea__cmmn = True
        mhpbx__dlhu = nae__pxt.type_to_blk[ozp__gmt]
        xlbc__kpl = getattr(ruvs__cihak, f'block_{mhpbx__dlhu}')
        gpufq__aob = ListInstance(context, builder, types.List(ozp__gmt),
            xlbc__kpl)
        yhas__ofn = context.get_constant(types.int64, nae__pxt.block_offsets[i]
            )
        gpufq__aob.setitem(yhas__ofn, jqdfn__wusc, iedea__cmmn)
    data_tup = context.make_tuple(builder, types.Tuple([nae__pxt]), [
        ruvs__cihak._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    dyf__jzobt = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            kqr__eocl = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*kqr__eocl)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            cfr__cfrjs = builder.extract_value(in_dataframe_payload.data, i)
            jqdfn__wusc = context.cast(builder, cfr__cfrjs, fromty.data[i],
                toty.data[i])
            iedea__cmmn = False
        else:
            jqdfn__wusc = builder.extract_value(in_dataframe_payload.data, i)
            iedea__cmmn = True
        if iedea__cmmn:
            context.nrt.incref(builder, toty.data[i], jqdfn__wusc)
        dyf__jzobt.append(jqdfn__wusc)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), dyf__jzobt)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    ggze__bpusc = fromty.table_type
    hwtfh__yts = cgutils.create_struct_proxy(ggze__bpusc)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    izf__ogd = toty.table_type
    gsmc__ntz = cgutils.create_struct_proxy(izf__ogd)(context, builder)
    gsmc__ntz.parent = in_dataframe_payload.parent
    for ozp__gmt, mhpbx__dlhu in izf__ogd.type_to_blk.items():
        ogqu__kabdt = context.get_constant(types.int64, len(izf__ogd.
            block_to_arr_ind[mhpbx__dlhu]))
        nxjfp__vaa, adrvp__vvv = ListInstance.allocate_ex(context, builder,
            types.List(ozp__gmt), ogqu__kabdt)
        adrvp__vvv.size = ogqu__kabdt
        setattr(gsmc__ntz, f'block_{mhpbx__dlhu}', adrvp__vvv.value)
    for i in range(len(fromty.data)):
        fprxd__niob = fromty.data[i]
        qowk__bbdxm = toty.data[i]
        if fprxd__niob != qowk__bbdxm:
            kqr__eocl = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*kqr__eocl)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        pclga__cdg = ggze__bpusc.type_to_blk[fprxd__niob]
        vyxy__wbevi = getattr(hwtfh__yts, f'block_{pclga__cdg}')
        bfjfy__oiki = ListInstance(context, builder, types.List(fprxd__niob
            ), vyxy__wbevi)
        neobz__vzvuz = context.get_constant(types.int64, ggze__bpusc.
            block_offsets[i])
        cfr__cfrjs = bfjfy__oiki.getitem(neobz__vzvuz)
        if fprxd__niob != qowk__bbdxm:
            jqdfn__wusc = context.cast(builder, cfr__cfrjs, fprxd__niob,
                qowk__bbdxm)
            iedea__cmmn = False
        else:
            jqdfn__wusc = cfr__cfrjs
            iedea__cmmn = True
        yeq__sdzpi = izf__ogd.type_to_blk[ozp__gmt]
        adrvp__vvv = getattr(gsmc__ntz, f'block_{yeq__sdzpi}')
        ezzny__csks = ListInstance(context, builder, types.List(qowk__bbdxm
            ), adrvp__vvv)
        uhu__ywurl = context.get_constant(types.int64, izf__ogd.
            block_offsets[i])
        ezzny__csks.setitem(uhu__ywurl, jqdfn__wusc, iedea__cmmn)
    data_tup = context.make_tuple(builder, types.Tuple([izf__ogd]), [
        gsmc__ntz._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    nae__pxt = fromty.table_type
    ruvs__cihak = cgutils.create_struct_proxy(nae__pxt)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    dyf__jzobt = []
    for i, ozp__gmt in enumerate(toty.data):
        fprxd__niob = fromty.data[i]
        if ozp__gmt != fprxd__niob:
            kqr__eocl = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*kqr__eocl)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        mhpbx__dlhu = nae__pxt.type_to_blk[ozp__gmt]
        xlbc__kpl = getattr(ruvs__cihak, f'block_{mhpbx__dlhu}')
        gpufq__aob = ListInstance(context, builder, types.List(ozp__gmt),
            xlbc__kpl)
        yhas__ofn = context.get_constant(types.int64, nae__pxt.block_offsets[i]
            )
        cfr__cfrjs = gpufq__aob.getitem(yhas__ofn)
        if ozp__gmt != fprxd__niob:
            jqdfn__wusc = context.cast(builder, cfr__cfrjs, fprxd__niob,
                ozp__gmt)
            iedea__cmmn = False
        else:
            jqdfn__wusc = cfr__cfrjs
            iedea__cmmn = True
        if iedea__cmmn:
            context.nrt.incref(builder, ozp__gmt, jqdfn__wusc)
        dyf__jzobt.append(jqdfn__wusc)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), dyf__jzobt)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    pfb__bux, hpjf__iukyb, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    rhdsz__nqa = gen_const_tup(pfb__bux)
    thr__urxa = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    thr__urxa += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(hpjf__iukyb, index_arg, rhdsz__nqa))
    ytg__sonj = {}
    exec(thr__urxa, {'bodo': bodo, 'np': np}, ytg__sonj)
    gky__kxxav = ytg__sonj['_init_df']
    return gky__kxxav


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    apyf__fmob = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(apyf__fmob, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    apyf__fmob = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(apyf__fmob, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    ejf__bjjfq = ''
    if not is_overload_none(dtype):
        ejf__bjjfq = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        zorit__zexiy = (len(data.types) - 1) // 2
        bqmx__adyug = [ozp__gmt.literal_value for ozp__gmt in data.types[1:
            zorit__zexiy + 1]]
        data_val_types = dict(zip(bqmx__adyug, data.types[zorit__zexiy + 1:]))
        dyf__jzobt = ['data[{}]'.format(i) for i in range(zorit__zexiy + 1,
            2 * zorit__zexiy + 1)]
        data_dict = dict(zip(bqmx__adyug, dyf__jzobt))
        if is_overload_none(index):
            for i, ozp__gmt in enumerate(data.types[zorit__zexiy + 1:]):
                if isinstance(ozp__gmt, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(zorit__zexiy + 1 + i))
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
        ugs__nfidq = '.copy()' if copy else ''
        yrzjw__csmm = get_overload_const_list(columns)
        zorit__zexiy = len(yrzjw__csmm)
        data_val_types = {ylva__vjlc: data.copy(ndim=1) for ylva__vjlc in
            yrzjw__csmm}
        dyf__jzobt = ['data[:,{}]{}'.format(i, ugs__nfidq) for i in range(
            zorit__zexiy)]
        data_dict = dict(zip(yrzjw__csmm, dyf__jzobt))
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
    hpjf__iukyb = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[ylva__vjlc], df_len, ejf__bjjfq) for ylva__vjlc in
        col_names))
    if len(col_names) == 0:
        hpjf__iukyb = '()'
    return col_names, hpjf__iukyb, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for ylva__vjlc in col_names:
        if ylva__vjlc in data_dict and is_iterable_type(data_val_types[
            ylva__vjlc]):
            df_len = 'len({})'.format(data_dict[ylva__vjlc])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(ylva__vjlc in data_dict for ylva__vjlc in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    lomv__chmjp = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for ylva__vjlc in col_names:
        if ylva__vjlc not in data_dict:
            data_dict[ylva__vjlc] = lomv__chmjp


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
            ozp__gmt = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(ozp__gmt)
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
        vzaii__qqrr = idx.literal_value
        if isinstance(vzaii__qqrr, int):
            myn__uhdza = tup.types[vzaii__qqrr]
        elif isinstance(vzaii__qqrr, slice):
            myn__uhdza = types.BaseTuple.from_types(tup.types[vzaii__qqrr])
        return signature(myn__uhdza, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    cngo__xyr, idx = sig.args
    idx = idx.literal_value
    tup, nxjfp__vaa = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(cngo__xyr)
        if not 0 <= idx < len(cngo__xyr):
            raise IndexError('cannot index at %d in %s' % (idx, cngo__xyr))
        gyddb__htyez = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        gnwiu__xqgwy = cgutils.unpack_tuple(builder, tup)[idx]
        gyddb__htyez = context.make_tuple(builder, sig.return_type,
            gnwiu__xqgwy)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, gyddb__htyez)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, lxyhf__fdg, suffix_x,
            suffix_y, is_join, indicator, _bodo_na_equal, lxv__xly) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        sgtpi__utv = set(left_on) & set(right_on)
        jawxx__nsjb = set(left_df.columns) & set(right_df.columns)
        efosq__gvhhr = jawxx__nsjb - sgtpi__utv
        mtdqa__jlhg = '$_bodo_index_' in left_on
        kmhc__qlcle = '$_bodo_index_' in right_on
        how = get_overload_const_str(lxyhf__fdg)
        lhrv__run = how in {'left', 'outer'}
        yymex__udcv = how in {'right', 'outer'}
        columns = []
        data = []
        if mtdqa__jlhg:
            fco__xfo = bodo.utils.typing.get_index_data_arr_types(left_df.index
                )[0]
        else:
            fco__xfo = left_df.data[left_df.columns.index(left_on[0])]
        if kmhc__qlcle:
            qca__rtqdl = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            qca__rtqdl = right_df.data[right_df.columns.index(right_on[0])]
        if mtdqa__jlhg and not kmhc__qlcle and not is_join.literal_value:
            azlvz__fdj = right_on[0]
            if azlvz__fdj in left_df.columns:
                columns.append(azlvz__fdj)
                if (qca__rtqdl == bodo.dict_str_arr_type and fco__xfo ==
                    bodo.string_array_type):
                    yyjnw__iniu = bodo.string_array_type
                else:
                    yyjnw__iniu = qca__rtqdl
                data.append(yyjnw__iniu)
        if kmhc__qlcle and not mtdqa__jlhg and not is_join.literal_value:
            ctir__habih = left_on[0]
            if ctir__habih in right_df.columns:
                columns.append(ctir__habih)
                if (fco__xfo == bodo.dict_str_arr_type and qca__rtqdl ==
                    bodo.string_array_type):
                    yyjnw__iniu = bodo.string_array_type
                else:
                    yyjnw__iniu = fco__xfo
                data.append(yyjnw__iniu)
        for fprxd__niob, gooq__mydr in zip(left_df.data, left_df.columns):
            columns.append(str(gooq__mydr) + suffix_x.literal_value if 
                gooq__mydr in efosq__gvhhr else gooq__mydr)
            if gooq__mydr in sgtpi__utv:
                if fprxd__niob == bodo.dict_str_arr_type:
                    fprxd__niob = right_df.data[right_df.columns.index(
                        gooq__mydr)]
                data.append(fprxd__niob)
            else:
                if (fprxd__niob == bodo.dict_str_arr_type and gooq__mydr in
                    left_on):
                    if kmhc__qlcle:
                        fprxd__niob = qca__rtqdl
                    else:
                        jigzc__dbhms = left_on.index(gooq__mydr)
                        tlq__qtqst = right_on[jigzc__dbhms]
                        fprxd__niob = right_df.data[right_df.columns.index(
                            tlq__qtqst)]
                if yymex__udcv:
                    fprxd__niob = to_nullable_type(fprxd__niob)
                data.append(fprxd__niob)
        for fprxd__niob, gooq__mydr in zip(right_df.data, right_df.columns):
            if gooq__mydr not in sgtpi__utv:
                columns.append(str(gooq__mydr) + suffix_y.literal_value if 
                    gooq__mydr in efosq__gvhhr else gooq__mydr)
                if (fprxd__niob == bodo.dict_str_arr_type and gooq__mydr in
                    right_on):
                    if mtdqa__jlhg:
                        fprxd__niob = fco__xfo
                    else:
                        jigzc__dbhms = right_on.index(gooq__mydr)
                        yzpu__xzvp = left_on[jigzc__dbhms]
                        fprxd__niob = left_df.data[left_df.columns.index(
                            yzpu__xzvp)]
                if lhrv__run:
                    fprxd__niob = to_nullable_type(fprxd__niob)
                data.append(fprxd__niob)
        suxw__eqbsh = get_overload_const_bool(indicator)
        if suxw__eqbsh:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        if mtdqa__jlhg and kmhc__qlcle and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif mtdqa__jlhg and not kmhc__qlcle:
            index_typ = right_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif kmhc__qlcle and not mtdqa__jlhg:
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        jjugj__jctgn = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(jjugj__jctgn, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    eqmef__ufk = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return eqmef__ufk._getvalue()


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
    nlwy__kcbw = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    seq__enekw = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', nlwy__kcbw, seq__enekw,
        package_name='pandas', module_name='General')
    thr__urxa = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        xawrx__abfp = 0
        hpjf__iukyb = []
        names = []
        for i, lel__pgtxx in enumerate(objs.types):
            assert isinstance(lel__pgtxx, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(lel__pgtxx, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                lel__pgtxx, 'pandas.concat()')
            if isinstance(lel__pgtxx, SeriesType):
                names.append(str(xawrx__abfp))
                xawrx__abfp += 1
                hpjf__iukyb.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(lel__pgtxx.columns)
                for qpbho__kkd in range(len(lel__pgtxx.data)):
                    hpjf__iukyb.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, qpbho__kkd))
        return bodo.hiframes.dataframe_impl._gen_init_df(thr__urxa, names,
            ', '.join(hpjf__iukyb), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(ozp__gmt, DataFrameType) for ozp__gmt in objs
            .types)
        iggkw__usrm = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            iggkw__usrm.extend(df.columns)
        iggkw__usrm = list(dict.fromkeys(iggkw__usrm).keys())
        zjqw__mgnbd = {}
        for xawrx__abfp, ylva__vjlc in enumerate(iggkw__usrm):
            for df in objs.types:
                if ylva__vjlc in df.columns:
                    zjqw__mgnbd['arr_typ{}'.format(xawrx__abfp)] = df.data[df
                        .columns.index(ylva__vjlc)]
                    break
        assert len(zjqw__mgnbd) == len(iggkw__usrm)
        vyw__xgrtb = []
        for xawrx__abfp, ylva__vjlc in enumerate(iggkw__usrm):
            args = []
            for i, df in enumerate(objs.types):
                if ylva__vjlc in df.columns:
                    fjxdm__pja = df.columns.index(ylva__vjlc)
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, fjxdm__pja))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, xawrx__abfp))
            thr__urxa += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(xawrx__abfp, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(thr__urxa,
            iggkw__usrm, ', '.join('A{}'.format(i) for i in range(len(
            iggkw__usrm))), index, zjqw__mgnbd)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(ozp__gmt, SeriesType) for ozp__gmt in objs.types)
        thr__urxa += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            thr__urxa += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            thr__urxa += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        thr__urxa += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        ytg__sonj = {}
        exec(thr__urxa, {'bodo': bodo, 'np': np, 'numba': numba}, ytg__sonj)
        return ytg__sonj['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for xawrx__abfp, ylva__vjlc in enumerate(df_type.columns):
            thr__urxa += '  arrs{} = []\n'.format(xawrx__abfp)
            thr__urxa += '  for i in range(len(objs)):\n'
            thr__urxa += '    df = objs[i]\n'
            thr__urxa += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(xawrx__abfp))
            thr__urxa += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(xawrx__abfp))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            thr__urxa += '  arrs_index = []\n'
            thr__urxa += '  for i in range(len(objs)):\n'
            thr__urxa += '    df = objs[i]\n'
            thr__urxa += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(thr__urxa, df_type
            .columns, ', '.join('out_arr{}'.format(i) for i in range(len(
            df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        thr__urxa += '  arrs = []\n'
        thr__urxa += '  for i in range(len(objs)):\n'
        thr__urxa += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        thr__urxa += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            thr__urxa += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            thr__urxa += '  arrs_index = []\n'
            thr__urxa += '  for i in range(len(objs)):\n'
            thr__urxa += '    S = objs[i]\n'
            thr__urxa += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            thr__urxa += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        thr__urxa += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        ytg__sonj = {}
        exec(thr__urxa, {'bodo': bodo, 'np': np, 'numba': numba}, ytg__sonj)
        return ytg__sonj['impl']
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
        apyf__fmob = df.copy(index=index, is_table_format=False)
        return signature(apyf__fmob, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    unwx__vny = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return unwx__vny._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    nlwy__kcbw = dict(index=index, name=name)
    seq__enekw = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', nlwy__kcbw, seq__enekw,
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
        zjqw__mgnbd = (types.Array(types.int64, 1, 'C'),) + df.data
        ixxi__dejum = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, zjqw__mgnbd)
        return signature(ixxi__dejum, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    unwx__vny = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return unwx__vny._getvalue()


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
    unwx__vny = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return unwx__vny._getvalue()


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
    unwx__vny = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return unwx__vny._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    wejq__avg = get_overload_const_bool(check_duplicates)
    ujto__gxpa = not is_overload_none(value_names)
    imkhf__dxbw = isinstance(values_tup, types.UniTuple)
    if imkhf__dxbw:
        jdbub__ahr = [to_nullable_type(values_tup.dtype)]
    else:
        jdbub__ahr = [to_nullable_type(uybel__cpps) for uybel__cpps in
            values_tup]
    thr__urxa = 'def impl(\n'
    thr__urxa += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    thr__urxa += '):\n'
    thr__urxa += '    if parallel:\n'
    rab__xqy = ', '.join([f'array_to_info(index_tup[{i}])' for i in range(
        len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    thr__urxa += f'        info_list = [{rab__xqy}]\n'
    thr__urxa += '        cpp_table = arr_info_list_to_table(info_list)\n'
    thr__urxa += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
    prxhe__zto = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    wedn__llxnf = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    ukb__qkmrd = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    thr__urxa += f'        index_tup = ({prxhe__zto},)\n'
    thr__urxa += f'        columns_tup = ({wedn__llxnf},)\n'
    thr__urxa += f'        values_tup = ({ukb__qkmrd},)\n'
    thr__urxa += '        delete_table(cpp_table)\n'
    thr__urxa += '        delete_table(out_cpp_table)\n'
    thr__urxa += '    columns_arr = columns_tup[0]\n'
    if imkhf__dxbw:
        thr__urxa += '    values_arrs = [arr for arr in values_tup]\n'
    thr__urxa += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    thr__urxa += '        index_tup\n'
    thr__urxa += '    )\n'
    thr__urxa += '    n_rows = len(unique_index_arr_tup[0])\n'
    thr__urxa += '    num_values_arrays = len(values_tup)\n'
    thr__urxa += '    n_unique_pivots = len(pivot_values)\n'
    if imkhf__dxbw:
        thr__urxa += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        thr__urxa += '    n_cols = n_unique_pivots\n'
    thr__urxa += '    col_map = {}\n'
    thr__urxa += '    for i in range(n_unique_pivots):\n'
    thr__urxa += '        if bodo.libs.array_kernels.isna(pivot_values, i):\n'
    thr__urxa += '            raise ValueError(\n'
    thr__urxa += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    thr__urxa += '            )\n'
    thr__urxa += '        col_map[pivot_values[i]] = i\n'
    vxnty__amqci = False
    for i, gyyun__nnck in enumerate(jdbub__ahr):
        if is_str_arr_type(gyyun__nnck):
            vxnty__amqci = True
            thr__urxa += (
                f'    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]\n'
                )
            thr__urxa += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if vxnty__amqci:
        if wejq__avg:
            thr__urxa += '    nbytes = (n_rows + 7) >> 3\n'
            thr__urxa += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        thr__urxa += '    for i in range(len(columns_arr)):\n'
        thr__urxa += '        col_name = columns_arr[i]\n'
        thr__urxa += '        pivot_idx = col_map[col_name]\n'
        thr__urxa += '        row_idx = row_vector[i]\n'
        if wejq__avg:
            thr__urxa += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            thr__urxa += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            thr__urxa += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            thr__urxa += '        else:\n'
            thr__urxa += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if imkhf__dxbw:
            thr__urxa += '        for j in range(num_values_arrays):\n'
            thr__urxa += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            thr__urxa += '            len_arr = len_arrs_0[col_idx]\n'
            thr__urxa += '            values_arr = values_arrs[j]\n'
            thr__urxa += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            thr__urxa += (
                '                len_arr[row_idx] = len(values_arr[i])\n')
            thr__urxa += (
                '                total_lens_0[col_idx] += len(values_arr[i])\n'
                )
        else:
            for i, gyyun__nnck in enumerate(jdbub__ahr):
                if is_str_arr_type(gyyun__nnck):
                    thr__urxa += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    thr__urxa += f"""            len_arrs_{i}[pivot_idx][row_idx] = len(values_tup[{i}][i])
"""
                    thr__urxa += f"""            total_lens_{i}[pivot_idx] += len(values_tup[{i}][i])
"""
    for i, gyyun__nnck in enumerate(jdbub__ahr):
        if is_str_arr_type(gyyun__nnck):
            thr__urxa += f'    data_arrs_{i} = [\n'
            thr__urxa += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            thr__urxa += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            thr__urxa += '        )\n'
            thr__urxa += '        for i in range(n_cols)\n'
            thr__urxa += '    ]\n'
        else:
            thr__urxa += f'    data_arrs_{i} = [\n'
            thr__urxa += (
                f'        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})\n'
                )
            thr__urxa += '        for _ in range(n_cols)\n'
            thr__urxa += '    ]\n'
    if not vxnty__amqci and wejq__avg:
        thr__urxa += '    nbytes = (n_rows + 7) >> 3\n'
        thr__urxa += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    thr__urxa += '    for i in range(len(columns_arr)):\n'
    thr__urxa += '        col_name = columns_arr[i]\n'
    thr__urxa += '        pivot_idx = col_map[col_name]\n'
    thr__urxa += '        row_idx = row_vector[i]\n'
    if not vxnty__amqci and wejq__avg:
        thr__urxa += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        thr__urxa += (
            '        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):\n'
            )
        thr__urxa += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        thr__urxa += '        else:\n'
        thr__urxa += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)\n'
            )
    if imkhf__dxbw:
        thr__urxa += '        for j in range(num_values_arrays):\n'
        thr__urxa += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        thr__urxa += '            col_arr = data_arrs_0[col_idx]\n'
        thr__urxa += '            values_arr = values_arrs[j]\n'
        thr__urxa += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        thr__urxa += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        thr__urxa += '            else:\n'
        thr__urxa += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, gyyun__nnck in enumerate(jdbub__ahr):
            thr__urxa += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            thr__urxa += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            thr__urxa += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            thr__urxa += f'        else:\n'
            thr__urxa += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        thr__urxa += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        thr__urxa += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if ujto__gxpa:
        thr__urxa += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            thr__urxa += '    total_chars = 0\n'
            thr__urxa += '    for i in range(len(value_names)):\n'
            thr__urxa += '        total_chars += len(value_names[i])\n'
            thr__urxa += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            thr__urxa += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            thr__urxa += '    total_chars = 0\n'
            thr__urxa += '    for i in range(len(pivot_values)):\n'
            thr__urxa += '        total_chars += len(pivot_values[i])\n'
            thr__urxa += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            thr__urxa += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        thr__urxa += '    for i in range(len(value_names)):\n'
        thr__urxa += '        for j in range(len(pivot_values)):\n'
        thr__urxa += (
            '            new_value_names[(i * len(pivot_values)) + j] = value_names[i]\n'
            )
        thr__urxa += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        thr__urxa += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        thr__urxa += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    pdskr__aijg = ', '.join(f'data_arrs_{i}' for i in range(len(jdbub__ahr)))
    thr__urxa += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({pdskr__aijg},), n_rows)
"""
    thr__urxa += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    thr__urxa += '        (table,), index, column_index\n'
    thr__urxa += '    )\n'
    ytg__sonj = {}
    cfsxx__vcr = {f'data_arr_typ_{i}': gyyun__nnck for i, gyyun__nnck in
        enumerate(jdbub__ahr)}
    espb__rlz = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **cfsxx__vcr}
    exec(thr__urxa, espb__rlz, ytg__sonj)
    impl = ytg__sonj['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    fyr__prqv = {}
    fyr__prqv['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, kuc__qpza in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        yuv__peqnp = None
        if isinstance(kuc__qpza, bodo.DatetimeArrayType):
            btv__vdbl = 'datetimetz'
            iozg__naf = 'datetime64[ns]'
            if isinstance(kuc__qpza.tz, int):
                azmei__hytma = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(kuc__qpza.tz))
            else:
                azmei__hytma = pd.DatetimeTZDtype(tz=kuc__qpza.tz).tz
            yuv__peqnp = {'timezone': pa.lib.tzinfo_to_string(azmei__hytma)}
        elif isinstance(kuc__qpza, types.Array) or kuc__qpza == boolean_array:
            btv__vdbl = iozg__naf = kuc__qpza.dtype.name
            if iozg__naf.startswith('datetime'):
                btv__vdbl = 'datetime'
        elif is_str_arr_type(kuc__qpza):
            btv__vdbl = 'unicode'
            iozg__naf = 'object'
        elif kuc__qpza == binary_array_type:
            btv__vdbl = 'bytes'
            iozg__naf = 'object'
        elif isinstance(kuc__qpza, DecimalArrayType):
            btv__vdbl = iozg__naf = 'object'
        elif isinstance(kuc__qpza, IntegerArrayType):
            ymq__pgqit = kuc__qpza.dtype.name
            if ymq__pgqit.startswith('int'):
                btv__vdbl = 'Int' + ymq__pgqit[3:]
            elif ymq__pgqit.startswith('uint'):
                btv__vdbl = 'UInt' + ymq__pgqit[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, kuc__qpza))
            iozg__naf = kuc__qpza.dtype.name
        elif kuc__qpza == datetime_date_array_type:
            btv__vdbl = 'datetime'
            iozg__naf = 'object'
        elif isinstance(kuc__qpza, (StructArrayType, ArrayItemArrayType)):
            btv__vdbl = 'object'
            iozg__naf = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, kuc__qpza))
        kffs__svldp = {'name': col_name, 'field_name': col_name,
            'pandas_type': btv__vdbl, 'numpy_type': iozg__naf, 'metadata':
            yuv__peqnp}
        fyr__prqv['columns'].append(kffs__svldp)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            tjetm__vps = '__index_level_0__'
            gjx__quf = None
        else:
            tjetm__vps = '%s'
            gjx__quf = '%s'
        fyr__prqv['index_columns'] = [tjetm__vps]
        fyr__prqv['columns'].append({'name': gjx__quf, 'field_name':
            tjetm__vps, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        fyr__prqv['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        fyr__prqv['index_columns'] = []
    fyr__prqv['pandas_version'] = pd.__version__
    return fyr__prqv


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
        fxd__ejo = []
        for ucsme__ppurv in partition_cols:
            try:
                idx = df.columns.index(ucsme__ppurv)
            except ValueError as soy__cjqa:
                raise BodoError(
                    f'Partition column {ucsme__ppurv} is not in dataframe')
            fxd__ejo.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    jpbd__nxx = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType)
    hpbar__bbji = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not jpbd__nxx)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not jpbd__nxx or is_overload_true
        (_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and jpbd__nxx and not is_overload_true(_is_parallel)
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
        zgk__rxk = df.runtime_data_types
        itma__mrou = len(zgk__rxk)
        yuv__peqnp = gen_pandas_parquet_metadata([''] * itma__mrou,
            zgk__rxk, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        hwok__rbvu = yuv__peqnp['columns'][:itma__mrou]
        yuv__peqnp['columns'] = yuv__peqnp['columns'][itma__mrou:]
        hwok__rbvu = [json.dumps(zwpq__yzwyw).replace('""', '{0}') for
            zwpq__yzwyw in hwok__rbvu]
        rcwcx__vet = json.dumps(yuv__peqnp)
        cww__lafkq = '"columns": ['
        kdhx__ajtu = rcwcx__vet.find(cww__lafkq)
        if kdhx__ajtu == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        crx__orr = kdhx__ajtu + len(cww__lafkq)
        rtzw__hkbeu = rcwcx__vet[:crx__orr]
        rcwcx__vet = rcwcx__vet[crx__orr:]
        sbfi__mczgq = len(yuv__peqnp['columns'])
    else:
        rcwcx__vet = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and jpbd__nxx:
        rcwcx__vet = rcwcx__vet.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            rcwcx__vet = rcwcx__vet.replace('"%s"', '%s')
    if not df.is_table_format:
        hpjf__iukyb = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    thr__urxa = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        thr__urxa += '    py_table = get_dataframe_table(df)\n'
        thr__urxa += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        thr__urxa += '    info_list = [{}]\n'.format(hpjf__iukyb)
        thr__urxa += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        thr__urxa += '    columns_index = get_dataframe_column_names(df)\n'
        thr__urxa += '    names_arr = index_to_array(columns_index)\n'
        thr__urxa += '    col_names = array_to_info(names_arr)\n'
    else:
        thr__urxa += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and hpbar__bbji:
        thr__urxa += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        qvuh__wui = True
    else:
        thr__urxa += '    index_col = array_to_info(np.empty(0))\n'
        qvuh__wui = False
    if df.has_runtime_cols:
        thr__urxa += '    columns_lst = []\n'
        thr__urxa += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            thr__urxa += f'    for _ in range(len(py_table.block_{i})):\n'
            thr__urxa += f"""        columns_lst.append({hwok__rbvu[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            thr__urxa += '        num_cols += 1\n'
        if sbfi__mczgq:
            thr__urxa += "    columns_lst.append('')\n"
        thr__urxa += '    columns_str = ", ".join(columns_lst)\n'
        thr__urxa += ('    metadata = """' + rtzw__hkbeu +
            '""" + columns_str + """' + rcwcx__vet + '"""\n')
    else:
        thr__urxa += '    metadata = """' + rcwcx__vet + '"""\n'
    thr__urxa += '    if compression is None:\n'
    thr__urxa += "        compression = 'none'\n"
    thr__urxa += '    if df.index.name is not None:\n'
    thr__urxa += '        name_ptr = df.index.name\n'
    thr__urxa += '    else:\n'
    thr__urxa += "        name_ptr = 'null'\n"
    thr__urxa += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    iyebn__asx = None
    if partition_cols:
        iyebn__asx = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        ouz__shhxq = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in fxd__ejo)
        if ouz__shhxq:
            thr__urxa += '    cat_info_list = [{}]\n'.format(ouz__shhxq)
            thr__urxa += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            thr__urxa += '    cat_table = table\n'
        thr__urxa += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        thr__urxa += (
            f'    part_cols_idxs = np.array({fxd__ejo}, dtype=np.int32)\n')
        thr__urxa += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        thr__urxa += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        thr__urxa += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        thr__urxa += (
            '                            unicode_to_utf8(compression),\n')
        thr__urxa += '                            _is_parallel,\n'
        thr__urxa += (
            '                            unicode_to_utf8(bucket_region),\n')
        thr__urxa += '                            row_group_size)\n'
        thr__urxa += '    delete_table_decref_arrays(table)\n'
        thr__urxa += '    delete_info_decref_array(index_col)\n'
        thr__urxa += '    delete_info_decref_array(col_names_no_partitions)\n'
        thr__urxa += '    delete_info_decref_array(col_names)\n'
        if ouz__shhxq:
            thr__urxa += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        thr__urxa += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        thr__urxa += (
            '                            table, col_names, index_col,\n')
        thr__urxa += '                            ' + str(qvuh__wui) + ',\n'
        thr__urxa += '                            unicode_to_utf8(metadata),\n'
        thr__urxa += (
            '                            unicode_to_utf8(compression),\n')
        thr__urxa += (
            '                            _is_parallel, 1, df.index.start,\n')
        thr__urxa += (
            '                            df.index.stop, df.index.step,\n')
        thr__urxa += '                            unicode_to_utf8(name_ptr),\n'
        thr__urxa += (
            '                            unicode_to_utf8(bucket_region),\n')
        thr__urxa += '                            row_group_size)\n'
        thr__urxa += '    delete_table_decref_arrays(table)\n'
        thr__urxa += '    delete_info_decref_array(index_col)\n'
        thr__urxa += '    delete_info_decref_array(col_names)\n'
    else:
        thr__urxa += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        thr__urxa += (
            '                            table, col_names, index_col,\n')
        thr__urxa += '                            ' + str(qvuh__wui) + ',\n'
        thr__urxa += '                            unicode_to_utf8(metadata),\n'
        thr__urxa += (
            '                            unicode_to_utf8(compression),\n')
        thr__urxa += '                            _is_parallel, 0, 0, 0, 0,\n'
        thr__urxa += '                            unicode_to_utf8(name_ptr),\n'
        thr__urxa += (
            '                            unicode_to_utf8(bucket_region),\n')
        thr__urxa += '                            row_group_size)\n'
        thr__urxa += '    delete_table_decref_arrays(table)\n'
        thr__urxa += '    delete_info_decref_array(index_col)\n'
        thr__urxa += '    delete_info_decref_array(col_names)\n'
    ytg__sonj = {}
    if df.has_runtime_cols:
        scn__xuig = None
    else:
        for gooq__mydr in df.columns:
            if not isinstance(gooq__mydr, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        scn__xuig = pd.array(df.columns)
    exec(thr__urxa, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': scn__xuig,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': iyebn__asx, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, ytg__sonj)
    vtuv__dzhzi = ytg__sonj['df_to_parquet']
    return vtuv__dzhzi


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    gsah__dioa = 'all_ok'
    axcs__qjyv = urlparse(con)
    hhxnt__xxrb = axcs__qjyv.scheme
    if _is_parallel and bodo.get_rank() == 0:
        vsr__jor = 100
        if chunksize is None:
            cqjlt__xwdoq = vsr__jor
        else:
            cqjlt__xwdoq = min(chunksize, vsr__jor)
        if _is_table_create:
            df = df.iloc[:cqjlt__xwdoq, :]
        else:
            df = df.iloc[cqjlt__xwdoq:, :]
            if len(df) == 0:
                return gsah__dioa
    argf__ohro = df.columns
    try:
        if hhxnt__xxrb == 'snowflake':
            tfqr__zvy = axcs__qjyv.password
            if tfqr__zvy and con.count(tfqr__zvy) == 1:
                con = con.replace(tfqr__zvy, quote(tfqr__zvy))
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
                df.columns = [(ylva__vjlc.upper() if ylva__vjlc.islower() else
                    ylva__vjlc) for ylva__vjlc in df.columns]
            except ImportError as soy__cjqa:
                gsah__dioa = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return gsah__dioa
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as hre__vyyle:
            gsah__dioa = hre__vyyle.args[0]
        return gsah__dioa
    finally:
        df.columns = argf__ohro


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
        ewa__cylb = bodo.libs.distributed_api.get_rank()
        gsah__dioa = 'unset'
        if ewa__cylb != 0:
            gsah__dioa = bcast_scalar(gsah__dioa)
        elif ewa__cylb == 0:
            gsah__dioa = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, True, _is_parallel)
            gsah__dioa = bcast_scalar(gsah__dioa)
        if_exists = 'append'
        if _is_parallel and gsah__dioa == 'all_ok':
            gsah__dioa = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, False, _is_parallel)
        if gsah__dioa != 'all_ok':
            print('err_msg=', gsah__dioa)
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
        xdg__ykqaq = get_overload_const_str(path_or_buf)
        if xdg__ykqaq.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        ljn__vbrtj = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(ljn__vbrtj))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(ljn__vbrtj))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    hkux__iecj = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    fzhkj__sxm = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', hkux__iecj, fzhkj__sxm,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    thr__urxa = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        bfnr__nffj = data.data.dtype.categories
        thr__urxa += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        bfnr__nffj = data.dtype.categories
        thr__urxa += '  data_values = data\n'
    zorit__zexiy = len(bfnr__nffj)
    thr__urxa += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    thr__urxa += '  numba.parfors.parfor.init_prange()\n'
    thr__urxa += '  n = len(data_values)\n'
    for i in range(zorit__zexiy):
        thr__urxa += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    thr__urxa += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    thr__urxa += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for qpbho__kkd in range(zorit__zexiy):
        thr__urxa += '          data_arr_{}[i] = 0\n'.format(qpbho__kkd)
    thr__urxa += '      else:\n'
    for imwd__udac in range(zorit__zexiy):
        thr__urxa += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            imwd__udac)
    hpjf__iukyb = ', '.join(f'data_arr_{i}' for i in range(zorit__zexiy))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(bfnr__nffj[0], np.datetime64):
        bfnr__nffj = tuple(pd.Timestamp(ylva__vjlc) for ylva__vjlc in
            bfnr__nffj)
    elif isinstance(bfnr__nffj[0], np.timedelta64):
        bfnr__nffj = tuple(pd.Timedelta(ylva__vjlc) for ylva__vjlc in
            bfnr__nffj)
    return bodo.hiframes.dataframe_impl._gen_init_df(thr__urxa, bfnr__nffj,
        hpjf__iukyb, index)


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
    for wycjh__vnzr in pd_unsupported:
        vcj__zytav = mod_name + '.' + wycjh__vnzr.__name__
        overload(wycjh__vnzr, no_unliteral=True)(create_unsupported_overload
            (vcj__zytav))


def _install_dataframe_unsupported():
    for bihq__bfcyg in dataframe_unsupported_attrs:
        uyw__tnu = 'DataFrame.' + bihq__bfcyg
        overload_attribute(DataFrameType, bihq__bfcyg)(
            create_unsupported_overload(uyw__tnu))
    for vcj__zytav in dataframe_unsupported:
        uyw__tnu = 'DataFrame.' + vcj__zytav + '()'
        overload_method(DataFrameType, vcj__zytav)(create_unsupported_overload
            (uyw__tnu))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
