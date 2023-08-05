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
            ujynr__yjjrl = 'Series'
        else:
            ujynr__yjjrl = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{ujynr__yjjrl}.rolling()')
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
        bbn__wlk = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, bbn__wlk)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    cibxo__awkaj = dict(win_type=win_type, axis=axis, closed=closed)
    tyap__zzd = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', cibxo__awkaj, tyap__zzd,
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
    cibxo__awkaj = dict(win_type=win_type, axis=axis, closed=closed)
    tyap__zzd = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', cibxo__awkaj, tyap__zzd,
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
        kym__ourvw, guhy__ruxk, uunsv__oue, ohcg__ndgb, flod__eeywi = args
        fuc__tzbsz = signature.return_type
        bcfqz__tqif = cgutils.create_struct_proxy(fuc__tzbsz)(context, builder)
        bcfqz__tqif.obj = kym__ourvw
        bcfqz__tqif.window = guhy__ruxk
        bcfqz__tqif.min_periods = uunsv__oue
        bcfqz__tqif.center = ohcg__ndgb
        context.nrt.incref(builder, signature.args[0], kym__ourvw)
        context.nrt.incref(builder, signature.args[1], guhy__ruxk)
        context.nrt.incref(builder, signature.args[2], uunsv__oue)
        context.nrt.incref(builder, signature.args[3], ohcg__ndgb)
        return bcfqz__tqif._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    fuc__tzbsz = RollingType(obj_type, window_type, on, selection, False)
    return fuc__tzbsz(obj_type, window_type, min_periods_type, center_type,
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
    chdwv__nyme = not isinstance(rolling.window_type, types.Integer)
    gfsfi__ufo = 'variable' if chdwv__nyme else 'fixed'
    gdutv__qnhx = 'None'
    if chdwv__nyme:
        gdutv__qnhx = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    yajx__fexkm = []
    mhyb__rjzop = 'on_arr, ' if chdwv__nyme else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{gfsfi__ufo}(bodo.hiframes.pd_series_ext.get_series_data(df), {mhyb__rjzop}index_arr, window, minp, center, func, raw)'
            , gdutv__qnhx, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    fgmj__fwj = rolling.obj_type.data
    out_cols = []
    for mtseu__eug in rolling.selection:
        mvsit__rqtco = rolling.obj_type.columns.index(mtseu__eug)
        if mtseu__eug == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            qlbjd__msrq = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {mvsit__rqtco})'
                )
            out_cols.append(mtseu__eug)
        else:
            if not isinstance(fgmj__fwj[mvsit__rqtco].dtype, (types.Boolean,
                types.Number)):
                continue
            qlbjd__msrq = (
                f'bodo.hiframes.rolling.rolling_{gfsfi__ufo}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {mvsit__rqtco}), {mhyb__rjzop}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(mtseu__eug)
        yajx__fexkm.append(qlbjd__msrq)
    return ', '.join(yajx__fexkm), gdutv__qnhx, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    cibxo__awkaj = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    tyap__zzd = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', cibxo__awkaj, tyap__zzd,
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
    cibxo__awkaj = dict(win_type=win_type, axis=axis, closed=closed, method
        =method)
    tyap__zzd = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', cibxo__awkaj, tyap__zzd,
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
        zdonu__ohh = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        emwf__dqrwr = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{yoa__momsa}'" if
                isinstance(yoa__momsa, str) else f'{yoa__momsa}' for
                yoa__momsa in rolling.selection if yoa__momsa != rolling.on))
        rxusj__ycxe = sul__pgvn = ''
        if fname == 'apply':
            rxusj__ycxe = 'func, raw, args, kwargs'
            sul__pgvn = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            rxusj__ycxe = sul__pgvn = 'other, pairwise'
        if fname == 'cov':
            rxusj__ycxe = sul__pgvn = 'other, pairwise, ddof'
        spyqm__elt = (
            f'lambda df, window, minp, center, {rxusj__ycxe}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {emwf__dqrwr}){selection}.{fname}({sul__pgvn})'
            )
        zdonu__ohh += f"""  return rolling.obj.apply({spyqm__elt}, rolling.window, rolling.min_periods, rolling.center, {rxusj__ycxe})
"""
        bxfe__umtx = {}
        exec(zdonu__ohh, {'bodo': bodo}, bxfe__umtx)
        impl = bxfe__umtx['impl']
        return impl
    tlzws__vsd = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if tlzws__vsd else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if tlzws__vsd else rolling.obj_type.columns
        other_cols = None if tlzws__vsd else other.columns
        yajx__fexkm, gdutv__qnhx = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        yajx__fexkm, gdutv__qnhx, out_cols = _gen_df_rolling_out_data(rolling)
    uxd__nlewu = tlzws__vsd or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    cuxg__utkym = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    cuxg__utkym += '  df = rolling.obj\n'
    cuxg__utkym += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if tlzws__vsd else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    ujynr__yjjrl = 'None'
    if tlzws__vsd:
        ujynr__yjjrl = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif uxd__nlewu:
        mtseu__eug = (set(out_cols) - set([rolling.on])).pop()
        ujynr__yjjrl = f"'{mtseu__eug}'" if isinstance(mtseu__eug, str
            ) else str(mtseu__eug)
    cuxg__utkym += f'  name = {ujynr__yjjrl}\n'
    cuxg__utkym += '  window = rolling.window\n'
    cuxg__utkym += '  center = rolling.center\n'
    cuxg__utkym += '  minp = rolling.min_periods\n'
    cuxg__utkym += f'  on_arr = {gdutv__qnhx}\n'
    if fname == 'apply':
        cuxg__utkym += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        cuxg__utkym += f"  func = '{fname}'\n"
        cuxg__utkym += f'  index_arr = None\n'
        cuxg__utkym += f'  raw = False\n'
    if uxd__nlewu:
        cuxg__utkym += (
            f'  return bodo.hiframes.pd_series_ext.init_series({yajx__fexkm}, index, name)'
            )
        bxfe__umtx = {}
        hisz__sppky = {'bodo': bodo}
        exec(cuxg__utkym, hisz__sppky, bxfe__umtx)
        impl = bxfe__umtx['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(cuxg__utkym, out_cols,
        yajx__fexkm)


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
        kgu__upvto = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(kgu__upvto)


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
    ulu__ruf = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(ulu__ruf) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    chdwv__nyme = not isinstance(window_type, types.Integer)
    gdutv__qnhx = 'None'
    if chdwv__nyme:
        gdutv__qnhx = 'bodo.utils.conversion.index_to_array(index)'
    mhyb__rjzop = 'on_arr, ' if chdwv__nyme else ''
    yajx__fexkm = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {mhyb__rjzop}window, minp, center)'
            , gdutv__qnhx)
    for mtseu__eug in out_cols:
        if mtseu__eug in df_cols and mtseu__eug in other_cols:
            pvoj__mhit = df_cols.index(mtseu__eug)
            aup__gjw = other_cols.index(mtseu__eug)
            qlbjd__msrq = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {pvoj__mhit}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {aup__gjw}), {mhyb__rjzop}window, minp, center)'
                )
        else:
            qlbjd__msrq = 'np.full(len(df), np.nan)'
        yajx__fexkm.append(qlbjd__msrq)
    return ', '.join(yajx__fexkm), gdutv__qnhx


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    mrb__jrh = {'pairwise': pairwise, 'ddof': ddof}
    jodk__ctdv = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        mrb__jrh, jodk__ctdv, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    mrb__jrh = {'ddof': ddof, 'pairwise': pairwise}
    jodk__ctdv = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        mrb__jrh, jodk__ctdv, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, sxjyf__bok = args
        if isinstance(rolling, RollingType):
            ulu__ruf = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(sxjyf__bok, (tuple, list)):
                if len(set(sxjyf__bok).difference(set(ulu__ruf))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(sxjyf__bok).difference(set(ulu__ruf))))
                selection = list(sxjyf__bok)
            else:
                if sxjyf__bok not in ulu__ruf:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(sxjyf__bok))
                selection = [sxjyf__bok]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            nzris__ewka = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(nzris__ewka, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        ulu__ruf = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            ulu__ruf = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            ulu__ruf = rolling.obj_type.columns
        if attr in ulu__ruf:
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
    xwmr__zinpo = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    fgmj__fwj = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in xwmr__zinpo):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        xolug__ozg = fgmj__fwj[xwmr__zinpo.index(get_literal_value(on))]
        if not isinstance(xolug__ozg, types.Array
            ) or xolug__ozg.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(crscf__dre.dtype, (types.Boolean, types.Number)) for
        crscf__dre in fgmj__fwj):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
