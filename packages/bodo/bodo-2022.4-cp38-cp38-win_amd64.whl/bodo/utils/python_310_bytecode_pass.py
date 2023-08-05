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
    cuxe__zwg = keyword_expr.items.copy()
    uev__vxag = keyword_expr.value_indexes
    for pfh__tblo, ayq__tuvtk in uev__vxag.items():
        cuxe__zwg[ayq__tuvtk] = pfh__tblo, cuxe__zwg[ayq__tuvtk][1]
    new_body[buildmap_idx] = None
    return cuxe__zwg


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    gaj__wfkm = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    cuxe__zwg = []
    scu__ceyi = buildmap_idx + 1
    while scu__ceyi <= search_end:
        qgooh__jybu = body[scu__ceyi]
        if not (isinstance(qgooh__jybu, ir.Assign) and isinstance(
            qgooh__jybu.value, ir.Const)):
            raise UnsupportedError(gaj__wfkm)
        xoy__iwzg = qgooh__jybu.target.name
        awur__pnah = qgooh__jybu.value.value
        scu__ceyi += 1
        xfzz__rkn = True
        while scu__ceyi <= search_end and xfzz__rkn:
            vjbk__ffklo = body[scu__ceyi]
            if (isinstance(vjbk__ffklo, ir.Assign) and isinstance(
                vjbk__ffklo.value, ir.Expr) and vjbk__ffklo.value.op ==
                'getattr' and vjbk__ffklo.value.value.name == buildmap_name and
                vjbk__ffklo.value.attr == '__setitem__'):
                xfzz__rkn = False
            else:
                scu__ceyi += 1
        if xfzz__rkn or scu__ceyi == search_end:
            raise UnsupportedError(gaj__wfkm)
        wcy__idn = body[scu__ceyi + 1]
        if not (isinstance(wcy__idn, ir.Assign) and isinstance(wcy__idn.
            value, ir.Expr) and wcy__idn.value.op == 'call' and wcy__idn.
            value.func.name == vjbk__ffklo.target.name and len(wcy__idn.
            value.args) == 2 and wcy__idn.value.args[0].name == xoy__iwzg):
            raise UnsupportedError(gaj__wfkm)
        zyci__jtkeo = wcy__idn.value.args[1]
        cuxe__zwg.append((awur__pnah, zyci__jtkeo))
        new_body[scu__ceyi] = None
        new_body[scu__ceyi + 1] = None
        scu__ceyi += 2
    return cuxe__zwg


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    gaj__wfkm = 'CALL_FUNCTION_EX with **kwargs not supported'
    scu__ceyi = 0
    tjutj__ggl = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        pze__axb = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        pze__axb = vararg_stmt.target.name
    ofnce__pwo = True
    while search_end >= scu__ceyi and ofnce__pwo:
        ouptw__iueyg = body[search_end]
        if (isinstance(ouptw__iueyg, ir.Assign) and ouptw__iueyg.target.
            name == pze__axb and isinstance(ouptw__iueyg.value, ir.Expr) and
            ouptw__iueyg.value.op == 'build_tuple' and not ouptw__iueyg.
            value.items):
            ofnce__pwo = False
            new_body[search_end] = None
        else:
            if search_end == scu__ceyi or not (isinstance(ouptw__iueyg, ir.
                Assign) and ouptw__iueyg.target.name == pze__axb and
                isinstance(ouptw__iueyg.value, ir.Expr) and ouptw__iueyg.
                value.op == 'binop' and ouptw__iueyg.value.fn == operator.add):
                raise UnsupportedError(gaj__wfkm)
            hpy__mes = ouptw__iueyg.value.lhs.name
            guqja__dgb = ouptw__iueyg.value.rhs.name
            ndjtb__obr = body[search_end - 1]
            if not (isinstance(ndjtb__obr, ir.Assign) and isinstance(
                ndjtb__obr.value, ir.Expr) and ndjtb__obr.value.op ==
                'build_tuple' and len(ndjtb__obr.value.items) == 1):
                raise UnsupportedError(gaj__wfkm)
            if ndjtb__obr.target.name == hpy__mes:
                pze__axb = guqja__dgb
            elif ndjtb__obr.target.name == guqja__dgb:
                pze__axb = hpy__mes
            else:
                raise UnsupportedError(gaj__wfkm)
            tjutj__ggl.append(ndjtb__obr.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            jeglm__mksfp = True
            while search_end >= scu__ceyi and jeglm__mksfp:
                ord__eskfj = body[search_end]
                if isinstance(ord__eskfj, ir.Assign
                    ) and ord__eskfj.target.name == pze__axb:
                    jeglm__mksfp = False
                else:
                    search_end -= 1
    if ofnce__pwo:
        raise UnsupportedError(gaj__wfkm)
    return tjutj__ggl[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    gaj__wfkm = 'CALL_FUNCTION_EX with **kwargs not supported'
    for wuf__tbqd in func_ir.blocks.values():
        hoaeh__mmxvy = False
        new_body = []
        for dhkx__hiywk, vkley__lhdvq in enumerate(wuf__tbqd.body):
            if (isinstance(vkley__lhdvq, ir.Assign) and isinstance(
                vkley__lhdvq.value, ir.Expr) and vkley__lhdvq.value.op ==
                'call' and vkley__lhdvq.value.varkwarg is not None):
                hoaeh__mmxvy = True
                opv__mho = vkley__lhdvq.value
                args = opv__mho.args
                cuxe__zwg = opv__mho.kws
                emb__kiv = opv__mho.vararg
                dyrf__lnm = opv__mho.varkwarg
                veon__zbhcd = dhkx__hiywk - 1
                ywz__sdmnp = veon__zbhcd
                tcl__thdv = None
                gqhxy__dfmrj = True
                while ywz__sdmnp >= 0 and gqhxy__dfmrj:
                    tcl__thdv = wuf__tbqd.body[ywz__sdmnp]
                    if isinstance(tcl__thdv, ir.Assign
                        ) and tcl__thdv.target.name == dyrf__lnm.name:
                        gqhxy__dfmrj = False
                    else:
                        ywz__sdmnp -= 1
                if cuxe__zwg or gqhxy__dfmrj or not (isinstance(tcl__thdv.
                    value, ir.Expr) and tcl__thdv.value.op == 'build_map'):
                    raise UnsupportedError(gaj__wfkm)
                if tcl__thdv.value.items:
                    cuxe__zwg = _call_function_ex_replace_kws_small(tcl__thdv
                        .value, new_body, ywz__sdmnp)
                else:
                    cuxe__zwg = _call_function_ex_replace_kws_large(wuf__tbqd
                        .body, dyrf__lnm.name, ywz__sdmnp, dhkx__hiywk - 1,
                        new_body)
                veon__zbhcd = ywz__sdmnp
                if emb__kiv is not None:
                    if args:
                        raise UnsupportedError(gaj__wfkm)
                    ogu__ytrw = veon__zbhcd
                    ytf__ynam = None
                    gqhxy__dfmrj = True
                    while ogu__ytrw >= 0 and gqhxy__dfmrj:
                        ytf__ynam = wuf__tbqd.body[ogu__ytrw]
                        if isinstance(ytf__ynam, ir.Assign
                            ) and ytf__ynam.target.name == emb__kiv.name:
                            gqhxy__dfmrj = False
                        else:
                            ogu__ytrw -= 1
                    if gqhxy__dfmrj:
                        raise UnsupportedError(gaj__wfkm)
                    if isinstance(ytf__ynam.value, ir.Expr
                        ) and ytf__ynam.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(ytf__ynam
                            .value, new_body, ogu__ytrw)
                    else:
                        args = _call_function_ex_replace_args_large(ytf__ynam,
                            wuf__tbqd.body, new_body, ogu__ytrw)
                pgr__dfxf = ir.Expr.call(opv__mho.func, args, cuxe__zwg,
                    opv__mho.loc, target=opv__mho.target)
                if vkley__lhdvq.target.name in func_ir._definitions and len(
                    func_ir._definitions[vkley__lhdvq.target.name]) == 1:
                    func_ir._definitions[vkley__lhdvq.target.name].clear()
                func_ir._definitions[vkley__lhdvq.target.name].append(pgr__dfxf
                    )
                vkley__lhdvq = ir.Assign(pgr__dfxf, vkley__lhdvq.target,
                    vkley__lhdvq.loc)
            new_body.append(vkley__lhdvq)
        if hoaeh__mmxvy:
            wuf__tbqd.body = [ppxp__ezrey for ppxp__ezrey in new_body if 
                ppxp__ezrey is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for wuf__tbqd in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        hoaeh__mmxvy = False
        for dhkx__hiywk, vkley__lhdvq in enumerate(wuf__tbqd.body):
            fhf__utl = True
            vcehq__krun = None
            if isinstance(vkley__lhdvq, ir.Assign) and isinstance(vkley__lhdvq
                .value, ir.Expr):
                if vkley__lhdvq.value.op == 'build_map':
                    vcehq__krun = vkley__lhdvq.target.name
                    lit_old_idx[vkley__lhdvq.target.name] = dhkx__hiywk
                    lit_new_idx[vkley__lhdvq.target.name] = dhkx__hiywk
                    map_updates[vkley__lhdvq.target.name
                        ] = vkley__lhdvq.value.items.copy()
                    fhf__utl = False
                elif vkley__lhdvq.value.op == 'call' and dhkx__hiywk > 0:
                    nvx__ejvf = vkley__lhdvq.value.func.name
                    vjbk__ffklo = wuf__tbqd.body[dhkx__hiywk - 1]
                    args = vkley__lhdvq.value.args
                    if (isinstance(vjbk__ffklo, ir.Assign) and vjbk__ffklo.
                        target.name == nvx__ejvf and isinstance(vjbk__ffklo
                        .value, ir.Expr) and vjbk__ffklo.value.op ==
                        'getattr' and vjbk__ffklo.value.value.name in
                        lit_old_idx):
                        llz__pje = vjbk__ffklo.value.value.name
                        uhbm__uhngk = vjbk__ffklo.value.attr
                        if uhbm__uhngk == '__setitem__':
                            fhf__utl = False
                            map_updates[llz__pje].append(args)
                            new_body[-1] = None
                        elif uhbm__uhngk == 'update' and args[0
                            ].name in lit_old_idx:
                            fhf__utl = False
                            map_updates[llz__pje].extend(map_updates[args[0
                                ].name])
                            new_body[-1] = None
                        if not fhf__utl:
                            lit_new_idx[llz__pje] = dhkx__hiywk
                            func_ir._definitions[vjbk__ffklo.target.name
                                ].remove(vjbk__ffklo.value)
            if not (isinstance(vkley__lhdvq, ir.Assign) and isinstance(
                vkley__lhdvq.value, ir.Expr) and vkley__lhdvq.value.op ==
                'getattr' and vkley__lhdvq.value.value.name in lit_old_idx and
                vkley__lhdvq.value.attr in ('__setitem__', 'update')):
                for wsp__obw in vkley__lhdvq.list_vars():
                    if (wsp__obw.name in lit_old_idx and wsp__obw.name !=
                        vcehq__krun):
                        _insert_build_map(func_ir, wsp__obw.name, wuf__tbqd
                            .body, new_body, lit_old_idx, lit_new_idx,
                            map_updates)
            if fhf__utl:
                new_body.append(vkley__lhdvq)
            else:
                func_ir._definitions[vkley__lhdvq.target.name].remove(
                    vkley__lhdvq.value)
                hoaeh__mmxvy = True
                new_body.append(None)
        pgznz__xluk = list(lit_old_idx.keys())
        for ndcoe__lep in pgznz__xluk:
            _insert_build_map(func_ir, ndcoe__lep, wuf__tbqd.body, new_body,
                lit_old_idx, lit_new_idx, map_updates)
        if hoaeh__mmxvy:
            wuf__tbqd.body = [ppxp__ezrey for ppxp__ezrey in new_body if 
                ppxp__ezrey is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    crg__jgpt = lit_old_idx[name]
    kaded__lyymm = lit_new_idx[name]
    yzxb__eunk = map_updates[name]
    new_body[kaded__lyymm] = _build_new_build_map(func_ir, name, old_body,
        crg__jgpt, yzxb__eunk)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    fgm__ihius = old_body[old_lineno]
    xuj__hlv = fgm__ihius.target
    pndz__ufkuz = fgm__ihius.value
    bmq__def = []
    nqfc__qolb = []
    for ryyc__ngj in new_items:
        fxgcb__xmr, mpbt__nmj = ryyc__ngj
        rphop__xalt = guard(get_definition, func_ir, fxgcb__xmr)
        if isinstance(rphop__xalt, (ir.Const, ir.Global, ir.FreeVar)):
            bmq__def.append(rphop__xalt.value)
        mziy__ixp = guard(get_definition, func_ir, mpbt__nmj)
        if isinstance(mziy__ixp, (ir.Const, ir.Global, ir.FreeVar)):
            nqfc__qolb.append(mziy__ixp.value)
        else:
            nqfc__qolb.append(numba.core.interpreter._UNKNOWN_VALUE(
                mpbt__nmj.name))
    uev__vxag = {}
    if len(bmq__def) == len(new_items):
        uqoz__lud = {ppxp__ezrey: zip__iql for ppxp__ezrey, zip__iql in zip
            (bmq__def, nqfc__qolb)}
        for dhkx__hiywk, fxgcb__xmr in enumerate(bmq__def):
            uev__vxag[fxgcb__xmr] = dhkx__hiywk
    else:
        uqoz__lud = None
    xugyt__xudog = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=uqoz__lud, value_indexes=uev__vxag, loc=pndz__ufkuz.loc)
    func_ir._definitions[name].append(xugyt__xudog)
    return ir.Assign(xugyt__xudog, ir.Var(xuj__hlv.scope, name, xuj__hlv.
        loc), xugyt__xudog.loc)
