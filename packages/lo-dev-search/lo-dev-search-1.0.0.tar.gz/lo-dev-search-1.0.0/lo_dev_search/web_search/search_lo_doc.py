# coding: utf-8
import webbrowser
from ..utils import util

def search(arg1:str, arg2 = "", arg3 = ""):
    """
    Searches the supplied search engine and narrows search to LibreOffice API.

    Args:
        arg1 (str):First keyword in search. Can be specific string such as writer, draw,
            impress, calc, chart2, base.
        arg2 (str, optional): Second Keyword in search.
        arg3 (str, optional): contains any other search terms.
    """
    s1 = arg1
    s2 = arg2
    s3 = arg3
    ss = arg1.lower()
    if ss == 'writer':
        if arg2 == "":
            s1 = "text"
            s2 = "module"
    elif ss == 'draw':
        if arg2 == "":
            s1 = "drawing"
            s2 = "module"
    elif ss == 'impress':
        if arg2 == "":
            s1 = "presentation"
            s2 = "module"
    elif ss == 'calc':
        if arg2 == "":
            s1 = "sheet"
            s2 = "module"
    elif ss == 'chart2':
        if arg2 == "":
            s1 = "chart2"
            s2 = "module"
    elif ss == 'base':
        if arg2 == "":
            s1 = "sdbc"
            s2 = "module"
    if not ss.startswith('x'):
        if s2 == "":
            print("Consider adding 'service' or 'module' to the search args")
    stxt = f"{s1} {s2} {s3}".rstrip()
    print(f"Searching LO docs for {stxt}")
    config = util.get_app_cfg()
    url = config.lodoc_search.format(stxt)
    webbrowser.open(url)
