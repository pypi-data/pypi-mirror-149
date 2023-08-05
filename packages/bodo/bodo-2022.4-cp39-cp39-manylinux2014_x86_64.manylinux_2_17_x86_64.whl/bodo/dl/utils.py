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
    cyfu__xpbu = MPI.COMM_WORLD
    mydd__qvfa = cyfu__xpbu.Get_rank()
    yske__czvq = get_host_ranks()
    htj__ayy = get_nodes_first_ranks()
    if mydd__qvfa in htj__ayy:
        try:
            jxh__grjwv = get_num_gpus(framework)
        except Exception as etoc__flx:
            jxh__grjwv = etoc__flx
        sfym__ltgj = create_subcomm_mpi4py(htj__ayy)
        ngq__ywqlk = sfym__ltgj.gather(jxh__grjwv)
        if mydd__qvfa == 0:
            gpu_ranks = []
            rlkms__ytaah = None
            for oti__cqvj, byzqj__lbdp in enumerate(yske__czvq.values()):
                gfcto__vvee = ngq__ywqlk[oti__cqvj]
                if isinstance(gfcto__vvee, Exception):
                    rlkms__ytaah = gfcto__vvee
                    break
                if gfcto__vvee == 0:
                    continue
                hcrxg__iwoxd = len(byzqj__lbdp) // gfcto__vvee
                for hrdlf__jvkmn, bdf__zsvo in enumerate(byzqj__lbdp):
                    if hrdlf__jvkmn % hcrxg__iwoxd == 0:
                        fmvo__veyk = hrdlf__jvkmn / hcrxg__iwoxd
                        if fmvo__veyk < gfcto__vvee:
                            gpu_ranks.append(bdf__zsvo)
            if rlkms__ytaah:
                cyfu__xpbu.bcast(rlkms__ytaah)
                raise rlkms__ytaah
            else:
                cyfu__xpbu.bcast(gpu_ranks)
    if mydd__qvfa != 0:
        gpu_ranks = cyfu__xpbu.bcast(None)
        if isinstance(gpu_ranks, Exception):
            etoc__flx = gpu_ranks
            raise etoc__flx
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
    qroqw__yxj = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        sfym__ltgj = MPI.COMM_WORLD.Split(color=0 if qroqw__yxj in
            gpu_ranks else MPI.UNDEFINED, key=qroqw__yxj)
        if sfym__ltgj != MPI.COMM_NULL:
            hvd.init(comm=sfym__ltgj)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                ulf__wco = tf.config.experimental.list_physical_devices('GPU')
                for upwjt__ayz in ulf__wco:
                    tf.config.experimental.set_memory_growth(upwjt__ayz, True)
                tf.config.experimental.set_visible_devices(ulf__wco[hvd.
                    local_rank()], 'GPU')
    else:
        if qroqw__yxj == 0:
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
        synjt__hmhr = 17
        cyfu__xpbu = MPI.COMM_WORLD
        efpyx__xoal = MPI.Get_processor_name()
        wpfl__bdyx = get_host_ranks()[efpyx__xoal]
        assert_dl_initialized()
        if bodo.get_rank() == wpfl__bdyx[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for mydd__qvfa in wpfl__bdyx[1:]:
                cyfu__xpbu.isend(1, dest=mydd__qvfa, tag=synjt__hmhr)
        else:
            while True:
                kvaui__xax = MPI.Status()
                ras__zydxh = cyfu__xpbu.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    kvaui__xax)
                if ras__zydxh:
                    assert kvaui__xax.source == wpfl__bdyx[0]
                    assert kvaui__xax.tag == synjt__hmhr
                    cyfu__xpbu.recv(source=0, tag=synjt__hmhr)
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
