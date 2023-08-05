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
        jbw__gog = state
        ovvt__ezckl = inspect.getsourcelines(jbw__gog)[0][0]
        assert ovvt__ezckl.startswith('@bodo.jit') or ovvt__ezckl.startswith(
            '@jit')
        etzcz__xnx = eval(ovvt__ezckl[1:])
        self.dispatcher = etzcz__xnx(jbw__gog)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    tjpwz__ltbvk = MPI.COMM_WORLD
    while True:
        vxbu__ync = tjpwz__ltbvk.bcast(None, root=MASTER_RANK)
        if vxbu__ync[0] == 'exec':
            jbw__gog = pickle.loads(vxbu__ync[1])
            for nrqp__qsuw, wflm__nlvnb in list(jbw__gog.__globals__.items()):
                if isinstance(wflm__nlvnb, MasterModeDispatcher):
                    jbw__gog.__globals__[nrqp__qsuw] = wflm__nlvnb.dispatcher
            if jbw__gog.__module__ not in sys.modules:
                sys.modules[jbw__gog.__module__] = pytypes.ModuleType(jbw__gog
                    .__module__)
            ovvt__ezckl = inspect.getsourcelines(jbw__gog)[0][0]
            assert ovvt__ezckl.startswith('@bodo.jit'
                ) or ovvt__ezckl.startswith('@jit')
            etzcz__xnx = eval(ovvt__ezckl[1:])
            func = etzcz__xnx(jbw__gog)
            recq__dgufe = vxbu__ync[2]
            vwe__pwqs = vxbu__ync[3]
            rsfb__hdle = []
            for etcza__gkkz in recq__dgufe:
                if etcza__gkkz == 'scatter':
                    rsfb__hdle.append(bodo.scatterv(None))
                elif etcza__gkkz == 'bcast':
                    rsfb__hdle.append(tjpwz__ltbvk.bcast(None, root=
                        MASTER_RANK))
            mjnqh__pke = {}
            for argname, etcza__gkkz in vwe__pwqs.items():
                if etcza__gkkz == 'scatter':
                    mjnqh__pke[argname] = bodo.scatterv(None)
                elif etcza__gkkz == 'bcast':
                    mjnqh__pke[argname] = tjpwz__ltbvk.bcast(None, root=
                        MASTER_RANK)
            uro__ltwu = func(*rsfb__hdle, **mjnqh__pke)
            if uro__ltwu is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(uro__ltwu)
            del (vxbu__ync, jbw__gog, func, etzcz__xnx, recq__dgufe,
                vwe__pwqs, rsfb__hdle, mjnqh__pke, uro__ltwu)
            gc.collect()
        elif vxbu__ync[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    tjpwz__ltbvk = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        recq__dgufe = ['scatter' for kbpz__ebtk in range(len(args))]
        vwe__pwqs = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        tzrn__wdtn = func.py_func.__code__.co_varnames
        emci__jtp = func.targetoptions

        def get_distribution(argname):
            if argname in emci__jtp.get('distributed', []
                ) or argname in emci__jtp.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        recq__dgufe = [get_distribution(argname) for argname in tzrn__wdtn[
            :len(args)]]
        vwe__pwqs = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    fkew__rwm = pickle.dumps(func.py_func)
    tjpwz__ltbvk.bcast(['exec', fkew__rwm, recq__dgufe, vwe__pwqs])
    rsfb__hdle = []
    for yzq__vqnc, etcza__gkkz in zip(args, recq__dgufe):
        if etcza__gkkz == 'scatter':
            rsfb__hdle.append(bodo.scatterv(yzq__vqnc))
        elif etcza__gkkz == 'bcast':
            tjpwz__ltbvk.bcast(yzq__vqnc)
            rsfb__hdle.append(yzq__vqnc)
    mjnqh__pke = {}
    for argname, yzq__vqnc in kwargs.items():
        etcza__gkkz = vwe__pwqs[argname]
        if etcza__gkkz == 'scatter':
            mjnqh__pke[argname] = bodo.scatterv(yzq__vqnc)
        elif etcza__gkkz == 'bcast':
            tjpwz__ltbvk.bcast(yzq__vqnc)
            mjnqh__pke[argname] = yzq__vqnc
    mrqbi__qjvwg = []
    for nrqp__qsuw, wflm__nlvnb in list(func.py_func.__globals__.items()):
        if isinstance(wflm__nlvnb, MasterModeDispatcher):
            mrqbi__qjvwg.append((func.py_func.__globals__, nrqp__qsuw, func
                .py_func.__globals__[nrqp__qsuw]))
            func.py_func.__globals__[nrqp__qsuw] = wflm__nlvnb.dispatcher
    uro__ltwu = func(*rsfb__hdle, **mjnqh__pke)
    for fyh__ier, nrqp__qsuw, wflm__nlvnb in mrqbi__qjvwg:
        fyh__ier[nrqp__qsuw] = wflm__nlvnb
    if uro__ltwu is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        uro__ltwu = bodo.gatherv(uro__ltwu)
    return uro__ltwu


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
