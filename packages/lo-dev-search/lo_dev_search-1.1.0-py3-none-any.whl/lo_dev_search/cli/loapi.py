# coding: utf-8
# region Imports
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Union
from lo_dev_search.api_data.ooo_type import OooType
from ..api_search import search_api
from ..data_class.component import Component
from ..data_class.module_info import ModuleInfo
from ..web_search import __mod_path__
# endregion Imports

# region Internal Func


def _browse(url: str) -> None:
    # opening in subprocess prevents extra output to termnial.
    cmd = [sys.executable, str(Path(__mod_path__, "browse.py")), url]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# endregion Internal Func

# region Terminal Questions


def query_comp_choice(comps: List[Component]) -> Union[int, None]:
    """
    Ask for a choice of which component to open url for.

    Arguments:
        comps (List[Component]): List of components to choose from.

    Returns:
        (Union[int, None]): Integer representing the zero base index within comps or None if canceled.
    """
    # https://tinyurl.com/yyg38fp2
    # https://tinyurl.com/y2pv2cdh
    c_len = len(comps)
    # valid is 1 to length of comps + 1 for None
    valid = tuple([i for i in range(1, c_len + 1)])
    question = 'Choose an option (default 1):'
    prompt = f'\n{"[0],":<5} Cancel'
    for i, comp in enumerate(comps, 1):
        prompt = prompt + \
            f"\n{f'[{i}],':<5} {comp.name:<33} - {comp.id_component:<55} - {comp.type}"
        i += 1
    prompt += '\n'
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice == '':
            return 0
        if choice == 'q':
            return None
        if choice.isdigit():
            j = int(choice)
        else:
            j = -1
        if j == 0:
            return None
        if j in valid:
            return j - 1
        else:
            sys.stdout.write(f"Please respond with input from 0 - {c_len}\n")


def query_mod_choice(infos: List[ModuleInfo]) -> Union[int, None]:
    """
    Ask for a choice of which ModuleInfo to open url for.

    Arguments:
        comps (List[ModuleInfo]): List of ModuleInfo to choose from.

    Returns:
        (Union[int, None]): Integer representing the zero base index within comps or None if canceled.
    """
    c_len = len(infos)
    # valid is 1 to length of infos + 1 for None
    valid = tuple([i for i in range(1, c_len + 1)])
    question = 'Choose an option (default 1):'
    prompt = f'\n{"[0],":<5} Cancel'
    for i, info in enumerate(infos, 1):
        prompt = prompt + \
            f"\n{f'[{i}],':<5} {info.id_module_info}"
        i += 1
    prompt += '\n'
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice == '':
            return 0
        if choice == 'q':
            return None
        if choice.isdigit():
            j = int(choice)
        else:
            j = -1
        if j == 0:
            return None
        if j in valid:
            return j - 1
        else:
            sys.stdout.write(f"Please respond with input from 0 - {c_len}\n")
# endregion Terminal Questions

# region Parser

# region Parser Args


def _args_comp(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-s', '--search',
        help=f"",
        action='store',
        dest='search',
        required=True
    )
    parser.add_argument(
        '-b', '--no-before',
        help="No leading wildcard in search",
        action='store_false',
        dest='leading',
        default=True
    )
    parser.add_argument(
        '-a', '--no-after',
        help="No trailing wildcard in search",
        action='store_false',
        dest='trailing',
        default=True
    )
    parser.add_argument(
        '-m', '--max-results',
        help="Limits the number of results returned: Default (default: %(default)s)",
        action='store',
        dest='limit',
        type=int,
        default=10
    )
    parser.add_argument(
        '-t',
        '--component-type',
        default='any',
        const='any',
        nargs='?',
        dest='component_type',
        choices=['any', 'const', 'enum', 'exception', 'interface',
                 'singleton', 'service', 'struct', 'typedef'],
        help="Select type of component (default: %(default)s)")


def _args_mod(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-s', '--search',
        help=f"",
        action='store',
        dest='search',
        required=True
    )
    parser.add_argument(
        '-b', '--no-before',
        help="No leading wildcard in search",
        action='store_false',
        dest='leading',
        default=True
    )
    parser.add_argument(
        '-a', '--no-after',
        help="No trailing wildcard in search",
        action='store_false',
        dest='trailing',
        default=True
    )
    parser.add_argument(
        '-m', '--max-results',
        help="Limits the number of results returned: Default (default: %(default)s)",
        action='store',
        dest='limit',
        type=int,
        default=10
    )
# endregion Parser Args

# region Parser Actions


def _args_comp_action(args: argparse.Namespace) -> int:
    search = "%".join(str(args.search).split())
    if len(search) <= 2:
        print("Search requires at least 3 characters")
        return 0
    if args.leading:
        search = "%" + search
    if args.trailing:
        search = search + '%'
    if args.component_type == "any":
        o_type = None
    else:
        o_type = OooType(args.component_type)
    results = search_api.search_component(
        search=search, type=o_type, limit=int(args.limit))
    if len(results) == 0:
        print('Search produced no results')
        return 0
    choice = query_comp_choice(results)
    if choice is not None:
        url = results[choice].url
        _browse(url)
    return 0


def _args_mod_action(args: argparse.Namespace) -> int:
    search = "%".join(str(args.search).split())
    if len(search) <= 2:
        print("Search requires at least 3 characters")
        return 0
    if args.leading:
        search = "%" + search
    if args.trailing:
        search = search + '%'
    results = search_api.search_module_info(search, limit=int(args.limit))
    if len(results) == 0:
        print('Search produced no results')
        return 0
    choice = query_mod_choice(results)
    if choice is not None:
        md = results[choice]
        s = "_1_1".join(md.id_module_info.split('.'))
        url = f"{md.url_base}/namespace{s}.html"
        _browse(url)
    return 0
# endregion Parser Actions

# region Parser Command Process


def _args_process_cmd(args: argparse.Namespace) -> int:
    if args.command == "comp":
        return _args_comp_action(args)
    elif args.command == "ns":
        return _args_mod_action(args)
    return 0
# endregion Parser Command Process

# endregion Parser


def main() -> int:
    parser = argparse.ArgumentParser(description='main')
    subparser = parser.add_subparsers(dest="command")
    cmd_comp = subparser.add_parser(
        name="comp", help="Search for components")
    cmd_mod = subparser.add_parser(
        name="ns", help="Search for Namspace")
    _args_comp(cmd_comp)
    _args_mod(cmd_mod)
    if len(sys.argv) <= 1:
        parser.print_help()
        return 0
    args = parser.parse_args()
    # print(args)
    _args_process_cmd(args)

    return 0
