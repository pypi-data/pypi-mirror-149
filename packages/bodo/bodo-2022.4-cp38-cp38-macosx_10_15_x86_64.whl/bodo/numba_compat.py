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
    myn__hpka = numba.core.bytecode.FunctionIdentity.from_function(func)
    qod__ztewi = numba.core.interpreter.Interpreter(myn__hpka)
    tdfto__yvd = numba.core.bytecode.ByteCode(func_id=myn__hpka)
    func_ir = qod__ztewi.interpret(tdfto__yvd)
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
        akdbd__rwgh = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        akdbd__rwgh.run()
    vnwip__idqbg = numba.core.postproc.PostProcessor(func_ir)
    vnwip__idqbg.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, opiy__kokhg in visit_vars_extensions.items():
        if isinstance(stmt, t):
            opiy__kokhg(stmt, callback, cbdata)
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
    vhj__emvz = ['ravel', 'transpose', 'reshape']
    for fnr__vtc in blocks.values():
        for hbbqi__nonoa in fnr__vtc.body:
            if type(hbbqi__nonoa) in alias_analysis_extensions:
                opiy__kokhg = alias_analysis_extensions[type(hbbqi__nonoa)]
                opiy__kokhg(hbbqi__nonoa, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(hbbqi__nonoa, ir.Assign):
                xfqnp__yvexh = hbbqi__nonoa.value
                boqr__rfb = hbbqi__nonoa.target.name
                if is_immutable_type(boqr__rfb, typemap):
                    continue
                if isinstance(xfqnp__yvexh, ir.Var
                    ) and boqr__rfb != xfqnp__yvexh.name:
                    _add_alias(boqr__rfb, xfqnp__yvexh.name, alias_map,
                        arg_aliases)
                if isinstance(xfqnp__yvexh, ir.Expr) and (xfqnp__yvexh.op ==
                    'cast' or xfqnp__yvexh.op in ['getitem', 'static_getitem']
                    ):
                    _add_alias(boqr__rfb, xfqnp__yvexh.value.name,
                        alias_map, arg_aliases)
                if isinstance(xfqnp__yvexh, ir.Expr
                    ) and xfqnp__yvexh.op == 'inplace_binop':
                    _add_alias(boqr__rfb, xfqnp__yvexh.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(xfqnp__yvexh, ir.Expr
                    ) and xfqnp__yvexh.op == 'getattr' and xfqnp__yvexh.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(boqr__rfb, xfqnp__yvexh.value.name,
                        alias_map, arg_aliases)
                if (isinstance(xfqnp__yvexh, ir.Expr) and xfqnp__yvexh.op ==
                    'getattr' and xfqnp__yvexh.attr not in ['shape'] and 
                    xfqnp__yvexh.value.name in arg_aliases):
                    _add_alias(boqr__rfb, xfqnp__yvexh.value.name,
                        alias_map, arg_aliases)
                if isinstance(xfqnp__yvexh, ir.Expr
                    ) and xfqnp__yvexh.op == 'getattr' and xfqnp__yvexh.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(boqr__rfb, xfqnp__yvexh.value.name,
                        alias_map, arg_aliases)
                if isinstance(xfqnp__yvexh, ir.Expr) and xfqnp__yvexh.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(boqr__rfb, typemap):
                    for vfkj__qztq in xfqnp__yvexh.items:
                        _add_alias(boqr__rfb, vfkj__qztq.name, alias_map,
                            arg_aliases)
                if isinstance(xfqnp__yvexh, ir.Expr
                    ) and xfqnp__yvexh.op == 'call':
                    lnaah__tin = guard(find_callname, func_ir, xfqnp__yvexh,
                        typemap)
                    if lnaah__tin is None:
                        continue
                    dpheh__rasxt, tjjgb__qie = lnaah__tin
                    if lnaah__tin in alias_func_extensions:
                        rexj__onv = alias_func_extensions[lnaah__tin]
                        rexj__onv(boqr__rfb, xfqnp__yvexh.args, alias_map,
                            arg_aliases)
                    if tjjgb__qie == 'numpy' and dpheh__rasxt in vhj__emvz:
                        _add_alias(boqr__rfb, xfqnp__yvexh.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(tjjgb__qie, ir.Var
                        ) and dpheh__rasxt in vhj__emvz:
                        _add_alias(boqr__rfb, tjjgb__qie.name, alias_map,
                            arg_aliases)
    bmfd__kuqi = copy.deepcopy(alias_map)
    for vfkj__qztq in bmfd__kuqi:
        for eakr__vxns in bmfd__kuqi[vfkj__qztq]:
            alias_map[vfkj__qztq] |= alias_map[eakr__vxns]
        for eakr__vxns in bmfd__kuqi[vfkj__qztq]:
            alias_map[eakr__vxns] = alias_map[vfkj__qztq]
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
    gyte__qam = compute_cfg_from_blocks(func_ir.blocks)
    czp__fbc = compute_use_defs(func_ir.blocks)
    hmhf__nri = compute_live_map(gyte__qam, func_ir.blocks, czp__fbc.usemap,
        czp__fbc.defmap)
    eev__zsmt = True
    while eev__zsmt:
        eev__zsmt = False
        for bmy__ysgj, block in func_ir.blocks.items():
            lives = {vfkj__qztq.name for vfkj__qztq in block.terminator.
                list_vars()}
            for hwfu__jlt, qzwdy__wdx in gyte__qam.successors(bmy__ysgj):
                lives |= hmhf__nri[hwfu__jlt]
            lua__pet = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    boqr__rfb = stmt.target
                    flmxz__isup = stmt.value
                    if boqr__rfb.name not in lives:
                        if isinstance(flmxz__isup, ir.Expr
                            ) and flmxz__isup.op == 'make_function':
                            continue
                        if isinstance(flmxz__isup, ir.Expr
                            ) and flmxz__isup.op == 'getattr':
                            continue
                        if isinstance(flmxz__isup, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(boqr__rfb,
                            None), types.Function):
                            continue
                        if isinstance(flmxz__isup, ir.Expr
                            ) and flmxz__isup.op == 'build_map':
                            continue
                        if isinstance(flmxz__isup, ir.Expr
                            ) and flmxz__isup.op == 'build_tuple':
                            continue
                    if isinstance(flmxz__isup, ir.Var
                        ) and boqr__rfb.name == flmxz__isup.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    sko__jowr = analysis.ir_extension_usedefs[type(stmt)]
                    vrqkn__fqp, lgqw__zlfym = sko__jowr(stmt)
                    lives -= lgqw__zlfym
                    lives |= vrqkn__fqp
                else:
                    lives |= {vfkj__qztq.name for vfkj__qztq in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(boqr__rfb.name)
                lua__pet.append(stmt)
            lua__pet.reverse()
            if len(block.body) != len(lua__pet):
                eev__zsmt = True
            block.body = lua__pet


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    kutkj__egeju = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (kutkj__egeju,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    ozu__hzas = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), ozu__hzas)


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
            for bnvke__qtts in fnty.templates:
                self._inline_overloads.update(bnvke__qtts._inline_overloads)
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
    ozu__hzas = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), ozu__hzas)
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
    okk__ftza, jzkr__ynis = self._get_impl(args, kws)
    if okk__ftza is None:
        return
    cvfju__xqyl = types.Dispatcher(okk__ftza)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        fukxy__kqyx = okk__ftza._compiler
        flags = compiler.Flags()
        irx__mdwg = fukxy__kqyx.targetdescr.typing_context
        crpep__omj = fukxy__kqyx.targetdescr.target_context
        afs__fhj = fukxy__kqyx.pipeline_class(irx__mdwg, crpep__omj, None,
            None, None, flags, None)
        pjzd__awc = InlineWorker(irx__mdwg, crpep__omj, fukxy__kqyx.locals,
            afs__fhj, flags, None)
        llgrq__jbh = cvfju__xqyl.dispatcher.get_call_template
        bnvke__qtts, mwt__sdr, xvm__wajl, kws = llgrq__jbh(jzkr__ynis, kws)
        if xvm__wajl in self._inline_overloads:
            return self._inline_overloads[xvm__wajl]['iinfo'].signature
        ir = pjzd__awc.run_untyped_passes(cvfju__xqyl.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, crpep__omj, ir, xvm__wajl, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, xvm__wajl, None)
        self._inline_overloads[sig.args] = {'folded_args': xvm__wajl}
        nppl__hxk = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = nppl__hxk
        if not self._inline.is_always_inline:
            sig = cvfju__xqyl.get_call_type(self.context, jzkr__ynis, kws)
            self._compiled_overloads[sig.args] = cvfju__xqyl.get_overload(sig)
        efoj__lahbx = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': xvm__wajl,
            'iinfo': efoj__lahbx}
    else:
        sig = cvfju__xqyl.get_call_type(self.context, jzkr__ynis, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = cvfju__xqyl.get_overload(sig)
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
    mrykn__kjmda = [True, False]
    creb__nnsf = [False, True]
    fwg__faj = _ResolutionFailures(context, self, args, kws, depth=self._depth)
    from numba.core.target_extension import get_local_target
    sdvpt__hzmxl = get_local_target(context)
    dnulq__gwud = utils.order_by_target_specificity(sdvpt__hzmxl, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for pkz__rkt in dnulq__gwud:
        uuxim__fmfuc = pkz__rkt(context)
        enxs__adcq = (mrykn__kjmda if uuxim__fmfuc.prefer_literal else
            creb__nnsf)
        enxs__adcq = [True] if getattr(uuxim__fmfuc, '_no_unliteral', False
            ) else enxs__adcq
        for keedg__xiku in enxs__adcq:
            try:
                if keedg__xiku:
                    sig = uuxim__fmfuc.apply(args, kws)
                else:
                    ifpos__vlv = tuple([_unlit_non_poison(a) for a in args])
                    cxvj__rpmx = {aqhp__thwjd: _unlit_non_poison(vfkj__qztq
                        ) for aqhp__thwjd, vfkj__qztq in kws.items()}
                    sig = uuxim__fmfuc.apply(ifpos__vlv, cxvj__rpmx)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    fwg__faj.add_error(uuxim__fmfuc, False, e, keedg__xiku)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = uuxim__fmfuc.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    jgp__bnwio = getattr(uuxim__fmfuc, 'cases', None)
                    if jgp__bnwio is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            jgp__bnwio)
                    else:
                        msg = 'No match.'
                    fwg__faj.add_error(uuxim__fmfuc, True, msg, keedg__xiku)
    fwg__faj.raise_error()


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
    bnvke__qtts = self.template(context)
    jjca__wzvw = None
    ijpt__yswa = None
    rdct__lpplp = None
    enxs__adcq = [True, False] if bnvke__qtts.prefer_literal else [False, True]
    enxs__adcq = [True] if getattr(bnvke__qtts, '_no_unliteral', False
        ) else enxs__adcq
    for keedg__xiku in enxs__adcq:
        if keedg__xiku:
            try:
                rdct__lpplp = bnvke__qtts.apply(args, kws)
            except Exception as fex__iylgh:
                if isinstance(fex__iylgh, errors.ForceLiteralArg):
                    raise fex__iylgh
                jjca__wzvw = fex__iylgh
                rdct__lpplp = None
            else:
                break
        else:
            yhdj__yssv = tuple([_unlit_non_poison(a) for a in args])
            inr__aht = {aqhp__thwjd: _unlit_non_poison(vfkj__qztq) for 
                aqhp__thwjd, vfkj__qztq in kws.items()}
            dwjm__qjr = yhdj__yssv == args and kws == inr__aht
            if not dwjm__qjr and rdct__lpplp is None:
                try:
                    rdct__lpplp = bnvke__qtts.apply(yhdj__yssv, inr__aht)
                except Exception as fex__iylgh:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        fex__iylgh, errors.NumbaError):
                        raise fex__iylgh
                    if isinstance(fex__iylgh, errors.ForceLiteralArg):
                        if bnvke__qtts.prefer_literal:
                            raise fex__iylgh
                    ijpt__yswa = fex__iylgh
                else:
                    break
    if rdct__lpplp is None and (ijpt__yswa is not None or jjca__wzvw is not
        None):
        vmab__psk = '- Resolution failure for {} arguments:\n{}\n'
        vknc__llerq = _termcolor.highlight(vmab__psk)
        if numba.core.config.DEVELOPER_MODE:
            rwegr__crr = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    hmo__jdnjh = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    hmo__jdnjh = ['']
                jjjsa__wuvb = '\n{}'.format(2 * rwegr__crr)
                ann__jid = _termcolor.reset(jjjsa__wuvb + jjjsa__wuvb.join(
                    _bt_as_lines(hmo__jdnjh)))
                return _termcolor.reset(ann__jid)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            lrvy__yaa = str(e)
            lrvy__yaa = lrvy__yaa if lrvy__yaa else str(repr(e)) + add_bt(e)
            ecqk__vskly = errors.TypingError(textwrap.dedent(lrvy__yaa))
            return vknc__llerq.format(literalness, str(ecqk__vskly))
        import bodo
        if isinstance(jjca__wzvw, bodo.utils.typing.BodoError):
            raise jjca__wzvw
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', jjca__wzvw) +
                nested_msg('non-literal', ijpt__yswa))
        else:
            if 'missing a required argument' in jjca__wzvw.msg:
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
            raise errors.TypingError(msg, loc=jjca__wzvw.loc)
    return rdct__lpplp


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
    dpheh__rasxt = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=dpheh__rasxt)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            vwry__yei = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), vwry__yei)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    utqnq__wlkzg = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            utqnq__wlkzg.append(types.Omitted(a.value))
        else:
            utqnq__wlkzg.append(self.typeof_pyval(a))
    raiaa__rgjt = None
    try:
        error = None
        raiaa__rgjt = self.compile(tuple(utqnq__wlkzg))
    except errors.ForceLiteralArg as e:
        rgbz__yxvst = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if rgbz__yxvst:
            cwpbd__xgvj = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            dzyj__nxxb = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(rgbz__yxvst))
            raise errors.CompilerError(cwpbd__xgvj.format(dzyj__nxxb))
        jzkr__ynis = []
        try:
            for i, vfkj__qztq in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        jzkr__ynis.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        jzkr__ynis.append(types.literal(args[i]))
                else:
                    jzkr__ynis.append(args[i])
            args = jzkr__ynis
        except (OSError, FileNotFoundError) as yfq__wbs:
            error = FileNotFoundError(str(yfq__wbs) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                raiaa__rgjt = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        fmhq__ncrcw = []
        for i, trvw__utts in enumerate(args):
            val = trvw__utts.value if isinstance(trvw__utts, numba.core.
                dispatcher.OmittedArg) else trvw__utts
            try:
                rzrd__eznqy = typeof(val, Purpose.argument)
            except ValueError as hqfkl__fvu:
                fmhq__ncrcw.append((i, str(hqfkl__fvu)))
            else:
                if rzrd__eznqy is None:
                    fmhq__ncrcw.append((i,
                        f'cannot determine Numba type of value {val}'))
        if fmhq__ncrcw:
            zhc__xpij = '\n'.join(f'- argument {i}: {yqbe__pqa}' for i,
                yqbe__pqa in fmhq__ncrcw)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{zhc__xpij}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                msh__fdd = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                sazx__yvot = False
                for kggd__hlzsw in msh__fdd:
                    if kggd__hlzsw in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        sazx__yvot = True
                        break
                if not sazx__yvot:
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
                vwry__yei = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), vwry__yei)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return raiaa__rgjt


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
    for ywd__qipx in cres.library._codegen._engine._defined_symbols:
        if ywd__qipx.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in ywd__qipx and (
            'bodo_gb_udf_update_local' in ywd__qipx or 
            'bodo_gb_udf_combine' in ywd__qipx or 'bodo_gb_udf_eval' in
            ywd__qipx or 'bodo_gb_apply_general_udfs' in ywd__qipx):
            gb_agg_cfunc_addr[ywd__qipx
                ] = cres.library.get_pointer_to_function(ywd__qipx)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for ywd__qipx in cres.library._codegen._engine._defined_symbols:
        if ywd__qipx.startswith('cfunc') and ('get_join_cond_addr' not in
            ywd__qipx or 'bodo_join_gen_cond' in ywd__qipx):
            join_gen_cond_cfunc_addr[ywd__qipx
                ] = cres.library.get_pointer_to_function(ywd__qipx)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    okk__ftza = self._get_dispatcher_for_current_target()
    if okk__ftza is not self:
        return okk__ftza.compile(sig)
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
            ynci__nrq = self.overloads.get(tuple(args))
            if ynci__nrq is not None:
                return ynci__nrq.entry_point
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
            ipno__xtn = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=ipno__xtn):
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
    egknu__yhg = self._final_module
    mzg__wwy = []
    ftju__lfc = 0
    for fn in egknu__yhg.functions:
        ftju__lfc += 1
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
            mzg__wwy.append(fn.name)
    if ftju__lfc == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if mzg__wwy:
        egknu__yhg = egknu__yhg.clone()
        for name in mzg__wwy:
            egknu__yhg.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = egknu__yhg
    return egknu__yhg


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
    for mxowr__tzpa in self.constraints:
        loc = mxowr__tzpa.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                mxowr__tzpa(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                ltmq__mebcy = numba.core.errors.TypingError(str(e), loc=
                    mxowr__tzpa.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(ltmq__mebcy, e))
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
                    ltmq__mebcy = numba.core.errors.TypingError(msg.format(
                        con=mxowr__tzpa, err=str(e)), loc=mxowr__tzpa.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(ltmq__mebcy, e))
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
    for oqufh__una in self._failures.values():
        for mrl__fpy in oqufh__una:
            if isinstance(mrl__fpy.error, ForceLiteralArg):
                raise mrl__fpy.error
            if isinstance(mrl__fpy.error, bodo.utils.typing.BodoError):
                raise mrl__fpy.error
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
    not__uzag = False
    lua__pet = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        ivtaf__hwb = set()
        kufwx__ojna = lives & alias_set
        for vfkj__qztq in kufwx__ojna:
            ivtaf__hwb |= alias_map[vfkj__qztq]
        lives_n_aliases = lives | ivtaf__hwb | arg_aliases
        if type(stmt) in remove_dead_extensions:
            opiy__kokhg = remove_dead_extensions[type(stmt)]
            stmt = opiy__kokhg(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                not__uzag = True
                continue
        if isinstance(stmt, ir.Assign):
            boqr__rfb = stmt.target
            flmxz__isup = stmt.value
            if boqr__rfb.name not in lives and has_no_side_effect(flmxz__isup,
                lives_n_aliases, call_table):
                not__uzag = True
                continue
            if saved_array_analysis and boqr__rfb.name in lives and is_expr(
                flmxz__isup, 'getattr'
                ) and flmxz__isup.attr == 'shape' and is_array_typ(typemap[
                flmxz__isup.value.name]
                ) and flmxz__isup.value.name not in lives:
                hen__outw = {vfkj__qztq: aqhp__thwjd for aqhp__thwjd,
                    vfkj__qztq in func_ir.blocks.items()}
                if block in hen__outw:
                    bmy__ysgj = hen__outw[block]
                    pho__gjdb = saved_array_analysis.get_equiv_set(bmy__ysgj)
                    tvjv__yimxf = pho__gjdb.get_equiv_set(flmxz__isup.value)
                    if tvjv__yimxf is not None:
                        for vfkj__qztq in tvjv__yimxf:
                            if vfkj__qztq.endswith('#0'):
                                vfkj__qztq = vfkj__qztq[:-2]
                            if vfkj__qztq in typemap and is_array_typ(typemap
                                [vfkj__qztq]) and vfkj__qztq in lives:
                                flmxz__isup.value = ir.Var(flmxz__isup.
                                    value.scope, vfkj__qztq, flmxz__isup.
                                    value.loc)
                                not__uzag = True
                                break
            if isinstance(flmxz__isup, ir.Var
                ) and boqr__rfb.name == flmxz__isup.name:
                not__uzag = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                not__uzag = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            sko__jowr = analysis.ir_extension_usedefs[type(stmt)]
            vrqkn__fqp, lgqw__zlfym = sko__jowr(stmt)
            lives -= lgqw__zlfym
            lives |= vrqkn__fqp
        else:
            lives |= {vfkj__qztq.name for vfkj__qztq in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                foook__bne = set()
                if isinstance(flmxz__isup, ir.Expr):
                    foook__bne = {vfkj__qztq.name for vfkj__qztq in
                        flmxz__isup.list_vars()}
                if boqr__rfb.name not in foook__bne:
                    lives.remove(boqr__rfb.name)
        lua__pet.append(stmt)
    lua__pet.reverse()
    block.body = lua__pet
    return not__uzag


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            ohhn__enjz, = args
            if isinstance(ohhn__enjz, types.IterableType):
                dtype = ohhn__enjz.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), ohhn__enjz)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    dank__tva = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (dank__tva, self.dtype)
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
        except LiteralTypingError as pdyw__kozbj:
            return
    try:
        return literal(value)
    except LiteralTypingError as pdyw__kozbj:
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
        fohuc__xkq = py_func.__qualname__
    except AttributeError as pdyw__kozbj:
        fohuc__xkq = py_func.__name__
    wuy__rhbk = inspect.getfile(py_func)
    for cls in self._locator_classes:
        cxko__rcpsu = cls.from_function(py_func, wuy__rhbk)
        if cxko__rcpsu is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (fohuc__xkq, wuy__rhbk))
    self._locator = cxko__rcpsu
    qud__fkt = inspect.getfile(py_func)
    aiwfy__qedu = os.path.splitext(os.path.basename(qud__fkt))[0]
    if wuy__rhbk.startswith('<ipython-'):
        tju__tlcl = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', aiwfy__qedu, count=1)
        if tju__tlcl == aiwfy__qedu:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        aiwfy__qedu = tju__tlcl
    jvp__cnhh = '%s.%s' % (aiwfy__qedu, fohuc__xkq)
    omuy__rmd = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(jvp__cnhh, omuy__rmd)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    kathw__tik = list(filter(lambda a: self._istuple(a.name), args))
    if len(kathw__tik) == 2 and fn.__name__ == 'add':
        fhpui__rljna = self.typemap[kathw__tik[0].name]
        loeh__zfp = self.typemap[kathw__tik[1].name]
        if fhpui__rljna.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                kathw__tik[1]))
        if loeh__zfp.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                kathw__tik[0]))
        try:
            toxkf__fya = [equiv_set.get_shape(x) for x in kathw__tik]
            if None in toxkf__fya:
                return None
            wuob__ceq = sum(toxkf__fya, ())
            return ArrayAnalysis.AnalyzeResult(shape=wuob__ceq)
        except GuardException as pdyw__kozbj:
            return None
    ymk__kcl = list(filter(lambda a: self._isarray(a.name), args))
    require(len(ymk__kcl) > 0)
    nlc__def = [x.name for x in ymk__kcl]
    wrwm__jdirz = [self.typemap[x.name].ndim for x in ymk__kcl]
    bwe__cjh = max(wrwm__jdirz)
    require(bwe__cjh > 0)
    toxkf__fya = [equiv_set.get_shape(x) for x in ymk__kcl]
    if any(a is None for a in toxkf__fya):
        return ArrayAnalysis.AnalyzeResult(shape=ymk__kcl[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, ymk__kcl))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, toxkf__fya,
        nlc__def)


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
    lmv__hihu = code_obj.code
    cyb__snyqg = len(lmv__hihu.co_freevars)
    ogps__dql = lmv__hihu.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        phn__hom, op = ir_utils.find_build_sequence(caller_ir, code_obj.closure
            )
        assert op == 'build_tuple'
        ogps__dql = [vfkj__qztq.name for vfkj__qztq in phn__hom]
    jkaqg__xbirh = caller_ir.func_id.func.__globals__
    try:
        jkaqg__xbirh = getattr(code_obj, 'globals', jkaqg__xbirh)
    except KeyError as pdyw__kozbj:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/source/programming_with_bodo/bodo_api_reference/udfs.html"
        )
    lqlwb__nazh = []
    for x in ogps__dql:
        try:
            ofhgc__gbzri = caller_ir.get_definition(x)
        except KeyError as pdyw__kozbj:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(ofhgc__gbzri, (ir.Const, ir.Global, ir.FreeVar)):
            val = ofhgc__gbzri.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                kutkj__egeju = ir_utils.mk_unique_var('nested_func').replace(
                    '.', '_')
                jkaqg__xbirh[kutkj__egeju] = bodo.jit(distributed=False)(val)
                jkaqg__xbirh[kutkj__egeju].is_nested_func = True
                val = kutkj__egeju
            if isinstance(val, CPUDispatcher):
                kutkj__egeju = ir_utils.mk_unique_var('nested_func').replace(
                    '.', '_')
                jkaqg__xbirh[kutkj__egeju] = val
                val = kutkj__egeju
            lqlwb__nazh.append(val)
        elif isinstance(ofhgc__gbzri, ir.Expr
            ) and ofhgc__gbzri.op == 'make_function':
            smxm__btjq = convert_code_obj_to_function(ofhgc__gbzri, caller_ir)
            kutkj__egeju = ir_utils.mk_unique_var('nested_func').replace('.',
                '_')
            jkaqg__xbirh[kutkj__egeju] = bodo.jit(distributed=False)(smxm__btjq
                )
            jkaqg__xbirh[kutkj__egeju].is_nested_func = True
            lqlwb__nazh.append(kutkj__egeju)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    wufzf__bkd = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        lqlwb__nazh)])
    zwmvr__ilvu = ','.join([('c_%d' % i) for i in range(cyb__snyqg)])
    wpikb__owoky = list(lmv__hihu.co_varnames)
    qmnj__pvjd = 0
    fkis__rcvcw = lmv__hihu.co_argcount
    llz__qsi = caller_ir.get_definition(code_obj.defaults)
    if llz__qsi is not None:
        if isinstance(llz__qsi, tuple):
            d = [caller_ir.get_definition(x).value for x in llz__qsi]
            gff__fywc = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in llz__qsi.items]
            gff__fywc = tuple(d)
        qmnj__pvjd = len(gff__fywc)
    dagv__izyi = fkis__rcvcw - qmnj__pvjd
    qjimd__hhasl = ','.join([('%s' % wpikb__owoky[i]) for i in range(
        dagv__izyi)])
    if qmnj__pvjd:
        ojni__osld = [('%s = %s' % (wpikb__owoky[i + dagv__izyi], gff__fywc
            [i])) for i in range(qmnj__pvjd)]
        qjimd__hhasl += ', '
        qjimd__hhasl += ', '.join(ojni__osld)
    return _create_function_from_code_obj(lmv__hihu, wufzf__bkd,
        qjimd__hhasl, zwmvr__ilvu, jkaqg__xbirh)


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
    for nog__hqll, (cfde__asps, sbamb__ixhnh) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % sbamb__ixhnh)
            ncg__jolzm = _pass_registry.get(cfde__asps).pass_inst
            if isinstance(ncg__jolzm, CompilerPass):
                self._runPass(nog__hqll, ncg__jolzm, state)
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
                    pipeline_name, sbamb__ixhnh)
                fpdfz__qog = self._patch_error(msg, e)
                raise fpdfz__qog
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
    xuvg__lije = None
    lgqw__zlfym = {}

    def lookup(var, already_seen, varonly=True):
        val = lgqw__zlfym.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    cje__igf = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        boqr__rfb = stmt.target
        flmxz__isup = stmt.value
        lgqw__zlfym[boqr__rfb.name] = flmxz__isup
        if isinstance(flmxz__isup, ir.Var) and flmxz__isup.name in lgqw__zlfym:
            flmxz__isup = lookup(flmxz__isup, set())
        if isinstance(flmxz__isup, ir.Expr):
            ckoe__wqfx = set(lookup(vfkj__qztq, set(), True).name for
                vfkj__qztq in flmxz__isup.list_vars())
            if name in ckoe__wqfx:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(flmxz__isup)]
                vfp__smp = [x for x, gie__cgp in args if gie__cgp.name != name]
                args = [(x, gie__cgp) for x, gie__cgp in args if x !=
                    gie__cgp.name]
                lgrf__gbjju = dict(args)
                if len(vfp__smp) == 1:
                    lgrf__gbjju[vfp__smp[0]] = ir.Var(boqr__rfb.scope, name +
                        '#init', boqr__rfb.loc)
                replace_vars_inner(flmxz__isup, lgrf__gbjju)
                xuvg__lije = nodes[i:]
                break
    return xuvg__lije


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
        audjz__arp = expand_aliases({vfkj__qztq.name for vfkj__qztq in stmt
            .list_vars()}, alias_map, arg_aliases)
        qmwlc__kykt = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        lel__mzya = expand_aliases({vfkj__qztq.name for vfkj__qztq in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        gjmds__ydhf = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(qmwlc__kykt & lel__mzya | gjmds__ydhf & audjz__arp) == 0:
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
    nuf__eta = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            nuf__eta.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                nuf__eta.update(get_parfor_writes(stmt, func_ir))
    return nuf__eta


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    nuf__eta = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        nuf__eta.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        nuf__eta = {vfkj__qztq.name for vfkj__qztq in stmt.df_out_vars.values()
            }
        if stmt.out_key_vars is not None:
            nuf__eta.update({vfkj__qztq.name for vfkj__qztq in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        nuf__eta = {vfkj__qztq.name for vfkj__qztq in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        nuf__eta = {vfkj__qztq.name for vfkj__qztq in stmt.out_data_vars.
            values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            nuf__eta.update({vfkj__qztq.name for vfkj__qztq in stmt.
                out_key_arrs})
            nuf__eta.update({vfkj__qztq.name for vfkj__qztq in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        lnaah__tin = guard(find_callname, func_ir, stmt.value)
        if lnaah__tin in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            nuf__eta.add(stmt.value.args[0].name)
        if lnaah__tin == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            nuf__eta.add(stmt.value.args[1].name)
    return nuf__eta


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
        opiy__kokhg = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        mzkce__ftgi = opiy__kokhg.format(self, msg)
        self.args = mzkce__ftgi,
    else:
        opiy__kokhg = _termcolor.errmsg('{0}')
        mzkce__ftgi = opiy__kokhg.format(self)
        self.args = mzkce__ftgi,
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
        for wsyv__aokby in options['distributed']:
            dist_spec[wsyv__aokby] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for wsyv__aokby in options['distributed_block']:
            dist_spec[wsyv__aokby] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    mcei__zct = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, ssb__yiawx in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(ssb__yiawx)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    lvgdj__nkv = {}
    for hnxx__vfor in reversed(inspect.getmro(cls)):
        lvgdj__nkv.update(hnxx__vfor.__dict__)
    lzewu__bau, bug__tjche, ilee__anv, pwp__cgar = {}, {}, {}, {}
    for aqhp__thwjd, vfkj__qztq in lvgdj__nkv.items():
        if isinstance(vfkj__qztq, pytypes.FunctionType):
            lzewu__bau[aqhp__thwjd] = vfkj__qztq
        elif isinstance(vfkj__qztq, property):
            bug__tjche[aqhp__thwjd] = vfkj__qztq
        elif isinstance(vfkj__qztq, staticmethod):
            ilee__anv[aqhp__thwjd] = vfkj__qztq
        else:
            pwp__cgar[aqhp__thwjd] = vfkj__qztq
    miskw__mny = (set(lzewu__bau) | set(bug__tjche) | set(ilee__anv)) & set(
        spec)
    if miskw__mny:
        raise NameError('name shadowing: {0}'.format(', '.join(miskw__mny)))
    wtfdg__udje = pwp__cgar.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(pwp__cgar)
    if pwp__cgar:
        msg = 'class members are not yet supported: {0}'
        exhm__yhb = ', '.join(pwp__cgar.keys())
        raise TypeError(msg.format(exhm__yhb))
    for aqhp__thwjd, vfkj__qztq in bug__tjche.items():
        if vfkj__qztq.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(aqhp__thwjd)
                )
    jit_methods = {aqhp__thwjd: bodo.jit(returns_maybe_distributed=
        mcei__zct)(vfkj__qztq) for aqhp__thwjd, vfkj__qztq in lzewu__bau.
        items()}
    jit_props = {}
    for aqhp__thwjd, vfkj__qztq in bug__tjche.items():
        ozu__hzas = {}
        if vfkj__qztq.fget:
            ozu__hzas['get'] = bodo.jit(vfkj__qztq.fget)
        if vfkj__qztq.fset:
            ozu__hzas['set'] = bodo.jit(vfkj__qztq.fset)
        jit_props[aqhp__thwjd] = ozu__hzas
    jit_static_methods = {aqhp__thwjd: bodo.jit(vfkj__qztq.__func__) for 
        aqhp__thwjd, vfkj__qztq in ilee__anv.items()}
    bcx__stkvm = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    kwafu__jofz = dict(class_type=bcx__stkvm, __doc__=wtfdg__udje)
    kwafu__jofz.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), kwafu__jofz)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, bcx__stkvm)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(bcx__stkvm, typingctx, targetctx).register()
    as_numba_type.register(cls, bcx__stkvm.instance_type)
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
    cekx__uthk = ','.join('{0}:{1}'.format(aqhp__thwjd, vfkj__qztq) for 
        aqhp__thwjd, vfkj__qztq in struct.items())
    voo__omfsz = ','.join('{0}:{1}'.format(aqhp__thwjd, vfkj__qztq) for 
        aqhp__thwjd, vfkj__qztq in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), cekx__uthk, voo__omfsz)
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
    mvlzg__wsmw = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if mvlzg__wsmw is None:
        return
    zqpz__aynpb, jjake__aftz = mvlzg__wsmw
    for a in itertools.chain(zqpz__aynpb, jjake__aftz.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, zqpz__aynpb, jjake__aftz)
    except ForceLiteralArg as e:
        hfo__xbbvz = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(hfo__xbbvz, self.kws)
        vys__nzksi = set()
        tnjs__zabqz = set()
        xjx__iwfh = {}
        for nog__hqll in e.requested_args:
            obla__qbvg = typeinfer.func_ir.get_definition(folded[nog__hqll])
            if isinstance(obla__qbvg, ir.Arg):
                vys__nzksi.add(obla__qbvg.index)
                if obla__qbvg.index in e.file_infos:
                    xjx__iwfh[obla__qbvg.index] = e.file_infos[obla__qbvg.index
                        ]
            else:
                tnjs__zabqz.add(nog__hqll)
        if tnjs__zabqz:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif vys__nzksi:
            raise ForceLiteralArg(vys__nzksi, loc=self.loc, file_infos=
                xjx__iwfh)
    if sig is None:
        xzox__zhep = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in zqpz__aynpb]
        args += [('%s=%s' % (aqhp__thwjd, vfkj__qztq)) for aqhp__thwjd,
            vfkj__qztq in sorted(jjake__aftz.items())]
        zbbsc__ppgbr = xzox__zhep.format(fnty, ', '.join(map(str, args)))
        adkay__dnod = context.explain_function_type(fnty)
        msg = '\n'.join([zbbsc__ppgbr, adkay__dnod])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        ehfkp__guvlc = context.unify_pairs(sig.recvr, fnty.this)
        if ehfkp__guvlc is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if ehfkp__guvlc is not None and ehfkp__guvlc.is_precise():
            gecf__pgla = fnty.copy(this=ehfkp__guvlc)
            typeinfer.propagate_refined_type(self.func, gecf__pgla)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            hfvw__atvai = target.getone()
            if context.unify_pairs(hfvw__atvai, sig.return_type
                ) == hfvw__atvai:
                sig = sig.replace(return_type=hfvw__atvai)
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
        cwpbd__xgvj = '*other* must be a {} but got a {} instead'
        raise TypeError(cwpbd__xgvj.format(ForceLiteralArg, type(other)))
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
    vwgnp__ksrs = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for aqhp__thwjd, vfkj__qztq in kwargs.items():
        rfegb__bkql = None
        try:
            tkhy__idrgh = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[tkhy__idrgh.name] = [vfkj__qztq]
            rfegb__bkql = get_const_value_inner(func_ir, tkhy__idrgh)
            func_ir._definitions.pop(tkhy__idrgh.name)
            if isinstance(rfegb__bkql, str):
                rfegb__bkql = sigutils._parse_signature_string(rfegb__bkql)
            if isinstance(rfegb__bkql, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {aqhp__thwjd} is annotated as type class {rfegb__bkql}."""
                    )
            assert isinstance(rfegb__bkql, types.Type)
            if isinstance(rfegb__bkql, (types.List, types.Set)):
                rfegb__bkql = rfegb__bkql.copy(reflected=False)
            vwgnp__ksrs[aqhp__thwjd] = rfegb__bkql
        except BodoError as pdyw__kozbj:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(rfegb__bkql, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(vfkj__qztq, ir.Global):
                    msg = f'Global {vfkj__qztq.name!r} is not defined.'
                if isinstance(vfkj__qztq, ir.FreeVar):
                    msg = f'Freevar {vfkj__qztq.name!r} is not defined.'
            if isinstance(vfkj__qztq, ir.Expr) and vfkj__qztq.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=aqhp__thwjd, msg=msg, loc=loc)
    for name, typ in vwgnp__ksrs.items():
        self._legalize_arg_type(name, typ, loc)
    return vwgnp__ksrs


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
    lgt__wwlb = inst.arg
    assert lgt__wwlb > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(lgt__wwlb)]))
    tmps = [state.make_temp() for _ in range(lgt__wwlb - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    gddh__avvfi = ir.Global('format', format, loc=self.loc)
    self.store(value=gddh__avvfi, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    bze__xby = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=bze__xby, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    lgt__wwlb = inst.arg
    assert lgt__wwlb > 0, 'invalid BUILD_STRING count'
    ypkg__spr = self.get(strings[0])
    for other, ply__yqli in zip(strings[1:], tmps):
        other = self.get(other)
        xfqnp__yvexh = ir.Expr.binop(operator.add, lhs=ypkg__spr, rhs=other,
            loc=self.loc)
        self.store(xfqnp__yvexh, ply__yqli)
        ypkg__spr = self.get(ply__yqli)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    spipj__sxq = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, spipj__sxq])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    ucjn__okbr = mk_unique_var(f'{var_name}')
    rivoa__qcpfe = ucjn__okbr.replace('<', '_').replace('>', '_')
    rivoa__qcpfe = rivoa__qcpfe.replace('.', '_').replace('$', '_v')
    return rivoa__qcpfe


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
                riv__vewmx = get_overload_const_str(val2)
                if riv__vewmx != 'ns':
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
        nte__vfy = states['defmap']
        if len(nte__vfy) == 0:
            noplh__dnk = assign.target
            numba.core.ssa._logger.debug('first assign: %s', noplh__dnk)
            if noplh__dnk.name not in scope.localvars:
                noplh__dnk = scope.define(assign.target.name, loc=assign.loc)
        else:
            noplh__dnk = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=noplh__dnk, value=assign.value, loc=
            assign.loc)
        nte__vfy[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    axun__cptfd = []
    for aqhp__thwjd, vfkj__qztq in typing.npydecl.registry.globals:
        if aqhp__thwjd == func:
            axun__cptfd.append(vfkj__qztq)
    for aqhp__thwjd, vfkj__qztq in typing.templates.builtin_registry.globals:
        if aqhp__thwjd == func:
            axun__cptfd.append(vfkj__qztq)
    if len(axun__cptfd) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return axun__cptfd


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    nvtay__cuwt = {}
    hxj__dsl = find_topo_order(blocks)
    uznj__kmmy = {}
    for bmy__ysgj in hxj__dsl:
        block = blocks[bmy__ysgj]
        lua__pet = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                boqr__rfb = stmt.target.name
                flmxz__isup = stmt.value
                if (flmxz__isup.op == 'getattr' and flmxz__isup.attr in
                    arr_math and isinstance(typemap[flmxz__isup.value.name],
                    types.npytypes.Array)):
                    flmxz__isup = stmt.value
                    vsdwx__hir = flmxz__isup.value
                    nvtay__cuwt[boqr__rfb] = vsdwx__hir
                    scope = vsdwx__hir.scope
                    loc = vsdwx__hir.loc
                    crha__tdfde = ir.Var(scope, mk_unique_var('$np_g_var'), loc
                        )
                    typemap[crha__tdfde.name] = types.misc.Module(numpy)
                    etyqj__ogipe = ir.Global('np', numpy, loc)
                    bek__gisv = ir.Assign(etyqj__ogipe, crha__tdfde, loc)
                    flmxz__isup.value = crha__tdfde
                    lua__pet.append(bek__gisv)
                    func_ir._definitions[crha__tdfde.name] = [etyqj__ogipe]
                    func = getattr(numpy, flmxz__isup.attr)
                    brlvd__bbhzr = get_np_ufunc_typ_lst(func)
                    uznj__kmmy[boqr__rfb] = brlvd__bbhzr
                if (flmxz__isup.op == 'call' and flmxz__isup.func.name in
                    nvtay__cuwt):
                    vsdwx__hir = nvtay__cuwt[flmxz__isup.func.name]
                    awkt__qfl = calltypes.pop(flmxz__isup)
                    hgzp__ahtw = awkt__qfl.args[:len(flmxz__isup.args)]
                    kphhi__uhcc = {name: typemap[vfkj__qztq.name] for name,
                        vfkj__qztq in flmxz__isup.kws}
                    ejhy__ekwzn = uznj__kmmy[flmxz__isup.func.name]
                    nxfb__hah = None
                    for gcjpc__cjwba in ejhy__ekwzn:
                        try:
                            nxfb__hah = gcjpc__cjwba.get_call_type(typingctx,
                                [typemap[vsdwx__hir.name]] + list(
                                hgzp__ahtw), kphhi__uhcc)
                            typemap.pop(flmxz__isup.func.name)
                            typemap[flmxz__isup.func.name] = gcjpc__cjwba
                            calltypes[flmxz__isup] = nxfb__hah
                            break
                        except Exception as pdyw__kozbj:
                            pass
                    if nxfb__hah is None:
                        raise TypeError(
                            f'No valid template found for {flmxz__isup.func.name}'
                            )
                    flmxz__isup.args = [vsdwx__hir] + flmxz__isup.args
            lua__pet.append(stmt)
        block.body = lua__pet


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    ttmh__kghev = ufunc.nin
    xrkx__nashk = ufunc.nout
    dagv__izyi = ufunc.nargs
    assert dagv__izyi == ttmh__kghev + xrkx__nashk
    if len(args) < ttmh__kghev:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            ttmh__kghev))
    if len(args) > dagv__izyi:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), dagv__izyi)
            )
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    eja__gofkh = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    tzxm__vko = max(eja__gofkh)
    tzpqr__ivb = args[ttmh__kghev:]
    if not all(d == tzxm__vko for d in eja__gofkh[ttmh__kghev:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(stmy__qumqo, types.ArrayCompatible) and not
        isinstance(stmy__qumqo, types.Bytes) for stmy__qumqo in tzpqr__ivb):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(stmy__qumqo.mutable for stmy__qumqo in tzpqr__ivb):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    qibnf__uwowd = [(x.dtype if isinstance(x, types.ArrayCompatible) and 
        not isinstance(x, types.Bytes) else x) for x in args]
    fev__zjxk = None
    if tzxm__vko > 0 and len(tzpqr__ivb) < ufunc.nout:
        fev__zjxk = 'C'
        ahrzc__bqjok = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in ahrzc__bqjok and 'F' in ahrzc__bqjok:
            fev__zjxk = 'F'
    return qibnf__uwowd, tzpqr__ivb, tzxm__vko, fev__zjxk


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
        gjck__anoua = 'Dict.key_type cannot be of type {}'
        raise TypingError(gjck__anoua.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        gjck__anoua = 'Dict.value_type cannot be of type {}'
        raise TypingError(gjck__anoua.format(valty))
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
    aat__yvp = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[aat__yvp]
        return impl, args
    except KeyError as pdyw__kozbj:
        pass
    impl, args = self._build_impl(aat__yvp, args, kws)
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
        dmn__lfkjj = find_topo_order(parfor.loop_body)
    jgsqj__zjvbj = dmn__lfkjj[0]
    bbga__dgjjc = {}
    _update_parfor_get_setitems(parfor.loop_body[jgsqj__zjvbj].body, parfor
        .index_var, alias_map, bbga__dgjjc, lives_n_aliases)
    bdm__irch = set(bbga__dgjjc.keys())
    for wauoq__pje in dmn__lfkjj:
        if wauoq__pje == jgsqj__zjvbj:
            continue
        for stmt in parfor.loop_body[wauoq__pje].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            gsukz__wrf = set(vfkj__qztq.name for vfkj__qztq in stmt.list_vars()
                )
            yvcm__dsav = gsukz__wrf & bdm__irch
            for a in yvcm__dsav:
                bbga__dgjjc.pop(a, None)
    for wauoq__pje in dmn__lfkjj:
        if wauoq__pje == jgsqj__zjvbj:
            continue
        block = parfor.loop_body[wauoq__pje]
        fgu__nod = bbga__dgjjc.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            fgu__nod, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    ejuon__ilo = max(blocks.keys())
    bgxc__mqus, owi__etphc = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    ibq__fox = ir.Jump(bgxc__mqus, ir.Loc('parfors_dummy', -1))
    blocks[ejuon__ilo].body.append(ibq__fox)
    gyte__qam = compute_cfg_from_blocks(blocks)
    czp__fbc = compute_use_defs(blocks)
    hmhf__nri = compute_live_map(gyte__qam, blocks, czp__fbc.usemap,
        czp__fbc.defmap)
    alias_set = set(alias_map.keys())
    for bmy__ysgj, block in blocks.items():
        lua__pet = []
        dtw__bnw = {vfkj__qztq.name for vfkj__qztq in block.terminator.
            list_vars()}
        for hwfu__jlt, qzwdy__wdx in gyte__qam.successors(bmy__ysgj):
            dtw__bnw |= hmhf__nri[hwfu__jlt]
        for stmt in reversed(block.body):
            ivtaf__hwb = dtw__bnw & alias_set
            for vfkj__qztq in ivtaf__hwb:
                dtw__bnw |= alias_map[vfkj__qztq]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in dtw__bnw and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                lnaah__tin = guard(find_callname, func_ir, stmt.value)
                if lnaah__tin == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in dtw__bnw and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            dtw__bnw |= {vfkj__qztq.name for vfkj__qztq in stmt.list_vars()}
            lua__pet.append(stmt)
        lua__pet.reverse()
        block.body = lua__pet
    typemap.pop(owi__etphc.name)
    blocks[ejuon__ilo].body.pop()

    def trim_empty_parfor_branches(parfor):
        eev__zsmt = False
        blocks = parfor.loop_body.copy()
        for bmy__ysgj, block in blocks.items():
            if len(block.body):
                khbm__qikao = block.body[-1]
                if isinstance(khbm__qikao, ir.Branch):
                    if len(blocks[khbm__qikao.truebr].body) == 1 and len(blocks
                        [khbm__qikao.falsebr].body) == 1:
                        rvev__pboty = blocks[khbm__qikao.truebr].body[0]
                        munu__mmr = blocks[khbm__qikao.falsebr].body[0]
                        if isinstance(rvev__pboty, ir.Jump) and isinstance(
                            munu__mmr, ir.Jump
                            ) and rvev__pboty.target == munu__mmr.target:
                            parfor.loop_body[bmy__ysgj].body[-1] = ir.Jump(
                                rvev__pboty.target, khbm__qikao.loc)
                            eev__zsmt = True
                    elif len(blocks[khbm__qikao.truebr].body) == 1:
                        rvev__pboty = blocks[khbm__qikao.truebr].body[0]
                        if isinstance(rvev__pboty, ir.Jump
                            ) and rvev__pboty.target == khbm__qikao.falsebr:
                            parfor.loop_body[bmy__ysgj].body[-1] = ir.Jump(
                                rvev__pboty.target, khbm__qikao.loc)
                            eev__zsmt = True
                    elif len(blocks[khbm__qikao.falsebr].body) == 1:
                        munu__mmr = blocks[khbm__qikao.falsebr].body[0]
                        if isinstance(munu__mmr, ir.Jump
                            ) and munu__mmr.target == khbm__qikao.truebr:
                            parfor.loop_body[bmy__ysgj].body[-1] = ir.Jump(
                                munu__mmr.target, khbm__qikao.loc)
                            eev__zsmt = True
        return eev__zsmt
    eev__zsmt = True
    while eev__zsmt:
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
        eev__zsmt = trim_empty_parfor_branches(parfor)
    rfi__wuqmj = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        rfi__wuqmj &= len(block.body) == 0
    if rfi__wuqmj:
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
    dpjms__aled = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                dpjms__aled += 1
                parfor = stmt
                xcjgb__xrr = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = xcjgb__xrr.scope
                loc = ir.Loc('parfors_dummy', -1)
                vjp__zzvy = ir.Var(scope, mk_unique_var('$const'), loc)
                xcjgb__xrr.body.append(ir.Assign(ir.Const(0, loc),
                    vjp__zzvy, loc))
                xcjgb__xrr.body.append(ir.Return(vjp__zzvy, loc))
                gyte__qam = compute_cfg_from_blocks(parfor.loop_body)
                for mhsp__mcy in gyte__qam.dead_nodes():
                    del parfor.loop_body[mhsp__mcy]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                xcjgb__xrr = parfor.loop_body[max(parfor.loop_body.keys())]
                xcjgb__xrr.body.pop()
                xcjgb__xrr.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return dpjms__aled


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
            ynci__nrq = self.overloads.get(tuple(args))
            if ynci__nrq is not None:
                return ynci__nrq.entry_point
            self._pre_compile(args, return_type, flags)
            vbggn__yggyp = self.func_ir
            ipno__xtn = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=ipno__xtn):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=vbggn__yggyp, args=
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
        pjuu__hkwz = copy.deepcopy(flags)
        pjuu__hkwz.no_rewrites = True

        def compile_local(the_ir, the_flags):
            dwg__kfty = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return dwg__kfty.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        zgc__tmvh = compile_local(func_ir, pjuu__hkwz)
        ggpzt__wksva = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    ggpzt__wksva = compile_local(func_ir, flags)
                except Exception as pdyw__kozbj:
                    pass
        if ggpzt__wksva is not None:
            cres = ggpzt__wksva
        else:
            cres = zgc__tmvh
        return cres
    else:
        dwg__kfty = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return dwg__kfty.compile_ir(func_ir=func_ir, lifted=lifted,
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
    afeqt__nplg = self.get_data_type(typ.dtype)
    wbulp__hzf = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        wbulp__hzf):
        kime__xnyh = ary.ctypes.data
        gqtlg__ing = self.add_dynamic_addr(builder, kime__xnyh, info=str(
            type(kime__xnyh)))
        auz__gan = self.add_dynamic_addr(builder, id(ary), info=str(type(ary)))
        self.global_arrays.append(ary)
    else:
        phsx__ebqmg = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            phsx__ebqmg = phsx__ebqmg.view('int64')
        val = bytearray(phsx__ebqmg.data)
        jobq__ikb = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        gqtlg__ing = cgutils.global_constant(builder, '.const.array.data',
            jobq__ikb)
        gqtlg__ing.align = self.get_abi_alignment(afeqt__nplg)
        auz__gan = None
    osg__noz = self.get_value_type(types.intp)
    pdx__rax = [self.get_constant(types.intp, lpdw__vtwlk) for lpdw__vtwlk in
        ary.shape]
    korel__ipr = lir.Constant(lir.ArrayType(osg__noz, len(pdx__rax)), pdx__rax)
    rog__wwx = [self.get_constant(types.intp, lpdw__vtwlk) for lpdw__vtwlk in
        ary.strides]
    nvk__bsoto = lir.Constant(lir.ArrayType(osg__noz, len(rog__wwx)), rog__wwx)
    bbvii__jtxch = self.get_constant(types.intp, ary.dtype.itemsize)
    img__ddt = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        img__ddt, bbvii__jtxch, gqtlg__ing.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), korel__ipr, nvk__bsoto])


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
    gyw__rwy = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    wuhlx__tdpz = lir.Function(module, gyw__rwy, name='nrt_atomic_{0}'.
        format(op))
    [ntxuh__wva] = wuhlx__tdpz.args
    cfkd__abf = wuhlx__tdpz.append_basic_block()
    builder = lir.IRBuilder(cfkd__abf)
    oodl__ptm = lir.Constant(_word_type, 1)
    if False:
        owxi__xeq = builder.atomic_rmw(op, ntxuh__wva, oodl__ptm, ordering=
            ordering)
        res = getattr(builder, op)(owxi__xeq, oodl__ptm)
        builder.ret(res)
    else:
        owxi__xeq = builder.load(ntxuh__wva)
        bbbo__bheg = getattr(builder, op)(owxi__xeq, oodl__ptm)
        dhpo__goa = builder.icmp_signed('!=', owxi__xeq, lir.Constant(
            owxi__xeq.type, -1))
        with cgutils.if_likely(builder, dhpo__goa):
            builder.store(bbbo__bheg, ntxuh__wva)
        builder.ret(bbbo__bheg)
    return wuhlx__tdpz


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
        cffp__gbd = state.targetctx.codegen()
        state.library = cffp__gbd.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    qod__ztewi = state.func_ir
    typemap = state.typemap
    jeixi__tde = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    bmhan__iwnsn = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            qod__ztewi, typemap, jeixi__tde, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            nky__fqj = lowering.Lower(targetctx, library, fndesc,
                qod__ztewi, metadata=metadata)
            nky__fqj.lower()
            if not flags.no_cpython_wrapper:
                nky__fqj.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(jeixi__tde, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        nky__fqj.create_cfunc_wrapper()
            env = nky__fqj.env
            oozge__vck = nky__fqj.call_helper
            del nky__fqj
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, oozge__vck, cfunc=None, env=env)
        else:
            ania__qux = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(ania__qux, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, oozge__vck, cfunc=ania__qux,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        lbprz__ldj = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = lbprz__ldj - bmhan__iwnsn
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
        psw__jcpbv = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, psw__jcpbv),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            eusno__bef.do_break()
        vpw__fhmiv = c.builder.icmp_signed('!=', psw__jcpbv, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(vpw__fhmiv, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, psw__jcpbv)
                c.pyapi.decref(psw__jcpbv)
                eusno__bef.do_break()
        c.pyapi.decref(psw__jcpbv)
    uzv__nwra, list = listobj.ListInstance.allocate_ex(c.context, c.builder,
        typ, size)
    with c.builder.if_else(uzv__nwra, likely=True) as (dzx__oare, haj__vjjli):
        with dzx__oare:
            list.size = size
            fjfsx__xnmvn = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                fjfsx__xnmvn), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        fjfsx__xnmvn))
                    with cgutils.for_range(c.builder, size) as eusno__bef:
                        itemobj = c.pyapi.list_getitem(obj, eusno__bef.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        lnqbc__fmip = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(lnqbc__fmip.is_error, likely
                            =False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            eusno__bef.do_break()
                        list.setitem(eusno__bef.index, lnqbc__fmip.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with haj__vjjli:
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
    hzj__yft, rvqjm__gakjw, hlr__pkav, impi__smmsr, ajpvw__cmmr = (
        compile_time_get_string_data(literal_string))
    egknu__yhg = builder.module
    gv = context.insert_const_bytes(egknu__yhg, hzj__yft)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        rvqjm__gakjw), context.get_constant(types.int32, hlr__pkav),
        context.get_constant(types.uint32, impi__smmsr), context.
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
    ujwgu__khtw = None
    if isinstance(shape, types.Integer):
        ujwgu__khtw = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(lpdw__vtwlk, (types.Integer, types.IntEnumMember)
            ) for lpdw__vtwlk in shape):
            ujwgu__khtw = len(shape)
    return ujwgu__khtw


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
            ujwgu__khtw = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if ujwgu__khtw == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(
                    ujwgu__khtw))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            nlc__def = self._get_names(x)
            if len(nlc__def) != 0:
                return nlc__def[0]
            return nlc__def
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    nlc__def = self._get_names(obj)
    if len(nlc__def) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(nlc__def[0])


def get_equiv_set(self, obj):
    nlc__def = self._get_names(obj)
    if len(nlc__def) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(nlc__def[0])


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
    pksq__ztvn = []
    for jsqrw__uyc in func_ir.arg_names:
        if jsqrw__uyc in typemap and isinstance(typemap[jsqrw__uyc], types.
            containers.UniTuple) and typemap[jsqrw__uyc].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(jsqrw__uyc))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for oyn__eft in func_ir.blocks.values():
        for stmt in oyn__eft.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    sdht__hihvf = getattr(val, 'code', None)
                    if sdht__hihvf is not None:
                        if getattr(val, 'closure', None) is not None:
                            noq__awsat = '<creating a function from a closure>'
                            xfqnp__yvexh = ''
                        else:
                            noq__awsat = sdht__hihvf.co_name
                            xfqnp__yvexh = '(%s) ' % noq__awsat
                    else:
                        noq__awsat = '<could not ascertain use case>'
                        xfqnp__yvexh = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (noq__awsat, xfqnp__yvexh))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                haumu__jij = False
                if isinstance(val, pytypes.FunctionType):
                    haumu__jij = val in {numba.gdb, numba.gdb_init}
                if not haumu__jij:
                    haumu__jij = getattr(val, '_name', '') == 'gdb_internal'
                if haumu__jij:
                    pksq__ztvn.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    dcf__sqs = func_ir.get_definition(var)
                    imq__fypf = guard(find_callname, func_ir, dcf__sqs)
                    if imq__fypf and imq__fypf[1] == 'numpy':
                        ty = getattr(numpy, imq__fypf[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    tre__hungm = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(tre__hungm), loc=stmt.loc)
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
    if len(pksq__ztvn) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        wyzwd__mfpe = '\n'.join([x.strformat() for x in pksq__ztvn])
        raise errors.UnsupportedError(msg % wyzwd__mfpe)


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
    aqhp__thwjd, vfkj__qztq = next(iter(val.items()))
    nbvu__daqvf = typeof_impl(aqhp__thwjd, c)
    egef__dim = typeof_impl(vfkj__qztq, c)
    if nbvu__daqvf is None or egef__dim is None:
        raise ValueError(
            f'Cannot type dict element type {type(aqhp__thwjd)}, {type(vfkj__qztq)}'
            )
    return types.DictType(nbvu__daqvf, egef__dim)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    cktwx__tvsxd = cgutils.alloca_once_value(c.builder, val)
    vkxz__fou = c.pyapi.object_hasattr_string(val, '_opaque')
    nngbs__gtx = c.builder.icmp_unsigned('==', vkxz__fou, lir.Constant(
        vkxz__fou.type, 0))
    sjt__xqssa = typ.key_type
    urjg__nveju = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(sjt__xqssa, urjg__nveju)

    def copy_dict(out_dict, in_dict):
        for aqhp__thwjd, vfkj__qztq in in_dict.items():
            out_dict[aqhp__thwjd] = vfkj__qztq
    with c.builder.if_then(nngbs__gtx):
        qtx__vrew = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        isj__tcew = c.pyapi.call_function_objargs(qtx__vrew, [])
        eabn__mbiw = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(eabn__mbiw, [isj__tcew, val])
        c.builder.store(isj__tcew, cktwx__tvsxd)
    val = c.builder.load(cktwx__tvsxd)
    obfl__hnpnk = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    jmkfr__tueo = c.pyapi.object_type(val)
    ohoiv__pltu = c.builder.icmp_unsigned('==', jmkfr__tueo, obfl__hnpnk)
    with c.builder.if_else(ohoiv__pltu) as (wkn__swb, hvcwp__gnua):
        with wkn__swb:
            jvvy__dtozm = c.pyapi.object_getattr_string(val, '_opaque')
            iqzw__vword = types.MemInfoPointer(types.voidptr)
            lnqbc__fmip = c.unbox(iqzw__vword, jvvy__dtozm)
            mi = lnqbc__fmip.value
            utqnq__wlkzg = iqzw__vword, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *utqnq__wlkzg)
            odg__lhu = context.get_constant_null(utqnq__wlkzg[1])
            args = mi, odg__lhu
            mzqb__zql, ikdr__kcjfe = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, ikdr__kcjfe)
            c.pyapi.decref(jvvy__dtozm)
            axgxf__uqihn = c.builder.basic_block
        with hvcwp__gnua:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", jmkfr__tueo, obfl__hnpnk)
            phptm__kjgv = c.builder.basic_block
    mqwj__wka = c.builder.phi(ikdr__kcjfe.type)
    xxb__vhx = c.builder.phi(mzqb__zql.type)
    mqwj__wka.add_incoming(ikdr__kcjfe, axgxf__uqihn)
    mqwj__wka.add_incoming(ikdr__kcjfe.type(None), phptm__kjgv)
    xxb__vhx.add_incoming(mzqb__zql, axgxf__uqihn)
    xxb__vhx.add_incoming(cgutils.true_bit, phptm__kjgv)
    c.pyapi.decref(obfl__hnpnk)
    c.pyapi.decref(jmkfr__tueo)
    with c.builder.if_then(nngbs__gtx):
        c.pyapi.decref(val)
    return NativeValue(mqwj__wka, is_error=xxb__vhx)


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
    miu__etys = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=miu__etys, name=updatevar)
    vazzw__vhae = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=vazzw__vhae, name=res)


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
        for aqhp__thwjd, vfkj__qztq in other.items():
            d[aqhp__thwjd] = vfkj__qztq
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
    xfqnp__yvexh = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(xfqnp__yvexh, res)


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
    qdgwg__ycrtm = PassManager(name)
    if state.func_ir is None:
        qdgwg__ycrtm.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            qdgwg__ycrtm.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        qdgwg__ycrtm.add_pass(FixupArgs, 'fix up args')
    qdgwg__ycrtm.add_pass(IRProcessing, 'processing IR')
    qdgwg__ycrtm.add_pass(WithLifting, 'Handle with contexts')
    qdgwg__ycrtm.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        qdgwg__ycrtm.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        qdgwg__ycrtm.add_pass(DeadBranchPrune, 'dead branch pruning')
        qdgwg__ycrtm.add_pass(GenericRewrites, 'nopython rewrites')
    qdgwg__ycrtm.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    qdgwg__ycrtm.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        qdgwg__ycrtm.add_pass(DeadBranchPrune, 'dead branch pruning')
    qdgwg__ycrtm.add_pass(FindLiterallyCalls, 'find literally calls')
    qdgwg__ycrtm.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        qdgwg__ycrtm.add_pass(ReconstructSSA, 'ssa')
    qdgwg__ycrtm.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    qdgwg__ycrtm.finalize()
    return qdgwg__ycrtm


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
    a, mayz__qxvnz = args
    if isinstance(a, types.List) and isinstance(mayz__qxvnz, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(mayz__qxvnz, types.List):
        return signature(mayz__qxvnz, types.intp, mayz__qxvnz)


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
        soa__yurm, pjbu__saf = 0, 1
    else:
        soa__yurm, pjbu__saf = 1, 0
    kstm__sscj = ListInstance(context, builder, sig.args[soa__yurm], args[
        soa__yurm])
    eltoa__bnd = kstm__sscj.size
    shssp__ylvxf = args[pjbu__saf]
    fjfsx__xnmvn = lir.Constant(shssp__ylvxf.type, 0)
    shssp__ylvxf = builder.select(cgutils.is_neg_int(builder, shssp__ylvxf),
        fjfsx__xnmvn, shssp__ylvxf)
    img__ddt = builder.mul(shssp__ylvxf, eltoa__bnd)
    gggi__ecyg = ListInstance.allocate(context, builder, sig.return_type,
        img__ddt)
    gggi__ecyg.size = img__ddt
    with cgutils.for_range_slice(builder, fjfsx__xnmvn, img__ddt,
        eltoa__bnd, inc=True) as (qmnu__isa, _):
        with cgutils.for_range(builder, eltoa__bnd) as eusno__bef:
            value = kstm__sscj.getitem(eusno__bef.index)
            gggi__ecyg.setitem(builder.add(eusno__bef.index, qmnu__isa),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, gggi__ecyg.value
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
    tsw__pwwi = first.unify(self, second)
    if tsw__pwwi is not None:
        return tsw__pwwi
    tsw__pwwi = second.unify(self, first)
    if tsw__pwwi is not None:
        return tsw__pwwi
    jvtma__jbq = self.can_convert(fromty=first, toty=second)
    if jvtma__jbq is not None and jvtma__jbq <= Conversion.safe:
        return second
    jvtma__jbq = self.can_convert(fromty=second, toty=first)
    if jvtma__jbq is not None and jvtma__jbq <= Conversion.safe:
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
    img__ddt = payload.used
    listobj = c.pyapi.list_new(img__ddt)
    uzv__nwra = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(uzv__nwra, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(img__ddt.
            type, 0))
        with payload._iterate() as eusno__bef:
            i = c.builder.load(index)
            item = eusno__bef.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return uzv__nwra, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    ngrh__rir = h.type
    yfn__kmzv = self.mask
    dtype = self._ty.dtype
    irx__mdwg = context.typing_context
    fnty = irx__mdwg.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(irx__mdwg, (dtype, dtype), {})
    ezk__wgy = context.get_function(fnty, sig)
    blovi__cdzi = ir.Constant(ngrh__rir, 1)
    aqr__mrtut = ir.Constant(ngrh__rir, 5)
    pznjw__dws = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, yfn__kmzv))
    if for_insert:
        cmccu__lub = yfn__kmzv.type(-1)
        mblb__qxt = cgutils.alloca_once_value(builder, cmccu__lub)
    xysdu__pihm = builder.append_basic_block('lookup.body')
    vqeqv__fwnta = builder.append_basic_block('lookup.found')
    zjb__zpv = builder.append_basic_block('lookup.not_found')
    mbk__fhkih = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        byff__vwt = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, byff__vwt)):
            qog__aueyu = ezk__wgy(builder, (item, entry.key))
            with builder.if_then(qog__aueyu):
                builder.branch(vqeqv__fwnta)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, byff__vwt)):
            builder.branch(zjb__zpv)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, byff__vwt)):
                ewk__ddxa = builder.load(mblb__qxt)
                ewk__ddxa = builder.select(builder.icmp_unsigned('==',
                    ewk__ddxa, cmccu__lub), i, ewk__ddxa)
                builder.store(ewk__ddxa, mblb__qxt)
    with cgutils.for_range(builder, ir.Constant(ngrh__rir, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, blovi__cdzi)
        i = builder.and_(i, yfn__kmzv)
        builder.store(i, index)
    builder.branch(xysdu__pihm)
    with builder.goto_block(xysdu__pihm):
        i = builder.load(index)
        check_entry(i)
        ugvi__itff = builder.load(pznjw__dws)
        ugvi__itff = builder.lshr(ugvi__itff, aqr__mrtut)
        i = builder.add(blovi__cdzi, builder.mul(i, aqr__mrtut))
        i = builder.and_(yfn__kmzv, builder.add(i, ugvi__itff))
        builder.store(i, index)
        builder.store(ugvi__itff, pznjw__dws)
        builder.branch(xysdu__pihm)
    with builder.goto_block(zjb__zpv):
        if for_insert:
            i = builder.load(index)
            ewk__ddxa = builder.load(mblb__qxt)
            i = builder.select(builder.icmp_unsigned('==', ewk__ddxa,
                cmccu__lub), i, ewk__ddxa)
            builder.store(i, index)
        builder.branch(mbk__fhkih)
    with builder.goto_block(vqeqv__fwnta):
        builder.branch(mbk__fhkih)
    builder.position_at_end(mbk__fhkih)
    haumu__jij = builder.phi(ir.IntType(1), 'found')
    haumu__jij.add_incoming(cgutils.true_bit, vqeqv__fwnta)
    haumu__jij.add_incoming(cgutils.false_bit, zjb__zpv)
    return haumu__jij, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    agq__pah = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    jesj__xgl = payload.used
    blovi__cdzi = ir.Constant(jesj__xgl.type, 1)
    jesj__xgl = payload.used = builder.add(jesj__xgl, blovi__cdzi)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, agq__pah), likely=True):
        payload.fill = builder.add(payload.fill, blovi__cdzi)
    if do_resize:
        self.upsize(jesj__xgl)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    haumu__jij, i = payload._lookup(item, h, for_insert=True)
    kiv__fyrfg = builder.not_(haumu__jij)
    with builder.if_then(kiv__fyrfg):
        entry = payload.get_entry(i)
        agq__pah = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        jesj__xgl = payload.used
        blovi__cdzi = ir.Constant(jesj__xgl.type, 1)
        jesj__xgl = payload.used = builder.add(jesj__xgl, blovi__cdzi)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, agq__pah), likely=True):
            payload.fill = builder.add(payload.fill, blovi__cdzi)
        if do_resize:
            self.upsize(jesj__xgl)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    jesj__xgl = payload.used
    blovi__cdzi = ir.Constant(jesj__xgl.type, 1)
    jesj__xgl = payload.used = self._builder.sub(jesj__xgl, blovi__cdzi)
    if do_resize:
        self.downsize(jesj__xgl)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    gwzac__iqqm = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, gwzac__iqqm)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    mvvwh__vyvk = payload
    uzv__nwra = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(uzv__nwra), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with mvvwh__vyvk._iterate() as eusno__bef:
        entry = eusno__bef.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(mvvwh__vyvk.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as eusno__bef:
        entry = eusno__bef.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    uzv__nwra = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(uzv__nwra), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    uzv__nwra = cgutils.alloca_once_value(builder, cgutils.true_bit)
    ngrh__rir = context.get_value_type(types.intp)
    fjfsx__xnmvn = ir.Constant(ngrh__rir, 0)
    blovi__cdzi = ir.Constant(ngrh__rir, 1)
    khrxo__vicqm = context.get_data_type(types.SetPayload(self._ty))
    zwwt__lcszt = context.get_abi_sizeof(khrxo__vicqm)
    zhaqw__vieky = self._entrysize
    zwwt__lcszt -= zhaqw__vieky
    ipy__issv, qay__zyol = cgutils.muladd_with_overflow(builder, nentries,
        ir.Constant(ngrh__rir, zhaqw__vieky), ir.Constant(ngrh__rir,
        zwwt__lcszt))
    with builder.if_then(qay__zyol, likely=False):
        builder.store(cgutils.false_bit, uzv__nwra)
    with builder.if_then(builder.load(uzv__nwra), likely=True):
        if realloc:
            olmb__uzex = self._set.meminfo
            ntxuh__wva = context.nrt.meminfo_varsize_alloc(builder,
                olmb__uzex, size=ipy__issv)
            txb__cjzjt = cgutils.is_null(builder, ntxuh__wva)
        else:
            kcrw__ife = _imp_dtor(context, builder.module, self._ty)
            olmb__uzex = context.nrt.meminfo_new_varsize_dtor(builder,
                ipy__issv, builder.bitcast(kcrw__ife, cgutils.voidptr_t))
            txb__cjzjt = cgutils.is_null(builder, olmb__uzex)
        with builder.if_else(txb__cjzjt, likely=False) as (byr__nxt, dzx__oare
            ):
            with byr__nxt:
                builder.store(cgutils.false_bit, uzv__nwra)
            with dzx__oare:
                if not realloc:
                    self._set.meminfo = olmb__uzex
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, ipy__issv, 255)
                payload.used = fjfsx__xnmvn
                payload.fill = fjfsx__xnmvn
                payload.finger = fjfsx__xnmvn
                zfg__cjsn = builder.sub(nentries, blovi__cdzi)
                payload.mask = zfg__cjsn
    return builder.load(uzv__nwra)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    uzv__nwra = cgutils.alloca_once_value(builder, cgutils.true_bit)
    ngrh__rir = context.get_value_type(types.intp)
    fjfsx__xnmvn = ir.Constant(ngrh__rir, 0)
    blovi__cdzi = ir.Constant(ngrh__rir, 1)
    khrxo__vicqm = context.get_data_type(types.SetPayload(self._ty))
    zwwt__lcszt = context.get_abi_sizeof(khrxo__vicqm)
    zhaqw__vieky = self._entrysize
    zwwt__lcszt -= zhaqw__vieky
    yfn__kmzv = src_payload.mask
    nentries = builder.add(blovi__cdzi, yfn__kmzv)
    ipy__issv = builder.add(ir.Constant(ngrh__rir, zwwt__lcszt), builder.
        mul(ir.Constant(ngrh__rir, zhaqw__vieky), nentries))
    with builder.if_then(builder.load(uzv__nwra), likely=True):
        kcrw__ife = _imp_dtor(context, builder.module, self._ty)
        olmb__uzex = context.nrt.meminfo_new_varsize_dtor(builder,
            ipy__issv, builder.bitcast(kcrw__ife, cgutils.voidptr_t))
        txb__cjzjt = cgutils.is_null(builder, olmb__uzex)
        with builder.if_else(txb__cjzjt, likely=False) as (byr__nxt, dzx__oare
            ):
            with byr__nxt:
                builder.store(cgutils.false_bit, uzv__nwra)
            with dzx__oare:
                self._set.meminfo = olmb__uzex
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = fjfsx__xnmvn
                payload.mask = yfn__kmzv
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, zhaqw__vieky)
                with src_payload._iterate() as eusno__bef:
                    context.nrt.incref(builder, self._ty.dtype, eusno__bef.
                        entry.key)
    return builder.load(uzv__nwra)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    xcw__fmmey = context.get_value_type(types.voidptr)
    aygzh__kal = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [xcw__fmmey, aygzh__kal, xcw__fmmey])
    dpheh__rasxt = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=dpheh__rasxt)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        ppsro__elt = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer()
            )
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, ppsro__elt)
        with payload._iterate() as eusno__bef:
            entry = eusno__bef.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    yjy__sirvo, = sig.args
    phn__hom, = args
    lpn__vlul = numba.core.imputils.call_len(context, builder, yjy__sirvo,
        phn__hom)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, lpn__vlul)
    with numba.core.imputils.for_iter(context, builder, yjy__sirvo, phn__hom
        ) as eusno__bef:
        inst.add(eusno__bef.value)
        context.nrt.decref(builder, set_type.dtype, eusno__bef.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    yjy__sirvo = sig.args[1]
    phn__hom = args[1]
    lpn__vlul = numba.core.imputils.call_len(context, builder, yjy__sirvo,
        phn__hom)
    if lpn__vlul is not None:
        jxwb__evasy = builder.add(inst.payload.used, lpn__vlul)
        inst.upsize(jxwb__evasy)
    with numba.core.imputils.for_iter(context, builder, yjy__sirvo, phn__hom
        ) as eusno__bef:
        usziu__jjb = context.cast(builder, eusno__bef.value, yjy__sirvo.
            dtype, inst.dtype)
        inst.add(usziu__jjb)
        context.nrt.decref(builder, yjy__sirvo.dtype, eusno__bef.value)
    if lpn__vlul is not None:
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
    xspq__nhxa = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, xspq__nhxa, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    ania__qux = target_context.get_executable(library, fndesc, env)
    pbmr__pdd = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=ania__qux, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return pbmr__pdd


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
