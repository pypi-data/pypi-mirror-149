#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

import argparse

from .bookmark import (
    add_bookmark,
    list_bookmarks,
    delete_bookmark,
    BookmarkException
)

USAGE = """bm [--tags TAGS [TAGS ...]] [-h]
          [cmd] [text]

bm add https://github.com/wxnacy/bookmark --tags github --tags bookmark
bm list
bm delete https://github.com/wxnacy/bookmark
"""

def init_argparse() -> argparse.ArgumentParser:
    """初始化命令参数"""
    parser = argparse.ArgumentParser(add_help = False, usage = USAGE)
    parser.add_argument('cmd', nargs='?')
    parser.add_argument('text', nargs='?', default='')
    parser.add_argument('--tags', nargs='+')
    parser.add_argument('-h', '--help', action='help',
        default=argparse.SUPPRESS, help='Show this help message and exit.')
    return parser

def add(arg: argparse.Namespace):
    try:
        add_bookmark(arg.text, arg.tags)
    except BookmarkException as e:
        print(str(e))
    except Exception as e:
        raise e
    else:
        print(f'Created bookmark \'{arg.text}\'')

def ls(arg: argparse.Namespace):
    bookmarks = list_bookmarks(arg.tags) or []
    for bm in bookmarks:
        print(bm.text)

def list(arg: argparse.Namespace):
    bookmarks = list_bookmarks(arg.tags) or []
    for bm in bookmarks:
        print(bm.text, ','.join(bm.tags))

def delete(arg: argparse.Namespace):
    count = delete_bookmark(arg.text)
    print(f'Delete {arg.text} count {count}')

def main():
    import sys
    parser = init_argparse()
    arg = parser.parse_args()
    #  print(arg.help)

    cmd = arg.cmd
    if not cmd:
        cmd = 'list'

    func = getattr(sys.modules[__name__], cmd)
    func(arg)

if __name__ == "__main__":
    main()
