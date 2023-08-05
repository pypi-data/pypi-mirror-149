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
        ohq__figf = state
        rvt__dta = inspect.getsourcelines(ohq__figf)[0][0]
        assert rvt__dta.startswith('@bodo.jit') or rvt__dta.startswith('@jit')
        dyb__vcktd = eval(rvt__dta[1:])
        self.dispatcher = dyb__vcktd(ohq__figf)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    fkd__qhkbq = MPI.COMM_WORLD
    while True:
        pio__mwqj = fkd__qhkbq.bcast(None, root=MASTER_RANK)
        if pio__mwqj[0] == 'exec':
            ohq__figf = pickle.loads(pio__mwqj[1])
            for ark__now, rvvr__tigfv in list(ohq__figf.__globals__.items()):
                if isinstance(rvvr__tigfv, MasterModeDispatcher):
                    ohq__figf.__globals__[ark__now] = rvvr__tigfv.dispatcher
            if ohq__figf.__module__ not in sys.modules:
                sys.modules[ohq__figf.__module__] = pytypes.ModuleType(
                    ohq__figf.__module__)
            rvt__dta = inspect.getsourcelines(ohq__figf)[0][0]
            assert rvt__dta.startswith('@bodo.jit') or rvt__dta.startswith(
                '@jit')
            dyb__vcktd = eval(rvt__dta[1:])
            func = dyb__vcktd(ohq__figf)
            gaors__etzv = pio__mwqj[2]
            sed__dqzp = pio__mwqj[3]
            iif__dwmb = []
            for tpqwi__epqhf in gaors__etzv:
                if tpqwi__epqhf == 'scatter':
                    iif__dwmb.append(bodo.scatterv(None))
                elif tpqwi__epqhf == 'bcast':
                    iif__dwmb.append(fkd__qhkbq.bcast(None, root=MASTER_RANK))
            coaeq__vmubl = {}
            for argname, tpqwi__epqhf in sed__dqzp.items():
                if tpqwi__epqhf == 'scatter':
                    coaeq__vmubl[argname] = bodo.scatterv(None)
                elif tpqwi__epqhf == 'bcast':
                    coaeq__vmubl[argname] = fkd__qhkbq.bcast(None, root=
                        MASTER_RANK)
            yae__uzko = func(*iif__dwmb, **coaeq__vmubl)
            if yae__uzko is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(yae__uzko)
            del (pio__mwqj, ohq__figf, func, dyb__vcktd, gaors__etzv,
                sed__dqzp, iif__dwmb, coaeq__vmubl, yae__uzko)
            gc.collect()
        elif pio__mwqj[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    fkd__qhkbq = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        gaors__etzv = ['scatter' for bsgff__qshko in range(len(args))]
        sed__dqzp = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        gssa__zeh = func.py_func.__code__.co_varnames
        czo__crv = func.targetoptions

        def get_distribution(argname):
            if argname in czo__crv.get('distributed', []
                ) or argname in czo__crv.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        gaors__etzv = [get_distribution(argname) for argname in gssa__zeh[:
            len(args)]]
        sed__dqzp = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    kjmfa__lrp = pickle.dumps(func.py_func)
    fkd__qhkbq.bcast(['exec', kjmfa__lrp, gaors__etzv, sed__dqzp])
    iif__dwmb = []
    for feu__gqna, tpqwi__epqhf in zip(args, gaors__etzv):
        if tpqwi__epqhf == 'scatter':
            iif__dwmb.append(bodo.scatterv(feu__gqna))
        elif tpqwi__epqhf == 'bcast':
            fkd__qhkbq.bcast(feu__gqna)
            iif__dwmb.append(feu__gqna)
    coaeq__vmubl = {}
    for argname, feu__gqna in kwargs.items():
        tpqwi__epqhf = sed__dqzp[argname]
        if tpqwi__epqhf == 'scatter':
            coaeq__vmubl[argname] = bodo.scatterv(feu__gqna)
        elif tpqwi__epqhf == 'bcast':
            fkd__qhkbq.bcast(feu__gqna)
            coaeq__vmubl[argname] = feu__gqna
    kmjbk__hmimp = []
    for ark__now, rvvr__tigfv in list(func.py_func.__globals__.items()):
        if isinstance(rvvr__tigfv, MasterModeDispatcher):
            kmjbk__hmimp.append((func.py_func.__globals__, ark__now, func.
                py_func.__globals__[ark__now]))
            func.py_func.__globals__[ark__now] = rvvr__tigfv.dispatcher
    yae__uzko = func(*iif__dwmb, **coaeq__vmubl)
    for mmg__dmh, ark__now, rvvr__tigfv in kmjbk__hmimp:
        mmg__dmh[ark__now] = rvvr__tigfv
    if yae__uzko is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        yae__uzko = bodo.gatherv(yae__uzko)
    return yae__uzko


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
