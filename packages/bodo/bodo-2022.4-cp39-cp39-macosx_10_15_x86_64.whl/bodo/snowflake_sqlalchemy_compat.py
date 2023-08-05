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
    bcpp__rxg = {}
    scqnj__npmp, xkpf__nhs = self._current_database_schema(connection, **kw)
    prl__fqrxv = self._denormalize_quote_join(scqnj__npmp, schema)
    try:
        gnw__kxkag = self._get_schema_primary_keys(connection, prl__fqrxv, **kw
            )
        zfkvi__pbfpu = connection.execute(text(
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
    except sa_exc.ProgrammingError as bajr__tdi:
        if bajr__tdi.orig.errno == 90030:
            return None
        raise
    for table_name, jfn__tfa, wzil__bzhex, vyvk__hieg, lgp__gnc, oqcp__okz, zrwc__mpvr, rxd__gdbzr, svkw__wktk, sqwt__nfsh in zfkvi__pbfpu:
        table_name = self.normalize_name(table_name)
        jfn__tfa = self.normalize_name(jfn__tfa)
        if table_name not in bcpp__rxg:
            bcpp__rxg[table_name] = list()
        if jfn__tfa.startswith('sys_clustering_column'):
            continue
        gtp__zrmba = self.ischema_names.get(wzil__bzhex, None)
        gfuv__iry = {}
        if gtp__zrmba is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(wzil__bzhex, jfn__tfa))
            gtp__zrmba = sqltypes.NULLTYPE
        elif issubclass(gtp__zrmba, sqltypes.FLOAT):
            gfuv__iry['precision'] = lgp__gnc
            gfuv__iry['decimal_return_scale'] = oqcp__okz
        elif issubclass(gtp__zrmba, sqltypes.Numeric):
            gfuv__iry['precision'] = lgp__gnc
            gfuv__iry['scale'] = oqcp__okz
        elif issubclass(gtp__zrmba, (sqltypes.String, sqltypes.BINARY)):
            gfuv__iry['length'] = vyvk__hieg
        ayh__fkr = gtp__zrmba if isinstance(gtp__zrmba, sqltypes.NullType
            ) else gtp__zrmba(**gfuv__iry)
        ycr__ase = gnw__kxkag.get(table_name)
        bcpp__rxg[table_name].append({'name': jfn__tfa, 'type': ayh__fkr,
            'nullable': zrwc__mpvr == 'YES', 'default': rxd__gdbzr,
            'autoincrement': svkw__wktk == 'YES', 'comment': sqwt__nfsh,
            'primary_key': jfn__tfa in gnw__kxkag[table_name][
            'constrained_columns'] if ycr__ase else False})
    return bcpp__rxg


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
    bcpp__rxg = []
    scqnj__npmp, xkpf__nhs = self._current_database_schema(connection, **kw)
    prl__fqrxv = self._denormalize_quote_join(scqnj__npmp, schema)
    gnw__kxkag = self._get_schema_primary_keys(connection, prl__fqrxv, **kw)
    zfkvi__pbfpu = connection.execute(text(
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
    for table_name, jfn__tfa, wzil__bzhex, vyvk__hieg, lgp__gnc, oqcp__okz, zrwc__mpvr, rxd__gdbzr, svkw__wktk, sqwt__nfsh in zfkvi__pbfpu:
        table_name = self.normalize_name(table_name)
        jfn__tfa = self.normalize_name(jfn__tfa)
        if jfn__tfa.startswith('sys_clustering_column'):
            continue
        gtp__zrmba = self.ischema_names.get(wzil__bzhex, None)
        gfuv__iry = {}
        if gtp__zrmba is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(wzil__bzhex, jfn__tfa))
            gtp__zrmba = sqltypes.NULLTYPE
        elif issubclass(gtp__zrmba, sqltypes.FLOAT):
            gfuv__iry['precision'] = lgp__gnc
            gfuv__iry['decimal_return_scale'] = oqcp__okz
        elif issubclass(gtp__zrmba, sqltypes.Numeric):
            gfuv__iry['precision'] = lgp__gnc
            gfuv__iry['scale'] = oqcp__okz
        elif issubclass(gtp__zrmba, (sqltypes.String, sqltypes.BINARY)):
            gfuv__iry['length'] = vyvk__hieg
        ayh__fkr = gtp__zrmba if isinstance(gtp__zrmba, sqltypes.NullType
            ) else gtp__zrmba(**gfuv__iry)
        ycr__ase = gnw__kxkag.get(table_name)
        bcpp__rxg.append({'name': jfn__tfa, 'type': ayh__fkr, 'nullable': 
            zrwc__mpvr == 'YES', 'default': rxd__gdbzr, 'autoincrement': 
            svkw__wktk == 'YES', 'comment': sqwt__nfsh if sqwt__nfsh != '' else
            None, 'primary_key': jfn__tfa in gnw__kxkag[table_name][
            'constrained_columns'] if ycr__ase else False})
    return bcpp__rxg


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
