# coding: utf-8
import os
from pathlib import Path
from ..db import __api_db__


class DbConnect:
    def __init__(self) -> None:
        self._conn = __api_db__

    @property
    def connection_str(self) -> str:
        """Gets connection_str value"""
        return self._conn

