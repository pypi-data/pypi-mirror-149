# coding: utf-8
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class ModuleInfo:
    id_module_info: str
    url_base: str
    file: str
