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
    oqgd__eegk = context.get_python_api(builder)
    return oqgd__eegk.unserialize(oqgd__eegk.serialize_object(pyval))


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
        pox__dqpc = ', '.join('e{}'.format(suqub__mkgi) for suqub__mkgi in
            range(len(args)))
        if pox__dqpc:
            pox__dqpc += ', '
        ofvd__avp = ', '.join("{} = ''".format(ynb__jfc) for ynb__jfc in
            kws.keys())
        xbk__ejo = f'def format_stub(string, {pox__dqpc} {ofvd__avp}):\n'
        xbk__ejo += '    pass\n'
        qndzm__ouyuh = {}
        exec(xbk__ejo, {}, qndzm__ouyuh)
        mqyex__ogcab = qndzm__ouyuh['format_stub']
        antam__zqb = numba.core.utils.pysignature(mqyex__ogcab)
        gyn__qbwwq = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, gyn__qbwwq).replace(pysig=antam__zqb)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for rqoqo__irtxv in ('logging.Logger', 'logging.RootLogger'):
        for blm__xhcg in func_names:
            ztdwr__fzcn = f'@bound_function("{rqoqo__irtxv}.{blm__xhcg}")\n'
            ztdwr__fzcn += (
                f'def resolve_{blm__xhcg}(self, logger_typ, args, kws):\n')
            ztdwr__fzcn += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(ztdwr__fzcn)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for erbie__nutls in logging_logger_unsupported_attrs:
        vsp__myj = 'logging.Logger.' + erbie__nutls
        overload_attribute(LoggingLoggerType, erbie__nutls)(
            create_unsupported_overload(vsp__myj))
    for ejlh__lfuvj in logging_logger_unsupported_methods:
        vsp__myj = 'logging.Logger.' + ejlh__lfuvj
        overload_method(LoggingLoggerType, ejlh__lfuvj)(
            create_unsupported_overload(vsp__myj))


_install_logging_logger_unsupported_objects()
