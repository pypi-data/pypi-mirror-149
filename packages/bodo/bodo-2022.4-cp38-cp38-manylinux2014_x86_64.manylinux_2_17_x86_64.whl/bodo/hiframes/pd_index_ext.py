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
            heckm__dvc = val.dtype.numpy_dtype
            dtype = numba.np.numpy_support.from_dtype(heckm__dvc)
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
        ohqcx__locy = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(_dt_index_data_typ.dtype, types.int64))]
        super(DatetimeIndexModel, self).__init__(dmm, fe_type, ohqcx__locy)


make_attribute_wrapper(DatetimeIndexType, 'data', '_data')
make_attribute_wrapper(DatetimeIndexType, 'name', '_name')
make_attribute_wrapper(DatetimeIndexType, 'dict', '_dict')


@overload_method(DatetimeIndexType, 'copy', no_unliteral=True)
def overload_datetime_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    dfsq__wmp = dict(deep=deep, dtype=dtype, names=names)
    oidgs__kyaw = idx_typ_to_format_str_map[DatetimeIndexType].format('copy()')
    check_unsupported_args('copy', dfsq__wmp, idx_cpy_arg_defaults, fn_str=
        oidgs__kyaw, package_name='pandas', module_name='Index')
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
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iany__hfb = c.pyapi.import_module_noblock(doth__bclib)
    kbabu__iijw = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, kbabu__iijw.data)
    ifhoh__klgo = c.pyapi.from_native_value(typ.data, kbabu__iijw.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, kbabu__iijw.name)
    wnqn__sjki = c.pyapi.from_native_value(typ.name_typ, kbabu__iijw.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([ifhoh__klgo])
    jomss__hwehy = c.pyapi.object_getattr_string(iany__hfb, 'DatetimeIndex')
    kws = c.pyapi.dict_pack([('name', wnqn__sjki)])
    bwop__off = c.pyapi.call(jomss__hwehy, args, kws)
    c.pyapi.decref(ifhoh__klgo)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(iany__hfb)
    c.pyapi.decref(jomss__hwehy)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return bwop__off


@unbox(DatetimeIndexType)
def unbox_datetime_index(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        ymci__lfzdr = c.pyapi.object_getattr_string(val, 'array')
    else:
        ymci__lfzdr = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, ymci__lfzdr).value
    wnqn__sjki = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, wnqn__sjki).value
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mpgqx__rmn.data = data
    mpgqx__rmn.name = name
    dtype = _dt_index_data_typ.dtype
    qic__ubya, yasu__mrj = c.pyapi.call_jit_code(lambda : numba.typed.Dict.
        empty(dtype, types.int64), types.DictType(dtype, types.int64)(), [])
    mpgqx__rmn.dict = yasu__mrj
    c.pyapi.decref(ymci__lfzdr)
    c.pyapi.decref(wnqn__sjki)
    return NativeValue(mpgqx__rmn._getvalue())


@intrinsic
def init_datetime_index(typingctx, data, name):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        ciku__sdf, amhzd__rvh = args
        kbabu__iijw = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        kbabu__iijw.data = ciku__sdf
        kbabu__iijw.name = amhzd__rvh
        context.nrt.incref(builder, signature.args[0], ciku__sdf)
        context.nrt.incref(builder, signature.args[1], amhzd__rvh)
        dtype = _dt_index_data_typ.dtype
        kbabu__iijw.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return kbabu__iijw._getvalue()
    vcumj__gtyz = DatetimeIndexType(name, data)
    sig = signature(vcumj__gtyz, data, name)
    return sig, codegen


def init_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) >= 1 and not kws
    ahk__yxgk = args[0]
    if equiv_set.has_shape(ahk__yxgk):
        return ArrayAnalysis.AnalyzeResult(shape=ahk__yxgk, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_datetime_index
    ) = init_index_equiv


def gen_dti_field_impl(field):
    fehg__xwa = 'def impl(dti):\n'
    fehg__xwa += '    numba.parfors.parfor.init_prange()\n'
    fehg__xwa += '    A = bodo.hiframes.pd_index_ext.get_index_data(dti)\n'
    fehg__xwa += '    name = bodo.hiframes.pd_index_ext.get_index_name(dti)\n'
    fehg__xwa += '    n = len(A)\n'
    fehg__xwa += '    S = np.empty(n, np.int64)\n'
    fehg__xwa += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    fehg__xwa += '        val = A[i]\n'
    fehg__xwa += '        ts = bodo.utils.conversion.box_if_dt64(val)\n'
    if field in ['weekday']:
        fehg__xwa += '        S[i] = ts.' + field + '()\n'
    else:
        fehg__xwa += '        S[i] = ts.' + field + '\n'
    fehg__xwa += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    man__pms = {}
    exec(fehg__xwa, {'numba': numba, 'np': np, 'bodo': bodo}, man__pms)
    impl = man__pms['impl']
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
        sdl__nwy = len(A)
        S = np.empty(sdl__nwy, np.bool_)
        for i in numba.parfors.parfor.internal_prange(sdl__nwy):
            val = A[i]
            lvxv__yzsw = bodo.utils.conversion.box_if_dt64(val)
            S[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(lvxv__yzsw.year)
        return S
    return impl


@overload_attribute(DatetimeIndexType, 'date')
def overload_datetime_index_date(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        sdl__nwy = len(A)
        S = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(sdl__nwy)
        for i in numba.parfors.parfor.internal_prange(sdl__nwy):
            val = A[i]
            lvxv__yzsw = bodo.utils.conversion.box_if_dt64(val)
            S[i] = datetime.date(lvxv__yzsw.year, lvxv__yzsw.month,
                lvxv__yzsw.day)
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
    qehci__iyf = dict(axis=axis, skipna=skipna)
    dpmm__hxxja = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.min', qehci__iyf, dpmm__hxxja,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.min()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        rqbu__yier = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_max_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(rqbu__yier)):
            if not bodo.libs.array_kernels.isna(rqbu__yier, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(rqbu__yier
                    [i])
                s = min(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'max', no_unliteral=True)
def overload_datetime_index_max(dti, axis=None, skipna=True):
    qehci__iyf = dict(axis=axis, skipna=skipna)
    dpmm__hxxja = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.max', qehci__iyf, dpmm__hxxja,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.max()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        rqbu__yier = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(rqbu__yier)):
            if not bodo.libs.array_kernels.isna(rqbu__yier, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(rqbu__yier
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
    qehci__iyf = dict(freq=freq, tz=tz, normalize=normalize, closed=closed,
        ambiguous=ambiguous, dayfirst=dayfirst, yearfirst=yearfirst, dtype=
        dtype, copy=copy)
    dpmm__hxxja = dict(freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False)
    check_unsupported_args('pandas.DatetimeIndex', qehci__iyf, dpmm__hxxja,
        package_name='pandas', module_name='Index')

    def f(data=None, freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False, name=None):
        jmnpg__rem = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_dt64ns(jmnpg__rem)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


def overload_sub_operator_datetime_index(lhs, rhs):
    if isinstance(lhs, DatetimeIndexType
        ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        plb__wlq = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            rqbu__yier = bodo.hiframes.pd_index_ext.get_index_data(lhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(lhs)
            sdl__nwy = len(rqbu__yier)
            S = np.empty(sdl__nwy, plb__wlq)
            oriz__krwzy = rhs.value
            for i in numba.parfors.parfor.internal_prange(sdl__nwy):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    rqbu__yier[i]) - oriz__krwzy)
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl
    if isinstance(rhs, DatetimeIndexType
        ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        plb__wlq = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            rqbu__yier = bodo.hiframes.pd_index_ext.get_index_data(rhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(rhs)
            sdl__nwy = len(rqbu__yier)
            S = np.empty(sdl__nwy, plb__wlq)
            oriz__krwzy = lhs.value
            for i in numba.parfors.parfor.internal_prange(sdl__nwy):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    oriz__krwzy - bodo.hiframes.pd_timestamp_ext.
                    dt64_to_integer(rqbu__yier[i]))
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl


def gen_dti_str_binop_impl(op, is_lhs_dti):
    dkr__jgre = numba.core.utils.OPERATORS_TO_BUILTINS[op]
    fehg__xwa = 'def impl(lhs, rhs):\n'
    if is_lhs_dti:
        fehg__xwa += '  dt_index, _str = lhs, rhs\n'
        dabk__fmqf = 'arr[i] {} other'.format(dkr__jgre)
    else:
        fehg__xwa += '  dt_index, _str = rhs, lhs\n'
        dabk__fmqf = 'other {} arr[i]'.format(dkr__jgre)
    fehg__xwa += (
        '  arr = bodo.hiframes.pd_index_ext.get_index_data(dt_index)\n')
    fehg__xwa += '  l = len(arr)\n'
    fehg__xwa += (
        '  other = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(_str)\n')
    fehg__xwa += '  S = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    fehg__xwa += '  for i in numba.parfors.parfor.internal_prange(l):\n'
    fehg__xwa += '    S[i] = {}\n'.format(dabk__fmqf)
    fehg__xwa += '  return S\n'
    man__pms = {}
    exec(fehg__xwa, {'bodo': bodo, 'numba': numba, 'np': np}, man__pms)
    impl = man__pms['impl']
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
    cpsvq__fvveq = getattr(data, 'dtype', None)
    if not is_overload_none(dtype):
        rmu__xmjs = parse_dtype(dtype, 'pandas.Index')
    else:
        rmu__xmjs = cpsvq__fvveq
    if isinstance(rmu__xmjs, types.misc.PyObject):
        raise BodoError(
            "pd.Index() object 'dtype' is not specific enough for typing. Please provide a more exact type (e.g. str)."
            )
    if isinstance(data, RangeIndexType):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.RangeIndex(data, name=name)
    elif isinstance(data, DatetimeIndexType) or rmu__xmjs == types.NPDatetime(
        'ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.DatetimeIndex(data, name=name)
    elif isinstance(data, TimedeltaIndexType
        ) or rmu__xmjs == types.NPTimedelta('ns'):

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
        if isinstance(rmu__xmjs, (types.Integer, types.Float, types.Boolean)):

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                jmnpg__rem = bodo.utils.conversion.coerce_to_array(data)
                wci__aihdr = bodo.utils.conversion.fix_arr_dtype(jmnpg__rem,
                    rmu__xmjs)
                return bodo.hiframes.pd_index_ext.init_numeric_index(wci__aihdr
                    , name)
        elif rmu__xmjs in [types.string, bytes_type]:

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
                gqir__qaxhy = bodo.hiframes.pd_index_ext.get_index_data(dti)
                val = gqir__qaxhy[ind]
                return bodo.utils.conversion.box_if_dt64(val)
            return impl
        else:

            def impl(dti, ind):
                gqir__qaxhy = bodo.hiframes.pd_index_ext.get_index_data(dti)
                name = bodo.hiframes.pd_index_ext.get_index_name(dti)
                kvb__nsxy = gqir__qaxhy[ind]
                return bodo.hiframes.pd_index_ext.init_datetime_index(kvb__nsxy
                    , name)
            return impl


@overload(operator.getitem, no_unliteral=True)
def overload_timedelta_index_getitem(I, ind):
    if not isinstance(I, TimedeltaIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            mbeyq__oab = bodo.hiframes.pd_index_ext.get_index_data(I)
            return pd.Timedelta(mbeyq__oab[ind])
        return impl

    def impl(I, ind):
        mbeyq__oab = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        kvb__nsxy = mbeyq__oab[ind]
        return bodo.hiframes.pd_index_ext.init_timedelta_index(kvb__nsxy, name)
    return impl


@numba.njit(no_cpython_wrapper=True)
def validate_endpoints(closed):
    ymimd__myxg = False
    jlml__qwjr = False
    if closed is None:
        ymimd__myxg = True
        jlml__qwjr = True
    elif closed == 'left':
        ymimd__myxg = True
    elif closed == 'right':
        jlml__qwjr = True
    else:
        raise ValueError("Closed has to be either 'left', 'right' or None")
    return ymimd__myxg, jlml__qwjr


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
    qehci__iyf = dict(tz=tz, normalize=normalize, closed=closed)
    dpmm__hxxja = dict(tz=None, normalize=False, closed=None)
    check_unsupported_args('pandas.date_range', qehci__iyf, dpmm__hxxja,
        package_name='pandas', module_name='General')
    if not is_overload_none(tz):
        raise_bodo_error('pd.date_range(): tz argument not supported yet')
    houh__esi = ''
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
        houh__esi = "  freq = 'D'\n"
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise_bodo_error(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )
    fehg__xwa = """def f(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None):
"""
    fehg__xwa += houh__esi
    if is_overload_none(start):
        fehg__xwa += "  start_t = pd.Timestamp('1800-01-03')\n"
    else:
        fehg__xwa += '  start_t = pd.Timestamp(start)\n'
    if is_overload_none(end):
        fehg__xwa += "  end_t = pd.Timestamp('1800-01-03')\n"
    else:
        fehg__xwa += '  end_t = pd.Timestamp(end)\n'
    if not is_overload_none(freq):
        fehg__xwa += (
            '  stride = bodo.hiframes.pd_index_ext.to_offset_value(freq)\n')
        if is_overload_none(periods):
            fehg__xwa += '  b = start_t.value\n'
            fehg__xwa += (
                '  e = b + (end_t.value - b) // stride * stride + stride // 2 + 1\n'
                )
        elif not is_overload_none(start):
            fehg__xwa += '  b = start_t.value\n'
            fehg__xwa += '  addend = np.int64(periods) * np.int64(stride)\n'
            fehg__xwa += '  e = np.int64(b) + addend\n'
        elif not is_overload_none(end):
            fehg__xwa += '  e = end_t.value + stride\n'
            fehg__xwa += '  addend = np.int64(periods) * np.int64(-stride)\n'
            fehg__xwa += '  b = np.int64(e) + addend\n'
        else:
            raise_bodo_error(
                "at least 'start' or 'end' should be specified if a 'period' is given."
                )
        fehg__xwa += '  arr = np.arange(b, e, stride, np.int64)\n'
    else:
        fehg__xwa += '  delta = end_t.value - start_t.value\n'
        fehg__xwa += '  step = delta / (periods - 1)\n'
        fehg__xwa += '  arr1 = np.arange(0, periods, 1, np.float64)\n'
        fehg__xwa += '  arr1 *= step\n'
        fehg__xwa += '  arr1 += start_t.value\n'
        fehg__xwa += '  arr = arr1.astype(np.int64)\n'
        fehg__xwa += '  arr[-1] = end_t.value\n'
    fehg__xwa += '  A = bodo.utils.conversion.convert_to_dt64ns(arr)\n'
    fehg__xwa += (
        '  return bodo.hiframes.pd_index_ext.init_datetime_index(A, name)\n')
    man__pms = {}
    exec(fehg__xwa, {'bodo': bodo, 'np': np, 'pd': pd}, man__pms)
    f = man__pms['f']
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
        joav__ewj = pd.Timedelta('1 day')
        if start is not None:
            joav__ewj = pd.Timedelta(start)
        hvhu__ejr = pd.Timedelta('1 day')
        if end is not None:
            hvhu__ejr = pd.Timedelta(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of start and end are defined'
                )
        ymimd__myxg, jlml__qwjr = (bodo.hiframes.pd_index_ext.
            validate_endpoints(closed))
        if freq is not None:
            wvfh__sufa = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = joav__ewj.value
                kldug__ebki = b + (hvhu__ejr.value - b
                    ) // wvfh__sufa * wvfh__sufa + wvfh__sufa // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = joav__ewj.value
                laj__odg = np.int64(periods) * np.int64(wvfh__sufa)
                kldug__ebki = np.int64(b) + laj__odg
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                kldug__ebki = hvhu__ejr.value + wvfh__sufa
                laj__odg = np.int64(periods) * np.int64(-wvfh__sufa)
                b = np.int64(kldug__ebki) + laj__odg
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            gxs__qkir = np.arange(b, kldug__ebki, wvfh__sufa, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            nuk__lhjc = hvhu__ejr.value - joav__ewj.value
            step = nuk__lhjc / (periods - 1)
            dfpsg__fptk = np.arange(0, periods, 1, np.float64)
            dfpsg__fptk *= step
            dfpsg__fptk += joav__ewj.value
            gxs__qkir = dfpsg__fptk.astype(np.int64)
            gxs__qkir[-1] = hvhu__ejr.value
        if not ymimd__myxg and len(gxs__qkir) and gxs__qkir[0
            ] == joav__ewj.value:
            gxs__qkir = gxs__qkir[1:]
        if not jlml__qwjr and len(gxs__qkir) and gxs__qkir[-1
            ] == hvhu__ejr.value:
            gxs__qkir = gxs__qkir[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(gxs__qkir)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return f


@overload_method(DatetimeIndexType, 'isocalendar', inline='always',
    no_unliteral=True)
def overload_pd_timestamp_isocalendar(idx):

    def impl(idx):
        A = bodo.hiframes.pd_index_ext.get_index_data(idx)
        numba.parfors.parfor.init_prange()
        sdl__nwy = len(A)
        wklj__cft = bodo.libs.int_arr_ext.alloc_int_array(sdl__nwy, np.uint32)
        xfms__gjgg = bodo.libs.int_arr_ext.alloc_int_array(sdl__nwy, np.uint32)
        qozml__ispwd = bodo.libs.int_arr_ext.alloc_int_array(sdl__nwy, np.
            uint32)
        for i in numba.parfors.parfor.internal_prange(sdl__nwy):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(wklj__cft, i)
                bodo.libs.array_kernels.setna(xfms__gjgg, i)
                bodo.libs.array_kernels.setna(qozml__ispwd, i)
                continue
            wklj__cft[i], xfms__gjgg[i], qozml__ispwd[i
                ] = bodo.utils.conversion.box_if_dt64(A[i]).isocalendar()
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((wklj__cft,
            xfms__gjgg, qozml__ispwd), idx, ('year', 'week', 'day'))
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
        ohqcx__locy = [('data', _timedelta_index_data_typ), ('name',
            fe_type.name_typ), ('dict', types.DictType(
            _timedelta_index_data_typ.dtype, types.int64))]
        super(TimedeltaIndexTypeModel, self).__init__(dmm, fe_type, ohqcx__locy
            )


@typeof_impl.register(pd.TimedeltaIndex)
def typeof_timedelta_index(val, c):
    return TimedeltaIndexType(get_val_type_maybe_str_literal(val.name))


@box(TimedeltaIndexType)
def box_timedelta_index(typ, val, c):
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iany__hfb = c.pyapi.import_module_noblock(doth__bclib)
    timedelta_index = numba.core.cgutils.create_struct_proxy(typ)(c.context,
        c.builder, val)
    c.context.nrt.incref(c.builder, _timedelta_index_data_typ,
        timedelta_index.data)
    ifhoh__klgo = c.pyapi.from_native_value(_timedelta_index_data_typ,
        timedelta_index.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, timedelta_index.name)
    wnqn__sjki = c.pyapi.from_native_value(typ.name_typ, timedelta_index.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([ifhoh__klgo])
    kws = c.pyapi.dict_pack([('name', wnqn__sjki)])
    jomss__hwehy = c.pyapi.object_getattr_string(iany__hfb, 'TimedeltaIndex')
    bwop__off = c.pyapi.call(jomss__hwehy, args, kws)
    c.pyapi.decref(ifhoh__klgo)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(iany__hfb)
    c.pyapi.decref(jomss__hwehy)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return bwop__off


@unbox(TimedeltaIndexType)
def unbox_timedelta_index(typ, val, c):
    skk__xsrgs = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_timedelta_index_data_typ, skk__xsrgs).value
    wnqn__sjki = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, wnqn__sjki).value
    c.pyapi.decref(skk__xsrgs)
    c.pyapi.decref(wnqn__sjki)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mpgqx__rmn.data = data
    mpgqx__rmn.name = name
    dtype = _timedelta_index_data_typ.dtype
    qic__ubya, yasu__mrj = c.pyapi.call_jit_code(lambda : numba.typed.Dict.
        empty(dtype, types.int64), types.DictType(dtype, types.int64)(), [])
    mpgqx__rmn.dict = yasu__mrj
    return NativeValue(mpgqx__rmn._getvalue())


@intrinsic
def init_timedelta_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        ciku__sdf, amhzd__rvh = args
        timedelta_index = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        timedelta_index.data = ciku__sdf
        timedelta_index.name = amhzd__rvh
        context.nrt.incref(builder, signature.args[0], ciku__sdf)
        context.nrt.incref(builder, signature.args[1], amhzd__rvh)
        dtype = _timedelta_index_data_typ.dtype
        timedelta_index.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return timedelta_index._getvalue()
    vcumj__gtyz = TimedeltaIndexType(name)
    sig = signature(vcumj__gtyz, data, name)
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
    dfsq__wmp = dict(deep=deep, dtype=dtype, names=names)
    oidgs__kyaw = idx_typ_to_format_str_map[TimedeltaIndexType].format('copy()'
        )
    check_unsupported_args('TimedeltaIndex.copy', dfsq__wmp,
        idx_cpy_arg_defaults, fn_str=oidgs__kyaw, package_name='pandas',
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
    qehci__iyf = dict(axis=axis, skipna=skipna)
    dpmm__hxxja = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.min', qehci__iyf, dpmm__hxxja,
        package_name='pandas', module_name='Index')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        sdl__nwy = len(data)
        fptj__jtpo = numba.cpython.builtins.get_type_max_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(sdl__nwy):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            fptj__jtpo = min(fptj__jtpo, val)
        sid__tbs = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            fptj__jtpo)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(sid__tbs, count)
    return impl


@overload_method(TimedeltaIndexType, 'max', inline='always', no_unliteral=True)
def overload_timedelta_index_max(tdi, axis=None, skipna=True):
    qehci__iyf = dict(axis=axis, skipna=skipna)
    dpmm__hxxja = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.max', qehci__iyf, dpmm__hxxja,
        package_name='pandas', module_name='Index')
    if not is_overload_none(axis) or not is_overload_true(skipna):
        raise BodoError(
            'Index.min(): axis and skipna arguments not supported yet')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        sdl__nwy = len(data)
        ufqu__spkjh = numba.cpython.builtins.get_type_min_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(sdl__nwy):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            ufqu__spkjh = max(ufqu__spkjh, val)
        sid__tbs = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            ufqu__spkjh)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(sid__tbs, count)
    return impl


def gen_tdi_field_impl(field):
    fehg__xwa = 'def impl(tdi):\n'
    fehg__xwa += '    numba.parfors.parfor.init_prange()\n'
    fehg__xwa += '    A = bodo.hiframes.pd_index_ext.get_index_data(tdi)\n'
    fehg__xwa += '    name = bodo.hiframes.pd_index_ext.get_index_name(tdi)\n'
    fehg__xwa += '    n = len(A)\n'
    fehg__xwa += '    S = np.empty(n, np.int64)\n'
    fehg__xwa += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    fehg__xwa += (
        '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
        )
    if field == 'nanoseconds':
        fehg__xwa += '        S[i] = td64 % 1000\n'
    elif field == 'microseconds':
        fehg__xwa += '        S[i] = td64 // 1000 % 100000\n'
    elif field == 'seconds':
        fehg__xwa += (
            '        S[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
    elif field == 'days':
        fehg__xwa += '        S[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n'
    else:
        assert False, 'invalid timedelta field'
    fehg__xwa += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    man__pms = {}
    exec(fehg__xwa, {'numba': numba, 'np': np, 'bodo': bodo}, man__pms)
    impl = man__pms['impl']
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
    qehci__iyf = dict(unit=unit, freq=freq, dtype=dtype, copy=copy)
    dpmm__hxxja = dict(unit=None, freq=None, dtype=None, copy=False)
    check_unsupported_args('pandas.TimedeltaIndex', qehci__iyf, dpmm__hxxja,
        package_name='pandas', module_name='Index')

    def impl(data=None, unit=None, freq=None, dtype=None, copy=False, name=None
        ):
        jmnpg__rem = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_td64ns(jmnpg__rem)
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
        ohqcx__locy = [('start', types.int64), ('stop', types.int64), (
            'step', types.int64), ('name', fe_type.name_typ)]
        super(RangeIndexModel, self).__init__(dmm, fe_type, ohqcx__locy)


make_attribute_wrapper(RangeIndexType, 'start', '_start')
make_attribute_wrapper(RangeIndexType, 'stop', '_stop')
make_attribute_wrapper(RangeIndexType, 'step', '_step')
make_attribute_wrapper(RangeIndexType, 'name', '_name')


@overload_method(RangeIndexType, 'copy', no_unliteral=True)
def overload_range_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    dfsq__wmp = dict(deep=deep, dtype=dtype, names=names)
    oidgs__kyaw = idx_typ_to_format_str_map[RangeIndexType].format('copy()')
    check_unsupported_args('RangeIndex.copy', dfsq__wmp,
        idx_cpy_arg_defaults, fn_str=oidgs__kyaw, package_name='pandas',
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
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iwgp__bqgj = c.pyapi.import_module_noblock(doth__bclib)
    gtcqu__oxpq = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    nrhrw__ghavq = c.pyapi.from_native_value(types.int64, gtcqu__oxpq.start,
        c.env_manager)
    jwm__rsqda = c.pyapi.from_native_value(types.int64, gtcqu__oxpq.stop, c
        .env_manager)
    tlqm__mlmw = c.pyapi.from_native_value(types.int64, gtcqu__oxpq.step, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, gtcqu__oxpq.name)
    wnqn__sjki = c.pyapi.from_native_value(typ.name_typ, gtcqu__oxpq.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([nrhrw__ghavq, jwm__rsqda, tlqm__mlmw])
    kws = c.pyapi.dict_pack([('name', wnqn__sjki)])
    jomss__hwehy = c.pyapi.object_getattr_string(iwgp__bqgj, 'RangeIndex')
    jpw__jaaf = c.pyapi.call(jomss__hwehy, args, kws)
    c.pyapi.decref(nrhrw__ghavq)
    c.pyapi.decref(jwm__rsqda)
    c.pyapi.decref(tlqm__mlmw)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(iwgp__bqgj)
    c.pyapi.decref(jomss__hwehy)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return jpw__jaaf


@intrinsic
def init_range_index(typingctx, start, stop, step, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 4
        gtcqu__oxpq = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        gtcqu__oxpq.start = args[0]
        gtcqu__oxpq.stop = args[1]
        gtcqu__oxpq.step = args[2]
        gtcqu__oxpq.name = args[3]
        context.nrt.incref(builder, signature.return_type.name_typ, args[3])
        return gtcqu__oxpq._getvalue()
    return RangeIndexType(name)(start, stop, step, name), codegen


def init_range_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    start, stop, step, psfzh__vebdl = args
    if self.typemap[start.name] == types.IntegerLiteral(0) and self.typemap[
        step.name] == types.IntegerLiteral(1) and equiv_set.has_shape(stop):
        return ArrayAnalysis.AnalyzeResult(shape=stop, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_range_index
    ) = init_range_index_equiv


@unbox(RangeIndexType)
def unbox_range_index(typ, val, c):
    nrhrw__ghavq = c.pyapi.object_getattr_string(val, 'start')
    start = c.pyapi.to_native_value(types.int64, nrhrw__ghavq).value
    jwm__rsqda = c.pyapi.object_getattr_string(val, 'stop')
    stop = c.pyapi.to_native_value(types.int64, jwm__rsqda).value
    tlqm__mlmw = c.pyapi.object_getattr_string(val, 'step')
    step = c.pyapi.to_native_value(types.int64, tlqm__mlmw).value
    wnqn__sjki = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, wnqn__sjki).value
    c.pyapi.decref(nrhrw__ghavq)
    c.pyapi.decref(jwm__rsqda)
    c.pyapi.decref(tlqm__mlmw)
    c.pyapi.decref(wnqn__sjki)
    gtcqu__oxpq = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gtcqu__oxpq.start = start
    gtcqu__oxpq.stop = stop
    gtcqu__oxpq.step = step
    gtcqu__oxpq.name = name
    return NativeValue(gtcqu__oxpq._getvalue())


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
        bvyht__zkxi = (
            'RangeIndex(...) must be called with integers, {value} was passed for {field}'
            )
        if not is_overload_none(value) and not isinstance(value, types.
            IntegerLiteral) and not isinstance(value, types.Integer):
            raise BodoError(bvyht__zkxi.format(value=value, field=field))
    _ensure_int_or_none(start, 'start')
    _ensure_int_or_none(stop, 'stop')
    _ensure_int_or_none(step, 'step')
    if is_overload_none(start) and is_overload_none(stop) and is_overload_none(
        step):
        bvyht__zkxi = 'RangeIndex(...) must be called with integers'
        raise BodoError(bvyht__zkxi)
    ydir__wtd = 'start'
    unpqq__kgp = 'stop'
    vpn__zak = 'step'
    if is_overload_none(start):
        ydir__wtd = '0'
    if is_overload_none(stop):
        unpqq__kgp = 'start'
        ydir__wtd = '0'
    if is_overload_none(step):
        vpn__zak = '1'
    fehg__xwa = """def _pd_range_index_imp(start=None, stop=None, step=None, dtype=None, copy=False, name=None):
"""
    fehg__xwa += '  return init_range_index({}, {}, {}, name)\n'.format(
        ydir__wtd, unpqq__kgp, vpn__zak)
    man__pms = {}
    exec(fehg__xwa, {'init_range_index': init_range_index}, man__pms)
    zqo__qon = man__pms['_pd_range_index_imp']
    return zqo__qon


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
                qwxu__elrf = numba.cpython.unicode._normalize_slice(idx, len(I)
                    )
                name = bodo.hiframes.pd_index_ext.get_index_name(I)
                start = I._start + I._step * qwxu__elrf.start
                stop = I._start + I._step * qwxu__elrf.stop
                step = I._step * qwxu__elrf.step
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
        ohqcx__locy = [('data', bodo.IntegerArrayType(types.int64)), (
            'name', fe_type.name_typ), ('dict', types.DictType(types.int64,
            types.int64))]
        super(PeriodIndexModel, self).__init__(dmm, fe_type, ohqcx__locy)


make_attribute_wrapper(PeriodIndexType, 'data', '_data')
make_attribute_wrapper(PeriodIndexType, 'name', '_name')
make_attribute_wrapper(PeriodIndexType, 'dict', '_dict')


@overload_method(PeriodIndexType, 'copy', no_unliteral=True)
def overload_period_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    freq = A.freq
    dfsq__wmp = dict(deep=deep, dtype=dtype, names=names)
    oidgs__kyaw = idx_typ_to_format_str_map[PeriodIndexType].format('copy()')
    check_unsupported_args('PeriodIndex.copy', dfsq__wmp,
        idx_cpy_arg_defaults, fn_str=oidgs__kyaw, package_name='pandas',
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
        ciku__sdf, amhzd__rvh, psfzh__vebdl = args
        lxtp__lkew = signature.return_type
        mlive__ogt = cgutils.create_struct_proxy(lxtp__lkew)(context, builder)
        mlive__ogt.data = ciku__sdf
        mlive__ogt.name = amhzd__rvh
        context.nrt.incref(builder, signature.args[0], args[0])
        context.nrt.incref(builder, signature.args[1], args[1])
        mlive__ogt.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(types.int64, types.int64), types.DictType(
            types.int64, types.int64)(), [])
        return mlive__ogt._getvalue()
    zvo__eup = get_overload_const_str(freq)
    vcumj__gtyz = PeriodIndexType(zvo__eup, name)
    sig = signature(vcumj__gtyz, data, name, freq)
    return sig, codegen


@box(PeriodIndexType)
def box_period_index(typ, val, c):
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iwgp__bqgj = c.pyapi.import_module_noblock(doth__bclib)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, bodo.IntegerArrayType(types.int64),
        mpgqx__rmn.data)
    ymci__lfzdr = c.pyapi.from_native_value(bodo.IntegerArrayType(types.
        int64), mpgqx__rmn.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, mpgqx__rmn.name)
    wnqn__sjki = c.pyapi.from_native_value(typ.name_typ, mpgqx__rmn.name, c
        .env_manager)
    tsryb__xgrej = c.pyapi.string_from_constant_string(typ.freq)
    args = c.pyapi.tuple_pack([])
    kws = c.pyapi.dict_pack([('ordinal', ymci__lfzdr), ('name', wnqn__sjki),
        ('freq', tsryb__xgrej)])
    jomss__hwehy = c.pyapi.object_getattr_string(iwgp__bqgj, 'PeriodIndex')
    jpw__jaaf = c.pyapi.call(jomss__hwehy, args, kws)
    c.pyapi.decref(ymci__lfzdr)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(tsryb__xgrej)
    c.pyapi.decref(iwgp__bqgj)
    c.pyapi.decref(jomss__hwehy)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return jpw__jaaf


@unbox(PeriodIndexType)
def unbox_period_index(typ, val, c):
    arr_typ = bodo.IntegerArrayType(types.int64)
    ujj__ezbdn = c.pyapi.object_getattr_string(val, 'asi8')
    xvh__mup = c.pyapi.call_method(val, 'isna', ())
    wnqn__sjki = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, wnqn__sjki).value
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iany__hfb = c.pyapi.import_module_noblock(doth__bclib)
    kgaix__ornby = c.pyapi.object_getattr_string(iany__hfb, 'arrays')
    ymci__lfzdr = c.pyapi.call_method(kgaix__ornby, 'IntegerArray', (
        ujj__ezbdn, xvh__mup))
    data = c.pyapi.to_native_value(arr_typ, ymci__lfzdr).value
    c.pyapi.decref(ujj__ezbdn)
    c.pyapi.decref(xvh__mup)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(iany__hfb)
    c.pyapi.decref(kgaix__ornby)
    c.pyapi.decref(ymci__lfzdr)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mpgqx__rmn.data = data
    mpgqx__rmn.name = name
    qic__ubya, yasu__mrj = c.pyapi.call_jit_code(lambda : numba.typed.Dict.
        empty(types.int64, types.int64), types.DictType(types.int64, types.
        int64)(), [])
    mpgqx__rmn.dict = yasu__mrj
    return NativeValue(mpgqx__rmn._getvalue())


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
        vmiwb__mgo = get_categories_int_type(fe_type.data.dtype)
        ohqcx__locy = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(vmiwb__mgo, types.int64))]
        super(CategoricalIndexTypeModel, self).__init__(dmm, fe_type,
            ohqcx__locy)


@typeof_impl.register(pd.CategoricalIndex)
def typeof_categorical_index(val, c):
    return CategoricalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(CategoricalIndexType)
def box_categorical_index(typ, val, c):
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iany__hfb = c.pyapi.import_module_noblock(doth__bclib)
    owc__eum = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, owc__eum.data)
    ifhoh__klgo = c.pyapi.from_native_value(typ.data, owc__eum.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, owc__eum.name)
    wnqn__sjki = c.pyapi.from_native_value(typ.name_typ, owc__eum.name, c.
        env_manager)
    args = c.pyapi.tuple_pack([ifhoh__klgo])
    kws = c.pyapi.dict_pack([('name', wnqn__sjki)])
    jomss__hwehy = c.pyapi.object_getattr_string(iany__hfb, 'CategoricalIndex')
    bwop__off = c.pyapi.call(jomss__hwehy, args, kws)
    c.pyapi.decref(ifhoh__klgo)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(iany__hfb)
    c.pyapi.decref(jomss__hwehy)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return bwop__off


@unbox(CategoricalIndexType)
def unbox_categorical_index(typ, val, c):
    from bodo.hiframes.pd_categorical_ext import get_categories_int_type
    skk__xsrgs = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, skk__xsrgs).value
    wnqn__sjki = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, wnqn__sjki).value
    c.pyapi.decref(skk__xsrgs)
    c.pyapi.decref(wnqn__sjki)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mpgqx__rmn.data = data
    mpgqx__rmn.name = name
    dtype = get_categories_int_type(typ.data.dtype)
    qic__ubya, yasu__mrj = c.pyapi.call_jit_code(lambda : numba.typed.Dict.
        empty(dtype, types.int64), types.DictType(dtype, types.int64)(), [])
    mpgqx__rmn.dict = yasu__mrj
    return NativeValue(mpgqx__rmn._getvalue())


@intrinsic
def init_categorical_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        ciku__sdf, amhzd__rvh = args
        owc__eum = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        owc__eum.data = ciku__sdf
        owc__eum.name = amhzd__rvh
        context.nrt.incref(builder, signature.args[0], ciku__sdf)
        context.nrt.incref(builder, signature.args[1], amhzd__rvh)
        dtype = get_categories_int_type(signature.return_type.data.dtype)
        owc__eum.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return owc__eum._getvalue()
    vcumj__gtyz = CategoricalIndexType(data, name)
    sig = signature(vcumj__gtyz, data, name)
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
    oidgs__kyaw = idx_typ_to_format_str_map[CategoricalIndexType].format(
        'copy()')
    dfsq__wmp = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('CategoricalIndex.copy', dfsq__wmp,
        idx_cpy_arg_defaults, fn_str=oidgs__kyaw, package_name='pandas',
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
        ohqcx__locy = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(types.UniTuple(fe_type.data.arr_type.
            dtype, 2), types.int64))]
        super(IntervalIndexTypeModel, self).__init__(dmm, fe_type, ohqcx__locy)


@typeof_impl.register(pd.IntervalIndex)
def typeof_interval_index(val, c):
    return IntervalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(IntervalIndexType)
def box_interval_index(typ, val, c):
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iany__hfb = c.pyapi.import_module_noblock(doth__bclib)
    xxv__fct = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, xxv__fct.data)
    ifhoh__klgo = c.pyapi.from_native_value(typ.data, xxv__fct.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, xxv__fct.name)
    wnqn__sjki = c.pyapi.from_native_value(typ.name_typ, xxv__fct.name, c.
        env_manager)
    args = c.pyapi.tuple_pack([ifhoh__klgo])
    kws = c.pyapi.dict_pack([('name', wnqn__sjki)])
    jomss__hwehy = c.pyapi.object_getattr_string(iany__hfb, 'IntervalIndex')
    bwop__off = c.pyapi.call(jomss__hwehy, args, kws)
    c.pyapi.decref(ifhoh__klgo)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(iany__hfb)
    c.pyapi.decref(jomss__hwehy)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return bwop__off


@unbox(IntervalIndexType)
def unbox_interval_index(typ, val, c):
    skk__xsrgs = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, skk__xsrgs).value
    wnqn__sjki = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, wnqn__sjki).value
    c.pyapi.decref(skk__xsrgs)
    c.pyapi.decref(wnqn__sjki)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mpgqx__rmn.data = data
    mpgqx__rmn.name = name
    dtype = types.UniTuple(typ.data.arr_type.dtype, 2)
    qic__ubya, yasu__mrj = c.pyapi.call_jit_code(lambda : numba.typed.Dict.
        empty(dtype, types.int64), types.DictType(dtype, types.int64)(), [])
    mpgqx__rmn.dict = yasu__mrj
    return NativeValue(mpgqx__rmn._getvalue())


@intrinsic
def init_interval_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        ciku__sdf, amhzd__rvh = args
        xxv__fct = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        xxv__fct.data = ciku__sdf
        xxv__fct.name = amhzd__rvh
        context.nrt.incref(builder, signature.args[0], ciku__sdf)
        context.nrt.incref(builder, signature.args[1], amhzd__rvh)
        dtype = types.UniTuple(data.arr_type.dtype, 2)
        xxv__fct.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return xxv__fct._getvalue()
    vcumj__gtyz = IntervalIndexType(data, name)
    sig = signature(vcumj__gtyz, data, name)
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
        ohqcx__locy = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(fe_type.dtype, types.int64))]
        super(NumericIndexModel, self).__init__(dmm, fe_type, ohqcx__locy)


make_attribute_wrapper(NumericIndexType, 'data', '_data')
make_attribute_wrapper(NumericIndexType, 'name', '_name')
make_attribute_wrapper(NumericIndexType, 'dict', '_dict')


@overload_method(NumericIndexType, 'copy', no_unliteral=True)
def overload_numeric_index_copy(A, name=None, deep=False, dtype=None, names
    =None):
    oidgs__kyaw = idx_typ_to_format_str_map[NumericIndexType].format('copy()')
    dfsq__wmp = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', dfsq__wmp, idx_cpy_arg_defaults,
        fn_str=oidgs__kyaw, package_name='pandas', module_name='Index')
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
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iwgp__bqgj = c.pyapi.import_module_noblock(doth__bclib)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, mpgqx__rmn.data)
    ymci__lfzdr = c.pyapi.from_native_value(typ.data, mpgqx__rmn.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, mpgqx__rmn.name)
    wnqn__sjki = c.pyapi.from_native_value(typ.name_typ, mpgqx__rmn.name, c
        .env_manager)
    gcqi__gzx = c.pyapi.make_none()
    vppnb__xjsa = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    jpw__jaaf = c.pyapi.call_method(iwgp__bqgj, 'Index', (ymci__lfzdr,
        gcqi__gzx, vppnb__xjsa, wnqn__sjki))
    c.pyapi.decref(ymci__lfzdr)
    c.pyapi.decref(gcqi__gzx)
    c.pyapi.decref(vppnb__xjsa)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(iwgp__bqgj)
    c.context.nrt.decref(c.builder, typ, val)
    return jpw__jaaf


@intrinsic
def init_numeric_index(typingctx, data, name=None):
    name = types.none if is_overload_none(name) else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        lxtp__lkew = signature.return_type
        mpgqx__rmn = cgutils.create_struct_proxy(lxtp__lkew)(context, builder)
        mpgqx__rmn.data = args[0]
        mpgqx__rmn.name = args[1]
        context.nrt.incref(builder, lxtp__lkew.data, args[0])
        context.nrt.incref(builder, lxtp__lkew.name_typ, args[1])
        dtype = lxtp__lkew.dtype
        mpgqx__rmn.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return mpgqx__rmn._getvalue()
    return NumericIndexType(data.dtype, name, data)(data, name), codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_numeric_index
    ) = init_index_equiv


@unbox(NumericIndexType)
def unbox_numeric_index(typ, val, c):
    skk__xsrgs = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, skk__xsrgs).value
    wnqn__sjki = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, wnqn__sjki).value
    c.pyapi.decref(skk__xsrgs)
    c.pyapi.decref(wnqn__sjki)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mpgqx__rmn.data = data
    mpgqx__rmn.name = name
    dtype = typ.dtype
    qic__ubya, yasu__mrj = c.pyapi.call_jit_code(lambda : numba.typed.Dict.
        empty(dtype, types.int64), types.DictType(dtype, types.int64)(), [])
    mpgqx__rmn.dict = yasu__mrj
    return NativeValue(mpgqx__rmn._getvalue())


def create_numeric_constructor(func, func_str, default_dtype):

    def overload_impl(data=None, dtype=None, copy=False, name=None):
        tle__igcc = dict(dtype=dtype)
        loet__sdcz = dict(dtype=None)
        check_unsupported_args(func_str, tle__igcc, loet__sdcz,
            package_name='pandas', module_name='Index')
        if is_overload_false(copy):

            def impl(data=None, dtype=None, copy=False, name=None):
                jmnpg__rem = bodo.utils.conversion.coerce_to_ndarray(data)
                hcbd__yonrz = bodo.utils.conversion.fix_arr_dtype(jmnpg__rem,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(
                    hcbd__yonrz, name)
        else:

            def impl(data=None, dtype=None, copy=False, name=None):
                jmnpg__rem = bodo.utils.conversion.coerce_to_ndarray(data)
                if copy:
                    jmnpg__rem = jmnpg__rem.copy()
                hcbd__yonrz = bodo.utils.conversion.fix_arr_dtype(jmnpg__rem,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(
                    hcbd__yonrz, name)
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
        ohqcx__locy = [('data', fe_type.data), ('name', fe_type.name_typ),
            ('dict', types.DictType(string_type, types.int64))]
        super(StringIndexModel, self).__init__(dmm, fe_type, ohqcx__locy)


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
        ohqcx__locy = [('data', binary_array_type), ('name', fe_type.
            name_typ), ('dict', types.DictType(bytes_type, types.int64))]
        super(BinaryIndexModel, self).__init__(dmm, fe_type, ohqcx__locy)


make_attribute_wrapper(BinaryIndexType, 'data', '_data')
make_attribute_wrapper(BinaryIndexType, 'name', '_name')
make_attribute_wrapper(BinaryIndexType, 'dict', '_dict')


@unbox(BinaryIndexType)
@unbox(StringIndexType)
def unbox_binary_str_index(typ, val, c):
    tzj__ybj = typ.data
    scalar_type = typ.data.dtype
    skk__xsrgs = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(tzj__ybj, skk__xsrgs).value
    wnqn__sjki = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, wnqn__sjki).value
    c.pyapi.decref(skk__xsrgs)
    c.pyapi.decref(wnqn__sjki)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mpgqx__rmn.data = data
    mpgqx__rmn.name = name
    qic__ubya, yasu__mrj = c.pyapi.call_jit_code(lambda : numba.typed.Dict.
        empty(scalar_type, types.int64), types.DictType(scalar_type, types.
        int64)(), [])
    mpgqx__rmn.dict = yasu__mrj
    return NativeValue(mpgqx__rmn._getvalue())


@box(BinaryIndexType)
@box(StringIndexType)
def box_binary_str_index(typ, val, c):
    tzj__ybj = typ.data
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iwgp__bqgj = c.pyapi.import_module_noblock(doth__bclib)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, tzj__ybj, mpgqx__rmn.data)
    ymci__lfzdr = c.pyapi.from_native_value(tzj__ybj, mpgqx__rmn.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, mpgqx__rmn.name)
    wnqn__sjki = c.pyapi.from_native_value(typ.name_typ, mpgqx__rmn.name, c
        .env_manager)
    gcqi__gzx = c.pyapi.make_none()
    vppnb__xjsa = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    jpw__jaaf = c.pyapi.call_method(iwgp__bqgj, 'Index', (ymci__lfzdr,
        gcqi__gzx, vppnb__xjsa, wnqn__sjki))
    c.pyapi.decref(ymci__lfzdr)
    c.pyapi.decref(gcqi__gzx)
    c.pyapi.decref(vppnb__xjsa)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(iwgp__bqgj)
    c.context.nrt.decref(c.builder, typ, val)
    return jpw__jaaf


@intrinsic
def init_binary_str_index(typingctx, data, name=None):
    name = types.none if name is None else name
    sig = type(bodo.utils.typing.get_index_type_from_dtype(data.dtype))(name,
        data)(data, name)
    hnku__ldb = get_binary_str_codegen(is_binary=data.dtype == bytes_type)
    return sig, hnku__ldb


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_binary_str_index
    ) = init_index_equiv


def get_binary_str_codegen(is_binary=False):
    if is_binary:
        dwuee__cryv = 'bytes_type'
    else:
        dwuee__cryv = 'string_type'
    fehg__xwa = 'def impl(context, builder, signature, args):\n'
    fehg__xwa += '    assert len(args) == 2\n'
    fehg__xwa += '    index_typ = signature.return_type\n'
    fehg__xwa += (
        '    index_val = cgutils.create_struct_proxy(index_typ)(context, builder)\n'
        )
    fehg__xwa += '    index_val.data = args[0]\n'
    fehg__xwa += '    index_val.name = args[1]\n'
    fehg__xwa += '    # increase refcount of stored values\n'
    fehg__xwa += (
        '    context.nrt.incref(builder, signature.args[0], args[0])\n')
    fehg__xwa += (
        '    context.nrt.incref(builder, index_typ.name_typ, args[1])\n')
    fehg__xwa += '    # create empty dict for get_loc hashmap\n'
    fehg__xwa += '    index_val.dict = context.compile_internal(\n'
    fehg__xwa += '       builder,\n'
    fehg__xwa += (
        f'       lambda: numba.typed.Dict.empty({dwuee__cryv}, types.int64),\n'
        )
    fehg__xwa += (
        f'        types.DictType({dwuee__cryv}, types.int64)(), [],)\n')
    fehg__xwa += '    return index_val._getvalue()\n'
    man__pms = {}
    exec(fehg__xwa, {'bodo': bodo, 'signature': signature, 'cgutils':
        cgutils, 'numba': numba, 'types': types, 'bytes_type': bytes_type,
        'string_type': string_type}, man__pms)
    impl = man__pms['impl']
    return impl


@overload_method(BinaryIndexType, 'copy', no_unliteral=True)
@overload_method(StringIndexType, 'copy', no_unliteral=True)
def overload_binary_string_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    typ = type(A)
    oidgs__kyaw = idx_typ_to_format_str_map[typ].format('copy()')
    dfsq__wmp = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', dfsq__wmp, idx_cpy_arg_defaults,
        fn_str=oidgs__kyaw, package_name='pandas', module_name='Index')
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
    qehci__iyf = dict(axis=axis, allow_fill=allow_fill, fill_value=fill_value)
    shxgc__tcrx = dict(axis=0, allow_fill=True, fill_value=None)
    check_unsupported_args('Index.take', qehci__iyf, shxgc__tcrx,
        package_name='pandas', module_name='Index')
    return lambda I, indices: I[indices]


@numba.njit(no_cpython_wrapper=True)
def _init_engine(I):
    if len(I) > 0 and not I._dict:
        gxs__qkir = bodo.utils.conversion.coerce_to_array(I)
        for i in range(len(gxs__qkir)):
            val = gxs__qkir[i]
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
            bvyht__zkxi = (
                'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                )
            warnings.warn(bvyht__zkxi)
            gxs__qkir = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(gxs__qkir)):
                if gxs__qkir[i] == key:
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
    qehci__iyf = dict(method=method, tolerance=tolerance)
    dpmm__hxxja = dict(method=None, tolerance=None)
    check_unsupported_args('Index.get_loc', qehci__iyf, dpmm__hxxja,
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
            bvyht__zkxi = (
                'Index.get_loc() can be slow for global Index objects (pass as argument to JIT function for better performance).'
                )
            warnings.warn(bvyht__zkxi)
            gxs__qkir = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(gxs__qkir)):
                if gxs__qkir[i] == key:
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
        udpr__enn = overload_name in {'isna', 'isnull'}
        if isinstance(I, RangeIndexType):

            def impl(I):
                numba.parfors.parfor.init_prange()
                sdl__nwy = len(I)
                elts__vqg = np.empty(sdl__nwy, np.bool_)
                for i in numba.parfors.parfor.internal_prange(sdl__nwy):
                    elts__vqg[i] = not udpr__enn
                return elts__vqg
            return impl
        fehg__xwa = f"""def impl(I):
    numba.parfors.parfor.init_prange()
    arr = bodo.hiframes.pd_index_ext.get_index_data(I)
    n = len(arr)
    out_arr = np.empty(n, np.bool_)
    for i in numba.parfors.parfor.internal_prange(n):
       out_arr[i] = {'' if udpr__enn else 'not '}bodo.libs.array_kernels.isna(arr, i)
    return out_arr
"""
        man__pms = {}
        exec(fehg__xwa, {'bodo': bodo, 'np': np, 'numba': numba}, man__pms)
        impl = man__pms['impl']
        return impl
    return overload_index_isna_specific_method


isna_overload_types = (RangeIndexType, NumericIndexType, StringIndexType,
    BinaryIndexType, CategoricalIndexType, PeriodIndexType,
    DatetimeIndexType, TimedeltaIndexType)
isna_specific_methods = 'isna', 'notna', 'isnull', 'notnull'


def _install_isna_specific_methods():
    for jfq__rpf in isna_overload_types:
        for overload_name in isna_specific_methods:
            overload_impl = create_isna_specific_method(overload_name)
            overload_method(jfq__rpf, overload_name, no_unliteral=True,
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
            gxs__qkir = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(gxs__qkir, 1)
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
            gxs__qkir = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(gxs__qkir, 2)
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
        gxs__qkir = bodo.hiframes.pd_index_ext.get_index_data(I)
        elts__vqg = bodo.libs.array_kernels.duplicated((gxs__qkir,))
        return elts__vqg
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
    qehci__iyf = dict(keep=keep)
    dpmm__hxxja = dict(keep='first')
    check_unsupported_args('Index.drop_duplicates', qehci__iyf, dpmm__hxxja,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):
        return lambda I, keep='first': I.copy()
    fehg__xwa = """def impl(I, keep='first'):
    data = bodo.hiframes.pd_index_ext.get_index_data(I)
    arr = bodo.libs.array_kernels.drop_duplicates_array(data)
    name = bodo.hiframes.pd_index_ext.get_index_name(I)
"""
    if isinstance(I, PeriodIndexType):
        fehg__xwa += f"""    return bodo.hiframes.pd_index_ext.init_period_index(arr, name, '{I.freq}')
"""
    else:
        fehg__xwa += (
            '    return bodo.utils.conversion.index_from_array(arr, name)')
    man__pms = {}
    exec(fehg__xwa, {'bodo': bodo}, man__pms)
    impl = man__pms['impl']
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
    ahk__yxgk = args[0]
    if isinstance(self.typemap[ahk__yxgk.name], HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(ahk__yxgk):
        return ArrayAnalysis.AnalyzeResult(shape=ahk__yxgk, pre=[])
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
    qehci__iyf = dict(na_action=na_action)
    wcogu__qia = dict(na_action=None)
    check_unsupported_args('Index.map', qehci__iyf, wcogu__qia,
        package_name='pandas', module_name='Index')
    dtype = I.dtype
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.map')
    if dtype == types.NPDatetime('ns'):
        dtype = pd_timestamp_type
    if dtype == types.NPTimedelta('ns'):
        dtype = pd_timedelta_type
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = dtype.elem_type
    wzyvy__vxhdy = numba.core.registry.cpu_target.typing_context
    lfy__jexs = numba.core.registry.cpu_target.target_context
    try:
        amgg__wreyn = get_const_func_output_type(mapper, (dtype,), {},
            wzyvy__vxhdy, lfy__jexs)
    except Exception as kldug__ebki:
        raise_bodo_error(get_udf_error_msg('Index.map()', kldug__ebki))
    qqw__pcl = get_udf_out_arr_type(amgg__wreyn)
    func = get_overload_const_func(mapper, None)
    fehg__xwa = 'def f(I, mapper, na_action=None):\n'
    fehg__xwa += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    fehg__xwa += '  A = bodo.utils.conversion.coerce_to_array(I)\n'
    fehg__xwa += '  numba.parfors.parfor.init_prange()\n'
    fehg__xwa += '  n = len(A)\n'
    fehg__xwa += '  S = bodo.utils.utils.alloc_type(n, _arr_typ, (-1,))\n'
    fehg__xwa += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    fehg__xwa += '    t2 = bodo.utils.conversion.box_if_dt64(A[i])\n'
    fehg__xwa += '    v = map_func(t2)\n'
    fehg__xwa += '    S[i] = bodo.utils.conversion.unbox_if_timestamp(v)\n'
    fehg__xwa += '  return bodo.utils.conversion.index_from_array(S, name)\n'
    scglu__izgl = bodo.compiler.udf_jit(func)
    man__pms = {}
    exec(fehg__xwa, {'numba': numba, 'np': np, 'pd': pd, 'bodo': bodo,
        'map_func': scglu__izgl, '_arr_typ': qqw__pcl, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'data_arr_type': qqw__pcl.dtype},
        man__pms)
    f = man__pms['f']
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
    smwoz__khqrk, spwat__uqfi = sig.args
    if smwoz__khqrk != spwat__uqfi:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return a._data is b._data and a._name is b._name
    return context.compile_internal(builder, index_is_impl, sig, args)


@lower_builtin(operator.is_, RangeIndexType, RangeIndexType)
def range_index_is(context, builder, sig, args):
    smwoz__khqrk, spwat__uqfi = sig.args
    if smwoz__khqrk != spwat__uqfi:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._start == b._start and a._stop == b._stop and a._step ==
            b._step and a._name is b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)


def create_binary_op_overload(op):

    def overload_index_binary_op(lhs, rhs):
        if is_index_type(lhs):
            fehg__xwa = (
                'def impl(lhs, rhs):\n  arr = bodo.utils.conversion.coerce_to_array(lhs)\n'
                )
            if rhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                fehg__xwa += """  dt = bodo.utils.conversion.unbox_if_timestamp(rhs)
  return op(arr, dt)
"""
            else:
                fehg__xwa += """  rhs_arr = bodo.utils.conversion.get_array_if_series_or_index(rhs)
  return op(arr, rhs_arr)
"""
            man__pms = {}
            exec(fehg__xwa, {'bodo': bodo, 'op': op}, man__pms)
            impl = man__pms['impl']
            return impl
        if is_index_type(rhs):
            fehg__xwa = (
                'def impl(lhs, rhs):\n  arr = bodo.utils.conversion.coerce_to_array(rhs)\n'
                )
            if lhs in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type,
                bodo.hiframes.pd_timestamp_ext.pd_timedelta_type]:
                fehg__xwa += """  dt = bodo.utils.conversion.unbox_if_timestamp(lhs)
  return op(dt, arr)
"""
            else:
                fehg__xwa += """  lhs_arr = bodo.utils.conversion.get_array_if_series_or_index(lhs)
  return op(lhs_arr, arr)
"""
            man__pms = {}
            exec(fehg__xwa, {'bodo': bodo, 'op': op}, man__pms)
            impl = man__pms['impl']
            return impl
        if isinstance(lhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(lhs.data):

                def impl3(lhs, rhs):
                    data = bodo.utils.conversion.coerce_to_array(lhs)
                    gxs__qkir = bodo.utils.conversion.coerce_to_array(data)
                    bavg__dnh = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    elts__vqg = op(gxs__qkir, bavg__dnh)
                    return elts__vqg
                return impl3
            count = len(lhs.data.types)
            fehg__xwa = 'def f(lhs, rhs):\n'
            fehg__xwa += '  return [{}]\n'.format(','.join(
                'op(lhs[{}], rhs{})'.format(i, f'[{i}]' if is_iterable_type
                (rhs) else '') for i in range(count)))
            man__pms = {}
            exec(fehg__xwa, {'op': op, 'np': np}, man__pms)
            impl = man__pms['f']
            return impl
        if isinstance(rhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(rhs.data):

                def impl4(lhs, rhs):
                    data = bodo.hiframes.pd_index_ext.get_index_data(rhs)
                    gxs__qkir = bodo.utils.conversion.coerce_to_array(data)
                    bavg__dnh = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    elts__vqg = op(bavg__dnh, gxs__qkir)
                    return elts__vqg
                return impl4
            count = len(rhs.data.types)
            fehg__xwa = 'def f(lhs, rhs):\n'
            fehg__xwa += '  return [{}]\n'.format(','.join(
                'op(lhs{}, rhs[{}])'.format(f'[{i}]' if is_iterable_type(
                lhs) else '', i) for i in range(count)))
            man__pms = {}
            exec(fehg__xwa, {'op': op, 'np': np}, man__pms)
            impl = man__pms['f']
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
        ohqcx__locy = [('data', fe_type.data), ('name', fe_type.name_typ)]
        super(HeterogeneousIndexModel, self).__init__(dmm, fe_type, ohqcx__locy
            )


make_attribute_wrapper(HeterogeneousIndexType, 'data', '_data')
make_attribute_wrapper(HeterogeneousIndexType, 'name', '_name')


@overload_method(HeterogeneousIndexType, 'copy', no_unliteral=True)
def overload_heter_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    oidgs__kyaw = idx_typ_to_format_str_map[HeterogeneousIndexType].format(
        'copy()')
    dfsq__wmp = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', dfsq__wmp, idx_cpy_arg_defaults,
        fn_str=oidgs__kyaw, package_name='pandas', module_name='Index')
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
    doth__bclib = c.context.insert_const_string(c.builder.module, 'pandas')
    iwgp__bqgj = c.pyapi.import_module_noblock(doth__bclib)
    mpgqx__rmn = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, mpgqx__rmn.data)
    ymci__lfzdr = c.pyapi.from_native_value(typ.data, mpgqx__rmn.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, mpgqx__rmn.name)
    wnqn__sjki = c.pyapi.from_native_value(typ.name_typ, mpgqx__rmn.name, c
        .env_manager)
    gcqi__gzx = c.pyapi.make_none()
    vppnb__xjsa = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    jpw__jaaf = c.pyapi.call_method(iwgp__bqgj, 'Index', (ymci__lfzdr,
        gcqi__gzx, vppnb__xjsa, wnqn__sjki))
    c.pyapi.decref(ymci__lfzdr)
    c.pyapi.decref(gcqi__gzx)
    c.pyapi.decref(vppnb__xjsa)
    c.pyapi.decref(wnqn__sjki)
    c.pyapi.decref(iwgp__bqgj)
    c.context.nrt.decref(c.builder, typ, val)
    return jpw__jaaf


@intrinsic
def init_heter_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        lxtp__lkew = signature.return_type
        mpgqx__rmn = cgutils.create_struct_proxy(lxtp__lkew)(context, builder)
        mpgqx__rmn.data = args[0]
        mpgqx__rmn.name = args[1]
        context.nrt.incref(builder, lxtp__lkew.data, args[0])
        context.nrt.incref(builder, lxtp__lkew.name_typ, args[1])
        return mpgqx__rmn._getvalue()
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
    lznfe__fnd = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index}
    if type(I) in lznfe__fnd:
        init_func = lznfe__fnd[type(I)]
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
    kfp__qced = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, kfp__qced])


@lower_constant(PeriodIndexType)
def lower_constant_period_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, bodo.IntegerArrayType(
        types.int64), pd.arrays.IntegerArray(pyval.asi8, pyval.isna()))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    kfp__qced = context.get_constant_null(types.DictType(types.int64, types
        .int64))
    return lir.Constant.literal_struct([data, name, kfp__qced])


@lower_constant(NumericIndexType)
def lower_constant_numeric_index(context, builder, ty, pyval):
    assert isinstance(ty.dtype, (types.Integer, types.Float, types.Boolean))
    data = context.get_constant_generic(builder, types.Array(ty.dtype, 1,
        'C'), pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    kfp__qced = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, kfp__qced])


@lower_constant(StringIndexType)
@lower_constant(BinaryIndexType)
def lower_constant_binary_string_index(context, builder, ty, pyval):
    tzj__ybj = ty.data
    scalar_type = ty.data.dtype
    data = context.get_constant_generic(builder, tzj__ybj, pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    kfp__qced = context.get_constant_null(types.DictType(scalar_type, types
        .int64))
    return lir.Constant.literal_struct([data, name, kfp__qced])


@lower_builtin('getiter', RangeIndexType)
def getiter_range_index(context, builder, sig, args):
    [yce__culuh] = sig.args
    [adn__fxmzc] = args
    wopg__orgc = context.make_helper(builder, yce__culuh, value=adn__fxmzc)
    qme__jkjjh = context.make_helper(builder, sig.return_type)
    ycvxd__nso = cgutils.alloca_once_value(builder, wopg__orgc.start)
    pkgj__wyao = context.get_constant(types.intp, 0)
    wccl__hwp = cgutils.alloca_once_value(builder, pkgj__wyao)
    qme__jkjjh.iter = ycvxd__nso
    qme__jkjjh.stop = wopg__orgc.stop
    qme__jkjjh.step = wopg__orgc.step
    qme__jkjjh.count = wccl__hwp
    vhgx__cpc = builder.sub(wopg__orgc.stop, wopg__orgc.start)
    mijje__ngdb = context.get_constant(types.intp, 1)
    dxsgl__gdne = builder.icmp_signed('>', vhgx__cpc, pkgj__wyao)
    jrgmx__jiaps = builder.icmp_signed('>', wopg__orgc.step, pkgj__wyao)
    kfo__wfttb = builder.not_(builder.xor(dxsgl__gdne, jrgmx__jiaps))
    with builder.if_then(kfo__wfttb):
        pnp__pin = builder.srem(vhgx__cpc, wopg__orgc.step)
        pnp__pin = builder.select(dxsgl__gdne, pnp__pin, builder.neg(pnp__pin))
        awq__cucc = builder.icmp_signed('>', pnp__pin, pkgj__wyao)
        zihp__vjbx = builder.add(builder.sdiv(vhgx__cpc, wopg__orgc.step),
            builder.select(awq__cucc, mijje__ngdb, pkgj__wyao))
        builder.store(zihp__vjbx, wccl__hwp)
    bwop__off = qme__jkjjh._getvalue()
    trnts__hezv = impl_ret_new_ref(context, builder, sig.return_type, bwop__off
        )
    return trnts__hezv


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
    for eewg__sasu in index_unsupported_methods:
        for mrwe__wksy, typ in index_types:
            overload_method(typ, eewg__sasu, no_unliteral=True)(
                create_unsupported_overload(mrwe__wksy.format(eewg__sasu +
                '()')))
    for fvc__kcx in index_unsupported_atrs:
        for mrwe__wksy, typ in index_types:
            overload_attribute(typ, fvc__kcx, no_unliteral=True)(
                create_unsupported_overload(mrwe__wksy.format(fvc__kcx)))
    dyo__ovh = [(StringIndexType, string_index_unsupported_atrs), (
        BinaryIndexType, binary_index_unsupported_atrs), (
        CategoricalIndexType, cat_idx_unsupported_atrs), (IntervalIndexType,
        interval_idx_unsupported_atrs), (MultiIndexType,
        multi_index_unsupported_atrs), (DatetimeIndexType,
        dt_index_unsupported_atrs), (TimedeltaIndexType,
        td_index_unsupported_atrs), (PeriodIndexType,
        period_index_unsupported_atrs)]
    xiuwx__earlk = [(CategoricalIndexType, cat_idx_unsupported_methods), (
        IntervalIndexType, interval_idx_unsupported_methods), (
        MultiIndexType, multi_index_unsupported_methods), (
        DatetimeIndexType, dt_index_unsupported_methods), (
        TimedeltaIndexType, td_index_unsupported_methods), (PeriodIndexType,
        period_index_unsupported_methods)]
    for typ, dwkqz__kfd in xiuwx__earlk:
        mrwe__wksy = idx_typ_to_format_str_map[typ]
        for uur__bos in dwkqz__kfd:
            overload_method(typ, uur__bos, no_unliteral=True)(
                create_unsupported_overload(mrwe__wksy.format(uur__bos + '()'))
                )
    for typ, rwif__jakpd in dyo__ovh:
        mrwe__wksy = idx_typ_to_format_str_map[typ]
        for fvc__kcx in rwif__jakpd:
            overload_attribute(typ, fvc__kcx, no_unliteral=True)(
                create_unsupported_overload(mrwe__wksy.format(fvc__kcx)))
    for kevf__lgucp in [RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, MultiIndexType]:
        for uur__bos in ['max', 'min']:
            mrwe__wksy = idx_typ_to_format_str_map[kevf__lgucp]
            overload_method(kevf__lgucp, uur__bos, no_unliteral=True)(
                create_unsupported_overload(mrwe__wksy.format(uur__bos + '()'))
                )


_install_index_unsupported()
