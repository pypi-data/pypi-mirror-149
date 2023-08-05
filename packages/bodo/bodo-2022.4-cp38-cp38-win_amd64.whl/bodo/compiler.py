"""
Defines Bodo's compiler pipeline.
"""
import os
import warnings
from collections import namedtuple
import numba
from numba.core import ir, ir_utils, types
from numba.core.compiler import DefaultPassBuilder
from numba.core.compiler_machinery import AnalysisPass, FunctionPass, register_pass
from numba.core.inline_closurecall import inline_closure_call
from numba.core.ir_utils import build_definitions, find_callname, get_definition, guard
from numba.core.registry import CPUDispatcher
from numba.core.typed_passes import DumpParforDiagnostics, InlineOverloads, IRLegalization, NopythonTypeInference, ParforPass, PreParforPass
from numba.core.untyped_passes import MakeFunctionToJitFunction, ReconstructSSA, WithLifting
import bodo
import bodo.hiframes.dataframe_indexing
import bodo.hiframes.datetime_datetime_ext
import bodo.hiframes.datetime_timedelta_ext
import bodo.io
import bodo.libs
import bodo.libs.array_kernels
import bodo.libs.int_arr_ext
import bodo.libs.re_ext
import bodo.libs.spark_extra
import bodo.transforms
import bodo.transforms.series_pass
import bodo.transforms.untyped_pass
import bodo.utils
import bodo.utils.table_utils
import bodo.utils.typing
from bodo.transforms.series_pass import SeriesPass
from bodo.transforms.table_column_del_pass import TableColumnDelPass
from bodo.transforms.typing_pass import BodoTypeInference
from bodo.transforms.untyped_pass import UntypedPass
from bodo.utils.utils import is_assign, is_call_assign, is_expr
numba.core.config.DISABLE_PERFORMANCE_WARNINGS = 1
from numba.core.errors import NumbaExperimentalFeatureWarning, NumbaPendingDeprecationWarning
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
inline_all_calls = False


class BodoCompiler(numba.core.compiler.CompilerBase):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=True,
            inline_calls_pass=inline_all_calls)

    def _create_bodo_pipeline(self, distributed=True, inline_calls_pass=
        False, udf_pipeline=False):
        hepfa__fecq = 'bodo' if distributed else 'bodo_seq'
        hepfa__fecq = (hepfa__fecq + '_inline' if inline_calls_pass else
            hepfa__fecq)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state,
            hepfa__fecq)
        if inline_calls_pass:
            pm.add_pass_after(InlinePass, WithLifting)
        if udf_pipeline:
            pm.add_pass_after(ConvertCallsUDFPass, WithLifting)
        add_pass_before(pm, BodoUntypedPass, ReconstructSSA)
        replace_pass(pm, BodoTypeInference, NopythonTypeInference)
        remove_pass(pm, MakeFunctionToJitFunction)
        add_pass_before(pm, BodoSeriesPass, PreParforPass)
        if distributed:
            pm.add_pass_after(BodoDistributedPass, ParforPass)
        else:
            pm.add_pass_after(LowerParforSeq, ParforPass)
            pm.add_pass_after(LowerBodoIRExtSeq, LowerParforSeq)
        add_pass_before(pm, BodoTableColumnDelPass, IRLegalization)
        pm.add_pass_after(BodoDumpDistDiagnosticsPass, DumpParforDiagnostics)
        pm.finalize()
        return [pm]


def add_pass_before(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for aqzza__gab, (yarw__eafqq, ibz__suwx) in enumerate(pm.passes):
        if yarw__eafqq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(aqzza__gab, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for aqzza__gab, (yarw__eafqq, ibz__suwx) in enumerate(pm.passes):
        if yarw__eafqq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[aqzza__gab] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for aqzza__gab, (yarw__eafqq, ibz__suwx) in enumerate(pm.passes):
        if yarw__eafqq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(aqzza__gab)
    pm._finalized = False


@register_pass(mutates_CFG=True, analysis_only=False)
class InlinePass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        inline_calls(state.func_ir, state.locals)
        state.func_ir.blocks = ir_utils.simplify_CFG(state.func_ir.blocks)
        return True


def _convert_bodo_dispatcher_to_udf(rhs, func_ir):
    ofx__lactg = guard(get_definition, func_ir, rhs.func)
    if isinstance(ofx__lactg, (ir.Global, ir.FreeVar, ir.Const)):
        klc__qnq = ofx__lactg.value
    else:
        yslmf__tcb = guard(find_callname, func_ir, rhs)
        if not (yslmf__tcb and isinstance(yslmf__tcb[0], str) and
            isinstance(yslmf__tcb[1], str)):
            return
        func_name, func_mod = yslmf__tcb
        try:
            import importlib
            jfe__lpdqa = importlib.import_module(func_mod)
            klc__qnq = getattr(jfe__lpdqa, func_name)
        except:
            return
    if isinstance(klc__qnq, CPUDispatcher) and issubclass(klc__qnq.
        _compiler.pipeline_class, BodoCompiler
        ) and klc__qnq._compiler.pipeline_class != BodoCompilerUDF:
        klc__qnq._compiler.pipeline_class = BodoCompilerUDF
        klc__qnq.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for hbxz__zotn in block.body:
                if is_call_assign(hbxz__zotn):
                    _convert_bodo_dispatcher_to_udf(hbxz__zotn.value, state
                        .func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        pkt__bjnw = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags)
        pkt__bjnw.run()
        return True


def _update_definitions(func_ir, node_list):
    nsbdr__ktf = ir.Loc('', 0)
    dqch__vhk = ir.Block(ir.Scope(None, nsbdr__ktf), nsbdr__ktf)
    dqch__vhk.body = node_list
    build_definitions({(0): dqch__vhk}, func_ir._definitions)


_series_inline_attrs = {'values', 'shape', 'size', 'empty', 'name', 'index',
    'dtype'}
_series_no_inline_methods = {'to_list', 'tolist', 'rolling', 'to_csv',
    'count', 'fillna', 'to_dict', 'map', 'apply', 'pipe', 'combine',
    'bfill', 'ffill', 'pad', 'backfill', 'mask', 'where'}
_series_method_alias = {'isnull': 'isna', 'product': 'prod', 'kurtosis':
    'kurt', 'is_monotonic': 'is_monotonic_increasing', 'notnull': 'notna'}
_dataframe_no_inline_methods = {'apply', 'itertuples', 'pipe', 'to_parquet',
    'to_sql', 'to_csv', 'to_json', 'assign', 'to_string', 'query',
    'rolling', 'mask', 'where'}
TypingInfo = namedtuple('TypingInfo', ['typingctx', 'targetctx', 'typemap',
    'calltypes', 'curr_loc'])


def _inline_bodo_getattr(stmt, rhs, rhs_type, new_body, func_ir, typingctx,
    targetctx, typemap, calltypes):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import compile_func_single_block
    if isinstance(rhs_type, SeriesType) and rhs.attr in _series_inline_attrs:
        ykcg__wsi = 'overload_series_' + rhs.attr
        ijy__idq = getattr(bodo.hiframes.series_impl, ykcg__wsi)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        ykcg__wsi = 'overload_dataframe_' + rhs.attr
        ijy__idq = getattr(bodo.hiframes.dataframe_impl, ykcg__wsi)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    lbi__pgc = ijy__idq(rhs_type)
    uegbk__gufxm = TypingInfo(typingctx, targetctx, typemap, calltypes,
        stmt.loc)
    ljux__spkkp = compile_func_single_block(lbi__pgc, (rhs.value,), stmt.
        target, uegbk__gufxm)
    _update_definitions(func_ir, ljux__spkkp)
    new_body += ljux__spkkp
    return True


def _inline_bodo_call(rhs, i, func_mod, func_name, pass_info, new_body,
    block, typingctx, targetctx, calltypes, work_list):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import replace_func, update_locs
    func_ir = pass_info.func_ir
    typemap = pass_info.typemap
    if isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        SeriesType) and func_name not in _series_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        if (func_name in bodo.hiframes.series_impl.explicit_binop_funcs or 
            func_name.startswith('r') and func_name[1:] in bodo.hiframes.
            series_impl.explicit_binop_funcs):
            return False
        rhs.args.insert(0, func_mod)
        gjhh__urwc = tuple(typemap[mopz__opnrh.name] for mopz__opnrh in rhs
            .args)
        ytdyi__qsu = {hepfa__fecq: typemap[mopz__opnrh.name] for 
            hepfa__fecq, mopz__opnrh in dict(rhs.kws).items()}
        lbi__pgc = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*gjhh__urwc, **ytdyi__qsu)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        gjhh__urwc = tuple(typemap[mopz__opnrh.name] for mopz__opnrh in rhs
            .args)
        ytdyi__qsu = {hepfa__fecq: typemap[mopz__opnrh.name] for 
            hepfa__fecq, mopz__opnrh in dict(rhs.kws).items()}
        lbi__pgc = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*gjhh__urwc, **ytdyi__qsu)
    else:
        return False
    ksvm__vbjq = replace_func(pass_info, lbi__pgc, rhs.args, pysig=numba.
        core.utils.pysignature(lbi__pgc), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    dyf__lvgqt, ibz__suwx = inline_closure_call(func_ir, ksvm__vbjq.glbls,
        block, len(new_body), ksvm__vbjq.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=ksvm__vbjq.arg_types, typemap=typemap,
        calltypes=calltypes, work_list=work_list)
    for exnj__wik in dyf__lvgqt.values():
        exnj__wik.loc = rhs.loc
        update_locs(exnj__wik.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    zcl__ryxql = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = zcl__ryxql(func_ir, typemap)
    wuamh__fne = func_ir.blocks
    work_list = list((hzvb__zvkjl, wuamh__fne[hzvb__zvkjl]) for hzvb__zvkjl in
        reversed(wuamh__fne.keys()))
    while work_list:
        muwn__mrzim, block = work_list.pop()
        new_body = []
        buzhk__yuq = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                yslmf__tcb = guard(find_callname, func_ir, rhs, typemap)
                if yslmf__tcb is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = yslmf__tcb
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    buzhk__yuq = True
                    break
            new_body.append(stmt)
        if not buzhk__yuq:
            wuamh__fne[muwn__mrzim].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        fqgpx__gpjag = DistributedPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes, state.
            return_type, state.metadata, state.flags)
        state.return_type = fqgpx__gpjag.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        dvey__rba = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        dvey__rba.run()
        dvey__rba.run()
        dvey__rba.run()
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        odjs__ffc = 0
        qtcoc__yds = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            odjs__ffc = int(os.environ[qtcoc__yds])
        except:
            pass
        if odjs__ffc > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(odjs__ffc, state
                .metadata)
        return True


class BodoCompilerSeq(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False,
            inline_calls_pass=inline_all_calls)


class BodoCompilerUDF(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False, udf_pipeline=True)


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerParforSeq(FunctionPass):
    _name = 'bodo_lower_parfor_seq_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bodo.transforms.distributed_pass.lower_parfor_sequential(state.
            typingctx, state.func_ir, state.typemap, state.calltypes, state
            .metadata)
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerBodoIRExtSeq(FunctionPass):
    _name = 'bodo_lower_ir_ext_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        from bodo.transforms.distributed_pass import distributed_run_extensions
        from bodo.transforms.table_column_del_pass import remove_dead_table_columns
        from bodo.utils.transform import compile_func_single_block
        from bodo.utils.typing import decode_if_dict_array, to_str_arr_if_dict_array
        state.func_ir._definitions = build_definitions(state.func_ir.blocks)
        uegbk__gufxm = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, uegbk__gufxm)
        for block in state.func_ir.blocks.values():
            new_body = []
            for hbxz__zotn in block.body:
                if type(hbxz__zotn) in distributed_run_extensions:
                    isw__dlj = distributed_run_extensions[type(hbxz__zotn)]
                    gwn__dvt = isw__dlj(hbxz__zotn, None, state.typemap,
                        state.calltypes, state.typingctx, state.targetctx)
                    new_body += gwn__dvt
                elif is_call_assign(hbxz__zotn):
                    rhs = hbxz__zotn.value
                    yslmf__tcb = guard(find_callname, state.func_ir, rhs)
                    if yslmf__tcb == ('gatherv', 'bodo') or yslmf__tcb == (
                        'allgatherv', 'bodo'):
                        lzlg__biqah = state.typemap[hbxz__zotn.target.name]
                        til__cob = state.typemap[rhs.args[0].name]
                        if isinstance(til__cob, types.Array) and isinstance(
                            lzlg__biqah, types.Array):
                            jirj__pmac = til__cob.copy(readonly=False)
                            bjrv__krqpn = lzlg__biqah.copy(readonly=False)
                            if jirj__pmac == bjrv__krqpn:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), hbxz__zotn.target, uegbk__gufxm)
                                continue
                        if (lzlg__biqah != til__cob and 
                            to_str_arr_if_dict_array(lzlg__biqah) ==
                            to_str_arr_if_dict_array(til__cob)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), hbxz__zotn.target,
                                uegbk__gufxm, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            hbxz__zotn.value = rhs.args[0]
                    new_body.append(hbxz__zotn)
                else:
                    new_body.append(hbxz__zotn)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bxq__wsc = TableColumnDelPass(state.func_ir, state.typingctx, state
            .targetctx, state.typemap, state.calltypes)
        return bxq__wsc.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    ovn__qiq = set()
    while work_list:
        muwn__mrzim, block = work_list.pop()
        ovn__qiq.add(muwn__mrzim)
        for i, shbd__ztdvw in enumerate(block.body):
            if isinstance(shbd__ztdvw, ir.Assign):
                oxjvo__igy = shbd__ztdvw.value
                if isinstance(oxjvo__igy, ir.Expr) and oxjvo__igy.op == 'call':
                    ofx__lactg = guard(get_definition, func_ir, oxjvo__igy.func
                        )
                    if isinstance(ofx__lactg, (ir.Global, ir.FreeVar)
                        ) and isinstance(ofx__lactg.value, CPUDispatcher
                        ) and issubclass(ofx__lactg.value._compiler.
                        pipeline_class, BodoCompiler):
                        cpbsp__jowvy = ofx__lactg.value.py_func
                        arg_types = None
                        if typingctx:
                            gbfyw__zxe = dict(oxjvo__igy.kws)
                            pgiyo__kjnp = tuple(typemap[mopz__opnrh.name] for
                                mopz__opnrh in oxjvo__igy.args)
                            oiuz__rus = {tlr__ynv: typemap[mopz__opnrh.name
                                ] for tlr__ynv, mopz__opnrh in gbfyw__zxe.
                                items()}
                            ibz__suwx, arg_types = (ofx__lactg.value.
                                fold_argument_types(pgiyo__kjnp, oiuz__rus))
                        ibz__suwx, wesio__sfas = inline_closure_call(func_ir,
                            cpbsp__jowvy.__globals__, block, i,
                            cpbsp__jowvy, typingctx=typingctx, targetctx=
                            targetctx, arg_typs=arg_types, typemap=typemap,
                            calltypes=calltypes, work_list=work_list)
                        _locals.update((wesio__sfas[tlr__ynv].name,
                            mopz__opnrh) for tlr__ynv, mopz__opnrh in
                            ofx__lactg.value.locals.items() if tlr__ynv in
                            wesio__sfas)
                        break
    return ovn__qiq


def udf_jit(signature_or_function=None, **options):
    jbih__wydz = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=jbih__wydz,
        pipeline_class=bodo.compiler.BodoCompilerUDF, **options)


def is_udf_call(func_type):
    return isinstance(func_type, numba.core.types.Dispatcher
        ) and func_type.dispatcher._compiler.pipeline_class == BodoCompilerUDF


def is_user_dispatcher(func_type):
    return isinstance(func_type, numba.core.types.functions.ObjModeDispatcher
        ) or isinstance(func_type, numba.core.types.Dispatcher) and issubclass(
        func_type.dispatcher._compiler.pipeline_class, BodoCompiler)


@register_pass(mutates_CFG=False, analysis_only=True)
class DummyCR(FunctionPass):
    _name = 'bodo_dummy_cr'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        state.cr = (state.func_ir, state.typemap, state.calltypes, state.
            return_type)
        return True


def remove_passes_after(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for aqzza__gab, (yarw__eafqq, ibz__suwx) in enumerate(pm.passes):
        if yarw__eafqq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:aqzza__gab + 1]
    pm._finalized = False


class TyperCompiler(BodoCompiler):

    def define_pipelines(self):
        [pm] = self._create_bodo_pipeline()
        remove_passes_after(pm, InlineOverloads)
        pm.add_pass_after(DummyCR, InlineOverloads)
        pm.finalize()
        return [pm]


def get_func_type_info(func, arg_types, kw_types):
    typingctx = numba.core.registry.cpu_target.typing_context
    targetctx = numba.core.registry.cpu_target.target_context
    qjhxp__copx = None
    zkjaj__jitn = None
    _locals = {}
    preyx__mxdv = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(preyx__mxdv, arg_types,
        kw_types)
    awwck__tvm = numba.core.compiler.Flags()
    zkih__lemo = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    gzo__udv = {'nopython': True, 'boundscheck': False, 'parallel': zkih__lemo}
    numba.core.registry.cpu_target.options.parse_as_flags(awwck__tvm, gzo__udv)
    hjq__keh = TyperCompiler(typingctx, targetctx, qjhxp__copx, args,
        zkjaj__jitn, awwck__tvm, _locals)
    return hjq__keh.compile_extra(func)
