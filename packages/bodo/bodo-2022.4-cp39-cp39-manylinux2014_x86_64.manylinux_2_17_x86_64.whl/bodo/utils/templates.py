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
            hsmlt__fqaq = set()
            xvg__dwymn = list(self.context._get_attribute_templates(self.key))
            swgw__cge = xvg__dwymn.index(self) + 1
            for xbil__rnk in range(swgw__cge, len(xvg__dwymn)):
                if isinstance(xvg__dwymn[xbil__rnk], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    hsmlt__fqaq.add(xvg__dwymn[xbil__rnk]._attr)
            self._attr_set = hsmlt__fqaq
        return attr_name in self._attr_set
