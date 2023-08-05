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
            gvto__bfms = idx
            uff__bor = df.data
            gmijl__aogot = df.columns
            rdcj__kka = self.replace_range_with_numeric_idx_if_needed(df,
                gvto__bfms)
            hnn__nef = DataFrameType(uff__bor, rdcj__kka, gmijl__aogot)
            return hnn__nef(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            drz__bftk = idx.types[0]
            bvjy__czuug = idx.types[1]
            if isinstance(drz__bftk, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(bvjy__czuug):
                    jel__drc = get_overload_const_str(bvjy__czuug)
                    if jel__drc not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, jel__drc))
                    enlsu__xrrgp = df.columns.index(jel__drc)
                    return df.data[enlsu__xrrgp].dtype(*args)
                if isinstance(bvjy__czuug, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(drz__bftk
                ) and drz__bftk.dtype == types.bool_ or isinstance(drz__bftk,
                types.SliceType):
                rdcj__kka = self.replace_range_with_numeric_idx_if_needed(df,
                    drz__bftk)
                if is_overload_constant_str(bvjy__czuug):
                    cldqq__uwov = get_overload_const_str(bvjy__czuug)
                    if cldqq__uwov not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {cldqq__uwov}'
                            )
                    enlsu__xrrgp = df.columns.index(cldqq__uwov)
                    ulwud__okei = df.data[enlsu__xrrgp]
                    gqhqk__yetd = ulwud__okei.dtype
                    tbqkk__ekn = types.literal(df.columns[enlsu__xrrgp])
                    hnn__nef = bodo.SeriesType(gqhqk__yetd, ulwud__okei,
                        rdcj__kka, tbqkk__ekn)
                    return hnn__nef(*args)
                if isinstance(bvjy__czuug, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                elif is_overload_constant_list(bvjy__czuug):
                    mnp__pfbc = get_overload_const_list(bvjy__czuug)
                    qnrnb__bpth = types.unliteral(bvjy__czuug)
                    if qnrnb__bpth.dtype == types.bool_:
                        if len(df.columns) != len(mnp__pfbc):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {mnp__pfbc} has {len(mnp__pfbc)} values'
                                )
                        cxl__ysul = []
                        hei__rite = []
                        for ewld__efxjk in range(len(mnp__pfbc)):
                            if mnp__pfbc[ewld__efxjk]:
                                cxl__ysul.append(df.columns[ewld__efxjk])
                                hei__rite.append(df.data[ewld__efxjk])
                        mub__bugkd = tuple()
                        hnn__nef = DataFrameType(tuple(hei__rite),
                            rdcj__kka, tuple(cxl__ysul))
                        return hnn__nef(*args)
                    elif qnrnb__bpth.dtype == bodo.string_type:
                        mub__bugkd, hei__rite = self.get_kept_cols_and_data(df,
                            mnp__pfbc)
                        hnn__nef = DataFrameType(hei__rite, rdcj__kka,
                            mub__bugkd)
                        return hnn__nef(*args)
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
                cxl__ysul = []
                hei__rite = []
                for ewld__efxjk, goql__cnxn in enumerate(df.columns):
                    if goql__cnxn[0] != ind_val:
                        continue
                    cxl__ysul.append(goql__cnxn[1] if len(goql__cnxn) == 2 else
                        goql__cnxn[1:])
                    hei__rite.append(df.data[ewld__efxjk])
                ulwud__okei = tuple(hei__rite)
                gptw__upid = df.index
                vjx__grl = tuple(cxl__ysul)
                hnn__nef = DataFrameType(ulwud__okei, gptw__upid, vjx__grl)
                return hnn__nef(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                enlsu__xrrgp = df.columns.index(ind_val)
                ulwud__okei = df.data[enlsu__xrrgp]
                gqhqk__yetd = ulwud__okei.dtype
                gptw__upid = df.index
                tbqkk__ekn = types.literal(df.columns[enlsu__xrrgp])
                hnn__nef = bodo.SeriesType(gqhqk__yetd, ulwud__okei,
                    gptw__upid, tbqkk__ekn)
                return hnn__nef(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            ulwud__okei = df.data
            gptw__upid = self.replace_range_with_numeric_idx_if_needed(df, ind)
            vjx__grl = df.columns
            hnn__nef = DataFrameType(ulwud__okei, gptw__upid, vjx__grl,
                is_table_format=df.is_table_format)
            return hnn__nef(*args)
        elif is_overload_constant_list(ind):
            wzff__qex = get_overload_const_list(ind)
            vjx__grl, ulwud__okei = self.get_kept_cols_and_data(df, wzff__qex)
            gptw__upid = df.index
            hnn__nef = DataFrameType(ulwud__okei, gptw__upid, vjx__grl)
            return hnn__nef(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for rfrxu__xze in cols_to_keep_list:
            if rfrxu__xze not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(rfrxu__xze, df.columns))
        vjx__grl = tuple(cols_to_keep_list)
        ulwud__okei = tuple(df.data[df.columns.index(gmvxm__hhw)] for
            gmvxm__hhw in vjx__grl)
        return vjx__grl, ulwud__okei

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        rdcj__kka = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64,
            df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return rdcj__kka


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
            cxl__ysul = []
            hei__rite = []
            for ewld__efxjk, goql__cnxn in enumerate(df.columns):
                if goql__cnxn[0] != ind_val:
                    continue
                cxl__ysul.append(goql__cnxn[1] if len(goql__cnxn) == 2 else
                    goql__cnxn[1:])
                hei__rite.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(ewld__efxjk))
            fjeqr__bnl = 'def impl(df, ind):\n'
            pqd__ejs = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
            return bodo.hiframes.dataframe_impl._gen_init_df(fjeqr__bnl,
                cxl__ysul, ', '.join(hei__rite), pqd__ejs)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        wzff__qex = get_overload_const_list(ind)
        for rfrxu__xze in wzff__qex:
            if rfrxu__xze not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(rfrxu__xze, df.columns))
        hei__rite = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}).copy()'
            .format(df.columns.index(rfrxu__xze)) for rfrxu__xze in wzff__qex)
        fjeqr__bnl = 'def impl(df, ind):\n'
        pqd__ejs = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(fjeqr__bnl,
            wzff__qex, hei__rite, pqd__ejs)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        fjeqr__bnl = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            fjeqr__bnl += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        pqd__ejs = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            hei__rite = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            hei__rite = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(rfrxu__xze)})[ind]'
                 for rfrxu__xze in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(fjeqr__bnl, df.
            columns, hei__rite, pqd__ejs, out_df_type=df)
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
        gmvxm__hhw = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(gmvxm__hhw)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        dcbv__hlcr = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, dcbv__hlcr)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        lftb__obdeb, = args
        kqa__svzkq = signature.return_type
        fub__aob = cgutils.create_struct_proxy(kqa__svzkq)(context, builder)
        fub__aob.obj = lftb__obdeb
        context.nrt.incref(builder, signature.args[0], lftb__obdeb)
        return fub__aob._getvalue()
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
        meu__hhvum = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            jqjz__nulem = get_overload_const_int(idx.types[1])
            if jqjz__nulem < 0 or jqjz__nulem >= meu__hhvum:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            gzjp__ckpqg = [jqjz__nulem]
        else:
            is_out_series = False
            gzjp__ckpqg = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= meu__hhvum for
                ind in gzjp__ckpqg):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[gzjp__ckpqg])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                jqjz__nulem = gzjp__ckpqg[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, jqjz__nulem
                        )[idx[0]])
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
    fjeqr__bnl = 'def impl(I, idx):\n'
    fjeqr__bnl += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        fjeqr__bnl += f'  idx_t = {idx}\n'
    else:
        fjeqr__bnl += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    pqd__ejs = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    hei__rite = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(rfrxu__xze)})[idx_t]'
         for rfrxu__xze in col_names)
    if is_out_series:
        lhakk__bnusn = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        fjeqr__bnl += f"""  return bodo.hiframes.pd_series_ext.init_series({hei__rite}, {pqd__ejs}, {lhakk__bnusn})
"""
        jdhz__tynur = {}
        exec(fjeqr__bnl, {'bodo': bodo}, jdhz__tynur)
        return jdhz__tynur['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(fjeqr__bnl, col_names,
        hei__rite, pqd__ejs)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    fjeqr__bnl = 'def impl(I, idx):\n'
    fjeqr__bnl += '  df = I._obj\n'
    sqi__fdklj = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(rfrxu__xze)})[{idx}]'
         for rfrxu__xze in col_names)
    fjeqr__bnl += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    fjeqr__bnl += f"""  return bodo.hiframes.pd_series_ext.init_series(({sqi__fdklj},), row_idx, None)
"""
    jdhz__tynur = {}
    exec(fjeqr__bnl, {'bodo': bodo}, jdhz__tynur)
    impl = jdhz__tynur['impl']
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
        gmvxm__hhw = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(gmvxm__hhw)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        dcbv__hlcr = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, dcbv__hlcr)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        lftb__obdeb, = args
        ikr__bflg = signature.return_type
        kxbxo__wdo = cgutils.create_struct_proxy(ikr__bflg)(context, builder)
        kxbxo__wdo.obj = lftb__obdeb
        context.nrt.incref(builder, signature.args[0], lftb__obdeb)
        return kxbxo__wdo._getvalue()
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
        fjeqr__bnl = 'def impl(I, idx):\n'
        fjeqr__bnl += '  df = I._obj\n'
        fjeqr__bnl += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        pqd__ejs = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        hei__rite = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx_t]'
            .format(df.columns.index(rfrxu__xze)) for rfrxu__xze in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(fjeqr__bnl, df.
            columns, hei__rite, pqd__ejs)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        sqx__xaxsp = idx.types[1]
        if is_overload_constant_str(sqx__xaxsp):
            mts__sevsf = get_overload_const_str(sqx__xaxsp)
            jqjz__nulem = df.columns.index(mts__sevsf)

            def impl_col_name(I, idx):
                df = I._obj
                pqd__ejs = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                qxt__uvj = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df
                    , jqjz__nulem)
                return bodo.hiframes.pd_series_ext.init_series(qxt__uvj,
                    pqd__ejs, mts__sevsf).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(sqx__xaxsp):
            col_idx_list = get_overload_const_list(sqx__xaxsp)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(rfrxu__xze in df.columns for
                rfrxu__xze in col_idx_list):
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
    hei__rite = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx[0]]'
        .format(df.columns.index(rfrxu__xze)) for rfrxu__xze in col_idx_list)
    pqd__ejs = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]'
    fjeqr__bnl = 'def impl(I, idx):\n'
    fjeqr__bnl += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(fjeqr__bnl,
        col_idx_list, hei__rite, pqd__ejs)


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
        gmvxm__hhw = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(gmvxm__hhw)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        dcbv__hlcr = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, dcbv__hlcr)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        lftb__obdeb, = args
        ygr__wox = signature.return_type
        dvkjz__dcl = cgutils.create_struct_proxy(ygr__wox)(context, builder)
        dvkjz__dcl.obj = lftb__obdeb
        context.nrt.incref(builder, signature.args[0], lftb__obdeb)
        return dvkjz__dcl._getvalue()
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
        jqjz__nulem = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            qxt__uvj = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                jqjz__nulem)
            return qxt__uvj[idx[0]]
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
        jqjz__nulem = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[jqjz__nulem]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            qxt__uvj = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                jqjz__nulem)
            qxt__uvj[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    dvkjz__dcl = cgutils.create_struct_proxy(fromty)(context, builder, val)
    pcuxn__wuibw = context.cast(builder, dvkjz__dcl.obj, fromty.df_type,
        toty.df_type)
    xfvmf__tht = cgutils.create_struct_proxy(toty)(context, builder)
    xfvmf__tht.obj = pcuxn__wuibw
    return xfvmf__tht._getvalue()
