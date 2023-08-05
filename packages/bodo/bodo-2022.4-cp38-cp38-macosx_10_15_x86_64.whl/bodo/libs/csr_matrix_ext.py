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
        bpllj__enmg = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, bpllj__enmg)


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
        hkqg__hood, pqxoj__ztgh, mdz__sidpc, ckdaz__ttq = args
        mgw__jzpl = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        mgw__jzpl.data = hkqg__hood
        mgw__jzpl.indices = pqxoj__ztgh
        mgw__jzpl.indptr = mdz__sidpc
        mgw__jzpl.shape = ckdaz__ttq
        context.nrt.incref(builder, signature.args[0], hkqg__hood)
        context.nrt.incref(builder, signature.args[1], pqxoj__ztgh)
        context.nrt.incref(builder, signature.args[2], mdz__sidpc)
        return mgw__jzpl._getvalue()
    sao__bklu = CSRMatrixType(data_t.dtype, indices_t.dtype)
    xnbts__bve = sao__bklu(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return xnbts__bve, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    mgw__jzpl = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ggd__yadnc = c.pyapi.object_getattr_string(val, 'data')
    pxi__hzhn = c.pyapi.object_getattr_string(val, 'indices')
    ujtd__ulzf = c.pyapi.object_getattr_string(val, 'indptr')
    xlu__twx = c.pyapi.object_getattr_string(val, 'shape')
    mgw__jzpl.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'),
        ggd__yadnc).value
    mgw__jzpl.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), pxi__hzhn).value
    mgw__jzpl.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), ujtd__ulzf).value
    mgw__jzpl.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 2
        ), xlu__twx).value
    c.pyapi.decref(ggd__yadnc)
    c.pyapi.decref(pxi__hzhn)
    c.pyapi.decref(ujtd__ulzf)
    c.pyapi.decref(xlu__twx)
    uekt__cruz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mgw__jzpl._getvalue(), is_error=uekt__cruz)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    dgj__zns = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    nue__mmls = c.pyapi.import_module_noblock(dgj__zns)
    mgw__jzpl = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        mgw__jzpl.data)
    ggd__yadnc = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        mgw__jzpl.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        mgw__jzpl.indices)
    pxi__hzhn = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), mgw__jzpl.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        mgw__jzpl.indptr)
    ujtd__ulzf = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), mgw__jzpl.indptr, c.env_manager)
    xlu__twx = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        mgw__jzpl.shape, c.env_manager)
    rbyu__wbr = c.pyapi.tuple_pack([ggd__yadnc, pxi__hzhn, ujtd__ulzf])
    rcm__cimsx = c.pyapi.call_method(nue__mmls, 'csr_matrix', (rbyu__wbr,
        xlu__twx))
    c.pyapi.decref(rbyu__wbr)
    c.pyapi.decref(ggd__yadnc)
    c.pyapi.decref(pxi__hzhn)
    c.pyapi.decref(ujtd__ulzf)
    c.pyapi.decref(xlu__twx)
    c.pyapi.decref(nue__mmls)
    c.context.nrt.decref(c.builder, typ, val)
    return rcm__cimsx


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
    cto__yxzqu = A.dtype
    jvvqd__nngc = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            oqhzz__ufegv, mabb__qhye = A.shape
            uoclc__ggaqn = numba.cpython.unicode._normalize_slice(idx[0],
                oqhzz__ufegv)
            ojx__flu = numba.cpython.unicode._normalize_slice(idx[1],
                mabb__qhye)
            if uoclc__ggaqn.step != 1 or ojx__flu.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            ialdy__glkg = uoclc__ggaqn.start
            tsd__acu = uoclc__ggaqn.stop
            zgv__gutiz = ojx__flu.start
            mfg__sbd = ojx__flu.stop
            bfbx__keojm = A.indptr
            aff__kxz = A.indices
            ihlqq__bmai = A.data
            bvpcg__wfle = tsd__acu - ialdy__glkg
            uwjp__funod = mfg__sbd - zgv__gutiz
            zuhum__lwrw = 0
            tyh__kfkn = 0
            for ebxuc__nrf in range(bvpcg__wfle):
                gugf__tznds = bfbx__keojm[ialdy__glkg + ebxuc__nrf]
                wun__kpskp = bfbx__keojm[ialdy__glkg + ebxuc__nrf + 1]
                for lzk__ned in range(gugf__tznds, wun__kpskp):
                    if aff__kxz[lzk__ned] >= zgv__gutiz and aff__kxz[lzk__ned
                        ] < mfg__sbd:
                        zuhum__lwrw += 1
            aqmu__lvvy = np.empty(bvpcg__wfle + 1, jvvqd__nngc)
            ogjs__vqvvq = np.empty(zuhum__lwrw, jvvqd__nngc)
            lexj__mmxaj = np.empty(zuhum__lwrw, cto__yxzqu)
            aqmu__lvvy[0] = 0
            for ebxuc__nrf in range(bvpcg__wfle):
                gugf__tznds = bfbx__keojm[ialdy__glkg + ebxuc__nrf]
                wun__kpskp = bfbx__keojm[ialdy__glkg + ebxuc__nrf + 1]
                for lzk__ned in range(gugf__tznds, wun__kpskp):
                    if aff__kxz[lzk__ned] >= zgv__gutiz and aff__kxz[lzk__ned
                        ] < mfg__sbd:
                        ogjs__vqvvq[tyh__kfkn] = aff__kxz[lzk__ned
                            ] - zgv__gutiz
                        lexj__mmxaj[tyh__kfkn] = ihlqq__bmai[lzk__ned]
                        tyh__kfkn += 1
                aqmu__lvvy[ebxuc__nrf + 1] = tyh__kfkn
            return init_csr_matrix(lexj__mmxaj, ogjs__vqvvq, aqmu__lvvy, (
                bvpcg__wfle, uwjp__funod))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
