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
    yhsc__nosep = {}
    jux__sdmpu, njus__ozyf = self._current_database_schema(connection, **kw)
    zhxmo__bzj = self._denormalize_quote_join(jux__sdmpu, schema)
    try:
        qlqjd__mbdf = self._get_schema_primary_keys(connection, zhxmo__bzj,
            **kw)
        eyv__lltp = connection.execute(text(
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
    except sa_exc.ProgrammingError as vpse__attr:
        if vpse__attr.orig.errno == 90030:
            return None
        raise
    for table_name, btwd__dpd, tvj__zari, thkiq__okupt, ngfb__bgw, fqpl__swlni, awymb__sbiss, six__owpee, wngf__qdepy, tpv__nbyp in eyv__lltp:
        table_name = self.normalize_name(table_name)
        btwd__dpd = self.normalize_name(btwd__dpd)
        if table_name not in yhsc__nosep:
            yhsc__nosep[table_name] = list()
        if btwd__dpd.startswith('sys_clustering_column'):
            continue
        kjxn__nlwsh = self.ischema_names.get(tvj__zari, None)
        cie__npuas = {}
        if kjxn__nlwsh is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(tvj__zari, btwd__dpd))
            kjxn__nlwsh = sqltypes.NULLTYPE
        elif issubclass(kjxn__nlwsh, sqltypes.FLOAT):
            cie__npuas['precision'] = ngfb__bgw
            cie__npuas['decimal_return_scale'] = fqpl__swlni
        elif issubclass(kjxn__nlwsh, sqltypes.Numeric):
            cie__npuas['precision'] = ngfb__bgw
            cie__npuas['scale'] = fqpl__swlni
        elif issubclass(kjxn__nlwsh, (sqltypes.String, sqltypes.BINARY)):
            cie__npuas['length'] = thkiq__okupt
        ztper__ezpts = kjxn__nlwsh if isinstance(kjxn__nlwsh, sqltypes.NullType
            ) else kjxn__nlwsh(**cie__npuas)
        akzga__ubszd = qlqjd__mbdf.get(table_name)
        yhsc__nosep[table_name].append({'name': btwd__dpd, 'type':
            ztper__ezpts, 'nullable': awymb__sbiss == 'YES', 'default':
            six__owpee, 'autoincrement': wngf__qdepy == 'YES', 'comment':
            tpv__nbyp, 'primary_key': btwd__dpd in qlqjd__mbdf[table_name][
            'constrained_columns'] if akzga__ubszd else False})
    return yhsc__nosep


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
    yhsc__nosep = []
    jux__sdmpu, njus__ozyf = self._current_database_schema(connection, **kw)
    zhxmo__bzj = self._denormalize_quote_join(jux__sdmpu, schema)
    qlqjd__mbdf = self._get_schema_primary_keys(connection, zhxmo__bzj, **kw)
    eyv__lltp = connection.execute(text(
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
    for table_name, btwd__dpd, tvj__zari, thkiq__okupt, ngfb__bgw, fqpl__swlni, awymb__sbiss, six__owpee, wngf__qdepy, tpv__nbyp in eyv__lltp:
        table_name = self.normalize_name(table_name)
        btwd__dpd = self.normalize_name(btwd__dpd)
        if btwd__dpd.startswith('sys_clustering_column'):
            continue
        kjxn__nlwsh = self.ischema_names.get(tvj__zari, None)
        cie__npuas = {}
        if kjxn__nlwsh is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(tvj__zari, btwd__dpd))
            kjxn__nlwsh = sqltypes.NULLTYPE
        elif issubclass(kjxn__nlwsh, sqltypes.FLOAT):
            cie__npuas['precision'] = ngfb__bgw
            cie__npuas['decimal_return_scale'] = fqpl__swlni
        elif issubclass(kjxn__nlwsh, sqltypes.Numeric):
            cie__npuas['precision'] = ngfb__bgw
            cie__npuas['scale'] = fqpl__swlni
        elif issubclass(kjxn__nlwsh, (sqltypes.String, sqltypes.BINARY)):
            cie__npuas['length'] = thkiq__okupt
        ztper__ezpts = kjxn__nlwsh if isinstance(kjxn__nlwsh, sqltypes.NullType
            ) else kjxn__nlwsh(**cie__npuas)
        akzga__ubszd = qlqjd__mbdf.get(table_name)
        yhsc__nosep.append({'name': btwd__dpd, 'type': ztper__ezpts,
            'nullable': awymb__sbiss == 'YES', 'default': six__owpee,
            'autoincrement': wngf__qdepy == 'YES', 'comment': tpv__nbyp if 
            tpv__nbyp != '' else None, 'primary_key': btwd__dpd in
            qlqjd__mbdf[table_name]['constrained_columns'] if akzga__ubszd else
            False})
    return yhsc__nosep


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
