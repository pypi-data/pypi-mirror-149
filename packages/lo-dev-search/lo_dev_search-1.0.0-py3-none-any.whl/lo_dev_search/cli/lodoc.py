#!/usr/bin/env python
# coding: utf-8
import sys
from ..web_search import search_lo_doc

def _display_help() -> None:
    help="""Search LibreOffice API.
    Use prefixes such as: writer, draw, impress, base, calc, chart2.
    Example:
        lodoc text module
        lodoc text service
        lodoc xtext
        lodoc Impress
        """
    print(help)

def main() -> int:
    search = sys.argv[1:] 
    search_len = len(search)
    if search_len == 0:
        _display_help()
        return 0

    arg1 = str(search.pop(0))
    if arg1.lower() in ('-h', '--help'):
        _display_help()
        return 0
    arg2 = "" if search_len < 2 else search.pop(0)
    arg3 = "" if search_len < 3 else " ".join(search)
    search_lo_doc.search(arg1=arg1, arg2=arg2, arg3=arg3)
    return 0

# if __name__ == "__main__":
#     raise SystemExit(main())