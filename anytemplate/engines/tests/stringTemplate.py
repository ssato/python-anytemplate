#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os.path
import unittest
import anytemplate.engines.stringTemplate as TT
import anytemplate.engines.base
import anytemplate.tests.common

from anytemplate.globals import CompileError


class Test00(unittest.TestCase):

    def test_20_renders_impl(self):
        engine = TT.Engine()

        trs = (("aaa", None, "aaa"), ("$a", {'a': "aaa"}, "aaa"))
        for (tmpl_s, ctx, exp) in trs:
            self.assertEquals(engine.renders_impl(tmpl_s, ctx), exp)

    def test_22_renders_impl__safe(self):
        engine = TT.Engine()
        self.assertEquals(engine.renders_impl("$a", {}, safe=True), "$a")

    def test_24_renders_impl__error(self):
        engine = TT.Engine()
        try:
            engine.renders_impl("$a", {})
            engine = None
        except CompileError:
            pass
        self.assertFalse(engine is None)


class Test10(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        if os.path.exists(self.workdir):
            anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_20_render_impl(self):
        engine = TT.Engine()

        trs = (("aaa", None, "aaa"), ("$a", {'a': "aaa"}, "aaa"))
        for (tmpl_s, ctx, exp) in trs:
            tmpl = os.path.join(self.workdir, "test.tmpl")
            open(tmpl, 'w').write(tmpl_s)

            self.assertEquals(engine.render_impl(tmpl, ctx), exp)

# vim:sw=4:ts=4:et:
