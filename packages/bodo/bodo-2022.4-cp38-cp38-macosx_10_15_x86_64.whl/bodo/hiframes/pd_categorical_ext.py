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
        mcd__ubscr = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=mcd__ubscr)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    gjn__gsh = tuple(val.categories.values)
    elem_type = None if len(gjn__gsh) == 0 else bodo.typeof(val.categories.
        values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(gjn__gsh, elem_type, val.ordered, bodo.typeof
        (val.categories), int_type)


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
        fnhb__lybp = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, fnhb__lybp)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    tqt__dmjr = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    bpznp__daid = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, eeri__sia, eeri__sia = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    hvaei__yfix = PDCategoricalDtype(bpznp__daid, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, tqt__dmjr)
    return hvaei__yfix(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    flrnj__jqwi = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, flrnj__jqwi).value
    c.pyapi.decref(flrnj__jqwi)
    kspv__fbka = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, kspv__fbka).value
    c.pyapi.decref(kspv__fbka)
    nlx__ayarf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=nlx__ayarf)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    flrnj__jqwi = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    kog__uyfaf = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    rtri__bnzel = c.context.insert_const_string(c.builder.module, 'pandas')
    jux__bag = c.pyapi.import_module_noblock(rtri__bnzel)
    hsu__mui = c.pyapi.call_method(jux__bag, 'CategoricalDtype', (
        kog__uyfaf, flrnj__jqwi))
    c.pyapi.decref(flrnj__jqwi)
    c.pyapi.decref(kog__uyfaf)
    c.pyapi.decref(jux__bag)
    c.context.nrt.decref(c.builder, typ, val)
    return hsu__mui


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
        olpy__zjau = get_categories_int_type(fe_type.dtype)
        fnhb__lybp = [('dtype', fe_type.dtype), ('codes', types.Array(
            olpy__zjau, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, fnhb__lybp)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    wgkbm__yicv = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), wgkbm__yicv
        ).value
    c.pyapi.decref(wgkbm__yicv)
    hsu__mui = c.pyapi.object_getattr_string(val, 'dtype')
    holu__cwvo = c.pyapi.to_native_value(typ.dtype, hsu__mui).value
    c.pyapi.decref(hsu__mui)
    figrd__otwus = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    figrd__otwus.codes = codes
    figrd__otwus.dtype = holu__cwvo
    return NativeValue(figrd__otwus._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    fcit__hjfc = get_categories_int_type(typ.dtype)
    meeae__oup = context.get_constant_generic(builder, types.Array(
        fcit__hjfc, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, meeae__oup])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    asf__rxuqk = len(cat_dtype.categories)
    if asf__rxuqk < np.iinfo(np.int8).max:
        dtype = types.int8
    elif asf__rxuqk < np.iinfo(np.int16).max:
        dtype = types.int16
    elif asf__rxuqk < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    rtri__bnzel = c.context.insert_const_string(c.builder.module, 'pandas')
    jux__bag = c.pyapi.import_module_noblock(rtri__bnzel)
    olpy__zjau = get_categories_int_type(dtype)
    oczyi__tpy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    qce__pmyfy = types.Array(olpy__zjau, 1, 'C')
    c.context.nrt.incref(c.builder, qce__pmyfy, oczyi__tpy.codes)
    wgkbm__yicv = c.pyapi.from_native_value(qce__pmyfy, oczyi__tpy.codes, c
        .env_manager)
    c.context.nrt.incref(c.builder, dtype, oczyi__tpy.dtype)
    hsu__mui = c.pyapi.from_native_value(dtype, oczyi__tpy.dtype, c.env_manager
        )
    nmaeo__tigu = c.pyapi.borrow_none()
    jozrd__hszc = c.pyapi.object_getattr_string(jux__bag, 'Categorical')
    nmjtd__jyban = c.pyapi.call_method(jozrd__hszc, 'from_codes', (
        wgkbm__yicv, nmaeo__tigu, nmaeo__tigu, hsu__mui))
    c.pyapi.decref(jozrd__hszc)
    c.pyapi.decref(wgkbm__yicv)
    c.pyapi.decref(hsu__mui)
    c.pyapi.decref(jux__bag)
    c.context.nrt.decref(c.builder, typ, val)
    return nmjtd__jyban


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
            zjba__jaz = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                qtlme__rrve = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), zjba__jaz)
                return qtlme__rrve
            return impl_lit

        def impl(A, other):
            zjba__jaz = get_code_for_value(A.dtype, other)
            qtlme__rrve = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), zjba__jaz)
            return qtlme__rrve
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        unas__mftpj = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(unas__mftpj)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    oczyi__tpy = cat_dtype.categories
    n = len(oczyi__tpy)
    for bpb__wjs in range(n):
        if oczyi__tpy[bpb__wjs] == val:
            return bpb__wjs
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    lzja__ist = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype')
    if lzja__ist != A.dtype.elem_type and lzja__ist != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if lzja__ist == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            qtlme__rrve = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for bpb__wjs in numba.parfors.parfor.internal_prange(n):
                mesq__xylm = codes[bpb__wjs]
                if mesq__xylm == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(
                            qtlme__rrve, bpb__wjs)
                    else:
                        bodo.libs.array_kernels.setna(qtlme__rrve, bpb__wjs)
                    continue
                qtlme__rrve[bpb__wjs] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[mesq__xylm]))
            return qtlme__rrve
        return impl
    qce__pmyfy = dtype_to_array_type(lzja__ist)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        qtlme__rrve = bodo.utils.utils.alloc_type(n, qce__pmyfy, (-1,))
        for bpb__wjs in numba.parfors.parfor.internal_prange(n):
            mesq__xylm = codes[bpb__wjs]
            if mesq__xylm == -1:
                bodo.libs.array_kernels.setna(qtlme__rrve, bpb__wjs)
                continue
            qtlme__rrve[bpb__wjs] = bodo.utils.conversion.unbox_if_timestamp(
                categories[mesq__xylm])
        return qtlme__rrve
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        esz__hhxm, holu__cwvo = args
        oczyi__tpy = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        oczyi__tpy.codes = esz__hhxm
        oczyi__tpy.dtype = holu__cwvo
        context.nrt.incref(builder, signature.args[0], esz__hhxm)
        context.nrt.incref(builder, signature.args[1], holu__cwvo)
        return oczyi__tpy._getvalue()
    edpn__owu = CategoricalArrayType(cat_dtype)
    sig = edpn__owu(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    owd__vtfcy = args[0]
    if equiv_set.has_shape(owd__vtfcy):
        return ArrayAnalysis.AnalyzeResult(shape=owd__vtfcy, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    olpy__zjau = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, olpy__zjau)
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
            fpx__uvso = {}
            meeae__oup = np.empty(n + 1, np.int64)
            elyd__fggxz = {}
            cvavf__tpjun = []
            ewv__tkqna = {}
            for bpb__wjs in range(n):
                ewv__tkqna[categories[bpb__wjs]] = bpb__wjs
            for vwpq__bxo in to_replace:
                if vwpq__bxo != value:
                    if vwpq__bxo in ewv__tkqna:
                        if value in ewv__tkqna:
                            fpx__uvso[vwpq__bxo] = vwpq__bxo
                            wlcr__zky = ewv__tkqna[vwpq__bxo]
                            elyd__fggxz[wlcr__zky] = ewv__tkqna[value]
                            cvavf__tpjun.append(wlcr__zky)
                        else:
                            fpx__uvso[vwpq__bxo] = value
                            ewv__tkqna[value] = ewv__tkqna[vwpq__bxo]
            qbher__sbmfg = np.sort(np.array(cvavf__tpjun))
            wqk__olnwd = 0
            slp__chkwm = []
            for mturi__udds in range(-1, n):
                while wqk__olnwd < len(qbher__sbmfg
                    ) and mturi__udds > qbher__sbmfg[wqk__olnwd]:
                    wqk__olnwd += 1
                slp__chkwm.append(wqk__olnwd)
            for ejchm__ehgs in range(-1, n):
                yuuf__wugg = ejchm__ehgs
                if ejchm__ehgs in elyd__fggxz:
                    yuuf__wugg = elyd__fggxz[ejchm__ehgs]
                meeae__oup[ejchm__ehgs + 1] = yuuf__wugg - slp__chkwm[
                    yuuf__wugg + 1]
            return fpx__uvso, meeae__oup, len(qbher__sbmfg)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for bpb__wjs in range(len(new_codes_arr)):
        new_codes_arr[bpb__wjs] = codes_map_arr[old_codes_arr[bpb__wjs] + 1]


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
    lims__eujx = arr.dtype.ordered
    mht__ypdw = arr.dtype.elem_type
    mlp__lqai = get_overload_const(to_replace)
    fabm__lrks = get_overload_const(value)
    if (arr.dtype.categories is not None and mlp__lqai is not NOT_CONSTANT and
        fabm__lrks is not NOT_CONSTANT):
        mdaf__ufd, codes_map_arr, eeri__sia = python_build_replace_dicts(
            mlp__lqai, fabm__lrks, arr.dtype.categories)
        if len(mdaf__ufd) == 0:
            return lambda arr, to_replace, value: arr.copy()
        vux__hpqy = []
        for xsgd__rvvc in arr.dtype.categories:
            if xsgd__rvvc in mdaf__ufd:
                gfuii__urpq = mdaf__ufd[xsgd__rvvc]
                if gfuii__urpq != xsgd__rvvc:
                    vux__hpqy.append(gfuii__urpq)
            else:
                vux__hpqy.append(xsgd__rvvc)
        jlwrf__bxyw = pd.CategoricalDtype(vux__hpqy, lims__eujx
            ).categories.values
        hjvr__lot = MetaType(tuple(jlwrf__bxyw))

        def impl_dtype(arr, to_replace, value):
            tjhma__kgdp = init_cat_dtype(bodo.utils.conversion.
                index_from_array(jlwrf__bxyw), lims__eujx, None, hjvr__lot)
            oczyi__tpy = alloc_categorical_array(len(arr.codes), tjhma__kgdp)
            reassign_codes(oczyi__tpy.codes, arr.codes, codes_map_arr)
            return oczyi__tpy
        return impl_dtype
    mht__ypdw = arr.dtype.elem_type
    if mht__ypdw == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            fpx__uvso, codes_map_arr, tvkq__vbvy = build_replace_dicts(
                to_replace, value, categories.values)
            if len(fpx__uvso) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), lims__eujx,
                    None, None))
            n = len(categories)
            jlwrf__bxyw = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                tvkq__vbvy, -1)
            yax__jbck = 0
            for mturi__udds in range(n):
                fkld__avmqi = categories[mturi__udds]
                if fkld__avmqi in fpx__uvso:
                    iriq__hdhee = fpx__uvso[fkld__avmqi]
                    if iriq__hdhee != fkld__avmqi:
                        jlwrf__bxyw[yax__jbck] = iriq__hdhee
                        yax__jbck += 1
                else:
                    jlwrf__bxyw[yax__jbck] = fkld__avmqi
                    yax__jbck += 1
            oczyi__tpy = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                jlwrf__bxyw), lims__eujx, None, None))
            reassign_codes(oczyi__tpy.codes, arr.codes, codes_map_arr)
            return oczyi__tpy
        return impl_str
    zvg__pdc = dtype_to_array_type(mht__ypdw)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        fpx__uvso, codes_map_arr, tvkq__vbvy = build_replace_dicts(to_replace,
            value, categories.values)
        if len(fpx__uvso) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), lims__eujx, None, None))
        n = len(categories)
        jlwrf__bxyw = bodo.utils.utils.alloc_type(n - tvkq__vbvy, zvg__pdc,
            None)
        yax__jbck = 0
        for bpb__wjs in range(n):
            fkld__avmqi = categories[bpb__wjs]
            if fkld__avmqi in fpx__uvso:
                iriq__hdhee = fpx__uvso[fkld__avmqi]
                if iriq__hdhee != fkld__avmqi:
                    jlwrf__bxyw[yax__jbck] = iriq__hdhee
                    yax__jbck += 1
            else:
                jlwrf__bxyw[yax__jbck] = fkld__avmqi
                yax__jbck += 1
        oczyi__tpy = alloc_categorical_array(len(arr.codes), init_cat_dtype
            (bodo.utils.conversion.index_from_array(jlwrf__bxyw),
            lims__eujx, None, None))
        reassign_codes(oczyi__tpy.codes, arr.codes, codes_map_arr)
        return oczyi__tpy
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
    kdnj__pckr = dict()
    odl__xctjq = 0
    for bpb__wjs in range(len(vals)):
        val = vals[bpb__wjs]
        if val in kdnj__pckr:
            continue
        kdnj__pckr[val] = odl__xctjq
        odl__xctjq += 1
    return kdnj__pckr


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    kdnj__pckr = dict()
    for bpb__wjs in range(len(vals)):
        val = vals[bpb__wjs]
        kdnj__pckr[val] = bpb__wjs
    return kdnj__pckr


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    ulvl__rcct = dict(fastpath=fastpath)
    eif__lkjw = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', ulvl__rcct, eif__lkjw)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        akn__rkzej = get_overload_const(categories)
        if akn__rkzej is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                akmfq__tvg = False
            else:
                akmfq__tvg = get_overload_const_bool(ordered)
            brn__hgb = pd.CategoricalDtype(akn__rkzej, akmfq__tvg
                ).categories.values
            xpri__ema = MetaType(tuple(brn__hgb))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                tjhma__kgdp = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(brn__hgb), akmfq__tvg, None, xpri__ema)
                return bodo.utils.conversion.fix_arr_dtype(data, tjhma__kgdp)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            gjn__gsh = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                gjn__gsh, ordered, None, None)
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
            hwyrk__iolun = arr.codes[ind]
            return arr.dtype.categories[max(hwyrk__iolun, 0)]
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
    for bpb__wjs in range(len(arr1)):
        if arr1[bpb__wjs] != arr2[bpb__wjs]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    gap__odg = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    dqb__uwi = not isinstance(val, CategoricalArrayType) and is_iterable_type(
        val) and is_common_scalar_dtype([val.dtype, arr.dtype.elem_type]
        ) and not (isinstance(arr.dtype.elem_type, types.Integer) and
        isinstance(val.dtype, types.Float))
    dmfkx__hzf = categorical_arrs_match(arr, val)
    ymdp__oja = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    dbb__dqga = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not gap__odg:
            raise BodoError(ymdp__oja)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            hwyrk__iolun = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = hwyrk__iolun
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (gap__odg or dqb__uwi or dmfkx__hzf !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ymdp__oja)
        if dmfkx__hzf == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(dbb__dqga)
        if gap__odg:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                gfpq__cvst = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for mturi__udds in range(n):
                    arr.codes[ind[mturi__udds]] = gfpq__cvst
            return impl_scalar
        if dmfkx__hzf == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for bpb__wjs in range(n):
                    arr.codes[ind[bpb__wjs]] = val.codes[bpb__wjs]
            return impl_arr_ind_mask
        if dmfkx__hzf == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(dbb__dqga)
                n = len(val.codes)
                for bpb__wjs in range(n):
                    arr.codes[ind[bpb__wjs]] = val.codes[bpb__wjs]
            return impl_arr_ind_mask
        if dqb__uwi:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for mturi__udds in range(n):
                    hkx__viwh = bodo.utils.conversion.unbox_if_timestamp(val
                        [mturi__udds])
                    if hkx__viwh not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    hwyrk__iolun = categories.get_loc(hkx__viwh)
                    arr.codes[ind[mturi__udds]] = hwyrk__iolun
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (gap__odg or dqb__uwi or dmfkx__hzf !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ymdp__oja)
        if dmfkx__hzf == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(dbb__dqga)
        if gap__odg:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                gfpq__cvst = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for mturi__udds in range(n):
                    if ind[mturi__udds]:
                        arr.codes[mturi__udds] = gfpq__cvst
            return impl_scalar
        if dmfkx__hzf == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                wqjeq__zpikq = 0
                for bpb__wjs in range(n):
                    if ind[bpb__wjs]:
                        arr.codes[bpb__wjs] = val.codes[wqjeq__zpikq]
                        wqjeq__zpikq += 1
            return impl_bool_ind_mask
        if dmfkx__hzf == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(dbb__dqga)
                n = len(ind)
                wqjeq__zpikq = 0
                for bpb__wjs in range(n):
                    if ind[bpb__wjs]:
                        arr.codes[bpb__wjs] = val.codes[wqjeq__zpikq]
                        wqjeq__zpikq += 1
            return impl_bool_ind_mask
        if dqb__uwi:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                wqjeq__zpikq = 0
                categories = arr.dtype.categories
                for mturi__udds in range(n):
                    if ind[mturi__udds]:
                        hkx__viwh = bodo.utils.conversion.unbox_if_timestamp(
                            val[wqjeq__zpikq])
                        if hkx__viwh not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        hwyrk__iolun = categories.get_loc(hkx__viwh)
                        arr.codes[mturi__udds] = hwyrk__iolun
                        wqjeq__zpikq += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (gap__odg or dqb__uwi or dmfkx__hzf !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ymdp__oja)
        if dmfkx__hzf == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(dbb__dqga)
        if gap__odg:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                gfpq__cvst = arr.dtype.categories.get_loc(val)
                bip__nzi = numba.cpython.unicode._normalize_slice(ind, len(arr)
                    )
                for mturi__udds in range(bip__nzi.start, bip__nzi.stop,
                    bip__nzi.step):
                    arr.codes[mturi__udds] = gfpq__cvst
            return impl_scalar
        if dmfkx__hzf == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if dmfkx__hzf == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(dbb__dqga)
                arr.codes[ind] = val.codes
            return impl_arr
        if dqb__uwi:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                bip__nzi = numba.cpython.unicode._normalize_slice(ind, len(arr)
                    )
                wqjeq__zpikq = 0
                for mturi__udds in range(bip__nzi.start, bip__nzi.stop,
                    bip__nzi.step):
                    hkx__viwh = bodo.utils.conversion.unbox_if_timestamp(val
                        [wqjeq__zpikq])
                    if hkx__viwh not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    hwyrk__iolun = categories.get_loc(hkx__viwh)
                    arr.codes[mturi__udds] = hwyrk__iolun
                    wqjeq__zpikq += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
