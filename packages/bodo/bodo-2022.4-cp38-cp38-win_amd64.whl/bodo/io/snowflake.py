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
    szwj__jiw = urlparse(conn_str)
    vdzu__okzd = {}
    if szwj__jiw.username:
        vdzu__okzd['user'] = szwj__jiw.username
    if szwj__jiw.password:
        vdzu__okzd['password'] = szwj__jiw.password
    if szwj__jiw.hostname:
        vdzu__okzd['account'] = szwj__jiw.hostname
    if szwj__jiw.port:
        vdzu__okzd['port'] = szwj__jiw.port
    if szwj__jiw.path:
        byp__qxg = szwj__jiw.path
        if byp__qxg.startswith('/'):
            byp__qxg = byp__qxg[1:]
        mqvfg__ojgbs, schema = byp__qxg.split('/')
        vdzu__okzd['database'] = mqvfg__ojgbs
        if schema:
            vdzu__okzd['schema'] = schema
    if szwj__jiw.query:
        for mdn__dlzjx, mng__jmy in parse_qsl(szwj__jiw.query):
            vdzu__okzd[mdn__dlzjx] = mng__jmy
            if mdn__dlzjx == 'session_parameters':
                vdzu__okzd[mdn__dlzjx] = json.loads(mng__jmy)
    vdzu__okzd['application'] = 'bodo'
    return vdzu__okzd


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for fibq__eyyo in batches:
            fibq__eyyo._bodo_num_rows = fibq__eyyo.rowcount
            self._bodo_total_rows += fibq__eyyo._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    zujs__vlwly = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    vlm__zfdru = MPI.COMM_WORLD
    iqow__kpm = tracing.Event('snowflake_connect', is_parallel=False)
    ovw__vjau = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**ovw__vjau)
    iqow__kpm.finalize()
    if bodo.get_rank() == 0:
        ipat__jyz = conn.cursor()
        kqpwt__gnm = tracing.Event('get_schema', is_parallel=False)
        fjyhp__etdm = f'select * from ({query}) x LIMIT {100}'
        hlqzc__mkzd = ipat__jyz.execute(fjyhp__etdm).fetch_arrow_all()
        if hlqzc__mkzd is None:
            ommen__kfmb = ipat__jyz.describe(query)
            jbfbx__sswi = [pa.field(bsget__mgfuu.name,
                FIELD_TYPE_TO_PA_TYPE[bsget__mgfuu.type_code]) for
                bsget__mgfuu in ommen__kfmb]
            schema = pa.schema(jbfbx__sswi)
        else:
            schema = hlqzc__mkzd.schema
        kqpwt__gnm.finalize()
        zciv__vqj = tracing.Event('execute_query', is_parallel=False)
        ipat__jyz.execute(query)
        zciv__vqj.finalize()
        batches = ipat__jyz.get_result_batches()
        vlm__zfdru.bcast((batches, schema))
    else:
        batches, schema = vlm__zfdru.bcast(None)
    fjz__mjgu = SnowflakeDataset(batches, schema, conn)
    zujs__vlwly.finalize()
    return fjz__mjgu
