import hashlib
import inspect
import warnings
import snowflake.sqlalchemy
import sqlalchemy.types as sqltypes
from sqlalchemy import exc as sa_exc
from sqlalchemy import util as sa_util
from sqlalchemy.sql import text
_check_snowflake_sqlalchemy_change = True


def _get_schema_columns(self, connection, schema, **kw):
    gbfr__jsck = {}
    epgbl__tgiob, ptpf__hrtf = self._current_database_schema(connection, **kw)
    xgvmf__zjbei = self._denormalize_quote_join(epgbl__tgiob, schema)
    try:
        puae__lpn = self._get_schema_primary_keys(connection, xgvmf__zjbei,
            **kw)
        ykoa__vjbcx = connection.execute(text(
            """
        SELECT /* sqlalchemy:_get_schema_columns */
                ic.table_name,
                ic.column_name,
                ic.data_type,
                ic.character_maximum_length,
                ic.numeric_precision,
                ic.numeric_scale,
                ic.is_nullable,
                ic.column_default,
                ic.is_identity,
                ic.comment
            FROM information_schema.columns ic
            WHERE ic.table_schema=:table_schema
            ORDER BY ic.ordinal_position"""
            ), {'table_schema': self.denormalize_name(schema)})
    except sa_exc.ProgrammingError as svc__cvg:
        if svc__cvg.orig.errno == 90030:
            return None
        raise
    for table_name, msaqe__yzab, oqzvs__gjw, pxft__ndauw, iae__gmv, fhbmv__ywgd, jxmrw__lpu, vxfo__deo, hio__mggy, xas__ruu in ykoa__vjbcx:
        table_name = self.normalize_name(table_name)
        msaqe__yzab = self.normalize_name(msaqe__yzab)
        if table_name not in gbfr__jsck:
            gbfr__jsck[table_name] = list()
        if msaqe__yzab.startswith('sys_clustering_column'):
            continue
        grtw__rakm = self.ischema_names.get(oqzvs__gjw, None)
        hqetl__nykjb = {}
        if grtw__rakm is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(oqzvs__gjw, msaqe__yzab))
            grtw__rakm = sqltypes.NULLTYPE
        elif issubclass(grtw__rakm, sqltypes.FLOAT):
            hqetl__nykjb['precision'] = iae__gmv
            hqetl__nykjb['decimal_return_scale'] = fhbmv__ywgd
        elif issubclass(grtw__rakm, sqltypes.Numeric):
            hqetl__nykjb['precision'] = iae__gmv
            hqetl__nykjb['scale'] = fhbmv__ywgd
        elif issubclass(grtw__rakm, (sqltypes.String, sqltypes.BINARY)):
            hqetl__nykjb['length'] = pxft__ndauw
        tiso__ppq = grtw__rakm if isinstance(grtw__rakm, sqltypes.NullType
            ) else grtw__rakm(**hqetl__nykjb)
        isyst__pkx = puae__lpn.get(table_name)
        gbfr__jsck[table_name].append({'name': msaqe__yzab, 'type':
            tiso__ppq, 'nullable': jxmrw__lpu == 'YES', 'default':
            vxfo__deo, 'autoincrement': hio__mggy == 'YES', 'comment':
            xas__ruu, 'primary_key': msaqe__yzab in puae__lpn[table_name][
            'constrained_columns'] if isyst__pkx else False})
    return gbfr__jsck


if _check_snowflake_sqlalchemy_change:
    lines = inspect.getsource(snowflake.sqlalchemy.snowdialect.
        SnowflakeDialect._get_schema_columns)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdf39af1ac165319d3b6074e8cf9296a090a21f0e2c05b644ff8ec0e56e2d769':
        warnings.warn(
            'snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_schema_columns has changed'
            )
snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_schema_columns = (
    _get_schema_columns)


def _get_table_columns(self, connection, table_name, schema=None, **kw):
    gbfr__jsck = []
    epgbl__tgiob, ptpf__hrtf = self._current_database_schema(connection, **kw)
    xgvmf__zjbei = self._denormalize_quote_join(epgbl__tgiob, schema)
    puae__lpn = self._get_schema_primary_keys(connection, xgvmf__zjbei, **kw)
    ykoa__vjbcx = connection.execute(text(
        """
    SELECT /* sqlalchemy:get_table_columns */
            ic.table_name,
            ic.column_name,
            ic.data_type,
            ic.character_maximum_length,
            ic.numeric_precision,
            ic.numeric_scale,
            ic.is_nullable,
            ic.column_default,
            ic.is_identity,
            ic.comment
        FROM information_schema.columns ic
        WHERE ic.table_schema=:table_schema
        AND ic.table_name=:table_name
        ORDER BY ic.ordinal_position"""
        ), {'table_schema': self.denormalize_name(schema), 'table_name':
        self.denormalize_name(table_name)})
    for table_name, msaqe__yzab, oqzvs__gjw, pxft__ndauw, iae__gmv, fhbmv__ywgd, jxmrw__lpu, vxfo__deo, hio__mggy, xas__ruu in ykoa__vjbcx:
        table_name = self.normalize_name(table_name)
        msaqe__yzab = self.normalize_name(msaqe__yzab)
        if msaqe__yzab.startswith('sys_clustering_column'):
            continue
        grtw__rakm = self.ischema_names.get(oqzvs__gjw, None)
        hqetl__nykjb = {}
        if grtw__rakm is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(oqzvs__gjw, msaqe__yzab))
            grtw__rakm = sqltypes.NULLTYPE
        elif issubclass(grtw__rakm, sqltypes.FLOAT):
            hqetl__nykjb['precision'] = iae__gmv
            hqetl__nykjb['decimal_return_scale'] = fhbmv__ywgd
        elif issubclass(grtw__rakm, sqltypes.Numeric):
            hqetl__nykjb['precision'] = iae__gmv
            hqetl__nykjb['scale'] = fhbmv__ywgd
        elif issubclass(grtw__rakm, (sqltypes.String, sqltypes.BINARY)):
            hqetl__nykjb['length'] = pxft__ndauw
        tiso__ppq = grtw__rakm if isinstance(grtw__rakm, sqltypes.NullType
            ) else grtw__rakm(**hqetl__nykjb)
        isyst__pkx = puae__lpn.get(table_name)
        gbfr__jsck.append({'name': msaqe__yzab, 'type': tiso__ppq,
            'nullable': jxmrw__lpu == 'YES', 'default': vxfo__deo,
            'autoincrement': hio__mggy == 'YES', 'comment': xas__ruu if 
            xas__ruu != '' else None, 'primary_key': msaqe__yzab in
            puae__lpn[table_name]['constrained_columns'] if isyst__pkx else
            False})
    return gbfr__jsck


if _check_snowflake_sqlalchemy_change:
    lines = inspect.getsource(snowflake.sqlalchemy.snowdialect.
        SnowflakeDialect._get_table_columns)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9ecc8a2425c655836ade4008b1b98a8fd1819f3be43ba77b0fbbfc1f8740e2be':
        warnings.warn(
            'snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_table_columns has changed'
            )
snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_table_columns = (
    _get_table_columns)
