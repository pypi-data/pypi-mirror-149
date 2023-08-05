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
        pnj__jhjyw = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(pnj__jhjyw)
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
        edh__wqyfr = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, edh__wqyfr)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    zbbg__yag = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    nfqbm__euwhj = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer()])
    swj__hjuj = cgutils.get_or_insert_function(builder.module, nfqbm__euwhj,
        name='initialize_csv_reader')
    builder.call(swj__hjuj, [zbbg__yag.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), zbbg__yag.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [mxev__ddog] = sig.args
    [iuruh__hhe] = args
    zbbg__yag = cgutils.create_struct_proxy(mxev__ddog)(context, builder,
        value=iuruh__hhe)
    nfqbm__euwhj = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer()])
    swj__hjuj = cgutils.get_or_insert_function(builder.module, nfqbm__euwhj,
        name='update_csv_reader')
    btd__peadh = builder.call(swj__hjuj, [zbbg__yag.csv_reader])
    result.set_valid(btd__peadh)
    with builder.if_then(btd__peadh):
        pcsn__oupn = builder.load(zbbg__yag.index)
        audv__dik = types.Tuple([sig.return_type.first_type, types.int64])
        nzik__jbeqz = gen_read_csv_objmode(sig.args[0])
        kdi__wukgh = signature(audv__dik, bodo.ir.connector.
            stream_reader_type, types.int64)
        yrglv__mpcsa = context.compile_internal(builder, nzik__jbeqz,
            kdi__wukgh, [zbbg__yag.csv_reader, pcsn__oupn])
        upauf__wql, hfhfk__nrjy = cgutils.unpack_tuple(builder, yrglv__mpcsa)
        pwc__uzt = builder.add(pcsn__oupn, hfhfk__nrjy, flags=['nsw'])
        builder.store(pwc__uzt, zbbg__yag.index)
        result.yield_(upauf__wql)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        uevei__ysck = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        uevei__ysck.csv_reader = args[0]
        zpbya__nnhf = context.get_constant(types.uintp, 0)
        uevei__ysck.index = cgutils.alloca_once_value(builder, zpbya__nnhf)
        return uevei__ysck._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    pwbbg__wikpj = csv_iterator_typeref.instance_type
    sig = signature(pwbbg__wikpj, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    iephv__vxke = 'def read_csv_objmode(f_reader):\n'
    icja__qwy = [sanitize_varname(tftsu__moclw) for tftsu__moclw in
        csv_iterator_type._out_colnames]
    mbcj__twcyu = ir_utils.next_label()
    ewsu__mwacn = globals()
    out_types = csv_iterator_type._out_types
    ewsu__mwacn[f'table_type_{mbcj__twcyu}'] = TableType(tuple(out_types))
    ewsu__mwacn[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    zcvf__hgn = list(range(len(csv_iterator_type._usecols)))
    iephv__vxke += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        icja__qwy, out_types, csv_iterator_type._usecols, zcvf__hgn,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, mbcj__twcyu, ewsu__mwacn,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    myhj__cptr = bodo.ir.csv_ext._gen_parallel_flag_name(icja__qwy)
    udmej__lgvww = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [myhj__cptr]
    iephv__vxke += f"  return {', '.join(udmej__lgvww)}"
    ewsu__mwacn = globals()
    aaenu__rzaz = {}
    exec(iephv__vxke, ewsu__mwacn, aaenu__rzaz)
    wqxdc__mbp = aaenu__rzaz['read_csv_objmode']
    vbhmm__vjp = numba.njit(wqxdc__mbp)
    bodo.ir.csv_ext.compiled_funcs.append(vbhmm__vjp)
    wizay__fyoh = 'def read_func(reader, local_start):\n'
    wizay__fyoh += f"  {', '.join(udmej__lgvww)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        wizay__fyoh += f'  local_len = len(T)\n'
        wizay__fyoh += '  total_size = local_len\n'
        wizay__fyoh += f'  if ({myhj__cptr}):\n'
        wizay__fyoh += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        wizay__fyoh += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        mlt__dxcr = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        wizay__fyoh += '  total_size = 0\n'
        mlt__dxcr = (
            f'bodo.utils.conversion.convert_to_index({udmej__lgvww[1]}, {csv_iterator_type._index_name!r})'
            )
    wizay__fyoh += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({udmej__lgvww[0]},), {mlt__dxcr}, out_df_typ), total_size)
"""
    exec(wizay__fyoh, {'bodo': bodo, 'objmode_func': vbhmm__vjp, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, aaenu__rzaz)
    return aaenu__rzaz['read_func']
