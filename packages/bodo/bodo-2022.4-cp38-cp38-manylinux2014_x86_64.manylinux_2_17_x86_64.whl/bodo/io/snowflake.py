from urllib.parse import parse_qsl, urlparse
import pyarrow as pa
import snowflake.connector
import bodo
from bodo.utils import tracing
FIELD_TYPE_TO_PA_TYPE = [pa.int64(), pa.float64(), pa.string(), pa.date32(),
    pa.timestamp('ns'), pa.string(), pa.timestamp('ns'), pa.timestamp('ns'),
    pa.timestamp('ns'), pa.string(), pa.string(), pa.binary(), pa.time64(
    'ns'), pa.bool_()]


def get_connection_params(conn_str):
    import json
    ukuwv__eylh = urlparse(conn_str)
    zwsld__gymj = {}
    if ukuwv__eylh.username:
        zwsld__gymj['user'] = ukuwv__eylh.username
    if ukuwv__eylh.password:
        zwsld__gymj['password'] = ukuwv__eylh.password
    if ukuwv__eylh.hostname:
        zwsld__gymj['account'] = ukuwv__eylh.hostname
    if ukuwv__eylh.port:
        zwsld__gymj['port'] = ukuwv__eylh.port
    if ukuwv__eylh.path:
        xevn__nzo = ukuwv__eylh.path
        if xevn__nzo.startswith('/'):
            xevn__nzo = xevn__nzo[1:]
        itgm__tuq, schema = xevn__nzo.split('/')
        zwsld__gymj['database'] = itgm__tuq
        if schema:
            zwsld__gymj['schema'] = schema
    if ukuwv__eylh.query:
        for rpzo__guszy, jak__uas in parse_qsl(ukuwv__eylh.query):
            zwsld__gymj[rpzo__guszy] = jak__uas
            if rpzo__guszy == 'session_parameters':
                zwsld__gymj[rpzo__guszy] = json.loads(jak__uas)
    zwsld__gymj['application'] = 'bodo'
    return zwsld__gymj


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for yjjuj__cxbpl in batches:
            yjjuj__cxbpl._bodo_num_rows = yjjuj__cxbpl.rowcount
            self._bodo_total_rows += yjjuj__cxbpl._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    jztpy__qnfp = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    conq__nabu = MPI.COMM_WORLD
    pabtq__hvww = tracing.Event('snowflake_connect', is_parallel=False)
    yidk__twkca = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**yidk__twkca)
    pabtq__hvww.finalize()
    if bodo.get_rank() == 0:
        rbulh__evp = conn.cursor()
        safx__gphkm = tracing.Event('get_schema', is_parallel=False)
        whyu__mlhh = f'select * from ({query}) x LIMIT {100}'
        pwddq__sew = rbulh__evp.execute(whyu__mlhh).fetch_arrow_all()
        if pwddq__sew is None:
            egid__dkt = rbulh__evp.describe(query)
            mscq__ypf = [pa.field(yjtvy__wqfay.name, FIELD_TYPE_TO_PA_TYPE[
                yjtvy__wqfay.type_code]) for yjtvy__wqfay in egid__dkt]
            schema = pa.schema(mscq__ypf)
        else:
            schema = pwddq__sew.schema
        safx__gphkm.finalize()
        fxyrs__auja = tracing.Event('execute_query', is_parallel=False)
        rbulh__evp.execute(query)
        fxyrs__auja.finalize()
        batches = rbulh__evp.get_result_batches()
        conq__nabu.bcast((batches, schema))
    else:
        batches, schema = conq__nabu.bcast(None)
    wol__salzy = SnowflakeDataset(batches, schema, conn)
    jztpy__qnfp.finalize()
    return wol__salzy
