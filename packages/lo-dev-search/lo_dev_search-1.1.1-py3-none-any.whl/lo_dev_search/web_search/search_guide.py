# coding: utf-8
import sys
from enum import IntEnum, auto
from ..utils import util
from pathlib import Path
import subprocess
_PATH = str(Path(__file__).parent)

class SearchDevEnum(IntEnum):
    NONE = auto()
    DEV = auto()
    WRITER = auto()
    CALC = auto()
    DRAW = auto()
    CHART = auto()
    BASE = auto()
    FORM = auto()
    IMPRESS = auto()


def search_url_writer(search: str = '') -> str:
    config = util.get_app_cfg()
    if search == '':
        url = config.loguide_writer_url
    else:
        url = config.loguide_writer_search.format(search)
    return url

def search_url_calc(search: str = '') -> str:
    config = util.get_app_cfg()
    if search == '':
        url = config.loguide_calc_url
    else:
        url = config.loguide_calc_search.format(search)
    return url

def search_url_draw(search: str = '') -> str:
    config = util.get_app_cfg()
    if search == '':
        url = config.loguide_draw_url
    else:
        url = config.loguide_draw_search.format(search)
    return url

def search_url_chart(search: str = '') -> str:
    config = util.get_app_cfg()
    if search == '':
        url = config.loguide_chart_url
    else:
        url = config.loguide_chart_search.format(search)
    return url

def search_url_base(search: str = '') -> str:
    config = util.get_app_cfg()
    if search == '':
        url = config.loguide_base_url
    else:
        url = config.loguide_base_search.format(search)
    return url

def search_url_form(search: str = '') -> str:
    config = util.get_app_cfg()
    if search == '':
        url = config.loguide_form_url
    else:
        url = config.loguide_form_search.format(search)
    return url

def search_url_dev(search: str = '') -> str:
    config = util.get_app_cfg()
    if search == '':
        url = config.loguide_dev_url
    else:
        url = config.loguide_dev_search.format(search)
    return url

def _browse(url: str) -> None:
    # opening in subprocess prevents extra output to termnial.
    cmd = [sys.executable, str(Path(_PATH, "browse.py")), url]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def search(where: SearchDevEnum, search_str: str = '', verbatim: bool = True) -> None:
    # The drawing capabilities of Draw and Impress are identical.
    # https://tinyurl.com/y2pqyyv8
    def get_txt(s: str) -> str:
        if s == '':
            return s
        st = s.strip("'").strip('"')
        return f'"{st}"'
    if verbatim:
        s = get_txt(search_str)
    else:
        s = search_str
    if where == SearchDevEnum.BASE:
        _browse(search_url_base(s))
    elif where == SearchDevEnum.CALC:
        _browse(search_url_calc(s))
    elif where == SearchDevEnum.CHART:
        _browse(search_url_chart(s))
    elif where == SearchDevEnum.DRAW:
        _browse(search_url_draw(s))
    elif where == SearchDevEnum.IMPRESS:
        _browse(search_url_draw(s))
    elif where == SearchDevEnum.FORM:
        _browse(search_url_form(s))
    elif where == SearchDevEnum.WRITER:
        _browse(search_url_writer(s))
    elif where == SearchDevEnum.WRITER:
        _browse(search_url_dev(s))
    elif where == SearchDevEnum.DEV:
        _browse(search_url_dev(s))
    else:
        _browse(util.get_app_cfg().loguide_url)

