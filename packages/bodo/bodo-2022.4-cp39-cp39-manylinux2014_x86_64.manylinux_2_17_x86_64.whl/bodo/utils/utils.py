"""
Collection of utility functions. Needs to be refactored in separate files.
"""
import hashlib
import inspect
import keyword
import re
import warnings
from enum import Enum
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.ir_utils import find_callname, find_const, get_definition, guard, mk_unique_var, require
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload
from numba.np.arrayobj import get_itemsize, make_array, populate_array
import bodo
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import num_total_chars, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import NOT_CONSTANT, BodoError, BodoWarning, MetaType, is_str_arr_type
int128_type = types.Integer('int128', 128)


class CTypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Date = 13
    Datetime = 14
    Timedelta = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 20


_numba_to_c_type_map = {types.int8: CTypeEnum.Int8.value, types.uint8:
    CTypeEnum.UInt8.value, types.int32: CTypeEnum.Int32.value, types.uint32:
    CTypeEnum.UInt32.value, types.int64: CTypeEnum.Int64.value, types.
    uint64: CTypeEnum.UInt64.value, types.float32: CTypeEnum.Float32.value,
    types.float64: CTypeEnum.Float64.value, types.NPDatetime('ns'):
    CTypeEnum.Datetime.value, types.NPTimedelta('ns'): CTypeEnum.Timedelta.
    value, types.bool_: CTypeEnum.Bool.value, types.int16: CTypeEnum.Int16.
    value, types.uint16: CTypeEnum.UInt16.value, int128_type: CTypeEnum.
    Int128.value}
numba.core.errors.error_extras = {'unsupported_error': '', 'typing': '',
    'reportable': '', 'interpreter': '', 'constant_inference': ''}
np_alloc_callnames = 'empty', 'zeros', 'ones', 'full'
CONST_DICT_SLOW_WARN_THRESHOLD = 100
CONST_LIST_SLOW_WARN_THRESHOLD = 100000


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


def get_constant(func_ir, var, default=NOT_CONSTANT):
    bzxp__zdkv = guard(get_definition, func_ir, var)
    if bzxp__zdkv is None:
        return default
    if isinstance(bzxp__zdkv, ir.Const):
        return bzxp__zdkv.value
    if isinstance(bzxp__zdkv, ir.Var):
        return get_constant(func_ir, bzxp__zdkv, default)
    return default


def numba_to_c_type(t):
    if isinstance(t, bodo.libs.decimal_arr_ext.Decimal128Type):
        return CTypeEnum.Decimal.value
    if t == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return CTypeEnum.Date.value
    return _numba_to_c_type_map[t]


def is_alloc_callname(func_name, mod_name):
    return isinstance(mod_name, str) and (mod_name == 'numpy' and func_name in
        np_alloc_callnames or func_name == 'empty_inferred' and mod_name in
        ('numba.extending', 'numba.np.unsafe.ndarray') or func_name ==
        'pre_alloc_string_array' and mod_name == 'bodo.libs.str_arr_ext' or
        func_name == 'pre_alloc_binary_array' and mod_name ==
        'bodo.libs.binary_arr_ext' or func_name ==
        'alloc_random_access_string_array' and mod_name ==
        'bodo.libs.str_ext' or func_name == 'pre_alloc_array_item_array' and
        mod_name == 'bodo.libs.array_item_arr_ext' or func_name ==
        'pre_alloc_struct_array' and mod_name == 'bodo.libs.struct_arr_ext' or
        func_name == 'pre_alloc_map_array' and mod_name ==
        'bodo.libs.map_arr_ext' or func_name == 'pre_alloc_tuple_array' and
        mod_name == 'bodo.libs.tuple_arr_ext' or func_name ==
        'alloc_bool_array' and mod_name == 'bodo.libs.bool_arr_ext' or 
        func_name == 'alloc_int_array' and mod_name ==
        'bodo.libs.int_arr_ext' or func_name == 'alloc_datetime_date_array' and
        mod_name == 'bodo.hiframes.datetime_date_ext' or func_name ==
        'alloc_datetime_timedelta_array' and mod_name ==
        'bodo.hiframes.datetime_timedelta_ext' or func_name ==
        'alloc_decimal_array' and mod_name == 'bodo.libs.decimal_arr_ext' or
        func_name == 'alloc_categorical_array' and mod_name ==
        'bodo.hiframes.pd_categorical_ext' or func_name == 'gen_na_array' and
        mod_name == 'bodo.libs.array_kernels')


def find_build_tuple(func_ir, var):
    require(isinstance(var, (ir.Var, str)))
    dbiub__ieey = get_definition(func_ir, var)
    require(isinstance(dbiub__ieey, ir.Expr))
    require(dbiub__ieey.op == 'build_tuple')
    return dbiub__ieey.items


def cprint(*s):
    print(*s)


@infer_global(cprint)
class CprintInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.none, *unliteral_all(args))


typ_to_format = {types.int32: 'd', types.uint32: 'u', types.int64: 'lld',
    types.uint64: 'llu', types.float32: 'f', types.float64: 'lf', types.
    voidptr: 's'}


@lower_builtin(cprint, types.VarArg(types.Any))
def cprint_lower(context, builder, sig, args):
    for xlca__eul, val in enumerate(args):
        typ = sig.args[xlca__eul]
        if isinstance(typ, types.ArrayCTypes):
            cgutils.printf(builder, '%p ', val)
            continue
        ykobd__cizlb = typ_to_format[typ]
        cgutils.printf(builder, '%{} '.format(ykobd__cizlb), val)
    cgutils.printf(builder, '\n')
    return context.get_dummy_value()


def is_whole_slice(typemap, func_ir, var, accept_stride=False):
    require(typemap[var.name] == types.slice2_type or accept_stride and 
        typemap[var.name] == types.slice3_type)
    wtlh__zel = get_definition(func_ir, var)
    require(isinstance(wtlh__zel, ir.Expr) and wtlh__zel.op == 'call')
    assert len(wtlh__zel.args) == 2 or accept_stride and len(wtlh__zel.args
        ) == 3
    assert find_callname(func_ir, wtlh__zel) == ('slice', 'builtins')
    aoozj__dsp = get_definition(func_ir, wtlh__zel.args[0])
    gtl__cibf = get_definition(func_ir, wtlh__zel.args[1])
    require(isinstance(aoozj__dsp, ir.Const) and aoozj__dsp.value == None)
    require(isinstance(gtl__cibf, ir.Const) and gtl__cibf.value == None)
    return True


def is_slice_equiv_arr(arr_var, index_var, func_ir, equiv_set,
    accept_stride=False):
    cij__yed = get_definition(func_ir, index_var)
    require(find_callname(func_ir, cij__yed) == ('slice', 'builtins'))
    require(len(cij__yed.args) in (2, 3))
    require(find_const(func_ir, cij__yed.args[0]) in (0, None))
    require(equiv_set.is_equiv(cij__yed.args[1], arr_var.name + '#0'))
    require(accept_stride or len(cij__yed.args) == 2 or find_const(func_ir,
        cij__yed.args[2]) == 1)
    return True


def get_slice_step(typemap, func_ir, var):
    require(typemap[var.name] == types.slice3_type)
    wtlh__zel = get_definition(func_ir, var)
    require(isinstance(wtlh__zel, ir.Expr) and wtlh__zel.op == 'call')
    assert len(wtlh__zel.args) == 3
    return wtlh__zel.args[2]


def is_array_typ(var_typ, include_index_series=True):
    return is_np_array_typ(var_typ) or var_typ in (string_array_type, bodo.
        binary_array_type, bodo.dict_str_arr_type, bodo.hiframes.split_impl
        .string_array_split_view_type, bodo.hiframes.datetime_date_ext.
        datetime_date_array_type, bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type, boolean_array, bodo.libs.str_ext.
        random_access_string_array) or isinstance(var_typ, (
        IntegerArrayType, bodo.libs.decimal_arr_ext.DecimalArrayType, bodo.
        hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType, bodo.libs.struct_arr_ext.
        StructArrayType, bodo.libs.interval_arr_ext.IntervalArrayType, bodo
        .libs.tuple_arr_ext.TupleArrayType, bodo.libs.map_arr_ext.
        MapArrayType, bodo.libs.csr_matrix_ext.CSRMatrixType, bodo.
        DatetimeArrayType)) or include_index_series and (isinstance(var_typ,
        (bodo.hiframes.pd_series_ext.SeriesType, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType)) or bodo.hiframes.pd_index_ext.
        is_pd_index_type(var_typ))


def is_np_array_typ(var_typ):
    return isinstance(var_typ, types.Array)


def is_distributable_typ(var_typ):
    return is_array_typ(var_typ) or isinstance(var_typ, bodo.hiframes.table
        .TableType) or isinstance(var_typ, bodo.hiframes.pd_dataframe_ext.
        DataFrameType) or isinstance(var_typ, types.List
        ) and is_distributable_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_typ(var_typ.value_type)


def is_distributable_tuple_typ(var_typ):
    return isinstance(var_typ, types.BaseTuple) and any(
        is_distributable_typ(t) or is_distributable_tuple_typ(t) for t in
        var_typ.types) or isinstance(var_typ, types.List
        ) and is_distributable_tuple_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_tuple_typ(var_typ.value_type
        ) or isinstance(var_typ, types.iterators.EnumerateType) and (
        is_distributable_typ(var_typ.yield_type[1]) or
        is_distributable_tuple_typ(var_typ.yield_type[1]))


@numba.generated_jit(nopython=True, cache=True)
def build_set_seen_na(A):

    def impl(A):
        s = dict()
        hfa__fwhf = False
        for xlca__eul in range(len(A)):
            if bodo.libs.array_kernels.isna(A, xlca__eul):
                hfa__fwhf = True
                continue
            s[A[xlca__eul]] = 0
        return s, hfa__fwhf
    return impl


def empty_like_type(n, arr):
    return np.empty(n, arr.dtype)


@overload(empty_like_type, no_unliteral=True)
def empty_like_type_overload(n, arr):
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda n, arr: bodo.hiframes.pd_categorical_ext.
            alloc_categorical_array(n, arr.dtype))
    if isinstance(arr, types.Array):
        return lambda n, arr: np.empty(n, arr.dtype)
    if isinstance(arr, types.List) and arr.dtype == string_type:

        def empty_like_type_str_list(n, arr):
            return [''] * n
        return empty_like_type_str_list
    if isinstance(arr, types.List) and arr.dtype == bytes_type:

        def empty_like_type_binary_list(n, arr):
            return [b''] * n
        return empty_like_type_binary_list
    if isinstance(arr, IntegerArrayType):
        krjw__nkt = arr.dtype

        def empty_like_type_int_arr(n, arr):
            return bodo.libs.int_arr_ext.alloc_int_array(n, krjw__nkt)
        return empty_like_type_int_arr
    if arr == boolean_array:

        def empty_like_type_bool_arr(n, arr):
            return bodo.libs.bool_arr_ext.alloc_bool_array(n)
        return empty_like_type_bool_arr
    if arr == bodo.hiframes.datetime_date_ext.datetime_date_array_type:

        def empty_like_type_datetime_date_arr(n, arr):
            return bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(n)
        return empty_like_type_datetime_date_arr
    if (arr == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type):

        def empty_like_type_datetime_timedelta_arr(n, arr):
            return (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(n))
        return empty_like_type_datetime_timedelta_arr
    if isinstance(arr, bodo.libs.decimal_arr_ext.DecimalArrayType):
        precision = arr.precision
        scale = arr.scale

        def empty_like_type_decimal_arr(n, arr):
            return bodo.libs.decimal_arr_ext.alloc_decimal_array(n,
                precision, scale)
        return empty_like_type_decimal_arr
    assert arr == string_array_type

    def empty_like_type_str_arr(n, arr):
        dqle__cmsi = 20
        if len(arr) != 0:
            dqle__cmsi = num_total_chars(arr) // len(arr)
        return pre_alloc_string_array(n, n * dqle__cmsi)
    return empty_like_type_str_arr


def _empty_nd_impl(context, builder, arrtype, shapes):
    dbz__mgusc = make_array(arrtype)
    zvq__eshb = dbz__mgusc(context, builder)
    skyyf__xomms = context.get_data_type(arrtype.dtype)
    ynd__vrpa = context.get_constant(types.intp, get_itemsize(context, arrtype)
        )
    zbzuu__rihr = context.get_constant(types.intp, 1)
    bzj__ohryl = lir.Constant(lir.IntType(1), 0)
    for s in shapes:
        rto__rmvy = builder.smul_with_overflow(zbzuu__rihr, s)
        zbzuu__rihr = builder.extract_value(rto__rmvy, 0)
        bzj__ohryl = builder.or_(bzj__ohryl, builder.extract_value(
            rto__rmvy, 1))
    if arrtype.ndim == 0:
        jpts__emxur = ()
    elif arrtype.layout == 'C':
        jpts__emxur = [ynd__vrpa]
        for tdhq__rre in reversed(shapes[1:]):
            jpts__emxur.append(builder.mul(jpts__emxur[-1], tdhq__rre))
        jpts__emxur = tuple(reversed(jpts__emxur))
    elif arrtype.layout == 'F':
        jpts__emxur = [ynd__vrpa]
        for tdhq__rre in shapes[:-1]:
            jpts__emxur.append(builder.mul(jpts__emxur[-1], tdhq__rre))
        jpts__emxur = tuple(jpts__emxur)
    else:
        raise NotImplementedError(
            "Don't know how to allocate array with layout '{0}'.".format(
            arrtype.layout))
    lba__hky = builder.smul_with_overflow(zbzuu__rihr, ynd__vrpa)
    jteni__dim = builder.extract_value(lba__hky, 0)
    bzj__ohryl = builder.or_(bzj__ohryl, builder.extract_value(lba__hky, 1))
    with builder.if_then(bzj__ohryl, likely=False):
        cgutils.printf(builder,
            'array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.'
            )
    dtype = arrtype.dtype
    yumu__cnk = context.get_preferred_array_alignment(dtype)
    vtuw__klp = context.get_constant(types.uint32, yumu__cnk)
    hbh__all = context.nrt.meminfo_alloc_aligned(builder, size=jteni__dim,
        align=vtuw__klp)
    data = context.nrt.meminfo_data(builder, hbh__all)
    nsmu__mhyc = context.get_value_type(types.intp)
    mpm__qantm = cgutils.pack_array(builder, shapes, ty=nsmu__mhyc)
    qmizs__ftrl = cgutils.pack_array(builder, jpts__emxur, ty=nsmu__mhyc)
    populate_array(zvq__eshb, data=builder.bitcast(data, skyyf__xomms.
        as_pointer()), shape=mpm__qantm, strides=qmizs__ftrl, itemsize=
        ynd__vrpa, meminfo=hbh__all)
    return zvq__eshb


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.np.arrayobj._empty_nd_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b6a998927680caa35917a553c79704e9d813d8f1873d83a5f8513837c159fa29':
        warnings.warn('numba.np.arrayobj._empty_nd_impl has changed')


def alloc_arr_tup(n, arr_tup, init_vals=()):
    fzy__wpq = []
    for sfpuo__cldb in arr_tup:
        fzy__wpq.append(np.empty(n, sfpuo__cldb.dtype))
    return tuple(fzy__wpq)


@overload(alloc_arr_tup, no_unliteral=True)
def alloc_arr_tup_overload(n, data, init_vals=()):
    asfae__rbgg = data.count
    vzad__qgq = ','.join(['empty_like_type(n, data[{}])'.format(xlca__eul) for
        xlca__eul in range(asfae__rbgg)])
    if init_vals != ():
        vzad__qgq = ','.join(['np.full(n, init_vals[{}], data[{}].dtype)'.
            format(xlca__eul, xlca__eul) for xlca__eul in range(asfae__rbgg)])
    fktd__dhnvj = 'def f(n, data, init_vals=()):\n'
    fktd__dhnvj += '  return ({}{})\n'.format(vzad__qgq, ',' if asfae__rbgg ==
        1 else '')
    dbu__xdke = {}
    exec(fktd__dhnvj, {'empty_like_type': empty_like_type, 'np': np}, dbu__xdke
        )
    klmz__oso = dbu__xdke['f']
    return klmz__oso


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_to_scalar(n):
    if isinstance(n, types.BaseTuple) and len(n.types) == 1:
        return lambda n: n[0]
    return lambda n: n


def alloc_type(n, t, s=None):
    return np.empty(n, t.dtype)


@overload(alloc_type)
def overload_alloc_type(n, t, s=None):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(typ,
        'bodo.alloc_type()')
    if is_str_arr_type(typ):
        return (lambda n, t, s=None: bodo.libs.str_arr_ext.
            pre_alloc_string_array(n, s[0]))
    if typ == bodo.binary_array_type:
        return (lambda n, t, s=None: bodo.libs.binary_arr_ext.
            pre_alloc_binary_array(n, s[0]))
    if isinstance(typ, bodo.libs.array_item_arr_ext.ArrayItemArrayType):
        dtype = typ.dtype
        return (lambda n, t, s=None: bodo.libs.array_item_arr_ext.
            pre_alloc_array_item_array(n, s, dtype))
    if isinstance(typ, bodo.libs.struct_arr_ext.StructArrayType):
        dtypes = typ.data
        names = typ.names
        return (lambda n, t, s=None: bodo.libs.struct_arr_ext.
            pre_alloc_struct_array(n, s, dtypes, names))
    if isinstance(typ, bodo.libs.map_arr_ext.MapArrayType):
        struct_typ = bodo.libs.struct_arr_ext.StructArrayType((typ.
            key_arr_type, typ.value_arr_type), ('key', 'value'))
        return lambda n, t, s=None: bodo.libs.map_arr_ext.pre_alloc_map_array(n
            , s, struct_typ)
    if isinstance(typ, bodo.libs.tuple_arr_ext.TupleArrayType):
        dtypes = typ.data
        return (lambda n, t, s=None: bodo.libs.tuple_arr_ext.
            pre_alloc_tuple_array(n, s, dtypes))
    if isinstance(typ, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        if isinstance(t, types.TypeRef):
            if typ.dtype.categories is None:
                raise BodoError(
                    'UDFs or Groupbys that return Categorical values must have categories known at compile time.'
                    )
            is_ordered = typ.dtype.ordered
            int_type = typ.dtype.int_type
            new_cats_arr = pd.CategoricalDtype(typ.dtype.categories, is_ordered
                ).categories.values
            new_cats_tup = MetaType(tuple(new_cats_arr))
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, bodo.hiframes.pd_categorical_ext
                .init_cat_dtype(bodo.utils.conversion.index_from_array(
                new_cats_arr), is_ordered, int_type, new_cats_tup)))
        else:
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, t.dtype))
    if typ.dtype == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return (lambda n, t, s=None: bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(n))
    if (typ.dtype == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_type):
        return (lambda n, t, s=None: bodo.hiframes.datetime_timedelta_ext.
            alloc_datetime_timedelta_array(n))
    if isinstance(typ, DecimalArrayType):
        precision = typ.dtype.precision
        scale = typ.dtype.scale
        return (lambda n, t, s=None: bodo.libs.decimal_arr_ext.
            alloc_decimal_array(n, precision, scale))
    dtype = numba.np.numpy_support.as_dtype(typ.dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda n, t, s=None: bodo.libs.int_arr_ext.alloc_int_array(n,
            dtype)
    if typ == boolean_array:
        return lambda n, t, s=None: bodo.libs.bool_arr_ext.alloc_bool_array(n)
    return lambda n, t, s=None: np.empty(n, dtype)


def astype(A, t):
    return A.astype(t.dtype)


@overload(astype, no_unliteral=True)
def overload_astype(A, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    dtype = typ.dtype
    if A == typ:
        return lambda A, t: A
    if isinstance(A, (types.Array, IntegerArrayType)) and isinstance(typ,
        types.Array):
        return lambda A, t: A.astype(dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda A, t: bodo.libs.int_arr_ext.init_integer_array(A.
            astype(dtype), np.full(len(A) + 7 >> 3, 255, np.uint8))
    if (A == bodo.libs.dict_arr_ext.dict_str_arr_type and typ == bodo.
        string_array_type):
        return lambda A, t: bodo.utils.typing.decode_if_dict_array(A)
    raise BodoError(f'cannot convert array type {A} to {typ}')


def full_type(n, val, t):
    return np.full(n, val, t.dtype)


@overload(full_type, no_unliteral=True)
def overload_full_type(n, val, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    if isinstance(typ, types.Array):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: np.full(n, val, dtype)
    if isinstance(typ, IntegerArrayType):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: bodo.libs.int_arr_ext.init_integer_array(np
            .full(n, val, dtype), np.full(tuple_to_scalar(n) + 7 >> 3, 255,
            np.uint8))
    if typ == boolean_array:
        return lambda n, val, t: bodo.libs.bool_arr_ext.init_bool_array(np.
            full(n, val, np.bool_), np.full(tuple_to_scalar(n) + 7 >> 3, 
            255, np.uint8))
    if typ == string_array_type:

        def impl_str(n, val, t):
            bcni__suw = n * len(val)
            A = pre_alloc_string_array(n, bcni__suw)
            for xlca__eul in range(n):
                A[xlca__eul] = val
            return A
        return impl_str

    def impl(n, val, t):
        A = alloc_type(n, typ, (-1,))
        for xlca__eul in range(n):
            A[xlca__eul] = val
        return A
    return impl


@intrinsic
def is_null_pointer(typingctx, ptr_typ=None):

    def codegen(context, builder, signature, args):
        qod__yspyp, = args
        tvp__mxcjb = context.get_constant_null(ptr_typ)
        return builder.icmp_unsigned('==', qod__yspyp, tvp__mxcjb)
    return types.bool_(ptr_typ), codegen


@intrinsic
def is_null_value(typingctx, val_typ=None):

    def codegen(context, builder, signature, args):
        val, = args
        jrtcb__mpvy = cgutils.alloca_once_value(builder, val)
        mbdx__aviu = cgutils.alloca_once_value(builder, context.
            get_constant_null(val_typ))
        return is_ll_eq(builder, jrtcb__mpvy, mbdx__aviu)
    return types.bool_(val_typ), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_list_to_array(A, data, elem_type):
    elem_type = elem_type.instance_type if isinstance(elem_type, types.TypeRef
        ) else elem_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'tuple_list_to_array()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(elem_type,
        'tuple_list_to_array()')
    fktd__dhnvj = 'def impl(A, data, elem_type):\n'
    fktd__dhnvj += '  for i, d in enumerate(data):\n'
    if elem_type == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        fktd__dhnvj += (
            '    A[i] = bodo.utils.conversion.unbox_if_timestamp(d)\n')
    else:
        fktd__dhnvj += '    A[i] = d\n'
    dbu__xdke = {}
    exec(fktd__dhnvj, {'bodo': bodo}, dbu__xdke)
    impl = dbu__xdke['impl']
    return impl


def object_length(c, obj):
    aipt__jrk = c.context.get_argument_type(types.pyobject)
    mozrf__adfpj = lir.FunctionType(lir.IntType(64), [aipt__jrk])
    oihf__ygphj = cgutils.get_or_insert_function(c.builder.module,
        mozrf__adfpj, name='PyObject_Length')
    return c.builder.call(oihf__ygphj, (obj,))


@intrinsic
def incref(typingctx, data=None):

    def codegen(context, builder, signature, args):
        ynhh__ugd, = args
        context.nrt.incref(builder, signature.args[0], ynhh__ugd)
    return types.void(data), codegen


def gen_getitem(out_var, in_var, ind, calltypes, nodes):
    sfc__gksgi = out_var.loc
    bkni__inyk = ir.Expr.static_getitem(in_var, ind, None, sfc__gksgi)
    calltypes[bkni__inyk] = None
    nodes.append(ir.Assign(bkni__inyk, out_var, sfc__gksgi))


def is_static_getsetitem(node):
    return is_expr(node, 'static_getitem') or isinstance(node, ir.StaticSetItem
        )


def get_getsetitem_index_var(node, typemap, nodes):
    index_var = node.index_var if is_static_getsetitem(node) else node.index
    if index_var is None:
        assert is_static_getsetitem(node)
        try:
            drxqh__fjcj = types.literal(node.index)
        except:
            drxqh__fjcj = numba.typeof(node.index)
        index_var = ir.Var(node.value.scope, ir_utils.mk_unique_var(
            'dummy_index'), node.loc)
        typemap[index_var.name] = drxqh__fjcj
        nodes.append(ir.Assign(ir.Const(node.index, node.loc), index_var,
            node.loc))
    return index_var


import copy
ir.Const.__deepcopy__ = lambda self, memo: ir.Const(self.value, copy.
    deepcopy(self.loc))


def is_call_assign(stmt):
    return isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
        ) and stmt.value.op == 'call'


def is_call(expr):
    return isinstance(expr, ir.Expr) and expr.op == 'call'


def is_var_assign(inst):
    return isinstance(inst, ir.Assign) and isinstance(inst.value, ir.Var)


def is_assign(inst):
    return isinstance(inst, ir.Assign)


def is_expr(val, op):
    return isinstance(val, ir.Expr) and val.op == op


def sanitize_varname(varname):
    if isinstance(varname, (tuple, list)):
        varname = '_'.join(sanitize_varname(v) for v in varname)
    varname = str(varname)
    yngx__iic = re.sub('\\W+', '_', varname)
    if not yngx__iic or not yngx__iic[0].isalpha():
        yngx__iic = '_' + yngx__iic
    if not yngx__iic.isidentifier() or keyword.iskeyword(yngx__iic):
        yngx__iic = mk_unique_var('new_name').replace('.', '_')
    return yngx__iic


def dump_node_list(node_list):
    for n in node_list:
        print('   ', n)


def debug_prints():
    return numba.core.config.DEBUG_ARRAY_OPT == 1


@overload(reversed)
def list_reverse(A):
    if isinstance(A, types.List):

        def impl_reversed(A):
            dnfr__equb = len(A)
            for xlca__eul in range(dnfr__equb):
                yield A[dnfr__equb - 1 - xlca__eul]
        return impl_reversed


@numba.njit
def count_nonnan(a):
    return np.count_nonzero(~np.isnan(a))


@numba.njit
def nanvar_ddof1(a):
    wzk__gme = count_nonnan(a)
    if wzk__gme <= 1:
        return np.nan
    return np.nanvar(a) * (wzk__gme / (wzk__gme - 1))


@numba.njit
def nanstd_ddof1(a):
    return np.sqrt(nanvar_ddof1(a))


def has_supported_h5py():
    try:
        import h5py
        from bodo.io import _hdf5
    except ImportError as usxu__cizo:
        ponba__bnk = False
    else:
        ponba__bnk = h5py.version.hdf5_version_tuple[1] in (10, 12)
    return ponba__bnk


def check_h5py():
    if not has_supported_h5py():
        raise BodoError("install 'h5py' package to enable hdf5 support")


def has_pyarrow():
    try:
        import pyarrow
    except ImportError as usxu__cizo:
        ifaol__ysreg = False
    else:
        ifaol__ysreg = True
    return ifaol__ysreg


def has_scipy():
    try:
        import scipy
    except ImportError as usxu__cizo:
        mlaq__ysda = False
    else:
        mlaq__ysda = True
    return mlaq__ysda


@intrinsic
def check_and_propagate_cpp_exception(typingctx):

    def codegen(context, builder, sig, args):
        oek__jbrii = context.get_python_api(builder)
        gnw__troo = oek__jbrii.err_occurred()
        pqsmt__rcs = cgutils.is_not_null(builder, gnw__troo)
        with builder.if_then(pqsmt__rcs):
            builder.ret(numba.core.callconv.RETCODE_EXC)
    return types.void(), codegen


def inlined_check_and_propagate_cpp_exception(context, builder):
    oek__jbrii = context.get_python_api(builder)
    gnw__troo = oek__jbrii.err_occurred()
    pqsmt__rcs = cgutils.is_not_null(builder, gnw__troo)
    with builder.if_then(pqsmt__rcs):
        builder.ret(numba.core.callconv.RETCODE_EXC)


@numba.njit
def check_java_installation(fname):
    with numba.objmode():
        check_java_installation_(fname)


def check_java_installation_(fname):
    if not fname.startswith('hdfs://'):
        return
    import shutil
    if not shutil.which('java'):
        aqpv__vrg = (
            "Java not found. Make sure openjdk is installed for hdfs. openjdk can be installed by calling 'conda install openjdk=8 -c conda-forge'."
            )
        raise BodoError(aqpv__vrg)


dt_err = """
        If you are trying to set NULL values for timedelta64 in regular Python, 

        consider using np.timedelta64('nat') instead of None
        """


@lower_constant(types.List)
def lower_constant_list(context, builder, typ, pyval):
    if len(pyval) > CONST_LIST_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global lists can result in long compilation times. Please pass large lists as arguments to JIT functions or use arrays.'
            ))
    uftm__vtujt = []
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in list must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
        uftm__vtujt.append(context.get_constant_generic(builder, typ.dtype, a))
    ewmt__ryfd = context.get_constant_generic(builder, types.int64, len(pyval))
    jegxu__dss = context.get_constant_generic(builder, types.bool_, False)
    ylisu__yuw = context.get_constant_null(types.pyobject)
    peef__vhogs = lir.Constant.literal_struct([ewmt__ryfd, ewmt__ryfd,
        jegxu__dss] + uftm__vtujt)
    peef__vhogs = cgutils.global_constant(builder, '.const.payload',
        peef__vhogs).bitcast(cgutils.voidptr_t)
    ufkfg__kcwn = context.get_constant(types.int64, -1)
    qhfb__gozlu = context.get_constant_null(types.voidptr)
    hbh__all = lir.Constant.literal_struct([ufkfg__kcwn, qhfb__gozlu,
        qhfb__gozlu, peef__vhogs, ufkfg__kcwn])
    hbh__all = cgutils.global_constant(builder, '.const.meminfo', hbh__all
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([hbh__all, ylisu__yuw])


@lower_constant(types.Set)
def lower_constant_set(context, builder, typ, pyval):
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in set must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
    gsxw__ptiv = types.List(typ.dtype)
    uqcij__uoici = context.get_constant_generic(builder, gsxw__ptiv, list(
        pyval))
    onc__klwu = context.compile_internal(builder, lambda l: set(l), types.
        Set(typ.dtype)(gsxw__ptiv), [uqcij__uoici])
    return onc__klwu


def lower_const_dict_fast_path(context, builder, typ, pyval):
    from bodo.utils.typing import can_replace
    qrte__drkbm = pd.Series(pyval.keys()).values
    homnr__jlabs = pd.Series(pyval.values()).values
    qgny__wwvvq = bodo.typeof(qrte__drkbm)
    pjei__amhsn = bodo.typeof(homnr__jlabs)
    require(qgny__wwvvq.dtype == typ.key_type or can_replace(typ.key_type,
        qgny__wwvvq.dtype))
    require(pjei__amhsn.dtype == typ.value_type or can_replace(typ.
        value_type, pjei__amhsn.dtype))
    mmc__iudy = context.get_constant_generic(builder, qgny__wwvvq, qrte__drkbm)
    sgvhz__seqwl = context.get_constant_generic(builder, pjei__amhsn,
        homnr__jlabs)

    def create_dict(keys, vals):
        yoty__rejx = {}
        for k, v in zip(keys, vals):
            yoty__rejx[k] = v
        return yoty__rejx
    ansac__dstxg = context.compile_internal(builder, create_dict, typ(
        qgny__wwvvq, pjei__amhsn), [mmc__iudy, sgvhz__seqwl])
    return ansac__dstxg


@lower_constant(types.DictType)
def lower_constant_dict(context, builder, typ, pyval):
    try:
        return lower_const_dict_fast_path(context, builder, typ, pyval)
    except:
        pass
    if len(pyval) > CONST_DICT_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global dictionaries can result in long compilation times. Please pass large dictionaries as arguments to JIT functions.'
            ))
    tncf__ezzv = typ.key_type
    utyn__oacie = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(tncf__ezzv, utyn__oacie)
    ansac__dstxg = context.compile_internal(builder, make_dict, typ(), [])

    def set_dict_val(d, k, v):
        d[k] = v
    for k, v in pyval.items():
        lsc__pks = context.get_constant_generic(builder, tncf__ezzv, k)
        gaju__wiys = context.get_constant_generic(builder, utyn__oacie, v)
        context.compile_internal(builder, set_dict_val, types.none(typ,
            tncf__ezzv, utyn__oacie), [ansac__dstxg, lsc__pks, gaju__wiys])
    return ansac__dstxg
