"""
Support for Series.str methods
"""
import operator
import re
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.split_impl import get_split_view_data_ptr, get_split_view_index, string_array_split_view_type
from bodo.libs.array import get_search_regex
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.str_arr_ext import get_utf8_size, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import str_findall_count
from bodo.utils.typing import BodoError, create_unsupported_overload, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_str_len, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error


class SeriesStrMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        mzetq__sccrf = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(mzetq__sccrf)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yahky__tpew = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, yahky__tpew)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        jcvpb__mmntt, = args
        jtr__syopa = signature.return_type
        julh__gztyh = cgutils.create_struct_proxy(jtr__syopa)(context, builder)
        julh__gztyh.obj = jcvpb__mmntt
        context.nrt.incref(builder, signature.args[0], jcvpb__mmntt)
        return julh__gztyh._getvalue()
    return SeriesStrMethodType(obj)(obj), codegen


def str_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.UnicodeType) and not is_overload_constant_str(
        arg):
        raise_bodo_error(
            "Series.str.{}(): parameter '{}' expected a string object, not {}"
            .format(func_name, arg_name, arg))


def int_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.Integer) and not is_overload_constant_int(arg
        ):
        raise BodoError(
            "Series.str.{}(): parameter '{}' expected an int object, not {}"
            .format(func_name, arg_name, arg))


def not_supported_arg_check(func_name, arg_name, arg, defval):
    if arg_name == 'na':
        if not isinstance(arg, types.Omitted) and (not isinstance(arg,
            float) or not np.isnan(arg)):
            raise BodoError(
                "Series.str.{}(): parameter '{}' is not supported, default: np.nan"
                .format(func_name, arg_name))
    elif not isinstance(arg, types.Omitted) and arg != defval:
        raise BodoError(
            "Series.str.{}(): parameter '{}' is not supported, default: {}"
            .format(func_name, arg_name, defval))


def common_validate_padding(func_name, width, fillchar):
    if is_overload_constant_str(fillchar):
        if get_overload_const_str_len(fillchar) != 1:
            raise BodoError(
                'Series.str.{}(): fillchar must be a character, not str'.
                format(func_name))
    elif not isinstance(fillchar, types.UnicodeType):
        raise BodoError('Series.str.{}(): fillchar must be a character, not {}'
            .format(func_name, fillchar))
    int_arg_check(func_name, 'width', width)


@overload_attribute(SeriesType, 'str')
def overload_series_str(S):
    if not (is_str_arr_type(S.data) or S.data ==
        string_array_split_view_type or isinstance(S.data, ArrayItemArrayType)
        ):
        raise_bodo_error(
            'Series.str: input should be a series of string or arrays')
    return lambda S: bodo.hiframes.series_str_impl.init_series_str_method(S)


@overload_method(SeriesStrMethodType, 'len', inline='always', no_unliteral=True
    )
def overload_str_method_len(S_str):

    def impl(S_str):
        S = S_str._obj
        deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(deibv__vbv, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'split', inline='always',
    no_unliteral=True)
def overload_str_method_split(S_str, pat=None, n=-1, expand=False):
    if not is_overload_none(pat):
        str_arg_check('split', 'pat', pat)
    int_arg_check('split', 'n', n)
    not_supported_arg_check('split', 'expand', expand, False)
    if is_overload_constant_str(pat) and len(get_overload_const_str(pat)
        ) == 1 and get_overload_const_str(pat).isascii(
        ) and is_overload_constant_int(n) and get_overload_const_int(n
        ) == -1 and S_str.stype.data == string_array_type:

        def _str_split_view_impl(S_str, pat=None, n=-1, expand=False):
            S = S_str._obj
            deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
            kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
            mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(deibv__vbv,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kzm__lttz, mzetq__sccrf)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(deibv__vbv, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    vgx__qmih = S_str.stype.data
    if (vgx__qmih != string_array_split_view_type and not is_str_arr_type(
        vgx__qmih)) and not isinstance(vgx__qmih, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(vgx__qmih, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
            kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
            mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(deibv__vbv, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kzm__lttz, mzetq__sccrf)
        return _str_get_array_impl
    if vgx__qmih == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
            kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
            mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(deibv__vbv)
            clgd__ppmi = 0
            for zbjeo__ncvu in numba.parfors.parfor.internal_prange(n):
                gypm__pyf, gypm__pyf, qoojj__pdmny = get_split_view_index(
                    deibv__vbv, zbjeo__ncvu, i)
                clgd__ppmi += qoojj__pdmny
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, clgd__ppmi)
            for bgtzl__ewaky in numba.parfors.parfor.internal_prange(n):
                wwotd__yqpy, exdo__sao, qoojj__pdmny = get_split_view_index(
                    deibv__vbv, bgtzl__ewaky, i)
                if wwotd__yqpy == 0:
                    bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
                    wfr__huh = get_split_view_data_ptr(deibv__vbv, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        bgtzl__ewaky)
                    wfr__huh = get_split_view_data_ptr(deibv__vbv, exdo__sao)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    bgtzl__ewaky, wfr__huh, qoojj__pdmny)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kzm__lttz, mzetq__sccrf)
        return _str_get_split_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(deibv__vbv)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(deibv__vbv, bgtzl__ewaky
                ) or not len(deibv__vbv[bgtzl__ewaky]) > i >= -len(deibv__vbv
                [bgtzl__ewaky]):
                out_arr[bgtzl__ewaky] = ''
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
            else:
                out_arr[bgtzl__ewaky] = deibv__vbv[bgtzl__ewaky][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    vgx__qmih = S_str.stype.data
    if (vgx__qmih != string_array_split_view_type and vgx__qmih !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        vgx__qmih)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(jyr__qro)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                out_arr[bgtzl__ewaky] = ''
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
            else:
                wkcs__lfuz = jyr__qro[bgtzl__ewaky]
                out_arr[bgtzl__ewaky] = sep.join(wkcs__lfuz)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'replace', inline='always',
    no_unliteral=True)
def overload_str_method_replace(S_str, pat, repl, n=-1, case=None, flags=0,
    regex=True):
    not_supported_arg_check('replace', 'n', n, -1)
    not_supported_arg_check('replace', 'case', case, None)
    str_arg_check('replace', 'pat', pat)
    str_arg_check('replace', 'repl', repl)
    int_arg_check('replace', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_replace_dict_impl(S_str, pat, repl, n=-1, case=None, flags
            =0, regex=True):
            S = S_str._obj
            deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
            kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
            mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(deibv__vbv, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kzm__lttz, mzetq__sccrf)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
            kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
            mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            yqhvm__eeabs = re.compile(pat, flags)
            tcsxf__prh = len(deibv__vbv)
            out_arr = pre_alloc_string_array(tcsxf__prh, -1)
            for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh
                ):
                if bodo.libs.array_kernels.isna(deibv__vbv, bgtzl__ewaky):
                    out_arr[bgtzl__ewaky] = ''
                    bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
                    continue
                out_arr[bgtzl__ewaky] = yqhvm__eeabs.sub(repl, deibv__vbv[
                    bgtzl__ewaky])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kzm__lttz, mzetq__sccrf)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(deibv__vbv)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(tcsxf__prh, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(deibv__vbv, bgtzl__ewaky):
                out_arr[bgtzl__ewaky] = ''
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
                continue
            out_arr[bgtzl__ewaky] = deibv__vbv[bgtzl__ewaky].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    wiey__dpajm = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(ljqsr__nslv in pat) for ljqsr__nslv in wiey__dpajm])
    else:
        return True


@overload_method(SeriesStrMethodType, 'contains', no_unliteral=True)
def overload_str_method_contains(S_str, pat, case=True, flags=0, na=np.nan,
    regex=True):
    not_supported_arg_check('contains', 'na', na, np.nan)
    str_arg_check('contains', 'pat', pat)
    int_arg_check('contains', 'flags', flags)
    if not is_overload_constant_bool(regex):
        raise BodoError(
            "Series.str.contains(): 'regex' argument should be a constant boolean"
            )
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.contains(): 'case' argument should be a constant boolean"
            )
    xjj__rmau = re.IGNORECASE.value
    sby__ycugp = 'def impl(\n'
    sby__ycugp += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    sby__ycugp += '):\n'
    sby__ycugp += '  S = S_str._obj\n'
    sby__ycugp += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    sby__ycugp += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    sby__ycugp += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    sby__ycugp += '  l = len(arr)\n'
    sby__ycugp += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                sby__ycugp += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                sby__ycugp += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            sby__ycugp += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        sby__ycugp += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        sby__ycugp += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            sby__ycugp += '  upper_pat = pat.upper()\n'
        sby__ycugp += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        sby__ycugp += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        sby__ycugp += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        sby__ycugp += '      else: \n'
        if is_overload_true(case):
            sby__ycugp += '          out_arr[i] = pat in arr[i]\n'
        else:
            sby__ycugp += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    sby__ycugp += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zrukk__gog = {}
    exec(sby__ycugp, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': xjj__rmau, 'get_search_regex':
        get_search_regex}, zrukk__gog)
    impl = zrukk__gog['impl']
    return impl


@overload_method(SeriesStrMethodType, 'cat', no_unliteral=True)
def overload_str_method_cat(S_str, others=None, sep=None, na_rep=None, join
    ='left'):
    if not isinstance(others, DataFrameType):
        raise_bodo_error(
            "Series.str.cat(): 'others' must be a DataFrame currently")
    if not is_overload_none(sep):
        str_arg_check('cat', 'sep', sep)
    if not is_overload_constant_str(join) or get_overload_const_str(join
        ) != 'left':
        raise_bodo_error("Series.str.cat(): 'join' not supported yet")
    sby__ycugp = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    sby__ycugp += '  S = S_str._obj\n'
    sby__ycugp += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    sby__ycugp += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    sby__ycugp += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    sby__ycugp += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        sby__ycugp += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(fgaox__rhuk ==
        bodo.dict_str_arr_type for fgaox__rhuk in others.data):
        vkvel__iiosg = ', '.join(f'data{i}' for i in range(len(others.columns))
            )
        sby__ycugp += f"""  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {vkvel__iiosg}), sep)
"""
    else:
        sekb__vsq = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        sby__ycugp += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        sby__ycugp += '  numba.parfors.parfor.init_prange()\n'
        sby__ycugp += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        sby__ycugp += f'      if {sekb__vsq}:\n'
        sby__ycugp += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        sby__ycugp += '          continue\n'
        yoql__ouxx = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        rej__mdn = "''" if is_overload_none(sep) else 'sep'
        sby__ycugp += f'      out_arr[i] = {rej__mdn}.join([{yoql__ouxx}])\n'
    sby__ycugp += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zrukk__gog = {}
    exec(sby__ycugp, {'bodo': bodo, 'numba': numba}, zrukk__gog)
    impl = zrukk__gog['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        yqhvm__eeabs = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(tcsxf__prh, np.int64)
        for i in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(yqhvm__eeabs, jyr__qro[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(tcsxf__prh, np.int64)
        for i in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = jyr__qro[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'rfind', inline='always',
    no_unliteral=True)
def overload_str_method_rfind(S_str, sub, start=0, end=None):
    str_arg_check('rfind', 'sub', sub)
    if start != 0:
        int_arg_check('rfind', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rfind', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(tcsxf__prh, np.int64)
        for i in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = jyr__qro[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'center', inline='always',
    no_unliteral=True)
def overload_str_method_center(S_str, width, fillchar=' '):
    common_validate_padding('center', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tcsxf__prh, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                out_arr[bgtzl__ewaky] = ''
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
            else:
                out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'slice_replace', inline='always',
    no_unliteral=True)
def overload_str_method_slice_replace(S_str, start=0, stop=None, repl=''):
    int_arg_check('slice_replace', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice_replace', 'stop', stop)
    str_arg_check('slice_replace', 'repl', repl)

    def impl(S_str, start=0, stop=None, repl=''):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tcsxf__prh, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
            else:
                if stop is not None:
                    mfr__obk = jyr__qro[bgtzl__ewaky][stop:]
                else:
                    mfr__obk = ''
                out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky][:start
                    ] + repl + mfr__obk
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):

        def impl(S_str, repeats):
            S = S_str._obj
            jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
            mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
            kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            tcsxf__prh = len(jyr__qro)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tcsxf__prh,
                -1)
            for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh
                ):
                if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                    bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
                else:
                    out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kzm__lttz, mzetq__sccrf)
        return impl
    elif is_overload_constant_list(repeats):
        fpww__tdspz = get_overload_const_list(repeats)
        all__ucp = all([isinstance(hwuyq__zkjsn, int) for hwuyq__zkjsn in
            fpww__tdspz])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        all__ucp = True
    else:
        all__ucp = False
    if all__ucp:

        def impl(S_str, repeats):
            S = S_str._obj
            jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
            mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
            kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
            qkpv__epv = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            tcsxf__prh = len(jyr__qro)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tcsxf__prh,
                -1)
            for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh
                ):
                if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                    bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
                else:
                    out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky] * qkpv__epv[
                        bgtzl__ewaky]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kzm__lttz, mzetq__sccrf)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


@overload_method(SeriesStrMethodType, 'ljust', inline='always',
    no_unliteral=True)
def overload_str_method_ljust(S_str, width, fillchar=' '):
    common_validate_padding('ljust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tcsxf__prh, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                out_arr[bgtzl__ewaky] = ''
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
            else:
                out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky].ljust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'rjust', inline='always',
    no_unliteral=True)
def overload_str_method_rjust(S_str, width, fillchar=' '):
    common_validate_padding('rjust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tcsxf__prh, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                out_arr[bgtzl__ewaky] = ''
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
            else:
                out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky].rjust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tcsxf__prh, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                out_arr[bgtzl__ewaky] = ''
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
            elif side == 'left':
                out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)

    def impl(S_str, width):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tcsxf__prh, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                out_arr[bgtzl__ewaky] = ''
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
            else:
                out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(tcsxf__prh, -1)
        for bgtzl__ewaky in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, bgtzl__ewaky):
                out_arr[bgtzl__ewaky] = ''
                bodo.libs.array_kernels.setna(out_arr, bgtzl__ewaky)
            else:
                out_arr[bgtzl__ewaky] = jyr__qro[bgtzl__ewaky][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
            kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
            mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(deibv__vbv, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kzm__lttz, mzetq__sccrf)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(tcsxf__prh)
        for i in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = jyr__qro[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
            kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
            mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(deibv__vbv, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kzm__lttz, mzetq__sccrf)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        jyr__qro = bodo.hiframes.pd_series_ext.get_series_data(S)
        mzetq__sccrf = bodo.hiframes.pd_series_ext.get_series_name(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        tcsxf__prh = len(jyr__qro)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(tcsxf__prh)
        for i in numba.parfors.parfor.internal_prange(tcsxf__prh):
            if bodo.libs.array_kernels.isna(jyr__qro, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = jyr__qro[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kzm__lttz,
            mzetq__sccrf)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_str_method_getitem(S_str, ind):
    if not isinstance(S_str, SeriesStrMethodType):
        return
    if not isinstance(types.unliteral(ind), (types.SliceType, types.Integer)):
        raise BodoError(
            'index input to Series.str[] should be a slice or an integer')
    if isinstance(ind, types.SliceType):
        return lambda S_str, ind: S_str.slice(ind.start, ind.stop, ind.step)
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda S_str, ind: S_str.get(ind)


@overload_method(SeriesStrMethodType, 'extract', inline='always',
    no_unliteral=True)
def overload_str_method_extract(S_str, pat, flags=0, expand=True):
    if not is_overload_constant_bool(expand):
        raise BodoError(
            "Series.str.extract(): 'expand' argument should be a constant bool"
            )
    lwwgf__ewwk, regex = _get_column_names_from_regex(pat, flags, 'extract')
    pwx__mjn = len(lwwgf__ewwk)
    sby__ycugp = 'def impl(S_str, pat, flags=0, expand=True):\n'
    sby__ycugp += '  regex = re.compile(pat, flags=flags)\n'
    sby__ycugp += '  S = S_str._obj\n'
    sby__ycugp += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    sby__ycugp += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    sby__ycugp += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    sby__ycugp += '  numba.parfors.parfor.init_prange()\n'
    sby__ycugp += '  n = len(str_arr)\n'
    for i in range(pwx__mjn):
        sby__ycugp += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    sby__ycugp += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    sby__ycugp += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(pwx__mjn):
        sby__ycugp += "          out_arr_{}[j] = ''\n".format(i)
        sby__ycugp += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    sby__ycugp += '      else:\n'
    sby__ycugp += '          m = regex.search(str_arr[j])\n'
    sby__ycugp += '          if m:\n'
    sby__ycugp += '            g = m.groups()\n'
    for i in range(pwx__mjn):
        sby__ycugp += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    sby__ycugp += '          else:\n'
    for i in range(pwx__mjn):
        sby__ycugp += "            out_arr_{}[j] = ''\n".format(i)
        sby__ycugp += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        mzetq__sccrf = "'{}'".format(list(regex.groupindex.keys()).pop()
            ) if len(regex.groupindex.keys()) > 0 else 'name'
        sby__ycugp += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(mzetq__sccrf))
        zrukk__gog = {}
        exec(sby__ycugp, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, zrukk__gog)
        impl = zrukk__gog['impl']
        return impl
    fespl__mlj = ', '.join('out_arr_{}'.format(i) for i in range(pwx__mjn))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(sby__ycugp,
        lwwgf__ewwk, fespl__mlj, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    lwwgf__ewwk, gypm__pyf = _get_column_names_from_regex(pat, flags,
        'extractall')
    pwx__mjn = len(lwwgf__ewwk)
    lbbnj__rhi = isinstance(S_str.stype.index, StringIndexType)
    sby__ycugp = 'def impl(S_str, pat, flags=0):\n'
    sby__ycugp += '  regex = re.compile(pat, flags=flags)\n'
    sby__ycugp += '  S = S_str._obj\n'
    sby__ycugp += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    sby__ycugp += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    sby__ycugp += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    sby__ycugp += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    sby__ycugp += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    sby__ycugp += '  numba.parfors.parfor.init_prange()\n'
    sby__ycugp += '  n = len(str_arr)\n'
    sby__ycugp += '  out_n_l = [0]\n'
    for i in range(pwx__mjn):
        sby__ycugp += '  num_chars_{} = 0\n'.format(i)
    if lbbnj__rhi:
        sby__ycugp += '  index_num_chars = 0\n'
    sby__ycugp += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if lbbnj__rhi:
        sby__ycugp += '      index_num_chars += get_utf8_size(index_arr[i])\n'
    sby__ycugp += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    sby__ycugp += '          continue\n'
    sby__ycugp += '      m = regex.findall(str_arr[i])\n'
    sby__ycugp += '      out_n_l[0] += len(m)\n'
    for i in range(pwx__mjn):
        sby__ycugp += '      l_{} = 0\n'.format(i)
    sby__ycugp += '      for s in m:\n'
    for i in range(pwx__mjn):
        sby__ycugp += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if pwx__mjn > 1 else '')
    for i in range(pwx__mjn):
        sby__ycugp += '      num_chars_{0} += l_{0}\n'.format(i)
    sby__ycugp += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(pwx__mjn):
        sby__ycugp += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if lbbnj__rhi:
        sby__ycugp += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        sby__ycugp += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    sby__ycugp += '  out_match_arr = np.empty(out_n, np.int64)\n'
    sby__ycugp += '  out_ind = 0\n'
    sby__ycugp += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    sby__ycugp += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    sby__ycugp += '          continue\n'
    sby__ycugp += '      m = regex.findall(str_arr[j])\n'
    sby__ycugp += '      for k, s in enumerate(m):\n'
    for i in range(pwx__mjn):
        sby__ycugp += (
            '        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})\n'
            .format(i, '[{}]'.format(i) if pwx__mjn > 1 else ''))
    sby__ycugp += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    sby__ycugp += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    sby__ycugp += '        out_ind += 1\n'
    sby__ycugp += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    sby__ycugp += "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n"
    fespl__mlj = ', '.join('out_arr_{}'.format(i) for i in range(pwx__mjn))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(sby__ycugp,
        lwwgf__ewwk, fespl__mlj, 'out_index', extra_globals={
        'get_utf8_size': get_utf8_size, 're': re})
    return impl


def _get_column_names_from_regex(pat, flags, func_name):
    if not is_overload_constant_str(pat):
        raise BodoError(
            "Series.str.{}(): 'pat' argument should be a constant string".
            format(func_name))
    if not is_overload_constant_int(flags):
        raise BodoError(
            "Series.str.{}(): 'flags' argument should be a constant int".
            format(func_name))
    pat = get_overload_const_str(pat)
    flags = get_overload_const_int(flags)
    regex = re.compile(pat, flags=flags)
    if regex.groups == 0:
        raise BodoError(
            'Series.str.{}(): pattern {} contains no capture groups'.format
            (func_name, pat))
    mvie__oddmq = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    lwwgf__ewwk = [mvie__oddmq.get(1 + i, i) for i in range(regex.groups)]
    return lwwgf__ewwk, regex


def create_str2str_methods_overload(func_name):
    if func_name in ['lstrip', 'rstrip', 'strip']:
        sby__ycugp = 'def f(S_str, to_strip=None):\n'
    else:
        sby__ycugp = 'def f(S_str):\n'
    sby__ycugp += '    S = S_str._obj\n'
    sby__ycugp += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    sby__ycugp += '    str_arr = decode_if_dict_array(str_arr)\n'
    sby__ycugp += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    sby__ycugp += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    sby__ycugp += '    numba.parfors.parfor.init_prange()\n'
    sby__ycugp += '    n = len(str_arr)\n'
    if func_name in ('capitalize', 'lower', 'swapcase', 'title', 'upper'):
        sby__ycugp += '    num_chars = num_total_chars(str_arr)\n'
    else:
        sby__ycugp += '    num_chars = -1\n'
    sby__ycugp += (
        '    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)\n'
        )
    sby__ycugp += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    sby__ycugp += '        if bodo.libs.array_kernels.isna(str_arr, j):\n'
    sby__ycugp += '            out_arr[j] = ""\n'
    sby__ycugp += '            bodo.libs.array_kernels.setna(out_arr, j)\n'
    sby__ycugp += '        else:\n'
    if func_name in ['lstrip', 'rstrip', 'strip']:
        sby__ycugp += ('            out_arr[j] = str_arr[j].{}(to_strip)\n'
            .format(func_name))
    else:
        sby__ycugp += '            out_arr[j] = str_arr[j].{}()\n'.format(
            func_name)
    sby__ycugp += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zrukk__gog = {}
    exec(sby__ycugp, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo
        .libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, zrukk__gog)
    cxwd__lbyw = zrukk__gog['f']
    if func_name in ['lstrip', 'rstrip', 'strip']:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            return cxwd__lbyw
        return overload_strip_method
    else:

        def overload_str2str_methods(S_str):
            return cxwd__lbyw
        return overload_str2str_methods


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        sby__ycugp = 'def f(S_str):\n'
        sby__ycugp += '    S = S_str._obj\n'
        sby__ycugp += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        sby__ycugp += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sby__ycugp += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        sby__ycugp += '    numba.parfors.parfor.init_prange()\n'
        sby__ycugp += '    l = len(str_arr)\n'
        sby__ycugp += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        sby__ycugp += '    for i in numba.parfors.parfor.internal_prange(l):\n'
        sby__ycugp += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
        sby__ycugp += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        sby__ycugp += '        else:\n'
        sby__ycugp += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        sby__ycugp += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        sby__ycugp += '      out_arr,index, name)\n'
        zrukk__gog = {}
        exec(sby__ycugp, {'bodo': bodo, 'numba': numba, 'np': np}, zrukk__gog)
        cxwd__lbyw = zrukk__gog['f']
        return cxwd__lbyw
    return overload_str2bool_methods


def _install_str2str_methods():
    for tiw__ysq in bodo.hiframes.pd_series_ext.str2str_methods:
        zzap__uoynp = create_str2str_methods_overload(tiw__ysq)
        overload_method(SeriesStrMethodType, tiw__ysq, inline='always',
            no_unliteral=True)(zzap__uoynp)


def _install_str2bool_methods():
    for tiw__ysq in bodo.hiframes.pd_series_ext.str2bool_methods:
        zzap__uoynp = create_str2bool_methods_overload(tiw__ysq)
        overload_method(SeriesStrMethodType, tiw__ysq, inline='always',
            no_unliteral=True)(zzap__uoynp)


_install_str2str_methods()
_install_str2bool_methods()


@overload_attribute(SeriesType, 'cat')
def overload_series_cat(s):
    if not isinstance(s.dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):
        raise BodoError('Can only use .cat accessor with categorical values.')
    return lambda s: bodo.hiframes.series_str_impl.init_series_cat_method(s)


class SeriesCatMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        mzetq__sccrf = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(mzetq__sccrf)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yahky__tpew = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, yahky__tpew)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        jcvpb__mmntt, = args
        tfv__zsf = signature.return_type
        nplbg__qgyf = cgutils.create_struct_proxy(tfv__zsf)(context, builder)
        nplbg__qgyf.obj = jcvpb__mmntt
        context.nrt.incref(builder, signature.args[0], jcvpb__mmntt)
        return nplbg__qgyf._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        deibv__vbv = bodo.hiframes.pd_series_ext.get_series_data(S)
        kzm__lttz = bodo.hiframes.pd_series_ext.get_series_index(S)
        mzetq__sccrf = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(deibv__vbv),
            kzm__lttz, mzetq__sccrf)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for qjw__hwsg in unsupported_cat_attrs:
        qlrqs__cabz = 'Series.cat.' + qjw__hwsg
        overload_attribute(SeriesCatMethodType, qjw__hwsg)(
            create_unsupported_overload(qlrqs__cabz))
    for mnnnx__ldb in unsupported_cat_methods:
        qlrqs__cabz = 'Series.cat.' + mnnnx__ldb
        overload_method(SeriesCatMethodType, mnnnx__ldb)(
            create_unsupported_overload(qlrqs__cabz))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for mnnnx__ldb in unsupported_str_methods:
        qlrqs__cabz = 'Series.str.' + mnnnx__ldb
        overload_method(SeriesStrMethodType, mnnnx__ldb)(
            create_unsupported_overload(qlrqs__cabz))


_install_strseries_unsupported()
