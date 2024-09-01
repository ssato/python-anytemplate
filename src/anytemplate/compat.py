#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# pylint: disable=invalid-name, redefined-builtin, unused-argument
"""Module to keep backward compatibilities.
"""
from __future__ import absolute_import

import codecs
import os.path

try:
    from anyconfig.api import (  # pylint: disable=unused-import
        loads, load, merge
    )
except ImportError:
    import json

    def loads(content, **_kwargs):  # type: ignore[misc]
        """Wrapper for josn.loads."""
        return json.loads(content)

    def load(path_or_io, **_kwargs):  # type: ignore[misc]
        """Wrapper for josn.load."""
        if isinstance(path_or_io, (str, )):
            return json.load(open(path_or_io, encoding="utf-8"))

        return json.load(path_or_io)

    def merge(dic: dict, upd: dict, *_args, **_kwargs) -> None:  # type: ignore
        """Update `dic` with `upd`."""
        dic.update(upd)


ENCODING = "UTF-8"


def get_file_extension(filepath: str) -> str:
    """
    Copy if anyconfig.utils.get_file_extension is not available.

    >>> get_file_extension("/a/b/c")
    ''
    >>> get_file_extension("/a/b.txt")
    'txt'
    >>> get_file_extension("/a/b/c.tar.xz")
    'xz'
    """
    _ext = os.path.splitext(filepath)[-1]
    if _ext:
        return _ext[1:] if _ext.startswith('.') else _ext

    return ''


def json_loads(content: str, *_args, **kwargs) -> dict:
    """Wrapper for `loads`."""
    return loads(content, **kwargs) or {}


def json_load(filepath: str, *_args, **kwargs) -> dict:
    """Wrapper for `load`."""
    return load(filepath, **kwargs) or {}


def copen(filepath, flag='r', encoding=ENCODING):
    """
    >>> c = copen(__file__)
    >>> c is not None
    True
    """
    return codecs.open(filepath, flag + 'b', encoding)
