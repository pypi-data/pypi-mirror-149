"""CSR Matrix data type implementation for scipy.sparse.csr_matrix
"""
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError


class CSRMatrixType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, dtype, idx_dtype):
        self.dtype = dtype
        self.idx_dtype = idx_dtype
        super(CSRMatrixType, self).__init__(name=
            f'CSRMatrixType({dtype}, {idx_dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    def copy(self):
        return CSRMatrixType(self.dtype, self.idx_dtype)


@register_model(CSRMatrixType)
class CSRMatrixModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sxnne__ovm = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, sxnne__ovm)


make_attribute_wrapper(CSRMatrixType, 'data', 'data')
make_attribute_wrapper(CSRMatrixType, 'indices', 'indices')
make_attribute_wrapper(CSRMatrixType, 'indptr', 'indptr')
make_attribute_wrapper(CSRMatrixType, 'shape', 'shape')


@intrinsic
def init_csr_matrix(typingctx, data_t, indices_t, indptr_t, shape_t=None):
    assert isinstance(data_t, types.Array)
    assert isinstance(indices_t, types.Array) and isinstance(indices_t.
        dtype, types.Integer)
    assert indices_t == indptr_t

    def codegen(context, builder, signature, args):
        qyhw__nvdab, ekzi__fmio, ilckz__jbkuq, urpn__iww = args
        yvehb__wjr = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        yvehb__wjr.data = qyhw__nvdab
        yvehb__wjr.indices = ekzi__fmio
        yvehb__wjr.indptr = ilckz__jbkuq
        yvehb__wjr.shape = urpn__iww
        context.nrt.incref(builder, signature.args[0], qyhw__nvdab)
        context.nrt.incref(builder, signature.args[1], ekzi__fmio)
        context.nrt.incref(builder, signature.args[2], ilckz__jbkuq)
        return yvehb__wjr._getvalue()
    qes__jqe = CSRMatrixType(data_t.dtype, indices_t.dtype)
    yewvb__mjp = qes__jqe(data_t, indices_t, indptr_t, types.UniTuple(types
        .int64, 2))
    return yewvb__mjp, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    yvehb__wjr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    iaki__vfjpi = c.pyapi.object_getattr_string(val, 'data')
    rsss__fkdj = c.pyapi.object_getattr_string(val, 'indices')
    wfut__ghoe = c.pyapi.object_getattr_string(val, 'indptr')
    ajg__baiom = c.pyapi.object_getattr_string(val, 'shape')
    yvehb__wjr.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'
        ), iaki__vfjpi).value
    yvehb__wjr.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), rsss__fkdj).value
    yvehb__wjr.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), wfut__ghoe).value
    yvehb__wjr.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 
        2), ajg__baiom).value
    c.pyapi.decref(iaki__vfjpi)
    c.pyapi.decref(rsss__fkdj)
    c.pyapi.decref(wfut__ghoe)
    c.pyapi.decref(ajg__baiom)
    wkkdh__sncjz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yvehb__wjr._getvalue(), is_error=wkkdh__sncjz)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    yzflm__wxmb = c.context.insert_const_string(c.builder.module,
        'scipy.sparse')
    armcv__weps = c.pyapi.import_module_noblock(yzflm__wxmb)
    yvehb__wjr = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        yvehb__wjr.data)
    iaki__vfjpi = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        yvehb__wjr.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        yvehb__wjr.indices)
    rsss__fkdj = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), yvehb__wjr.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        yvehb__wjr.indptr)
    wfut__ghoe = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), yvehb__wjr.indptr, c.env_manager)
    ajg__baiom = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        yvehb__wjr.shape, c.env_manager)
    vlzzf__xlpeg = c.pyapi.tuple_pack([iaki__vfjpi, rsss__fkdj, wfut__ghoe])
    vvftc__dvxjl = c.pyapi.call_method(armcv__weps, 'csr_matrix', (
        vlzzf__xlpeg, ajg__baiom))
    c.pyapi.decref(vlzzf__xlpeg)
    c.pyapi.decref(iaki__vfjpi)
    c.pyapi.decref(rsss__fkdj)
    c.pyapi.decref(wfut__ghoe)
    c.pyapi.decref(ajg__baiom)
    c.pyapi.decref(armcv__weps)
    c.context.nrt.decref(c.builder, typ, val)
    return vvftc__dvxjl


@overload(len, no_unliteral=True)
def overload_csr_matrix_len(A):
    if isinstance(A, CSRMatrixType):
        return lambda A: A.shape[0]


@overload_attribute(CSRMatrixType, 'ndim')
def overload_csr_matrix_ndim(A):
    return lambda A: 2


@overload_method(CSRMatrixType, 'copy', no_unliteral=True)
def overload_csr_matrix_copy(A):

    def copy_impl(A):
        return init_csr_matrix(A.data.copy(), A.indices.copy(), A.indptr.
            copy(), A.shape)
    return copy_impl


@overload(operator.getitem, no_unliteral=True)
def csr_matrix_getitem(A, idx):
    if not isinstance(A, CSRMatrixType):
        return
    vnq__ctrx = A.dtype
    zfsjk__zsgt = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            ncoz__ilb, ihy__ynci = A.shape
            mavvk__zzxvj = numba.cpython.unicode._normalize_slice(idx[0],
                ncoz__ilb)
            kpx__gpq = numba.cpython.unicode._normalize_slice(idx[1], ihy__ynci
                )
            if mavvk__zzxvj.step != 1 or kpx__gpq.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            uuoia__ctusu = mavvk__zzxvj.start
            cytk__waz = mavvk__zzxvj.stop
            ofl__yibk = kpx__gpq.start
            xpm__znq = kpx__gpq.stop
            edqvd__xdr = A.indptr
            llut__lcf = A.indices
            ibya__etwac = A.data
            cpsi__kqrpq = cytk__waz - uuoia__ctusu
            bxzh__ttah = xpm__znq - ofl__yibk
            ihnmu__vdum = 0
            dtpl__mlxrv = 0
            for fesd__tmdi in range(cpsi__kqrpq):
                fwyrg__txfr = edqvd__xdr[uuoia__ctusu + fesd__tmdi]
                mdriz__zqk = edqvd__xdr[uuoia__ctusu + fesd__tmdi + 1]
                for ols__iyd in range(fwyrg__txfr, mdriz__zqk):
                    if llut__lcf[ols__iyd] >= ofl__yibk and llut__lcf[ols__iyd
                        ] < xpm__znq:
                        ihnmu__vdum += 1
            hovo__ltb = np.empty(cpsi__kqrpq + 1, zfsjk__zsgt)
            gjyz__jsji = np.empty(ihnmu__vdum, zfsjk__zsgt)
            trmmx__gyklq = np.empty(ihnmu__vdum, vnq__ctrx)
            hovo__ltb[0] = 0
            for fesd__tmdi in range(cpsi__kqrpq):
                fwyrg__txfr = edqvd__xdr[uuoia__ctusu + fesd__tmdi]
                mdriz__zqk = edqvd__xdr[uuoia__ctusu + fesd__tmdi + 1]
                for ols__iyd in range(fwyrg__txfr, mdriz__zqk):
                    if llut__lcf[ols__iyd] >= ofl__yibk and llut__lcf[ols__iyd
                        ] < xpm__znq:
                        gjyz__jsji[dtpl__mlxrv] = llut__lcf[ols__iyd
                            ] - ofl__yibk
                        trmmx__gyklq[dtpl__mlxrv] = ibya__etwac[ols__iyd]
                        dtpl__mlxrv += 1
                hovo__ltb[fesd__tmdi + 1] = dtpl__mlxrv
            return init_csr_matrix(trmmx__gyklq, gjyz__jsji, hovo__ltb, (
                cpsi__kqrpq, bxzh__ttah))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
