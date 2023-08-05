"""
Implementation of pd.read_sql in BODO.
We piggyback on the pandas implementation. Future plan is to have a faster
version for this task.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.table import Table, TableType
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.distributed_api import bcast, bcast_scalar
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_and_propagate_cpp_exception
MPI_ROOT = 0


class SqlReader(ir.Stmt):

    def __init__(self, sql_request, connection, df_out, df_colnames,
        out_vars, out_types, converted_colnames, db_type, loc,
        unsupported_columns, unsupported_arrow_types, is_select_query,
        index_column_name, index_column_type):
        self.connector_typ = 'sql'
        self.sql_request = sql_request
        self.connection = connection
        self.df_out = df_out
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.converted_colnames = converted_colnames
        self.loc = loc
        self.limit = req_limit(sql_request)
        self.db_type = db_type
        self.filters = None
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.is_select_query = is_select_query
        self.index_column_name = index_column_name
        self.index_column_type = index_column_type
        self.type_usecol_offset = list(range(len(df_colnames)))

    def __repr__(self):
        return (
            f'{self.df_out} = ReadSql(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, vars={self.out_vars}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, type_usecol_offset={self.type_usecol_offset},)'
            )


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    ombdn__yuzx = sql_node.out_vars[0].name
    xcfky__wvpk = sql_node.out_vars[1].name
    if ombdn__yuzx not in lives and xcfky__wvpk not in lives:
        return None
    elif ombdn__yuzx not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif xcfky__wvpk not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        rhk__cpbcs = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        mzes__qtklj = []
        lav__mnpdg = []
        for qag__kjvh in sql_node.type_usecol_offset:
            kvnyw__ora = sql_node.df_colnames[qag__kjvh]
            mzes__qtklj.append(kvnyw__ora)
            if isinstance(sql_node.out_types[qag__kjvh], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                lav__mnpdg.append(kvnyw__ora)
        if sql_node.index_column_name:
            mzes__qtklj.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                lav__mnpdg.append(sql_node.index_column_name)
        eyzoo__vslut = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', rhk__cpbcs,
            eyzoo__vslut, mzes__qtklj)
        if lav__mnpdg:
            mpou__xpfz = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', mpou__xpfz,
                eyzoo__vslut, lav__mnpdg)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        zqpc__ynfj = set(sql_node.unsupported_columns)
        ybypf__dcgsn = set(sql_node.type_usecol_offset)
        fkpkp__dtbm = ybypf__dcgsn & zqpc__ynfj
        if fkpkp__dtbm:
            zxwfr__xbrwv = sorted(fkpkp__dtbm)
            ojg__xrrs = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            yip__fhm = 0
            for ccjj__bwtkn in zxwfr__xbrwv:
                while sql_node.unsupported_columns[yip__fhm] != ccjj__bwtkn:
                    yip__fhm += 1
                ojg__xrrs.append(
                    f"Column '{sql_node.original_df_colnames[ccjj__bwtkn]}' with unsupported arrow type {sql_node.unsupported_arrow_types[yip__fhm]}"
                    )
                yip__fhm += 1
            nbln__rxj = '\n'.join(ojg__xrrs)
            raise BodoError(nbln__rxj, loc=sql_node.loc)
    tdmyk__nyfzd, eqyl__qqol = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    mqe__gqgv = ', '.join(tdmyk__nyfzd.values())
    vvb__itjg = f'def sql_impl(sql_request, conn, {mqe__gqgv}):\n'
    if sql_node.filters:
        sfj__sbmz = []
        for jofxw__mwg in sql_node.filters:
            vfhz__klxw = [' '.join(['(', hqmau__mgfdw[0], hqmau__mgfdw[1], 
                '{' + tdmyk__nyfzd[hqmau__mgfdw[2].name] + '}' if
                isinstance(hqmau__mgfdw[2], ir.Var) else hqmau__mgfdw[2],
                ')']) for hqmau__mgfdw in jofxw__mwg]
            sfj__sbmz.append(' ( ' + ' AND '.join(vfhz__klxw) + ' ) ')
        giyt__fkqbf = ' WHERE ' + ' OR '.join(sfj__sbmz)
        for qag__kjvh, osz__ryrt in enumerate(tdmyk__nyfzd.values()):
            vvb__itjg += f'    {osz__ryrt} = get_sql_literal({osz__ryrt})\n'
        vvb__itjg += f'    sql_request = f"{{sql_request}} {giyt__fkqbf}"\n'
    vvb__itjg += (
        '    (table_var, index_var) = _sql_reader_py(sql_request, conn)\n')
    swgb__gizlh = {}
    exec(vvb__itjg, {}, swgb__gizlh)
    msius__wehgc = swgb__gizlh['sql_impl']
    anl__kbzi = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        sql_node.index_column_name, sql_node.index_column_type, sql_node.
        type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, sql_node.is_select_query)
    yfm__ochx = compile_to_numba_ir(msius__wehgc, {'_sql_reader_py':
        anl__kbzi, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type) + tuple(
        typemap[guhtq__kvw.name] for guhtq__kvw in eqyl__qqol), typemap=
        typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query:
        gkpbq__ddfe = [sql_node.df_colnames[qag__kjvh] for qag__kjvh in
            sql_node.type_usecol_offset]
        if sql_node.index_column_name:
            gkpbq__ddfe.append(sql_node.index_column_name)
        miifc__qfg = escape_column_names(gkpbq__ddfe, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            tbfxv__rbjem = ('SELECT ' + miifc__qfg + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            tbfxv__rbjem = ('SELECT ' + miifc__qfg + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        tbfxv__rbjem = sql_node.sql_request
    replace_arg_nodes(yfm__ochx, [ir.Const(tbfxv__rbjem, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc)] + eqyl__qqol)
    sjqj__izrjx = yfm__ochx.body[:-3]
    sjqj__izrjx[-2].target = sql_node.out_vars[0]
    sjqj__izrjx[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        sjqj__izrjx.pop(-1)
    elif not sql_node.type_usecol_offset:
        sjqj__izrjx.pop(-2)
    return sjqj__izrjx


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        gkpbq__ddfe = [(hksu__mlas.upper() if hksu__mlas in
            converted_colnames else hksu__mlas) for hksu__mlas in col_names]
        miifc__qfg = ', '.join([f'"{hksu__mlas}"' for hksu__mlas in
            gkpbq__ddfe])
    elif db_type == 'mysql' or db_type == 'mysql+pymysql':
        miifc__qfg = ', '.join([f'`{hksu__mlas}`' for hksu__mlas in col_names])
    else:
        miifc__qfg = ', '.join([f'"{hksu__mlas}"' for hksu__mlas in col_names])
    return miifc__qfg


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    bwo__wrfb = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(bwo__wrfb,
        'Filter pushdown')
    if bwo__wrfb == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(bwo__wrfb, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif bwo__wrfb == bodo.pd_timestamp_type:

        def impl(filter_value):
            ezyn__nrito = filter_value.nanosecond
            pnfb__pgpy = ''
            if ezyn__nrito < 10:
                pnfb__pgpy = '00'
            elif ezyn__nrito < 100:
                pnfb__pgpy = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{pnfb__pgpy}{ezyn__nrito}'"
                )
        return impl
    elif bwo__wrfb == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {bwo__wrfb} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    gdne__ols = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    bwo__wrfb = types.unliteral(filter_value)
    if isinstance(bwo__wrfb, types.List) and (isinstance(bwo__wrfb.dtype,
        scalar_isinstance) or bwo__wrfb.dtype in gdne__ols):

        def impl(filter_value):
            sox__pqz = ', '.join([_get_snowflake_sql_literal_scalar(
                hksu__mlas) for hksu__mlas in filter_value])
            return f'({sox__pqz})'
        return impl
    elif isinstance(bwo__wrfb, scalar_isinstance) or bwo__wrfb in gdne__ols:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {bwo__wrfb} used in filter pushdown.'
            )


def sql_remove_dead_column(sql_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(sql_node,
        column_live_map, equiv_vars, typemap, 'SQLReader', sql_node.df_colnames
        )


numba.parfors.array_analysis.array_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[SqlReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[SqlReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[SqlReader] = remove_dead_sql
numba.core.analysis.ir_extension_usedefs[SqlReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[SqlReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[SqlReader] = sql_distributed_run
remove_dead_column_extensions[SqlReader] = sql_remove_dead_column
ir_extension_table_column_use[SqlReader
    ] = bodo.ir.connector.connector_table_column_use
compiled_funcs = []


@numba.njit
def sqlalchemy_check():
    with numba.objmode():
        sqlalchemy_check_()


def sqlalchemy_check_():
    try:
        import sqlalchemy
    except ImportError as ixvw__zcuh:
        yot__fkogp = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(yot__fkogp)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as ixvw__zcuh:
        yot__fkogp = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(yot__fkogp)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as ixvw__zcuh:
        yot__fkogp = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(yot__fkogp)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as ixvw__zcuh:
        yot__fkogp = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(yot__fkogp)


def req_limit(sql_request):
    import re
    ctjr__yfhvh = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    nel__twh = ctjr__yfhvh.search(sql_request)
    if nel__twh:
        return int(nel__twh.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, is_select_query):
    nhhev__tuqg = next_label()
    gkpbq__ddfe = [col_names[qag__kjvh] for qag__kjvh in type_usecol_offset]
    cei__mipz = [col_typs[qag__kjvh] for qag__kjvh in type_usecol_offset]
    if index_column_name:
        gkpbq__ddfe.append(index_column_name)
        cei__mipz.append(index_column_type)
    nwk__fie = None
    fjfmb__hzfyd = None
    udq__sofvr = types.none
    if type_usecol_offset:
        udq__sofvr = TableType(tuple(col_typs))
    vvb__itjg = 'def sql_reader_py(sql_request, conn):\n'
    if db_type == 'snowflake':
        vvb__itjg += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")

        def is_nullable(typ):
            return bodo.utils.utils.is_array_typ(typ, False
                ) and not isinstance(typ, types.Array) and not isinstance(typ,
                bodo.DatetimeArrayType)
        uia__nbm = [int(is_nullable(col_typs[qag__kjvh])) for qag__kjvh in
            type_usecol_offset]
        if index_column_name:
            uia__nbm.append(int(is_nullable(index_column_type)))
        vvb__itjg += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(uia__nbm)}, np.array({uia__nbm}, dtype=np.int32).ctypes)
"""
        vvb__itjg += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            vvb__itjg += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            vvb__itjg += '  index_var = None\n'
        if type_usecol_offset:
            yip__fhm = []
            juzws__slbs = 0
            for qag__kjvh in range(len(col_names)):
                if juzws__slbs < len(type_usecol_offset
                    ) and qag__kjvh == type_usecol_offset[juzws__slbs]:
                    yip__fhm.append(juzws__slbs)
                    juzws__slbs += 1
                else:
                    yip__fhm.append(-1)
            nwk__fie = np.array(yip__fhm, dtype=np.int64)
            vvb__itjg += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{nhhev__tuqg}, py_table_type_{nhhev__tuqg})
"""
        else:
            vvb__itjg += '  table_var = None\n'
        vvb__itjg += '  delete_table(out_table)\n'
        vvb__itjg += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            vvb__itjg += f"""  type_usecols_offsets_arr_{nhhev__tuqg}_2 = type_usecols_offsets_arr_{nhhev__tuqg}
"""
            fjfmb__hzfyd = np.array(type_usecol_offset, dtype=np.int64)
        vvb__itjg += '  df_typeref_2 = df_typeref\n'
        vvb__itjg += '  sqlalchemy_check()\n'
        if db_type == 'mysql' or db_type == 'mysql+pymysql':
            vvb__itjg += '  pymysql_check()\n'
        elif db_type == 'oracle':
            vvb__itjg += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            vvb__itjg += '  psycopg2_check()\n'
        if parallel and is_select_query:
            vvb__itjg += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                vvb__itjg += f'  nb_row = {limit}\n'
            else:
                vvb__itjg += '  with objmode(nb_row="int64"):\n'
                vvb__itjg += f'     if rank == {MPI_ROOT}:\n'
                vvb__itjg += (
                    "         sql_cons = 'select count(*) from (' + sql_request + ') x'\n"
                    )
                vvb__itjg += '         frame = pd.read_sql(sql_cons, conn)\n'
                vvb__itjg += '         nb_row = frame.iat[0,0]\n'
                vvb__itjg += '     else:\n'
                vvb__itjg += '         nb_row = 0\n'
                vvb__itjg += '  nb_row = bcast_scalar(nb_row)\n'
            vvb__itjg += f"""  with objmode(table_var=py_table_type_{nhhev__tuqg}, index_var=index_col_typ):
"""
            vvb__itjg += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                vvb__itjg += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                vvb__itjg += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            vvb__itjg += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            vvb__itjg += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            vvb__itjg += f"""  with objmode(table_var=py_table_type_{nhhev__tuqg}, index_var=index_col_typ):
"""
            vvb__itjg += '    df_ret = pd.read_sql(sql_request, conn)\n'
            vvb__itjg += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            vvb__itjg += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            vvb__itjg += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            vvb__itjg += '    index_var = None\n'
        if type_usecol_offset:
            vvb__itjg += f'    arrs = []\n'
            vvb__itjg += f'    for i in range(df_ret.shape[1]):\n'
            vvb__itjg += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            vvb__itjg += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{nhhev__tuqg}_2, {len(col_names)})
"""
        else:
            vvb__itjg += '    table_var = None\n'
    vvb__itjg += '  return (table_var, index_var)\n'
    kpyh__rejq = globals()
    kpyh__rejq.update({'bodo': bodo, f'py_table_type_{nhhev__tuqg}':
        udq__sofvr, 'index_col_typ': index_column_type})
    if db_type == 'snowflake':
        kpyh__rejq.update({'np': np, 'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'snowflake_read':
            _snowflake_read, 'info_to_array': info_to_array,
            'info_from_table': info_from_table, 'delete_table':
            delete_table, 'cpp_table_to_py_table': cpp_table_to_py_table,
            f'table_idx_{nhhev__tuqg}': nwk__fie})
    else:
        kpyh__rejq.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(cei__mipz), bodo.RangeIndexType(None),
            tuple(gkpbq__ddfe)), 'Table': Table,
            f'type_usecols_offsets_arr_{nhhev__tuqg}': fjfmb__hzfyd})
    swgb__gizlh = {}
    exec(vvb__itjg, kpyh__rejq, swgb__gizlh)
    anl__kbzi = swgb__gizlh['sql_reader_py']
    yanlb__bpubm = numba.njit(anl__kbzi)
    compiled_funcs.append(yanlb__bpubm)
    return yanlb__bpubm


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.int64, types.voidptr))
import llvmlite.binding as ll
from bodo.io import arrow_cpp
ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
