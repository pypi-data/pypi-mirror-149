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
        kvwxr__ythey = self._get_h5_type(lhs, rhs)
        if kvwxr__ythey is not None:
            ajcm__akh = str(kvwxr__ythey.dtype)
            vfqla__mnckg = 'def _h5_read_impl(dset, index):\n'
            vfqla__mnckg += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(kvwxr__ythey.ndim, ajcm__akh))
            dqk__dci = {}
            exec(vfqla__mnckg, {}, dqk__dci)
            vhm__cyah = dqk__dci['_h5_read_impl']
            nqu__jce = compile_to_numba_ir(vhm__cyah, {'bodo': bodo}
                ).blocks.popitem()[1]
            kqti__absu = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(nqu__jce, [rhs.value, kqti__absu])
            nbn__gjxbd = nqu__jce.body[:-3]
            nbn__gjxbd[-1].target = assign.target
            return nbn__gjxbd
        return None

    def _get_h5_type(self, lhs, rhs):
        kvwxr__ythey = self._get_h5_type_locals(lhs)
        if kvwxr__ythey is not None:
            return kvwxr__ythey
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        kqti__absu = rhs.index if rhs.op == 'getitem' else rhs.index_var
        ndlv__ezfn = guard(find_const, self.func_ir, kqti__absu)
        require(not isinstance(ndlv__ezfn, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            plo__ugbof = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            isqy__mtrud = get_const_value_inner(self.func_ir, plo__ugbof,
                arg_types=self.arg_types)
            obj_name_list.append(isqy__mtrud)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        zfev__zut = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        fqps__zgijk = h5py.File(zfev__zut, 'r')
        imkk__ycw = fqps__zgijk
        for isqy__mtrud in obj_name_list:
            imkk__ycw = imkk__ycw[isqy__mtrud]
        require(isinstance(imkk__ycw, h5py.Dataset))
        fjhv__svqf = len(imkk__ycw.shape)
        zrsvc__ufq = numba.np.numpy_support.from_dtype(imkk__ycw.dtype)
        fqps__zgijk.close()
        return types.Array(zrsvc__ufq, fjhv__svqf, 'C')

    def _get_h5_type_locals(self, varname):
        xbit__elmfo = self.locals.pop(varname, None)
        if xbit__elmfo is None and varname is not None:
            xbit__elmfo = self.flags.h5_types.get(varname, None)
        return xbit__elmfo
