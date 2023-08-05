"""typing for rolling window functions
"""
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.hiframes.pd_groupby_ext import DataFrameGroupByType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.rolling import supported_rolling_funcs, unsupported_rolling_methods
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, get_literal_value, is_const_func_type, is_literal_type, is_overload_bool, is_overload_constant_str, is_overload_int, is_overload_none, raise_bodo_error


class RollingType(types.Type):

    def __init__(self, obj_type, window_type, on, selection,
        explicit_select=False, series_select=False):
        if isinstance(obj_type, bodo.SeriesType):
            kwofy__zojc = 'Series'
        else:
            kwofy__zojc = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{kwofy__zojc}.rolling()')
        self.obj_type = obj_type
        self.window_type = window_type
        self.on = on
        self.selection = selection
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(RollingType, self).__init__(name=
            f'RollingType({obj_type}, {window_type}, {on}, {selection}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return RollingType(self.obj_type, self.window_type, self.on, self.
            selection, self.explicit_select, self.series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(RollingType)
class RollingModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jue__deymu = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, jue__deymu)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    wbyti__gfvf = dict(win_type=win_type, axis=axis, closed=closed)
    llvx__dudn = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', wbyti__gfvf, llvx__dudn,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(df, window, min_periods, center, on)

    def impl(df, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(df, window,
            min_periods, center, on)
    return impl


@overload_method(SeriesType, 'rolling', inline='always', no_unliteral=True)
def overload_series_rolling(S, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    wbyti__gfvf = dict(win_type=win_type, axis=axis, closed=closed)
    llvx__dudn = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', wbyti__gfvf, llvx__dudn,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(S, window, min_periods, center, on)

    def impl(S, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(S, window,
            min_periods, center, on)
    return impl


@intrinsic
def init_rolling(typingctx, obj_type, window_type, min_periods_type,
    center_type, on_type=None):

    def codegen(context, builder, signature, args):
        nul__xdr, slte__ardzc, pjq__unuzs, jkb__bidbn, ufe__wmc = args
        vvpm__reiua = signature.return_type
        sugz__didqi = cgutils.create_struct_proxy(vvpm__reiua)(context, builder
            )
        sugz__didqi.obj = nul__xdr
        sugz__didqi.window = slte__ardzc
        sugz__didqi.min_periods = pjq__unuzs
        sugz__didqi.center = jkb__bidbn
        context.nrt.incref(builder, signature.args[0], nul__xdr)
        context.nrt.incref(builder, signature.args[1], slte__ardzc)
        context.nrt.incref(builder, signature.args[2], pjq__unuzs)
        context.nrt.incref(builder, signature.args[3], jkb__bidbn)
        return sugz__didqi._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    vvpm__reiua = RollingType(obj_type, window_type, on, selection, False)
    return vvpm__reiua(obj_type, window_type, min_periods_type, center_type,
        on_type), codegen


def _handle_default_min_periods(min_periods, window):
    return min_periods


@overload(_handle_default_min_periods)
def overload_handle_default_min_periods(min_periods, window):
    if is_overload_none(min_periods):
        if isinstance(window, types.Integer):
            return lambda min_periods, window: window
        else:
            return lambda min_periods, window: 1
    else:
        return lambda min_periods, window: min_periods


def _gen_df_rolling_out_data(rolling):
    chzb__lnjm = not isinstance(rolling.window_type, types.Integer)
    hjxk__rqy = 'variable' if chzb__lnjm else 'fixed'
    nuq__yrfor = 'None'
    if chzb__lnjm:
        nuq__yrfor = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    kbvon__ruzj = []
    lgaoo__zpi = 'on_arr, ' if chzb__lnjm else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{hjxk__rqy}(bodo.hiframes.pd_series_ext.get_series_data(df), {lgaoo__zpi}index_arr, window, minp, center, func, raw)'
            , nuq__yrfor, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    feoxd__ncw = rolling.obj_type.data
    out_cols = []
    for uvz__ipky in rolling.selection:
        zhgss__qax = rolling.obj_type.columns.index(uvz__ipky)
        if uvz__ipky == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            rszcg__qno = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {zhgss__qax})'
                )
            out_cols.append(uvz__ipky)
        else:
            if not isinstance(feoxd__ncw[zhgss__qax].dtype, (types.Boolean,
                types.Number)):
                continue
            rszcg__qno = (
                f'bodo.hiframes.rolling.rolling_{hjxk__rqy}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {zhgss__qax}), {lgaoo__zpi}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(uvz__ipky)
        kbvon__ruzj.append(rszcg__qno)
    return ', '.join(kbvon__ruzj), nuq__yrfor, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    wbyti__gfvf = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    llvx__dudn = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', wbyti__gfvf, llvx__dudn,
        package_name='pandas', module_name='Window')
    if not is_const_func_type(func):
        raise BodoError(
            f"Rolling.apply(): 'func' parameter must be a function, not {func} (builtin functions not supported yet)."
            )
    if not is_overload_bool(raw):
        raise BodoError(
            f"Rolling.apply(): 'raw' parameter must be bool, not {raw}.")
    return _gen_rolling_impl(rolling, 'apply')


@overload_method(DataFrameGroupByType, 'rolling', inline='always',
    no_unliteral=True)
def groupby_rolling_overload(grp, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None, method='single'):
    wbyti__gfvf = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    llvx__dudn = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', wbyti__gfvf, llvx__dudn,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(grp, window, min_periods, center, on)

    def _impl(grp, window, min_periods=None, center=False, win_type=None,
        on=None, axis=0, closed=None, method='single'):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(grp, window,
            min_periods, center, on)
    return _impl


def _gen_rolling_impl(rolling, fname, other=None):
    if isinstance(rolling.obj_type, DataFrameGroupByType):
        kfyj__fmxt = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        mlqr__adfgr = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{cctd__khtyg}'" if
                isinstance(cctd__khtyg, str) else f'{cctd__khtyg}' for
                cctd__khtyg in rolling.selection if cctd__khtyg != rolling.on))
        pwlcu__hxe = ieo__wucx = ''
        if fname == 'apply':
            pwlcu__hxe = 'func, raw, args, kwargs'
            ieo__wucx = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            pwlcu__hxe = ieo__wucx = 'other, pairwise'
        if fname == 'cov':
            pwlcu__hxe = ieo__wucx = 'other, pairwise, ddof'
        xzbta__pljr = (
            f'lambda df, window, minp, center, {pwlcu__hxe}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {mlqr__adfgr}){selection}.{fname}({ieo__wucx})'
            )
        kfyj__fmxt += f"""  return rolling.obj.apply({xzbta__pljr}, rolling.window, rolling.min_periods, rolling.center, {pwlcu__hxe})
"""
        pqpdi__uxkyr = {}
        exec(kfyj__fmxt, {'bodo': bodo}, pqpdi__uxkyr)
        impl = pqpdi__uxkyr['impl']
        return impl
    wig__zvcmi = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if wig__zvcmi else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if wig__zvcmi else rolling.obj_type.columns
        other_cols = None if wig__zvcmi else other.columns
        kbvon__ruzj, nuq__yrfor = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        kbvon__ruzj, nuq__yrfor, out_cols = _gen_df_rolling_out_data(rolling)
    chlg__xmyd = wig__zvcmi or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    bcat__zuefi = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    bcat__zuefi += '  df = rolling.obj\n'
    bcat__zuefi += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if wig__zvcmi else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    kwofy__zojc = 'None'
    if wig__zvcmi:
        kwofy__zojc = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif chlg__xmyd:
        uvz__ipky = (set(out_cols) - set([rolling.on])).pop()
        kwofy__zojc = f"'{uvz__ipky}'" if isinstance(uvz__ipky, str) else str(
            uvz__ipky)
    bcat__zuefi += f'  name = {kwofy__zojc}\n'
    bcat__zuefi += '  window = rolling.window\n'
    bcat__zuefi += '  center = rolling.center\n'
    bcat__zuefi += '  minp = rolling.min_periods\n'
    bcat__zuefi += f'  on_arr = {nuq__yrfor}\n'
    if fname == 'apply':
        bcat__zuefi += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        bcat__zuefi += f"  func = '{fname}'\n"
        bcat__zuefi += f'  index_arr = None\n'
        bcat__zuefi += f'  raw = False\n'
    if chlg__xmyd:
        bcat__zuefi += (
            f'  return bodo.hiframes.pd_series_ext.init_series({kbvon__ruzj}, index, name)'
            )
        pqpdi__uxkyr = {}
        gdvs__qlpg = {'bodo': bodo}
        exec(bcat__zuefi, gdvs__qlpg, pqpdi__uxkyr)
        impl = pqpdi__uxkyr['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(bcat__zuefi, out_cols,
        kbvon__ruzj)


def _get_rolling_func_args(fname):
    if fname == 'apply':
        return (
            'func, raw=False, engine=None, engine_kwargs=None, args=None, kwargs=None\n'
            )
    elif fname == 'corr':
        return 'other=None, pairwise=None, ddof=1\n'
    elif fname == 'cov':
        return 'other=None, pairwise=None, ddof=1\n'
    return ''


def create_rolling_overload(fname):

    def overload_rolling_func(rolling):
        return _gen_rolling_impl(rolling, fname)
    return overload_rolling_func


def _install_rolling_methods():
    for fname in supported_rolling_funcs:
        if fname in ('apply', 'corr', 'cov'):
            continue
        hxqm__txhjy = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(hxqm__txhjy)


def _install_rolling_unsupported_methods():
    for fname in unsupported_rolling_methods:
        overload_method(RollingType, fname, no_unliteral=True)(
            create_unsupported_overload(
            f'pandas.core.window.rolling.Rolling.{fname}()'))


_install_rolling_methods()
_install_rolling_unsupported_methods()


def _get_corr_cov_out_cols(rolling, other, func_name):
    if not isinstance(other, DataFrameType):
        raise_bodo_error(
            f"DataFrame.rolling.{func_name}(): requires providing a DataFrame for 'other'"
            )
    glzis__wtldk = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(glzis__wtldk) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    chzb__lnjm = not isinstance(window_type, types.Integer)
    nuq__yrfor = 'None'
    if chzb__lnjm:
        nuq__yrfor = 'bodo.utils.conversion.index_to_array(index)'
    lgaoo__zpi = 'on_arr, ' if chzb__lnjm else ''
    kbvon__ruzj = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {lgaoo__zpi}window, minp, center)'
            , nuq__yrfor)
    for uvz__ipky in out_cols:
        if uvz__ipky in df_cols and uvz__ipky in other_cols:
            umboo__goezz = df_cols.index(uvz__ipky)
            iosza__llpxn = other_cols.index(uvz__ipky)
            rszcg__qno = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {umboo__goezz}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {iosza__llpxn}), {lgaoo__zpi}window, minp, center)'
                )
        else:
            rszcg__qno = 'np.full(len(df), np.nan)'
        kbvon__ruzj.append(rszcg__qno)
    return ', '.join(kbvon__ruzj), nuq__yrfor


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    tept__pzra = {'pairwise': pairwise, 'ddof': ddof}
    azhzl__shcdh = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        tept__pzra, azhzl__shcdh, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    tept__pzra = {'ddof': ddof, 'pairwise': pairwise}
    azhzl__shcdh = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        tept__pzra, azhzl__shcdh, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, tos__kccg = args
        if isinstance(rolling, RollingType):
            glzis__wtldk = rolling.obj_type.selection if isinstance(rolling
                .obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(tos__kccg, (tuple, list)):
                if len(set(tos__kccg).difference(set(glzis__wtldk))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(tos__kccg).difference(set(glzis__wtldk))))
                selection = list(tos__kccg)
            else:
                if tos__kccg not in glzis__wtldk:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(tos__kccg))
                selection = [tos__kccg]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            ihp__yioi = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(ihp__yioi, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        glzis__wtldk = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            glzis__wtldk = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            glzis__wtldk = rolling.obj_type.columns
        if attr in glzis__wtldk:
            return RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, (attr,) if rolling.on is None else (attr,
                rolling.on), True, True)


def _validate_rolling_args(obj, window, min_periods, center, on):
    assert isinstance(obj, (SeriesType, DataFrameType, DataFrameGroupByType)
        ), 'invalid rolling obj'
    func_name = 'Series' if isinstance(obj, SeriesType
        ) else 'DataFrame' if isinstance(obj, DataFrameType
        ) else 'DataFrameGroupBy'
    if not (is_overload_int(window) or is_overload_constant_str(window) or 
        window == bodo.string_type or window in (pd_timedelta_type,
        datetime_timedelta_type)):
        raise BodoError(
            f"{func_name}.rolling(): 'window' should be int or time offset (str, pd.Timedelta, datetime.timedelta), not {window}"
            )
    if not is_overload_bool(center):
        raise BodoError(
            f'{func_name}.rolling(): center must be a boolean, not {center}')
    if not (is_overload_none(min_periods) or isinstance(min_periods, types.
        Integer)):
        raise BodoError(
            f'{func_name}.rolling(): min_periods must be an integer, not {min_periods}'
            )
    if isinstance(obj, SeriesType) and not is_overload_none(on):
        raise BodoError(
            f"{func_name}.rolling(): 'on' not supported for Series yet (can use a DataFrame instead)."
            )
    zbeg__vzkh = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    feoxd__ncw = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in zbeg__vzkh):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        kenfb__bydb = feoxd__ncw[zbeg__vzkh.index(get_literal_value(on))]
        if not isinstance(kenfb__bydb, types.Array
            ) or kenfb__bydb.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(tmwh__czcn.dtype, (types.Boolean, types.Number)) for
        tmwh__czcn in feoxd__ncw):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
