"""
Numba monkey patches to fix issues related to Bodo. Should be imported before any
other module in bodo package.
"""
import copy
import functools
import hashlib
import inspect
import itertools
import operator
import os
import re
import sys
import textwrap
import traceback
import types as pytypes
import warnings
from collections import OrderedDict
from collections.abc import Sequence
from contextlib import ExitStack
import numba
import numba.core.boxing
import numba.core.inline_closurecall
import numba.core.typing.listdecl
import numba.np.linalg
from numba.core import analysis, cgutils, errors, ir, ir_utils, types
from numba.core.compiler import Compiler
from numba.core.errors import ForceLiteralArg, LiteralTypingError, TypingError
from numba.core.ir_utils import GuardException, _create_function_from_code_obj, analysis, build_definitions, find_callname, guard, has_no_side_effect, mk_unique_var, remove_dead_extensions, replace_vars_inner, require, visit_vars_extensions, visit_vars_inner
from numba.core.types import literal
from numba.core.types.functions import _bt_as_lines, _ResolutionFailures, _termcolor, _unlit_non_poison
from numba.core.typing.templates import AbstractTemplate, Signature, _EmptyImplementationEntry, _inline_info, _OverloadAttributeTemplate, infer_global, signature
from numba.core.typing.typeof import Purpose, typeof
from numba.experimental.jitclass import base as jitclass_base
from numba.experimental.jitclass import decorators as jitclass_decorators
from numba.extending import NativeValue, lower_builtin, typeof_impl
from numba.parfors.parfor import get_expr_args
from bodo.utils.python_310_bytecode_pass import Bodo310ByteCodePass, peep_hole_call_function_ex_to_call_function_kw, peep_hole_fuse_dict_add_updates
from bodo.utils.typing import BodoError, get_overload_const_str, is_overload_constant_str, raise_bodo_error
_check_numba_change = False
numba.core.typing.templates._IntrinsicTemplate.prefer_literal = True


def run_frontend(func, inline_closures=False, emit_dels=False):
    from numba.core.utils import PYVERSION
    yibrx__qume = numba.core.bytecode.FunctionIdentity.from_function(func)
    yvmo__xipzj = numba.core.interpreter.Interpreter(yibrx__qume)
    qkmbn__axj = numba.core.bytecode.ByteCode(func_id=yibrx__qume)
    func_ir = yvmo__xipzj.interpret(qkmbn__axj)
    if PYVERSION == (3, 10):
        func_ir = peep_hole_call_function_ex_to_call_function_kw(func_ir)
        func_ir = peep_hole_fuse_dict_add_updates(func_ir)
    if inline_closures:
        from numba.core.inline_closurecall import InlineClosureCallPass


        class DummyPipeline:

            def __init__(self, f_ir):
                self.state = numba.core.compiler.StateDict()
                self.state.typingctx = None
                self.state.targetctx = None
                self.state.args = None
                self.state.func_ir = f_ir
                self.state.typemap = None
                self.state.return_type = None
                self.state.calltypes = None
        numba.core.rewrites.rewrite_registry.apply('before-inference',
            DummyPipeline(func_ir).state)
        ajf__mgy = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        ajf__mgy.run()
    tzwdh__ggsb = numba.core.postproc.PostProcessor(func_ir)
    tzwdh__ggsb.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, bxcfn__ydyq in visit_vars_extensions.items():
        if isinstance(stmt, t):
            bxcfn__ydyq(stmt, callback, cbdata)
            return
    if isinstance(stmt, ir.Assign):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Arg):
        stmt.name = visit_vars_inner(stmt.name, callback, cbdata)
    elif isinstance(stmt, ir.Return):
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Raise):
        stmt.exception = visit_vars_inner(stmt.exception, callback, cbdata)
    elif isinstance(stmt, ir.Branch):
        stmt.cond = visit_vars_inner(stmt.cond, callback, cbdata)
    elif isinstance(stmt, ir.Jump):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
    elif isinstance(stmt, ir.Del):
        var = ir.Var(None, stmt.value, stmt.loc)
        var = visit_vars_inner(var, callback, cbdata)
        stmt.value = var.name
    elif isinstance(stmt, ir.DelAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
    elif isinstance(stmt, ir.SetAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.DelItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
    elif isinstance(stmt, ir.StaticSetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index_var = visit_vars_inner(stmt.index_var, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.SetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Print):
        stmt.args = [visit_vars_inner(x, callback, cbdata) for x in stmt.args]
        stmt.vararg = visit_vars_inner(stmt.vararg, callback, cbdata)
    else:
        pass
    return


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.visit_vars_stmt)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '52b7b645ba65c35f3cf564f936e113261db16a2dff1e80fbee2459af58844117':
        warnings.warn('numba.core.ir_utils.visit_vars_stmt has changed')
numba.core.ir_utils.visit_vars_stmt = visit_vars_stmt
old_run_pass = numba.core.typed_passes.InlineOverloads.run_pass


def InlineOverloads_run_pass(self, state):
    import bodo
    bodo.compiler.bodo_overload_inline_pass(state.func_ir, state.typingctx,
        state.targetctx, state.typemap, state.calltypes)
    return old_run_pass(self, state)


numba.core.typed_passes.InlineOverloads.run_pass = InlineOverloads_run_pass
from numba.core.ir_utils import _add_alias, alias_analysis_extensions, alias_func_extensions
_immutable_type_class = (types.Number, types.scalars._NPDatetimeBase, types
    .iterators.RangeType, types.UnicodeType)


def is_immutable_type(var, typemap):
    if typemap is None or var not in typemap:
        return False
    typ = typemap[var]
    if isinstance(typ, _immutable_type_class):
        return True
    if isinstance(typ, types.BaseTuple) and all(isinstance(t,
        _immutable_type_class) for t in typ.types):
        return True
    return False


def find_potential_aliases(blocks, args, typemap, func_ir, alias_map=None,
    arg_aliases=None):
    if alias_map is None:
        alias_map = {}
    if arg_aliases is None:
        arg_aliases = set(a for a in args if not is_immutable_type(a, typemap))
    func_ir._definitions = build_definitions(func_ir.blocks)
    upsxe__rcvmw = ['ravel', 'transpose', 'reshape']
    for qnml__ppr in blocks.values():
        for tiyd__kstx in qnml__ppr.body:
            if type(tiyd__kstx) in alias_analysis_extensions:
                bxcfn__ydyq = alias_analysis_extensions[type(tiyd__kstx)]
                bxcfn__ydyq(tiyd__kstx, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(tiyd__kstx, ir.Assign):
                xeen__kstp = tiyd__kstx.value
                bsxd__mxrwo = tiyd__kstx.target.name
                if is_immutable_type(bsxd__mxrwo, typemap):
                    continue
                if isinstance(xeen__kstp, ir.Var
                    ) and bsxd__mxrwo != xeen__kstp.name:
                    _add_alias(bsxd__mxrwo, xeen__kstp.name, alias_map,
                        arg_aliases)
                if isinstance(xeen__kstp, ir.Expr) and (xeen__kstp.op ==
                    'cast' or xeen__kstp.op in ['getitem', 'static_getitem']):
                    _add_alias(bsxd__mxrwo, xeen__kstp.value.name,
                        alias_map, arg_aliases)
                if isinstance(xeen__kstp, ir.Expr
                    ) and xeen__kstp.op == 'inplace_binop':
                    _add_alias(bsxd__mxrwo, xeen__kstp.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(xeen__kstp, ir.Expr
                    ) and xeen__kstp.op == 'getattr' and xeen__kstp.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(bsxd__mxrwo, xeen__kstp.value.name,
                        alias_map, arg_aliases)
                if isinstance(xeen__kstp, ir.Expr
                    ) and xeen__kstp.op == 'getattr' and xeen__kstp.attr not in [
                    'shape'] and xeen__kstp.value.name in arg_aliases:
                    _add_alias(bsxd__mxrwo, xeen__kstp.value.name,
                        alias_map, arg_aliases)
                if isinstance(xeen__kstp, ir.Expr
                    ) and xeen__kstp.op == 'getattr' and xeen__kstp.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(bsxd__mxrwo, xeen__kstp.value.name,
                        alias_map, arg_aliases)
                if isinstance(xeen__kstp, ir.Expr) and xeen__kstp.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(bsxd__mxrwo, typemap):
                    for wktxs__azm in xeen__kstp.items:
                        _add_alias(bsxd__mxrwo, wktxs__azm.name, alias_map,
                            arg_aliases)
                if isinstance(xeen__kstp, ir.Expr) and xeen__kstp.op == 'call':
                    gbyu__ogs = guard(find_callname, func_ir, xeen__kstp,
                        typemap)
                    if gbyu__ogs is None:
                        continue
                    tirhx__fjmy, ule__solr = gbyu__ogs
                    if gbyu__ogs in alias_func_extensions:
                        zgyli__nbx = alias_func_extensions[gbyu__ogs]
                        zgyli__nbx(bsxd__mxrwo, xeen__kstp.args, alias_map,
                            arg_aliases)
                    if ule__solr == 'numpy' and tirhx__fjmy in upsxe__rcvmw:
                        _add_alias(bsxd__mxrwo, xeen__kstp.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(ule__solr, ir.Var
                        ) and tirhx__fjmy in upsxe__rcvmw:
                        _add_alias(bsxd__mxrwo, ule__solr.name, alias_map,
                            arg_aliases)
    dmcek__tvw = copy.deepcopy(alias_map)
    for wktxs__azm in dmcek__tvw:
        for kgn__zdd in dmcek__tvw[wktxs__azm]:
            alias_map[wktxs__azm] |= alias_map[kgn__zdd]
        for kgn__zdd in dmcek__tvw[wktxs__azm]:
            alias_map[kgn__zdd] = alias_map[wktxs__azm]
    return alias_map, arg_aliases


if _check_numba_change:
    lines = inspect.getsource(ir_utils.find_potential_aliases)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e6cf3e0f502f903453eb98346fc6854f87dc4ea1ac62f65c2d6aef3bf690b6c5':
        warnings.warn('ir_utils.find_potential_aliases has changed')
ir_utils.find_potential_aliases = find_potential_aliases
numba.parfors.array_analysis.find_potential_aliases = find_potential_aliases
if _check_numba_change:
    lines = inspect.getsource(ir_utils.dead_code_elimination)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '40a8626300a1a17523944ec7842b093c91258bbc60844bbd72191a35a4c366bf':
        warnings.warn('ir_utils.dead_code_elimination has changed')


def mini_dce(func_ir, typemap=None, alias_map=None, arg_aliases=None):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    wbpr__wxbrh = compute_cfg_from_blocks(func_ir.blocks)
    qab__frps = compute_use_defs(func_ir.blocks)
    lfjf__cie = compute_live_map(wbpr__wxbrh, func_ir.blocks, qab__frps.
        usemap, qab__frps.defmap)
    wxdgj__olvg = True
    while wxdgj__olvg:
        wxdgj__olvg = False
        for cbqkh__hhzu, block in func_ir.blocks.items():
            lives = {wktxs__azm.name for wktxs__azm in block.terminator.
                list_vars()}
            for bngk__qordb, lwrt__zmhfg in wbpr__wxbrh.successors(cbqkh__hhzu
                ):
                lives |= lfjf__cie[bngk__qordb]
            lzzii__ynzte = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    bsxd__mxrwo = stmt.target
                    ucgeh__vre = stmt.value
                    if bsxd__mxrwo.name not in lives:
                        if isinstance(ucgeh__vre, ir.Expr
                            ) and ucgeh__vre.op == 'make_function':
                            continue
                        if isinstance(ucgeh__vre, ir.Expr
                            ) and ucgeh__vre.op == 'getattr':
                            continue
                        if isinstance(ucgeh__vre, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(bsxd__mxrwo,
                            None), types.Function):
                            continue
                        if isinstance(ucgeh__vre, ir.Expr
                            ) and ucgeh__vre.op == 'build_map':
                            continue
                        if isinstance(ucgeh__vre, ir.Expr
                            ) and ucgeh__vre.op == 'build_tuple':
                            continue
                    if isinstance(ucgeh__vre, ir.Var
                        ) and bsxd__mxrwo.name == ucgeh__vre.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    lmbwe__lwy = analysis.ir_extension_usedefs[type(stmt)]
                    dlul__zazmk, akex__uuy = lmbwe__lwy(stmt)
                    lives -= akex__uuy
                    lives |= dlul__zazmk
                else:
                    lives |= {wktxs__azm.name for wktxs__azm in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(bsxd__mxrwo.name)
                lzzii__ynzte.append(stmt)
            lzzii__ynzte.reverse()
            if len(block.body) != len(lzzii__ynzte):
                wxdgj__olvg = True
            block.body = lzzii__ynzte


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    gbr__iqzv = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (gbr__iqzv,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    tqli__cnyk = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), tqli__cnyk)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '7f6974584cb10e49995b652827540cc6732e497c0b9f8231b44fd83fcc1c0a83':
        warnings.warn(
            'numba.core.typing.templates.make_overload_template has changed')
numba.core.typing.templates.make_overload_template = make_overload_template


def _resolve(self, typ, attr):
    if self._attr != attr:
        return None
    if isinstance(typ, types.TypeRef):
        assert typ == self.key
    else:
        assert isinstance(typ, self.key)


    class MethodTemplate(AbstractTemplate):
        key = self.key, attr
        _inline = self._inline
        _no_unliteral = getattr(self, '_no_unliteral', False)
        _overload_func = staticmethod(self._overload_func)
        _inline_overloads = self._inline_overloads
        prefer_literal = self.prefer_literal

        def generic(_, args, kws):
            args = (typ,) + tuple(args)
            fnty = self._get_function_type(self.context, typ)
            sig = self._get_signature(self.context, fnty, args, kws)
            sig = sig.replace(pysig=numba.core.utils.pysignature(self.
                _overload_func))
            for ftd__ajcbr in fnty.templates:
                self._inline_overloads.update(ftd__ajcbr._inline_overloads)
            if sig is not None:
                return sig.as_method()
    return types.BoundFunction(MethodTemplate, typ)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadMethodTemplate._resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ce8e0935dc939d0867ef969e1ed2975adb3533a58a4133fcc90ae13c4418e4d6':
        warnings.warn(
            'numba.core.typing.templates._OverloadMethodTemplate._resolve has changed'
            )
numba.core.typing.templates._OverloadMethodTemplate._resolve = _resolve


def make_overload_attribute_template(typ, attr, overload_func, inline,
    prefer_literal=False, base=_OverloadAttributeTemplate, **kwargs):
    assert isinstance(typ, types.Type) or issubclass(typ, types.Type)
    name = 'OverloadAttributeTemplate_%s_%s' % (typ, attr)
    no_unliteral = kwargs.pop('no_unliteral', False)
    tqli__cnyk = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), tqli__cnyk)
    return obj


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_attribute_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f066c38c482d6cf8bf5735a529c3264118ba9b52264b24e58aad12a6b1960f5d':
        warnings.warn(
            'numba.core.typing.templates.make_overload_attribute_template has changed'
            )
numba.core.typing.templates.make_overload_attribute_template = (
    make_overload_attribute_template)


def generic(self, args, kws):
    from numba.core.typed_passes import PreLowerStripPhis
    hqyz__rdmlf, ilbr__ignn = self._get_impl(args, kws)
    if hqyz__rdmlf is None:
        return
    yfwu__snreq = types.Dispatcher(hqyz__rdmlf)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        fevdq__vfnld = hqyz__rdmlf._compiler
        flags = compiler.Flags()
        cumq__svmj = fevdq__vfnld.targetdescr.typing_context
        qphq__ryb = fevdq__vfnld.targetdescr.target_context
        tee__trcrz = fevdq__vfnld.pipeline_class(cumq__svmj, qphq__ryb,
            None, None, None, flags, None)
        ghcul__lyp = InlineWorker(cumq__svmj, qphq__ryb, fevdq__vfnld.
            locals, tee__trcrz, flags, None)
        jpwp__xxrof = yfwu__snreq.dispatcher.get_call_template
        ftd__ajcbr, fuvuy__hvlrm, vwd__kkxp, kws = jpwp__xxrof(ilbr__ignn, kws)
        if vwd__kkxp in self._inline_overloads:
            return self._inline_overloads[vwd__kkxp]['iinfo'].signature
        ir = ghcul__lyp.run_untyped_passes(yfwu__snreq.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, qphq__ryb, ir, vwd__kkxp, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, vwd__kkxp, None)
        self._inline_overloads[sig.args] = {'folded_args': vwd__kkxp}
        bfg__ixz = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = bfg__ixz
        if not self._inline.is_always_inline:
            sig = yfwu__snreq.get_call_type(self.context, ilbr__ignn, kws)
            self._compiled_overloads[sig.args] = yfwu__snreq.get_overload(sig)
        hby__wky = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': vwd__kkxp,
            'iinfo': hby__wky}
    else:
        sig = yfwu__snreq.get_call_type(self.context, ilbr__ignn, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = yfwu__snreq.get_overload(sig)
    return sig


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d453a6d0215ebf0bab1279ff59eb0040b34938623be99142ce20acc09cdeb64':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate.generic has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate.generic = generic


def bound_function(template_key, no_unliteral=False):

    def wrapper(method_resolver):

        @functools.wraps(method_resolver)
        def attribute_resolver(self, ty):


            class MethodTemplate(AbstractTemplate):
                key = template_key

                def generic(_, args, kws):
                    sig = method_resolver(self, ty, args, kws)
                    if sig is not None and sig.recvr is None:
                        sig = sig.replace(recvr=ty)
                    return sig
            MethodTemplate._no_unliteral = no_unliteral
            return types.BoundFunction(MethodTemplate, ty)
        return attribute_resolver
    return wrapper


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.bound_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a2feefe64eae6a15c56affc47bf0c1d04461f9566913442d539452b397103322':
        warnings.warn('numba.core.typing.templates.bound_function has changed')
numba.core.typing.templates.bound_function = bound_function


def get_call_type(self, context, args, kws):
    from numba.core import utils
    unu__vle = [True, False]
    bhaip__kufhs = [False, True]
    itz__kfb = _ResolutionFailures(context, self, args, kws, depth=self._depth)
    from numba.core.target_extension import get_local_target
    mujj__jjza = get_local_target(context)
    qkzj__vwx = utils.order_by_target_specificity(mujj__jjza, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for vdwx__rkra in qkzj__vwx:
        daoam__hzcum = vdwx__rkra(context)
        rfwbm__tert = unu__vle if daoam__hzcum.prefer_literal else bhaip__kufhs
        rfwbm__tert = [True] if getattr(daoam__hzcum, '_no_unliteral', False
            ) else rfwbm__tert
        for sipke__kuj in rfwbm__tert:
            try:
                if sipke__kuj:
                    sig = daoam__hzcum.apply(args, kws)
                else:
                    fiho__pvcao = tuple([_unlit_non_poison(a) for a in args])
                    lrnes__khkv = {rsjx__nrxf: _unlit_non_poison(wktxs__azm
                        ) for rsjx__nrxf, wktxs__azm in kws.items()}
                    sig = daoam__hzcum.apply(fiho__pvcao, lrnes__khkv)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    itz__kfb.add_error(daoam__hzcum, False, e, sipke__kuj)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = daoam__hzcum.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    mvqvr__mwml = getattr(daoam__hzcum, 'cases', None)
                    if mvqvr__mwml is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            mvqvr__mwml)
                    else:
                        msg = 'No match.'
                    itz__kfb.add_error(daoam__hzcum, True, msg, sipke__kuj)
    itz__kfb.raise_error()


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BaseFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '25f038a7216f8e6f40068ea81e11fd9af8ad25d19888f7304a549941b01b7015':
        warnings.warn(
            'numba.core.types.functions.BaseFunction.get_call_type has changed'
            )
numba.core.types.functions.BaseFunction.get_call_type = get_call_type
bodo_typing_error_info = """
This is often caused by the use of unsupported features or typing issues.
See https://docs.bodo.ai/
"""


def get_call_type2(self, context, args, kws):
    ftd__ajcbr = self.template(context)
    vpl__ooicz = None
    bwsa__iey = None
    xazft__lbkio = None
    rfwbm__tert = [True, False] if ftd__ajcbr.prefer_literal else [False, True]
    rfwbm__tert = [True] if getattr(ftd__ajcbr, '_no_unliteral', False
        ) else rfwbm__tert
    for sipke__kuj in rfwbm__tert:
        if sipke__kuj:
            try:
                xazft__lbkio = ftd__ajcbr.apply(args, kws)
            except Exception as zzq__qphx:
                if isinstance(zzq__qphx, errors.ForceLiteralArg):
                    raise zzq__qphx
                vpl__ooicz = zzq__qphx
                xazft__lbkio = None
            else:
                break
        else:
            pgrec__gpnzg = tuple([_unlit_non_poison(a) for a in args])
            tvd__pjqv = {rsjx__nrxf: _unlit_non_poison(wktxs__azm) for 
                rsjx__nrxf, wktxs__azm in kws.items()}
            yor__wuwp = pgrec__gpnzg == args and kws == tvd__pjqv
            if not yor__wuwp and xazft__lbkio is None:
                try:
                    xazft__lbkio = ftd__ajcbr.apply(pgrec__gpnzg, tvd__pjqv)
                except Exception as zzq__qphx:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        zzq__qphx, errors.NumbaError):
                        raise zzq__qphx
                    if isinstance(zzq__qphx, errors.ForceLiteralArg):
                        if ftd__ajcbr.prefer_literal:
                            raise zzq__qphx
                    bwsa__iey = zzq__qphx
                else:
                    break
    if xazft__lbkio is None and (bwsa__iey is not None or vpl__ooicz is not
        None):
        lpo__nlu = '- Resolution failure for {} arguments:\n{}\n'
        ctgm__dtiy = _termcolor.highlight(lpo__nlu)
        if numba.core.config.DEVELOPER_MODE:
            ihw__zjqk = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    qfbb__jjk = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    qfbb__jjk = ['']
                rue__uivv = '\n{}'.format(2 * ihw__zjqk)
                yoygu__amxj = _termcolor.reset(rue__uivv + rue__uivv.join(
                    _bt_as_lines(qfbb__jjk)))
                return _termcolor.reset(yoygu__amxj)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            tyu__hqq = str(e)
            tyu__hqq = tyu__hqq if tyu__hqq else str(repr(e)) + add_bt(e)
            zwu__cfce = errors.TypingError(textwrap.dedent(tyu__hqq))
            return ctgm__dtiy.format(literalness, str(zwu__cfce))
        import bodo
        if isinstance(vpl__ooicz, bodo.utils.typing.BodoError):
            raise vpl__ooicz
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', vpl__ooicz) +
                nested_msg('non-literal', bwsa__iey))
        else:
            if 'missing a required argument' in vpl__ooicz.msg:
                msg = 'missing a required argument'
            else:
                msg = 'Compilation error for '
                if isinstance(self.this, bodo.hiframes.pd_dataframe_ext.
                    DataFrameType):
                    msg += 'DataFrame.'
                elif isinstance(self.this, bodo.hiframes.pd_series_ext.
                    SeriesType):
                    msg += 'Series.'
                msg += f'{self.typing_key[1]}().{bodo_typing_error_info}'
            raise errors.TypingError(msg, loc=vpl__ooicz.loc)
    return xazft__lbkio


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BoundFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '502cd77c0084452e903a45a0f1f8107550bfbde7179363b57dabd617ce135f4a':
        warnings.warn(
            'numba.core.types.functions.BoundFunction.get_call_type has changed'
            )
numba.core.types.functions.BoundFunction.get_call_type = get_call_type2


def string_from_string_and_size(self, string, size):
    from llvmlite import ir as lir
    fnty = lir.FunctionType(self.pyobj, [self.cstring, self.py_ssize_t])
    tirhx__fjmy = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=tirhx__fjmy)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            lri__gsqgp = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), lri__gsqgp)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    wqn__mhw = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            wqn__mhw.append(types.Omitted(a.value))
        else:
            wqn__mhw.append(self.typeof_pyval(a))
    iul__ydncm = None
    try:
        error = None
        iul__ydncm = self.compile(tuple(wqn__mhw))
    except errors.ForceLiteralArg as e:
        szpo__gzkcr = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if szpo__gzkcr:
            ucrg__qqj = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            igsn__umonv = ', '.join('Arg #{} is {}'.format(i, args[i]) for
                i in sorted(szpo__gzkcr))
            raise errors.CompilerError(ucrg__qqj.format(igsn__umonv))
        ilbr__ignn = []
        try:
            for i, wktxs__azm in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        ilbr__ignn.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        ilbr__ignn.append(types.literal(args[i]))
                else:
                    ilbr__ignn.append(args[i])
            args = ilbr__ignn
        except (OSError, FileNotFoundError) as lkb__epg:
            error = FileNotFoundError(str(lkb__epg) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                iul__ydncm = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        lws__zwtv = []
        for i, pzvo__whe in enumerate(args):
            val = pzvo__whe.value if isinstance(pzvo__whe, numba.core.
                dispatcher.OmittedArg) else pzvo__whe
            try:
                bodkm__bykyq = typeof(val, Purpose.argument)
            except ValueError as equ__lqfw:
                lws__zwtv.append((i, str(equ__lqfw)))
            else:
                if bodkm__bykyq is None:
                    lws__zwtv.append((i,
                        f'cannot determine Numba type of value {val}'))
        if lws__zwtv:
            wuzb__uopgq = '\n'.join(f'- argument {i}: {dtvdm__kgnbv}' for i,
                dtvdm__kgnbv in lws__zwtv)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{wuzb__uopgq}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                ypus__drno = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                yat__kzb = False
                for lxq__joeq in ypus__drno:
                    if lxq__joeq in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        yat__kzb = True
                        break
                if not yat__kzb:
                    msg = f'{str(e)}'
                msg += '\n' + e.loc.strformat() + '\n'
                e.patch_message(msg)
        error_rewrite(e, 'typing')
    except errors.UnsupportedError as e:
        error_rewrite(e, 'unsupported_error')
    except (errors.NotDefinedError, errors.RedefinedError, errors.
        VerificationError) as e:
        error_rewrite(e, 'interpreter')
    except errors.ConstantInferenceError as e:
        error_rewrite(e, 'constant_inference')
    except bodo.utils.typing.BodoError as e:
        error = bodo.utils.typing.BodoError(str(e))
    except Exception as e:
        if numba.core.config.SHOW_HELP:
            if hasattr(e, 'patch_message'):
                lri__gsqgp = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), lri__gsqgp)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return iul__ydncm


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher._DispatcherBase.
        _compile_for_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5cdfbf0b13a528abf9f0408e70f67207a03e81d610c26b1acab5b2dc1f79bf06':
        warnings.warn(
            'numba.core.dispatcher._DispatcherBase._compile_for_args has changed'
            )
numba.core.dispatcher._DispatcherBase._compile_for_args = _compile_for_args


def resolve_gb_agg_funcs(cres):
    from bodo.ir.aggregate import gb_agg_cfunc_addr
    for vdprq__oba in cres.library._codegen._engine._defined_symbols:
        if vdprq__oba.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in vdprq__oba and (
            'bodo_gb_udf_update_local' in vdprq__oba or 
            'bodo_gb_udf_combine' in vdprq__oba or 'bodo_gb_udf_eval' in
            vdprq__oba or 'bodo_gb_apply_general_udfs' in vdprq__oba):
            gb_agg_cfunc_addr[vdprq__oba
                ] = cres.library.get_pointer_to_function(vdprq__oba)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for vdprq__oba in cres.library._codegen._engine._defined_symbols:
        if vdprq__oba.startswith('cfunc') and ('get_join_cond_addr' not in
            vdprq__oba or 'bodo_join_gen_cond' in vdprq__oba):
            join_gen_cond_cfunc_addr[vdprq__oba
                ] = cres.library.get_pointer_to_function(vdprq__oba)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    hqyz__rdmlf = self._get_dispatcher_for_current_target()
    if hqyz__rdmlf is not self:
        return hqyz__rdmlf.compile(sig)
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        if not self._can_compile:
            raise RuntimeError('compilation disabled')
        with self._compiling_counter:
            args, return_type = sigutils.normalize_signature(sig)
            kgd__lsswr = self.overloads.get(tuple(args))
            if kgd__lsswr is not None:
                return kgd__lsswr.entry_point
            cres = self._cache.load_overload(sig, self.targetctx)
            if cres is not None:
                resolve_gb_agg_funcs(cres)
                resolve_join_general_cond_funcs(cres)
                self._cache_hits[sig] += 1
                if not cres.objectmode:
                    self.targetctx.insert_user_function(cres.entry_point,
                        cres.fndesc, [cres.library])
                self.add_overload(cres)
                return cres.entry_point
            self._cache_misses[sig] += 1
            whgh__xwm = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=whgh__xwm):
                try:
                    cres = self._compiler.compile(args, return_type)
                except errors.ForceLiteralArg as e:

                    def folded(args, kws):
                        return self._compiler.fold_argument_types(args, kws)[1]
                    raise e.bind_fold_arguments(folded)
                self.add_overload(cres)
            self._cache.save_overload(sig, cres)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.Dispatcher.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '934ec993577ea3b1c7dd2181ac02728abf8559fd42c17062cc821541b092ff8f':
        warnings.warn('numba.core.dispatcher.Dispatcher.compile has changed')
numba.core.dispatcher.Dispatcher.compile = compile


def _get_module_for_linking(self):
    import llvmlite.binding as ll
    self._ensure_finalized()
    if self._shared_module is not None:
        return self._shared_module
    upg__ysleb = self._final_module
    nnit__wpil = []
    jmv__lrpw = 0
    for fn in upg__ysleb.functions:
        jmv__lrpw += 1
        if not fn.is_declaration and fn.linkage == ll.Linkage.external:
            if 'get_agg_udf_addr' not in fn.name:
                if 'bodo_gb_udf_update_local' in fn.name:
                    continue
                if 'bodo_gb_udf_combine' in fn.name:
                    continue
                if 'bodo_gb_udf_eval' in fn.name:
                    continue
                if 'bodo_gb_apply_general_udfs' in fn.name:
                    continue
            if 'get_join_cond_addr' not in fn.name:
                if 'bodo_join_gen_cond' in fn.name:
                    continue
            nnit__wpil.append(fn.name)
    if jmv__lrpw == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if nnit__wpil:
        upg__ysleb = upg__ysleb.clone()
        for name in nnit__wpil:
            upg__ysleb.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = upg__ysleb
    return upg__ysleb


if _check_numba_change:
    lines = inspect.getsource(numba.core.codegen.CPUCodeLibrary.
        _get_module_for_linking)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '56dde0e0555b5ec85b93b97c81821bce60784515a1fbf99e4542e92d02ff0a73':
        warnings.warn(
            'numba.core.codegen.CPUCodeLibrary._get_module_for_linking has changed'
            )
numba.core.codegen.CPUCodeLibrary._get_module_for_linking = (
    _get_module_for_linking)


def propagate(self, typeinfer):
    import bodo
    errors = []
    for jqr__tjff in self.constraints:
        loc = jqr__tjff.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                jqr__tjff(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                pbdy__wbrq = numba.core.errors.TypingError(str(e), loc=
                    jqr__tjff.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(pbdy__wbrq, e))
            except bodo.utils.typing.BodoError as e:
                if loc not in e.locs_in_msg:
                    errors.append(bodo.utils.typing.BodoError(str(e.msg) +
                        '\n' + loc.strformat() + '\n', locs_in_msg=e.
                        locs_in_msg + [loc]))
                else:
                    errors.append(bodo.utils.typing.BodoError(e.msg,
                        locs_in_msg=e.locs_in_msg))
            except Exception as e:
                from numba.core import utils
                if utils.use_old_style_errors():
                    numba.core.typeinfer._logger.debug('captured error',
                        exc_info=e)
                    msg = """Internal error at {con}.
{err}
Enable logging at debug level for details."""
                    pbdy__wbrq = numba.core.errors.TypingError(msg.format(
                        con=jqr__tjff, err=str(e)), loc=jqr__tjff.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(pbdy__wbrq, e))
                elif utils.use_new_style_errors():
                    raise e
                else:
                    msg = (
                        f"Unknown CAPTURED_ERRORS style: '{numba.core.config.CAPTURED_ERRORS}'."
                        )
                    assert 0, msg
    return errors


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.ConstraintNetwork.propagate)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e73635eeba9ba43cb3372f395b747ae214ce73b729fb0adba0a55237a1cb063':
        warnings.warn(
            'numba.core.typeinfer.ConstraintNetwork.propagate has changed')
numba.core.typeinfer.ConstraintNetwork.propagate = propagate


def raise_error(self):
    import bodo
    for fywzu__zhlws in self._failures.values():
        for iueh__ksiab in fywzu__zhlws:
            if isinstance(iueh__ksiab.error, ForceLiteralArg):
                raise iueh__ksiab.error
            if isinstance(iueh__ksiab.error, bodo.utils.typing.BodoError):
                raise iueh__ksiab.error
    raise TypingError(self.format())


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.
        _ResolutionFailures.raise_error)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84b89430f5c8b46cfc684804e6037f00a0f170005cd128ad245551787b2568ea':
        warnings.warn(
            'numba.core.types.functions._ResolutionFailures.raise_error has changed'
            )
numba.core.types.functions._ResolutionFailures.raise_error = raise_error


def bodo_remove_dead_block(block, lives, call_table, arg_aliases, alias_map,
    alias_set, func_ir, typemap):
    from bodo.transforms.distributed_pass import saved_array_analysis
    from bodo.utils.utils import is_array_typ, is_expr
    dmss__cluxj = False
    lzzii__ynzte = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        erljc__krpt = set()
        qcm__wqx = lives & alias_set
        for wktxs__azm in qcm__wqx:
            erljc__krpt |= alias_map[wktxs__azm]
        lives_n_aliases = lives | erljc__krpt | arg_aliases
        if type(stmt) in remove_dead_extensions:
            bxcfn__ydyq = remove_dead_extensions[type(stmt)]
            stmt = bxcfn__ydyq(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                dmss__cluxj = True
                continue
        if isinstance(stmt, ir.Assign):
            bsxd__mxrwo = stmt.target
            ucgeh__vre = stmt.value
            if bsxd__mxrwo.name not in lives and has_no_side_effect(ucgeh__vre,
                lives_n_aliases, call_table):
                dmss__cluxj = True
                continue
            if saved_array_analysis and bsxd__mxrwo.name in lives and is_expr(
                ucgeh__vre, 'getattr'
                ) and ucgeh__vre.attr == 'shape' and is_array_typ(typemap[
                ucgeh__vre.value.name]) and ucgeh__vre.value.name not in lives:
                asoi__dtpxt = {wktxs__azm: rsjx__nrxf for rsjx__nrxf,
                    wktxs__azm in func_ir.blocks.items()}
                if block in asoi__dtpxt:
                    cbqkh__hhzu = asoi__dtpxt[block]
                    rouyi__xra = saved_array_analysis.get_equiv_set(cbqkh__hhzu
                        )
                    dxla__gjsnh = rouyi__xra.get_equiv_set(ucgeh__vre.value)
                    if dxla__gjsnh is not None:
                        for wktxs__azm in dxla__gjsnh:
                            if wktxs__azm.endswith('#0'):
                                wktxs__azm = wktxs__azm[:-2]
                            if wktxs__azm in typemap and is_array_typ(typemap
                                [wktxs__azm]) and wktxs__azm in lives:
                                ucgeh__vre.value = ir.Var(ucgeh__vre.value.
                                    scope, wktxs__azm, ucgeh__vre.value.loc)
                                dmss__cluxj = True
                                break
            if isinstance(ucgeh__vre, ir.Var
                ) and bsxd__mxrwo.name == ucgeh__vre.name:
                dmss__cluxj = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                dmss__cluxj = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            lmbwe__lwy = analysis.ir_extension_usedefs[type(stmt)]
            dlul__zazmk, akex__uuy = lmbwe__lwy(stmt)
            lives -= akex__uuy
            lives |= dlul__zazmk
        else:
            lives |= {wktxs__azm.name for wktxs__azm in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                fxcc__crghv = set()
                if isinstance(ucgeh__vre, ir.Expr):
                    fxcc__crghv = {wktxs__azm.name for wktxs__azm in
                        ucgeh__vre.list_vars()}
                if bsxd__mxrwo.name not in fxcc__crghv:
                    lives.remove(bsxd__mxrwo.name)
        lzzii__ynzte.append(stmt)
    lzzii__ynzte.reverse()
    block.body = lzzii__ynzte
    return dmss__cluxj


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            yhp__evy, = args
            if isinstance(yhp__evy, types.IterableType):
                dtype = yhp__evy.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), yhp__evy)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    tky__jpi = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (tky__jpi, self.dtype)
    super(types.Set, self).__init__(name=name)


types.Set.__init__ = Set__init__


@lower_builtin(operator.eq, types.UnicodeType, types.UnicodeType)
def eq_str(context, builder, sig, args):
    func = numba.cpython.unicode.unicode_eq(*sig.args)
    return context.compile_internal(builder, func, sig, args)


numba.parfors.parfor.push_call_vars = (lambda blocks, saved_globals,
    saved_getattrs, typemap, nested=False: None)


def maybe_literal(value):
    if isinstance(value, (list, dict, pytypes.FunctionType)):
        return
    if isinstance(value, tuple):
        try:
            return types.Tuple([literal(x) for x in value])
        except LiteralTypingError as xbl__twf:
            return
    try:
        return literal(value)
    except LiteralTypingError as xbl__twf:
        return


if _check_numba_change:
    lines = inspect.getsource(types.maybe_literal)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8fb2fd93acf214b28e33e37d19dc2f7290a42792ec59b650553ac278854b5081':
        warnings.warn('types.maybe_literal has changed')
types.maybe_literal = maybe_literal
types.misc.maybe_literal = maybe_literal


def CacheImpl__init__(self, py_func):
    self._lineno = py_func.__code__.co_firstlineno
    try:
        sxuw__lvl = py_func.__qualname__
    except AttributeError as xbl__twf:
        sxuw__lvl = py_func.__name__
    anqur__kvkm = inspect.getfile(py_func)
    for cls in self._locator_classes:
        ueurw__xdzlh = cls.from_function(py_func, anqur__kvkm)
        if ueurw__xdzlh is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (sxuw__lvl, anqur__kvkm))
    self._locator = ueurw__xdzlh
    dfh__fjoh = inspect.getfile(py_func)
    ngkb__vnsyw = os.path.splitext(os.path.basename(dfh__fjoh))[0]
    if anqur__kvkm.startswith('<ipython-'):
        qfh__hzp = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)', '\\1\\3',
            ngkb__vnsyw, count=1)
        if qfh__hzp == ngkb__vnsyw:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        ngkb__vnsyw = qfh__hzp
    oyb__qugdw = '%s.%s' % (ngkb__vnsyw, sxuw__lvl)
    phyws__phj = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(oyb__qugdw, phyws__phj)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    oexv__adpuf = list(filter(lambda a: self._istuple(a.name), args))
    if len(oexv__adpuf) == 2 and fn.__name__ == 'add':
        geys__ydrw = self.typemap[oexv__adpuf[0].name]
        feg__rzh = self.typemap[oexv__adpuf[1].name]
        if geys__ydrw.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                oexv__adpuf[1]))
        if feg__rzh.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                oexv__adpuf[0]))
        try:
            nyjs__labw = [equiv_set.get_shape(x) for x in oexv__adpuf]
            if None in nyjs__labw:
                return None
            zdv__licwi = sum(nyjs__labw, ())
            return ArrayAnalysis.AnalyzeResult(shape=zdv__licwi)
        except GuardException as xbl__twf:
            return None
    kirg__vjljd = list(filter(lambda a: self._isarray(a.name), args))
    require(len(kirg__vjljd) > 0)
    iyqcz__oqai = [x.name for x in kirg__vjljd]
    armoj__jmzfw = [self.typemap[x.name].ndim for x in kirg__vjljd]
    kwq__nal = max(armoj__jmzfw)
    require(kwq__nal > 0)
    nyjs__labw = [equiv_set.get_shape(x) for x in kirg__vjljd]
    if any(a is None for a in nyjs__labw):
        return ArrayAnalysis.AnalyzeResult(shape=kirg__vjljd[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, kirg__vjljd))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, nyjs__labw,
        iyqcz__oqai)


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_broadcast)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6c91fec038f56111338ea2b08f5f0e7f61ebdab1c81fb811fe26658cc354e40f':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast has changed'
            )
numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast = (
    _analyze_broadcast)


def slice_size(self, index, dsize, equiv_set, scope, stmts):
    return None, None


numba.parfors.array_analysis.ArrayAnalysis.slice_size = slice_size


def convert_code_obj_to_function(code_obj, caller_ir):
    import bodo
    ojose__qjgfq = code_obj.code
    ujzc__opxpg = len(ojose__qjgfq.co_freevars)
    hwxfv__ara = ojose__qjgfq.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        ehdbi__sjoy, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        hwxfv__ara = [wktxs__azm.name for wktxs__azm in ehdbi__sjoy]
    gpj__hgbao = caller_ir.func_id.func.__globals__
    try:
        gpj__hgbao = getattr(code_obj, 'globals', gpj__hgbao)
    except KeyError as xbl__twf:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/source/programming_with_bodo/bodo_api_reference/udfs.html"
        )
    hnpnn__thwe = []
    for x in hwxfv__ara:
        try:
            gihi__uiv = caller_ir.get_definition(x)
        except KeyError as xbl__twf:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(gihi__uiv, (ir.Const, ir.Global, ir.FreeVar)):
            val = gihi__uiv.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                gbr__iqzv = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                gpj__hgbao[gbr__iqzv] = bodo.jit(distributed=False)(val)
                gpj__hgbao[gbr__iqzv].is_nested_func = True
                val = gbr__iqzv
            if isinstance(val, CPUDispatcher):
                gbr__iqzv = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                gpj__hgbao[gbr__iqzv] = val
                val = gbr__iqzv
            hnpnn__thwe.append(val)
        elif isinstance(gihi__uiv, ir.Expr
            ) and gihi__uiv.op == 'make_function':
            kdti__maov = convert_code_obj_to_function(gihi__uiv, caller_ir)
            gbr__iqzv = ir_utils.mk_unique_var('nested_func').replace('.', '_')
            gpj__hgbao[gbr__iqzv] = bodo.jit(distributed=False)(kdti__maov)
            gpj__hgbao[gbr__iqzv].is_nested_func = True
            hnpnn__thwe.append(gbr__iqzv)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    vqteo__mcge = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate
        (hnpnn__thwe)])
    srw__rdee = ','.join([('c_%d' % i) for i in range(ujzc__opxpg)])
    tkk__ttol = list(ojose__qjgfq.co_varnames)
    sgk__rzsf = 0
    jrebx__dij = ojose__qjgfq.co_argcount
    snwz__sbo = caller_ir.get_definition(code_obj.defaults)
    if snwz__sbo is not None:
        if isinstance(snwz__sbo, tuple):
            d = [caller_ir.get_definition(x).value for x in snwz__sbo]
            fiqvc__yzqn = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in snwz__sbo.items]
            fiqvc__yzqn = tuple(d)
        sgk__rzsf = len(fiqvc__yzqn)
    wuw__vnqwd = jrebx__dij - sgk__rzsf
    qcjfi__wkagm = ','.join([('%s' % tkk__ttol[i]) for i in range(wuw__vnqwd)])
    if sgk__rzsf:
        ejyr__rbym = [('%s = %s' % (tkk__ttol[i + wuw__vnqwd], fiqvc__yzqn[
            i])) for i in range(sgk__rzsf)]
        qcjfi__wkagm += ', '
        qcjfi__wkagm += ', '.join(ejyr__rbym)
    return _create_function_from_code_obj(ojose__qjgfq, vqteo__mcge,
        qcjfi__wkagm, srw__rdee, gpj__hgbao)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.convert_code_obj_to_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b840769812418d589460e924a15477e83e7919aac8a3dcb0188ff447344aa8ac':
        warnings.warn(
            'numba.core.ir_utils.convert_code_obj_to_function has changed')
numba.core.ir_utils.convert_code_obj_to_function = convert_code_obj_to_function
numba.core.untyped_passes.convert_code_obj_to_function = (
    convert_code_obj_to_function)


def passmanager_run(self, state):
    from numba.core.compiler import _EarlyPipelineCompletion
    if not self.finalized:
        raise RuntimeError('Cannot run non-finalised pipeline')
    from numba.core.compiler_machinery import CompilerPass, _pass_registry
    import bodo
    for rhcy__xzave, (myc__vsme, jekh__utyd) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % jekh__utyd)
            iet__rhum = _pass_registry.get(myc__vsme).pass_inst
            if isinstance(iet__rhum, CompilerPass):
                self._runPass(rhcy__xzave, iet__rhum, state)
            else:
                raise BaseException('Legacy pass in use')
        except _EarlyPipelineCompletion as e:
            raise e
        except bodo.utils.typing.BodoError as e:
            raise
        except Exception as e:
            if numba.core.config.DEVELOPER_MODE:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                msg = 'Failed in %s mode pipeline (step: %s)' % (self.
                    pipeline_name, jekh__utyd)
                labqq__poyv = self._patch_error(msg, e)
                raise labqq__poyv
            else:
                raise e


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler_machinery.PassManager.run)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '43505782e15e690fd2d7e53ea716543bec37aa0633502956864edf649e790cdb':
        warnings.warn(
            'numba.core.compiler_machinery.PassManager.run has changed')
numba.core.compiler_machinery.PassManager.run = passmanager_run
if _check_numba_change:
    lines = inspect.getsource(numba.np.ufunc.parallel._launch_threads)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a57ef28c4168fdd436a5513bba4351ebc6d9fba76c5819f44046431a79b9030f':
        warnings.warn('numba.np.ufunc.parallel._launch_threads has changed')
numba.np.ufunc.parallel._launch_threads = lambda : None


def get_reduce_nodes(reduction_node, nodes, func_ir):
    bxjkh__govdo = None
    akex__uuy = {}

    def lookup(var, already_seen, varonly=True):
        val = akex__uuy.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    olnu__gifr = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        bsxd__mxrwo = stmt.target
        ucgeh__vre = stmt.value
        akex__uuy[bsxd__mxrwo.name] = ucgeh__vre
        if isinstance(ucgeh__vre, ir.Var) and ucgeh__vre.name in akex__uuy:
            ucgeh__vre = lookup(ucgeh__vre, set())
        if isinstance(ucgeh__vre, ir.Expr):
            bwnbl__pxol = set(lookup(wktxs__azm, set(), True).name for
                wktxs__azm in ucgeh__vre.list_vars())
            if name in bwnbl__pxol:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(ucgeh__vre)]
                gwhdm__ajkwi = [x for x, lcpri__psl in args if lcpri__psl.
                    name != name]
                args = [(x, lcpri__psl) for x, lcpri__psl in args if x !=
                    lcpri__psl.name]
                ezx__kep = dict(args)
                if len(gwhdm__ajkwi) == 1:
                    ezx__kep[gwhdm__ajkwi[0]] = ir.Var(bsxd__mxrwo.scope, 
                        name + '#init', bsxd__mxrwo.loc)
                replace_vars_inner(ucgeh__vre, ezx__kep)
                bxjkh__govdo = nodes[i:]
                break
    return bxjkh__govdo


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_reduce_nodes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a05b52aff9cb02e595a510cd34e973857303a71097fc5530567cb70ca183ef3b':
        warnings.warn('numba.parfors.parfor.get_reduce_nodes has changed')
numba.parfors.parfor.get_reduce_nodes = get_reduce_nodes


def _can_reorder_stmts(stmt, next_stmt, func_ir, call_table, alias_map,
    arg_aliases):
    from numba.parfors.parfor import Parfor, expand_aliases, is_assert_equiv
    if isinstance(stmt, Parfor) and not isinstance(next_stmt, Parfor
        ) and not isinstance(next_stmt, ir.Print) and (not isinstance(
        next_stmt, ir.Assign) or has_no_side_effect(next_stmt.value, set(),
        call_table) or guard(is_assert_equiv, func_ir, next_stmt.value)):
        ictob__xmdu = expand_aliases({wktxs__azm.name for wktxs__azm in
            stmt.list_vars()}, alias_map, arg_aliases)
        kurs__hrdwz = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        wnmzt__qxmrx = expand_aliases({wktxs__azm.name for wktxs__azm in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        oflb__okhdw = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(kurs__hrdwz & wnmzt__qxmrx | oflb__okhdw & ictob__xmdu) == 0:
            return True
    return False


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor._can_reorder_stmts)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '18caa9a01b21ab92b4f79f164cfdbc8574f15ea29deedf7bafdf9b0e755d777c':
        warnings.warn('numba.parfors.parfor._can_reorder_stmts has changed')
numba.parfors.parfor._can_reorder_stmts = _can_reorder_stmts


def get_parfor_writes(parfor, func_ir):
    from numba.parfors.parfor import Parfor
    assert isinstance(parfor, Parfor)
    kgngv__akr = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            kgngv__akr.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                kgngv__akr.update(get_parfor_writes(stmt, func_ir))
    return kgngv__akr


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    kgngv__akr = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        kgngv__akr.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        kgngv__akr = {wktxs__azm.name for wktxs__azm in stmt.df_out_vars.
            values()}
        if stmt.out_key_vars is not None:
            kgngv__akr.update({wktxs__azm.name for wktxs__azm in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        kgngv__akr = {wktxs__azm.name for wktxs__azm in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        kgngv__akr = {wktxs__azm.name for wktxs__azm in stmt.out_data_vars.
            values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            kgngv__akr.update({wktxs__azm.name for wktxs__azm in stmt.
                out_key_arrs})
            kgngv__akr.update({wktxs__azm.name for wktxs__azm in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        gbyu__ogs = guard(find_callname, func_ir, stmt.value)
        if gbyu__ogs in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            kgngv__akr.add(stmt.value.args[0].name)
        if gbyu__ogs == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            kgngv__akr.add(stmt.value.args[1].name)
    return kgngv__akr


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.get_stmt_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1a7a80b64c9a0eb27e99dc8eaae187bde379d4da0b74c84fbf87296d87939974':
        warnings.warn('numba.core.ir_utils.get_stmt_writes has changed')


def patch_message(self, new_message):
    self.msg = new_message
    self.args = (new_message,) + self.args[1:]


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.patch_message)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ed189a428a7305837e76573596d767b6e840e99f75c05af6941192e0214fa899':
        warnings.warn('numba.core.errors.NumbaError.patch_message has changed')
numba.core.errors.NumbaError.patch_message = patch_message


def add_context(self, msg):
    if numba.core.config.DEVELOPER_MODE:
        self.contexts.append(msg)
        bxcfn__ydyq = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        bkyxb__slknt = bxcfn__ydyq.format(self, msg)
        self.args = bkyxb__slknt,
    else:
        bxcfn__ydyq = _termcolor.errmsg('{0}')
        bkyxb__slknt = bxcfn__ydyq.format(self)
        self.args = bkyxb__slknt,
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.add_context)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6a388d87788f8432c2152ac55ca9acaa94dbc3b55be973b2cf22dd4ee7179ab8':
        warnings.warn('numba.core.errors.NumbaError.add_context has changed')
numba.core.errors.NumbaError.add_context = add_context


def _get_dist_spec_from_options(spec, **options):
    from bodo.transforms.distributed_analysis import Distribution
    dist_spec = {}
    if 'distributed' in options:
        for geq__zgs in options['distributed']:
            dist_spec[geq__zgs] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for geq__zgs in options['distributed_block']:
            dist_spec[geq__zgs] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    hqlqz__ztqna = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, pleh__pkfs in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(pleh__pkfs)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    pgblk__ekgm = {}
    for emy__lnsnw in reversed(inspect.getmro(cls)):
        pgblk__ekgm.update(emy__lnsnw.__dict__)
    rod__hinfo, keel__fry, sxhz__doic, kxgf__lol = {}, {}, {}, {}
    for rsjx__nrxf, wktxs__azm in pgblk__ekgm.items():
        if isinstance(wktxs__azm, pytypes.FunctionType):
            rod__hinfo[rsjx__nrxf] = wktxs__azm
        elif isinstance(wktxs__azm, property):
            keel__fry[rsjx__nrxf] = wktxs__azm
        elif isinstance(wktxs__azm, staticmethod):
            sxhz__doic[rsjx__nrxf] = wktxs__azm
        else:
            kxgf__lol[rsjx__nrxf] = wktxs__azm
    eqx__lus = (set(rod__hinfo) | set(keel__fry) | set(sxhz__doic)) & set(spec)
    if eqx__lus:
        raise NameError('name shadowing: {0}'.format(', '.join(eqx__lus)))
    hudim__mqlkj = kxgf__lol.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(kxgf__lol)
    if kxgf__lol:
        msg = 'class members are not yet supported: {0}'
        syw__jwad = ', '.join(kxgf__lol.keys())
        raise TypeError(msg.format(syw__jwad))
    for rsjx__nrxf, wktxs__azm in keel__fry.items():
        if wktxs__azm.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(rsjx__nrxf))
    jit_methods = {rsjx__nrxf: bodo.jit(returns_maybe_distributed=
        hqlqz__ztqna)(wktxs__azm) for rsjx__nrxf, wktxs__azm in rod__hinfo.
        items()}
    jit_props = {}
    for rsjx__nrxf, wktxs__azm in keel__fry.items():
        tqli__cnyk = {}
        if wktxs__azm.fget:
            tqli__cnyk['get'] = bodo.jit(wktxs__azm.fget)
        if wktxs__azm.fset:
            tqli__cnyk['set'] = bodo.jit(wktxs__azm.fset)
        jit_props[rsjx__nrxf] = tqli__cnyk
    jit_static_methods = {rsjx__nrxf: bodo.jit(wktxs__azm.__func__) for 
        rsjx__nrxf, wktxs__azm in sxhz__doic.items()}
    ael__pubc = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    hoawf__hako = dict(class_type=ael__pubc, __doc__=hudim__mqlkj)
    hoawf__hako.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), hoawf__hako)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, ael__pubc)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(ael__pubc, typingctx, targetctx).register()
    as_numba_type.register(cls, ael__pubc.instance_type)
    return cls


if _check_numba_change:
    lines = inspect.getsource(jitclass_base.register_class_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '005e6e2e89a47f77a19ba86305565050d4dbc2412fc4717395adf2da348671a9':
        warnings.warn('jitclass_base.register_class_type has changed')
jitclass_base.register_class_type = register_class_type


def ClassType__init__(self, class_def, ctor_template_cls, struct,
    jit_methods, jit_props, jit_static_methods, dist_spec=None):
    if dist_spec is None:
        dist_spec = {}
    self.class_name = class_def.__name__
    self.class_doc = class_def.__doc__
    self._ctor_template_class = ctor_template_cls
    self.jit_methods = jit_methods
    self.jit_props = jit_props
    self.jit_static_methods = jit_static_methods
    self.struct = struct
    self.dist_spec = dist_spec
    sae__okx = ','.join('{0}:{1}'.format(rsjx__nrxf, wktxs__azm) for 
        rsjx__nrxf, wktxs__azm in struct.items())
    mglgd__lvtt = ','.join('{0}:{1}'.format(rsjx__nrxf, wktxs__azm) for 
        rsjx__nrxf, wktxs__azm in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), sae__okx, mglgd__lvtt)
    super(types.misc.ClassType, self).__init__(name)


if _check_numba_change:
    lines = inspect.getsource(types.misc.ClassType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b848ea82946c88f540e81f93ba95dfa7cd66045d944152a337fe2fc43451c30':
        warnings.warn('types.misc.ClassType.__init__ has changed')
types.misc.ClassType.__init__ = ClassType__init__


def jitclass(cls_or_spec=None, spec=None, **options):
    if cls_or_spec is not None and spec is None and not isinstance(cls_or_spec,
        type):
        spec = cls_or_spec
        cls_or_spec = None

    def wrap(cls):
        if numba.core.config.DISABLE_JIT:
            return cls
        else:
            from numba.experimental.jitclass.base import ClassBuilder
            return register_class_type(cls, spec, types.ClassType,
                ClassBuilder, **options)
    if cls_or_spec is None:
        return wrap
    else:
        return wrap(cls_or_spec)


if _check_numba_change:
    lines = inspect.getsource(jitclass_decorators.jitclass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '265f1953ee5881d1a5d90238d3c932cd300732e41495657e65bf51e59f7f4af5':
        warnings.warn('jitclass_decorators.jitclass has changed')


def CallConstraint_resolve(self, typeinfer, typevars, fnty):
    assert fnty
    context = typeinfer.context
    mmk__jmjrg = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if mmk__jmjrg is None:
        return
    znw__fqzji, rcci__ejont = mmk__jmjrg
    for a in itertools.chain(znw__fqzji, rcci__ejont.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, znw__fqzji, rcci__ejont)
    except ForceLiteralArg as e:
        nzo__sssq = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(nzo__sssq, self.kws)
        vql__kwjp = set()
        qglfq__adm = set()
        luqct__ccem = {}
        for rhcy__xzave in e.requested_args:
            cbe__dml = typeinfer.func_ir.get_definition(folded[rhcy__xzave])
            if isinstance(cbe__dml, ir.Arg):
                vql__kwjp.add(cbe__dml.index)
                if cbe__dml.index in e.file_infos:
                    luqct__ccem[cbe__dml.index] = e.file_infos[cbe__dml.index]
            else:
                qglfq__adm.add(rhcy__xzave)
        if qglfq__adm:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif vql__kwjp:
            raise ForceLiteralArg(vql__kwjp, loc=self.loc, file_infos=
                luqct__ccem)
    if sig is None:
        uuh__jwn = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in znw__fqzji]
        args += [('%s=%s' % (rsjx__nrxf, wktxs__azm)) for rsjx__nrxf,
            wktxs__azm in sorted(rcci__ejont.items())]
        dkxt__xail = uuh__jwn.format(fnty, ', '.join(map(str, args)))
        gyt__gdm = context.explain_function_type(fnty)
        msg = '\n'.join([dkxt__xail, gyt__gdm])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        azftb__rxm = context.unify_pairs(sig.recvr, fnty.this)
        if azftb__rxm is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if azftb__rxm is not None and azftb__rxm.is_precise():
            arkdr__hwiai = fnty.copy(this=azftb__rxm)
            typeinfer.propagate_refined_type(self.func, arkdr__hwiai)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            glt__dhvf = target.getone()
            if context.unify_pairs(glt__dhvf, sig.return_type) == glt__dhvf:
                sig = sig.replace(return_type=glt__dhvf)
    self.signature = sig
    self._add_refine_map(typeinfer, typevars, sig)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.CallConstraint.resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c78cd8ffc64b836a6a2ddf0362d481b52b9d380c5249920a87ff4da052ce081f':
        warnings.warn('numba.core.typeinfer.CallConstraint.resolve has changed'
            )
numba.core.typeinfer.CallConstraint.resolve = CallConstraint_resolve


def ForceLiteralArg__init__(self, arg_indices, fold_arguments=None, loc=
    None, file_infos=None):
    super(ForceLiteralArg, self).__init__(
        'Pseudo-exception to force literal arguments in the dispatcher',
        loc=loc)
    self.requested_args = frozenset(arg_indices)
    self.fold_arguments = fold_arguments
    if file_infos is None:
        self.file_infos = {}
    else:
        self.file_infos = file_infos


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b241d5e36a4cf7f4c73a7ad3238693612926606c7a278cad1978070b82fb55ef':
        warnings.warn('numba.core.errors.ForceLiteralArg.__init__ has changed')
numba.core.errors.ForceLiteralArg.__init__ = ForceLiteralArg__init__


def ForceLiteralArg_bind_fold_arguments(self, fold_arguments):
    e = ForceLiteralArg(self.requested_args, fold_arguments, loc=self.loc,
        file_infos=self.file_infos)
    return numba.core.utils.chain_exception(e, self)


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.
        bind_fold_arguments)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e93cca558f7c604a47214a8f2ec33ee994104cb3e5051166f16d7cc9315141d':
        warnings.warn(
            'numba.core.errors.ForceLiteralArg.bind_fold_arguments has changed'
            )
numba.core.errors.ForceLiteralArg.bind_fold_arguments = (
    ForceLiteralArg_bind_fold_arguments)


def ForceLiteralArg_combine(self, other):
    if not isinstance(other, ForceLiteralArg):
        ucrg__qqj = '*other* must be a {} but got a {} instead'
        raise TypeError(ucrg__qqj.format(ForceLiteralArg, type(other)))
    return ForceLiteralArg(self.requested_args | other.requested_args,
        file_infos={**self.file_infos, **other.file_infos})


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.combine)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '49bf06612776f5d755c1c7d1c5eb91831a57665a8fed88b5651935f3bf33e899':
        warnings.warn('numba.core.errors.ForceLiteralArg.combine has changed')
numba.core.errors.ForceLiteralArg.combine = ForceLiteralArg_combine


def _get_global_type(self, gv):
    from bodo.utils.typing import FunctionLiteral
    ty = self._lookup_global(gv)
    if ty is not None:
        return ty
    if isinstance(gv, pytypes.ModuleType):
        return types.Module(gv)
    if isinstance(gv, pytypes.FunctionType):
        return FunctionLiteral(gv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.
        _get_global_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8ffe6b81175d1eecd62a37639b5005514b4477d88f35f5b5395041ac8c945a4a':
        warnings.warn(
            'numba.core.typing.context.BaseContext._get_global_type has changed'
            )
numba.core.typing.context.BaseContext._get_global_type = _get_global_type


def _legalize_args(self, func_ir, args, kwargs, loc, func_globals,
    func_closures):
    from numba.core import sigutils
    from bodo.utils.transform import get_const_value_inner
    if args:
        raise errors.CompilerError(
            "objectmode context doesn't take any positional arguments")
    sqcdw__alxh = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for rsjx__nrxf, wktxs__azm in kwargs.items():
        fqfon__weujg = None
        try:
            hmjpt__zqe = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var
                ('dummy'), loc)
            func_ir._definitions[hmjpt__zqe.name] = [wktxs__azm]
            fqfon__weujg = get_const_value_inner(func_ir, hmjpt__zqe)
            func_ir._definitions.pop(hmjpt__zqe.name)
            if isinstance(fqfon__weujg, str):
                fqfon__weujg = sigutils._parse_signature_string(fqfon__weujg)
            if isinstance(fqfon__weujg, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {rsjx__nrxf} is annotated as type class {fqfon__weujg}."""
                    )
            assert isinstance(fqfon__weujg, types.Type)
            if isinstance(fqfon__weujg, (types.List, types.Set)):
                fqfon__weujg = fqfon__weujg.copy(reflected=False)
            sqcdw__alxh[rsjx__nrxf] = fqfon__weujg
        except BodoError as xbl__twf:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(fqfon__weujg, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(wktxs__azm, ir.Global):
                    msg = f'Global {wktxs__azm.name!r} is not defined.'
                if isinstance(wktxs__azm, ir.FreeVar):
                    msg = f'Freevar {wktxs__azm.name!r} is not defined.'
            if isinstance(wktxs__azm, ir.Expr) and wktxs__azm.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=rsjx__nrxf, msg=msg, loc=loc)
    for name, typ in sqcdw__alxh.items():
        self._legalize_arg_type(name, typ, loc)
    return sqcdw__alxh


if _check_numba_change:
    lines = inspect.getsource(numba.core.withcontexts._ObjModeContextType.
        _legalize_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '867c9ba7f1bcf438be56c38e26906bb551f59a99f853a9f68b71208b107c880e':
        warnings.warn(
            'numba.core.withcontexts._ObjModeContextType._legalize_args has changed'
            )
numba.core.withcontexts._ObjModeContextType._legalize_args = _legalize_args


def op_FORMAT_VALUE_byteflow(self, state, inst):
    flags = inst.arg
    if flags & 3 != 0:
        msg = 'str/repr/ascii conversion in f-strings not supported yet'
        raise errors.UnsupportedError(msg, loc=self.get_debug_loc(inst.lineno))
    format_spec = None
    if flags & 4 == 4:
        format_spec = state.pop()
    value = state.pop()
    fmtvar = state.make_temp()
    res = state.make_temp()
    state.append(inst, value=value, res=res, fmtvar=fmtvar, format_spec=
        format_spec)
    state.push(res)


def op_BUILD_STRING_byteflow(self, state, inst):
    tfsb__bgxdg = inst.arg
    assert tfsb__bgxdg > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(tfsb__bgxdg)]))
    tmps = [state.make_temp() for _ in range(tfsb__bgxdg - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    iie__xqo = ir.Global('format', format, loc=self.loc)
    self.store(value=iie__xqo, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    cxdf__ftg = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=cxdf__ftg, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    tfsb__bgxdg = inst.arg
    assert tfsb__bgxdg > 0, 'invalid BUILD_STRING count'
    sksb__cvkdt = self.get(strings[0])
    for other, zipx__aifiw in zip(strings[1:], tmps):
        other = self.get(other)
        xeen__kstp = ir.Expr.binop(operator.add, lhs=sksb__cvkdt, rhs=other,
            loc=self.loc)
        self.store(xeen__kstp, zipx__aifiw)
        sksb__cvkdt = self.get(zipx__aifiw)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    ngsoh__aqbtd = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, ngsoh__aqbtd])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    src__qaedh = mk_unique_var(f'{var_name}')
    hdnst__xgzfm = src__qaedh.replace('<', '_').replace('>', '_')
    hdnst__xgzfm = hdnst__xgzfm.replace('.', '_').replace('$', '_v')
    return hdnst__xgzfm


if _check_numba_change:
    lines = inspect.getsource(numba.core.inline_closurecall.
        _created_inlined_var_name)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0d91aac55cd0243e58809afe9d252562f9ae2899cde1112cc01a46804e01821e':
        warnings.warn(
            'numba.core.inline_closurecall._created_inlined_var_name has changed'
            )
numba.core.inline_closurecall._created_inlined_var_name = (
    _created_inlined_var_name)


def resolve_number___call__(self, classty):
    import numpy as np
    from numba.core.typing.templates import make_callable_template
    import bodo
    ty = classty.instance_type
    if isinstance(ty, types.NPDatetime):

        def typer(val1, val2):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(val1,
                'numpy.datetime64')
            if val1 == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
                if not is_overload_constant_str(val2):
                    raise_bodo_error(
                        "datetime64(): 'units' must be a 'str' specifying 'ns'"
                        )
                rrl__tjcsh = get_overload_const_str(val2)
                if rrl__tjcsh != 'ns':
                    raise BodoError("datetime64(): 'units' must be 'ns'")
                return types.NPDatetime('ns')
    else:

        def typer(val):
            if isinstance(val, (types.BaseTuple, types.Sequence)):
                fnty = self.context.resolve_value_type(np.array)
                sig = fnty.get_call_type(self.context, (val, types.DType(ty
                    )), {})
                return sig.return_type
            elif isinstance(val, (types.Number, types.Boolean, types.
                IntEnumMember)):
                return ty
            elif val == types.unicode_type:
                return ty
            elif isinstance(val, (types.NPDatetime, types.NPTimedelta)):
                if ty.bitwidth == 64:
                    return ty
                else:
                    msg = (
                        f'Cannot cast {val} to {ty} as {ty} is not 64 bits wide.'
                        )
                    raise errors.TypingError(msg)
            elif isinstance(val, types.Array
                ) and val.ndim == 0 and val.dtype == ty:
                return ty
            else:
                msg = f'Casting {val} to {ty} directly is unsupported.'
                if isinstance(val, types.Array):
                    msg += f" Try doing '<array>.astype(np.{ty})' instead"
                raise errors.TypingError(msg)
    return types.Function(make_callable_template(key=ty, typer=typer))


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.
        NumberClassAttribute.resolve___call__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdaf0c7d0820130481bb2bd922985257b9281b670f0bafffe10e51cabf0d5081':
        warnings.warn(
            'numba.core.typing.builtins.NumberClassAttribute.resolve___call__ has changed'
            )
numba.core.typing.builtins.NumberClassAttribute.resolve___call__ = (
    resolve_number___call__)


def on_assign(self, states, assign):
    if assign.target.name == states['varname']:
        scope = states['scope']
        ppjkx__iiigy = states['defmap']
        if len(ppjkx__iiigy) == 0:
            tpkgq__fpzob = assign.target
            numba.core.ssa._logger.debug('first assign: %s', tpkgq__fpzob)
            if tpkgq__fpzob.name not in scope.localvars:
                tpkgq__fpzob = scope.define(assign.target.name, loc=assign.loc)
        else:
            tpkgq__fpzob = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=tpkgq__fpzob, value=assign.value, loc=
            assign.loc)
        ppjkx__iiigy[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    abi__xtt = []
    for rsjx__nrxf, wktxs__azm in typing.npydecl.registry.globals:
        if rsjx__nrxf == func:
            abi__xtt.append(wktxs__azm)
    for rsjx__nrxf, wktxs__azm in typing.templates.builtin_registry.globals:
        if rsjx__nrxf == func:
            abi__xtt.append(wktxs__azm)
    if len(abi__xtt) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return abi__xtt


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    iin__hqgw = {}
    hhgpc__uei = find_topo_order(blocks)
    fdm__npb = {}
    for cbqkh__hhzu in hhgpc__uei:
        block = blocks[cbqkh__hhzu]
        lzzii__ynzte = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                bsxd__mxrwo = stmt.target.name
                ucgeh__vre = stmt.value
                if (ucgeh__vre.op == 'getattr' and ucgeh__vre.attr in
                    arr_math and isinstance(typemap[ucgeh__vre.value.name],
                    types.npytypes.Array)):
                    ucgeh__vre = stmt.value
                    nyx__hbhkj = ucgeh__vre.value
                    iin__hqgw[bsxd__mxrwo] = nyx__hbhkj
                    scope = nyx__hbhkj.scope
                    loc = nyx__hbhkj.loc
                    fjhiz__bkxlj = ir.Var(scope, mk_unique_var('$np_g_var'),
                        loc)
                    typemap[fjhiz__bkxlj.name] = types.misc.Module(numpy)
                    skjym__ynz = ir.Global('np', numpy, loc)
                    xdnm__iyg = ir.Assign(skjym__ynz, fjhiz__bkxlj, loc)
                    ucgeh__vre.value = fjhiz__bkxlj
                    lzzii__ynzte.append(xdnm__iyg)
                    func_ir._definitions[fjhiz__bkxlj.name] = [skjym__ynz]
                    func = getattr(numpy, ucgeh__vre.attr)
                    vgsbr__bhbxr = get_np_ufunc_typ_lst(func)
                    fdm__npb[bsxd__mxrwo] = vgsbr__bhbxr
                if (ucgeh__vre.op == 'call' and ucgeh__vre.func.name in
                    iin__hqgw):
                    nyx__hbhkj = iin__hqgw[ucgeh__vre.func.name]
                    iguz__ttk = calltypes.pop(ucgeh__vre)
                    zouva__mcw = iguz__ttk.args[:len(ucgeh__vre.args)]
                    vmuvx__vicor = {name: typemap[wktxs__azm.name] for name,
                        wktxs__azm in ucgeh__vre.kws}
                    pbr__plej = fdm__npb[ucgeh__vre.func.name]
                    gdsz__weun = None
                    for pwo__dzljm in pbr__plej:
                        try:
                            gdsz__weun = pwo__dzljm.get_call_type(typingctx,
                                [typemap[nyx__hbhkj.name]] + list(
                                zouva__mcw), vmuvx__vicor)
                            typemap.pop(ucgeh__vre.func.name)
                            typemap[ucgeh__vre.func.name] = pwo__dzljm
                            calltypes[ucgeh__vre] = gdsz__weun
                            break
                        except Exception as xbl__twf:
                            pass
                    if gdsz__weun is None:
                        raise TypeError(
                            f'No valid template found for {ucgeh__vre.func.name}'
                            )
                    ucgeh__vre.args = [nyx__hbhkj] + ucgeh__vre.args
            lzzii__ynzte.append(stmt)
        block.body = lzzii__ynzte


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    xaja__hlzfw = ufunc.nin
    bbr__oask = ufunc.nout
    wuw__vnqwd = ufunc.nargs
    assert wuw__vnqwd == xaja__hlzfw + bbr__oask
    if len(args) < xaja__hlzfw:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            xaja__hlzfw))
    if len(args) > wuw__vnqwd:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), wuw__vnqwd)
            )
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    dcn__xgfkt = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    porub__hgzh = max(dcn__xgfkt)
    hcjjx__duf = args[xaja__hlzfw:]
    if not all(d == porub__hgzh for d in dcn__xgfkt[xaja__hlzfw:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(mmwe__bpsrf, types.ArrayCompatible) and not
        isinstance(mmwe__bpsrf, types.Bytes) for mmwe__bpsrf in hcjjx__duf):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(mmwe__bpsrf.mutable for mmwe__bpsrf in hcjjx__duf):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    zbth__pgzzt = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    zkh__uog = None
    if porub__hgzh > 0 and len(hcjjx__duf) < ufunc.nout:
        zkh__uog = 'C'
        pwg__iviwu = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in pwg__iviwu and 'F' in pwg__iviwu:
            zkh__uog = 'F'
    return zbth__pgzzt, hcjjx__duf, porub__hgzh, zkh__uog


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.Numpy_rules_ufunc.
        _handle_inputs)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4b97c64ad9c3d50e082538795054f35cf6d2fe962c3ca40e8377a4601b344d5c':
        warnings.warn('Numpy_rules_ufunc._handle_inputs has changed')
numba.core.typing.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)
numba.np.ufunc.dufunc.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)


def DictType__init__(self, keyty, valty, initial_value=None):
    from numba.types import DictType, InitialValue, NoneType, Optional, Tuple, TypeRef, unliteral
    assert not isinstance(keyty, TypeRef)
    assert not isinstance(valty, TypeRef)
    keyty = unliteral(keyty)
    valty = unliteral(valty)
    if isinstance(keyty, (Optional, NoneType)):
        wmcvz__wcd = 'Dict.key_type cannot be of type {}'
        raise TypingError(wmcvz__wcd.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        wmcvz__wcd = 'Dict.value_type cannot be of type {}'
        raise TypingError(wmcvz__wcd.format(valty))
    self.key_type = keyty
    self.value_type = valty
    self.keyvalue_type = Tuple([keyty, valty])
    name = '{}[{},{}]<iv={}>'.format(self.__class__.__name__, keyty, valty,
        initial_value)
    super(DictType, self).__init__(name)
    InitialValue.__init__(self, initial_value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.DictType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '475acd71224bd51526750343246e064ff071320c0d10c17b8b8ac81d5070d094':
        warnings.warn('DictType.__init__ has changed')
numba.core.types.containers.DictType.__init__ = DictType__init__


def _legalize_arg_types(self, args):
    for i, a in enumerate(args, start=1):
        if isinstance(a, types.Dispatcher):
            msg = (
                'Does not support function type inputs into with-context for arg {}'
                )
            raise errors.TypingError(msg.format(i))


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.ObjModeLiftedWith.
        _legalize_arg_types)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4793f44ebc7da8843e8f298e08cd8a5428b4b84b89fd9d5c650273fdb8fee5ee':
        warnings.warn('ObjModeLiftedWith._legalize_arg_types has changed')
numba.core.dispatcher.ObjModeLiftedWith._legalize_arg_types = (
    _legalize_arg_types)


def _overload_template_get_impl(self, args, kws):
    otpv__keyf = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[otpv__keyf]
        return impl, args
    except KeyError as xbl__twf:
        pass
    impl, args = self._build_impl(otpv__keyf, args, kws)
    return impl, args


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate._get_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4e27d07b214ca16d6e8ed88f70d886b6b095e160d8f77f8df369dd4ed2eb3fae':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate._get_impl has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate._get_impl = (
    _overload_template_get_impl)


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        lwov__zwdhk = find_topo_order(parfor.loop_body)
    qqhik__rbm = lwov__zwdhk[0]
    team__hmc = {}
    _update_parfor_get_setitems(parfor.loop_body[qqhik__rbm].body, parfor.
        index_var, alias_map, team__hmc, lives_n_aliases)
    uub__fwplv = set(team__hmc.keys())
    for rwy__cjm in lwov__zwdhk:
        if rwy__cjm == qqhik__rbm:
            continue
        for stmt in parfor.loop_body[rwy__cjm].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            tom__uxvvu = set(wktxs__azm.name for wktxs__azm in stmt.list_vars()
                )
            zzbsg__ypx = tom__uxvvu & uub__fwplv
            for a in zzbsg__ypx:
                team__hmc.pop(a, None)
    for rwy__cjm in lwov__zwdhk:
        if rwy__cjm == qqhik__rbm:
            continue
        block = parfor.loop_body[rwy__cjm]
        jzy__oegmg = team__hmc.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            jzy__oegmg, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    kfyt__kkkpp = max(blocks.keys())
    gkv__fjq, rkb__qmwv = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    cfpml__xnsso = ir.Jump(gkv__fjq, ir.Loc('parfors_dummy', -1))
    blocks[kfyt__kkkpp].body.append(cfpml__xnsso)
    wbpr__wxbrh = compute_cfg_from_blocks(blocks)
    qab__frps = compute_use_defs(blocks)
    lfjf__cie = compute_live_map(wbpr__wxbrh, blocks, qab__frps.usemap,
        qab__frps.defmap)
    alias_set = set(alias_map.keys())
    for cbqkh__hhzu, block in blocks.items():
        lzzii__ynzte = []
        rih__veyqr = {wktxs__azm.name for wktxs__azm in block.terminator.
            list_vars()}
        for bngk__qordb, lwrt__zmhfg in wbpr__wxbrh.successors(cbqkh__hhzu):
            rih__veyqr |= lfjf__cie[bngk__qordb]
        for stmt in reversed(block.body):
            erljc__krpt = rih__veyqr & alias_set
            for wktxs__azm in erljc__krpt:
                rih__veyqr |= alias_map[wktxs__azm]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in rih__veyqr and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                gbyu__ogs = guard(find_callname, func_ir, stmt.value)
                if gbyu__ogs == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in rih__veyqr and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            rih__veyqr |= {wktxs__azm.name for wktxs__azm in stmt.list_vars()}
            lzzii__ynzte.append(stmt)
        lzzii__ynzte.reverse()
        block.body = lzzii__ynzte
    typemap.pop(rkb__qmwv.name)
    blocks[kfyt__kkkpp].body.pop()

    def trim_empty_parfor_branches(parfor):
        wxdgj__olvg = False
        blocks = parfor.loop_body.copy()
        for cbqkh__hhzu, block in blocks.items():
            if len(block.body):
                ztcb__tgs = block.body[-1]
                if isinstance(ztcb__tgs, ir.Branch):
                    if len(blocks[ztcb__tgs.truebr].body) == 1 and len(blocks
                        [ztcb__tgs.falsebr].body) == 1:
                        oitqz__lybw = blocks[ztcb__tgs.truebr].body[0]
                        pbs__iszp = blocks[ztcb__tgs.falsebr].body[0]
                        if isinstance(oitqz__lybw, ir.Jump) and isinstance(
                            pbs__iszp, ir.Jump
                            ) and oitqz__lybw.target == pbs__iszp.target:
                            parfor.loop_body[cbqkh__hhzu].body[-1] = ir.Jump(
                                oitqz__lybw.target, ztcb__tgs.loc)
                            wxdgj__olvg = True
                    elif len(blocks[ztcb__tgs.truebr].body) == 1:
                        oitqz__lybw = blocks[ztcb__tgs.truebr].body[0]
                        if isinstance(oitqz__lybw, ir.Jump
                            ) and oitqz__lybw.target == ztcb__tgs.falsebr:
                            parfor.loop_body[cbqkh__hhzu].body[-1] = ir.Jump(
                                oitqz__lybw.target, ztcb__tgs.loc)
                            wxdgj__olvg = True
                    elif len(blocks[ztcb__tgs.falsebr].body) == 1:
                        pbs__iszp = blocks[ztcb__tgs.falsebr].body[0]
                        if isinstance(pbs__iszp, ir.Jump
                            ) and pbs__iszp.target == ztcb__tgs.truebr:
                            parfor.loop_body[cbqkh__hhzu].body[-1] = ir.Jump(
                                pbs__iszp.target, ztcb__tgs.loc)
                            wxdgj__olvg = True
        return wxdgj__olvg
    wxdgj__olvg = True
    while wxdgj__olvg:
        """
        Process parfor body recursively.
        Note that this is the only place in this function that uses the
        argument lives instead of lives_n_aliases.  The former does not
        include the aliases of live variables but only the live variable
        names themselves.  See a comment in this function for how that
        is used.
        """
        remove_dead_parfor_recursive(parfor, lives, arg_aliases, alias_map,
            func_ir, typemap)
        simplify_parfor_body_CFG(func_ir.blocks)
        wxdgj__olvg = trim_empty_parfor_branches(parfor)
    mwzc__god = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        mwzc__god &= len(block.body) == 0
    if mwzc__god:
        return None
    return parfor


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.remove_dead_parfor)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1c9b008a7ead13e988e1efe67618d8f87f0b9f3d092cc2cd6bfcd806b1fdb859':
        warnings.warn('remove_dead_parfor has changed')
numba.parfors.parfor.remove_dead_parfor = remove_dead_parfor
numba.core.ir_utils.remove_dead_extensions[numba.parfors.parfor.Parfor
    ] = remove_dead_parfor


def simplify_parfor_body_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import simplify_CFG
    from numba.parfors.parfor import Parfor
    phizz__zcwy = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                phizz__zcwy += 1
                parfor = stmt
                bsg__ewgdd = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = bsg__ewgdd.scope
                loc = ir.Loc('parfors_dummy', -1)
                lcju__wah = ir.Var(scope, mk_unique_var('$const'), loc)
                bsg__ewgdd.body.append(ir.Assign(ir.Const(0, loc),
                    lcju__wah, loc))
                bsg__ewgdd.body.append(ir.Return(lcju__wah, loc))
                wbpr__wxbrh = compute_cfg_from_blocks(parfor.loop_body)
                for lkw__rrsc in wbpr__wxbrh.dead_nodes():
                    del parfor.loop_body[lkw__rrsc]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                bsg__ewgdd = parfor.loop_body[max(parfor.loop_body.keys())]
                bsg__ewgdd.body.pop()
                bsg__ewgdd.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return phizz__zcwy


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def _lifted_compile(self, sig):
    import numba.core.event as ev
    from numba.core import compiler, sigutils
    from numba.core.compiler_lock import global_compiler_lock
    from numba.core.ir_utils import remove_dels
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        with self._compiling_counter:
            flags = self.flags
            args, return_type = sigutils.normalize_signature(sig)
            kgd__lsswr = self.overloads.get(tuple(args))
            if kgd__lsswr is not None:
                return kgd__lsswr.entry_point
            self._pre_compile(args, return_type, flags)
            nrm__ebayx = self.func_ir
            whgh__xwm = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=whgh__xwm):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=nrm__ebayx, args=args,
                    return_type=return_type, flags=flags, locals=self.
                    locals, lifted=(), lifted_from=self.lifted_from,
                    is_lifted_loop=True)
                if cres.typing_error is not None and not flags.enable_pyobject:
                    raise cres.typing_error
                self.add_overload(cres)
            remove_dels(self.func_ir.blocks)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.LiftedCode.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1351ebc5d8812dc8da167b30dad30eafb2ca9bf191b49aaed6241c21e03afff1':
        warnings.warn('numba.core.dispatcher.LiftedCode.compile has changed')
numba.core.dispatcher.LiftedCode.compile = _lifted_compile


def compile_ir(typingctx, targetctx, func_ir, args, return_type, flags,
    locals, lifted=(), lifted_from=None, is_lifted_loop=False, library=None,
    pipeline_class=Compiler):
    if is_lifted_loop:
        qtx__gkl = copy.deepcopy(flags)
        qtx__gkl.no_rewrites = True

        def compile_local(the_ir, the_flags):
            ydgtr__jivn = pipeline_class(typingctx, targetctx, library,
                args, return_type, the_flags, locals)
            return ydgtr__jivn.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        zqb__jkjhh = compile_local(func_ir, qtx__gkl)
        gojj__icpi = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    gojj__icpi = compile_local(func_ir, flags)
                except Exception as xbl__twf:
                    pass
        if gojj__icpi is not None:
            cres = gojj__icpi
        else:
            cres = zqb__jkjhh
        return cres
    else:
        ydgtr__jivn = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return ydgtr__jivn.compile_ir(func_ir=func_ir, lifted=lifted,
            lifted_from=lifted_from)


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.compile_ir)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c48ce5493f4c43326e8cbdd46f3ea038b2b9045352d9d25894244798388e5e5b':
        warnings.warn('numba.core.compiler.compile_ir has changed')
numba.core.compiler.compile_ir = compile_ir


def make_constant_array(self, builder, typ, ary):
    import math
    from llvmlite import ir as lir
    xirar__lblj = self.get_data_type(typ.dtype)
    utpph__wcjxv = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        utpph__wcjxv):
        lwm__kxjg = ary.ctypes.data
        qxk__zru = self.add_dynamic_addr(builder, lwm__kxjg, info=str(type(
            lwm__kxjg)))
        wfn__jvd = self.add_dynamic_addr(builder, id(ary), info=str(type(ary)))
        self.global_arrays.append(ary)
    else:
        osd__ghib = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            osd__ghib = osd__ghib.view('int64')
        val = bytearray(osd__ghib.data)
        kxst__lod = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        qxk__zru = cgutils.global_constant(builder, '.const.array.data',
            kxst__lod)
        qxk__zru.align = self.get_abi_alignment(xirar__lblj)
        wfn__jvd = None
    pxf__nmlo = self.get_value_type(types.intp)
    ltpw__ldfh = [self.get_constant(types.intp, uztg__btvy) for uztg__btvy in
        ary.shape]
    jslaw__uzjko = lir.Constant(lir.ArrayType(pxf__nmlo, len(ltpw__ldfh)),
        ltpw__ldfh)
    ruh__pekv = [self.get_constant(types.intp, uztg__btvy) for uztg__btvy in
        ary.strides]
    jqx__wpqra = lir.Constant(lir.ArrayType(pxf__nmlo, len(ruh__pekv)),
        ruh__pekv)
    niar__bdkkh = self.get_constant(types.intp, ary.dtype.itemsize)
    rxkri__agz = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        rxkri__agz, niar__bdkkh, qxk__zru.bitcast(self.get_value_type(types
        .CPointer(typ.dtype))), jslaw__uzjko, jqx__wpqra])


if _check_numba_change:
    lines = inspect.getsource(numba.core.base.BaseContext.make_constant_array)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5721b5360b51f782f79bd794f7bf4d48657911ecdc05c30db22fd55f15dad821':
        warnings.warn(
            'numba.core.base.BaseContext.make_constant_array has changed')
numba.core.base.BaseContext.make_constant_array = make_constant_array


def _define_atomic_inc_dec(module, op, ordering):
    from llvmlite import ir as lir
    from numba.core.runtime.nrtdynmod import _word_type
    fzg__kcx = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    nyl__enb = lir.Function(module, fzg__kcx, name='nrt_atomic_{0}'.format(op))
    [auh__elrd] = nyl__enb.args
    jla__dxxnr = nyl__enb.append_basic_block()
    builder = lir.IRBuilder(jla__dxxnr)
    pwu__mbgs = lir.Constant(_word_type, 1)
    if False:
        brp__rjzro = builder.atomic_rmw(op, auh__elrd, pwu__mbgs, ordering=
            ordering)
        res = getattr(builder, op)(brp__rjzro, pwu__mbgs)
        builder.ret(res)
    else:
        brp__rjzro = builder.load(auh__elrd)
        ifz__onkz = getattr(builder, op)(brp__rjzro, pwu__mbgs)
        zrjw__qcus = builder.icmp_signed('!=', brp__rjzro, lir.Constant(
            brp__rjzro.type, -1))
        with cgutils.if_likely(builder, zrjw__qcus):
            builder.store(ifz__onkz, auh__elrd)
        builder.ret(ifz__onkz)
    return nyl__enb


if _check_numba_change:
    lines = inspect.getsource(numba.core.runtime.nrtdynmod.
        _define_atomic_inc_dec)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9cc02c532b2980b6537b702f5608ea603a1ff93c6d3c785ae2cf48bace273f48':
        warnings.warn(
            'numba.core.runtime.nrtdynmod._define_atomic_inc_dec has changed')
numba.core.runtime.nrtdynmod._define_atomic_inc_dec = _define_atomic_inc_dec


def NativeLowering_run_pass(self, state):
    from llvmlite import binding as llvm
    from numba.core import funcdesc, lowering
    from numba.core.typed_passes import fallback_context
    if state.library is None:
        naquc__vexal = state.targetctx.codegen()
        state.library = naquc__vexal.create_library(state.func_id.func_qualname
            )
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    yvmo__xipzj = state.func_ir
    typemap = state.typemap
    aaet__htp = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    kml__kzcz = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            yvmo__xipzj, typemap, aaet__htp, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            ekpjz__kzguh = lowering.Lower(targetctx, library, fndesc,
                yvmo__xipzj, metadata=metadata)
            ekpjz__kzguh.lower()
            if not flags.no_cpython_wrapper:
                ekpjz__kzguh.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(aaet__htp, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        ekpjz__kzguh.create_cfunc_wrapper()
            env = ekpjz__kzguh.env
            slqa__rxica = ekpjz__kzguh.call_helper
            del ekpjz__kzguh
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, slqa__rxica, cfunc=None, env=env
                )
        else:
            vfjl__mqc = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(vfjl__mqc, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, slqa__rxica, cfunc=vfjl__mqc,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        mgrct__ccqiu = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = mgrct__ccqiu - kml__kzcz
        metadata['llvm_pass_timings'] = library.recorded_timings
    return True


if _check_numba_change:
    lines = inspect.getsource(numba.core.typed_passes.NativeLowering.run_pass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a777ce6ce1bb2b1cbaa3ac6c2c0e2adab69a9c23888dff5f1cbb67bfb176b5de':
        warnings.warn(
            'numba.core.typed_passes.NativeLowering.run_pass has changed')
numba.core.typed_passes.NativeLowering.run_pass = NativeLowering_run_pass


def _python_list_to_native(typ, obj, c, size, listptr, errorptr):
    from llvmlite import ir as lir
    from numba.core.boxing import _NumbaTypeHelper
    from numba.cpython import listobj

    def check_element_type(nth, itemobj, expected_typobj):
        dcrf__uit = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, dcrf__uit),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            xtw__xufps.do_break()
        xzv__ohx = c.builder.icmp_signed('!=', dcrf__uit, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(xzv__ohx, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, dcrf__uit)
                c.pyapi.decref(dcrf__uit)
                xtw__xufps.do_break()
        c.pyapi.decref(dcrf__uit)
    lru__ligj, list = listobj.ListInstance.allocate_ex(c.context, c.builder,
        typ, size)
    with c.builder.if_else(lru__ligj, likely=True) as (efle__eorg, voxzv__idcph
        ):
        with efle__eorg:
            list.size = size
            wxwim__nwcac = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                wxwim__nwcac), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        wxwim__nwcac))
                    with cgutils.for_range(c.builder, size) as xtw__xufps:
                        itemobj = c.pyapi.list_getitem(obj, xtw__xufps.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        wwd__qed = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(wwd__qed.is_error, likely=False
                            ):
                            c.builder.store(cgutils.true_bit, errorptr)
                            xtw__xufps.do_break()
                        list.setitem(xtw__xufps.index, wwd__qed.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with voxzv__idcph:
            c.builder.store(cgutils.true_bit, errorptr)
    with c.builder.if_then(c.builder.load(errorptr)):
        c.context.nrt.decref(c.builder, typ, list.value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.boxing._python_list_to_native)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f8e546df8b07adfe74a16b6aafb1d4fddbae7d3516d7944b3247cc7c9b7ea88a':
        warnings.warn('numba.core.boxing._python_list_to_native has changed')
numba.core.boxing._python_list_to_native = _python_list_to_native


def make_string_from_constant(context, builder, typ, literal_string):
    from llvmlite import ir as lir
    from numba.cpython.hashing import _Py_hash_t
    from numba.cpython.unicode import compile_time_get_string_data
    hpagr__nurhe, uwvza__qvp, exyuz__kdya, iufk__ifgdt, gcr__cua = (
        compile_time_get_string_data(literal_string))
    upg__ysleb = builder.module
    gv = context.insert_const_bytes(upg__ysleb, hpagr__nurhe)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        uwvza__qvp), context.get_constant(types.int32, exyuz__kdya),
        context.get_constant(types.uint32, iufk__ifgdt), context.
        get_constant(_Py_hash_t, -1), context.get_constant_null(types.
        MemInfoPointer(types.voidptr)), context.get_constant_null(types.
        pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    kcqhu__ynh = None
    if isinstance(shape, types.Integer):
        kcqhu__ynh = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(uztg__btvy, (types.Integer, types.IntEnumMember)) for
            uztg__btvy in shape):
            kcqhu__ynh = len(shape)
    return kcqhu__ynh


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.parse_shape)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e62e3ff09d36df5ac9374055947d6a8be27160ce32960d3ef6cb67f89bd16429':
        warnings.warn('numba.core.typing.npydecl.parse_shape has changed')
numba.core.typing.npydecl.parse_shape = parse_shape


def _get_names(self, obj):
    if isinstance(obj, ir.Var) or isinstance(obj, str):
        name = obj if isinstance(obj, str) else obj.name
        if name not in self.typemap:
            return name,
        typ = self.typemap[name]
        if isinstance(typ, (types.BaseTuple, types.ArrayCompatible)):
            kcqhu__ynh = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if kcqhu__ynh == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(kcqhu__ynh)
                    )
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            iyqcz__oqai = self._get_names(x)
            if len(iyqcz__oqai) != 0:
                return iyqcz__oqai[0]
            return iyqcz__oqai
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    iyqcz__oqai = self._get_names(obj)
    if len(iyqcz__oqai) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(iyqcz__oqai[0])


def get_equiv_set(self, obj):
    iyqcz__oqai = self._get_names(obj)
    if len(iyqcz__oqai) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(iyqcz__oqai[0])


if _check_numba_change:
    for name, orig, new, hash in ((
        'numba.parfors.array_analysis.ShapeEquivSet._get_names', numba.
        parfors.array_analysis.ShapeEquivSet._get_names, _get_names,
        '8c9bf136109028d5445fd0a82387b6abeb70c23b20b41e2b50c34ba5359516ee'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const',
        numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const,
        get_equiv_const,
        'bef410ca31a9e29df9ee74a4a27d339cc332564e4a237828b8a4decf625ce44e'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set', numba.
        parfors.array_analysis.ShapeEquivSet.get_equiv_set, get_equiv_set,
        'ec936d340c488461122eb74f28a28b88227cb1f1bca2b9ba3c19258cfe1eb40a')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
numba.parfors.array_analysis.ShapeEquivSet._get_names = _get_names
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const = get_equiv_const
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set = get_equiv_set


def raise_on_unsupported_feature(func_ir, typemap):
    import numpy
    mdr__gbzqd = []
    for ilgsk__zvl in func_ir.arg_names:
        if ilgsk__zvl in typemap and isinstance(typemap[ilgsk__zvl], types.
            containers.UniTuple) and typemap[ilgsk__zvl].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(ilgsk__zvl))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for rghxb__kuqb in func_ir.blocks.values():
        for stmt in rghxb__kuqb.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    sdc__oyaqg = getattr(val, 'code', None)
                    if sdc__oyaqg is not None:
                        if getattr(val, 'closure', None) is not None:
                            anhvs__hot = '<creating a function from a closure>'
                            xeen__kstp = ''
                        else:
                            anhvs__hot = sdc__oyaqg.co_name
                            xeen__kstp = '(%s) ' % anhvs__hot
                    else:
                        anhvs__hot = '<could not ascertain use case>'
                        xeen__kstp = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (anhvs__hot, xeen__kstp))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                mcqy__xqgbe = False
                if isinstance(val, pytypes.FunctionType):
                    mcqy__xqgbe = val in {numba.gdb, numba.gdb_init}
                if not mcqy__xqgbe:
                    mcqy__xqgbe = getattr(val, '_name', '') == 'gdb_internal'
                if mcqy__xqgbe:
                    mdr__gbzqd.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    wto__axw = func_ir.get_definition(var)
                    ykasg__tpy = guard(find_callname, func_ir, wto__axw)
                    if ykasg__tpy and ykasg__tpy[1] == 'numpy':
                        ty = getattr(numpy, ykasg__tpy[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    cmfb__wnlv = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(cmfb__wnlv), loc=stmt.loc)
            if isinstance(stmt.value, ir.Global):
                ty = typemap[stmt.target.name]
                msg = (
                    "The use of a %s type, assigned to variable '%s' in globals, is not supported as globals are considered compile-time constants and there is no known way to compile a %s type as a constant."
                    )
                if isinstance(ty, types.ListType):
                    raise TypingError(msg % (ty, stmt.value.name, ty), loc=
                        stmt.loc)
            if isinstance(stmt.value, ir.Yield) and not func_ir.is_generator:
                msg = 'The use of generator expressions is unsupported.'
                raise errors.UnsupportedError(msg, loc=stmt.loc)
    if len(mdr__gbzqd) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        cevp__awru = '\n'.join([x.strformat() for x in mdr__gbzqd])
        raise errors.UnsupportedError(msg % cevp__awru)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.raise_on_unsupported_feature)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '237a4fe8395a40899279c718bc3754102cd2577463ef2f48daceea78d79b2d5e':
        warnings.warn(
            'numba.core.ir_utils.raise_on_unsupported_feature has changed')
numba.core.ir_utils.raise_on_unsupported_feature = raise_on_unsupported_feature
numba.core.typed_passes.raise_on_unsupported_feature = (
    raise_on_unsupported_feature)


@typeof_impl.register(dict)
def _typeof_dict(val, c):
    if len(val) == 0:
        raise ValueError('Cannot type empty dict')
    rsjx__nrxf, wktxs__azm = next(iter(val.items()))
    mgq__iutl = typeof_impl(rsjx__nrxf, c)
    vszol__osett = typeof_impl(wktxs__azm, c)
    if mgq__iutl is None or vszol__osett is None:
        raise ValueError(
            f'Cannot type dict element type {type(rsjx__nrxf)}, {type(wktxs__azm)}'
            )
    return types.DictType(mgq__iutl, vszol__osett)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    ftujz__nft = cgutils.alloca_once_value(c.builder, val)
    iuex__mbk = c.pyapi.object_hasattr_string(val, '_opaque')
    dsqd__ekvrn = c.builder.icmp_unsigned('==', iuex__mbk, lir.Constant(
        iuex__mbk.type, 0))
    znel__sxi = typ.key_type
    tatmd__dgl = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(znel__sxi, tatmd__dgl)

    def copy_dict(out_dict, in_dict):
        for rsjx__nrxf, wktxs__azm in in_dict.items():
            out_dict[rsjx__nrxf] = wktxs__azm
    with c.builder.if_then(dsqd__ekvrn):
        wjm__lwoot = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        bkgzh__bdqrc = c.pyapi.call_function_objargs(wjm__lwoot, [])
        kemi__gkls = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(kemi__gkls, [bkgzh__bdqrc, val])
        c.builder.store(bkgzh__bdqrc, ftujz__nft)
    val = c.builder.load(ftujz__nft)
    huwyf__rjaa = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    wzbd__tiq = c.pyapi.object_type(val)
    jst__vjrdj = c.builder.icmp_unsigned('==', wzbd__tiq, huwyf__rjaa)
    with c.builder.if_else(jst__vjrdj) as (zamv__tbq, zlnpf__jox):
        with zamv__tbq:
            gyw__ylqw = c.pyapi.object_getattr_string(val, '_opaque')
            wfnfn__ctr = types.MemInfoPointer(types.voidptr)
            wwd__qed = c.unbox(wfnfn__ctr, gyw__ylqw)
            mi = wwd__qed.value
            wqn__mhw = wfnfn__ctr, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *wqn__mhw)
            fls__cmk = context.get_constant_null(wqn__mhw[1])
            args = mi, fls__cmk
            mruyd__nyzuo, zndmi__pvmf = c.pyapi.call_jit_code(convert, sig,
                args)
            c.context.nrt.decref(c.builder, typ, zndmi__pvmf)
            c.pyapi.decref(gyw__ylqw)
            unoym__hcht = c.builder.basic_block
        with zlnpf__jox:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", wzbd__tiq, huwyf__rjaa)
            ohxp__gxvdb = c.builder.basic_block
    mkxw__xsshs = c.builder.phi(zndmi__pvmf.type)
    xap__mehlu = c.builder.phi(mruyd__nyzuo.type)
    mkxw__xsshs.add_incoming(zndmi__pvmf, unoym__hcht)
    mkxw__xsshs.add_incoming(zndmi__pvmf.type(None), ohxp__gxvdb)
    xap__mehlu.add_incoming(mruyd__nyzuo, unoym__hcht)
    xap__mehlu.add_incoming(cgutils.true_bit, ohxp__gxvdb)
    c.pyapi.decref(huwyf__rjaa)
    c.pyapi.decref(wzbd__tiq)
    with c.builder.if_then(dsqd__ekvrn):
        c.pyapi.decref(val)
    return NativeValue(mkxw__xsshs, is_error=xap__mehlu)


import numba.typed.typeddict
if _check_numba_change:
    lines = inspect.getsource(numba.core.pythonapi._unboxers.functions[
        numba.core.types.DictType])
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5f6f183b94dc57838538c668a54c2476576c85d8553843f3219f5162c61e7816':
        warnings.warn('unbox_dicttype has changed')
numba.core.pythonapi._unboxers.functions[types.DictType] = unbox_dicttype


def op_DICT_UPDATE_byteflow(self, state, inst):
    value = state.pop()
    index = inst.arg
    target = state.peek(index)
    updatevar = state.make_temp()
    res = state.make_temp()
    state.append(inst, target=target, value=value, updatevar=updatevar, res=res
        )


if _check_numba_change:
    if hasattr(numba.core.byteflow.TraceRunner, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_DICT_UPDATE has changed')
numba.core.byteflow.TraceRunner.op_DICT_UPDATE = op_DICT_UPDATE_byteflow


def op_DICT_UPDATE_interpreter(self, inst, target, value, updatevar, res):
    from numba.core import ir
    target = self.get(target)
    value = self.get(value)
    xyz__pqdtg = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=xyz__pqdtg, name=updatevar)
    pbqkw__yvfet = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc
        )
    self.store(value=pbqkw__yvfet, name=res)


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_DICT_UPDATE has changed')
numba.core.interpreter.Interpreter.op_DICT_UPDATE = op_DICT_UPDATE_interpreter


@numba.extending.overload_method(numba.core.types.DictType, 'update')
def ol_dict_update(d, other):
    if not isinstance(d, numba.core.types.DictType):
        return
    if not isinstance(other, numba.core.types.DictType):
        return

    def impl(d, other):
        for rsjx__nrxf, wktxs__azm in other.items():
            d[rsjx__nrxf] = wktxs__azm
    return impl


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'ol_dict_update'):
        warnings.warn('numba.typed.dictobject.ol_dict_update has changed')


def op_CALL_FUNCTION_EX_byteflow(self, state, inst):
    from numba.core.utils import PYVERSION
    if inst.arg & 1 and PYVERSION != (3, 10):
        errmsg = 'CALL_FUNCTION_EX with **kwargs not supported'
        raise errors.UnsupportedError(errmsg)
    if inst.arg & 1:
        varkwarg = state.pop()
    else:
        varkwarg = None
    vararg = state.pop()
    func = state.pop()
    res = state.make_temp()
    state.append(inst, func=func, vararg=vararg, varkwarg=varkwarg, res=res)
    state.push(res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.byteflow.TraceRunner.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '349e7cfd27f5dab80fe15a7728c5f098f3f225ba8512d84331e39d01e863c6d4':
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX has changed')
numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_byteflow)


def op_CALL_FUNCTION_EX_interpreter(self, inst, func, vararg, varkwarg, res):
    func = self.get(func)
    vararg = self.get(vararg)
    if varkwarg is not None:
        varkwarg = self.get(varkwarg)
    xeen__kstp = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(xeen__kstp, res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.interpreter.Interpreter.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84846e5318ab7ccc8f9abaae6ab9e0ca879362648196f9d4b0ffb91cf2e01f5d':
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX has changed'
            )
numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_interpreter)


@classmethod
def ir_expr_call(cls, func, args, kws, loc, vararg=None, varkwarg=None,
    target=None):
    assert isinstance(func, ir.Var)
    assert isinstance(loc, ir.Loc)
    op = 'call'
    return cls(op=op, loc=loc, func=func, args=args, kws=kws, vararg=vararg,
        varkwarg=varkwarg, target=target)


if _check_numba_change:
    lines = inspect.getsource(ir.Expr.call)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '665601d0548d4f648d454492e542cb8aa241107a8df6bc68d0eec664c9ada738':
        warnings.warn('ir.Expr.call has changed')
ir.Expr.call = ir_expr_call


@staticmethod
def define_untyped_pipeline(state, name='untyped'):
    from numba.core.compiler_machinery import PassManager
    from numba.core.untyped_passes import DeadBranchPrune, FindLiterallyCalls, FixupArgs, GenericRewrites, InlineClosureLikes, InlineInlinables, IRProcessing, LiteralPropagationSubPipelinePass, LiteralUnroll, MakeFunctionToJitFunction, ReconstructSSA, RewriteSemanticConstants, TranslateByteCode, WithLifting
    from numba.core.utils import PYVERSION
    psgpk__kmbn = PassManager(name)
    if state.func_ir is None:
        psgpk__kmbn.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            psgpk__kmbn.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        psgpk__kmbn.add_pass(FixupArgs, 'fix up args')
    psgpk__kmbn.add_pass(IRProcessing, 'processing IR')
    psgpk__kmbn.add_pass(WithLifting, 'Handle with contexts')
    psgpk__kmbn.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        psgpk__kmbn.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        psgpk__kmbn.add_pass(DeadBranchPrune, 'dead branch pruning')
        psgpk__kmbn.add_pass(GenericRewrites, 'nopython rewrites')
    psgpk__kmbn.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    psgpk__kmbn.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        psgpk__kmbn.add_pass(DeadBranchPrune, 'dead branch pruning')
    psgpk__kmbn.add_pass(FindLiterallyCalls, 'find literally calls')
    psgpk__kmbn.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        psgpk__kmbn.add_pass(ReconstructSSA, 'ssa')
    psgpk__kmbn.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    psgpk__kmbn.finalize()
    return psgpk__kmbn


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fc5a0665658cc30588a78aca984ac2d323d5d3a45dce538cc62688530c772896':
        warnings.warn(
            'numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline has changed'
            )
numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline = (
    define_untyped_pipeline)


def mul_list_generic(self, args, kws):
    a, rhmou__myow = args
    if isinstance(a, types.List) and isinstance(rhmou__myow, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(rhmou__myow, types.List):
        return signature(rhmou__myow, types.intp, rhmou__myow)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.listdecl.MulList.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '95882385a8ffa67aa576e8169b9ee6b3197e0ad3d5def4b47fa65ce8cd0f1575':
        warnings.warn('numba.core.typing.listdecl.MulList.generic has changed')
numba.core.typing.listdecl.MulList.generic = mul_list_generic


@lower_builtin(operator.mul, types.Integer, types.List)
def list_mul(context, builder, sig, args):
    from llvmlite import ir as lir
    from numba.core.imputils import impl_ret_new_ref
    from numba.cpython.listobj import ListInstance
    if isinstance(sig.args[0], types.List):
        djdp__svfip, lwlqs__shown = 0, 1
    else:
        djdp__svfip, lwlqs__shown = 1, 0
    rjhrt__bcwmj = ListInstance(context, builder, sig.args[djdp__svfip],
        args[djdp__svfip])
    vccrv__pbi = rjhrt__bcwmj.size
    yqx__vmtq = args[lwlqs__shown]
    wxwim__nwcac = lir.Constant(yqx__vmtq.type, 0)
    yqx__vmtq = builder.select(cgutils.is_neg_int(builder, yqx__vmtq),
        wxwim__nwcac, yqx__vmtq)
    rxkri__agz = builder.mul(yqx__vmtq, vccrv__pbi)
    iagju__mvi = ListInstance.allocate(context, builder, sig.return_type,
        rxkri__agz)
    iagju__mvi.size = rxkri__agz
    with cgutils.for_range_slice(builder, wxwim__nwcac, rxkri__agz,
        vccrv__pbi, inc=True) as (syowj__ienh, _):
        with cgutils.for_range(builder, vccrv__pbi) as xtw__xufps:
            value = rjhrt__bcwmj.getitem(xtw__xufps.index)
            iagju__mvi.setitem(builder.add(xtw__xufps.index, syowj__ienh),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, iagju__mvi.value
        )


def unify_pairs(self, first, second):
    from numba.core.typeconv import Conversion
    if first == second:
        return first
    if first is types.undefined:
        return second
    elif second is types.undefined:
        return first
    if first is types.unknown or second is types.unknown:
        return types.unknown
    ccb__pckz = first.unify(self, second)
    if ccb__pckz is not None:
        return ccb__pckz
    ccb__pckz = second.unify(self, first)
    if ccb__pckz is not None:
        return ccb__pckz
    wbbh__codc = self.can_convert(fromty=first, toty=second)
    if wbbh__codc is not None and wbbh__codc <= Conversion.safe:
        return second
    wbbh__codc = self.can_convert(fromty=second, toty=first)
    if wbbh__codc is not None and wbbh__codc <= Conversion.safe:
        return first
    if isinstance(first, types.Literal) or isinstance(second, types.Literal):
        first = types.unliteral(first)
        second = types.unliteral(second)
        return self.unify_pairs(first, second)
    return None


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.unify_pairs
        )
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f0eaf4cfdf1537691de26efd24d7e320f7c3f10d35e9aefe70cb946b3be0008c':
        warnings.warn(
            'numba.core.typing.context.BaseContext.unify_pairs has changed')
numba.core.typing.context.BaseContext.unify_pairs = unify_pairs


def _native_set_to_python_list(typ, payload, c):
    from llvmlite import ir
    rxkri__agz = payload.used
    listobj = c.pyapi.list_new(rxkri__agz)
    lru__ligj = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(lru__ligj, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(rxkri__agz
            .type, 0))
        with payload._iterate() as xtw__xufps:
            i = c.builder.load(index)
            item = xtw__xufps.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return lru__ligj, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    nxrsi__hzgqx = h.type
    rvkq__tcu = self.mask
    dtype = self._ty.dtype
    cumq__svmj = context.typing_context
    fnty = cumq__svmj.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(cumq__svmj, (dtype, dtype), {})
    aglo__zdret = context.get_function(fnty, sig)
    hhml__gxz = ir.Constant(nxrsi__hzgqx, 1)
    zog__oofl = ir.Constant(nxrsi__hzgqx, 5)
    ymbv__zexbp = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, rvkq__tcu))
    if for_insert:
        pid__mvuz = rvkq__tcu.type(-1)
        vdy__foox = cgutils.alloca_once_value(builder, pid__mvuz)
    digmg__ggdj = builder.append_basic_block('lookup.body')
    koyf__mfmx = builder.append_basic_block('lookup.found')
    the__itcz = builder.append_basic_block('lookup.not_found')
    rplk__xboj = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        dngkc__arv = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, dngkc__arv)):
            hkody__kejvh = aglo__zdret(builder, (item, entry.key))
            with builder.if_then(hkody__kejvh):
                builder.branch(koyf__mfmx)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, dngkc__arv)):
            builder.branch(the__itcz)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, dngkc__arv)):
                roy__mrpcb = builder.load(vdy__foox)
                roy__mrpcb = builder.select(builder.icmp_unsigned('==',
                    roy__mrpcb, pid__mvuz), i, roy__mrpcb)
                builder.store(roy__mrpcb, vdy__foox)
    with cgutils.for_range(builder, ir.Constant(nxrsi__hzgqx, numba.cpython
        .setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, hhml__gxz)
        i = builder.and_(i, rvkq__tcu)
        builder.store(i, index)
    builder.branch(digmg__ggdj)
    with builder.goto_block(digmg__ggdj):
        i = builder.load(index)
        check_entry(i)
        yjfep__tucx = builder.load(ymbv__zexbp)
        yjfep__tucx = builder.lshr(yjfep__tucx, zog__oofl)
        i = builder.add(hhml__gxz, builder.mul(i, zog__oofl))
        i = builder.and_(rvkq__tcu, builder.add(i, yjfep__tucx))
        builder.store(i, index)
        builder.store(yjfep__tucx, ymbv__zexbp)
        builder.branch(digmg__ggdj)
    with builder.goto_block(the__itcz):
        if for_insert:
            i = builder.load(index)
            roy__mrpcb = builder.load(vdy__foox)
            i = builder.select(builder.icmp_unsigned('==', roy__mrpcb,
                pid__mvuz), i, roy__mrpcb)
            builder.store(i, index)
        builder.branch(rplk__xboj)
    with builder.goto_block(koyf__mfmx):
        builder.branch(rplk__xboj)
    builder.position_at_end(rplk__xboj)
    mcqy__xqgbe = builder.phi(ir.IntType(1), 'found')
    mcqy__xqgbe.add_incoming(cgutils.true_bit, koyf__mfmx)
    mcqy__xqgbe.add_incoming(cgutils.false_bit, the__itcz)
    return mcqy__xqgbe, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    utwiy__qvkp = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    lrc__ofv = payload.used
    hhml__gxz = ir.Constant(lrc__ofv.type, 1)
    lrc__ofv = payload.used = builder.add(lrc__ofv, hhml__gxz)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, utwiy__qvkp), likely=True):
        payload.fill = builder.add(payload.fill, hhml__gxz)
    if do_resize:
        self.upsize(lrc__ofv)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    mcqy__xqgbe, i = payload._lookup(item, h, for_insert=True)
    fhrg__deju = builder.not_(mcqy__xqgbe)
    with builder.if_then(fhrg__deju):
        entry = payload.get_entry(i)
        utwiy__qvkp = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        lrc__ofv = payload.used
        hhml__gxz = ir.Constant(lrc__ofv.type, 1)
        lrc__ofv = payload.used = builder.add(lrc__ofv, hhml__gxz)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, utwiy__qvkp), likely=True):
            payload.fill = builder.add(payload.fill, hhml__gxz)
        if do_resize:
            self.upsize(lrc__ofv)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    lrc__ofv = payload.used
    hhml__gxz = ir.Constant(lrc__ofv.type, 1)
    lrc__ofv = payload.used = self._builder.sub(lrc__ofv, hhml__gxz)
    if do_resize:
        self.downsize(lrc__ofv)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    vddp__bmjl = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, vddp__bmjl)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    drgl__aszm = payload
    lru__ligj = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(lru__ligj), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with drgl__aszm._iterate() as xtw__xufps:
        entry = xtw__xufps.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(drgl__aszm.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as xtw__xufps:
        entry = xtw__xufps.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    lru__ligj = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(lru__ligj), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    lru__ligj = cgutils.alloca_once_value(builder, cgutils.true_bit)
    nxrsi__hzgqx = context.get_value_type(types.intp)
    wxwim__nwcac = ir.Constant(nxrsi__hzgqx, 0)
    hhml__gxz = ir.Constant(nxrsi__hzgqx, 1)
    ekr__dcz = context.get_data_type(types.SetPayload(self._ty))
    cuchw__xmt = context.get_abi_sizeof(ekr__dcz)
    djmbb__eyeei = self._entrysize
    cuchw__xmt -= djmbb__eyeei
    rmtrj__naxsh, snp__cak = cgutils.muladd_with_overflow(builder, nentries,
        ir.Constant(nxrsi__hzgqx, djmbb__eyeei), ir.Constant(nxrsi__hzgqx,
        cuchw__xmt))
    with builder.if_then(snp__cak, likely=False):
        builder.store(cgutils.false_bit, lru__ligj)
    with builder.if_then(builder.load(lru__ligj), likely=True):
        if realloc:
            nvc__fofm = self._set.meminfo
            auh__elrd = context.nrt.meminfo_varsize_alloc(builder,
                nvc__fofm, size=rmtrj__naxsh)
            vqsc__ywcc = cgutils.is_null(builder, auh__elrd)
        else:
            gulou__qnapq = _imp_dtor(context, builder.module, self._ty)
            nvc__fofm = context.nrt.meminfo_new_varsize_dtor(builder,
                rmtrj__naxsh, builder.bitcast(gulou__qnapq, cgutils.voidptr_t))
            vqsc__ywcc = cgutils.is_null(builder, nvc__fofm)
        with builder.if_else(vqsc__ywcc, likely=False) as (fncz__guukk,
            efle__eorg):
            with fncz__guukk:
                builder.store(cgutils.false_bit, lru__ligj)
            with efle__eorg:
                if not realloc:
                    self._set.meminfo = nvc__fofm
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, rmtrj__naxsh, 255)
                payload.used = wxwim__nwcac
                payload.fill = wxwim__nwcac
                payload.finger = wxwim__nwcac
                tlgq__fxg = builder.sub(nentries, hhml__gxz)
                payload.mask = tlgq__fxg
    return builder.load(lru__ligj)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    lru__ligj = cgutils.alloca_once_value(builder, cgutils.true_bit)
    nxrsi__hzgqx = context.get_value_type(types.intp)
    wxwim__nwcac = ir.Constant(nxrsi__hzgqx, 0)
    hhml__gxz = ir.Constant(nxrsi__hzgqx, 1)
    ekr__dcz = context.get_data_type(types.SetPayload(self._ty))
    cuchw__xmt = context.get_abi_sizeof(ekr__dcz)
    djmbb__eyeei = self._entrysize
    cuchw__xmt -= djmbb__eyeei
    rvkq__tcu = src_payload.mask
    nentries = builder.add(hhml__gxz, rvkq__tcu)
    rmtrj__naxsh = builder.add(ir.Constant(nxrsi__hzgqx, cuchw__xmt),
        builder.mul(ir.Constant(nxrsi__hzgqx, djmbb__eyeei), nentries))
    with builder.if_then(builder.load(lru__ligj), likely=True):
        gulou__qnapq = _imp_dtor(context, builder.module, self._ty)
        nvc__fofm = context.nrt.meminfo_new_varsize_dtor(builder,
            rmtrj__naxsh, builder.bitcast(gulou__qnapq, cgutils.voidptr_t))
        vqsc__ywcc = cgutils.is_null(builder, nvc__fofm)
        with builder.if_else(vqsc__ywcc, likely=False) as (fncz__guukk,
            efle__eorg):
            with fncz__guukk:
                builder.store(cgutils.false_bit, lru__ligj)
            with efle__eorg:
                self._set.meminfo = nvc__fofm
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = wxwim__nwcac
                payload.mask = rvkq__tcu
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, djmbb__eyeei)
                with src_payload._iterate() as xtw__xufps:
                    context.nrt.incref(builder, self._ty.dtype, xtw__xufps.
                        entry.key)
    return builder.load(lru__ligj)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    myw__ksrm = context.get_value_type(types.voidptr)
    gopzc__ldc = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [myw__ksrm, gopzc__ldc, myw__ksrm])
    tirhx__fjmy = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=tirhx__fjmy)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        cjzr__oezem = builder.bitcast(fn.args[0], cgutils.voidptr_t.
            as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, cjzr__oezem)
        with payload._iterate() as xtw__xufps:
            entry = xtw__xufps.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    crem__qft, = sig.args
    ehdbi__sjoy, = args
    qplqp__guk = numba.core.imputils.call_len(context, builder, crem__qft,
        ehdbi__sjoy)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, qplqp__guk)
    with numba.core.imputils.for_iter(context, builder, crem__qft, ehdbi__sjoy
        ) as xtw__xufps:
        inst.add(xtw__xufps.value)
        context.nrt.decref(builder, set_type.dtype, xtw__xufps.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    crem__qft = sig.args[1]
    ehdbi__sjoy = args[1]
    qplqp__guk = numba.core.imputils.call_len(context, builder, crem__qft,
        ehdbi__sjoy)
    if qplqp__guk is not None:
        cbzaw__iphsd = builder.add(inst.payload.used, qplqp__guk)
        inst.upsize(cbzaw__iphsd)
    with numba.core.imputils.for_iter(context, builder, crem__qft, ehdbi__sjoy
        ) as xtw__xufps:
        afaw__upnr = context.cast(builder, xtw__xufps.value, crem__qft.
            dtype, inst.dtype)
        inst.add(afaw__upnr)
        context.nrt.decref(builder, crem__qft.dtype, xtw__xufps.value)
    if qplqp__guk is not None:
        inst.downsize(inst.payload.used)
    return context.get_dummy_value()


if _check_numba_change:
    for name, orig, hash in ((
        'numba.core.boxing._native_set_to_python_list', numba.core.boxing.
        _native_set_to_python_list,
        'b47f3d5e582c05d80899ee73e1c009a7e5121e7a660d42cb518bb86933f3c06f'),
        ('numba.cpython.setobj._SetPayload._lookup', numba.cpython.setobj.
        _SetPayload._lookup,
        'c797b5399d7b227fe4eea3a058b3d3103f59345699388afb125ae47124bee395'),
        ('numba.cpython.setobj.SetInstance._add_entry', numba.cpython.
        setobj.SetInstance._add_entry,
        'c5ed28a5fdb453f242e41907cb792b66da2df63282c17abe0b68fc46782a7f94'),
        ('numba.cpython.setobj.SetInstance._add_key', numba.cpython.setobj.
        SetInstance._add_key,
        '324d6172638d02a361cfa0ca7f86e241e5a56a008d4ab581a305f9ae5ea4a75f'),
        ('numba.cpython.setobj.SetInstance._remove_entry', numba.cpython.
        setobj.SetInstance._remove_entry,
        '2c441b00daac61976e673c0e738e8e76982669bd2851951890dd40526fa14da1'),
        ('numba.cpython.setobj.SetInstance.pop', numba.cpython.setobj.
        SetInstance.pop,
        '1a7b7464cbe0577f2a38f3af9acfef6d4d25d049b1e216157275fbadaab41d1b'),
        ('numba.cpython.setobj.SetInstance._resize', numba.cpython.setobj.
        SetInstance._resize,
        '5ca5c2ba4f8c4bf546fde106b9c2656d4b22a16d16e163fb64c5d85ea4d88746'),
        ('numba.cpython.setobj.SetInstance._replace_payload', numba.cpython
        .setobj.SetInstance._replace_payload,
        'ada75a6c85828bff69c8469538c1979801f560a43fb726221a9c21bf208ae78d'),
        ('numba.cpython.setobj.SetInstance._allocate_payload', numba.
        cpython.setobj.SetInstance._allocate_payload,
        '2e80c419df43ebc71075b4f97fc1701c10dbc576aed248845e176b8d5829e61b'),
        ('numba.cpython.setobj.SetInstance._copy_payload', numba.cpython.
        setobj.SetInstance._copy_payload,
        '0885ac36e1eb5a0a0fc4f5d91e54b2102b69e536091fed9f2610a71d225193ec'),
        ('numba.cpython.setobj.set_constructor', numba.cpython.setobj.
        set_constructor,
        '3d521a60c3b8eaf70aa0f7267427475dfddd8f5e5053b5bfe309bb5f1891b0ce'),
        ('numba.cpython.setobj.set_update', numba.cpython.setobj.set_update,
        '965c4f7f7abcea5cbe0491b602e6d4bcb1800fa1ec39b1ffccf07e1bc56051c3')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.boxing._native_set_to_python_list = _native_set_to_python_list
numba.cpython.setobj._SetPayload._lookup = _lookup
numba.cpython.setobj.SetInstance._add_entry = _add_entry
numba.cpython.setobj.SetInstance._add_key = _add_key
numba.cpython.setobj.SetInstance._remove_entry = _remove_entry
numba.cpython.setobj.SetInstance.pop = pop
numba.cpython.setobj.SetInstance._resize = _resize
numba.cpython.setobj.SetInstance._replace_payload = _replace_payload
numba.cpython.setobj.SetInstance._allocate_payload = _allocate_payload
numba.cpython.setobj.SetInstance._copy_payload = _copy_payload


def _reduce(self):
    libdata = self.library.serialize_using_object_code()
    typeann = str(self.type_annotation)
    fndesc = self.fndesc
    fndesc.typemap = fndesc.calltypes = None
    referenced_envs = self._find_referenced_environments()
    yhm__wfgfr = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, yhm__wfgfr, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    vfjl__mqc = target_context.get_executable(library, fndesc, env)
    caq__lfdk = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=vfjl__mqc, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return caq__lfdk


if _check_numba_change:
    for name, orig, hash in (('numba.core.compiler.CompileResult._reduce',
        numba.core.compiler.CompileResult._reduce,
        '5f86eacfa5202c202b3dc200f1a7a9b6d3f9d1ec16d43a52cb2d580c34fbfa82'),
        ('numba.core.compiler.CompileResult._rebuild', numba.core.compiler.
        CompileResult._rebuild,
        '44fa9dc2255883ab49195d18c3cca8c0ad715d0dd02033bd7e2376152edc4e84')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.compiler.CompileResult._reduce = _reduce
numba.core.compiler.CompileResult._rebuild = _rebuild
