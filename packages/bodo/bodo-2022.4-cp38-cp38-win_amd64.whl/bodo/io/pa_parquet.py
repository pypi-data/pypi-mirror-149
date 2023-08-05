import asyncio
import os
import threading
from collections import defaultdict
from concurrent import futures
from urllib.parse import urlparse
import pyarrow.parquet as pq
from bodo.io.fs_io import get_s3_bucket_region_njit


def get_parquet_filesnames_from_deltalake(delta_lake_path):
    try:
        from deltalake import DeltaTable
    except Exception as ibkjk__gpbhu:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    nwzo__dvz = None
    kxwa__lhprk = delta_lake_path.rstrip('/')
    lgbk__pdez = 'AWS_DEFAULT_REGION' in os.environ
    jvjw__hdvv = os.environ.get('AWS_DEFAULT_REGION', '')
    mmod__cni = False
    if delta_lake_path.startswith('s3://'):
        bka__jis = get_s3_bucket_region_njit(delta_lake_path, parallel=False)
        if bka__jis != '':
            os.environ['AWS_DEFAULT_REGION'] = bka__jis
            mmod__cni = True
    sizza__ilhjn = DeltaTable(delta_lake_path)
    nwzo__dvz = sizza__ilhjn.files()
    nwzo__dvz = [(kxwa__lhprk + '/' + xkjiw__kisuw) for xkjiw__kisuw in
        sorted(nwzo__dvz)]
    if mmod__cni:
        if lgbk__pdez:
            os.environ['AWS_DEFAULT_REGION'] = jvjw__hdvv
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return nwzo__dvz


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    wpj__epjdu = None
    ors__ckbp = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        wpj__epjdu = manifest.common_metadata_path
        ors__ckbp = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        jrozd__wzi = urlparse(path_or_paths[0]).scheme
        for kxwa__lhprk in path_or_paths:
            if not jrozd__wzi and not fs.isfile(kxwa__lhprk):
                raise OSError(
                    f'Passed non-file path: {kxwa__lhprk}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(kxwa__lhprk,
                open_file_func=open_file_func)
            pieces.append(piece)
    return pieces, partitions, wpj__epjdu, ors__ckbp


pq._make_manifest = _make_manifest


def get_dataset_schema(dataset):
    if dataset.metadata is None and dataset.schema is None:
        if dataset.common_metadata is not None:
            dataset.schema = dataset.common_metadata.schema
        else:
            dataset.schema = dataset.pieces[0].get_metadata().schema
    elif dataset.schema is None:
        dataset.schema = dataset.metadata.schema
    zuhdh__ciuti = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for brn__injs in dataset.partitions.partition_names:
            if zuhdh__ciuti.get_field_index(brn__injs) != -1:
                ilibe__ysu = zuhdh__ciuti.get_field_index(brn__injs)
                zuhdh__ciuti = zuhdh__ciuti.remove(ilibe__ysu)
    return zuhdh__ciuti


class VisitLevelThread(threading.Thread):

    def __init__(self, manifest):
        threading.Thread.__init__(self)
        self.manifest = manifest
        self.exc = None

    def run(self):
        try:
            manifest = self.manifest
            manifest.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(manifest.loop)
            manifest.loop.run_until_complete(manifest._visit_level(0,
                manifest.dirpath, []))
        except Exception as ibkjk__gpbhu:
            self.exc = ibkjk__gpbhu
        finally:
            if hasattr(manifest, 'loop') and not manifest.loop.is_closed():
                manifest.loop.close()

    def join(self):
        super(VisitLevelThread, self).join()
        if self.exc:
            raise self.exc


class ParquetManifest:

    def __init__(self, dirpath, open_file_func=None, filesystem=None,
        pathsep='/', partition_scheme='hive', metadata_nthreads=1):
        filesystem, dirpath = pq._get_filesystem_and_path(filesystem, dirpath)
        self.filesystem = filesystem
        self.open_file_func = open_file_func
        self.pathsep = pathsep
        self.dirpath = pq._stringify_path(dirpath)
        self.partition_scheme = partition_scheme
        self.partitions = pq.ParquetPartitions()
        self.pieces = []
        self._metadata_nthreads = metadata_nthreads
        self._thread_pool = futures.ThreadPoolExecutor(max_workers=
            metadata_nthreads)
        self.common_metadata_path = None
        self.metadata_path = None
        self.delta_lake_filter = set()
        self.partition_vals = defaultdict(set)
        ogu__cugyq = VisitLevelThread(self)
        ogu__cugyq.start()
        ogu__cugyq.join()
        for ukj__ogj in self.partition_vals.keys():
            self.partition_vals[ukj__ogj] = sorted(self.partition_vals[
                ukj__ogj])
        for vqgq__diy in self.partitions.levels:
            vqgq__diy.keys = sorted(vqgq__diy.keys)
        for czm__sajd in self.pieces:
            if czm__sajd.partition_keys is not None:
                czm__sajd.partition_keys = [(vsxqa__xcfx, self.
                    partition_vals[vsxqa__xcfx].index(nbz__sbc)) for 
                    vsxqa__xcfx, nbz__sbc in czm__sajd.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, afum__jza, base_path, cvlam__nxgfr):
        fs = self.filesystem
        vspi__dqegn, erh__ghxmb, prjl__nxdvu = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if afum__jza == 0 and '_delta_log' in erh__ghxmb:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        mpoj__kkqm = []
        for kxwa__lhprk in prjl__nxdvu:
            if kxwa__lhprk == '':
                continue
            iqj__tnxie = self.pathsep.join((base_path, kxwa__lhprk))
            if kxwa__lhprk.endswith('_common_metadata'):
                self.common_metadata_path = iqj__tnxie
            elif kxwa__lhprk.endswith('_metadata'):
                self.metadata_path = iqj__tnxie
            elif self._should_silently_exclude(kxwa__lhprk):
                continue
            elif self.delta_lake_filter and iqj__tnxie not in self.delta_lake_filter:
                continue
            else:
                mpoj__kkqm.append(iqj__tnxie)
        txsj__frbyu = [self.pathsep.join((base_path, pasec__vzwk)) for
            pasec__vzwk in erh__ghxmb if not pq._is_private_directory(
            pasec__vzwk)]
        mpoj__kkqm.sort()
        txsj__frbyu.sort()
        if len(mpoj__kkqm) > 0 and len(txsj__frbyu) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(txsj__frbyu) > 0:
            await self._visit_directories(afum__jza, txsj__frbyu, cvlam__nxgfr)
        else:
            self._push_pieces(mpoj__kkqm, cvlam__nxgfr)

    async def _visit_directories(self, afum__jza, erh__ghxmb, cvlam__nxgfr):
        vbz__ahdv = []
        for kxwa__lhprk in erh__ghxmb:
            pbk__uixu, rxzyz__eog = pq._path_split(kxwa__lhprk, self.pathsep)
            vsxqa__xcfx, iitp__gprwl = pq._parse_hive_partition(rxzyz__eog)
            rjowh__ecbz = self.partitions.get_index(afum__jza, vsxqa__xcfx,
                iitp__gprwl)
            self.partition_vals[vsxqa__xcfx].add(iitp__gprwl)
            kkc__cvkhb = cvlam__nxgfr + [(vsxqa__xcfx, iitp__gprwl)]
            vbz__ahdv.append(self._visit_level(afum__jza + 1, kxwa__lhprk,
                kkc__cvkhb))
        await asyncio.wait(vbz__ahdv)


ParquetManifest._should_silently_exclude = (pq.ParquetManifest.
    _should_silently_exclude)
ParquetManifest._parse_partition = pq.ParquetManifest._parse_partition
ParquetManifest._push_pieces = pq.ParquetManifest._push_pieces
pq.ParquetManifest = ParquetManifest


def pieces(self):
    return self._pieces


pq.ParquetDataset.pieces = property(pieces)


def partitions(self):
    return self._partitions


pq.ParquetDataset.partitions = property(partitions)
