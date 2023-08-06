# coding: utf-8
from dataclasses import dataclass


@dataclass
class ModuleDetail:
    id_namespace: str
    name: str
    namespace: str
    href: str
    component_type: str
    sort: int = -1

    def __lt__(self, other: object):
        if not isinstance(other, ModuleDetail):
            return NotImplemented
        return self.sort < other.sort
