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
    except Exception as rnlx__dlak:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    aod__utlbq = None
    sra__tvn = delta_lake_path.rstrip('/')
    ohtyp__qgq = 'AWS_DEFAULT_REGION' in os.environ
    dbq__qhwz = os.environ.get('AWS_DEFAULT_REGION', '')
    etz__ifd = False
    if delta_lake_path.startswith('s3://'):
        lxti__gsqt = get_s3_bucket_region_njit(delta_lake_path, parallel=False)
        if lxti__gsqt != '':
            os.environ['AWS_DEFAULT_REGION'] = lxti__gsqt
            etz__ifd = True
    fpzwt__gzoq = DeltaTable(delta_lake_path)
    aod__utlbq = fpzwt__gzoq.files()
    aod__utlbq = [(sra__tvn + '/' + evo__acg) for evo__acg in sorted(
        aod__utlbq)]
    if etz__ifd:
        if ohtyp__qgq:
            os.environ['AWS_DEFAULT_REGION'] = dbq__qhwz
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return aod__utlbq


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    ezr__vpm = None
    yrwvl__uadjr = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        ezr__vpm = manifest.common_metadata_path
        yrwvl__uadjr = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        tex__zbmhn = urlparse(path_or_paths[0]).scheme
        for sra__tvn in path_or_paths:
            if not tex__zbmhn and not fs.isfile(sra__tvn):
                raise OSError(
                    f'Passed non-file path: {sra__tvn}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(sra__tvn, open_file_func
                =open_file_func)
            pieces.append(piece)
    return pieces, partitions, ezr__vpm, yrwvl__uadjr


pq._make_manifest = _make_manifest


def get_dataset_schema(dataset):
    if dataset.metadata is None and dataset.schema is None:
        if dataset.common_metadata is not None:
            dataset.schema = dataset.common_metadata.schema
        else:
            dataset.schema = dataset.pieces[0].get_metadata().schema
    elif dataset.schema is None:
        dataset.schema = dataset.metadata.schema
    kpt__jrde = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for nkhh__nibxs in dataset.partitions.partition_names:
            if kpt__jrde.get_field_index(nkhh__nibxs) != -1:
                mcofg__izb = kpt__jrde.get_field_index(nkhh__nibxs)
                kpt__jrde = kpt__jrde.remove(mcofg__izb)
    return kpt__jrde


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
        except Exception as rnlx__dlak:
            self.exc = rnlx__dlak
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
        sbj__ntaz = VisitLevelThread(self)
        sbj__ntaz.start()
        sbj__ntaz.join()
        for uurix__xztds in self.partition_vals.keys():
            self.partition_vals[uurix__xztds] = sorted(self.partition_vals[
                uurix__xztds])
        for syhgb__ykkz in self.partitions.levels:
            syhgb__ykkz.keys = sorted(syhgb__ykkz.keys)
        for dei__dtus in self.pieces:
            if dei__dtus.partition_keys is not None:
                dei__dtus.partition_keys = [(mfe__lgio, self.partition_vals
                    [mfe__lgio].index(esvl__yebww)) for mfe__lgio,
                    esvl__yebww in dei__dtus.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, mgkup__dlpyl, base_path, qjvgg__epwn):
        fs = self.filesystem
        rwx__tjute, ebald__ljjoa, pyk__aeyo = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if mgkup__dlpyl == 0 and '_delta_log' in ebald__ljjoa:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        ealb__mjxkf = []
        for sra__tvn in pyk__aeyo:
            if sra__tvn == '':
                continue
            buur__cgnh = self.pathsep.join((base_path, sra__tvn))
            if sra__tvn.endswith('_common_metadata'):
                self.common_metadata_path = buur__cgnh
            elif sra__tvn.endswith('_metadata'):
                self.metadata_path = buur__cgnh
            elif self._should_silently_exclude(sra__tvn):
                continue
            elif self.delta_lake_filter and buur__cgnh not in self.delta_lake_filter:
                continue
            else:
                ealb__mjxkf.append(buur__cgnh)
        nmx__lqe = [self.pathsep.join((base_path, xnmp__ecxbf)) for
            xnmp__ecxbf in ebald__ljjoa if not pq._is_private_directory(
            xnmp__ecxbf)]
        ealb__mjxkf.sort()
        nmx__lqe.sort()
        if len(ealb__mjxkf) > 0 and len(nmx__lqe) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(nmx__lqe) > 0:
            await self._visit_directories(mgkup__dlpyl, nmx__lqe, qjvgg__epwn)
        else:
            self._push_pieces(ealb__mjxkf, qjvgg__epwn)

    async def _visit_directories(self, mgkup__dlpyl, ebald__ljjoa, qjvgg__epwn
        ):
        bdmb__kilpb = []
        for sra__tvn in ebald__ljjoa:
            oar__dokr, fwrg__pwla = pq._path_split(sra__tvn, self.pathsep)
            mfe__lgio, ckeq__uald = pq._parse_hive_partition(fwrg__pwla)
            qhiqa__yto = self.partitions.get_index(mgkup__dlpyl, mfe__lgio,
                ckeq__uald)
            self.partition_vals[mfe__lgio].add(ckeq__uald)
            kti__wcvjo = qjvgg__epwn + [(mfe__lgio, ckeq__uald)]
            bdmb__kilpb.append(self._visit_level(mgkup__dlpyl + 1, sra__tvn,
                kti__wcvjo))
        await asyncio.wait(bdmb__kilpb)


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
