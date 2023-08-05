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
        dkbx__gxph = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, dkbx__gxph)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        ayzep__sadvj, spiab__vajl, fzlg__qggpu = args
        npry__znaqi = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        npry__znaqi.data = ayzep__sadvj
        npry__znaqi.indices = spiab__vajl
        npry__znaqi.has_global_dictionary = fzlg__qggpu
        context.nrt.incref(builder, signature.args[0], ayzep__sadvj)
        context.nrt.incref(builder, signature.args[1], spiab__vajl)
        return npry__znaqi._getvalue()
    uzmwy__xhja = DictionaryArrayType(data_t)
    xcxy__dhpka = uzmwy__xhja(data_t, indices_t, types.bool_)
    return xcxy__dhpka, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    for blmnq__jpy in range(len(A)):
        if pd.isna(A[blmnq__jpy]):
            A[blmnq__jpy] = None
    return pa.array(A).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    if bodo.hiframes.boxing._use_dict_str_type:
        blr__rrs = c.pyapi.unserialize(c.pyapi.serialize_object(to_pa_dict_arr)
            )
        val = c.pyapi.call_function_objargs(blr__rrs, [val])
        c.pyapi.decref(blr__rrs)
    npry__znaqi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hcc__ohnqj = c.pyapi.object_getattr_string(val, 'dictionary')
    qecm__ckhl = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    jyhl__agiar = c.pyapi.call_method(hcc__ohnqj, 'to_numpy', (qecm__ckhl,))
    npry__znaqi.data = c.unbox(typ.data, jyhl__agiar).value
    mua__mty = c.pyapi.object_getattr_string(val, 'indices')
    jtxvc__ltwuw = c.context.insert_const_string(c.builder.module, 'pandas')
    crhcb__odplc = c.pyapi.import_module_noblock(jtxvc__ltwuw)
    ckfk__ryyst = c.pyapi.string_from_constant_string('Int32')
    ourjd__vfv = c.pyapi.call_method(crhcb__odplc, 'array', (mua__mty,
        ckfk__ryyst))
    npry__znaqi.indices = c.unbox(dict_indices_arr_type, ourjd__vfv).value
    npry__znaqi.has_global_dictionary = c.context.get_constant(types.bool_,
        False)
    c.pyapi.decref(hcc__ohnqj)
    c.pyapi.decref(qecm__ckhl)
    c.pyapi.decref(jyhl__agiar)
    c.pyapi.decref(mua__mty)
    c.pyapi.decref(crhcb__odplc)
    c.pyapi.decref(ckfk__ryyst)
    c.pyapi.decref(ourjd__vfv)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    qzu__ayt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(npry__znaqi._getvalue(), is_error=qzu__ayt)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    npry__znaqi = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, npry__znaqi.data)
        gufv__telyf = c.box(typ.data, npry__znaqi.data)
        gkxw__fycla = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, npry__znaqi.indices)
        siiqx__oqu = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        trcd__eqb = cgutils.get_or_insert_function(c.builder.module,
            siiqx__oqu, name='box_dict_str_array')
        zxgag__iuh = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, gkxw__fycla.data)
        howsi__pbmu = c.builder.extract_value(zxgag__iuh.shape, 0)
        uzbj__dbyz = zxgag__iuh.data
        iiwpj__mqlw = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, gkxw__fycla.null_bitmap).data
        jyhl__agiar = c.builder.call(trcd__eqb, [howsi__pbmu, gufv__telyf,
            uzbj__dbyz, iiwpj__mqlw])
        c.pyapi.decref(gufv__telyf)
    else:
        jtxvc__ltwuw = c.context.insert_const_string(c.builder.module,
            'pyarrow')
        ibls__qdgc = c.pyapi.import_module_noblock(jtxvc__ltwuw)
        cavy__ynvsq = c.pyapi.object_getattr_string(ibls__qdgc,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, npry__znaqi.data)
        gufv__telyf = c.box(typ.data, npry__znaqi.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, npry__znaqi.
            indices)
        mua__mty = c.box(dict_indices_arr_type, npry__znaqi.indices)
        vbxgz__nzcn = c.pyapi.call_method(cavy__ynvsq, 'from_arrays', (
            mua__mty, gufv__telyf))
        qecm__ckhl = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        jyhl__agiar = c.pyapi.call_method(vbxgz__nzcn, 'to_numpy', (
            qecm__ckhl,))
        c.pyapi.decref(ibls__qdgc)
        c.pyapi.decref(gufv__telyf)
        c.pyapi.decref(mua__mty)
        c.pyapi.decref(cavy__ynvsq)
        c.pyapi.decref(vbxgz__nzcn)
        c.pyapi.decref(qecm__ckhl)
    c.context.nrt.decref(c.builder, typ, val)
    return jyhl__agiar


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
    yitd__nwsn = pyval.dictionary.to_numpy(False)
    rvfxk__pklb = pd.array(pyval.indices, 'Int32')
    yitd__nwsn = context.get_constant_generic(builder, typ.data, yitd__nwsn)
    rvfxk__pklb = context.get_constant_generic(builder,
        dict_indices_arr_type, rvfxk__pklb)
    rnj__dbvam = context.get_constant(types.bool_, False)
    zefm__qkrss = lir.Constant.literal_struct([yitd__nwsn, rvfxk__pklb,
        rnj__dbvam])
    return zefm__qkrss


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            qeuu__mjb = A._indices[ind]
            return A._data[qeuu__mjb]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        ayzep__sadvj = A._data
        spiab__vajl = A._indices
        howsi__pbmu = len(spiab__vajl)
        qnsep__img = [get_str_arr_item_length(ayzep__sadvj, blmnq__jpy) for
            blmnq__jpy in range(len(ayzep__sadvj))]
        ven__kjzwz = 0
        for blmnq__jpy in range(howsi__pbmu):
            if not bodo.libs.array_kernels.isna(spiab__vajl, blmnq__jpy):
                ven__kjzwz += qnsep__img[spiab__vajl[blmnq__jpy]]
        qzd__mby = pre_alloc_string_array(howsi__pbmu, ven__kjzwz)
        for blmnq__jpy in range(howsi__pbmu):
            if bodo.libs.array_kernels.isna(spiab__vajl, blmnq__jpy):
                bodo.libs.array_kernels.setna(qzd__mby, blmnq__jpy)
                continue
            ind = spiab__vajl[blmnq__jpy]
            if bodo.libs.array_kernels.isna(ayzep__sadvj, ind):
                bodo.libs.array_kernels.setna(qzd__mby, blmnq__jpy)
                continue
            qzd__mby[blmnq__jpy] = ayzep__sadvj[ind]
        return qzd__mby
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    qeuu__mjb = -1
    ayzep__sadvj = arr._data
    for blmnq__jpy in range(len(ayzep__sadvj)):
        if bodo.libs.array_kernels.isna(ayzep__sadvj, blmnq__jpy):
            continue
        if ayzep__sadvj[blmnq__jpy] == val:
            qeuu__mjb = blmnq__jpy
            break
    return qeuu__mjb


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    howsi__pbmu = len(arr)
    qeuu__mjb = find_dict_ind(arr, val)
    if qeuu__mjb == -1:
        return init_bool_array(np.full(howsi__pbmu, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == qeuu__mjb


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    howsi__pbmu = len(arr)
    qeuu__mjb = find_dict_ind(arr, val)
    if qeuu__mjb == -1:
        return init_bool_array(np.full(howsi__pbmu, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != qeuu__mjb


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
        rsot__gsozm = arr._data
        ptrka__gjpyd = bodo.libs.int_arr_ext.alloc_int_array(len(
            rsot__gsozm), dtype)
        for vdcs__pue in range(len(rsot__gsozm)):
            if bodo.libs.array_kernels.isna(rsot__gsozm, vdcs__pue):
                bodo.libs.array_kernels.setna(ptrka__gjpyd, vdcs__pue)
                continue
            ptrka__gjpyd[vdcs__pue] = np.int64(rsot__gsozm[vdcs__pue])
        howsi__pbmu = len(arr)
        spiab__vajl = arr._indices
        qzd__mby = bodo.libs.int_arr_ext.alloc_int_array(howsi__pbmu, dtype)
        for blmnq__jpy in range(howsi__pbmu):
            if bodo.libs.array_kernels.isna(spiab__vajl, blmnq__jpy):
                bodo.libs.array_kernels.setna(qzd__mby, blmnq__jpy)
                continue
            qzd__mby[blmnq__jpy] = ptrka__gjpyd[spiab__vajl[blmnq__jpy]]
        return qzd__mby
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    equ__xduto = len(arrs)
    xmjj__wcytj = 'def impl(arrs, sep):\n'
    xmjj__wcytj += '  ind_map = {}\n'
    xmjj__wcytj += '  out_strs = []\n'
    xmjj__wcytj += '  n = len(arrs[0])\n'
    for blmnq__jpy in range(equ__xduto):
        xmjj__wcytj += f'  indices{blmnq__jpy} = arrs[{blmnq__jpy}]._indices\n'
    for blmnq__jpy in range(equ__xduto):
        xmjj__wcytj += f'  data{blmnq__jpy} = arrs[{blmnq__jpy}]._data\n'
    xmjj__wcytj += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    xmjj__wcytj += '  for i in range(n):\n'
    zol__soyvk = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{blmnq__jpy}], i)' for
        blmnq__jpy in range(equ__xduto)])
    xmjj__wcytj += f'    if {zol__soyvk}:\n'
    xmjj__wcytj += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    xmjj__wcytj += '      continue\n'
    for blmnq__jpy in range(equ__xduto):
        xmjj__wcytj += f'    ind{blmnq__jpy} = indices{blmnq__jpy}[i]\n'
    odoyj__pekmo = '(' + ', '.join(f'ind{blmnq__jpy}' for blmnq__jpy in
        range(equ__xduto)) + ')'
    xmjj__wcytj += f'    if {odoyj__pekmo} not in ind_map:\n'
    xmjj__wcytj += '      out_ind = len(out_strs)\n'
    xmjj__wcytj += f'      ind_map[{odoyj__pekmo}] = out_ind\n'
    gbmq__aajwb = "''" if is_overload_none(sep) else 'sep'
    divy__tzs = ', '.join([f'data{blmnq__jpy}[ind{blmnq__jpy}]' for
        blmnq__jpy in range(equ__xduto)])
    xmjj__wcytj += f'      v = {gbmq__aajwb}.join([{divy__tzs}])\n'
    xmjj__wcytj += '      out_strs.append(v)\n'
    xmjj__wcytj += '    else:\n'
    xmjj__wcytj += f'      out_ind = ind_map[{odoyj__pekmo}]\n'
    xmjj__wcytj += '    out_indices[i] = out_ind\n'
    xmjj__wcytj += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    xmjj__wcytj += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    byw__cgv = {}
    exec(xmjj__wcytj, {'bodo': bodo, 'numba': numba, 'np': np}, byw__cgv)
    impl = byw__cgv['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    kxof__ypfq = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    xcxy__dhpka = toty(fromty)
    sbz__fcguz = context.compile_internal(builder, kxof__ypfq, xcxy__dhpka,
        (val,))
    return impl_ret_new_ref(context, builder, toty, sbz__fcguz)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    yitd__nwsn = arr._data
    mcaxh__sed = len(yitd__nwsn)
    cbl__zvg = pre_alloc_string_array(mcaxh__sed, -1)
    if regex:
        flck__kkkf = re.compile(pat, flags)
        for blmnq__jpy in range(mcaxh__sed):
            if bodo.libs.array_kernels.isna(yitd__nwsn, blmnq__jpy):
                bodo.libs.array_kernels.setna(cbl__zvg, blmnq__jpy)
                continue
            cbl__zvg[blmnq__jpy] = flck__kkkf.sub(repl=repl, string=
                yitd__nwsn[blmnq__jpy])
    else:
        for blmnq__jpy in range(mcaxh__sed):
            if bodo.libs.array_kernels.isna(yitd__nwsn, blmnq__jpy):
                bodo.libs.array_kernels.setna(cbl__zvg, blmnq__jpy)
                continue
            cbl__zvg[blmnq__jpy] = yitd__nwsn[blmnq__jpy].replace(pat, repl)
    return init_dict_arr(cbl__zvg, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    npry__znaqi = arr._data
    llphj__hkmhh = len(npry__znaqi)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(llphj__hkmhh)
    for blmnq__jpy in range(llphj__hkmhh):
        dict_arr_out[blmnq__jpy] = npry__znaqi[blmnq__jpy].startswith(pat)
    rvfxk__pklb = arr._indices
    yqfdo__aum = len(rvfxk__pklb)
    qzd__mby = bodo.libs.bool_arr_ext.alloc_bool_array(yqfdo__aum)
    for blmnq__jpy in range(yqfdo__aum):
        if bodo.libs.array_kernels.isna(arr, blmnq__jpy):
            bodo.libs.array_kernels.setna(qzd__mby, blmnq__jpy)
        else:
            qzd__mby[blmnq__jpy] = dict_arr_out[rvfxk__pklb[blmnq__jpy]]
    return qzd__mby


@register_jitable
def str_endswith(arr, pat, na):
    npry__znaqi = arr._data
    llphj__hkmhh = len(npry__znaqi)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(llphj__hkmhh)
    for blmnq__jpy in range(llphj__hkmhh):
        dict_arr_out[blmnq__jpy] = npry__znaqi[blmnq__jpy].endswith(pat)
    rvfxk__pklb = arr._indices
    yqfdo__aum = len(rvfxk__pklb)
    qzd__mby = bodo.libs.bool_arr_ext.alloc_bool_array(yqfdo__aum)
    for blmnq__jpy in range(yqfdo__aum):
        if bodo.libs.array_kernels.isna(arr, blmnq__jpy):
            bodo.libs.array_kernels.setna(qzd__mby, blmnq__jpy)
        else:
            qzd__mby[blmnq__jpy] = dict_arr_out[rvfxk__pklb[blmnq__jpy]]
    return qzd__mby


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    npry__znaqi = arr._data
    ncjd__ljb = pd.Series(npry__znaqi)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = ncjd__ljb.array._str_contains(pat, case, flags, na,
            regex)
    rvfxk__pklb = arr._indices
    yqfdo__aum = len(rvfxk__pklb)
    qzd__mby = bodo.libs.bool_arr_ext.alloc_bool_array(yqfdo__aum)
    for blmnq__jpy in range(yqfdo__aum):
        if bodo.libs.array_kernels.isna(arr, blmnq__jpy):
            bodo.libs.array_kernels.setna(qzd__mby, blmnq__jpy)
        else:
            qzd__mby[blmnq__jpy] = dict_arr_out[rvfxk__pklb[blmnq__jpy]]
    return qzd__mby


@register_jitable
def str_contains_non_regex(arr, pat, case):
    npry__znaqi = arr._data
    llphj__hkmhh = len(npry__znaqi)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(llphj__hkmhh)
    if not case:
        wzpf__xped = pat.upper()
    for blmnq__jpy in range(llphj__hkmhh):
        if case:
            dict_arr_out[blmnq__jpy] = pat in npry__znaqi[blmnq__jpy]
        else:
            dict_arr_out[blmnq__jpy] = wzpf__xped in npry__znaqi[blmnq__jpy
                ].upper()
    rvfxk__pklb = arr._indices
    yqfdo__aum = len(rvfxk__pklb)
    qzd__mby = bodo.libs.bool_arr_ext.alloc_bool_array(yqfdo__aum)
    for blmnq__jpy in range(yqfdo__aum):
        if bodo.libs.array_kernels.isna(arr, blmnq__jpy):
            bodo.libs.array_kernels.setna(qzd__mby, blmnq__jpy)
        else:
            qzd__mby[blmnq__jpy] = dict_arr_out[rvfxk__pklb[blmnq__jpy]]
    return qzd__mby
