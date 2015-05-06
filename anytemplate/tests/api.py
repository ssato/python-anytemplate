#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
#
import unittest

import anytemplate.api as TT
import anytemplate.compat
import anytemplate.engines.stringTemplate

from anytemplate.engine import find_by_name


class Test_00(unittest.TestCase):

    def test_10_find_engine_class__by_filepath(self):
        if find_by_name("jinja2"):
            import anytemplate.engines.jinja2

            cls = TT.find_engine_class("foo.j2")
            self.assertEquals(cls, anytemplate.engines.jinja2.Engine)

    def test_12_find_engine_class__by_name(self):
        cls = TT.find_engine_class("foo.t", "string.Template")
        self.assertEquals(cls, anytemplate.engines.stringTemplate.Engine)

    def test_20_renders__stringTemplate(self):
        self.assertEquals(TT.renders("$a", dict(a="aaa", ),
                                     at_engine="string.Template"),
                          "aaa")

    def test_22_renders__jinja2(self):
        if find_by_name("jinja2"):
            self.assertEquals(TT.renders("{{ a }}", dict(a="aaa", ),
                                         at_engine="jinja2"),
                              "aaa")

# vim:sw=4:ts=4:et:
