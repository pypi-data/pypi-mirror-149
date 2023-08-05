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
    bxo__ywu = urlparse(conn_str)
    mba__watgq = {}
    if bxo__ywu.username:
        mba__watgq['user'] = bxo__ywu.username
    if bxo__ywu.password:
        mba__watgq['password'] = bxo__ywu.password
    if bxo__ywu.hostname:
        mba__watgq['account'] = bxo__ywu.hostname
    if bxo__ywu.port:
        mba__watgq['port'] = bxo__ywu.port
    if bxo__ywu.path:
        ncbmj__wtjmm = bxo__ywu.path
        if ncbmj__wtjmm.startswith('/'):
            ncbmj__wtjmm = ncbmj__wtjmm[1:]
        oekvj__xhvlx, schema = ncbmj__wtjmm.split('/')
        mba__watgq['database'] = oekvj__xhvlx
        if schema:
            mba__watgq['schema'] = schema
    if bxo__ywu.query:
        for kez__jlrb, ezslq__huuyo in parse_qsl(bxo__ywu.query):
            mba__watgq[kez__jlrb] = ezslq__huuyo
            if kez__jlrb == 'session_parameters':
                mba__watgq[kez__jlrb] = json.loads(ezslq__huuyo)
    mba__watgq['application'] = 'bodo'
    return mba__watgq


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for bthl__dzvk in batches:
            bthl__dzvk._bodo_num_rows = bthl__dzvk.rowcount
            self._bodo_total_rows += bthl__dzvk._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    oopx__vzt = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    uxc__qyqq = MPI.COMM_WORLD
    tor__kkd = tracing.Event('snowflake_connect', is_parallel=False)
    tacc__ggt = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**tacc__ggt)
    tor__kkd.finalize()
    if bodo.get_rank() == 0:
        dbdur__lxy = conn.cursor()
        qeqv__vvs = tracing.Event('get_schema', is_parallel=False)
        mkkzr__wjal = f'select * from ({query}) x LIMIT {100}'
        efw__jtpuu = dbdur__lxy.execute(mkkzr__wjal).fetch_arrow_all()
        if efw__jtpuu is None:
            byzlc__vytty = dbdur__lxy.describe(query)
            oxsxx__xwp = [pa.field(nzwkk__ukv.name, FIELD_TYPE_TO_PA_TYPE[
                nzwkk__ukv.type_code]) for nzwkk__ukv in byzlc__vytty]
            schema = pa.schema(oxsxx__xwp)
        else:
            schema = efw__jtpuu.schema
        qeqv__vvs.finalize()
        pnhg__leul = tracing.Event('execute_query', is_parallel=False)
        dbdur__lxy.execute(query)
        pnhg__leul.finalize()
        batches = dbdur__lxy.get_result_batches()
        uxc__qyqq.bcast((batches, schema))
    else:
        batches, schema = uxc__qyqq.bcast(None)
    yegq__jak = SnowflakeDataset(batches, schema, conn)
    oopx__vzt.finalize()
    return yegq__jak
