"""
Helper functions and classes to simplify Template Generation
for Bodo classes.
"""
import numba
from numba.core.typing.templates import AttributeTemplate


class OverloadedKeyAttributeTemplate(AttributeTemplate):
    _attr_set = None

    def _is_existing_attr(self, attr_name):
        if self._attr_set is None:
            qxl__cybo = set()
            euj__gijp = list(self.context._get_attribute_templates(self.key))
            zra__xhb = euj__gijp.index(self) + 1
            for yhok__dkci in range(zra__xhb, len(euj__gijp)):
                if isinstance(euj__gijp[yhok__dkci], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    qxl__cybo.add(euj__gijp[yhok__dkci]._attr)
            self._attr_set = qxl__cybo
        return attr_name in self._attr_set
