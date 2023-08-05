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
    pfdo__vtssz = MPI.COMM_WORLD
    hykmd__sjd = pfdo__vtssz.Get_rank()
    ktcpd__bexfk = get_host_ranks()
    hch__gvb = get_nodes_first_ranks()
    if hykmd__sjd in hch__gvb:
        try:
            fei__rxw = get_num_gpus(framework)
        except Exception as hnvqj__lyf:
            fei__rxw = hnvqj__lyf
        vcuds__ezcez = create_subcomm_mpi4py(hch__gvb)
        wycr__xcn = vcuds__ezcez.gather(fei__rxw)
        if hykmd__sjd == 0:
            gpu_ranks = []
            uzhiw__xss = None
            for wea__praco, lefgk__skshe in enumerate(ktcpd__bexfk.values()):
                uerzg__mwz = wycr__xcn[wea__praco]
                if isinstance(uerzg__mwz, Exception):
                    uzhiw__xss = uerzg__mwz
                    break
                if uerzg__mwz == 0:
                    continue
                wedi__bgw = len(lefgk__skshe) // uerzg__mwz
                for wibtq__vblcw, jrdj__qhl in enumerate(lefgk__skshe):
                    if wibtq__vblcw % wedi__bgw == 0:
                        vxck__wfey = wibtq__vblcw / wedi__bgw
                        if vxck__wfey < uerzg__mwz:
                            gpu_ranks.append(jrdj__qhl)
            if uzhiw__xss:
                pfdo__vtssz.bcast(uzhiw__xss)
                raise uzhiw__xss
            else:
                pfdo__vtssz.bcast(gpu_ranks)
    if hykmd__sjd != 0:
        gpu_ranks = pfdo__vtssz.bcast(None)
        if isinstance(gpu_ranks, Exception):
            hnvqj__lyf = gpu_ranks
            raise hnvqj__lyf
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
    dhtr__grnpi = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        vcuds__ezcez = MPI.COMM_WORLD.Split(color=0 if dhtr__grnpi in
            gpu_ranks else MPI.UNDEFINED, key=dhtr__grnpi)
        if vcuds__ezcez != MPI.COMM_NULL:
            hvd.init(comm=vcuds__ezcez)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                nmfe__stq = tf.config.experimental.list_physical_devices('GPU')
                for spdph__twrkx in nmfe__stq:
                    tf.config.experimental.set_memory_growth(spdph__twrkx, True
                        )
                tf.config.experimental.set_visible_devices(nmfe__stq[hvd.
                    local_rank()], 'GPU')
    else:
        if dhtr__grnpi == 0:
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
        rvuu__ebxuo = 17
        pfdo__vtssz = MPI.COMM_WORLD
        nivow__bsw = MPI.Get_processor_name()
        leu__ztfon = get_host_ranks()[nivow__bsw]
        assert_dl_initialized()
        if bodo.get_rank() == leu__ztfon[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for hykmd__sjd in leu__ztfon[1:]:
                pfdo__vtssz.isend(1, dest=hykmd__sjd, tag=rvuu__ebxuo)
        else:
            while True:
                utw__uxs = MPI.Status()
                wbahr__hqird = pfdo__vtssz.Iprobe(MPI.ANY_SOURCE, MPI.
                    ANY_TAG, utw__uxs)
                if wbahr__hqird:
                    assert utw__uxs.source == leu__ztfon[0]
                    assert utw__uxs.tag == rvuu__ebxuo
                    pfdo__vtssz.recv(source=0, tag=rvuu__ebxuo)
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
