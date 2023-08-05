"""File containing utility functions for supporting DataFrame operations with Table Format."""
import numba
import numpy as np
from numba.core import types
import bodo
from bodo.hiframes.table import TableType
from bodo.utils.typing import get_overload_const_str, is_overload_constant_str, is_overload_none, raise_bodo_error


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_mappable_table_func(table, func_name, out_arr_typ, used_cols=None
    ):
    if not is_overload_constant_str(func_name):
        raise_bodo_error(
            'generate_mappable_table_func(): func_name must be a constant string'
            )
    func_name = get_overload_const_str(func_name)
    wqzjy__lbh = out_arr_typ.instance_type if isinstance(out_arr_typ, types
        .TypeRef) else out_arr_typ
    mku__makvf = len(table.arr_types)
    xhre__une = tuple([wqzjy__lbh] * mku__makvf)
    cli__zuesr = TableType(xhre__une)
    mxnnl__iqqc = {'bodo': bodo, 'lst_dtype': wqzjy__lbh, 'table_typ':
        cli__zuesr}
    cnc__koj = 'def impl(table, func_name, out_arr_typ, used_cols=None):\n'
    cnc__koj += (
        f'  out_list = bodo.hiframes.table.alloc_empty_list_type({mku__makvf}, lst_dtype)\n'
        )
    if not is_overload_none(used_cols):
        cnc__koj += f'  used_cols_set = set(used_cols)\n'
    else:
        cnc__koj += f'  used_cols_set = used_cols\n'
    cnc__koj += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for sghn__htgt in table.type_to_blk.values():
        cnc__koj += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {sghn__htgt})\n'
            )
        mxnnl__iqqc[f'col_indices_{sghn__htgt}'] = np.array(table.
            block_to_arr_ind[sghn__htgt], dtype=np.int64)
        cnc__koj += f'  for i in range(len(blk)):\n'
        cnc__koj += f'    col_loc = col_indices_{sghn__htgt}[i]\n'
        if not is_overload_none(used_cols):
            cnc__koj += f'    if col_loc not in used_cols_set:\n'
            cnc__koj += f'        continue\n'
        cnc__koj += f'    out_list[col_loc] = {func_name}(blk[i])\n'
    cnc__koj += (
        '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
        )
    hfa__emgyt = {}
    exec(cnc__koj, mxnnl__iqqc, hfa__emgyt)
    return hfa__emgyt['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    mxnnl__iqqc = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    cnc__koj = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    cnc__koj += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for sghn__htgt in table.type_to_blk.values():
        cnc__koj += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {sghn__htgt})\n'
            )
        mxnnl__iqqc[f'col_indices_{sghn__htgt}'] = np.array(table.
            block_to_arr_ind[sghn__htgt], dtype=np.int64)
        cnc__koj += '  for i in range(len(blk)):\n'
        cnc__koj += f'    col_loc = col_indices_{sghn__htgt}[i]\n'
        cnc__koj += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    cnc__koj += '  if parallel:\n'
    cnc__koj += '    for i in range(start_offset, len(out_arr)):\n'
    cnc__koj += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    hfa__emgyt = {}
    exec(cnc__koj, mxnnl__iqqc, hfa__emgyt)
    return hfa__emgyt['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    vddiz__bdl = table.type_to_blk[arr_type]
    mxnnl__iqqc = {'bodo': bodo}
    mxnnl__iqqc['col_indices'] = np.array(table.block_to_arr_ind[vddiz__bdl
        ], dtype=np.int64)
    cnc__koj = 'def impl(table, col_nums, arr_type):\n'
    cnc__koj += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {vddiz__bdl})\n')
    cnc__koj += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    cnc__koj += '  n = len(table)\n'
    zlwr__whow = bodo.utils.typing.is_str_arr_type(arr_type)
    if zlwr__whow:
        cnc__koj += '  total_chars = 0\n'
        cnc__koj += '  for c in col_nums:\n'
        cnc__koj += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        cnc__koj += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        cnc__koj += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        cnc__koj += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        cnc__koj += (
            '  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))\n'
            )
    cnc__koj += '  for i in range(len(col_nums)):\n'
    cnc__koj += '    c = col_nums[i]\n'
    if not zlwr__whow:
        cnc__koj += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    cnc__koj += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    cnc__koj += '    off = i * n\n'
    cnc__koj += '    for j in range(len(arr)):\n'
    cnc__koj += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    cnc__koj += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    cnc__koj += '      else:\n'
    cnc__koj += '        out_arr[off+j] = arr[j]\n'
    cnc__koj += '  return out_arr\n'
    gaw__juby = {}
    exec(cnc__koj, mxnnl__iqqc, gaw__juby)
    dcw__srwua = gaw__juby['impl']
    return dcw__srwua
