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
    kdosb__rbj = guard(get_definition, func_ir, var)
    if kdosb__rbj is None:
        return default
    if isinstance(kdosb__rbj, ir.Const):
        return kdosb__rbj.value
    if isinstance(kdosb__rbj, ir.Var):
        return get_constant(func_ir, kdosb__rbj, default)
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
    osufc__uxoc = get_definition(func_ir, var)
    require(isinstance(osufc__uxoc, ir.Expr))
    require(osufc__uxoc.op == 'build_tuple')
    return osufc__uxoc.items


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
    for sxzje__abcdv, val in enumerate(args):
        typ = sig.args[sxzje__abcdv]
        if isinstance(typ, types.ArrayCTypes):
            cgutils.printf(builder, '%p ', val)
            continue
        vna__wsmd = typ_to_format[typ]
        cgutils.printf(builder, '%{} '.format(vna__wsmd), val)
    cgutils.printf(builder, '\n')
    return context.get_dummy_value()


def is_whole_slice(typemap, func_ir, var, accept_stride=False):
    require(typemap[var.name] == types.slice2_type or accept_stride and 
        typemap[var.name] == types.slice3_type)
    urgs__phg = get_definition(func_ir, var)
    require(isinstance(urgs__phg, ir.Expr) and urgs__phg.op == 'call')
    assert len(urgs__phg.args) == 2 or accept_stride and len(urgs__phg.args
        ) == 3
    assert find_callname(func_ir, urgs__phg) == ('slice', 'builtins')
    dxdct__rkwjd = get_definition(func_ir, urgs__phg.args[0])
    jmb__hjdxe = get_definition(func_ir, urgs__phg.args[1])
    require(isinstance(dxdct__rkwjd, ir.Const) and dxdct__rkwjd.value == None)
    require(isinstance(jmb__hjdxe, ir.Const) and jmb__hjdxe.value == None)
    return True


def is_slice_equiv_arr(arr_var, index_var, func_ir, equiv_set,
    accept_stride=False):
    mhkf__gloo = get_definition(func_ir, index_var)
    require(find_callname(func_ir, mhkf__gloo) == ('slice', 'builtins'))
    require(len(mhkf__gloo.args) in (2, 3))
    require(find_const(func_ir, mhkf__gloo.args[0]) in (0, None))
    require(equiv_set.is_equiv(mhkf__gloo.args[1], arr_var.name + '#0'))
    require(accept_stride or len(mhkf__gloo.args) == 2 or find_const(
        func_ir, mhkf__gloo.args[2]) == 1)
    return True


def get_slice_step(typemap, func_ir, var):
    require(typemap[var.name] == types.slice3_type)
    urgs__phg = get_definition(func_ir, var)
    require(isinstance(urgs__phg, ir.Expr) and urgs__phg.op == 'call')
    assert len(urgs__phg.args) == 3
    return urgs__phg.args[2]


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
        jamj__qhpgn = False
        for sxzje__abcdv in range(len(A)):
            if bodo.libs.array_kernels.isna(A, sxzje__abcdv):
                jamj__qhpgn = True
                continue
            s[A[sxzje__abcdv]] = 0
        return s, jamj__qhpgn
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
        duug__hze = arr.dtype

        def empty_like_type_int_arr(n, arr):
            return bodo.libs.int_arr_ext.alloc_int_array(n, duug__hze)
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
        dkxy__wzozn = 20
        if len(arr) != 0:
            dkxy__wzozn = num_total_chars(arr) // len(arr)
        return pre_alloc_string_array(n, n * dkxy__wzozn)
    return empty_like_type_str_arr


def _empty_nd_impl(context, builder, arrtype, shapes):
    osnj__bzfm = make_array(arrtype)
    yyw__kkjmy = osnj__bzfm(context, builder)
    rpgb__ixg = context.get_data_type(arrtype.dtype)
    moao__yrbuv = context.get_constant(types.intp, get_itemsize(context,
        arrtype))
    hnd__utuet = context.get_constant(types.intp, 1)
    erqx__xng = lir.Constant(lir.IntType(1), 0)
    for s in shapes:
        pms__ucn = builder.smul_with_overflow(hnd__utuet, s)
        hnd__utuet = builder.extract_value(pms__ucn, 0)
        erqx__xng = builder.or_(erqx__xng, builder.extract_value(pms__ucn, 1))
    if arrtype.ndim == 0:
        elv__dmd = ()
    elif arrtype.layout == 'C':
        elv__dmd = [moao__yrbuv]
        for vetqo__bczbc in reversed(shapes[1:]):
            elv__dmd.append(builder.mul(elv__dmd[-1], vetqo__bczbc))
        elv__dmd = tuple(reversed(elv__dmd))
    elif arrtype.layout == 'F':
        elv__dmd = [moao__yrbuv]
        for vetqo__bczbc in shapes[:-1]:
            elv__dmd.append(builder.mul(elv__dmd[-1], vetqo__bczbc))
        elv__dmd = tuple(elv__dmd)
    else:
        raise NotImplementedError(
            "Don't know how to allocate array with layout '{0}'.".format(
            arrtype.layout))
    hnu__meedy = builder.smul_with_overflow(hnd__utuet, moao__yrbuv)
    num__aho = builder.extract_value(hnu__meedy, 0)
    erqx__xng = builder.or_(erqx__xng, builder.extract_value(hnu__meedy, 1))
    with builder.if_then(erqx__xng, likely=False):
        cgutils.printf(builder,
            'array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.'
            )
    dtype = arrtype.dtype
    wpi__mxro = context.get_preferred_array_alignment(dtype)
    bbgr__doj = context.get_constant(types.uint32, wpi__mxro)
    fzlc__ygvza = context.nrt.meminfo_alloc_aligned(builder, size=num__aho,
        align=bbgr__doj)
    data = context.nrt.meminfo_data(builder, fzlc__ygvza)
    ceg__zhcjf = context.get_value_type(types.intp)
    ulty__wpzn = cgutils.pack_array(builder, shapes, ty=ceg__zhcjf)
    qpw__zyuaj = cgutils.pack_array(builder, elv__dmd, ty=ceg__zhcjf)
    populate_array(yyw__kkjmy, data=builder.bitcast(data, rpgb__ixg.
        as_pointer()), shape=ulty__wpzn, strides=qpw__zyuaj, itemsize=
        moao__yrbuv, meminfo=fzlc__ygvza)
    return yyw__kkjmy


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.np.arrayobj._empty_nd_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b6a998927680caa35917a553c79704e9d813d8f1873d83a5f8513837c159fa29':
        warnings.warn('numba.np.arrayobj._empty_nd_impl has changed')


def alloc_arr_tup(n, arr_tup, init_vals=()):
    fqxnt__xeht = []
    for fhhn__aozk in arr_tup:
        fqxnt__xeht.append(np.empty(n, fhhn__aozk.dtype))
    return tuple(fqxnt__xeht)


@overload(alloc_arr_tup, no_unliteral=True)
def alloc_arr_tup_overload(n, data, init_vals=()):
    pejlw__xwza = data.count
    uvyb__saw = ','.join(['empty_like_type(n, data[{}])'.format(
        sxzje__abcdv) for sxzje__abcdv in range(pejlw__xwza)])
    if init_vals != ():
        uvyb__saw = ','.join(['np.full(n, init_vals[{}], data[{}].dtype)'.
            format(sxzje__abcdv, sxzje__abcdv) for sxzje__abcdv in range(
            pejlw__xwza)])
    ivowv__aul = 'def f(n, data, init_vals=()):\n'
    ivowv__aul += '  return ({}{})\n'.format(uvyb__saw, ',' if pejlw__xwza ==
        1 else '')
    oyxrr__oxhhx = {}
    exec(ivowv__aul, {'empty_like_type': empty_like_type, 'np': np},
        oyxrr__oxhhx)
    abgei__eswty = oyxrr__oxhhx['f']
    return abgei__eswty


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
            jzm__gebur = n * len(val)
            A = pre_alloc_string_array(n, jzm__gebur)
            for sxzje__abcdv in range(n):
                A[sxzje__abcdv] = val
            return A
        return impl_str

    def impl(n, val, t):
        A = alloc_type(n, typ, (-1,))
        for sxzje__abcdv in range(n):
            A[sxzje__abcdv] = val
        return A
    return impl


@intrinsic
def is_null_pointer(typingctx, ptr_typ=None):

    def codegen(context, builder, signature, args):
        qufqr__qffo, = args
        ern__aie = context.get_constant_null(ptr_typ)
        return builder.icmp_unsigned('==', qufqr__qffo, ern__aie)
    return types.bool_(ptr_typ), codegen


@intrinsic
def is_null_value(typingctx, val_typ=None):

    def codegen(context, builder, signature, args):
        val, = args
        vqrs__rso = cgutils.alloca_once_value(builder, val)
        octf__voc = cgutils.alloca_once_value(builder, context.
            get_constant_null(val_typ))
        return is_ll_eq(builder, vqrs__rso, octf__voc)
    return types.bool_(val_typ), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_list_to_array(A, data, elem_type):
    elem_type = elem_type.instance_type if isinstance(elem_type, types.TypeRef
        ) else elem_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'tuple_list_to_array()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(elem_type,
        'tuple_list_to_array()')
    ivowv__aul = 'def impl(A, data, elem_type):\n'
    ivowv__aul += '  for i, d in enumerate(data):\n'
    if elem_type == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        ivowv__aul += (
            '    A[i] = bodo.utils.conversion.unbox_if_timestamp(d)\n')
    else:
        ivowv__aul += '    A[i] = d\n'
    oyxrr__oxhhx = {}
    exec(ivowv__aul, {'bodo': bodo}, oyxrr__oxhhx)
    impl = oyxrr__oxhhx['impl']
    return impl


def object_length(c, obj):
    umv__tig = c.context.get_argument_type(types.pyobject)
    wdiv__gwfx = lir.FunctionType(lir.IntType(64), [umv__tig])
    dvp__mbkn = cgutils.get_or_insert_function(c.builder.module, wdiv__gwfx,
        name='PyObject_Length')
    return c.builder.call(dvp__mbkn, (obj,))


@intrinsic
def incref(typingctx, data=None):

    def codegen(context, builder, signature, args):
        ieow__gibf, = args
        context.nrt.incref(builder, signature.args[0], ieow__gibf)
    return types.void(data), codegen


def gen_getitem(out_var, in_var, ind, calltypes, nodes):
    ssx__sxdwn = out_var.loc
    tor__gbqu = ir.Expr.static_getitem(in_var, ind, None, ssx__sxdwn)
    calltypes[tor__gbqu] = None
    nodes.append(ir.Assign(tor__gbqu, out_var, ssx__sxdwn))


def is_static_getsetitem(node):
    return is_expr(node, 'static_getitem') or isinstance(node, ir.StaticSetItem
        )


def get_getsetitem_index_var(node, typemap, nodes):
    index_var = node.index_var if is_static_getsetitem(node) else node.index
    if index_var is None:
        assert is_static_getsetitem(node)
        try:
            lyxma__slpis = types.literal(node.index)
        except:
            lyxma__slpis = numba.typeof(node.index)
        index_var = ir.Var(node.value.scope, ir_utils.mk_unique_var(
            'dummy_index'), node.loc)
        typemap[index_var.name] = lyxma__slpis
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
    spf__wlf = re.sub('\\W+', '_', varname)
    if not spf__wlf or not spf__wlf[0].isalpha():
        spf__wlf = '_' + spf__wlf
    if not spf__wlf.isidentifier() or keyword.iskeyword(spf__wlf):
        spf__wlf = mk_unique_var('new_name').replace('.', '_')
    return spf__wlf


def dump_node_list(node_list):
    for n in node_list:
        print('   ', n)


def debug_prints():
    return numba.core.config.DEBUG_ARRAY_OPT == 1


@overload(reversed)
def list_reverse(A):
    if isinstance(A, types.List):

        def impl_reversed(A):
            btpu__axkv = len(A)
            for sxzje__abcdv in range(btpu__axkv):
                yield A[btpu__axkv - 1 - sxzje__abcdv]
        return impl_reversed


@numba.njit
def count_nonnan(a):
    return np.count_nonzero(~np.isnan(a))


@numba.njit
def nanvar_ddof1(a):
    fbt__kpk = count_nonnan(a)
    if fbt__kpk <= 1:
        return np.nan
    return np.nanvar(a) * (fbt__kpk / (fbt__kpk - 1))


@numba.njit
def nanstd_ddof1(a):
    return np.sqrt(nanvar_ddof1(a))


def has_supported_h5py():
    try:
        import h5py
        from bodo.io import _hdf5
    except ImportError as tri__fddui:
        zxzbh__xehyu = False
    else:
        zxzbh__xehyu = h5py.version.hdf5_version_tuple[1] in (10, 12)
    return zxzbh__xehyu


def check_h5py():
    if not has_supported_h5py():
        raise BodoError("install 'h5py' package to enable hdf5 support")


def has_pyarrow():
    try:
        import pyarrow
    except ImportError as tri__fddui:
        ipsd__gqnjz = False
    else:
        ipsd__gqnjz = True
    return ipsd__gqnjz


def has_scipy():
    try:
        import scipy
    except ImportError as tri__fddui:
        brre__vopie = False
    else:
        brre__vopie = True
    return brre__vopie


@intrinsic
def check_and_propagate_cpp_exception(typingctx):

    def codegen(context, builder, sig, args):
        mmy__vrm = context.get_python_api(builder)
        evt__eed = mmy__vrm.err_occurred()
        yvu__kgowl = cgutils.is_not_null(builder, evt__eed)
        with builder.if_then(yvu__kgowl):
            builder.ret(numba.core.callconv.RETCODE_EXC)
    return types.void(), codegen


def inlined_check_and_propagate_cpp_exception(context, builder):
    mmy__vrm = context.get_python_api(builder)
    evt__eed = mmy__vrm.err_occurred()
    yvu__kgowl = cgutils.is_not_null(builder, evt__eed)
    with builder.if_then(yvu__kgowl):
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
        osx__zvj = (
            "Java not found. Make sure openjdk is installed for hdfs. openjdk can be installed by calling 'conda install openjdk=8 -c conda-forge'."
            )
        raise BodoError(osx__zvj)


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
    qhv__dzo = []
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in list must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
        qhv__dzo.append(context.get_constant_generic(builder, typ.dtype, a))
    flma__pelq = context.get_constant_generic(builder, types.int64, len(pyval))
    jraxl__dft = context.get_constant_generic(builder, types.bool_, False)
    ekvuj__slvcn = context.get_constant_null(types.pyobject)
    mow__icl = lir.Constant.literal_struct([flma__pelq, flma__pelq,
        jraxl__dft] + qhv__dzo)
    mow__icl = cgutils.global_constant(builder, '.const.payload', mow__icl
        ).bitcast(cgutils.voidptr_t)
    anovx__iici = context.get_constant(types.int64, -1)
    icjq__sndik = context.get_constant_null(types.voidptr)
    fzlc__ygvza = lir.Constant.literal_struct([anovx__iici, icjq__sndik,
        icjq__sndik, mow__icl, anovx__iici])
    fzlc__ygvza = cgutils.global_constant(builder, '.const.meminfo',
        fzlc__ygvza).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([fzlc__ygvza, ekvuj__slvcn])


@lower_constant(types.Set)
def lower_constant_set(context, builder, typ, pyval):
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in set must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
    pkr__xwth = types.List(typ.dtype)
    pgcq__fpjb = context.get_constant_generic(builder, pkr__xwth, list(pyval))
    puhtt__wpkr = context.compile_internal(builder, lambda l: set(l), types
        .Set(typ.dtype)(pkr__xwth), [pgcq__fpjb])
    return puhtt__wpkr


def lower_const_dict_fast_path(context, builder, typ, pyval):
    from bodo.utils.typing import can_replace
    njzn__tzd = pd.Series(pyval.keys()).values
    ujsu__qhj = pd.Series(pyval.values()).values
    isav__voem = bodo.typeof(njzn__tzd)
    pumfe__nin = bodo.typeof(ujsu__qhj)
    require(isav__voem.dtype == typ.key_type or can_replace(typ.key_type,
        isav__voem.dtype))
    require(pumfe__nin.dtype == typ.value_type or can_replace(typ.
        value_type, pumfe__nin.dtype))
    vuzvk__qen = context.get_constant_generic(builder, isav__voem, njzn__tzd)
    sute__tdbwd = context.get_constant_generic(builder, pumfe__nin, ujsu__qhj)

    def create_dict(keys, vals):
        qudgt__igkzz = {}
        for k, v in zip(keys, vals):
            qudgt__igkzz[k] = v
        return qudgt__igkzz
    akevo__fjwk = context.compile_internal(builder, create_dict, typ(
        isav__voem, pumfe__nin), [vuzvk__qen, sute__tdbwd])
    return akevo__fjwk


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
    vsrb__fwjz = typ.key_type
    jcif__pojh = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(vsrb__fwjz, jcif__pojh)
    akevo__fjwk = context.compile_internal(builder, make_dict, typ(), [])

    def set_dict_val(d, k, v):
        d[k] = v
    for k, v in pyval.items():
        utxcz__cie = context.get_constant_generic(builder, vsrb__fwjz, k)
        zag__zgvqx = context.get_constant_generic(builder, jcif__pojh, v)
        context.compile_internal(builder, set_dict_val, types.none(typ,
            vsrb__fwjz, jcif__pojh), [akevo__fjwk, utxcz__cie, zag__zgvqx])
    return akevo__fjwk
