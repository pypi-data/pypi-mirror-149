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
    bmcsq__yuoz = numba.core.bytecode.FunctionIdentity.from_function(func)
    guxxx__xrpc = numba.core.interpreter.Interpreter(bmcsq__yuoz)
    bnio__vaicp = numba.core.bytecode.ByteCode(func_id=bmcsq__yuoz)
    func_ir = guxxx__xrpc.interpret(bnio__vaicp)
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
        gaf__kxgcj = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        gaf__kxgcj.run()
    wlftx__rayba = numba.core.postproc.PostProcessor(func_ir)
    wlftx__rayba.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, evjy__ktpr in visit_vars_extensions.items():
        if isinstance(stmt, t):
            evjy__ktpr(stmt, callback, cbdata)
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
    xln__kwd = ['ravel', 'transpose', 'reshape']
    for gcrb__ptvf in blocks.values():
        for fxzmw__axqop in gcrb__ptvf.body:
            if type(fxzmw__axqop) in alias_analysis_extensions:
                evjy__ktpr = alias_analysis_extensions[type(fxzmw__axqop)]
                evjy__ktpr(fxzmw__axqop, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(fxzmw__axqop, ir.Assign):
                ksh__mleh = fxzmw__axqop.value
                eml__fqbg = fxzmw__axqop.target.name
                if is_immutable_type(eml__fqbg, typemap):
                    continue
                if isinstance(ksh__mleh, ir.Var
                    ) and eml__fqbg != ksh__mleh.name:
                    _add_alias(eml__fqbg, ksh__mleh.name, alias_map,
                        arg_aliases)
                if isinstance(ksh__mleh, ir.Expr) and (ksh__mleh.op ==
                    'cast' or ksh__mleh.op in ['getitem', 'static_getitem']):
                    _add_alias(eml__fqbg, ksh__mleh.value.name, alias_map,
                        arg_aliases)
                if isinstance(ksh__mleh, ir.Expr
                    ) and ksh__mleh.op == 'inplace_binop':
                    _add_alias(eml__fqbg, ksh__mleh.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(ksh__mleh, ir.Expr
                    ) and ksh__mleh.op == 'getattr' and ksh__mleh.attr in ['T',
                    'ctypes', 'flat']:
                    _add_alias(eml__fqbg, ksh__mleh.value.name, alias_map,
                        arg_aliases)
                if isinstance(ksh__mleh, ir.Expr
                    ) and ksh__mleh.op == 'getattr' and ksh__mleh.attr not in [
                    'shape'] and ksh__mleh.value.name in arg_aliases:
                    _add_alias(eml__fqbg, ksh__mleh.value.name, alias_map,
                        arg_aliases)
                if isinstance(ksh__mleh, ir.Expr
                    ) and ksh__mleh.op == 'getattr' and ksh__mleh.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(eml__fqbg, ksh__mleh.value.name, alias_map,
                        arg_aliases)
                if isinstance(ksh__mleh, ir.Expr) and ksh__mleh.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(eml__fqbg, typemap):
                    for srd__bakys in ksh__mleh.items:
                        _add_alias(eml__fqbg, srd__bakys.name, alias_map,
                            arg_aliases)
                if isinstance(ksh__mleh, ir.Expr) and ksh__mleh.op == 'call':
                    dyal__ayui = guard(find_callname, func_ir, ksh__mleh,
                        typemap)
                    if dyal__ayui is None:
                        continue
                    wuyk__nugps, iuokm__ksvpx = dyal__ayui
                    if dyal__ayui in alias_func_extensions:
                        loyr__bbc = alias_func_extensions[dyal__ayui]
                        loyr__bbc(eml__fqbg, ksh__mleh.args, alias_map,
                            arg_aliases)
                    if iuokm__ksvpx == 'numpy' and wuyk__nugps in xln__kwd:
                        _add_alias(eml__fqbg, ksh__mleh.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(iuokm__ksvpx, ir.Var
                        ) and wuyk__nugps in xln__kwd:
                        _add_alias(eml__fqbg, iuokm__ksvpx.name, alias_map,
                            arg_aliases)
    fcv__mel = copy.deepcopy(alias_map)
    for srd__bakys in fcv__mel:
        for irn__nvk in fcv__mel[srd__bakys]:
            alias_map[srd__bakys] |= alias_map[irn__nvk]
        for irn__nvk in fcv__mel[srd__bakys]:
            alias_map[irn__nvk] = alias_map[srd__bakys]
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
    btdd__bak = compute_cfg_from_blocks(func_ir.blocks)
    iua__ifceg = compute_use_defs(func_ir.blocks)
    xkv__ond = compute_live_map(btdd__bak, func_ir.blocks, iua__ifceg.
        usemap, iua__ifceg.defmap)
    mvx__lry = True
    while mvx__lry:
        mvx__lry = False
        for rdznx__fysxz, block in func_ir.blocks.items():
            lives = {srd__bakys.name for srd__bakys in block.terminator.
                list_vars()}
            for xswdm__nsnzj, nhv__cdeg in btdd__bak.successors(rdznx__fysxz):
                lives |= xkv__ond[xswdm__nsnzj]
            liw__qismk = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    eml__fqbg = stmt.target
                    amr__qxksy = stmt.value
                    if eml__fqbg.name not in lives:
                        if isinstance(amr__qxksy, ir.Expr
                            ) and amr__qxksy.op == 'make_function':
                            continue
                        if isinstance(amr__qxksy, ir.Expr
                            ) and amr__qxksy.op == 'getattr':
                            continue
                        if isinstance(amr__qxksy, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(eml__fqbg,
                            None), types.Function):
                            continue
                        if isinstance(amr__qxksy, ir.Expr
                            ) and amr__qxksy.op == 'build_map':
                            continue
                        if isinstance(amr__qxksy, ir.Expr
                            ) and amr__qxksy.op == 'build_tuple':
                            continue
                    if isinstance(amr__qxksy, ir.Var
                        ) and eml__fqbg.name == amr__qxksy.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    vro__lrc = analysis.ir_extension_usedefs[type(stmt)]
                    ipvlm__awujz, qwtw__wbez = vro__lrc(stmt)
                    lives -= qwtw__wbez
                    lives |= ipvlm__awujz
                else:
                    lives |= {srd__bakys.name for srd__bakys in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(eml__fqbg.name)
                liw__qismk.append(stmt)
            liw__qismk.reverse()
            if len(block.body) != len(liw__qismk):
                mvx__lry = True
            block.body = liw__qismk


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    nchhe__oenxg = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (nchhe__oenxg,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    saxnu__eqec = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), saxnu__eqec)


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
            for klqvp__lllmt in fnty.templates:
                self._inline_overloads.update(klqvp__lllmt._inline_overloads)
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
    saxnu__eqec = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), saxnu__eqec)
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
    hjhrc__lzxr, wigie__ecllq = self._get_impl(args, kws)
    if hjhrc__lzxr is None:
        return
    bya__imslh = types.Dispatcher(hjhrc__lzxr)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        evd__tcv = hjhrc__lzxr._compiler
        flags = compiler.Flags()
        tbbaj__wnus = evd__tcv.targetdescr.typing_context
        iqgjj__ygh = evd__tcv.targetdescr.target_context
        ezmvv__fjdwx = evd__tcv.pipeline_class(tbbaj__wnus, iqgjj__ygh,
            None, None, None, flags, None)
        tpah__llgl = InlineWorker(tbbaj__wnus, iqgjj__ygh, evd__tcv.locals,
            ezmvv__fjdwx, flags, None)
        mbpt__dam = bya__imslh.dispatcher.get_call_template
        klqvp__lllmt, hzjmq__lyj, ngcho__wjrq, kws = mbpt__dam(wigie__ecllq,
            kws)
        if ngcho__wjrq in self._inline_overloads:
            return self._inline_overloads[ngcho__wjrq]['iinfo'].signature
        ir = tpah__llgl.run_untyped_passes(bya__imslh.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, iqgjj__ygh, ir, ngcho__wjrq, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, ngcho__wjrq, None)
        self._inline_overloads[sig.args] = {'folded_args': ngcho__wjrq}
        cdg__tpdpl = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = cdg__tpdpl
        if not self._inline.is_always_inline:
            sig = bya__imslh.get_call_type(self.context, wigie__ecllq, kws)
            self._compiled_overloads[sig.args] = bya__imslh.get_overload(sig)
        oyq__zey = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': ngcho__wjrq,
            'iinfo': oyq__zey}
    else:
        sig = bya__imslh.get_call_type(self.context, wigie__ecllq, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = bya__imslh.get_overload(sig)
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
    npugq__lxmwg = [True, False]
    glrwm__rbi = [False, True]
    edcs__ohx = _ResolutionFailures(context, self, args, kws, depth=self._depth
        )
    from numba.core.target_extension import get_local_target
    dqhs__fjqi = get_local_target(context)
    lnra__xupbm = utils.order_by_target_specificity(dqhs__fjqi, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for awwvt__tvo in lnra__xupbm:
        xuf__xax = awwvt__tvo(context)
        ainl__nvav = npugq__lxmwg if xuf__xax.prefer_literal else glrwm__rbi
        ainl__nvav = [True] if getattr(xuf__xax, '_no_unliteral', False
            ) else ainl__nvav
        for zfqkg__cbjt in ainl__nvav:
            try:
                if zfqkg__cbjt:
                    sig = xuf__xax.apply(args, kws)
                else:
                    yrsae__fkslw = tuple([_unlit_non_poison(a) for a in args])
                    cinp__uwqwb = {vgh__lbtqf: _unlit_non_poison(srd__bakys
                        ) for vgh__lbtqf, srd__bakys in kws.items()}
                    sig = xuf__xax.apply(yrsae__fkslw, cinp__uwqwb)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    edcs__ohx.add_error(xuf__xax, False, e, zfqkg__cbjt)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = xuf__xax.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    gcy__jqmar = getattr(xuf__xax, 'cases', None)
                    if gcy__jqmar is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            gcy__jqmar)
                    else:
                        msg = 'No match.'
                    edcs__ohx.add_error(xuf__xax, True, msg, zfqkg__cbjt)
    edcs__ohx.raise_error()


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
    klqvp__lllmt = self.template(context)
    qnofz__rmwo = None
    ehfr__kebr = None
    peucz__avrwg = None
    ainl__nvav = [True, False] if klqvp__lllmt.prefer_literal else [False, True
        ]
    ainl__nvav = [True] if getattr(klqvp__lllmt, '_no_unliteral', False
        ) else ainl__nvav
    for zfqkg__cbjt in ainl__nvav:
        if zfqkg__cbjt:
            try:
                peucz__avrwg = klqvp__lllmt.apply(args, kws)
            except Exception as dulkd__zsss:
                if isinstance(dulkd__zsss, errors.ForceLiteralArg):
                    raise dulkd__zsss
                qnofz__rmwo = dulkd__zsss
                peucz__avrwg = None
            else:
                break
        else:
            gzdhm__hqsuc = tuple([_unlit_non_poison(a) for a in args])
            fjvos__yfyzq = {vgh__lbtqf: _unlit_non_poison(srd__bakys) for 
                vgh__lbtqf, srd__bakys in kws.items()}
            zmqht__imc = gzdhm__hqsuc == args and kws == fjvos__yfyzq
            if not zmqht__imc and peucz__avrwg is None:
                try:
                    peucz__avrwg = klqvp__lllmt.apply(gzdhm__hqsuc,
                        fjvos__yfyzq)
                except Exception as dulkd__zsss:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        dulkd__zsss, errors.NumbaError):
                        raise dulkd__zsss
                    if isinstance(dulkd__zsss, errors.ForceLiteralArg):
                        if klqvp__lllmt.prefer_literal:
                            raise dulkd__zsss
                    ehfr__kebr = dulkd__zsss
                else:
                    break
    if peucz__avrwg is None and (ehfr__kebr is not None or qnofz__rmwo is not
        None):
        qrlb__sbbhm = '- Resolution failure for {} arguments:\n{}\n'
        dgrj__zuqn = _termcolor.highlight(qrlb__sbbhm)
        if numba.core.config.DEVELOPER_MODE:
            knw__ahwr = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    izkgw__ralh = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    izkgw__ralh = ['']
                kcb__nsf = '\n{}'.format(2 * knw__ahwr)
                nuai__rgwtz = _termcolor.reset(kcb__nsf + kcb__nsf.join(
                    _bt_as_lines(izkgw__ralh)))
                return _termcolor.reset(nuai__rgwtz)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            unjy__qdb = str(e)
            unjy__qdb = unjy__qdb if unjy__qdb else str(repr(e)) + add_bt(e)
            gdcy__edpba = errors.TypingError(textwrap.dedent(unjy__qdb))
            return dgrj__zuqn.format(literalness, str(gdcy__edpba))
        import bodo
        if isinstance(qnofz__rmwo, bodo.utils.typing.BodoError):
            raise qnofz__rmwo
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', qnofz__rmwo) +
                nested_msg('non-literal', ehfr__kebr))
        else:
            if 'missing a required argument' in qnofz__rmwo.msg:
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
            raise errors.TypingError(msg, loc=qnofz__rmwo.loc)
    return peucz__avrwg


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
    wuyk__nugps = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=wuyk__nugps)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            wfrg__gsp = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), wfrg__gsp)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    fxq__oieck = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            fxq__oieck.append(types.Omitted(a.value))
        else:
            fxq__oieck.append(self.typeof_pyval(a))
    qkghd__kgf = None
    try:
        error = None
        qkghd__kgf = self.compile(tuple(fxq__oieck))
    except errors.ForceLiteralArg as e:
        vrg__ggrzl = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if vrg__ggrzl:
            mmve__gmh = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            hwru__ynj = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(vrg__ggrzl))
            raise errors.CompilerError(mmve__gmh.format(hwru__ynj))
        wigie__ecllq = []
        try:
            for i, srd__bakys in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        wigie__ecllq.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        wigie__ecllq.append(types.literal(args[i]))
                else:
                    wigie__ecllq.append(args[i])
            args = wigie__ecllq
        except (OSError, FileNotFoundError) as safe__yjtu:
            error = FileNotFoundError(str(safe__yjtu) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                qkghd__kgf = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        awet__icqy = []
        for i, dtp__klru in enumerate(args):
            val = dtp__klru.value if isinstance(dtp__klru, numba.core.
                dispatcher.OmittedArg) else dtp__klru
            try:
                xmknk__prwfg = typeof(val, Purpose.argument)
            except ValueError as irk__qczx:
                awet__icqy.append((i, str(irk__qczx)))
            else:
                if xmknk__prwfg is None:
                    awet__icqy.append((i,
                        f'cannot determine Numba type of value {val}'))
        if awet__icqy:
            rpe__eoa = '\n'.join(f'- argument {i}: {ohumh__mizhd}' for i,
                ohumh__mizhd in awet__icqy)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{rpe__eoa}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                uuj__pajy = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                pbqvi__zut = False
                for demi__ushcr in uuj__pajy:
                    if demi__ushcr in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        pbqvi__zut = True
                        break
                if not pbqvi__zut:
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
                wfrg__gsp = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), wfrg__gsp)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return qkghd__kgf


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
    for mxerh__jpa in cres.library._codegen._engine._defined_symbols:
        if mxerh__jpa.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in mxerh__jpa and (
            'bodo_gb_udf_update_local' in mxerh__jpa or 
            'bodo_gb_udf_combine' in mxerh__jpa or 'bodo_gb_udf_eval' in
            mxerh__jpa or 'bodo_gb_apply_general_udfs' in mxerh__jpa):
            gb_agg_cfunc_addr[mxerh__jpa
                ] = cres.library.get_pointer_to_function(mxerh__jpa)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for mxerh__jpa in cres.library._codegen._engine._defined_symbols:
        if mxerh__jpa.startswith('cfunc') and ('get_join_cond_addr' not in
            mxerh__jpa or 'bodo_join_gen_cond' in mxerh__jpa):
            join_gen_cond_cfunc_addr[mxerh__jpa
                ] = cres.library.get_pointer_to_function(mxerh__jpa)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    hjhrc__lzxr = self._get_dispatcher_for_current_target()
    if hjhrc__lzxr is not self:
        return hjhrc__lzxr.compile(sig)
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
            amwup__xazx = self.overloads.get(tuple(args))
            if amwup__xazx is not None:
                return amwup__xazx.entry_point
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
            djebe__qxhm = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=djebe__qxhm):
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
    qbr__dvici = self._final_module
    kyoz__fimhy = []
    hbqi__yjij = 0
    for fn in qbr__dvici.functions:
        hbqi__yjij += 1
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
            kyoz__fimhy.append(fn.name)
    if hbqi__yjij == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if kyoz__fimhy:
        qbr__dvici = qbr__dvici.clone()
        for name in kyoz__fimhy:
            qbr__dvici.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = qbr__dvici
    return qbr__dvici


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
    for lscm__khv in self.constraints:
        loc = lscm__khv.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                lscm__khv(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                xflg__imvr = numba.core.errors.TypingError(str(e), loc=
                    lscm__khv.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(xflg__imvr, e))
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
                    xflg__imvr = numba.core.errors.TypingError(msg.format(
                        con=lscm__khv, err=str(e)), loc=lscm__khv.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(xflg__imvr, e))
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
    for faaow__jrjya in self._failures.values():
        for hhhmd__nut in faaow__jrjya:
            if isinstance(hhhmd__nut.error, ForceLiteralArg):
                raise hhhmd__nut.error
            if isinstance(hhhmd__nut.error, bodo.utils.typing.BodoError):
                raise hhhmd__nut.error
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
    pbnlb__koiq = False
    liw__qismk = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        qths__jiqzf = set()
        btat__xssgs = lives & alias_set
        for srd__bakys in btat__xssgs:
            qths__jiqzf |= alias_map[srd__bakys]
        lives_n_aliases = lives | qths__jiqzf | arg_aliases
        if type(stmt) in remove_dead_extensions:
            evjy__ktpr = remove_dead_extensions[type(stmt)]
            stmt = evjy__ktpr(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                pbnlb__koiq = True
                continue
        if isinstance(stmt, ir.Assign):
            eml__fqbg = stmt.target
            amr__qxksy = stmt.value
            if eml__fqbg.name not in lives and has_no_side_effect(amr__qxksy,
                lives_n_aliases, call_table):
                pbnlb__koiq = True
                continue
            if saved_array_analysis and eml__fqbg.name in lives and is_expr(
                amr__qxksy, 'getattr'
                ) and amr__qxksy.attr == 'shape' and is_array_typ(typemap[
                amr__qxksy.value.name]) and amr__qxksy.value.name not in lives:
                qaiz__fda = {srd__bakys: vgh__lbtqf for vgh__lbtqf,
                    srd__bakys in func_ir.blocks.items()}
                if block in qaiz__fda:
                    rdznx__fysxz = qaiz__fda[block]
                    pozg__yuaeq = saved_array_analysis.get_equiv_set(
                        rdznx__fysxz)
                    tps__qlufp = pozg__yuaeq.get_equiv_set(amr__qxksy.value)
                    if tps__qlufp is not None:
                        for srd__bakys in tps__qlufp:
                            if srd__bakys.endswith('#0'):
                                srd__bakys = srd__bakys[:-2]
                            if srd__bakys in typemap and is_array_typ(typemap
                                [srd__bakys]) and srd__bakys in lives:
                                amr__qxksy.value = ir.Var(amr__qxksy.value.
                                    scope, srd__bakys, amr__qxksy.value.loc)
                                pbnlb__koiq = True
                                break
            if isinstance(amr__qxksy, ir.Var
                ) and eml__fqbg.name == amr__qxksy.name:
                pbnlb__koiq = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                pbnlb__koiq = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            vro__lrc = analysis.ir_extension_usedefs[type(stmt)]
            ipvlm__awujz, qwtw__wbez = vro__lrc(stmt)
            lives -= qwtw__wbez
            lives |= ipvlm__awujz
        else:
            lives |= {srd__bakys.name for srd__bakys in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                thu__pdxt = set()
                if isinstance(amr__qxksy, ir.Expr):
                    thu__pdxt = {srd__bakys.name for srd__bakys in
                        amr__qxksy.list_vars()}
                if eml__fqbg.name not in thu__pdxt:
                    lives.remove(eml__fqbg.name)
        liw__qismk.append(stmt)
    liw__qismk.reverse()
    block.body = liw__qismk
    return pbnlb__koiq


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            grkm__lbty, = args
            if isinstance(grkm__lbty, types.IterableType):
                dtype = grkm__lbty.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), grkm__lbty)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    dfstw__nimid = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (dfstw__nimid, self.dtype)
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
        except LiteralTypingError as csli__pch:
            return
    try:
        return literal(value)
    except LiteralTypingError as csli__pch:
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
        kqdlr__ezkdr = py_func.__qualname__
    except AttributeError as csli__pch:
        kqdlr__ezkdr = py_func.__name__
    szs__opo = inspect.getfile(py_func)
    for cls in self._locator_classes:
        dnqv__ctlh = cls.from_function(py_func, szs__opo)
        if dnqv__ctlh is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (kqdlr__ezkdr, szs__opo))
    self._locator = dnqv__ctlh
    nfpy__uamm = inspect.getfile(py_func)
    mxxr__rnjq = os.path.splitext(os.path.basename(nfpy__uamm))[0]
    if szs__opo.startswith('<ipython-'):
        klqu__drukj = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', mxxr__rnjq, count=1)
        if klqu__drukj == mxxr__rnjq:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        mxxr__rnjq = klqu__drukj
    wiyg__qatjk = '%s.%s' % (mxxr__rnjq, kqdlr__ezkdr)
    pky__cqt = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(wiyg__qatjk, pky__cqt)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    dtrrg__xirnr = list(filter(lambda a: self._istuple(a.name), args))
    if len(dtrrg__xirnr) == 2 and fn.__name__ == 'add':
        oxni__wsn = self.typemap[dtrrg__xirnr[0].name]
        csvc__prek = self.typemap[dtrrg__xirnr[1].name]
        if oxni__wsn.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                dtrrg__xirnr[1]))
        if csvc__prek.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                dtrrg__xirnr[0]))
        try:
            pur__vrtg = [equiv_set.get_shape(x) for x in dtrrg__xirnr]
            if None in pur__vrtg:
                return None
            llv__xleu = sum(pur__vrtg, ())
            return ArrayAnalysis.AnalyzeResult(shape=llv__xleu)
        except GuardException as csli__pch:
            return None
    rqr__wtsni = list(filter(lambda a: self._isarray(a.name), args))
    require(len(rqr__wtsni) > 0)
    ees__tns = [x.name for x in rqr__wtsni]
    mshw__doqbb = [self.typemap[x.name].ndim for x in rqr__wtsni]
    wsbb__vmid = max(mshw__doqbb)
    require(wsbb__vmid > 0)
    pur__vrtg = [equiv_set.get_shape(x) for x in rqr__wtsni]
    if any(a is None for a in pur__vrtg):
        return ArrayAnalysis.AnalyzeResult(shape=rqr__wtsni[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, rqr__wtsni))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, pur__vrtg,
        ees__tns)


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
    pbo__qddza = code_obj.code
    tdppj__oki = len(pbo__qddza.co_freevars)
    tre__gkvb = pbo__qddza.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        hzs__tsxv, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        tre__gkvb = [srd__bakys.name for srd__bakys in hzs__tsxv]
    xwk__gahmx = caller_ir.func_id.func.__globals__
    try:
        xwk__gahmx = getattr(code_obj, 'globals', xwk__gahmx)
    except KeyError as csli__pch:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/source/programming_with_bodo/bodo_api_reference/udfs.html"
        )
    fqse__yqc = []
    for x in tre__gkvb:
        try:
            rpga__siif = caller_ir.get_definition(x)
        except KeyError as csli__pch:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(rpga__siif, (ir.Const, ir.Global, ir.FreeVar)):
            val = rpga__siif.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                nchhe__oenxg = ir_utils.mk_unique_var('nested_func').replace(
                    '.', '_')
                xwk__gahmx[nchhe__oenxg] = bodo.jit(distributed=False)(val)
                xwk__gahmx[nchhe__oenxg].is_nested_func = True
                val = nchhe__oenxg
            if isinstance(val, CPUDispatcher):
                nchhe__oenxg = ir_utils.mk_unique_var('nested_func').replace(
                    '.', '_')
                xwk__gahmx[nchhe__oenxg] = val
                val = nchhe__oenxg
            fqse__yqc.append(val)
        elif isinstance(rpga__siif, ir.Expr
            ) and rpga__siif.op == 'make_function':
            myufy__thg = convert_code_obj_to_function(rpga__siif, caller_ir)
            nchhe__oenxg = ir_utils.mk_unique_var('nested_func').replace('.',
                '_')
            xwk__gahmx[nchhe__oenxg] = bodo.jit(distributed=False)(myufy__thg)
            xwk__gahmx[nchhe__oenxg].is_nested_func = True
            fqse__yqc.append(nchhe__oenxg)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    nher__itn = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        fqse__yqc)])
    afnce__qsgf = ','.join([('c_%d' % i) for i in range(tdppj__oki)])
    kzc__yrw = list(pbo__qddza.co_varnames)
    qsk__sjav = 0
    yrr__tmhpk = pbo__qddza.co_argcount
    rmea__uzub = caller_ir.get_definition(code_obj.defaults)
    if rmea__uzub is not None:
        if isinstance(rmea__uzub, tuple):
            d = [caller_ir.get_definition(x).value for x in rmea__uzub]
            orrp__fhtf = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in rmea__uzub.items]
            orrp__fhtf = tuple(d)
        qsk__sjav = len(orrp__fhtf)
    inrqw__ncx = yrr__tmhpk - qsk__sjav
    inmt__hzevn = ','.join([('%s' % kzc__yrw[i]) for i in range(inrqw__ncx)])
    if qsk__sjav:
        pjdt__mywq = [('%s = %s' % (kzc__yrw[i + inrqw__ncx], orrp__fhtf[i]
            )) for i in range(qsk__sjav)]
        inmt__hzevn += ', '
        inmt__hzevn += ', '.join(pjdt__mywq)
    return _create_function_from_code_obj(pbo__qddza, nher__itn,
        inmt__hzevn, afnce__qsgf, xwk__gahmx)


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
    for jidxw__vmxpf, (czzil__ozk, txti__ztjf) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % txti__ztjf)
            rqa__hngjb = _pass_registry.get(czzil__ozk).pass_inst
            if isinstance(rqa__hngjb, CompilerPass):
                self._runPass(jidxw__vmxpf, rqa__hngjb, state)
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
                    pipeline_name, txti__ztjf)
                bfc__hxpgv = self._patch_error(msg, e)
                raise bfc__hxpgv
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
    mnu__mcq = None
    qwtw__wbez = {}

    def lookup(var, already_seen, varonly=True):
        val = qwtw__wbez.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    apy__srl = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        eml__fqbg = stmt.target
        amr__qxksy = stmt.value
        qwtw__wbez[eml__fqbg.name] = amr__qxksy
        if isinstance(amr__qxksy, ir.Var) and amr__qxksy.name in qwtw__wbez:
            amr__qxksy = lookup(amr__qxksy, set())
        if isinstance(amr__qxksy, ir.Expr):
            oug__jucl = set(lookup(srd__bakys, set(), True).name for
                srd__bakys in amr__qxksy.list_vars())
            if name in oug__jucl:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(amr__qxksy)]
                oari__unykq = [x for x, zlxn__kbfxe in args if zlxn__kbfxe.
                    name != name]
                args = [(x, zlxn__kbfxe) for x, zlxn__kbfxe in args if x !=
                    zlxn__kbfxe.name]
                qnsjn__gpg = dict(args)
                if len(oari__unykq) == 1:
                    qnsjn__gpg[oari__unykq[0]] = ir.Var(eml__fqbg.scope, 
                        name + '#init', eml__fqbg.loc)
                replace_vars_inner(amr__qxksy, qnsjn__gpg)
                mnu__mcq = nodes[i:]
                break
    return mnu__mcq


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
        seh__zug = expand_aliases({srd__bakys.name for srd__bakys in stmt.
            list_vars()}, alias_map, arg_aliases)
        ipfw__ozvw = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        emj__myze = expand_aliases({srd__bakys.name for srd__bakys in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        ncbx__iwt = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(ipfw__ozvw & emj__myze | ncbx__iwt & seh__zug) == 0:
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
    vbum__rkthh = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            vbum__rkthh.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                vbum__rkthh.update(get_parfor_writes(stmt, func_ir))
    return vbum__rkthh


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    vbum__rkthh = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        vbum__rkthh.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        vbum__rkthh = {srd__bakys.name for srd__bakys in stmt.df_out_vars.
            values()}
        if stmt.out_key_vars is not None:
            vbum__rkthh.update({srd__bakys.name for srd__bakys in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        vbum__rkthh = {srd__bakys.name for srd__bakys in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        vbum__rkthh = {srd__bakys.name for srd__bakys in stmt.out_data_vars
            .values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            vbum__rkthh.update({srd__bakys.name for srd__bakys in stmt.
                out_key_arrs})
            vbum__rkthh.update({srd__bakys.name for srd__bakys in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        dyal__ayui = guard(find_callname, func_ir, stmt.value)
        if dyal__ayui in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            vbum__rkthh.add(stmt.value.args[0].name)
        if dyal__ayui == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            vbum__rkthh.add(stmt.value.args[1].name)
    return vbum__rkthh


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
        evjy__ktpr = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        qrml__xks = evjy__ktpr.format(self, msg)
        self.args = qrml__xks,
    else:
        evjy__ktpr = _termcolor.errmsg('{0}')
        qrml__xks = evjy__ktpr.format(self)
        self.args = qrml__xks,
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
        for kbdvb__pdo in options['distributed']:
            dist_spec[kbdvb__pdo] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for kbdvb__pdo in options['distributed_block']:
            dist_spec[kbdvb__pdo] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    lqw__sxljz = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, xdo__fxn in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(xdo__fxn)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    ktx__ptjq = {}
    for zqz__hktjf in reversed(inspect.getmro(cls)):
        ktx__ptjq.update(zqz__hktjf.__dict__)
    cozh__nztm, tqn__yfn, wjwm__cjm, ulyij__buwz = {}, {}, {}, {}
    for vgh__lbtqf, srd__bakys in ktx__ptjq.items():
        if isinstance(srd__bakys, pytypes.FunctionType):
            cozh__nztm[vgh__lbtqf] = srd__bakys
        elif isinstance(srd__bakys, property):
            tqn__yfn[vgh__lbtqf] = srd__bakys
        elif isinstance(srd__bakys, staticmethod):
            wjwm__cjm[vgh__lbtqf] = srd__bakys
        else:
            ulyij__buwz[vgh__lbtqf] = srd__bakys
    jcnv__ncw = (set(cozh__nztm) | set(tqn__yfn) | set(wjwm__cjm)) & set(spec)
    if jcnv__ncw:
        raise NameError('name shadowing: {0}'.format(', '.join(jcnv__ncw)))
    vfn__iggi = ulyij__buwz.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(ulyij__buwz)
    if ulyij__buwz:
        msg = 'class members are not yet supported: {0}'
        fxvhq__jstnv = ', '.join(ulyij__buwz.keys())
        raise TypeError(msg.format(fxvhq__jstnv))
    for vgh__lbtqf, srd__bakys in tqn__yfn.items():
        if srd__bakys.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(vgh__lbtqf))
    jit_methods = {vgh__lbtqf: bodo.jit(returns_maybe_distributed=
        lqw__sxljz)(srd__bakys) for vgh__lbtqf, srd__bakys in cozh__nztm.
        items()}
    jit_props = {}
    for vgh__lbtqf, srd__bakys in tqn__yfn.items():
        saxnu__eqec = {}
        if srd__bakys.fget:
            saxnu__eqec['get'] = bodo.jit(srd__bakys.fget)
        if srd__bakys.fset:
            saxnu__eqec['set'] = bodo.jit(srd__bakys.fset)
        jit_props[vgh__lbtqf] = saxnu__eqec
    jit_static_methods = {vgh__lbtqf: bodo.jit(srd__bakys.__func__) for 
        vgh__lbtqf, srd__bakys in wjwm__cjm.items()}
    hvnw__cjlrs = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    pfmc__jmfrn = dict(class_type=hvnw__cjlrs, __doc__=vfn__iggi)
    pfmc__jmfrn.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), pfmc__jmfrn)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, hvnw__cjlrs)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(hvnw__cjlrs, typingctx, targetctx).register()
    as_numba_type.register(cls, hvnw__cjlrs.instance_type)
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
    pzdav__nzf = ','.join('{0}:{1}'.format(vgh__lbtqf, srd__bakys) for 
        vgh__lbtqf, srd__bakys in struct.items())
    mavg__aun = ','.join('{0}:{1}'.format(vgh__lbtqf, srd__bakys) for 
        vgh__lbtqf, srd__bakys in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), pzdav__nzf, mavg__aun)
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
    cta__esa = numba.core.typeinfer.fold_arg_vars(typevars, self.args, self
        .vararg, self.kws)
    if cta__esa is None:
        return
    agt__rpl, kmy__pxn = cta__esa
    for a in itertools.chain(agt__rpl, kmy__pxn.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, agt__rpl, kmy__pxn)
    except ForceLiteralArg as e:
        mahpu__eryp = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(mahpu__eryp, self.kws)
        rcbe__ncx = set()
        mijsj__nvi = set()
        napi__qyyv = {}
        for jidxw__vmxpf in e.requested_args:
            ydbnc__rwmc = typeinfer.func_ir.get_definition(folded[jidxw__vmxpf]
                )
            if isinstance(ydbnc__rwmc, ir.Arg):
                rcbe__ncx.add(ydbnc__rwmc.index)
                if ydbnc__rwmc.index in e.file_infos:
                    napi__qyyv[ydbnc__rwmc.index] = e.file_infos[ydbnc__rwmc
                        .index]
            else:
                mijsj__nvi.add(jidxw__vmxpf)
        if mijsj__nvi:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif rcbe__ncx:
            raise ForceLiteralArg(rcbe__ncx, loc=self.loc, file_infos=
                napi__qyyv)
    if sig is None:
        tuf__wsk = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in agt__rpl]
        args += [('%s=%s' % (vgh__lbtqf, srd__bakys)) for vgh__lbtqf,
            srd__bakys in sorted(kmy__pxn.items())]
        wdc__scs = tuf__wsk.format(fnty, ', '.join(map(str, args)))
        upaqj__hvgkh = context.explain_function_type(fnty)
        msg = '\n'.join([wdc__scs, upaqj__hvgkh])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        ans__zbn = context.unify_pairs(sig.recvr, fnty.this)
        if ans__zbn is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if ans__zbn is not None and ans__zbn.is_precise():
            chonc__dcim = fnty.copy(this=ans__zbn)
            typeinfer.propagate_refined_type(self.func, chonc__dcim)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            uiyfw__xorwi = target.getone()
            if context.unify_pairs(uiyfw__xorwi, sig.return_type
                ) == uiyfw__xorwi:
                sig = sig.replace(return_type=uiyfw__xorwi)
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
        mmve__gmh = '*other* must be a {} but got a {} instead'
        raise TypeError(mmve__gmh.format(ForceLiteralArg, type(other)))
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
    yppug__tocvx = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for vgh__lbtqf, srd__bakys in kwargs.items():
        tozgt__qttz = None
        try:
            lvong__myzep = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[lvong__myzep.name] = [srd__bakys]
            tozgt__qttz = get_const_value_inner(func_ir, lvong__myzep)
            func_ir._definitions.pop(lvong__myzep.name)
            if isinstance(tozgt__qttz, str):
                tozgt__qttz = sigutils._parse_signature_string(tozgt__qttz)
            if isinstance(tozgt__qttz, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {vgh__lbtqf} is annotated as type class {tozgt__qttz}."""
                    )
            assert isinstance(tozgt__qttz, types.Type)
            if isinstance(tozgt__qttz, (types.List, types.Set)):
                tozgt__qttz = tozgt__qttz.copy(reflected=False)
            yppug__tocvx[vgh__lbtqf] = tozgt__qttz
        except BodoError as csli__pch:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(tozgt__qttz, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(srd__bakys, ir.Global):
                    msg = f'Global {srd__bakys.name!r} is not defined.'
                if isinstance(srd__bakys, ir.FreeVar):
                    msg = f'Freevar {srd__bakys.name!r} is not defined.'
            if isinstance(srd__bakys, ir.Expr) and srd__bakys.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=vgh__lbtqf, msg=msg, loc=loc)
    for name, typ in yppug__tocvx.items():
        self._legalize_arg_type(name, typ, loc)
    return yppug__tocvx


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
    fak__yzra = inst.arg
    assert fak__yzra > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(fak__yzra)]))
    tmps = [state.make_temp() for _ in range(fak__yzra - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    zohzq__zwf = ir.Global('format', format, loc=self.loc)
    self.store(value=zohzq__zwf, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    ighaq__ugd = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=ighaq__ugd, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    fak__yzra = inst.arg
    assert fak__yzra > 0, 'invalid BUILD_STRING count'
    yxli__ipzh = self.get(strings[0])
    for other, wph__ryxfc in zip(strings[1:], tmps):
        other = self.get(other)
        ksh__mleh = ir.Expr.binop(operator.add, lhs=yxli__ipzh, rhs=other,
            loc=self.loc)
        self.store(ksh__mleh, wph__ryxfc)
        yxli__ipzh = self.get(wph__ryxfc)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    bvk__dhrxn = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, bvk__dhrxn])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    vmsl__yfy = mk_unique_var(f'{var_name}')
    usj__gspqt = vmsl__yfy.replace('<', '_').replace('>', '_')
    usj__gspqt = usj__gspqt.replace('.', '_').replace('$', '_v')
    return usj__gspqt


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
                oglfk__pur = get_overload_const_str(val2)
                if oglfk__pur != 'ns':
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
        sddp__keat = states['defmap']
        if len(sddp__keat) == 0:
            imssq__ypzk = assign.target
            numba.core.ssa._logger.debug('first assign: %s', imssq__ypzk)
            if imssq__ypzk.name not in scope.localvars:
                imssq__ypzk = scope.define(assign.target.name, loc=assign.loc)
        else:
            imssq__ypzk = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=imssq__ypzk, value=assign.value, loc=
            assign.loc)
        sddp__keat[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    czke__mdvs = []
    for vgh__lbtqf, srd__bakys in typing.npydecl.registry.globals:
        if vgh__lbtqf == func:
            czke__mdvs.append(srd__bakys)
    for vgh__lbtqf, srd__bakys in typing.templates.builtin_registry.globals:
        if vgh__lbtqf == func:
            czke__mdvs.append(srd__bakys)
    if len(czke__mdvs) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return czke__mdvs


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    opn__lwua = {}
    mjgnv__utin = find_topo_order(blocks)
    pnek__aqe = {}
    for rdznx__fysxz in mjgnv__utin:
        block = blocks[rdznx__fysxz]
        liw__qismk = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                eml__fqbg = stmt.target.name
                amr__qxksy = stmt.value
                if (amr__qxksy.op == 'getattr' and amr__qxksy.attr in
                    arr_math and isinstance(typemap[amr__qxksy.value.name],
                    types.npytypes.Array)):
                    amr__qxksy = stmt.value
                    tux__pcqn = amr__qxksy.value
                    opn__lwua[eml__fqbg] = tux__pcqn
                    scope = tux__pcqn.scope
                    loc = tux__pcqn.loc
                    lsw__mpnpx = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[lsw__mpnpx.name] = types.misc.Module(numpy)
                    gls__sadad = ir.Global('np', numpy, loc)
                    couls__zzp = ir.Assign(gls__sadad, lsw__mpnpx, loc)
                    amr__qxksy.value = lsw__mpnpx
                    liw__qismk.append(couls__zzp)
                    func_ir._definitions[lsw__mpnpx.name] = [gls__sadad]
                    func = getattr(numpy, amr__qxksy.attr)
                    uol__alu = get_np_ufunc_typ_lst(func)
                    pnek__aqe[eml__fqbg] = uol__alu
                if (amr__qxksy.op == 'call' and amr__qxksy.func.name in
                    opn__lwua):
                    tux__pcqn = opn__lwua[amr__qxksy.func.name]
                    fpb__vjqp = calltypes.pop(amr__qxksy)
                    vwvmq__hvzk = fpb__vjqp.args[:len(amr__qxksy.args)]
                    hev__ejzs = {name: typemap[srd__bakys.name] for name,
                        srd__bakys in amr__qxksy.kws}
                    cnlue__vcdg = pnek__aqe[amr__qxksy.func.name]
                    wnmpo__slgs = None
                    for dpvgl__rpubo in cnlue__vcdg:
                        try:
                            wnmpo__slgs = dpvgl__rpubo.get_call_type(typingctx,
                                [typemap[tux__pcqn.name]] + list(
                                vwvmq__hvzk), hev__ejzs)
                            typemap.pop(amr__qxksy.func.name)
                            typemap[amr__qxksy.func.name] = dpvgl__rpubo
                            calltypes[amr__qxksy] = wnmpo__slgs
                            break
                        except Exception as csli__pch:
                            pass
                    if wnmpo__slgs is None:
                        raise TypeError(
                            f'No valid template found for {amr__qxksy.func.name}'
                            )
                    amr__qxksy.args = [tux__pcqn] + amr__qxksy.args
            liw__qismk.append(stmt)
        block.body = liw__qismk


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    tnpve__pfyo = ufunc.nin
    bwwn__nwwwi = ufunc.nout
    inrqw__ncx = ufunc.nargs
    assert inrqw__ncx == tnpve__pfyo + bwwn__nwwwi
    if len(args) < tnpve__pfyo:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            tnpve__pfyo))
    if len(args) > inrqw__ncx:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), inrqw__ncx)
            )
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    zak__nwgb = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    lwh__yzvq = max(zak__nwgb)
    tyc__uevc = args[tnpve__pfyo:]
    if not all(d == lwh__yzvq for d in zak__nwgb[tnpve__pfyo:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(kuhvp__ukjvu, types.ArrayCompatible) and not
        isinstance(kuhvp__ukjvu, types.Bytes) for kuhvp__ukjvu in tyc__uevc):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(kuhvp__ukjvu.mutable for kuhvp__ukjvu in tyc__uevc):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    fzd__oiwo = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    eik__xjp = None
    if lwh__yzvq > 0 and len(tyc__uevc) < ufunc.nout:
        eik__xjp = 'C'
        esp__eced = [(x.layout if isinstance(x, types.ArrayCompatible) and 
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in esp__eced and 'F' in esp__eced:
            eik__xjp = 'F'
    return fzd__oiwo, tyc__uevc, lwh__yzvq, eik__xjp


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
        llpkk__akt = 'Dict.key_type cannot be of type {}'
        raise TypingError(llpkk__akt.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        llpkk__akt = 'Dict.value_type cannot be of type {}'
        raise TypingError(llpkk__akt.format(valty))
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
    oqr__okkx = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[oqr__okkx]
        return impl, args
    except KeyError as csli__pch:
        pass
    impl, args = self._build_impl(oqr__okkx, args, kws)
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
        qypdr__brkfq = find_topo_order(parfor.loop_body)
    gauq__cqk = qypdr__brkfq[0]
    akg__ruo = {}
    _update_parfor_get_setitems(parfor.loop_body[gauq__cqk].body, parfor.
        index_var, alias_map, akg__ruo, lives_n_aliases)
    ifx__afn = set(akg__ruo.keys())
    for obb__doku in qypdr__brkfq:
        if obb__doku == gauq__cqk:
            continue
        for stmt in parfor.loop_body[obb__doku].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            gbt__bmjab = set(srd__bakys.name for srd__bakys in stmt.list_vars()
                )
            dlhw__ufry = gbt__bmjab & ifx__afn
            for a in dlhw__ufry:
                akg__ruo.pop(a, None)
    for obb__doku in qypdr__brkfq:
        if obb__doku == gauq__cqk:
            continue
        block = parfor.loop_body[obb__doku]
        ziif__cjcl = akg__ruo.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            ziif__cjcl, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    ooocz__ufk = max(blocks.keys())
    kbwra__lfu, seu__incz = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    jiwuo__rhc = ir.Jump(kbwra__lfu, ir.Loc('parfors_dummy', -1))
    blocks[ooocz__ufk].body.append(jiwuo__rhc)
    btdd__bak = compute_cfg_from_blocks(blocks)
    iua__ifceg = compute_use_defs(blocks)
    xkv__ond = compute_live_map(btdd__bak, blocks, iua__ifceg.usemap,
        iua__ifceg.defmap)
    alias_set = set(alias_map.keys())
    for rdznx__fysxz, block in blocks.items():
        liw__qismk = []
        odpea__pxd = {srd__bakys.name for srd__bakys in block.terminator.
            list_vars()}
        for xswdm__nsnzj, nhv__cdeg in btdd__bak.successors(rdznx__fysxz):
            odpea__pxd |= xkv__ond[xswdm__nsnzj]
        for stmt in reversed(block.body):
            qths__jiqzf = odpea__pxd & alias_set
            for srd__bakys in qths__jiqzf:
                odpea__pxd |= alias_map[srd__bakys]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in odpea__pxd and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                dyal__ayui = guard(find_callname, func_ir, stmt.value)
                if dyal__ayui == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in odpea__pxd and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            odpea__pxd |= {srd__bakys.name for srd__bakys in stmt.list_vars()}
            liw__qismk.append(stmt)
        liw__qismk.reverse()
        block.body = liw__qismk
    typemap.pop(seu__incz.name)
    blocks[ooocz__ufk].body.pop()

    def trim_empty_parfor_branches(parfor):
        mvx__lry = False
        blocks = parfor.loop_body.copy()
        for rdznx__fysxz, block in blocks.items():
            if len(block.body):
                leqmg__tgfp = block.body[-1]
                if isinstance(leqmg__tgfp, ir.Branch):
                    if len(blocks[leqmg__tgfp.truebr].body) == 1 and len(blocks
                        [leqmg__tgfp.falsebr].body) == 1:
                        pwc__lxbne = blocks[leqmg__tgfp.truebr].body[0]
                        vxe__dmzj = blocks[leqmg__tgfp.falsebr].body[0]
                        if isinstance(pwc__lxbne, ir.Jump) and isinstance(
                            vxe__dmzj, ir.Jump
                            ) and pwc__lxbne.target == vxe__dmzj.target:
                            parfor.loop_body[rdznx__fysxz].body[-1] = ir.Jump(
                                pwc__lxbne.target, leqmg__tgfp.loc)
                            mvx__lry = True
                    elif len(blocks[leqmg__tgfp.truebr].body) == 1:
                        pwc__lxbne = blocks[leqmg__tgfp.truebr].body[0]
                        if isinstance(pwc__lxbne, ir.Jump
                            ) and pwc__lxbne.target == leqmg__tgfp.falsebr:
                            parfor.loop_body[rdznx__fysxz].body[-1] = ir.Jump(
                                pwc__lxbne.target, leqmg__tgfp.loc)
                            mvx__lry = True
                    elif len(blocks[leqmg__tgfp.falsebr].body) == 1:
                        vxe__dmzj = blocks[leqmg__tgfp.falsebr].body[0]
                        if isinstance(vxe__dmzj, ir.Jump
                            ) and vxe__dmzj.target == leqmg__tgfp.truebr:
                            parfor.loop_body[rdznx__fysxz].body[-1] = ir.Jump(
                                vxe__dmzj.target, leqmg__tgfp.loc)
                            mvx__lry = True
        return mvx__lry
    mvx__lry = True
    while mvx__lry:
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
        mvx__lry = trim_empty_parfor_branches(parfor)
    ktrf__lkyd = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        ktrf__lkyd &= len(block.body) == 0
    if ktrf__lkyd:
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
    ugpfl__rvm = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                ugpfl__rvm += 1
                parfor = stmt
                lbidk__zceht = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = lbidk__zceht.scope
                loc = ir.Loc('parfors_dummy', -1)
                qpvr__ttmbk = ir.Var(scope, mk_unique_var('$const'), loc)
                lbidk__zceht.body.append(ir.Assign(ir.Const(0, loc),
                    qpvr__ttmbk, loc))
                lbidk__zceht.body.append(ir.Return(qpvr__ttmbk, loc))
                btdd__bak = compute_cfg_from_blocks(parfor.loop_body)
                for ltel__czk in btdd__bak.dead_nodes():
                    del parfor.loop_body[ltel__czk]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                lbidk__zceht = parfor.loop_body[max(parfor.loop_body.keys())]
                lbidk__zceht.body.pop()
                lbidk__zceht.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return ugpfl__rvm


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
            amwup__xazx = self.overloads.get(tuple(args))
            if amwup__xazx is not None:
                return amwup__xazx.entry_point
            self._pre_compile(args, return_type, flags)
            ghspf__cmilu = self.func_ir
            djebe__qxhm = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=djebe__qxhm):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=ghspf__cmilu, args=
                    args, return_type=return_type, flags=flags, locals=self
                    .locals, lifted=(), lifted_from=self.lifted_from,
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
        xlna__gbr = copy.deepcopy(flags)
        xlna__gbr.no_rewrites = True

        def compile_local(the_ir, the_flags):
            xbjsw__cwed = pipeline_class(typingctx, targetctx, library,
                args, return_type, the_flags, locals)
            return xbjsw__cwed.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        awd__wlo = compile_local(func_ir, xlna__gbr)
        pxnyu__xgwri = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    pxnyu__xgwri = compile_local(func_ir, flags)
                except Exception as csli__pch:
                    pass
        if pxnyu__xgwri is not None:
            cres = pxnyu__xgwri
        else:
            cres = awd__wlo
        return cres
    else:
        xbjsw__cwed = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return xbjsw__cwed.compile_ir(func_ir=func_ir, lifted=lifted,
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
    bigja__aiq = self.get_data_type(typ.dtype)
    jya__ityfj = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        jya__ityfj):
        rpm__ryusg = ary.ctypes.data
        tzki__izp = self.add_dynamic_addr(builder, rpm__ryusg, info=str(
            type(rpm__ryusg)))
        hqv__qgr = self.add_dynamic_addr(builder, id(ary), info=str(type(ary)))
        self.global_arrays.append(ary)
    else:
        jtc__pjz = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            jtc__pjz = jtc__pjz.view('int64')
        val = bytearray(jtc__pjz.data)
        tqd__zhho = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        tzki__izp = cgutils.global_constant(builder, '.const.array.data',
            tqd__zhho)
        tzki__izp.align = self.get_abi_alignment(bigja__aiq)
        hqv__qgr = None
    nxm__usc = self.get_value_type(types.intp)
    gsyze__svext = [self.get_constant(types.intp, jlp__bvkyp) for
        jlp__bvkyp in ary.shape]
    dyx__vor = lir.Constant(lir.ArrayType(nxm__usc, len(gsyze__svext)),
        gsyze__svext)
    popzk__sea = [self.get_constant(types.intp, jlp__bvkyp) for jlp__bvkyp in
        ary.strides]
    qtz__yphf = lir.Constant(lir.ArrayType(nxm__usc, len(popzk__sea)),
        popzk__sea)
    rxwf__huuz = self.get_constant(types.intp, ary.dtype.itemsize)
    vcy__wyqif = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        vcy__wyqif, rxwf__huuz, tzki__izp.bitcast(self.get_value_type(types
        .CPointer(typ.dtype))), dyx__vor, qtz__yphf])


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
    kvjxf__wqdbb = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    qnty__xtdsn = lir.Function(module, kvjxf__wqdbb, name='nrt_atomic_{0}'.
        format(op))
    [kezrs__wbd] = qnty__xtdsn.args
    ppg__nkaue = qnty__xtdsn.append_basic_block()
    builder = lir.IRBuilder(ppg__nkaue)
    jtbt__ebur = lir.Constant(_word_type, 1)
    if False:
        uxca__sikob = builder.atomic_rmw(op, kezrs__wbd, jtbt__ebur,
            ordering=ordering)
        res = getattr(builder, op)(uxca__sikob, jtbt__ebur)
        builder.ret(res)
    else:
        uxca__sikob = builder.load(kezrs__wbd)
        ntpe__hzz = getattr(builder, op)(uxca__sikob, jtbt__ebur)
        cjp__trz = builder.icmp_signed('!=', uxca__sikob, lir.Constant(
            uxca__sikob.type, -1))
        with cgutils.if_likely(builder, cjp__trz):
            builder.store(ntpe__hzz, kezrs__wbd)
        builder.ret(ntpe__hzz)
    return qnty__xtdsn


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
        coaye__mbo = state.targetctx.codegen()
        state.library = coaye__mbo.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    guxxx__xrpc = state.func_ir
    typemap = state.typemap
    gfl__nroe = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    wcah__otspy = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            guxxx__xrpc, typemap, gfl__nroe, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            ypx__hnrq = lowering.Lower(targetctx, library, fndesc,
                guxxx__xrpc, metadata=metadata)
            ypx__hnrq.lower()
            if not flags.no_cpython_wrapper:
                ypx__hnrq.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(gfl__nroe, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        ypx__hnrq.create_cfunc_wrapper()
            env = ypx__hnrq.env
            qsgfe__lrw = ypx__hnrq.call_helper
            del ypx__hnrq
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, qsgfe__lrw, cfunc=None, env=env)
        else:
            aunl__vxnu = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(aunl__vxnu, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, qsgfe__lrw, cfunc=aunl__vxnu,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        ubpn__jwd = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = ubpn__jwd - wcah__otspy
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
        iqe__gzsh = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, iqe__gzsh),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            lchxr__doczo.do_break()
        kzte__pdo = c.builder.icmp_signed('!=', iqe__gzsh, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(kzte__pdo, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, iqe__gzsh)
                c.pyapi.decref(iqe__gzsh)
                lchxr__doczo.do_break()
        c.pyapi.decref(iqe__gzsh)
    mvux__wpesf, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(mvux__wpesf, likely=True) as (jkf__ubm, zwl__nah):
        with jkf__ubm:
            list.size = size
            nive__hzxwn = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                nive__hzxwn), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        nive__hzxwn))
                    with cgutils.for_range(c.builder, size) as lchxr__doczo:
                        itemobj = c.pyapi.list_getitem(obj, lchxr__doczo.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        xgcek__avpt = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(xgcek__avpt.is_error, likely
                            =False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            lchxr__doczo.do_break()
                        list.setitem(lchxr__doczo.index, xgcek__avpt.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with zwl__nah:
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
    icyo__ldjy, oie__bqxs, pdc__vczve, ejgi__cenj, fjtot__rnfg = (
        compile_time_get_string_data(literal_string))
    qbr__dvici = builder.module
    gv = context.insert_const_bytes(qbr__dvici, icyo__ldjy)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        oie__bqxs), context.get_constant(types.int32, pdc__vczve), context.
        get_constant(types.uint32, ejgi__cenj), context.get_constant(
        _Py_hash_t, -1), context.get_constant_null(types.MemInfoPointer(
        types.voidptr)), context.get_constant_null(types.pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    rmzio__ksku = None
    if isinstance(shape, types.Integer):
        rmzio__ksku = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(jlp__bvkyp, (types.Integer, types.IntEnumMember)) for
            jlp__bvkyp in shape):
            rmzio__ksku = len(shape)
    return rmzio__ksku


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
            rmzio__ksku = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if rmzio__ksku == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(
                    rmzio__ksku))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            ees__tns = self._get_names(x)
            if len(ees__tns) != 0:
                return ees__tns[0]
            return ees__tns
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    ees__tns = self._get_names(obj)
    if len(ees__tns) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(ees__tns[0])


def get_equiv_set(self, obj):
    ees__tns = self._get_names(obj)
    if len(ees__tns) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(ees__tns[0])


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
    wpj__urwqo = []
    for gcws__oxor in func_ir.arg_names:
        if gcws__oxor in typemap and isinstance(typemap[gcws__oxor], types.
            containers.UniTuple) and typemap[gcws__oxor].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(gcws__oxor))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for ergkr__phfj in func_ir.blocks.values():
        for stmt in ergkr__phfj.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    xpo__hpc = getattr(val, 'code', None)
                    if xpo__hpc is not None:
                        if getattr(val, 'closure', None) is not None:
                            znug__prve = '<creating a function from a closure>'
                            ksh__mleh = ''
                        else:
                            znug__prve = xpo__hpc.co_name
                            ksh__mleh = '(%s) ' % znug__prve
                    else:
                        znug__prve = '<could not ascertain use case>'
                        ksh__mleh = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (znug__prve, ksh__mleh))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                ymh__durxo = False
                if isinstance(val, pytypes.FunctionType):
                    ymh__durxo = val in {numba.gdb, numba.gdb_init}
                if not ymh__durxo:
                    ymh__durxo = getattr(val, '_name', '') == 'gdb_internal'
                if ymh__durxo:
                    wpj__urwqo.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    tfxe__tdmbx = func_ir.get_definition(var)
                    muxs__xzyfn = guard(find_callname, func_ir, tfxe__tdmbx)
                    if muxs__xzyfn and muxs__xzyfn[1] == 'numpy':
                        ty = getattr(numpy, muxs__xzyfn[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    aqehm__qht = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(aqehm__qht), loc=stmt.loc)
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
    if len(wpj__urwqo) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        iqs__lib = '\n'.join([x.strformat() for x in wpj__urwqo])
        raise errors.UnsupportedError(msg % iqs__lib)


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
    vgh__lbtqf, srd__bakys = next(iter(val.items()))
    vrpsn__kjan = typeof_impl(vgh__lbtqf, c)
    qbdjy__knf = typeof_impl(srd__bakys, c)
    if vrpsn__kjan is None or qbdjy__knf is None:
        raise ValueError(
            f'Cannot type dict element type {type(vgh__lbtqf)}, {type(srd__bakys)}'
            )
    return types.DictType(vrpsn__kjan, qbdjy__knf)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    dwx__aij = cgutils.alloca_once_value(c.builder, val)
    ycmk__ieidd = c.pyapi.object_hasattr_string(val, '_opaque')
    lbbzj__hfq = c.builder.icmp_unsigned('==', ycmk__ieidd, lir.Constant(
        ycmk__ieidd.type, 0))
    poo__rpepf = typ.key_type
    agp__npv = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(poo__rpepf, agp__npv)

    def copy_dict(out_dict, in_dict):
        for vgh__lbtqf, srd__bakys in in_dict.items():
            out_dict[vgh__lbtqf] = srd__bakys
    with c.builder.if_then(lbbzj__hfq):
        tlp__cuwid = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        ajvgc__pzg = c.pyapi.call_function_objargs(tlp__cuwid, [])
        aave__wpgt = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(aave__wpgt, [ajvgc__pzg, val])
        c.builder.store(ajvgc__pzg, dwx__aij)
    val = c.builder.load(dwx__aij)
    ujwv__kwhax = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    msxj__ytw = c.pyapi.object_type(val)
    rzads__vqwc = c.builder.icmp_unsigned('==', msxj__ytw, ujwv__kwhax)
    with c.builder.if_else(rzads__vqwc) as (fioos__wqbnr, xhh__arknd):
        with fioos__wqbnr:
            kuagt__ktao = c.pyapi.object_getattr_string(val, '_opaque')
            exhol__qrepy = types.MemInfoPointer(types.voidptr)
            xgcek__avpt = c.unbox(exhol__qrepy, kuagt__ktao)
            mi = xgcek__avpt.value
            fxq__oieck = exhol__qrepy, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *fxq__oieck)
            qtwp__wuw = context.get_constant_null(fxq__oieck[1])
            args = mi, qtwp__wuw
            sbim__dzwvm, yng__wbair = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, yng__wbair)
            c.pyapi.decref(kuagt__ktao)
            idvz__ecn = c.builder.basic_block
        with xhh__arknd:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", msxj__ytw, ujwv__kwhax)
            cxv__lfadb = c.builder.basic_block
    toqcy__ajvw = c.builder.phi(yng__wbair.type)
    ydlz__atu = c.builder.phi(sbim__dzwvm.type)
    toqcy__ajvw.add_incoming(yng__wbair, idvz__ecn)
    toqcy__ajvw.add_incoming(yng__wbair.type(None), cxv__lfadb)
    ydlz__atu.add_incoming(sbim__dzwvm, idvz__ecn)
    ydlz__atu.add_incoming(cgutils.true_bit, cxv__lfadb)
    c.pyapi.decref(ujwv__kwhax)
    c.pyapi.decref(msxj__ytw)
    with c.builder.if_then(lbbzj__hfq):
        c.pyapi.decref(val)
    return NativeValue(toqcy__ajvw, is_error=ydlz__atu)


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
    myvx__wrhjt = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=myvx__wrhjt, name=updatevar)
    jswq__ortl = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=jswq__ortl, name=res)


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
        for vgh__lbtqf, srd__bakys in other.items():
            d[vgh__lbtqf] = srd__bakys
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
    ksh__mleh = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(ksh__mleh, res)


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
    lervh__khnsb = PassManager(name)
    if state.func_ir is None:
        lervh__khnsb.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            lervh__khnsb.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        lervh__khnsb.add_pass(FixupArgs, 'fix up args')
    lervh__khnsb.add_pass(IRProcessing, 'processing IR')
    lervh__khnsb.add_pass(WithLifting, 'Handle with contexts')
    lervh__khnsb.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        lervh__khnsb.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        lervh__khnsb.add_pass(DeadBranchPrune, 'dead branch pruning')
        lervh__khnsb.add_pass(GenericRewrites, 'nopython rewrites')
    lervh__khnsb.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    lervh__khnsb.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        lervh__khnsb.add_pass(DeadBranchPrune, 'dead branch pruning')
    lervh__khnsb.add_pass(FindLiterallyCalls, 'find literally calls')
    lervh__khnsb.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        lervh__khnsb.add_pass(ReconstructSSA, 'ssa')
    lervh__khnsb.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    lervh__khnsb.finalize()
    return lervh__khnsb


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
    a, baapv__vidg = args
    if isinstance(a, types.List) and isinstance(baapv__vidg, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(baapv__vidg, types.List):
        return signature(baapv__vidg, types.intp, baapv__vidg)


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
        hmrvw__unk, yerv__ykg = 0, 1
    else:
        hmrvw__unk, yerv__ykg = 1, 0
    nxoe__ahr = ListInstance(context, builder, sig.args[hmrvw__unk], args[
        hmrvw__unk])
    ssro__ivvmx = nxoe__ahr.size
    afzc__evs = args[yerv__ykg]
    nive__hzxwn = lir.Constant(afzc__evs.type, 0)
    afzc__evs = builder.select(cgutils.is_neg_int(builder, afzc__evs),
        nive__hzxwn, afzc__evs)
    vcy__wyqif = builder.mul(afzc__evs, ssro__ivvmx)
    wlyq__bzp = ListInstance.allocate(context, builder, sig.return_type,
        vcy__wyqif)
    wlyq__bzp.size = vcy__wyqif
    with cgutils.for_range_slice(builder, nive__hzxwn, vcy__wyqif,
        ssro__ivvmx, inc=True) as (lur__pzrz, _):
        with cgutils.for_range(builder, ssro__ivvmx) as lchxr__doczo:
            value = nxoe__ahr.getitem(lchxr__doczo.index)
            wlyq__bzp.setitem(builder.add(lchxr__doczo.index, lur__pzrz),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, wlyq__bzp.value)


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
    xygvy__zoqgg = first.unify(self, second)
    if xygvy__zoqgg is not None:
        return xygvy__zoqgg
    xygvy__zoqgg = second.unify(self, first)
    if xygvy__zoqgg is not None:
        return xygvy__zoqgg
    wvclb__ihmun = self.can_convert(fromty=first, toty=second)
    if wvclb__ihmun is not None and wvclb__ihmun <= Conversion.safe:
        return second
    wvclb__ihmun = self.can_convert(fromty=second, toty=first)
    if wvclb__ihmun is not None and wvclb__ihmun <= Conversion.safe:
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
    vcy__wyqif = payload.used
    listobj = c.pyapi.list_new(vcy__wyqif)
    mvux__wpesf = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(mvux__wpesf, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(vcy__wyqif
            .type, 0))
        with payload._iterate() as lchxr__doczo:
            i = c.builder.load(index)
            item = lchxr__doczo.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return mvux__wpesf, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    ygdi__oauq = h.type
    aqha__pcnp = self.mask
    dtype = self._ty.dtype
    tbbaj__wnus = context.typing_context
    fnty = tbbaj__wnus.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(tbbaj__wnus, (dtype, dtype), {})
    vjt__pnkj = context.get_function(fnty, sig)
    vxxk__hab = ir.Constant(ygdi__oauq, 1)
    dsbyw__gnv = ir.Constant(ygdi__oauq, 5)
    vwe__mjv = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, aqha__pcnp))
    if for_insert:
        psb__psi = aqha__pcnp.type(-1)
        fsa__aqsnd = cgutils.alloca_once_value(builder, psb__psi)
    lerxp__epm = builder.append_basic_block('lookup.body')
    bbbqe__upqll = builder.append_basic_block('lookup.found')
    vamqe__wkfzr = builder.append_basic_block('lookup.not_found')
    kbufa__bbe = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        qlzcu__wbrta = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, qlzcu__wbrta)):
            eck__dco = vjt__pnkj(builder, (item, entry.key))
            with builder.if_then(eck__dco):
                builder.branch(bbbqe__upqll)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, qlzcu__wbrta)):
            builder.branch(vamqe__wkfzr)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, qlzcu__wbrta)):
                paww__oeti = builder.load(fsa__aqsnd)
                paww__oeti = builder.select(builder.icmp_unsigned('==',
                    paww__oeti, psb__psi), i, paww__oeti)
                builder.store(paww__oeti, fsa__aqsnd)
    with cgutils.for_range(builder, ir.Constant(ygdi__oauq, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, vxxk__hab)
        i = builder.and_(i, aqha__pcnp)
        builder.store(i, index)
    builder.branch(lerxp__epm)
    with builder.goto_block(lerxp__epm):
        i = builder.load(index)
        check_entry(i)
        xfxi__xwwv = builder.load(vwe__mjv)
        xfxi__xwwv = builder.lshr(xfxi__xwwv, dsbyw__gnv)
        i = builder.add(vxxk__hab, builder.mul(i, dsbyw__gnv))
        i = builder.and_(aqha__pcnp, builder.add(i, xfxi__xwwv))
        builder.store(i, index)
        builder.store(xfxi__xwwv, vwe__mjv)
        builder.branch(lerxp__epm)
    with builder.goto_block(vamqe__wkfzr):
        if for_insert:
            i = builder.load(index)
            paww__oeti = builder.load(fsa__aqsnd)
            i = builder.select(builder.icmp_unsigned('==', paww__oeti,
                psb__psi), i, paww__oeti)
            builder.store(i, index)
        builder.branch(kbufa__bbe)
    with builder.goto_block(bbbqe__upqll):
        builder.branch(kbufa__bbe)
    builder.position_at_end(kbufa__bbe)
    ymh__durxo = builder.phi(ir.IntType(1), 'found')
    ymh__durxo.add_incoming(cgutils.true_bit, bbbqe__upqll)
    ymh__durxo.add_incoming(cgutils.false_bit, vamqe__wkfzr)
    return ymh__durxo, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    pppyq__iftgt = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    gxg__givq = payload.used
    vxxk__hab = ir.Constant(gxg__givq.type, 1)
    gxg__givq = payload.used = builder.add(gxg__givq, vxxk__hab)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, pppyq__iftgt), likely=True):
        payload.fill = builder.add(payload.fill, vxxk__hab)
    if do_resize:
        self.upsize(gxg__givq)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    ymh__durxo, i = payload._lookup(item, h, for_insert=True)
    pfu__qwcxz = builder.not_(ymh__durxo)
    with builder.if_then(pfu__qwcxz):
        entry = payload.get_entry(i)
        pppyq__iftgt = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        gxg__givq = payload.used
        vxxk__hab = ir.Constant(gxg__givq.type, 1)
        gxg__givq = payload.used = builder.add(gxg__givq, vxxk__hab)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, pppyq__iftgt), likely=True):
            payload.fill = builder.add(payload.fill, vxxk__hab)
        if do_resize:
            self.upsize(gxg__givq)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    gxg__givq = payload.used
    vxxk__hab = ir.Constant(gxg__givq.type, 1)
    gxg__givq = payload.used = self._builder.sub(gxg__givq, vxxk__hab)
    if do_resize:
        self.downsize(gxg__givq)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    ktf__vxo = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, ktf__vxo)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    jcd__fpn = payload
    mvux__wpesf = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(mvux__wpesf), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with jcd__fpn._iterate() as lchxr__doczo:
        entry = lchxr__doczo.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(jcd__fpn.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as lchxr__doczo:
        entry = lchxr__doczo.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    mvux__wpesf = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(mvux__wpesf), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    mvux__wpesf = cgutils.alloca_once_value(builder, cgutils.true_bit)
    ygdi__oauq = context.get_value_type(types.intp)
    nive__hzxwn = ir.Constant(ygdi__oauq, 0)
    vxxk__hab = ir.Constant(ygdi__oauq, 1)
    zwyck__ibwn = context.get_data_type(types.SetPayload(self._ty))
    nwllz__auont = context.get_abi_sizeof(zwyck__ibwn)
    crflm__ccdb = self._entrysize
    nwllz__auont -= crflm__ccdb
    bxkws__epqz, ila__uer = cgutils.muladd_with_overflow(builder, nentries,
        ir.Constant(ygdi__oauq, crflm__ccdb), ir.Constant(ygdi__oauq,
        nwllz__auont))
    with builder.if_then(ila__uer, likely=False):
        builder.store(cgutils.false_bit, mvux__wpesf)
    with builder.if_then(builder.load(mvux__wpesf), likely=True):
        if realloc:
            boew__lufek = self._set.meminfo
            kezrs__wbd = context.nrt.meminfo_varsize_alloc(builder,
                boew__lufek, size=bxkws__epqz)
            ghjr__ybd = cgutils.is_null(builder, kezrs__wbd)
        else:
            ngreq__lqrnf = _imp_dtor(context, builder.module, self._ty)
            boew__lufek = context.nrt.meminfo_new_varsize_dtor(builder,
                bxkws__epqz, builder.bitcast(ngreq__lqrnf, cgutils.voidptr_t))
            ghjr__ybd = cgutils.is_null(builder, boew__lufek)
        with builder.if_else(ghjr__ybd, likely=False) as (jfm__aindt, jkf__ubm
            ):
            with jfm__aindt:
                builder.store(cgutils.false_bit, mvux__wpesf)
            with jkf__ubm:
                if not realloc:
                    self._set.meminfo = boew__lufek
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, bxkws__epqz, 255)
                payload.used = nive__hzxwn
                payload.fill = nive__hzxwn
                payload.finger = nive__hzxwn
                rcvf__lin = builder.sub(nentries, vxxk__hab)
                payload.mask = rcvf__lin
    return builder.load(mvux__wpesf)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    mvux__wpesf = cgutils.alloca_once_value(builder, cgutils.true_bit)
    ygdi__oauq = context.get_value_type(types.intp)
    nive__hzxwn = ir.Constant(ygdi__oauq, 0)
    vxxk__hab = ir.Constant(ygdi__oauq, 1)
    zwyck__ibwn = context.get_data_type(types.SetPayload(self._ty))
    nwllz__auont = context.get_abi_sizeof(zwyck__ibwn)
    crflm__ccdb = self._entrysize
    nwllz__auont -= crflm__ccdb
    aqha__pcnp = src_payload.mask
    nentries = builder.add(vxxk__hab, aqha__pcnp)
    bxkws__epqz = builder.add(ir.Constant(ygdi__oauq, nwllz__auont),
        builder.mul(ir.Constant(ygdi__oauq, crflm__ccdb), nentries))
    with builder.if_then(builder.load(mvux__wpesf), likely=True):
        ngreq__lqrnf = _imp_dtor(context, builder.module, self._ty)
        boew__lufek = context.nrt.meminfo_new_varsize_dtor(builder,
            bxkws__epqz, builder.bitcast(ngreq__lqrnf, cgutils.voidptr_t))
        ghjr__ybd = cgutils.is_null(builder, boew__lufek)
        with builder.if_else(ghjr__ybd, likely=False) as (jfm__aindt, jkf__ubm
            ):
            with jfm__aindt:
                builder.store(cgutils.false_bit, mvux__wpesf)
            with jkf__ubm:
                self._set.meminfo = boew__lufek
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = nive__hzxwn
                payload.mask = aqha__pcnp
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, crflm__ccdb)
                with src_payload._iterate() as lchxr__doczo:
                    context.nrt.incref(builder, self._ty.dtype,
                        lchxr__doczo.entry.key)
    return builder.load(mvux__wpesf)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    bzat__kukf = context.get_value_type(types.voidptr)
    ykvf__axkx = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [bzat__kukf, ykvf__axkx, bzat__kukf])
    wuyk__nugps = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=wuyk__nugps)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        makno__hcd = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer()
            )
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, makno__hcd)
        with payload._iterate() as lchxr__doczo:
            entry = lchxr__doczo.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    dqgr__ucij, = sig.args
    hzs__tsxv, = args
    msjl__auq = numba.core.imputils.call_len(context, builder, dqgr__ucij,
        hzs__tsxv)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, msjl__auq)
    with numba.core.imputils.for_iter(context, builder, dqgr__ucij, hzs__tsxv
        ) as lchxr__doczo:
        inst.add(lchxr__doczo.value)
        context.nrt.decref(builder, set_type.dtype, lchxr__doczo.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    dqgr__ucij = sig.args[1]
    hzs__tsxv = args[1]
    msjl__auq = numba.core.imputils.call_len(context, builder, dqgr__ucij,
        hzs__tsxv)
    if msjl__auq is not None:
        gork__mjdjd = builder.add(inst.payload.used, msjl__auq)
        inst.upsize(gork__mjdjd)
    with numba.core.imputils.for_iter(context, builder, dqgr__ucij, hzs__tsxv
        ) as lchxr__doczo:
        xwd__xlg = context.cast(builder, lchxr__doczo.value, dqgr__ucij.
            dtype, inst.dtype)
        inst.add(xwd__xlg)
        context.nrt.decref(builder, dqgr__ucij.dtype, lchxr__doczo.value)
    if msjl__auq is not None:
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
    muihs__hkygp = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, muihs__hkygp, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    aunl__vxnu = target_context.get_executable(library, fndesc, env)
    wevgo__fnt = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=aunl__vxnu, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return wevgo__fnt


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
