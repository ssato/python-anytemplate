#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
#
import unittest

import anytemplate.api as TT
import anytemplate.engines.jinja2
import anytemplate.compat


class Test_00(unittest.TestCase):

    def test_10_find_engine_class(self):
        if anytemplate.engines.jinja2.SUPPORTED:
            cls = TT.find_engine_class("foo.j2")
            self.assertEquals(cls, anytemplate.engines.jinja2.Jjnja2Engine)

    def test_20_renders(self):
        self.assertEquals(TT.renders("$a", dict(a="aaa", ),
                                     at_engine="string.Template"),
                          "aaa")

# vim:sw=4:ts=4:et:
