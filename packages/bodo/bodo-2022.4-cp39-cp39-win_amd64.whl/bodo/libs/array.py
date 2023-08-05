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
        auec__qnxqg = context.make_helper(builder, arr_type, in_arr)
        in_arr = auec__qnxqg.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        tdq__zqf = context.make_helper(builder, arr_type, in_arr)
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='list_string_array_to_info')
        return builder.call(cfot__myy, [tdq__zqf.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                exxbw__zbp = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for dlmj__okkce in arr_typ.data:
                    exxbw__zbp += get_types(dlmj__okkce)
                return exxbw__zbp
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
            axgpb__his = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                mtlpi__qsg = context.make_helper(builder, arr_typ, value=arr)
                tknsd__wrsb = get_lengths(_get_map_arr_data_type(arr_typ),
                    mtlpi__qsg.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                ekff__sln = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                tknsd__wrsb = get_lengths(arr_typ.dtype, ekff__sln.data)
                tknsd__wrsb = cgutils.pack_array(builder, [ekff__sln.
                    n_arrays] + [builder.extract_value(tknsd__wrsb,
                    pwqv__cogvx) for pwqv__cogvx in range(tknsd__wrsb.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                ekff__sln = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                tknsd__wrsb = []
                for pwqv__cogvx, dlmj__okkce in enumerate(arr_typ.data):
                    tpzm__ikb = get_lengths(dlmj__okkce, builder.
                        extract_value(ekff__sln.data, pwqv__cogvx))
                    tknsd__wrsb += [builder.extract_value(tpzm__ikb,
                        rff__bpsn) for rff__bpsn in range(tpzm__ikb.type.count)
                        ]
                tknsd__wrsb = cgutils.pack_array(builder, [axgpb__his,
                    context.get_constant(types.int64, -1)] + tknsd__wrsb)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                tknsd__wrsb = cgutils.pack_array(builder, [axgpb__his])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return tknsd__wrsb

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                mtlpi__qsg = context.make_helper(builder, arr_typ, value=arr)
                xds__qffq = get_buffers(_get_map_arr_data_type(arr_typ),
                    mtlpi__qsg.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                ekff__sln = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                sjue__ycxvn = get_buffers(arr_typ.dtype, ekff__sln.data)
                zkc__tve = context.make_array(types.Array(offset_type, 1, 'C')
                    )(context, builder, ekff__sln.offsets)
                hah__oxcvb = builder.bitcast(zkc__tve.data, lir.IntType(8).
                    as_pointer())
                baw__xnve = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, ekff__sln.null_bitmap)
                rlall__roms = builder.bitcast(baw__xnve.data, lir.IntType(8
                    ).as_pointer())
                xds__qffq = cgutils.pack_array(builder, [hah__oxcvb,
                    rlall__roms] + [builder.extract_value(sjue__ycxvn,
                    pwqv__cogvx) for pwqv__cogvx in range(sjue__ycxvn.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                ekff__sln = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                sjue__ycxvn = []
                for pwqv__cogvx, dlmj__okkce in enumerate(arr_typ.data):
                    hkd__hpw = get_buffers(dlmj__okkce, builder.
                        extract_value(ekff__sln.data, pwqv__cogvx))
                    sjue__ycxvn += [builder.extract_value(hkd__hpw,
                        rff__bpsn) for rff__bpsn in range(hkd__hpw.type.count)]
                baw__xnve = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, ekff__sln.null_bitmap)
                rlall__roms = builder.bitcast(baw__xnve.data, lir.IntType(8
                    ).as_pointer())
                xds__qffq = cgutils.pack_array(builder, [rlall__roms] +
                    sjue__ycxvn)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                naat__qsy = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    naat__qsy = int128_type
                elif arr_typ == datetime_date_array_type:
                    naat__qsy = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                yofc__aih = context.make_array(types.Array(naat__qsy, 1, 'C'))(
                    context, builder, arr.data)
                baw__xnve = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, arr.null_bitmap)
                bjfb__abkl = builder.bitcast(yofc__aih.data, lir.IntType(8)
                    .as_pointer())
                rlall__roms = builder.bitcast(baw__xnve.data, lir.IntType(8
                    ).as_pointer())
                xds__qffq = cgutils.pack_array(builder, [rlall__roms,
                    bjfb__abkl])
            elif arr_typ in (string_array_type, binary_array_type):
                ekff__sln = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                pgq__ted = context.make_helper(builder, offset_arr_type,
                    ekff__sln.offsets).data
                xfhml__somkg = context.make_helper(builder, char_arr_type,
                    ekff__sln.data).data
                ozcd__opc = context.make_helper(builder,
                    null_bitmap_arr_type, ekff__sln.null_bitmap).data
                xds__qffq = cgutils.pack_array(builder, [builder.bitcast(
                    pgq__ted, lir.IntType(8).as_pointer()), builder.bitcast
                    (ozcd__opc, lir.IntType(8).as_pointer()), builder.
                    bitcast(xfhml__somkg, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                bjfb__abkl = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                mdw__mwbgn = lir.Constant(lir.IntType(8).as_pointer(), None)
                xds__qffq = cgutils.pack_array(builder, [mdw__mwbgn,
                    bjfb__abkl])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return xds__qffq

        def get_field_names(arr_typ):
            mim__onp = []
            if isinstance(arr_typ, StructArrayType):
                for avx__dlb, cuwv__xsdpk in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    mim__onp.append(avx__dlb)
                    mim__onp += get_field_names(cuwv__xsdpk)
            elif isinstance(arr_typ, ArrayItemArrayType):
                mim__onp += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                mim__onp += get_field_names(_get_map_arr_data_type(arr_typ))
            return mim__onp
        exxbw__zbp = get_types(arr_type)
        mvwp__cufou = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in exxbw__zbp])
        tom__rnm = cgutils.alloca_once_value(builder, mvwp__cufou)
        tknsd__wrsb = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, tknsd__wrsb)
        xds__qffq = get_buffers(arr_type, in_arr)
        kgum__sbpps = cgutils.alloca_once_value(builder, xds__qffq)
        mim__onp = get_field_names(arr_type)
        if len(mim__onp) == 0:
            mim__onp = ['irrelevant']
        tonol__dtozf = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in mim__onp])
        uelm__tws = cgutils.alloca_once_value(builder, tonol__dtozf)
        if isinstance(arr_type, MapArrayType):
            qhg__neafb = _get_map_arr_data_type(arr_type)
            iyr__gegk = context.make_helper(builder, arr_type, value=in_arr)
            yjy__tbl = iyr__gegk.data
        else:
            qhg__neafb = arr_type
            yjy__tbl = in_arr
        tfye__cwhql = context.make_helper(builder, qhg__neafb, yjy__tbl)
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='nested_array_to_info')
        mcf__tmdob = builder.call(cfot__myy, [builder.bitcast(tom__rnm, lir
            .IntType(32).as_pointer()), builder.bitcast(kgum__sbpps, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            uelm__tws, lir.IntType(8).as_pointer()), tfye__cwhql.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
    if arr_type in (string_array_type, binary_array_type):
        tcmzq__wlhde = context.make_helper(builder, arr_type, in_arr)
        vwonh__lkel = ArrayItemArrayType(char_arr_type)
        tdq__zqf = context.make_helper(builder, vwonh__lkel, tcmzq__wlhde.data)
        ekff__sln = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        pgq__ted = context.make_helper(builder, offset_arr_type, ekff__sln.
            offsets).data
        xfhml__somkg = context.make_helper(builder, char_arr_type,
            ekff__sln.data).data
        ozcd__opc = context.make_helper(builder, null_bitmap_arr_type,
            ekff__sln.null_bitmap).data
        ufhen__luk = builder.zext(builder.load(builder.gep(pgq__ted, [
            ekff__sln.n_arrays])), lir.IntType(64))
        yuswi__mmvmr = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='string_array_to_info')
        return builder.call(cfot__myy, [ekff__sln.n_arrays, ufhen__luk,
            xfhml__somkg, pgq__ted, ozcd__opc, tdq__zqf.meminfo, yuswi__mmvmr])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        dhow__hghc = arr.data
        ejkkf__rtfkc = arr.indices
        sig = array_info_type(arr_type.data)
        pcgse__snk = array_to_info_codegen(context, builder, sig, (
            dhow__hghc,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        xgkc__yju = array_to_info_codegen(context, builder, sig, (
            ejkkf__rtfkc,), False)
        ahql__iild = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, ejkkf__rtfkc)
        rlall__roms = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, ahql__iild.null_bitmap).data
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='dict_str_array_to_info')
        azpfy__murrk = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(cfot__myy, [pcgse__snk, xgkc__yju, builder.
            bitcast(rlall__roms, lir.IntType(8).as_pointer()), azpfy__murrk])
    crfh__mxiac = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        ioaif__sph = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        yug__xtgys = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(yug__xtgys, 1, 'C')
        crfh__mxiac = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if crfh__mxiac:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        axgpb__his = builder.extract_value(arr.shape, 0)
        dfl__ivfti = arr_type.dtype
        vsje__yliw = numba_to_c_type(dfl__ivfti)
        hnz__anfzb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), vsje__yliw))
        if crfh__mxiac:
            xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            cfot__myy = cgutils.get_or_insert_function(builder.module,
                xkrrg__hwx, name='categorical_array_to_info')
            return builder.call(cfot__myy, [axgpb__his, builder.bitcast(arr
                .data, lir.IntType(8).as_pointer()), builder.load(
                hnz__anfzb), ioaif__sph, arr.meminfo])
        else:
            xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            cfot__myy = cgutils.get_or_insert_function(builder.module,
                xkrrg__hwx, name='numpy_array_to_info')
            return builder.call(cfot__myy, [axgpb__his, builder.bitcast(arr
                .data, lir.IntType(8).as_pointer()), builder.load(
                hnz__anfzb), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        dfl__ivfti = arr_type.dtype
        naat__qsy = dfl__ivfti
        if isinstance(arr_type, DecimalArrayType):
            naat__qsy = int128_type
        if arr_type == datetime_date_array_type:
            naat__qsy = types.int64
        yofc__aih = context.make_array(types.Array(naat__qsy, 1, 'C'))(context,
            builder, arr.data)
        axgpb__his = builder.extract_value(yofc__aih.shape, 0)
        daivd__ofgrv = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        vsje__yliw = numba_to_c_type(dfl__ivfti)
        hnz__anfzb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), vsje__yliw))
        if isinstance(arr_type, DecimalArrayType):
            xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            cfot__myy = cgutils.get_or_insert_function(builder.module,
                xkrrg__hwx, name='decimal_array_to_info')
            return builder.call(cfot__myy, [axgpb__his, builder.bitcast(
                yofc__aih.data, lir.IntType(8).as_pointer()), builder.load(
                hnz__anfzb), builder.bitcast(daivd__ofgrv.data, lir.IntType
                (8).as_pointer()), yofc__aih.meminfo, daivd__ofgrv.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        else:
            xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            cfot__myy = cgutils.get_or_insert_function(builder.module,
                xkrrg__hwx, name='nullable_array_to_info')
            return builder.call(cfot__myy, [axgpb__his, builder.bitcast(
                yofc__aih.data, lir.IntType(8).as_pointer()), builder.load(
                hnz__anfzb), builder.bitcast(daivd__ofgrv.data, lir.IntType
                (8).as_pointer()), yofc__aih.meminfo, daivd__ofgrv.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        joa__pjr = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        zqk__rshks = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        axgpb__his = builder.extract_value(joa__pjr.shape, 0)
        vsje__yliw = numba_to_c_type(arr_type.arr_type.dtype)
        hnz__anfzb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), vsje__yliw))
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='interval_array_to_info')
        return builder.call(cfot__myy, [axgpb__his, builder.bitcast(
            joa__pjr.data, lir.IntType(8).as_pointer()), builder.bitcast(
            zqk__rshks.data, lir.IntType(8).as_pointer()), builder.load(
            hnz__anfzb), joa__pjr.meminfo, zqk__rshks.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    rvah__wgya = cgutils.alloca_once(builder, lir.IntType(64))
    bjfb__abkl = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    vwhv__xxk = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    xkrrg__hwx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    cfot__myy = cgutils.get_or_insert_function(builder.module, xkrrg__hwx,
        name='info_to_numpy_array')
    builder.call(cfot__myy, [in_info, rvah__wgya, bjfb__abkl, vwhv__xxk])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    qshqx__jmf = context.get_value_type(types.intp)
    nxfd__pssvz = cgutils.pack_array(builder, [builder.load(rvah__wgya)],
        ty=qshqx__jmf)
    vye__ifc = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    hnec__wmy = cgutils.pack_array(builder, [vye__ifc], ty=qshqx__jmf)
    xfhml__somkg = builder.bitcast(builder.load(bjfb__abkl), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=xfhml__somkg, shape=
        nxfd__pssvz, strides=hnec__wmy, itemsize=vye__ifc, meminfo=builder.
        load(vwhv__xxk))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    vpkva__thiwc = context.make_helper(builder, arr_type)
    xkrrg__hwx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    cfot__myy = cgutils.get_or_insert_function(builder.module, xkrrg__hwx,
        name='info_to_list_string_array')
    builder.call(cfot__myy, [in_info, vpkva__thiwc._get_ptr_by_name('meminfo')]
        )
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return vpkva__thiwc._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    acvuv__wtsg = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        rnx__sqsy = lengths_pos
        ywop__kczh = infos_pos
        tyr__ynjjr, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        qed__tghl = ArrayItemArrayPayloadType(arr_typ)
        lpfw__oxe = context.get_data_type(qed__tghl)
        rke__xmx = context.get_abi_sizeof(lpfw__oxe)
        pvn__bek = define_array_item_dtor(context, builder, arr_typ, qed__tghl)
        wuog__zbj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, rke__xmx), pvn__bek)
        zzgm__pdnw = context.nrt.meminfo_data(builder, wuog__zbj)
        hrrre__ybubi = builder.bitcast(zzgm__pdnw, lpfw__oxe.as_pointer())
        ekff__sln = cgutils.create_struct_proxy(qed__tghl)(context, builder)
        ekff__sln.n_arrays = builder.extract_value(builder.load(lengths_ptr
            ), rnx__sqsy)
        ekff__sln.data = tyr__ynjjr
        owur__aye = builder.load(array_infos_ptr)
        avvg__azc = builder.bitcast(builder.extract_value(owur__aye,
            ywop__kczh), acvuv__wtsg)
        ekff__sln.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, avvg__azc)
        dikt__geu = builder.bitcast(builder.extract_value(owur__aye, 
            ywop__kczh + 1), acvuv__wtsg)
        ekff__sln.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, dikt__geu)
        builder.store(ekff__sln._getvalue(), hrrre__ybubi)
        tdq__zqf = context.make_helper(builder, arr_typ)
        tdq__zqf.meminfo = wuog__zbj
        return tdq__zqf._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        qic__vtxlr = []
        ywop__kczh = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for why__jwnu in arr_typ.data:
            tyr__ynjjr, lengths_pos, infos_pos = nested_to_array(context,
                builder, why__jwnu, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            qic__vtxlr.append(tyr__ynjjr)
        qed__tghl = StructArrayPayloadType(arr_typ.data)
        lpfw__oxe = context.get_value_type(qed__tghl)
        rke__xmx = context.get_abi_sizeof(lpfw__oxe)
        pvn__bek = define_struct_arr_dtor(context, builder, arr_typ, qed__tghl)
        wuog__zbj = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, rke__xmx), pvn__bek)
        zzgm__pdnw = context.nrt.meminfo_data(builder, wuog__zbj)
        hrrre__ybubi = builder.bitcast(zzgm__pdnw, lpfw__oxe.as_pointer())
        ekff__sln = cgutils.create_struct_proxy(qed__tghl)(context, builder)
        ekff__sln.data = cgutils.pack_array(builder, qic__vtxlr
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, qic__vtxlr)
        owur__aye = builder.load(array_infos_ptr)
        dikt__geu = builder.bitcast(builder.extract_value(owur__aye,
            ywop__kczh), acvuv__wtsg)
        ekff__sln.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, dikt__geu)
        builder.store(ekff__sln._getvalue(), hrrre__ybubi)
        dzuhf__pez = context.make_helper(builder, arr_typ)
        dzuhf__pez.meminfo = wuog__zbj
        return dzuhf__pez._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        owur__aye = builder.load(array_infos_ptr)
        xscop__xdlrc = builder.bitcast(builder.extract_value(owur__aye,
            infos_pos), acvuv__wtsg)
        tcmzq__wlhde = context.make_helper(builder, arr_typ)
        vwonh__lkel = ArrayItemArrayType(char_arr_type)
        tdq__zqf = context.make_helper(builder, vwonh__lkel)
        xkrrg__hwx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='info_to_string_array')
        builder.call(cfot__myy, [xscop__xdlrc, tdq__zqf._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        tcmzq__wlhde.data = tdq__zqf._getvalue()
        return tcmzq__wlhde._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        owur__aye = builder.load(array_infos_ptr)
        bwjrr__nkm = builder.bitcast(builder.extract_value(owur__aye, 
            infos_pos + 1), acvuv__wtsg)
        return _lower_info_to_array_numpy(arr_typ, context, builder, bwjrr__nkm
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        naat__qsy = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            naat__qsy = int128_type
        elif arr_typ == datetime_date_array_type:
            naat__qsy = types.int64
        owur__aye = builder.load(array_infos_ptr)
        dikt__geu = builder.bitcast(builder.extract_value(owur__aye,
            infos_pos), acvuv__wtsg)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, dikt__geu)
        bwjrr__nkm = builder.bitcast(builder.extract_value(owur__aye, 
            infos_pos + 1), acvuv__wtsg)
        arr.data = _lower_info_to_array_numpy(types.Array(naat__qsy, 1, 'C'
            ), context, builder, bwjrr__nkm)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, ptw__laaem = args
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
                return 1 + sum([get_num_arrays(why__jwnu) for why__jwnu in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(why__jwnu) for why__jwnu in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            enou__gmwkv = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            enou__gmwkv = _get_map_arr_data_type(arr_type)
        else:
            enou__gmwkv = arr_type
        wwaw__akap = get_num_arrays(enou__gmwkv)
        tknsd__wrsb = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), 0) for ptw__laaem in range(wwaw__akap)])
        lengths_ptr = cgutils.alloca_once_value(builder, tknsd__wrsb)
        mdw__mwbgn = lir.Constant(lir.IntType(8).as_pointer(), None)
        mbe__pvt = cgutils.pack_array(builder, [mdw__mwbgn for ptw__laaem in
            range(get_num_infos(enou__gmwkv))])
        array_infos_ptr = cgutils.alloca_once_value(builder, mbe__pvt)
        xkrrg__hwx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='info_to_nested_array')
        builder.call(cfot__myy, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, ptw__laaem, ptw__laaem = nested_to_array(context, builder,
            enou__gmwkv, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            auec__qnxqg = context.make_helper(builder, arr_type)
            auec__qnxqg.data = arr
            context.nrt.incref(builder, enou__gmwkv, arr)
            arr = auec__qnxqg._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, enou__gmwkv)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        tcmzq__wlhde = context.make_helper(builder, arr_type)
        vwonh__lkel = ArrayItemArrayType(char_arr_type)
        tdq__zqf = context.make_helper(builder, vwonh__lkel)
        xkrrg__hwx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='info_to_string_array')
        builder.call(cfot__myy, [in_info, tdq__zqf._get_ptr_by_name('meminfo')]
            )
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        tcmzq__wlhde.data = tdq__zqf._getvalue()
        return tcmzq__wlhde._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='get_nested_info')
        pcgse__snk = builder.call(cfot__myy, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        xgkc__yju = builder.call(cfot__myy, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        zsa__xlarp = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        zsa__xlarp.data = info_to_array_codegen(context, builder, sig, (
            pcgse__snk, context.get_constant_null(arr_type.data)))
        qjz__swzz = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = qjz__swzz(array_info_type, qjz__swzz)
        zsa__xlarp.indices = info_to_array_codegen(context, builder, sig, (
            xgkc__yju, context.get_constant_null(qjz__swzz)))
        xkrrg__hwx = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='get_has_global_dictionary')
        azpfy__murrk = builder.call(cfot__myy, [in_info])
        zsa__xlarp.has_global_dictionary = builder.trunc(azpfy__murrk,
            cgutils.bool_t)
        return zsa__xlarp._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        yug__xtgys = get_categories_int_type(arr_type.dtype)
        dvwu__ksx = types.Array(yug__xtgys, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(dvwu__ksx, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            zxssm__hwqxh = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(zxssm__hwqxh))
            int_type = arr_type.dtype.int_type
            gvg__vqldg = bodo.typeof(zxssm__hwqxh)
            yrjnd__zgf = context.get_constant_generic(builder, gvg__vqldg,
                zxssm__hwqxh)
            dfl__ivfti = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(gvg__vqldg), [yrjnd__zgf])
        else:
            dfl__ivfti = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, dfl__ivfti)
        out_arr.dtype = dfl__ivfti
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        xfhml__somkg = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = xfhml__somkg
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        naat__qsy = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            naat__qsy = int128_type
        elif arr_type == datetime_date_array_type:
            naat__qsy = types.int64
        cyq__dwsv = types.Array(naat__qsy, 1, 'C')
        yofc__aih = context.make_array(cyq__dwsv)(context, builder)
        dnmv__bre = types.Array(types.uint8, 1, 'C')
        sqhc__zxl = context.make_array(dnmv__bre)(context, builder)
        rvah__wgya = cgutils.alloca_once(builder, lir.IntType(64))
        reejf__yav = cgutils.alloca_once(builder, lir.IntType(64))
        bjfb__abkl = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ckn__jmlre = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        vwhv__xxk = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        dlbzk__zfuwt = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        xkrrg__hwx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='info_to_nullable_array')
        builder.call(cfot__myy, [in_info, rvah__wgya, reejf__yav,
            bjfb__abkl, ckn__jmlre, vwhv__xxk, dlbzk__zfuwt])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        qshqx__jmf = context.get_value_type(types.intp)
        nxfd__pssvz = cgutils.pack_array(builder, [builder.load(rvah__wgya)
            ], ty=qshqx__jmf)
        vye__ifc = context.get_constant(types.intp, context.get_abi_sizeof(
            context.get_data_type(naat__qsy)))
        hnec__wmy = cgutils.pack_array(builder, [vye__ifc], ty=qshqx__jmf)
        xfhml__somkg = builder.bitcast(builder.load(bjfb__abkl), context.
            get_data_type(naat__qsy).as_pointer())
        numba.np.arrayobj.populate_array(yofc__aih, data=xfhml__somkg,
            shape=nxfd__pssvz, strides=hnec__wmy, itemsize=vye__ifc,
            meminfo=builder.load(vwhv__xxk))
        arr.data = yofc__aih._getvalue()
        nxfd__pssvz = cgutils.pack_array(builder, [builder.load(reejf__yav)
            ], ty=qshqx__jmf)
        vye__ifc = context.get_constant(types.intp, context.get_abi_sizeof(
            context.get_data_type(types.uint8)))
        hnec__wmy = cgutils.pack_array(builder, [vye__ifc], ty=qshqx__jmf)
        xfhml__somkg = builder.bitcast(builder.load(ckn__jmlre), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(sqhc__zxl, data=xfhml__somkg,
            shape=nxfd__pssvz, strides=hnec__wmy, itemsize=vye__ifc,
            meminfo=builder.load(dlbzk__zfuwt))
        arr.null_bitmap = sqhc__zxl._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        joa__pjr = context.make_array(arr_type.arr_type)(context, builder)
        zqk__rshks = context.make_array(arr_type.arr_type)(context, builder)
        rvah__wgya = cgutils.alloca_once(builder, lir.IntType(64))
        vuwf__fdv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        hwlek__viw = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        hgm__vnqg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        xhdex__xcgh = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        xkrrg__hwx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='info_to_interval_array')
        builder.call(cfot__myy, [in_info, rvah__wgya, vuwf__fdv, hwlek__viw,
            hgm__vnqg, xhdex__xcgh])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        qshqx__jmf = context.get_value_type(types.intp)
        nxfd__pssvz = cgutils.pack_array(builder, [builder.load(rvah__wgya)
            ], ty=qshqx__jmf)
        vye__ifc = context.get_constant(types.intp, context.get_abi_sizeof(
            context.get_data_type(arr_type.arr_type.dtype)))
        hnec__wmy = cgutils.pack_array(builder, [vye__ifc], ty=qshqx__jmf)
        rdmqs__djpv = builder.bitcast(builder.load(vuwf__fdv), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(joa__pjr, data=rdmqs__djpv, shape=
            nxfd__pssvz, strides=hnec__wmy, itemsize=vye__ifc, meminfo=
            builder.load(hgm__vnqg))
        arr.left = joa__pjr._getvalue()
        pydzu__bvunx = builder.bitcast(builder.load(hwlek__viw), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(zqk__rshks, data=pydzu__bvunx,
            shape=nxfd__pssvz, strides=hnec__wmy, itemsize=vye__ifc,
            meminfo=builder.load(xhdex__xcgh))
        arr.right = zqk__rshks._getvalue()
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
        axgpb__his, ptw__laaem = args
        vsje__yliw = numba_to_c_type(array_type.dtype)
        hnz__anfzb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), vsje__yliw))
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='alloc_numpy')
        return builder.call(cfot__myy, [axgpb__his, builder.load(hnz__anfzb)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        axgpb__his, ifar__wof = args
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='alloc_string_array')
        return builder.call(cfot__myy, [axgpb__his, ifar__wof])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    fmiv__jrx, = args
    gel__prfhv = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], fmiv__jrx)
    xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer().as_pointer(), lir.IntType(64)])
    cfot__myy = cgutils.get_or_insert_function(builder.module, xkrrg__hwx,
        name='arr_info_list_to_table')
    return builder.call(cfot__myy, [gel__prfhv.data, gel__prfhv.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='info_from_table')
        return builder.call(cfot__myy, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    vfxd__yyvd = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        igu__uyhsr, jqzsr__htv, ptw__laaem = args
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='info_from_table')
        qvru__keb = cgutils.create_struct_proxy(vfxd__yyvd)(context, builder)
        qvru__keb.parent = cgutils.get_null_value(qvru__keb.parent.type)
        eiwkt__odblq = context.make_array(table_idx_arr_t)(context, builder,
            jqzsr__htv)
        apn__mppp = context.get_constant(types.int64, -1)
        lxca__bhm = context.get_constant(types.int64, 0)
        veh__uvx = cgutils.alloca_once_value(builder, lxca__bhm)
        for t, rwy__blkqm in vfxd__yyvd.type_to_blk.items():
            ezou__aokj = context.get_constant(types.int64, len(vfxd__yyvd.
                block_to_arr_ind[rwy__blkqm]))
            ptw__laaem, scxax__zww = ListInstance.allocate_ex(context,
                builder, types.List(t), ezou__aokj)
            scxax__zww.size = ezou__aokj
            xdmc__cogyt = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(vfxd__yyvd.block_to_arr_ind[
                rwy__blkqm], dtype=np.int64))
            lyfe__nsfnk = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, xdmc__cogyt)
            with cgutils.for_range(builder, ezou__aokj) as bwt__xqd:
                pwqv__cogvx = bwt__xqd.index
                xohi__yywk = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    lyfe__nsfnk, pwqv__cogvx)
                vargf__rbe = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, eiwkt__odblq, xohi__yywk)
                qcl__xkywm = builder.icmp_unsigned('!=', vargf__rbe, apn__mppp)
                with builder.if_else(qcl__xkywm) as (ilrnu__tdym, cbzxo__yacf):
                    with ilrnu__tdym:
                        ucngl__ihzsx = builder.call(cfot__myy, [igu__uyhsr,
                            vargf__rbe])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            ucngl__ihzsx])
                        scxax__zww.inititem(pwqv__cogvx, arr, incref=False)
                        axgpb__his = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(axgpb__his, veh__uvx)
                    with cbzxo__yacf:
                        kiis__sykv = context.get_constant_null(t)
                        scxax__zww.inititem(pwqv__cogvx, kiis__sykv, incref
                            =False)
            setattr(qvru__keb, f'block_{rwy__blkqm}', scxax__zww.value)
        qvru__keb.len = builder.load(veh__uvx)
        return qvru__keb._getvalue()
    return vfxd__yyvd(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    vfxd__yyvd = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        dbgv__yjyv, ptw__laaem = args
        cfwld__ziemb = cgutils.create_struct_proxy(vfxd__yyvd)(context,
            builder, dbgv__yjyv)
        if vfxd__yyvd.has_runtime_cols:
            lxcc__pcv = lir.Constant(lir.IntType(64), 0)
            for rwy__blkqm, t in enumerate(vfxd__yyvd.arr_types):
                rrqk__zrrs = getattr(cfwld__ziemb, f'block_{rwy__blkqm}')
                phm__wcft = ListInstance(context, builder, types.List(t),
                    rrqk__zrrs)
                lxcc__pcv = builder.add(lxcc__pcv, phm__wcft.size)
        else:
            lxcc__pcv = lir.Constant(lir.IntType(64), len(vfxd__yyvd.arr_types)
                )
        ptw__laaem, ywa__zijz = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), lxcc__pcv)
        ywa__zijz.size = lxcc__pcv
        if vfxd__yyvd.has_runtime_cols:
            zpfc__igsl = lir.Constant(lir.IntType(64), 0)
            for rwy__blkqm, t in enumerate(vfxd__yyvd.arr_types):
                rrqk__zrrs = getattr(cfwld__ziemb, f'block_{rwy__blkqm}')
                phm__wcft = ListInstance(context, builder, types.List(t),
                    rrqk__zrrs)
                ezou__aokj = phm__wcft.size
                with cgutils.for_range(builder, ezou__aokj) as bwt__xqd:
                    pwqv__cogvx = bwt__xqd.index
                    arr = phm__wcft.getitem(pwqv__cogvx)
                    fbe__kiy = signature(array_info_type, t)
                    augy__pkhe = arr,
                    qqho__mbwze = array_to_info_codegen(context, builder,
                        fbe__kiy, augy__pkhe)
                    ywa__zijz.inititem(builder.add(zpfc__igsl, pwqv__cogvx),
                        qqho__mbwze, incref=False)
                zpfc__igsl = builder.add(zpfc__igsl, ezou__aokj)
        else:
            for t, rwy__blkqm in vfxd__yyvd.type_to_blk.items():
                ezou__aokj = context.get_constant(types.int64, len(
                    vfxd__yyvd.block_to_arr_ind[rwy__blkqm]))
                rrqk__zrrs = getattr(cfwld__ziemb, f'block_{rwy__blkqm}')
                phm__wcft = ListInstance(context, builder, types.List(t),
                    rrqk__zrrs)
                xdmc__cogyt = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(vfxd__yyvd.
                    block_to_arr_ind[rwy__blkqm], dtype=np.int64))
                lyfe__nsfnk = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, xdmc__cogyt)
                with cgutils.for_range(builder, ezou__aokj) as bwt__xqd:
                    pwqv__cogvx = bwt__xqd.index
                    xohi__yywk = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        lyfe__nsfnk, pwqv__cogvx)
                    xyrn__ryedh = signature(types.none, vfxd__yyvd, types.
                        List(t), types.int64, types.int64)
                    kasr__iylh = (dbgv__yjyv, rrqk__zrrs, pwqv__cogvx,
                        xohi__yywk)
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, xyrn__ryedh, kasr__iylh)
                    arr = phm__wcft.getitem(pwqv__cogvx)
                    fbe__kiy = signature(array_info_type, t)
                    augy__pkhe = arr,
                    qqho__mbwze = array_to_info_codegen(context, builder,
                        fbe__kiy, augy__pkhe)
                    ywa__zijz.inititem(xohi__yywk, qqho__mbwze, incref=False)
        vwv__prjbk = ywa__zijz.value
        gqw__fac = signature(table_type, types.List(array_info_type))
        gbmw__hqx = vwv__prjbk,
        igu__uyhsr = arr_info_list_to_table_codegen(context, builder,
            gqw__fac, gbmw__hqx)
        context.nrt.decref(builder, types.List(array_info_type), vwv__prjbk)
        return igu__uyhsr
    return table_type(vfxd__yyvd, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xkrrg__hwx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='delete_table')
        builder.call(cfot__myy, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='shuffle_table')
        mcf__tmdob = builder.call(cfot__myy, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
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
        xkrrg__hwx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='delete_shuffle_info')
        return builder.call(cfot__myy, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='reverse_shuffle_table')
        return builder.call(cfot__myy, args)
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
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='hash_join_table')
        mcf__tmdob = builder.call(cfot__myy, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
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
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='sort_values_table')
        mcf__tmdob = builder.call(cfot__myy, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='sample_table')
        mcf__tmdob = builder.call(cfot__myy, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='shuffle_renormalization')
        mcf__tmdob = builder.call(cfot__myy, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='shuffle_renormalization_group')
        mcf__tmdob = builder.call(cfot__myy, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='drop_duplicates_table')
        mcf__tmdob = builder.call(cfot__myy, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
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
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='pivot_groupby_and_aggregate')
        mcf__tmdob = builder.call(cfot__myy, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
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
        xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        cfot__myy = cgutils.get_or_insert_function(builder.module,
            xkrrg__hwx, name='groupby_and_aggregate')
        mcf__tmdob = builder.call(cfot__myy, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return mcf__tmdob
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
    mfd__bpydi = array_to_info(in_arr)
    fyux__nqyt = array_to_info(in_values)
    fdfgg__kvod = array_to_info(out_arr)
    poy__aeij = arr_info_list_to_table([mfd__bpydi, fyux__nqyt, fdfgg__kvod])
    _array_isin(fdfgg__kvod, mfd__bpydi, fyux__nqyt, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(poy__aeij)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    mfd__bpydi = array_to_info(in_arr)
    fdfgg__kvod = array_to_info(out_arr)
    _get_search_regex(mfd__bpydi, case, pat, fdfgg__kvod)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    qclh__tip = col_array_typ.dtype
    if isinstance(qclh__tip, types.Number) or qclh__tip in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                qvru__keb, zoxf__qrx = args
                qvru__keb = builder.bitcast(qvru__keb, lir.IntType(8).
                    as_pointer().as_pointer())
                fbfie__mquq = lir.Constant(lir.IntType(64), c_ind)
                gpn__vwzk = builder.load(builder.gep(qvru__keb, [fbfie__mquq]))
                gpn__vwzk = builder.bitcast(gpn__vwzk, context.
                    get_data_type(qclh__tip).as_pointer())
                return builder.load(builder.gep(gpn__vwzk, [zoxf__qrx]))
            return qclh__tip(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                qvru__keb, zoxf__qrx = args
                qvru__keb = builder.bitcast(qvru__keb, lir.IntType(8).
                    as_pointer().as_pointer())
                fbfie__mquq = lir.Constant(lir.IntType(64), c_ind)
                gpn__vwzk = builder.load(builder.gep(qvru__keb, [fbfie__mquq]))
                xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                xskxk__llzzd = cgutils.get_or_insert_function(builder.
                    module, xkrrg__hwx, name='array_info_getitem')
                eeprn__xwjk = cgutils.alloca_once(builder, lir.IntType(64))
                args = gpn__vwzk, zoxf__qrx, eeprn__xwjk
                bjfb__abkl = builder.call(xskxk__llzzd, args)
                return context.make_tuple(builder, sig.return_type, [
                    bjfb__abkl, builder.load(eeprn__xwjk)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                vvc__ltf = lir.Constant(lir.IntType(64), 1)
                ejum__npyii = lir.Constant(lir.IntType(64), 2)
                qvru__keb, zoxf__qrx = args
                qvru__keb = builder.bitcast(qvru__keb, lir.IntType(8).
                    as_pointer().as_pointer())
                fbfie__mquq = lir.Constant(lir.IntType(64), c_ind)
                gpn__vwzk = builder.load(builder.gep(qvru__keb, [fbfie__mquq]))
                xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                nnp__isi = cgutils.get_or_insert_function(builder.module,
                    xkrrg__hwx, name='get_nested_info')
                args = gpn__vwzk, ejum__npyii
                iqhv__tqupf = builder.call(nnp__isi, args)
                xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                alz__obmp = cgutils.get_or_insert_function(builder.module,
                    xkrrg__hwx, name='array_info_getdata1')
                args = iqhv__tqupf,
                vufvi__iwtg = builder.call(alz__obmp, args)
                vufvi__iwtg = builder.bitcast(vufvi__iwtg, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                kdv__mmw = builder.sext(builder.load(builder.gep(
                    vufvi__iwtg, [zoxf__qrx])), lir.IntType(64))
                args = gpn__vwzk, vvc__ltf
                sared__tcfvb = builder.call(nnp__isi, args)
                xkrrg__hwx = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                xskxk__llzzd = cgutils.get_or_insert_function(builder.
                    module, xkrrg__hwx, name='array_info_getitem')
                eeprn__xwjk = cgutils.alloca_once(builder, lir.IntType(64))
                args = sared__tcfvb, kdv__mmw, eeprn__xwjk
                bjfb__abkl = builder.call(xskxk__llzzd, args)
                return context.make_tuple(builder, sig.return_type, [
                    bjfb__abkl, builder.load(eeprn__xwjk)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{qclh__tip}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                klik__uxnj, zoxf__qrx = args
                klik__uxnj = builder.bitcast(klik__uxnj, lir.IntType(8).
                    as_pointer().as_pointer())
                fbfie__mquq = lir.Constant(lir.IntType(64), c_ind)
                gpn__vwzk = builder.load(builder.gep(klik__uxnj, [fbfie__mquq])
                    )
                ozcd__opc = builder.bitcast(gpn__vwzk, context.
                    get_data_type(types.bool_).as_pointer())
                uhx__slydl = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    ozcd__opc, zoxf__qrx)
                zlevq__yypx = builder.icmp_unsigned('!=', uhx__slydl, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(zlevq__yypx, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        qclh__tip = col_array_dtype.dtype
        if qclh__tip in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    qvru__keb, zoxf__qrx = args
                    qvru__keb = builder.bitcast(qvru__keb, lir.IntType(8).
                        as_pointer().as_pointer())
                    fbfie__mquq = lir.Constant(lir.IntType(64), c_ind)
                    gpn__vwzk = builder.load(builder.gep(qvru__keb, [
                        fbfie__mquq]))
                    gpn__vwzk = builder.bitcast(gpn__vwzk, context.
                        get_data_type(qclh__tip).as_pointer())
                    fxqh__mtw = builder.load(builder.gep(gpn__vwzk, [
                        zoxf__qrx]))
                    zlevq__yypx = builder.icmp_unsigned('!=', fxqh__mtw,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(zlevq__yypx, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(qclh__tip, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    qvru__keb, zoxf__qrx = args
                    qvru__keb = builder.bitcast(qvru__keb, lir.IntType(8).
                        as_pointer().as_pointer())
                    fbfie__mquq = lir.Constant(lir.IntType(64), c_ind)
                    gpn__vwzk = builder.load(builder.gep(qvru__keb, [
                        fbfie__mquq]))
                    gpn__vwzk = builder.bitcast(gpn__vwzk, context.
                        get_data_type(qclh__tip).as_pointer())
                    fxqh__mtw = builder.load(builder.gep(gpn__vwzk, [
                        zoxf__qrx]))
                    bdkx__lcgv = signature(types.bool_, qclh__tip)
                    uhx__slydl = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, bdkx__lcgv, (fxqh__mtw,))
                    return builder.not_(builder.sext(uhx__slydl, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
