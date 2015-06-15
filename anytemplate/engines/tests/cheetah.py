#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os
import unittest

import anytemplate.tests.common

try:
    import anytemplate.engines.cheetah as TT
    try:
        import Cheetah.Template  # flake8: noqa
    except ImportError:
        TT = None  # flake8: noqa
except ImportError:
    TT = None


class Test(unittest.TestCase):

    def test_12__init__w_kwargs(self):
        if TT is not None:
            self.assertTrue(isinstance(TT.Engine(errorCatcher=None),
                                       TT.Engine))

    def test_20_renders(self):
        tmpl_s = "hello, $name!"
        exp = "hello, John!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s, {"name": "John", }), exp)

    def test_22_renders__no_context(self):
        tmpl_s = "hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s), tmpl_s)

    def test_24_renders__no_context__w_at_path(self):
        tmpl_s = "hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s, at_paths=['.']), tmpl_s)

    def test_26_renders__no_context__w_file(self):
        tmpl_s = "hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s, file="x"), tmpl_s)

    def test_28_renders__with_engine_special_option(self):
        if TT is not None:
            egn = TT.Engine(compilerSettings={'cheetahVarStartToken': '@'})
            self.assertEquals(egn.renders("@a", {'a': ""}), '')

    def test_36_renders_impl__no_context__w_filename(self):
        tmpl_s = "hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders_impl(tmpl_s, {}, file="x"),
                              tmpl_s)


class Test10(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_10_render(self):
        tmpl = os.path.join(self.workdir, "a.t")
        tmpl_s = "$getVar('greeting', 'hello!')"
        ctx = dict(greeting="hello, Cheetah!", )
        open(tmpl, 'w').write(tmpl_s)

        if TT is not None:
            egn = TT.Engine()
            res = egn.render(tmpl, ctx, at_paths=[self.workdir])
            self.assertEquals(res, ctx["greeting"])

    def test_12_render__no_context(self):
        tmpl = os.path.join(self.workdir, "a.t")
        tmpl_s = "$getVar('greeting', 'hello!')"
        open(tmpl, 'w').write(tmpl_s)

        if TT is not None:
            egn = TT.Engine()
            res = egn.render(tmpl)
            self.assertEquals(res, "hello!")

    def test_26_render_impl__w_source(self):
        tmpl = os.path.join(self.workdir, "a.t")
        tmpl_s = "$getVar('greeting', 'hello!')"
        ctx = dict(greeting="hello, Cheetah!", )
        open(tmpl, 'w').write(tmpl_s)

        if TT is not None:
            egn = TT.Engine()
            res = egn.render_impl(tmpl, ctx, at_paths=[self.workdir],
                                  source="aaa")
            self.assertEquals(res, ctx["greeting"])

# vim:sw=4:ts=4:et:
