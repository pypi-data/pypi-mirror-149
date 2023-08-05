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
            bxdee__ywfuy = self.fs.open_input_file(path)
        except:
            bxdee__ywfuy = self.fs.open_input_stream(path)
    elif mode == 'wb':
        bxdee__ywfuy = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, bxdee__ywfuy, path, mode, block_size, **kwargs)


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
    xvsc__stuc = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    upigj__nlsv = False
    cido__wreou = get_proxy_uri_from_env_vars()
    if storage_options:
        upigj__nlsv = storage_options.get('anon', False)
    return S3FileSystem(anonymous=upigj__nlsv, region=region,
        endpoint_override=xvsc__stuc, proxy_options=cido__wreou)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    xvsc__stuc = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    upigj__nlsv = False
    cido__wreou = get_proxy_uri_from_env_vars()
    if storage_options:
        upigj__nlsv = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=xvsc__stuc,
        anonymous=upigj__nlsv, proxy_options=cido__wreou)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    vqq__beb = urlparse(path)
    if vqq__beb.scheme in ('abfs', 'abfss'):
        wmop__hrxd = path
        if vqq__beb.port is None:
            kel__pft = 0
        else:
            kel__pft = vqq__beb.port
        teby__ujvm = None
    else:
        wmop__hrxd = vqq__beb.hostname
        kel__pft = vqq__beb.port
        teby__ujvm = vqq__beb.username
    try:
        fs = HdFS(host=wmop__hrxd, port=kel__pft, user=teby__ujvm)
    except Exception as pcg__wlxf:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            pcg__wlxf))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        fjx__vsxnw = fs.isdir(path)
    except gcsfs.utils.HttpError as pcg__wlxf:
        raise BodoError(
            f'{pcg__wlxf}. Make sure your google cloud credentials are set!')
    return fjx__vsxnw


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [bts__jtvsw.split('/')[-1] for bts__jtvsw in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        vqq__beb = urlparse(path)
        cfolo__pafu = (vqq__beb.netloc + vqq__beb.path).rstrip('/')
        tcdfc__hihhj = fs.get_file_info(cfolo__pafu)
        if tcdfc__hihhj.type in (pa_fs.FileType.NotFound, pa_fs.FileType.
            Unknown):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if (not tcdfc__hihhj.size and tcdfc__hihhj.type == pa_fs.FileType.
            Directory):
            return True
        return False
    except (FileNotFoundError, OSError) as pcg__wlxf:
        raise
    except BodoError as bcydb__daj:
        raise
    except Exception as pcg__wlxf:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(pcg__wlxf).__name__}: {str(pcg__wlxf)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    jvvrn__atqz = None
    try:
        if s3_is_directory(fs, path):
            vqq__beb = urlparse(path)
            cfolo__pafu = (vqq__beb.netloc + vqq__beb.path).rstrip('/')
            wxnn__tdcl = pa_fs.FileSelector(cfolo__pafu, recursive=False)
            wta__quja = fs.get_file_info(wxnn__tdcl)
            if wta__quja and wta__quja[0].path in [cfolo__pafu,
                f'{cfolo__pafu}/'] and int(wta__quja[0].size or 0) == 0:
                wta__quja = wta__quja[1:]
            jvvrn__atqz = [lzdm__vuh.base_name for lzdm__vuh in wta__quja]
    except BodoError as bcydb__daj:
        raise
    except Exception as pcg__wlxf:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(pcg__wlxf).__name__}: {str(pcg__wlxf)}
{bodo_error_msg}"""
            )
    return jvvrn__atqz


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    vqq__beb = urlparse(path)
    eqoy__hav = vqq__beb.path
    try:
        ddf__altn = HadoopFileSystem.from_uri(path)
    except Exception as pcg__wlxf:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            pcg__wlxf))
    vfkt__zmlnt = ddf__altn.get_file_info([eqoy__hav])
    if vfkt__zmlnt[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not vfkt__zmlnt[0].size and vfkt__zmlnt[0].type == FileType.Directory:
        return ddf__altn, True
    return ddf__altn, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    jvvrn__atqz = None
    ddf__altn, fjx__vsxnw = hdfs_is_directory(path)
    if fjx__vsxnw:
        vqq__beb = urlparse(path)
        eqoy__hav = vqq__beb.path
        wxnn__tdcl = FileSelector(eqoy__hav, recursive=True)
        try:
            wta__quja = ddf__altn.get_file_info(wxnn__tdcl)
        except Exception as pcg__wlxf:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(eqoy__hav, pcg__wlxf))
        jvvrn__atqz = [lzdm__vuh.base_name for lzdm__vuh in wta__quja]
    return ddf__altn, jvvrn__atqz


def abfs_is_directory(path):
    ddf__altn = get_hdfs_fs(path)
    try:
        vfkt__zmlnt = ddf__altn.info(path)
    except OSError as bcydb__daj:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if vfkt__zmlnt['size'] == 0 and vfkt__zmlnt['kind'].lower() == 'directory':
        return ddf__altn, True
    return ddf__altn, False


def abfs_list_dir_fnames(path):
    jvvrn__atqz = None
    ddf__altn, fjx__vsxnw = abfs_is_directory(path)
    if fjx__vsxnw:
        vqq__beb = urlparse(path)
        eqoy__hav = vqq__beb.path
        try:
            pto__wxdj = ddf__altn.ls(eqoy__hav)
        except Exception as pcg__wlxf:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(eqoy__hav, pcg__wlxf))
        jvvrn__atqz = [fname[fname.rindex('/') + 1:] for fname in pto__wxdj]
    return ddf__altn, jvvrn__atqz


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    ssb__enss = urlparse(path)
    fname = path
    fs = None
    yafeb__loepf = 'read_json' if ftype == 'json' else 'read_csv'
    uou__eojeq = (
        f'pd.{yafeb__loepf}(): there is no {ftype} file in directory: {fname}')
    lyzi__sgnw = directory_of_files_common_filter
    if ssb__enss.scheme == 's3':
        jwkl__adtx = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        gahno__nxp = s3_list_dir_fnames(fs, path)
        cfolo__pafu = (ssb__enss.netloc + ssb__enss.path).rstrip('/')
        fname = cfolo__pafu
        if gahno__nxp:
            gahno__nxp = [(cfolo__pafu + '/' + bts__jtvsw) for bts__jtvsw in
                sorted(filter(lyzi__sgnw, gahno__nxp))]
            lfgs__nsf = [bts__jtvsw for bts__jtvsw in gahno__nxp if int(fs.
                get_file_info(bts__jtvsw).size or 0) > 0]
            if len(lfgs__nsf) == 0:
                raise BodoError(uou__eojeq)
            fname = lfgs__nsf[0]
        yos__siva = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        msgt__muz = fs._open(fname)
    elif ssb__enss.scheme == 'hdfs':
        jwkl__adtx = True
        fs, gahno__nxp = hdfs_list_dir_fnames(path)
        yos__siva = fs.get_file_info([ssb__enss.path])[0].size
        if gahno__nxp:
            path = path.rstrip('/')
            gahno__nxp = [(path + '/' + bts__jtvsw) for bts__jtvsw in
                sorted(filter(lyzi__sgnw, gahno__nxp))]
            lfgs__nsf = [bts__jtvsw for bts__jtvsw in gahno__nxp if fs.
                get_file_info([urlparse(bts__jtvsw).path])[0].size > 0]
            if len(lfgs__nsf) == 0:
                raise BodoError(uou__eojeq)
            fname = lfgs__nsf[0]
            fname = urlparse(fname).path
            yos__siva = fs.get_file_info([fname])[0].size
        msgt__muz = fs.open_input_file(fname)
    elif ssb__enss.scheme in ('abfs', 'abfss'):
        jwkl__adtx = True
        fs, gahno__nxp = abfs_list_dir_fnames(path)
        yos__siva = fs.info(fname)['size']
        if gahno__nxp:
            path = path.rstrip('/')
            gahno__nxp = [(path + '/' + bts__jtvsw) for bts__jtvsw in
                sorted(filter(lyzi__sgnw, gahno__nxp))]
            lfgs__nsf = [bts__jtvsw for bts__jtvsw in gahno__nxp if fs.info
                (bts__jtvsw)['size'] > 0]
            if len(lfgs__nsf) == 0:
                raise BodoError(uou__eojeq)
            fname = lfgs__nsf[0]
            yos__siva = fs.info(fname)['size']
            fname = urlparse(fname).path
        msgt__muz = fs.open(fname, 'rb')
    else:
        if ssb__enss.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {ssb__enss.scheme}. Please refer to https://docs.bodo.ai/latest/source/file_io.html'
                )
        jwkl__adtx = False
        if os.path.isdir(path):
            pto__wxdj = filter(lyzi__sgnw, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            lfgs__nsf = [bts__jtvsw for bts__jtvsw in sorted(pto__wxdj) if 
                os.path.getsize(bts__jtvsw) > 0]
            if len(lfgs__nsf) == 0:
                raise BodoError(uou__eojeq)
            fname = lfgs__nsf[0]
        yos__siva = os.path.getsize(fname)
        msgt__muz = fname
    return jwkl__adtx, msgt__muz, yos__siva, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    rqgs__eprji = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            umaqi__fyy, pjrz__vtmcj = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = umaqi__fyy.region
        except Exception as pcg__wlxf:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{pcg__wlxf}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = rqgs__eprji.bcast(bucket_loc)
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
        zgvf__eaaaw = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        qbx__ttuzi, duoer__dok = unicode_to_utf8_and_len(D)
        yvlfr__ckdwz = 0
        if is_parallel:
            yvlfr__ckdwz = bodo.libs.distributed_api.dist_exscan(duoer__dok,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), qbx__ttuzi, yvlfr__ckdwz,
            duoer__dok, is_parallel, unicode_to_utf8(zgvf__eaaaw))
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
    csd__nduz = get_overload_constant_dict(storage_options)
    ftn__xxbt = 'def impl(storage_options):\n'
    ftn__xxbt += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    ftn__xxbt += f'    storage_options_py = {str(csd__nduz)}\n'
    ftn__xxbt += '  return storage_options_py\n'
    hkdlm__ijssh = {}
    exec(ftn__xxbt, globals(), hkdlm__ijssh)
    return hkdlm__ijssh['impl']
