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
    ufnsn__hge = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    wok__elon = []
    for yfmb__zkjd in node.out_vars:
        typ = typemap[yfmb__zkjd.name]
        if typ == types.none:
            continue
        koqg__jelkm = array_analysis._gen_shape_call(equiv_set, yfmb__zkjd,
            typ.ndim, None, ufnsn__hge)
        equiv_set.insert_equiv(yfmb__zkjd, koqg__jelkm)
        wok__elon.append(koqg__jelkm[0])
        equiv_set.define(yfmb__zkjd, set())
    if len(wok__elon) > 1:
        equiv_set.insert_equiv(*wok__elon)
    return [], ufnsn__hge


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        xblg__napwf = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        xblg__napwf = Distribution.OneD_Var
    else:
        xblg__napwf = Distribution.OneD
    for zzxx__pjx in node.out_vars:
        if zzxx__pjx.name in array_dists:
            xblg__napwf = Distribution(min(xblg__napwf.value, array_dists[
                zzxx__pjx.name].value))
    for zzxx__pjx in node.out_vars:
        array_dists[zzxx__pjx.name] = xblg__napwf


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
    for yfmb__zkjd, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(yfmb__zkjd.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    zkw__udd = []
    for yfmb__zkjd in node.out_vars:
        hub__ndc = visit_vars_inner(yfmb__zkjd, callback, cbdata)
        zkw__udd.append(hub__ndc)
    node.out_vars = zkw__udd
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for teokr__xvai in node.filters:
            for mgfof__qtqh in range(len(teokr__xvai)):
                val = teokr__xvai[mgfof__qtqh]
                teokr__xvai[mgfof__qtqh] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({zzxx__pjx.name for zzxx__pjx in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for fkes__bjf in node.filters:
            for zzxx__pjx in fkes__bjf:
                if isinstance(zzxx__pjx[2], ir.Var):
                    use_set.add(zzxx__pjx[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    qosg__bdfp = set(zzxx__pjx.name for zzxx__pjx in node.out_vars)
    return set(), qosg__bdfp


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    zkw__udd = []
    for yfmb__zkjd in node.out_vars:
        hub__ndc = replace_vars_inner(yfmb__zkjd, var_dict)
        zkw__udd.append(hub__ndc)
    node.out_vars = zkw__udd
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for teokr__xvai in node.filters:
            for mgfof__qtqh in range(len(teokr__xvai)):
                val = teokr__xvai[mgfof__qtqh]
                teokr__xvai[mgfof__qtqh] = val[0], val[1], replace_vars_inner(
                    val[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for yfmb__zkjd in node.out_vars:
        mni__zrrov = definitions[yfmb__zkjd.name]
        if node not in mni__zrrov:
            mni__zrrov.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        frgni__prpt = []
        vivuf__zmkme = [zzxx__pjx[2] for fkes__bjf in filters for zzxx__pjx in
            fkes__bjf]
        akani__xpv = set()
        for byvtu__rju in vivuf__zmkme:
            if isinstance(byvtu__rju, ir.Var):
                if byvtu__rju.name not in akani__xpv:
                    frgni__prpt.append(byvtu__rju)
                akani__xpv.add(byvtu__rju.name)
        return {zzxx__pjx.name: f'f{mgfof__qtqh}' for mgfof__qtqh,
            zzxx__pjx in enumerate(frgni__prpt)}, frgni__prpt
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
    uhu__zbla = len(used_columns)
    for mgfof__qtqh in range(len(used_columns) - 1, -1, -1):
        if used_columns[mgfof__qtqh] < num_columns:
            break
        uhu__zbla = mgfof__qtqh
    return used_columns[:uhu__zbla]


def cast_float_to_nullable(df, df_type):
    import bodo
    jftv__cskgp = {}
    for mgfof__qtqh, hsg__yhcb in enumerate(df_type.data):
        if isinstance(hsg__yhcb, bodo.IntegerArrayType):
            fcvu__tuj = hsg__yhcb.get_pandas_scalar_type_instance
            if fcvu__tuj not in jftv__cskgp:
                jftv__cskgp[fcvu__tuj] = []
            jftv__cskgp[fcvu__tuj].append(df.columns[mgfof__qtqh])
    for typ, ucvq__ccpq in jftv__cskgp.items():
        df[ucvq__ccpq] = df[ucvq__ccpq].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    expa__vkrat = node.out_vars[0].name
    assert isinstance(typemap[expa__vkrat], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, xsdrn__qbt = get_live_column_nums_block(column_live_map,
            equiv_vars, expa__vkrat)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not xsdrn__qbt and not used_columns:
            used_columns = [0]
        if not xsdrn__qbt and len(used_columns) != len(node.type_usecol_offset
            ):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    uoeka__prib = False
    if array_dists is not None:
        vie__pyju = node.out_vars[0].name
        uoeka__prib = array_dists[vie__pyju] in (Distribution.OneD,
            Distribution.OneD_Var)
        xaafm__nxrl = node.out_vars[1].name
        assert typemap[xaafm__nxrl
            ] == types.none or not uoeka__prib or array_dists[xaafm__nxrl] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return uoeka__prib
