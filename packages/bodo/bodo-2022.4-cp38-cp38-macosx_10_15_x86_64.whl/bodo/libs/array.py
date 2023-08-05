"""Tools for handling bodo arrays, e.g. passing to C/C++ code
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import intrinsic, models, register_model
from numba.np.arrayobj import _getitem_array_single_int
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, get_categories_int_type
from bodo.libs import array_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, define_array_item_dtor, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType, int128_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType, _get_map_arr_data_type, init_map_arr_codegen
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, char_arr_type, null_bitmap_arr_type, offset_arr_type, string_array_type
from bodo.libs.struct_arr_ext import StructArrayPayloadType, StructArrayType, StructType, _get_struct_arr_payload, define_struct_arr_dtor
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, is_str_arr_type, raise_bodo_error
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, numba_to_c_type
ll.add_symbol('list_string_array_to_info', array_ext.list_string_array_to_info)
ll.add_symbol('nested_array_to_info', array_ext.nested_array_to_info)
ll.add_symbol('string_array_to_info', array_ext.string_array_to_info)
ll.add_symbol('dict_str_array_to_info', array_ext.dict_str_array_to_info)
ll.add_symbol('get_nested_info', array_ext.get_nested_info)
ll.add_symbol('get_has_global_dictionary', array_ext.get_has_global_dictionary)
ll.add_symbol('numpy_array_to_info', array_ext.numpy_array_to_info)
ll.add_symbol('categorical_array_to_info', array_ext.categorical_array_to_info)
ll.add_symbol('nullable_array_to_info', array_ext.nullable_array_to_info)
ll.add_symbol('interval_array_to_info', array_ext.interval_array_to_info)
ll.add_symbol('decimal_array_to_info', array_ext.decimal_array_to_info)
ll.add_symbol('info_to_nested_array', array_ext.info_to_nested_array)
ll.add_symbol('info_to_list_string_array', array_ext.info_to_list_string_array)
ll.add_symbol('info_to_string_array', array_ext.info_to_string_array)
ll.add_symbol('info_to_numpy_array', array_ext.info_to_numpy_array)
ll.add_symbol('info_to_nullable_array', array_ext.info_to_nullable_array)
ll.add_symbol('info_to_interval_array', array_ext.info_to_interval_array)
ll.add_symbol('alloc_numpy', array_ext.alloc_numpy)
ll.add_symbol('alloc_string_array', array_ext.alloc_string_array)
ll.add_symbol('arr_info_list_to_table', array_ext.arr_info_list_to_table)
ll.add_symbol('info_from_table', array_ext.info_from_table)
ll.add_symbol('delete_info_decref_array', array_ext.delete_info_decref_array)
ll.add_symbol('delete_table_decref_arrays', array_ext.
    delete_table_decref_arrays)
ll.add_symbol('delete_table', array_ext.delete_table)
ll.add_symbol('shuffle_table', array_ext.shuffle_table)
ll.add_symbol('get_shuffle_info', array_ext.get_shuffle_info)
ll.add_symbol('delete_shuffle_info', array_ext.delete_shuffle_info)
ll.add_symbol('reverse_shuffle_table', array_ext.reverse_shuffle_table)
ll.add_symbol('hash_join_table', array_ext.hash_join_table)
ll.add_symbol('drop_duplicates_table', array_ext.drop_duplicates_table)
ll.add_symbol('sort_values_table', array_ext.sort_values_table)
ll.add_symbol('sample_table', array_ext.sample_table)
ll.add_symbol('shuffle_renormalization', array_ext.shuffle_renormalization)
ll.add_symbol('shuffle_renormalization_group', array_ext.
    shuffle_renormalization_group)
ll.add_symbol('groupby_and_aggregate', array_ext.groupby_and_aggregate)
ll.add_symbol('pivot_groupby_and_aggregate', array_ext.
    pivot_groupby_and_aggregate)
ll.add_symbol('get_groupby_labels', array_ext.get_groupby_labels)
ll.add_symbol('array_isin', array_ext.array_isin)
ll.add_symbol('get_search_regex', array_ext.get_search_regex)
ll.add_symbol('array_info_getitem', array_ext.array_info_getitem)
ll.add_symbol('array_info_getdata1', array_ext.array_info_getdata1)


class ArrayInfoType(types.Type):

    def __init__(self):
        super(ArrayInfoType, self).__init__(name='ArrayInfoType()')


array_info_type = ArrayInfoType()
register_model(ArrayInfoType)(models.OpaqueModel)


class TableTypeCPP(types.Type):

    def __init__(self):
        super(TableTypeCPP, self).__init__(name='TableTypeCPP()')


table_type = TableTypeCPP()
register_model(TableTypeCPP)(models.OpaqueModel)


@intrinsic
def array_to_info(typingctx, arr_type_t=None):
    return array_info_type(arr_type_t), array_to_info_codegen


def array_to_info_codegen(context, builder, sig, args, incref=True):
    in_arr, = args
    arr_type = sig.args[0]
    if incref:
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, TupleArrayType):
        eqie__magtp = context.make_helper(builder, arr_type, in_arr)
        in_arr = eqie__magtp.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        rrj__qzs = context.make_helper(builder, arr_type, in_arr)
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='list_string_array_to_info')
        return builder.call(luobi__yhh, [rrj__qzs.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                gthp__kphq = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for qrih__sjm in arr_typ.data:
                    gthp__kphq += get_types(qrih__sjm)
                return gthp__kphq
            elif isinstance(arr_typ, (types.Array, IntegerArrayType)
                ) or arr_typ == boolean_array:
                return get_types(arr_typ.dtype)
            elif arr_typ == string_array_type:
                return [CTypeEnum.STRING.value]
            elif arr_typ == binary_array_type:
                return [CTypeEnum.BINARY.value]
            elif isinstance(arr_typ, DecimalArrayType):
                return [CTypeEnum.Decimal.value, arr_typ.precision, arr_typ
                    .scale]
            else:
                return [numba_to_c_type(arr_typ)]

        def get_lengths(arr_typ, arr):
            aejx__hwx = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                pjyt__iid = context.make_helper(builder, arr_typ, value=arr)
                hpwwt__mplet = get_lengths(_get_map_arr_data_type(arr_typ),
                    pjyt__iid.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                fgd__jetuk = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                hpwwt__mplet = get_lengths(arr_typ.dtype, fgd__jetuk.data)
                hpwwt__mplet = cgutils.pack_array(builder, [fgd__jetuk.
                    n_arrays] + [builder.extract_value(hpwwt__mplet,
                    rjtd__svl) for rjtd__svl in range(hpwwt__mplet.type.count)]
                    )
            elif isinstance(arr_typ, StructArrayType):
                fgd__jetuk = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                hpwwt__mplet = []
                for rjtd__svl, qrih__sjm in enumerate(arr_typ.data):
                    nji__wsa = get_lengths(qrih__sjm, builder.extract_value
                        (fgd__jetuk.data, rjtd__svl))
                    hpwwt__mplet += [builder.extract_value(nji__wsa,
                        xfit__qwsuw) for xfit__qwsuw in range(nji__wsa.type
                        .count)]
                hpwwt__mplet = cgutils.pack_array(builder, [aejx__hwx,
                    context.get_constant(types.int64, -1)] + hpwwt__mplet)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                hpwwt__mplet = cgutils.pack_array(builder, [aejx__hwx])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return hpwwt__mplet

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                pjyt__iid = context.make_helper(builder, arr_typ, value=arr)
                ldk__vle = get_buffers(_get_map_arr_data_type(arr_typ),
                    pjyt__iid.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                fgd__jetuk = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                tkdg__buqu = get_buffers(arr_typ.dtype, fgd__jetuk.data)
                epot__mquf = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, fgd__jetuk.offsets)
                eryd__jjjx = builder.bitcast(epot__mquf.data, lir.IntType(8
                    ).as_pointer())
                mywdz__icr = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, fgd__jetuk.null_bitmap)
                psfyn__otbti = builder.bitcast(mywdz__icr.data, lir.IntType
                    (8).as_pointer())
                ldk__vle = cgutils.pack_array(builder, [eryd__jjjx,
                    psfyn__otbti] + [builder.extract_value(tkdg__buqu,
                    rjtd__svl) for rjtd__svl in range(tkdg__buqu.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                fgd__jetuk = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                tkdg__buqu = []
                for rjtd__svl, qrih__sjm in enumerate(arr_typ.data):
                    xhm__cobo = get_buffers(qrih__sjm, builder.
                        extract_value(fgd__jetuk.data, rjtd__svl))
                    tkdg__buqu += [builder.extract_value(xhm__cobo,
                        xfit__qwsuw) for xfit__qwsuw in range(xhm__cobo.
                        type.count)]
                mywdz__icr = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, fgd__jetuk.null_bitmap)
                psfyn__otbti = builder.bitcast(mywdz__icr.data, lir.IntType
                    (8).as_pointer())
                ldk__vle = cgutils.pack_array(builder, [psfyn__otbti] +
                    tkdg__buqu)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                bsoip__xuz = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    bsoip__xuz = int128_type
                elif arr_typ == datetime_date_array_type:
                    bsoip__xuz = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                wltiq__prtci = context.make_array(types.Array(bsoip__xuz, 1,
                    'C'))(context, builder, arr.data)
                mywdz__icr = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                vuj__kmeof = builder.bitcast(wltiq__prtci.data, lir.IntType
                    (8).as_pointer())
                psfyn__otbti = builder.bitcast(mywdz__icr.data, lir.IntType
                    (8).as_pointer())
                ldk__vle = cgutils.pack_array(builder, [psfyn__otbti,
                    vuj__kmeof])
            elif arr_typ in (string_array_type, binary_array_type):
                fgd__jetuk = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                xvaq__rxyme = context.make_helper(builder, offset_arr_type,
                    fgd__jetuk.offsets).data
                ompcl__drzfu = context.make_helper(builder, char_arr_type,
                    fgd__jetuk.data).data
                lew__xpvk = context.make_helper(builder,
                    null_bitmap_arr_type, fgd__jetuk.null_bitmap).data
                ldk__vle = cgutils.pack_array(builder, [builder.bitcast(
                    xvaq__rxyme, lir.IntType(8).as_pointer()), builder.
                    bitcast(lew__xpvk, lir.IntType(8).as_pointer()),
                    builder.bitcast(ompcl__drzfu, lir.IntType(8).as_pointer())]
                    )
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                vuj__kmeof = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                vyru__jrx = lir.Constant(lir.IntType(8).as_pointer(), None)
                ldk__vle = cgutils.pack_array(builder, [vyru__jrx, vuj__kmeof])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return ldk__vle

        def get_field_names(arr_typ):
            qeiz__wqfsu = []
            if isinstance(arr_typ, StructArrayType):
                for wrkj__njsvb, ckpw__gop in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    qeiz__wqfsu.append(wrkj__njsvb)
                    qeiz__wqfsu += get_field_names(ckpw__gop)
            elif isinstance(arr_typ, ArrayItemArrayType):
                qeiz__wqfsu += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                qeiz__wqfsu += get_field_names(_get_map_arr_data_type(arr_typ))
            return qeiz__wqfsu
        gthp__kphq = get_types(arr_type)
        ezanc__suf = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in gthp__kphq])
        qraq__hrzs = cgutils.alloca_once_value(builder, ezanc__suf)
        hpwwt__mplet = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, hpwwt__mplet)
        ldk__vle = get_buffers(arr_type, in_arr)
        qiy__dewxz = cgutils.alloca_once_value(builder, ldk__vle)
        qeiz__wqfsu = get_field_names(arr_type)
        if len(qeiz__wqfsu) == 0:
            qeiz__wqfsu = ['irrelevant']
        oqihz__pjyc = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in qeiz__wqfsu])
        cncy__mrugt = cgutils.alloca_once_value(builder, oqihz__pjyc)
        if isinstance(arr_type, MapArrayType):
            qhkao__mol = _get_map_arr_data_type(arr_type)
            niik__qvj = context.make_helper(builder, arr_type, value=in_arr)
            wcii__rhec = niik__qvj.data
        else:
            qhkao__mol = arr_type
            wcii__rhec = in_arr
        tpb__yuzal = context.make_helper(builder, qhkao__mol, wcii__rhec)
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='nested_array_to_info')
        quva__sva = builder.call(luobi__yhh, [builder.bitcast(qraq__hrzs,
            lir.IntType(32).as_pointer()), builder.bitcast(qiy__dewxz, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            cncy__mrugt, lir.IntType(8).as_pointer()), tpb__yuzal.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    if arr_type in (string_array_type, binary_array_type):
        wfwz__knwsa = context.make_helper(builder, arr_type, in_arr)
        qpsi__vnx = ArrayItemArrayType(char_arr_type)
        rrj__qzs = context.make_helper(builder, qpsi__vnx, wfwz__knwsa.data)
        fgd__jetuk = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        xvaq__rxyme = context.make_helper(builder, offset_arr_type,
            fgd__jetuk.offsets).data
        ompcl__drzfu = context.make_helper(builder, char_arr_type,
            fgd__jetuk.data).data
        lew__xpvk = context.make_helper(builder, null_bitmap_arr_type,
            fgd__jetuk.null_bitmap).data
        qga__kiz = builder.zext(builder.load(builder.gep(xvaq__rxyme, [
            fgd__jetuk.n_arrays])), lir.IntType(64))
        wud__eeyc = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='string_array_to_info')
        return builder.call(luobi__yhh, [fgd__jetuk.n_arrays, qga__kiz,
            ompcl__drzfu, xvaq__rxyme, lew__xpvk, rrj__qzs.meminfo, wud__eeyc])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        gsj__fwld = arr.data
        emo__qzrcg = arr.indices
        sig = array_info_type(arr_type.data)
        nrnhd__yld = array_to_info_codegen(context, builder, sig, (
            gsj__fwld,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        ddirr__cizlm = array_to_info_codegen(context, builder, sig, (
            emo__qzrcg,), False)
        zuh__moptz = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, emo__qzrcg)
        psfyn__otbti = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, zuh__moptz.null_bitmap).data
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='dict_str_array_to_info')
        rlk__qafjt = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(luobi__yhh, [nrnhd__yld, ddirr__cizlm, builder.
            bitcast(psfyn__otbti, lir.IntType(8).as_pointer()), rlk__qafjt])
    nmse__tuar = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        scpy__nujjh = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        mge__hjot = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(mge__hjot, 1, 'C')
        nmse__tuar = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if nmse__tuar:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        aejx__hwx = builder.extract_value(arr.shape, 0)
        irq__nsopx = arr_type.dtype
        pltpr__slj = numba_to_c_type(irq__nsopx)
        gse__opejg = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), pltpr__slj))
        if nmse__tuar:
            umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            luobi__yhh = cgutils.get_or_insert_function(builder.module,
                umzk__knq, name='categorical_array_to_info')
            return builder.call(luobi__yhh, [aejx__hwx, builder.bitcast(arr
                .data, lir.IntType(8).as_pointer()), builder.load(
                gse__opejg), scpy__nujjh, arr.meminfo])
        else:
            umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            luobi__yhh = cgutils.get_or_insert_function(builder.module,
                umzk__knq, name='numpy_array_to_info')
            return builder.call(luobi__yhh, [aejx__hwx, builder.bitcast(arr
                .data, lir.IntType(8).as_pointer()), builder.load(
                gse__opejg), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        irq__nsopx = arr_type.dtype
        bsoip__xuz = irq__nsopx
        if isinstance(arr_type, DecimalArrayType):
            bsoip__xuz = int128_type
        if arr_type == datetime_date_array_type:
            bsoip__xuz = types.int64
        wltiq__prtci = context.make_array(types.Array(bsoip__xuz, 1, 'C'))(
            context, builder, arr.data)
        aejx__hwx = builder.extract_value(wltiq__prtci.shape, 0)
        kprw__avgw = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        pltpr__slj = numba_to_c_type(irq__nsopx)
        gse__opejg = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), pltpr__slj))
        if isinstance(arr_type, DecimalArrayType):
            umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            luobi__yhh = cgutils.get_or_insert_function(builder.module,
                umzk__knq, name='decimal_array_to_info')
            return builder.call(luobi__yhh, [aejx__hwx, builder.bitcast(
                wltiq__prtci.data, lir.IntType(8).as_pointer()), builder.
                load(gse__opejg), builder.bitcast(kprw__avgw.data, lir.
                IntType(8).as_pointer()), wltiq__prtci.meminfo, kprw__avgw.
                meminfo, context.get_constant(types.int32, arr_type.
                precision), context.get_constant(types.int32, arr_type.scale)])
        else:
            umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            luobi__yhh = cgutils.get_or_insert_function(builder.module,
                umzk__knq, name='nullable_array_to_info')
            return builder.call(luobi__yhh, [aejx__hwx, builder.bitcast(
                wltiq__prtci.data, lir.IntType(8).as_pointer()), builder.
                load(gse__opejg), builder.bitcast(kprw__avgw.data, lir.
                IntType(8).as_pointer()), wltiq__prtci.meminfo, kprw__avgw.
                meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        besie__dzu = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        jgc__kyl = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        aejx__hwx = builder.extract_value(besie__dzu.shape, 0)
        pltpr__slj = numba_to_c_type(arr_type.arr_type.dtype)
        gse__opejg = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), pltpr__slj))
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='interval_array_to_info')
        return builder.call(luobi__yhh, [aejx__hwx, builder.bitcast(
            besie__dzu.data, lir.IntType(8).as_pointer()), builder.bitcast(
            jgc__kyl.data, lir.IntType(8).as_pointer()), builder.load(
            gse__opejg), besie__dzu.meminfo, jgc__kyl.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    oidxn__zakn = cgutils.alloca_once(builder, lir.IntType(64))
    vuj__kmeof = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    gmpo__sua = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    umzk__knq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64).as_pointer(), lir.IntType(8).as_pointer().
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    luobi__yhh = cgutils.get_or_insert_function(builder.module, umzk__knq,
        name='info_to_numpy_array')
    builder.call(luobi__yhh, [in_info, oidxn__zakn, vuj__kmeof, gmpo__sua])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    mrn__rmx = context.get_value_type(types.intp)
    ggui__mmxk = cgutils.pack_array(builder, [builder.load(oidxn__zakn)],
        ty=mrn__rmx)
    nes__cwxz = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    hjmzx__nig = cgutils.pack_array(builder, [nes__cwxz], ty=mrn__rmx)
    ompcl__drzfu = builder.bitcast(builder.load(vuj__kmeof), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=ompcl__drzfu, shape=
        ggui__mmxk, strides=hjmzx__nig, itemsize=nes__cwxz, meminfo=builder
        .load(gmpo__sua))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    jigdr__tvhne = context.make_helper(builder, arr_type)
    umzk__knq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(8).as_pointer().as_pointer()])
    luobi__yhh = cgutils.get_or_insert_function(builder.module, umzk__knq,
        name='info_to_list_string_array')
    builder.call(luobi__yhh, [in_info, jigdr__tvhne._get_ptr_by_name(
        'meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return jigdr__tvhne._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    roi__zjr = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        fdni__kfyyb = lengths_pos
        rbnmj__fiegn = infos_pos
        igatr__kttos, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        gkgjp__lthq = ArrayItemArrayPayloadType(arr_typ)
        wmus__zozk = context.get_data_type(gkgjp__lthq)
        fzf__qfu = context.get_abi_sizeof(wmus__zozk)
        mjf__yuzd = define_array_item_dtor(context, builder, arr_typ,
            gkgjp__lthq)
        wajtp__eytwl = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, fzf__qfu), mjf__yuzd)
        wfvj__umc = context.nrt.meminfo_data(builder, wajtp__eytwl)
        gfjgy__ucif = builder.bitcast(wfvj__umc, wmus__zozk.as_pointer())
        fgd__jetuk = cgutils.create_struct_proxy(gkgjp__lthq)(context, builder)
        fgd__jetuk.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), fdni__kfyyb)
        fgd__jetuk.data = igatr__kttos
        hfwf__eefq = builder.load(array_infos_ptr)
        wqla__nim = builder.bitcast(builder.extract_value(hfwf__eefq,
            rbnmj__fiegn), roi__zjr)
        fgd__jetuk.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, wqla__nim)
        vkoyp__dvrf = builder.bitcast(builder.extract_value(hfwf__eefq, 
            rbnmj__fiegn + 1), roi__zjr)
        fgd__jetuk.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, vkoyp__dvrf)
        builder.store(fgd__jetuk._getvalue(), gfjgy__ucif)
        rrj__qzs = context.make_helper(builder, arr_typ)
        rrj__qzs.meminfo = wajtp__eytwl
        return rrj__qzs._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        ixucq__vrik = []
        rbnmj__fiegn = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for onti__ejf in arr_typ.data:
            igatr__kttos, lengths_pos, infos_pos = nested_to_array(context,
                builder, onti__ejf, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            ixucq__vrik.append(igatr__kttos)
        gkgjp__lthq = StructArrayPayloadType(arr_typ.data)
        wmus__zozk = context.get_value_type(gkgjp__lthq)
        fzf__qfu = context.get_abi_sizeof(wmus__zozk)
        mjf__yuzd = define_struct_arr_dtor(context, builder, arr_typ,
            gkgjp__lthq)
        wajtp__eytwl = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, fzf__qfu), mjf__yuzd)
        wfvj__umc = context.nrt.meminfo_data(builder, wajtp__eytwl)
        gfjgy__ucif = builder.bitcast(wfvj__umc, wmus__zozk.as_pointer())
        fgd__jetuk = cgutils.create_struct_proxy(gkgjp__lthq)(context, builder)
        fgd__jetuk.data = cgutils.pack_array(builder, ixucq__vrik
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, ixucq__vrik)
        hfwf__eefq = builder.load(array_infos_ptr)
        vkoyp__dvrf = builder.bitcast(builder.extract_value(hfwf__eefq,
            rbnmj__fiegn), roi__zjr)
        fgd__jetuk.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, vkoyp__dvrf)
        builder.store(fgd__jetuk._getvalue(), gfjgy__ucif)
        mgphj__gpewp = context.make_helper(builder, arr_typ)
        mgphj__gpewp.meminfo = wajtp__eytwl
        return mgphj__gpewp._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        hfwf__eefq = builder.load(array_infos_ptr)
        uaje__lzcrx = builder.bitcast(builder.extract_value(hfwf__eefq,
            infos_pos), roi__zjr)
        wfwz__knwsa = context.make_helper(builder, arr_typ)
        qpsi__vnx = ArrayItemArrayType(char_arr_type)
        rrj__qzs = context.make_helper(builder, qpsi__vnx)
        umzk__knq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='info_to_string_array')
        builder.call(luobi__yhh, [uaje__lzcrx, rrj__qzs._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        wfwz__knwsa.data = rrj__qzs._getvalue()
        return wfwz__knwsa._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        hfwf__eefq = builder.load(array_infos_ptr)
        cllri__kooy = builder.bitcast(builder.extract_value(hfwf__eefq, 
            infos_pos + 1), roi__zjr)
        return _lower_info_to_array_numpy(arr_typ, context, builder,
            cllri__kooy), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        bsoip__xuz = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            bsoip__xuz = int128_type
        elif arr_typ == datetime_date_array_type:
            bsoip__xuz = types.int64
        hfwf__eefq = builder.load(array_infos_ptr)
        vkoyp__dvrf = builder.bitcast(builder.extract_value(hfwf__eefq,
            infos_pos), roi__zjr)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, vkoyp__dvrf)
        cllri__kooy = builder.bitcast(builder.extract_value(hfwf__eefq, 
            infos_pos + 1), roi__zjr)
        arr.data = _lower_info_to_array_numpy(types.Array(bsoip__xuz, 1,
            'C'), context, builder, cllri__kooy)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, ezyez__wsz = args
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        return _lower_info_to_array_list_string_array(arr_type, context,
            builder, in_info)
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType,
        StructArrayType, TupleArrayType)):

        def get_num_arrays(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 1 + get_num_arrays(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_arrays(onti__ejf) for onti__ejf in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(onti__ejf) for onti__ejf in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            bpmc__exvp = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            bpmc__exvp = _get_map_arr_data_type(arr_type)
        else:
            bpmc__exvp = arr_type
        qyo__xqqkd = get_num_arrays(bpmc__exvp)
        hpwwt__mplet = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), 0) for ezyez__wsz in range(qyo__xqqkd)])
        lengths_ptr = cgutils.alloca_once_value(builder, hpwwt__mplet)
        vyru__jrx = lir.Constant(lir.IntType(8).as_pointer(), None)
        liar__mjkij = cgutils.pack_array(builder, [vyru__jrx for ezyez__wsz in
            range(get_num_infos(bpmc__exvp))])
        array_infos_ptr = cgutils.alloca_once_value(builder, liar__mjkij)
        umzk__knq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='info_to_nested_array')
        builder.call(luobi__yhh, [in_info, builder.bitcast(lengths_ptr, lir
            .IntType(64).as_pointer()), builder.bitcast(array_infos_ptr,
            lir.IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, ezyez__wsz, ezyez__wsz = nested_to_array(context, builder,
            bpmc__exvp, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            eqie__magtp = context.make_helper(builder, arr_type)
            eqie__magtp.data = arr
            context.nrt.incref(builder, bpmc__exvp, arr)
            arr = eqie__magtp._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, bpmc__exvp)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        wfwz__knwsa = context.make_helper(builder, arr_type)
        qpsi__vnx = ArrayItemArrayType(char_arr_type)
        rrj__qzs = context.make_helper(builder, qpsi__vnx)
        umzk__knq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='info_to_string_array')
        builder.call(luobi__yhh, [in_info, rrj__qzs._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        wfwz__knwsa.data = rrj__qzs._getvalue()
        return wfwz__knwsa._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='get_nested_info')
        nrnhd__yld = builder.call(luobi__yhh, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        ddirr__cizlm = builder.call(luobi__yhh, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        mhq__slkk = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        mhq__slkk.data = info_to_array_codegen(context, builder, sig, (
            nrnhd__yld, context.get_constant_null(arr_type.data)))
        wbg__uny = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = wbg__uny(array_info_type, wbg__uny)
        mhq__slkk.indices = info_to_array_codegen(context, builder, sig, (
            ddirr__cizlm, context.get_constant_null(wbg__uny)))
        umzk__knq = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='get_has_global_dictionary')
        rlk__qafjt = builder.call(luobi__yhh, [in_info])
        mhq__slkk.has_global_dictionary = builder.trunc(rlk__qafjt, cgutils
            .bool_t)
        return mhq__slkk._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        mge__hjot = get_categories_int_type(arr_type.dtype)
        lxh__ygbbs = types.Array(mge__hjot, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(lxh__ygbbs, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            erfx__aqdo = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(erfx__aqdo))
            int_type = arr_type.dtype.int_type
            punn__exk = bodo.typeof(erfx__aqdo)
            uyg__pcbtx = context.get_constant_generic(builder, punn__exk,
                erfx__aqdo)
            irq__nsopx = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(punn__exk), [uyg__pcbtx])
        else:
            irq__nsopx = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, irq__nsopx)
        out_arr.dtype = irq__nsopx
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        ompcl__drzfu = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = ompcl__drzfu
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        bsoip__xuz = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            bsoip__xuz = int128_type
        elif arr_type == datetime_date_array_type:
            bsoip__xuz = types.int64
        amf__xdjo = types.Array(bsoip__xuz, 1, 'C')
        wltiq__prtci = context.make_array(amf__xdjo)(context, builder)
        xbikj__jwhko = types.Array(types.uint8, 1, 'C')
        tzhgx__jqbzd = context.make_array(xbikj__jwhko)(context, builder)
        oidxn__zakn = cgutils.alloca_once(builder, lir.IntType(64))
        yhy__rvy = cgutils.alloca_once(builder, lir.IntType(64))
        vuj__kmeof = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        tsoa__cqj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        gmpo__sua = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        fiki__jika = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        umzk__knq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='info_to_nullable_array')
        builder.call(luobi__yhh, [in_info, oidxn__zakn, yhy__rvy,
            vuj__kmeof, tsoa__cqj, gmpo__sua, fiki__jika])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        mrn__rmx = context.get_value_type(types.intp)
        ggui__mmxk = cgutils.pack_array(builder, [builder.load(oidxn__zakn)
            ], ty=mrn__rmx)
        nes__cwxz = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(bsoip__xuz)))
        hjmzx__nig = cgutils.pack_array(builder, [nes__cwxz], ty=mrn__rmx)
        ompcl__drzfu = builder.bitcast(builder.load(vuj__kmeof), context.
            get_data_type(bsoip__xuz).as_pointer())
        numba.np.arrayobj.populate_array(wltiq__prtci, data=ompcl__drzfu,
            shape=ggui__mmxk, strides=hjmzx__nig, itemsize=nes__cwxz,
            meminfo=builder.load(gmpo__sua))
        arr.data = wltiq__prtci._getvalue()
        ggui__mmxk = cgutils.pack_array(builder, [builder.load(yhy__rvy)],
            ty=mrn__rmx)
        nes__cwxz = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(types.uint8)))
        hjmzx__nig = cgutils.pack_array(builder, [nes__cwxz], ty=mrn__rmx)
        ompcl__drzfu = builder.bitcast(builder.load(tsoa__cqj), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(tzhgx__jqbzd, data=ompcl__drzfu,
            shape=ggui__mmxk, strides=hjmzx__nig, itemsize=nes__cwxz,
            meminfo=builder.load(fiki__jika))
        arr.null_bitmap = tzhgx__jqbzd._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        besie__dzu = context.make_array(arr_type.arr_type)(context, builder)
        jgc__kyl = context.make_array(arr_type.arr_type)(context, builder)
        oidxn__zakn = cgutils.alloca_once(builder, lir.IntType(64))
        cbg__crbn = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        dykfr__oavs = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        uic__trciy = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        knxh__qsw = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        umzk__knq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='info_to_interval_array')
        builder.call(luobi__yhh, [in_info, oidxn__zakn, cbg__crbn,
            dykfr__oavs, uic__trciy, knxh__qsw])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        mrn__rmx = context.get_value_type(types.intp)
        ggui__mmxk = cgutils.pack_array(builder, [builder.load(oidxn__zakn)
            ], ty=mrn__rmx)
        nes__cwxz = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(arr_type.arr_type.dtype)))
        hjmzx__nig = cgutils.pack_array(builder, [nes__cwxz], ty=mrn__rmx)
        peoy__zhnjt = builder.bitcast(builder.load(cbg__crbn), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(besie__dzu, data=peoy__zhnjt,
            shape=ggui__mmxk, strides=hjmzx__nig, itemsize=nes__cwxz,
            meminfo=builder.load(uic__trciy))
        arr.left = besie__dzu._getvalue()
        akk__jopin = builder.bitcast(builder.load(dykfr__oavs), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(jgc__kyl, data=akk__jopin, shape=
            ggui__mmxk, strides=hjmzx__nig, itemsize=nes__cwxz, meminfo=
            builder.load(knxh__qsw))
        arr.right = jgc__kyl._getvalue()
        return arr._getvalue()
    raise_bodo_error(f'info_to_array(): array type {arr_type} is not supported'
        )


@intrinsic
def info_to_array(typingctx, info_type, array_type):
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    assert info_type == array_info_type, 'info_to_array: expected info type'
    return arr_type(info_type, array_type), info_to_array_codegen


@intrinsic
def test_alloc_np(typingctx, len_typ, arr_type):
    array_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type

    def codegen(context, builder, sig, args):
        aejx__hwx, ezyez__wsz = args
        pltpr__slj = numba_to_c_type(array_type.dtype)
        gse__opejg = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), pltpr__slj))
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='alloc_numpy')
        return builder.call(luobi__yhh, [aejx__hwx, builder.load(gse__opejg)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        aejx__hwx, usn__srk = args
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='alloc_string_array')
        return builder.call(luobi__yhh, [aejx__hwx, usn__srk])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    flzbm__vbri, = args
    kxjss__isly = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], flzbm__vbri)
    umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer().as_pointer(), lir.IntType(64)])
    luobi__yhh = cgutils.get_or_insert_function(builder.module, umzk__knq,
        name='arr_info_list_to_table')
    return builder.call(luobi__yhh, [kxjss__isly.data, kxjss__isly.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='info_from_table')
        return builder.call(luobi__yhh, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    unl__lngd = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cvhw__opsq, fnzqa__boz, ezyez__wsz = args
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='info_from_table')
        dkvl__npj = cgutils.create_struct_proxy(unl__lngd)(context, builder)
        dkvl__npj.parent = cgutils.get_null_value(dkvl__npj.parent.type)
        qrs__bnvv = context.make_array(table_idx_arr_t)(context, builder,
            fnzqa__boz)
        qnq__llpg = context.get_constant(types.int64, -1)
        bhcx__sdtj = context.get_constant(types.int64, 0)
        dwc__qka = cgutils.alloca_once_value(builder, bhcx__sdtj)
        for t, gfi__swfpa in unl__lngd.type_to_blk.items():
            omdqd__lvtti = context.get_constant(types.int64, len(unl__lngd.
                block_to_arr_ind[gfi__swfpa]))
            ezyez__wsz, kyb__kkr = ListInstance.allocate_ex(context,
                builder, types.List(t), omdqd__lvtti)
            kyb__kkr.size = omdqd__lvtti
            jvdjc__wezmj = context.make_constant_array(builder, types.Array
                (types.int64, 1, 'C'), np.array(unl__lngd.block_to_arr_ind[
                gfi__swfpa], dtype=np.int64))
            psn__vil = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, jvdjc__wezmj)
            with cgutils.for_range(builder, omdqd__lvtti) as sjggv__jecc:
                rjtd__svl = sjggv__jecc.index
                alph__srfj = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'), psn__vil,
                    rjtd__svl)
                zfeyk__zqd = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, qrs__bnvv, alph__srfj)
                taepz__won = builder.icmp_unsigned('!=', zfeyk__zqd, qnq__llpg)
                with builder.if_else(taepz__won) as (vsx__juxc, xoy__jjg):
                    with vsx__juxc:
                        qwty__lzhcx = builder.call(luobi__yhh, [cvhw__opsq,
                            zfeyk__zqd])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            qwty__lzhcx])
                        kyb__kkr.inititem(rjtd__svl, arr, incref=False)
                        aejx__hwx = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(aejx__hwx, dwc__qka)
                    with xoy__jjg:
                        igbf__cno = context.get_constant_null(t)
                        kyb__kkr.inititem(rjtd__svl, igbf__cno, incref=False)
            setattr(dkvl__npj, f'block_{gfi__swfpa}', kyb__kkr.value)
        dkvl__npj.len = builder.load(dwc__qka)
        return dkvl__npj._getvalue()
    return unl__lngd(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    unl__lngd = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        lug__fbu, ezyez__wsz = args
        mzn__ncbhh = cgutils.create_struct_proxy(unl__lngd)(context,
            builder, lug__fbu)
        if unl__lngd.has_runtime_cols:
            roo__qjcrn = lir.Constant(lir.IntType(64), 0)
            for gfi__swfpa, t in enumerate(unl__lngd.arr_types):
                ywcws__ndoyr = getattr(mzn__ncbhh, f'block_{gfi__swfpa}')
                vqc__shw = ListInstance(context, builder, types.List(t),
                    ywcws__ndoyr)
                roo__qjcrn = builder.add(roo__qjcrn, vqc__shw.size)
        else:
            roo__qjcrn = lir.Constant(lir.IntType(64), len(unl__lngd.arr_types)
                )
        ezyez__wsz, ewde__ukk = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), roo__qjcrn)
        ewde__ukk.size = roo__qjcrn
        if unl__lngd.has_runtime_cols:
            nwvvs__ozgsf = lir.Constant(lir.IntType(64), 0)
            for gfi__swfpa, t in enumerate(unl__lngd.arr_types):
                ywcws__ndoyr = getattr(mzn__ncbhh, f'block_{gfi__swfpa}')
                vqc__shw = ListInstance(context, builder, types.List(t),
                    ywcws__ndoyr)
                omdqd__lvtti = vqc__shw.size
                with cgutils.for_range(builder, omdqd__lvtti) as sjggv__jecc:
                    rjtd__svl = sjggv__jecc.index
                    arr = vqc__shw.getitem(rjtd__svl)
                    zbn__rlr = signature(array_info_type, t)
                    yxn__sxv = arr,
                    uqi__clxs = array_to_info_codegen(context, builder,
                        zbn__rlr, yxn__sxv)
                    ewde__ukk.inititem(builder.add(nwvvs__ozgsf, rjtd__svl),
                        uqi__clxs, incref=False)
                nwvvs__ozgsf = builder.add(nwvvs__ozgsf, omdqd__lvtti)
        else:
            for t, gfi__swfpa in unl__lngd.type_to_blk.items():
                omdqd__lvtti = context.get_constant(types.int64, len(
                    unl__lngd.block_to_arr_ind[gfi__swfpa]))
                ywcws__ndoyr = getattr(mzn__ncbhh, f'block_{gfi__swfpa}')
                vqc__shw = ListInstance(context, builder, types.List(t),
                    ywcws__ndoyr)
                jvdjc__wezmj = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(unl__lngd.
                    block_to_arr_ind[gfi__swfpa], dtype=np.int64))
                psn__vil = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, jvdjc__wezmj)
                with cgutils.for_range(builder, omdqd__lvtti) as sjggv__jecc:
                    rjtd__svl = sjggv__jecc.index
                    alph__srfj = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        psn__vil, rjtd__svl)
                    bhou__wglx = signature(types.none, unl__lngd, types.
                        List(t), types.int64, types.int64)
                    lqf__qbge = lug__fbu, ywcws__ndoyr, rjtd__svl, alph__srfj
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, bhou__wglx, lqf__qbge)
                    arr = vqc__shw.getitem(rjtd__svl)
                    zbn__rlr = signature(array_info_type, t)
                    yxn__sxv = arr,
                    uqi__clxs = array_to_info_codegen(context, builder,
                        zbn__rlr, yxn__sxv)
                    ewde__ukk.inititem(alph__srfj, uqi__clxs, incref=False)
        ptbi__pzwc = ewde__ukk.value
        ydy__aond = signature(table_type, types.List(array_info_type))
        lde__shigf = ptbi__pzwc,
        cvhw__opsq = arr_info_list_to_table_codegen(context, builder,
            ydy__aond, lde__shigf)
        context.nrt.decref(builder, types.List(array_info_type), ptbi__pzwc)
        return cvhw__opsq
    return table_type(unl__lngd, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='delete_table')
        builder.call(luobi__yhh, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='shuffle_table')
        quva__sva = builder.call(luobi__yhh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    return table_type(table_t, types.int64, types.boolean, types.int32
        ), codegen


class ShuffleInfoType(types.Type):

    def __init__(self):
        super(ShuffleInfoType, self).__init__(name='ShuffleInfoType()')


shuffle_info_type = ShuffleInfoType()
register_model(ShuffleInfoType)(models.OpaqueModel)
get_shuffle_info = types.ExternalFunction('get_shuffle_info',
    shuffle_info_type(table_type))


@intrinsic
def delete_shuffle_info(typingctx, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[0] == types.none:
            return
        umzk__knq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='delete_shuffle_info')
        return builder.call(luobi__yhh, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='reverse_shuffle_table')
        return builder.call(luobi__yhh, args)
    return table_type(table_type, shuffle_info_t), codegen


@intrinsic
def get_null_shuffle_info(typingctx):

    def codegen(context, builder, sig, args):
        return context.get_constant_null(sig.return_type)
    return shuffle_info_type(), codegen


@intrinsic
def hash_join_table(typingctx, left_table_t, right_table_t, left_parallel_t,
    right_parallel_t, n_keys_t, n_data_left_t, n_data_right_t, same_vect_t,
    same_need_typechange_t, is_left_t, is_right_t, is_join_t,
    optional_col_t, indicator, _bodo_na_equal, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len):
    assert left_table_t == table_type
    assert right_table_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='hash_join_table')
        quva__sva = builder.call(luobi__yhh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.int64, types.int64, types.int64, types.voidptr,
        types.voidptr, types.boolean, types.boolean, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.int64, types.voidptr, types.int64), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='sort_values_table')
        quva__sva = builder.call(luobi__yhh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='sample_table')
        quva__sva = builder.call(luobi__yhh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='shuffle_renormalization')
        quva__sva = builder.call(luobi__yhh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='shuffle_renormalization_group')
        quva__sva = builder.call(luobi__yhh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='drop_duplicates_table')
        quva__sva = builder.call(luobi__yhh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    return table_type(table_t, types.boolean, types.int64, types.int64,
        types.boolean, types.boolean), codegen


@intrinsic
def pivot_groupby_and_aggregate(typingctx, table_t, n_keys_t,
    dispatch_table_t, dispatch_info_t, input_has_index, ftypes,
    func_offsets, udf_n_redvars, is_parallel, is_crosstab, skipdropna_t,
    return_keys, return_index, update_cb, combine_cb, eval_cb,
    udf_table_dummy_t):
    assert table_t == table_type
    assert dispatch_table_t == table_type
    assert dispatch_info_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='pivot_groupby_and_aggregate')
        quva__sva = builder.call(luobi__yhh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    return table_type(table_t, types.int64, table_t, table_t, types.boolean,
        types.voidptr, types.voidptr, types.voidptr, types.boolean, types.
        boolean, types.boolean, types.boolean, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, table_t), codegen


@intrinsic
def groupby_and_aggregate(typingctx, table_t, n_keys_t, input_has_index,
    ftypes, func_offsets, udf_n_redvars, is_parallel, skipdropna_t,
    shift_periods_t, transform_func, head_n, return_keys, return_index,
    dropna, update_cb, combine_cb, eval_cb, general_udfs_cb, udf_table_dummy_t
    ):
    assert table_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        luobi__yhh = cgutils.get_or_insert_function(builder.module,
            umzk__knq, name='groupby_and_aggregate')
        quva__sva = builder.call(luobi__yhh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return quva__sva
    return table_type(table_t, types.int64, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        int64, types.int64, types.int64, types.boolean, types.boolean,
        types.boolean, types.voidptr, types.voidptr, types.voidptr, types.
        voidptr, table_t), codegen


get_groupby_labels = types.ExternalFunction('get_groupby_labels', types.
    int64(table_type, types.voidptr, types.voidptr, types.boolean, types.bool_)
    )
_array_isin = types.ExternalFunction('array_isin', types.void(
    array_info_type, array_info_type, array_info_type, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def array_isin(out_arr, in_arr, in_values, is_parallel):
    in_arr = decode_if_dict_array(in_arr)
    in_values = decode_if_dict_array(in_values)
    cgf__zzu = array_to_info(in_arr)
    mlrx__gil = array_to_info(in_values)
    txeg__mqxxr = array_to_info(out_arr)
    ufyj__ppwh = arr_info_list_to_table([cgf__zzu, mlrx__gil, txeg__mqxxr])
    _array_isin(txeg__mqxxr, cgf__zzu, mlrx__gil, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(ufyj__ppwh)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    cgf__zzu = array_to_info(in_arr)
    txeg__mqxxr = array_to_info(out_arr)
    _get_search_regex(cgf__zzu, case, pat, txeg__mqxxr)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    rywm__pnji = col_array_typ.dtype
    if isinstance(rywm__pnji, types.Number) or rywm__pnji in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                dkvl__npj, qum__zybcq = args
                dkvl__npj = builder.bitcast(dkvl__npj, lir.IntType(8).
                    as_pointer().as_pointer())
                nzzb__oqxy = lir.Constant(lir.IntType(64), c_ind)
                yvbar__ybk = builder.load(builder.gep(dkvl__npj, [nzzb__oqxy]))
                yvbar__ybk = builder.bitcast(yvbar__ybk, context.
                    get_data_type(rywm__pnji).as_pointer())
                return builder.load(builder.gep(yvbar__ybk, [qum__zybcq]))
            return rywm__pnji(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                dkvl__npj, qum__zybcq = args
                dkvl__npj = builder.bitcast(dkvl__npj, lir.IntType(8).
                    as_pointer().as_pointer())
                nzzb__oqxy = lir.Constant(lir.IntType(64), c_ind)
                yvbar__ybk = builder.load(builder.gep(dkvl__npj, [nzzb__oqxy]))
                umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                bal__cmql = cgutils.get_or_insert_function(builder.module,
                    umzk__knq, name='array_info_getitem')
                yddk__zuq = cgutils.alloca_once(builder, lir.IntType(64))
                args = yvbar__ybk, qum__zybcq, yddk__zuq
                vuj__kmeof = builder.call(bal__cmql, args)
                return context.make_tuple(builder, sig.return_type, [
                    vuj__kmeof, builder.load(yddk__zuq)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                bzq__rnc = lir.Constant(lir.IntType(64), 1)
                haol__iqkh = lir.Constant(lir.IntType(64), 2)
                dkvl__npj, qum__zybcq = args
                dkvl__npj = builder.bitcast(dkvl__npj, lir.IntType(8).
                    as_pointer().as_pointer())
                nzzb__oqxy = lir.Constant(lir.IntType(64), c_ind)
                yvbar__ybk = builder.load(builder.gep(dkvl__npj, [nzzb__oqxy]))
                umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64)])
                eho__siqk = cgutils.get_or_insert_function(builder.module,
                    umzk__knq, name='get_nested_info')
                args = yvbar__ybk, haol__iqkh
                tpyp__sjsv = builder.call(eho__siqk, args)
                umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer()])
                kqwp__zja = cgutils.get_or_insert_function(builder.module,
                    umzk__knq, name='array_info_getdata1')
                args = tpyp__sjsv,
                xsp__qbbl = builder.call(kqwp__zja, args)
                xsp__qbbl = builder.bitcast(xsp__qbbl, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                jgxnx__baswh = builder.sext(builder.load(builder.gep(
                    xsp__qbbl, [qum__zybcq])), lir.IntType(64))
                args = yvbar__ybk, bzq__rnc
                teu__lbkhd = builder.call(eho__siqk, args)
                umzk__knq = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                bal__cmql = cgutils.get_or_insert_function(builder.module,
                    umzk__knq, name='array_info_getitem')
                yddk__zuq = cgutils.alloca_once(builder, lir.IntType(64))
                args = teu__lbkhd, jgxnx__baswh, yddk__zuq
                vuj__kmeof = builder.call(bal__cmql, args)
                return context.make_tuple(builder, sig.return_type, [
                    vuj__kmeof, builder.load(yddk__zuq)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{rywm__pnji}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                povpl__qvs, qum__zybcq = args
                povpl__qvs = builder.bitcast(povpl__qvs, lir.IntType(8).
                    as_pointer().as_pointer())
                nzzb__oqxy = lir.Constant(lir.IntType(64), c_ind)
                yvbar__ybk = builder.load(builder.gep(povpl__qvs, [nzzb__oqxy])
                    )
                lew__xpvk = builder.bitcast(yvbar__ybk, context.
                    get_data_type(types.bool_).as_pointer())
                shde__ihycc = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    lew__xpvk, qum__zybcq)
                hfoeh__gyw = builder.icmp_unsigned('!=', shde__ihycc, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(hfoeh__gyw, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        rywm__pnji = col_array_dtype.dtype
        if rywm__pnji in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    dkvl__npj, qum__zybcq = args
                    dkvl__npj = builder.bitcast(dkvl__npj, lir.IntType(8).
                        as_pointer().as_pointer())
                    nzzb__oqxy = lir.Constant(lir.IntType(64), c_ind)
                    yvbar__ybk = builder.load(builder.gep(dkvl__npj, [
                        nzzb__oqxy]))
                    yvbar__ybk = builder.bitcast(yvbar__ybk, context.
                        get_data_type(rywm__pnji).as_pointer())
                    gitj__gsnm = builder.load(builder.gep(yvbar__ybk, [
                        qum__zybcq]))
                    hfoeh__gyw = builder.icmp_unsigned('!=', gitj__gsnm,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(hfoeh__gyw, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(rywm__pnji, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    dkvl__npj, qum__zybcq = args
                    dkvl__npj = builder.bitcast(dkvl__npj, lir.IntType(8).
                        as_pointer().as_pointer())
                    nzzb__oqxy = lir.Constant(lir.IntType(64), c_ind)
                    yvbar__ybk = builder.load(builder.gep(dkvl__npj, [
                        nzzb__oqxy]))
                    yvbar__ybk = builder.bitcast(yvbar__ybk, context.
                        get_data_type(rywm__pnji).as_pointer())
                    gitj__gsnm = builder.load(builder.gep(yvbar__ybk, [
                        qum__zybcq]))
                    jynp__hjpje = signature(types.bool_, rywm__pnji)
                    shde__ihycc = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, jynp__hjpje, (gitj__gsnm,))
                    return builder.not_(builder.sext(shde__ihycc, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
