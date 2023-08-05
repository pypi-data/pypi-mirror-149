"""
Analysis and transformation for HDF5 support.
"""
import types as pytypes
import numba
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, find_callname, find_const, get_definition, guard, replace_arg_nodes, require
import bodo
import bodo.io
from bodo.utils.transform import get_const_value_inner


class H5_IO:

    def __init__(self, func_ir, _locals, flags, arg_types):
        self.func_ir = func_ir
        self.locals = _locals
        self.flags = flags
        self.arg_types = arg_types

    def handle_possible_h5_read(self, assign, lhs, rhs):
        xduac__mpy = self._get_h5_type(lhs, rhs)
        if xduac__mpy is not None:
            ttdhv__urza = str(xduac__mpy.dtype)
            ulrtx__mbeq = 'def _h5_read_impl(dset, index):\n'
            ulrtx__mbeq += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(xduac__mpy.ndim, ttdhv__urza))
            mpbj__qmzo = {}
            exec(ulrtx__mbeq, {}, mpbj__qmzo)
            tokd__uanhj = mpbj__qmzo['_h5_read_impl']
            gpey__dgnw = compile_to_numba_ir(tokd__uanhj, {'bodo': bodo}
                ).blocks.popitem()[1]
            geru__faxvu = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(gpey__dgnw, [rhs.value, geru__faxvu])
            tbow__umqj = gpey__dgnw.body[:-3]
            tbow__umqj[-1].target = assign.target
            return tbow__umqj
        return None

    def _get_h5_type(self, lhs, rhs):
        xduac__mpy = self._get_h5_type_locals(lhs)
        if xduac__mpy is not None:
            return xduac__mpy
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        geru__faxvu = rhs.index if rhs.op == 'getitem' else rhs.index_var
        aww__rmxz = guard(find_const, self.func_ir, geru__faxvu)
        require(not isinstance(aww__rmxz, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            kuu__psn = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            wtp__tsawj = get_const_value_inner(self.func_ir, kuu__psn,
                arg_types=self.arg_types)
            obj_name_list.append(wtp__tsawj)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        get__iob = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        dslfg__qfixv = h5py.File(get__iob, 'r')
        drj__giao = dslfg__qfixv
        for wtp__tsawj in obj_name_list:
            drj__giao = drj__giao[wtp__tsawj]
        require(isinstance(drj__giao, h5py.Dataset))
        laeq__pgxsv = len(drj__giao.shape)
        qcisy__ham = numba.np.numpy_support.from_dtype(drj__giao.dtype)
        dslfg__qfixv.close()
        return types.Array(qcisy__ham, laeq__pgxsv, 'C')

    def _get_h5_type_locals(self, varname):
        kwi__qfcs = self.locals.pop(varname, None)
        if kwi__qfcs is None and varname is not None:
            kwi__qfcs = self.flags.h5_types.get(varname, None)
        return kwi__qfcs
