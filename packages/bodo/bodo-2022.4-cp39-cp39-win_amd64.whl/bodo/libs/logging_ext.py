"""
JIT support for Python's logging module
"""
import logging
import numba
from numba.core import types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import bound_function
from numba.core.typing.templates import AttributeTemplate, infer_getattr, signature
from numba.extending import NativeValue, box, models, overload_attribute, overload_method, register_model, typeof_impl, unbox
from bodo.utils.typing import create_unsupported_overload, gen_objmode_attr_overload


class LoggingLoggerType(types.Type):

    def __init__(self, is_root=False):
        self.is_root = is_root
        super(LoggingLoggerType, self).__init__(name=
            f'LoggingLoggerType(is_root={is_root})')


@typeof_impl.register(logging.RootLogger)
@typeof_impl.register(logging.Logger)
def typeof_logging(val, c):
    if isinstance(val, logging.RootLogger):
        return LoggingLoggerType(is_root=True)
    else:
        return LoggingLoggerType(is_root=False)


register_model(LoggingLoggerType)(models.OpaqueModel)


@box(LoggingLoggerType)
def box_logging_logger(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(LoggingLoggerType)
def unbox_logging_logger(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@lower_constant(LoggingLoggerType)
def lower_constant_logger(context, builder, ty, pyval):
    cxkh__vvcwt = context.get_python_api(builder)
    return cxkh__vvcwt.unserialize(cxkh__vvcwt.serialize_object(pyval))


gen_objmode_attr_overload(LoggingLoggerType, 'level', None, types.int64)
gen_objmode_attr_overload(LoggingLoggerType, 'name', None, 'unicode_type')
gen_objmode_attr_overload(LoggingLoggerType, 'propagate', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'disabled', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'parent', None,
    LoggingLoggerType())
gen_objmode_attr_overload(LoggingLoggerType, 'root', None,
    LoggingLoggerType(is_root=True))


@infer_getattr
class LoggingLoggerAttribute(AttributeTemplate):
    key = LoggingLoggerType

    def _resolve_helper(self, logger_typ, args, kws):
        kws = dict(kws)
        zaecv__kiau = ', '.join('e{}'.format(qwzsd__wmdjf) for qwzsd__wmdjf in
            range(len(args)))
        if zaecv__kiau:
            zaecv__kiau += ', '
        pyie__ogfm = ', '.join("{} = ''".format(yfyqf__puqe) for
            yfyqf__puqe in kws.keys())
        qvcf__vil = f'def format_stub(string, {zaecv__kiau} {pyie__ogfm}):\n'
        qvcf__vil += '    pass\n'
        vqrk__dvesy = {}
        exec(qvcf__vil, {}, vqrk__dvesy)
        rmxo__imkia = vqrk__dvesy['format_stub']
        efo__rolws = numba.core.utils.pysignature(rmxo__imkia)
        ftipl__glsj = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, ftipl__glsj).replace(pysig=efo__rolws)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for uypn__wuqlx in ('logging.Logger', 'logging.RootLogger'):
        for hnqbi__mxm in func_names:
            dbh__hfy = f'@bound_function("{uypn__wuqlx}.{hnqbi__mxm}")\n'
            dbh__hfy += (
                f'def resolve_{hnqbi__mxm}(self, logger_typ, args, kws):\n')
            dbh__hfy += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(dbh__hfy)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for bjhrd__zkfw in logging_logger_unsupported_attrs:
        aulrm__oubfa = 'logging.Logger.' + bjhrd__zkfw
        overload_attribute(LoggingLoggerType, bjhrd__zkfw)(
            create_unsupported_overload(aulrm__oubfa))
    for pskz__yzt in logging_logger_unsupported_methods:
        aulrm__oubfa = 'logging.Logger.' + pskz__yzt
        overload_method(LoggingLoggerType, pskz__yzt)(
            create_unsupported_overload(aulrm__oubfa))


_install_logging_logger_unsupported_objects()
