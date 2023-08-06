# coding: utf-8
# region Imports
import sys
from ..web_search import search_lo_doc
# endregion Imports

# region interal Func


def _display_help() -> None:
    help = """Search LibreOffice API.
    Option -h, --help, Displays this help
    Option -v, --no-verbatim, for a non verbatim search.
    Use prefixes such as: writer, draw, impress, base, calc, chart2.
    Example:
        lodoc text module
        lodoc -v text module
        lodoc text service
        lodoc xtext
        lodoc Impress
        """
    print(help)
# endregion interal Func

# region main()


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
    if arg1.lower() in ('-v', '--no-verbatim'):
        verbatim = False
        arg1 = str(search.pop(0))
    else:
        verbatim = True
    arg2 = "" if search_len < 2 else search.pop(0)
    arg3 = "" if search_len < 3 else " ".join(search)
    search_lo_doc.search(arg1=arg1, arg2=arg2, arg3=arg3, verbatim=verbatim)
    return 0
# endregion main()
