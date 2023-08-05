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
    dbi__kly = out_arr_typ.instance_type if isinstance(out_arr_typ, types.
        TypeRef) else out_arr_typ
    oyt__emps = len(table.arr_types)
    wjw__gowm = tuple([dbi__kly] * oyt__emps)
    esq__avc = TableType(wjw__gowm)
    rwyno__fld = {'bodo': bodo, 'lst_dtype': dbi__kly, 'table_typ': esq__avc}
    rdwo__wygm = 'def impl(table, func_name, out_arr_typ, used_cols=None):\n'
    rdwo__wygm += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({oyt__emps}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        rdwo__wygm += f'  used_cols_set = set(used_cols)\n'
    else:
        rdwo__wygm += f'  used_cols_set = used_cols\n'
    rdwo__wygm += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for dweex__zlat in table.type_to_blk.values():
        rdwo__wygm += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {dweex__zlat})\n'
            )
        rwyno__fld[f'col_indices_{dweex__zlat}'] = np.array(table.
            block_to_arr_ind[dweex__zlat], dtype=np.int64)
        rdwo__wygm += f'  for i in range(len(blk)):\n'
        rdwo__wygm += f'    col_loc = col_indices_{dweex__zlat}[i]\n'
        if not is_overload_none(used_cols):
            rdwo__wygm += f'    if col_loc not in used_cols_set:\n'
            rdwo__wygm += f'        continue\n'
        rdwo__wygm += f'    out_list[col_loc] = {func_name}(blk[i])\n'
    rdwo__wygm += (
        '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
        )
    nhko__ecj = {}
    exec(rdwo__wygm, rwyno__fld, nhko__ecj)
    return nhko__ecj['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    rwyno__fld = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    rdwo__wygm = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    rdwo__wygm += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for dweex__zlat in table.type_to_blk.values():
        rdwo__wygm += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {dweex__zlat})\n'
            )
        rwyno__fld[f'col_indices_{dweex__zlat}'] = np.array(table.
            block_to_arr_ind[dweex__zlat], dtype=np.int64)
        rdwo__wygm += '  for i in range(len(blk)):\n'
        rdwo__wygm += f'    col_loc = col_indices_{dweex__zlat}[i]\n'
        rdwo__wygm += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    rdwo__wygm += '  if parallel:\n'
    rdwo__wygm += '    for i in range(start_offset, len(out_arr)):\n'
    rdwo__wygm += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    nhko__ecj = {}
    exec(rdwo__wygm, rwyno__fld, nhko__ecj)
    return nhko__ecj['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    xmj__lpdjm = table.type_to_blk[arr_type]
    rwyno__fld = {'bodo': bodo}
    rwyno__fld['col_indices'] = np.array(table.block_to_arr_ind[xmj__lpdjm],
        dtype=np.int64)
    rdwo__wygm = 'def impl(table, col_nums, arr_type):\n'
    rdwo__wygm += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {xmj__lpdjm})\n')
    rdwo__wygm += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    rdwo__wygm += '  n = len(table)\n'
    rxc__iir = bodo.utils.typing.is_str_arr_type(arr_type)
    if rxc__iir:
        rdwo__wygm += '  total_chars = 0\n'
        rdwo__wygm += '  for c in col_nums:\n'
        rdwo__wygm += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        rdwo__wygm += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        rdwo__wygm += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        rdwo__wygm += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        rdwo__wygm += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    rdwo__wygm += '  for i in range(len(col_nums)):\n'
    rdwo__wygm += '    c = col_nums[i]\n'
    if not rxc__iir:
        rdwo__wygm += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    rdwo__wygm += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    rdwo__wygm += '    off = i * n\n'
    rdwo__wygm += '    for j in range(len(arr)):\n'
    rdwo__wygm += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    rdwo__wygm += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    rdwo__wygm += '      else:\n'
    rdwo__wygm += '        out_arr[off+j] = arr[j]\n'
    rdwo__wygm += '  return out_arr\n'
    ofs__qxca = {}
    exec(rdwo__wygm, rwyno__fld, ofs__qxca)
    dif__swxa = ofs__qxca['impl']
    return dif__swxa
