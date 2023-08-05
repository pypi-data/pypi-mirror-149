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
            self.na_position_b = tuple([(True if opsfb__zcev == 'last' else
                False) for opsfb__zcev in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        rwm__holqh = ''
        for lngcq__jncbp, tts__pkei in self.df_in_vars.items():
            rwm__holqh += "'{}':{}, ".format(lngcq__jncbp, tts__pkei.name)
        mzsm__chr = '{}{{{}}}'.format(self.df_in, rwm__holqh)
        vtp__ekcuh = ''
        for lngcq__jncbp, tts__pkei in self.df_out_vars.items():
            vtp__ekcuh += "'{}':{}, ".format(lngcq__jncbp, tts__pkei.name)
        mtm__rnzj = '{}{{{}}}'.format(self.df_out, vtp__ekcuh)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(tts__pkei
            .name for tts__pkei in self.key_arrs), mzsm__chr, ', '.join(
            tts__pkei.name for tts__pkei in self.out_key_arrs), mtm__rnzj)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    exos__weotq = []
    okxa__auns = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for tit__orq in okxa__auns:
        bti__sbc = equiv_set.get_shape(tit__orq)
        if bti__sbc is not None:
            exos__weotq.append(bti__sbc[0])
    if len(exos__weotq) > 1:
        equiv_set.insert_equiv(*exos__weotq)
    ogk__qcenv = []
    exos__weotq = []
    vvln__idlji = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for tit__orq in vvln__idlji:
        dvka__chpa = typemap[tit__orq.name]
        llzsd__ipy = array_analysis._gen_shape_call(equiv_set, tit__orq,
            dvka__chpa.ndim, None, ogk__qcenv)
        equiv_set.insert_equiv(tit__orq, llzsd__ipy)
        exos__weotq.append(llzsd__ipy[0])
        equiv_set.define(tit__orq, set())
    if len(exos__weotq) > 1:
        equiv_set.insert_equiv(*exos__weotq)
    return [], ogk__qcenv


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    okxa__auns = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    oml__zvzc = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    aba__pxia = Distribution.OneD
    for tit__orq in okxa__auns:
        aba__pxia = Distribution(min(aba__pxia.value, array_dists[tit__orq.
            name].value))
    nbsqd__ptc = Distribution(min(aba__pxia.value, Distribution.OneD_Var.value)
        )
    for tit__orq in oml__zvzc:
        if tit__orq.name in array_dists:
            nbsqd__ptc = Distribution(min(nbsqd__ptc.value, array_dists[
                tit__orq.name].value))
    if nbsqd__ptc != Distribution.OneD_Var:
        aba__pxia = nbsqd__ptc
    for tit__orq in okxa__auns:
        array_dists[tit__orq.name] = aba__pxia
    for tit__orq in oml__zvzc:
        array_dists[tit__orq.name] = nbsqd__ptc
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for nnbhz__nqk, avsa__mxly in zip(sort_node.key_arrs, sort_node.
        out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=avsa__mxly.
            name, src=nnbhz__nqk.name, loc=sort_node.loc))
    for peoe__ruq, tit__orq in sort_node.df_in_vars.items():
        adkb__kisg = sort_node.df_out_vars[peoe__ruq]
        typeinferer.constraints.append(typeinfer.Propagate(dst=adkb__kisg.
            name, src=tit__orq.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for tit__orq in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[tit__orq.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for cfk__ydrq in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[cfk__ydrq] = visit_vars_inner(sort_node.key_arrs
            [cfk__ydrq], callback, cbdata)
        sort_node.out_key_arrs[cfk__ydrq] = visit_vars_inner(sort_node.
            out_key_arrs[cfk__ydrq], callback, cbdata)
    for peoe__ruq in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[peoe__ruq] = visit_vars_inner(sort_node.
            df_in_vars[peoe__ruq], callback, cbdata)
    for peoe__ruq in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[peoe__ruq] = visit_vars_inner(sort_node.
            df_out_vars[peoe__ruq], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    tkkh__iwloq = []
    for peoe__ruq, tit__orq in sort_node.df_out_vars.items():
        if tit__orq.name not in lives:
            tkkh__iwloq.append(peoe__ruq)
    for kkucw__vynut in tkkh__iwloq:
        sort_node.df_in_vars.pop(kkucw__vynut)
        sort_node.df_out_vars.pop(kkucw__vynut)
    if len(sort_node.df_out_vars) == 0 and all(tts__pkei.name not in lives for
        tts__pkei in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({tts__pkei.name for tts__pkei in sort_node.key_arrs})
    use_set.update({tts__pkei.name for tts__pkei in sort_node.df_in_vars.
        values()})
    if not sort_node.inplace:
        def_set.update({tts__pkei.name for tts__pkei in sort_node.out_key_arrs}
            )
        def_set.update({tts__pkei.name for tts__pkei in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    ypc__fvrw = set()
    if not sort_node.inplace:
        ypc__fvrw = set(tts__pkei.name for tts__pkei in sort_node.
            df_out_vars.values())
        ypc__fvrw.update({tts__pkei.name for tts__pkei in sort_node.
            out_key_arrs})
    return set(), ypc__fvrw


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for cfk__ydrq in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[cfk__ydrq] = replace_vars_inner(sort_node.
            key_arrs[cfk__ydrq], var_dict)
        sort_node.out_key_arrs[cfk__ydrq] = replace_vars_inner(sort_node.
            out_key_arrs[cfk__ydrq], var_dict)
    for peoe__ruq in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[peoe__ruq] = replace_vars_inner(sort_node.
            df_in_vars[peoe__ruq], var_dict)
    for peoe__ruq in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[peoe__ruq] = replace_vars_inner(sort_node.
            df_out_vars[peoe__ruq], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    wyk__opyne = False
    vkzri__rer = list(sort_node.df_in_vars.values())
    vvln__idlji = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        wyk__opyne = True
        for tts__pkei in (sort_node.key_arrs + sort_node.out_key_arrs +
            vkzri__rer + vvln__idlji):
            if array_dists[tts__pkei.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                tts__pkei.name] != distributed_pass.Distribution.OneD_Var:
                wyk__opyne = False
    loc = sort_node.loc
    owh__whsex = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        esx__dzbq = []
        for tts__pkei in key_arrs:
            ntw__thfje = _copy_array_nodes(tts__pkei, nodes, typingctx,
                targetctx, typemap, calltypes)
            esx__dzbq.append(ntw__thfje)
        key_arrs = esx__dzbq
        ffvag__mchp = []
        for tts__pkei in vkzri__rer:
            bkm__kzxpp = _copy_array_nodes(tts__pkei, nodes, typingctx,
                targetctx, typemap, calltypes)
            ffvag__mchp.append(bkm__kzxpp)
        vkzri__rer = ffvag__mchp
    key_name_args = [f'key{cfk__ydrq}' for cfk__ydrq in range(len(key_arrs))]
    dmig__ihxc = ', '.join(key_name_args)
    col_name_args = [f'c{cfk__ydrq}' for cfk__ydrq in range(len(vkzri__rer))]
    ttsvo__ivmpw = ', '.join(col_name_args)
    oivj__jxzmo = 'def f({}, {}):\n'.format(dmig__ihxc, ttsvo__ivmpw)
    oivj__jxzmo += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, wyk__opyne)
    oivj__jxzmo += '  return key_arrs, data\n'
    eji__pmwnt = {}
    exec(oivj__jxzmo, {}, eji__pmwnt)
    pbsk__wdrjn = eji__pmwnt['f']
    vlmu__hoy = types.Tuple([typemap[tts__pkei.name] for tts__pkei in key_arrs]
        )
    kvzfz__uqewt = types.Tuple([typemap[tts__pkei.name] for tts__pkei in
        vkzri__rer])
    kjif__lji = compile_to_numba_ir(pbsk__wdrjn, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(vlmu__hoy.types) + list(kvzfz__uqewt
        .types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(kjif__lji, key_arrs + vkzri__rer)
    nodes += kjif__lji.body[:-2]
    osvq__txf = nodes[-1].target
    cvm__nauxo = ir.Var(owh__whsex, mk_unique_var('key_data'), loc)
    typemap[cvm__nauxo.name] = vlmu__hoy
    gen_getitem(cvm__nauxo, osvq__txf, 0, calltypes, nodes)
    ovxfn__jqfy = ir.Var(owh__whsex, mk_unique_var('sort_data'), loc)
    typemap[ovxfn__jqfy.name] = kvzfz__uqewt
    gen_getitem(ovxfn__jqfy, osvq__txf, 1, calltypes, nodes)
    for cfk__ydrq, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, cvm__nauxo, cfk__ydrq, calltypes, nodes)
    for cfk__ydrq, var in enumerate(vvln__idlji):
        gen_getitem(var, ovxfn__jqfy, cfk__ydrq, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    kjif__lji = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(kjif__lji, [var])
    nodes += kjif__lji.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    oivj__jxzmo = ''
    vzpbj__smc = len(key_name_args)
    ubv__zxkc = ['array_to_info({})'.format(hpfio__vvu) for hpfio__vvu in
        key_name_args] + ['array_to_info({})'.format(hpfio__vvu) for
        hpfio__vvu in col_name_args]
    oivj__jxzmo += '  info_list_total = [{}]\n'.format(','.join(ubv__zxkc))
    oivj__jxzmo += '  table_total = arr_info_list_to_table(info_list_total)\n'
    oivj__jxzmo += '  vect_ascending = np.array([{}])\n'.format(','.join(
        '1' if pqfl__mfp else '0' for pqfl__mfp in ascending_list))
    oivj__jxzmo += '  na_position = np.array([{}])\n'.format(','.join('1' if
        pqfl__mfp else '0' for pqfl__mfp in na_position_b))
    oivj__jxzmo += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(vzpbj__smc, parallel_b))
    gdvw__lmfnn = 0
    vcmly__wrjiw = []
    for hpfio__vvu in key_name_args:
        vcmly__wrjiw.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(gdvw__lmfnn, hpfio__vvu))
        gdvw__lmfnn += 1
    oivj__jxzmo += '  key_arrs = ({},)\n'.format(','.join(vcmly__wrjiw))
    mokwy__cspgr = []
    for hpfio__vvu in col_name_args:
        mokwy__cspgr.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(gdvw__lmfnn, hpfio__vvu))
        gdvw__lmfnn += 1
    if len(mokwy__cspgr) > 0:
        oivj__jxzmo += '  data = ({},)\n'.format(','.join(mokwy__cspgr))
    else:
        oivj__jxzmo += '  data = ()\n'
    oivj__jxzmo += '  delete_table(out_table)\n'
    oivj__jxzmo += '  delete_table(table_total)\n'
    return oivj__jxzmo
