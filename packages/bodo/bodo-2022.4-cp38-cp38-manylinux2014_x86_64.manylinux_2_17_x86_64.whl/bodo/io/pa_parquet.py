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
    except Exception as gsf__yoy:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    qxd__ohp = None
    vpbrq__aow = delta_lake_path.rstrip('/')
    psd__ism = 'AWS_DEFAULT_REGION' in os.environ
    vpwu__xeerb = os.environ.get('AWS_DEFAULT_REGION', '')
    boce__uplm = False
    if delta_lake_path.startswith('s3://'):
        bxkp__sfnl = get_s3_bucket_region_njit(delta_lake_path, parallel=False)
        if bxkp__sfnl != '':
            os.environ['AWS_DEFAULT_REGION'] = bxkp__sfnl
            boce__uplm = True
    iju__owj = DeltaTable(delta_lake_path)
    qxd__ohp = iju__owj.files()
    qxd__ohp = [(vpbrq__aow + '/' + oingi__qch) for oingi__qch in sorted(
        qxd__ohp)]
    if boce__uplm:
        if psd__ism:
            os.environ['AWS_DEFAULT_REGION'] = vpwu__xeerb
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return qxd__ohp


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    jwpaz__kfd = None
    cfbbx__srvq = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        jwpaz__kfd = manifest.common_metadata_path
        cfbbx__srvq = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        baf__ecgec = urlparse(path_or_paths[0]).scheme
        for vpbrq__aow in path_or_paths:
            if not baf__ecgec and not fs.isfile(vpbrq__aow):
                raise OSError(
                    f'Passed non-file path: {vpbrq__aow}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(vpbrq__aow,
                open_file_func=open_file_func)
            pieces.append(piece)
    return pieces, partitions, jwpaz__kfd, cfbbx__srvq


pq._make_manifest = _make_manifest


def get_dataset_schema(dataset):
    if dataset.metadata is None and dataset.schema is None:
        if dataset.common_metadata is not None:
            dataset.schema = dataset.common_metadata.schema
        else:
            dataset.schema = dataset.pieces[0].get_metadata().schema
    elif dataset.schema is None:
        dataset.schema = dataset.metadata.schema
    ysswn__mqx = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for zttmg__kfeeg in dataset.partitions.partition_names:
            if ysswn__mqx.get_field_index(zttmg__kfeeg) != -1:
                fwf__wvlvk = ysswn__mqx.get_field_index(zttmg__kfeeg)
                ysswn__mqx = ysswn__mqx.remove(fwf__wvlvk)
    return ysswn__mqx


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
        except Exception as gsf__yoy:
            self.exc = gsf__yoy
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
        gppyi__iss = VisitLevelThread(self)
        gppyi__iss.start()
        gppyi__iss.join()
        for gbovq__tycbk in self.partition_vals.keys():
            self.partition_vals[gbovq__tycbk] = sorted(self.partition_vals[
                gbovq__tycbk])
        for jei__fsp in self.partitions.levels:
            jei__fsp.keys = sorted(jei__fsp.keys)
        for gcmw__utjzs in self.pieces:
            if gcmw__utjzs.partition_keys is not None:
                gcmw__utjzs.partition_keys = [(vgw__ssxqf, self.
                    partition_vals[vgw__ssxqf].index(ith__fbyuj)) for 
                    vgw__ssxqf, ith__fbyuj in gcmw__utjzs.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, fjbtv__jjgxw, base_path, awb__jlee):
        fs = self.filesystem
        qei__nsp, cndyb__rpcxz, rjv__aam = await self.loop.run_in_executor(self
            ._thread_pool, lambda fs, base_bath: next(fs.walk(base_path)),
            fs, base_path)
        if fjbtv__jjgxw == 0 and '_delta_log' in cndyb__rpcxz:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        cdft__fyt = []
        for vpbrq__aow in rjv__aam:
            if vpbrq__aow == '':
                continue
            ocku__extk = self.pathsep.join((base_path, vpbrq__aow))
            if vpbrq__aow.endswith('_common_metadata'):
                self.common_metadata_path = ocku__extk
            elif vpbrq__aow.endswith('_metadata'):
                self.metadata_path = ocku__extk
            elif self._should_silently_exclude(vpbrq__aow):
                continue
            elif self.delta_lake_filter and ocku__extk not in self.delta_lake_filter:
                continue
            else:
                cdft__fyt.append(ocku__extk)
        qclb__gcc = [self.pathsep.join((base_path, owwtq__ejrf)) for
            owwtq__ejrf in cndyb__rpcxz if not pq._is_private_directory(
            owwtq__ejrf)]
        cdft__fyt.sort()
        qclb__gcc.sort()
        if len(cdft__fyt) > 0 and len(qclb__gcc) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(qclb__gcc) > 0:
            await self._visit_directories(fjbtv__jjgxw, qclb__gcc, awb__jlee)
        else:
            self._push_pieces(cdft__fyt, awb__jlee)

    async def _visit_directories(self, fjbtv__jjgxw, cndyb__rpcxz, awb__jlee):
        xic__ogx = []
        for vpbrq__aow in cndyb__rpcxz:
            rxjue__svr, tcb__uoz = pq._path_split(vpbrq__aow, self.pathsep)
            vgw__ssxqf, qcg__wihh = pq._parse_hive_partition(tcb__uoz)
            tfay__ofn = self.partitions.get_index(fjbtv__jjgxw, vgw__ssxqf,
                qcg__wihh)
            self.partition_vals[vgw__ssxqf].add(qcg__wihh)
            wtfgl__clq = awb__jlee + [(vgw__ssxqf, qcg__wihh)]
            xic__ogx.append(self._visit_level(fjbtv__jjgxw + 1, vpbrq__aow,
                wtfgl__clq))
        await asyncio.wait(xic__ogx)


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
