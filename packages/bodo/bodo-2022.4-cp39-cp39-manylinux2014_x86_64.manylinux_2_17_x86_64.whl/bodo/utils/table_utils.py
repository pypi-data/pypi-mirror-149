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
    don__mfq = out_arr_typ.instance_type if isinstance(out_arr_typ, types.
        TypeRef) else out_arr_typ
    stgi__fdopc = len(table.arr_types)
    ncbay__rgxv = tuple([don__mfq] * stgi__fdopc)
    ewrp__ufs = TableType(ncbay__rgxv)
    wmv__lpk = {'bodo': bodo, 'lst_dtype': don__mfq, 'table_typ': ewrp__ufs}
    zrlyr__acr = 'def impl(table, func_name, out_arr_typ, used_cols=None):\n'
    zrlyr__acr += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({stgi__fdopc}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        zrlyr__acr += f'  used_cols_set = set(used_cols)\n'
    else:
        zrlyr__acr += f'  used_cols_set = used_cols\n'
    zrlyr__acr += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for xpyd__kbuez in table.type_to_blk.values():
        zrlyr__acr += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {xpyd__kbuez})\n'
            )
        wmv__lpk[f'col_indices_{xpyd__kbuez}'] = np.array(table.
            block_to_arr_ind[xpyd__kbuez], dtype=np.int64)
        zrlyr__acr += f'  for i in range(len(blk)):\n'
        zrlyr__acr += f'    col_loc = col_indices_{xpyd__kbuez}[i]\n'
        if not is_overload_none(used_cols):
            zrlyr__acr += f'    if col_loc not in used_cols_set:\n'
            zrlyr__acr += f'        continue\n'
        zrlyr__acr += f'    out_list[col_loc] = {func_name}(blk[i])\n'
    zrlyr__acr += (
        '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
        )
    dwjvr__gxbl = {}
    exec(zrlyr__acr, wmv__lpk, dwjvr__gxbl)
    return dwjvr__gxbl['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    wmv__lpk = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.distributed_api.
        Reduce_Type.Sum.value)}
    zrlyr__acr = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    zrlyr__acr += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for xpyd__kbuez in table.type_to_blk.values():
        zrlyr__acr += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {xpyd__kbuez})\n'
            )
        wmv__lpk[f'col_indices_{xpyd__kbuez}'] = np.array(table.
            block_to_arr_ind[xpyd__kbuez], dtype=np.int64)
        zrlyr__acr += '  for i in range(len(blk)):\n'
        zrlyr__acr += f'    col_loc = col_indices_{xpyd__kbuez}[i]\n'
        zrlyr__acr += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    zrlyr__acr += '  if parallel:\n'
    zrlyr__acr += '    for i in range(start_offset, len(out_arr)):\n'
    zrlyr__acr += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    dwjvr__gxbl = {}
    exec(zrlyr__acr, wmv__lpk, dwjvr__gxbl)
    return dwjvr__gxbl['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    ktui__bag = table.type_to_blk[arr_type]
    wmv__lpk = {'bodo': bodo}
    wmv__lpk['col_indices'] = np.array(table.block_to_arr_ind[ktui__bag],
        dtype=np.int64)
    zrlyr__acr = 'def impl(table, col_nums, arr_type):\n'
    zrlyr__acr += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {ktui__bag})\n')
    zrlyr__acr += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    zrlyr__acr += '  n = len(table)\n'
    dawbk__gafs = bodo.utils.typing.is_str_arr_type(arr_type)
    if dawbk__gafs:
        zrlyr__acr += '  total_chars = 0\n'
        zrlyr__acr += '  for c in col_nums:\n'
        zrlyr__acr += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        zrlyr__acr += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        zrlyr__acr += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        zrlyr__acr += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        zrlyr__acr += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    zrlyr__acr += '  for i in range(len(col_nums)):\n'
    zrlyr__acr += '    c = col_nums[i]\n'
    if not dawbk__gafs:
        zrlyr__acr += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    zrlyr__acr += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    zrlyr__acr += '    off = i * n\n'
    zrlyr__acr += '    for j in range(len(arr)):\n'
    zrlyr__acr += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    zrlyr__acr += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    zrlyr__acr += '      else:\n'
    zrlyr__acr += '        out_arr[off+j] = arr[j]\n'
    zrlyr__acr += '  return out_arr\n'
    fzkph__pew = {}
    exec(zrlyr__acr, wmv__lpk, fzkph__pew)
    necpu__kxsvc = fzkph__pew['impl']
    return necpu__kxsvc
