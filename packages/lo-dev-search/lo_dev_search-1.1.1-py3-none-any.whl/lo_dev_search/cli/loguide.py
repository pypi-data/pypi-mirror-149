#!/usr/bin/env python
# coding: utf-8
# region Imports
import argparse
from ..web_search.search_guide import search, SearchDevEnum
# endregion Imports

# region Interanl Func


def _get_help(app_name: str) -> str:
    return f"Search {app_name} developer guide for supplied search terms."
# endregion Interanl Func

# region parser
# region    Add Arguments


def _args_cmd_writer(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('search', nargs='*', help=_get_help("Writer"))
    parser.add_argument(
        "-v",
        "--no-verbatim",
        help="Non verbatim search",
        action="store_false",
        dest="verbatim",
        default=True,
    )


def _args_cmd_calc(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('search', nargs='*', help=_get_help("Calc"))
    parser.add_argument(
        "-v",
        "--no-verbatim",
        help="Non verbatim search",
        action="store_false",
        dest="verbatim",
        default=True,
    )


def _args_cmd_draw(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('search', nargs='*', help=_get_help("Draw"))
    parser.add_argument(
        "-v",
        "--no-verbatim",
        help="Non verbatim search",
        action="store_false",
        dest="verbatim",
        default=True,
    )


def _args_cmd_impress(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('search', nargs='*', help=_get_help("Impress"))
    parser.add_argument(
        "-v",
        "--no-verbatim",
        help="Non verbatim search",
        action="store_false",
        dest="verbatim",
        default=True,
    )


def _args_cmd_chart(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('search', nargs='*', help=_get_help("Chart"))
    parser.add_argument(
        "-v",
        "--no-verbatim",
        help="Non verbatim search",
        action="store_false",
        dest="verbatim",
        default=True,
    )


def _args_cmd_base(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('search', nargs='*', help=_get_help("Base"))
    parser.add_argument(
        "-v",
        "--no-verbatim",
        help="Non verbatim search",
        action="store_false",
        dest="verbatim",
        default=True,
    )


def _args_cmd_form(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('search', nargs='*', help=_get_help("Form"))
    parser.add_argument(
        "-v",
        "--no-verbatim",
        help="Non verbatim search",
        action="store_false",
        dest="verbatim",
        default=True,
    )


def _args_cmd_general(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'search', nargs='*', help="Search developer guide for supplied search terms.")
    parser.add_argument(
        "-v",
        "--no-verbatim",
        help="Non verbatim search",
        action="store_false",
        dest="verbatim",
        default=True,
    )
# endregion    Add Arguments


def _args_process_cmd(
    args: argparse.Namespace
) -> None:
    def get_search():
        return " ".join(args.search)
    if args.command == "writer":
        search(SearchDevEnum.WRITER, get_search(), bool(args.verbatim))
    elif args.command == "calc":
        search(SearchDevEnum.CALC, get_search(), bool(args.verbatim))
    elif args.command == "draw":
        search(SearchDevEnum.DRAW, get_search(), bool(args.verbatim))
    elif args.command == "impress":
        search(SearchDevEnum.IMPRESS, get_search(), bool(args.verbatim))
    elif args.command == "chart":
        search(SearchDevEnum.CHART, get_search(), bool(args.verbatim))
    elif args.command == "base":
        search(SearchDevEnum.BASE, get_search(), bool(args.verbatim))
    elif args.command == "form":
        search(SearchDevEnum.FORM, get_search(), bool(args.verbatim))
    elif args.command == "general":
        search(SearchDevEnum.DEV, get_search(), bool(args.verbatim))
# endregion parser

# region main()


def main() -> int:
    parser = argparse.ArgumentParser(description='main')
    subparser = parser.add_subparsers(dest="command")
    cmd_writer = subparser.add_parser(
        name="writer", help="Search Writer developer guide")
    cmd_calc = subparser.add_parser(
        name="calc", help="Search Calc developer guide")
    cmd_draw = subparser.add_parser(
        name="draw", help="Search Draw developer guide")
    cmd_impress = subparser.add_parser(
        name="impress", help="Search Impress developer guide")
    cmd_chart = subparser.add_parser(
        name="chart", help="Search Chart developer guide")
    cmd_base = subparser.add_parser(
        name="base", help="Search Base developer guide")
    cmd_form = subparser.add_parser(
        name="form", help="Search Form developer guide")
    cmd_general = subparser.add_parser(
        name="general", help="Search all of developer guide")
    _args_cmd_writer(cmd_writer)
    _args_cmd_calc(cmd_calc)
    _args_cmd_draw(cmd_draw)
    _args_cmd_impress(cmd_impress)
    _args_cmd_chart(cmd_chart)
    _args_cmd_base(cmd_base)
    _args_cmd_form(cmd_form)
    _args_cmd_general(cmd_general)

    args = parser.parse_args()
    if args.command is None:
        search(SearchDevEnum.NONE)
        # parser.print_help()
        return 0
    _args_process_cmd(args)
    # print(args)
    return 0
# endregion main()
