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
        gyt__gtfhj = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=gyt__gtfhj)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    qts__lpxf = tuple(val.categories.values)
    elem_type = None if len(qts__lpxf) == 0 else bodo.typeof(val.categories
        .values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(qts__lpxf, elem_type, val.ordered, bodo.
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
        ivn__hrg = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, ivn__hrg)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    znjdb__wth = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    ceqi__hmew = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, nul__wcnfj, nul__wcnfj = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    zxas__wmsk = PDCategoricalDtype(ceqi__hmew, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, znjdb__wth)
    return zxas__wmsk(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    deqnk__uzd = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, deqnk__uzd).value
    c.pyapi.decref(deqnk__uzd)
    vbo__qmrl = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, vbo__qmrl).value
    c.pyapi.decref(vbo__qmrl)
    peobh__slpa = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=peobh__slpa)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    deqnk__uzd = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    oib__uvj = c.pyapi.from_native_value(typ.data, cat_dtype.categories, c.
        env_manager)
    xci__kszc = c.context.insert_const_string(c.builder.module, 'pandas')
    otfw__ijvjh = c.pyapi.import_module_noblock(xci__kszc)
    qhds__rmhgs = c.pyapi.call_method(otfw__ijvjh, 'CategoricalDtype', (
        oib__uvj, deqnk__uzd))
    c.pyapi.decref(deqnk__uzd)
    c.pyapi.decref(oib__uvj)
    c.pyapi.decref(otfw__ijvjh)
    c.context.nrt.decref(c.builder, typ, val)
    return qhds__rmhgs


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
        sexe__fjz = get_categories_int_type(fe_type.dtype)
        ivn__hrg = [('dtype', fe_type.dtype), ('codes', types.Array(
            sexe__fjz, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, ivn__hrg)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    zdw__ffdlj = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), zdw__ffdlj
        ).value
    c.pyapi.decref(zdw__ffdlj)
    qhds__rmhgs = c.pyapi.object_getattr_string(val, 'dtype')
    ueys__xpm = c.pyapi.to_native_value(typ.dtype, qhds__rmhgs).value
    c.pyapi.decref(qhds__rmhgs)
    aolna__zrze = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    aolna__zrze.codes = codes
    aolna__zrze.dtype = ueys__xpm
    return NativeValue(aolna__zrze._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    eyow__kllp = get_categories_int_type(typ.dtype)
    pjha__ocn = context.get_constant_generic(builder, types.Array(
        eyow__kllp, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, pjha__ocn])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    asdlt__ddo = len(cat_dtype.categories)
    if asdlt__ddo < np.iinfo(np.int8).max:
        dtype = types.int8
    elif asdlt__ddo < np.iinfo(np.int16).max:
        dtype = types.int16
    elif asdlt__ddo < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    xci__kszc = c.context.insert_const_string(c.builder.module, 'pandas')
    otfw__ijvjh = c.pyapi.import_module_noblock(xci__kszc)
    sexe__fjz = get_categories_int_type(dtype)
    bhe__vglt = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    tkxz__aczra = types.Array(sexe__fjz, 1, 'C')
    c.context.nrt.incref(c.builder, tkxz__aczra, bhe__vglt.codes)
    zdw__ffdlj = c.pyapi.from_native_value(tkxz__aczra, bhe__vglt.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, bhe__vglt.dtype)
    qhds__rmhgs = c.pyapi.from_native_value(dtype, bhe__vglt.dtype, c.
        env_manager)
    oxf__vqvqm = c.pyapi.borrow_none()
    mbzju__kdo = c.pyapi.object_getattr_string(otfw__ijvjh, 'Categorical')
    cbtl__cidpy = c.pyapi.call_method(mbzju__kdo, 'from_codes', (zdw__ffdlj,
        oxf__vqvqm, oxf__vqvqm, qhds__rmhgs))
    c.pyapi.decref(mbzju__kdo)
    c.pyapi.decref(zdw__ffdlj)
    c.pyapi.decref(qhds__rmhgs)
    c.pyapi.decref(otfw__ijvjh)
    c.context.nrt.decref(c.builder, typ, val)
    return cbtl__cidpy


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
            yehgc__nej = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                ofvxa__zsn = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), yehgc__nej)
                return ofvxa__zsn
            return impl_lit

        def impl(A, other):
            yehgc__nej = get_code_for_value(A.dtype, other)
            ofvxa__zsn = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), yehgc__nej)
            return ofvxa__zsn
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        dmat__vqzqv = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(dmat__vqzqv)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    bhe__vglt = cat_dtype.categories
    n = len(bhe__vglt)
    for izgup__dziqw in range(n):
        if bhe__vglt[izgup__dziqw] == val:
            return izgup__dziqw
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    cresf__ywpi = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if cresf__ywpi != A.dtype.elem_type and cresf__ywpi != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if cresf__ywpi == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            ofvxa__zsn = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for izgup__dziqw in numba.parfors.parfor.internal_prange(n):
                kmjwg__hblxq = codes[izgup__dziqw]
                if kmjwg__hblxq == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(ofvxa__zsn
                            , izgup__dziqw)
                    else:
                        bodo.libs.array_kernels.setna(ofvxa__zsn, izgup__dziqw)
                    continue
                ofvxa__zsn[izgup__dziqw] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[kmjwg__hblxq]))
            return ofvxa__zsn
        return impl
    tkxz__aczra = dtype_to_array_type(cresf__ywpi)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        ofvxa__zsn = bodo.utils.utils.alloc_type(n, tkxz__aczra, (-1,))
        for izgup__dziqw in numba.parfors.parfor.internal_prange(n):
            kmjwg__hblxq = codes[izgup__dziqw]
            if kmjwg__hblxq == -1:
                bodo.libs.array_kernels.setna(ofvxa__zsn, izgup__dziqw)
                continue
            ofvxa__zsn[izgup__dziqw
                ] = bodo.utils.conversion.unbox_if_timestamp(categories[
                kmjwg__hblxq])
        return ofvxa__zsn
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        suk__kbv, ueys__xpm = args
        bhe__vglt = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        bhe__vglt.codes = suk__kbv
        bhe__vglt.dtype = ueys__xpm
        context.nrt.incref(builder, signature.args[0], suk__kbv)
        context.nrt.incref(builder, signature.args[1], ueys__xpm)
        return bhe__vglt._getvalue()
    ysc__pvwt = CategoricalArrayType(cat_dtype)
    sig = ysc__pvwt(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    nuoee__agt = args[0]
    if equiv_set.has_shape(nuoee__agt):
        return ArrayAnalysis.AnalyzeResult(shape=nuoee__agt, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    sexe__fjz = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, sexe__fjz)
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
            cxv__srbo = {}
            pjha__ocn = np.empty(n + 1, np.int64)
            vzxo__qsoc = {}
            stf__qrunl = []
            xwuy__uphb = {}
            for izgup__dziqw in range(n):
                xwuy__uphb[categories[izgup__dziqw]] = izgup__dziqw
            for wehf__owk in to_replace:
                if wehf__owk != value:
                    if wehf__owk in xwuy__uphb:
                        if value in xwuy__uphb:
                            cxv__srbo[wehf__owk] = wehf__owk
                            cetjr__idsu = xwuy__uphb[wehf__owk]
                            vzxo__qsoc[cetjr__idsu] = xwuy__uphb[value]
                            stf__qrunl.append(cetjr__idsu)
                        else:
                            cxv__srbo[wehf__owk] = value
                            xwuy__uphb[value] = xwuy__uphb[wehf__owk]
            ugib__ocm = np.sort(np.array(stf__qrunl))
            pqiy__zpfjo = 0
            ybe__ewuog = []
            for mjmzm__zwxx in range(-1, n):
                while pqiy__zpfjo < len(ugib__ocm) and mjmzm__zwxx > ugib__ocm[
                    pqiy__zpfjo]:
                    pqiy__zpfjo += 1
                ybe__ewuog.append(pqiy__zpfjo)
            for str__dfs in range(-1, n):
                exg__ilah = str__dfs
                if str__dfs in vzxo__qsoc:
                    exg__ilah = vzxo__qsoc[str__dfs]
                pjha__ocn[str__dfs + 1] = exg__ilah - ybe__ewuog[exg__ilah + 1]
            return cxv__srbo, pjha__ocn, len(ugib__ocm)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for izgup__dziqw in range(len(new_codes_arr)):
        new_codes_arr[izgup__dziqw] = codes_map_arr[old_codes_arr[
            izgup__dziqw] + 1]


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
    bwvug__dylo = arr.dtype.ordered
    dpqyx__lanuc = arr.dtype.elem_type
    sdbx__hof = get_overload_const(to_replace)
    yinv__qkt = get_overload_const(value)
    if (arr.dtype.categories is not None and sdbx__hof is not NOT_CONSTANT and
        yinv__qkt is not NOT_CONSTANT):
        nvvg__apwke, codes_map_arr, nul__wcnfj = python_build_replace_dicts(
            sdbx__hof, yinv__qkt, arr.dtype.categories)
        if len(nvvg__apwke) == 0:
            return lambda arr, to_replace, value: arr.copy()
        dtlbd__oen = []
        for xwzwj__uhr in arr.dtype.categories:
            if xwzwj__uhr in nvvg__apwke:
                dqc__ewmu = nvvg__apwke[xwzwj__uhr]
                if dqc__ewmu != xwzwj__uhr:
                    dtlbd__oen.append(dqc__ewmu)
            else:
                dtlbd__oen.append(xwzwj__uhr)
        fatwm__wids = pd.CategoricalDtype(dtlbd__oen, bwvug__dylo
            ).categories.values
        pkf__xdjav = MetaType(tuple(fatwm__wids))

        def impl_dtype(arr, to_replace, value):
            ggxif__byx = init_cat_dtype(bodo.utils.conversion.
                index_from_array(fatwm__wids), bwvug__dylo, None, pkf__xdjav)
            bhe__vglt = alloc_categorical_array(len(arr.codes), ggxif__byx)
            reassign_codes(bhe__vglt.codes, arr.codes, codes_map_arr)
            return bhe__vglt
        return impl_dtype
    dpqyx__lanuc = arr.dtype.elem_type
    if dpqyx__lanuc == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            cxv__srbo, codes_map_arr, urlt__cknr = build_replace_dicts(
                to_replace, value, categories.values)
            if len(cxv__srbo) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), bwvug__dylo,
                    None, None))
            n = len(categories)
            fatwm__wids = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                urlt__cknr, -1)
            luw__mftqs = 0
            for mjmzm__zwxx in range(n):
                ieu__pfo = categories[mjmzm__zwxx]
                if ieu__pfo in cxv__srbo:
                    fglp__cxg = cxv__srbo[ieu__pfo]
                    if fglp__cxg != ieu__pfo:
                        fatwm__wids[luw__mftqs] = fglp__cxg
                        luw__mftqs += 1
                else:
                    fatwm__wids[luw__mftqs] = ieu__pfo
                    luw__mftqs += 1
            bhe__vglt = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                fatwm__wids), bwvug__dylo, None, None))
            reassign_codes(bhe__vglt.codes, arr.codes, codes_map_arr)
            return bhe__vglt
        return impl_str
    rlzh__aud = dtype_to_array_type(dpqyx__lanuc)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        cxv__srbo, codes_map_arr, urlt__cknr = build_replace_dicts(to_replace,
            value, categories.values)
        if len(cxv__srbo) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), bwvug__dylo, None, None))
        n = len(categories)
        fatwm__wids = bodo.utils.utils.alloc_type(n - urlt__cknr, rlzh__aud,
            None)
        luw__mftqs = 0
        for izgup__dziqw in range(n):
            ieu__pfo = categories[izgup__dziqw]
            if ieu__pfo in cxv__srbo:
                fglp__cxg = cxv__srbo[ieu__pfo]
                if fglp__cxg != ieu__pfo:
                    fatwm__wids[luw__mftqs] = fglp__cxg
                    luw__mftqs += 1
            else:
                fatwm__wids[luw__mftqs] = ieu__pfo
                luw__mftqs += 1
        bhe__vglt = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(fatwm__wids),
            bwvug__dylo, None, None))
        reassign_codes(bhe__vglt.codes, arr.codes, codes_map_arr)
        return bhe__vglt
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
    otu__sjuku = dict()
    ucs__dgtvk = 0
    for izgup__dziqw in range(len(vals)):
        val = vals[izgup__dziqw]
        if val in otu__sjuku:
            continue
        otu__sjuku[val] = ucs__dgtvk
        ucs__dgtvk += 1
    return otu__sjuku


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    otu__sjuku = dict()
    for izgup__dziqw in range(len(vals)):
        val = vals[izgup__dziqw]
        otu__sjuku[val] = izgup__dziqw
    return otu__sjuku


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    utpg__dylh = dict(fastpath=fastpath)
    tuvhs__ukdwc = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', utpg__dylh, tuvhs__ukdwc)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        bnh__ovu = get_overload_const(categories)
        if bnh__ovu is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                gaas__lbk = False
            else:
                gaas__lbk = get_overload_const_bool(ordered)
            dfnnh__kazex = pd.CategoricalDtype(bnh__ovu, gaas__lbk
                ).categories.values
            atwuv__ptz = MetaType(tuple(dfnnh__kazex))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                ggxif__byx = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(dfnnh__kazex), gaas__lbk, None, atwuv__ptz
                    )
                return bodo.utils.conversion.fix_arr_dtype(data, ggxif__byx)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            qts__lpxf = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                qts__lpxf, ordered, None, None)
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
            eng__hamui = arr.codes[ind]
            return arr.dtype.categories[max(eng__hamui, 0)]
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
    for izgup__dziqw in range(len(arr1)):
        if arr1[izgup__dziqw] != arr2[izgup__dziqw]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    svofs__wklzl = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    nqgjb__vtncd = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    ztz__hmld = categorical_arrs_match(arr, val)
    vmuw__wmghc = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    bxdi__mko = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not svofs__wklzl:
            raise BodoError(vmuw__wmghc)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            eng__hamui = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = eng__hamui
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (svofs__wklzl or nqgjb__vtncd or ztz__hmld !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(vmuw__wmghc)
        if ztz__hmld == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bxdi__mko)
        if svofs__wklzl:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                fzl__rgu = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for mjmzm__zwxx in range(n):
                    arr.codes[ind[mjmzm__zwxx]] = fzl__rgu
            return impl_scalar
        if ztz__hmld == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for izgup__dziqw in range(n):
                    arr.codes[ind[izgup__dziqw]] = val.codes[izgup__dziqw]
            return impl_arr_ind_mask
        if ztz__hmld == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bxdi__mko)
                n = len(val.codes)
                for izgup__dziqw in range(n):
                    arr.codes[ind[izgup__dziqw]] = val.codes[izgup__dziqw]
            return impl_arr_ind_mask
        if nqgjb__vtncd:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for mjmzm__zwxx in range(n):
                    bdms__tkht = bodo.utils.conversion.unbox_if_timestamp(val
                        [mjmzm__zwxx])
                    if bdms__tkht not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    eng__hamui = categories.get_loc(bdms__tkht)
                    arr.codes[ind[mjmzm__zwxx]] = eng__hamui
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (svofs__wklzl or nqgjb__vtncd or ztz__hmld !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(vmuw__wmghc)
        if ztz__hmld == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bxdi__mko)
        if svofs__wklzl:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                fzl__rgu = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for mjmzm__zwxx in range(n):
                    if ind[mjmzm__zwxx]:
                        arr.codes[mjmzm__zwxx] = fzl__rgu
            return impl_scalar
        if ztz__hmld == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                hpn__tqx = 0
                for izgup__dziqw in range(n):
                    if ind[izgup__dziqw]:
                        arr.codes[izgup__dziqw] = val.codes[hpn__tqx]
                        hpn__tqx += 1
            return impl_bool_ind_mask
        if ztz__hmld == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bxdi__mko)
                n = len(ind)
                hpn__tqx = 0
                for izgup__dziqw in range(n):
                    if ind[izgup__dziqw]:
                        arr.codes[izgup__dziqw] = val.codes[hpn__tqx]
                        hpn__tqx += 1
            return impl_bool_ind_mask
        if nqgjb__vtncd:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                hpn__tqx = 0
                categories = arr.dtype.categories
                for mjmzm__zwxx in range(n):
                    if ind[mjmzm__zwxx]:
                        bdms__tkht = bodo.utils.conversion.unbox_if_timestamp(
                            val[hpn__tqx])
                        if bdms__tkht not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        eng__hamui = categories.get_loc(bdms__tkht)
                        arr.codes[mjmzm__zwxx] = eng__hamui
                        hpn__tqx += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (svofs__wklzl or nqgjb__vtncd or ztz__hmld !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(vmuw__wmghc)
        if ztz__hmld == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bxdi__mko)
        if svofs__wklzl:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                fzl__rgu = arr.dtype.categories.get_loc(val)
                rmo__uxayg = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for mjmzm__zwxx in range(rmo__uxayg.start, rmo__uxayg.stop,
                    rmo__uxayg.step):
                    arr.codes[mjmzm__zwxx] = fzl__rgu
            return impl_scalar
        if ztz__hmld == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if ztz__hmld == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bxdi__mko)
                arr.codes[ind] = val.codes
            return impl_arr
        if nqgjb__vtncd:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                rmo__uxayg = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                hpn__tqx = 0
                for mjmzm__zwxx in range(rmo__uxayg.start, rmo__uxayg.stop,
                    rmo__uxayg.step):
                    bdms__tkht = bodo.utils.conversion.unbox_if_timestamp(val
                        [hpn__tqx])
                    if bdms__tkht not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    eng__hamui = categories.get_loc(bdms__tkht)
                    arr.codes[mjmzm__zwxx] = eng__hamui
                    hpn__tqx += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
