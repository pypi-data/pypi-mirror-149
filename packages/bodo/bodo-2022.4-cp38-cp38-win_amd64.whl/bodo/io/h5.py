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
        qvdr__wuijm = self._get_h5_type(lhs, rhs)
        if qvdr__wuijm is not None:
            tjrue__wsb = str(qvdr__wuijm.dtype)
            rzzy__dqr = 'def _h5_read_impl(dset, index):\n'
            rzzy__dqr += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(qvdr__wuijm.ndim, tjrue__wsb))
            bfwl__sox = {}
            exec(rzzy__dqr, {}, bfwl__sox)
            rbx__dhci = bfwl__sox['_h5_read_impl']
            onb__eej = compile_to_numba_ir(rbx__dhci, {'bodo': bodo}
                ).blocks.popitem()[1]
            kov__kirnu = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(onb__eej, [rhs.value, kov__kirnu])
            qopon__rnv = onb__eej.body[:-3]
            qopon__rnv[-1].target = assign.target
            return qopon__rnv
        return None

    def _get_h5_type(self, lhs, rhs):
        qvdr__wuijm = self._get_h5_type_locals(lhs)
        if qvdr__wuijm is not None:
            return qvdr__wuijm
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        kov__kirnu = rhs.index if rhs.op == 'getitem' else rhs.index_var
        qgha__dkqjx = guard(find_const, self.func_ir, kov__kirnu)
        require(not isinstance(qgha__dkqjx, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            kpze__vnabu = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            fwy__jnol = get_const_value_inner(self.func_ir, kpze__vnabu,
                arg_types=self.arg_types)
            obj_name_list.append(fwy__jnol)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        ooau__apzvv = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        vbnz__wtmgp = h5py.File(ooau__apzvv, 'r')
        ramon__klcfg = vbnz__wtmgp
        for fwy__jnol in obj_name_list:
            ramon__klcfg = ramon__klcfg[fwy__jnol]
        require(isinstance(ramon__klcfg, h5py.Dataset))
        owiii__doz = len(ramon__klcfg.shape)
        ave__omcn = numba.np.numpy_support.from_dtype(ramon__klcfg.dtype)
        vbnz__wtmgp.close()
        return types.Array(ave__omcn, owiii__doz, 'C')

    def _get_h5_type_locals(self, varname):
        yyhuo__jmhe = self.locals.pop(varname, None)
        if yyhuo__jmhe is None and varname is not None:
            yyhuo__jmhe = self.flags.h5_types.get(varname, None)
        return yyhuo__jmhe
