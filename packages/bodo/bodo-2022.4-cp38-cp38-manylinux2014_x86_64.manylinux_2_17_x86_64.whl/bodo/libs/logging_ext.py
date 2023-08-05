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
    eqoi__tztg = context.get_python_api(builder)
    return eqoi__tztg.unserialize(eqoi__tztg.serialize_object(pyval))


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
        abn__ipvp = ', '.join('e{}'.format(pnv__nznfi) for pnv__nznfi in
            range(len(args)))
        if abn__ipvp:
            abn__ipvp += ', '
        fyrld__ixsbe = ', '.join("{} = ''".format(jaxel__otj) for
            jaxel__otj in kws.keys())
        zxss__zaq = f'def format_stub(string, {abn__ipvp} {fyrld__ixsbe}):\n'
        zxss__zaq += '    pass\n'
        fnxb__gukt = {}
        exec(zxss__zaq, {}, fnxb__gukt)
        jobgh__vixdi = fnxb__gukt['format_stub']
        npc__aogrx = numba.core.utils.pysignature(jobgh__vixdi)
        womkv__bri = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, womkv__bri).replace(pysig=npc__aogrx)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for mce__xafo in ('logging.Logger', 'logging.RootLogger'):
        for blbi__ymkp in func_names:
            tbvms__vazt = f'@bound_function("{mce__xafo}.{blbi__ymkp}")\n'
            tbvms__vazt += (
                f'def resolve_{blbi__ymkp}(self, logger_typ, args, kws):\n')
            tbvms__vazt += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(tbvms__vazt)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for ohhi__njpm in logging_logger_unsupported_attrs:
        qmp__nvjd = 'logging.Logger.' + ohhi__njpm
        overload_attribute(LoggingLoggerType, ohhi__njpm)(
            create_unsupported_overload(qmp__nvjd))
    for wfyef__wpu in logging_logger_unsupported_methods:
        qmp__nvjd = 'logging.Logger.' + wfyef__wpu
        overload_method(LoggingLoggerType, wfyef__wpu)(
            create_unsupported_overload(qmp__nvjd))


_install_logging_logger_unsupported_objects()
