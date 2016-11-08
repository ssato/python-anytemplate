#
# Copyright (C). 2016 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import sys
import unittest


class Test(unittest.TestCase):

    def test_10_nullhandler(self):
        cls = "NullHandler"
        sys.modules["logging"] = None
        import anytemplate.globals

        self.assertFalse(cls in globals())
        self.assertFalse(getattr(anytemplate.globals, cls) is None)

# vim:sw=4:ts=4:et:
