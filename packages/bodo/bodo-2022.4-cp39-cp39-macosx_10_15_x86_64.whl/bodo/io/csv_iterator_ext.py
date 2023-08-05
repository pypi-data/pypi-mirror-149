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
        zrcs__fki = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(zrcs__fki)
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
        sti__afmok = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, sti__afmok)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    vix__dvjyu = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    yizdz__afbpb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer()])
    vas__qscl = cgutils.get_or_insert_function(builder.module, yizdz__afbpb,
        name='initialize_csv_reader')
    builder.call(vas__qscl, [vix__dvjyu.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), vix__dvjyu.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [vihp__ihr] = sig.args
    [sfve__yipar] = args
    vix__dvjyu = cgutils.create_struct_proxy(vihp__ihr)(context, builder,
        value=sfve__yipar)
    yizdz__afbpb = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer()])
    vas__qscl = cgutils.get_or_insert_function(builder.module, yizdz__afbpb,
        name='update_csv_reader')
    srj__yazbk = builder.call(vas__qscl, [vix__dvjyu.csv_reader])
    result.set_valid(srj__yazbk)
    with builder.if_then(srj__yazbk):
        azux__sce = builder.load(vix__dvjyu.index)
        arjsj__mfy = types.Tuple([sig.return_type.first_type, types.int64])
        enzk__mejis = gen_read_csv_objmode(sig.args[0])
        wdr__qsbaz = signature(arjsj__mfy, bodo.ir.connector.
            stream_reader_type, types.int64)
        qucfm__apsi = context.compile_internal(builder, enzk__mejis,
            wdr__qsbaz, [vix__dvjyu.csv_reader, azux__sce])
        mfut__efew, mazv__xle = cgutils.unpack_tuple(builder, qucfm__apsi)
        knu__wcbbm = builder.add(azux__sce, mazv__xle, flags=['nsw'])
        builder.store(knu__wcbbm, vix__dvjyu.index)
        result.yield_(mfut__efew)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        dfme__awvvd = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        dfme__awvvd.csv_reader = args[0]
        cfx__zjcb = context.get_constant(types.uintp, 0)
        dfme__awvvd.index = cgutils.alloca_once_value(builder, cfx__zjcb)
        return dfme__awvvd._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    erny__ttyi = csv_iterator_typeref.instance_type
    sig = signature(erny__ttyi, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    tep__lnnh = 'def read_csv_objmode(f_reader):\n'
    pur__lcurm = [sanitize_varname(jgpuk__eex) for jgpuk__eex in
        csv_iterator_type._out_colnames]
    fxjs__vcdhz = ir_utils.next_label()
    qnicy__loqvu = globals()
    out_types = csv_iterator_type._out_types
    qnicy__loqvu[f'table_type_{fxjs__vcdhz}'] = TableType(tuple(out_types))
    qnicy__loqvu[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    rvd__gcrpj = list(range(len(csv_iterator_type._usecols)))
    tep__lnnh += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        pur__lcurm, out_types, csv_iterator_type._usecols, rvd__gcrpj,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, fxjs__vcdhz, qnicy__loqvu,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    qcp__yhwuo = bodo.ir.csv_ext._gen_parallel_flag_name(pur__lcurm)
    ojjwl__aat = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [qcp__yhwuo]
    tep__lnnh += f"  return {', '.join(ojjwl__aat)}"
    qnicy__loqvu = globals()
    qvl__dsm = {}
    exec(tep__lnnh, qnicy__loqvu, qvl__dsm)
    zbj__vil = qvl__dsm['read_csv_objmode']
    dmh__kkfki = numba.njit(zbj__vil)
    bodo.ir.csv_ext.compiled_funcs.append(dmh__kkfki)
    dahy__nxshc = 'def read_func(reader, local_start):\n'
    dahy__nxshc += f"  {', '.join(ojjwl__aat)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        dahy__nxshc += f'  local_len = len(T)\n'
        dahy__nxshc += '  total_size = local_len\n'
        dahy__nxshc += f'  if ({qcp__yhwuo}):\n'
        dahy__nxshc += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        dahy__nxshc += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        lawma__mhuz = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        dahy__nxshc += '  total_size = 0\n'
        lawma__mhuz = (
            f'bodo.utils.conversion.convert_to_index({ojjwl__aat[1]}, {csv_iterator_type._index_name!r})'
            )
    dahy__nxshc += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({ojjwl__aat[0]},), {lawma__mhuz}, out_df_typ), total_size)
"""
    exec(dahy__nxshc, {'bodo': bodo, 'objmode_func': dmh__kkfki, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, qvl__dsm)
    return qvl__dsm['read_func']
