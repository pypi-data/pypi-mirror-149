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
            ted__jximp = 'Series'
        else:
            ted__jximp = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{ted__jximp}.rolling()')
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
        ybkhr__grtp = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, ybkhr__grtp)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    tpjzd__aejy = dict(win_type=win_type, axis=axis, closed=closed)
    bfp__tda = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', tpjzd__aejy, bfp__tda,
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
    tpjzd__aejy = dict(win_type=win_type, axis=axis, closed=closed)
    bfp__tda = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', tpjzd__aejy, bfp__tda,
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
        qhnd__ujlb, mhd__qtxm, ylm__fdkyl, kgmm__ghuo, yfgwb__xmt = args
        ubap__koqjt = signature.return_type
        aselt__smqyq = cgutils.create_struct_proxy(ubap__koqjt)(context,
            builder)
        aselt__smqyq.obj = qhnd__ujlb
        aselt__smqyq.window = mhd__qtxm
        aselt__smqyq.min_periods = ylm__fdkyl
        aselt__smqyq.center = kgmm__ghuo
        context.nrt.incref(builder, signature.args[0], qhnd__ujlb)
        context.nrt.incref(builder, signature.args[1], mhd__qtxm)
        context.nrt.incref(builder, signature.args[2], ylm__fdkyl)
        context.nrt.incref(builder, signature.args[3], kgmm__ghuo)
        return aselt__smqyq._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    ubap__koqjt = RollingType(obj_type, window_type, on, selection, False)
    return ubap__koqjt(obj_type, window_type, min_periods_type, center_type,
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
    dpfz__unok = not isinstance(rolling.window_type, types.Integer)
    dpbho__lwtm = 'variable' if dpfz__unok else 'fixed'
    asln__dplr = 'None'
    if dpfz__unok:
        asln__dplr = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    ijqhg__oomo = []
    nicn__utxrc = 'on_arr, ' if dpfz__unok else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{dpbho__lwtm}(bodo.hiframes.pd_series_ext.get_series_data(df), {nicn__utxrc}index_arr, window, minp, center, func, raw)'
            , asln__dplr, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    rmtv__bsa = rolling.obj_type.data
    out_cols = []
    for cvxoq__idyp in rolling.selection:
        wuzoa__qihgm = rolling.obj_type.columns.index(cvxoq__idyp)
        if cvxoq__idyp == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            qjgca__somg = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {wuzoa__qihgm})'
                )
            out_cols.append(cvxoq__idyp)
        else:
            if not isinstance(rmtv__bsa[wuzoa__qihgm].dtype, (types.Boolean,
                types.Number)):
                continue
            qjgca__somg = (
                f'bodo.hiframes.rolling.rolling_{dpbho__lwtm}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {wuzoa__qihgm}), {nicn__utxrc}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(cvxoq__idyp)
        ijqhg__oomo.append(qjgca__somg)
    return ', '.join(ijqhg__oomo), asln__dplr, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    tpjzd__aejy = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    bfp__tda = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', tpjzd__aejy, bfp__tda,
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
    tpjzd__aejy = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    bfp__tda = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', tpjzd__aejy, bfp__tda,
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
        hrv__rfn = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        xujf__pail = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{aubrx__bls}'" if
                isinstance(aubrx__bls, str) else f'{aubrx__bls}' for
                aubrx__bls in rolling.selection if aubrx__bls != rolling.on))
        igt__blc = rpy__oth = ''
        if fname == 'apply':
            igt__blc = 'func, raw, args, kwargs'
            rpy__oth = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            igt__blc = rpy__oth = 'other, pairwise'
        if fname == 'cov':
            igt__blc = rpy__oth = 'other, pairwise, ddof'
        uem__vgm = (
            f'lambda df, window, minp, center, {igt__blc}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {xujf__pail}){selection}.{fname}({rpy__oth})'
            )
        hrv__rfn += f"""  return rolling.obj.apply({uem__vgm}, rolling.window, rolling.min_periods, rolling.center, {igt__blc})
"""
        skkfe__bulha = {}
        exec(hrv__rfn, {'bodo': bodo}, skkfe__bulha)
        impl = skkfe__bulha['impl']
        return impl
    njz__bqlq = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if njz__bqlq else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if njz__bqlq else rolling.obj_type.columns
        other_cols = None if njz__bqlq else other.columns
        ijqhg__oomo, asln__dplr = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        ijqhg__oomo, asln__dplr, out_cols = _gen_df_rolling_out_data(rolling)
    yzqz__rrmdv = njz__bqlq or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    miyr__hunz = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    miyr__hunz += '  df = rolling.obj\n'
    miyr__hunz += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if njz__bqlq else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    ted__jximp = 'None'
    if njz__bqlq:
        ted__jximp = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif yzqz__rrmdv:
        cvxoq__idyp = (set(out_cols) - set([rolling.on])).pop()
        ted__jximp = f"'{cvxoq__idyp}'" if isinstance(cvxoq__idyp, str
            ) else str(cvxoq__idyp)
    miyr__hunz += f'  name = {ted__jximp}\n'
    miyr__hunz += '  window = rolling.window\n'
    miyr__hunz += '  center = rolling.center\n'
    miyr__hunz += '  minp = rolling.min_periods\n'
    miyr__hunz += f'  on_arr = {asln__dplr}\n'
    if fname == 'apply':
        miyr__hunz += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        miyr__hunz += f"  func = '{fname}'\n"
        miyr__hunz += f'  index_arr = None\n'
        miyr__hunz += f'  raw = False\n'
    if yzqz__rrmdv:
        miyr__hunz += (
            f'  return bodo.hiframes.pd_series_ext.init_series({ijqhg__oomo}, index, name)'
            )
        skkfe__bulha = {}
        xipsw__bjyy = {'bodo': bodo}
        exec(miyr__hunz, xipsw__bjyy, skkfe__bulha)
        impl = skkfe__bulha['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(miyr__hunz, out_cols,
        ijqhg__oomo)


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
        gwf__mnql = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(gwf__mnql)


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
    pbl__cremn = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(pbl__cremn) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    dpfz__unok = not isinstance(window_type, types.Integer)
    asln__dplr = 'None'
    if dpfz__unok:
        asln__dplr = 'bodo.utils.conversion.index_to_array(index)'
    nicn__utxrc = 'on_arr, ' if dpfz__unok else ''
    ijqhg__oomo = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {nicn__utxrc}window, minp, center)'
            , asln__dplr)
    for cvxoq__idyp in out_cols:
        if cvxoq__idyp in df_cols and cvxoq__idyp in other_cols:
            mqzns__eikzh = df_cols.index(cvxoq__idyp)
            cbmxo__biw = other_cols.index(cvxoq__idyp)
            qjgca__somg = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {mqzns__eikzh}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {cbmxo__biw}), {nicn__utxrc}window, minp, center)'
                )
        else:
            qjgca__somg = 'np.full(len(df), np.nan)'
        ijqhg__oomo.append(qjgca__somg)
    return ', '.join(ijqhg__oomo), asln__dplr


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    xlhx__ptjr = {'pairwise': pairwise, 'ddof': ddof}
    ddjcu__qjwp = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        xlhx__ptjr, ddjcu__qjwp, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    xlhx__ptjr = {'ddof': ddof, 'pairwise': pairwise}
    ddjcu__qjwp = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        xlhx__ptjr, ddjcu__qjwp, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, ezoss__acl = args
        if isinstance(rolling, RollingType):
            pbl__cremn = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(ezoss__acl, (tuple, list)):
                if len(set(ezoss__acl).difference(set(pbl__cremn))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(ezoss__acl).difference(set(pbl__cremn))))
                selection = list(ezoss__acl)
            else:
                if ezoss__acl not in pbl__cremn:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(ezoss__acl))
                selection = [ezoss__acl]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            cayb__dfa = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(cayb__dfa, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        pbl__cremn = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            pbl__cremn = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            pbl__cremn = rolling.obj_type.columns
        if attr in pbl__cremn:
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
    ilghw__krfuv = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    rmtv__bsa = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in ilghw__krfuv):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        pty__dqyy = rmtv__bsa[ilghw__krfuv.index(get_literal_value(on))]
        if not isinstance(pty__dqyy, types.Array
            ) or pty__dqyy.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(xkzqc__dcjmw.dtype, (types.Boolean, types.Number)
        ) for xkzqc__dcjmw in rmtv__bsa):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
