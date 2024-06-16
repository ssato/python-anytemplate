#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, protected-access
from __future__ import absolute_import

import anytemplate.engine as TT
import anytemplate.engines.strtemplate as strtemplate


def test_find_by_filename():
    strtemplate.Engine._file_extensions.append("t")
    assert strtemplate.Engine in TT.find_by_filename("foo.t")
    strtemplate.Engine._file_extensions.remove("t")


def test_find_by_name__found():
    assert TT.find_by_name("string.Template") == strtemplate.Engine


def test_find_by_name__not_found():
    assert TT.find_by_name("not_existing_engine") is None

# vim:sw=4:ts=4:et:
