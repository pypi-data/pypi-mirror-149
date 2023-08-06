# coding: utf-8
import __main__
from pathlib import Path
from typing import List, Union, overload
from ..cfg import config

_APP_CFG = None


def get_app_cfg() -> config.AppConfig:
    """
    Get App Config. config is cached
    """
    global _APP_CFG
    if _APP_CFG is None:
        _APP_CFG = config.read_config_default()
    return _APP_CFG


@overload
def mkdirp(dest_dir: str) -> None:
    ...


@overload
def mkdirp(dest_dir: Path) -> None:
    ...


def mkdirp(dest_dir: Union[str, Path]) -> None:
    """
    Creates path and subpaths not existing.

    Args:
        dest_dir (Union[str, Path]): PathLike object

    Since:
        Python 3.5
    """
    # Python ≥ 3.5
    if isinstance(dest_dir, Path):
        dest_dir.mkdir(parents=True, exist_ok=True)
    else:
        Path(dest_dir).mkdir(parents=True, exist_ok=True)
