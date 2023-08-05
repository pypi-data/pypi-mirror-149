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
    iqs__lol = keyword_expr.items.copy()
    oxz__znk = keyword_expr.value_indexes
    for zvy__jqasv, tyf__lsez in oxz__znk.items():
        iqs__lol[tyf__lsez] = zvy__jqasv, iqs__lol[tyf__lsez][1]
    new_body[buildmap_idx] = None
    return iqs__lol


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    suehu__dxa = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    iqs__lol = []
    akc__nvqss = buildmap_idx + 1
    while akc__nvqss <= search_end:
        iikz__elhmm = body[akc__nvqss]
        if not (isinstance(iikz__elhmm, ir.Assign) and isinstance(
            iikz__elhmm.value, ir.Const)):
            raise UnsupportedError(suehu__dxa)
        rph__ixr = iikz__elhmm.target.name
        fgsby__jqt = iikz__elhmm.value.value
        akc__nvqss += 1
        pajc__ipmvu = True
        while akc__nvqss <= search_end and pajc__ipmvu:
            fbtk__htjhv = body[akc__nvqss]
            if (isinstance(fbtk__htjhv, ir.Assign) and isinstance(
                fbtk__htjhv.value, ir.Expr) and fbtk__htjhv.value.op ==
                'getattr' and fbtk__htjhv.value.value.name == buildmap_name and
                fbtk__htjhv.value.attr == '__setitem__'):
                pajc__ipmvu = False
            else:
                akc__nvqss += 1
        if pajc__ipmvu or akc__nvqss == search_end:
            raise UnsupportedError(suehu__dxa)
        frjk__dhro = body[akc__nvqss + 1]
        if not (isinstance(frjk__dhro, ir.Assign) and isinstance(frjk__dhro
            .value, ir.Expr) and frjk__dhro.value.op == 'call' and 
            frjk__dhro.value.func.name == fbtk__htjhv.target.name and len(
            frjk__dhro.value.args) == 2 and frjk__dhro.value.args[0].name ==
            rph__ixr):
            raise UnsupportedError(suehu__dxa)
        xnyiw__nruz = frjk__dhro.value.args[1]
        iqs__lol.append((fgsby__jqt, xnyiw__nruz))
        new_body[akc__nvqss] = None
        new_body[akc__nvqss + 1] = None
        akc__nvqss += 2
    return iqs__lol


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    suehu__dxa = 'CALL_FUNCTION_EX with **kwargs not supported'
    akc__nvqss = 0
    bceym__nuvk = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        vmv__iaikb = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        vmv__iaikb = vararg_stmt.target.name
    nhyal__cww = True
    while search_end >= akc__nvqss and nhyal__cww:
        fgjw__rpqd = body[search_end]
        if (isinstance(fgjw__rpqd, ir.Assign) and fgjw__rpqd.target.name ==
            vmv__iaikb and isinstance(fgjw__rpqd.value, ir.Expr) and 
            fgjw__rpqd.value.op == 'build_tuple' and not fgjw__rpqd.value.items
            ):
            nhyal__cww = False
            new_body[search_end] = None
        else:
            if search_end == akc__nvqss or not (isinstance(fgjw__rpqd, ir.
                Assign) and fgjw__rpqd.target.name == vmv__iaikb and
                isinstance(fgjw__rpqd.value, ir.Expr) and fgjw__rpqd.value.
                op == 'binop' and fgjw__rpqd.value.fn == operator.add):
                raise UnsupportedError(suehu__dxa)
            gdhb__igmno = fgjw__rpqd.value.lhs.name
            juh__kmb = fgjw__rpqd.value.rhs.name
            sztdh__gha = body[search_end - 1]
            if not (isinstance(sztdh__gha, ir.Assign) and isinstance(
                sztdh__gha.value, ir.Expr) and sztdh__gha.value.op ==
                'build_tuple' and len(sztdh__gha.value.items) == 1):
                raise UnsupportedError(suehu__dxa)
            if sztdh__gha.target.name == gdhb__igmno:
                vmv__iaikb = juh__kmb
            elif sztdh__gha.target.name == juh__kmb:
                vmv__iaikb = gdhb__igmno
            else:
                raise UnsupportedError(suehu__dxa)
            bceym__nuvk.append(sztdh__gha.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            wxbbk__babk = True
            while search_end >= akc__nvqss and wxbbk__babk:
                ikz__fbi = body[search_end]
                if isinstance(ikz__fbi, ir.Assign
                    ) and ikz__fbi.target.name == vmv__iaikb:
                    wxbbk__babk = False
                else:
                    search_end -= 1
    if nhyal__cww:
        raise UnsupportedError(suehu__dxa)
    return bceym__nuvk[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    suehu__dxa = 'CALL_FUNCTION_EX with **kwargs not supported'
    for vkk__zqs in func_ir.blocks.values():
        abzv__hykz = False
        new_body = []
        for cevum__hvqq, zpny__tvp in enumerate(vkk__zqs.body):
            if (isinstance(zpny__tvp, ir.Assign) and isinstance(zpny__tvp.
                value, ir.Expr) and zpny__tvp.value.op == 'call' and 
                zpny__tvp.value.varkwarg is not None):
                abzv__hykz = True
                rbep__dsfv = zpny__tvp.value
                args = rbep__dsfv.args
                iqs__lol = rbep__dsfv.kws
                iksk__yldp = rbep__dsfv.vararg
                oim__csijy = rbep__dsfv.varkwarg
                dyih__zuq = cevum__hvqq - 1
                uzaxo__tdt = dyih__zuq
                qfi__tprx = None
                acty__sqwkm = True
                while uzaxo__tdt >= 0 and acty__sqwkm:
                    qfi__tprx = vkk__zqs.body[uzaxo__tdt]
                    if isinstance(qfi__tprx, ir.Assign
                        ) and qfi__tprx.target.name == oim__csijy.name:
                        acty__sqwkm = False
                    else:
                        uzaxo__tdt -= 1
                if iqs__lol or acty__sqwkm or not (isinstance(qfi__tprx.
                    value, ir.Expr) and qfi__tprx.value.op == 'build_map'):
                    raise UnsupportedError(suehu__dxa)
                if qfi__tprx.value.items:
                    iqs__lol = _call_function_ex_replace_kws_small(qfi__tprx
                        .value, new_body, uzaxo__tdt)
                else:
                    iqs__lol = _call_function_ex_replace_kws_large(vkk__zqs
                        .body, oim__csijy.name, uzaxo__tdt, cevum__hvqq - 1,
                        new_body)
                dyih__zuq = uzaxo__tdt
                if iksk__yldp is not None:
                    if args:
                        raise UnsupportedError(suehu__dxa)
                    bgpj__oxnkz = dyih__zuq
                    mfxrp__qdtl = None
                    acty__sqwkm = True
                    while bgpj__oxnkz >= 0 and acty__sqwkm:
                        mfxrp__qdtl = vkk__zqs.body[bgpj__oxnkz]
                        if isinstance(mfxrp__qdtl, ir.Assign
                            ) and mfxrp__qdtl.target.name == iksk__yldp.name:
                            acty__sqwkm = False
                        else:
                            bgpj__oxnkz -= 1
                    if acty__sqwkm:
                        raise UnsupportedError(suehu__dxa)
                    if isinstance(mfxrp__qdtl.value, ir.Expr
                        ) and mfxrp__qdtl.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(mfxrp__qdtl
                            .value, new_body, bgpj__oxnkz)
                    else:
                        args = _call_function_ex_replace_args_large(mfxrp__qdtl
                            , vkk__zqs.body, new_body, bgpj__oxnkz)
                qqxsu__pcd = ir.Expr.call(rbep__dsfv.func, args, iqs__lol,
                    rbep__dsfv.loc, target=rbep__dsfv.target)
                if zpny__tvp.target.name in func_ir._definitions and len(
                    func_ir._definitions[zpny__tvp.target.name]) == 1:
                    func_ir._definitions[zpny__tvp.target.name].clear()
                func_ir._definitions[zpny__tvp.target.name].append(qqxsu__pcd)
                zpny__tvp = ir.Assign(qqxsu__pcd, zpny__tvp.target,
                    zpny__tvp.loc)
            new_body.append(zpny__tvp)
        if abzv__hykz:
            vkk__zqs.body = [euqc__xbttn for euqc__xbttn in new_body if 
                euqc__xbttn is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for vkk__zqs in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        abzv__hykz = False
        for cevum__hvqq, zpny__tvp in enumerate(vkk__zqs.body):
            etesx__nsjc = True
            twp__ehl = None
            if isinstance(zpny__tvp, ir.Assign) and isinstance(zpny__tvp.
                value, ir.Expr):
                if zpny__tvp.value.op == 'build_map':
                    twp__ehl = zpny__tvp.target.name
                    lit_old_idx[zpny__tvp.target.name] = cevum__hvqq
                    lit_new_idx[zpny__tvp.target.name] = cevum__hvqq
                    map_updates[zpny__tvp.target.name
                        ] = zpny__tvp.value.items.copy()
                    etesx__nsjc = False
                elif zpny__tvp.value.op == 'call' and cevum__hvqq > 0:
                    sqpm__ujmoy = zpny__tvp.value.func.name
                    fbtk__htjhv = vkk__zqs.body[cevum__hvqq - 1]
                    args = zpny__tvp.value.args
                    if (isinstance(fbtk__htjhv, ir.Assign) and fbtk__htjhv.
                        target.name == sqpm__ujmoy and isinstance(
                        fbtk__htjhv.value, ir.Expr) and fbtk__htjhv.value.
                        op == 'getattr' and fbtk__htjhv.value.value.name in
                        lit_old_idx):
                        sjig__mro = fbtk__htjhv.value.value.name
                        jsj__tmn = fbtk__htjhv.value.attr
                        if jsj__tmn == '__setitem__':
                            etesx__nsjc = False
                            map_updates[sjig__mro].append(args)
                            new_body[-1] = None
                        elif jsj__tmn == 'update' and args[0
                            ].name in lit_old_idx:
                            etesx__nsjc = False
                            map_updates[sjig__mro].extend(map_updates[args[
                                0].name])
                            new_body[-1] = None
                        if not etesx__nsjc:
                            lit_new_idx[sjig__mro] = cevum__hvqq
                            func_ir._definitions[fbtk__htjhv.target.name
                                ].remove(fbtk__htjhv.value)
            if not (isinstance(zpny__tvp, ir.Assign) and isinstance(
                zpny__tvp.value, ir.Expr) and zpny__tvp.value.op ==
                'getattr' and zpny__tvp.value.value.name in lit_old_idx and
                zpny__tvp.value.attr in ('__setitem__', 'update')):
                for bkq__oyqe in zpny__tvp.list_vars():
                    if (bkq__oyqe.name in lit_old_idx and bkq__oyqe.name !=
                        twp__ehl):
                        _insert_build_map(func_ir, bkq__oyqe.name, vkk__zqs
                            .body, new_body, lit_old_idx, lit_new_idx,
                            map_updates)
            if etesx__nsjc:
                new_body.append(zpny__tvp)
            else:
                func_ir._definitions[zpny__tvp.target.name].remove(zpny__tvp
                    .value)
                abzv__hykz = True
                new_body.append(None)
        ozzi__bkizi = list(lit_old_idx.keys())
        for zjubp__dipa in ozzi__bkizi:
            _insert_build_map(func_ir, zjubp__dipa, vkk__zqs.body, new_body,
                lit_old_idx, lit_new_idx, map_updates)
        if abzv__hykz:
            vkk__zqs.body = [euqc__xbttn for euqc__xbttn in new_body if 
                euqc__xbttn is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    srxt__jfh = lit_old_idx[name]
    qvq__jmfzy = lit_new_idx[name]
    mzed__nrcs = map_updates[name]
    new_body[qvq__jmfzy] = _build_new_build_map(func_ir, name, old_body,
        srxt__jfh, mzed__nrcs)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    wwl__iwed = old_body[old_lineno]
    uaqvj__rddw = wwl__iwed.target
    gjtt__chnb = wwl__iwed.value
    acz__vpia = []
    uloxw__sff = []
    for cap__lhe in new_items:
        aiqln__decq, gwg__mnteu = cap__lhe
        knro__wwmgp = guard(get_definition, func_ir, aiqln__decq)
        if isinstance(knro__wwmgp, (ir.Const, ir.Global, ir.FreeVar)):
            acz__vpia.append(knro__wwmgp.value)
        sua__yblep = guard(get_definition, func_ir, gwg__mnteu)
        if isinstance(sua__yblep, (ir.Const, ir.Global, ir.FreeVar)):
            uloxw__sff.append(sua__yblep.value)
        else:
            uloxw__sff.append(numba.core.interpreter._UNKNOWN_VALUE(
                gwg__mnteu.name))
    oxz__znk = {}
    if len(acz__vpia) == len(new_items):
        ybx__fwzr = {euqc__xbttn: ujxk__uxd for euqc__xbttn, ujxk__uxd in
            zip(acz__vpia, uloxw__sff)}
        for cevum__hvqq, aiqln__decq in enumerate(acz__vpia):
            oxz__znk[aiqln__decq] = cevum__hvqq
    else:
        ybx__fwzr = None
    pmggc__hvdk = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=ybx__fwzr, value_indexes=oxz__znk, loc=gjtt__chnb.loc)
    func_ir._definitions[name].append(pmggc__hvdk)
    return ir.Assign(pmggc__hvdk, ir.Var(uaqvj__rddw.scope, name,
        uaqvj__rddw.loc), pmggc__hvdk.loc)
