#
# Copyright (C). 2016 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import sys
import unittest


class Test(unittest.TestCase):

    def test_10_nullhandler(self):
        cls = "NullHandler"
        sys.modules["logging"] = None
        import anytemplate.globals

        self.assertFalse(cls in globals())
        self.assertFalse(getattr(anytemplate.globals, cls) is None)

    def test_20_engines(self):
        for mod in ("Cheetah", "jinja2", "mako", "tenjin", "pystache"):
            sys.modules[mod] = None
            import anytemplate.engine

            self.assertTrue(sys.modules[mod] is None)
            self.assertFalse(anytemplate.engine is None)

# vim:sw=4:ts=4:et:
