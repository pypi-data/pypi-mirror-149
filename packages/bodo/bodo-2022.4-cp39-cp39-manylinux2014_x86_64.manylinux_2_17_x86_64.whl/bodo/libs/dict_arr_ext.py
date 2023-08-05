"""Dictionary encoded array data type, similar to DictionaryArray of Arrow.
The purpose is to improve memory consumption and performance over string_array_type for
string arrays that have a lot of repetitive values (typical in practice).
Can be extended to be used with types other than strings as well.
See:
https://bodo.atlassian.net/browse/BE-2295
https://bodo.atlassian.net/wiki/spaces/B/pages/993722369/Dictionary-encoded+String+Array+Support+in+Parquet+read+compute+...
https://arrow.apache.org/docs/cpp/api/array.html#dictionary-encoded
"""
import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_builtin, lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo
from bodo.libs import hstr_ext
from bodo.libs.bool_arr_ext import init_bool_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, get_str_arr_item_length, overload_str_arr_astype, pre_alloc_string_array
from bodo.utils.typing import BodoArrayIterator, is_overload_none, raise_bodo_error
ll.add_symbol('box_dict_str_array', hstr_ext.box_dict_str_array)
dict_indices_arr_type = IntegerArrayType(types.int32)


class DictionaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, arr_data_type):
        self.data = arr_data_type
        super(DictionaryArrayType, self).__init__(name=
            f'DictionaryArrayType({arr_data_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self.data.dtype

    def copy(self):
        return DictionaryArrayType(self.data)

    @property
    def indices_type(self):
        return dict_indices_arr_type

    @property
    def indices_dtype(self):
        return dict_indices_arr_type.dtype

    def unify(self, typingctx, other):
        if other == bodo.string_array_type:
            return bodo.string_array_type


dict_str_arr_type = DictionaryArrayType(bodo.string_array_type)


@register_model(DictionaryArrayType)
class DictionaryArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ygttv__smn = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, ygttv__smn)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        vlwlm__oyi, hcmb__scelb, rost__myc = args
        jbzpd__wpdct = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        jbzpd__wpdct.data = vlwlm__oyi
        jbzpd__wpdct.indices = hcmb__scelb
        jbzpd__wpdct.has_global_dictionary = rost__myc
        context.nrt.incref(builder, signature.args[0], vlwlm__oyi)
        context.nrt.incref(builder, signature.args[1], hcmb__scelb)
        return jbzpd__wpdct._getvalue()
    heyfb__bgoxp = DictionaryArrayType(data_t)
    wvxh__tlcjp = heyfb__bgoxp(data_t, indices_t, types.bool_)
    return wvxh__tlcjp, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    for cvx__juy in range(len(A)):
        if pd.isna(A[cvx__juy]):
            A[cvx__juy] = None
    return pa.array(A).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    if bodo.hiframes.boxing._use_dict_str_type:
        qnnw__gyge = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(qnnw__gyge, [val])
        c.pyapi.decref(qnnw__gyge)
    jbzpd__wpdct = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mwmvg__zeoet = c.pyapi.object_getattr_string(val, 'dictionary')
    zflm__scsoy = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    pbgb__otvq = c.pyapi.call_method(mwmvg__zeoet, 'to_numpy', (zflm__scsoy,))
    jbzpd__wpdct.data = c.unbox(typ.data, pbgb__otvq).value
    yzh__ucytu = c.pyapi.object_getattr_string(val, 'indices')
    gebu__lcphe = c.context.insert_const_string(c.builder.module, 'pandas')
    ful__kxq = c.pyapi.import_module_noblock(gebu__lcphe)
    ptt__ako = c.pyapi.string_from_constant_string('Int32')
    yevhx__qtfwl = c.pyapi.call_method(ful__kxq, 'array', (yzh__ucytu,
        ptt__ako))
    jbzpd__wpdct.indices = c.unbox(dict_indices_arr_type, yevhx__qtfwl).value
    jbzpd__wpdct.has_global_dictionary = c.context.get_constant(types.bool_,
        False)
    c.pyapi.decref(mwmvg__zeoet)
    c.pyapi.decref(zflm__scsoy)
    c.pyapi.decref(pbgb__otvq)
    c.pyapi.decref(yzh__ucytu)
    c.pyapi.decref(ful__kxq)
    c.pyapi.decref(ptt__ako)
    c.pyapi.decref(yevhx__qtfwl)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    jje__ljelp = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(jbzpd__wpdct._getvalue(), is_error=jje__ljelp)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    jbzpd__wpdct = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, jbzpd__wpdct.data)
        mci__nvgh = c.box(typ.data, jbzpd__wpdct.data)
        hxitv__gpti = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, jbzpd__wpdct.indices)
        yxw__yqd = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        lmt__xojw = cgutils.get_or_insert_function(c.builder.module,
            yxw__yqd, name='box_dict_str_array')
        tfx__lwn = cgutils.create_struct_proxy(types.Array(types.int32, 1, 'C')
            )(c.context, c.builder, hxitv__gpti.data)
        wakk__pfxmq = c.builder.extract_value(tfx__lwn.shape, 0)
        mlrs__piz = tfx__lwn.data
        xfng__lcav = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, hxitv__gpti.null_bitmap).data
        pbgb__otvq = c.builder.call(lmt__xojw, [wakk__pfxmq, mci__nvgh,
            mlrs__piz, xfng__lcav])
        c.pyapi.decref(mci__nvgh)
    else:
        gebu__lcphe = c.context.insert_const_string(c.builder.module, 'pyarrow'
            )
        lsoat__ygqis = c.pyapi.import_module_noblock(gebu__lcphe)
        bibrl__htvb = c.pyapi.object_getattr_string(lsoat__ygqis,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, jbzpd__wpdct.data)
        mci__nvgh = c.box(typ.data, jbzpd__wpdct.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, jbzpd__wpdct
            .indices)
        yzh__ucytu = c.box(dict_indices_arr_type, jbzpd__wpdct.indices)
        dzpp__bsrqo = c.pyapi.call_method(bibrl__htvb, 'from_arrays', (
            yzh__ucytu, mci__nvgh))
        zflm__scsoy = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        pbgb__otvq = c.pyapi.call_method(dzpp__bsrqo, 'to_numpy', (
            zflm__scsoy,))
        c.pyapi.decref(lsoat__ygqis)
        c.pyapi.decref(mci__nvgh)
        c.pyapi.decref(yzh__ucytu)
        c.pyapi.decref(bibrl__htvb)
        c.pyapi.decref(dzpp__bsrqo)
        c.pyapi.decref(zflm__scsoy)
    c.context.nrt.decref(c.builder, typ, val)
    return pbgb__otvq


@overload(len, no_unliteral=True)
def overload_dict_arr_len(A):
    if isinstance(A, DictionaryArrayType):
        return lambda A: len(A._indices)


@overload_attribute(DictionaryArrayType, 'shape')
def overload_dict_arr_shape(A):
    return lambda A: (len(A._indices),)


@overload_attribute(DictionaryArrayType, 'ndim')
def overload_dict_arr_ndim(A):
    return lambda A: 1


@overload_attribute(DictionaryArrayType, 'size')
def overload_dict_arr_size(A):
    return lambda A: len(A._indices)


@overload_method(DictionaryArrayType, 'tolist', no_unliteral=True)
def overload_dict_arr_tolist(A):
    return lambda A: list(A)


overload_method(DictionaryArrayType, 'astype', no_unliteral=True)(
    overload_str_arr_astype)


@overload_method(DictionaryArrayType, 'copy', no_unliteral=True)
def overload_dict_arr_copy(A):

    def copy_impl(A):
        return init_dict_arr(A._data.copy(), A._indices.copy(), A.
            _has_global_dictionary)
    return copy_impl


@overload_attribute(DictionaryArrayType, 'dtype')
def overload_dict_arr_dtype(A):
    return lambda A: A._data.dtype


@overload_attribute(DictionaryArrayType, 'nbytes')
def dict_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._indices.nbytes


@lower_constant(DictionaryArrayType)
def lower_constant_dict_arr(context, builder, typ, pyval):
    if bodo.hiframes.boxing._use_dict_str_type and isinstance(pyval, np.ndarray
        ):
        pyval = pa.array(pyval).dictionary_encode()
    hljpm__kamc = pyval.dictionary.to_numpy(False)
    wll__rbu = pd.array(pyval.indices, 'Int32')
    hljpm__kamc = context.get_constant_generic(builder, typ.data, hljpm__kamc)
    wll__rbu = context.get_constant_generic(builder, dict_indices_arr_type,
        wll__rbu)
    ccyls__wri = context.get_constant(types.bool_, False)
    cgo__arb = lir.Constant.literal_struct([hljpm__kamc, wll__rbu, ccyls__wri])
    return cgo__arb


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            hkbeu__nhagl = A._indices[ind]
            return A._data[hkbeu__nhagl]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        vlwlm__oyi = A._data
        hcmb__scelb = A._indices
        wakk__pfxmq = len(hcmb__scelb)
        afkn__kzm = [get_str_arr_item_length(vlwlm__oyi, cvx__juy) for
            cvx__juy in range(len(vlwlm__oyi))]
        gqebb__flxhc = 0
        for cvx__juy in range(wakk__pfxmq):
            if not bodo.libs.array_kernels.isna(hcmb__scelb, cvx__juy):
                gqebb__flxhc += afkn__kzm[hcmb__scelb[cvx__juy]]
        vms__yct = pre_alloc_string_array(wakk__pfxmq, gqebb__flxhc)
        for cvx__juy in range(wakk__pfxmq):
            if bodo.libs.array_kernels.isna(hcmb__scelb, cvx__juy):
                bodo.libs.array_kernels.setna(vms__yct, cvx__juy)
                continue
            ind = hcmb__scelb[cvx__juy]
            if bodo.libs.array_kernels.isna(vlwlm__oyi, ind):
                bodo.libs.array_kernels.setna(vms__yct, cvx__juy)
                continue
            vms__yct[cvx__juy] = vlwlm__oyi[ind]
        return vms__yct
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    hkbeu__nhagl = -1
    vlwlm__oyi = arr._data
    for cvx__juy in range(len(vlwlm__oyi)):
        if bodo.libs.array_kernels.isna(vlwlm__oyi, cvx__juy):
            continue
        if vlwlm__oyi[cvx__juy] == val:
            hkbeu__nhagl = cvx__juy
            break
    return hkbeu__nhagl


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    wakk__pfxmq = len(arr)
    hkbeu__nhagl = find_dict_ind(arr, val)
    if hkbeu__nhagl == -1:
        return init_bool_array(np.full(wakk__pfxmq, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == hkbeu__nhagl


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    wakk__pfxmq = len(arr)
    hkbeu__nhagl = find_dict_ind(arr, val)
    if hkbeu__nhagl == -1:
        return init_bool_array(np.full(wakk__pfxmq, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != hkbeu__nhagl


def get_binary_op_overload(op, lhs, rhs):
    if op == operator.eq:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_eq(lhs, rhs)
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_eq(rhs, lhs)
    if op == operator.ne:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_ne(lhs, rhs)
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_ne(rhs, lhs)


def convert_dict_arr_to_int(arr, dtype):
    return arr


@overload(convert_dict_arr_to_int)
def convert_dict_arr_to_int_overload(arr, dtype):

    def impl(arr, dtype):
        kcbj__gjpw = arr._data
        ohx__qzvrw = bodo.libs.int_arr_ext.alloc_int_array(len(kcbj__gjpw),
            dtype)
        for rxmbu__lupf in range(len(kcbj__gjpw)):
            if bodo.libs.array_kernels.isna(kcbj__gjpw, rxmbu__lupf):
                bodo.libs.array_kernels.setna(ohx__qzvrw, rxmbu__lupf)
                continue
            ohx__qzvrw[rxmbu__lupf] = np.int64(kcbj__gjpw[rxmbu__lupf])
        wakk__pfxmq = len(arr)
        hcmb__scelb = arr._indices
        vms__yct = bodo.libs.int_arr_ext.alloc_int_array(wakk__pfxmq, dtype)
        for cvx__juy in range(wakk__pfxmq):
            if bodo.libs.array_kernels.isna(hcmb__scelb, cvx__juy):
                bodo.libs.array_kernels.setna(vms__yct, cvx__juy)
                continue
            vms__yct[cvx__juy] = ohx__qzvrw[hcmb__scelb[cvx__juy]]
        return vms__yct
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    egw__cfx = len(arrs)
    spxi__xdy = 'def impl(arrs, sep):\n'
    spxi__xdy += '  ind_map = {}\n'
    spxi__xdy += '  out_strs = []\n'
    spxi__xdy += '  n = len(arrs[0])\n'
    for cvx__juy in range(egw__cfx):
        spxi__xdy += f'  indices{cvx__juy} = arrs[{cvx__juy}]._indices\n'
    for cvx__juy in range(egw__cfx):
        spxi__xdy += f'  data{cvx__juy} = arrs[{cvx__juy}]._data\n'
    spxi__xdy += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    spxi__xdy += '  for i in range(n):\n'
    nuvcq__tln = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{cvx__juy}], i)' for cvx__juy in
        range(egw__cfx)])
    spxi__xdy += f'    if {nuvcq__tln}:\n'
    spxi__xdy += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    spxi__xdy += '      continue\n'
    for cvx__juy in range(egw__cfx):
        spxi__xdy += f'    ind{cvx__juy} = indices{cvx__juy}[i]\n'
    wjos__mpd = '(' + ', '.join(f'ind{cvx__juy}' for cvx__juy in range(
        egw__cfx)) + ')'
    spxi__xdy += f'    if {wjos__mpd} not in ind_map:\n'
    spxi__xdy += '      out_ind = len(out_strs)\n'
    spxi__xdy += f'      ind_map[{wjos__mpd}] = out_ind\n'
    zncyt__oab = "''" if is_overload_none(sep) else 'sep'
    qciti__mzkc = ', '.join([f'data{cvx__juy}[ind{cvx__juy}]' for cvx__juy in
        range(egw__cfx)])
    spxi__xdy += f'      v = {zncyt__oab}.join([{qciti__mzkc}])\n'
    spxi__xdy += '      out_strs.append(v)\n'
    spxi__xdy += '    else:\n'
    spxi__xdy += f'      out_ind = ind_map[{wjos__mpd}]\n'
    spxi__xdy += '    out_indices[i] = out_ind\n'
    spxi__xdy += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    spxi__xdy += (
        '  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)\n'
        )
    kiv__uazwk = {}
    exec(spxi__xdy, {'bodo': bodo, 'numba': numba, 'np': np}, kiv__uazwk)
    impl = kiv__uazwk['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    jqtc__rvnu = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    wvxh__tlcjp = toty(fromty)
    lgak__ruuqy = context.compile_internal(builder, jqtc__rvnu, wvxh__tlcjp,
        (val,))
    return impl_ret_new_ref(context, builder, toty, lgak__ruuqy)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    hljpm__kamc = arr._data
    ebg__pwr = len(hljpm__kamc)
    vpnah__pht = pre_alloc_string_array(ebg__pwr, -1)
    if regex:
        ujusy__rzv = re.compile(pat, flags)
        for cvx__juy in range(ebg__pwr):
            if bodo.libs.array_kernels.isna(hljpm__kamc, cvx__juy):
                bodo.libs.array_kernels.setna(vpnah__pht, cvx__juy)
                continue
            vpnah__pht[cvx__juy] = ujusy__rzv.sub(repl=repl, string=
                hljpm__kamc[cvx__juy])
    else:
        for cvx__juy in range(ebg__pwr):
            if bodo.libs.array_kernels.isna(hljpm__kamc, cvx__juy):
                bodo.libs.array_kernels.setna(vpnah__pht, cvx__juy)
                continue
            vpnah__pht[cvx__juy] = hljpm__kamc[cvx__juy].replace(pat, repl)
    return init_dict_arr(vpnah__pht, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    jbzpd__wpdct = arr._data
    zlyc__yiy = len(jbzpd__wpdct)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(zlyc__yiy)
    for cvx__juy in range(zlyc__yiy):
        dict_arr_out[cvx__juy] = jbzpd__wpdct[cvx__juy].startswith(pat)
    wll__rbu = arr._indices
    hwu__tvp = len(wll__rbu)
    vms__yct = bodo.libs.bool_arr_ext.alloc_bool_array(hwu__tvp)
    for cvx__juy in range(hwu__tvp):
        if bodo.libs.array_kernels.isna(arr, cvx__juy):
            bodo.libs.array_kernels.setna(vms__yct, cvx__juy)
        else:
            vms__yct[cvx__juy] = dict_arr_out[wll__rbu[cvx__juy]]
    return vms__yct


@register_jitable
def str_endswith(arr, pat, na):
    jbzpd__wpdct = arr._data
    zlyc__yiy = len(jbzpd__wpdct)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(zlyc__yiy)
    for cvx__juy in range(zlyc__yiy):
        dict_arr_out[cvx__juy] = jbzpd__wpdct[cvx__juy].endswith(pat)
    wll__rbu = arr._indices
    hwu__tvp = len(wll__rbu)
    vms__yct = bodo.libs.bool_arr_ext.alloc_bool_array(hwu__tvp)
    for cvx__juy in range(hwu__tvp):
        if bodo.libs.array_kernels.isna(arr, cvx__juy):
            bodo.libs.array_kernels.setna(vms__yct, cvx__juy)
        else:
            vms__yct[cvx__juy] = dict_arr_out[wll__rbu[cvx__juy]]
    return vms__yct


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    jbzpd__wpdct = arr._data
    rhnc__ndzsg = pd.Series(jbzpd__wpdct)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = rhnc__ndzsg.array._str_contains(pat, case, flags, na,
            regex)
    wll__rbu = arr._indices
    hwu__tvp = len(wll__rbu)
    vms__yct = bodo.libs.bool_arr_ext.alloc_bool_array(hwu__tvp)
    for cvx__juy in range(hwu__tvp):
        if bodo.libs.array_kernels.isna(arr, cvx__juy):
            bodo.libs.array_kernels.setna(vms__yct, cvx__juy)
        else:
            vms__yct[cvx__juy] = dict_arr_out[wll__rbu[cvx__juy]]
    return vms__yct


@register_jitable
def str_contains_non_regex(arr, pat, case):
    jbzpd__wpdct = arr._data
    zlyc__yiy = len(jbzpd__wpdct)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(zlyc__yiy)
    if not case:
        jyg__obaea = pat.upper()
    for cvx__juy in range(zlyc__yiy):
        if case:
            dict_arr_out[cvx__juy] = pat in jbzpd__wpdct[cvx__juy]
        else:
            dict_arr_out[cvx__juy] = jyg__obaea in jbzpd__wpdct[cvx__juy
                ].upper()
    wll__rbu = arr._indices
    hwu__tvp = len(wll__rbu)
    vms__yct = bodo.libs.bool_arr_ext.alloc_bool_array(hwu__tvp)
    for cvx__juy in range(hwu__tvp):
        if bodo.libs.array_kernels.isna(arr, cvx__juy):
            bodo.libs.array_kernels.setna(vms__yct, cvx__juy)
        else:
            vms__yct[cvx__juy] = dict_arr_out[wll__rbu[cvx__juy]]
    return vms__yct
