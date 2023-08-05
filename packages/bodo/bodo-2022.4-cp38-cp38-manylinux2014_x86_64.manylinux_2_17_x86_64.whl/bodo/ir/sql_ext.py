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
    rvu__ngwj = sql_node.out_vars[0].name
    cwyd__qgsr = sql_node.out_vars[1].name
    if rvu__ngwj not in lives and cwyd__qgsr not in lives:
        return None
    elif rvu__ngwj not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif cwyd__qgsr not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        kgoh__bpov = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        tyutw__qbaw = []
        ktxi__lzlvy = []
        for cnx__xoq in sql_node.type_usecol_offset:
            yoa__acox = sql_node.df_colnames[cnx__xoq]
            tyutw__qbaw.append(yoa__acox)
            if isinstance(sql_node.out_types[cnx__xoq], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                ktxi__lzlvy.append(yoa__acox)
        if sql_node.index_column_name:
            tyutw__qbaw.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                ktxi__lzlvy.append(sql_node.index_column_name)
        wuzxt__xtmdg = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', kgoh__bpov,
            wuzxt__xtmdg, tyutw__qbaw)
        if ktxi__lzlvy:
            jfk__okn = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', jfk__okn,
                wuzxt__xtmdg, ktxi__lzlvy)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        lte__iars = set(sql_node.unsupported_columns)
        rqes__zky = set(sql_node.type_usecol_offset)
        trqi__uptyf = rqes__zky & lte__iars
        if trqi__uptyf:
            xzckm__yix = sorted(trqi__uptyf)
            ettb__kpci = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            tmn__ddvk = 0
            for bgkmy__tnbfa in xzckm__yix:
                while sql_node.unsupported_columns[tmn__ddvk] != bgkmy__tnbfa:
                    tmn__ddvk += 1
                ettb__kpci.append(
                    f"Column '{sql_node.original_df_colnames[bgkmy__tnbfa]}' with unsupported arrow type {sql_node.unsupported_arrow_types[tmn__ddvk]}"
                    )
                tmn__ddvk += 1
            phde__ryunu = '\n'.join(ettb__kpci)
            raise BodoError(phde__ryunu, loc=sql_node.loc)
    hfn__riv, jiphy__abbxf = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    xwwj__cba = ', '.join(hfn__riv.values())
    qgyfz__ueguk = f'def sql_impl(sql_request, conn, {xwwj__cba}):\n'
    if sql_node.filters:
        jgs__vtq = []
        for icuan__oqtag in sql_node.filters:
            vrn__dukiw = [' '.join(['(', huf__hui[0], huf__hui[1], '{' +
                hfn__riv[huf__hui[2].name] + '}' if isinstance(huf__hui[2],
                ir.Var) else huf__hui[2], ')']) for huf__hui in icuan__oqtag]
            jgs__vtq.append(' ( ' + ' AND '.join(vrn__dukiw) + ' ) ')
        bzp__pptg = ' WHERE ' + ' OR '.join(jgs__vtq)
        for cnx__xoq, qubv__qeu in enumerate(hfn__riv.values()):
            qgyfz__ueguk += f'    {qubv__qeu} = get_sql_literal({qubv__qeu})\n'
        qgyfz__ueguk += f'    sql_request = f"{{sql_request}} {bzp__pptg}"\n'
    qgyfz__ueguk += (
        '    (table_var, index_var) = _sql_reader_py(sql_request, conn)\n')
    rpvhy__qbrm = {}
    exec(qgyfz__ueguk, {}, rpvhy__qbrm)
    vnaad__wow = rpvhy__qbrm['sql_impl']
    lsu__jgks = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        sql_node.index_column_name, sql_node.index_column_type, sql_node.
        type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, sql_node.is_select_query)
    bkb__mqdzx = compile_to_numba_ir(vnaad__wow, {'_sql_reader_py':
        lsu__jgks, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type) + tuple(
        typemap[agwj__qzqf.name] for agwj__qzqf in jiphy__abbxf), typemap=
        typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query:
        dgc__ugf = [sql_node.df_colnames[cnx__xoq] for cnx__xoq in sql_node
            .type_usecol_offset]
        if sql_node.index_column_name:
            dgc__ugf.append(sql_node.index_column_name)
        lefll__djtp = escape_column_names(dgc__ugf, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            hlqa__ykcv = ('SELECT ' + lefll__djtp + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            hlqa__ykcv = ('SELECT ' + lefll__djtp + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        hlqa__ykcv = sql_node.sql_request
    replace_arg_nodes(bkb__mqdzx, [ir.Const(hlqa__ykcv, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc)] + jiphy__abbxf)
    bpg__tde = bkb__mqdzx.body[:-3]
    bpg__tde[-2].target = sql_node.out_vars[0]
    bpg__tde[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        bpg__tde.pop(-1)
    elif not sql_node.type_usecol_offset:
        bpg__tde.pop(-2)
    return bpg__tde


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        dgc__ugf = [(rljus__tlu.upper() if rljus__tlu in converted_colnames
             else rljus__tlu) for rljus__tlu in col_names]
        lefll__djtp = ', '.join([f'"{rljus__tlu}"' for rljus__tlu in dgc__ugf])
    elif db_type == 'mysql' or db_type == 'mysql+pymysql':
        lefll__djtp = ', '.join([f'`{rljus__tlu}`' for rljus__tlu in col_names]
            )
    else:
        lefll__djtp = ', '.join([f'"{rljus__tlu}"' for rljus__tlu in col_names]
            )
    return lefll__djtp


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    mgbf__yadnk = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(mgbf__yadnk,
        'Filter pushdown')
    if mgbf__yadnk == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(mgbf__yadnk, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif mgbf__yadnk == bodo.pd_timestamp_type:

        def impl(filter_value):
            vok__atfrr = filter_value.nanosecond
            ebroz__kfchd = ''
            if vok__atfrr < 10:
                ebroz__kfchd = '00'
            elif vok__atfrr < 100:
                ebroz__kfchd = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{ebroz__kfchd}{vok__atfrr}'"
                )
        return impl
    elif mgbf__yadnk == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {mgbf__yadnk} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    vcka__sgmyz = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    mgbf__yadnk = types.unliteral(filter_value)
    if isinstance(mgbf__yadnk, types.List) and (isinstance(mgbf__yadnk.
        dtype, scalar_isinstance) or mgbf__yadnk.dtype in vcka__sgmyz):

        def impl(filter_value):
            jic__avl = ', '.join([_get_snowflake_sql_literal_scalar(
                rljus__tlu) for rljus__tlu in filter_value])
            return f'({jic__avl})'
        return impl
    elif isinstance(mgbf__yadnk, scalar_isinstance
        ) or mgbf__yadnk in vcka__sgmyz:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {mgbf__yadnk} used in filter pushdown.'
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
    except ImportError as hjtvy__jhfz:
        aahac__ksxmb = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(aahac__ksxmb)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as hjtvy__jhfz:
        aahac__ksxmb = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(aahac__ksxmb)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as hjtvy__jhfz:
        aahac__ksxmb = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(aahac__ksxmb)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as hjtvy__jhfz:
        aahac__ksxmb = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(aahac__ksxmb)


def req_limit(sql_request):
    import re
    let__gtkyc = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    ztet__nsqc = let__gtkyc.search(sql_request)
    if ztet__nsqc:
        return int(ztet__nsqc.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, is_select_query):
    zndxr__bomie = next_label()
    dgc__ugf = [col_names[cnx__xoq] for cnx__xoq in type_usecol_offset]
    nlr__dod = [col_typs[cnx__xoq] for cnx__xoq in type_usecol_offset]
    if index_column_name:
        dgc__ugf.append(index_column_name)
        nlr__dod.append(index_column_type)
    ftopi__fxca = None
    oqjqw__sjzp = None
    qkeuw__hfv = types.none
    if type_usecol_offset:
        qkeuw__hfv = TableType(tuple(col_typs))
    qgyfz__ueguk = 'def sql_reader_py(sql_request, conn):\n'
    if db_type == 'snowflake':
        qgyfz__ueguk += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")

        def is_nullable(typ):
            return bodo.utils.utils.is_array_typ(typ, False
                ) and not isinstance(typ, types.Array) and not isinstance(typ,
                bodo.DatetimeArrayType)
        mtpw__wqp = [int(is_nullable(col_typs[cnx__xoq])) for cnx__xoq in
            type_usecol_offset]
        if index_column_name:
            mtpw__wqp.append(int(is_nullable(index_column_type)))
        qgyfz__ueguk += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(mtpw__wqp)}, np.array({mtpw__wqp}, dtype=np.int32).ctypes)
"""
        qgyfz__ueguk += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            qgyfz__ueguk += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            qgyfz__ueguk += '  index_var = None\n'
        if type_usecol_offset:
            tmn__ddvk = []
            yyew__tyn = 0
            for cnx__xoq in range(len(col_names)):
                if yyew__tyn < len(type_usecol_offset
                    ) and cnx__xoq == type_usecol_offset[yyew__tyn]:
                    tmn__ddvk.append(yyew__tyn)
                    yyew__tyn += 1
                else:
                    tmn__ddvk.append(-1)
            ftopi__fxca = np.array(tmn__ddvk, dtype=np.int64)
            qgyfz__ueguk += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{zndxr__bomie}, py_table_type_{zndxr__bomie})
"""
        else:
            qgyfz__ueguk += '  table_var = None\n'
        qgyfz__ueguk += '  delete_table(out_table)\n'
        qgyfz__ueguk += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            qgyfz__ueguk += f"""  type_usecols_offsets_arr_{zndxr__bomie}_2 = type_usecols_offsets_arr_{zndxr__bomie}
"""
            oqjqw__sjzp = np.array(type_usecol_offset, dtype=np.int64)
        qgyfz__ueguk += '  df_typeref_2 = df_typeref\n'
        qgyfz__ueguk += '  sqlalchemy_check()\n'
        if db_type == 'mysql' or db_type == 'mysql+pymysql':
            qgyfz__ueguk += '  pymysql_check()\n'
        elif db_type == 'oracle':
            qgyfz__ueguk += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            qgyfz__ueguk += '  psycopg2_check()\n'
        if parallel and is_select_query:
            qgyfz__ueguk += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                qgyfz__ueguk += f'  nb_row = {limit}\n'
            else:
                qgyfz__ueguk += '  with objmode(nb_row="int64"):\n'
                qgyfz__ueguk += f'     if rank == {MPI_ROOT}:\n'
                qgyfz__ueguk += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                qgyfz__ueguk += (
                    '         frame = pd.read_sql(sql_cons, conn)\n')
                qgyfz__ueguk += '         nb_row = frame.iat[0,0]\n'
                qgyfz__ueguk += '     else:\n'
                qgyfz__ueguk += '         nb_row = 0\n'
                qgyfz__ueguk += '  nb_row = bcast_scalar(nb_row)\n'
            qgyfz__ueguk += f"""  with objmode(table_var=py_table_type_{zndxr__bomie}, index_var=index_col_typ):
"""
            qgyfz__ueguk += """    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)
"""
            if db_type == 'oracle':
                qgyfz__ueguk += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                qgyfz__ueguk += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            qgyfz__ueguk += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            qgyfz__ueguk += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            qgyfz__ueguk += f"""  with objmode(table_var=py_table_type_{zndxr__bomie}, index_var=index_col_typ):
"""
            qgyfz__ueguk += '    df_ret = pd.read_sql(sql_request, conn)\n'
            qgyfz__ueguk += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            qgyfz__ueguk += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            qgyfz__ueguk += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            qgyfz__ueguk += '    index_var = None\n'
        if type_usecol_offset:
            qgyfz__ueguk += f'    arrs = []\n'
            qgyfz__ueguk += f'    for i in range(df_ret.shape[1]):\n'
            qgyfz__ueguk += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            qgyfz__ueguk += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{zndxr__bomie}_2, {len(col_names)})
"""
        else:
            qgyfz__ueguk += '    table_var = None\n'
    qgyfz__ueguk += '  return (table_var, index_var)\n'
    ootp__pio = globals()
    ootp__pio.update({'bodo': bodo, f'py_table_type_{zndxr__bomie}':
        qkeuw__hfv, 'index_col_typ': index_column_type})
    if db_type == 'snowflake':
        ootp__pio.update({'np': np, 'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'snowflake_read':
            _snowflake_read, 'info_to_array': info_to_array,
            'info_from_table': info_from_table, 'delete_table':
            delete_table, 'cpp_table_to_py_table': cpp_table_to_py_table,
            f'table_idx_{zndxr__bomie}': ftopi__fxca})
    else:
        ootp__pio.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(nlr__dod), bodo.RangeIndexType(None),
            tuple(dgc__ugf)), 'Table': Table,
            f'type_usecols_offsets_arr_{zndxr__bomie}': oqjqw__sjzp})
    rpvhy__qbrm = {}
    exec(qgyfz__ueguk, ootp__pio, rpvhy__qbrm)
    lsu__jgks = rpvhy__qbrm['sql_reader_py']
    xdlsk__rngsq = numba.njit(lsu__jgks)
    compiled_funcs.append(xdlsk__rngsq)
    return xdlsk__rngsq


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.int64, types.voidptr))
import llvmlite.binding as ll
from bodo.io import arrow_cpp
ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
