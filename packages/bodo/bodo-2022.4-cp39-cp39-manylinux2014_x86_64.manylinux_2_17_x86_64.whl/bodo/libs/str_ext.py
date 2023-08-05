import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_getattr, infer_global, signature
from numba.extending import intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_str, is_overload_constant_int, is_overload_constant_str


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


ll.add_symbol('del_str', hstr_ext.del_str)
ll.add_symbol('unicode_to_utf8', hstr_ext.unicode_to_utf8)
ll.add_symbol('memcmp', hstr_ext.memcmp)
ll.add_symbol('int_to_hex', hstr_ext.int_to_hex)
string_type = types.unicode_type


@numba.njit
def contains_regex(e, in_str):
    with numba.objmode(res='bool_'):
        res = bool(e.search(in_str))
    return res


@numba.generated_jit
def str_findall_count(regex, in_str):

    def _str_findall_count_impl(regex, in_str):
        with numba.objmode(res='int64'):
            res = len(regex.findall(in_str))
        return res
    return _str_findall_count_impl


utf8_str_type = types.ArrayCTypes(types.Array(types.uint8, 1, 'C'))


@intrinsic
def unicode_to_utf8_and_len(typingctx, str_typ=None):
    assert str_typ in (string_type, types.Optional(string_type)) or isinstance(
        str_typ, types.StringLiteral)
    jfi__hpwy = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        cff__nhj, = args
        wkc__isz = cgutils.create_struct_proxy(string_type)(context,
            builder, value=cff__nhj)
        wrzhg__cnp = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        smmg__taare = cgutils.create_struct_proxy(jfi__hpwy)(context, builder)
        is_ascii = builder.icmp_unsigned('==', wkc__isz.is_ascii, lir.
            Constant(wkc__isz.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (skrah__nruc, gwder__jxir):
            with skrah__nruc:
                context.nrt.incref(builder, string_type, cff__nhj)
                wrzhg__cnp.data = wkc__isz.data
                wrzhg__cnp.meminfo = wkc__isz.meminfo
                smmg__taare.f1 = wkc__isz.length
            with gwder__jxir:
                zhl__cidz = lir.FunctionType(lir.IntType(64), [lir.IntType(
                    8).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                dzykq__hjw = cgutils.get_or_insert_function(builder.module,
                    zhl__cidz, name='unicode_to_utf8')
                kohyg__vtskf = context.get_constant_null(types.voidptr)
                hew__xedt = builder.call(dzykq__hjw, [kohyg__vtskf,
                    wkc__isz.data, wkc__isz.length, wkc__isz.kind])
                smmg__taare.f1 = hew__xedt
                jrf__eovm = builder.add(hew__xedt, lir.Constant(lir.IntType
                    (64), 1))
                wrzhg__cnp.meminfo = context.nrt.meminfo_alloc_aligned(builder,
                    size=jrf__eovm, align=32)
                wrzhg__cnp.data = context.nrt.meminfo_data(builder,
                    wrzhg__cnp.meminfo)
                builder.call(dzykq__hjw, [wrzhg__cnp.data, wkc__isz.data,
                    wkc__isz.length, wkc__isz.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    wrzhg__cnp.data, [hew__xedt]))
        smmg__taare.f0 = wrzhg__cnp._getvalue()
        return smmg__taare._getvalue()
    return jfi__hpwy(string_type), codegen


def unicode_to_utf8(s):
    return s


@overload(unicode_to_utf8)
def overload_unicode_to_utf8(s):
    return lambda s: unicode_to_utf8_and_len(s)[0]


@overload(max)
def overload_builtin_max(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload(min)
def overload_builtin_min(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@intrinsic
def memcmp(typingctx, dest_t, src_t, count_t=None):

    def codegen(context, builder, sig, args):
        zhl__cidz = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        evhrq__nbncl = cgutils.get_or_insert_function(builder.module,
            zhl__cidz, name='memcmp')
        return builder.call(evhrq__nbncl, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    sqw__xarro = n(10)

    def impl(n):
        if n == 0:
            return 1
        pxrpd__ubr = 0
        if n < 0:
            n = -n
            pxrpd__ubr += 1
        while n > 0:
            n = n // sqw__xarro
            pxrpd__ubr += 1
        return pxrpd__ubr
    return impl


class StdStringType(types.Opaque):

    def __init__(self):
        super(StdStringType, self).__init__(name='StdStringType')


std_str_type = StdStringType()
register_model(StdStringType)(models.OpaqueModel)
del_str = types.ExternalFunction('del_str', types.void(std_str_type))
get_c_str = types.ExternalFunction('get_c_str', types.voidptr(std_str_type))
dummy_use = numba.njit(lambda a: None)


@overload(int)
def int_str_overload(in_str, base=10):
    if in_str == string_type:
        if is_overload_constant_int(base) and get_overload_const_int(base
            ) == 10:

            def _str_to_int_impl(in_str, base=10):
                val = _str_to_int64(in_str._data, in_str._length)
                dummy_use(in_str)
                return val
            return _str_to_int_impl

        def _str_to_int_base_impl(in_str, base=10):
            val = _str_to_int64_base(in_str._data, in_str._length, base)
            dummy_use(in_str)
            return val
        return _str_to_int_base_impl


@infer_global(float)
class StrToFloat(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        [uoxn__dyr] = args
        if isinstance(uoxn__dyr, StdStringType):
            return signature(types.float64, uoxn__dyr)
        if uoxn__dyr == string_type:
            return signature(types.float64, uoxn__dyr)


ll.add_symbol('init_string_const', hstr_ext.init_string_const)
ll.add_symbol('get_c_str', hstr_ext.get_c_str)
ll.add_symbol('str_to_int64', hstr_ext.str_to_int64)
ll.add_symbol('str_to_uint64', hstr_ext.str_to_uint64)
ll.add_symbol('str_to_int64_base', hstr_ext.str_to_int64_base)
ll.add_symbol('str_to_float64', hstr_ext.str_to_float64)
ll.add_symbol('str_to_float32', hstr_ext.str_to_float32)
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('str_from_float32', hstr_ext.str_from_float32)
ll.add_symbol('str_from_float64', hstr_ext.str_from_float64)
get_std_str_len = types.ExternalFunction('get_str_len', signature(types.
    intp, std_str_type))
init_string_from_chars = types.ExternalFunction('init_string_const',
    std_str_type(types.voidptr, types.intp))
_str_to_int64 = types.ExternalFunction('str_to_int64', signature(types.
    int64, types.voidptr, types.int64))
_str_to_uint64 = types.ExternalFunction('str_to_uint64', signature(types.
    uint64, types.voidptr, types.int64))
_str_to_int64_base = types.ExternalFunction('str_to_int64_base', signature(
    types.int64, types.voidptr, types.int64, types.int64))


def gen_unicode_to_std_str(context, builder, unicode_val):
    wkc__isz = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    zhl__cidz = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(64)])
    vpwa__asib = cgutils.get_or_insert_function(builder.module, zhl__cidz,
        name='init_string_const')
    return builder.call(vpwa__asib, [wkc__isz.data, wkc__isz.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        okgm__syf = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(okgm__syf._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return okgm__syf
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    wkc__isz = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return wkc__isz.data


@intrinsic
def unicode_to_std_str(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_unicode_to_std_str(context, builder, args[0])
    return std_str_type(string_type), codegen


@intrinsic
def std_str_to_unicode(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_std_str_to_unicode(context, builder, args[0], True)
    return string_type(std_str_type), codegen


class RandomAccessStringArrayType(types.ArrayCompatible):

    def __init__(self):
        super(RandomAccessStringArrayType, self).__init__(name=
            'RandomAccessStringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    def copy(self):
        RandomAccessStringArrayType()


random_access_string_array = RandomAccessStringArrayType()


@register_model(RandomAccessStringArrayType)
class RandomAccessStringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zlif__euqgt = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, zlif__euqgt)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        vuf__cjlti, = args
        qdyod__ugunk = types.List(string_type)
        ifri__esd = numba.cpython.listobj.ListInstance.allocate(context,
            builder, qdyod__ugunk, vuf__cjlti)
        ifri__esd.size = vuf__cjlti
        aij__veysi = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        aij__veysi.data = ifri__esd.value
        return aij__veysi._getvalue()
    return random_access_string_array(types.intp), codegen


@overload(operator.getitem, no_unliteral=True)
def random_access_str_arr_getitem(A, ind):
    if A != random_access_string_array:
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]


@overload(operator.setitem)
def random_access_str_arr_setitem(A, idx, val):
    if A != random_access_string_array:
        return
    if isinstance(idx, types.Integer):
        assert val == string_type

        def impl_scalar(A, idx, val):
            A._data[idx] = val
        return impl_scalar


@overload(len, no_unliteral=True)
def overload_str_arr_len(A):
    if A == random_access_string_array:
        return lambda A: len(A._data)


@overload_attribute(RandomAccessStringArrayType, 'shape')
def overload_str_arr_shape(A):
    return lambda A: (len(A._data),)


def alloc_random_access_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_str_ext_alloc_random_access_string_array
    ) = alloc_random_access_str_arr_equiv
str_from_float32 = types.ExternalFunction('str_from_float32', types.void(
    types.voidptr, types.float32))
str_from_float64 = types.ExternalFunction('str_from_float64', types.void(
    types.voidptr, types.float64))


def float_to_str(s, v):
    pass


@overload(float_to_str)
def float_to_str_overload(s, v):
    assert isinstance(v, types.Float)
    if v == types.float32:
        return lambda s, v: str_from_float32(s._data, v)
    return lambda s, v: str_from_float64(s._data, v)


@overload(str)
def float_str_overload(v):
    if isinstance(v, types.Float):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(v):
            if v == 0:
                return '0.0'
            jas__xgdqo = 0
            xlzwv__pce = v
            if xlzwv__pce < 0:
                jas__xgdqo = 1
                xlzwv__pce = -xlzwv__pce
            if xlzwv__pce < 1:
                fcv__hxo = 1
            else:
                fcv__hxo = 1 + int(np.floor(np.log10(xlzwv__pce)))
            length = jas__xgdqo + fcv__hxo + 1 + 6
            s = numba.cpython.unicode._malloc_string(kind, 1, length, True)
            float_to_str(s, v)
            return s
        return impl


@overload(format, no_unliteral=True)
def overload_format(value, format_spec=''):
    if is_overload_constant_str(format_spec) and get_overload_const_str(
        format_spec) == '':

        def impl_fast(value, format_spec=''):
            return str(value)
        return impl_fast

    def impl(value, format_spec=''):
        with numba.objmode(res='string'):
            res = format(value, format_spec)
        return res
    return impl


@lower_cast(StdStringType, types.float64)
def cast_str_to_float64(context, builder, fromty, toty, val):
    zhl__cidz = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    vpwa__asib = cgutils.get_or_insert_function(builder.module, zhl__cidz,
        name='str_to_float64')
    res = builder.call(vpwa__asib, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    zhl__cidz = lir.FunctionType(lir.FloatType(), [lir.IntType(8).as_pointer()]
        )
    vpwa__asib = cgutils.get_or_insert_function(builder.module, zhl__cidz,
        name='str_to_float32')
    res = builder.call(vpwa__asib, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.float64)
def cast_unicode_str_to_float64(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float64(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.float32)
def cast_unicode_str_to_float32(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float32(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.int64)
@lower_cast(string_type, types.int32)
@lower_cast(string_type, types.int16)
@lower_cast(string_type, types.int8)
def cast_unicode_str_to_int64(context, builder, fromty, toty, val):
    wkc__isz = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    zhl__cidz = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    vpwa__asib = cgutils.get_or_insert_function(builder.module, zhl__cidz,
        name='str_to_int64')
    res = builder.call(vpwa__asib, (wkc__isz.data, wkc__isz.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    wkc__isz = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    zhl__cidz = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    vpwa__asib = cgutils.get_or_insert_function(builder.module, zhl__cidz,
        name='str_to_uint64')
    res = builder.call(vpwa__asib, (wkc__isz.data, wkc__isz.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        igc__lbmm = ', '.join('e{}'.format(bkf__ixe) for bkf__ixe in range(
            len(args)))
        if igc__lbmm:
            igc__lbmm += ', '
        qvrtk__gshc = ', '.join("{} = ''".format(a) for a in kws.keys())
        zzen__qlt = f'def format_stub(string, {igc__lbmm} {qvrtk__gshc}):\n'
        zzen__qlt += '    pass\n'
        pitxr__gxqwh = {}
        exec(zzen__qlt, {}, pitxr__gxqwh)
        ueyd__eln = pitxr__gxqwh['format_stub']
        ncy__gxa = numba.core.utils.pysignature(ueyd__eln)
        ttg__vunte = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, ttg__vunte).replace(pysig=ncy__gxa)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    bpli__wshi = pat is not None and len(pat) > 1
    if bpli__wshi:
        byaxp__gyeph = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    ifri__esd = len(arr)
    cruv__ypt = 0
    jsh__kranu = 0
    for bkf__ixe in numba.parfors.parfor.internal_prange(ifri__esd):
        if bodo.libs.array_kernels.isna(arr, bkf__ixe):
            continue
        if bpli__wshi:
            amt__aqch = byaxp__gyeph.split(arr[bkf__ixe], maxsplit=n)
        elif pat == '':
            amt__aqch = [''] + list(arr[bkf__ixe]) + ['']
        else:
            amt__aqch = arr[bkf__ixe].split(pat, n)
        cruv__ypt += len(amt__aqch)
        for s in amt__aqch:
            jsh__kranu += bodo.libs.str_arr_ext.get_utf8_size(s)
    flsil__nyvl = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        ifri__esd, (cruv__ypt, jsh__kranu), bodo.libs.str_arr_ext.
        string_array_type)
    fti__exan = bodo.libs.array_item_arr_ext.get_offsets(flsil__nyvl)
    oxhh__coezt = bodo.libs.array_item_arr_ext.get_null_bitmap(flsil__nyvl)
    ptq__tocyx = bodo.libs.array_item_arr_ext.get_data(flsil__nyvl)
    qqqt__dzkd = 0
    for yeai__jwpq in numba.parfors.parfor.internal_prange(ifri__esd):
        fti__exan[yeai__jwpq] = qqqt__dzkd
        if bodo.libs.array_kernels.isna(arr, yeai__jwpq):
            bodo.libs.int_arr_ext.set_bit_to_arr(oxhh__coezt, yeai__jwpq, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(oxhh__coezt, yeai__jwpq, 1)
        if bpli__wshi:
            amt__aqch = byaxp__gyeph.split(arr[yeai__jwpq], maxsplit=n)
        elif pat == '':
            amt__aqch = [''] + list(arr[yeai__jwpq]) + ['']
        else:
            amt__aqch = arr[yeai__jwpq].split(pat, n)
        nnyhw__ozvxo = len(amt__aqch)
        for jvnhh__gmcj in range(nnyhw__ozvxo):
            s = amt__aqch[jvnhh__gmcj]
            ptq__tocyx[qqqt__dzkd] = s
            qqqt__dzkd += 1
    fti__exan[ifri__esd] = qqqt__dzkd
    return flsil__nyvl


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                rtx__zmgwr = '-0x'
                x = x * -1
            else:
                rtx__zmgwr = '0x'
            x = np.uint64(x)
            if x == 0:
                bngfu__yeds = 1
            else:
                bngfu__yeds = fast_ceil_log2(x + 1)
                bngfu__yeds = (bngfu__yeds + 3) // 4
            length = len(rtx__zmgwr) + bngfu__yeds
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, rtx__zmgwr._data,
                len(rtx__zmgwr), 1)
            int_to_hex(output, bngfu__yeds, len(rtx__zmgwr), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    ycebr__godbg = 0 if x & x - 1 == 0 else 1
    bhrfn__szztq = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    dwd__ksbsf = 32
    for bkf__ixe in range(len(bhrfn__szztq)):
        yqqso__zlba = 0 if x & bhrfn__szztq[bkf__ixe] == 0 else dwd__ksbsf
        ycebr__godbg = ycebr__godbg + yqqso__zlba
        x = x >> yqqso__zlba
        dwd__ksbsf = dwd__ksbsf >> 1
    return ycebr__godbg


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        ttto__aahr = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        zhl__cidz = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        lknh__eek = cgutils.get_or_insert_function(builder.module,
            zhl__cidz, name='int_to_hex')
        kxnk__mrio = builder.inttoptr(builder.add(builder.ptrtoint(
            ttto__aahr.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(lknh__eek, (kxnk__mrio, out_len, int_val))
    return types.void(output, out_len, header_len, int_val), codegen


def alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    pass


@overload(alloc_empty_bytes_or_string_data)
def overload_alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    typ = typ.instance_type if isinstance(typ, types.TypeRef) else typ
    if typ == bodo.bytes_type:
        return lambda typ, kind, length, is_ascii=0: np.empty(length, np.uint8)
    if typ == string_type:
        return (lambda typ, kind, length, is_ascii=0: numba.cpython.unicode
            ._empty_string(kind, length, is_ascii))
    raise BodoError(
        f'Internal Error: Expected Bytes or String type, found {typ}')


def get_unicode_or_numpy_data(val):
    pass


@overload(get_unicode_or_numpy_data)
def overload_get_unicode_or_numpy_data(val):
    if val == string_type:
        return lambda val: val._data
    if isinstance(val, types.Array):
        return lambda val: val.ctypes
    raise BodoError(
        f'Internal Error: Expected String or Numpy Array, found {val}')
