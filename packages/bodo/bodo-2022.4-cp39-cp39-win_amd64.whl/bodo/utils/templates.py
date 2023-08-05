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
            kubqt__cyyrg = set()
            iek__iiujk = list(self.context._get_attribute_templates(self.key))
            ryzus__mllwh = iek__iiujk.index(self) + 1
            for xhuf__oomi in range(ryzus__mllwh, len(iek__iiujk)):
                if isinstance(iek__iiujk[xhuf__oomi], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    kubqt__cyyrg.add(iek__iiujk[xhuf__oomi]._attr)
            self._attr_set = kubqt__cyyrg
        return attr_name in self._attr_set
