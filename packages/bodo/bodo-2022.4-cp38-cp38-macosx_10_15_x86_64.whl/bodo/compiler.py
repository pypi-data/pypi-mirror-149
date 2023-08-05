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
        gzhn__ynix = 'bodo' if distributed else 'bodo_seq'
        gzhn__ynix = (gzhn__ynix + '_inline' if inline_calls_pass else
            gzhn__ynix)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, gzhn__ynix
            )
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
    for ftev__kac, (aft__rsq, zlr__sdy) in enumerate(pm.passes):
        if aft__rsq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(ftev__kac, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for ftev__kac, (aft__rsq, zlr__sdy) in enumerate(pm.passes):
        if aft__rsq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[ftev__kac] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for ftev__kac, (aft__rsq, zlr__sdy) in enumerate(pm.passes):
        if aft__rsq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(ftev__kac)
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
    gwai__bos = guard(get_definition, func_ir, rhs.func)
    if isinstance(gwai__bos, (ir.Global, ir.FreeVar, ir.Const)):
        bjx__ngjwm = gwai__bos.value
    else:
        cbbmf__hiq = guard(find_callname, func_ir, rhs)
        if not (cbbmf__hiq and isinstance(cbbmf__hiq[0], str) and
            isinstance(cbbmf__hiq[1], str)):
            return
        func_name, func_mod = cbbmf__hiq
        try:
            import importlib
            dck__gmzpf = importlib.import_module(func_mod)
            bjx__ngjwm = getattr(dck__gmzpf, func_name)
        except:
            return
    if isinstance(bjx__ngjwm, CPUDispatcher) and issubclass(bjx__ngjwm.
        _compiler.pipeline_class, BodoCompiler
        ) and bjx__ngjwm._compiler.pipeline_class != BodoCompilerUDF:
        bjx__ngjwm._compiler.pipeline_class = BodoCompilerUDF
        bjx__ngjwm.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for yejf__ruo in block.body:
                if is_call_assign(yejf__ruo):
                    _convert_bodo_dispatcher_to_udf(yejf__ruo.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        nwh__com = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags)
        nwh__com.run()
        return True


def _update_definitions(func_ir, node_list):
    mam__bctjk = ir.Loc('', 0)
    dupbh__jdwja = ir.Block(ir.Scope(None, mam__bctjk), mam__bctjk)
    dupbh__jdwja.body = node_list
    build_definitions({(0): dupbh__jdwja}, func_ir._definitions)


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
        vot__ewiv = 'overload_series_' + rhs.attr
        rumg__mlkkb = getattr(bodo.hiframes.series_impl, vot__ewiv)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        vot__ewiv = 'overload_dataframe_' + rhs.attr
        rumg__mlkkb = getattr(bodo.hiframes.dataframe_impl, vot__ewiv)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    zzxq__jkn = rumg__mlkkb(rhs_type)
    ztvlu__xjx = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    kqvpy__syyyn = compile_func_single_block(zzxq__jkn, (rhs.value,), stmt.
        target, ztvlu__xjx)
    _update_definitions(func_ir, kqvpy__syyyn)
    new_body += kqvpy__syyyn
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
        hpfoe__fnc = tuple(typemap[lgfdm__xqh.name] for lgfdm__xqh in rhs.args)
        kzc__izc = {gzhn__ynix: typemap[lgfdm__xqh.name] for gzhn__ynix,
            lgfdm__xqh in dict(rhs.kws).items()}
        zzxq__jkn = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*hpfoe__fnc, **kzc__izc)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        hpfoe__fnc = tuple(typemap[lgfdm__xqh.name] for lgfdm__xqh in rhs.args)
        kzc__izc = {gzhn__ynix: typemap[lgfdm__xqh.name] for gzhn__ynix,
            lgfdm__xqh in dict(rhs.kws).items()}
        zzxq__jkn = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*hpfoe__fnc, **kzc__izc)
    else:
        return False
    ngybv__xotyd = replace_func(pass_info, zzxq__jkn, rhs.args, pysig=numba
        .core.utils.pysignature(zzxq__jkn), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    xhaz__idgd, zlr__sdy = inline_closure_call(func_ir, ngybv__xotyd.glbls,
        block, len(new_body), ngybv__xotyd.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=ngybv__xotyd.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for jhcr__emkw in xhaz__idgd.values():
        jhcr__emkw.loc = rhs.loc
        update_locs(jhcr__emkw.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    mzun__qyx = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = mzun__qyx(func_ir, typemap)
    etwx__lhfl = func_ir.blocks
    work_list = list((cnb__frog, etwx__lhfl[cnb__frog]) for cnb__frog in
        reversed(etwx__lhfl.keys()))
    while work_list:
        gzjtz__avwb, block = work_list.pop()
        new_body = []
        ibxrz__stga = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                cbbmf__hiq = guard(find_callname, func_ir, rhs, typemap)
                if cbbmf__hiq is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = cbbmf__hiq
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    ibxrz__stga = True
                    break
            new_body.append(stmt)
        if not ibxrz__stga:
            etwx__lhfl[gzjtz__avwb].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        ado__wyc = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = ado__wyc.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        yth__ehgv = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        yth__ehgv.run()
        yth__ehgv.run()
        yth__ehgv.run()
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        snps__dpz = 0
        pzfg__yhzy = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            snps__dpz = int(os.environ[pzfg__yhzy])
        except:
            pass
        if snps__dpz > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(snps__dpz, state
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
        ztvlu__xjx = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, ztvlu__xjx)
        for block in state.func_ir.blocks.values():
            new_body = []
            for yejf__ruo in block.body:
                if type(yejf__ruo) in distributed_run_extensions:
                    fnwbb__erpxi = distributed_run_extensions[type(yejf__ruo)]
                    xapr__vqaf = fnwbb__erpxi(yejf__ruo, None, state.
                        typemap, state.calltypes, state.typingctx, state.
                        targetctx)
                    new_body += xapr__vqaf
                elif is_call_assign(yejf__ruo):
                    rhs = yejf__ruo.value
                    cbbmf__hiq = guard(find_callname, state.func_ir, rhs)
                    if cbbmf__hiq == ('gatherv', 'bodo') or cbbmf__hiq == (
                        'allgatherv', 'bodo'):
                        iwx__vbp = state.typemap[yejf__ruo.target.name]
                        amcnx__rjye = state.typemap[rhs.args[0].name]
                        if isinstance(amcnx__rjye, types.Array) and isinstance(
                            iwx__vbp, types.Array):
                            lgdn__fwn = amcnx__rjye.copy(readonly=False)
                            wzxol__yrq = iwx__vbp.copy(readonly=False)
                            if lgdn__fwn == wzxol__yrq:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), yejf__ruo.target, ztvlu__xjx)
                                continue
                        if (iwx__vbp != amcnx__rjye and 
                            to_str_arr_if_dict_array(iwx__vbp) ==
                            to_str_arr_if_dict_array(amcnx__rjye)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), yejf__ruo.target,
                                ztvlu__xjx, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            yejf__ruo.value = rhs.args[0]
                    new_body.append(yejf__ruo)
                else:
                    new_body.append(yejf__ruo)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        fep__jnvuv = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return fep__jnvuv.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    ojyx__ivbap = set()
    while work_list:
        gzjtz__avwb, block = work_list.pop()
        ojyx__ivbap.add(gzjtz__avwb)
        for i, mzxa__mef in enumerate(block.body):
            if isinstance(mzxa__mef, ir.Assign):
                fjfxc__nhf = mzxa__mef.value
                if isinstance(fjfxc__nhf, ir.Expr) and fjfxc__nhf.op == 'call':
                    gwai__bos = guard(get_definition, func_ir, fjfxc__nhf.func)
                    if isinstance(gwai__bos, (ir.Global, ir.FreeVar)
                        ) and isinstance(gwai__bos.value, CPUDispatcher
                        ) and issubclass(gwai__bos.value._compiler.
                        pipeline_class, BodoCompiler):
                        nfy__uwuuu = gwai__bos.value.py_func
                        arg_types = None
                        if typingctx:
                            espw__xveb = dict(fjfxc__nhf.kws)
                            vup__uwc = tuple(typemap[lgfdm__xqh.name] for
                                lgfdm__xqh in fjfxc__nhf.args)
                            zxzov__kyg = {bmqzy__xcq: typemap[lgfdm__xqh.
                                name] for bmqzy__xcq, lgfdm__xqh in
                                espw__xveb.items()}
                            zlr__sdy, arg_types = (gwai__bos.value.
                                fold_argument_types(vup__uwc, zxzov__kyg))
                        zlr__sdy, uphd__omvj = inline_closure_call(func_ir,
                            nfy__uwuuu.__globals__, block, i, nfy__uwuuu,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((uphd__omvj[bmqzy__xcq].name,
                            lgfdm__xqh) for bmqzy__xcq, lgfdm__xqh in
                            gwai__bos.value.locals.items() if bmqzy__xcq in
                            uphd__omvj)
                        break
    return ojyx__ivbap


def udf_jit(signature_or_function=None, **options):
    nqp__lli = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=nqp__lli,
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
    for ftev__kac, (aft__rsq, zlr__sdy) in enumerate(pm.passes):
        if aft__rsq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:ftev__kac + 1]
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
    cjncu__wsc = None
    auzg__gpvm = None
    _locals = {}
    teqvs__wiat = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(teqvs__wiat, arg_types,
        kw_types)
    xnqct__ghrtf = numba.core.compiler.Flags()
    txnc__bqqr = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    gydmb__rkwa = {'nopython': True, 'boundscheck': False, 'parallel':
        txnc__bqqr}
    numba.core.registry.cpu_target.options.parse_as_flags(xnqct__ghrtf,
        gydmb__rkwa)
    oqi__vwtsd = TyperCompiler(typingctx, targetctx, cjncu__wsc, args,
        auzg__gpvm, xnqct__ghrtf, _locals)
    return oqi__vwtsd.compile_extra(func)
