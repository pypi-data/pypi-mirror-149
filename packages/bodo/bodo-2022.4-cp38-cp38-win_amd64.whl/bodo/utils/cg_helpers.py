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
    yis__tvh = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    dgfgv__xogju = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    gdezj__cteuh = builder.gep(null_bitmap_ptr, [yis__tvh], inbounds=True)
    ydai__tcr = builder.load(gdezj__cteuh)
    sxy__evnnd = lir.ArrayType(lir.IntType(8), 8)
    cvbs__mad = cgutils.alloca_once_value(builder, lir.Constant(sxy__evnnd,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    xmxor__qfpf = builder.load(builder.gep(cvbs__mad, [lir.Constant(lir.
        IntType(64), 0), dgfgv__xogju], inbounds=True))
    if val:
        builder.store(builder.or_(ydai__tcr, xmxor__qfpf), gdezj__cteuh)
    else:
        xmxor__qfpf = builder.xor(xmxor__qfpf, lir.Constant(lir.IntType(8), -1)
            )
        builder.store(builder.and_(ydai__tcr, xmxor__qfpf), gdezj__cteuh)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    yis__tvh = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    dgfgv__xogju = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    ydai__tcr = builder.load(builder.gep(null_bitmap_ptr, [yis__tvh],
        inbounds=True))
    sxy__evnnd = lir.ArrayType(lir.IntType(8), 8)
    cvbs__mad = cgutils.alloca_once_value(builder, lir.Constant(sxy__evnnd,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    xmxor__qfpf = builder.load(builder.gep(cvbs__mad, [lir.Constant(lir.
        IntType(64), 0), dgfgv__xogju], inbounds=True))
    return builder.and_(ydai__tcr, xmxor__qfpf)


def pyarray_check(builder, context, obj):
    zqyb__bkpw = context.get_argument_type(types.pyobject)
    tuwu__qkzoi = lir.FunctionType(lir.IntType(32), [zqyb__bkpw])
    bpmqi__lmny = cgutils.get_or_insert_function(builder.module,
        tuwu__qkzoi, name='is_np_array')
    return builder.call(bpmqi__lmny, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    zqyb__bkpw = context.get_argument_type(types.pyobject)
    sic__kstk = context.get_value_type(types.intp)
    knwzs__xemqk = lir.FunctionType(lir.IntType(8).as_pointer(), [
        zqyb__bkpw, sic__kstk])
    tqbsm__gnaxm = cgutils.get_or_insert_function(builder.module,
        knwzs__xemqk, name='array_getptr1')
    cuuq__luc = lir.FunctionType(zqyb__bkpw, [zqyb__bkpw, lir.IntType(8).
        as_pointer()])
    sqxn__bwyd = cgutils.get_or_insert_function(builder.module, cuuq__luc,
        name='array_getitem')
    gbjb__cxh = builder.call(tqbsm__gnaxm, [arr_obj, ind])
    return builder.call(sqxn__bwyd, [arr_obj, gbjb__cxh])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    zqyb__bkpw = context.get_argument_type(types.pyobject)
    sic__kstk = context.get_value_type(types.intp)
    knwzs__xemqk = lir.FunctionType(lir.IntType(8).as_pointer(), [
        zqyb__bkpw, sic__kstk])
    tqbsm__gnaxm = cgutils.get_or_insert_function(builder.module,
        knwzs__xemqk, name='array_getptr1')
    cdik__dxbj = lir.FunctionType(lir.VoidType(), [zqyb__bkpw, lir.IntType(
        8).as_pointer(), zqyb__bkpw])
    fkeq__iypy = cgutils.get_or_insert_function(builder.module, cdik__dxbj,
        name='array_setitem')
    gbjb__cxh = builder.call(tqbsm__gnaxm, [arr_obj, ind])
    builder.call(fkeq__iypy, [arr_obj, gbjb__cxh, val_obj])


def seq_getitem(builder, context, obj, ind):
    zqyb__bkpw = context.get_argument_type(types.pyobject)
    sic__kstk = context.get_value_type(types.intp)
    eoo__lzv = lir.FunctionType(zqyb__bkpw, [zqyb__bkpw, sic__kstk])
    okag__cqewi = cgutils.get_or_insert_function(builder.module, eoo__lzv,
        name='seq_getitem')
    return builder.call(okag__cqewi, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    zqyb__bkpw = context.get_argument_type(types.pyobject)
    cwzxm__esudu = lir.FunctionType(lir.IntType(32), [zqyb__bkpw, zqyb__bkpw])
    snkqs__wkbg = cgutils.get_or_insert_function(builder.module,
        cwzxm__esudu, name='is_na_value')
    return builder.call(snkqs__wkbg, [val, C_NA])


def list_check(builder, context, obj):
    zqyb__bkpw = context.get_argument_type(types.pyobject)
    czdng__wzkhu = context.get_value_type(types.int32)
    qnxy__dvx = lir.FunctionType(czdng__wzkhu, [zqyb__bkpw])
    zco__hvjx = cgutils.get_or_insert_function(builder.module, qnxy__dvx,
        name='list_check')
    return builder.call(zco__hvjx, [obj])


def dict_keys(builder, context, obj):
    zqyb__bkpw = context.get_argument_type(types.pyobject)
    qnxy__dvx = lir.FunctionType(zqyb__bkpw, [zqyb__bkpw])
    zco__hvjx = cgutils.get_or_insert_function(builder.module, qnxy__dvx,
        name='dict_keys')
    return builder.call(zco__hvjx, [obj])


def dict_values(builder, context, obj):
    zqyb__bkpw = context.get_argument_type(types.pyobject)
    qnxy__dvx = lir.FunctionType(zqyb__bkpw, [zqyb__bkpw])
    zco__hvjx = cgutils.get_or_insert_function(builder.module, qnxy__dvx,
        name='dict_values')
    return builder.call(zco__hvjx, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    zqyb__bkpw = context.get_argument_type(types.pyobject)
    qnxy__dvx = lir.FunctionType(lir.VoidType(), [zqyb__bkpw, zqyb__bkpw])
    zco__hvjx = cgutils.get_or_insert_function(builder.module, qnxy__dvx,
        name='dict_merge_from_seq2')
    builder.call(zco__hvjx, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    szbi__luhg = cgutils.alloca_once_value(builder, val)
    mljwu__ghd = list_check(builder, context, val)
    uyt__tmy = builder.icmp_unsigned('!=', mljwu__ghd, lir.Constant(
        mljwu__ghd.type, 0))
    with builder.if_then(uyt__tmy):
        tdf__whd = context.insert_const_string(builder.module, 'numpy')
        pqlbe__zjmbk = c.pyapi.import_module_noblock(tdf__whd)
        dxhiw__kqkze = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            dxhiw__kqkze = str(typ.dtype)
        ugm__fup = c.pyapi.object_getattr_string(pqlbe__zjmbk, dxhiw__kqkze)
        ercu__klsh = builder.load(szbi__luhg)
        eor__ayrs = c.pyapi.call_method(pqlbe__zjmbk, 'asarray', (
            ercu__klsh, ugm__fup))
        builder.store(eor__ayrs, szbi__luhg)
        c.pyapi.decref(pqlbe__zjmbk)
        c.pyapi.decref(ugm__fup)
    val = builder.load(szbi__luhg)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        oiaoh__rdvsy = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        weeaw__enkjh, frzu__src = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [oiaoh__rdvsy])
        context.nrt.decref(builder, typ, oiaoh__rdvsy)
        return cgutils.pack_array(builder, [frzu__src])
    if isinstance(typ, (StructType, types.BaseTuple)):
        tdf__whd = context.insert_const_string(builder.module, 'pandas')
        eead__lql = c.pyapi.import_module_noblock(tdf__whd)
        C_NA = c.pyapi.object_getattr_string(eead__lql, 'NA')
        eljom__btf = bodo.utils.transform.get_type_alloc_counts(typ)
        qleul__glkrf = context.make_tuple(builder, types.Tuple(eljom__btf *
            [types.int64]), eljom__btf * [context.get_constant(types.int64, 0)]
            )
        kwd__usj = cgutils.alloca_once_value(builder, qleul__glkrf)
        tqrvi__mskhg = 0
        svjm__zmal = typ.data if isinstance(typ, StructType) else typ.types
        for hejo__mstij, t in enumerate(svjm__zmal):
            lkqkr__mij = bodo.utils.transform.get_type_alloc_counts(t)
            if lkqkr__mij == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    hejo__mstij])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, hejo__mstij)
            dllr__qhjt = is_na_value(builder, context, val_obj, C_NA)
            euic__uvoh = builder.icmp_unsigned('!=', dllr__qhjt, lir.
                Constant(dllr__qhjt.type, 1))
            with builder.if_then(euic__uvoh):
                qleul__glkrf = builder.load(kwd__usj)
                lqui__kag = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for hejo__mstij in range(lkqkr__mij):
                    zuul__ljbb = builder.extract_value(qleul__glkrf, 
                        tqrvi__mskhg + hejo__mstij)
                    tule__jbon = builder.extract_value(lqui__kag, hejo__mstij)
                    qleul__glkrf = builder.insert_value(qleul__glkrf,
                        builder.add(zuul__ljbb, tule__jbon), tqrvi__mskhg +
                        hejo__mstij)
                builder.store(qleul__glkrf, kwd__usj)
            tqrvi__mskhg += lkqkr__mij
        c.pyapi.decref(eead__lql)
        c.pyapi.decref(C_NA)
        return builder.load(kwd__usj)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    tdf__whd = context.insert_const_string(builder.module, 'pandas')
    eead__lql = c.pyapi.import_module_noblock(tdf__whd)
    C_NA = c.pyapi.object_getattr_string(eead__lql, 'NA')
    eljom__btf = bodo.utils.transform.get_type_alloc_counts(typ)
    qleul__glkrf = context.make_tuple(builder, types.Tuple(eljom__btf * [
        types.int64]), [n] + (eljom__btf - 1) * [context.get_constant(types
        .int64, 0)])
    kwd__usj = cgutils.alloca_once_value(builder, qleul__glkrf)
    with cgutils.for_range(builder, n) as dut__riq:
        pilza__fauvd = dut__riq.index
        dnaf__loaa = seq_getitem(builder, context, arr_obj, pilza__fauvd)
        dllr__qhjt = is_na_value(builder, context, dnaf__loaa, C_NA)
        euic__uvoh = builder.icmp_unsigned('!=', dllr__qhjt, lir.Constant(
            dllr__qhjt.type, 1))
        with builder.if_then(euic__uvoh):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                qleul__glkrf = builder.load(kwd__usj)
                lqui__kag = get_array_elem_counts(c, builder, context,
                    dnaf__loaa, typ.dtype)
                for hejo__mstij in range(eljom__btf - 1):
                    zuul__ljbb = builder.extract_value(qleul__glkrf, 
                        hejo__mstij + 1)
                    tule__jbon = builder.extract_value(lqui__kag, hejo__mstij)
                    qleul__glkrf = builder.insert_value(qleul__glkrf,
                        builder.add(zuul__ljbb, tule__jbon), hejo__mstij + 1)
                builder.store(qleul__glkrf, kwd__usj)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                tqrvi__mskhg = 1
                for hejo__mstij, t in enumerate(typ.data):
                    lkqkr__mij = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if lkqkr__mij == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(dnaf__loaa, hejo__mstij
                            )
                    else:
                        val_obj = c.pyapi.dict_getitem_string(dnaf__loaa,
                            typ.names[hejo__mstij])
                    dllr__qhjt = is_na_value(builder, context, val_obj, C_NA)
                    euic__uvoh = builder.icmp_unsigned('!=', dllr__qhjt,
                        lir.Constant(dllr__qhjt.type, 1))
                    with builder.if_then(euic__uvoh):
                        qleul__glkrf = builder.load(kwd__usj)
                        lqui__kag = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for hejo__mstij in range(lkqkr__mij):
                            zuul__ljbb = builder.extract_value(qleul__glkrf,
                                tqrvi__mskhg + hejo__mstij)
                            tule__jbon = builder.extract_value(lqui__kag,
                                hejo__mstij)
                            qleul__glkrf = builder.insert_value(qleul__glkrf,
                                builder.add(zuul__ljbb, tule__jbon), 
                                tqrvi__mskhg + hejo__mstij)
                        builder.store(qleul__glkrf, kwd__usj)
                    tqrvi__mskhg += lkqkr__mij
            else:
                assert isinstance(typ, MapArrayType), typ
                qleul__glkrf = builder.load(kwd__usj)
                bcai__ylhi = dict_keys(builder, context, dnaf__loaa)
                qsqwe__btk = dict_values(builder, context, dnaf__loaa)
                mjea__naf = get_array_elem_counts(c, builder, context,
                    bcai__ylhi, typ.key_arr_type)
                hjfcy__uxu = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for hejo__mstij in range(1, hjfcy__uxu + 1):
                    zuul__ljbb = builder.extract_value(qleul__glkrf,
                        hejo__mstij)
                    tule__jbon = builder.extract_value(mjea__naf, 
                        hejo__mstij - 1)
                    qleul__glkrf = builder.insert_value(qleul__glkrf,
                        builder.add(zuul__ljbb, tule__jbon), hejo__mstij)
                qji__tcml = get_array_elem_counts(c, builder, context,
                    qsqwe__btk, typ.value_arr_type)
                for hejo__mstij in range(hjfcy__uxu + 1, eljom__btf):
                    zuul__ljbb = builder.extract_value(qleul__glkrf,
                        hejo__mstij)
                    tule__jbon = builder.extract_value(qji__tcml, 
                        hejo__mstij - hjfcy__uxu)
                    qleul__glkrf = builder.insert_value(qleul__glkrf,
                        builder.add(zuul__ljbb, tule__jbon), hejo__mstij)
                builder.store(qleul__glkrf, kwd__usj)
                c.pyapi.decref(bcai__ylhi)
                c.pyapi.decref(qsqwe__btk)
        c.pyapi.decref(dnaf__loaa)
    c.pyapi.decref(eead__lql)
    c.pyapi.decref(C_NA)
    return builder.load(kwd__usj)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    rqm__gjid = n_elems.type.count
    assert rqm__gjid >= 1
    waisi__oxc = builder.extract_value(n_elems, 0)
    if rqm__gjid != 1:
        rhxt__mkj = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, hejo__mstij) for hejo__mstij in range(1, rqm__gjid)])
        ckw__owe = types.Tuple([types.int64] * (rqm__gjid - 1))
    else:
        rhxt__mkj = context.get_dummy_value()
        ckw__owe = types.none
    cmic__nof = types.TypeRef(arr_type)
    erpcb__wizu = arr_type(types.int64, cmic__nof, ckw__owe)
    args = [waisi__oxc, context.get_dummy_value(), rhxt__mkj]
    pkg__yowye = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        weeaw__enkjh, iqmg__ovcj = c.pyapi.call_jit_code(pkg__yowye,
            erpcb__wizu, args)
    else:
        iqmg__ovcj = context.compile_internal(builder, pkg__yowye,
            erpcb__wizu, args)
    return iqmg__ovcj


def is_ll_eq(builder, val1, val2):
    oce__isnd = val1.type.pointee
    djxuh__dadu = val2.type.pointee
    assert oce__isnd == djxuh__dadu, 'invalid llvm value comparison'
    if isinstance(oce__isnd, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(oce__isnd.elements) if isinstance(oce__isnd, lir.
            BaseStructType) else oce__isnd.count
        csvx__kuw = lir.Constant(lir.IntType(1), 1)
        for hejo__mstij in range(n_elems):
            rxvro__mtwr = lir.IntType(32)(0)
            fftrb__zwjp = lir.IntType(32)(hejo__mstij)
            oth__rwl = builder.gep(val1, [rxvro__mtwr, fftrb__zwjp],
                inbounds=True)
            qgxcf__twk = builder.gep(val2, [rxvro__mtwr, fftrb__zwjp],
                inbounds=True)
            csvx__kuw = builder.and_(csvx__kuw, is_ll_eq(builder, oth__rwl,
                qgxcf__twk))
        return csvx__kuw
    qxvqb__gtq = builder.load(val1)
    ctaue__kvtjy = builder.load(val2)
    if qxvqb__gtq.type in (lir.FloatType(), lir.DoubleType()):
        jkp__zcat = 32 if qxvqb__gtq.type == lir.FloatType() else 64
        qxvqb__gtq = builder.bitcast(qxvqb__gtq, lir.IntType(jkp__zcat))
        ctaue__kvtjy = builder.bitcast(ctaue__kvtjy, lir.IntType(jkp__zcat))
    return builder.icmp_unsigned('==', qxvqb__gtq, ctaue__kvtjy)
