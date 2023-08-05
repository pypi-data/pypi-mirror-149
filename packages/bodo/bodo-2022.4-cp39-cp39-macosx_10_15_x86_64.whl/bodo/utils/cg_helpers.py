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
    bdwr__ise = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    wykw__cba = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    ibvy__npln = builder.gep(null_bitmap_ptr, [bdwr__ise], inbounds=True)
    dwh__ezue = builder.load(ibvy__npln)
    tjys__xlnr = lir.ArrayType(lir.IntType(8), 8)
    kdg__nmpwb = cgutils.alloca_once_value(builder, lir.Constant(tjys__xlnr,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    mpph__bcexa = builder.load(builder.gep(kdg__nmpwb, [lir.Constant(lir.
        IntType(64), 0), wykw__cba], inbounds=True))
    if val:
        builder.store(builder.or_(dwh__ezue, mpph__bcexa), ibvy__npln)
    else:
        mpph__bcexa = builder.xor(mpph__bcexa, lir.Constant(lir.IntType(8), -1)
            )
        builder.store(builder.and_(dwh__ezue, mpph__bcexa), ibvy__npln)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    bdwr__ise = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    wykw__cba = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    dwh__ezue = builder.load(builder.gep(null_bitmap_ptr, [bdwr__ise],
        inbounds=True))
    tjys__xlnr = lir.ArrayType(lir.IntType(8), 8)
    kdg__nmpwb = cgutils.alloca_once_value(builder, lir.Constant(tjys__xlnr,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    mpph__bcexa = builder.load(builder.gep(kdg__nmpwb, [lir.Constant(lir.
        IntType(64), 0), wykw__cba], inbounds=True))
    return builder.and_(dwh__ezue, mpph__bcexa)


def pyarray_check(builder, context, obj):
    nmgkd__ixt = context.get_argument_type(types.pyobject)
    ips__hnizh = lir.FunctionType(lir.IntType(32), [nmgkd__ixt])
    pjzab__xwwk = cgutils.get_or_insert_function(builder.module, ips__hnizh,
        name='is_np_array')
    return builder.call(pjzab__xwwk, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    nmgkd__ixt = context.get_argument_type(types.pyobject)
    htws__gqb = context.get_value_type(types.intp)
    nsb__ava = lir.FunctionType(lir.IntType(8).as_pointer(), [nmgkd__ixt,
        htws__gqb])
    ounqy__hnmq = cgutils.get_or_insert_function(builder.module, nsb__ava,
        name='array_getptr1')
    zhj__tvxql = lir.FunctionType(nmgkd__ixt, [nmgkd__ixt, lir.IntType(8).
        as_pointer()])
    ckgus__rdwn = cgutils.get_or_insert_function(builder.module, zhj__tvxql,
        name='array_getitem')
    hmbkh__xyuq = builder.call(ounqy__hnmq, [arr_obj, ind])
    return builder.call(ckgus__rdwn, [arr_obj, hmbkh__xyuq])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    nmgkd__ixt = context.get_argument_type(types.pyobject)
    htws__gqb = context.get_value_type(types.intp)
    nsb__ava = lir.FunctionType(lir.IntType(8).as_pointer(), [nmgkd__ixt,
        htws__gqb])
    ounqy__hnmq = cgutils.get_or_insert_function(builder.module, nsb__ava,
        name='array_getptr1')
    chcsp__rrfw = lir.FunctionType(lir.VoidType(), [nmgkd__ixt, lir.IntType
        (8).as_pointer(), nmgkd__ixt])
    fek__poqw = cgutils.get_or_insert_function(builder.module, chcsp__rrfw,
        name='array_setitem')
    hmbkh__xyuq = builder.call(ounqy__hnmq, [arr_obj, ind])
    builder.call(fek__poqw, [arr_obj, hmbkh__xyuq, val_obj])


def seq_getitem(builder, context, obj, ind):
    nmgkd__ixt = context.get_argument_type(types.pyobject)
    htws__gqb = context.get_value_type(types.intp)
    xmvxg__gwsye = lir.FunctionType(nmgkd__ixt, [nmgkd__ixt, htws__gqb])
    qoss__isgp = cgutils.get_or_insert_function(builder.module,
        xmvxg__gwsye, name='seq_getitem')
    return builder.call(qoss__isgp, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    nmgkd__ixt = context.get_argument_type(types.pyobject)
    wsiim__eisen = lir.FunctionType(lir.IntType(32), [nmgkd__ixt, nmgkd__ixt])
    esav__rol = cgutils.get_or_insert_function(builder.module, wsiim__eisen,
        name='is_na_value')
    return builder.call(esav__rol, [val, C_NA])


def list_check(builder, context, obj):
    nmgkd__ixt = context.get_argument_type(types.pyobject)
    rkvgw__repxr = context.get_value_type(types.int32)
    mvcmw__becqd = lir.FunctionType(rkvgw__repxr, [nmgkd__ixt])
    ipl__qqvmz = cgutils.get_or_insert_function(builder.module,
        mvcmw__becqd, name='list_check')
    return builder.call(ipl__qqvmz, [obj])


def dict_keys(builder, context, obj):
    nmgkd__ixt = context.get_argument_type(types.pyobject)
    mvcmw__becqd = lir.FunctionType(nmgkd__ixt, [nmgkd__ixt])
    ipl__qqvmz = cgutils.get_or_insert_function(builder.module,
        mvcmw__becqd, name='dict_keys')
    return builder.call(ipl__qqvmz, [obj])


def dict_values(builder, context, obj):
    nmgkd__ixt = context.get_argument_type(types.pyobject)
    mvcmw__becqd = lir.FunctionType(nmgkd__ixt, [nmgkd__ixt])
    ipl__qqvmz = cgutils.get_or_insert_function(builder.module,
        mvcmw__becqd, name='dict_values')
    return builder.call(ipl__qqvmz, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    nmgkd__ixt = context.get_argument_type(types.pyobject)
    mvcmw__becqd = lir.FunctionType(lir.VoidType(), [nmgkd__ixt, nmgkd__ixt])
    ipl__qqvmz = cgutils.get_or_insert_function(builder.module,
        mvcmw__becqd, name='dict_merge_from_seq2')
    builder.call(ipl__qqvmz, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    kzwh__zwp = cgutils.alloca_once_value(builder, val)
    zjs__gvvga = list_check(builder, context, val)
    hormo__kkmsr = builder.icmp_unsigned('!=', zjs__gvvga, lir.Constant(
        zjs__gvvga.type, 0))
    with builder.if_then(hormo__kkmsr):
        vhqbk__inyfg = context.insert_const_string(builder.module, 'numpy')
        bryv__nlvq = c.pyapi.import_module_noblock(vhqbk__inyfg)
        ydafm__zjoul = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            ydafm__zjoul = str(typ.dtype)
        szeoa__czj = c.pyapi.object_getattr_string(bryv__nlvq, ydafm__zjoul)
        jpx__qjed = builder.load(kzwh__zwp)
        rkg__cqqa = c.pyapi.call_method(bryv__nlvq, 'asarray', (jpx__qjed,
            szeoa__czj))
        builder.store(rkg__cqqa, kzwh__zwp)
        c.pyapi.decref(bryv__nlvq)
        c.pyapi.decref(szeoa__czj)
    val = builder.load(kzwh__zwp)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        fnzm__ztxvs = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        hhj__ihg, pgpic__yavvb = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [fnzm__ztxvs])
        context.nrt.decref(builder, typ, fnzm__ztxvs)
        return cgutils.pack_array(builder, [pgpic__yavvb])
    if isinstance(typ, (StructType, types.BaseTuple)):
        vhqbk__inyfg = context.insert_const_string(builder.module, 'pandas')
        idx__xwr = c.pyapi.import_module_noblock(vhqbk__inyfg)
        C_NA = c.pyapi.object_getattr_string(idx__xwr, 'NA')
        klgbu__sekx = bodo.utils.transform.get_type_alloc_counts(typ)
        pnuov__taw = context.make_tuple(builder, types.Tuple(klgbu__sekx *
            [types.int64]), klgbu__sekx * [context.get_constant(types.int64,
            0)])
        gzar__gnq = cgutils.alloca_once_value(builder, pnuov__taw)
        ksa__ktz = 0
        nmbk__eooqz = typ.data if isinstance(typ, StructType) else typ.types
        for wbi__lsu, t in enumerate(nmbk__eooqz):
            qcgfc__lxplp = bodo.utils.transform.get_type_alloc_counts(t)
            if qcgfc__lxplp == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    wbi__lsu])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, wbi__lsu)
            exhjk__nnd = is_na_value(builder, context, val_obj, C_NA)
            vefx__htfh = builder.icmp_unsigned('!=', exhjk__nnd, lir.
                Constant(exhjk__nnd.type, 1))
            with builder.if_then(vefx__htfh):
                pnuov__taw = builder.load(gzar__gnq)
                mntvd__zmq = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for wbi__lsu in range(qcgfc__lxplp):
                    icu__ihye = builder.extract_value(pnuov__taw, ksa__ktz +
                        wbi__lsu)
                    qge__hmz = builder.extract_value(mntvd__zmq, wbi__lsu)
                    pnuov__taw = builder.insert_value(pnuov__taw, builder.
                        add(icu__ihye, qge__hmz), ksa__ktz + wbi__lsu)
                builder.store(pnuov__taw, gzar__gnq)
            ksa__ktz += qcgfc__lxplp
        c.pyapi.decref(idx__xwr)
        c.pyapi.decref(C_NA)
        return builder.load(gzar__gnq)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    vhqbk__inyfg = context.insert_const_string(builder.module, 'pandas')
    idx__xwr = c.pyapi.import_module_noblock(vhqbk__inyfg)
    C_NA = c.pyapi.object_getattr_string(idx__xwr, 'NA')
    klgbu__sekx = bodo.utils.transform.get_type_alloc_counts(typ)
    pnuov__taw = context.make_tuple(builder, types.Tuple(klgbu__sekx * [
        types.int64]), [n] + (klgbu__sekx - 1) * [context.get_constant(
        types.int64, 0)])
    gzar__gnq = cgutils.alloca_once_value(builder, pnuov__taw)
    with cgutils.for_range(builder, n) as vcxm__vcnp:
        osxy__kdmbs = vcxm__vcnp.index
        mce__wlq = seq_getitem(builder, context, arr_obj, osxy__kdmbs)
        exhjk__nnd = is_na_value(builder, context, mce__wlq, C_NA)
        vefx__htfh = builder.icmp_unsigned('!=', exhjk__nnd, lir.Constant(
            exhjk__nnd.type, 1))
        with builder.if_then(vefx__htfh):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                pnuov__taw = builder.load(gzar__gnq)
                mntvd__zmq = get_array_elem_counts(c, builder, context,
                    mce__wlq, typ.dtype)
                for wbi__lsu in range(klgbu__sekx - 1):
                    icu__ihye = builder.extract_value(pnuov__taw, wbi__lsu + 1)
                    qge__hmz = builder.extract_value(mntvd__zmq, wbi__lsu)
                    pnuov__taw = builder.insert_value(pnuov__taw, builder.
                        add(icu__ihye, qge__hmz), wbi__lsu + 1)
                builder.store(pnuov__taw, gzar__gnq)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                ksa__ktz = 1
                for wbi__lsu, t in enumerate(typ.data):
                    qcgfc__lxplp = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if qcgfc__lxplp == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(mce__wlq, wbi__lsu)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(mce__wlq, typ
                            .names[wbi__lsu])
                    exhjk__nnd = is_na_value(builder, context, val_obj, C_NA)
                    vefx__htfh = builder.icmp_unsigned('!=', exhjk__nnd,
                        lir.Constant(exhjk__nnd.type, 1))
                    with builder.if_then(vefx__htfh):
                        pnuov__taw = builder.load(gzar__gnq)
                        mntvd__zmq = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for wbi__lsu in range(qcgfc__lxplp):
                            icu__ihye = builder.extract_value(pnuov__taw, 
                                ksa__ktz + wbi__lsu)
                            qge__hmz = builder.extract_value(mntvd__zmq,
                                wbi__lsu)
                            pnuov__taw = builder.insert_value(pnuov__taw,
                                builder.add(icu__ihye, qge__hmz), ksa__ktz +
                                wbi__lsu)
                        builder.store(pnuov__taw, gzar__gnq)
                    ksa__ktz += qcgfc__lxplp
            else:
                assert isinstance(typ, MapArrayType), typ
                pnuov__taw = builder.load(gzar__gnq)
                zcap__jyglw = dict_keys(builder, context, mce__wlq)
                ebltg__qhu = dict_values(builder, context, mce__wlq)
                yqu__dby = get_array_elem_counts(c, builder, context,
                    zcap__jyglw, typ.key_arr_type)
                wrb__qpxlx = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for wbi__lsu in range(1, wrb__qpxlx + 1):
                    icu__ihye = builder.extract_value(pnuov__taw, wbi__lsu)
                    qge__hmz = builder.extract_value(yqu__dby, wbi__lsu - 1)
                    pnuov__taw = builder.insert_value(pnuov__taw, builder.
                        add(icu__ihye, qge__hmz), wbi__lsu)
                ufv__unegx = get_array_elem_counts(c, builder, context,
                    ebltg__qhu, typ.value_arr_type)
                for wbi__lsu in range(wrb__qpxlx + 1, klgbu__sekx):
                    icu__ihye = builder.extract_value(pnuov__taw, wbi__lsu)
                    qge__hmz = builder.extract_value(ufv__unegx, wbi__lsu -
                        wrb__qpxlx)
                    pnuov__taw = builder.insert_value(pnuov__taw, builder.
                        add(icu__ihye, qge__hmz), wbi__lsu)
                builder.store(pnuov__taw, gzar__gnq)
                c.pyapi.decref(zcap__jyglw)
                c.pyapi.decref(ebltg__qhu)
        c.pyapi.decref(mce__wlq)
    c.pyapi.decref(idx__xwr)
    c.pyapi.decref(C_NA)
    return builder.load(gzar__gnq)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    cph__vzt = n_elems.type.count
    assert cph__vzt >= 1
    qbia__idawa = builder.extract_value(n_elems, 0)
    if cph__vzt != 1:
        tzhf__ghtmu = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, wbi__lsu) for wbi__lsu in range(1, cph__vzt)])
        cauj__opa = types.Tuple([types.int64] * (cph__vzt - 1))
    else:
        tzhf__ghtmu = context.get_dummy_value()
        cauj__opa = types.none
    vlp__jjyvn = types.TypeRef(arr_type)
    bwewb__otpou = arr_type(types.int64, vlp__jjyvn, cauj__opa)
    args = [qbia__idawa, context.get_dummy_value(), tzhf__ghtmu]
    mvyov__jadba = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        hhj__ihg, dyqsy__uogyl = c.pyapi.call_jit_code(mvyov__jadba,
            bwewb__otpou, args)
    else:
        dyqsy__uogyl = context.compile_internal(builder, mvyov__jadba,
            bwewb__otpou, args)
    return dyqsy__uogyl


def is_ll_eq(builder, val1, val2):
    zjss__dirmz = val1.type.pointee
    wbn__ryna = val2.type.pointee
    assert zjss__dirmz == wbn__ryna, 'invalid llvm value comparison'
    if isinstance(zjss__dirmz, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(zjss__dirmz.elements) if isinstance(zjss__dirmz, lir.
            BaseStructType) else zjss__dirmz.count
        ugj__lhv = lir.Constant(lir.IntType(1), 1)
        for wbi__lsu in range(n_elems):
            izo__jlytl = lir.IntType(32)(0)
            pxq__rov = lir.IntType(32)(wbi__lsu)
            snmt__qlx = builder.gep(val1, [izo__jlytl, pxq__rov], inbounds=True
                )
            dmzk__gjqi = builder.gep(val2, [izo__jlytl, pxq__rov], inbounds
                =True)
            ugj__lhv = builder.and_(ugj__lhv, is_ll_eq(builder, snmt__qlx,
                dmzk__gjqi))
        return ugj__lhv
    ojupe__nwklh = builder.load(val1)
    nted__lqwsv = builder.load(val2)
    if ojupe__nwklh.type in (lir.FloatType(), lir.DoubleType()):
        tel__pnma = 32 if ojupe__nwklh.type == lir.FloatType() else 64
        ojupe__nwklh = builder.bitcast(ojupe__nwklh, lir.IntType(tel__pnma))
        nted__lqwsv = builder.bitcast(nted__lqwsv, lir.IntType(tel__pnma))
    return builder.icmp_unsigned('==', ojupe__nwklh, nted__lqwsv)
