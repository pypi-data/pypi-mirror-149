# coding: utf-8
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True, eq=True)
class Component:
    id_component: str
    name: str
    namespace: str
    type: str
    version: str
    lo_ver: str
    file: str
    c_name: str
    url: str
    map_name: Union[str, None] = None
    sort: int = -1

    def __lt__(self, other: object):
        if not isinstance(other, Component):
            return NotImplemented
        return self.sort < other.sort
