#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
#
import unittest

import anytemplate.engine as TT
import anytemplate.engines.jinja2
import anytemplate.engines.string


class Test_00(unittest.TestCase):

    def test_10_find_by_filename(self):
        if anytemplate.engines.jinja2.SUPPORTED:
            clss = TT.find_by_filename("foo.j2")
            self.assertTrue(anytemplate.engines.jinja2.Jjnja2Engine in clss)

    def test_20_find_by_name__found(self):
        self.assertEquals(TT.find_by_name("string.Template"),
                          anytemplate.engines.string.StringTemplateEngine)

        if anytemplate.engines.jinja2.SUPPORTED:
            self.assertEquals(TT.find_by_name("jinja2"),
                              anytemplate.engines.jinja2.Jjnja2Engine)

    def test_20_find_by_name__not_found(self):
        self.assertTrue(TT.find_by_name("not_existing_engine") is None)

# vim:sw=4:ts=4:et:
