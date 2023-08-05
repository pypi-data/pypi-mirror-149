"""
Indexing support for pd.DataFrame type.
"""
import operator
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.transform import gen_const_tup
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_list, get_overload_const_str, is_immutable_array, is_list_like_index_type, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, raise_bodo_error


@infer_global(operator.getitem)
class DataFrameGetItemTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        check_runtime_cols_unsupported(args[0], 'DataFrame getitem (df[])')
        if isinstance(args[0], DataFrameType):
            return self.typecheck_df_getitem(args)
        elif isinstance(args[0], DataFrameLocType):
            return self.typecheck_loc_getitem(args)
        else:
            return

    def typecheck_loc_getitem(self, args):
        I = args[0]
        idx = args[1]
        df = I.df_type
        if isinstance(df.columns[0], tuple):
            raise_bodo_error(
                'DataFrame.loc[] getitem (location-based indexing) with multi-indexed columns not supported yet'
                )
        if is_list_like_index_type(idx) and idx.dtype == types.bool_:
            qym__zmg = idx
            wwyfk__voo = df.data
            brhh__pkiv = df.columns
            jqncg__nswor = self.replace_range_with_numeric_idx_if_needed(df,
                qym__zmg)
            itfwj__afked = DataFrameType(wwyfk__voo, jqncg__nswor, brhh__pkiv)
            return itfwj__afked(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            zeh__zfwge = idx.types[0]
            pbyt__fmp = idx.types[1]
            if isinstance(zeh__zfwge, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(pbyt__fmp):
                    ihk__fjoi = get_overload_const_str(pbyt__fmp)
                    if ihk__fjoi not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, ihk__fjoi))
                    ibl__ddxo = df.columns.index(ihk__fjoi)
                    return df.data[ibl__ddxo].dtype(*args)
                if isinstance(pbyt__fmp, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(zeh__zfwge
                ) and zeh__zfwge.dtype == types.bool_ or isinstance(zeh__zfwge,
                types.SliceType):
                jqncg__nswor = self.replace_range_with_numeric_idx_if_needed(df
                    , zeh__zfwge)
                if is_overload_constant_str(pbyt__fmp):
                    oqjlm__jtn = get_overload_const_str(pbyt__fmp)
                    if oqjlm__jtn not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {oqjlm__jtn}'
                            )
                    ibl__ddxo = df.columns.index(oqjlm__jtn)
                    ban__bbimq = df.data[ibl__ddxo]
                    axv__zvk = ban__bbimq.dtype
                    wtpgd__ykx = types.literal(df.columns[ibl__ddxo])
                    itfwj__afked = bodo.SeriesType(axv__zvk, ban__bbimq,
                        jqncg__nswor, wtpgd__ykx)
                    return itfwj__afked(*args)
                if isinstance(pbyt__fmp, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                elif is_overload_constant_list(pbyt__fmp):
                    advcm__wxep = get_overload_const_list(pbyt__fmp)
                    jmyno__vtzix = types.unliteral(pbyt__fmp)
                    if jmyno__vtzix.dtype == types.bool_:
                        if len(df.columns) != len(advcm__wxep):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {advcm__wxep} has {len(advcm__wxep)} values'
                                )
                        wsaf__ufpr = []
                        kap__zrix = []
                        for oqamo__posg in range(len(advcm__wxep)):
                            if advcm__wxep[oqamo__posg]:
                                wsaf__ufpr.append(df.columns[oqamo__posg])
                                kap__zrix.append(df.data[oqamo__posg])
                        bavt__cwczt = tuple()
                        itfwj__afked = DataFrameType(tuple(kap__zrix),
                            jqncg__nswor, tuple(wsaf__ufpr))
                        return itfwj__afked(*args)
                    elif jmyno__vtzix.dtype == bodo.string_type:
                        bavt__cwczt, kap__zrix = self.get_kept_cols_and_data(df
                            , advcm__wxep)
                        itfwj__afked = DataFrameType(kap__zrix,
                            jqncg__nswor, bavt__cwczt)
                        return itfwj__afked(*args)
        raise_bodo_error(
            f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet. If you are trying to select a subset of the columns by passing a list of column names, that list must be a compile time constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
            )

    def typecheck_df_getitem(self, args):
        df = args[0]
        ind = args[1]
        if is_overload_constant_str(ind) or is_overload_constant_int(ind):
            ind_val = get_overload_const_str(ind) if is_overload_constant_str(
                ind) else get_overload_const_int(ind)
            if isinstance(df.columns[0], tuple):
                wsaf__ufpr = []
                kap__zrix = []
                for oqamo__posg, lfhw__zzlcn in enumerate(df.columns):
                    if lfhw__zzlcn[0] != ind_val:
                        continue
                    wsaf__ufpr.append(lfhw__zzlcn[1] if len(lfhw__zzlcn) ==
                        2 else lfhw__zzlcn[1:])
                    kap__zrix.append(df.data[oqamo__posg])
                ban__bbimq = tuple(kap__zrix)
                yjqd__pfpl = df.index
                vzhsf__ccyyv = tuple(wsaf__ufpr)
                itfwj__afked = DataFrameType(ban__bbimq, yjqd__pfpl,
                    vzhsf__ccyyv)
                return itfwj__afked(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                ibl__ddxo = df.columns.index(ind_val)
                ban__bbimq = df.data[ibl__ddxo]
                axv__zvk = ban__bbimq.dtype
                yjqd__pfpl = df.index
                wtpgd__ykx = types.literal(df.columns[ibl__ddxo])
                itfwj__afked = bodo.SeriesType(axv__zvk, ban__bbimq,
                    yjqd__pfpl, wtpgd__ykx)
                return itfwj__afked(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            ban__bbimq = df.data
            yjqd__pfpl = self.replace_range_with_numeric_idx_if_needed(df, ind)
            vzhsf__ccyyv = df.columns
            itfwj__afked = DataFrameType(ban__bbimq, yjqd__pfpl,
                vzhsf__ccyyv, is_table_format=df.is_table_format)
            return itfwj__afked(*args)
        elif is_overload_constant_list(ind):
            yrwf__npe = get_overload_const_list(ind)
            vzhsf__ccyyv, ban__bbimq = self.get_kept_cols_and_data(df,
                yrwf__npe)
            yjqd__pfpl = df.index
            itfwj__afked = DataFrameType(ban__bbimq, yjqd__pfpl, vzhsf__ccyyv)
            return itfwj__afked(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for jtwh__ndhxs in cols_to_keep_list:
            if jtwh__ndhxs not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(jtwh__ndhxs, df.columns))
        vzhsf__ccyyv = tuple(cols_to_keep_list)
        ban__bbimq = tuple(df.data[df.columns.index(pwlx__uuvc)] for
            pwlx__uuvc in vzhsf__ccyyv)
        return vzhsf__ccyyv, ban__bbimq

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        jqncg__nswor = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return jqncg__nswor


DataFrameGetItemTemplate._no_unliteral = True


@lower_builtin(operator.getitem, DataFrameType, types.Any)
def getitem_df_lower(context, builder, sig, args):
    impl = df_getitem_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_getitem_overload(df, ind):
    if not isinstance(df, DataFrameType):
        return
    if is_overload_constant_str(ind) or is_overload_constant_int(ind):
        ind_val = get_overload_const_str(ind) if is_overload_constant_str(ind
            ) else get_overload_const_int(ind)
        if isinstance(df.columns[0], tuple):
            wsaf__ufpr = []
            kap__zrix = []
            for oqamo__posg, lfhw__zzlcn in enumerate(df.columns):
                if lfhw__zzlcn[0] != ind_val:
                    continue
                wsaf__ufpr.append(lfhw__zzlcn[1] if len(lfhw__zzlcn) == 2 else
                    lfhw__zzlcn[1:])
                kap__zrix.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(oqamo__posg))
            plbm__ohad = 'def impl(df, ind):\n'
            rtq__obe = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
            return bodo.hiframes.dataframe_impl._gen_init_df(plbm__ohad,
                wsaf__ufpr, ', '.join(kap__zrix), rtq__obe)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        yrwf__npe = get_overload_const_list(ind)
        for jtwh__ndhxs in yrwf__npe:
            if jtwh__ndhxs not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(jtwh__ndhxs, df.columns))
        kap__zrix = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}).copy()'
            .format(df.columns.index(jtwh__ndhxs)) for jtwh__ndhxs in yrwf__npe
            )
        plbm__ohad = 'def impl(df, ind):\n'
        rtq__obe = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(plbm__ohad,
            yrwf__npe, kap__zrix, rtq__obe)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        plbm__ohad = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            plbm__ohad += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        rtq__obe = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            kap__zrix = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            kap__zrix = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(jtwh__ndhxs)})[ind]'
                 for jtwh__ndhxs in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(plbm__ohad, df.
            columns, kap__zrix, rtq__obe, out_df_type=df)
    raise_bodo_error('df[] getitem using {} not supported'.format(ind))


@overload(operator.setitem, no_unliteral=True)
def df_setitem_overload(df, idx, val):
    check_runtime_cols_unsupported(df, 'DataFrame setitem (df[])')
    if not isinstance(df, DataFrameType):
        return
    raise_bodo_error('DataFrame setitem: transform necessary')


class DataFrameILocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        pwlx__uuvc = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(pwlx__uuvc)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gmo__faavj = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, gmo__faavj)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        xhg__jub, = args
        rctqb__jojgw = signature.return_type
        pbio__sfb = cgutils.create_struct_proxy(rctqb__jojgw)(context, builder)
        pbio__sfb.obj = xhg__jub
        context.nrt.incref(builder, signature.args[0], xhg__jub)
        return pbio__sfb._getvalue()
    return DataFrameILocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iloc')
def overload_dataframe_iloc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iloc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iloc(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iloc_getitem(I, idx):
    if not isinstance(I, DataFrameILocType):
        return
    df = I.df_type
    if isinstance(idx, types.Integer):
        return _gen_iloc_getitem_row_impl(df, df.columns, 'idx')
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and not isinstance(
        idx[1], types.SliceType):
        if not (is_overload_constant_list(idx.types[1]) or
            is_overload_constant_int(idx.types[1])):
            raise_bodo_error(
                'idx2 in df.iloc[idx1, idx2] should be a constant integer or constant list of integers. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                )
        rgjk__cold = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            rsq__ftlq = get_overload_const_int(idx.types[1])
            if rsq__ftlq < 0 or rsq__ftlq >= rgjk__cold:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            wpfeq__rvwk = [rsq__ftlq]
        else:
            is_out_series = False
            wpfeq__rvwk = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= rgjk__cold for
                ind in wpfeq__rvwk):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[wpfeq__rvwk])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                rsq__ftlq = wpfeq__rvwk[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, rsq__ftlq)[
                        idx[0]])
                return impl
            return _gen_iloc_getitem_row_impl(df, col_names, 'idx[0]')
        if is_list_like_index_type(idx.types[0]) and isinstance(idx.types[0
            ].dtype, (types.Integer, types.Boolean)) or isinstance(idx.
            types[0], types.SliceType):
            return _gen_iloc_getitem_bool_slice_impl(df, col_names, idx.
                types[0], 'idx[0]', is_out_series)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
        Integer, types.Boolean)) or isinstance(idx, types.SliceType):
        return _gen_iloc_getitem_bool_slice_impl(df, df.columns, idx, 'idx',
            False)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):
        raise_bodo_error(
            'slice2 in df.iloc[slice1,slice2] should be constant. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
            )
    raise_bodo_error(f'df.iloc[] getitem using {idx} not supported')


def _gen_iloc_getitem_bool_slice_impl(df, col_names, idx_typ, idx,
    is_out_series):
    plbm__ohad = 'def impl(I, idx):\n'
    plbm__ohad += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        plbm__ohad += f'  idx_t = {idx}\n'
    else:
        plbm__ohad += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    rtq__obe = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    kap__zrix = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(jtwh__ndhxs)})[idx_t]'
         for jtwh__ndhxs in col_names)
    if is_out_series:
        nysv__qht = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        plbm__ohad += f"""  return bodo.hiframes.pd_series_ext.init_series({kap__zrix}, {rtq__obe}, {nysv__qht})
"""
        oxgk__pjsoz = {}
        exec(plbm__ohad, {'bodo': bodo}, oxgk__pjsoz)
        return oxgk__pjsoz['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(plbm__ohad, col_names,
        kap__zrix, rtq__obe)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    plbm__ohad = 'def impl(I, idx):\n'
    plbm__ohad += '  df = I._obj\n'
    tborr__dtwvh = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(jtwh__ndhxs)})[{idx}]'
         for jtwh__ndhxs in col_names)
    plbm__ohad += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    plbm__ohad += f"""  return bodo.hiframes.pd_series_ext.init_series(({tborr__dtwvh},), row_idx, None)
"""
    oxgk__pjsoz = {}
    exec(plbm__ohad, {'bodo': bodo}, oxgk__pjsoz)
    impl = oxgk__pjsoz['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def df_iloc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameILocType):
        return
    raise_bodo_error(
        f'DataFrame.iloc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameLocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        pwlx__uuvc = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(pwlx__uuvc)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gmo__faavj = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, gmo__faavj)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        xhg__jub, = args
        ipfr__nbuwo = signature.return_type
        htx__lzhnh = cgutils.create_struct_proxy(ipfr__nbuwo)(context, builder)
        htx__lzhnh.obj = xhg__jub
        context.nrt.incref(builder, signature.args[0], xhg__jub)
        return htx__lzhnh._getvalue()
    return DataFrameLocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'loc')
def overload_dataframe_loc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.loc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_loc(df)


@lower_builtin(operator.getitem, DataFrameLocType, types.Any)
def loc_getitem_lower(context, builder, sig, args):
    impl = overload_loc_getitem(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def overload_loc_getitem(I, idx):
    if not isinstance(I, DataFrameLocType):
        return
    df = I.df_type
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        plbm__ohad = 'def impl(I, idx):\n'
        plbm__ohad += '  df = I._obj\n'
        plbm__ohad += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        rtq__obe = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        kap__zrix = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx_t]'
            .format(df.columns.index(jtwh__ndhxs)) for jtwh__ndhxs in df.
            columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(plbm__ohad, df.
            columns, kap__zrix, rtq__obe)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        wmlf__ses = idx.types[1]
        if is_overload_constant_str(wmlf__ses):
            bazdt__vwnkj = get_overload_const_str(wmlf__ses)
            rsq__ftlq = df.columns.index(bazdt__vwnkj)

            def impl_col_name(I, idx):
                df = I._obj
                rtq__obe = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                qqjjx__lfq = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, rsq__ftlq)
                return bodo.hiframes.pd_series_ext.init_series(qqjjx__lfq,
                    rtq__obe, bazdt__vwnkj).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(wmlf__ses):
            col_idx_list = get_overload_const_list(wmlf__ses)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(jtwh__ndhxs in df.columns for
                jtwh__ndhxs in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        col_idx_list = list(pd.Series(df.columns, dtype=object)[col_idx_list])
    kap__zrix = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx[0]]'
        .format(df.columns.index(jtwh__ndhxs)) for jtwh__ndhxs in col_idx_list)
    rtq__obe = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]'
    plbm__ohad = 'def impl(I, idx):\n'
    plbm__ohad += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(plbm__ohad,
        col_idx_list, kap__zrix, rtq__obe)


@overload(operator.setitem, no_unliteral=True)
def df_loc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameLocType):
        return
    raise_bodo_error(
        f'DataFrame.loc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameIatType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        pwlx__uuvc = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(pwlx__uuvc)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gmo__faavj = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, gmo__faavj)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        xhg__jub, = args
        zte__prh = signature.return_type
        dkntw__lyand = cgutils.create_struct_proxy(zte__prh)(context, builder)
        dkntw__lyand.obj = xhg__jub
        context.nrt.incref(builder, signature.args[0], xhg__jub)
        return dkntw__lyand._getvalue()
    return DataFrameIatType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iat')
def overload_dataframe_iat(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iat')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iat(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iat_getitem(I, idx):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat getitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                )
        rsq__ftlq = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            qqjjx__lfq = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                rsq__ftlq)
            return qqjjx__lfq[idx[0]]
        return impl_col_ind
    raise BodoError('df.iat[] getitem using {} not supported'.format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_iat_setitem(I, idx, val):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat setitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        rsq__ftlq = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[rsq__ftlq]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            qqjjx__lfq = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                rsq__ftlq)
            qqjjx__lfq[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    dkntw__lyand = cgutils.create_struct_proxy(fromty)(context, builder, val)
    pqjy__iutdf = context.cast(builder, dkntw__lyand.obj, fromty.df_type,
        toty.df_type)
    jqoj__obdti = cgutils.create_struct_proxy(toty)(context, builder)
    jqoj__obdti.obj = pqjy__iutdf
    return jqoj__obdti._getvalue()
