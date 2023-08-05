"""
transforms the IR to handle bytecode issues in Python 3.10. This
should be removed once https://github.com/numba/numba/pull/7866
is included in Numba 0.56
"""
import operator
import numba
from numba.core import ir
from numba.core.compiler_machinery import FunctionPass, register_pass
from numba.core.errors import UnsupportedError
from numba.core.ir_utils import dprint_func_ir, get_definition, guard


@register_pass(mutates_CFG=False, analysis_only=False)
class Bodo310ByteCodePass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        dprint_func_ir(state.func_ir,
            'starting Bodo 3.10 Bytecode optimizations pass')
        peep_hole_call_function_ex_to_call_function_kw(state.func_ir)
        peep_hole_fuse_dict_add_updates(state.func_ir)
        return True


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    blhb__zoljc = keyword_expr.items.copy()
    cnv__cmz = keyword_expr.value_indexes
    for gpp__bpqdu, oixv__zsv in cnv__cmz.items():
        blhb__zoljc[oixv__zsv] = gpp__bpqdu, blhb__zoljc[oixv__zsv][1]
    new_body[buildmap_idx] = None
    return blhb__zoljc


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    czhgf__uhhee = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    blhb__zoljc = []
    mwx__zwlt = buildmap_idx + 1
    while mwx__zwlt <= search_end:
        qul__gwdn = body[mwx__zwlt]
        if not (isinstance(qul__gwdn, ir.Assign) and isinstance(qul__gwdn.
            value, ir.Const)):
            raise UnsupportedError(czhgf__uhhee)
        snet__rxq = qul__gwdn.target.name
        rlcf__tlqk = qul__gwdn.value.value
        mwx__zwlt += 1
        ctn__jzrc = True
        while mwx__zwlt <= search_end and ctn__jzrc:
            uzoum__rtekd = body[mwx__zwlt]
            if (isinstance(uzoum__rtekd, ir.Assign) and isinstance(
                uzoum__rtekd.value, ir.Expr) and uzoum__rtekd.value.op ==
                'getattr' and uzoum__rtekd.value.value.name ==
                buildmap_name and uzoum__rtekd.value.attr == '__setitem__'):
                ctn__jzrc = False
            else:
                mwx__zwlt += 1
        if ctn__jzrc or mwx__zwlt == search_end:
            raise UnsupportedError(czhgf__uhhee)
        sfaq__wqvw = body[mwx__zwlt + 1]
        if not (isinstance(sfaq__wqvw, ir.Assign) and isinstance(sfaq__wqvw
            .value, ir.Expr) and sfaq__wqvw.value.op == 'call' and 
            sfaq__wqvw.value.func.name == uzoum__rtekd.target.name and len(
            sfaq__wqvw.value.args) == 2 and sfaq__wqvw.value.args[0].name ==
            snet__rxq):
            raise UnsupportedError(czhgf__uhhee)
        qtkg__neryq = sfaq__wqvw.value.args[1]
        blhb__zoljc.append((rlcf__tlqk, qtkg__neryq))
        new_body[mwx__zwlt] = None
        new_body[mwx__zwlt + 1] = None
        mwx__zwlt += 2
    return blhb__zoljc


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    czhgf__uhhee = 'CALL_FUNCTION_EX with **kwargs not supported'
    mwx__zwlt = 0
    qbo__uvwgw = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        wjr__fhq = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        wjr__fhq = vararg_stmt.target.name
    dhfdl__bfy = True
    while search_end >= mwx__zwlt and dhfdl__bfy:
        ljnrx__eijk = body[search_end]
        if (isinstance(ljnrx__eijk, ir.Assign) and ljnrx__eijk.target.name ==
            wjr__fhq and isinstance(ljnrx__eijk.value, ir.Expr) and 
            ljnrx__eijk.value.op == 'build_tuple' and not ljnrx__eijk.value
            .items):
            dhfdl__bfy = False
            new_body[search_end] = None
        else:
            if search_end == mwx__zwlt or not (isinstance(ljnrx__eijk, ir.
                Assign) and ljnrx__eijk.target.name == wjr__fhq and
                isinstance(ljnrx__eijk.value, ir.Expr) and ljnrx__eijk.
                value.op == 'binop' and ljnrx__eijk.value.fn == operator.add):
                raise UnsupportedError(czhgf__uhhee)
            glhmj__sawgh = ljnrx__eijk.value.lhs.name
            slnb__uim = ljnrx__eijk.value.rhs.name
            loy__uaxco = body[search_end - 1]
            if not (isinstance(loy__uaxco, ir.Assign) and isinstance(
                loy__uaxco.value, ir.Expr) and loy__uaxco.value.op ==
                'build_tuple' and len(loy__uaxco.value.items) == 1):
                raise UnsupportedError(czhgf__uhhee)
            if loy__uaxco.target.name == glhmj__sawgh:
                wjr__fhq = slnb__uim
            elif loy__uaxco.target.name == slnb__uim:
                wjr__fhq = glhmj__sawgh
            else:
                raise UnsupportedError(czhgf__uhhee)
            qbo__uvwgw.append(loy__uaxco.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            afm__ohart = True
            while search_end >= mwx__zwlt and afm__ohart:
                tgta__euhoz = body[search_end]
                if isinstance(tgta__euhoz, ir.Assign
                    ) and tgta__euhoz.target.name == wjr__fhq:
                    afm__ohart = False
                else:
                    search_end -= 1
    if dhfdl__bfy:
        raise UnsupportedError(czhgf__uhhee)
    return qbo__uvwgw[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    czhgf__uhhee = 'CALL_FUNCTION_EX with **kwargs not supported'
    for aza__eir in func_ir.blocks.values():
        qppmf__qmnuu = False
        new_body = []
        for unh__qyj, qogc__rwf in enumerate(aza__eir.body):
            if (isinstance(qogc__rwf, ir.Assign) and isinstance(qogc__rwf.
                value, ir.Expr) and qogc__rwf.value.op == 'call' and 
                qogc__rwf.value.varkwarg is not None):
                qppmf__qmnuu = True
                dwlto__juius = qogc__rwf.value
                args = dwlto__juius.args
                blhb__zoljc = dwlto__juius.kws
                tozq__kuepc = dwlto__juius.vararg
                zqg__xme = dwlto__juius.varkwarg
                bbm__gsmi = unh__qyj - 1
                ttlcj__lwzch = bbm__gsmi
                faq__uop = None
                vflm__svrph = True
                while ttlcj__lwzch >= 0 and vflm__svrph:
                    faq__uop = aza__eir.body[ttlcj__lwzch]
                    if isinstance(faq__uop, ir.Assign
                        ) and faq__uop.target.name == zqg__xme.name:
                        vflm__svrph = False
                    else:
                        ttlcj__lwzch -= 1
                if blhb__zoljc or vflm__svrph or not (isinstance(faq__uop.
                    value, ir.Expr) and faq__uop.value.op == 'build_map'):
                    raise UnsupportedError(czhgf__uhhee)
                if faq__uop.value.items:
                    blhb__zoljc = _call_function_ex_replace_kws_small(faq__uop
                        .value, new_body, ttlcj__lwzch)
                else:
                    blhb__zoljc = _call_function_ex_replace_kws_large(aza__eir
                        .body, zqg__xme.name, ttlcj__lwzch, unh__qyj - 1,
                        new_body)
                bbm__gsmi = ttlcj__lwzch
                if tozq__kuepc is not None:
                    if args:
                        raise UnsupportedError(czhgf__uhhee)
                    bse__asb = bbm__gsmi
                    ldltm__emkuz = None
                    vflm__svrph = True
                    while bse__asb >= 0 and vflm__svrph:
                        ldltm__emkuz = aza__eir.body[bse__asb]
                        if isinstance(ldltm__emkuz, ir.Assign
                            ) and ldltm__emkuz.target.name == tozq__kuepc.name:
                            vflm__svrph = False
                        else:
                            bse__asb -= 1
                    if vflm__svrph:
                        raise UnsupportedError(czhgf__uhhee)
                    if isinstance(ldltm__emkuz.value, ir.Expr
                        ) and ldltm__emkuz.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(
                            ldltm__emkuz.value, new_body, bse__asb)
                    else:
                        args = _call_function_ex_replace_args_large(
                            ldltm__emkuz, aza__eir.body, new_body, bse__asb)
                xrn__ldv = ir.Expr.call(dwlto__juius.func, args,
                    blhb__zoljc, dwlto__juius.loc, target=dwlto__juius.target)
                if qogc__rwf.target.name in func_ir._definitions and len(
                    func_ir._definitions[qogc__rwf.target.name]) == 1:
                    func_ir._definitions[qogc__rwf.target.name].clear()
                func_ir._definitions[qogc__rwf.target.name].append(xrn__ldv)
                qogc__rwf = ir.Assign(xrn__ldv, qogc__rwf.target, qogc__rwf.loc
                    )
            new_body.append(qogc__rwf)
        if qppmf__qmnuu:
            aza__eir.body = [saauk__bix for saauk__bix in new_body if 
                saauk__bix is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for aza__eir in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        qppmf__qmnuu = False
        for unh__qyj, qogc__rwf in enumerate(aza__eir.body):
            ffb__onqq = True
            erub__sziza = None
            if isinstance(qogc__rwf, ir.Assign) and isinstance(qogc__rwf.
                value, ir.Expr):
                if qogc__rwf.value.op == 'build_map':
                    erub__sziza = qogc__rwf.target.name
                    lit_old_idx[qogc__rwf.target.name] = unh__qyj
                    lit_new_idx[qogc__rwf.target.name] = unh__qyj
                    map_updates[qogc__rwf.target.name
                        ] = qogc__rwf.value.items.copy()
                    ffb__onqq = False
                elif qogc__rwf.value.op == 'call' and unh__qyj > 0:
                    mxezv__pjfus = qogc__rwf.value.func.name
                    uzoum__rtekd = aza__eir.body[unh__qyj - 1]
                    args = qogc__rwf.value.args
                    if (isinstance(uzoum__rtekd, ir.Assign) and 
                        uzoum__rtekd.target.name == mxezv__pjfus and
                        isinstance(uzoum__rtekd.value, ir.Expr) and 
                        uzoum__rtekd.value.op == 'getattr' and uzoum__rtekd
                        .value.value.name in lit_old_idx):
                        tze__kwzhb = uzoum__rtekd.value.value.name
                        inig__wetzs = uzoum__rtekd.value.attr
                        if inig__wetzs == '__setitem__':
                            ffb__onqq = False
                            map_updates[tze__kwzhb].append(args)
                            new_body[-1] = None
                        elif inig__wetzs == 'update' and args[0
                            ].name in lit_old_idx:
                            ffb__onqq = False
                            map_updates[tze__kwzhb].extend(map_updates[args
                                [0].name])
                            new_body[-1] = None
                        if not ffb__onqq:
                            lit_new_idx[tze__kwzhb] = unh__qyj
                            func_ir._definitions[uzoum__rtekd.target.name
                                ].remove(uzoum__rtekd.value)
            if not (isinstance(qogc__rwf, ir.Assign) and isinstance(
                qogc__rwf.value, ir.Expr) and qogc__rwf.value.op ==
                'getattr' and qogc__rwf.value.value.name in lit_old_idx and
                qogc__rwf.value.attr in ('__setitem__', 'update')):
                for vxltt__ztmbu in qogc__rwf.list_vars():
                    if (vxltt__ztmbu.name in lit_old_idx and vxltt__ztmbu.
                        name != erub__sziza):
                        _insert_build_map(func_ir, vxltt__ztmbu.name,
                            aza__eir.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if ffb__onqq:
                new_body.append(qogc__rwf)
            else:
                func_ir._definitions[qogc__rwf.target.name].remove(qogc__rwf
                    .value)
                qppmf__qmnuu = True
                new_body.append(None)
        ztzcn__xqiwd = list(lit_old_idx.keys())
        for ltpvq__rujm in ztzcn__xqiwd:
            _insert_build_map(func_ir, ltpvq__rujm, aza__eir.body, new_body,
                lit_old_idx, lit_new_idx, map_updates)
        if qppmf__qmnuu:
            aza__eir.body = [saauk__bix for saauk__bix in new_body if 
                saauk__bix is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    clcci__hnbu = lit_old_idx[name]
    nrq__hxvbv = lit_new_idx[name]
    cgil__qlncj = map_updates[name]
    new_body[nrq__hxvbv] = _build_new_build_map(func_ir, name, old_body,
        clcci__hnbu, cgil__qlncj)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    greko__tmuhl = old_body[old_lineno]
    hllo__akbt = greko__tmuhl.target
    qzhu__wjsf = greko__tmuhl.value
    qivi__rmthe = []
    yqpxz__njz = []
    for gkyl__klvyh in new_items:
        pcl__scbn, duc__tjb = gkyl__klvyh
        aks__sqmio = guard(get_definition, func_ir, pcl__scbn)
        if isinstance(aks__sqmio, (ir.Const, ir.Global, ir.FreeVar)):
            qivi__rmthe.append(aks__sqmio.value)
        pcbla__jdqj = guard(get_definition, func_ir, duc__tjb)
        if isinstance(pcbla__jdqj, (ir.Const, ir.Global, ir.FreeVar)):
            yqpxz__njz.append(pcbla__jdqj.value)
        else:
            yqpxz__njz.append(numba.core.interpreter._UNKNOWN_VALUE(
                duc__tjb.name))
    cnv__cmz = {}
    if len(qivi__rmthe) == len(new_items):
        wfq__ejs = {saauk__bix: zvi__gygys for saauk__bix, zvi__gygys in
            zip(qivi__rmthe, yqpxz__njz)}
        for unh__qyj, pcl__scbn in enumerate(qivi__rmthe):
            cnv__cmz[pcl__scbn] = unh__qyj
    else:
        wfq__ejs = None
    khcz__tvt = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=wfq__ejs, value_indexes=cnv__cmz, loc=qzhu__wjsf.loc)
    func_ir._definitions[name].append(khcz__tvt)
    return ir.Assign(khcz__tvt, ir.Var(hllo__akbt.scope, name, hllo__akbt.
        loc), khcz__tvt.loc)
