#
# Copyright (C). 2016 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import sys


def test_20_engines():
    for mod in ("Cheetah", "jinja2", "mako", "tenjin", "pystache"):
        sys.modules[mod] = None
        import anytemplate.engine

        assert sys.modules[mod] is None
        assert anytemplate.engine is not None
