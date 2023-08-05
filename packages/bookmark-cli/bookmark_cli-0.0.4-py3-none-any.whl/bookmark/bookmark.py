#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
书签模块
"""

import os
import json
from typing import (
    List
)

__all__ = ['add_bookmark', 'list_bookmarks',
    'delete_bookmark']

BM_DB_PATH = os.path.expanduser('~/.bookmark')

class BookmarkException(Exception):
    """Bookmark base Exception"""
    pass

class BookmarkExistsException(BookmarkException):
    """书签已经存在的异常"""
    pass


class Bookmark(object):
    """书签类"""
    text: str
    tags: list = None

    def __init__(self, text: str, tags: list = None):
        """
        :text: 书签内容
        :tags: 标签

        """
        self.text = text
        if not tags:
            tags = []
        self.tags = tags

    def dict(self) -> dict:
        data = {}
        for key in self.__annotations__.keys():
            data[key] = getattr(self, key)
        return data

    def json(self) -> str:
        return json.dumps(self, default = lambda o: o.dict(), sort_keys = True)


def add_bookmark(text: str, tags=None):
    bm = _search_text(text)
    if bm:
        raise BookmarkExistsException(f"Bookmark '{text}' exists!")
    _add_bookmark(text, tags)

def _add_bookmark(text: str, tags: list=None):
    """添加书签"""
    bm = Bookmark(text, tags)
    with open(BM_DB_PATH, 'a') as f:
        f.write(bm.json())
        f.write('\n')

def _search_text(text: str) -> Bookmark:
    """搜索本文是否已经存在"""
    for bm in _list_bookmark():
        if bm.text == text:
            return bm
    return None

def list_bookmarks(tags: list = None) -> List[Bookmark]:
    return _list_bookmark(tags)

def _list_bookmark(tags: list=None) -> List[Bookmark]:
    """添加书签"""
    if not tags:
        tags = []
    with open(BM_DB_PATH, 'r') as f:
        lines = f.readlines()

    bookmarks = []
    for line in lines:
        if not line or line == '\n':
            continue
        bm = Bookmark(**json.loads(line))

        command_tags = [ o for o in tags if o in bm.tags ]
        add_flag1 = not tags
        add_flag2 = tags and command_tags
        is_add = add_flag1 or add_flag2

        if is_add:
            bookmarks.append(bm)
    return bookmarks


def delete_bookmark(text: str, tags: list=None) -> int:
    return _delete_bookmark(text, tags)

def _delete_bookmark(text: str, tags: list = None) -> int:
    """删除书签"""
    with open(BM_DB_PATH, 'r') as f:
        lines = f.readlines()
    new_lines = []
    count = 0
    for line in lines:
        if not line or line == '\n':
            continue
        bm = Bookmark(**json.loads(line))
        if bm.text == text:
            count += 1
            continue
        if line:
            new_lines.append(line)
    with open(BM_DB_PATH, 'w') as f:
        f.write('\n'.join(new_lines))
    return count

