"""IR node for the join and merge"""
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic, overload
import bodo
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, hash_join_table, info_from_table, info_to_array
from bodo.libs.int_arr_ext import IntDtype
from bodo.libs.str_arr_ext import cp_str_list_to_array, to_list_if_immutable_arr
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.typing import BodoError, dtype_to_array_type, find_common_np_dtype, is_dtype_nullable, is_nullable_type, is_str_arr_type, to_nullable_type
from bodo.utils.utils import alloc_arr_tup, debug_prints, is_null_pointer
join_gen_cond_cfunc = {}
join_gen_cond_cfunc_addr = {}


@intrinsic
def add_join_gen_cond_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        tyum__olau = func.signature
        vdccl__usmer = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        bre__subb = cgutils.get_or_insert_function(builder.module,
            vdccl__usmer, sym._literal_value)
        builder.call(bre__subb, [context.get_constant_null(tyum__olau.args[
            0]), context.get_constant_null(tyum__olau.args[1]), context.
            get_constant_null(tyum__olau.args[2]), context.
            get_constant_null(tyum__olau.args[3]), context.
            get_constant_null(tyum__olau.args[4]), context.
            get_constant_null(tyum__olau.args[5]), context.get_constant(
            types.int64, 0), context.get_constant(types.int64, 0)])
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


class Join(ir.Stmt):

    def __init__(self, df_out, left_df, right_df, left_keys, right_keys,
        out_data_vars, left_vars, right_vars, how, suffix_x, suffix_y, loc,
        is_left, is_right, is_join, left_index, right_index, indicator,
        is_na_equal, gen_cond_expr):
        self.df_out = df_out
        self.left_df = left_df
        self.right_df = right_df
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.out_data_vars = out_data_vars
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.suffix_x = suffix_x
        self.suffix_y = suffix_y
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator = indicator
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        self.left_cond_cols = set(owgig__erylq for owgig__erylq in
            left_vars.keys() if f'(left.{owgig__erylq})' in gen_cond_expr)
        self.right_cond_cols = set(owgig__erylq for owgig__erylq in
            right_vars.keys() if f'(right.{owgig__erylq})' in gen_cond_expr)
        jnss__hjah = set(left_keys) & set(right_keys)
        qlezu__xuft = set(left_vars.keys()) & set(right_vars.keys())
        qvv__pryeu = qlezu__xuft - jnss__hjah
        vect_same_key = []
        n_keys = len(left_keys)
        for wgyk__cabpi in range(n_keys):
            mhf__bhpu = left_keys[wgyk__cabpi]
            otvvz__swux = right_keys[wgyk__cabpi]
            vect_same_key.append(mhf__bhpu == otvvz__swux)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(owgig__erylq) + suffix_x if 
            owgig__erylq in qvv__pryeu else owgig__erylq): ('left',
            owgig__erylq) for owgig__erylq in left_vars.keys()}
        self.column_origins.update({(str(owgig__erylq) + suffix_y if 
            owgig__erylq in qvv__pryeu else owgig__erylq): ('right',
            owgig__erylq) for owgig__erylq in right_vars.keys()})
        if '$_bodo_index_' in qvv__pryeu:
            qvv__pryeu.remove('$_bodo_index_')
        self.add_suffix = qvv__pryeu

    def __repr__(self):
        vbm__aytis = ''
        for owgig__erylq, itg__omak in self.out_data_vars.items():
            vbm__aytis += "'{}':{}, ".format(owgig__erylq, itg__omak.name)
        vrjd__agtk = '{}{{{}}}'.format(self.df_out, vbm__aytis)
        hdzof__sjj = ''
        for owgig__erylq, itg__omak in self.left_vars.items():
            hdzof__sjj += "'{}':{}, ".format(owgig__erylq, itg__omak.name)
        rcyrx__cvhn = '{}{{{}}}'.format(self.left_df, hdzof__sjj)
        hdzof__sjj = ''
        for owgig__erylq, itg__omak in self.right_vars.items():
            hdzof__sjj += "'{}':{}, ".format(owgig__erylq, itg__omak.name)
        itgom__aiyj = '{}{{{}}}'.format(self.right_df, hdzof__sjj)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, vrjd__agtk, rcyrx__cvhn, itgom__aiyj)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    slyf__stybq = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    fbb__otjv = []
    kgdw__gnle = list(join_node.left_vars.values())
    for who__bure in kgdw__gnle:
        auvj__irb = typemap[who__bure.name]
        sfkw__trrs = equiv_set.get_shape(who__bure)
        if sfkw__trrs:
            fbb__otjv.append(sfkw__trrs[0])
    if len(fbb__otjv) > 1:
        equiv_set.insert_equiv(*fbb__otjv)
    fbb__otjv = []
    kgdw__gnle = list(join_node.right_vars.values())
    for who__bure in kgdw__gnle:
        auvj__irb = typemap[who__bure.name]
        sfkw__trrs = equiv_set.get_shape(who__bure)
        if sfkw__trrs:
            fbb__otjv.append(sfkw__trrs[0])
    if len(fbb__otjv) > 1:
        equiv_set.insert_equiv(*fbb__otjv)
    fbb__otjv = []
    for who__bure in join_node.out_data_vars.values():
        auvj__irb = typemap[who__bure.name]
        ufn__lxrk = array_analysis._gen_shape_call(equiv_set, who__bure,
            auvj__irb.ndim, None, slyf__stybq)
        equiv_set.insert_equiv(who__bure, ufn__lxrk)
        fbb__otjv.append(ufn__lxrk[0])
        equiv_set.define(who__bure, set())
    if len(fbb__otjv) > 1:
        equiv_set.insert_equiv(*fbb__otjv)
    return [], slyf__stybq


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    vgch__yvh = Distribution.OneD
    xkkq__dtk = Distribution.OneD
    for who__bure in join_node.left_vars.values():
        vgch__yvh = Distribution(min(vgch__yvh.value, array_dists[who__bure
            .name].value))
    for who__bure in join_node.right_vars.values():
        xkkq__dtk = Distribution(min(xkkq__dtk.value, array_dists[who__bure
            .name].value))
    eph__qwv = Distribution.OneD_Var
    for who__bure in join_node.out_data_vars.values():
        if who__bure.name in array_dists:
            eph__qwv = Distribution(min(eph__qwv.value, array_dists[
                who__bure.name].value))
    pqd__sjn = Distribution(min(eph__qwv.value, vgch__yvh.value))
    wjdrd__lqms = Distribution(min(eph__qwv.value, xkkq__dtk.value))
    eph__qwv = Distribution(max(pqd__sjn.value, wjdrd__lqms.value))
    for who__bure in join_node.out_data_vars.values():
        array_dists[who__bure.name] = eph__qwv
    if eph__qwv != Distribution.OneD_Var:
        vgch__yvh = eph__qwv
        xkkq__dtk = eph__qwv
    for who__bure in join_node.left_vars.values():
        array_dists[who__bure.name] = vgch__yvh
    for who__bure in join_node.right_vars.values():
        array_dists[who__bure.name] = xkkq__dtk
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    jnss__hjah = set(join_node.left_keys) & set(join_node.right_keys)
    qlezu__xuft = set(join_node.left_vars.keys()) & set(join_node.
        right_vars.keys())
    qvv__pryeu = qlezu__xuft - jnss__hjah
    for iiio__wnn, dphph__wanjy in join_node.out_data_vars.items():
        if join_node.indicator and iiio__wnn == '_merge':
            continue
        if not iiio__wnn in join_node.column_origins:
            raise BodoError('join(): The variable ' + iiio__wnn +
                ' is absent from the output')
        qamxy__schpy = join_node.column_origins[iiio__wnn]
        if qamxy__schpy[0] == 'left':
            who__bure = join_node.left_vars[qamxy__schpy[1]]
        else:
            who__bure = join_node.right_vars[qamxy__schpy[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=dphph__wanjy
            .name, src=who__bure.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for obuwt__gneki in list(join_node.left_vars.keys()):
        join_node.left_vars[obuwt__gneki] = visit_vars_inner(join_node.
            left_vars[obuwt__gneki], callback, cbdata)
    for obuwt__gneki in list(join_node.right_vars.keys()):
        join_node.right_vars[obuwt__gneki] = visit_vars_inner(join_node.
            right_vars[obuwt__gneki], callback, cbdata)
    for obuwt__gneki in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[obuwt__gneki] = visit_vars_inner(join_node.
            out_data_vars[obuwt__gneki], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    eltu__vkb = []
    tqai__zrqzk = True
    for obuwt__gneki, who__bure in join_node.out_data_vars.items():
        if who__bure.name in lives:
            tqai__zrqzk = False
            continue
        if obuwt__gneki == '$_bodo_index_':
            continue
        if join_node.indicator and obuwt__gneki == '_merge':
            eltu__vkb.append('_merge')
            join_node.indicator = False
            continue
        vop__ohum, tvj__hlxcb = join_node.column_origins[obuwt__gneki]
        if (vop__ohum == 'left' and tvj__hlxcb not in join_node.left_keys and
            tvj__hlxcb not in join_node.left_cond_cols):
            join_node.left_vars.pop(tvj__hlxcb)
            eltu__vkb.append(obuwt__gneki)
        if (vop__ohum == 'right' and tvj__hlxcb not in join_node.right_keys and
            tvj__hlxcb not in join_node.right_cond_cols):
            join_node.right_vars.pop(tvj__hlxcb)
            eltu__vkb.append(obuwt__gneki)
    for cname in eltu__vkb:
        join_node.out_data_vars.pop(cname)
    if tqai__zrqzk:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({itg__omak.name for itg__omak in join_node.left_vars.
        values()})
    use_set.update({itg__omak.name for itg__omak in join_node.right_vars.
        values()})
    def_set.update({itg__omak.name for itg__omak in join_node.out_data_vars
        .values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    cgjsy__iczpl = set(itg__omak.name for itg__omak in join_node.
        out_data_vars.values())
    return set(), cgjsy__iczpl


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for obuwt__gneki in list(join_node.left_vars.keys()):
        join_node.left_vars[obuwt__gneki] = replace_vars_inner(join_node.
            left_vars[obuwt__gneki], var_dict)
    for obuwt__gneki in list(join_node.right_vars.keys()):
        join_node.right_vars[obuwt__gneki] = replace_vars_inner(join_node.
            right_vars[obuwt__gneki], var_dict)
    for obuwt__gneki in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[obuwt__gneki] = replace_vars_inner(join_node
            .out_data_vars[obuwt__gneki], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for who__bure in join_node.out_data_vars.values():
        definitions[who__bure.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    ake__msorh = tuple(join_node.left_vars[owgig__erylq] for owgig__erylq in
        join_node.left_keys)
    dlexp__lkhw = tuple(join_node.right_vars[owgig__erylq] for owgig__erylq in
        join_node.right_keys)
    oebnk__unwo = tuple(join_node.left_vars.keys())
    alpum__noac = tuple(join_node.right_vars.keys())
    ijgok__dlfam = ()
    fgf__eauoa = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        iaquz__oaw = join_node.right_keys[0]
        if iaquz__oaw in oebnk__unwo:
            fgf__eauoa = iaquz__oaw,
            ijgok__dlfam = join_node.right_vars[iaquz__oaw],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        iaquz__oaw = join_node.left_keys[0]
        if iaquz__oaw in alpum__noac:
            fgf__eauoa = iaquz__oaw,
            ijgok__dlfam = join_node.left_vars[iaquz__oaw],
            optional_column = True
    vtpvo__ecogq = tuple(join_node.out_data_vars[cname] for cname in fgf__eauoa
        )
    mjx__iowcr = tuple(itg__omak for wit__xamzt, itg__omak in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if wit__xamzt
         not in join_node.left_keys)
    poqu__ciqm = tuple(itg__omak for wit__xamzt, itg__omak in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if 
        wit__xamzt not in join_node.right_keys)
    ttxl__foezv = (ijgok__dlfam + ake__msorh + dlexp__lkhw + mjx__iowcr +
        poqu__ciqm)
    kttjf__jbtqt = tuple(typemap[itg__omak.name] for itg__omak in ttxl__foezv)
    ucb__ordh = tuple('opti_c' + str(ufjlq__rnih) for ufjlq__rnih in range(
        len(ijgok__dlfam)))
    left_other_names = tuple('t1_c' + str(ufjlq__rnih) for ufjlq__rnih in
        range(len(mjx__iowcr)))
    right_other_names = tuple('t2_c' + str(ufjlq__rnih) for ufjlq__rnih in
        range(len(poqu__ciqm)))
    left_other_types = tuple([typemap[owgig__erylq.name] for owgig__erylq in
        mjx__iowcr])
    right_other_types = tuple([typemap[owgig__erylq.name] for owgig__erylq in
        poqu__ciqm])
    left_key_names = tuple('t1_key' + str(ufjlq__rnih) for ufjlq__rnih in
        range(n_keys))
    right_key_names = tuple('t2_key' + str(ufjlq__rnih) for ufjlq__rnih in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(ucb__ordh[0
        ]) if len(ucb__ordh) == 1 else '', ','.join(left_key_names), ','.
        join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[itg__omak.name] for itg__omak in ake__msorh)
    right_key_types = tuple(typemap[itg__omak.name] for itg__omak in
        dlexp__lkhw)
    for ufjlq__rnih in range(n_keys):
        glbs[f'key_type_{ufjlq__rnih}'] = _match_join_key_types(left_key_types
            [ufjlq__rnih], right_key_types[ufjlq__rnih], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[ufjlq__rnih]}, key_type_{ufjlq__rnih})'
         for ufjlq__rnih in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[ufjlq__rnih]}, key_type_{ufjlq__rnih})'
         for ufjlq__rnih in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    fjtcf__qpwhp = []
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            dyr__vieeo = str(cname) + join_node.suffix_x
        else:
            dyr__vieeo = cname
        assert dyr__vieeo in join_node.out_data_vars
        fjtcf__qpwhp.append(join_node.out_data_vars[dyr__vieeo])
    for ufjlq__rnih, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[ufjlq__rnih] and not join_node.is_join:
            if cname in join_node.add_suffix:
                dyr__vieeo = str(cname) + join_node.suffix_y
            else:
                dyr__vieeo = cname
            assert dyr__vieeo in join_node.out_data_vars
            fjtcf__qpwhp.append(join_node.out_data_vars[dyr__vieeo])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                dyr__vieeo = str(cname) + join_node.suffix_x
            else:
                dyr__vieeo = str(cname) + join_node.suffix_y
        else:
            dyr__vieeo = cname
        return join_node.out_data_vars[dyr__vieeo]
    vsl__illzv = vtpvo__ecogq + tuple(fjtcf__qpwhp)
    vsl__illzv += tuple(_get_out_col_var(wit__xamzt, True) for wit__xamzt,
        itg__omak in sorted(join_node.left_vars.items(), key=lambda a: str(
        a[0])) if wit__xamzt not in join_node.left_keys)
    vsl__illzv += tuple(_get_out_col_var(wit__xamzt, False) for wit__xamzt,
        itg__omak in sorted(join_node.right_vars.items(), key=lambda a: str
        (a[0])) if wit__xamzt not in join_node.right_keys)
    if join_node.indicator:
        vsl__illzv += _get_out_col_var('_merge', False),
    daxml__ksrw = [('t3_c' + str(ufjlq__rnih)) for ufjlq__rnih in range(len
        (vsl__illzv))]
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel
            func_text += """    t2_keys, data_right = parallel_asof_comm(t1_keys, t2_keys, data_right)
"""
        func_text += """    out_t1_keys, out_t2_keys, out_data_left, out_data_right = bodo.ir.join.local_merge_asof(t1_keys, t2_keys, data_left, data_right)
"""
    else:
        func_text += _gen_local_hash_join(optional_column, left_key_names,
            right_key_names, left_key_types, right_key_types,
            left_other_names, right_other_names, left_other_types,
            right_other_types, join_node.vect_same_key, join_node.is_left,
            join_node.is_right, join_node.is_join, left_parallel,
            right_parallel, glbs, [typemap[itg__omak.name] for itg__omak in
            vsl__illzv], join_node.loc, join_node.indicator, join_node.
            is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums)
    if join_node.how == 'asof':
        for ufjlq__rnih in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(ufjlq__rnih
                , ufjlq__rnih)
        for ufjlq__rnih in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                ufjlq__rnih, ufjlq__rnih)
        for ufjlq__rnih in range(n_keys):
            func_text += (
                f'    t1_keys_{ufjlq__rnih} = out_t1_keys[{ufjlq__rnih}]\n')
        for ufjlq__rnih in range(n_keys):
            func_text += (
                f'    t2_keys_{ufjlq__rnih} = out_t2_keys[{ufjlq__rnih}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {daxml__ksrw[idx]} = opti_0\n'
        idx += 1
    for ufjlq__rnih in range(n_keys):
        func_text += f'    {daxml__ksrw[idx]} = t1_keys_{ufjlq__rnih}\n'
        idx += 1
    for ufjlq__rnih in range(n_keys):
        if not join_node.vect_same_key[ufjlq__rnih] and not join_node.is_join:
            func_text += f'    {daxml__ksrw[idx]} = t2_keys_{ufjlq__rnih}\n'
            idx += 1
    for ufjlq__rnih in range(len(left_other_names)):
        func_text += f'    {daxml__ksrw[idx]} = left_{ufjlq__rnih}\n'
        idx += 1
    for ufjlq__rnih in range(len(right_other_names)):
        func_text += f'    {daxml__ksrw[idx]} = right_{ufjlq__rnih}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {daxml__ksrw[idx]} = indicator_col\n'
        idx += 1
    cjm__eny = {}
    exec(func_text, {}, cjm__eny)
    vdg__band = cjm__eny['f']
    glbs.update({'bodo': bodo, 'np': np, 'pd': pd,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'parallel_asof_comm':
        parallel_asof_comm, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'hash_join_table':
        hash_join_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'add_join_gen_cond_cfunc_sym': add_join_gen_cond_cfunc_sym,
        'get_join_cond_addr': get_join_cond_addr})
    if general_cond_cfunc:
        glbs.update({'general_cond_cfunc': general_cond_cfunc})
    ick__iwo = compile_to_numba_ir(vdg__band, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=kttjf__jbtqt, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(ick__iwo, ttxl__foezv)
    fzf__sduwm = ick__iwo.body[:-3]
    for ufjlq__rnih in range(len(vsl__illzv)):
        fzf__sduwm[-len(vsl__illzv) + ufjlq__rnih].target = vsl__illzv[
            ufjlq__rnih]
    return fzf__sduwm


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    ojxli__hsdd = next_label()
    zil__kjxx = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    fkzsg__vasr = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{ojxli__hsdd}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        zil__kjxx, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        fkzsg__vasr, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    cjm__eny = {}
    exec(func_text, table_getitem_funcs, cjm__eny)
    funp__oljg = cjm__eny[f'bodo_join_gen_cond{ojxli__hsdd}']
    oqm__tgy = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    ngknj__xwbe = numba.cfunc(oqm__tgy, nopython=True)(funp__oljg)
    join_gen_cond_cfunc[ngknj__xwbe.native_name] = ngknj__xwbe
    join_gen_cond_cfunc_addr[ngknj__xwbe.native_name] = ngknj__xwbe.address
    return ngknj__xwbe, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    gzq__objx = []
    for owgig__erylq, jud__xetk in col_to_ind.items():
        cname = f'({table_name}.{owgig__erylq})'
        if cname not in expr:
            continue
        bgqj__ugfb = f'getitem_{table_name}_val_{jud__xetk}'
        ahubi__bzzug = f'_bodo_{table_name}_val_{jud__xetk}'
        bslf__zixki = typemap[col_vars[owgig__erylq].name]
        if is_str_arr_type(bslf__zixki):
            func_text += f"""  {ahubi__bzzug}, {ahubi__bzzug}_size = {bgqj__ugfb}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {ahubi__bzzug} = bodo.libs.str_arr_ext.decode_utf8({ahubi__bzzug}, {ahubi__bzzug}_size)
"""
        else:
            func_text += (
                f'  {ahubi__bzzug} = {bgqj__ugfb}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[bgqj__ugfb
            ] = bodo.libs.array._gen_row_access_intrinsic(bslf__zixki,
            jud__xetk)
        expr = expr.replace(cname, ahubi__bzzug)
        qaw__pjxm = f'({na_check_name}.{table_name}.{owgig__erylq})'
        if qaw__pjxm in expr:
            svk__ajdbp = f'nacheck_{table_name}_val_{jud__xetk}'
            hgqy__spyz = f'_bodo_isna_{table_name}_val_{jud__xetk}'
            if (isinstance(bslf__zixki, bodo.libs.int_arr_ext.
                IntegerArrayType) or bslf__zixki == bodo.libs.bool_arr_ext.
                boolean_array or is_str_arr_type(bslf__zixki)):
                func_text += f"""  {hgqy__spyz} = {svk__ajdbp}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {hgqy__spyz} = {svk__ajdbp}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[svk__ajdbp
                ] = bodo.libs.array._gen_row_na_check_intrinsic(bslf__zixki,
                jud__xetk)
            expr = expr.replace(qaw__pjxm, hgqy__spyz)
        if jud__xetk >= n_keys:
            gzq__objx.append(jud__xetk)
    return expr, func_text, gzq__objx


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {owgig__erylq: ufjlq__rnih for ufjlq__rnih, owgig__erylq in
        enumerate(key_names)}
    ufjlq__rnih = n_keys
    for owgig__erylq in sorted(col_vars, key=lambda a: str(a)):
        if owgig__erylq in key_names:
            continue
        col_to_ind[owgig__erylq] = ufjlq__rnih
        ufjlq__rnih += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as ezp__pmkab:
        if is_str_arr_type(t1) and is_str_arr_type(t2):
            return bodo.string_array_type
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    kmv__jfqd = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[itg__omak.name] in kmv__jfqd for
        itg__omak in join_node.left_vars.values())
    right_parallel = all(array_dists[itg__omak.name] in kmv__jfqd for
        itg__omak in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[itg__omak.name] in kmv__jfqd for
            itg__omak in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[itg__omak.name] in kmv__jfqd for
            itg__omak in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[itg__omak.name] in kmv__jfqd for itg__omak in
            join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    orl__xzr = []
    for ufjlq__rnih in range(len(left_key_names)):
        qzhs__lztr = _match_join_key_types(left_key_types[ufjlq__rnih],
            right_key_types[ufjlq__rnih], loc)
        orl__xzr.append(needs_typechange(qzhs__lztr, is_right,
            vect_same_key[ufjlq__rnih]))
    for ufjlq__rnih in range(len(left_other_names)):
        orl__xzr.append(needs_typechange(left_other_types[ufjlq__rnih],
            is_right, False))
    for ufjlq__rnih in range(len(right_key_names)):
        if not vect_same_key[ufjlq__rnih] and not is_join:
            qzhs__lztr = _match_join_key_types(left_key_types[ufjlq__rnih],
                right_key_types[ufjlq__rnih], loc)
            orl__xzr.append(needs_typechange(qzhs__lztr, is_left, False))
    for ufjlq__rnih in range(len(right_other_names)):
        orl__xzr.append(needs_typechange(right_other_types[ufjlq__rnih],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                jmd__wxwrf = IntDtype(in_type.dtype).name
                assert jmd__wxwrf.endswith('Dtype()')
                jmd__wxwrf = jmd__wxwrf[:-7]
                qiv__bcy = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{jmd__wxwrf}"))
"""
                hdv__inwk = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                qiv__bcy = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                hdv__inwk = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            qiv__bcy = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            hdv__inwk = f'typ_{idx}'
        else:
            qiv__bcy = ''
            hdv__inwk = in_name
        return qiv__bcy, hdv__inwk
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    ewklk__ukwu = []
    for ufjlq__rnih in range(n_keys):
        ewklk__ukwu.append('t1_keys[{}]'.format(ufjlq__rnih))
    for ufjlq__rnih in range(len(left_other_names)):
        ewklk__ukwu.append('data_left[{}]'.format(ufjlq__rnih))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in ewklk__ukwu))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    ecy__vrpie = []
    for ufjlq__rnih in range(n_keys):
        ecy__vrpie.append('t2_keys[{}]'.format(ufjlq__rnih))
    for ufjlq__rnih in range(len(right_other_names)):
        ecy__vrpie.append('data_right[{}]'.format(ufjlq__rnih))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in ecy__vrpie))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        wbk__shmsu else '0' for wbk__shmsu in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if wbk__shmsu else '0' for wbk__shmsu in orl__xzr))
    func_text += f"""    left_table_cond_columns = np.array({left_col_nums if len(left_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    func_text += f"""    right_table_cond_columns = np.array({right_col_nums if len(right_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    if general_cond_cfunc:
        func_text += f"""    cfunc_cond = add_join_gen_cond_cfunc_sym(general_cond_cfunc, '{general_cond_cfunc.native_name}')
"""
        func_text += (
            f"    cfunc_cond = get_join_cond_addr('{general_cond_cfunc.native_name}')\n"
            )
    else:
        func_text += '    cfunc_cond = 0\n'
    func_text += (
        """    out_table = hash_join_table(table_left, table_right, {}, {}, {}, {}, {}, vect_same_key.ctypes, vect_need_typechange.ctypes, {}, {}, {}, {}, {}, {}, cfunc_cond, left_table_cond_columns.ctypes, {}, right_table_cond_columns.ctypes, {})
"""
        .format(left_parallel, right_parallel, n_keys, len(left_other_names
        ), len(right_other_names), is_left, is_right, is_join,
        optional_column, indicator, is_na_equal, len(left_col_nums), len(
        right_col_nums)))
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    idx = 0
    if optional_column:
        ksa__atgh = get_out_type(idx, out_types[idx], 'opti_c0', False, False)
        func_text += ksa__atgh[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {ksa__atgh[1]})
"""
        idx += 1
    for ufjlq__rnih, pxrt__tbef in enumerate(left_key_names):
        qzhs__lztr = _match_join_key_types(left_key_types[ufjlq__rnih],
            right_key_types[ufjlq__rnih], loc)
        ksa__atgh = get_out_type(idx, qzhs__lztr, f't1_keys[{ufjlq__rnih}]',
            is_right, vect_same_key[ufjlq__rnih])
        func_text += ksa__atgh[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        if qzhs__lztr != left_key_types[ufjlq__rnih] and left_key_types[
            ufjlq__rnih] != bodo.dict_str_arr_type:
            func_text += f"""    t1_keys_{ufjlq__rnih} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {ksa__atgh[1]}), out_type_{idx})
"""
        else:
            func_text += f"""    t1_keys_{ufjlq__rnih} = info_to_array(info_from_table(out_table, {idx}), {ksa__atgh[1]})
"""
        idx += 1
    for ufjlq__rnih, pxrt__tbef in enumerate(left_other_names):
        ksa__atgh = get_out_type(idx, left_other_types[ufjlq__rnih],
            pxrt__tbef, is_right, False)
        func_text += ksa__atgh[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(ufjlq__rnih, idx, ksa__atgh[1]))
        idx += 1
    for ufjlq__rnih, pxrt__tbef in enumerate(right_key_names):
        if not vect_same_key[ufjlq__rnih] and not is_join:
            qzhs__lztr = _match_join_key_types(left_key_types[ufjlq__rnih],
                right_key_types[ufjlq__rnih], loc)
            ksa__atgh = get_out_type(idx, qzhs__lztr,
                f't2_keys[{ufjlq__rnih}]', is_left, False)
            func_text += ksa__atgh[0]
            glbs[f'out_type_{idx}'] = out_types[idx - len(left_other_names)]
            if qzhs__lztr != right_key_types[ufjlq__rnih] and right_key_types[
                ufjlq__rnih] != bodo.dict_str_arr_type:
                func_text += f"""    t2_keys_{ufjlq__rnih} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {ksa__atgh[1]}), out_type_{idx})
"""
            else:
                func_text += f"""    t2_keys_{ufjlq__rnih} = info_to_array(info_from_table(out_table, {idx}), {ksa__atgh[1]})
"""
            idx += 1
    for ufjlq__rnih, pxrt__tbef in enumerate(right_other_names):
        ksa__atgh = get_out_type(idx, right_other_types[ufjlq__rnih],
            pxrt__tbef, is_left, False)
        func_text += ksa__atgh[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(ufjlq__rnih, idx, ksa__atgh[1]))
        idx += 1
    if indicator:
        func_text += f"""    typ_{idx} = pd.Categorical(values=['both'], categories=('left_only', 'right_only', 'both'))
"""
        func_text += f"""    indicator_col = info_to_array(info_from_table(out_table, {idx}), typ_{idx})
"""
        idx += 1
    func_text += '    delete_table(out_table)\n'
    return func_text


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    gcqx__xjz = bodo.libs.distributed_api.get_size()
    ofw__alcpn = np.empty(gcqx__xjz, left_key_arrs[0].dtype)
    jfnqj__zqch = np.empty(gcqx__xjz, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(ofw__alcpn, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(jfnqj__zqch, left_key_arrs[0][-1])
    ehya__lfnd = np.zeros(gcqx__xjz, np.int32)
    glph__fql = np.zeros(gcqx__xjz, np.int32)
    kyop__cghb = np.zeros(gcqx__xjz, np.int32)
    hmy__uzyd = right_key_arrs[0][0]
    wws__fiyxz = right_key_arrs[0][-1]
    dmcqb__wxxuu = -1
    ufjlq__rnih = 0
    while ufjlq__rnih < gcqx__xjz - 1 and jfnqj__zqch[ufjlq__rnih] < hmy__uzyd:
        ufjlq__rnih += 1
    while ufjlq__rnih < gcqx__xjz and ofw__alcpn[ufjlq__rnih] <= wws__fiyxz:
        dmcqb__wxxuu, imo__ifj = _count_overlap(right_key_arrs[0],
            ofw__alcpn[ufjlq__rnih], jfnqj__zqch[ufjlq__rnih])
        if dmcqb__wxxuu != 0:
            dmcqb__wxxuu -= 1
            imo__ifj += 1
        ehya__lfnd[ufjlq__rnih] = imo__ifj
        glph__fql[ufjlq__rnih] = dmcqb__wxxuu
        ufjlq__rnih += 1
    while ufjlq__rnih < gcqx__xjz:
        ehya__lfnd[ufjlq__rnih] = 1
        glph__fql[ufjlq__rnih] = len(right_key_arrs[0]) - 1
        ufjlq__rnih += 1
    bodo.libs.distributed_api.alltoall(ehya__lfnd, kyop__cghb, 1)
    hxcjd__rhm = kyop__cghb.sum()
    twl__wrzqu = np.empty(hxcjd__rhm, right_key_arrs[0].dtype)
    tkxoz__ppt = alloc_arr_tup(hxcjd__rhm, right_data)
    xowa__nfv = bodo.ir.join.calc_disp(kyop__cghb)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], twl__wrzqu,
        ehya__lfnd, kyop__cghb, glph__fql, xowa__nfv)
    bodo.libs.distributed_api.alltoallv_tup(right_data, tkxoz__ppt,
        ehya__lfnd, kyop__cghb, glph__fql, xowa__nfv)
    return (twl__wrzqu,), tkxoz__ppt


@numba.njit
def _count_overlap(r_key_arr, start, end):
    imo__ifj = 0
    dmcqb__wxxuu = 0
    yek__use = 0
    while yek__use < len(r_key_arr) and r_key_arr[yek__use] < start:
        dmcqb__wxxuu += 1
        yek__use += 1
    while yek__use < len(r_key_arr) and start <= r_key_arr[yek__use] <= end:
        yek__use += 1
        imo__ifj += 1
    return dmcqb__wxxuu, imo__ifj


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    aldmt__bfy = np.empty_like(arr)
    aldmt__bfy[0] = 0
    for ufjlq__rnih in range(1, len(arr)):
        aldmt__bfy[ufjlq__rnih] = aldmt__bfy[ufjlq__rnih - 1] + arr[
            ufjlq__rnih - 1]
    return aldmt__bfy


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    svsio__ogo = len(left_keys[0])
    awye__lsxfi = len(right_keys[0])
    dgxl__ojkxi = alloc_arr_tup(svsio__ogo, left_keys)
    vvrs__rqblr = alloc_arr_tup(svsio__ogo, right_keys)
    oetj__ntkfd = alloc_arr_tup(svsio__ogo, data_left)
    extz__swhga = alloc_arr_tup(svsio__ogo, data_right)
    tizen__qwdbb = 0
    wbfg__lyqox = 0
    for tizen__qwdbb in range(svsio__ogo):
        if wbfg__lyqox < 0:
            wbfg__lyqox = 0
        while wbfg__lyqox < awye__lsxfi and getitem_arr_tup(right_keys,
            wbfg__lyqox) <= getitem_arr_tup(left_keys, tizen__qwdbb):
            wbfg__lyqox += 1
        wbfg__lyqox -= 1
        setitem_arr_tup(dgxl__ojkxi, tizen__qwdbb, getitem_arr_tup(
            left_keys, tizen__qwdbb))
        setitem_arr_tup(oetj__ntkfd, tizen__qwdbb, getitem_arr_tup(
            data_left, tizen__qwdbb))
        if wbfg__lyqox >= 0:
            setitem_arr_tup(vvrs__rqblr, tizen__qwdbb, getitem_arr_tup(
                right_keys, wbfg__lyqox))
            setitem_arr_tup(extz__swhga, tizen__qwdbb, getitem_arr_tup(
                data_right, wbfg__lyqox))
        else:
            bodo.libs.array_kernels.setna_tup(vvrs__rqblr, tizen__qwdbb)
            bodo.libs.array_kernels.setna_tup(extz__swhga, tizen__qwdbb)
    return dgxl__ojkxi, vvrs__rqblr, oetj__ntkfd, extz__swhga


def copy_arr_tup(arrs):
    return tuple(a.copy() for a in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    imo__ifj = arrs.count
    func_text = 'def f(arrs):\n'
    func_text += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(ufjlq__rnih) for ufjlq__rnih in range(imo__ifj)))
    cjm__eny = {}
    exec(func_text, {}, cjm__eny)
    chgy__fbo = cjm__eny['f']
    return chgy__fbo
