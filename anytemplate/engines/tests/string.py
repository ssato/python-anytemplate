#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import os.path
import unittest
import anytemplate.engines.string as TT
import anytemplate.tests.common


class Test_00(unittest.TestCase):

    def test_20_renders_impl(self):
        engine = TT.StringTemplateEngine()

        trs = (("aaa", None, "aaa"), ("$a", {'a': "aaa"}, "aaa"))
        for (tmpl_s, ctx, exp) in trs:
            self.assertEquals(engine.renders_impl(tmpl_s, ctx), exp)


class Test_10(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        if os.path.exists(self.workdir):
            anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_20_render_impl(self):
        engine = TT.StringTemplateEngine()

        trs = (("aaa", None, "aaa"), ("$a", {'a': "aaa"}, "aaa"))
        for (tmpl_s, ctx, exp) in trs:
            tmpl = os.path.join(self.workdir, "test.tmpl")
            open(tmpl, 'w').write(tmpl_s)

            self.assertEquals(engine.render_impl(tmpl, ctx), exp)

# vim:sw=4:ts=4:et:
