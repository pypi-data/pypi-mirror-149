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
        ugco__vxrp = func.signature
        ceo__yonj = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        ersfd__dvuly = cgutils.get_or_insert_function(builder.module,
            ceo__yonj, sym._literal_value)
        builder.call(ersfd__dvuly, [context.get_constant_null(ugco__vxrp.
            args[0]), context.get_constant_null(ugco__vxrp.args[1]),
            context.get_constant_null(ugco__vxrp.args[2]), context.
            get_constant_null(ugco__vxrp.args[3]), context.
            get_constant_null(ugco__vxrp.args[4]), context.
            get_constant_null(ugco__vxrp.args[5]), context.get_constant(
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
        self.left_cond_cols = set(blkhj__hdut for blkhj__hdut in left_vars.
            keys() if f'(left.{blkhj__hdut})' in gen_cond_expr)
        self.right_cond_cols = set(blkhj__hdut for blkhj__hdut in
            right_vars.keys() if f'(right.{blkhj__hdut})' in gen_cond_expr)
        yhvjx__sub = set(left_keys) & set(right_keys)
        gktxu__jnmf = set(left_vars.keys()) & set(right_vars.keys())
        yprd__owy = gktxu__jnmf - yhvjx__sub
        vect_same_key = []
        n_keys = len(left_keys)
        for onw__iwiyj in range(n_keys):
            mkd__gcnry = left_keys[onw__iwiyj]
            vzbz__lyohx = right_keys[onw__iwiyj]
            vect_same_key.append(mkd__gcnry == vzbz__lyohx)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(blkhj__hdut) + suffix_x if blkhj__hdut in
            yprd__owy else blkhj__hdut): ('left', blkhj__hdut) for
            blkhj__hdut in left_vars.keys()}
        self.column_origins.update({(str(blkhj__hdut) + suffix_y if 
            blkhj__hdut in yprd__owy else blkhj__hdut): ('right',
            blkhj__hdut) for blkhj__hdut in right_vars.keys()})
        if '$_bodo_index_' in yprd__owy:
            yprd__owy.remove('$_bodo_index_')
        self.add_suffix = yprd__owy

    def __repr__(self):
        kqp__xeuw = ''
        for blkhj__hdut, dzue__nyw in self.out_data_vars.items():
            kqp__xeuw += "'{}':{}, ".format(blkhj__hdut, dzue__nyw.name)
        ojk__odl = '{}{{{}}}'.format(self.df_out, kqp__xeuw)
        rxps__jlds = ''
        for blkhj__hdut, dzue__nyw in self.left_vars.items():
            rxps__jlds += "'{}':{}, ".format(blkhj__hdut, dzue__nyw.name)
        xhee__owhg = '{}{{{}}}'.format(self.left_df, rxps__jlds)
        rxps__jlds = ''
        for blkhj__hdut, dzue__nyw in self.right_vars.items():
            rxps__jlds += "'{}':{}, ".format(blkhj__hdut, dzue__nyw.name)
        skmvk__upkx = '{}{{{}}}'.format(self.right_df, rxps__jlds)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, ojk__odl, xhee__owhg, skmvk__upkx)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    bam__tzvxr = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    haopc__jfftf = []
    teni__rfkss = list(join_node.left_vars.values())
    for ffpg__ftm in teni__rfkss:
        lfm__roji = typemap[ffpg__ftm.name]
        zaja__ydfh = equiv_set.get_shape(ffpg__ftm)
        if zaja__ydfh:
            haopc__jfftf.append(zaja__ydfh[0])
    if len(haopc__jfftf) > 1:
        equiv_set.insert_equiv(*haopc__jfftf)
    haopc__jfftf = []
    teni__rfkss = list(join_node.right_vars.values())
    for ffpg__ftm in teni__rfkss:
        lfm__roji = typemap[ffpg__ftm.name]
        zaja__ydfh = equiv_set.get_shape(ffpg__ftm)
        if zaja__ydfh:
            haopc__jfftf.append(zaja__ydfh[0])
    if len(haopc__jfftf) > 1:
        equiv_set.insert_equiv(*haopc__jfftf)
    haopc__jfftf = []
    for ffpg__ftm in join_node.out_data_vars.values():
        lfm__roji = typemap[ffpg__ftm.name]
        lskq__jeixp = array_analysis._gen_shape_call(equiv_set, ffpg__ftm,
            lfm__roji.ndim, None, bam__tzvxr)
        equiv_set.insert_equiv(ffpg__ftm, lskq__jeixp)
        haopc__jfftf.append(lskq__jeixp[0])
        equiv_set.define(ffpg__ftm, set())
    if len(haopc__jfftf) > 1:
        equiv_set.insert_equiv(*haopc__jfftf)
    return [], bam__tzvxr


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    emdno__rad = Distribution.OneD
    ubg__dew = Distribution.OneD
    for ffpg__ftm in join_node.left_vars.values():
        emdno__rad = Distribution(min(emdno__rad.value, array_dists[
            ffpg__ftm.name].value))
    for ffpg__ftm in join_node.right_vars.values():
        ubg__dew = Distribution(min(ubg__dew.value, array_dists[ffpg__ftm.
            name].value))
    wlh__sxtov = Distribution.OneD_Var
    for ffpg__ftm in join_node.out_data_vars.values():
        if ffpg__ftm.name in array_dists:
            wlh__sxtov = Distribution(min(wlh__sxtov.value, array_dists[
                ffpg__ftm.name].value))
    bare__hunex = Distribution(min(wlh__sxtov.value, emdno__rad.value))
    wajbx__chval = Distribution(min(wlh__sxtov.value, ubg__dew.value))
    wlh__sxtov = Distribution(max(bare__hunex.value, wajbx__chval.value))
    for ffpg__ftm in join_node.out_data_vars.values():
        array_dists[ffpg__ftm.name] = wlh__sxtov
    if wlh__sxtov != Distribution.OneD_Var:
        emdno__rad = wlh__sxtov
        ubg__dew = wlh__sxtov
    for ffpg__ftm in join_node.left_vars.values():
        array_dists[ffpg__ftm.name] = emdno__rad
    for ffpg__ftm in join_node.right_vars.values():
        array_dists[ffpg__ftm.name] = ubg__dew
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    yhvjx__sub = set(join_node.left_keys) & set(join_node.right_keys)
    gktxu__jnmf = set(join_node.left_vars.keys()) & set(join_node.
        right_vars.keys())
    yprd__owy = gktxu__jnmf - yhvjx__sub
    for vdp__gaj, jxn__luwpq in join_node.out_data_vars.items():
        if join_node.indicator and vdp__gaj == '_merge':
            continue
        if not vdp__gaj in join_node.column_origins:
            raise BodoError('join(): The variable ' + vdp__gaj +
                ' is absent from the output')
        yaxid__oiuqa = join_node.column_origins[vdp__gaj]
        if yaxid__oiuqa[0] == 'left':
            ffpg__ftm = join_node.left_vars[yaxid__oiuqa[1]]
        else:
            ffpg__ftm = join_node.right_vars[yaxid__oiuqa[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=jxn__luwpq.
            name, src=ffpg__ftm.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for tvplk__juyh in list(join_node.left_vars.keys()):
        join_node.left_vars[tvplk__juyh] = visit_vars_inner(join_node.
            left_vars[tvplk__juyh], callback, cbdata)
    for tvplk__juyh in list(join_node.right_vars.keys()):
        join_node.right_vars[tvplk__juyh] = visit_vars_inner(join_node.
            right_vars[tvplk__juyh], callback, cbdata)
    for tvplk__juyh in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[tvplk__juyh] = visit_vars_inner(join_node.
            out_data_vars[tvplk__juyh], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    buk__fgps = []
    mrniv__nfsdd = True
    for tvplk__juyh, ffpg__ftm in join_node.out_data_vars.items():
        if ffpg__ftm.name in lives:
            mrniv__nfsdd = False
            continue
        if tvplk__juyh == '$_bodo_index_':
            continue
        if join_node.indicator and tvplk__juyh == '_merge':
            buk__fgps.append('_merge')
            join_node.indicator = False
            continue
        exb__gpsd, uyubs__dtxd = join_node.column_origins[tvplk__juyh]
        if (exb__gpsd == 'left' and uyubs__dtxd not in join_node.left_keys and
            uyubs__dtxd not in join_node.left_cond_cols):
            join_node.left_vars.pop(uyubs__dtxd)
            buk__fgps.append(tvplk__juyh)
        if (exb__gpsd == 'right' and uyubs__dtxd not in join_node.
            right_keys and uyubs__dtxd not in join_node.right_cond_cols):
            join_node.right_vars.pop(uyubs__dtxd)
            buk__fgps.append(tvplk__juyh)
    for cname in buk__fgps:
        join_node.out_data_vars.pop(cname)
    if mrniv__nfsdd:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({dzue__nyw.name for dzue__nyw in join_node.left_vars.
        values()})
    use_set.update({dzue__nyw.name for dzue__nyw in join_node.right_vars.
        values()})
    def_set.update({dzue__nyw.name for dzue__nyw in join_node.out_data_vars
        .values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    wjquh__ewp = set(dzue__nyw.name for dzue__nyw in join_node.
        out_data_vars.values())
    return set(), wjquh__ewp


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for tvplk__juyh in list(join_node.left_vars.keys()):
        join_node.left_vars[tvplk__juyh] = replace_vars_inner(join_node.
            left_vars[tvplk__juyh], var_dict)
    for tvplk__juyh in list(join_node.right_vars.keys()):
        join_node.right_vars[tvplk__juyh] = replace_vars_inner(join_node.
            right_vars[tvplk__juyh], var_dict)
    for tvplk__juyh in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[tvplk__juyh] = replace_vars_inner(join_node
            .out_data_vars[tvplk__juyh], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ffpg__ftm in join_node.out_data_vars.values():
        definitions[ffpg__ftm.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    zsjp__szbcf = tuple(join_node.left_vars[blkhj__hdut] for blkhj__hdut in
        join_node.left_keys)
    bqhwe__mmyjo = tuple(join_node.right_vars[blkhj__hdut] for blkhj__hdut in
        join_node.right_keys)
    lia__dzs = tuple(join_node.left_vars.keys())
    yikcl__zzgy = tuple(join_node.right_vars.keys())
    pmyb__mcyqc = ()
    nhc__ctzel = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        kucq__bjw = join_node.right_keys[0]
        if kucq__bjw in lia__dzs:
            nhc__ctzel = kucq__bjw,
            pmyb__mcyqc = join_node.right_vars[kucq__bjw],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        kucq__bjw = join_node.left_keys[0]
        if kucq__bjw in yikcl__zzgy:
            nhc__ctzel = kucq__bjw,
            pmyb__mcyqc = join_node.left_vars[kucq__bjw],
            optional_column = True
    gfo__cbx = tuple(join_node.out_data_vars[cname] for cname in nhc__ctzel)
    fae__uir = tuple(dzue__nyw for anfn__mpyl, dzue__nyw in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if anfn__mpyl
         not in join_node.left_keys)
    balwp__hnq = tuple(dzue__nyw for anfn__mpyl, dzue__nyw in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if 
        anfn__mpyl not in join_node.right_keys)
    cnsnb__qpzhf = (pmyb__mcyqc + zsjp__szbcf + bqhwe__mmyjo + fae__uir +
        balwp__hnq)
    giwl__beb = tuple(typemap[dzue__nyw.name] for dzue__nyw in cnsnb__qpzhf)
    ajfv__wwio = tuple('opti_c' + str(enjmh__pcie) for enjmh__pcie in range
        (len(pmyb__mcyqc)))
    left_other_names = tuple('t1_c' + str(enjmh__pcie) for enjmh__pcie in
        range(len(fae__uir)))
    right_other_names = tuple('t2_c' + str(enjmh__pcie) for enjmh__pcie in
        range(len(balwp__hnq)))
    left_other_types = tuple([typemap[blkhj__hdut.name] for blkhj__hdut in
        fae__uir])
    right_other_types = tuple([typemap[blkhj__hdut.name] for blkhj__hdut in
        balwp__hnq])
    left_key_names = tuple('t1_key' + str(enjmh__pcie) for enjmh__pcie in
        range(n_keys))
    right_key_names = tuple('t2_key' + str(enjmh__pcie) for enjmh__pcie in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(ajfv__wwio[
        0]) if len(ajfv__wwio) == 1 else '', ','.join(left_key_names), ','.
        join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[dzue__nyw.name] for dzue__nyw in zsjp__szbcf
        )
    right_key_types = tuple(typemap[dzue__nyw.name] for dzue__nyw in
        bqhwe__mmyjo)
    for enjmh__pcie in range(n_keys):
        glbs[f'key_type_{enjmh__pcie}'] = _match_join_key_types(left_key_types
            [enjmh__pcie], right_key_types[enjmh__pcie], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[enjmh__pcie]}, key_type_{enjmh__pcie})'
         for enjmh__pcie in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[enjmh__pcie]}, key_type_{enjmh__pcie})'
         for enjmh__pcie in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    exg__dnx = []
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            gpslf__alnyx = str(cname) + join_node.suffix_x
        else:
            gpslf__alnyx = cname
        assert gpslf__alnyx in join_node.out_data_vars
        exg__dnx.append(join_node.out_data_vars[gpslf__alnyx])
    for enjmh__pcie, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[enjmh__pcie] and not join_node.is_join:
            if cname in join_node.add_suffix:
                gpslf__alnyx = str(cname) + join_node.suffix_y
            else:
                gpslf__alnyx = cname
            assert gpslf__alnyx in join_node.out_data_vars
            exg__dnx.append(join_node.out_data_vars[gpslf__alnyx])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                gpslf__alnyx = str(cname) + join_node.suffix_x
            else:
                gpslf__alnyx = str(cname) + join_node.suffix_y
        else:
            gpslf__alnyx = cname
        return join_node.out_data_vars[gpslf__alnyx]
    fmi__ixzj = gfo__cbx + tuple(exg__dnx)
    fmi__ixzj += tuple(_get_out_col_var(anfn__mpyl, True) for anfn__mpyl,
        dzue__nyw in sorted(join_node.left_vars.items(), key=lambda a: str(
        a[0])) if anfn__mpyl not in join_node.left_keys)
    fmi__ixzj += tuple(_get_out_col_var(anfn__mpyl, False) for anfn__mpyl,
        dzue__nyw in sorted(join_node.right_vars.items(), key=lambda a: str
        (a[0])) if anfn__mpyl not in join_node.right_keys)
    if join_node.indicator:
        fmi__ixzj += _get_out_col_var('_merge', False),
    idq__bsx = [('t3_c' + str(enjmh__pcie)) for enjmh__pcie in range(len(
        fmi__ixzj))]
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
            right_parallel, glbs, [typemap[dzue__nyw.name] for dzue__nyw in
            fmi__ixzj], join_node.loc, join_node.indicator, join_node.
            is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums)
    if join_node.how == 'asof':
        for enjmh__pcie in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(enjmh__pcie
                , enjmh__pcie)
        for enjmh__pcie in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                enjmh__pcie, enjmh__pcie)
        for enjmh__pcie in range(n_keys):
            func_text += (
                f'    t1_keys_{enjmh__pcie} = out_t1_keys[{enjmh__pcie}]\n')
        for enjmh__pcie in range(n_keys):
            func_text += (
                f'    t2_keys_{enjmh__pcie} = out_t2_keys[{enjmh__pcie}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {idq__bsx[idx]} = opti_0\n'
        idx += 1
    for enjmh__pcie in range(n_keys):
        func_text += f'    {idq__bsx[idx]} = t1_keys_{enjmh__pcie}\n'
        idx += 1
    for enjmh__pcie in range(n_keys):
        if not join_node.vect_same_key[enjmh__pcie] and not join_node.is_join:
            func_text += f'    {idq__bsx[idx]} = t2_keys_{enjmh__pcie}\n'
            idx += 1
    for enjmh__pcie in range(len(left_other_names)):
        func_text += f'    {idq__bsx[idx]} = left_{enjmh__pcie}\n'
        idx += 1
    for enjmh__pcie in range(len(right_other_names)):
        func_text += f'    {idq__bsx[idx]} = right_{enjmh__pcie}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {idq__bsx[idx]} = indicator_col\n'
        idx += 1
    xuf__nuf = {}
    exec(func_text, {}, xuf__nuf)
    jsjs__wjq = xuf__nuf['f']
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
    ybc__evsd = compile_to_numba_ir(jsjs__wjq, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=giwl__beb, typemap=typemap, calltypes
        =calltypes).blocks.popitem()[1]
    replace_arg_nodes(ybc__evsd, cnsnb__qpzhf)
    etmml__bkli = ybc__evsd.body[:-3]
    for enjmh__pcie in range(len(fmi__ixzj)):
        etmml__bkli[-len(fmi__ixzj) + enjmh__pcie].target = fmi__ixzj[
            enjmh__pcie]
    return etmml__bkli


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    qcl__eyr = next_label()
    kvc__gzs = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    cjcyx__vxv = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{qcl__eyr}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        kvc__gzs, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        cjcyx__vxv, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    xuf__nuf = {}
    exec(func_text, table_getitem_funcs, xuf__nuf)
    jpp__tgzz = xuf__nuf[f'bodo_join_gen_cond{qcl__eyr}']
    hio__kic = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    obkw__pqpio = numba.cfunc(hio__kic, nopython=True)(jpp__tgzz)
    join_gen_cond_cfunc[obkw__pqpio.native_name] = obkw__pqpio
    join_gen_cond_cfunc_addr[obkw__pqpio.native_name] = obkw__pqpio.address
    return obkw__pqpio, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    hjkr__nog = []
    for blkhj__hdut, sac__fagbc in col_to_ind.items():
        cname = f'({table_name}.{blkhj__hdut})'
        if cname not in expr:
            continue
        yfkl__bfkg = f'getitem_{table_name}_val_{sac__fagbc}'
        tdi__upci = f'_bodo_{table_name}_val_{sac__fagbc}'
        wjxzc__pmcly = typemap[col_vars[blkhj__hdut].name]
        if is_str_arr_type(wjxzc__pmcly):
            func_text += f"""  {tdi__upci}, {tdi__upci}_size = {yfkl__bfkg}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {tdi__upci} = bodo.libs.str_arr_ext.decode_utf8({tdi__upci}, {tdi__upci}_size)
"""
        else:
            func_text += (
                f'  {tdi__upci} = {yfkl__bfkg}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[yfkl__bfkg
            ] = bodo.libs.array._gen_row_access_intrinsic(wjxzc__pmcly,
            sac__fagbc)
        expr = expr.replace(cname, tdi__upci)
        gnqv__dlkn = f'({na_check_name}.{table_name}.{blkhj__hdut})'
        if gnqv__dlkn in expr:
            nxifn__itvf = f'nacheck_{table_name}_val_{sac__fagbc}'
            pjix__chacx = f'_bodo_isna_{table_name}_val_{sac__fagbc}'
            if (isinstance(wjxzc__pmcly, bodo.libs.int_arr_ext.
                IntegerArrayType) or wjxzc__pmcly == bodo.libs.bool_arr_ext
                .boolean_array or is_str_arr_type(wjxzc__pmcly)):
                func_text += f"""  {pjix__chacx} = {nxifn__itvf}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {pjix__chacx} = {nxifn__itvf}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[nxifn__itvf
                ] = bodo.libs.array._gen_row_na_check_intrinsic(wjxzc__pmcly,
                sac__fagbc)
            expr = expr.replace(gnqv__dlkn, pjix__chacx)
        if sac__fagbc >= n_keys:
            hjkr__nog.append(sac__fagbc)
    return expr, func_text, hjkr__nog


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {blkhj__hdut: enjmh__pcie for enjmh__pcie, blkhj__hdut in
        enumerate(key_names)}
    enjmh__pcie = n_keys
    for blkhj__hdut in sorted(col_vars, key=lambda a: str(a)):
        if blkhj__hdut in key_names:
            continue
        col_to_ind[blkhj__hdut] = enjmh__pcie
        enjmh__pcie += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as jxhmk__enej:
        if is_str_arr_type(t1) and is_str_arr_type(t2):
            return bodo.string_array_type
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    blpbo__zbdef = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[dzue__nyw.name] in blpbo__zbdef for
        dzue__nyw in join_node.left_vars.values())
    right_parallel = all(array_dists[dzue__nyw.name] in blpbo__zbdef for
        dzue__nyw in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[dzue__nyw.name] in blpbo__zbdef for
            dzue__nyw in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[dzue__nyw.name] in blpbo__zbdef for
            dzue__nyw in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[dzue__nyw.name] in blpbo__zbdef for
            dzue__nyw in join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    ovtu__xwo = []
    for enjmh__pcie in range(len(left_key_names)):
        ofkm__wzq = _match_join_key_types(left_key_types[enjmh__pcie],
            right_key_types[enjmh__pcie], loc)
        ovtu__xwo.append(needs_typechange(ofkm__wzq, is_right,
            vect_same_key[enjmh__pcie]))
    for enjmh__pcie in range(len(left_other_names)):
        ovtu__xwo.append(needs_typechange(left_other_types[enjmh__pcie],
            is_right, False))
    for enjmh__pcie in range(len(right_key_names)):
        if not vect_same_key[enjmh__pcie] and not is_join:
            ofkm__wzq = _match_join_key_types(left_key_types[enjmh__pcie],
                right_key_types[enjmh__pcie], loc)
            ovtu__xwo.append(needs_typechange(ofkm__wzq, is_left, False))
    for enjmh__pcie in range(len(right_other_names)):
        ovtu__xwo.append(needs_typechange(right_other_types[enjmh__pcie],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                bcops__loj = IntDtype(in_type.dtype).name
                assert bcops__loj.endswith('Dtype()')
                bcops__loj = bcops__loj[:-7]
                vwn__ltxba = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{bcops__loj}"))
"""
                fmtvt__san = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                vwn__ltxba = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                fmtvt__san = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            vwn__ltxba = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            fmtvt__san = f'typ_{idx}'
        else:
            vwn__ltxba = ''
            fmtvt__san = in_name
        return vwn__ltxba, fmtvt__san
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    swoe__lig = []
    for enjmh__pcie in range(n_keys):
        swoe__lig.append('t1_keys[{}]'.format(enjmh__pcie))
    for enjmh__pcie in range(len(left_other_names)):
        swoe__lig.append('data_left[{}]'.format(enjmh__pcie))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in swoe__lig))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    cwljc__lbxlm = []
    for enjmh__pcie in range(n_keys):
        cwljc__lbxlm.append('t2_keys[{}]'.format(enjmh__pcie))
    for enjmh__pcie in range(len(right_other_names)):
        cwljc__lbxlm.append('data_right[{}]'.format(enjmh__pcie))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in cwljc__lbxlm))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        niwn__akib else '0' for niwn__akib in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if niwn__akib else '0' for niwn__akib in ovtu__xwo))
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
        ysam__sooc = get_out_type(idx, out_types[idx], 'opti_c0', False, False)
        func_text += ysam__sooc[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {ysam__sooc[1]})
"""
        idx += 1
    for enjmh__pcie, zziwz__swmeb in enumerate(left_key_names):
        ofkm__wzq = _match_join_key_types(left_key_types[enjmh__pcie],
            right_key_types[enjmh__pcie], loc)
        ysam__sooc = get_out_type(idx, ofkm__wzq, f't1_keys[{enjmh__pcie}]',
            is_right, vect_same_key[enjmh__pcie])
        func_text += ysam__sooc[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        if ofkm__wzq != left_key_types[enjmh__pcie] and left_key_types[
            enjmh__pcie] != bodo.dict_str_arr_type:
            func_text += f"""    t1_keys_{enjmh__pcie} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {ysam__sooc[1]}), out_type_{idx})
"""
        else:
            func_text += f"""    t1_keys_{enjmh__pcie} = info_to_array(info_from_table(out_table, {idx}), {ysam__sooc[1]})
"""
        idx += 1
    for enjmh__pcie, zziwz__swmeb in enumerate(left_other_names):
        ysam__sooc = get_out_type(idx, left_other_types[enjmh__pcie],
            zziwz__swmeb, is_right, False)
        func_text += ysam__sooc[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(enjmh__pcie, idx, ysam__sooc[1]))
        idx += 1
    for enjmh__pcie, zziwz__swmeb in enumerate(right_key_names):
        if not vect_same_key[enjmh__pcie] and not is_join:
            ofkm__wzq = _match_join_key_types(left_key_types[enjmh__pcie],
                right_key_types[enjmh__pcie], loc)
            ysam__sooc = get_out_type(idx, ofkm__wzq,
                f't2_keys[{enjmh__pcie}]', is_left, False)
            func_text += ysam__sooc[0]
            glbs[f'out_type_{idx}'] = out_types[idx - len(left_other_names)]
            if ofkm__wzq != right_key_types[enjmh__pcie] and right_key_types[
                enjmh__pcie] != bodo.dict_str_arr_type:
                func_text += f"""    t2_keys_{enjmh__pcie} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {ysam__sooc[1]}), out_type_{idx})
"""
            else:
                func_text += f"""    t2_keys_{enjmh__pcie} = info_to_array(info_from_table(out_table, {idx}), {ysam__sooc[1]})
"""
            idx += 1
    for enjmh__pcie, zziwz__swmeb in enumerate(right_other_names):
        ysam__sooc = get_out_type(idx, right_other_types[enjmh__pcie],
            zziwz__swmeb, is_left, False)
        func_text += ysam__sooc[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(enjmh__pcie, idx, ysam__sooc[1]))
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
    fpbrz__xdd = bodo.libs.distributed_api.get_size()
    ysz__egjs = np.empty(fpbrz__xdd, left_key_arrs[0].dtype)
    cijs__tea = np.empty(fpbrz__xdd, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(ysz__egjs, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(cijs__tea, left_key_arrs[0][-1])
    dsa__iys = np.zeros(fpbrz__xdd, np.int32)
    qrvoe__sgh = np.zeros(fpbrz__xdd, np.int32)
    kcr__rzqlv = np.zeros(fpbrz__xdd, np.int32)
    vti__qsf = right_key_arrs[0][0]
    zgo__tcasp = right_key_arrs[0][-1]
    azbs__dxax = -1
    enjmh__pcie = 0
    while enjmh__pcie < fpbrz__xdd - 1 and cijs__tea[enjmh__pcie] < vti__qsf:
        enjmh__pcie += 1
    while enjmh__pcie < fpbrz__xdd and ysz__egjs[enjmh__pcie] <= zgo__tcasp:
        azbs__dxax, hgtd__xbidx = _count_overlap(right_key_arrs[0],
            ysz__egjs[enjmh__pcie], cijs__tea[enjmh__pcie])
        if azbs__dxax != 0:
            azbs__dxax -= 1
            hgtd__xbidx += 1
        dsa__iys[enjmh__pcie] = hgtd__xbidx
        qrvoe__sgh[enjmh__pcie] = azbs__dxax
        enjmh__pcie += 1
    while enjmh__pcie < fpbrz__xdd:
        dsa__iys[enjmh__pcie] = 1
        qrvoe__sgh[enjmh__pcie] = len(right_key_arrs[0]) - 1
        enjmh__pcie += 1
    bodo.libs.distributed_api.alltoall(dsa__iys, kcr__rzqlv, 1)
    mbnv__czl = kcr__rzqlv.sum()
    eoood__dcp = np.empty(mbnv__czl, right_key_arrs[0].dtype)
    qgvq__jivrs = alloc_arr_tup(mbnv__czl, right_data)
    kiqg__ggdny = bodo.ir.join.calc_disp(kcr__rzqlv)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], eoood__dcp,
        dsa__iys, kcr__rzqlv, qrvoe__sgh, kiqg__ggdny)
    bodo.libs.distributed_api.alltoallv_tup(right_data, qgvq__jivrs,
        dsa__iys, kcr__rzqlv, qrvoe__sgh, kiqg__ggdny)
    return (eoood__dcp,), qgvq__jivrs


@numba.njit
def _count_overlap(r_key_arr, start, end):
    hgtd__xbidx = 0
    azbs__dxax = 0
    zznoe__rilq = 0
    while zznoe__rilq < len(r_key_arr) and r_key_arr[zznoe__rilq] < start:
        azbs__dxax += 1
        zznoe__rilq += 1
    while zznoe__rilq < len(r_key_arr) and start <= r_key_arr[zznoe__rilq
        ] <= end:
        zznoe__rilq += 1
        hgtd__xbidx += 1
    return azbs__dxax, hgtd__xbidx


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    ltcvn__zxba = np.empty_like(arr)
    ltcvn__zxba[0] = 0
    for enjmh__pcie in range(1, len(arr)):
        ltcvn__zxba[enjmh__pcie] = ltcvn__zxba[enjmh__pcie - 1] + arr[
            enjmh__pcie - 1]
    return ltcvn__zxba


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    zfx__akleh = len(left_keys[0])
    fpqrd__spk = len(right_keys[0])
    rbeqi__vazx = alloc_arr_tup(zfx__akleh, left_keys)
    xaw__mqgb = alloc_arr_tup(zfx__akleh, right_keys)
    ppg__owed = alloc_arr_tup(zfx__akleh, data_left)
    eyom__faeur = alloc_arr_tup(zfx__akleh, data_right)
    felk__mtl = 0
    kfkve__ddl = 0
    for felk__mtl in range(zfx__akleh):
        if kfkve__ddl < 0:
            kfkve__ddl = 0
        while kfkve__ddl < fpqrd__spk and getitem_arr_tup(right_keys,
            kfkve__ddl) <= getitem_arr_tup(left_keys, felk__mtl):
            kfkve__ddl += 1
        kfkve__ddl -= 1
        setitem_arr_tup(rbeqi__vazx, felk__mtl, getitem_arr_tup(left_keys,
            felk__mtl))
        setitem_arr_tup(ppg__owed, felk__mtl, getitem_arr_tup(data_left,
            felk__mtl))
        if kfkve__ddl >= 0:
            setitem_arr_tup(xaw__mqgb, felk__mtl, getitem_arr_tup(
                right_keys, kfkve__ddl))
            setitem_arr_tup(eyom__faeur, felk__mtl, getitem_arr_tup(
                data_right, kfkve__ddl))
        else:
            bodo.libs.array_kernels.setna_tup(xaw__mqgb, felk__mtl)
            bodo.libs.array_kernels.setna_tup(eyom__faeur, felk__mtl)
    return rbeqi__vazx, xaw__mqgb, ppg__owed, eyom__faeur


def copy_arr_tup(arrs):
    return tuple(a.copy() for a in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    hgtd__xbidx = arrs.count
    func_text = 'def f(arrs):\n'
    func_text += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(enjmh__pcie) for enjmh__pcie in range(hgtd__xbidx)))
    xuf__nuf = {}
    exec(func_text, {}, xuf__nuf)
    tlqb__zvfuy = xuf__nuf['f']
    return tlqb__zvfuy
