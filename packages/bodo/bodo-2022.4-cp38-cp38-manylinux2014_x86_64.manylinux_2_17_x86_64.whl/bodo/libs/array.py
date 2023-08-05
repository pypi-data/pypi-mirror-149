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
        pqtg__rvlny = context.make_helper(builder, arr_type, in_arr)
        in_arr = pqtg__rvlny.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        rhliz__val = context.make_helper(builder, arr_type, in_arr)
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='list_string_array_to_info')
        return builder.call(nadu__fau, [rhliz__val.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                ckf__slbo = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for kmlgk__ott in arr_typ.data:
                    ckf__slbo += get_types(kmlgk__ott)
                return ckf__slbo
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
            nfxqx__pbykk = context.compile_internal(builder, lambda a: len(
                a), types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                shc__cqt = context.make_helper(builder, arr_typ, value=arr)
                phx__vdkc = get_lengths(_get_map_arr_data_type(arr_typ),
                    shc__cqt.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                glwlp__hoha = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                phx__vdkc = get_lengths(arr_typ.dtype, glwlp__hoha.data)
                phx__vdkc = cgutils.pack_array(builder, [glwlp__hoha.
                    n_arrays] + [builder.extract_value(phx__vdkc,
                    hoau__cvwd) for hoau__cvwd in range(phx__vdkc.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                glwlp__hoha = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                phx__vdkc = []
                for hoau__cvwd, kmlgk__ott in enumerate(arr_typ.data):
                    zgv__dyoz = get_lengths(kmlgk__ott, builder.
                        extract_value(glwlp__hoha.data, hoau__cvwd))
                    phx__vdkc += [builder.extract_value(zgv__dyoz,
                        pszn__goue) for pszn__goue in range(zgv__dyoz.type.
                        count)]
                phx__vdkc = cgutils.pack_array(builder, [nfxqx__pbykk,
                    context.get_constant(types.int64, -1)] + phx__vdkc)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                phx__vdkc = cgutils.pack_array(builder, [nfxqx__pbykk])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return phx__vdkc

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                shc__cqt = context.make_helper(builder, arr_typ, value=arr)
                vswd__qxwob = get_buffers(_get_map_arr_data_type(arr_typ),
                    shc__cqt.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                glwlp__hoha = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                xltc__fcdsh = get_buffers(arr_typ.dtype, glwlp__hoha.data)
                psw__juvrk = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, glwlp__hoha.offsets)
                umgz__fya = builder.bitcast(psw__juvrk.data, lir.IntType(8)
                    .as_pointer())
                cshbi__gcl = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, glwlp__hoha.null_bitmap)
                yerwg__sgymb = builder.bitcast(cshbi__gcl.data, lir.IntType
                    (8).as_pointer())
                vswd__qxwob = cgutils.pack_array(builder, [umgz__fya,
                    yerwg__sgymb] + [builder.extract_value(xltc__fcdsh,
                    hoau__cvwd) for hoau__cvwd in range(xltc__fcdsh.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                glwlp__hoha = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                xltc__fcdsh = []
                for hoau__cvwd, kmlgk__ott in enumerate(arr_typ.data):
                    kil__vonar = get_buffers(kmlgk__ott, builder.
                        extract_value(glwlp__hoha.data, hoau__cvwd))
                    xltc__fcdsh += [builder.extract_value(kil__vonar,
                        pszn__goue) for pszn__goue in range(kil__vonar.type
                        .count)]
                cshbi__gcl = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, glwlp__hoha.null_bitmap)
                yerwg__sgymb = builder.bitcast(cshbi__gcl.data, lir.IntType
                    (8).as_pointer())
                vswd__qxwob = cgutils.pack_array(builder, [yerwg__sgymb] +
                    xltc__fcdsh)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                dkzw__xzxci = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    dkzw__xzxci = int128_type
                elif arr_typ == datetime_date_array_type:
                    dkzw__xzxci = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                xhg__xob = context.make_array(types.Array(dkzw__xzxci, 1, 'C')
                    )(context, builder, arr.data)
                cshbi__gcl = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                bqbek__douwo = builder.bitcast(xhg__xob.data, lir.IntType(8
                    ).as_pointer())
                yerwg__sgymb = builder.bitcast(cshbi__gcl.data, lir.IntType
                    (8).as_pointer())
                vswd__qxwob = cgutils.pack_array(builder, [yerwg__sgymb,
                    bqbek__douwo])
            elif arr_typ in (string_array_type, binary_array_type):
                glwlp__hoha = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                jnub__gcyoy = context.make_helper(builder, offset_arr_type,
                    glwlp__hoha.offsets).data
                qwqo__nxcms = context.make_helper(builder, char_arr_type,
                    glwlp__hoha.data).data
                wfahq__wdjf = context.make_helper(builder,
                    null_bitmap_arr_type, glwlp__hoha.null_bitmap).data
                vswd__qxwob = cgutils.pack_array(builder, [builder.bitcast(
                    jnub__gcyoy, lir.IntType(8).as_pointer()), builder.
                    bitcast(wfahq__wdjf, lir.IntType(8).as_pointer()),
                    builder.bitcast(qwqo__nxcms, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                bqbek__douwo = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                ndx__clnlu = lir.Constant(lir.IntType(8).as_pointer(), None)
                vswd__qxwob = cgutils.pack_array(builder, [ndx__clnlu,
                    bqbek__douwo])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return vswd__qxwob

        def get_field_names(arr_typ):
            cotvv__tvss = []
            if isinstance(arr_typ, StructArrayType):
                for vgg__azq, ohjir__ilrcr in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    cotvv__tvss.append(vgg__azq)
                    cotvv__tvss += get_field_names(ohjir__ilrcr)
            elif isinstance(arr_typ, ArrayItemArrayType):
                cotvv__tvss += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                cotvv__tvss += get_field_names(_get_map_arr_data_type(arr_typ))
            return cotvv__tvss
        ckf__slbo = get_types(arr_type)
        ghpjm__plgd = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in ckf__slbo])
        qqup__jghvr = cgutils.alloca_once_value(builder, ghpjm__plgd)
        phx__vdkc = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, phx__vdkc)
        vswd__qxwob = get_buffers(arr_type, in_arr)
        iua__efliu = cgutils.alloca_once_value(builder, vswd__qxwob)
        cotvv__tvss = get_field_names(arr_type)
        if len(cotvv__tvss) == 0:
            cotvv__tvss = ['irrelevant']
        kmd__zxiv = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in cotvv__tvss])
        tfek__vzun = cgutils.alloca_once_value(builder, kmd__zxiv)
        if isinstance(arr_type, MapArrayType):
            ggu__yqn = _get_map_arr_data_type(arr_type)
            gdivh__xbyl = context.make_helper(builder, arr_type, value=in_arr)
            wfhwf__jujsf = gdivh__xbyl.data
        else:
            ggu__yqn = arr_type
            wfhwf__jujsf = in_arr
        tdzw__alfy = context.make_helper(builder, ggu__yqn, wfhwf__jujsf)
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='nested_array_to_info')
        eowwm__qebsl = builder.call(nadu__fau, [builder.bitcast(qqup__jghvr,
            lir.IntType(32).as_pointer()), builder.bitcast(iua__efliu, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            tfek__vzun, lir.IntType(8).as_pointer()), tdzw__alfy.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
    if arr_type in (string_array_type, binary_array_type):
        dunc__bdv = context.make_helper(builder, arr_type, in_arr)
        fmbpk__ijxp = ArrayItemArrayType(char_arr_type)
        rhliz__val = context.make_helper(builder, fmbpk__ijxp, dunc__bdv.data)
        glwlp__hoha = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        jnub__gcyoy = context.make_helper(builder, offset_arr_type,
            glwlp__hoha.offsets).data
        qwqo__nxcms = context.make_helper(builder, char_arr_type,
            glwlp__hoha.data).data
        wfahq__wdjf = context.make_helper(builder, null_bitmap_arr_type,
            glwlp__hoha.null_bitmap).data
        hmfv__lmjw = builder.zext(builder.load(builder.gep(jnub__gcyoy, [
            glwlp__hoha.n_arrays])), lir.IntType(64))
        qmlht__llerj = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='string_array_to_info')
        return builder.call(nadu__fau, [glwlp__hoha.n_arrays, hmfv__lmjw,
            qwqo__nxcms, jnub__gcyoy, wfahq__wdjf, rhliz__val.meminfo,
            qmlht__llerj])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        gul__lyzf = arr.data
        lewg__esf = arr.indices
        sig = array_info_type(arr_type.data)
        xfw__wlwo = array_to_info_codegen(context, builder, sig, (gul__lyzf
            ,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        eyy__xzg = array_to_info_codegen(context, builder, sig, (lewg__esf,
            ), False)
        msj__pmegh = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, lewg__esf)
        yerwg__sgymb = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, msj__pmegh.null_bitmap).data
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='dict_str_array_to_info')
        oflsy__qeoig = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(nadu__fau, [xfw__wlwo, eyy__xzg, builder.
            bitcast(yerwg__sgymb, lir.IntType(8).as_pointer()), oflsy__qeoig])
    avp__smra = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        cuqp__nmiv = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        eqi__zmha = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(eqi__zmha, 1, 'C')
        avp__smra = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if avp__smra:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        nfxqx__pbykk = builder.extract_value(arr.shape, 0)
        iubjn__fqzjh = arr_type.dtype
        jftdo__isqo = numba_to_c_type(iubjn__fqzjh)
        zmsns__sga = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), jftdo__isqo))
        if avp__smra:
            gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(64), lir.IntType(8).as_pointer()])
            nadu__fau = cgutils.get_or_insert_function(builder.module,
                gmnzm__ferwt, name='categorical_array_to_info')
            return builder.call(nadu__fau, [nfxqx__pbykk, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                zmsns__sga), cuqp__nmiv, arr.meminfo])
        else:
            gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer()])
            nadu__fau = cgutils.get_or_insert_function(builder.module,
                gmnzm__ferwt, name='numpy_array_to_info')
            return builder.call(nadu__fau, [nfxqx__pbykk, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                zmsns__sga), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        iubjn__fqzjh = arr_type.dtype
        dkzw__xzxci = iubjn__fqzjh
        if isinstance(arr_type, DecimalArrayType):
            dkzw__xzxci = int128_type
        if arr_type == datetime_date_array_type:
            dkzw__xzxci = types.int64
        xhg__xob = context.make_array(types.Array(dkzw__xzxci, 1, 'C'))(context
            , builder, arr.data)
        nfxqx__pbykk = builder.extract_value(xhg__xob.shape, 0)
        yubxb__nzf = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        jftdo__isqo = numba_to_c_type(iubjn__fqzjh)
        zmsns__sga = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), jftdo__isqo))
        if isinstance(arr_type, DecimalArrayType):
            gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32), lir.
                IntType(32)])
            nadu__fau = cgutils.get_or_insert_function(builder.module,
                gmnzm__ferwt, name='decimal_array_to_info')
            return builder.call(nadu__fau, [nfxqx__pbykk, builder.bitcast(
                xhg__xob.data, lir.IntType(8).as_pointer()), builder.load(
                zmsns__sga), builder.bitcast(yubxb__nzf.data, lir.IntType(8
                ).as_pointer()), xhg__xob.meminfo, yubxb__nzf.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        else:
            gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer()])
            nadu__fau = cgutils.get_or_insert_function(builder.module,
                gmnzm__ferwt, name='nullable_array_to_info')
            return builder.call(nadu__fau, [nfxqx__pbykk, builder.bitcast(
                xhg__xob.data, lir.IntType(8).as_pointer()), builder.load(
                zmsns__sga), builder.bitcast(yubxb__nzf.data, lir.IntType(8
                ).as_pointer()), xhg__xob.meminfo, yubxb__nzf.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        ooe__afh = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        gjxif__fli = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        nfxqx__pbykk = builder.extract_value(ooe__afh.shape, 0)
        jftdo__isqo = numba_to_c_type(arr_type.arr_type.dtype)
        zmsns__sga = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), jftdo__isqo))
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='interval_array_to_info')
        return builder.call(nadu__fau, [nfxqx__pbykk, builder.bitcast(
            ooe__afh.data, lir.IntType(8).as_pointer()), builder.bitcast(
            gjxif__fli.data, lir.IntType(8).as_pointer()), builder.load(
            zmsns__sga), ooe__afh.meminfo, gjxif__fli.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    fyon__nipa = cgutils.alloca_once(builder, lir.IntType(64))
    bqbek__douwo = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    btguv__wqh = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    gmnzm__ferwt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    nadu__fau = cgutils.get_or_insert_function(builder.module, gmnzm__ferwt,
        name='info_to_numpy_array')
    builder.call(nadu__fau, [in_info, fyon__nipa, bqbek__douwo, btguv__wqh])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    ewik__nrq = context.get_value_type(types.intp)
    qkrgj__wnbbj = cgutils.pack_array(builder, [builder.load(fyon__nipa)],
        ty=ewik__nrq)
    hpgj__ejhdq = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    ndmeu__jyqj = cgutils.pack_array(builder, [hpgj__ejhdq], ty=ewik__nrq)
    qwqo__nxcms = builder.bitcast(builder.load(bqbek__douwo), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=qwqo__nxcms, shape=
        qkrgj__wnbbj, strides=ndmeu__jyqj, itemsize=hpgj__ejhdq, meminfo=
        builder.load(btguv__wqh))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    prnzs__fvkt = context.make_helper(builder, arr_type)
    gmnzm__ferwt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    nadu__fau = cgutils.get_or_insert_function(builder.module, gmnzm__ferwt,
        name='info_to_list_string_array')
    builder.call(nadu__fau, [in_info, prnzs__fvkt._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return prnzs__fvkt._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    yhxg__ufjqt = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        rejpu__ocnrl = lengths_pos
        kmp__tdrvk = infos_pos
        jicc__wpswg, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        mgdpe__tzm = ArrayItemArrayPayloadType(arr_typ)
        xzi__usmj = context.get_data_type(mgdpe__tzm)
        xroxn__yje = context.get_abi_sizeof(xzi__usmj)
        vyh__dgq = define_array_item_dtor(context, builder, arr_typ, mgdpe__tzm
            )
        ggus__ilf = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, xroxn__yje), vyh__dgq)
        ywueb__qaj = context.nrt.meminfo_data(builder, ggus__ilf)
        dodls__ztej = builder.bitcast(ywueb__qaj, xzi__usmj.as_pointer())
        glwlp__hoha = cgutils.create_struct_proxy(mgdpe__tzm)(context, builder)
        glwlp__hoha.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), rejpu__ocnrl)
        glwlp__hoha.data = jicc__wpswg
        pgwiv__jajx = builder.load(array_infos_ptr)
        nvjg__jmbsk = builder.bitcast(builder.extract_value(pgwiv__jajx,
            kmp__tdrvk), yhxg__ufjqt)
        glwlp__hoha.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, nvjg__jmbsk)
        the__icaf = builder.bitcast(builder.extract_value(pgwiv__jajx, 
            kmp__tdrvk + 1), yhxg__ufjqt)
        glwlp__hoha.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, the__icaf)
        builder.store(glwlp__hoha._getvalue(), dodls__ztej)
        rhliz__val = context.make_helper(builder, arr_typ)
        rhliz__val.meminfo = ggus__ilf
        return rhliz__val._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        mem__xrl = []
        kmp__tdrvk = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for oan__tcd in arr_typ.data:
            jicc__wpswg, lengths_pos, infos_pos = nested_to_array(context,
                builder, oan__tcd, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            mem__xrl.append(jicc__wpswg)
        mgdpe__tzm = StructArrayPayloadType(arr_typ.data)
        xzi__usmj = context.get_value_type(mgdpe__tzm)
        xroxn__yje = context.get_abi_sizeof(xzi__usmj)
        vyh__dgq = define_struct_arr_dtor(context, builder, arr_typ, mgdpe__tzm
            )
        ggus__ilf = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, xroxn__yje), vyh__dgq)
        ywueb__qaj = context.nrt.meminfo_data(builder, ggus__ilf)
        dodls__ztej = builder.bitcast(ywueb__qaj, xzi__usmj.as_pointer())
        glwlp__hoha = cgutils.create_struct_proxy(mgdpe__tzm)(context, builder)
        glwlp__hoha.data = cgutils.pack_array(builder, mem__xrl
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, mem__xrl)
        pgwiv__jajx = builder.load(array_infos_ptr)
        the__icaf = builder.bitcast(builder.extract_value(pgwiv__jajx,
            kmp__tdrvk), yhxg__ufjqt)
        glwlp__hoha.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, the__icaf)
        builder.store(glwlp__hoha._getvalue(), dodls__ztej)
        krb__cipst = context.make_helper(builder, arr_typ)
        krb__cipst.meminfo = ggus__ilf
        return krb__cipst._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        pgwiv__jajx = builder.load(array_infos_ptr)
        ipetw__oxyrj = builder.bitcast(builder.extract_value(pgwiv__jajx,
            infos_pos), yhxg__ufjqt)
        dunc__bdv = context.make_helper(builder, arr_typ)
        fmbpk__ijxp = ArrayItemArrayType(char_arr_type)
        rhliz__val = context.make_helper(builder, fmbpk__ijxp)
        gmnzm__ferwt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='info_to_string_array')
        builder.call(nadu__fau, [ipetw__oxyrj, rhliz__val._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        dunc__bdv.data = rhliz__val._getvalue()
        return dunc__bdv._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        pgwiv__jajx = builder.load(array_infos_ptr)
        lvni__bmo = builder.bitcast(builder.extract_value(pgwiv__jajx, 
            infos_pos + 1), yhxg__ufjqt)
        return _lower_info_to_array_numpy(arr_typ, context, builder, lvni__bmo
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        dkzw__xzxci = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            dkzw__xzxci = int128_type
        elif arr_typ == datetime_date_array_type:
            dkzw__xzxci = types.int64
        pgwiv__jajx = builder.load(array_infos_ptr)
        the__icaf = builder.bitcast(builder.extract_value(pgwiv__jajx,
            infos_pos), yhxg__ufjqt)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, the__icaf)
        lvni__bmo = builder.bitcast(builder.extract_value(pgwiv__jajx, 
            infos_pos + 1), yhxg__ufjqt)
        arr.data = _lower_info_to_array_numpy(types.Array(dkzw__xzxci, 1,
            'C'), context, builder, lvni__bmo)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, fyo__aecol = args
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
                return 1 + sum([get_num_arrays(oan__tcd) for oan__tcd in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(oan__tcd) for oan__tcd in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            thp__poe = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            thp__poe = _get_map_arr_data_type(arr_type)
        else:
            thp__poe = arr_type
        uvmf__bfps = get_num_arrays(thp__poe)
        phx__vdkc = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for fyo__aecol in range(uvmf__bfps)])
        lengths_ptr = cgutils.alloca_once_value(builder, phx__vdkc)
        ndx__clnlu = lir.Constant(lir.IntType(8).as_pointer(), None)
        dtc__ovd = cgutils.pack_array(builder, [ndx__clnlu for fyo__aecol in
            range(get_num_infos(thp__poe))])
        array_infos_ptr = cgutils.alloca_once_value(builder, dtc__ovd)
        gmnzm__ferwt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='info_to_nested_array')
        builder.call(nadu__fau, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, fyo__aecol, fyo__aecol = nested_to_array(context, builder,
            thp__poe, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            pqtg__rvlny = context.make_helper(builder, arr_type)
            pqtg__rvlny.data = arr
            context.nrt.incref(builder, thp__poe, arr)
            arr = pqtg__rvlny._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, thp__poe)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        dunc__bdv = context.make_helper(builder, arr_type)
        fmbpk__ijxp = ArrayItemArrayType(char_arr_type)
        rhliz__val = context.make_helper(builder, fmbpk__ijxp)
        gmnzm__ferwt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='info_to_string_array')
        builder.call(nadu__fau, [in_info, rhliz__val._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        dunc__bdv.data = rhliz__val._getvalue()
        return dunc__bdv._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='get_nested_info')
        xfw__wlwo = builder.call(nadu__fau, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        eyy__xzg = builder.call(nadu__fau, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        bpl__ndra = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        bpl__ndra.data = info_to_array_codegen(context, builder, sig, (
            xfw__wlwo, context.get_constant_null(arr_type.data)))
        byqmr__amini = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = byqmr__amini(array_info_type, byqmr__amini)
        bpl__ndra.indices = info_to_array_codegen(context, builder, sig, (
            eyy__xzg, context.get_constant_null(byqmr__amini)))
        gmnzm__ferwt = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='get_has_global_dictionary')
        oflsy__qeoig = builder.call(nadu__fau, [in_info])
        bpl__ndra.has_global_dictionary = builder.trunc(oflsy__qeoig,
            cgutils.bool_t)
        return bpl__ndra._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        eqi__zmha = get_categories_int_type(arr_type.dtype)
        upwvu__wvm = types.Array(eqi__zmha, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(upwvu__wvm, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            xsiy__acoa = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(xsiy__acoa))
            int_type = arr_type.dtype.int_type
            vxyx__sdghe = bodo.typeof(xsiy__acoa)
            skz__iffxu = context.get_constant_generic(builder, vxyx__sdghe,
                xsiy__acoa)
            iubjn__fqzjh = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(vxyx__sdghe), [skz__iffxu])
        else:
            iubjn__fqzjh = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, iubjn__fqzjh)
        out_arr.dtype = iubjn__fqzjh
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        qwqo__nxcms = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = qwqo__nxcms
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        dkzw__xzxci = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            dkzw__xzxci = int128_type
        elif arr_type == datetime_date_array_type:
            dkzw__xzxci = types.int64
        bdwl__lpj = types.Array(dkzw__xzxci, 1, 'C')
        xhg__xob = context.make_array(bdwl__lpj)(context, builder)
        lppnm__laqix = types.Array(types.uint8, 1, 'C')
        fii__iig = context.make_array(lppnm__laqix)(context, builder)
        fyon__nipa = cgutils.alloca_once(builder, lir.IntType(64))
        eeigf__pwnt = cgutils.alloca_once(builder, lir.IntType(64))
        bqbek__douwo = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        dlujp__yppj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        btguv__wqh = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        wusq__clboh = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        gmnzm__ferwt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='info_to_nullable_array')
        builder.call(nadu__fau, [in_info, fyon__nipa, eeigf__pwnt,
            bqbek__douwo, dlujp__yppj, btguv__wqh, wusq__clboh])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ewik__nrq = context.get_value_type(types.intp)
        qkrgj__wnbbj = cgutils.pack_array(builder, [builder.load(fyon__nipa
            )], ty=ewik__nrq)
        hpgj__ejhdq = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(dkzw__xzxci)))
        ndmeu__jyqj = cgutils.pack_array(builder, [hpgj__ejhdq], ty=ewik__nrq)
        qwqo__nxcms = builder.bitcast(builder.load(bqbek__douwo), context.
            get_data_type(dkzw__xzxci).as_pointer())
        numba.np.arrayobj.populate_array(xhg__xob, data=qwqo__nxcms, shape=
            qkrgj__wnbbj, strides=ndmeu__jyqj, itemsize=hpgj__ejhdq,
            meminfo=builder.load(btguv__wqh))
        arr.data = xhg__xob._getvalue()
        qkrgj__wnbbj = cgutils.pack_array(builder, [builder.load(
            eeigf__pwnt)], ty=ewik__nrq)
        hpgj__ejhdq = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        ndmeu__jyqj = cgutils.pack_array(builder, [hpgj__ejhdq], ty=ewik__nrq)
        qwqo__nxcms = builder.bitcast(builder.load(dlujp__yppj), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(fii__iig, data=qwqo__nxcms, shape=
            qkrgj__wnbbj, strides=ndmeu__jyqj, itemsize=hpgj__ejhdq,
            meminfo=builder.load(wusq__clboh))
        arr.null_bitmap = fii__iig._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        ooe__afh = context.make_array(arr_type.arr_type)(context, builder)
        gjxif__fli = context.make_array(arr_type.arr_type)(context, builder)
        fyon__nipa = cgutils.alloca_once(builder, lir.IntType(64))
        nnm__knuub = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        pvwww__zaebj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        plsu__ehrk = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        lect__mbgtv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        gmnzm__ferwt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='info_to_interval_array')
        builder.call(nadu__fau, [in_info, fyon__nipa, nnm__knuub,
            pvwww__zaebj, plsu__ehrk, lect__mbgtv])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        ewik__nrq = context.get_value_type(types.intp)
        qkrgj__wnbbj = cgutils.pack_array(builder, [builder.load(fyon__nipa
            )], ty=ewik__nrq)
        hpgj__ejhdq = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        ndmeu__jyqj = cgutils.pack_array(builder, [hpgj__ejhdq], ty=ewik__nrq)
        cfnj__ajgi = builder.bitcast(builder.load(nnm__knuub), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(ooe__afh, data=cfnj__ajgi, shape=
            qkrgj__wnbbj, strides=ndmeu__jyqj, itemsize=hpgj__ejhdq,
            meminfo=builder.load(plsu__ehrk))
        arr.left = ooe__afh._getvalue()
        pnkd__dxpu = builder.bitcast(builder.load(pvwww__zaebj), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(gjxif__fli, data=pnkd__dxpu, shape
            =qkrgj__wnbbj, strides=ndmeu__jyqj, itemsize=hpgj__ejhdq,
            meminfo=builder.load(lect__mbgtv))
        arr.right = gjxif__fli._getvalue()
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
        nfxqx__pbykk, fyo__aecol = args
        jftdo__isqo = numba_to_c_type(array_type.dtype)
        zmsns__sga = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), jftdo__isqo))
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='alloc_numpy')
        return builder.call(nadu__fau, [nfxqx__pbykk, builder.load(zmsns__sga)]
            )
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        nfxqx__pbykk, ddx__blwg = args
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='alloc_string_array')
        return builder.call(nadu__fau, [nfxqx__pbykk, ddx__blwg])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    pbp__ydwg, = args
    xkpe__kuyon = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], pbp__ydwg)
    gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
    nadu__fau = cgutils.get_or_insert_function(builder.module, gmnzm__ferwt,
        name='arr_info_list_to_table')
    return builder.call(nadu__fau, [xkpe__kuyon.data, xkpe__kuyon.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='info_from_table')
        return builder.call(nadu__fau, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    xwst__kmp = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        ync__gzd, enx__telsv, fyo__aecol = args
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='info_from_table')
        ndeu__gumn = cgutils.create_struct_proxy(xwst__kmp)(context, builder)
        ndeu__gumn.parent = cgutils.get_null_value(ndeu__gumn.parent.type)
        msvnh__fsmeo = context.make_array(table_idx_arr_t)(context, builder,
            enx__telsv)
        gftd__slu = context.get_constant(types.int64, -1)
        cera__sgoau = context.get_constant(types.int64, 0)
        csvzl__xdf = cgutils.alloca_once_value(builder, cera__sgoau)
        for t, kewna__czwxi in xwst__kmp.type_to_blk.items():
            xbucj__vtwnf = context.get_constant(types.int64, len(xwst__kmp.
                block_to_arr_ind[kewna__czwxi]))
            fyo__aecol, iny__tyd = ListInstance.allocate_ex(context,
                builder, types.List(t), xbucj__vtwnf)
            iny__tyd.size = xbucj__vtwnf
            wswl__zlf = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(xwst__kmp.block_to_arr_ind[
                kewna__czwxi], dtype=np.int64))
            nfaip__tvimu = context.make_array(types.Array(types.int64, 1, 'C')
                )(context, builder, wswl__zlf)
            with cgutils.for_range(builder, xbucj__vtwnf) as levn__bbr:
                hoau__cvwd = levn__bbr.index
                jpl__xrzz = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    nfaip__tvimu, hoau__cvwd)
                mer__cbr = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, msvnh__fsmeo, jpl__xrzz)
                hgdrn__vfj = builder.icmp_unsigned('!=', mer__cbr, gftd__slu)
                with builder.if_else(hgdrn__vfj) as (qow__uci, wqe__weh):
                    with qow__uci:
                        eif__pvf = builder.call(nadu__fau, [ync__gzd, mer__cbr]
                            )
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            eif__pvf])
                        iny__tyd.inititem(hoau__cvwd, arr, incref=False)
                        nfxqx__pbykk = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(nfxqx__pbykk, csvzl__xdf)
                    with wqe__weh:
                        tsco__whhr = context.get_constant_null(t)
                        iny__tyd.inititem(hoau__cvwd, tsco__whhr, incref=False)
            setattr(ndeu__gumn, f'block_{kewna__czwxi}', iny__tyd.value)
        ndeu__gumn.len = builder.load(csvzl__xdf)
        return ndeu__gumn._getvalue()
    return xwst__kmp(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    xwst__kmp = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        kzrnm__oodf, fyo__aecol = args
        pihmc__ysss = cgutils.create_struct_proxy(xwst__kmp)(context,
            builder, kzrnm__oodf)
        if xwst__kmp.has_runtime_cols:
            npcuh__nwviz = lir.Constant(lir.IntType(64), 0)
            for kewna__czwxi, t in enumerate(xwst__kmp.arr_types):
                kysso__pkwj = getattr(pihmc__ysss, f'block_{kewna__czwxi}')
                epxe__imjjv = ListInstance(context, builder, types.List(t),
                    kysso__pkwj)
                npcuh__nwviz = builder.add(npcuh__nwviz, epxe__imjjv.size)
        else:
            npcuh__nwviz = lir.Constant(lir.IntType(64), len(xwst__kmp.
                arr_types))
        fyo__aecol, mpyks__gcex = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), npcuh__nwviz)
        mpyks__gcex.size = npcuh__nwviz
        if xwst__kmp.has_runtime_cols:
            cej__mqbzs = lir.Constant(lir.IntType(64), 0)
            for kewna__czwxi, t in enumerate(xwst__kmp.arr_types):
                kysso__pkwj = getattr(pihmc__ysss, f'block_{kewna__czwxi}')
                epxe__imjjv = ListInstance(context, builder, types.List(t),
                    kysso__pkwj)
                xbucj__vtwnf = epxe__imjjv.size
                with cgutils.for_range(builder, xbucj__vtwnf) as levn__bbr:
                    hoau__cvwd = levn__bbr.index
                    arr = epxe__imjjv.getitem(hoau__cvwd)
                    qon__jsxx = signature(array_info_type, t)
                    rvua__skf = arr,
                    tmi__gqps = array_to_info_codegen(context, builder,
                        qon__jsxx, rvua__skf)
                    mpyks__gcex.inititem(builder.add(cej__mqbzs, hoau__cvwd
                        ), tmi__gqps, incref=False)
                cej__mqbzs = builder.add(cej__mqbzs, xbucj__vtwnf)
        else:
            for t, kewna__czwxi in xwst__kmp.type_to_blk.items():
                xbucj__vtwnf = context.get_constant(types.int64, len(
                    xwst__kmp.block_to_arr_ind[kewna__czwxi]))
                kysso__pkwj = getattr(pihmc__ysss, f'block_{kewna__czwxi}')
                epxe__imjjv = ListInstance(context, builder, types.List(t),
                    kysso__pkwj)
                wswl__zlf = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(xwst__kmp.
                    block_to_arr_ind[kewna__czwxi], dtype=np.int64))
                nfaip__tvimu = context.make_array(types.Array(types.int64, 
                    1, 'C'))(context, builder, wswl__zlf)
                with cgutils.for_range(builder, xbucj__vtwnf) as levn__bbr:
                    hoau__cvwd = levn__bbr.index
                    jpl__xrzz = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        nfaip__tvimu, hoau__cvwd)
                    flfm__mlkf = signature(types.none, xwst__kmp, types.
                        List(t), types.int64, types.int64)
                    qpu__xbm = kzrnm__oodf, kysso__pkwj, hoau__cvwd, jpl__xrzz
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, flfm__mlkf, qpu__xbm)
                    arr = epxe__imjjv.getitem(hoau__cvwd)
                    qon__jsxx = signature(array_info_type, t)
                    rvua__skf = arr,
                    tmi__gqps = array_to_info_codegen(context, builder,
                        qon__jsxx, rvua__skf)
                    mpyks__gcex.inititem(jpl__xrzz, tmi__gqps, incref=False)
        tfhw__ztnr = mpyks__gcex.value
        vhl__urhip = signature(table_type, types.List(array_info_type))
        yrzbc__nwrlk = tfhw__ztnr,
        ync__gzd = arr_info_list_to_table_codegen(context, builder,
            vhl__urhip, yrzbc__nwrlk)
        context.nrt.decref(builder, types.List(array_info_type), tfhw__ztnr)
        return ync__gzd
    return table_type(xwst__kmp, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gmnzm__ferwt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='delete_table')
        builder.call(nadu__fau, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='shuffle_table')
        eowwm__qebsl = builder.call(nadu__fau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
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
        gmnzm__ferwt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='delete_shuffle_info')
        return builder.call(nadu__fau, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='reverse_shuffle_table')
        return builder.call(nadu__fau, args)
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
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='hash_join_table')
        eowwm__qebsl = builder.call(nadu__fau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
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
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='sort_values_table')
        eowwm__qebsl = builder.call(nadu__fau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='sample_table')
        eowwm__qebsl = builder.call(nadu__fau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='shuffle_renormalization')
        eowwm__qebsl = builder.call(nadu__fau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='shuffle_renormalization_group')
        eowwm__qebsl = builder.call(nadu__fau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='drop_duplicates_table')
        eowwm__qebsl = builder.call(nadu__fau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
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
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='pivot_groupby_and_aggregate')
        eowwm__qebsl = builder.call(nadu__fau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
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
        gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        nadu__fau = cgutils.get_or_insert_function(builder.module,
            gmnzm__ferwt, name='groupby_and_aggregate')
        eowwm__qebsl = builder.call(nadu__fau, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eowwm__qebsl
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
    rof__uyd = array_to_info(in_arr)
    zejn__xvar = array_to_info(in_values)
    jamwm__ddb = array_to_info(out_arr)
    drlip__gqjj = arr_info_list_to_table([rof__uyd, zejn__xvar, jamwm__ddb])
    _array_isin(jamwm__ddb, rof__uyd, zejn__xvar, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(drlip__gqjj)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    rof__uyd = array_to_info(in_arr)
    jamwm__ddb = array_to_info(out_arr)
    _get_search_regex(rof__uyd, case, pat, jamwm__ddb)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    noumd__dtkr = col_array_typ.dtype
    if isinstance(noumd__dtkr, types.Number) or noumd__dtkr in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                ndeu__gumn, ijhv__hvyvq = args
                ndeu__gumn = builder.bitcast(ndeu__gumn, lir.IntType(8).
                    as_pointer().as_pointer())
                ulr__esor = lir.Constant(lir.IntType(64), c_ind)
                wgd__hdfnz = builder.load(builder.gep(ndeu__gumn, [ulr__esor]))
                wgd__hdfnz = builder.bitcast(wgd__hdfnz, context.
                    get_data_type(noumd__dtkr).as_pointer())
                return builder.load(builder.gep(wgd__hdfnz, [ijhv__hvyvq]))
            return noumd__dtkr(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                ndeu__gumn, ijhv__hvyvq = args
                ndeu__gumn = builder.bitcast(ndeu__gumn, lir.IntType(8).
                    as_pointer().as_pointer())
                ulr__esor = lir.Constant(lir.IntType(64), c_ind)
                wgd__hdfnz = builder.load(builder.gep(ndeu__gumn, [ulr__esor]))
                gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                aikb__znky = cgutils.get_or_insert_function(builder.module,
                    gmnzm__ferwt, name='array_info_getitem')
                cltml__nfvr = cgutils.alloca_once(builder, lir.IntType(64))
                args = wgd__hdfnz, ijhv__hvyvq, cltml__nfvr
                bqbek__douwo = builder.call(aikb__znky, args)
                return context.make_tuple(builder, sig.return_type, [
                    bqbek__douwo, builder.load(cltml__nfvr)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                bwcu__ost = lir.Constant(lir.IntType(64), 1)
                jan__ahfp = lir.Constant(lir.IntType(64), 2)
                ndeu__gumn, ijhv__hvyvq = args
                ndeu__gumn = builder.bitcast(ndeu__gumn, lir.IntType(8).
                    as_pointer().as_pointer())
                ulr__esor = lir.Constant(lir.IntType(64), c_ind)
                wgd__hdfnz = builder.load(builder.gep(ndeu__gumn, [ulr__esor]))
                gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                rcavv__lthu = cgutils.get_or_insert_function(builder.module,
                    gmnzm__ferwt, name='get_nested_info')
                args = wgd__hdfnz, jan__ahfp
                fesqa__stt = builder.call(rcavv__lthu, args)
                gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                yzuij__dtkf = cgutils.get_or_insert_function(builder.module,
                    gmnzm__ferwt, name='array_info_getdata1')
                args = fesqa__stt,
                qvowr__fgyv = builder.call(yzuij__dtkf, args)
                qvowr__fgyv = builder.bitcast(qvowr__fgyv, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                zndt__zoaoq = builder.sext(builder.load(builder.gep(
                    qvowr__fgyv, [ijhv__hvyvq])), lir.IntType(64))
                args = wgd__hdfnz, bwcu__ost
                acdpa__hjmaz = builder.call(rcavv__lthu, args)
                gmnzm__ferwt = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                aikb__znky = cgutils.get_or_insert_function(builder.module,
                    gmnzm__ferwt, name='array_info_getitem')
                cltml__nfvr = cgutils.alloca_once(builder, lir.IntType(64))
                args = acdpa__hjmaz, zndt__zoaoq, cltml__nfvr
                bqbek__douwo = builder.call(aikb__znky, args)
                return context.make_tuple(builder, sig.return_type, [
                    bqbek__douwo, builder.load(cltml__nfvr)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{noumd__dtkr}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                alqcf__iwp, ijhv__hvyvq = args
                alqcf__iwp = builder.bitcast(alqcf__iwp, lir.IntType(8).
                    as_pointer().as_pointer())
                ulr__esor = lir.Constant(lir.IntType(64), c_ind)
                wgd__hdfnz = builder.load(builder.gep(alqcf__iwp, [ulr__esor]))
                wfahq__wdjf = builder.bitcast(wgd__hdfnz, context.
                    get_data_type(types.bool_).as_pointer())
                wawi__egd = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    wfahq__wdjf, ijhv__hvyvq)
                rumia__swxdc = builder.icmp_unsigned('!=', wawi__egd, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(rumia__swxdc, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        noumd__dtkr = col_array_dtype.dtype
        if noumd__dtkr in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    ndeu__gumn, ijhv__hvyvq = args
                    ndeu__gumn = builder.bitcast(ndeu__gumn, lir.IntType(8)
                        .as_pointer().as_pointer())
                    ulr__esor = lir.Constant(lir.IntType(64), c_ind)
                    wgd__hdfnz = builder.load(builder.gep(ndeu__gumn, [
                        ulr__esor]))
                    wgd__hdfnz = builder.bitcast(wgd__hdfnz, context.
                        get_data_type(noumd__dtkr).as_pointer())
                    nmb__aqhg = builder.load(builder.gep(wgd__hdfnz, [
                        ijhv__hvyvq]))
                    rumia__swxdc = builder.icmp_unsigned('!=', nmb__aqhg,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(rumia__swxdc, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(noumd__dtkr, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    ndeu__gumn, ijhv__hvyvq = args
                    ndeu__gumn = builder.bitcast(ndeu__gumn, lir.IntType(8)
                        .as_pointer().as_pointer())
                    ulr__esor = lir.Constant(lir.IntType(64), c_ind)
                    wgd__hdfnz = builder.load(builder.gep(ndeu__gumn, [
                        ulr__esor]))
                    wgd__hdfnz = builder.bitcast(wgd__hdfnz, context.
                        get_data_type(noumd__dtkr).as_pointer())
                    nmb__aqhg = builder.load(builder.gep(wgd__hdfnz, [
                        ijhv__hvyvq]))
                    kfzx__mbkh = signature(types.bool_, noumd__dtkr)
                    wawi__egd = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, kfzx__mbkh, (nmb__aqhg,))
                    return builder.not_(builder.sext(wawi__egd, lir.IntType(8))
                        )
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
