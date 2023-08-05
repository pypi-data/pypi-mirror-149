"""Support distributed deep learning with Horovod
"""
import time
import numba
import numpy as np
from mpi4py import MPI
import bodo
from bodo.libs.distributed_api import create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks
dl_status = None


def assert_dl_initialized():
    assert dl_status is not None, 'Horovod has not been initialized. Call bodo.dl.start() first'


class DLStatus(object):

    def __init__(self, framework, gpu_ranks):
        self.framework = framework
        self.gpu_ranks = gpu_ranks


def get_num_gpus(framework):
    if framework == 'torch':
        import torch
        return torch.cuda.device_count()
    elif framework == 'tensorflow':
        import tensorflow as tf
        return len(tf.config.experimental.list_physical_devices('GPU'))
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))


def get_gpu_ranks(framework):
    joaq__ppygb = MPI.COMM_WORLD
    cvbm__mhfs = joaq__ppygb.Get_rank()
    qem__dialr = get_host_ranks()
    dvsl__sjvrj = get_nodes_first_ranks()
    if cvbm__mhfs in dvsl__sjvrj:
        try:
            aazi__sxzd = get_num_gpus(framework)
        except Exception as gyji__qvhnb:
            aazi__sxzd = gyji__qvhnb
        ans__kkmk = create_subcomm_mpi4py(dvsl__sjvrj)
        ozuwn__usc = ans__kkmk.gather(aazi__sxzd)
        if cvbm__mhfs == 0:
            gpu_ranks = []
            wpq__nghjd = None
            for kvkp__rke, hhr__tckj in enumerate(qem__dialr.values()):
                lfgkg__vqwqy = ozuwn__usc[kvkp__rke]
                if isinstance(lfgkg__vqwqy, Exception):
                    wpq__nghjd = lfgkg__vqwqy
                    break
                if lfgkg__vqwqy == 0:
                    continue
                jvkxk__frg = len(hhr__tckj) // lfgkg__vqwqy
                for nqymm__tyyy, fhp__tvfl in enumerate(hhr__tckj):
                    if nqymm__tyyy % jvkxk__frg == 0:
                        fbl__qjz = nqymm__tyyy / jvkxk__frg
                        if fbl__qjz < lfgkg__vqwqy:
                            gpu_ranks.append(fhp__tvfl)
            if wpq__nghjd:
                joaq__ppygb.bcast(wpq__nghjd)
                raise wpq__nghjd
            else:
                joaq__ppygb.bcast(gpu_ranks)
    if cvbm__mhfs != 0:
        gpu_ranks = joaq__ppygb.bcast(None)
        if isinstance(gpu_ranks, Exception):
            gyji__qvhnb = gpu_ranks
            raise gyji__qvhnb
    return gpu_ranks


def is_cuda_available():
    assert_dl_initialized()
    return len(dl_status.gpu_ranks) > 0


def initialize_horovod(framework):
    global dl_status
    if dl_status is not None:
        assert dl_status.framework == framework, 'Attempted to initialize Horovod with different DL frameworks'
        return np.array(dl_status.gpu_ranks, dtype=np.int32)
    gpu_ranks = get_gpu_ranks(framework)
    if framework == 'torch':
        import horovod.torch as hvd
        import torch
        torch.set_num_threads(1)
    elif framework == 'tensorflow':
        import horovod.tensorflow as hvd
        import tensorflow as tf
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))
    fhou__nyc = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        ans__kkmk = MPI.COMM_WORLD.Split(color=0 if fhou__nyc in gpu_ranks else
            MPI.UNDEFINED, key=fhou__nyc)
        if ans__kkmk != MPI.COMM_NULL:
            hvd.init(comm=ans__kkmk)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                iwuy__yuqmj = tf.config.experimental.list_physical_devices(
                    'GPU')
                for upuf__celh in iwuy__yuqmj:
                    tf.config.experimental.set_memory_growth(upuf__celh, True)
                tf.config.experimental.set_visible_devices(iwuy__yuqmj[hvd.
                    local_rank()], 'GPU')
    else:
        if fhou__nyc == 0:
            print('[BODO-DL]: No GPUs found in cluster. Using CPUs')
        hvd.init()
    dl_status = DLStatus(framework, np.array(gpu_ranks, dtype=np.int32))


@numba.njit
def start(framework):
    with numba.objmode:
        initialize_horovod(framework)


@numba.njit
def end():
    with numba.objmode:
        end_py()


def end_py():
    if is_cuda_available():
        cmz__fxf = 17
        joaq__ppygb = MPI.COMM_WORLD
        mycco__addr = MPI.Get_processor_name()
        pzfm__rvj = get_host_ranks()[mycco__addr]
        assert_dl_initialized()
        if bodo.get_rank() == pzfm__rvj[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for cvbm__mhfs in pzfm__rvj[1:]:
                joaq__ppygb.isend(1, dest=cvbm__mhfs, tag=cmz__fxf)
        else:
            while True:
                gkh__cxfbu = MPI.Status()
                pfy__bhjir = joaq__ppygb.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    gkh__cxfbu)
                if pfy__bhjir:
                    assert gkh__cxfbu.source == pzfm__rvj[0]
                    assert gkh__cxfbu.tag == cmz__fxf
                    joaq__ppygb.recv(source=0, tag=cmz__fxf)
                    break
                time.sleep(1.0)
    else:
        bodo.barrier()


def _prepare_data_get_gpu_ranks():
    assert_dl_initialized()
    return dl_status.gpu_ranks


@numba.njit
def prepare_data(data):
    with numba.objmode(gpu_ranks='int32[:]'):
        gpu_ranks = _prepare_data_get_gpu_ranks()
    if len(gpu_ranks) > 0:
        data = bodo.rebalance(data, dests=list(gpu_ranks), parallel=True)
    else:
        data = bodo.rebalance(data, parallel=True)
    return data
