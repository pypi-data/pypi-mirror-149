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
            self.na_position_b = tuple([(True if kroeq__hgwd == 'last' else
                False) for kroeq__hgwd in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        kpkwn__nhbx = ''
        for vizpp__etr, spa__sjzp in self.df_in_vars.items():
            kpkwn__nhbx += "'{}':{}, ".format(vizpp__etr, spa__sjzp.name)
        uekb__nzlj = '{}{{{}}}'.format(self.df_in, kpkwn__nhbx)
        tzew__agp = ''
        for vizpp__etr, spa__sjzp in self.df_out_vars.items():
            tzew__agp += "'{}':{}, ".format(vizpp__etr, spa__sjzp.name)
        hzzpc__uwdzl = '{}{{{}}}'.format(self.df_out, tzew__agp)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(spa__sjzp
            .name for spa__sjzp in self.key_arrs), uekb__nzlj, ', '.join(
            spa__sjzp.name for spa__sjzp in self.out_key_arrs), hzzpc__uwdzl)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    qoa__igofb = []
    ujfcc__qqr = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for vaxye__arq in ujfcc__qqr:
        tec__gqgt = equiv_set.get_shape(vaxye__arq)
        if tec__gqgt is not None:
            qoa__igofb.append(tec__gqgt[0])
    if len(qoa__igofb) > 1:
        equiv_set.insert_equiv(*qoa__igofb)
    vct__frnnr = []
    qoa__igofb = []
    fpk__fys = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for vaxye__arq in fpk__fys:
        csru__srib = typemap[vaxye__arq.name]
        xcead__cxmh = array_analysis._gen_shape_call(equiv_set, vaxye__arq,
            csru__srib.ndim, None, vct__frnnr)
        equiv_set.insert_equiv(vaxye__arq, xcead__cxmh)
        qoa__igofb.append(xcead__cxmh[0])
        equiv_set.define(vaxye__arq, set())
    if len(qoa__igofb) > 1:
        equiv_set.insert_equiv(*qoa__igofb)
    return [], vct__frnnr


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    ujfcc__qqr = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    pgcj__wyli = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    oyhrb__crm = Distribution.OneD
    for vaxye__arq in ujfcc__qqr:
        oyhrb__crm = Distribution(min(oyhrb__crm.value, array_dists[
            vaxye__arq.name].value))
    ozgl__yjmi = Distribution(min(oyhrb__crm.value, Distribution.OneD_Var.
        value))
    for vaxye__arq in pgcj__wyli:
        if vaxye__arq.name in array_dists:
            ozgl__yjmi = Distribution(min(ozgl__yjmi.value, array_dists[
                vaxye__arq.name].value))
    if ozgl__yjmi != Distribution.OneD_Var:
        oyhrb__crm = ozgl__yjmi
    for vaxye__arq in ujfcc__qqr:
        array_dists[vaxye__arq.name] = oyhrb__crm
    for vaxye__arq in pgcj__wyli:
        array_dists[vaxye__arq.name] = ozgl__yjmi
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for agrcx__hgta, kovz__qst in zip(sort_node.key_arrs, sort_node.
        out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=kovz__qst.
            name, src=agrcx__hgta.name, loc=sort_node.loc))
    for vfusd__rnduz, vaxye__arq in sort_node.df_in_vars.items():
        rciam__ect = sort_node.df_out_vars[vfusd__rnduz]
        typeinferer.constraints.append(typeinfer.Propagate(dst=rciam__ect.
            name, src=vaxye__arq.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for vaxye__arq in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[vaxye__arq.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for buqj__wmuo in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[buqj__wmuo] = visit_vars_inner(sort_node.
            key_arrs[buqj__wmuo], callback, cbdata)
        sort_node.out_key_arrs[buqj__wmuo] = visit_vars_inner(sort_node.
            out_key_arrs[buqj__wmuo], callback, cbdata)
    for vfusd__rnduz in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[vfusd__rnduz] = visit_vars_inner(sort_node.
            df_in_vars[vfusd__rnduz], callback, cbdata)
    for vfusd__rnduz in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[vfusd__rnduz] = visit_vars_inner(sort_node.
            df_out_vars[vfusd__rnduz], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    kixh__dzlc = []
    for vfusd__rnduz, vaxye__arq in sort_node.df_out_vars.items():
        if vaxye__arq.name not in lives:
            kixh__dzlc.append(vfusd__rnduz)
    for mgoa__nuox in kixh__dzlc:
        sort_node.df_in_vars.pop(mgoa__nuox)
        sort_node.df_out_vars.pop(mgoa__nuox)
    if len(sort_node.df_out_vars) == 0 and all(spa__sjzp.name not in lives for
        spa__sjzp in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({spa__sjzp.name for spa__sjzp in sort_node.key_arrs})
    use_set.update({spa__sjzp.name for spa__sjzp in sort_node.df_in_vars.
        values()})
    if not sort_node.inplace:
        def_set.update({spa__sjzp.name for spa__sjzp in sort_node.out_key_arrs}
            )
        def_set.update({spa__sjzp.name for spa__sjzp in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    rezc__kycpp = set()
    if not sort_node.inplace:
        rezc__kycpp = set(spa__sjzp.name for spa__sjzp in sort_node.
            df_out_vars.values())
        rezc__kycpp.update({spa__sjzp.name for spa__sjzp in sort_node.
            out_key_arrs})
    return set(), rezc__kycpp


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for buqj__wmuo in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[buqj__wmuo] = replace_vars_inner(sort_node.
            key_arrs[buqj__wmuo], var_dict)
        sort_node.out_key_arrs[buqj__wmuo] = replace_vars_inner(sort_node.
            out_key_arrs[buqj__wmuo], var_dict)
    for vfusd__rnduz in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[vfusd__rnduz] = replace_vars_inner(sort_node.
            df_in_vars[vfusd__rnduz], var_dict)
    for vfusd__rnduz in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[vfusd__rnduz] = replace_vars_inner(sort_node.
            df_out_vars[vfusd__rnduz], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    nof__nphm = False
    usbhi__qecj = list(sort_node.df_in_vars.values())
    fpk__fys = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        nof__nphm = True
        for spa__sjzp in (sort_node.key_arrs + sort_node.out_key_arrs +
            usbhi__qecj + fpk__fys):
            if array_dists[spa__sjzp.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                spa__sjzp.name] != distributed_pass.Distribution.OneD_Var:
                nof__nphm = False
    loc = sort_node.loc
    shbnw__zbqd = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        unu__upp = []
        for spa__sjzp in key_arrs:
            aex__ihjh = _copy_array_nodes(spa__sjzp, nodes, typingctx,
                targetctx, typemap, calltypes)
            unu__upp.append(aex__ihjh)
        key_arrs = unu__upp
        xjou__eyh = []
        for spa__sjzp in usbhi__qecj:
            yjw__ydg = _copy_array_nodes(spa__sjzp, nodes, typingctx,
                targetctx, typemap, calltypes)
            xjou__eyh.append(yjw__ydg)
        usbhi__qecj = xjou__eyh
    key_name_args = [f'key{buqj__wmuo}' for buqj__wmuo in range(len(key_arrs))]
    xuzbf__guy = ', '.join(key_name_args)
    col_name_args = [f'c{buqj__wmuo}' for buqj__wmuo in range(len(usbhi__qecj))
        ]
    vavl__ljxbk = ', '.join(col_name_args)
    wvgg__ehpe = 'def f({}, {}):\n'.format(xuzbf__guy, vavl__ljxbk)
    wvgg__ehpe += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, nof__nphm)
    wvgg__ehpe += '  return key_arrs, data\n'
    hequ__szr = {}
    exec(wvgg__ehpe, {}, hequ__szr)
    juo__hhtn = hequ__szr['f']
    wjk__rcdas = types.Tuple([typemap[spa__sjzp.name] for spa__sjzp in
        key_arrs])
    qqxg__nqe = types.Tuple([typemap[spa__sjzp.name] for spa__sjzp in
        usbhi__qecj])
    avuz__yjjh = compile_to_numba_ir(juo__hhtn, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(wjk__rcdas.types) + list(qqxg__nqe.
        types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(avuz__yjjh, key_arrs + usbhi__qecj)
    nodes += avuz__yjjh.body[:-2]
    lxvk__hkec = nodes[-1].target
    ccl__brhp = ir.Var(shbnw__zbqd, mk_unique_var('key_data'), loc)
    typemap[ccl__brhp.name] = wjk__rcdas
    gen_getitem(ccl__brhp, lxvk__hkec, 0, calltypes, nodes)
    fct__qiod = ir.Var(shbnw__zbqd, mk_unique_var('sort_data'), loc)
    typemap[fct__qiod.name] = qqxg__nqe
    gen_getitem(fct__qiod, lxvk__hkec, 1, calltypes, nodes)
    for buqj__wmuo, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, ccl__brhp, buqj__wmuo, calltypes, nodes)
    for buqj__wmuo, var in enumerate(fpk__fys):
        gen_getitem(var, fct__qiod, buqj__wmuo, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    avuz__yjjh = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(avuz__yjjh, [var])
    nodes += avuz__yjjh.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    wvgg__ehpe = ''
    jdsul__omoz = len(key_name_args)
    nuvn__kjhc = ['array_to_info({})'.format(bnk__atftu) for bnk__atftu in
        key_name_args] + ['array_to_info({})'.format(bnk__atftu) for
        bnk__atftu in col_name_args]
    wvgg__ehpe += '  info_list_total = [{}]\n'.format(','.join(nuvn__kjhc))
    wvgg__ehpe += '  table_total = arr_info_list_to_table(info_list_total)\n'
    wvgg__ehpe += '  vect_ascending = np.array([{}])\n'.format(','.join('1' if
        dli__svt else '0' for dli__svt in ascending_list))
    wvgg__ehpe += '  na_position = np.array([{}])\n'.format(','.join('1' if
        dli__svt else '0' for dli__svt in na_position_b))
    wvgg__ehpe += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(jdsul__omoz, parallel_b))
    pfqr__xdh = 0
    fqdiq__zlwxs = []
    for bnk__atftu in key_name_args:
        fqdiq__zlwxs.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(pfqr__xdh, bnk__atftu))
        pfqr__xdh += 1
    wvgg__ehpe += '  key_arrs = ({},)\n'.format(','.join(fqdiq__zlwxs))
    meq__ioij = []
    for bnk__atftu in col_name_args:
        meq__ioij.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(pfqr__xdh, bnk__atftu))
        pfqr__xdh += 1
    if len(meq__ioij) > 0:
        wvgg__ehpe += '  data = ({},)\n'.format(','.join(meq__ioij))
    else:
        wvgg__ehpe += '  data = ()\n'
    wvgg__ehpe += '  delete_table(out_table)\n'
    wvgg__ehpe += '  delete_table(table_total)\n'
    return wvgg__ehpe
