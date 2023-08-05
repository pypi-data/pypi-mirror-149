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
    msqx__tehzs = sql_node.out_vars[0].name
    ieu__bvq = sql_node.out_vars[1].name
    if msqx__tehzs not in lives and ieu__bvq not in lives:
        return None
    elif msqx__tehzs not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif ieu__bvq not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        klqi__nvtr = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        vxpoq__zxgqf = []
        otbmc__ofx = []
        for pcy__lzgs in sql_node.type_usecol_offset:
            ylnm__wzcl = sql_node.df_colnames[pcy__lzgs]
            vxpoq__zxgqf.append(ylnm__wzcl)
            if isinstance(sql_node.out_types[pcy__lzgs], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                otbmc__ofx.append(ylnm__wzcl)
        if sql_node.index_column_name:
            vxpoq__zxgqf.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                otbmc__ofx.append(sql_node.index_column_name)
        bbswp__bcgl = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', klqi__nvtr,
            bbswp__bcgl, vxpoq__zxgqf)
        if otbmc__ofx:
            likrl__veoay = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                likrl__veoay, bbswp__bcgl, otbmc__ofx)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        zgyv__rne = set(sql_node.unsupported_columns)
        dqhx__xexxf = set(sql_node.type_usecol_offset)
        tgpt__lgyjj = dqhx__xexxf & zgyv__rne
        if tgpt__lgyjj:
            kdcbq__qjb = sorted(tgpt__lgyjj)
            ogw__knu = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            erj__hwgvu = 0
            for xcpor__bdn in kdcbq__qjb:
                while sql_node.unsupported_columns[erj__hwgvu] != xcpor__bdn:
                    erj__hwgvu += 1
                ogw__knu.append(
                    f"Column '{sql_node.original_df_colnames[xcpor__bdn]}' with unsupported arrow type {sql_node.unsupported_arrow_types[erj__hwgvu]}"
                    )
                erj__hwgvu += 1
            ucv__cqz = '\n'.join(ogw__knu)
            raise BodoError(ucv__cqz, loc=sql_node.loc)
    cycg__ocoux, xnke__qgan = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    nnxnn__bwkr = ', '.join(cycg__ocoux.values())
    ishz__ierq = f'def sql_impl(sql_request, conn, {nnxnn__bwkr}):\n'
    if sql_node.filters:
        egx__fjki = []
        for otqna__cpvw in sql_node.filters:
            qcxpw__bgsm = [' '.join(['(', bmyn__urqvt[0], bmyn__urqvt[1], 
                '{' + cycg__ocoux[bmyn__urqvt[2].name] + '}' if isinstance(
                bmyn__urqvt[2], ir.Var) else bmyn__urqvt[2], ')']) for
                bmyn__urqvt in otqna__cpvw]
            egx__fjki.append(' ( ' + ' AND '.join(qcxpw__bgsm) + ' ) ')
        pgm__rqylw = ' WHERE ' + ' OR '.join(egx__fjki)
        for pcy__lzgs, lhp__gdth in enumerate(cycg__ocoux.values()):
            ishz__ierq += f'    {lhp__gdth} = get_sql_literal({lhp__gdth})\n'
        ishz__ierq += f'    sql_request = f"{{sql_request}} {pgm__rqylw}"\n'
    ishz__ierq += (
        '    (table_var, index_var) = _sql_reader_py(sql_request, conn)\n')
    zgqe__fadwo = {}
    exec(ishz__ierq, {}, zgqe__fadwo)
    dnv__tvar = zgqe__fadwo['sql_impl']
    enkc__lqrq = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, sql_node.is_select_query)
    bdi__zsbh = compile_to_numba_ir(dnv__tvar, {'_sql_reader_py':
        enkc__lqrq, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type) + tuple(
        typemap[pkd__fka.name] for pkd__fka in xnke__qgan), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query:
        oyop__zurxl = [sql_node.df_colnames[pcy__lzgs] for pcy__lzgs in
            sql_node.type_usecol_offset]
        if sql_node.index_column_name:
            oyop__zurxl.append(sql_node.index_column_name)
        gvdgz__ebet = escape_column_names(oyop__zurxl, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            xwohg__czlf = ('SELECT ' + gvdgz__ebet + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            xwohg__czlf = ('SELECT ' + gvdgz__ebet + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        xwohg__czlf = sql_node.sql_request
    replace_arg_nodes(bdi__zsbh, [ir.Const(xwohg__czlf, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc)] + xnke__qgan)
    zeef__fel = bdi__zsbh.body[:-3]
    zeef__fel[-2].target = sql_node.out_vars[0]
    zeef__fel[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        zeef__fel.pop(-1)
    elif not sql_node.type_usecol_offset:
        zeef__fel.pop(-2)
    return zeef__fel


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        oyop__zurxl = [(sqonj__imfs.upper() if sqonj__imfs in
            converted_colnames else sqonj__imfs) for sqonj__imfs in col_names]
        gvdgz__ebet = ', '.join([f'"{sqonj__imfs}"' for sqonj__imfs in
            oyop__zurxl])
    elif db_type == 'mysql' or db_type == 'mysql+pymysql':
        gvdgz__ebet = ', '.join([f'`{sqonj__imfs}`' for sqonj__imfs in
            col_names])
    else:
        gvdgz__ebet = ', '.join([f'"{sqonj__imfs}"' for sqonj__imfs in
            col_names])
    return gvdgz__ebet


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    tvqlb__jllv = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tvqlb__jllv,
        'Filter pushdown')
    if tvqlb__jllv == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(tvqlb__jllv, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif tvqlb__jllv == bodo.pd_timestamp_type:

        def impl(filter_value):
            lhzs__bukb = filter_value.nanosecond
            pkyp__xbtgk = ''
            if lhzs__bukb < 10:
                pkyp__xbtgk = '00'
            elif lhzs__bukb < 100:
                pkyp__xbtgk = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{pkyp__xbtgk}{lhzs__bukb}'"
                )
        return impl
    elif tvqlb__jllv == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {tvqlb__jllv} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    jia__puhl = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    tvqlb__jllv = types.unliteral(filter_value)
    if isinstance(tvqlb__jllv, types.List) and (isinstance(tvqlb__jllv.
        dtype, scalar_isinstance) or tvqlb__jllv.dtype in jia__puhl):

        def impl(filter_value):
            wgu__zuy = ', '.join([_get_snowflake_sql_literal_scalar(
                sqonj__imfs) for sqonj__imfs in filter_value])
            return f'({wgu__zuy})'
        return impl
    elif isinstance(tvqlb__jllv, scalar_isinstance
        ) or tvqlb__jllv in jia__puhl:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {tvqlb__jllv} used in filter pushdown.'
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
    except ImportError as ijzrm__vcdo:
        cqkq__jhhcl = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(cqkq__jhhcl)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as ijzrm__vcdo:
        cqkq__jhhcl = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(cqkq__jhhcl)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as ijzrm__vcdo:
        cqkq__jhhcl = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(cqkq__jhhcl)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as ijzrm__vcdo:
        cqkq__jhhcl = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(cqkq__jhhcl)


def req_limit(sql_request):
    import re
    lgp__kmm = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    wyc__wrzsy = lgp__kmm.search(sql_request)
    if wyc__wrzsy:
        return int(wyc__wrzsy.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, is_select_query):
    fhb__kzdxt = next_label()
    oyop__zurxl = [col_names[pcy__lzgs] for pcy__lzgs in type_usecol_offset]
    ffj__otrrm = [col_typs[pcy__lzgs] for pcy__lzgs in type_usecol_offset]
    if index_column_name:
        oyop__zurxl.append(index_column_name)
        ffj__otrrm.append(index_column_type)
    riwpo__vxas = None
    vyjqh__kvc = None
    sxd__duvi = types.none
    if type_usecol_offset:
        sxd__duvi = TableType(tuple(col_typs))
    ishz__ierq = 'def sql_reader_py(sql_request, conn):\n'
    if db_type == 'snowflake':
        ishz__ierq += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")

        def is_nullable(typ):
            return bodo.utils.utils.is_array_typ(typ, False
                ) and not isinstance(typ, types.Array) and not isinstance(typ,
                bodo.DatetimeArrayType)
        uvhuy__xxpsc = [int(is_nullable(col_typs[pcy__lzgs])) for pcy__lzgs in
            type_usecol_offset]
        if index_column_name:
            uvhuy__xxpsc.append(int(is_nullable(index_column_type)))
        ishz__ierq += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(uvhuy__xxpsc)}, np.array({uvhuy__xxpsc}, dtype=np.int32).ctypes)
"""
        ishz__ierq += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            ishz__ierq += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            ishz__ierq += '  index_var = None\n'
        if type_usecol_offset:
            erj__hwgvu = []
            kww__fkl = 0
            for pcy__lzgs in range(len(col_names)):
                if kww__fkl < len(type_usecol_offset
                    ) and pcy__lzgs == type_usecol_offset[kww__fkl]:
                    erj__hwgvu.append(kww__fkl)
                    kww__fkl += 1
                else:
                    erj__hwgvu.append(-1)
            riwpo__vxas = np.array(erj__hwgvu, dtype=np.int64)
            ishz__ierq += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{fhb__kzdxt}, py_table_type_{fhb__kzdxt})
"""
        else:
            ishz__ierq += '  table_var = None\n'
        ishz__ierq += '  delete_table(out_table)\n'
        ishz__ierq += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            ishz__ierq += f"""  type_usecols_offsets_arr_{fhb__kzdxt}_2 = type_usecols_offsets_arr_{fhb__kzdxt}
"""
            vyjqh__kvc = np.array(type_usecol_offset, dtype=np.int64)
        ishz__ierq += '  df_typeref_2 = df_typeref\n'
        ishz__ierq += '  sqlalchemy_check()\n'
        if db_type == 'mysql' or db_type == 'mysql+pymysql':
            ishz__ierq += '  pymysql_check()\n'
        elif db_type == 'oracle':
            ishz__ierq += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            ishz__ierq += '  psycopg2_check()\n'
        if parallel and is_select_query:
            ishz__ierq += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                ishz__ierq += f'  nb_row = {limit}\n'
            else:
                ishz__ierq += '  with objmode(nb_row="int64"):\n'
                ishz__ierq += f'     if rank == {MPI_ROOT}:\n'
                ishz__ierq += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                ishz__ierq += '         frame = pd.read_sql(sql_cons, conn)\n'
                ishz__ierq += '         nb_row = frame.iat[0,0]\n'
                ishz__ierq += '     else:\n'
                ishz__ierq += '         nb_row = 0\n'
                ishz__ierq += '  nb_row = bcast_scalar(nb_row)\n'
            ishz__ierq += f"""  with objmode(table_var=py_table_type_{fhb__kzdxt}, index_var=index_col_typ):
"""
            ishz__ierq += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                ishz__ierq += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                ishz__ierq += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            ishz__ierq += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            ishz__ierq += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            ishz__ierq += f"""  with objmode(table_var=py_table_type_{fhb__kzdxt}, index_var=index_col_typ):
"""
            ishz__ierq += '    df_ret = pd.read_sql(sql_request, conn)\n'
            ishz__ierq += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            ishz__ierq += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            ishz__ierq += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            ishz__ierq += '    index_var = None\n'
        if type_usecol_offset:
            ishz__ierq += f'    arrs = []\n'
            ishz__ierq += f'    for i in range(df_ret.shape[1]):\n'
            ishz__ierq += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            ishz__ierq += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{fhb__kzdxt}_2, {len(col_names)})
"""
        else:
            ishz__ierq += '    table_var = None\n'
    ishz__ierq += '  return (table_var, index_var)\n'
    inhk__wujv = globals()
    inhk__wujv.update({'bodo': bodo, f'py_table_type_{fhb__kzdxt}':
        sxd__duvi, 'index_col_typ': index_column_type})
    if db_type == 'snowflake':
        inhk__wujv.update({'np': np, 'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'snowflake_read':
            _snowflake_read, 'info_to_array': info_to_array,
            'info_from_table': info_from_table, 'delete_table':
            delete_table, 'cpp_table_to_py_table': cpp_table_to_py_table,
            f'table_idx_{fhb__kzdxt}': riwpo__vxas})
    else:
        inhk__wujv.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(ffj__otrrm), bodo.RangeIndexType(None),
            tuple(oyop__zurxl)), 'Table': Table,
            f'type_usecols_offsets_arr_{fhb__kzdxt}': vyjqh__kvc})
    zgqe__fadwo = {}
    exec(ishz__ierq, inhk__wujv, zgqe__fadwo)
    enkc__lqrq = zgqe__fadwo['sql_reader_py']
    ynzsc__fwe = numba.njit(enkc__lqrq)
    compiled_funcs.append(ynzsc__fwe)
    return ynzsc__fwe


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.int64, types.voidptr))
import llvmlite.binding as ll
from bodo.io import arrow_cpp
ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
