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
        xif__bgoss = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, xif__bgoss)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        wazf__pdq, wwf__lekm, zbi__yfmj = args
        rejsg__gjftu = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        rejsg__gjftu.data = wazf__pdq
        rejsg__gjftu.indices = wwf__lekm
        rejsg__gjftu.has_global_dictionary = zbi__yfmj
        context.nrt.incref(builder, signature.args[0], wazf__pdq)
        context.nrt.incref(builder, signature.args[1], wwf__lekm)
        return rejsg__gjftu._getvalue()
    ymwy__dei = DictionaryArrayType(data_t)
    zxnf__cjt = ymwy__dei(data_t, indices_t, types.bool_)
    return zxnf__cjt, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    for pnwk__ujug in range(len(A)):
        if pd.isna(A[pnwk__ujug]):
            A[pnwk__ujug] = None
    return pa.array(A).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    if bodo.hiframes.boxing._use_dict_str_type:
        srzj__hcx = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(srzj__hcx, [val])
        c.pyapi.decref(srzj__hcx)
    rejsg__gjftu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ysfia__kgwg = c.pyapi.object_getattr_string(val, 'dictionary')
    ifpv__bnoy = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    getsr__ujx = c.pyapi.call_method(ysfia__kgwg, 'to_numpy', (ifpv__bnoy,))
    rejsg__gjftu.data = c.unbox(typ.data, getsr__ujx).value
    wiic__noe = c.pyapi.object_getattr_string(val, 'indices')
    ktpc__usops = c.context.insert_const_string(c.builder.module, 'pandas')
    ugsty__avd = c.pyapi.import_module_noblock(ktpc__usops)
    qkar__oqroe = c.pyapi.string_from_constant_string('Int32')
    hil__eokzf = c.pyapi.call_method(ugsty__avd, 'array', (wiic__noe,
        qkar__oqroe))
    rejsg__gjftu.indices = c.unbox(dict_indices_arr_type, hil__eokzf).value
    rejsg__gjftu.has_global_dictionary = c.context.get_constant(types.bool_,
        False)
    c.pyapi.decref(ysfia__kgwg)
    c.pyapi.decref(ifpv__bnoy)
    c.pyapi.decref(getsr__ujx)
    c.pyapi.decref(wiic__noe)
    c.pyapi.decref(ugsty__avd)
    c.pyapi.decref(qkar__oqroe)
    c.pyapi.decref(hil__eokzf)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    iiz__bxtrd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rejsg__gjftu._getvalue(), is_error=iiz__bxtrd)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    rejsg__gjftu = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, rejsg__gjftu.data)
        kyk__ofnf = c.box(typ.data, rejsg__gjftu.data)
        vadfj__tqcn = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, rejsg__gjftu.indices)
        bxwq__ldu = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        vvuvc__svc = cgutils.get_or_insert_function(c.builder.module,
            bxwq__ldu, name='box_dict_str_array')
        rlf__nuyx = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, vadfj__tqcn.data)
        hmmz__ise = c.builder.extract_value(rlf__nuyx.shape, 0)
        rrfl__hdz = rlf__nuyx.data
        yhtv__wusl = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, vadfj__tqcn.null_bitmap).data
        getsr__ujx = c.builder.call(vvuvc__svc, [hmmz__ise, kyk__ofnf,
            rrfl__hdz, yhtv__wusl])
        c.pyapi.decref(kyk__ofnf)
    else:
        ktpc__usops = c.context.insert_const_string(c.builder.module, 'pyarrow'
            )
        saz__pwn = c.pyapi.import_module_noblock(ktpc__usops)
        tgxdy__regvq = c.pyapi.object_getattr_string(saz__pwn,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, rejsg__gjftu.data)
        kyk__ofnf = c.box(typ.data, rejsg__gjftu.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, rejsg__gjftu
            .indices)
        wiic__noe = c.box(dict_indices_arr_type, rejsg__gjftu.indices)
        rnu__dfg = c.pyapi.call_method(tgxdy__regvq, 'from_arrays', (
            wiic__noe, kyk__ofnf))
        ifpv__bnoy = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        getsr__ujx = c.pyapi.call_method(rnu__dfg, 'to_numpy', (ifpv__bnoy,))
        c.pyapi.decref(saz__pwn)
        c.pyapi.decref(kyk__ofnf)
        c.pyapi.decref(wiic__noe)
        c.pyapi.decref(tgxdy__regvq)
        c.pyapi.decref(rnu__dfg)
        c.pyapi.decref(ifpv__bnoy)
    c.context.nrt.decref(c.builder, typ, val)
    return getsr__ujx


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
    nbegq__trd = pyval.dictionary.to_numpy(False)
    cgp__lijny = pd.array(pyval.indices, 'Int32')
    nbegq__trd = context.get_constant_generic(builder, typ.data, nbegq__trd)
    cgp__lijny = context.get_constant_generic(builder,
        dict_indices_arr_type, cgp__lijny)
    naqzs__ljmi = context.get_constant(types.bool_, False)
    poyyd__bgbr = lir.Constant.literal_struct([nbegq__trd, cgp__lijny,
        naqzs__ljmi])
    return poyyd__bgbr


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            uvk__xzo = A._indices[ind]
            return A._data[uvk__xzo]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        wazf__pdq = A._data
        wwf__lekm = A._indices
        hmmz__ise = len(wwf__lekm)
        fnvz__scpo = [get_str_arr_item_length(wazf__pdq, pnwk__ujug) for
            pnwk__ujug in range(len(wazf__pdq))]
        zdnu__atua = 0
        for pnwk__ujug in range(hmmz__ise):
            if not bodo.libs.array_kernels.isna(wwf__lekm, pnwk__ujug):
                zdnu__atua += fnvz__scpo[wwf__lekm[pnwk__ujug]]
        aywo__gcxh = pre_alloc_string_array(hmmz__ise, zdnu__atua)
        for pnwk__ujug in range(hmmz__ise):
            if bodo.libs.array_kernels.isna(wwf__lekm, pnwk__ujug):
                bodo.libs.array_kernels.setna(aywo__gcxh, pnwk__ujug)
                continue
            ind = wwf__lekm[pnwk__ujug]
            if bodo.libs.array_kernels.isna(wazf__pdq, ind):
                bodo.libs.array_kernels.setna(aywo__gcxh, pnwk__ujug)
                continue
            aywo__gcxh[pnwk__ujug] = wazf__pdq[ind]
        return aywo__gcxh
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    uvk__xzo = -1
    wazf__pdq = arr._data
    for pnwk__ujug in range(len(wazf__pdq)):
        if bodo.libs.array_kernels.isna(wazf__pdq, pnwk__ujug):
            continue
        if wazf__pdq[pnwk__ujug] == val:
            uvk__xzo = pnwk__ujug
            break
    return uvk__xzo


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    hmmz__ise = len(arr)
    uvk__xzo = find_dict_ind(arr, val)
    if uvk__xzo == -1:
        return init_bool_array(np.full(hmmz__ise, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == uvk__xzo


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    hmmz__ise = len(arr)
    uvk__xzo = find_dict_ind(arr, val)
    if uvk__xzo == -1:
        return init_bool_array(np.full(hmmz__ise, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != uvk__xzo


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
        kuraj__esv = arr._data
        fbjm__rmis = bodo.libs.int_arr_ext.alloc_int_array(len(kuraj__esv),
            dtype)
        for jddol__yxmy in range(len(kuraj__esv)):
            if bodo.libs.array_kernels.isna(kuraj__esv, jddol__yxmy):
                bodo.libs.array_kernels.setna(fbjm__rmis, jddol__yxmy)
                continue
            fbjm__rmis[jddol__yxmy] = np.int64(kuraj__esv[jddol__yxmy])
        hmmz__ise = len(arr)
        wwf__lekm = arr._indices
        aywo__gcxh = bodo.libs.int_arr_ext.alloc_int_array(hmmz__ise, dtype)
        for pnwk__ujug in range(hmmz__ise):
            if bodo.libs.array_kernels.isna(wwf__lekm, pnwk__ujug):
                bodo.libs.array_kernels.setna(aywo__gcxh, pnwk__ujug)
                continue
            aywo__gcxh[pnwk__ujug] = fbjm__rmis[wwf__lekm[pnwk__ujug]]
        return aywo__gcxh
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    exnt__xly = len(arrs)
    czhm__kbbz = 'def impl(arrs, sep):\n'
    czhm__kbbz += '  ind_map = {}\n'
    czhm__kbbz += '  out_strs = []\n'
    czhm__kbbz += '  n = len(arrs[0])\n'
    for pnwk__ujug in range(exnt__xly):
        czhm__kbbz += f'  indices{pnwk__ujug} = arrs[{pnwk__ujug}]._indices\n'
    for pnwk__ujug in range(exnt__xly):
        czhm__kbbz += f'  data{pnwk__ujug} = arrs[{pnwk__ujug}]._data\n'
    czhm__kbbz += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    czhm__kbbz += '  for i in range(n):\n'
    ycr__tqcy = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{pnwk__ujug}], i)' for
        pnwk__ujug in range(exnt__xly)])
    czhm__kbbz += f'    if {ycr__tqcy}:\n'
    czhm__kbbz += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    czhm__kbbz += '      continue\n'
    for pnwk__ujug in range(exnt__xly):
        czhm__kbbz += f'    ind{pnwk__ujug} = indices{pnwk__ujug}[i]\n'
    eepp__fdus = '(' + ', '.join(f'ind{pnwk__ujug}' for pnwk__ujug in range
        (exnt__xly)) + ')'
    czhm__kbbz += f'    if {eepp__fdus} not in ind_map:\n'
    czhm__kbbz += '      out_ind = len(out_strs)\n'
    czhm__kbbz += f'      ind_map[{eepp__fdus}] = out_ind\n'
    uhghb__zomh = "''" if is_overload_none(sep) else 'sep'
    yjzjz__psaub = ', '.join([f'data{pnwk__ujug}[ind{pnwk__ujug}]' for
        pnwk__ujug in range(exnt__xly)])
    czhm__kbbz += f'      v = {uhghb__zomh}.join([{yjzjz__psaub}])\n'
    czhm__kbbz += '      out_strs.append(v)\n'
    czhm__kbbz += '    else:\n'
    czhm__kbbz += f'      out_ind = ind_map[{eepp__fdus}]\n'
    czhm__kbbz += '    out_indices[i] = out_ind\n'
    czhm__kbbz += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    czhm__kbbz += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    gffh__yhjz = {}
    exec(czhm__kbbz, {'bodo': bodo, 'numba': numba, 'np': np}, gffh__yhjz)
    impl = gffh__yhjz['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    thgh__zsbkt = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    zxnf__cjt = toty(fromty)
    wpd__nji = context.compile_internal(builder, thgh__zsbkt, zxnf__cjt, (val,)
        )
    return impl_ret_new_ref(context, builder, toty, wpd__nji)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    nbegq__trd = arr._data
    xata__lehg = len(nbegq__trd)
    zlg__zkjrc = pre_alloc_string_array(xata__lehg, -1)
    if regex:
        ipb__bdc = re.compile(pat, flags)
        for pnwk__ujug in range(xata__lehg):
            if bodo.libs.array_kernels.isna(nbegq__trd, pnwk__ujug):
                bodo.libs.array_kernels.setna(zlg__zkjrc, pnwk__ujug)
                continue
            zlg__zkjrc[pnwk__ujug] = ipb__bdc.sub(repl=repl, string=
                nbegq__trd[pnwk__ujug])
    else:
        for pnwk__ujug in range(xata__lehg):
            if bodo.libs.array_kernels.isna(nbegq__trd, pnwk__ujug):
                bodo.libs.array_kernels.setna(zlg__zkjrc, pnwk__ujug)
                continue
            zlg__zkjrc[pnwk__ujug] = nbegq__trd[pnwk__ujug].replace(pat, repl)
    return init_dict_arr(zlg__zkjrc, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    rejsg__gjftu = arr._data
    hryw__nwtxk = len(rejsg__gjftu)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(hryw__nwtxk)
    for pnwk__ujug in range(hryw__nwtxk):
        dict_arr_out[pnwk__ujug] = rejsg__gjftu[pnwk__ujug].startswith(pat)
    cgp__lijny = arr._indices
    nhtgr__mfas = len(cgp__lijny)
    aywo__gcxh = bodo.libs.bool_arr_ext.alloc_bool_array(nhtgr__mfas)
    for pnwk__ujug in range(nhtgr__mfas):
        if bodo.libs.array_kernels.isna(arr, pnwk__ujug):
            bodo.libs.array_kernels.setna(aywo__gcxh, pnwk__ujug)
        else:
            aywo__gcxh[pnwk__ujug] = dict_arr_out[cgp__lijny[pnwk__ujug]]
    return aywo__gcxh


@register_jitable
def str_endswith(arr, pat, na):
    rejsg__gjftu = arr._data
    hryw__nwtxk = len(rejsg__gjftu)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(hryw__nwtxk)
    for pnwk__ujug in range(hryw__nwtxk):
        dict_arr_out[pnwk__ujug] = rejsg__gjftu[pnwk__ujug].endswith(pat)
    cgp__lijny = arr._indices
    nhtgr__mfas = len(cgp__lijny)
    aywo__gcxh = bodo.libs.bool_arr_ext.alloc_bool_array(nhtgr__mfas)
    for pnwk__ujug in range(nhtgr__mfas):
        if bodo.libs.array_kernels.isna(arr, pnwk__ujug):
            bodo.libs.array_kernels.setna(aywo__gcxh, pnwk__ujug)
        else:
            aywo__gcxh[pnwk__ujug] = dict_arr_out[cgp__lijny[pnwk__ujug]]
    return aywo__gcxh


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    rejsg__gjftu = arr._data
    mbzr__uwg = pd.Series(rejsg__gjftu)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = mbzr__uwg.array._str_contains(pat, case, flags, na,
            regex)
    cgp__lijny = arr._indices
    nhtgr__mfas = len(cgp__lijny)
    aywo__gcxh = bodo.libs.bool_arr_ext.alloc_bool_array(nhtgr__mfas)
    for pnwk__ujug in range(nhtgr__mfas):
        if bodo.libs.array_kernels.isna(arr, pnwk__ujug):
            bodo.libs.array_kernels.setna(aywo__gcxh, pnwk__ujug)
        else:
            aywo__gcxh[pnwk__ujug] = dict_arr_out[cgp__lijny[pnwk__ujug]]
    return aywo__gcxh


@register_jitable
def str_contains_non_regex(arr, pat, case):
    rejsg__gjftu = arr._data
    hryw__nwtxk = len(rejsg__gjftu)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(hryw__nwtxk)
    if not case:
        pxek__jfx = pat.upper()
    for pnwk__ujug in range(hryw__nwtxk):
        if case:
            dict_arr_out[pnwk__ujug] = pat in rejsg__gjftu[pnwk__ujug]
        else:
            dict_arr_out[pnwk__ujug] = pxek__jfx in rejsg__gjftu[pnwk__ujug
                ].upper()
    cgp__lijny = arr._indices
    nhtgr__mfas = len(cgp__lijny)
    aywo__gcxh = bodo.libs.bool_arr_ext.alloc_bool_array(nhtgr__mfas)
    for pnwk__ujug in range(nhtgr__mfas):
        if bodo.libs.array_kernels.isna(arr, pnwk__ujug):
            bodo.libs.array_kernels.setna(aywo__gcxh, pnwk__ujug)
        else:
            aywo__gcxh[pnwk__ujug] = dict_arr_out[cgp__lijny[pnwk__ujug]]
    return aywo__gcxh
