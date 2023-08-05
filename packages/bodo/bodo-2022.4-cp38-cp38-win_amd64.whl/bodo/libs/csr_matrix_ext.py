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
        dzc__ryvqm = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, dzc__ryvqm)


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
        xmr__qpb, kjfuo__mcgw, blog__xzgcb, xrpnf__wnxe = args
        lqp__azkx = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        lqp__azkx.data = xmr__qpb
        lqp__azkx.indices = kjfuo__mcgw
        lqp__azkx.indptr = blog__xzgcb
        lqp__azkx.shape = xrpnf__wnxe
        context.nrt.incref(builder, signature.args[0], xmr__qpb)
        context.nrt.incref(builder, signature.args[1], kjfuo__mcgw)
        context.nrt.incref(builder, signature.args[2], blog__xzgcb)
        return lqp__azkx._getvalue()
    jbbxk__cpb = CSRMatrixType(data_t.dtype, indices_t.dtype)
    uctip__vvktz = jbbxk__cpb(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return uctip__vvktz, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    lqp__azkx = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hidm__delrw = c.pyapi.object_getattr_string(val, 'data')
    jis__gziu = c.pyapi.object_getattr_string(val, 'indices')
    whtuc__npqaw = c.pyapi.object_getattr_string(val, 'indptr')
    rju__mdv = c.pyapi.object_getattr_string(val, 'shape')
    lqp__azkx.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'),
        hidm__delrw).value
    lqp__azkx.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), jis__gziu).value
    lqp__azkx.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), whtuc__npqaw).value
    lqp__azkx.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 2
        ), rju__mdv).value
    c.pyapi.decref(hidm__delrw)
    c.pyapi.decref(jis__gziu)
    c.pyapi.decref(whtuc__npqaw)
    c.pyapi.decref(rju__mdv)
    rpdji__mpmg = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lqp__azkx._getvalue(), is_error=rpdji__mpmg)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    lcmdu__kktbl = c.context.insert_const_string(c.builder.module,
        'scipy.sparse')
    vdbrx__kwz = c.pyapi.import_module_noblock(lcmdu__kktbl)
    lqp__azkx = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        lqp__azkx.data)
    hidm__delrw = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        lqp__azkx.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        lqp__azkx.indices)
    jis__gziu = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), lqp__azkx.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        lqp__azkx.indptr)
    whtuc__npqaw = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), lqp__azkx.indptr, c.env_manager)
    rju__mdv = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        lqp__azkx.shape, c.env_manager)
    ymc__vadd = c.pyapi.tuple_pack([hidm__delrw, jis__gziu, whtuc__npqaw])
    pnr__whovf = c.pyapi.call_method(vdbrx__kwz, 'csr_matrix', (ymc__vadd,
        rju__mdv))
    c.pyapi.decref(ymc__vadd)
    c.pyapi.decref(hidm__delrw)
    c.pyapi.decref(jis__gziu)
    c.pyapi.decref(whtuc__npqaw)
    c.pyapi.decref(rju__mdv)
    c.pyapi.decref(vdbrx__kwz)
    c.context.nrt.decref(c.builder, typ, val)
    return pnr__whovf


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
    evp__qboe = A.dtype
    ccm__etcv = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            fxar__faom, wnqpc__raj = A.shape
            vkbb__vruqo = numba.cpython.unicode._normalize_slice(idx[0],
                fxar__faom)
            durls__jauc = numba.cpython.unicode._normalize_slice(idx[1],
                wnqpc__raj)
            if vkbb__vruqo.step != 1 or durls__jauc.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            rkdl__jqus = vkbb__vruqo.start
            req__xtfe = vkbb__vruqo.stop
            hdek__hhqdp = durls__jauc.start
            jvot__koog = durls__jauc.stop
            zccfj__ggmq = A.indptr
            daw__rjp = A.indices
            iljw__kdh = A.data
            mka__kdieu = req__xtfe - rkdl__jqus
            vysw__rrgs = jvot__koog - hdek__hhqdp
            olctg__powm = 0
            gykp__uxftp = 0
            for rjk__eutt in range(mka__kdieu):
                lnj__kojr = zccfj__ggmq[rkdl__jqus + rjk__eutt]
                tvbz__qmoll = zccfj__ggmq[rkdl__jqus + rjk__eutt + 1]
                for asonl__pmuhx in range(lnj__kojr, tvbz__qmoll):
                    if daw__rjp[asonl__pmuhx] >= hdek__hhqdp and daw__rjp[
                        asonl__pmuhx] < jvot__koog:
                        olctg__powm += 1
            wxh__aha = np.empty(mka__kdieu + 1, ccm__etcv)
            cabdi__rtbu = np.empty(olctg__powm, ccm__etcv)
            xekyq__usdht = np.empty(olctg__powm, evp__qboe)
            wxh__aha[0] = 0
            for rjk__eutt in range(mka__kdieu):
                lnj__kojr = zccfj__ggmq[rkdl__jqus + rjk__eutt]
                tvbz__qmoll = zccfj__ggmq[rkdl__jqus + rjk__eutt + 1]
                for asonl__pmuhx in range(lnj__kojr, tvbz__qmoll):
                    if daw__rjp[asonl__pmuhx] >= hdek__hhqdp and daw__rjp[
                        asonl__pmuhx] < jvot__koog:
                        cabdi__rtbu[gykp__uxftp] = daw__rjp[asonl__pmuhx
                            ] - hdek__hhqdp
                        xekyq__usdht[gykp__uxftp] = iljw__kdh[asonl__pmuhx]
                        gykp__uxftp += 1
                wxh__aha[rjk__eutt + 1] = gykp__uxftp
            return init_csr_matrix(xekyq__usdht, cabdi__rtbu, wxh__aha, (
                mka__kdieu, vysw__rrgs))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
