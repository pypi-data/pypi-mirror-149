import gc
import inspect
import sys
import types as pytypes
import bodo
master_mode_on = False
MASTER_RANK = 0


class MasterModeDispatcher(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, *args, **kwargs):
        assert bodo.get_rank() == MASTER_RANK
        return master_wrapper(self.dispatcher, *args, **kwargs)

    def __getstate__(self):
        assert bodo.get_rank() == MASTER_RANK
        return self.dispatcher.py_func

    def __setstate__(self, state):
        assert bodo.get_rank() != MASTER_RANK
        ctsh__emgp = state
        pnj__ntq = inspect.getsourcelines(ctsh__emgp)[0][0]
        assert pnj__ntq.startswith('@bodo.jit') or pnj__ntq.startswith('@jit')
        wdzcf__fjawu = eval(pnj__ntq[1:])
        self.dispatcher = wdzcf__fjawu(ctsh__emgp)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    ybawa__aev = MPI.COMM_WORLD
    while True:
        gar__ldms = ybawa__aev.bcast(None, root=MASTER_RANK)
        if gar__ldms[0] == 'exec':
            ctsh__emgp = pickle.loads(gar__ldms[1])
            for mwl__kldr, cfoo__kbfql in list(ctsh__emgp.__globals__.items()):
                if isinstance(cfoo__kbfql, MasterModeDispatcher):
                    ctsh__emgp.__globals__[mwl__kldr] = cfoo__kbfql.dispatcher
            if ctsh__emgp.__module__ not in sys.modules:
                sys.modules[ctsh__emgp.__module__] = pytypes.ModuleType(
                    ctsh__emgp.__module__)
            pnj__ntq = inspect.getsourcelines(ctsh__emgp)[0][0]
            assert pnj__ntq.startswith('@bodo.jit') or pnj__ntq.startswith(
                '@jit')
            wdzcf__fjawu = eval(pnj__ntq[1:])
            func = wdzcf__fjawu(ctsh__emgp)
            mzhd__qibo = gar__ldms[2]
            okl__qzhyw = gar__ldms[3]
            qiith__fnhm = []
            for qrpl__oepty in mzhd__qibo:
                if qrpl__oepty == 'scatter':
                    qiith__fnhm.append(bodo.scatterv(None))
                elif qrpl__oepty == 'bcast':
                    qiith__fnhm.append(ybawa__aev.bcast(None, root=MASTER_RANK)
                        )
            vgfg__woenm = {}
            for argname, qrpl__oepty in okl__qzhyw.items():
                if qrpl__oepty == 'scatter':
                    vgfg__woenm[argname] = bodo.scatterv(None)
                elif qrpl__oepty == 'bcast':
                    vgfg__woenm[argname] = ybawa__aev.bcast(None, root=
                        MASTER_RANK)
            xnd__nfsln = func(*qiith__fnhm, **vgfg__woenm)
            if xnd__nfsln is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(xnd__nfsln)
            del (gar__ldms, ctsh__emgp, func, wdzcf__fjawu, mzhd__qibo,
                okl__qzhyw, qiith__fnhm, vgfg__woenm, xnd__nfsln)
            gc.collect()
        elif gar__ldms[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    ybawa__aev = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        mzhd__qibo = ['scatter' for cnjf__ugfrg in range(len(args))]
        okl__qzhyw = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        bvm__ffeyq = func.py_func.__code__.co_varnames
        xfs__tcdmn = func.targetoptions

        def get_distribution(argname):
            if argname in xfs__tcdmn.get('distributed', []
                ) or argname in xfs__tcdmn.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        mzhd__qibo = [get_distribution(argname) for argname in bvm__ffeyq[:
            len(args)]]
        okl__qzhyw = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    gjcfs__irq = pickle.dumps(func.py_func)
    ybawa__aev.bcast(['exec', gjcfs__irq, mzhd__qibo, okl__qzhyw])
    qiith__fnhm = []
    for jrlv__cpcfu, qrpl__oepty in zip(args, mzhd__qibo):
        if qrpl__oepty == 'scatter':
            qiith__fnhm.append(bodo.scatterv(jrlv__cpcfu))
        elif qrpl__oepty == 'bcast':
            ybawa__aev.bcast(jrlv__cpcfu)
            qiith__fnhm.append(jrlv__cpcfu)
    vgfg__woenm = {}
    for argname, jrlv__cpcfu in kwargs.items():
        qrpl__oepty = okl__qzhyw[argname]
        if qrpl__oepty == 'scatter':
            vgfg__woenm[argname] = bodo.scatterv(jrlv__cpcfu)
        elif qrpl__oepty == 'bcast':
            ybawa__aev.bcast(jrlv__cpcfu)
            vgfg__woenm[argname] = jrlv__cpcfu
    hhx__ceeru = []
    for mwl__kldr, cfoo__kbfql in list(func.py_func.__globals__.items()):
        if isinstance(cfoo__kbfql, MasterModeDispatcher):
            hhx__ceeru.append((func.py_func.__globals__, mwl__kldr, func.
                py_func.__globals__[mwl__kldr]))
            func.py_func.__globals__[mwl__kldr] = cfoo__kbfql.dispatcher
    xnd__nfsln = func(*qiith__fnhm, **vgfg__woenm)
    for dttzb__ziw, mwl__kldr, cfoo__kbfql in hhx__ceeru:
        dttzb__ziw[mwl__kldr] = cfoo__kbfql
    if xnd__nfsln is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        xnd__nfsln = bodo.gatherv(xnd__nfsln)
    return xnd__nfsln


def init_master_mode():
    if bodo.get_size() == 1:
        return
    global master_mode_on
    assert master_mode_on is False, 'init_master_mode can only be called once on each process'
    master_mode_on = True
    assert sys.version_info[:2] >= (3, 8
        ), 'Python 3.8+ required for master mode'
    from bodo import jit
    globals()['jit'] = jit
    import cloudpickle
    from mpi4py import MPI
    globals()['pickle'] = cloudpickle
    globals()['MPI'] = MPI

    def master_exit():
        MPI.COMM_WORLD.bcast(['exit'])
    if bodo.get_rank() == MASTER_RANK:
        import atexit
        atexit.register(master_exit)
    else:
        worker_loop()
