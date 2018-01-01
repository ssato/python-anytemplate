#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# pylint: disable=invalid-name, redefined-builtin, unused-argument
"""Module to keep backward compatibilities.
"""
from __future__ import absolute_import

import codecs
import itertools
import locale
import os.path
import sys

try:
    import json
except ImportError:
    import simplejson as json  # :throw: ImportError


IS_PYTHON_3 = sys.version_info[0] == 3
ENCODING = locale.getdefaultlocale()[1] or "UTF-8"


# Borrowed from library doc, 9.7.1 Itertools functions:
def _from_iterable(iterables):
    """
    itertools.chain.from_iterable alternative.

    >>> list(_from_iterable([[1, 2], [3, 4]]))
    [1, 2, 3, 4]
    """
    for itr in iterables:
        for element in itr:
            yield element


def json_loads(content, *args, **kwargs):
    """
    Alternative if anyconfig is not available.

    :param content: JSON string
    """
    return json.loads(content)


def json_load(filepath, *args, **kwargs):
    """
    Alternative if anyconfig is not available.

    :param filepath: JSON file path
    """
    return json.load(open(filepath))


def get_file_extension(filepath):
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


def merge(dic, diff):
    """
    Merge mapping objects.

    :param dic: Original mapping object to update with `diff`
    :param diff: Diff mapping object
    :return: None but `dic` will be updated

    >>> dic = {}
    >>> merge(dic, {'a': 1})
    >>> assert 'a' in dic and dic['a'] == 1
    """
    dic.update(diff)


if IS_PYTHON_3:
    from_iterable = itertools.chain.from_iterable
    raw_input = input

    def copen(filepath, flag='r', encoding=ENCODING):
        """
        >>> c = copen(__file__)
        >>> c is not None
        True
        """
        return codecs.open(filepath, flag + 'b', encoding)
else:
    try:
        from_iterable = itertools.chain.from_iterable
    except AttributeError:
        from_iterable = _from_iterable

    raw_input = raw_input

    def copen(filepath, flag='r', encoding=ENCODING):
        """
        >>> c = copen(__file__)
        >>> c is not None
        True
        """
        return codecs.open(filepath, flag, encoding)

# vim:sw=4:ts=4:et:
