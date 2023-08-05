"""
S3 & Hadoop file system supports, and file system dependent calls
"""
import glob
import os
import warnings
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
from fsspec.implementations.arrow import ArrowFile, ArrowFSWrapper, wrap_exceptions
from numba.core import types
from numba.extending import NativeValue, models, overload, register_model, unbox
import bodo
from bodo.io import csv_cpp
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.str_ext import unicode_to_utf8, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, BodoWarning, get_overload_constant_dict
from bodo.utils.utils import check_java_installation


def fsspec_arrowfswrapper__open(self, path, mode='rb', block_size=None, **
    kwargs):
    if mode == 'rb':
        try:
            tjvzu__eqjlk = self.fs.open_input_file(path)
        except:
            tjvzu__eqjlk = self.fs.open_input_stream(path)
    elif mode == 'wb':
        tjvzu__eqjlk = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, tjvzu__eqjlk, path, mode, block_size, **kwargs)


ArrowFSWrapper._open = wrap_exceptions(fsspec_arrowfswrapper__open)
_csv_write = types.ExternalFunction('csv_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.voidptr))
ll.add_symbol('csv_write', csv_cpp.csv_write)
bodo_error_msg = """
    Some possible causes:
        (1) Incorrect path: Specified file/directory doesn't exist or is unreachable.
        (2) Missing credentials: You haven't provided S3 credentials, neither through 
            environment variables, nor through a local AWS setup 
            that makes the credentials available at ~/.aws/credentials.
        (3) Incorrect credentials: Your S3 credentials are incorrect or do not have
            the correct permissions.
        (4) Wrong bucket region is used. Set AWS_DEFAULT_REGION variable with correct bucket region.
    """


def get_proxy_uri_from_env_vars():
    return os.environ.get('http_proxy', None) or os.environ.get('https_proxy',
        None) or os.environ.get('HTTP_PROXY', None) or os.environ.get(
        'HTTPS_PROXY', None)


def get_s3_fs(region=None, storage_options=None):
    from pyarrow.fs import S3FileSystem
    djjp__ddeca = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    lpi__hlhuk = False
    eji__hbzz = get_proxy_uri_from_env_vars()
    if storage_options:
        lpi__hlhuk = storage_options.get('anon', False)
    return S3FileSystem(anonymous=lpi__hlhuk, region=region,
        endpoint_override=djjp__ddeca, proxy_options=eji__hbzz)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    djjp__ddeca = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    lpi__hlhuk = False
    eji__hbzz = get_proxy_uri_from_env_vars()
    if storage_options:
        lpi__hlhuk = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=djjp__ddeca,
        anonymous=lpi__hlhuk, proxy_options=eji__hbzz)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    fxqzn__jgbz = urlparse(path)
    if fxqzn__jgbz.scheme in ('abfs', 'abfss'):
        ycjd__natq = path
        if fxqzn__jgbz.port is None:
            zjk__wnp = 0
        else:
            zjk__wnp = fxqzn__jgbz.port
        yozg__qxm = None
    else:
        ycjd__natq = fxqzn__jgbz.hostname
        zjk__wnp = fxqzn__jgbz.port
        yozg__qxm = fxqzn__jgbz.username
    try:
        fs = HdFS(host=ycjd__natq, port=zjk__wnp, user=yozg__qxm)
    except Exception as ggp__eln:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            ggp__eln))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        kcs__pbocc = fs.isdir(path)
    except gcsfs.utils.HttpError as ggp__eln:
        raise BodoError(
            f'{ggp__eln}. Make sure your google cloud credentials are set!')
    return kcs__pbocc


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [lrz__eabuk.split('/')[-1] for lrz__eabuk in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        fxqzn__jgbz = urlparse(path)
        yaqda__qnh = (fxqzn__jgbz.netloc + fxqzn__jgbz.path).rstrip('/')
        ybvyc__tdx = fs.get_file_info(yaqda__qnh)
        if ybvyc__tdx.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not ybvyc__tdx.size and ybvyc__tdx.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as ggp__eln:
        raise
    except BodoError as vaoo__zkkb:
        raise
    except Exception as ggp__eln:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(ggp__eln).__name__}: {str(ggp__eln)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    lykx__jhxj = None
    try:
        if s3_is_directory(fs, path):
            fxqzn__jgbz = urlparse(path)
            yaqda__qnh = (fxqzn__jgbz.netloc + fxqzn__jgbz.path).rstrip('/')
            ginq__kpetm = pa_fs.FileSelector(yaqda__qnh, recursive=False)
            xdj__vwkuk = fs.get_file_info(ginq__kpetm)
            if xdj__vwkuk and xdj__vwkuk[0].path in [yaqda__qnh,
                f'{yaqda__qnh}/'] and int(xdj__vwkuk[0].size or 0) == 0:
                xdj__vwkuk = xdj__vwkuk[1:]
            lykx__jhxj = [ufoqw__bgqa.base_name for ufoqw__bgqa in xdj__vwkuk]
    except BodoError as vaoo__zkkb:
        raise
    except Exception as ggp__eln:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(ggp__eln).__name__}: {str(ggp__eln)}
{bodo_error_msg}"""
            )
    return lykx__jhxj


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    fxqzn__jgbz = urlparse(path)
    lip__tdwx = fxqzn__jgbz.path
    try:
        pxw__lnda = HadoopFileSystem.from_uri(path)
    except Exception as ggp__eln:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            ggp__eln))
    vgdj__xbh = pxw__lnda.get_file_info([lip__tdwx])
    if vgdj__xbh[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not vgdj__xbh[0].size and vgdj__xbh[0].type == FileType.Directory:
        return pxw__lnda, True
    return pxw__lnda, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    lykx__jhxj = None
    pxw__lnda, kcs__pbocc = hdfs_is_directory(path)
    if kcs__pbocc:
        fxqzn__jgbz = urlparse(path)
        lip__tdwx = fxqzn__jgbz.path
        ginq__kpetm = FileSelector(lip__tdwx, recursive=True)
        try:
            xdj__vwkuk = pxw__lnda.get_file_info(ginq__kpetm)
        except Exception as ggp__eln:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(lip__tdwx, ggp__eln))
        lykx__jhxj = [ufoqw__bgqa.base_name for ufoqw__bgqa in xdj__vwkuk]
    return pxw__lnda, lykx__jhxj


def abfs_is_directory(path):
    pxw__lnda = get_hdfs_fs(path)
    try:
        vgdj__xbh = pxw__lnda.info(path)
    except OSError as vaoo__zkkb:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if vgdj__xbh['size'] == 0 and vgdj__xbh['kind'].lower() == 'directory':
        return pxw__lnda, True
    return pxw__lnda, False


def abfs_list_dir_fnames(path):
    lykx__jhxj = None
    pxw__lnda, kcs__pbocc = abfs_is_directory(path)
    if kcs__pbocc:
        fxqzn__jgbz = urlparse(path)
        lip__tdwx = fxqzn__jgbz.path
        try:
            czgz__vjs = pxw__lnda.ls(lip__tdwx)
        except Exception as ggp__eln:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(lip__tdwx, ggp__eln))
        lykx__jhxj = [fname[fname.rindex('/') + 1:] for fname in czgz__vjs]
    return pxw__lnda, lykx__jhxj


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    cfzzt__wqc = urlparse(path)
    fname = path
    fs = None
    dtjvo__wrqi = 'read_json' if ftype == 'json' else 'read_csv'
    mzq__qdrzt = (
        f'pd.{dtjvo__wrqi}(): there is no {ftype} file in directory: {fname}')
    bkeg__ntmb = directory_of_files_common_filter
    if cfzzt__wqc.scheme == 's3':
        omvu__mtpq = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        vxyvt__jpr = s3_list_dir_fnames(fs, path)
        yaqda__qnh = (cfzzt__wqc.netloc + cfzzt__wqc.path).rstrip('/')
        fname = yaqda__qnh
        if vxyvt__jpr:
            vxyvt__jpr = [(yaqda__qnh + '/' + lrz__eabuk) for lrz__eabuk in
                sorted(filter(bkeg__ntmb, vxyvt__jpr))]
            gqj__nulj = [lrz__eabuk for lrz__eabuk in vxyvt__jpr if int(fs.
                get_file_info(lrz__eabuk).size or 0) > 0]
            if len(gqj__nulj) == 0:
                raise BodoError(mzq__qdrzt)
            fname = gqj__nulj[0]
        jytu__hks = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        gfhvu__fbmb = fs._open(fname)
    elif cfzzt__wqc.scheme == 'hdfs':
        omvu__mtpq = True
        fs, vxyvt__jpr = hdfs_list_dir_fnames(path)
        jytu__hks = fs.get_file_info([cfzzt__wqc.path])[0].size
        if vxyvt__jpr:
            path = path.rstrip('/')
            vxyvt__jpr = [(path + '/' + lrz__eabuk) for lrz__eabuk in
                sorted(filter(bkeg__ntmb, vxyvt__jpr))]
            gqj__nulj = [lrz__eabuk for lrz__eabuk in vxyvt__jpr if fs.
                get_file_info([urlparse(lrz__eabuk).path])[0].size > 0]
            if len(gqj__nulj) == 0:
                raise BodoError(mzq__qdrzt)
            fname = gqj__nulj[0]
            fname = urlparse(fname).path
            jytu__hks = fs.get_file_info([fname])[0].size
        gfhvu__fbmb = fs.open_input_file(fname)
    elif cfzzt__wqc.scheme in ('abfs', 'abfss'):
        omvu__mtpq = True
        fs, vxyvt__jpr = abfs_list_dir_fnames(path)
        jytu__hks = fs.info(fname)['size']
        if vxyvt__jpr:
            path = path.rstrip('/')
            vxyvt__jpr = [(path + '/' + lrz__eabuk) for lrz__eabuk in
                sorted(filter(bkeg__ntmb, vxyvt__jpr))]
            gqj__nulj = [lrz__eabuk for lrz__eabuk in vxyvt__jpr if fs.info
                (lrz__eabuk)['size'] > 0]
            if len(gqj__nulj) == 0:
                raise BodoError(mzq__qdrzt)
            fname = gqj__nulj[0]
            jytu__hks = fs.info(fname)['size']
            fname = urlparse(fname).path
        gfhvu__fbmb = fs.open(fname, 'rb')
    else:
        if cfzzt__wqc.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {cfzzt__wqc.scheme}. Please refer to https://docs.bodo.ai/latest/source/file_io.html'
                )
        omvu__mtpq = False
        if os.path.isdir(path):
            czgz__vjs = filter(bkeg__ntmb, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            gqj__nulj = [lrz__eabuk for lrz__eabuk in sorted(czgz__vjs) if 
                os.path.getsize(lrz__eabuk) > 0]
            if len(gqj__nulj) == 0:
                raise BodoError(mzq__qdrzt)
            fname = gqj__nulj[0]
        jytu__hks = os.path.getsize(fname)
        gfhvu__fbmb = fname
    return omvu__mtpq, gfhvu__fbmb, jytu__hks, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    bysb__bwi = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            kwkq__mmeo, pbe__doulh = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = kwkq__mmeo.region
        except Exception as ggp__eln:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{ggp__eln}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = bysb__bwi.bcast(bucket_loc)
    return bucket_loc


@numba.njit()
def get_s3_bucket_region_njit(s3_filepath, parallel):
    with numba.objmode(bucket_loc='unicode_type'):
        bucket_loc = ''
        if isinstance(s3_filepath, list):
            s3_filepath = s3_filepath[0]
        if s3_filepath.startswith('s3://'):
            bucket_loc = get_s3_bucket_region(s3_filepath, parallel)
    return bucket_loc


def csv_write(path_or_buf, D, is_parallel=False):
    return None


@overload(csv_write, no_unliteral=True)
def csv_write_overload(path_or_buf, D, is_parallel=False):

    def impl(path_or_buf, D, is_parallel=False):
        nvgw__cuccv = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        ituf__kpayb, tgyqg__yko = unicode_to_utf8_and_len(D)
        zmqcj__wnfw = 0
        if is_parallel:
            zmqcj__wnfw = bodo.libs.distributed_api.dist_exscan(tgyqg__yko,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), ituf__kpayb, zmqcj__wnfw,
            tgyqg__yko, is_parallel, unicode_to_utf8(nvgw__cuccv))
        bodo.utils.utils.check_and_propagate_cpp_exception()
    return impl


class StorageOptionsDictType(types.Opaque):

    def __init__(self):
        super(StorageOptionsDictType, self).__init__(name=
            'StorageOptionsDictType')


storage_options_dict_type = StorageOptionsDictType()
types.storage_options_dict_type = storage_options_dict_type
register_model(StorageOptionsDictType)(models.OpaqueModel)


@unbox(StorageOptionsDictType)
def unbox_storage_options_dict_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


def get_storage_options_pyobject(storage_options):
    pass


@overload(get_storage_options_pyobject, no_unliteral=True)
def overload_get_storage_options_pyobject(storage_options):
    lgfc__tqpwb = get_overload_constant_dict(storage_options)
    pywyr__tjwj = 'def impl(storage_options):\n'
    pywyr__tjwj += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    pywyr__tjwj += f'    storage_options_py = {str(lgfc__tqpwb)}\n'
    pywyr__tjwj += '  return storage_options_py\n'
    vdy__mlqs = {}
    exec(pywyr__tjwj, globals(), vdy__mlqs)
    return vdy__mlqs['impl']
