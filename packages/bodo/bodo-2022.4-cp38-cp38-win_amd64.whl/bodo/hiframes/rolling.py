"""implementations of rolling window functions (sequential and parallel)
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, register_jitable
import bodo
from bodo.libs.distributed_api import Reduce_Type
from bodo.utils.typing import BodoError, decode_if_dict_array, get_overload_const_func, get_overload_const_str, is_const_func_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true
from bodo.utils.utils import unliteral_all
supported_rolling_funcs = ('sum', 'mean', 'var', 'std', 'count', 'median',
    'min', 'max', 'cov', 'corr', 'apply')
unsupported_rolling_methods = ['skew', 'kurt', 'aggregate', 'quantile', 'sem']


def rolling_fixed(arr, win):
    return arr


def rolling_variable(arr, on_arr, win):
    return arr


def rolling_cov(arr, arr2, win):
    return arr


def rolling_corr(arr, arr2, win):
    return arr


@infer_global(rolling_cov)
@infer_global(rolling_corr)
class RollingCovType(AbstractTemplate):

    def generic(self, args, kws):
        arr = args[0]
        ogs__vwgdu = arr.copy(dtype=types.float64)
        return signature(ogs__vwgdu, *unliteral_all(args))


@lower_builtin(rolling_corr, types.VarArg(types.Any))
@lower_builtin(rolling_cov, types.VarArg(types.Any))
def lower_rolling_corr_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@overload(rolling_fixed, no_unliteral=True)
def overload_rolling_fixed(arr, index_arr, win, minp, center, fname, raw=
    True, parallel=False):
    assert is_overload_constant_bool(raw
        ), 'raw argument should be constant bool'
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    kol__kugb = get_overload_const_str(fname)
    if kol__kugb not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (kol__kugb))
    if kol__kugb in ('median', 'min', 'max'):
        wgk__qrb = 'def kernel_func(A):\n'
        wgk__qrb += '  if np.isnan(A).sum() != 0: return np.nan\n'
        wgk__qrb += '  return np.{}(A)\n'.format(kol__kugb)
        aym__mco = {}
        exec(wgk__qrb, {'np': np}, aym__mco)
        kernel_func = register_jitable(aym__mco['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        kol__kugb]
    return (lambda arr, index_arr, win, minp, center, fname, raw=True,
        parallel=False: roll_fixed_linear_generic(arr, win, minp, center,
        parallel, init_kernel, add_kernel, remove_kernel, calc_kernel))


@overload(rolling_variable, no_unliteral=True)
def overload_rolling_variable(arr, on_arr, index_arr, win, minp, center,
    fname, raw=True, parallel=False):
    assert is_overload_constant_bool(raw)
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    kol__kugb = get_overload_const_str(fname)
    if kol__kugb not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(kol__kugb))
    if kol__kugb in ('median', 'min', 'max'):
        wgk__qrb = 'def kernel_func(A):\n'
        wgk__qrb += '  arr  = dropna(A)\n'
        wgk__qrb += '  if len(arr) == 0: return np.nan\n'
        wgk__qrb += '  return np.{}(arr)\n'.format(kol__kugb)
        aym__mco = {}
        exec(wgk__qrb, {'np': np, 'dropna': _dropna}, aym__mco)
        kernel_func = register_jitable(aym__mco['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        kol__kugb]
    return (lambda arr, on_arr, index_arr, win, minp, center, fname, raw=
        True, parallel=False: roll_var_linear_generic(arr, on_arr, win,
        minp, center, parallel, init_kernel, add_kernel, remove_kernel,
        calc_kernel))


def _get_apply_func(f_type):
    func = get_overload_const_func(f_type, None)
    return bodo.compiler.udf_jit(func)


comm_border_tag = 22


@register_jitable
def roll_fixed_linear_generic(in_arr, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data(in_arr, win, minp, center, rank,
                n_pes, init_data, add_obs, remove_obs, calc_out)
        sps__lzlxw = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            fsv__birp) = sps__lzlxw
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(fsv__birp, True)
            for uee__neg in range(0, halo_size):
                data = add_obs(r_recv_buff[uee__neg], *data)
                updk__gcu = in_arr[N + uee__neg - win]
                data = remove_obs(updk__gcu, *data)
                output[N + uee__neg - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for uee__neg in range(0, halo_size):
                data = add_obs(l_recv_buff[uee__neg], *data)
            for uee__neg in range(0, win - 1):
                data = add_obs(in_arr[uee__neg], *data)
                if uee__neg > offset:
                    updk__gcu = l_recv_buff[uee__neg - offset - 1]
                    data = remove_obs(updk__gcu, *data)
                if uee__neg >= offset:
                    output[uee__neg - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    dcuze__pxc = max(minp, 1) - 1
    dcuze__pxc = min(dcuze__pxc, N)
    for uee__neg in range(0, dcuze__pxc):
        data = add_obs(in_arr[uee__neg], *data)
        if uee__neg >= offset:
            output[uee__neg - offset] = calc_out(minp, *data)
    for uee__neg in range(dcuze__pxc, N):
        val = in_arr[uee__neg]
        data = add_obs(val, *data)
        if uee__neg > win - 1:
            updk__gcu = in_arr[uee__neg - win]
            data = remove_obs(updk__gcu, *data)
        output[uee__neg - offset] = calc_out(minp, *data)
    mtkje__tlak = data
    for uee__neg in range(N, N + offset):
        if uee__neg > win - 1:
            updk__gcu = in_arr[uee__neg - win]
            data = remove_obs(updk__gcu, *data)
        output[uee__neg - offset] = calc_out(minp, *data)
    return output, mtkje__tlak


def roll_fixed_apply(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    pass


@overload(roll_fixed_apply, no_unliteral=True)
def overload_roll_fixed_apply(in_arr, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_fixed_apply_impl


def roll_fixed_apply_impl(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    index_arr = fix_index_arr(index_arr)
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_apply(in_arr, index_arr, win, minp,
                center, rank, n_pes, kernel_func, raw)
        sps__lzlxw = _border_icomm(in_arr, rank, n_pes, halo_size, True, center
            )
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            fsv__birp) = sps__lzlxw
        if raw == False:
            kinev__uiww = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, noa__lpwcv, rwr__zjzo,
                lyncb__esf, jhw__qek) = kinev__uiww
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(rwr__zjzo, noa__lpwcv, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(fsv__birp, True)
            if raw == False:
                bodo.libs.distributed_api.wait(jhw__qek, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(lyncb__esf, True)
            recv_left_compute(output, in_arr, index_arr, win, minp, offset,
                l_recv_buff, l_recv_buff_idx, kernel_func, raw)
    return output


def recv_right_compute(output, in_arr, index_arr, N, win, minp, offset,
    r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_right_compute, no_unliteral=True)
def overload_recv_right_compute(output, in_arr, index_arr, N, win, minp,
    offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, N, win, minp, offset,
            r_recv_buff, r_recv_buff_idx, kernel_func, raw):
            mtkje__tlak = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            dbda__lqh = 0
            for uee__neg in range(max(N - offset, 0), N):
                data = mtkje__tlak[dbda__lqh:dbda__lqh + win]
                if win - np.isnan(data).sum() < minp:
                    output[uee__neg] = np.nan
                else:
                    output[uee__neg] = kernel_func(data)
                dbda__lqh += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        mtkje__tlak = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        lwcu__qntou = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx)
            )
        dbda__lqh = 0
        for uee__neg in range(max(N - offset, 0), N):
            data = mtkje__tlak[dbda__lqh:dbda__lqh + win]
            if win - np.isnan(data).sum() < minp:
                output[uee__neg] = np.nan
            else:
                output[uee__neg] = kernel_func(pd.Series(data, lwcu__qntou[
                    dbda__lqh:dbda__lqh + win]))
            dbda__lqh += 1
    return impl_series


def recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_left_compute, no_unliteral=True)
def overload_recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, win, minp, offset, l_recv_buff,
            l_recv_buff_idx, kernel_func, raw):
            mtkje__tlak = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for uee__neg in range(0, win - offset - 1):
                data = mtkje__tlak[uee__neg:uee__neg + win]
                if win - np.isnan(data).sum() < minp:
                    output[uee__neg] = np.nan
                else:
                    output[uee__neg] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        mtkje__tlak = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        lwcu__qntou = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for uee__neg in range(0, win - offset - 1):
            data = mtkje__tlak[uee__neg:uee__neg + win]
            if win - np.isnan(data).sum() < minp:
                output[uee__neg] = np.nan
            else:
                output[uee__neg] = kernel_func(pd.Series(data, lwcu__qntou[
                    uee__neg:uee__neg + win]))
    return impl_series


def roll_fixed_apply_seq(in_arr, index_arr, win, minp, center, kernel_func,
    raw=True):
    pass


@overload(roll_fixed_apply_seq, no_unliteral=True)
def overload_roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
    kernel_func, raw=True):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"

    def roll_fixed_apply_seq_impl(in_arr, index_arr, win, minp, center,
        kernel_func, raw=True):
        N = len(in_arr)
        output = np.empty(N, dtype=np.float64)
        offset = (win - 1) // 2 if center else 0
        for uee__neg in range(0, N):
            start = max(uee__neg - win + 1 + offset, 0)
            end = min(uee__neg + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[uee__neg] = np.nan
            else:
                output[uee__neg] = apply_func(kernel_func, data, index_arr,
                    start, end, raw)
        return output
    return roll_fixed_apply_seq_impl


def apply_func(kernel_func, data, index_arr, start, end, raw):
    return kernel_func(data)


@overload(apply_func, no_unliteral=True)
def overload_apply_func(kernel_func, data, index_arr, start, end, raw):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"
    if is_overload_true(raw):
        return (lambda kernel_func, data, index_arr, start, end, raw:
            kernel_func(data))
    return lambda kernel_func, data, index_arr, start, end, raw: kernel_func(pd
        .Series(data, index_arr[start:end]))


def fix_index_arr(A):
    return A


@overload(fix_index_arr)
def overload_fix_index_arr(A):
    if is_overload_none(A):
        return lambda A: np.zeros(3)
    return lambda A: A


def get_offset_nanos(w):
    out = status = 0
    try:
        out = pd.tseries.frequencies.to_offset(w).nanos
    except:
        status = 1
    return out, status


def offset_to_nanos(w):
    return w


@overload(offset_to_nanos)
def overload_offset_to_nanos(w):
    if isinstance(w, types.Integer):
        return lambda w: w

    def impl(w):
        with numba.objmode(out='int64', status='int64'):
            out, status = get_offset_nanos(w)
        if status != 0:
            raise ValueError('Invalid offset value')
        return out
    return impl


@register_jitable
def roll_var_linear_generic(in_arr, on_arr_dt, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable(in_arr, on_arr, win, minp,
                rank, n_pes, init_data, add_obs, remove_obs, calc_out)
        sps__lzlxw = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, ysmln__sbb, l_recv_req,
            emdwd__dphsv) = sps__lzlxw
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(ysmln__sbb, ysmln__sbb, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(emdwd__dphsv, True)
            num_zero_starts = 0
            for uee__neg in range(0, N):
                if start[uee__neg] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for ivfjt__gge in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[ivfjt__gge], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for uee__neg in range(1, num_zero_starts):
                s = recv_starts[uee__neg]
                lcioo__sluxf = end[uee__neg]
                for ivfjt__gge in range(recv_starts[uee__neg - 1], s):
                    data = remove_obs(l_recv_buff[ivfjt__gge], *data)
                for ivfjt__gge in range(end[uee__neg - 1], lcioo__sluxf):
                    data = add_obs(in_arr[ivfjt__gge], *data)
                output[uee__neg] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    jxj__icg = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    mpexz__mtfcd = jxj__icg[0] - win
    if left_closed:
        mpexz__mtfcd -= 1
    recv_starts[0] = halo_size
    for ivfjt__gge in range(0, halo_size):
        if l_recv_t_buff[ivfjt__gge] > mpexz__mtfcd:
            recv_starts[0] = ivfjt__gge
            break
    for uee__neg in range(1, num_zero_starts):
        mpexz__mtfcd = jxj__icg[uee__neg] - win
        if left_closed:
            mpexz__mtfcd -= 1
        recv_starts[uee__neg] = halo_size
        for ivfjt__gge in range(recv_starts[uee__neg - 1], halo_size):
            if l_recv_t_buff[ivfjt__gge] > mpexz__mtfcd:
                recv_starts[uee__neg] = ivfjt__gge
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for ivfjt__gge in range(start[0], end[0]):
        data = add_obs(in_arr[ivfjt__gge], *data)
    output[0] = calc_out(minp, *data)
    for uee__neg in range(1, N):
        s = start[uee__neg]
        lcioo__sluxf = end[uee__neg]
        for ivfjt__gge in range(start[uee__neg - 1], s):
            data = remove_obs(in_arr[ivfjt__gge], *data)
        for ivfjt__gge in range(end[uee__neg - 1], lcioo__sluxf):
            data = add_obs(in_arr[ivfjt__gge], *data)
        output[uee__neg] = calc_out(minp, *data)
    return output


def roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    pass


@overload(roll_variable_apply, no_unliteral=True)
def overload_roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_variable_apply_impl


def roll_variable_apply_impl(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    index_arr = fix_index_arr(index_arr)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable_apply(in_arr, on_arr,
                index_arr, win, minp, rank, n_pes, kernel_func, raw)
        sps__lzlxw = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, ysmln__sbb, l_recv_req,
            emdwd__dphsv) = sps__lzlxw
        if raw == False:
            kinev__uiww = _border_icomm_var(index_arr, on_arr, rank, n_pes, win
                )
            (l_recv_buff_idx, ted__ljz, rwr__zjzo, dbfem__mcpop, lyncb__esf,
                bdqci__vwm) = kinev__uiww
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(ysmln__sbb, ysmln__sbb, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(rwr__zjzo, rwr__zjzo, rank, n_pes, True, False)
            _border_send_wait(dbfem__mcpop, dbfem__mcpop, rank, n_pes, True,
                False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(emdwd__dphsv, True)
            if raw == False:
                bodo.libs.distributed_api.wait(lyncb__esf, True)
                bodo.libs.distributed_api.wait(bdqci__vwm, True)
            num_zero_starts = 0
            for uee__neg in range(0, N):
                if start[uee__neg] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            recv_left_var_compute(output, in_arr, index_arr,
                num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx,
                minp, kernel_func, raw)
    return output


def recv_left_var_compute(output, in_arr, index_arr, num_zero_starts,
    recv_starts, l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
    pass


@overload(recv_left_var_compute)
def overload_recv_left_var_compute(output, in_arr, index_arr,
    num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx, minp,
    kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, num_zero_starts, recv_starts,
            l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
            for uee__neg in range(0, num_zero_starts):
                hzmhq__hwl = recv_starts[uee__neg]
                ukm__eibab = np.concatenate((l_recv_buff[hzmhq__hwl:],
                    in_arr[:uee__neg + 1]))
                if len(ukm__eibab) - np.isnan(ukm__eibab).sum() >= minp:
                    output[uee__neg] = kernel_func(ukm__eibab)
                else:
                    output[uee__neg] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for uee__neg in range(0, num_zero_starts):
            hzmhq__hwl = recv_starts[uee__neg]
            ukm__eibab = np.concatenate((l_recv_buff[hzmhq__hwl:], in_arr[:
                uee__neg + 1]))
            smgv__wtryp = np.concatenate((l_recv_buff_idx[hzmhq__hwl:],
                index_arr[:uee__neg + 1]))
            if len(ukm__eibab) - np.isnan(ukm__eibab).sum() >= minp:
                output[uee__neg] = kernel_func(pd.Series(ukm__eibab,
                    smgv__wtryp))
            else:
                output[uee__neg] = np.nan
    return impl_series


def roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp, start,
    end, kernel_func, raw):
    pass


@overload(roll_variable_apply_seq)
def overload_roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):
        return roll_variable_apply_seq_impl
    return roll_variable_apply_seq_impl_series


def roll_variable_apply_seq_impl(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for uee__neg in range(0, N):
        s = start[uee__neg]
        lcioo__sluxf = end[uee__neg]
        data = in_arr[s:lcioo__sluxf]
        if lcioo__sluxf - s - np.isnan(data).sum() >= minp:
            output[uee__neg] = kernel_func(data)
        else:
            output[uee__neg] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for uee__neg in range(0, N):
        s = start[uee__neg]
        lcioo__sluxf = end[uee__neg]
        data = in_arr[s:lcioo__sluxf]
        if lcioo__sluxf - s - np.isnan(data).sum() >= minp:
            output[uee__neg] = kernel_func(pd.Series(data, index_arr[s:
                lcioo__sluxf]))
        else:
            output[uee__neg] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    jxj__icg = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for uee__neg in range(1, N):
        yba__rtgf = jxj__icg[uee__neg]
        mpexz__mtfcd = jxj__icg[uee__neg] - win
        if left_closed:
            mpexz__mtfcd -= 1
        start[uee__neg] = uee__neg
        for ivfjt__gge in range(start[uee__neg - 1], uee__neg):
            if jxj__icg[ivfjt__gge] > mpexz__mtfcd:
                start[uee__neg] = ivfjt__gge
                break
        if jxj__icg[end[uee__neg - 1]] <= yba__rtgf:
            end[uee__neg] = uee__neg + 1
        else:
            end[uee__neg] = end[uee__neg - 1]
        if not right_closed:
            end[uee__neg] -= 1
    return start, end


@register_jitable
def init_data_sum():
    return 0, 0.0


@register_jitable
def add_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
    return nobs, sum_x


@register_jitable
def remove_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
    return nobs, sum_x


@register_jitable
def calc_sum(minp, nobs, sum_x):
    return sum_x if nobs >= minp else np.nan


@register_jitable
def init_data_mean():
    return 0, 0.0, 0


@register_jitable
def add_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
        if val < 0:
            neg_ct += 1
    return nobs, sum_x, neg_ct


@register_jitable
def remove_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
        if val < 0:
            neg_ct -= 1
    return nobs, sum_x, neg_ct


@register_jitable
def calc_mean(minp, nobs, sum_x, neg_ct):
    if nobs >= minp:
        mqhcc__yookq = sum_x / nobs
        if neg_ct == 0 and mqhcc__yookq < 0.0:
            mqhcc__yookq = 0
        elif neg_ct == nobs and mqhcc__yookq > 0.0:
            mqhcc__yookq = 0
    else:
        mqhcc__yookq = np.nan
    return mqhcc__yookq


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        ssv__ubyy = val - mean_x
        mean_x += ssv__ubyy / nobs
        ssqdm_x += (nobs - 1) * ssv__ubyy ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            ssv__ubyy = val - mean_x
            mean_x -= ssv__ubyy / nobs
            ssqdm_x -= (nobs + 1) * ssv__ubyy ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    nujvu__glel = 1.0
    mqhcc__yookq = np.nan
    if nobs >= minp and nobs > nujvu__glel:
        if nobs == 1:
            mqhcc__yookq = 0.0
        else:
            mqhcc__yookq = ssqdm_x / (nobs - nujvu__glel)
            if mqhcc__yookq < 0.0:
                mqhcc__yookq = 0.0
    return mqhcc__yookq


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    zkzu__dpyyx = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(zkzu__dpyyx)


@register_jitable
def init_data_count():
    return 0.0,


@register_jitable
def add_count(val, count_x):
    if not np.isnan(val):
        count_x += 1.0
    return count_x,


@register_jitable
def remove_count(val, count_x):
    if not np.isnan(val):
        count_x -= 1.0
    return count_x,


@register_jitable
def calc_count(minp, count_x):
    return count_x


@register_jitable
def calc_count_var(minp, count_x):
    return count_x if count_x >= minp else np.nan


linear_kernels = {'sum': (init_data_sum, add_sum, remove_sum, calc_sum),
    'mean': (init_data_mean, add_mean, remove_mean, calc_mean), 'var': (
    init_data_var, add_var, remove_var, calc_var), 'std': (init_data_var,
    add_var, remove_var, calc_std), 'count': (init_data_count, add_count,
    remove_count, calc_count)}


def shift():
    return


@overload(shift, jit_options={'cache': True})
def shift_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return shift_impl


def shift_impl(in_arr, shift, parallel):
    N = len(in_arr)
    in_arr = decode_if_dict_array(in_arr)
    output = alloc_shift(N, in_arr, (-1,))
    send_right = shift > 0
    send_left = shift <= 0
    is_parallel_str = False
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_shift(in_arr, shift, rank, n_pes)
        sps__lzlxw = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            fsv__birp) = sps__lzlxw
        if send_right and is_str_binary_array(in_arr):
            is_parallel_str = True
            shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
                l_recv_req, l_recv_buff, output)
    shift_seq(in_arr, shift, output, is_parallel_str)
    if parallel:
        if send_right:
            if not is_str_binary_array(in_arr):
                shift_left_recv(r_send_req, l_send_req, rank, n_pes,
                    halo_size, l_recv_req, l_recv_buff, output)
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(fsv__birp, True)
                for uee__neg in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, uee__neg):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            uee__neg)
                        continue
                    output[N - halo_size + uee__neg] = r_recv_buff[uee__neg]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False):
    N = len(in_arr)
    gzu__ogy = 1 if shift > 0 else -1
    shift = gzu__ogy * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    start = max(shift, 0)
    end = min(N, N + shift)
    for uee__neg in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, uee__neg - shift):
            bodo.libs.array_kernels.setna(output, uee__neg)
            continue
        output[uee__neg] = in_arr[uee__neg - shift]
    if shift < 0:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for uee__neg in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, uee__neg):
                bodo.libs.array_kernels.setna(output, uee__neg)
                continue
            output[uee__neg] = l_recv_buff[uee__neg]


def is_str_binary_array(arr):
    return False


@overload(is_str_binary_array)
def overload_is_str_binary_array(arr):
    if arr in [bodo.string_array_type, bodo.binary_array_type]:
        return lambda arr: True
    return lambda arr: False


def is_supported_shift_array_type(arr_type):
    return isinstance(arr_type, types.Array) and (isinstance(arr_type.dtype,
        types.Number) or arr_type.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]) or isinstance(arr_type, (bodo.IntegerArrayType,
        bodo.DecimalArrayType)) or arr_type in (bodo.boolean_array, bodo.
        datetime_date_array_type, bodo.string_array_type, bodo.
        binary_array_type, bodo.dict_str_arr_type)


def pct_change():
    return


@overload(pct_change, jit_options={'cache': True})
def pct_change_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return pct_change_impl


def pct_change_impl(in_arr, shift, parallel):
    N = len(in_arr)
    send_right = shift > 0
    send_left = shift <= 0
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_pct_change(in_arr, shift, rank, n_pes)
        sps__lzlxw = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            fsv__birp) = sps__lzlxw
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for uee__neg in range(0, halo_size):
                    ouvab__oeplp = l_recv_buff[uee__neg]
                    output[uee__neg] = (in_arr[uee__neg] - ouvab__oeplp
                        ) / ouvab__oeplp
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(fsv__birp, True)
                for uee__neg in range(0, halo_size):
                    ouvab__oeplp = r_recv_buff[uee__neg]
                    output[N - halo_size + uee__neg] = (in_arr[N -
                        halo_size + uee__neg] - ouvab__oeplp) / ouvab__oeplp
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    pta__guy = np.nan
    if arr.dtype == types.float32:
        pta__guy = np.float32('nan')

    def impl(arr):
        for uee__neg in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, uee__neg):
                return arr[uee__neg]
        return pta__guy
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    pta__guy = np.nan
    if arr.dtype == types.float32:
        pta__guy = np.float32('nan')

    def impl(arr):
        lmmm__kjlca = len(arr)
        for uee__neg in range(len(arr)):
            dbda__lqh = lmmm__kjlca - uee__neg - 1
            if not bodo.libs.array_kernels.isna(arr, dbda__lqh):
                return arr[dbda__lqh]
        return pta__guy
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    gzu__ogy = 1 if shift > 0 else -1
    shift = gzu__ogy * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        tjpg__xgf = get_first_non_na(in_arr[:shift])
        ozqms__dbonu = get_last_non_na(in_arr[:shift])
    else:
        tjpg__xgf = get_last_non_na(in_arr[:-shift])
        ozqms__dbonu = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for uee__neg in range(start, end):
        ouvab__oeplp = in_arr[uee__neg - shift]
        if np.isnan(ouvab__oeplp):
            ouvab__oeplp = tjpg__xgf
        else:
            tjpg__xgf = ouvab__oeplp
        val = in_arr[uee__neg]
        if np.isnan(val):
            val = ozqms__dbonu
        else:
            ozqms__dbonu = val
        output[uee__neg] = val / ouvab__oeplp - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    rufum__qbdy = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), rufum__qbdy, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), rufum__qbdy, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), rufum__qbdy, True)
    if send_left and rank != n_pes - 1:
        fsv__birp = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), rufum__qbdy, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        fsv__birp)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    rufum__qbdy = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for ivfjt__gge in range(-2, -N, -1):
        fnlku__qhder = on_arr[ivfjt__gge]
        if end - fnlku__qhder >= win_size:
            halo_size = -ivfjt__gge
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1),
            rufum__qbdy)
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), rufum__qbdy, True)
        ysmln__sbb = bodo.libs.distributed_api.isend(on_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), rufum__qbdy, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), rufum__qbdy)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), rufum__qbdy, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        emdwd__dphsv = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.
            int32(halo_size), np.int32(rank - 1), rufum__qbdy, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, ysmln__sbb, l_recv_req,
        emdwd__dphsv)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    biv__jlhh = bodo.libs.distributed_api.dist_reduce(int(N <= 2 *
        halo_size + 1), np.int32(Reduce_Type.Sum.value))
    return biv__jlhh != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    vcam__pqnr = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    ihx__nvzm = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        wmu__jvptq, brcnj__zgjrn = roll_fixed_linear_generic_seq(ihx__nvzm,
            win, minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        wmu__jvptq = np.empty(vcam__pqnr, np.float64)
    bodo.libs.distributed_api.bcast(wmu__jvptq)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return wmu__jvptq[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    vcam__pqnr = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    ihx__nvzm = bodo.libs.distributed_api.gatherv(in_arr)
    cnidn__mvc = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        wmu__jvptq = roll_fixed_apply_seq(ihx__nvzm, cnidn__mvc, win, minp,
            center, kernel_func, raw)
    else:
        wmu__jvptq = np.empty(vcam__pqnr, np.float64)
    bodo.libs.distributed_api.bcast(wmu__jvptq)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return wmu__jvptq[start:end]


def bcast_n_chars_if_str_binary_arr(arr):
    pass


@overload(bcast_n_chars_if_str_binary_arr)
def overload_bcast_n_chars_if_str_binary_arr(arr):
    if arr in [bodo.binary_array_type, bodo.string_array_type]:

        def impl(arr):
            return bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.
                libs.str_arr_ext.num_total_chars(arr)))
        return impl
    return lambda arr: -1


@register_jitable
def _handle_small_data_shift(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    vcam__pqnr = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    ihx__nvzm = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        wmu__jvptq = alloc_shift(len(ihx__nvzm), ihx__nvzm, (-1,))
        shift_seq(ihx__nvzm, shift, wmu__jvptq)
        imuyq__ifme = bcast_n_chars_if_str_binary_arr(wmu__jvptq)
    else:
        imuyq__ifme = bcast_n_chars_if_str_binary_arr(in_arr)
        wmu__jvptq = alloc_shift(vcam__pqnr, in_arr, (imuyq__ifme,))
    bodo.libs.distributed_api.bcast(wmu__jvptq)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return wmu__jvptq[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    vcam__pqnr = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ihx__nvzm = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        wmu__jvptq = pct_change_seq(ihx__nvzm, shift)
    else:
        wmu__jvptq = alloc_pct_change(vcam__pqnr, in_arr)
    bodo.libs.distributed_api.bcast(wmu__jvptq)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return wmu__jvptq[start:end]


def cast_dt64_arr_to_int(arr):
    return arr


@infer_global(cast_dt64_arr_to_int)
class DtArrToIntType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        assert args[0] == types.Array(types.NPDatetime('ns'), 1, 'C') or args[0
            ] == types.Array(types.int64, 1, 'C')
        return signature(types.Array(types.int64, 1, 'C'), *args)


@lower_builtin(cast_dt64_arr_to_int, types.Array(types.NPDatetime('ns'), 1,
    'C'))
@lower_builtin(cast_dt64_arr_to_int, types.Array(types.int64, 1, 'C'))
def lower_cast_dt64_arr_to_int(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@register_jitable
def _is_small_for_parallel_variable(on_arr, win_size):
    if len(on_arr) < 2:
        pkt__bhtxd = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        fuffc__xgk = end - start
        pkt__bhtxd = int(fuffc__xgk <= win_size)
    biv__jlhh = bodo.libs.distributed_api.dist_reduce(pkt__bhtxd, np.int32(
        Reduce_Type.Sum.value))
    return biv__jlhh != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    vcam__pqnr = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ihx__nvzm = bodo.libs.distributed_api.gatherv(in_arr)
    sgy__nip = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(sgy__nip, vcam__pqnr, win, False, True)
        wmu__jvptq = roll_var_linear_generic_seq(ihx__nvzm, sgy__nip, win,
            minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        wmu__jvptq = np.empty(vcam__pqnr, np.float64)
    bodo.libs.distributed_api.bcast(wmu__jvptq)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return wmu__jvptq[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    vcam__pqnr = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ihx__nvzm = bodo.libs.distributed_api.gatherv(in_arr)
    sgy__nip = bodo.libs.distributed_api.gatherv(on_arr)
    cnidn__mvc = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(sgy__nip, vcam__pqnr, win, False, True)
        wmu__jvptq = roll_variable_apply_seq(ihx__nvzm, sgy__nip,
            cnidn__mvc, win, minp, start, end, kernel_func, raw)
    else:
        wmu__jvptq = np.empty(vcam__pqnr, np.float64)
    bodo.libs.distributed_api.bcast(wmu__jvptq)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return wmu__jvptq[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    ewesv__soe = len(arr)
    hrhc__fgq = ewesv__soe - np.isnan(arr).sum()
    A = np.empty(hrhc__fgq, arr.dtype)
    dig__tjtqp = 0
    for uee__neg in range(ewesv__soe):
        val = arr[uee__neg]
        if not np.isnan(val):
            A[dig__tjtqp] = val
            dig__tjtqp += 1
    return A


def alloc_shift(n, A, s=None):
    return np.empty(n, A.dtype)


@overload(alloc_shift, no_unliteral=True)
def alloc_shift_overload(n, A, s=None):
    if not isinstance(A, types.Array):
        return lambda n, A, s=None: bodo.utils.utils.alloc_type(n, A, s)
    if isinstance(A.dtype, types.Integer):
        return lambda n, A, s=None: np.empty(n, np.float64)
    return lambda n, A, s=None: np.empty(n, A.dtype)


def alloc_pct_change(n, A):
    return np.empty(n, A.dtype)


@overload(alloc_pct_change, no_unliteral=True)
def alloc_pct_change_overload(n, A):
    if isinstance(A.dtype, types.Integer):
        return lambda n, A: np.empty(n, np.float64)
    return lambda n, A: np.empty(n, A.dtype)


def prep_values(A):
    return A.astype('float64')


@overload(prep_values, no_unliteral=True)
def prep_values_overload(A):
    if A == types.Array(types.float64, 1, 'C'):
        return lambda A: A
    return lambda A: A.astype(np.float64)


@register_jitable
def _validate_roll_fixed_args(win, minp):
    if win < 0:
        raise ValueError('window must be non-negative')
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if minp > win:
        raise ValueError('min_periods must be <= window')


@register_jitable
def _validate_roll_var_args(minp, center):
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if center:
        raise NotImplementedError(
            'rolling: center is not implemented for datetimelike and offset based windows'
            )
