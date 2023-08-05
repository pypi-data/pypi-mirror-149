import enum
import operator
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.typing import NOT_CONSTANT, BodoError, MetaType, check_unsupported_args, dtype_to_array_type, get_literal_value, get_overload_const, get_overload_const_bool, is_common_scalar_dtype, is_iterable_type, is_list_like_index_type, is_literal_type, is_overload_constant_bool, is_overload_none, is_overload_true, is_scalar_type, raise_bodo_error


class PDCategoricalDtype(types.Opaque):

    def __init__(self, categories, elem_type, ordered, data=None, int_type=None
        ):
        self.categories = categories
        self.elem_type = elem_type
        self.ordered = ordered
        self.data = _get_cat_index_type(elem_type) if data is None else data
        self.int_type = int_type
        wyhqh__nlk = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=wyhqh__nlk)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    xkk__qvbeh = tuple(val.categories.values)
    elem_type = None if len(xkk__qvbeh) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(xkk__qvbeh, elem_type, val.ordered, bodo.
        typeof(val.categories), int_type)


def _get_cat_index_type(elem_type):
    elem_type = bodo.string_type if elem_type is None else elem_type
    return bodo.utils.typing.get_index_type_from_dtype(elem_type)


@lower_constant(PDCategoricalDtype)
def lower_constant_categorical_type(context, builder, typ, pyval):
    categories = context.get_constant_generic(builder, bodo.typeof(pyval.
        categories), pyval.categories)
    ordered = context.get_constant(types.bool_, pyval.ordered)
    return lir.Constant.literal_struct([categories, ordered])


@register_model(PDCategoricalDtype)
class PDCategoricalDtypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zrlj__qidpq = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, zrlj__qidpq)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    mrtq__bzex = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    blqmm__bdrg = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, zlhtr__pqr, zlhtr__pqr = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    fidha__fqjy = PDCategoricalDtype(blqmm__bdrg, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, mrtq__bzex)
    return fidha__fqjy(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    xflsc__qoj = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, xflsc__qoj).value
    c.pyapi.decref(xflsc__qoj)
    gmhe__kukuq = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, gmhe__kukuq).value
    c.pyapi.decref(gmhe__kukuq)
    xyop__oiin = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=xyop__oiin)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    xflsc__qoj = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    jhgf__jaixe = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    sgcfy__lsd = c.context.insert_const_string(c.builder.module, 'pandas')
    cyp__tfi = c.pyapi.import_module_noblock(sgcfy__lsd)
    duso__hore = c.pyapi.call_method(cyp__tfi, 'CategoricalDtype', (
        jhgf__jaixe, xflsc__qoj))
    c.pyapi.decref(xflsc__qoj)
    c.pyapi.decref(jhgf__jaixe)
    c.pyapi.decref(cyp__tfi)
    c.context.nrt.decref(c.builder, typ, val)
    return duso__hore


@overload_attribute(PDCategoricalDtype, 'nbytes')
def pd_categorical_nbytes_overload(A):
    return lambda A: A.categories.nbytes + bodo.io.np_io.get_dtype_size(types
        .bool_)


class CategoricalArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(CategoricalArrayType, self).__init__(name=
            f'CategoricalArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return CategoricalArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.Categorical)
def _typeof_pd_cat(val, c):
    return CategoricalArrayType(bodo.typeof(val.dtype))


@register_model(CategoricalArrayType)
class CategoricalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nun__tbtzj = get_categories_int_type(fe_type.dtype)
        zrlj__qidpq = [('dtype', fe_type.dtype), ('codes', types.Array(
            nun__tbtzj, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, zrlj__qidpq)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    qgvf__odb = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), qgvf__odb
        ).value
    c.pyapi.decref(qgvf__odb)
    duso__hore = c.pyapi.object_getattr_string(val, 'dtype')
    icb__mskmv = c.pyapi.to_native_value(typ.dtype, duso__hore).value
    c.pyapi.decref(duso__hore)
    bnt__sdhui = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bnt__sdhui.codes = codes
    bnt__sdhui.dtype = icb__mskmv
    return NativeValue(bnt__sdhui._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    agsk__fvfj = get_categories_int_type(typ.dtype)
    cuz__mvbq = context.get_constant_generic(builder, types.Array(
        agsk__fvfj, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, cuz__mvbq])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    hfjb__gtj = len(cat_dtype.categories)
    if hfjb__gtj < np.iinfo(np.int8).max:
        dtype = types.int8
    elif hfjb__gtj < np.iinfo(np.int16).max:
        dtype = types.int16
    elif hfjb__gtj < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    sgcfy__lsd = c.context.insert_const_string(c.builder.module, 'pandas')
    cyp__tfi = c.pyapi.import_module_noblock(sgcfy__lsd)
    nun__tbtzj = get_categories_int_type(dtype)
    zsue__ioi = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    tux__tgco = types.Array(nun__tbtzj, 1, 'C')
    c.context.nrt.incref(c.builder, tux__tgco, zsue__ioi.codes)
    qgvf__odb = c.pyapi.from_native_value(tux__tgco, zsue__ioi.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, zsue__ioi.dtype)
    duso__hore = c.pyapi.from_native_value(dtype, zsue__ioi.dtype, c.
        env_manager)
    usw__vgidp = c.pyapi.borrow_none()
    lxb__pfpw = c.pyapi.object_getattr_string(cyp__tfi, 'Categorical')
    kezf__suq = c.pyapi.call_method(lxb__pfpw, 'from_codes', (qgvf__odb,
        usw__vgidp, usw__vgidp, duso__hore))
    c.pyapi.decref(lxb__pfpw)
    c.pyapi.decref(qgvf__odb)
    c.pyapi.decref(duso__hore)
    c.pyapi.decref(cyp__tfi)
    c.context.nrt.decref(c.builder, typ, val)
    return kezf__suq


def _to_readonly(t):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, TimedeltaIndexType
    if isinstance(t, CategoricalArrayType):
        return CategoricalArrayType(_to_readonly(t.dtype))
    if isinstance(t, PDCategoricalDtype):
        return PDCategoricalDtype(t.categories, t.elem_type, t.ordered,
            _to_readonly(t.data), t.int_type)
    if isinstance(t, types.Array):
        return types.Array(t.dtype, t.ndim, 'C', True)
    if isinstance(t, NumericIndexType):
        return NumericIndexType(t.dtype, t.name_typ, _to_readonly(t.data))
    if isinstance(t, (DatetimeIndexType, TimedeltaIndexType)):
        return t.__class__(t.name_typ, _to_readonly(t.data))
    return t


@lower_cast(CategoricalArrayType, CategoricalArrayType)
def cast_cat_arr(context, builder, fromty, toty, val):
    if _to_readonly(toty) == fromty:
        return val
    raise BodoError(f'Cannot cast from {fromty} to {toty}')


def create_cmp_op_overload(op):

    def overload_cat_arr_cmp(A, other):
        if not isinstance(A, CategoricalArrayType):
            return
        if A.dtype.categories and is_literal_type(other) and types.unliteral(
            other) == A.dtype.elem_type:
            val = get_literal_value(other)
            rxisa__pjy = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                tiq__vqocj = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), rxisa__pjy)
                return tiq__vqocj
            return impl_lit

        def impl(A, other):
            rxisa__pjy = get_code_for_value(A.dtype, other)
            tiq__vqocj = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), rxisa__pjy)
            return tiq__vqocj
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        ltku__oeyp = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(ltku__oeyp)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    zsue__ioi = cat_dtype.categories
    n = len(zsue__ioi)
    for fjevc__xdd in range(n):
        if zsue__ioi[fjevc__xdd] == val:
            return fjevc__xdd
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    szmxr__idt = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype'
        )
    if szmxr__idt != A.dtype.elem_type and szmxr__idt != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if szmxr__idt == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            tiq__vqocj = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for fjevc__xdd in numba.parfors.parfor.internal_prange(n):
                sobfq__kpcs = codes[fjevc__xdd]
                if sobfq__kpcs == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(tiq__vqocj
                            , fjevc__xdd)
                    else:
                        bodo.libs.array_kernels.setna(tiq__vqocj, fjevc__xdd)
                    continue
                tiq__vqocj[fjevc__xdd] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[sobfq__kpcs]))
            return tiq__vqocj
        return impl
    tux__tgco = dtype_to_array_type(szmxr__idt)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        tiq__vqocj = bodo.utils.utils.alloc_type(n, tux__tgco, (-1,))
        for fjevc__xdd in numba.parfors.parfor.internal_prange(n):
            sobfq__kpcs = codes[fjevc__xdd]
            if sobfq__kpcs == -1:
                bodo.libs.array_kernels.setna(tiq__vqocj, fjevc__xdd)
                continue
            tiq__vqocj[fjevc__xdd] = bodo.utils.conversion.unbox_if_timestamp(
                categories[sobfq__kpcs])
        return tiq__vqocj
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        xco__dei, icb__mskmv = args
        zsue__ioi = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        zsue__ioi.codes = xco__dei
        zsue__ioi.dtype = icb__mskmv
        context.nrt.incref(builder, signature.args[0], xco__dei)
        context.nrt.incref(builder, signature.args[1], icb__mskmv)
        return zsue__ioi._getvalue()
    vlj__duyfy = CategoricalArrayType(cat_dtype)
    sig = vlj__duyfy(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    loih__oftrt = args[0]
    if equiv_set.has_shape(loih__oftrt):
        return ArrayAnalysis.AnalyzeResult(shape=loih__oftrt, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    nun__tbtzj = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, nun__tbtzj)
        return init_categorical_array(codes, cat_dtype)
    return impl


def alloc_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_alloc_categorical_array
    ) = alloc_categorical_array_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_categorical_arr_codes(A):
    return lambda A: A.codes


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_categorical_array',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_categorical_arr_codes',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func


@overload_method(CategoricalArrayType, 'copy', no_unliteral=True)
def cat_arr_copy_overload(arr):
    return lambda arr: init_categorical_array(arr.codes.copy(), arr.dtype)


def build_replace_dicts(to_replace, value, categories):
    return dict(), np.empty(len(categories) + 1), 0


@overload(build_replace_dicts, no_unliteral=True)
def _build_replace_dicts(to_replace, value, categories):
    if isinstance(to_replace, types.Number) or to_replace == bodo.string_type:

        def impl(to_replace, value, categories):
            return build_replace_dicts([to_replace], value, categories)
        return impl
    else:

        def impl(to_replace, value, categories):
            n = len(categories)
            wzj__oiq = {}
            cuz__mvbq = np.empty(n + 1, np.int64)
            nhzb__nmfa = {}
            guqrm__atgdt = []
            kvemq__tqrgz = {}
            for fjevc__xdd in range(n):
                kvemq__tqrgz[categories[fjevc__xdd]] = fjevc__xdd
            for mwhbc__nfbv in to_replace:
                if mwhbc__nfbv != value:
                    if mwhbc__nfbv in kvemq__tqrgz:
                        if value in kvemq__tqrgz:
                            wzj__oiq[mwhbc__nfbv] = mwhbc__nfbv
                            soegs__lwd = kvemq__tqrgz[mwhbc__nfbv]
                            nhzb__nmfa[soegs__lwd] = kvemq__tqrgz[value]
                            guqrm__atgdt.append(soegs__lwd)
                        else:
                            wzj__oiq[mwhbc__nfbv] = value
                            kvemq__tqrgz[value] = kvemq__tqrgz[mwhbc__nfbv]
            zqtvz__pgcnr = np.sort(np.array(guqrm__atgdt))
            aqtp__pgpj = 0
            ertgk__bdrz = []
            for gjymz__njt in range(-1, n):
                while aqtp__pgpj < len(zqtvz__pgcnr
                    ) and gjymz__njt > zqtvz__pgcnr[aqtp__pgpj]:
                    aqtp__pgpj += 1
                ertgk__bdrz.append(aqtp__pgpj)
            for wun__kpu in range(-1, n):
                bicwp__bctpx = wun__kpu
                if wun__kpu in nhzb__nmfa:
                    bicwp__bctpx = nhzb__nmfa[wun__kpu]
                cuz__mvbq[wun__kpu + 1] = bicwp__bctpx - ertgk__bdrz[
                    bicwp__bctpx + 1]
            return wzj__oiq, cuz__mvbq, len(zqtvz__pgcnr)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for fjevc__xdd in range(len(new_codes_arr)):
        new_codes_arr[fjevc__xdd] = codes_map_arr[old_codes_arr[fjevc__xdd] + 1
            ]


@overload_method(CategoricalArrayType, 'replace', inline='always',
    no_unliteral=True)
def overload_replace(arr, to_replace, value):

    def impl(arr, to_replace, value):
        return bodo.hiframes.pd_categorical_ext.cat_replace(arr, to_replace,
            value)
    return impl


def cat_replace(arr, to_replace, value):
    return


@overload(cat_replace, no_unliteral=True)
def cat_replace_overload(arr, to_replace, value):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_replace,
        'CategoricalArray.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'CategoricalArray.replace()')
    gdktg__fwufx = arr.dtype.ordered
    rlexz__dkvv = arr.dtype.elem_type
    xjhk__ywji = get_overload_const(to_replace)
    omvz__uqv = get_overload_const(value)
    if (arr.dtype.categories is not None and xjhk__ywji is not NOT_CONSTANT and
        omvz__uqv is not NOT_CONSTANT):
        lse__ojybj, codes_map_arr, zlhtr__pqr = python_build_replace_dicts(
            xjhk__ywji, omvz__uqv, arr.dtype.categories)
        if len(lse__ojybj) == 0:
            return lambda arr, to_replace, value: arr.copy()
        hnz__wef = []
        for fwjt__oeb in arr.dtype.categories:
            if fwjt__oeb in lse__ojybj:
                czs__lurm = lse__ojybj[fwjt__oeb]
                if czs__lurm != fwjt__oeb:
                    hnz__wef.append(czs__lurm)
            else:
                hnz__wef.append(fwjt__oeb)
        fxq__dgwzr = pd.CategoricalDtype(hnz__wef, gdktg__fwufx
            ).categories.values
        fog__obfi = MetaType(tuple(fxq__dgwzr))

        def impl_dtype(arr, to_replace, value):
            vyfge__qybgq = init_cat_dtype(bodo.utils.conversion.
                index_from_array(fxq__dgwzr), gdktg__fwufx, None, fog__obfi)
            zsue__ioi = alloc_categorical_array(len(arr.codes), vyfge__qybgq)
            reassign_codes(zsue__ioi.codes, arr.codes, codes_map_arr)
            return zsue__ioi
        return impl_dtype
    rlexz__dkvv = arr.dtype.elem_type
    if rlexz__dkvv == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            wzj__oiq, codes_map_arr, lqide__baey = build_replace_dicts(
                to_replace, value, categories.values)
            if len(wzj__oiq) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), gdktg__fwufx,
                    None, None))
            n = len(categories)
            fxq__dgwzr = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                lqide__baey, -1)
            tawd__kngrm = 0
            for gjymz__njt in range(n):
                yfh__trobn = categories[gjymz__njt]
                if yfh__trobn in wzj__oiq:
                    iszw__fzrye = wzj__oiq[yfh__trobn]
                    if iszw__fzrye != yfh__trobn:
                        fxq__dgwzr[tawd__kngrm] = iszw__fzrye
                        tawd__kngrm += 1
                else:
                    fxq__dgwzr[tawd__kngrm] = yfh__trobn
                    tawd__kngrm += 1
            zsue__ioi = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                fxq__dgwzr), gdktg__fwufx, None, None))
            reassign_codes(zsue__ioi.codes, arr.codes, codes_map_arr)
            return zsue__ioi
        return impl_str
    ueoxt__azl = dtype_to_array_type(rlexz__dkvv)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        wzj__oiq, codes_map_arr, lqide__baey = build_replace_dicts(to_replace,
            value, categories.values)
        if len(wzj__oiq) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), gdktg__fwufx, None, None))
        n = len(categories)
        fxq__dgwzr = bodo.utils.utils.alloc_type(n - lqide__baey,
            ueoxt__azl, None)
        tawd__kngrm = 0
        for fjevc__xdd in range(n):
            yfh__trobn = categories[fjevc__xdd]
            if yfh__trobn in wzj__oiq:
                iszw__fzrye = wzj__oiq[yfh__trobn]
                if iszw__fzrye != yfh__trobn:
                    fxq__dgwzr[tawd__kngrm] = iszw__fzrye
                    tawd__kngrm += 1
            else:
                fxq__dgwzr[tawd__kngrm] = yfh__trobn
                tawd__kngrm += 1
        zsue__ioi = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(fxq__dgwzr),
            gdktg__fwufx, None, None))
        reassign_codes(zsue__ioi.codes, arr.codes, codes_map_arr)
        return zsue__ioi
    return impl


@overload(len, no_unliteral=True)
def overload_cat_arr_len(A):
    if isinstance(A, CategoricalArrayType):
        return lambda A: len(A.codes)


@overload_attribute(CategoricalArrayType, 'shape')
def overload_cat_arr_shape(A):
    return lambda A: (len(A.codes),)


@overload_attribute(CategoricalArrayType, 'ndim')
def overload_cat_arr_ndim(A):
    return lambda A: 1


@overload_attribute(CategoricalArrayType, 'nbytes')
def cat_arr_nbytes_overload(A):
    return lambda A: A.codes.nbytes + A.dtype.nbytes


@register_jitable
def get_label_dict_from_categories(vals):
    jlrg__qkfs = dict()
    jyn__unom = 0
    for fjevc__xdd in range(len(vals)):
        val = vals[fjevc__xdd]
        if val in jlrg__qkfs:
            continue
        jlrg__qkfs[val] = jyn__unom
        jyn__unom += 1
    return jlrg__qkfs


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    jlrg__qkfs = dict()
    for fjevc__xdd in range(len(vals)):
        val = vals[fjevc__xdd]
        jlrg__qkfs[val] = fjevc__xdd
    return jlrg__qkfs


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    sfk__dlvp = dict(fastpath=fastpath)
    rpbcv__hcf = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', sfk__dlvp, rpbcv__hcf)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        aws__uxafw = get_overload_const(categories)
        if aws__uxafw is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                lgdt__yflvf = False
            else:
                lgdt__yflvf = get_overload_const_bool(ordered)
            vjn__sns = pd.CategoricalDtype(aws__uxafw, lgdt__yflvf
                ).categories.values
            npfm__pxtfz = MetaType(tuple(vjn__sns))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                vyfge__qybgq = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(vjn__sns), lgdt__yflvf, None, npfm__pxtfz)
                return bodo.utils.conversion.fix_arr_dtype(data, vyfge__qybgq)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            xkk__qvbeh = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                xkk__qvbeh, ordered, None, None)
            return bodo.utils.conversion.fix_arr_dtype(data, cat_dtype)
        return impl_cats
    elif is_overload_none(ordered):

        def impl_auto(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, 'category')
        return impl_auto
    raise BodoError(
        f'pd.Categorical(): argument combination not supported yet: {values}, {categories}, {ordered}, {dtype}'
        )


@overload(operator.getitem, no_unliteral=True)
def categorical_array_getitem(arr, ind):
    if not isinstance(arr, CategoricalArrayType):
        return
    if isinstance(ind, types.Integer):

        def categorical_getitem_impl(arr, ind):
            vieva__tpnij = arr.codes[ind]
            return arr.dtype.categories[max(vieva__tpnij, 0)]
        return categorical_getitem_impl
    if is_list_like_index_type(ind) or isinstance(ind, types.SliceType):

        def impl_bool(arr, ind):
            return init_categorical_array(arr.codes[ind], arr.dtype)
        return impl_bool
    raise BodoError(
        f'getitem for CategoricalArrayType with indexing type {ind} not supported.'
        )


class CategoricalMatchingValues(enum.Enum):
    DIFFERENT_TYPES = -1
    DONT_MATCH = 0
    MAY_MATCH = 1
    DO_MATCH = 2


def categorical_arrs_match(arr1, arr2):
    if not (isinstance(arr1, CategoricalArrayType) and isinstance(arr2,
        CategoricalArrayType)):
        return CategoricalMatchingValues.DIFFERENT_TYPES
    if arr1.dtype.categories is None or arr2.dtype.categories is None:
        return CategoricalMatchingValues.MAY_MATCH
    return (CategoricalMatchingValues.DO_MATCH if arr1.dtype.categories ==
        arr2.dtype.categories and arr1.dtype.ordered == arr2.dtype.ordered else
        CategoricalMatchingValues.DONT_MATCH)


@register_jitable
def cat_dtype_equal(dtype1, dtype2):
    if dtype1.ordered != dtype2.ordered or len(dtype1.categories) != len(dtype2
        .categories):
        return False
    arr1 = dtype1.categories.values
    arr2 = dtype2.categories.values
    for fjevc__xdd in range(len(arr1)):
        if arr1[fjevc__xdd] != arr2[fjevc__xdd]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    hykzs__zmt = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    mlgnd__hvbd = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    qpgbg__nkk = categorical_arrs_match(arr, val)
    ors__zpkgx = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    bkipx__ksazb = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not hykzs__zmt:
            raise BodoError(ors__zpkgx)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            vieva__tpnij = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = vieva__tpnij
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (hykzs__zmt or mlgnd__hvbd or qpgbg__nkk !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ors__zpkgx)
        if qpgbg__nkk == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bkipx__ksazb)
        if hykzs__zmt:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                imd__cnwj = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for gjymz__njt in range(n):
                    arr.codes[ind[gjymz__njt]] = imd__cnwj
            return impl_scalar
        if qpgbg__nkk == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for fjevc__xdd in range(n):
                    arr.codes[ind[fjevc__xdd]] = val.codes[fjevc__xdd]
            return impl_arr_ind_mask
        if qpgbg__nkk == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bkipx__ksazb)
                n = len(val.codes)
                for fjevc__xdd in range(n):
                    arr.codes[ind[fjevc__xdd]] = val.codes[fjevc__xdd]
            return impl_arr_ind_mask
        if mlgnd__hvbd:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for gjymz__njt in range(n):
                    kah__qdk = bodo.utils.conversion.unbox_if_timestamp(val
                        [gjymz__njt])
                    if kah__qdk not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    vieva__tpnij = categories.get_loc(kah__qdk)
                    arr.codes[ind[gjymz__njt]] = vieva__tpnij
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (hykzs__zmt or mlgnd__hvbd or qpgbg__nkk !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ors__zpkgx)
        if qpgbg__nkk == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bkipx__ksazb)
        if hykzs__zmt:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                imd__cnwj = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for gjymz__njt in range(n):
                    if ind[gjymz__njt]:
                        arr.codes[gjymz__njt] = imd__cnwj
            return impl_scalar
        if qpgbg__nkk == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                mrwks__atq = 0
                for fjevc__xdd in range(n):
                    if ind[fjevc__xdd]:
                        arr.codes[fjevc__xdd] = val.codes[mrwks__atq]
                        mrwks__atq += 1
            return impl_bool_ind_mask
        if qpgbg__nkk == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bkipx__ksazb)
                n = len(ind)
                mrwks__atq = 0
                for fjevc__xdd in range(n):
                    if ind[fjevc__xdd]:
                        arr.codes[fjevc__xdd] = val.codes[mrwks__atq]
                        mrwks__atq += 1
            return impl_bool_ind_mask
        if mlgnd__hvbd:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                mrwks__atq = 0
                categories = arr.dtype.categories
                for gjymz__njt in range(n):
                    if ind[gjymz__njt]:
                        kah__qdk = bodo.utils.conversion.unbox_if_timestamp(val
                            [mrwks__atq])
                        if kah__qdk not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        vieva__tpnij = categories.get_loc(kah__qdk)
                        arr.codes[gjymz__njt] = vieva__tpnij
                        mrwks__atq += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (hykzs__zmt or mlgnd__hvbd or qpgbg__nkk !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ors__zpkgx)
        if qpgbg__nkk == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bkipx__ksazb)
        if hykzs__zmt:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                imd__cnwj = arr.dtype.categories.get_loc(val)
                mrhwg__qbnnf = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for gjymz__njt in range(mrhwg__qbnnf.start, mrhwg__qbnnf.
                    stop, mrhwg__qbnnf.step):
                    arr.codes[gjymz__njt] = imd__cnwj
            return impl_scalar
        if qpgbg__nkk == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if qpgbg__nkk == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bkipx__ksazb)
                arr.codes[ind] = val.codes
            return impl_arr
        if mlgnd__hvbd:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                mrhwg__qbnnf = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                mrwks__atq = 0
                for gjymz__njt in range(mrhwg__qbnnf.start, mrhwg__qbnnf.
                    stop, mrhwg__qbnnf.step):
                    kah__qdk = bodo.utils.conversion.unbox_if_timestamp(val
                        [mrwks__atq])
                    if kah__qdk not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    vieva__tpnij = categories.get_loc(kah__qdk)
                    arr.codes[gjymz__njt] = vieva__tpnij
                    mrwks__atq += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
