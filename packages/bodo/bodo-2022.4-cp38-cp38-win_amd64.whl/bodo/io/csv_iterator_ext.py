"""
Class information for DataFrame iterators returned by pd.read_csv. This is used
to handle situations in which pd.read_csv is used to return chunks with separate
read calls instead of just a single read.
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl
from numba.core.typing.templates import signature
from numba.extending import intrinsic, lower_builtin, models, register_model
import bodo
import bodo.ir.connector
import bodo.ir.csv_ext
from bodo import objmode
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io import csv_cpp
from bodo.ir.csv_ext import _gen_read_csv_objmode, astype
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname
ll.add_symbol('update_csv_reader', csv_cpp.update_csv_reader)
ll.add_symbol('initialize_csv_reader', csv_cpp.initialize_csv_reader)


class CSVIteratorType(types.SimpleIteratorType):

    def __init__(self, df_type, out_colnames, out_types, usecols, sep,
        index_ind, index_arr_typ, index_name, escapechar, storage_options):
        assert isinstance(df_type, DataFrameType
            ), 'CSVIterator must return a DataFrame'
        qwqdv__yuqz = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(qwqdv__yuqz)
        self._yield_type = df_type
        self._out_colnames = out_colnames
        self._out_types = out_types
        self._usecols = usecols
        self._sep = sep
        self._index_ind = index_ind
        self._index_arr_typ = index_arr_typ
        self._index_name = index_name
        self._escapechar = escapechar
        self._storage_options = storage_options

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(CSVIteratorType)
class CSVIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        dpvf__wkh = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, dpvf__wkh)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    zhmdl__ittvr = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, value=args[0])
    lqoc__byu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    vgry__udw = cgutils.get_or_insert_function(builder.module, lqoc__byu,
        name='initialize_csv_reader')
    builder.call(vgry__udw, [zhmdl__ittvr.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), zhmdl__ittvr.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [nit__fory] = sig.args
    [rlqug__irp] = args
    zhmdl__ittvr = cgutils.create_struct_proxy(nit__fory)(context, builder,
        value=rlqug__irp)
    lqoc__byu = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    vgry__udw = cgutils.get_or_insert_function(builder.module, lqoc__byu,
        name='update_csv_reader')
    zzgtj__upw = builder.call(vgry__udw, [zhmdl__ittvr.csv_reader])
    result.set_valid(zzgtj__upw)
    with builder.if_then(zzgtj__upw):
        zzxw__kfc = builder.load(zhmdl__ittvr.index)
        ctjx__tori = types.Tuple([sig.return_type.first_type, types.int64])
        zyr__urj = gen_read_csv_objmode(sig.args[0])
        ihipv__cerb = signature(ctjx__tori, bodo.ir.connector.
            stream_reader_type, types.int64)
        plsdw__fjfvr = context.compile_internal(builder, zyr__urj,
            ihipv__cerb, [zhmdl__ittvr.csv_reader, zzxw__kfc])
        ikmj__rmtwt, elkgw__qtera = cgutils.unpack_tuple(builder, plsdw__fjfvr)
        hdpyo__ynr = builder.add(zzxw__kfc, elkgw__qtera, flags=['nsw'])
        builder.store(hdpyo__ynr, zhmdl__ittvr.index)
        result.yield_(ikmj__rmtwt)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        jyjqu__izipq = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        jyjqu__izipq.csv_reader = args[0]
        pmqel__robjj = context.get_constant(types.uintp, 0)
        jyjqu__izipq.index = cgutils.alloca_once_value(builder, pmqel__robjj)
        return jyjqu__izipq._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    esp__zlav = csv_iterator_typeref.instance_type
    sig = signature(esp__zlav, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    wndk__nyi = 'def read_csv_objmode(f_reader):\n'
    bfbcb__cvyak = [sanitize_varname(ddosg__xtctx) for ddosg__xtctx in
        csv_iterator_type._out_colnames]
    ibkse__msiyl = ir_utils.next_label()
    wpkdu__ktksk = globals()
    out_types = csv_iterator_type._out_types
    wpkdu__ktksk[f'table_type_{ibkse__msiyl}'] = TableType(tuple(out_types))
    wpkdu__ktksk[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    wwhso__wcqr = list(range(len(csv_iterator_type._usecols)))
    wndk__nyi += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        bfbcb__cvyak, out_types, csv_iterator_type._usecols, wwhso__wcqr,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, ibkse__msiyl, wpkdu__ktksk,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    txoht__ikijo = bodo.ir.csv_ext._gen_parallel_flag_name(bfbcb__cvyak)
    nzx__iowkt = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [txoht__ikijo]
    wndk__nyi += f"  return {', '.join(nzx__iowkt)}"
    wpkdu__ktksk = globals()
    ouwlq__nnor = {}
    exec(wndk__nyi, wpkdu__ktksk, ouwlq__nnor)
    boxyi__iacuz = ouwlq__nnor['read_csv_objmode']
    zzyvr__pdkz = numba.njit(boxyi__iacuz)
    bodo.ir.csv_ext.compiled_funcs.append(zzyvr__pdkz)
    nzbb__pqydv = 'def read_func(reader, local_start):\n'
    nzbb__pqydv += f"  {', '.join(nzx__iowkt)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        nzbb__pqydv += f'  local_len = len(T)\n'
        nzbb__pqydv += '  total_size = local_len\n'
        nzbb__pqydv += f'  if ({txoht__ikijo}):\n'
        nzbb__pqydv += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        nzbb__pqydv += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        vic__nff = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        nzbb__pqydv += '  total_size = 0\n'
        vic__nff = (
            f'bodo.utils.conversion.convert_to_index({nzx__iowkt[1]}, {csv_iterator_type._index_name!r})'
            )
    nzbb__pqydv += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({nzx__iowkt[0]},), {vic__nff}, out_df_typ), total_size)
"""
    exec(nzbb__pqydv, {'bodo': bodo, 'objmode_func': zzyvr__pdkz, '_op': np
        .int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, ouwlq__nnor)
    return ouwlq__nnor['read_func']
