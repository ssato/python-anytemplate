#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""Module to keep backward compatibilities.
"""
from __future__ import absolute_import

import codecs
import itertools
import locale
import sys


IS_PYTHON_3 = sys.version_info[0] == 3
ENCODING = locale.getdefaultlocale()[1]


# Borrowed from library doc, 9.7.1 Itertools functions:
def _from_iterable(iterables):
    """
    itertools.chain.from_iterable alternative.

    >>> list(_from_iterable([[1, 2], [3, 4]]))
    [1, 2, 3, 4]
    """
    for it in iterables:
        for element in it:
            yield element


if IS_PYTHON_3:
    from_iterable = itertools.chain.from_iterable
    # pylint: disable=redefined-builtin
    raw_input = input
    # pylint: enable=redefined-builtin

    def copen(filepath, flag='r', encoding=ENCODING):
        return codecs.open(filepath, flag + 'b', encoding)
else:
    try:
        from_iterable = itertools.chain.from_iterable
    except AttributeError:
        from_iterable = _from_iterable

    raw_input = raw_input

    def copen(filepath, flag='r', encoding=ENCODING):
        """
        FIXME: How to test this ?

        >>> c = copen(__file__)
        >>> c is not None
        True
        """
        return codecs.open(filepath, flag, encoding)

# vim:sw=4:ts=4:et:
