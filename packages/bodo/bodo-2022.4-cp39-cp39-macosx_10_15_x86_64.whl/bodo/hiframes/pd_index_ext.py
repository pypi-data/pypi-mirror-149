import datetime
import operator
import warnings
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_constant
from numba.core.typing.templates import AttributeTemplate, signature
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
import bodo.hiframes
import bodo.utils.conversion
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_overload_const_func, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, get_val_type_maybe_str_literal, is_const_func_type, is_heterogeneous_tuple_type, is_iterable_type, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
from bodo.utils.utils import is_null_value
_dt_index_data_typ = types.Array(types.NPDatetime('ns'), 1, 'C')
_timedelta_index_data_typ = types.Array(types.NPTimedelta('ns'), 1, 'C')
iNaT = pd._libs.tslibs.iNaT
NaT = types.NPDatetime('ns')('NaT')
idx_cpy_arg_defaults = dict(deep=False, dtype=None, names=None)
idx_typ_to_format_str_map = dict()


@typeof_impl.register(pd.Index)
def typeof_pd_index(val, c):
    if val.inferred_type == 'string' or pd._libs.lib.infer_dtype(val, True
        ) == 'string':
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'bytes' or pd._libs.lib.infer_dtype(val, True
        ) == 'bytes':
        return BinaryIndexType(get_val_type_maybe_str_literal(val.name))
    if val.equals(pd.Index([])):
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'date':
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'integer' or pd._libs.lib.infer_dtype(val, True
        ) == 'integer':
        if isinstance(val.dtype, pd.core.arrays.integer._IntegerDtype):
            mzf__fqv = val.dtype.numpy_dtype
            dtype = numba.np.numpy_support.from_dtype(mzf__fqv)
        else:
            dtype = types.int64
        return NumericIndexType(dtype, get_val_type_maybe_str_literal(val.
            name), IntegerArrayType(dtype))
    if val.inferred_type == 'boolean' or pd._libs.lib.infer_dtype(val, True
        ) == 'boolean':
        return NumericIndexType(types.bool_, get_val_type_maybe_str_literal
            (val.name), boolean_array)
    raise NotImplementedError(f'unsupported pd.Index type {val}')


class DatetimeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.datetime64ns, 1, 'C'
            ) if data is None else data
        super(DatetimeIndexType, self).__init__(name=
            f'DatetimeIndex({name_typ}, {self.data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def tzval(self):
        return self.data.tz if isinstance(self.data, bodo.DatetimeArrayType
            ) else None

    def copy(self):
        return DatetimeIndexType(self.name_typ, self.data)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return self.data.dtype.type_name

    @property
    def numpy_type_name(self):
        return str(self.data.dtype)


types.datetime_index = DatetimeIndexType()


@typeof_impl.register(pd.DatetimeIndex)
def typeof_datetime_index(val, c):
    if isinstance(val.dtype, pd.DatetimeTZDtype):
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name),
            DatetimeArrayType(val.tz))
    return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(DatetimeIndexType)
class DatetimeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vcucv__hvqw = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(_dt_index_data_typ.dtype, types.int64))]
        super(DatetimeIndexModel, self).__init__(dmm, fe_type, vcucv__hvqw)


make_attribute_wrapper(DatetimeIndexType, 'data', '_data')
make_attribute_wrapper(DatetimeIndexType, 'name', '_name')
make_attribute_wrapper(DatetimeIndexType, 'dict', '_dict')


@overload_method(DatetimeIndexType, 'copy', no_unliteral=True)
def overload_datetime_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    ljixu__pamh = dict(deep=deep, dtype=dtype, names=names)
    bamx__ymo = idx_typ_to_format_str_map[DatetimeIndexType].format('copy()')
    check_unsupported_args('copy', ljixu__pamh, idx_cpy_arg_defaults,
        fn_str=bamx__ymo, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), A._name)
    return impl


@box(DatetimeIndexType)
def box_dt_index(typ, val, c):
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    ejr__gbzzp = c.pyapi.import_module_noblock(hjt__wuypf)
    inlk__jhil = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, inlk__jhil.data)
    mzsdj__jigp = c.pyapi.from_native_value(typ.data, inlk__jhil.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, inlk__jhil.name)
    ahx__uezg = c.pyapi.from_native_value(typ.name_typ, inlk__jhil.name, c.
        env_manager)
    args = c.pyapi.tuple_pack([mzsdj__jigp])
    mfdbe__mliak = c.pyapi.object_getattr_string(ejr__gbzzp, 'DatetimeIndex')
    kws = c.pyapi.dict_pack([('name', ahx__uezg)])
    dpl__hifwo = c.pyapi.call(mfdbe__mliak, args, kws)
    c.pyapi.decref(mzsdj__jigp)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(ejr__gbzzp)
    c.pyapi.decref(mfdbe__mliak)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return dpl__hifwo


@unbox(DatetimeIndexType)
def unbox_datetime_index(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        zzdgp__qelx = c.pyapi.object_getattr_string(val, 'array')
    else:
        zzdgp__qelx = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, zzdgp__qelx).value
    ahx__uezg = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ahx__uezg).value
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vhfil__iud.data = data
    vhfil__iud.name = name
    dtype = _dt_index_data_typ.dtype
    ewr__mtmun, fhop__dmlxf = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    vhfil__iud.dict = fhop__dmlxf
    c.pyapi.decref(zzdgp__qelx)
    c.pyapi.decref(ahx__uezg)
    return NativeValue(vhfil__iud._getvalue())


@intrinsic
def init_datetime_index(typingctx, data, name):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        wye__vrpbg, honl__jjln = args
        inlk__jhil = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        inlk__jhil.data = wye__vrpbg
        inlk__jhil.name = honl__jjln
        context.nrt.incref(builder, signature.args[0], wye__vrpbg)
        context.nrt.incref(builder, signature.args[1], honl__jjln)
        dtype = _dt_index_data_typ.dtype
        inlk__jhil.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return inlk__jhil._getvalue()
    krsg__nqpn = DatetimeIndexType(name, data)
    sig = signature(krsg__nqpn, data, name)
    return sig, codegen


def init_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) >= 1 and not kws
    mqaof__xymxi = args[0]
    if equiv_set.has_shape(mqaof__xymxi):
        return ArrayAnalysis.AnalyzeResult(shape=mqaof__xymxi, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_datetime_index
    ) = init_index_equiv


def gen_dti_field_impl(field):
    ixtwd__smxz = 'def impl(dti):\n'
    ixtwd__smxz += '    numba.parfors.parfor.init_prange()\n'
    ixtwd__smxz += '    A = bodo.hiframes.pd_index_ext.get_index_data(dti)\n'
    ixtwd__smxz += (
        '    name = bodo.hiframes.pd_index_ext.get_index_name(dti)\n')
    ixtwd__smxz += '    n = len(A)\n'
    ixtwd__smxz += '    S = np.empty(n, np.int64)\n'
    ixtwd__smxz += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    ixtwd__smxz += '        val = A[i]\n'
    ixtwd__smxz += '        ts = bodo.utils.conversion.box_if_dt64(val)\n'
    if field in ['weekday']:
        ixtwd__smxz += '        S[i] = ts.' + field + '()\n'
    else:
        ixtwd__smxz += '        S[i] = ts.' + field + '\n'
    ixtwd__smxz += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    qmzm__azcg = {}
    exec(ixtwd__smxz, {'numba': numba, 'np': np, 'bodo': bodo}, qmzm__azcg)
    impl = qmzm__azcg['impl']
    return impl


def _install_dti_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        if field in ['is_leap_year']:
            continue
        impl = gen_dti_field_impl(field)
        overload_attribute(DatetimeIndexType, field)(lambda dti: impl)


_install_dti_date_fields()


@overload_attribute(DatetimeIndexType, 'is_leap_year')
def overload_datetime_index_is_leap_year(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        nglwp__kmpbu = len(A)
        S = np.empty(nglwp__kmpbu, np.bool_)
        for i in numba.parfors.parfor.internal_prange(nglwp__kmpbu):
            val = A[i]
            czqk__hld = bodo.utils.conversion.box_if_dt64(val)
            S[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(czqk__hld.year)
        return S
    return impl


@overload_attribute(DatetimeIndexType, 'date')
def overload_datetime_index_date(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        nglwp__kmpbu = len(A)
        S = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            nglwp__kmpbu)
        for i in numba.parfors.parfor.internal_prange(nglwp__kmpbu):
            val = A[i]
            czqk__hld = bodo.utils.conversion.box_if_dt64(val)
            S[i] = datetime.date(czqk__hld.year, czqk__hld.month, czqk__hld.day
                )
        return S
    return impl


@numba.njit(no_cpython_wrapper=True)
def _dti_val_finalize(s, count):
    if not count:
        s = iNaT
    return bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(s)


@numba.njit(no_cpython_wrapper=True)
def _tdi_val_finalize(s, count):
    return pd.Timedelta('nan') if not count else pd.Timedelta(s)


@overload_method(DatetimeIndexType, 'min', no_unliteral=True)
def overload_datetime_index_min(dti, axis=None, skipna=True):
    rzhyy__ula = dict(axis=axis, skipna=skipna)
    lhn__ygle = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.min', rzhyy__ula, lhn__ygle,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.min()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        tuztz__fgq = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_max_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(tuztz__fgq)):
            if not bodo.libs.array_kernels.isna(tuztz__fgq, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(tuztz__fgq
                    [i])
                s = min(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'max', no_unliteral=True)
def overload_datetime_index_max(dti, axis=None, skipna=True):
    rzhyy__ula = dict(axis=axis, skipna=skipna)
    lhn__ygle = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.max', rzhyy__ula, lhn__ygle,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.max()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        tuztz__fgq = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(tuztz__fgq)):
            if not bodo.libs.array_kernels.isna(tuztz__fgq, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(tuztz__fgq
                    [i])
                s = max(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'tz_convert', no_unliteral=True)
def overload_pd_datetime_tz_convert(A, tz):

    def impl(A, tz):
        return init_datetime_index(A._data.tz_convert(tz), A._name)
    return impl


@infer_getattr
class DatetimeIndexAttribute(AttributeTemplate):
    key = DatetimeIndexType

    def resolve_values(self, ary):
        return _dt_index_data_typ


@overload(pd.DatetimeIndex, no_unliteral=True)
def pd_datetimeindex_overload(data=None, freq=None, tz=None, normalize=
    False, closed=None, ambiguous='raise', dayfirst=False, yearfirst=False,
    dtype=None, copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.DatetimeIndex() expected')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'pandas.DatetimeIndex()')
    rzhyy__ula = dict(freq=freq, tz=tz, normalize=normalize, closed=closed,
        ambiguous=ambiguous, dayfirst=dayfirst, yearfirst=yearfirst, dtype=
        dtype, copy=copy)
    lhn__ygle = dict(freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False)
    check_unsupported_args('pandas.DatetimeIndex', rzhyy__ula, lhn__ygle,
        package_name='pandas', module_name='Index')

    def f(data=None, freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False, name=None):
        blz__zvsm = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_dt64ns(blz__zvsm)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


def overload_sub_operator_datetime_index(lhs, rhs):
    if isinstance(lhs, DatetimeIndexType
        ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        tpn__japhm = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            tuztz__fgq = bodo.hiframes.pd_index_ext.get_index_data(lhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(lhs)
            nglwp__kmpbu = len(tuztz__fgq)
            S = np.empty(nglwp__kmpbu, tpn__japhm)
            umbmw__esaw = rhs.value
            for i in numba.parfors.parfor.internal_prange(nglwp__kmpbu):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    tuztz__fgq[i]) - umbmw__esaw)
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl
    if isinstance(rhs, DatetimeIndexType
        ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        tpn__japhm = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            tuztz__fgq = bodo.hiframes.pd_index_ext.get_index_data(rhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(rhs)
            nglwp__kmpbu = len(tuztz__fgq)
            S = np.empty(nglwp__kmpbu, tpn__japhm)
            umbmw__esaw = lhs.value
            for i in numba.parfors.parfor.internal_prange(nglwp__kmpbu):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    umbmw__esaw - bodo.hiframes.pd_timestamp_ext.
                    dt64_to_integer(tuztz__fgq[i]))
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl


def gen_dti_str_binop_impl(op, is_lhs_dti):
    eiv__koytm = numba.core.utils.OPERATORS_TO_BUILTINS[op]
    ixtwd__smxz = 'def impl(lhs, rhs):\n'
    if is_lhs_dti:
        ixtwd__smxz += '  dt_index, _str = lhs, rhs\n'
        syg__wugd = 'arr[i] {} other'.format(eiv__koytm)
    else:
        ixtwd__smxz += '  dt_index, _str = rhs, lhs\n'
        syg__wugd = 'other {} arr[i]'.format(eiv__koytm)
    ixtwd__smxz += (
        '  arr = bodo.hiframes.pd_index_ext.get_index_data(dt_index)\n')
    ixtwd__smxz += '  l = len(arr)\n'
    ixtwd__smxz += (
        '  other = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(_str)\n')
    ixtwd__smxz += '  S = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    ixtwd__smxz += '  for i in numba.parfors.parfor.internal_prange(l):\n'
    ixtwd__smxz += '    S[i] = {}\n'.format(syg__wugd)
    ixtwd__smxz += '  return S\n'
    qmzm__azcg = {}
    exec(ixtwd__smxz, {'bodo': bodo, 'numba': numba, 'np': np}, qmzm__azcg)
    impl = qmzm__azcg['impl']
    return impl


def overload_binop_dti_str(op):

    def overload_impl(lhs, rhs):
        if isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, True)
        if isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, False)
    return overload_impl


@overload(pd.Index, inline='always', no_unliteral=True)
def pd_index_overload(data=None, dtype=None, copy=False, name=None,
    tupleize_cols=True):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'pandas.Index()')
    data = types.unliteral(data) if not isinstance(data, types.LiteralList
        ) else data
    vhffq__gndp = getattr(data, 'dtype', None)
    if not is_overload_none(dtype):
        hbn__tuer = parse_dtype(dtype, 'pandas.Index')
    else:
        hbn__tuer = vhffq__gndp
    if isinstance(hbn__tuer, types.misc.PyObject):
        raise BodoError(
            "pd.Index() object 'dtype' is not specific enough for typing. Please provide a more exact type (e.g. str)."
            )
    if isinstance(data, RangeIndexType):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.RangeIndex(data, name=name)
    elif isinstance(data, DatetimeIndexType) or hbn__tuer == types.NPDatetime(
        'ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.DatetimeIndex(data, name=name)
    elif isinstance(data, TimedeltaIndexType
        ) or hbn__tuer == types.NPTimedelta('ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.TimedeltaIndex(data, name=name)
    elif is_heterogeneous_tuple_type(data):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return bodo.hiframes.pd_index_ext.init_heter_index(data, name)
        return impl
    elif bodo.utils.utils.is_array_typ(data, False) or isinstance(data, (
        SeriesType, types.List, types.UniTuple)):
        if isinstance(hbn__tuer, (types.Integer, types.Float, types.Boolean)):

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                blz__zvsm = bodo.utils.conversion.coerce_to_array(data)
                usmc__thurj = bodo.utils.conversion.fix_arr_dtype(blz__zvsm,
                    hbn__tuer)
                return bodo.hiframes.pd_index_ext.init_numeric_index(
                    usmc__thurj, name)
        elif hbn__tuer in [types.string, bytes_type]:

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                return bodo.hiframes.pd_index_ext.init_binary_str_index(bodo
                    .utils.conversion.coerce_to_array(data), name)
        else:
            raise BodoError(
                'pd.Index(): provided array is of unsupported type.')
    elif is_overload_none(data):
        raise BodoError(
            'data argument in pd.Index() is invalid: None or scalar is not acceptable'
            )
    else:
        raise BodoError(
            f'pd.Index(): the provided argument type {data} is not supported')
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_datetime_index_getitem(dti, ind):
    if isinstance(dti, DatetimeIndexType):
        if isinstance(ind, types.Integer):

            def impl(dti, ind):
                tdsk__qxtm = bodo.hiframes.pd_index_ext.get_index_data(dti)
                val = tdsk__qxtm[ind]
                return bodo.utils.conversion.box_if_dt64(val)
            return impl
        else:

            def impl(dti, ind):
                tdsk__qxtm = bodo.hiframes.pd_index_ext.get_index_data(dti)
                name = bodo.hiframes.pd_index_ext.get_index_name(dti)
                gek__gky = tdsk__qxtm[ind]
                return bodo.hiframes.pd_index_ext.init_datetime_index(gek__gky,
                    name)
            return impl


@overload(operator.getitem, no_unliteral=True)
def overload_timedelta_index_getitem(I, ind):
    if not isinstance(I, TimedeltaIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            mli__ipf = bodo.hiframes.pd_index_ext.get_index_data(I)
            return pd.Timedelta(mli__ipf[ind])
        return impl

    def impl(I, ind):
        mli__ipf = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        gek__gky = mli__ipf[ind]
        return bodo.hiframes.pd_index_ext.init_timedelta_index(gek__gky, name)
    return impl


@numba.njit(no_cpython_wrapper=True)
def validate_endpoints(closed):
    kyfpz__bub = False
    ale__mmpev = False
    if closed is None:
        kyfpz__bub = True
        ale__mmpev = True
    elif closed == 'left':
        kyfpz__bub = True
    elif closed == 'right':
        ale__mmpev = True
    else:
        raise ValueError("Closed has to be either 'left', 'right' or None")
    return kyfpz__bub, ale__mmpev


@numba.njit(no_cpython_wrapper=True)
def to_offset_value(freq):
    if freq is None:
        return None
    with numba.objmode(r='int64'):
        r = pd.tseries.frequencies.to_offset(freq).nanos
    return r


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _dummy_convert_none_to_int(val):
    if is_overload_none(val):

        def impl(val):
            return 0
        return impl
    if isinstance(val, types.Optional):

        def impl(val):
            if val is None:
                return 0
            return bodo.utils.indexing.unoptional(val)
        return impl
    return lambda val: val


@overload(pd.date_range, inline='always')
def pd_date_range_overload(start=None, end=None, periods=None, freq=None,
    tz=None, normalize=False, name=None, closed=None):
    rzhyy__ula = dict(tz=tz, normalize=normalize, closed=closed)
    lhn__ygle = dict(tz=None, normalize=False, closed=None)
    check_unsupported_args('pandas.date_range', rzhyy__ula, lhn__ygle,
        package_name='pandas', module_name='General')
    if not is_overload_none(tz):
        raise_bodo_error('pd.date_range(): tz argument not supported yet')
    pskjt__mth = ''
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
        pskjt__mth = "  freq = 'D'\n"
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise_bodo_error(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )
    ixtwd__smxz = """def f(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None):
"""
    ixtwd__smxz += pskjt__mth
    if is_overload_none(start):
        ixtwd__smxz += "  start_t = pd.Timestamp('1800-01-03')\n"
    else:
        ixtwd__smxz += '  start_t = pd.Timestamp(start)\n'
    if is_overload_none(end):
        ixtwd__smxz += "  end_t = pd.Timestamp('1800-01-03')\n"
    else:
        ixtwd__smxz += '  end_t = pd.Timestamp(end)\n'
    if not is_overload_none(freq):
        ixtwd__smxz += (
            '  stride = bodo.hiframes.pd_index_ext.to_offset_value(freq)\n')
        if is_overload_none(periods):
            ixtwd__smxz += '  b = start_t.value\n'
            ixtwd__smxz += (
                '  e = b + (end_t.value - b) // stride * stride + stride // 2 + 1\n'
                )
        elif not is_overload_none(start):
            ixtwd__smxz += '  b = start_t.value\n'
            ixtwd__smxz += '  addend = np.int64(periods) * np.int64(stride)\n'
            ixtwd__smxz += '  e = np.int64(b) + addend\n'
        elif not is_overload_none(end):
            ixtwd__smxz += '  e = end_t.value + stride\n'
            ixtwd__smxz += '  addend = np.int64(periods) * np.int64(-stride)\n'
            ixtwd__smxz += '  b = np.int64(e) + addend\n'
        else:
            raise_bodo_error(
                "at least 'start' or 'end' should be specified if a 'period' is given."
                )
        ixtwd__smxz += '  arr = np.arange(b, e, stride, np.int64)\n'
    else:
        ixtwd__smxz += '  delta = end_t.value - start_t.value\n'
        ixtwd__smxz += '  step = delta / (periods - 1)\n'
        ixtwd__smxz += '  arr1 = np.arange(0, periods, 1, np.float64)\n'
        ixtwd__smxz += '  arr1 *= step\n'
        ixtwd__smxz += '  arr1 += start_t.value\n'
        ixtwd__smxz += '  arr = arr1.astype(np.int64)\n'
        ixtwd__smxz += '  arr[-1] = end_t.value\n'
    ixtwd__smxz += '  A = bodo.utils.conversion.convert_to_dt64ns(arr)\n'
    ixtwd__smxz += (
        '  return bodo.hiframes.pd_index_ext.init_datetime_index(A, name)\n')
    qmzm__azcg = {}
    exec(ixtwd__smxz, {'bodo': bodo, 'np': np, 'pd': pd}, qmzm__azcg)
    f = qmzm__azcg['f']
    return f


@overload(pd.timedelta_range, no_unliteral=True)
def pd_timedelta_range_overload(start=None, end=None, periods=None, freq=
    None, name=None, closed=None):
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise BodoError(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )

    def f(start=None, end=None, periods=None, freq=None, name=None, closed=None
        ):
        if freq is None and (start is None or end is None or periods is None):
            freq = 'D'
        freq = bodo.hiframes.pd_index_ext.to_offset_value(freq)
        qtcy__asnpv = pd.Timedelta('1 day')
        if start is not None:
            qtcy__asnpv = pd.Timedelta(start)
        aez__xcmpa = pd.Timedelta('1 day')
        if end is not None:
            aez__xcmpa = pd.Timedelta(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of start and end are defined'
                )
        kyfpz__bub, ale__mmpev = bodo.hiframes.pd_index_ext.validate_endpoints(
            closed)
        if freq is not None:
            eusv__ypoa = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = qtcy__asnpv.value
                vdnmg__asqx = b + (aez__xcmpa.value - b
                    ) // eusv__ypoa * eusv__ypoa + eusv__ypoa // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = qtcy__asnpv.value
                cejf__rcip = np.int64(periods) * np.int64(eusv__ypoa)
                vdnmg__asqx = np.int64(b) + cejf__rcip
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                vdnmg__asqx = aez__xcmpa.value + eusv__ypoa
                cejf__rcip = np.int64(periods) * np.int64(-eusv__ypoa)
                b = np.int64(vdnmg__asqx) + cejf__rcip
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            jpi__cyptd = np.arange(b, vdnmg__asqx, eusv__ypoa, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            yfhw__wfa = aez__xcmpa.value - qtcy__asnpv.value
            step = yfhw__wfa / (periods - 1)
            meo__jao = np.arange(0, periods, 1, np.float64)
            meo__jao *= step
            meo__jao += qtcy__asnpv.value
            jpi__cyptd = meo__jao.astype(np.int64)
            jpi__cyptd[-1] = aez__xcmpa.value
        if not kyfpz__bub and len(jpi__cyptd) and jpi__cyptd[0
            ] == qtcy__asnpv.value:
            jpi__cyptd = jpi__cyptd[1:]
        if not ale__mmpev and len(jpi__cyptd) and jpi__cyptd[-1
            ] == aez__xcmpa.value:
            jpi__cyptd = jpi__cyptd[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(jpi__cyptd)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return f


@overload_method(DatetimeIndexType, 'isocalendar', inline='always',
    no_unliteral=True)
def overload_pd_timestamp_isocalendar(idx):

    def impl(idx):
        A = bodo.hiframes.pd_index_ext.get_index_data(idx)
        numba.parfors.parfor.init_prange()
        nglwp__kmpbu = len(A)
        qcedp__clvi = bodo.libs.int_arr_ext.alloc_int_array(nglwp__kmpbu,
            np.uint32)
        vkw__uweu = bodo.libs.int_arr_ext.alloc_int_array(nglwp__kmpbu, np.
            uint32)
        evx__mes = bodo.libs.int_arr_ext.alloc_int_array(nglwp__kmpbu, np.
            uint32)
        for i in numba.parfors.parfor.internal_prange(nglwp__kmpbu):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(qcedp__clvi, i)
                bodo.libs.array_kernels.setna(vkw__uweu, i)
                bodo.libs.array_kernels.setna(evx__mes, i)
                continue
            qcedp__clvi[i], vkw__uweu[i], evx__mes[i
                ] = bodo.utils.conversion.box_if_dt64(A[i]).isocalendar()
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((qcedp__clvi,
            vkw__uweu, evx__mes), idx, ('year', 'week', 'day'))
    return impl


class TimedeltaIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.timedelta64ns, 1, 'C'
            ) if data is None else data
        super(TimedeltaIndexType, self).__init__(name=
            f'TimedeltaIndexType({name_typ}, {self.data})')
    ndim = 1

    def copy(self):
        return TimedeltaIndexType(self.name_typ)

    @property
    def dtype(self):
        return types.NPTimedelta('ns')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.name_typ, self.data

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return 'timedelta'

    @property
    def numpy_type_name(self):
        return 'timedelta64[ns]'


timedelta_index = TimedeltaIndexType()
types.timedelta_index = timedelta_index


@register_model(TimedeltaIndexType)
class TimedeltaIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vcucv__hvqw = [('data', _timedelta_index_data_typ), ('name',
            fe_type.name_typ), ('dict', types.DictType(
            _timedelta_index_data_typ.dtype, types.int64))]
        super(TimedeltaIndexTypeModel, self).__init__(dmm, fe_type, vcucv__hvqw
            )


@typeof_impl.register(pd.TimedeltaIndex)
def typeof_timedelta_index(val, c):
    return TimedeltaIndexType(get_val_type_maybe_str_literal(val.name))


@box(TimedeltaIndexType)
def box_timedelta_index(typ, val, c):
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    ejr__gbzzp = c.pyapi.import_module_noblock(hjt__wuypf)
    timedelta_index = numba.core.cgutils.create_struct_proxy(typ)(c.context,
        c.builder, val)
    c.context.nrt.incref(c.builder, _timedelta_index_data_typ,
        timedelta_index.data)
    mzsdj__jigp = c.pyapi.from_native_value(_timedelta_index_data_typ,
        timedelta_index.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, timedelta_index.name)
    ahx__uezg = c.pyapi.from_native_value(typ.name_typ, timedelta_index.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([mzsdj__jigp])
    kws = c.pyapi.dict_pack([('name', ahx__uezg)])
    mfdbe__mliak = c.pyapi.object_getattr_string(ejr__gbzzp, 'TimedeltaIndex')
    dpl__hifwo = c.pyapi.call(mfdbe__mliak, args, kws)
    c.pyapi.decref(mzsdj__jigp)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(ejr__gbzzp)
    c.pyapi.decref(mfdbe__mliak)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return dpl__hifwo


@unbox(TimedeltaIndexType)
def unbox_timedelta_index(typ, val, c):
    jhka__vcfc = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_timedelta_index_data_typ, jhka__vcfc).value
    ahx__uezg = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ahx__uezg).value
    c.pyapi.decref(jhka__vcfc)
    c.pyapi.decref(ahx__uezg)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vhfil__iud.data = data
    vhfil__iud.name = name
    dtype = _timedelta_index_data_typ.dtype
    ewr__mtmun, fhop__dmlxf = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    vhfil__iud.dict = fhop__dmlxf
    return NativeValue(vhfil__iud._getvalue())


@intrinsic
def init_timedelta_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        wye__vrpbg, honl__jjln = args
        timedelta_index = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        timedelta_index.data = wye__vrpbg
        timedelta_index.name = honl__jjln
        context.nrt.incref(builder, signature.args[0], wye__vrpbg)
        context.nrt.incref(builder, signature.args[1], honl__jjln)
        dtype = _timedelta_index_data_typ.dtype
        timedelta_index.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return timedelta_index._getvalue()
    krsg__nqpn = TimedeltaIndexType(name)
    sig = signature(krsg__nqpn, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_timedelta_index
    ) = init_index_equiv


@infer_getattr
class TimedeltaIndexAttribute(AttributeTemplate):
    key = TimedeltaIndexType

    def resolve_values(self, ary):
        return _timedelta_index_data_typ


make_attribute_wrapper(TimedeltaIndexType, 'data', '_data')
make_attribute_wrapper(TimedeltaIndexType, 'name', '_name')
make_attribute_wrapper(TimedeltaIndexType, 'dict', '_dict')


@overload_method(TimedeltaIndexType, 'copy', no_unliteral=True)
def overload_timedelta_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    ljixu__pamh = dict(deep=deep, dtype=dtype, names=names)
    bamx__ymo = idx_typ_to_format_str_map[TimedeltaIndexType].format('copy()')
    check_unsupported_args('TimedeltaIndex.copy', ljixu__pamh,
        idx_cpy_arg_defaults, fn_str=bamx__ymo, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), A._name)
    return impl


@overload_method(TimedeltaIndexType, 'min', inline='always', no_unliteral=True)
def overload_timedelta_index_min(tdi, axis=None, skipna=True):
    rzhyy__ula = dict(axis=axis, skipna=skipna)
    lhn__ygle = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.min', rzhyy__ula, lhn__ygle,
        package_name='pandas', module_name='Index')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        nglwp__kmpbu = len(data)
        ixe__qztpv = numba.cpython.builtins.get_type_max_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(nglwp__kmpbu):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            ixe__qztpv = min(ixe__qztpv, val)
        bcf__mjyip = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            ixe__qztpv)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(bcf__mjyip, count)
    return impl


@overload_method(TimedeltaIndexType, 'max', inline='always', no_unliteral=True)
def overload_timedelta_index_max(tdi, axis=None, skipna=True):
    rzhyy__ula = dict(axis=axis, skipna=skipna)
    lhn__ygle = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.max', rzhyy__ula, lhn__ygle,
        package_name='pandas', module_name='Index')
    if not is_overload_none(axis) or not is_overload_true(skipna):
        raise BodoError(
            'Index.min(): axis and skipna arguments not supported yet')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        nglwp__kmpbu = len(data)
        esiq__xevpw = numba.cpython.builtins.get_type_min_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(nglwp__kmpbu):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            esiq__xevpw = max(esiq__xevpw, val)
        bcf__mjyip = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            esiq__xevpw)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(bcf__mjyip, count)
    return impl


def gen_tdi_field_impl(field):
    ixtwd__smxz = 'def impl(tdi):\n'
    ixtwd__smxz += '    numba.parfors.parfor.init_prange()\n'
    ixtwd__smxz += '    A = bodo.hiframes.pd_index_ext.get_index_data(tdi)\n'
    ixtwd__smxz += (
        '    name = bodo.hiframes.pd_index_ext.get_index_name(tdi)\n')
    ixtwd__smxz += '    n = len(A)\n'
    ixtwd__smxz += '    S = np.empty(n, np.int64)\n'
    ixtwd__smxz += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    ixtwd__smxz += (
        '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
        )
    if field == 'nanoseconds':
        ixtwd__smxz += '        S[i] = td64 % 1000\n'
    elif field == 'microseconds':
        ixtwd__smxz += '        S[i] = td64 // 1000 % 100000\n'
    elif field == 'seconds':
        ixtwd__smxz += (
            '        S[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
    elif field == 'days':
        ixtwd__smxz += (
            '        S[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
    else:
        assert False, 'invalid timedelta field'
    ixtwd__smxz += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    qmzm__azcg = {}
    exec(ixtwd__smxz, {'numba': numba, 'np': np, 'bodo': bodo}, qmzm__azcg)
    impl = qmzm__azcg['impl']
    return impl


def _install_tdi_time_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        impl = gen_tdi_field_impl(field)
        overload_attribute(TimedeltaIndexType, field)(lambda tdi: impl)


_install_tdi_time_fields()


@overload(pd.TimedeltaIndex, no_unliteral=True)
def pd_timedelta_index_overload(data=None, unit=None, freq=None, dtype=None,
    copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.TimedeltaIndex() expected')
    rzhyy__ula = dict(unit=unit, freq=freq, dtype=dtype, copy=copy)
    lhn__ygle = dict(unit=None, freq=None, dtype=None, copy=False)
    check_unsupported_args('pandas.TimedeltaIndex', rzhyy__ula, lhn__ygle,
        package_name='pandas', module_name='Index')

    def impl(data=None, unit=None, freq=None, dtype=None, copy=False, name=None
        ):
        blz__zvsm = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_td64ns(blz__zvsm)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return impl


class RangeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        if name_typ is None:
            name_typ = types.none
        self.name_typ = name_typ
        super(RangeIndexType, self).__init__(name='RangeIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return RangeIndexType(self.name_typ)

    @property
    def iterator_type(self):
        return types.iterators.RangeIteratorType(types.int64)

    @property
    def dtype(self):
        return types.int64

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)

    def unify(self, typingctx, other):
        if isinstance(other, NumericIndexType):
            name_typ = self.name_typ.unify(typingctx, other.name_typ)
            if name_typ is None:
                name_typ = types.none
            return NumericIndexType(types.int64, name_typ)


@typeof_impl.register(pd.RangeIndex)
def typeof_pd_range_index(val, c):
    return RangeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(RangeIndexType)
class RangeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vcucv__hvqw = [('start', types.int64), ('stop', types.int64), (
            'step', types.int64), ('name', fe_type.name_typ)]
        super(RangeIndexModel, self).__init__(dmm, fe_type, vcucv__hvqw)


make_attribute_wrapper(RangeIndexType, 'start', '_start')
make_attribute_wrapper(RangeIndexType, 'stop', '_stop')
make_attribute_wrapper(RangeIndexType, 'step', '_step')
make_attribute_wrapper(RangeIndexType, 'name', '_name')


@overload_method(RangeIndexType, 'copy', no_unliteral=True)
def overload_range_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    ljixu__pamh = dict(deep=deep, dtype=dtype, names=names)
    bamx__ymo = idx_typ_to_format_str_map[RangeIndexType].format('copy()')
    check_unsupported_args('RangeIndex.copy', ljixu__pamh,
        idx_cpy_arg_defaults, fn_str=bamx__ymo, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, A._name)
    return impl


@box(RangeIndexType)
def box_range_index(typ, val, c):
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    tgl__wgaq = c.pyapi.import_module_noblock(hjt__wuypf)
    jpzn__xhiu = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    oox__naa = c.pyapi.from_native_value(types.int64, jpzn__xhiu.start, c.
        env_manager)
    mdkk__dghp = c.pyapi.from_native_value(types.int64, jpzn__xhiu.stop, c.
        env_manager)
    exxdj__jahq = c.pyapi.from_native_value(types.int64, jpzn__xhiu.step, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, jpzn__xhiu.name)
    ahx__uezg = c.pyapi.from_native_value(typ.name_typ, jpzn__xhiu.name, c.
        env_manager)
    args = c.pyapi.tuple_pack([oox__naa, mdkk__dghp, exxdj__jahq])
    kws = c.pyapi.dict_pack([('name', ahx__uezg)])
    mfdbe__mliak = c.pyapi.object_getattr_string(tgl__wgaq, 'RangeIndex')
    myhw__dlr = c.pyapi.call(mfdbe__mliak, args, kws)
    c.pyapi.decref(oox__naa)
    c.pyapi.decref(mdkk__dghp)
    c.pyapi.decref(exxdj__jahq)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(tgl__wgaq)
    c.pyapi.decref(mfdbe__mliak)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return myhw__dlr


@intrinsic
def init_range_index(typingctx, start, stop, step, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 4
        jpzn__xhiu = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        jpzn__xhiu.start = args[0]
        jpzn__xhiu.stop = args[1]
        jpzn__xhiu.step = args[2]
        jpzn__xhiu.name = args[3]
        context.nrt.incref(builder, signature.return_type.name_typ, args[3])
        return jpzn__xhiu._getvalue()
    return RangeIndexType(name)(start, stop, step, name), codegen


def init_range_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    start, stop, step, pqh__pbh = args
    if self.typemap[start.name] == types.IntegerLiteral(0) and self.typemap[
        step.name] == types.IntegerLiteral(1) and equiv_set.has_shape(stop):
        return ArrayAnalysis.AnalyzeResult(shape=stop, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_range_index
    ) = init_range_index_equiv


@unbox(RangeIndexType)
def unbox_range_index(typ, val, c):
    oox__naa = c.pyapi.object_getattr_string(val, 'start')
    start = c.pyapi.to_native_value(types.int64, oox__naa).value
    mdkk__dghp = c.pyapi.object_getattr_string(val, 'stop')
    stop = c.pyapi.to_native_value(types.int64, mdkk__dghp).value
    exxdj__jahq = c.pyapi.object_getattr_string(val, 'step')
    step = c.pyapi.to_native_value(types.int64, exxdj__jahq).value
    ahx__uezg = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ahx__uezg).value
    c.pyapi.decref(oox__naa)
    c.pyapi.decref(mdkk__dghp)
    c.pyapi.decref(exxdj__jahq)
    c.pyapi.decref(ahx__uezg)
    jpzn__xhiu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jpzn__xhiu.start = start
    jpzn__xhiu.stop = stop
    jpzn__xhiu.step = step
    jpzn__xhiu.name = name
    return NativeValue(jpzn__xhiu._getvalue())


@lower_constant(RangeIndexType)
def lower_constant_range_index(context, builder, ty, pyval):
    start = context.get_constant(types.int64, pyval.start)
    stop = context.get_constant(types.int64, pyval.stop)
    step = context.get_constant(types.int64, pyval.step)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    return lir.Constant.literal_struct([start, stop, step, name])


@overload(pd.RangeIndex, no_unliteral=True, inline='always')
def range_index_overload(start=None, stop=None, step=None, dtype=None, copy
    =False, name=None):

    def _ensure_int_or_none(value, field):
        kywjx__npzbx = (
            'RangeIndex(...) must be called with integers, {value} was passed for {field}'
            )
        if not is_overload_none(value) and not isinstance(value, types.
            IntegerLiteral) and not isinstance(value, types.Integer):
            raise BodoError(kywjx__npzbx.format(value=value, field=field))
    _ensure_int_or_none(start, 'start')
    _ensure_int_or_none(stop, 'stop')
    _ensure_int_or_none(step, 'step')
    if is_overload_none(start) and is_overload_none(stop) and is_overload_none(
        step):
        kywjx__npzbx = 'RangeIndex(...) must be called with integers'
        raise BodoError(kywjx__npzbx)
    fjk__dmsh = 'start'
    lkjta__vucmv = 'stop'
    jcey__ytm = 'step'
    if is_overload_none(start):
        fjk__dmsh = '0'
    if is_overload_none(stop):
        lkjta__vucmv = 'start'
        fjk__dmsh = '0'
    if is_overload_none(step):
        jcey__ytm = '1'
    ixtwd__smxz = """def _pd_range_index_imp(start=None, stop=None, step=None, dtype=None, copy=False, name=None):
"""
    ixtwd__smxz += '  return init_range_index({}, {}, {}, name)\n'.format(
        fjk__dmsh, lkjta__vucmv, jcey__ytm)
    qmzm__azcg = {}
    exec(ixtwd__smxz, {'init_range_index': init_range_index}, qmzm__azcg)
    njcvw__vll = qmzm__azcg['_pd_range_index_imp']
    return njcvw__vll


@overload(pd.CategoricalIndex, no_unliteral=True, inline='always')
def categorical_index_overload(data=None, categories=None, ordered=None,
    dtype=None, copy=False, name=None):
    raise BodoError('pd.CategoricalIndex() initializer not yet supported.')


@overload_attribute(RangeIndexType, 'start')
def rangeIndex_get_start(ri):

    def impl(ri):
        return ri._start
    return impl


@overload_attribute(RangeIndexType, 'stop')
def rangeIndex_get_stop(ri):

    def impl(ri):
        return ri._stop
    return impl


@overload_attribute(RangeIndexType, 'step')
def rangeIndex_get_step(ri):

    def impl(ri):
        return ri._step
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_range_index_getitem(I, idx):
    if isinstance(I, RangeIndexType):
        if isinstance(types.unliteral(idx), types.Integer):
            return lambda I, idx: idx * I._step + I._start
        if isinstance(idx, types.SliceType):

            def impl(I, idx):
                vmk__cohcv = numba.cpython.unicode._normalize_slice(idx, len(I)
                    )
                name = bodo.hiframes.pd_index_ext.get_index_name(I)
                start = I._start + I._step * vmk__cohcv.start
                stop = I._start + I._step * vmk__cohcv.stop
                step = I._step * vmk__cohcv.step
                return bodo.hiframes.pd_index_ext.init_range_index(start,
                    stop, step, name)
            return impl
        return lambda I, idx: bodo.hiframes.pd_index_ext.init_numeric_index(np
            .arange(I._start, I._stop, I._step, np.int64)[idx], bodo.
            hiframes.pd_index_ext.get_index_name(I))


@overload(len, no_unliteral=True)
def overload_range_len(r):
    if isinstance(r, RangeIndexType):
        return lambda r: max(0, -(-(r._stop - r._start) // r._step))


class PeriodIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, freq, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.freq = freq
        self.name_typ = name_typ
        super(PeriodIndexType, self).__init__(name=
            'PeriodIndexType({}, {})'.format(freq, name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return PeriodIndexType(self.freq, self.name_typ)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'period[{self.freq}]'


@typeof_impl.register(pd.PeriodIndex)
def typeof_pd_period_index(val, c):
    return PeriodIndexType(val.freqstr, get_val_type_maybe_str_literal(val.
        name))


@register_model(PeriodIndexType)
class PeriodIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vcucv__hvqw = [('data', bodo.IntegerArrayType(types.int64)), (
            'name', fe_type.name_typ), ('dict', types.DictType(types.int64,
            types.int64))]
        super(PeriodIndexModel, self).__init__(dmm, fe_type, vcucv__hvqw)


make_attribute_wrapper(PeriodIndexType, 'data', '_data')
make_attribute_wrapper(PeriodIndexType, 'name', '_name')
make_attribute_wrapper(PeriodIndexType, 'dict', '_dict')


@overload_method(PeriodIndexType, 'copy', no_unliteral=True)
def overload_period_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    freq = A.freq
    ljixu__pamh = dict(deep=deep, dtype=dtype, names=names)
    bamx__ymo = idx_typ_to_format_str_map[PeriodIndexType].format('copy()')
    check_unsupported_args('PeriodIndex.copy', ljixu__pamh,
        idx_cpy_arg_defaults, fn_str=bamx__ymo, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), name, freq)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), A._name, freq)
    return impl


@intrinsic
def init_period_index(typingctx, data, name, freq):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        wye__vrpbg, honl__jjln, pqh__pbh = args
        xmp__zwsh = signature.return_type
        tkcn__dazr = cgutils.create_struct_proxy(xmp__zwsh)(context, builder)
        tkcn__dazr.data = wye__vrpbg
        tkcn__dazr.name = honl__jjln
        context.nrt.incref(builder, signature.args[0], args[0])
        context.nrt.incref(builder, signature.args[1], args[1])
        tkcn__dazr.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(types.int64, types.int64), types.DictType(
            types.int64, types.int64)(), [])
        return tkcn__dazr._getvalue()
    ejboi__ivh = get_overload_const_str(freq)
    krsg__nqpn = PeriodIndexType(ejboi__ivh, name)
    sig = signature(krsg__nqpn, data, name, freq)
    return sig, codegen


@box(PeriodIndexType)
def box_period_index(typ, val, c):
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    tgl__wgaq = c.pyapi.import_module_noblock(hjt__wuypf)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, bodo.IntegerArrayType(types.int64),
        vhfil__iud.data)
    zzdgp__qelx = c.pyapi.from_native_value(bodo.IntegerArrayType(types.
        int64), vhfil__iud.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, vhfil__iud.name)
    ahx__uezg = c.pyapi.from_native_value(typ.name_typ, vhfil__iud.name, c.
        env_manager)
    gxj__vcigf = c.pyapi.string_from_constant_string(typ.freq)
    args = c.pyapi.tuple_pack([])
    kws = c.pyapi.dict_pack([('ordinal', zzdgp__qelx), ('name', ahx__uezg),
        ('freq', gxj__vcigf)])
    mfdbe__mliak = c.pyapi.object_getattr_string(tgl__wgaq, 'PeriodIndex')
    myhw__dlr = c.pyapi.call(mfdbe__mliak, args, kws)
    c.pyapi.decref(zzdgp__qelx)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(gxj__vcigf)
    c.pyapi.decref(tgl__wgaq)
    c.pyapi.decref(mfdbe__mliak)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return myhw__dlr


@unbox(PeriodIndexType)
def unbox_period_index(typ, val, c):
    arr_typ = bodo.IntegerArrayType(types.int64)
    zjbf__wkwfq = c.pyapi.object_getattr_string(val, 'asi8')
    ziee__fyih = c.pyapi.call_method(val, 'isna', ())
    ahx__uezg = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ahx__uezg).value
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    ejr__gbzzp = c.pyapi.import_module_noblock(hjt__wuypf)
    sijpp__ridz = c.pyapi.object_getattr_string(ejr__gbzzp, 'arrays')
    zzdgp__qelx = c.pyapi.call_method(sijpp__ridz, 'IntegerArray', (
        zjbf__wkwfq, ziee__fyih))
    data = c.pyapi.to_native_value(arr_typ, zzdgp__qelx).value
    c.pyapi.decref(zjbf__wkwfq)
    c.pyapi.decref(ziee__fyih)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(ejr__gbzzp)
    c.pyapi.decref(sijpp__ridz)
    c.pyapi.decref(zzdgp__qelx)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vhfil__iud.data = data
    vhfil__iud.name = name
    ewr__mtmun, fhop__dmlxf = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(types.int64, types.int64), types.DictType(types.int64,
        types.int64)(), [])
    vhfil__iud.dict = fhop__dmlxf
    return NativeValue(vhfil__iud._getvalue())


class CategoricalIndexType(types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
        assert isinstance(data, CategoricalArrayType
            ), 'CategoricalIndexType expects CategoricalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(CategoricalIndexType, self).__init__(name=
            f'CategoricalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return CategoricalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'categorical'

    @property
    def numpy_type_name(self):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        return str(get_categories_int_type(self.dtype))


@register_model(CategoricalIndexType)
class CategoricalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        xlnzn__ldfrh = get_categories_int_type(fe_type.data.dtype)
        vcucv__hvqw = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(xlnzn__ldfrh, types.int64))]
        super(CategoricalIndexTypeModel, self).__init__(dmm, fe_type,
            vcucv__hvqw)


@typeof_impl.register(pd.CategoricalIndex)
def typeof_categorical_index(val, c):
    return CategoricalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(CategoricalIndexType)
def box_categorical_index(typ, val, c):
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    ejr__gbzzp = c.pyapi.import_module_noblock(hjt__wuypf)
    yghpr__qafn = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, yghpr__qafn.data)
    mzsdj__jigp = c.pyapi.from_native_value(typ.data, yghpr__qafn.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, yghpr__qafn.name)
    ahx__uezg = c.pyapi.from_native_value(typ.name_typ, yghpr__qafn.name, c
        .env_manager)
    args = c.pyapi.tuple_pack([mzsdj__jigp])
    kws = c.pyapi.dict_pack([('name', ahx__uezg)])
    mfdbe__mliak = c.pyapi.object_getattr_string(ejr__gbzzp, 'CategoricalIndex'
        )
    dpl__hifwo = c.pyapi.call(mfdbe__mliak, args, kws)
    c.pyapi.decref(mzsdj__jigp)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(ejr__gbzzp)
    c.pyapi.decref(mfdbe__mliak)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return dpl__hifwo


@unbox(CategoricalIndexType)
def unbox_categorical_index(typ, val, c):
    from bodo.hiframes.pd_categorical_ext import get_categories_int_type
    jhka__vcfc = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, jhka__vcfc).value
    ahx__uezg = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ahx__uezg).value
    c.pyapi.decref(jhka__vcfc)
    c.pyapi.decref(ahx__uezg)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vhfil__iud.data = data
    vhfil__iud.name = name
    dtype = get_categories_int_type(typ.data.dtype)
    ewr__mtmun, fhop__dmlxf = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    vhfil__iud.dict = fhop__dmlxf
    return NativeValue(vhfil__iud._getvalue())


@intrinsic
def init_categorical_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        wye__vrpbg, honl__jjln = args
        yghpr__qafn = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        yghpr__qafn.data = wye__vrpbg
        yghpr__qafn.name = honl__jjln
        context.nrt.incref(builder, signature.args[0], wye__vrpbg)
        context.nrt.incref(builder, signature.args[1], honl__jjln)
        dtype = get_categories_int_type(signature.return_type.data.dtype)
        yghpr__qafn.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return yghpr__qafn._getvalue()
    krsg__nqpn = CategoricalIndexType(data, name)
    sig = signature(krsg__nqpn, data, name)
    return sig, codegen


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_categorical_index
    ) = init_index_equiv
make_attribute_wrapper(CategoricalIndexType, 'data', '_data')
make_attribute_wrapper(CategoricalIndexType, 'name', '_name')
make_attribute_wrapper(CategoricalIndexType, 'dict', '_dict')


@overload_method(CategoricalIndexType, 'copy', no_unliteral=True)
def overload_categorical_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    bamx__ymo = idx_typ_to_format_str_map[CategoricalIndexType].format('copy()'
        )
    ljixu__pamh = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('CategoricalIndex.copy', ljixu__pamh,
        idx_cpy_arg_defaults, fn_str=bamx__ymo, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), A._name)
    return impl


class IntervalIndexType(types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.libs.interval_arr_ext import IntervalArrayType
        assert isinstance(data, IntervalArrayType
            ), 'IntervalIndexType expects IntervalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(IntervalIndexType, self).__init__(name=
            f'IntervalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return IntervalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'interval[{self.data.arr_type.dtype}, right]'


@register_model(IntervalIndexType)
class IntervalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vcucv__hvqw = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(types.UniTuple(fe_type.data.arr_type.
            dtype, 2), types.int64))]
        super(IntervalIndexTypeModel, self).__init__(dmm, fe_type, vcucv__hvqw)


@typeof_impl.register(pd.IntervalIndex)
def typeof_interval_index(val, c):
    return IntervalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(IntervalIndexType)
def box_interval_index(typ, val, c):
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    ejr__gbzzp = c.pyapi.import_module_noblock(hjt__wuypf)
    rpypb__xwijb = numba.core.cgutils.create_struct_proxy(typ)(c.context, c
        .builder, val)
    c.context.nrt.incref(c.builder, typ.data, rpypb__xwijb.data)
    mzsdj__jigp = c.pyapi.from_native_value(typ.data, rpypb__xwijb.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, rpypb__xwijb.name)
    ahx__uezg = c.pyapi.from_native_value(typ.name_typ, rpypb__xwijb.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([mzsdj__jigp])
    kws = c.pyapi.dict_pack([('name', ahx__uezg)])
    mfdbe__mliak = c.pyapi.object_getattr_string(ejr__gbzzp, 'IntervalIndex')
    dpl__hifwo = c.pyapi.call(mfdbe__mliak, args, kws)
    c.pyapi.decref(mzsdj__jigp)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(ejr__gbzzp)
    c.pyapi.decref(mfdbe__mliak)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return dpl__hifwo


@unbox(IntervalIndexType)
def unbox_interval_index(typ, val, c):
    jhka__vcfc = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, jhka__vcfc).value
    ahx__uezg = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ahx__uezg).value
    c.pyapi.decref(jhka__vcfc)
    c.pyapi.decref(ahx__uezg)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vhfil__iud.data = data
    vhfil__iud.name = name
    dtype = types.UniTuple(typ.data.arr_type.dtype, 2)
    ewr__mtmun, fhop__dmlxf = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    vhfil__iud.dict = fhop__dmlxf
    return NativeValue(vhfil__iud._getvalue())


@intrinsic
def init_interval_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        wye__vrpbg, honl__jjln = args
        rpypb__xwijb = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        rpypb__xwijb.data = wye__vrpbg
        rpypb__xwijb.name = honl__jjln
        context.nrt.incref(builder, signature.args[0], wye__vrpbg)
        context.nrt.incref(builder, signature.args[1], honl__jjln)
        dtype = types.UniTuple(data.arr_type.dtype, 2)
        rpypb__xwijb.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return rpypb__xwijb._getvalue()
    krsg__nqpn = IntervalIndexType(data, name)
    sig = signature(krsg__nqpn, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_interval_index
    ) = init_index_equiv
make_attribute_wrapper(IntervalIndexType, 'data', '_data')
make_attribute_wrapper(IntervalIndexType, 'name', '_name')
make_attribute_wrapper(IntervalIndexType, 'dict', '_dict')


class NumericIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, dtype, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.dtype = dtype
        self.name_typ = name_typ
        data = dtype_to_array_type(dtype) if data is None else data
        self.data = data
        super(NumericIndexType, self).__init__(name=
            f'NumericIndexType({dtype}, {name_typ}, {data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return NumericIndexType(self.dtype, self.name_typ, self.data)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)


with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    Int64Index = pd.Int64Index
    UInt64Index = pd.UInt64Index
    Float64Index = pd.Float64Index


@typeof_impl.register(Int64Index)
def typeof_pd_int64_index(val, c):
    return NumericIndexType(types.int64, get_val_type_maybe_str_literal(val
        .name))


@typeof_impl.register(UInt64Index)
def typeof_pd_uint64_index(val, c):
    return NumericIndexType(types.uint64, get_val_type_maybe_str_literal(
        val.name))


@typeof_impl.register(Float64Index)
def typeof_pd_float64_index(val, c):
    return NumericIndexType(types.float64, get_val_type_maybe_str_literal(
        val.name))


@register_model(NumericIndexType)
class NumericIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vcucv__hvqw = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(fe_type.dtype, types.int64))]
        super(NumericIndexModel, self).__init__(dmm, fe_type, vcucv__hvqw)


make_attribute_wrapper(NumericIndexType, 'data', '_data')
make_attribute_wrapper(NumericIndexType, 'name', '_name')
make_attribute_wrapper(NumericIndexType, 'dict', '_dict')


@overload_method(NumericIndexType, 'copy', no_unliteral=True)
def overload_numeric_index_copy(A, name=None, deep=False, dtype=None, names
    =None):
    bamx__ymo = idx_typ_to_format_str_map[NumericIndexType].format('copy()')
    ljixu__pamh = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', ljixu__pamh, idx_cpy_arg_defaults,
        fn_str=bamx__ymo, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(NumericIndexType)
def box_numeric_index(typ, val, c):
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    tgl__wgaq = c.pyapi.import_module_noblock(hjt__wuypf)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, vhfil__iud.data)
    zzdgp__qelx = c.pyapi.from_native_value(typ.data, vhfil__iud.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, vhfil__iud.name)
    ahx__uezg = c.pyapi.from_native_value(typ.name_typ, vhfil__iud.name, c.
        env_manager)
    hqa__gvs = c.pyapi.make_none()
    imxco__wiej = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    myhw__dlr = c.pyapi.call_method(tgl__wgaq, 'Index', (zzdgp__qelx,
        hqa__gvs, imxco__wiej, ahx__uezg))
    c.pyapi.decref(zzdgp__qelx)
    c.pyapi.decref(hqa__gvs)
    c.pyapi.decref(imxco__wiej)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(tgl__wgaq)
    c.context.nrt.decref(c.builder, typ, val)
    return myhw__dlr


@intrinsic
def init_numeric_index(typingctx, data, name=None):
    name = types.none if is_overload_none(name) else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        xmp__zwsh = signature.return_type
        vhfil__iud = cgutils.create_struct_proxy(xmp__zwsh)(context, builder)
        vhfil__iud.data = args[0]
        vhfil__iud.name = args[1]
        context.nrt.incref(builder, xmp__zwsh.data, args[0])
        context.nrt.incref(builder, xmp__zwsh.name_typ, args[1])
        dtype = xmp__zwsh.dtype
        vhfil__iud.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return vhfil__iud._getvalue()
    return NumericIndexType(data.dtype, name, data)(data, name), codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_numeric_index
    ) = init_index_equiv


@unbox(NumericIndexType)
def unbox_numeric_index(typ, val, c):
    jhka__vcfc = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, jhka__vcfc).value
    ahx__uezg = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ahx__uezg).value
    c.pyapi.decref(jhka__vcfc)
    c.pyapi.decref(ahx__uezg)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vhfil__iud.data = data
    vhfil__iud.name = name
    dtype = typ.dtype
    ewr__mtmun, fhop__dmlxf = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    vhfil__iud.dict = fhop__dmlxf
    return NativeValue(vhfil__iud._getvalue())


def create_numeric_constructor(func, func_str, default_dtype):

    def overload_impl(data=None, dtype=None, copy=False, name=None):
        gsm__pctmq = dict(dtype=dtype)
        olsyk__dvtk = dict(dtype=None)
        check_unsupported_args(func_str, gsm__pctmq, olsyk__dvtk,
            package_name='pandas', module_name='Index')
        if is_overload_false(copy):

            def impl(data=None, dtype=None, copy=False, name=None):
                blz__zvsm = bodo.utils.conversion.coerce_to_ndarray(data)
                hnty__jxrf = bodo.utils.conversion.fix_arr_dtype(blz__zvsm,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(hnty__jxrf
                    , name)
        else:

            def impl(data=None, dtype=None, copy=False, name=None):
                blz__zvsm = bodo.utils.conversion.coerce_to_ndarray(data)
                if copy:
                    blz__zvsm = blz__zvsm.copy()
                hnty__jxrf = bodo.utils.conversion.fix_arr_dtype(blz__zvsm,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(hnty__jxrf
                    , name)
        return impl
    return overload_impl


def _install_numeric_constructors():
    for func, func_str, default_dtype in ((Int64Index, 'pandas.Int64Index',
        np.int64), (UInt64Index, 'pandas.UInt64Index', np.uint64), (
        Float64Index, 'pandas.Float64Index', np.float64)):
        overload_impl = create_numeric_constructor(func, func_str,
            default_dtype)
        overload(func, no_unliteral=True)(overload_impl)


_install_numeric_constructors()


class StringIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = string_array_type if data_typ is None else data_typ
        super(StringIndexType, self).__init__(name=
            f'StringIndexType({name_typ}, {self.data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return StringIndexType(self.name_typ, self.data)

    @property
    def dtype(self):
        return string_type

    @property
    def pandas_type_name(self):
        return 'unicode'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


@register_model(StringIndexType)
class StringIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vcucv__hvqw = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(string_type, types.int64))]
        super(StringIndexModel, self).__init__(dmm, fe_type, vcucv__hvqw)


make_attribute_wrapper(StringIndexType, 'data', '_data')
make_attribute_wrapper(StringIndexType, 'name', '_name')
make_attribute_wrapper(StringIndexType, 'dict', '_dict')


class BinaryIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data_typ=None):
        assert data_typ is None or data_typ == binary_array_type, 'data_typ must be binary_array_type'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = binary_array_type
        super(BinaryIndexType, self).__init__(name='BinaryIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return BinaryIndexType(self.name_typ)

    @property
    def dtype(self):
        return bytes_type

    @property
    def pandas_type_name(self):
        return 'bytes'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


@register_model(BinaryIndexType)
class BinaryIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vcucv__hvqw = [('data', binary_array_type), ('name', fe_type.
            name_typ), ('dict', types.DictType(bytes_type, types.int64))]
        super(BinaryIndexModel, self).__init__(dmm, fe_type, vcucv__hvqw)


make_attribute_wrapper(BinaryIndexType, 'data', '_data')
make_attribute_wrapper(BinaryIndexType, 'name', '_name')
make_attribute_wrapper(BinaryIndexType, 'dict', '_dict')


@unbox(BinaryIndexType)
@unbox(StringIndexType)
def unbox_binary_str_index(typ, val, c):
    rjw__ykap = typ.data
    scalar_type = typ.data.dtype
    jhka__vcfc = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(rjw__ykap, jhka__vcfc).value
    ahx__uezg = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ahx__uezg).value
    c.pyapi.decref(jhka__vcfc)
    c.pyapi.decref(ahx__uezg)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vhfil__iud.data = data
    vhfil__iud.name = name
    ewr__mtmun, fhop__dmlxf = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(scalar_type, types.int64), types.DictType(scalar_type,
        types.int64)(), [])
    vhfil__iud.dict = fhop__dmlxf
    return NativeValue(vhfil__iud._getvalue())


@box(BinaryIndexType)
@box(StringIndexType)
def box_binary_str_index(typ, val, c):
    rjw__ykap = typ.data
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    tgl__wgaq = c.pyapi.import_module_noblock(hjt__wuypf)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, rjw__ykap, vhfil__iud.data)
    zzdgp__qelx = c.pyapi.from_native_value(rjw__ykap, vhfil__iud.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, vhfil__iud.name)
    ahx__uezg = c.pyapi.from_native_value(typ.name_typ, vhfil__iud.name, c.
        env_manager)
    hqa__gvs = c.pyapi.make_none()
    imxco__wiej = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    myhw__dlr = c.pyapi.call_method(tgl__wgaq, 'Index', (zzdgp__qelx,
        hqa__gvs, imxco__wiej, ahx__uezg))
    c.pyapi.decref(zzdgp__qelx)
    c.pyapi.decref(hqa__gvs)
    c.pyapi.decref(imxco__wiej)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(tgl__wgaq)
    c.context.nrt.decref(c.builder, typ, val)
    return myhw__dlr


@intrinsic
def init_binary_str_index(typingctx, data, name=None):
    name = types.none if name is None else name
    sig = type(bodo.utils.typing.get_index_type_from_dtype(data.dtype))(name,
        data)(data, name)
    nebhs__zvxh = get_binary_str_codegen(is_binary=data.dtype == bytes_type)
    return sig, nebhs__zvxh


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_binary_str_index
    ) = init_index_equiv


def get_binary_str_codegen(is_binary=False):
    if is_binary:
        vvss__ceio = 'bytes_type'
    else:
        vvss__ceio = 'string_type'
    ixtwd__smxz = 'def impl(context, builder, signature, args):\n'
    ixtwd__smxz += '    assert len(args) == 2\n'
    ixtwd__smxz += '    index_typ = signature.return_type\n'
    ixtwd__smxz += (
        '    index_val = cgutils.create_struct_proxy(index_typ)(context, builder)\n'
        )
    ixtwd__smxz += '    index_val.data = args[0]\n'
    ixtwd__smxz += '    index_val.name = args[1]\n'
    ixtwd__smxz += '    # increase refcount of stored values\n'
    ixtwd__smxz += (
        '    context.nrt.incref(builder, signature.args[0], args[0])\n')
    ixtwd__smxz += (
        '    context.nrt.incref(builder, index_typ.name_typ, args[1])\n')
    ixtwd__smxz += '    # create empty dict for get_loc hashmap\n'
    ixtwd__smxz += '    index_val.dict = context.compile_internal(\n'
    ixtwd__smxz += '       builder,\n'
    ixtwd__smxz += (
        f'       lambda: numba.typed.Dict.empty({vvss__ceio}, types.int64),\n')
    ixtwd__smxz += (
        f'        types.DictType({vvss__ceio}, types.int64)(), [],)\n')
    ixtwd__smxz += '    return index_val._getvalue()\n'
    qmzm__azcg = {}
    exec(ixtwd__smxz, {'bodo': bodo, 'signature': signature, 'cgutils':
        cgutils, 'numba': numba, 'types': types, 'bytes_type': bytes_type,
        'string_type': string_type}, qmzm__azcg)
    impl = qmzm__azcg['impl']
    return impl


@overload_method(BinaryIndexType, 'copy', no_unliteral=True)
@overload_method(StringIndexType, 'copy', no_unliteral=True)
def overload_binary_string_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    typ = type(A)
    bamx__ymo = idx_typ_to_format_str_map[typ].format('copy()')
    ljixu__pamh = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', ljixu__pamh, idx_cpy_arg_defaults,
        fn_str=bamx__ymo, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), A._name)
    return impl


@overload_attribute(BinaryIndexType, 'name')
@overload_attribute(StringIndexType, 'name')
@overload_attribute(DatetimeIndexType, 'name')
@overload_attribute(TimedeltaIndexType, 'name')
@overload_attribute(RangeIndexType, 'name')
@overload_attribute(PeriodIndexType, 'name')
@overload_attribute(NumericIndexType, 'name')
@overload_attribute(IntervalIndexType, 'name')
@overload_attribute(CategoricalIndexType, 'name')
@overload_attribute(MultiIndexType, 'name')
def Index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_index_getitem(I, ind):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType)
        ) and isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, NumericIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_numeric_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))
    if isinstance(I, (StringIndexType, BinaryIndexType)):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_binary_str_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))


def array_type_to_index(arr_typ, name_typ=None):
    if is_str_arr_type(arr_typ):
        return StringIndexType(name_typ, arr_typ)
    if arr_typ == bodo.binary_array_type:
        return BinaryIndexType(name_typ)
    assert isinstance(arr_typ, (types.Array, IntegerArrayType, bodo.
        CategoricalArrayType)) or arr_typ in (bodo.datetime_date_array_type,
        bodo.boolean_array
        ), f'Converting array type {arr_typ} to index not supported'
    if (arr_typ == bodo.datetime_date_array_type or arr_typ.dtype == types.
        NPDatetime('ns')):
        return DatetimeIndexType(name_typ)
    if isinstance(arr_typ, bodo.DatetimeArrayType):
        return DatetimeIndexType(name_typ, arr_typ)
    if isinstance(arr_typ, bodo.CategoricalArrayType):
        return CategoricalIndexType(arr_typ, name_typ)
    if arr_typ.dtype == types.NPTimedelta('ns'):
        return TimedeltaIndexType(name_typ)
    if isinstance(arr_typ.dtype, (types.Integer, types.Float, types.Boolean)):
        return NumericIndexType(arr_typ.dtype, name_typ, arr_typ)
    raise BodoError(f'invalid index type {arr_typ}')


def is_pd_index_type(t):
    return isinstance(t, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, StringIndexType, BinaryIndexType, RangeIndexType,
        HeterogeneousIndexType))


@overload_method(RangeIndexType, 'take', no_unliteral=True)
@overload_method(NumericIndexType, 'take', no_unliteral=True)
@overload_method(StringIndexType, 'take', no_unliteral=True)
@overload_method(BinaryIndexType, 'take', no_unliteral=True)
@overload_method(CategoricalIndexType, 'take', no_unliteral=True)
@overload_method(PeriodIndexType, 'take', no_unliteral=True)
@overload_method(DatetimeIndexType, 'take', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'take', no_unliteral=True)
def overload_index_take(I, indices, axis=0, allow_fill=True, fill_value=None):
    rzhyy__ula = dict(axis=axis, allow_fill=allow_fill, fill_value=fill_value)
    ffnih__mhxt = dict(axis=0, allow_fill=True, fill_value=None)
    check_unsupported_args('Index.take', rzhyy__ula, ffnih__mhxt,
        package_name='pandas', module_name='Index')
    return lambda I, indices: I[indices]


@numba.njit(no_cpython_wrapper=True)
def _init_engine(I):
    if len(I) > 0 and not I._dict:
        jpi__cyptd = bodo.utils.conversion.coerce_to_array(I)
        for i in range(len(jpi__cyptd)):
            val = jpi__cyptd[i]
            if val in I._dict:
                raise ValueError(
                    'Index.get_loc(): non-unique Index not supported yet')
            I._dict[val] = i


@overload(operator.contains, no_unliteral=True)
def index_contains(I, val):
    if not is_index_type(I):
        return
    if isinstance(I, RangeIndexType):
        return lambda I, val: range_contains(I.start, I.stop, I.step, val)

    def impl(I, val):
        key = bodo.utils.conversion.unbox_if_timestamp(val)
        if not is_null_value(I._dict):
            _init_engine(I)
            return key in I._dict
        else:
            kywjx__npzbx = (
                'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                )
            warnings.warn(kywjx__npzbx)
            jpi__cyptd = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(jpi__cyptd)):
                if jpi__cyptd[i] == key:
                    if ind != -1:
                        raise ValueError(
                            'Index.get_loc(): non-unique Index not supported yet'
                            )
                    ind = i
        return ind != -1
    return impl


@register_jitable
def range_contains(start, stop, step, val):
    if step > 0 and not start <= val < stop:
        return False
    if step < 0 and not stop <= val < start:
        return False
    return (val - start) % step == 0


@overload_method(RangeIndexType, 'get_loc', no_unliteral=True)
@overload_method(NumericIndexType, 'get_loc', no_unliteral=True)
@overload_method(StringIndexType, 'get_loc', no_unliteral=True)
@overload_method(BinaryIndexType, 'get_loc', no_unliteral=True)
@overload_method(PeriodIndexType, 'get_loc', no_unliteral=True)
@overload_method(DatetimeIndexType, 'get_loc', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'get_loc', no_unliteral=True)
def overload_index_get_loc(I, key, method=None, tolerance=None):
    rzhyy__ula = dict(method=method, tolerance=tolerance)
    lhn__ygle = dict(method=None, tolerance=None)
    check_unsupported_args('Index.get_loc', rzhyy__ula, lhn__ygle,
        package_name='pandas', module_name='Index')
    key = types.unliteral(key)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.get_loc')
    if key == pd_timestamp_type:
        key = bodo.datetime64ns
    if key == pd_timedelta_type:
        key = bodo.timedelta64ns
    if key != I.dtype:
        raise_bodo_error(
            'Index.get_loc(): invalid label type in Index.get_loc()')
    if isinstance(I, RangeIndexType):

        def impl_range(I, key, method=None, tolerance=None):
            if not range_contains(I.start, I.stop, I.step, key):
                raise KeyError('Index.get_loc(): key not found')
            return key - I.start if I.step == 1 else (key - I.start) // I.step
        return impl_range

    def impl(I, key, method=None, tolerance=None):
        key = bodo.utils.conversion.unbox_if_timestamp(key)
        if not is_null_value(I._dict):
            _init_engine(I)
            ind = I._dict.get(key, -1)
        else:
            kywjx__npzbx = (
                'Index.get_loc() can be slow for global Index objects (pass as argument to JIT function for better performance).'
                )
            warnings.warn(kywjx__npzbx)
            jpi__cyptd = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(jpi__cyptd)):
                if jpi__cyptd[i] == key:
                    if ind != -1:
                        raise ValueError(
                            'Index.get_loc(): non-unique Index not supported yet'
                            )
                    ind = i
        if ind == -1:
            raise KeyError('Index.get_loc(): key not found')
        return ind
    return impl


def create_isna_specific_method(overload_name):

    def overload_index_isna_specific_method(I):
        tdn__pyrte = overload_name in {'isna', 'isnull'}
        if isinstance(I, RangeIndexType):

            def impl(I):
                numba.parfors.parfor.init_prange()
                nglwp__kmpbu = len(I)
                fex__oeiti = np.empty(nglwp__kmpbu, np.bool_)
                for i in numba.parfors.parfor.internal_prange(nglwp__kmpbu):
                    fex__oeiti[i] = not tdn__pyrte
                return fex__oeiti
            return impl
        ixtwd__smxz = f"""def impl(I):
    numba.parfors.parfor.init_prange()
    arr = bodo.hiframes.pd_index_ext.get_index_data(I)
    n = len(arr)
    out_arr = np.empty(n, np.bool_)
    for i in numba.parfors.parfor.internal_prange(n):
       out_arr[i] = {'' if tdn__pyrte else 'not '}bodo.libs.array_kernels.isna(arr, i)
    return out_arr
"""
        qmzm__azcg = {}
        exec(ixtwd__smxz, {'bodo': bodo, 'np': np, 'numba': numba}, qmzm__azcg)
        impl = qmzm__azcg['impl']
        return impl
    return overload_index_isna_specific_method


isna_overload_types = (RangeIndexType, NumericIndexType, StringIndexType,
    BinaryIndexType, CategoricalIndexType, PeriodIndexType,
    DatetimeIndexType, TimedeltaIndexType)
isna_specific_methods = 'isna', 'notna', 'isnull', 'notnull'


def _install_isna_specific_methods():
    for remlj__rpgkf in isna_overload_types:
        for overload_name in isna_specific_methods:
            overload_impl = create_isna_specific_method(overload_name)
            overload_method(remlj__rpgkf, overload_name, no_unliteral=True,
                inline='always')(overload_impl)


_install_isna_specific_methods()


@overload_attribute(RangeIndexType, 'values')
@overload_attribute(NumericIndexType, 'values')
@overload_attribute(StringIndexType, 'values')
@overload_attribute(BinaryIndexType, 'values')
@overload_attribute(CategoricalIndexType, 'values')
@overload_attribute(PeriodIndexType, 'values')
@overload_attribute(DatetimeIndexType, 'values')
@overload_attribute(TimedeltaIndexType, 'values')
def overload_values(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I, 'Index.values'
        )
    return lambda I: bodo.utils.conversion.coerce_to_array(I)


@overload(len, no_unliteral=True)
def overload_index_len(I):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType,
        PeriodIndexType, IntervalIndexType, CategoricalIndexType,
        DatetimeIndexType, TimedeltaIndexType, HeterogeneousIndexType)):
        return lambda I: len(bodo.hiframes.pd_index_ext.get_index_data(I))


@overload_attribute(DatetimeIndexType, 'shape')
@overload_attribute(NumericIndexType, 'shape')
@overload_attribute(StringIndexType, 'shape')
@overload_attribute(BinaryIndexType, 'shape')
@overload_attribute(PeriodIndexType, 'shape')
@overload_attribute(TimedeltaIndexType, 'shape')
@overload_attribute(IntervalIndexType, 'shape')
@overload_attribute(CategoricalIndexType, 'shape')
def overload_index_shape(s):
    return lambda s: (len(bodo.hiframes.pd_index_ext.get_index_data(s)),)


@overload_attribute(RangeIndexType, 'shape')
def overload_range_index_shape(s):
    return lambda s: (len(s),)


@overload_attribute(NumericIndexType, 'is_monotonic', inline='always')
@overload_attribute(RangeIndexType, 'is_monotonic', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic', inline='always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic', inline='always')
@overload_attribute(NumericIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_increasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_increasing', inline=
    'always')
def overload_index_is_montonic(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.is_monotonic_increasing')
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            jpi__cyptd = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(jpi__cyptd, 1)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step > 0 or len(I) <= 1
        return impl


@overload_attribute(NumericIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_decreasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_decreasing', inline=
    'always')
def overload_index_is_montonic_decreasing(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.is_monotonic_decreasing')
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            jpi__cyptd = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(jpi__cyptd, 2)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step < 0 or len(I) <= 1
        return impl


@overload_method(NumericIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(DatetimeIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(TimedeltaIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(StringIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(PeriodIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(CategoricalIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(BinaryIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(RangeIndexType, 'duplicated', inline='always',
    no_unliteral=True)
def overload_index_duplicated(I, keep='first'):
    if isinstance(I, RangeIndexType):

        def impl(I, keep='first'):
            return np.zeros(len(I), np.bool_)
        return impl

    def impl(I, keep='first'):
        jpi__cyptd = bodo.hiframes.pd_index_ext.get_index_data(I)
        fex__oeiti = bodo.libs.array_kernels.duplicated((jpi__cyptd,))
        return fex__oeiti
    return impl


@overload_method(RangeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(NumericIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(StringIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(BinaryIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(CategoricalIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(PeriodIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(DatetimeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(TimedeltaIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
def overload_index_drop_duplicates(I, keep='first'):
    rzhyy__ula = dict(keep=keep)
    lhn__ygle = dict(keep='first')
    check_unsupported_args('Index.drop_duplicates', rzhyy__ula, lhn__ygle,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):
        return lambda I, keep='first': I.copy()
    ixtwd__smxz = """def impl(I, keep='first'):
    data = bodo.hiframes.pd_index_ext.get_index_data(I)
    arr = bodo.libs.array_kernels.drop_duplicates_array(data)
    name = bodo.hiframes.pd_index_ext.get_index_name(I)
"""
    if isinstance(I, PeriodIndexType):
        ixtwd__smxz += f"""    return bodo.hiframes.pd_index_ext.init_period_index(arr, name, '{I.freq}')
"""
    else:
        ixtwd__smxz += (
            '    return bodo.utils.conversion.index_from_array(arr, name)')
    qmzm__azcg = {}
    exec(ixtwd__smxz, {'bodo': bodo}, qmzm__azcg)
    impl = qmzm__azcg['impl']
    return impl


@numba.generated_jit(nopython=True)
def get_index_data(S):
    return lambda S: S._data


@numba.generated_jit(nopython=True)
def get_index_name(S):
    return lambda S: S._name


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_index_data',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_datetime_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_timedelta_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_numeric_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_binary_str_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_categorical_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func


def get_index_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    mqaof__xymxi = args[0]
    if isinstance(self.typemap[mqaof__xymxi.name], HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(mqaof__xymxi):
        return ArrayAnalysis.AnalyzeResult(shape=mqaof__xymxi, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_get_index_data
    ) = get_index_data_equiv


@overload_method(RangeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(NumericIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(StringIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(BinaryIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(CategoricalIndexType, 'map', inline='always', no_unliteral
    =True)
@overload_method(PeriodIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(DatetimeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'map', inline='always', no_unliteral=True)
def overload_index_map(I, mapper, na_action=None):
    if not is_const_func_type(mapper):
        raise BodoError("Index.map(): 'mapper' should be a function")
    rzhyy__ula = dict(na_action=na_action)
    xsj__xpk = dict(na_action=None)
    check_unsupported_args('Index.map', rzhyy__ula, xsj__xpk, package_name=
        'pandas', module_name='Index')
    dtype = I.dtype
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.map')
    if dtype == types.NPDatetime('ns'):
        dtype = pd_timestamp_type
    if dtype == types.NPTimedelta('ns'):
        dtype = pd_timedelta_type
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = dtype.elem_type
    uere__agtxy = numba.core.registry.cpu_target.typing_context
    amug__ajif = numba.core.registry.cpu_target.target_context
    try:
        olu__aev = get_const_func_output_type(mapper, (dtype,), {},
            uere__agtxy, amug__ajif)
    except Exception as vdnmg__asqx:
        raise_bodo_error(get_udf_error_msg('Index.map()', vdnmg__asqx))
    qnz__gkdhi = get_udf_out_arr_type(olu__aev)
    func = get_overload_const_func(mapper, None)
    ixtwd__smxz = 'def f(I, mapper, na_action=None):\n'
    ixtwd__smxz += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    ixtwd__smxz += '  A = bodo.utils.conversion.coerce_to_array(I)\n'
    ixtwd__smxz += '  numba.parfors.parfor.init_prange()\n'
    ixtwd__smxz += '  n = len(A)\n'
    ixtwd__smxz += '  S = bodo.utils.utils.alloc_type(n, _arr_typ, (-1,))\n'
    ixtwd__smxz += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    ixtwd__smxz += '    t2 = bodo.utils.conversion.box_if_dt64(A[i])\n'
    ixtwd__smxz += '    v = map_func(t2)\n'
    ixtwd__smxz += '    S[i] = bodo.utils.conversion.unbox_if_timestamp(v)\n'
    ixtwd__smxz += '  return bodo.utils.conversion.index_from_array(S, name)\n'
    ltb__mjary = bodo.compiler.udf_jit(func)
    qmzm__azcg = {}
    exec(ixtwd__smxz, {'numba': numba, 'np': np, 'pd': pd, 'bodo': bodo,
        'map_func': ltb__mjary, '_arr_typ': qnz__gkdhi,
        'init_nested_counts': bodo.utils.indexing.init_nested_counts,
        'add_nested_counts': bodo.utils.indexing.add_nested_counts,
        'data_arr_type': qnz__gkdhi.dtype}, qmzm__azcg)
    f = qmzm__azcg['f']
    return f


@lower_builtin(operator.is_, NumericIndexType, NumericIndexType)
@lower_builtin(operator.is_, StringIndexType, StringIndexType)
@lower_builtin(operator.is_, BinaryIndexType, BinaryIndexType)
@lower_builtin(operator.is_, PeriodIndexType, PeriodIndexType)
@lower_builtin(operator.is_, DatetimeIndexType, DatetimeIndexType)
@lower_builtin(operator.is_, TimedeltaIndexType, TimedeltaIndexType)
@lower_builtin(operator.is_, IntervalIndexType, IntervalIndexType)
@lower_builtin(operator.is_, CategoricalIndexType, CategoricalIndexType)
def index_is(context, builder, sig, args):
    ymx__cehm, qmpo__pxwa = sig.args
    if ymx__cehm != qmpo__pxwa:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return a._data is b._data and a._name is b._name
    return context.compile_internal(builder, index_is_impl, sig, args)


@lower_builtin(operator.is_, RangeIndexType, RangeIndexType)
def range_index_is(context, builder, sig, args):
    ymx__cehm, qmpo__pxwa = sig.args
    if ymx__cehm != qmpo__pxwa:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._start == b._start and a._stop == b._stop and a._step ==
            b._step and a._name is b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)


def create_binary_op_overload(op):

    def overload_index_binary_op(lhs, rhs):
        if is_index_type(lhs):
            ixtwd__smxz = """def impl(lhs, rhs):
  arr = bodo.utils.conversion.coerce_to_array(lhs)
"""
            if rhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                ixtwd__smxz += """  dt = bodo.utils.conversion.unbox_if_timestamp(rhs)
  return op(arr, dt)
"""
            else:
                ixtwd__smxz += """  rhs_arr = bodo.utils.conversion.get_array_if_series_or_index(rhs)
  return op(arr, rhs_arr)
"""
            qmzm__azcg = {}
            exec(ixtwd__smxz, {'bodo': bodo, 'op': op}, qmzm__azcg)
            impl = qmzm__azcg['impl']
            return impl
        if is_index_type(rhs):
            ixtwd__smxz = """def impl(lhs, rhs):
  arr = bodo.utils.conversion.coerce_to_array(rhs)
"""
            if lhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                ixtwd__smxz += """  dt = bodo.utils.conversion.unbox_if_timestamp(lhs)
  return op(dt, arr)
"""
            else:
                ixtwd__smxz += """  lhs_arr = bodo.utils.conversion.get_array_if_series_or_index(lhs)
  return op(lhs_arr, arr)
"""
            qmzm__azcg = {}
            exec(ixtwd__smxz, {'bodo': bodo, 'op': op}, qmzm__azcg)
            impl = qmzm__azcg['impl']
            return impl
        if isinstance(lhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(lhs.data):

                def impl3(lhs, rhs):
                    data = bodo.utils.conversion.coerce_to_array(lhs)
                    jpi__cyptd = bodo.utils.conversion.coerce_to_array(data)
                    eqmok__leuzr = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    fex__oeiti = op(jpi__cyptd, eqmok__leuzr)
                    return fex__oeiti
                return impl3
            count = len(lhs.data.types)
            ixtwd__smxz = 'def f(lhs, rhs):\n'
            ixtwd__smxz += '  return [{}]\n'.format(','.join(
                'op(lhs[{}], rhs{})'.format(i, f'[{i}]' if is_iterable_type
                (rhs) else '') for i in range(count)))
            qmzm__azcg = {}
            exec(ixtwd__smxz, {'op': op, 'np': np}, qmzm__azcg)
            impl = qmzm__azcg['f']
            return impl
        if isinstance(rhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(rhs.data):

                def impl4(lhs, rhs):
                    data = bodo.hiframes.pd_index_ext.get_index_data(rhs)
                    jpi__cyptd = bodo.utils.conversion.coerce_to_array(data)
                    eqmok__leuzr = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    fex__oeiti = op(eqmok__leuzr, jpi__cyptd)
                    return fex__oeiti
                return impl4
            count = len(rhs.data.types)
            ixtwd__smxz = 'def f(lhs, rhs):\n'
            ixtwd__smxz += '  return [{}]\n'.format(','.join(
                'op(lhs{}, rhs[{}])'.format(f'[{i}]' if is_iterable_type(
                lhs) else '', i) for i in range(count)))
            qmzm__azcg = {}
            exec(ixtwd__smxz, {'op': op, 'np': np}, qmzm__azcg)
            impl = qmzm__azcg['f']
            return impl
    return overload_index_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        overload_impl = create_binary_op_overload(op)
        overload(op, inline='always')(overload_impl)


_install_binary_ops()


def is_index_type(t):
    return isinstance(t, (RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, PeriodIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType))


@lower_cast(RangeIndexType, NumericIndexType)
def cast_range_index_to_int_index(context, builder, fromty, toty, val):
    f = lambda I: init_numeric_index(np.arange(I._start, I._stop, I._step),
        bodo.hiframes.pd_index_ext.get_index_name(I))
    return context.compile_internal(builder, f, toty(fromty), [val])


class HeterogeneousIndexType(types.Type):
    ndim = 1

    def __init__(self, data=None, name_typ=None):
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        super(HeterogeneousIndexType, self).__init__(name=
            f'heter_index({data}, {name_typ})')

    def copy(self):
        return HeterogeneousIndexType(self.data, self.name_typ)

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return 'object'


@register_model(HeterogeneousIndexType)
class HeterogeneousIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vcucv__hvqw = [('data', fe_type.data), ('name', fe_type.name_typ)]
        super(HeterogeneousIndexModel, self).__init__(dmm, fe_type, vcucv__hvqw
            )


make_attribute_wrapper(HeterogeneousIndexType, 'data', '_data')
make_attribute_wrapper(HeterogeneousIndexType, 'name', '_name')


@overload_method(HeterogeneousIndexType, 'copy', no_unliteral=True)
def overload_heter_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    bamx__ymo = idx_typ_to_format_str_map[HeterogeneousIndexType].format(
        'copy()')
    ljixu__pamh = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', ljixu__pamh, idx_cpy_arg_defaults,
        fn_str=bamx__ymo, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(HeterogeneousIndexType)
def box_heter_index(typ, val, c):
    hjt__wuypf = c.context.insert_const_string(c.builder.module, 'pandas')
    tgl__wgaq = c.pyapi.import_module_noblock(hjt__wuypf)
    vhfil__iud = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, vhfil__iud.data)
    zzdgp__qelx = c.pyapi.from_native_value(typ.data, vhfil__iud.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, vhfil__iud.name)
    ahx__uezg = c.pyapi.from_native_value(typ.name_typ, vhfil__iud.name, c.
        env_manager)
    hqa__gvs = c.pyapi.make_none()
    imxco__wiej = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    myhw__dlr = c.pyapi.call_method(tgl__wgaq, 'Index', (zzdgp__qelx,
        hqa__gvs, imxco__wiej, ahx__uezg))
    c.pyapi.decref(zzdgp__qelx)
    c.pyapi.decref(hqa__gvs)
    c.pyapi.decref(imxco__wiej)
    c.pyapi.decref(ahx__uezg)
    c.pyapi.decref(tgl__wgaq)
    c.context.nrt.decref(c.builder, typ, val)
    return myhw__dlr


@intrinsic
def init_heter_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        xmp__zwsh = signature.return_type
        vhfil__iud = cgutils.create_struct_proxy(xmp__zwsh)(context, builder)
        vhfil__iud.data = args[0]
        vhfil__iud.name = args[1]
        context.nrt.incref(builder, xmp__zwsh.data, args[0])
        context.nrt.incref(builder, xmp__zwsh.name_typ, args[1])
        return vhfil__iud._getvalue()
    return HeterogeneousIndexType(data, name)(data, name), codegen


@overload_attribute(HeterogeneousIndexType, 'name')
def heter_index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload_attribute(NumericIndexType, 'nbytes')
@overload_attribute(DatetimeIndexType, 'nbytes')
@overload_attribute(TimedeltaIndexType, 'nbytes')
@overload_attribute(RangeIndexType, 'nbytes')
@overload_attribute(StringIndexType, 'nbytes')
@overload_attribute(BinaryIndexType, 'nbytes')
@overload_attribute(CategoricalIndexType, 'nbytes')
@overload_attribute(PeriodIndexType, 'nbytes')
def overload_nbytes(I):
    if isinstance(I, RangeIndexType):

        def _impl_nbytes(I):
            return bodo.io.np_io.get_dtype_size(type(I._start)
                ) + bodo.io.np_io.get_dtype_size(type(I._step)
                ) + bodo.io.np_io.get_dtype_size(type(I._stop))
        return _impl_nbytes
    else:

        def _impl_nbytes(I):
            return I._data.nbytes
        return _impl_nbytes


@overload_method(NumericIndexType, 'rename', inline='always')
@overload_method(DatetimeIndexType, 'rename', inline='always')
@overload_method(TimedeltaIndexType, 'rename', inline='always')
@overload_method(RangeIndexType, 'rename', inline='always')
@overload_method(StringIndexType, 'rename', inline='always')
@overload_method(BinaryIndexType, 'rename', inline='always')
@overload_method(CategoricalIndexType, 'rename', inline='always')
@overload_method(PeriodIndexType, 'rename', inline='always')
@overload_method(IntervalIndexType, 'rename', inline='always')
@overload_method(HeterogeneousIndexType, 'rename', inline='always')
def overload_rename(I, name, inplace=False):
    if is_overload_true(inplace):
        raise BodoError('Index.rename(): inplace index renaming unsupported')
    return init_index(I, name)


def init_index(I, name):
    qolm__zihgx = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index}
    if type(I) in qolm__zihgx:
        init_func = qolm__zihgx[type(I)]
        return lambda I, name, inplace=False: init_func(bodo.hiframes.
            pd_index_ext.get_index_data(I).copy(), name)
    if isinstance(I, RangeIndexType):
        return lambda I, name, inplace=False: I.copy(name=name)
    if isinstance(I, PeriodIndexType):
        freq = I.freq
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_period_index(bodo.hiframes.pd_index_ext.get_index_data(I).
            copy(), name, freq))
    if isinstance(I, HeterogeneousIndexType):
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_heter_index(bodo.hiframes.pd_index_ext.get_index_data(I),
            name))
    raise_bodo_error(f'init_index(): Unknown type {type(I)}')


@overload(operator.getitem, no_unliteral=True)
def overload_heter_index_getitem(I, ind):
    if not isinstance(I, HeterogeneousIndexType):
        return
    if isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, HeterogeneousIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_heter_index(bodo
            .hiframes.pd_index_ext.get_index_data(I)[ind], bodo.hiframes.
            pd_index_ext.get_index_name(I))


@lower_constant(DatetimeIndexType)
@lower_constant(TimedeltaIndexType)
def lower_constant_time_index(context, builder, ty, pyval):
    if isinstance(ty.data, bodo.DatetimeArrayType):
        data = context.get_constant_generic(builder, ty.data, pyval.array)
    else:
        data = context.get_constant_generic(builder, types.Array(types.
            int64, 1, 'C'), pyval.values.view(np.int64))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    htu__waj = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, htu__waj])


@lower_constant(PeriodIndexType)
def lower_constant_period_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, bodo.IntegerArrayType(
        types.int64), pd.arrays.IntegerArray(pyval.asi8, pyval.isna()))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    htu__waj = context.get_constant_null(types.DictType(types.int64, types.
        int64))
    return lir.Constant.literal_struct([data, name, htu__waj])


@lower_constant(NumericIndexType)
def lower_constant_numeric_index(context, builder, ty, pyval):
    assert isinstance(ty.dtype, (types.Integer, types.Float, types.Boolean))
    data = context.get_constant_generic(builder, types.Array(ty.dtype, 1,
        'C'), pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    htu__waj = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, htu__waj])


@lower_constant(StringIndexType)
@lower_constant(BinaryIndexType)
def lower_constant_binary_string_index(context, builder, ty, pyval):
    rjw__ykap = ty.data
    scalar_type = ty.data.dtype
    data = context.get_constant_generic(builder, rjw__ykap, pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    htu__waj = context.get_constant_null(types.DictType(scalar_type, types.
        int64))
    return lir.Constant.literal_struct([data, name, htu__waj])


@lower_builtin('getiter', RangeIndexType)
def getiter_range_index(context, builder, sig, args):
    [fjbw__yjae] = sig.args
    [eeh__ocup] = args
    eitf__hbr = context.make_helper(builder, fjbw__yjae, value=eeh__ocup)
    qwo__iau = context.make_helper(builder, sig.return_type)
    codpt__hprna = cgutils.alloca_once_value(builder, eitf__hbr.start)
    cbfi__moy = context.get_constant(types.intp, 0)
    jqp__vdwmm = cgutils.alloca_once_value(builder, cbfi__moy)
    qwo__iau.iter = codpt__hprna
    qwo__iau.stop = eitf__hbr.stop
    qwo__iau.step = eitf__hbr.step
    qwo__iau.count = jqp__vdwmm
    skgt__gztpj = builder.sub(eitf__hbr.stop, eitf__hbr.start)
    uhui__poz = context.get_constant(types.intp, 1)
    qwbp__flim = builder.icmp_signed('>', skgt__gztpj, cbfi__moy)
    gcnr__rbg = builder.icmp_signed('>', eitf__hbr.step, cbfi__moy)
    nzce__txjgh = builder.not_(builder.xor(qwbp__flim, gcnr__rbg))
    with builder.if_then(nzce__txjgh):
        sln__jjwkg = builder.srem(skgt__gztpj, eitf__hbr.step)
        sln__jjwkg = builder.select(qwbp__flim, sln__jjwkg, builder.neg(
            sln__jjwkg))
        boy__gnh = builder.icmp_signed('>', sln__jjwkg, cbfi__moy)
        udhx__ckbo = builder.add(builder.sdiv(skgt__gztpj, eitf__hbr.step),
            builder.select(boy__gnh, uhui__poz, cbfi__moy))
        builder.store(udhx__ckbo, jqp__vdwmm)
    dpl__hifwo = qwo__iau._getvalue()
    fmd__yhix = impl_ret_new_ref(context, builder, sig.return_type, dpl__hifwo)
    return fmd__yhix


def _install_index_getiter():
    index_types = [NumericIndexType, StringIndexType, BinaryIndexType,
        CategoricalIndexType, TimedeltaIndexType, DatetimeIndexType]
    for typ in index_types:
        lower_builtin('getiter', typ)(numba.np.arrayobj.getiter_array)


_install_index_getiter()
index_unsupported_methods = ['all', 'any', 'append', 'argmax', 'argmin',
    'argsort', 'asof', 'asof_locs', 'astype', 'delete', 'difference',
    'drop', 'droplevel', 'dropna', 'equals', 'factorize', 'fillna',
    'format', 'get_indexer', 'get_indexer_for', 'get_indexer_non_unique',
    'get_level_values', 'get_slice_bound', 'get_value', 'groupby',
    'holds_integer', 'identical', 'insert', 'intersection', 'is_',
    'is_boolean', 'is_categorical', 'is_floating', 'is_integer',
    'is_interval', 'is_mixed', 'is_numeric', 'is_object',
    'is_type_compatible', 'isin', 'item', 'join', 'memory_usage', 'nunique',
    'putmask', 'ravel', 'reindex', 'repeat', 'searchsorted', 'set_names',
    'set_value', 'shift', 'slice_indexer', 'slice_locs', 'sort',
    'sort_values', 'sortlevel', 'str', 'symmetric_difference',
    'to_flat_index', 'to_frame', 'to_list', 'to_native_types', 'to_numpy',
    'to_series', 'tolist', 'transpose', 'union', 'unique', 'value_counts',
    'view', 'where']
index_unsupported_atrs = ['T', 'array', 'asi8', 'dtype', 'has_duplicates',
    'hasnans', 'inferred_type', 'is_all_dates', 'is_unique', 'ndim',
    'nlevels', 'size', 'names', 'empty']
cat_idx_unsupported_atrs = ['codes', 'categories', 'ordered',
    'is_monotonic', 'is_monotonic_increasing', 'is_monotonic_decreasing']
cat_idx_unsupported_methods = ['rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered', 'get_loc']
interval_idx_unsupported_atrs = ['closed', 'is_empty',
    'is_non_overlapping_monotonic', 'is_overlapping', 'left', 'right',
    'mid', 'length', 'values', 'shape', 'nbytes', 'is_monotonic',
    'is_monotonic_increasing', 'is_monotonic_decreasing']
interval_idx_unsupported_methods = ['contains', 'copy', 'overlaps',
    'set_closed', 'to_tuples', 'take', 'get_loc', 'isna', 'isnull', 'map']
multi_index_unsupported_atrs = ['levshape', 'levels', 'codes', 'dtypes',
    'values', 'shape', 'nbytes', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
multi_index_unsupported_methods = ['copy', 'set_levels', 'set_codes',
    'swaplevel', 'reorder_levels', 'remove_unused_levels', 'get_loc',
    'get_locs', 'get_loc_level', 'take', 'isna', 'isnull', 'map']
dt_index_unsupported_atrs = ['time', 'timez', 'tz', 'freq', 'freqstr',
    'inferred_freq']
dt_index_unsupported_methods = ['normalize', 'strftime', 'snap',
    'tz_localize', 'round', 'floor', 'ceil', 'to_period', 'to_perioddelta',
    'to_pydatetime', 'month_name', 'day_name', 'mean', 'indexer_at_time',
    'indexer_between', 'indexer_between_time']
td_index_unsupported_atrs = ['components', 'inferred_freq']
td_index_unsupported_methods = ['to_pydatetime', 'round', 'floor', 'ceil',
    'mean']
period_index_unsupported_atrs = ['day', 'dayofweek', 'day_of_week',
    'dayofyear', 'day_of_year', 'days_in_month', 'daysinmonth', 'freq',
    'freqstr', 'hour', 'is_leap_year', 'minute', 'month', 'quarter',
    'second', 'week', 'weekday', 'weekofyear', 'year', 'end_time', 'qyear',
    'start_time', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
string_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
binary_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
period_index_unsupported_methods = ['asfreq', 'strftime', 'to_timestamp']
index_types = [('pandas.RangeIndex.{}', RangeIndexType), (
    'pandas.Index.{} with numeric data', NumericIndexType), (
    'pandas.Index.{} with string data', StringIndexType), (
    'pandas.Index.{} with binary data', BinaryIndexType), (
    'pandas.TimedeltaIndex.{}', TimedeltaIndexType), (
    'pandas.IntervalIndex.{}', IntervalIndexType), (
    'pandas.CategoricalIndex.{}', CategoricalIndexType), (
    'pandas.PeriodIndex.{}', PeriodIndexType), ('pandas.DatetimeIndex.{}',
    DatetimeIndexType), ('pandas.MultiIndex.{}', MultiIndexType)]
for name, typ in index_types:
    idx_typ_to_format_str_map[typ] = name


def _install_index_unsupported():
    for rlq__ptgeg in index_unsupported_methods:
        for birj__fpyr, typ in index_types:
            overload_method(typ, rlq__ptgeg, no_unliteral=True)(
                create_unsupported_overload(birj__fpyr.format(rlq__ptgeg +
                '()')))
    for ujl__zvc in index_unsupported_atrs:
        for birj__fpyr, typ in index_types:
            overload_attribute(typ, ujl__zvc, no_unliteral=True)(
                create_unsupported_overload(birj__fpyr.format(ujl__zvc)))
    axluc__odn = [(StringIndexType, string_index_unsupported_atrs), (
        BinaryIndexType, binary_index_unsupported_atrs), (
        CategoricalIndexType, cat_idx_unsupported_atrs), (IntervalIndexType,
        interval_idx_unsupported_atrs), (MultiIndexType,
        multi_index_unsupported_atrs), (DatetimeIndexType,
        dt_index_unsupported_atrs), (TimedeltaIndexType,
        td_index_unsupported_atrs), (PeriodIndexType,
        period_index_unsupported_atrs)]
    gaw__nqed = [(CategoricalIndexType, cat_idx_unsupported_methods), (
        IntervalIndexType, interval_idx_unsupported_methods), (
        MultiIndexType, multi_index_unsupported_methods), (
        DatetimeIndexType, dt_index_unsupported_methods), (
        TimedeltaIndexType, td_index_unsupported_methods), (PeriodIndexType,
        period_index_unsupported_methods)]
    for typ, fpgi__plkbm in gaw__nqed:
        birj__fpyr = idx_typ_to_format_str_map[typ]
        for hmsil__ryd in fpgi__plkbm:
            overload_method(typ, hmsil__ryd, no_unliteral=True)(
                create_unsupported_overload(birj__fpyr.format(hmsil__ryd +
                '()')))
    for typ, cbwz__ifc in axluc__odn:
        birj__fpyr = idx_typ_to_format_str_map[typ]
        for ujl__zvc in cbwz__ifc:
            overload_attribute(typ, ujl__zvc, no_unliteral=True)(
                create_unsupported_overload(birj__fpyr.format(ujl__zvc)))
    for rjad__zav in [RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, MultiIndexType]:
        for hmsil__ryd in ['max', 'min']:
            birj__fpyr = idx_typ_to_format_str_map[rjad__zav]
            overload_method(rjad__zav, hmsil__ryd, no_unliteral=True)(
                create_unsupported_overload(birj__fpyr.format(hmsil__ryd +
                '()')))


_install_index_unsupported()
