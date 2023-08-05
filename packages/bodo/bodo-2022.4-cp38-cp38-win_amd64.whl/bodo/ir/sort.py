"""IR node for the data sorting"""
from collections import defaultdict
import numba
import numpy as np
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, mk_unique_var, replace_arg_nodes, replace_vars_inner, visit_vars_inner
import bodo
import bodo.libs.timsort
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, sort_values_table
from bodo.libs.str_arr_ext import cp_str_list_to_array, to_list_if_immutable_arr
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.utils import debug_prints, gen_getitem
MIN_SAMPLES = 1000000
samplePointsPerPartitionHint = 20
MPI_ROOT = 0


class Sort(ir.Stmt):

    def __init__(self, df_in, df_out, key_arrs, out_key_arrs, df_in_vars,
        df_out_vars, inplace, loc, ascending_list=True, na_position='last'):
        self.df_in = df_in
        self.df_out = df_out
        self.key_arrs = key_arrs
        self.out_key_arrs = out_key_arrs
        self.df_in_vars = df_in_vars
        self.df_out_vars = df_out_vars
        self.inplace = inplace
        if isinstance(na_position, str):
            if na_position == 'last':
                self.na_position_b = (True,) * len(key_arrs)
            else:
                self.na_position_b = (False,) * len(key_arrs)
        else:
            self.na_position_b = tuple([(True if olrs__iosz == 'last' else 
                False) for olrs__iosz in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        hfir__upzm = ''
        for cpoiv__qjad, yid__vsihf in self.df_in_vars.items():
            hfir__upzm += "'{}':{}, ".format(cpoiv__qjad, yid__vsihf.name)
        deblk__xszkj = '{}{{{}}}'.format(self.df_in, hfir__upzm)
        mcwu__csz = ''
        for cpoiv__qjad, yid__vsihf in self.df_out_vars.items():
            mcwu__csz += "'{}':{}, ".format(cpoiv__qjad, yid__vsihf.name)
        lko__uyqn = '{}{{{}}}'.format(self.df_out, mcwu__csz)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(
            yid__vsihf.name for yid__vsihf in self.key_arrs), deblk__xszkj,
            ', '.join(yid__vsihf.name for yid__vsihf in self.out_key_arrs),
            lko__uyqn)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    jhc__auhh = []
    plfh__ndr = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for npri__mongu in plfh__ndr:
        zgm__ffy = equiv_set.get_shape(npri__mongu)
        if zgm__ffy is not None:
            jhc__auhh.append(zgm__ffy[0])
    if len(jhc__auhh) > 1:
        equiv_set.insert_equiv(*jhc__auhh)
    fjl__iwujj = []
    jhc__auhh = []
    dueiq__kqt = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for npri__mongu in dueiq__kqt:
        ccfw__rxafc = typemap[npri__mongu.name]
        lvyzf__ejo = array_analysis._gen_shape_call(equiv_set, npri__mongu,
            ccfw__rxafc.ndim, None, fjl__iwujj)
        equiv_set.insert_equiv(npri__mongu, lvyzf__ejo)
        jhc__auhh.append(lvyzf__ejo[0])
        equiv_set.define(npri__mongu, set())
    if len(jhc__auhh) > 1:
        equiv_set.insert_equiv(*jhc__auhh)
    return [], fjl__iwujj


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    plfh__ndr = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    qtw__riwbe = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    yaqp__nwxo = Distribution.OneD
    for npri__mongu in plfh__ndr:
        yaqp__nwxo = Distribution(min(yaqp__nwxo.value, array_dists[
            npri__mongu.name].value))
    qolp__uense = Distribution(min(yaqp__nwxo.value, Distribution.OneD_Var.
        value))
    for npri__mongu in qtw__riwbe:
        if npri__mongu.name in array_dists:
            qolp__uense = Distribution(min(qolp__uense.value, array_dists[
                npri__mongu.name].value))
    if qolp__uense != Distribution.OneD_Var:
        yaqp__nwxo = qolp__uense
    for npri__mongu in plfh__ndr:
        array_dists[npri__mongu.name] = yaqp__nwxo
    for npri__mongu in qtw__riwbe:
        array_dists[npri__mongu.name] = qolp__uense
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for hohfo__opn, tas__xdu in zip(sort_node.key_arrs, sort_node.out_key_arrs
        ):
        typeinferer.constraints.append(typeinfer.Propagate(dst=tas__xdu.
            name, src=hohfo__opn.name, loc=sort_node.loc))
    for zzg__godo, npri__mongu in sort_node.df_in_vars.items():
        ctc__jqx = sort_node.df_out_vars[zzg__godo]
        typeinferer.constraints.append(typeinfer.Propagate(dst=ctc__jqx.
            name, src=npri__mongu.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for npri__mongu in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[npri__mongu.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for xxaom__ntd in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[xxaom__ntd] = visit_vars_inner(sort_node.
            key_arrs[xxaom__ntd], callback, cbdata)
        sort_node.out_key_arrs[xxaom__ntd] = visit_vars_inner(sort_node.
            out_key_arrs[xxaom__ntd], callback, cbdata)
    for zzg__godo in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[zzg__godo] = visit_vars_inner(sort_node.
            df_in_vars[zzg__godo], callback, cbdata)
    for zzg__godo in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[zzg__godo] = visit_vars_inner(sort_node.
            df_out_vars[zzg__godo], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    zxscj__ilf = []
    for zzg__godo, npri__mongu in sort_node.df_out_vars.items():
        if npri__mongu.name not in lives:
            zxscj__ilf.append(zzg__godo)
    for lbwo__bte in zxscj__ilf:
        sort_node.df_in_vars.pop(lbwo__bte)
        sort_node.df_out_vars.pop(lbwo__bte)
    if len(sort_node.df_out_vars) == 0 and all(yid__vsihf.name not in lives for
        yid__vsihf in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({yid__vsihf.name for yid__vsihf in sort_node.key_arrs})
    use_set.update({yid__vsihf.name for yid__vsihf in sort_node.df_in_vars.
        values()})
    if not sort_node.inplace:
        def_set.update({yid__vsihf.name for yid__vsihf in sort_node.
            out_key_arrs})
        def_set.update({yid__vsihf.name for yid__vsihf in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    ltcc__sjeru = set()
    if not sort_node.inplace:
        ltcc__sjeru = set(yid__vsihf.name for yid__vsihf in sort_node.
            df_out_vars.values())
        ltcc__sjeru.update({yid__vsihf.name for yid__vsihf in sort_node.
            out_key_arrs})
    return set(), ltcc__sjeru


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for xxaom__ntd in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[xxaom__ntd] = replace_vars_inner(sort_node.
            key_arrs[xxaom__ntd], var_dict)
        sort_node.out_key_arrs[xxaom__ntd] = replace_vars_inner(sort_node.
            out_key_arrs[xxaom__ntd], var_dict)
    for zzg__godo in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[zzg__godo] = replace_vars_inner(sort_node.
            df_in_vars[zzg__godo], var_dict)
    for zzg__godo in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[zzg__godo] = replace_vars_inner(sort_node.
            df_out_vars[zzg__godo], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    omefj__btj = False
    zzncc__svy = list(sort_node.df_in_vars.values())
    dueiq__kqt = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        omefj__btj = True
        for yid__vsihf in (sort_node.key_arrs + sort_node.out_key_arrs +
            zzncc__svy + dueiq__kqt):
            if array_dists[yid__vsihf.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                yid__vsihf.name] != distributed_pass.Distribution.OneD_Var:
                omefj__btj = False
    loc = sort_node.loc
    czgz__kubb = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        ysiz__vko = []
        for yid__vsihf in key_arrs:
            hmc__mghmo = _copy_array_nodes(yid__vsihf, nodes, typingctx,
                targetctx, typemap, calltypes)
            ysiz__vko.append(hmc__mghmo)
        key_arrs = ysiz__vko
        yyr__vzu = []
        for yid__vsihf in zzncc__svy:
            wpox__ydz = _copy_array_nodes(yid__vsihf, nodes, typingctx,
                targetctx, typemap, calltypes)
            yyr__vzu.append(wpox__ydz)
        zzncc__svy = yyr__vzu
    key_name_args = [f'key{xxaom__ntd}' for xxaom__ntd in range(len(key_arrs))]
    pii__rfnq = ', '.join(key_name_args)
    col_name_args = [f'c{xxaom__ntd}' for xxaom__ntd in range(len(zzncc__svy))]
    lrc__iqax = ', '.join(col_name_args)
    pqos__zrjl = 'def f({}, {}):\n'.format(pii__rfnq, lrc__iqax)
    pqos__zrjl += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, omefj__btj)
    pqos__zrjl += '  return key_arrs, data\n'
    otmn__wbsd = {}
    exec(pqos__zrjl, {}, otmn__wbsd)
    xaxs__xob = otmn__wbsd['f']
    zmy__hyl = types.Tuple([typemap[yid__vsihf.name] for yid__vsihf in
        key_arrs])
    lfcxc__pbkbk = types.Tuple([typemap[yid__vsihf.name] for yid__vsihf in
        zzncc__svy])
    omw__qutq = compile_to_numba_ir(xaxs__xob, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(zmy__hyl.types) + list(lfcxc__pbkbk.
        types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(omw__qutq, key_arrs + zzncc__svy)
    nodes += omw__qutq.body[:-2]
    vaedt__amxrn = nodes[-1].target
    rza__tmvip = ir.Var(czgz__kubb, mk_unique_var('key_data'), loc)
    typemap[rza__tmvip.name] = zmy__hyl
    gen_getitem(rza__tmvip, vaedt__amxrn, 0, calltypes, nodes)
    qrhme__mywat = ir.Var(czgz__kubb, mk_unique_var('sort_data'), loc)
    typemap[qrhme__mywat.name] = lfcxc__pbkbk
    gen_getitem(qrhme__mywat, vaedt__amxrn, 1, calltypes, nodes)
    for xxaom__ntd, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, rza__tmvip, xxaom__ntd, calltypes, nodes)
    for xxaom__ntd, var in enumerate(dueiq__kqt):
        gen_getitem(var, qrhme__mywat, xxaom__ntd, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    omw__qutq = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(omw__qutq, [var])
    nodes += omw__qutq.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    pqos__zrjl = ''
    nxst__ohntz = len(key_name_args)
    fwy__xeqa = ['array_to_info({})'.format(xpg__uhxk) for xpg__uhxk in
        key_name_args] + ['array_to_info({})'.format(xpg__uhxk) for
        xpg__uhxk in col_name_args]
    pqos__zrjl += '  info_list_total = [{}]\n'.format(','.join(fwy__xeqa))
    pqos__zrjl += '  table_total = arr_info_list_to_table(info_list_total)\n'
    pqos__zrjl += '  vect_ascending = np.array([{}])\n'.format(','.join('1' if
        wno__xqb else '0' for wno__xqb in ascending_list))
    pqos__zrjl += '  na_position = np.array([{}])\n'.format(','.join('1' if
        wno__xqb else '0' for wno__xqb in na_position_b))
    pqos__zrjl += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(nxst__ohntz, parallel_b))
    nbqu__juz = 0
    ktp__mibav = []
    for xpg__uhxk in key_name_args:
        ktp__mibav.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(nbqu__juz, xpg__uhxk))
        nbqu__juz += 1
    pqos__zrjl += '  key_arrs = ({},)\n'.format(','.join(ktp__mibav))
    ptium__tsrr = []
    for xpg__uhxk in col_name_args:
        ptium__tsrr.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(nbqu__juz, xpg__uhxk))
        nbqu__juz += 1
    if len(ptium__tsrr) > 0:
        pqos__zrjl += '  data = ({},)\n'.format(','.join(ptium__tsrr))
    else:
        pqos__zrjl += '  data = ()\n'
    pqos__zrjl += '  delete_table(out_table)\n'
    pqos__zrjl += '  delete_table(table_total)\n'
    return pqos__zrjl
