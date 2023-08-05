"""helper functions for code generation with llvmlite
"""
import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
import bodo
from bodo.libs import array_ext, hdist
ll.add_symbol('array_getitem', array_ext.array_getitem)
ll.add_symbol('seq_getitem', array_ext.seq_getitem)
ll.add_symbol('list_check', array_ext.list_check)
ll.add_symbol('dict_keys', array_ext.dict_keys)
ll.add_symbol('dict_values', array_ext.dict_values)
ll.add_symbol('dict_merge_from_seq2', array_ext.dict_merge_from_seq2)
ll.add_symbol('is_na_value', array_ext.is_na_value)


def set_bitmap_bit(builder, null_bitmap_ptr, ind, val):
    hti__frald = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    zuk__noipt = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    njc__cszme = builder.gep(null_bitmap_ptr, [hti__frald], inbounds=True)
    yevbw__trp = builder.load(njc__cszme)
    lemhl__jzv = lir.ArrayType(lir.IntType(8), 8)
    puwg__rugse = cgutils.alloca_once_value(builder, lir.Constant(
        lemhl__jzv, (1, 2, 4, 8, 16, 32, 64, 128)))
    jphny__del = builder.load(builder.gep(puwg__rugse, [lir.Constant(lir.
        IntType(64), 0), zuk__noipt], inbounds=True))
    if val:
        builder.store(builder.or_(yevbw__trp, jphny__del), njc__cszme)
    else:
        jphny__del = builder.xor(jphny__del, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(yevbw__trp, jphny__del), njc__cszme)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    hti__frald = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    zuk__noipt = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    yevbw__trp = builder.load(builder.gep(null_bitmap_ptr, [hti__frald],
        inbounds=True))
    lemhl__jzv = lir.ArrayType(lir.IntType(8), 8)
    puwg__rugse = cgutils.alloca_once_value(builder, lir.Constant(
        lemhl__jzv, (1, 2, 4, 8, 16, 32, 64, 128)))
    jphny__del = builder.load(builder.gep(puwg__rugse, [lir.Constant(lir.
        IntType(64), 0), zuk__noipt], inbounds=True))
    return builder.and_(yevbw__trp, jphny__del)


def pyarray_check(builder, context, obj):
    jiqkh__xpoug = context.get_argument_type(types.pyobject)
    yaht__xukl = lir.FunctionType(lir.IntType(32), [jiqkh__xpoug])
    twpvz__uvtq = cgutils.get_or_insert_function(builder.module, yaht__xukl,
        name='is_np_array')
    return builder.call(twpvz__uvtq, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    jiqkh__xpoug = context.get_argument_type(types.pyobject)
    dtjil__gsfqw = context.get_value_type(types.intp)
    ipeul__npqc = lir.FunctionType(lir.IntType(8).as_pointer(), [
        jiqkh__xpoug, dtjil__gsfqw])
    vudus__edl = cgutils.get_or_insert_function(builder.module, ipeul__npqc,
        name='array_getptr1')
    ops__mpb = lir.FunctionType(jiqkh__xpoug, [jiqkh__xpoug, lir.IntType(8)
        .as_pointer()])
    oklly__zncxu = cgutils.get_or_insert_function(builder.module, ops__mpb,
        name='array_getitem')
    jdqqk__hbkoe = builder.call(vudus__edl, [arr_obj, ind])
    return builder.call(oklly__zncxu, [arr_obj, jdqqk__hbkoe])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    jiqkh__xpoug = context.get_argument_type(types.pyobject)
    dtjil__gsfqw = context.get_value_type(types.intp)
    ipeul__npqc = lir.FunctionType(lir.IntType(8).as_pointer(), [
        jiqkh__xpoug, dtjil__gsfqw])
    vudus__edl = cgutils.get_or_insert_function(builder.module, ipeul__npqc,
        name='array_getptr1')
    cei__ywro = lir.FunctionType(lir.VoidType(), [jiqkh__xpoug, lir.IntType
        (8).as_pointer(), jiqkh__xpoug])
    kph__tssk = cgutils.get_or_insert_function(builder.module, cei__ywro,
        name='array_setitem')
    jdqqk__hbkoe = builder.call(vudus__edl, [arr_obj, ind])
    builder.call(kph__tssk, [arr_obj, jdqqk__hbkoe, val_obj])


def seq_getitem(builder, context, obj, ind):
    jiqkh__xpoug = context.get_argument_type(types.pyobject)
    dtjil__gsfqw = context.get_value_type(types.intp)
    vsjym__ktpb = lir.FunctionType(jiqkh__xpoug, [jiqkh__xpoug, dtjil__gsfqw])
    flx__exgh = cgutils.get_or_insert_function(builder.module, vsjym__ktpb,
        name='seq_getitem')
    return builder.call(flx__exgh, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    jiqkh__xpoug = context.get_argument_type(types.pyobject)
    foajw__lkm = lir.FunctionType(lir.IntType(32), [jiqkh__xpoug, jiqkh__xpoug]
        )
    dlx__tailm = cgutils.get_or_insert_function(builder.module, foajw__lkm,
        name='is_na_value')
    return builder.call(dlx__tailm, [val, C_NA])


def list_check(builder, context, obj):
    jiqkh__xpoug = context.get_argument_type(types.pyobject)
    pcwpl__wvvv = context.get_value_type(types.int32)
    htmyo__wegxq = lir.FunctionType(pcwpl__wvvv, [jiqkh__xpoug])
    qnj__oag = cgutils.get_or_insert_function(builder.module, htmyo__wegxq,
        name='list_check')
    return builder.call(qnj__oag, [obj])


def dict_keys(builder, context, obj):
    jiqkh__xpoug = context.get_argument_type(types.pyobject)
    htmyo__wegxq = lir.FunctionType(jiqkh__xpoug, [jiqkh__xpoug])
    qnj__oag = cgutils.get_or_insert_function(builder.module, htmyo__wegxq,
        name='dict_keys')
    return builder.call(qnj__oag, [obj])


def dict_values(builder, context, obj):
    jiqkh__xpoug = context.get_argument_type(types.pyobject)
    htmyo__wegxq = lir.FunctionType(jiqkh__xpoug, [jiqkh__xpoug])
    qnj__oag = cgutils.get_or_insert_function(builder.module, htmyo__wegxq,
        name='dict_values')
    return builder.call(qnj__oag, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    jiqkh__xpoug = context.get_argument_type(types.pyobject)
    htmyo__wegxq = lir.FunctionType(lir.VoidType(), [jiqkh__xpoug,
        jiqkh__xpoug])
    qnj__oag = cgutils.get_or_insert_function(builder.module, htmyo__wegxq,
        name='dict_merge_from_seq2')
    builder.call(qnj__oag, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    jbx__rxjb = cgutils.alloca_once_value(builder, val)
    evdu__kqa = list_check(builder, context, val)
    ujeg__ptz = builder.icmp_unsigned('!=', evdu__kqa, lir.Constant(
        evdu__kqa.type, 0))
    with builder.if_then(ujeg__ptz):
        hnupf__dgyh = context.insert_const_string(builder.module, 'numpy')
        dnge__kqv = c.pyapi.import_module_noblock(hnupf__dgyh)
        btxkt__lugx = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            btxkt__lugx = str(typ.dtype)
        skrev__lbb = c.pyapi.object_getattr_string(dnge__kqv, btxkt__lugx)
        njbzg__mvmpd = builder.load(jbx__rxjb)
        jfxr__ccuxl = c.pyapi.call_method(dnge__kqv, 'asarray', (
            njbzg__mvmpd, skrev__lbb))
        builder.store(jfxr__ccuxl, jbx__rxjb)
        c.pyapi.decref(dnge__kqv)
        c.pyapi.decref(skrev__lbb)
    val = builder.load(jbx__rxjb)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        qfm__kty = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        kck__tfpzn, qjgs__ptj = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [qfm__kty])
        context.nrt.decref(builder, typ, qfm__kty)
        return cgutils.pack_array(builder, [qjgs__ptj])
    if isinstance(typ, (StructType, types.BaseTuple)):
        hnupf__dgyh = context.insert_const_string(builder.module, 'pandas')
        ffnh__ybjt = c.pyapi.import_module_noblock(hnupf__dgyh)
        C_NA = c.pyapi.object_getattr_string(ffnh__ybjt, 'NA')
        pwyn__wsf = bodo.utils.transform.get_type_alloc_counts(typ)
        kifv__hzzdz = context.make_tuple(builder, types.Tuple(pwyn__wsf * [
            types.int64]), pwyn__wsf * [context.get_constant(types.int64, 0)])
        pgik__glwe = cgutils.alloca_once_value(builder, kifv__hzzdz)
        vrvwy__ntjb = 0
        nmpyt__tgngx = typ.data if isinstance(typ, StructType) else typ.types
        for jttr__pjd, t in enumerate(nmpyt__tgngx):
            vpun__owz = bodo.utils.transform.get_type_alloc_counts(t)
            if vpun__owz == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    jttr__pjd])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, jttr__pjd)
            zunah__ixby = is_na_value(builder, context, val_obj, C_NA)
            yhemh__cwcg = builder.icmp_unsigned('!=', zunah__ixby, lir.
                Constant(zunah__ixby.type, 1))
            with builder.if_then(yhemh__cwcg):
                kifv__hzzdz = builder.load(pgik__glwe)
                ivaxg__dqc = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for jttr__pjd in range(vpun__owz):
                    mhqz__dclm = builder.extract_value(kifv__hzzdz, 
                        vrvwy__ntjb + jttr__pjd)
                    rypdo__givoc = builder.extract_value(ivaxg__dqc, jttr__pjd)
                    kifv__hzzdz = builder.insert_value(kifv__hzzdz, builder
                        .add(mhqz__dclm, rypdo__givoc), vrvwy__ntjb + jttr__pjd
                        )
                builder.store(kifv__hzzdz, pgik__glwe)
            vrvwy__ntjb += vpun__owz
        c.pyapi.decref(ffnh__ybjt)
        c.pyapi.decref(C_NA)
        return builder.load(pgik__glwe)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    hnupf__dgyh = context.insert_const_string(builder.module, 'pandas')
    ffnh__ybjt = c.pyapi.import_module_noblock(hnupf__dgyh)
    C_NA = c.pyapi.object_getattr_string(ffnh__ybjt, 'NA')
    pwyn__wsf = bodo.utils.transform.get_type_alloc_counts(typ)
    kifv__hzzdz = context.make_tuple(builder, types.Tuple(pwyn__wsf * [
        types.int64]), [n] + (pwyn__wsf - 1) * [context.get_constant(types.
        int64, 0)])
    pgik__glwe = cgutils.alloca_once_value(builder, kifv__hzzdz)
    with cgutils.for_range(builder, n) as cwgb__ouj:
        xqfut__tpb = cwgb__ouj.index
        hzz__wsvkt = seq_getitem(builder, context, arr_obj, xqfut__tpb)
        zunah__ixby = is_na_value(builder, context, hzz__wsvkt, C_NA)
        yhemh__cwcg = builder.icmp_unsigned('!=', zunah__ixby, lir.Constant
            (zunah__ixby.type, 1))
        with builder.if_then(yhemh__cwcg):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                kifv__hzzdz = builder.load(pgik__glwe)
                ivaxg__dqc = get_array_elem_counts(c, builder, context,
                    hzz__wsvkt, typ.dtype)
                for jttr__pjd in range(pwyn__wsf - 1):
                    mhqz__dclm = builder.extract_value(kifv__hzzdz, 
                        jttr__pjd + 1)
                    rypdo__givoc = builder.extract_value(ivaxg__dqc, jttr__pjd)
                    kifv__hzzdz = builder.insert_value(kifv__hzzdz, builder
                        .add(mhqz__dclm, rypdo__givoc), jttr__pjd + 1)
                builder.store(kifv__hzzdz, pgik__glwe)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                vrvwy__ntjb = 1
                for jttr__pjd, t in enumerate(typ.data):
                    vpun__owz = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if vpun__owz == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(hzz__wsvkt, jttr__pjd)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(hzz__wsvkt,
                            typ.names[jttr__pjd])
                    zunah__ixby = is_na_value(builder, context, val_obj, C_NA)
                    yhemh__cwcg = builder.icmp_unsigned('!=', zunah__ixby,
                        lir.Constant(zunah__ixby.type, 1))
                    with builder.if_then(yhemh__cwcg):
                        kifv__hzzdz = builder.load(pgik__glwe)
                        ivaxg__dqc = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for jttr__pjd in range(vpun__owz):
                            mhqz__dclm = builder.extract_value(kifv__hzzdz,
                                vrvwy__ntjb + jttr__pjd)
                            rypdo__givoc = builder.extract_value(ivaxg__dqc,
                                jttr__pjd)
                            kifv__hzzdz = builder.insert_value(kifv__hzzdz,
                                builder.add(mhqz__dclm, rypdo__givoc), 
                                vrvwy__ntjb + jttr__pjd)
                        builder.store(kifv__hzzdz, pgik__glwe)
                    vrvwy__ntjb += vpun__owz
            else:
                assert isinstance(typ, MapArrayType), typ
                kifv__hzzdz = builder.load(pgik__glwe)
                ukj__wkyuw = dict_keys(builder, context, hzz__wsvkt)
                anaf__jft = dict_values(builder, context, hzz__wsvkt)
                berlt__zygjj = get_array_elem_counts(c, builder, context,
                    ukj__wkyuw, typ.key_arr_type)
                ahu__dfze = bodo.utils.transform.get_type_alloc_counts(typ.
                    key_arr_type)
                for jttr__pjd in range(1, ahu__dfze + 1):
                    mhqz__dclm = builder.extract_value(kifv__hzzdz, jttr__pjd)
                    rypdo__givoc = builder.extract_value(berlt__zygjj, 
                        jttr__pjd - 1)
                    kifv__hzzdz = builder.insert_value(kifv__hzzdz, builder
                        .add(mhqz__dclm, rypdo__givoc), jttr__pjd)
                dhnmu__fmwl = get_array_elem_counts(c, builder, context,
                    anaf__jft, typ.value_arr_type)
                for jttr__pjd in range(ahu__dfze + 1, pwyn__wsf):
                    mhqz__dclm = builder.extract_value(kifv__hzzdz, jttr__pjd)
                    rypdo__givoc = builder.extract_value(dhnmu__fmwl, 
                        jttr__pjd - ahu__dfze)
                    kifv__hzzdz = builder.insert_value(kifv__hzzdz, builder
                        .add(mhqz__dclm, rypdo__givoc), jttr__pjd)
                builder.store(kifv__hzzdz, pgik__glwe)
                c.pyapi.decref(ukj__wkyuw)
                c.pyapi.decref(anaf__jft)
        c.pyapi.decref(hzz__wsvkt)
    c.pyapi.decref(ffnh__ybjt)
    c.pyapi.decref(C_NA)
    return builder.load(pgik__glwe)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    qzmly__dyjmc = n_elems.type.count
    assert qzmly__dyjmc >= 1
    kuwgs__obzs = builder.extract_value(n_elems, 0)
    if qzmly__dyjmc != 1:
        bja__gqowz = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, jttr__pjd) for jttr__pjd in range(1, qzmly__dyjmc)])
        puk__eatbo = types.Tuple([types.int64] * (qzmly__dyjmc - 1))
    else:
        bja__gqowz = context.get_dummy_value()
        puk__eatbo = types.none
    kzesd__rrbmh = types.TypeRef(arr_type)
    sgw__ilwq = arr_type(types.int64, kzesd__rrbmh, puk__eatbo)
    args = [kuwgs__obzs, context.get_dummy_value(), bja__gqowz]
    pyx__zhmm = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        kck__tfpzn, eirge__obzdm = c.pyapi.call_jit_code(pyx__zhmm,
            sgw__ilwq, args)
    else:
        eirge__obzdm = context.compile_internal(builder, pyx__zhmm,
            sgw__ilwq, args)
    return eirge__obzdm


def is_ll_eq(builder, val1, val2):
    tsm__odcbk = val1.type.pointee
    dvpao__ybm = val2.type.pointee
    assert tsm__odcbk == dvpao__ybm, 'invalid llvm value comparison'
    if isinstance(tsm__odcbk, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(tsm__odcbk.elements) if isinstance(tsm__odcbk, lir.
            BaseStructType) else tsm__odcbk.count
        lnfbp__bztwx = lir.Constant(lir.IntType(1), 1)
        for jttr__pjd in range(n_elems):
            kcgxr__fbq = lir.IntType(32)(0)
            zev__fqx = lir.IntType(32)(jttr__pjd)
            xjzq__hnr = builder.gep(val1, [kcgxr__fbq, zev__fqx], inbounds=True
                )
            ego__wul = builder.gep(val2, [kcgxr__fbq, zev__fqx], inbounds=True)
            lnfbp__bztwx = builder.and_(lnfbp__bztwx, is_ll_eq(builder,
                xjzq__hnr, ego__wul))
        return lnfbp__bztwx
    sgeuj__qaf = builder.load(val1)
    cpuxq__zfnbw = builder.load(val2)
    if sgeuj__qaf.type in (lir.FloatType(), lir.DoubleType()):
        utkal__psz = 32 if sgeuj__qaf.type == lir.FloatType() else 64
        sgeuj__qaf = builder.bitcast(sgeuj__qaf, lir.IntType(utkal__psz))
        cpuxq__zfnbw = builder.bitcast(cpuxq__zfnbw, lir.IntType(utkal__psz))
    return builder.icmp_unsigned('==', sgeuj__qaf, cpuxq__zfnbw)
