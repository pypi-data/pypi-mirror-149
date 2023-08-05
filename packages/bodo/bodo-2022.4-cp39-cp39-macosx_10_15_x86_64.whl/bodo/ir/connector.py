"""
Common IR extension functions for connectors such as CSV, Parquet and JSON readers.
"""
from collections import defaultdict
import numba
from numba.core import ir, types
from numba.core.ir_utils import replace_vars_inner, visit_vars_inner
from numba.extending import box, models, register_model
from bodo.hiframes.table import TableType
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import get_live_column_nums_block
from bodo.utils.utils import debug_prints


def connector_array_analysis(node, equiv_set, typemap, array_analysis):
    uvizg__cyevh = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    oso__qxmig = []
    for eua__cvo in node.out_vars:
        typ = typemap[eua__cvo.name]
        if typ == types.none:
            continue
        qidq__vpv = array_analysis._gen_shape_call(equiv_set, eua__cvo, typ
            .ndim, None, uvizg__cyevh)
        equiv_set.insert_equiv(eua__cvo, qidq__vpv)
        oso__qxmig.append(qidq__vpv[0])
        equiv_set.define(eua__cvo, set())
    if len(oso__qxmig) > 1:
        equiv_set.insert_equiv(*oso__qxmig)
    return [], uvizg__cyevh


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        ytuh__ykw = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        ytuh__ykw = Distribution.OneD_Var
    else:
        ytuh__ykw = Distribution.OneD
    for urb__nzp in node.out_vars:
        if urb__nzp.name in array_dists:
            ytuh__ykw = Distribution(min(ytuh__ykw.value, array_dists[
                urb__nzp.name].value))
    for urb__nzp in node.out_vars:
        array_dists[urb__nzp.name] = ytuh__ykw


def connector_typeinfer(node, typeinferer):
    if node.connector_typ == 'csv':
        if node.chunksize is not None:
            typeinferer.lock_type(node.out_vars[0].name, node.out_types[0],
                loc=node.loc)
        else:
            typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(
                node.out_types)), loc=node.loc)
            typeinferer.lock_type(node.out_vars[1].name, node.
                index_column_typ, loc=node.loc)
        return
    if node.connector_typ in ('parquet', 'sql'):
        typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(node.
            out_types)), loc=node.loc)
        typeinferer.lock_type(node.out_vars[1].name, node.index_column_type,
            loc=node.loc)
        return
    for eua__cvo, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(eua__cvo.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    wpt__cuslh = []
    for eua__cvo in node.out_vars:
        dlapg__zxhjw = visit_vars_inner(eua__cvo, callback, cbdata)
        wpt__cuslh.append(dlapg__zxhjw)
    node.out_vars = wpt__cuslh
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for anwnf__zxo in node.filters:
            for iwgqh__uguf in range(len(anwnf__zxo)):
                val = anwnf__zxo[iwgqh__uguf]
                anwnf__zxo[iwgqh__uguf] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({urb__nzp.name for urb__nzp in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for tgt__uwb in node.filters:
            for urb__nzp in tgt__uwb:
                if isinstance(urb__nzp[2], ir.Var):
                    use_set.add(urb__nzp[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    dunzj__fhpk = set(urb__nzp.name for urb__nzp in node.out_vars)
    return set(), dunzj__fhpk


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    wpt__cuslh = []
    for eua__cvo in node.out_vars:
        dlapg__zxhjw = replace_vars_inner(eua__cvo, var_dict)
        wpt__cuslh.append(dlapg__zxhjw)
    node.out_vars = wpt__cuslh
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for anwnf__zxo in node.filters:
            for iwgqh__uguf in range(len(anwnf__zxo)):
                val = anwnf__zxo[iwgqh__uguf]
                anwnf__zxo[iwgqh__uguf] = val[0], val[1], replace_vars_inner(
                    val[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for eua__cvo in node.out_vars:
        spycc__gcgi = definitions[eua__cvo.name]
        if node not in spycc__gcgi:
            spycc__gcgi.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        rwpt__gpdb = []
        eopg__nta = [urb__nzp[2] for tgt__uwb in filters for urb__nzp in
            tgt__uwb]
        bzreh__yaf = set()
        for pvhko__luat in eopg__nta:
            if isinstance(pvhko__luat, ir.Var):
                if pvhko__luat.name not in bzreh__yaf:
                    rwpt__gpdb.append(pvhko__luat)
                bzreh__yaf.add(pvhko__luat.name)
        return {urb__nzp.name: f'f{iwgqh__uguf}' for iwgqh__uguf, urb__nzp in
            enumerate(rwpt__gpdb)}, rwpt__gpdb
    else:
        return {}, []


class StreamReaderType(types.Opaque):

    def __init__(self):
        super(StreamReaderType, self).__init__(name='StreamReaderType')


stream_reader_type = StreamReaderType()
register_model(StreamReaderType)(models.OpaqueModel)


@box(StreamReaderType)
def box_stream_reader(typ, val, c):
    c.pyapi.incref(val)
    return val


def trim_extra_used_columns(used_columns, num_columns):
    krofg__mnkn = len(used_columns)
    for iwgqh__uguf in range(len(used_columns) - 1, -1, -1):
        if used_columns[iwgqh__uguf] < num_columns:
            break
        krofg__mnkn = iwgqh__uguf
    return used_columns[:krofg__mnkn]


def cast_float_to_nullable(df, df_type):
    import bodo
    xiq__cnhzu = {}
    for iwgqh__uguf, kmpl__yzmhl in enumerate(df_type.data):
        if isinstance(kmpl__yzmhl, bodo.IntegerArrayType):
            swtk__qhyj = kmpl__yzmhl.get_pandas_scalar_type_instance
            if swtk__qhyj not in xiq__cnhzu:
                xiq__cnhzu[swtk__qhyj] = []
            xiq__cnhzu[swtk__qhyj].append(df.columns[iwgqh__uguf])
    for typ, akwis__wmi in xiq__cnhzu.items():
        df[akwis__wmi] = df[akwis__wmi].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    laewt__iug = node.out_vars[0].name
    assert isinstance(typemap[laewt__iug], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, lsbye__iscvb = get_live_column_nums_block(column_live_map
            , equiv_vars, laewt__iug)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not lsbye__iscvb and not used_columns:
            used_columns = [0]
        if not lsbye__iscvb and len(used_columns) != len(node.
            type_usecol_offset):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    msb__jzn = False
    if array_dists is not None:
        fsio__hvjfm = node.out_vars[0].name
        msb__jzn = array_dists[fsio__hvjfm] in (Distribution.OneD,
            Distribution.OneD_Var)
        vxfu__ivv = node.out_vars[1].name
        assert typemap[vxfu__ivv] == types.none or not msb__jzn or array_dists[
            vxfu__ivv] in (Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return msb__jzn
