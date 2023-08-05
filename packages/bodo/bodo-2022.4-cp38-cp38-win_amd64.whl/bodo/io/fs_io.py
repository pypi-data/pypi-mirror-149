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
            nllpb__sqtgi = self.fs.open_input_file(path)
        except:
            nllpb__sqtgi = self.fs.open_input_stream(path)
    elif mode == 'wb':
        nllpb__sqtgi = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, nllpb__sqtgi, path, mode, block_size, **kwargs)


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
    iout__jword = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    hfjhn__bkc = False
    caewj__ioj = get_proxy_uri_from_env_vars()
    if storage_options:
        hfjhn__bkc = storage_options.get('anon', False)
    return S3FileSystem(anonymous=hfjhn__bkc, region=region,
        endpoint_override=iout__jword, proxy_options=caewj__ioj)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    iout__jword = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    hfjhn__bkc = False
    caewj__ioj = get_proxy_uri_from_env_vars()
    if storage_options:
        hfjhn__bkc = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=iout__jword,
        anonymous=hfjhn__bkc, proxy_options=caewj__ioj)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    lpww__zkgxd = urlparse(path)
    if lpww__zkgxd.scheme in ('abfs', 'abfss'):
        dcho__rgt = path
        if lpww__zkgxd.port is None:
            wke__afehn = 0
        else:
            wke__afehn = lpww__zkgxd.port
        sfzdj__dwlhb = None
    else:
        dcho__rgt = lpww__zkgxd.hostname
        wke__afehn = lpww__zkgxd.port
        sfzdj__dwlhb = lpww__zkgxd.username
    try:
        fs = HdFS(host=dcho__rgt, port=wke__afehn, user=sfzdj__dwlhb)
    except Exception as orxga__parby:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            orxga__parby))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        mkxtt__jou = fs.isdir(path)
    except gcsfs.utils.HttpError as orxga__parby:
        raise BodoError(
            f'{orxga__parby}. Make sure your google cloud credentials are set!'
            )
    return mkxtt__jou


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [hhpoi__cxtfg.split('/')[-1] for hhpoi__cxtfg in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        lpww__zkgxd = urlparse(path)
        lvzir__idjpc = (lpww__zkgxd.netloc + lpww__zkgxd.path).rstrip('/')
        epci__lxre = fs.get_file_info(lvzir__idjpc)
        if epci__lxre.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not epci__lxre.size and epci__lxre.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as orxga__parby:
        raise
    except BodoError as ihbj__uyc:
        raise
    except Exception as orxga__parby:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(orxga__parby).__name__}: {str(orxga__parby)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    xqcd__hdv = None
    try:
        if s3_is_directory(fs, path):
            lpww__zkgxd = urlparse(path)
            lvzir__idjpc = (lpww__zkgxd.netloc + lpww__zkgxd.path).rstrip('/')
            wovqq__sjcm = pa_fs.FileSelector(lvzir__idjpc, recursive=False)
            pfkj__rkc = fs.get_file_info(wovqq__sjcm)
            if pfkj__rkc and pfkj__rkc[0].path in [lvzir__idjpc,
                f'{lvzir__idjpc}/'] and int(pfkj__rkc[0].size or 0) == 0:
                pfkj__rkc = pfkj__rkc[1:]
            xqcd__hdv = [oeso__wmf.base_name for oeso__wmf in pfkj__rkc]
    except BodoError as ihbj__uyc:
        raise
    except Exception as orxga__parby:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(orxga__parby).__name__}: {str(orxga__parby)}
{bodo_error_msg}"""
            )
    return xqcd__hdv


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    lpww__zkgxd = urlparse(path)
    fcxhy__cnpt = lpww__zkgxd.path
    try:
        zufoz__qhqg = HadoopFileSystem.from_uri(path)
    except Exception as orxga__parby:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            orxga__parby))
    kkkd__iofzc = zufoz__qhqg.get_file_info([fcxhy__cnpt])
    if kkkd__iofzc[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not kkkd__iofzc[0].size and kkkd__iofzc[0].type == FileType.Directory:
        return zufoz__qhqg, True
    return zufoz__qhqg, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    xqcd__hdv = None
    zufoz__qhqg, mkxtt__jou = hdfs_is_directory(path)
    if mkxtt__jou:
        lpww__zkgxd = urlparse(path)
        fcxhy__cnpt = lpww__zkgxd.path
        wovqq__sjcm = FileSelector(fcxhy__cnpt, recursive=True)
        try:
            pfkj__rkc = zufoz__qhqg.get_file_info(wovqq__sjcm)
        except Exception as orxga__parby:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(fcxhy__cnpt, orxga__parby))
        xqcd__hdv = [oeso__wmf.base_name for oeso__wmf in pfkj__rkc]
    return zufoz__qhqg, xqcd__hdv


def abfs_is_directory(path):
    zufoz__qhqg = get_hdfs_fs(path)
    try:
        kkkd__iofzc = zufoz__qhqg.info(path)
    except OSError as ihbj__uyc:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if kkkd__iofzc['size'] == 0 and kkkd__iofzc['kind'].lower() == 'directory':
        return zufoz__qhqg, True
    return zufoz__qhqg, False


def abfs_list_dir_fnames(path):
    xqcd__hdv = None
    zufoz__qhqg, mkxtt__jou = abfs_is_directory(path)
    if mkxtt__jou:
        lpww__zkgxd = urlparse(path)
        fcxhy__cnpt = lpww__zkgxd.path
        try:
            lqpkt__hnmoc = zufoz__qhqg.ls(fcxhy__cnpt)
        except Exception as orxga__parby:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(fcxhy__cnpt, orxga__parby))
        xqcd__hdv = [fname[fname.rindex('/') + 1:] for fname in lqpkt__hnmoc]
    return zufoz__qhqg, xqcd__hdv


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    cwk__jrbd = urlparse(path)
    fname = path
    fs = None
    xgcy__vexp = 'read_json' if ftype == 'json' else 'read_csv'
    cwp__lluh = (
        f'pd.{xgcy__vexp}(): there is no {ftype} file in directory: {fname}')
    yigd__kfrw = directory_of_files_common_filter
    if cwk__jrbd.scheme == 's3':
        yaq__fll = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        qtsia__kysbj = s3_list_dir_fnames(fs, path)
        lvzir__idjpc = (cwk__jrbd.netloc + cwk__jrbd.path).rstrip('/')
        fname = lvzir__idjpc
        if qtsia__kysbj:
            qtsia__kysbj = [(lvzir__idjpc + '/' + hhpoi__cxtfg) for
                hhpoi__cxtfg in sorted(filter(yigd__kfrw, qtsia__kysbj))]
            lhdc__pgcy = [hhpoi__cxtfg for hhpoi__cxtfg in qtsia__kysbj if 
                int(fs.get_file_info(hhpoi__cxtfg).size or 0) > 0]
            if len(lhdc__pgcy) == 0:
                raise BodoError(cwp__lluh)
            fname = lhdc__pgcy[0]
        brk__isy = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        zoq__ewhh = fs._open(fname)
    elif cwk__jrbd.scheme == 'hdfs':
        yaq__fll = True
        fs, qtsia__kysbj = hdfs_list_dir_fnames(path)
        brk__isy = fs.get_file_info([cwk__jrbd.path])[0].size
        if qtsia__kysbj:
            path = path.rstrip('/')
            qtsia__kysbj = [(path + '/' + hhpoi__cxtfg) for hhpoi__cxtfg in
                sorted(filter(yigd__kfrw, qtsia__kysbj))]
            lhdc__pgcy = [hhpoi__cxtfg for hhpoi__cxtfg in qtsia__kysbj if 
                fs.get_file_info([urlparse(hhpoi__cxtfg).path])[0].size > 0]
            if len(lhdc__pgcy) == 0:
                raise BodoError(cwp__lluh)
            fname = lhdc__pgcy[0]
            fname = urlparse(fname).path
            brk__isy = fs.get_file_info([fname])[0].size
        zoq__ewhh = fs.open_input_file(fname)
    elif cwk__jrbd.scheme in ('abfs', 'abfss'):
        yaq__fll = True
        fs, qtsia__kysbj = abfs_list_dir_fnames(path)
        brk__isy = fs.info(fname)['size']
        if qtsia__kysbj:
            path = path.rstrip('/')
            qtsia__kysbj = [(path + '/' + hhpoi__cxtfg) for hhpoi__cxtfg in
                sorted(filter(yigd__kfrw, qtsia__kysbj))]
            lhdc__pgcy = [hhpoi__cxtfg for hhpoi__cxtfg in qtsia__kysbj if 
                fs.info(hhpoi__cxtfg)['size'] > 0]
            if len(lhdc__pgcy) == 0:
                raise BodoError(cwp__lluh)
            fname = lhdc__pgcy[0]
            brk__isy = fs.info(fname)['size']
            fname = urlparse(fname).path
        zoq__ewhh = fs.open(fname, 'rb')
    else:
        if cwk__jrbd.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {cwk__jrbd.scheme}. Please refer to https://docs.bodo.ai/latest/source/file_io.html'
                )
        yaq__fll = False
        if os.path.isdir(path):
            lqpkt__hnmoc = filter(yigd__kfrw, glob.glob(os.path.join(os.
                path.abspath(path), '*')))
            lhdc__pgcy = [hhpoi__cxtfg for hhpoi__cxtfg in sorted(
                lqpkt__hnmoc) if os.path.getsize(hhpoi__cxtfg) > 0]
            if len(lhdc__pgcy) == 0:
                raise BodoError(cwp__lluh)
            fname = lhdc__pgcy[0]
        brk__isy = os.path.getsize(fname)
        zoq__ewhh = fname
    return yaq__fll, zoq__ewhh, brk__isy, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    mpv__jnw = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            pog__wao, eifk__pnppi = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = pog__wao.region
        except Exception as orxga__parby:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{orxga__parby}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = mpv__jnw.bcast(bucket_loc)
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
        mro__mrdc = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel
            )
        wym__rwb, mva__ovx = unicode_to_utf8_and_len(D)
        zly__vrwb = 0
        if is_parallel:
            zly__vrwb = bodo.libs.distributed_api.dist_exscan(mva__ovx, np.
                int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), wym__rwb, zly__vrwb,
            mva__ovx, is_parallel, unicode_to_utf8(mro__mrdc))
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
    jjgjy__zhr = get_overload_constant_dict(storage_options)
    gft__uhkq = 'def impl(storage_options):\n'
    gft__uhkq += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    gft__uhkq += f'    storage_options_py = {str(jjgjy__zhr)}\n'
    gft__uhkq += '  return storage_options_py\n'
    dvlk__yvpm = {}
    exec(gft__uhkq, globals(), dvlk__yvpm)
    return dvlk__yvpm['impl']
