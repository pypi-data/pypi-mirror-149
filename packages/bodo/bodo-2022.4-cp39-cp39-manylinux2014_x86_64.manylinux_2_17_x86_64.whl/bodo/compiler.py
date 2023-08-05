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
        lbkij__rpna = 'bodo' if distributed else 'bodo_seq'
        lbkij__rpna = (lbkij__rpna + '_inline' if inline_calls_pass else
            lbkij__rpna)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state,
            lbkij__rpna)
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
    for nys__djo, (xdvxf__ovfgv, fvw__dqnl) in enumerate(pm.passes):
        if xdvxf__ovfgv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(nys__djo, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for nys__djo, (xdvxf__ovfgv, fvw__dqnl) in enumerate(pm.passes):
        if xdvxf__ovfgv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[nys__djo] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for nys__djo, (xdvxf__ovfgv, fvw__dqnl) in enumerate(pm.passes):
        if xdvxf__ovfgv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(nys__djo)
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
    zcvn__tljgv = guard(get_definition, func_ir, rhs.func)
    if isinstance(zcvn__tljgv, (ir.Global, ir.FreeVar, ir.Const)):
        clc__eiia = zcvn__tljgv.value
    else:
        mdqjt__syete = guard(find_callname, func_ir, rhs)
        if not (mdqjt__syete and isinstance(mdqjt__syete[0], str) and
            isinstance(mdqjt__syete[1], str)):
            return
        func_name, func_mod = mdqjt__syete
        try:
            import importlib
            jfrvy__uls = importlib.import_module(func_mod)
            clc__eiia = getattr(jfrvy__uls, func_name)
        except:
            return
    if isinstance(clc__eiia, CPUDispatcher) and issubclass(clc__eiia.
        _compiler.pipeline_class, BodoCompiler
        ) and clc__eiia._compiler.pipeline_class != BodoCompilerUDF:
        clc__eiia._compiler.pipeline_class = BodoCompilerUDF
        clc__eiia.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for feos__ctiz in block.body:
                if is_call_assign(feos__ctiz):
                    _convert_bodo_dispatcher_to_udf(feos__ctiz.value, state
                        .func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        tpko__vjlp = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags)
        tpko__vjlp.run()
        return True


def _update_definitions(func_ir, node_list):
    iusx__oaoi = ir.Loc('', 0)
    lhhgo__ociyf = ir.Block(ir.Scope(None, iusx__oaoi), iusx__oaoi)
    lhhgo__ociyf.body = node_list
    build_definitions({(0): lhhgo__ociyf}, func_ir._definitions)


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
        grdk__jmab = 'overload_series_' + rhs.attr
        rlf__qmfey = getattr(bodo.hiframes.series_impl, grdk__jmab)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        grdk__jmab = 'overload_dataframe_' + rhs.attr
        rlf__qmfey = getattr(bodo.hiframes.dataframe_impl, grdk__jmab)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    xepm__dogt = rlf__qmfey(rhs_type)
    pwvxx__ginc = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc
        )
    rosm__omvil = compile_func_single_block(xepm__dogt, (rhs.value,), stmt.
        target, pwvxx__ginc)
    _update_definitions(func_ir, rosm__omvil)
    new_body += rosm__omvil
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
        njcs__xcycm = tuple(typemap[ofvi__tvi.name] for ofvi__tvi in rhs.args)
        lcfm__qlyr = {lbkij__rpna: typemap[ofvi__tvi.name] for lbkij__rpna,
            ofvi__tvi in dict(rhs.kws).items()}
        xepm__dogt = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*njcs__xcycm, **lcfm__qlyr)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        njcs__xcycm = tuple(typemap[ofvi__tvi.name] for ofvi__tvi in rhs.args)
        lcfm__qlyr = {lbkij__rpna: typemap[ofvi__tvi.name] for lbkij__rpna,
            ofvi__tvi in dict(rhs.kws).items()}
        xepm__dogt = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*njcs__xcycm, **lcfm__qlyr)
    else:
        return False
    eohx__xie = replace_func(pass_info, xepm__dogt, rhs.args, pysig=numba.
        core.utils.pysignature(xepm__dogt), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    fsd__lljuu, fvw__dqnl = inline_closure_call(func_ir, eohx__xie.glbls,
        block, len(new_body), eohx__xie.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=eohx__xie.arg_types, typemap=typemap,
        calltypes=calltypes, work_list=work_list)
    for yig__eymof in fsd__lljuu.values():
        yig__eymof.loc = rhs.loc
        update_locs(yig__eymof.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    lpsu__pvdw = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = lpsu__pvdw(func_ir, typemap)
    yfefy__gwjmx = func_ir.blocks
    work_list = list((nxur__ags, yfefy__gwjmx[nxur__ags]) for nxur__ags in
        reversed(yfefy__gwjmx.keys()))
    while work_list:
        dkhkr__vinn, block = work_list.pop()
        new_body = []
        qbi__gzfh = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                mdqjt__syete = guard(find_callname, func_ir, rhs, typemap)
                if mdqjt__syete is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = mdqjt__syete
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    qbi__gzfh = True
                    break
            new_body.append(stmt)
        if not qbi__gzfh:
            yfefy__gwjmx[dkhkr__vinn].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        nazh__mabvl = DistributedPass(state.func_ir, state.typingctx, state
            .targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = nazh__mabvl.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        tgh__smski = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        tgh__smski.run()
        tgh__smski.run()
        tgh__smski.run()
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        wmw__bxh = 0
        tim__hngd = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            wmw__bxh = int(os.environ[tim__hngd])
        except:
            pass
        if wmw__bxh > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(wmw__bxh, state.
                metadata)
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
        pwvxx__ginc = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, pwvxx__ginc)
        for block in state.func_ir.blocks.values():
            new_body = []
            for feos__ctiz in block.body:
                if type(feos__ctiz) in distributed_run_extensions:
                    rtio__egb = distributed_run_extensions[type(feos__ctiz)]
                    xyzpq__voqus = rtio__egb(feos__ctiz, None, state.
                        typemap, state.calltypes, state.typingctx, state.
                        targetctx)
                    new_body += xyzpq__voqus
                elif is_call_assign(feos__ctiz):
                    rhs = feos__ctiz.value
                    mdqjt__syete = guard(find_callname, state.func_ir, rhs)
                    if mdqjt__syete == ('gatherv', 'bodo') or mdqjt__syete == (
                        'allgatherv', 'bodo'):
                        otncz__owcuv = state.typemap[feos__ctiz.target.name]
                        uzwj__arl = state.typemap[rhs.args[0].name]
                        if isinstance(uzwj__arl, types.Array) and isinstance(
                            otncz__owcuv, types.Array):
                            mxze__rpk = uzwj__arl.copy(readonly=False)
                            sjyk__xehbp = otncz__owcuv.copy(readonly=False)
                            if mxze__rpk == sjyk__xehbp:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), feos__ctiz.target, pwvxx__ginc)
                                continue
                        if (otncz__owcuv != uzwj__arl and 
                            to_str_arr_if_dict_array(otncz__owcuv) ==
                            to_str_arr_if_dict_array(uzwj__arl)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), feos__ctiz.target,
                                pwvxx__ginc, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            feos__ctiz.value = rhs.args[0]
                    new_body.append(feos__ctiz)
                else:
                    new_body.append(feos__ctiz)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        qulm__lcr = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return qulm__lcr.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    cgpnn__gia = set()
    while work_list:
        dkhkr__vinn, block = work_list.pop()
        cgpnn__gia.add(dkhkr__vinn)
        for i, kxr__rhg in enumerate(block.body):
            if isinstance(kxr__rhg, ir.Assign):
                fcb__jyh = kxr__rhg.value
                if isinstance(fcb__jyh, ir.Expr) and fcb__jyh.op == 'call':
                    zcvn__tljgv = guard(get_definition, func_ir, fcb__jyh.func)
                    if isinstance(zcvn__tljgv, (ir.Global, ir.FreeVar)
                        ) and isinstance(zcvn__tljgv.value, CPUDispatcher
                        ) and issubclass(zcvn__tljgv.value._compiler.
                        pipeline_class, BodoCompiler):
                        jjuh__tdyq = zcvn__tljgv.value.py_func
                        arg_types = None
                        if typingctx:
                            bkliw__xwyg = dict(fcb__jyh.kws)
                            likvl__rtypq = tuple(typemap[ofvi__tvi.name] for
                                ofvi__tvi in fcb__jyh.args)
                            awczq__zfwb = {fkfl__css: typemap[ofvi__tvi.
                                name] for fkfl__css, ofvi__tvi in
                                bkliw__xwyg.items()}
                            fvw__dqnl, arg_types = (zcvn__tljgv.value.
                                fold_argument_types(likvl__rtypq, awczq__zfwb))
                        fvw__dqnl, grvcs__ggts = inline_closure_call(func_ir,
                            jjuh__tdyq.__globals__, block, i, jjuh__tdyq,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((grvcs__ggts[fkfl__css].name,
                            ofvi__tvi) for fkfl__css, ofvi__tvi in
                            zcvn__tljgv.value.locals.items() if fkfl__css in
                            grvcs__ggts)
                        break
    return cgpnn__gia


def udf_jit(signature_or_function=None, **options):
    gtxot__qbj = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=gtxot__qbj,
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
    for nys__djo, (xdvxf__ovfgv, fvw__dqnl) in enumerate(pm.passes):
        if xdvxf__ovfgv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:nys__djo + 1]
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
    xorl__azx = None
    oxbp__nlopa = None
    _locals = {}
    via__iiysn = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(via__iiysn, arg_types,
        kw_types)
    matye__jov = numba.core.compiler.Flags()
    rpq__stwhv = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    fljr__reayb = {'nopython': True, 'boundscheck': False, 'parallel':
        rpq__stwhv}
    numba.core.registry.cpu_target.options.parse_as_flags(matye__jov,
        fljr__reayb)
    gtcw__nuxwl = TyperCompiler(typingctx, targetctx, xorl__azx, args,
        oxbp__nlopa, matye__jov, _locals)
    return gtcw__nuxwl.compile_extra(func)
