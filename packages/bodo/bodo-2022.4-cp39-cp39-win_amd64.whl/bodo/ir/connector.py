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
    wlfh__zpge = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    ijc__zoec = []
    for fkdev__wrqer in node.out_vars:
        typ = typemap[fkdev__wrqer.name]
        if typ == types.none:
            continue
        rhjn__rae = array_analysis._gen_shape_call(equiv_set, fkdev__wrqer,
            typ.ndim, None, wlfh__zpge)
        equiv_set.insert_equiv(fkdev__wrqer, rhjn__rae)
        ijc__zoec.append(rhjn__rae[0])
        equiv_set.define(fkdev__wrqer, set())
    if len(ijc__zoec) > 1:
        equiv_set.insert_equiv(*ijc__zoec)
    return [], wlfh__zpge


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        ayw__bik = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        ayw__bik = Distribution.OneD_Var
    else:
        ayw__bik = Distribution.OneD
    for gsi__oehf in node.out_vars:
        if gsi__oehf.name in array_dists:
            ayw__bik = Distribution(min(ayw__bik.value, array_dists[
                gsi__oehf.name].value))
    for gsi__oehf in node.out_vars:
        array_dists[gsi__oehf.name] = ayw__bik


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
    for fkdev__wrqer, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(fkdev__wrqer.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    vyff__bfp = []
    for fkdev__wrqer in node.out_vars:
        ftqy__bkz = visit_vars_inner(fkdev__wrqer, callback, cbdata)
        vyff__bfp.append(ftqy__bkz)
    node.out_vars = vyff__bfp
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for qisaj__oop in node.filters:
            for qkkf__xow in range(len(qisaj__oop)):
                val = qisaj__oop[qkkf__xow]
                qisaj__oop[qkkf__xow] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({gsi__oehf.name for gsi__oehf in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for gaogq__gbpkc in node.filters:
            for gsi__oehf in gaogq__gbpkc:
                if isinstance(gsi__oehf[2], ir.Var):
                    use_set.add(gsi__oehf[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    ngpjr__kay = set(gsi__oehf.name for gsi__oehf in node.out_vars)
    return set(), ngpjr__kay


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    vyff__bfp = []
    for fkdev__wrqer in node.out_vars:
        ftqy__bkz = replace_vars_inner(fkdev__wrqer, var_dict)
        vyff__bfp.append(ftqy__bkz)
    node.out_vars = vyff__bfp
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for qisaj__oop in node.filters:
            for qkkf__xow in range(len(qisaj__oop)):
                val = qisaj__oop[qkkf__xow]
                qisaj__oop[qkkf__xow] = val[0], val[1], replace_vars_inner(val
                    [2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for fkdev__wrqer in node.out_vars:
        yewv__qvyg = definitions[fkdev__wrqer.name]
        if node not in yewv__qvyg:
            yewv__qvyg.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        unc__rqosc = []
        mnlk__yrij = [gsi__oehf[2] for gaogq__gbpkc in filters for
            gsi__oehf in gaogq__gbpkc]
        osoai__pwcpy = set()
        for yrn__rwvzp in mnlk__yrij:
            if isinstance(yrn__rwvzp, ir.Var):
                if yrn__rwvzp.name not in osoai__pwcpy:
                    unc__rqosc.append(yrn__rwvzp)
                osoai__pwcpy.add(yrn__rwvzp.name)
        return {gsi__oehf.name: f'f{qkkf__xow}' for qkkf__xow, gsi__oehf in
            enumerate(unc__rqosc)}, unc__rqosc
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
    fbczs__edx = len(used_columns)
    for qkkf__xow in range(len(used_columns) - 1, -1, -1):
        if used_columns[qkkf__xow] < num_columns:
            break
        fbczs__edx = qkkf__xow
    return used_columns[:fbczs__edx]


def cast_float_to_nullable(df, df_type):
    import bodo
    lmd__vjhnt = {}
    for qkkf__xow, hezc__ckxyk in enumerate(df_type.data):
        if isinstance(hezc__ckxyk, bodo.IntegerArrayType):
            cjxdu__wsdso = hezc__ckxyk.get_pandas_scalar_type_instance
            if cjxdu__wsdso not in lmd__vjhnt:
                lmd__vjhnt[cjxdu__wsdso] = []
            lmd__vjhnt[cjxdu__wsdso].append(df.columns[qkkf__xow])
    for typ, tou__vkyce in lmd__vjhnt.items():
        df[tou__vkyce] = df[tou__vkyce].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    gip__lcfkc = node.out_vars[0].name
    assert isinstance(typemap[gip__lcfkc], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, tsbqk__trc = get_live_column_nums_block(column_live_map,
            equiv_vars, gip__lcfkc)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not tsbqk__trc and not used_columns:
            used_columns = [0]
        if not tsbqk__trc and len(used_columns) != len(node.type_usecol_offset
            ):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    yqde__qtwkb = False
    if array_dists is not None:
        wwwh__ovb = node.out_vars[0].name
        yqde__qtwkb = array_dists[wwwh__ovb] in (Distribution.OneD,
            Distribution.OneD_Var)
        kqeax__wjnz = node.out_vars[1].name
        assert typemap[kqeax__wjnz
            ] == types.none or not yqde__qtwkb or array_dists[kqeax__wjnz] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return yqde__qtwkb
