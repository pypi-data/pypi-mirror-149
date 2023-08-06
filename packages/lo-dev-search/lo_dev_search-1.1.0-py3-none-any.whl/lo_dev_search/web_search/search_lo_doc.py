# coding: utf-8
import sys
from pathlib import Path
import subprocess
from ..utils import util
_PATH = str(Path(__file__).parent)


def search(arg1: str, arg2="", arg3="", verbatium: bool = True) -> None:
    """
    Searches the supplied search engine and narrows search to LibreOffice API.

    Args:
        arg1 (str):First keyword in search. Can be specific string such as writer, draw,
            impress, calc, chart2, base.
        arg2 (str, optional): Second Keyword in search.
        arg3 (str, optional): contains any other search terms.
    """
    # quoting is necessary for some search engines.
    # For instance google sometimes will change results if thinks a word is mispelled

    def get_txt(s: str) -> str:
        if s == '':
            return s
        if len(s.split()) == 1:
            st = s.strip("'").strip('"')
            return f'"{st}"'
        return s
    
    s1 = arg1
    s2 = arg2
    s3 = arg3
    ss = arg1.lower()
    auto_assigned = False
    if ss == '':
        print('Nothing to search!')
        return

    if ss == 'writer':
        if arg2 == "":
            s1 = "text"
            s2 = "module"
            auto_assigned = True
    elif ss == 'draw':
        if arg2 == "":
            s1 = "drawing"
            s2 = "module"
    elif ss == 'impress':
        if arg2 == "":
            s1 = "presentation"
            s2 = "module"
            auto_assigned = True
    elif ss == 'calc':
        if arg2 == "":
            s1 = "sheet"
            s2 = "module"
            auto_assigned = True
    elif ss == 'chart2':
        if arg2 == "":
            s1 = "chart2"
            s2 = "module"
            auto_assigned = True
    elif ss == 'base':
        if arg2 == "":
            s1 = "sdbc"
            s2 = "module"
            auto_assigned = True
    if not ss.startswith('x'):
        if s2 == "":
            print("Consider adding 'service' or 'module' to the search args")

    if verbatium:
        if auto_assigned is True:
            stxt = f"{get_txt(s1)} AND {get_txt(s2)} AND {get_txt(s3)}"
        else:
            stxt = get_txt(s1)
            quoted = stxt.endswith('"')
            if s2 != '':
                if quoted:
                    stxt += f" AND {get_txt(s2)}"
                else:
                    stxt += f" {get_txt(s2)}"
                quoted = stxt.endswith('"')
            if s3 != '':
                if quoted:
                    stxt += f" AND {get_txt(s3)}"
                else:
                    stxt += f" {get_txt(s3)}"
    else:
        stxt = f"{s1} {s2} {s3}".rstrip()
    print(f"Searching LO docs for {stxt}")
    config = util.get_app_cfg()
    url = config.lodoc_search.format(stxt)
    # opening in subprocess prevents extra output to termnial.
    cmd = [sys.executable, str(Path(_PATH, "browse.py")) ,url]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
