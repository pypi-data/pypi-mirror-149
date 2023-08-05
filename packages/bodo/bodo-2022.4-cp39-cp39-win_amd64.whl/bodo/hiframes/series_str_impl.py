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
        hnlhn__cqgd = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(hnlhn__cqgd)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ksdj__cqu = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, ksdj__cqu)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qval__dzr, = args
        fjfs__wqmy = signature.return_type
        dyso__byh = cgutils.create_struct_proxy(fjfs__wqmy)(context, builder)
        dyso__byh.obj = qval__dzr
        context.nrt.incref(builder, signature.args[0], qval__dzr)
        return dyso__byh._getvalue()
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
        dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(dcxrf__oqsxy, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
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
            dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
            byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
            hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(dcxrf__oqsxy,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                byip__iyiap, hnlhn__cqgd)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(dcxrf__oqsxy, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    tfr__jput = S_str.stype.data
    if (tfr__jput != string_array_split_view_type and not is_str_arr_type(
        tfr__jput)) and not isinstance(tfr__jput, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(tfr__jput, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
            byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
            hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(dcxrf__oqsxy, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                byip__iyiap, hnlhn__cqgd)
        return _str_get_array_impl
    if tfr__jput == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
            byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
            hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(dcxrf__oqsxy)
            ordqg__rjnq = 0
            for lulcf__mfipn in numba.parfors.parfor.internal_prange(n):
                bru__qmp, bru__qmp, ljjqp__xthod = get_split_view_index(
                    dcxrf__oqsxy, lulcf__mfipn, i)
                ordqg__rjnq += ljjqp__xthod
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, ordqg__rjnq)
            for duxt__gzer in numba.parfors.parfor.internal_prange(n):
                rhl__ffpyn, eamy__tgzyg, ljjqp__xthod = get_split_view_index(
                    dcxrf__oqsxy, duxt__gzer, i)
                if rhl__ffpyn == 0:
                    bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
                    wuuft__qxyq = get_split_view_data_ptr(dcxrf__oqsxy, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        duxt__gzer)
                    wuuft__qxyq = get_split_view_data_ptr(dcxrf__oqsxy,
                        eamy__tgzyg)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    duxt__gzer, wuuft__qxyq, ljjqp__xthod)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                byip__iyiap, hnlhn__cqgd)
        return _str_get_split_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(dcxrf__oqsxy)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(dcxrf__oqsxy, duxt__gzer
                ) or not len(dcxrf__oqsxy[duxt__gzer]) > i >= -len(dcxrf__oqsxy
                [duxt__gzer]):
                out_arr[duxt__gzer] = ''
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
            else:
                out_arr[duxt__gzer] = dcxrf__oqsxy[duxt__gzer][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    tfr__jput = S_str.stype.data
    if (tfr__jput != string_array_split_view_type and tfr__jput !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        tfr__jput)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(jmn__ysayi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                out_arr[duxt__gzer] = ''
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
            else:
                gfx__xsa = jmn__ysayi[duxt__gzer]
                out_arr[duxt__gzer] = sep.join(gfx__xsa)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
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
            dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
            byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
            hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(dcxrf__oqsxy, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                byip__iyiap, hnlhn__cqgd)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
            byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
            hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            hcuws__wqji = re.compile(pat, flags)
            gci__ejvg = len(dcxrf__oqsxy)
            out_arr = pre_alloc_string_array(gci__ejvg, -1)
            for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
                if bodo.libs.array_kernels.isna(dcxrf__oqsxy, duxt__gzer):
                    out_arr[duxt__gzer] = ''
                    bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
                    continue
                out_arr[duxt__gzer] = hcuws__wqji.sub(repl, dcxrf__oqsxy[
                    duxt__gzer])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                byip__iyiap, hnlhn__cqgd)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(dcxrf__oqsxy)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(gci__ejvg, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(dcxrf__oqsxy, duxt__gzer):
                out_arr[duxt__gzer] = ''
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
                continue
            out_arr[duxt__gzer] = dcxrf__oqsxy[duxt__gzer].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    zunp__gegj = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(nhl__baat in pat) for nhl__baat in zunp__gegj])
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
    vilxz__swhn = re.IGNORECASE.value
    ybu__lhdyh = 'def impl(\n'
    ybu__lhdyh += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    ybu__lhdyh += '):\n'
    ybu__lhdyh += '  S = S_str._obj\n'
    ybu__lhdyh += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    ybu__lhdyh += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    ybu__lhdyh += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    ybu__lhdyh += '  l = len(arr)\n'
    ybu__lhdyh += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                ybu__lhdyh += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                ybu__lhdyh += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            ybu__lhdyh += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        ybu__lhdyh += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        ybu__lhdyh += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            ybu__lhdyh += '  upper_pat = pat.upper()\n'
        ybu__lhdyh += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        ybu__lhdyh += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        ybu__lhdyh += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        ybu__lhdyh += '      else: \n'
        if is_overload_true(case):
            ybu__lhdyh += '          out_arr[i] = pat in arr[i]\n'
        else:
            ybu__lhdyh += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    ybu__lhdyh += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    rdo__dzv = {}
    exec(ybu__lhdyh, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': vilxz__swhn, 'get_search_regex':
        get_search_regex}, rdo__dzv)
    impl = rdo__dzv['impl']
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
    ybu__lhdyh = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    ybu__lhdyh += '  S = S_str._obj\n'
    ybu__lhdyh += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    ybu__lhdyh += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    ybu__lhdyh += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    ybu__lhdyh += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        ybu__lhdyh += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(icwy__wovi ==
        bodo.dict_str_arr_type for icwy__wovi in others.data):
        inv__ehln = ', '.join(f'data{i}' for i in range(len(others.columns)))
        ybu__lhdyh += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {inv__ehln}), sep)\n'
            )
    else:
        lafc__ufs = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        ybu__lhdyh += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        ybu__lhdyh += '  numba.parfors.parfor.init_prange()\n'
        ybu__lhdyh += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        ybu__lhdyh += f'      if {lafc__ufs}:\n'
        ybu__lhdyh += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        ybu__lhdyh += '          continue\n'
        jyl__lhvjb = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        ibbtz__okbfy = "''" if is_overload_none(sep) else 'sep'
        ybu__lhdyh += (
            f'      out_arr[i] = {ibbtz__okbfy}.join([{jyl__lhvjb}])\n')
    ybu__lhdyh += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    rdo__dzv = {}
    exec(ybu__lhdyh, {'bodo': bodo, 'numba': numba}, rdo__dzv)
    impl = rdo__dzv['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        hcuws__wqji = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(gci__ejvg, np.int64)
        for i in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(hcuws__wqji, jmn__ysayi[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
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
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(gci__ejvg, np.int64)
        for i in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = jmn__ysayi[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
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
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(gci__ejvg, np.int64)
        for i in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = jmn__ysayi[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
    return impl


@overload_method(SeriesStrMethodType, 'center', inline='always',
    no_unliteral=True)
def overload_str_method_center(S_str, width, fillchar=' '):
    common_validate_padding('center', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gci__ejvg, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                out_arr[duxt__gzer] = ''
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
            else:
                out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
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
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gci__ejvg, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
            else:
                if stop is not None:
                    aetdc__wzatd = jmn__ysayi[duxt__gzer][stop:]
                else:
                    aetdc__wzatd = ''
                out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer][:start
                    ] + repl + aetdc__wzatd
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):

        def impl(S_str, repeats):
            S = S_str._obj
            jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
            hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
            byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            gci__ejvg = len(jmn__ysayi)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gci__ejvg,
                -1)
            for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
                if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                    bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
                else:
                    out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                byip__iyiap, hnlhn__cqgd)
        return impl
    elif is_overload_constant_list(repeats):
        qgawi__rakgd = get_overload_const_list(repeats)
        kccp__nusas = all([isinstance(hutt__cmf, int) for hutt__cmf in
            qgawi__rakgd])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        kccp__nusas = True
    else:
        kccp__nusas = False
    if kccp__nusas:

        def impl(S_str, repeats):
            S = S_str._obj
            jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
            hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
            byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
            tam__wnhmd = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            gci__ejvg = len(jmn__ysayi)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gci__ejvg,
                -1)
            for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
                if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                    bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
                else:
                    out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer] * tam__wnhmd[
                        duxt__gzer]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                byip__iyiap, hnlhn__cqgd)
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
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gci__ejvg, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                out_arr[duxt__gzer] = ''
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
            else:
                out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer].ljust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
    return impl


@overload_method(SeriesStrMethodType, 'rjust', inline='always',
    no_unliteral=True)
def overload_str_method_rjust(S_str, width, fillchar=' '):
    common_validate_padding('rjust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gci__ejvg, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                out_arr[duxt__gzer] = ''
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
            else:
                out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer].rjust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
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
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gci__ejvg, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                out_arr[duxt__gzer] = ''
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
            elif side == 'left':
                out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)

    def impl(S_str, width):
        S = S_str._obj
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gci__ejvg, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                out_arr[duxt__gzer] = ''
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
            else:
                out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
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
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gci__ejvg, -1)
        for duxt__gzer in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, duxt__gzer):
                out_arr[duxt__gzer] = ''
                bodo.libs.array_kernels.setna(out_arr, duxt__gzer)
            else:
                out_arr[duxt__gzer] = jmn__ysayi[duxt__gzer][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
            byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
            hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(dcxrf__oqsxy,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                byip__iyiap, hnlhn__cqgd)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(gci__ejvg)
        for i in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = jmn__ysayi[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
            byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
            hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(dcxrf__oqsxy, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                byip__iyiap, hnlhn__cqgd)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        jmn__ysayi = bodo.hiframes.pd_series_ext.get_series_data(S)
        hnlhn__cqgd = bodo.hiframes.pd_series_ext.get_series_name(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gci__ejvg = len(jmn__ysayi)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(gci__ejvg)
        for i in numba.parfors.parfor.internal_prange(gci__ejvg):
            if bodo.libs.array_kernels.isna(jmn__ysayi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = jmn__ysayi[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, byip__iyiap,
            hnlhn__cqgd)
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
    vfe__olnu, regex = _get_column_names_from_regex(pat, flags, 'extract')
    sryis__yzlv = len(vfe__olnu)
    ybu__lhdyh = 'def impl(S_str, pat, flags=0, expand=True):\n'
    ybu__lhdyh += '  regex = re.compile(pat, flags=flags)\n'
    ybu__lhdyh += '  S = S_str._obj\n'
    ybu__lhdyh += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ybu__lhdyh += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    ybu__lhdyh += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    ybu__lhdyh += '  numba.parfors.parfor.init_prange()\n'
    ybu__lhdyh += '  n = len(str_arr)\n'
    for i in range(sryis__yzlv):
        ybu__lhdyh += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    ybu__lhdyh += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    ybu__lhdyh += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(sryis__yzlv):
        ybu__lhdyh += "          out_arr_{}[j] = ''\n".format(i)
        ybu__lhdyh += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    ybu__lhdyh += '      else:\n'
    ybu__lhdyh += '          m = regex.search(str_arr[j])\n'
    ybu__lhdyh += '          if m:\n'
    ybu__lhdyh += '            g = m.groups()\n'
    for i in range(sryis__yzlv):
        ybu__lhdyh += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    ybu__lhdyh += '          else:\n'
    for i in range(sryis__yzlv):
        ybu__lhdyh += "            out_arr_{}[j] = ''\n".format(i)
        ybu__lhdyh += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        hnlhn__cqgd = "'{}'".format(list(regex.groupindex.keys()).pop()
            ) if len(regex.groupindex.keys()) > 0 else 'name'
        ybu__lhdyh += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(hnlhn__cqgd))
        rdo__dzv = {}
        exec(ybu__lhdyh, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, rdo__dzv)
        impl = rdo__dzv['impl']
        return impl
    yzz__rzm = ', '.join('out_arr_{}'.format(i) for i in range(sryis__yzlv))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(ybu__lhdyh, vfe__olnu,
        yzz__rzm, 'index', extra_globals={'get_utf8_size': get_utf8_size,
        're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    vfe__olnu, bru__qmp = _get_column_names_from_regex(pat, flags, 'extractall'
        )
    sryis__yzlv = len(vfe__olnu)
    sipqw__njuy = isinstance(S_str.stype.index, StringIndexType)
    ybu__lhdyh = 'def impl(S_str, pat, flags=0):\n'
    ybu__lhdyh += '  regex = re.compile(pat, flags=flags)\n'
    ybu__lhdyh += '  S = S_str._obj\n'
    ybu__lhdyh += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ybu__lhdyh += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    ybu__lhdyh += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    ybu__lhdyh += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    ybu__lhdyh += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    ybu__lhdyh += '  numba.parfors.parfor.init_prange()\n'
    ybu__lhdyh += '  n = len(str_arr)\n'
    ybu__lhdyh += '  out_n_l = [0]\n'
    for i in range(sryis__yzlv):
        ybu__lhdyh += '  num_chars_{} = 0\n'.format(i)
    if sipqw__njuy:
        ybu__lhdyh += '  index_num_chars = 0\n'
    ybu__lhdyh += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if sipqw__njuy:
        ybu__lhdyh += '      index_num_chars += get_utf8_size(index_arr[i])\n'
    ybu__lhdyh += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    ybu__lhdyh += '          continue\n'
    ybu__lhdyh += '      m = regex.findall(str_arr[i])\n'
    ybu__lhdyh += '      out_n_l[0] += len(m)\n'
    for i in range(sryis__yzlv):
        ybu__lhdyh += '      l_{} = 0\n'.format(i)
    ybu__lhdyh += '      for s in m:\n'
    for i in range(sryis__yzlv):
        ybu__lhdyh += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if sryis__yzlv > 1 else '')
    for i in range(sryis__yzlv):
        ybu__lhdyh += '      num_chars_{0} += l_{0}\n'.format(i)
    ybu__lhdyh += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(sryis__yzlv):
        ybu__lhdyh += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if sipqw__njuy:
        ybu__lhdyh += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        ybu__lhdyh += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    ybu__lhdyh += '  out_match_arr = np.empty(out_n, np.int64)\n'
    ybu__lhdyh += '  out_ind = 0\n'
    ybu__lhdyh += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    ybu__lhdyh += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    ybu__lhdyh += '          continue\n'
    ybu__lhdyh += '      m = regex.findall(str_arr[j])\n'
    ybu__lhdyh += '      for k, s in enumerate(m):\n'
    for i in range(sryis__yzlv):
        ybu__lhdyh += (
            '        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})\n'
            .format(i, '[{}]'.format(i) if sryis__yzlv > 1 else ''))
    ybu__lhdyh += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    ybu__lhdyh += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    ybu__lhdyh += '        out_ind += 1\n'
    ybu__lhdyh += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    ybu__lhdyh += "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n"
    yzz__rzm = ', '.join('out_arr_{}'.format(i) for i in range(sryis__yzlv))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(ybu__lhdyh, vfe__olnu,
        yzz__rzm, 'out_index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
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
    kpy__gupq = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    vfe__olnu = [kpy__gupq.get(1 + i, i) for i in range(regex.groups)]
    return vfe__olnu, regex


def create_str2str_methods_overload(func_name):
    if func_name in ['lstrip', 'rstrip', 'strip']:
        ybu__lhdyh = 'def f(S_str, to_strip=None):\n'
    else:
        ybu__lhdyh = 'def f(S_str):\n'
    ybu__lhdyh += '    S = S_str._obj\n'
    ybu__lhdyh += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ybu__lhdyh += '    str_arr = decode_if_dict_array(str_arr)\n'
    ybu__lhdyh += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    ybu__lhdyh += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    ybu__lhdyh += '    numba.parfors.parfor.init_prange()\n'
    ybu__lhdyh += '    n = len(str_arr)\n'
    if func_name in ('capitalize', 'lower', 'swapcase', 'title', 'upper'):
        ybu__lhdyh += '    num_chars = num_total_chars(str_arr)\n'
    else:
        ybu__lhdyh += '    num_chars = -1\n'
    ybu__lhdyh += (
        '    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)\n'
        )
    ybu__lhdyh += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    ybu__lhdyh += '        if bodo.libs.array_kernels.isna(str_arr, j):\n'
    ybu__lhdyh += '            out_arr[j] = ""\n'
    ybu__lhdyh += '            bodo.libs.array_kernels.setna(out_arr, j)\n'
    ybu__lhdyh += '        else:\n'
    if func_name in ['lstrip', 'rstrip', 'strip']:
        ybu__lhdyh += ('            out_arr[j] = str_arr[j].{}(to_strip)\n'
            .format(func_name))
    else:
        ybu__lhdyh += '            out_arr[j] = str_arr[j].{}()\n'.format(
            func_name)
    ybu__lhdyh += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    rdo__dzv = {}
    exec(ybu__lhdyh, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo
        .libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, rdo__dzv)
    ndndy__ycd = rdo__dzv['f']
    if func_name in ['lstrip', 'rstrip', 'strip']:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            return ndndy__ycd
        return overload_strip_method
    else:

        def overload_str2str_methods(S_str):
            return ndndy__ycd
        return overload_str2str_methods


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        ybu__lhdyh = 'def f(S_str):\n'
        ybu__lhdyh += '    S = S_str._obj\n'
        ybu__lhdyh += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ybu__lhdyh += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ybu__lhdyh += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ybu__lhdyh += '    numba.parfors.parfor.init_prange()\n'
        ybu__lhdyh += '    l = len(str_arr)\n'
        ybu__lhdyh += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        ybu__lhdyh += '    for i in numba.parfors.parfor.internal_prange(l):\n'
        ybu__lhdyh += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
        ybu__lhdyh += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        ybu__lhdyh += '        else:\n'
        ybu__lhdyh += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        ybu__lhdyh += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        ybu__lhdyh += '      out_arr,index, name)\n'
        rdo__dzv = {}
        exec(ybu__lhdyh, {'bodo': bodo, 'numba': numba, 'np': np}, rdo__dzv)
        ndndy__ycd = rdo__dzv['f']
        return ndndy__ycd
    return overload_str2bool_methods


def _install_str2str_methods():
    for puv__aepgl in bodo.hiframes.pd_series_ext.str2str_methods:
        kuqa__ydob = create_str2str_methods_overload(puv__aepgl)
        overload_method(SeriesStrMethodType, puv__aepgl, inline='always',
            no_unliteral=True)(kuqa__ydob)


def _install_str2bool_methods():
    for puv__aepgl in bodo.hiframes.pd_series_ext.str2bool_methods:
        kuqa__ydob = create_str2bool_methods_overload(puv__aepgl)
        overload_method(SeriesStrMethodType, puv__aepgl, inline='always',
            no_unliteral=True)(kuqa__ydob)


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
        hnlhn__cqgd = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(hnlhn__cqgd)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ksdj__cqu = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, ksdj__cqu)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qval__dzr, = args
        qak__dsdmz = signature.return_type
        oqti__kgio = cgutils.create_struct_proxy(qak__dsdmz)(context, builder)
        oqti__kgio.obj = qval__dzr
        context.nrt.incref(builder, signature.args[0], qval__dzr)
        return oqti__kgio._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        dcxrf__oqsxy = bodo.hiframes.pd_series_ext.get_series_data(S)
        byip__iyiap = bodo.hiframes.pd_series_ext.get_series_index(S)
        hnlhn__cqgd = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(dcxrf__oqsxy),
            byip__iyiap, hnlhn__cqgd)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for ygr__xgjmf in unsupported_cat_attrs:
        mtab__ixtz = 'Series.cat.' + ygr__xgjmf
        overload_attribute(SeriesCatMethodType, ygr__xgjmf)(
            create_unsupported_overload(mtab__ixtz))
    for uory__moln in unsupported_cat_methods:
        mtab__ixtz = 'Series.cat.' + uory__moln
        overload_method(SeriesCatMethodType, uory__moln)(
            create_unsupported_overload(mtab__ixtz))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for uory__moln in unsupported_str_methods:
        mtab__ixtz = 'Series.str.' + uory__moln
        overload_method(SeriesStrMethodType, uory__moln)(
            create_unsupported_overload(mtab__ixtz))


_install_strseries_unsupported()
