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
        rzcg__dughz = func.signature
        rstri__byxg = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        udeqk__ema = cgutils.get_or_insert_function(builder.module,
            rstri__byxg, sym._literal_value)
        builder.call(udeqk__ema, [context.get_constant_null(rzcg__dughz.
            args[0]), context.get_constant_null(rzcg__dughz.args[1]),
            context.get_constant_null(rzcg__dughz.args[2]), context.
            get_constant_null(rzcg__dughz.args[3]), context.
            get_constant_null(rzcg__dughz.args[4]), context.
            get_constant_null(rzcg__dughz.args[5]), context.get_constant(
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
        self.left_cond_cols = set(rgny__qrez for rgny__qrez in left_vars.
            keys() if f'(left.{rgny__qrez})' in gen_cond_expr)
        self.right_cond_cols = set(rgny__qrez for rgny__qrez in right_vars.
            keys() if f'(right.{rgny__qrez})' in gen_cond_expr)
        xhmqh__ojwbj = set(left_keys) & set(right_keys)
        fmvhd__mpz = set(left_vars.keys()) & set(right_vars.keys())
        hyua__dfg = fmvhd__mpz - xhmqh__ojwbj
        vect_same_key = []
        n_keys = len(left_keys)
        for wpndu__evmce in range(n_keys):
            cmb__otd = left_keys[wpndu__evmce]
            wsrp__zjmw = right_keys[wpndu__evmce]
            vect_same_key.append(cmb__otd == wsrp__zjmw)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(rgny__qrez) + suffix_x if rgny__qrez in
            hyua__dfg else rgny__qrez): ('left', rgny__qrez) for rgny__qrez in
            left_vars.keys()}
        self.column_origins.update({(str(rgny__qrez) + suffix_y if 
            rgny__qrez in hyua__dfg else rgny__qrez): ('right', rgny__qrez) for
            rgny__qrez in right_vars.keys()})
        if '$_bodo_index_' in hyua__dfg:
            hyua__dfg.remove('$_bodo_index_')
        self.add_suffix = hyua__dfg

    def __repr__(self):
        mosc__xiqyn = ''
        for rgny__qrez, zjy__vsl in self.out_data_vars.items():
            mosc__xiqyn += "'{}':{}, ".format(rgny__qrez, zjy__vsl.name)
        bdn__zoidr = '{}{{{}}}'.format(self.df_out, mosc__xiqyn)
        zlzhq__fcxc = ''
        for rgny__qrez, zjy__vsl in self.left_vars.items():
            zlzhq__fcxc += "'{}':{}, ".format(rgny__qrez, zjy__vsl.name)
        fanp__mqjej = '{}{{{}}}'.format(self.left_df, zlzhq__fcxc)
        zlzhq__fcxc = ''
        for rgny__qrez, zjy__vsl in self.right_vars.items():
            zlzhq__fcxc += "'{}':{}, ".format(rgny__qrez, zjy__vsl.name)
        vjfie__adw = '{}{{{}}}'.format(self.right_df, zlzhq__fcxc)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, bdn__zoidr, fanp__mqjej, vjfie__adw)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    oewn__zuxnn = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    rla__org = []
    bii__gsk = list(join_node.left_vars.values())
    for btsd__pzyly in bii__gsk:
        iqzap__jhk = typemap[btsd__pzyly.name]
        jhv__hmxxd = equiv_set.get_shape(btsd__pzyly)
        if jhv__hmxxd:
            rla__org.append(jhv__hmxxd[0])
    if len(rla__org) > 1:
        equiv_set.insert_equiv(*rla__org)
    rla__org = []
    bii__gsk = list(join_node.right_vars.values())
    for btsd__pzyly in bii__gsk:
        iqzap__jhk = typemap[btsd__pzyly.name]
        jhv__hmxxd = equiv_set.get_shape(btsd__pzyly)
        if jhv__hmxxd:
            rla__org.append(jhv__hmxxd[0])
    if len(rla__org) > 1:
        equiv_set.insert_equiv(*rla__org)
    rla__org = []
    for btsd__pzyly in join_node.out_data_vars.values():
        iqzap__jhk = typemap[btsd__pzyly.name]
        mzevv__cpebm = array_analysis._gen_shape_call(equiv_set,
            btsd__pzyly, iqzap__jhk.ndim, None, oewn__zuxnn)
        equiv_set.insert_equiv(btsd__pzyly, mzevv__cpebm)
        rla__org.append(mzevv__cpebm[0])
        equiv_set.define(btsd__pzyly, set())
    if len(rla__org) > 1:
        equiv_set.insert_equiv(*rla__org)
    return [], oewn__zuxnn


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    iiz__xfner = Distribution.OneD
    chnqu__zdc = Distribution.OneD
    for btsd__pzyly in join_node.left_vars.values():
        iiz__xfner = Distribution(min(iiz__xfner.value, array_dists[
            btsd__pzyly.name].value))
    for btsd__pzyly in join_node.right_vars.values():
        chnqu__zdc = Distribution(min(chnqu__zdc.value, array_dists[
            btsd__pzyly.name].value))
    qllul__jpy = Distribution.OneD_Var
    for btsd__pzyly in join_node.out_data_vars.values():
        if btsd__pzyly.name in array_dists:
            qllul__jpy = Distribution(min(qllul__jpy.value, array_dists[
                btsd__pzyly.name].value))
    ptv__aps = Distribution(min(qllul__jpy.value, iiz__xfner.value))
    upsh__nobe = Distribution(min(qllul__jpy.value, chnqu__zdc.value))
    qllul__jpy = Distribution(max(ptv__aps.value, upsh__nobe.value))
    for btsd__pzyly in join_node.out_data_vars.values():
        array_dists[btsd__pzyly.name] = qllul__jpy
    if qllul__jpy != Distribution.OneD_Var:
        iiz__xfner = qllul__jpy
        chnqu__zdc = qllul__jpy
    for btsd__pzyly in join_node.left_vars.values():
        array_dists[btsd__pzyly.name] = iiz__xfner
    for btsd__pzyly in join_node.right_vars.values():
        array_dists[btsd__pzyly.name] = chnqu__zdc
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    xhmqh__ojwbj = set(join_node.left_keys) & set(join_node.right_keys)
    fmvhd__mpz = set(join_node.left_vars.keys()) & set(join_node.right_vars
        .keys())
    hyua__dfg = fmvhd__mpz - xhmqh__ojwbj
    for heo__ftdzu, oux__ihxif in join_node.out_data_vars.items():
        if join_node.indicator and heo__ftdzu == '_merge':
            continue
        if not heo__ftdzu in join_node.column_origins:
            raise BodoError('join(): The variable ' + heo__ftdzu +
                ' is absent from the output')
        gcrg__nltnj = join_node.column_origins[heo__ftdzu]
        if gcrg__nltnj[0] == 'left':
            btsd__pzyly = join_node.left_vars[gcrg__nltnj[1]]
        else:
            btsd__pzyly = join_node.right_vars[gcrg__nltnj[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=oux__ihxif.
            name, src=btsd__pzyly.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for dxrfl__wrxmj in list(join_node.left_vars.keys()):
        join_node.left_vars[dxrfl__wrxmj] = visit_vars_inner(join_node.
            left_vars[dxrfl__wrxmj], callback, cbdata)
    for dxrfl__wrxmj in list(join_node.right_vars.keys()):
        join_node.right_vars[dxrfl__wrxmj] = visit_vars_inner(join_node.
            right_vars[dxrfl__wrxmj], callback, cbdata)
    for dxrfl__wrxmj in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[dxrfl__wrxmj] = visit_vars_inner(join_node.
            out_data_vars[dxrfl__wrxmj], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    ulo__vpx = []
    chmnr__cvud = True
    for dxrfl__wrxmj, btsd__pzyly in join_node.out_data_vars.items():
        if btsd__pzyly.name in lives:
            chmnr__cvud = False
            continue
        if dxrfl__wrxmj == '$_bodo_index_':
            continue
        if join_node.indicator and dxrfl__wrxmj == '_merge':
            ulo__vpx.append('_merge')
            join_node.indicator = False
            continue
        tme__pxoxh, hqk__zlryg = join_node.column_origins[dxrfl__wrxmj]
        if (tme__pxoxh == 'left' and hqk__zlryg not in join_node.left_keys and
            hqk__zlryg not in join_node.left_cond_cols):
            join_node.left_vars.pop(hqk__zlryg)
            ulo__vpx.append(dxrfl__wrxmj)
        if (tme__pxoxh == 'right' and hqk__zlryg not in join_node.
            right_keys and hqk__zlryg not in join_node.right_cond_cols):
            join_node.right_vars.pop(hqk__zlryg)
            ulo__vpx.append(dxrfl__wrxmj)
    for cname in ulo__vpx:
        join_node.out_data_vars.pop(cname)
    if chmnr__cvud:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({zjy__vsl.name for zjy__vsl in join_node.left_vars.values()}
        )
    use_set.update({zjy__vsl.name for zjy__vsl in join_node.right_vars.
        values()})
    def_set.update({zjy__vsl.name for zjy__vsl in join_node.out_data_vars.
        values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    egwj__cvc = set(zjy__vsl.name for zjy__vsl in join_node.out_data_vars.
        values())
    return set(), egwj__cvc


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for dxrfl__wrxmj in list(join_node.left_vars.keys()):
        join_node.left_vars[dxrfl__wrxmj] = replace_vars_inner(join_node.
            left_vars[dxrfl__wrxmj], var_dict)
    for dxrfl__wrxmj in list(join_node.right_vars.keys()):
        join_node.right_vars[dxrfl__wrxmj] = replace_vars_inner(join_node.
            right_vars[dxrfl__wrxmj], var_dict)
    for dxrfl__wrxmj in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[dxrfl__wrxmj] = replace_vars_inner(join_node
            .out_data_vars[dxrfl__wrxmj], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for btsd__pzyly in join_node.out_data_vars.values():
        definitions[btsd__pzyly.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    rokaw__vblvd = tuple(join_node.left_vars[rgny__qrez] for rgny__qrez in
        join_node.left_keys)
    socz__abkhi = tuple(join_node.right_vars[rgny__qrez] for rgny__qrez in
        join_node.right_keys)
    xbqk__spfen = tuple(join_node.left_vars.keys())
    xcsc__jym = tuple(join_node.right_vars.keys())
    xup__svst = ()
    aru__bnhb = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        wsdh__dxg = join_node.right_keys[0]
        if wsdh__dxg in xbqk__spfen:
            aru__bnhb = wsdh__dxg,
            xup__svst = join_node.right_vars[wsdh__dxg],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        wsdh__dxg = join_node.left_keys[0]
        if wsdh__dxg in xcsc__jym:
            aru__bnhb = wsdh__dxg,
            xup__svst = join_node.left_vars[wsdh__dxg],
            optional_column = True
    nodxu__jwi = tuple(join_node.out_data_vars[cname] for cname in aru__bnhb)
    tyuf__fbjoy = tuple(zjy__vsl for lhpf__ccrug, zjy__vsl in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if 
        lhpf__ccrug not in join_node.left_keys)
    atfl__xsl = tuple(zjy__vsl for lhpf__ccrug, zjy__vsl in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if 
        lhpf__ccrug not in join_node.right_keys)
    vyki__gno = (xup__svst + rokaw__vblvd + socz__abkhi + tyuf__fbjoy +
        atfl__xsl)
    kghzj__lbwah = tuple(typemap[zjy__vsl.name] for zjy__vsl in vyki__gno)
    vma__zcm = tuple('opti_c' + str(uxd__iypo) for uxd__iypo in range(len(
        xup__svst)))
    left_other_names = tuple('t1_c' + str(uxd__iypo) for uxd__iypo in range
        (len(tyuf__fbjoy)))
    right_other_names = tuple('t2_c' + str(uxd__iypo) for uxd__iypo in
        range(len(atfl__xsl)))
    left_other_types = tuple([typemap[rgny__qrez.name] for rgny__qrez in
        tyuf__fbjoy])
    right_other_types = tuple([typemap[rgny__qrez.name] for rgny__qrez in
        atfl__xsl])
    left_key_names = tuple('t1_key' + str(uxd__iypo) for uxd__iypo in range
        (n_keys))
    right_key_names = tuple('t2_key' + str(uxd__iypo) for uxd__iypo in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(vma__zcm[0]
        ) if len(vma__zcm) == 1 else '', ','.join(left_key_names), ','.join
        (right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[zjy__vsl.name] for zjy__vsl in rokaw__vblvd)
    right_key_types = tuple(typemap[zjy__vsl.name] for zjy__vsl in socz__abkhi)
    for uxd__iypo in range(n_keys):
        glbs[f'key_type_{uxd__iypo}'] = _match_join_key_types(left_key_types
            [uxd__iypo], right_key_types[uxd__iypo], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[uxd__iypo]}, key_type_{uxd__iypo})'
         for uxd__iypo in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[uxd__iypo]}, key_type_{uxd__iypo})'
         for uxd__iypo in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    xmgt__tgcea = []
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            chfu__sicde = str(cname) + join_node.suffix_x
        else:
            chfu__sicde = cname
        assert chfu__sicde in join_node.out_data_vars
        xmgt__tgcea.append(join_node.out_data_vars[chfu__sicde])
    for uxd__iypo, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[uxd__iypo] and not join_node.is_join:
            if cname in join_node.add_suffix:
                chfu__sicde = str(cname) + join_node.suffix_y
            else:
                chfu__sicde = cname
            assert chfu__sicde in join_node.out_data_vars
            xmgt__tgcea.append(join_node.out_data_vars[chfu__sicde])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                chfu__sicde = str(cname) + join_node.suffix_x
            else:
                chfu__sicde = str(cname) + join_node.suffix_y
        else:
            chfu__sicde = cname
        return join_node.out_data_vars[chfu__sicde]
    ntraj__kfcz = nodxu__jwi + tuple(xmgt__tgcea)
    ntraj__kfcz += tuple(_get_out_col_var(lhpf__ccrug, True) for 
        lhpf__ccrug, zjy__vsl in sorted(join_node.left_vars.items(), key=lambda
        a: str(a[0])) if lhpf__ccrug not in join_node.left_keys)
    ntraj__kfcz += tuple(_get_out_col_var(lhpf__ccrug, False) for 
        lhpf__ccrug, zjy__vsl in sorted(join_node.right_vars.items(), key=
        lambda a: str(a[0])) if lhpf__ccrug not in join_node.right_keys)
    if join_node.indicator:
        ntraj__kfcz += _get_out_col_var('_merge', False),
    kjjqn__wow = [('t3_c' + str(uxd__iypo)) for uxd__iypo in range(len(
        ntraj__kfcz))]
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
            right_parallel, glbs, [typemap[zjy__vsl.name] for zjy__vsl in
            ntraj__kfcz], join_node.loc, join_node.indicator, join_node.
            is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums)
    if join_node.how == 'asof':
        for uxd__iypo in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(uxd__iypo,
                uxd__iypo)
        for uxd__iypo in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(uxd__iypo
                , uxd__iypo)
        for uxd__iypo in range(n_keys):
            func_text += (
                f'    t1_keys_{uxd__iypo} = out_t1_keys[{uxd__iypo}]\n')
        for uxd__iypo in range(n_keys):
            func_text += (
                f'    t2_keys_{uxd__iypo} = out_t2_keys[{uxd__iypo}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {kjjqn__wow[idx]} = opti_0\n'
        idx += 1
    for uxd__iypo in range(n_keys):
        func_text += f'    {kjjqn__wow[idx]} = t1_keys_{uxd__iypo}\n'
        idx += 1
    for uxd__iypo in range(n_keys):
        if not join_node.vect_same_key[uxd__iypo] and not join_node.is_join:
            func_text += f'    {kjjqn__wow[idx]} = t2_keys_{uxd__iypo}\n'
            idx += 1
    for uxd__iypo in range(len(left_other_names)):
        func_text += f'    {kjjqn__wow[idx]} = left_{uxd__iypo}\n'
        idx += 1
    for uxd__iypo in range(len(right_other_names)):
        func_text += f'    {kjjqn__wow[idx]} = right_{uxd__iypo}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {kjjqn__wow[idx]} = indicator_col\n'
        idx += 1
    vch__lhsk = {}
    exec(func_text, {}, vch__lhsk)
    jxnk__ljl = vch__lhsk['f']
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
    puajo__fio = compile_to_numba_ir(jxnk__ljl, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=kghzj__lbwah, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(puajo__fio, vyki__gno)
    qhb__rcl = puajo__fio.body[:-3]
    for uxd__iypo in range(len(ntraj__kfcz)):
        qhb__rcl[-len(ntraj__kfcz) + uxd__iypo].target = ntraj__kfcz[uxd__iypo]
    return qhb__rcl


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    obo__pozto = next_label()
    caguq__rrrbz = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    kan__qci = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{obo__pozto}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        caguq__rrrbz, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        kan__qci, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    vch__lhsk = {}
    exec(func_text, table_getitem_funcs, vch__lhsk)
    ifzj__bxr = vch__lhsk[f'bodo_join_gen_cond{obo__pozto}']
    ftn__tgsq = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    sws__ugrmj = numba.cfunc(ftn__tgsq, nopython=True)(ifzj__bxr)
    join_gen_cond_cfunc[sws__ugrmj.native_name] = sws__ugrmj
    join_gen_cond_cfunc_addr[sws__ugrmj.native_name] = sws__ugrmj.address
    return sws__ugrmj, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    uek__sfbf = []
    for rgny__qrez, skhu__btbq in col_to_ind.items():
        cname = f'({table_name}.{rgny__qrez})'
        if cname not in expr:
            continue
        rph__gtc = f'getitem_{table_name}_val_{skhu__btbq}'
        uqzoc__kiz = f'_bodo_{table_name}_val_{skhu__btbq}'
        riuq__nnn = typemap[col_vars[rgny__qrez].name]
        if is_str_arr_type(riuq__nnn):
            func_text += f"""  {uqzoc__kiz}, {uqzoc__kiz}_size = {rph__gtc}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {uqzoc__kiz} = bodo.libs.str_arr_ext.decode_utf8({uqzoc__kiz}, {uqzoc__kiz}_size)
"""
        else:
            func_text += (
                f'  {uqzoc__kiz} = {rph__gtc}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[rph__gtc
            ] = bodo.libs.array._gen_row_access_intrinsic(riuq__nnn, skhu__btbq
            )
        expr = expr.replace(cname, uqzoc__kiz)
        dju__xccmn = f'({na_check_name}.{table_name}.{rgny__qrez})'
        if dju__xccmn in expr:
            gnd__yqjv = f'nacheck_{table_name}_val_{skhu__btbq}'
            eezr__pca = f'_bodo_isna_{table_name}_val_{skhu__btbq}'
            if (isinstance(riuq__nnn, bodo.libs.int_arr_ext.
                IntegerArrayType) or riuq__nnn == bodo.libs.bool_arr_ext.
                boolean_array or is_str_arr_type(riuq__nnn)):
                func_text += f"""  {eezr__pca} = {gnd__yqjv}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {eezr__pca} = {gnd__yqjv}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[gnd__yqjv
                ] = bodo.libs.array._gen_row_na_check_intrinsic(riuq__nnn,
                skhu__btbq)
            expr = expr.replace(dju__xccmn, eezr__pca)
        if skhu__btbq >= n_keys:
            uek__sfbf.append(skhu__btbq)
    return expr, func_text, uek__sfbf


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {rgny__qrez: uxd__iypo for uxd__iypo, rgny__qrez in
        enumerate(key_names)}
    uxd__iypo = n_keys
    for rgny__qrez in sorted(col_vars, key=lambda a: str(a)):
        if rgny__qrez in key_names:
            continue
        col_to_ind[rgny__qrez] = uxd__iypo
        uxd__iypo += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as dewz__vmvw:
        if is_str_arr_type(t1) and is_str_arr_type(t2):
            return bodo.string_array_type
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    wjvwr__yhe = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[zjy__vsl.name] in wjvwr__yhe for
        zjy__vsl in join_node.left_vars.values())
    right_parallel = all(array_dists[zjy__vsl.name] in wjvwr__yhe for
        zjy__vsl in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[zjy__vsl.name] in wjvwr__yhe for
            zjy__vsl in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[zjy__vsl.name] in wjvwr__yhe for
            zjy__vsl in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[zjy__vsl.name] in wjvwr__yhe for zjy__vsl in
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
    fup__hxsjm = []
    for uxd__iypo in range(len(left_key_names)):
        dgvz__ohq = _match_join_key_types(left_key_types[uxd__iypo],
            right_key_types[uxd__iypo], loc)
        fup__hxsjm.append(needs_typechange(dgvz__ohq, is_right,
            vect_same_key[uxd__iypo]))
    for uxd__iypo in range(len(left_other_names)):
        fup__hxsjm.append(needs_typechange(left_other_types[uxd__iypo],
            is_right, False))
    for uxd__iypo in range(len(right_key_names)):
        if not vect_same_key[uxd__iypo] and not is_join:
            dgvz__ohq = _match_join_key_types(left_key_types[uxd__iypo],
                right_key_types[uxd__iypo], loc)
            fup__hxsjm.append(needs_typechange(dgvz__ohq, is_left, False))
    for uxd__iypo in range(len(right_other_names)):
        fup__hxsjm.append(needs_typechange(right_other_types[uxd__iypo],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                mcj__zaiw = IntDtype(in_type.dtype).name
                assert mcj__zaiw.endswith('Dtype()')
                mcj__zaiw = mcj__zaiw[:-7]
                uxat__gppf = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{mcj__zaiw}"))
"""
                ixpn__hwa = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                uxat__gppf = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                ixpn__hwa = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            uxat__gppf = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            ixpn__hwa = f'typ_{idx}'
        else:
            uxat__gppf = ''
            ixpn__hwa = in_name
        return uxat__gppf, ixpn__hwa
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    lyz__lvubi = []
    for uxd__iypo in range(n_keys):
        lyz__lvubi.append('t1_keys[{}]'.format(uxd__iypo))
    for uxd__iypo in range(len(left_other_names)):
        lyz__lvubi.append('data_left[{}]'.format(uxd__iypo))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in lyz__lvubi))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    cirl__fkfof = []
    for uxd__iypo in range(n_keys):
        cirl__fkfof.append('t2_keys[{}]'.format(uxd__iypo))
    for uxd__iypo in range(len(right_other_names)):
        cirl__fkfof.append('data_right[{}]'.format(uxd__iypo))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in cirl__fkfof))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        spqzn__fsnqm else '0' for spqzn__fsnqm in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if spqzn__fsnqm else '0' for spqzn__fsnqm in fup__hxsjm))
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
        wrbum__qhvax = get_out_type(idx, out_types[idx], 'opti_c0', False, 
            False)
        func_text += wrbum__qhvax[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {wrbum__qhvax[1]})
"""
        idx += 1
    for uxd__iypo, ytsk__rspi in enumerate(left_key_names):
        dgvz__ohq = _match_join_key_types(left_key_types[uxd__iypo],
            right_key_types[uxd__iypo], loc)
        wrbum__qhvax = get_out_type(idx, dgvz__ohq, f't1_keys[{uxd__iypo}]',
            is_right, vect_same_key[uxd__iypo])
        func_text += wrbum__qhvax[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        if dgvz__ohq != left_key_types[uxd__iypo] and left_key_types[uxd__iypo
            ] != bodo.dict_str_arr_type:
            func_text += f"""    t1_keys_{uxd__iypo} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {wrbum__qhvax[1]}), out_type_{idx})
"""
        else:
            func_text += f"""    t1_keys_{uxd__iypo} = info_to_array(info_from_table(out_table, {idx}), {wrbum__qhvax[1]})
"""
        idx += 1
    for uxd__iypo, ytsk__rspi in enumerate(left_other_names):
        wrbum__qhvax = get_out_type(idx, left_other_types[uxd__iypo],
            ytsk__rspi, is_right, False)
        func_text += wrbum__qhvax[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(uxd__iypo, idx, wrbum__qhvax[1]))
        idx += 1
    for uxd__iypo, ytsk__rspi in enumerate(right_key_names):
        if not vect_same_key[uxd__iypo] and not is_join:
            dgvz__ohq = _match_join_key_types(left_key_types[uxd__iypo],
                right_key_types[uxd__iypo], loc)
            wrbum__qhvax = get_out_type(idx, dgvz__ohq,
                f't2_keys[{uxd__iypo}]', is_left, False)
            func_text += wrbum__qhvax[0]
            glbs[f'out_type_{idx}'] = out_types[idx - len(left_other_names)]
            if dgvz__ohq != right_key_types[uxd__iypo] and right_key_types[
                uxd__iypo] != bodo.dict_str_arr_type:
                func_text += f"""    t2_keys_{uxd__iypo} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {wrbum__qhvax[1]}), out_type_{idx})
"""
            else:
                func_text += f"""    t2_keys_{uxd__iypo} = info_to_array(info_from_table(out_table, {idx}), {wrbum__qhvax[1]})
"""
            idx += 1
    for uxd__iypo, ytsk__rspi in enumerate(right_other_names):
        wrbum__qhvax = get_out_type(idx, right_other_types[uxd__iypo],
            ytsk__rspi, is_left, False)
        func_text += wrbum__qhvax[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(uxd__iypo, idx, wrbum__qhvax[1]))
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
    vvsm__dlrq = bodo.libs.distributed_api.get_size()
    jpe__kenbf = np.empty(vvsm__dlrq, left_key_arrs[0].dtype)
    dcz__iam = np.empty(vvsm__dlrq, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(jpe__kenbf, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(dcz__iam, left_key_arrs[0][-1])
    gqe__ssb = np.zeros(vvsm__dlrq, np.int32)
    ialen__jbiw = np.zeros(vvsm__dlrq, np.int32)
    ubcf__uvnl = np.zeros(vvsm__dlrq, np.int32)
    rda__cpwvf = right_key_arrs[0][0]
    xkid__eom = right_key_arrs[0][-1]
    ukh__ifvuj = -1
    uxd__iypo = 0
    while uxd__iypo < vvsm__dlrq - 1 and dcz__iam[uxd__iypo] < rda__cpwvf:
        uxd__iypo += 1
    while uxd__iypo < vvsm__dlrq and jpe__kenbf[uxd__iypo] <= xkid__eom:
        ukh__ifvuj, ytq__dwa = _count_overlap(right_key_arrs[0], jpe__kenbf
            [uxd__iypo], dcz__iam[uxd__iypo])
        if ukh__ifvuj != 0:
            ukh__ifvuj -= 1
            ytq__dwa += 1
        gqe__ssb[uxd__iypo] = ytq__dwa
        ialen__jbiw[uxd__iypo] = ukh__ifvuj
        uxd__iypo += 1
    while uxd__iypo < vvsm__dlrq:
        gqe__ssb[uxd__iypo] = 1
        ialen__jbiw[uxd__iypo] = len(right_key_arrs[0]) - 1
        uxd__iypo += 1
    bodo.libs.distributed_api.alltoall(gqe__ssb, ubcf__uvnl, 1)
    gsze__oft = ubcf__uvnl.sum()
    dctyh__nyqvz = np.empty(gsze__oft, right_key_arrs[0].dtype)
    rgltw__ywhp = alloc_arr_tup(gsze__oft, right_data)
    iox__vec = bodo.ir.join.calc_disp(ubcf__uvnl)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], dctyh__nyqvz,
        gqe__ssb, ubcf__uvnl, ialen__jbiw, iox__vec)
    bodo.libs.distributed_api.alltoallv_tup(right_data, rgltw__ywhp,
        gqe__ssb, ubcf__uvnl, ialen__jbiw, iox__vec)
    return (dctyh__nyqvz,), rgltw__ywhp


@numba.njit
def _count_overlap(r_key_arr, start, end):
    ytq__dwa = 0
    ukh__ifvuj = 0
    jtg__psllz = 0
    while jtg__psllz < len(r_key_arr) and r_key_arr[jtg__psllz] < start:
        ukh__ifvuj += 1
        jtg__psllz += 1
    while jtg__psllz < len(r_key_arr) and start <= r_key_arr[jtg__psllz
        ] <= end:
        jtg__psllz += 1
        ytq__dwa += 1
    return ukh__ifvuj, ytq__dwa


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    qkysw__gaoh = np.empty_like(arr)
    qkysw__gaoh[0] = 0
    for uxd__iypo in range(1, len(arr)):
        qkysw__gaoh[uxd__iypo] = qkysw__gaoh[uxd__iypo - 1] + arr[uxd__iypo - 1
            ]
    return qkysw__gaoh


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    jsjvu__gltke = len(left_keys[0])
    ekrz__ioym = len(right_keys[0])
    woe__vqp = alloc_arr_tup(jsjvu__gltke, left_keys)
    irk__pxreo = alloc_arr_tup(jsjvu__gltke, right_keys)
    adr__tjtf = alloc_arr_tup(jsjvu__gltke, data_left)
    qsyi__ftp = alloc_arr_tup(jsjvu__gltke, data_right)
    elfll__pbesn = 0
    qqazh__ycygs = 0
    for elfll__pbesn in range(jsjvu__gltke):
        if qqazh__ycygs < 0:
            qqazh__ycygs = 0
        while qqazh__ycygs < ekrz__ioym and getitem_arr_tup(right_keys,
            qqazh__ycygs) <= getitem_arr_tup(left_keys, elfll__pbesn):
            qqazh__ycygs += 1
        qqazh__ycygs -= 1
        setitem_arr_tup(woe__vqp, elfll__pbesn, getitem_arr_tup(left_keys,
            elfll__pbesn))
        setitem_arr_tup(adr__tjtf, elfll__pbesn, getitem_arr_tup(data_left,
            elfll__pbesn))
        if qqazh__ycygs >= 0:
            setitem_arr_tup(irk__pxreo, elfll__pbesn, getitem_arr_tup(
                right_keys, qqazh__ycygs))
            setitem_arr_tup(qsyi__ftp, elfll__pbesn, getitem_arr_tup(
                data_right, qqazh__ycygs))
        else:
            bodo.libs.array_kernels.setna_tup(irk__pxreo, elfll__pbesn)
            bodo.libs.array_kernels.setna_tup(qsyi__ftp, elfll__pbesn)
    return woe__vqp, irk__pxreo, adr__tjtf, qsyi__ftp


def copy_arr_tup(arrs):
    return tuple(a.copy() for a in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    ytq__dwa = arrs.count
    func_text = 'def f(arrs):\n'
    func_text += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(uxd__iypo) for uxd__iypo in range(ytq__dwa)))
    vch__lhsk = {}
    exec(func_text, {}, vch__lhsk)
    ygmzx__qce = vch__lhsk['f']
    return ygmzx__qce
