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
    kydo__etg = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        isbt__ghmf, = args
        oqmud__rog = cgutils.create_struct_proxy(string_type)(context,
            builder, value=isbt__ghmf)
        tyww__trom = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        ocyx__ixtq = cgutils.create_struct_proxy(kydo__etg)(context, builder)
        is_ascii = builder.icmp_unsigned('==', oqmud__rog.is_ascii, lir.
            Constant(oqmud__rog.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (cuhah__mpai, xofd__kbi):
            with cuhah__mpai:
                context.nrt.incref(builder, string_type, isbt__ghmf)
                tyww__trom.data = oqmud__rog.data
                tyww__trom.meminfo = oqmud__rog.meminfo
                ocyx__ixtq.f1 = oqmud__rog.length
            with xofd__kbi:
                vewwq__wpqd = lir.FunctionType(lir.IntType(64), [lir.
                    IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                    lir.IntType(64), lir.IntType(32)])
                vua__dfwd = cgutils.get_or_insert_function(builder.module,
                    vewwq__wpqd, name='unicode_to_utf8')
                igjpf__ozqu = context.get_constant_null(types.voidptr)
                vtg__kzdz = builder.call(vua__dfwd, [igjpf__ozqu,
                    oqmud__rog.data, oqmud__rog.length, oqmud__rog.kind])
                ocyx__ixtq.f1 = vtg__kzdz
                ifbfd__clvx = builder.add(vtg__kzdz, lir.Constant(lir.
                    IntType(64), 1))
                tyww__trom.meminfo = context.nrt.meminfo_alloc_aligned(builder,
                    size=ifbfd__clvx, align=32)
                tyww__trom.data = context.nrt.meminfo_data(builder,
                    tyww__trom.meminfo)
                builder.call(vua__dfwd, [tyww__trom.data, oqmud__rog.data,
                    oqmud__rog.length, oqmud__rog.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    tyww__trom.data, [vtg__kzdz]))
        ocyx__ixtq.f0 = tyww__trom._getvalue()
        return ocyx__ixtq._getvalue()
    return kydo__etg(string_type), codegen


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
        vewwq__wpqd = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        qakro__qqlsp = cgutils.get_or_insert_function(builder.module,
            vewwq__wpqd, name='memcmp')
        return builder.call(qakro__qqlsp, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    tkob__umpef = n(10)

    def impl(n):
        if n == 0:
            return 1
        lic__kcwz = 0
        if n < 0:
            n = -n
            lic__kcwz += 1
        while n > 0:
            n = n // tkob__umpef
            lic__kcwz += 1
        return lic__kcwz
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
        [ipen__gym] = args
        if isinstance(ipen__gym, StdStringType):
            return signature(types.float64, ipen__gym)
        if ipen__gym == string_type:
            return signature(types.float64, ipen__gym)


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
    oqmud__rog = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    vewwq__wpqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(64)])
    agw__ubouk = cgutils.get_or_insert_function(builder.module, vewwq__wpqd,
        name='init_string_const')
    return builder.call(agw__ubouk, [oqmud__rog.data, oqmud__rog.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        awxid__ebmx = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(awxid__ebmx._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return awxid__ebmx
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    oqmud__rog = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return oqmud__rog.data


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
        dnpf__lyvv = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, dnpf__lyvv)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        jyur__oaokv, = args
        skob__zqccc = types.List(string_type)
        wsotx__rqivd = numba.cpython.listobj.ListInstance.allocate(context,
            builder, skob__zqccc, jyur__oaokv)
        wsotx__rqivd.size = jyur__oaokv
        aplz__lmonk = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        aplz__lmonk.data = wsotx__rqivd.value
        return aplz__lmonk._getvalue()
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
            vmkeh__tono = 0
            ejq__caow = v
            if ejq__caow < 0:
                vmkeh__tono = 1
                ejq__caow = -ejq__caow
            if ejq__caow < 1:
                coh__xjk = 1
            else:
                coh__xjk = 1 + int(np.floor(np.log10(ejq__caow)))
            length = vmkeh__tono + coh__xjk + 1 + 6
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
    vewwq__wpqd = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    agw__ubouk = cgutils.get_or_insert_function(builder.module, vewwq__wpqd,
        name='str_to_float64')
    res = builder.call(agw__ubouk, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    vewwq__wpqd = lir.FunctionType(lir.FloatType(), [lir.IntType(8).
        as_pointer()])
    agw__ubouk = cgutils.get_or_insert_function(builder.module, vewwq__wpqd,
        name='str_to_float32')
    res = builder.call(agw__ubouk, (val,))
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
    oqmud__rog = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    vewwq__wpqd = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType
        (8).as_pointer(), lir.IntType(64)])
    agw__ubouk = cgutils.get_or_insert_function(builder.module, vewwq__wpqd,
        name='str_to_int64')
    res = builder.call(agw__ubouk, (oqmud__rog.data, oqmud__rog.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    oqmud__rog = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    vewwq__wpqd = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType
        (8).as_pointer(), lir.IntType(64)])
    agw__ubouk = cgutils.get_or_insert_function(builder.module, vewwq__wpqd,
        name='str_to_uint64')
    res = builder.call(agw__ubouk, (oqmud__rog.data, oqmud__rog.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        hyeoj__gjl = ', '.join('e{}'.format(jnp__rdq) for jnp__rdq in range
            (len(args)))
        if hyeoj__gjl:
            hyeoj__gjl += ', '
        eic__xprl = ', '.join("{} = ''".format(a) for a in kws.keys())
        gdihf__ugcr = f'def format_stub(string, {hyeoj__gjl} {eic__xprl}):\n'
        gdihf__ugcr += '    pass\n'
        rwu__cordw = {}
        exec(gdihf__ugcr, {}, rwu__cordw)
        bgzh__wcf = rwu__cordw['format_stub']
        yrw__dknc = numba.core.utils.pysignature(bgzh__wcf)
        seimj__ztm = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, seimj__ztm).replace(pysig=yrw__dknc)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    ryr__wdkd = pat is not None and len(pat) > 1
    if ryr__wdkd:
        wsdf__hrsbu = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    wsotx__rqivd = len(arr)
    bwi__vep = 0
    qjl__fze = 0
    for jnp__rdq in numba.parfors.parfor.internal_prange(wsotx__rqivd):
        if bodo.libs.array_kernels.isna(arr, jnp__rdq):
            continue
        if ryr__wdkd:
            oqof__oel = wsdf__hrsbu.split(arr[jnp__rdq], maxsplit=n)
        elif pat == '':
            oqof__oel = [''] + list(arr[jnp__rdq]) + ['']
        else:
            oqof__oel = arr[jnp__rdq].split(pat, n)
        bwi__vep += len(oqof__oel)
        for s in oqof__oel:
            qjl__fze += bodo.libs.str_arr_ext.get_utf8_size(s)
    xhpqi__epp = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        wsotx__rqivd, (bwi__vep, qjl__fze), bodo.libs.str_arr_ext.
        string_array_type)
    ngusy__dffw = bodo.libs.array_item_arr_ext.get_offsets(xhpqi__epp)
    jmas__fomf = bodo.libs.array_item_arr_ext.get_null_bitmap(xhpqi__epp)
    csl__cvf = bodo.libs.array_item_arr_ext.get_data(xhpqi__epp)
    ksy__oxy = 0
    for lnj__qmkma in numba.parfors.parfor.internal_prange(wsotx__rqivd):
        ngusy__dffw[lnj__qmkma] = ksy__oxy
        if bodo.libs.array_kernels.isna(arr, lnj__qmkma):
            bodo.libs.int_arr_ext.set_bit_to_arr(jmas__fomf, lnj__qmkma, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(jmas__fomf, lnj__qmkma, 1)
        if ryr__wdkd:
            oqof__oel = wsdf__hrsbu.split(arr[lnj__qmkma], maxsplit=n)
        elif pat == '':
            oqof__oel = [''] + list(arr[lnj__qmkma]) + ['']
        else:
            oqof__oel = arr[lnj__qmkma].split(pat, n)
        xak__hcxi = len(oqof__oel)
        for iihka__zflz in range(xak__hcxi):
            s = oqof__oel[iihka__zflz]
            csl__cvf[ksy__oxy] = s
            ksy__oxy += 1
    ngusy__dffw[wsotx__rqivd] = ksy__oxy
    return xhpqi__epp


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                ymg__ouqhx = '-0x'
                x = x * -1
            else:
                ymg__ouqhx = '0x'
            x = np.uint64(x)
            if x == 0:
                agxs__ljn = 1
            else:
                agxs__ljn = fast_ceil_log2(x + 1)
                agxs__ljn = (agxs__ljn + 3) // 4
            length = len(ymg__ouqhx) + agxs__ljn
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, ymg__ouqhx._data,
                len(ymg__ouqhx), 1)
            int_to_hex(output, agxs__ljn, len(ymg__ouqhx), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    gcuur__yvqd = 0 if x & x - 1 == 0 else 1
    qsv__zxi = [np.uint64(18446744069414584320), np.uint64(4294901760), np.
        uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    rys__evvca = 32
    for jnp__rdq in range(len(qsv__zxi)):
        guaec__ifdhe = 0 if x & qsv__zxi[jnp__rdq] == 0 else rys__evvca
        gcuur__yvqd = gcuur__yvqd + guaec__ifdhe
        x = x >> guaec__ifdhe
        rys__evvca = rys__evvca >> 1
    return gcuur__yvqd


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        grcj__erf = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        vewwq__wpqd = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        hatr__ywn = cgutils.get_or_insert_function(builder.module,
            vewwq__wpqd, name='int_to_hex')
        tuo__kiu = builder.inttoptr(builder.add(builder.ptrtoint(grcj__erf.
            data, lir.IntType(64)), header_len), lir.IntType(8).as_pointer())
        builder.call(hatr__ywn, (tuo__kiu, out_len, int_val))
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
