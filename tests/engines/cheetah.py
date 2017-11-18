#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import os
import unittest

import tests.common
import anytemplate.engines.cheetah as TT


class Test(unittest.TestCase):

    def test_12__init__w_kwargs(self):
        if TT.Template is not None:
            self.assertTrue(isinstance(TT.Engine(errorCatcher=None),
                                       TT.Engine))

    def test_20_renders(self):
        tmpl_s = "hello, $name!"
        exp = "hello, John!"

        if TT.Template is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s, {"name": "John", }), exp)

    def test_22_renders__no_context(self):
        tmpl_s = "hello world!"

        if TT.Template is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s), tmpl_s)

    def test_24_renders__no_context__w_at_path(self):
        tmpl_s = "hello world!"

        if TT.Template is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s, at_paths=['.']), tmpl_s)

    def test_26_renders__no_context__w_file(self):
        tmpl_s = "hello world!"

        if TT.Template is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s, file="x"), tmpl_s)

    def test_28_renders__with_engine_special_option(self):
        if TT.Template is not None:
            egn = TT.Engine(compilerSettings={'cheetahVarStartToken': '@'})
            self.assertEqual(egn.renders("@a", {'a': ""}), '')

    def test_36_renders_impl__no_context__w_filename(self):
        tmpl_s = "hello world!"

        if TT.Template is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders_impl(tmpl_s, {}, file="x"), tmpl_s)


class Test10(tests.common.TestsWithWorkdir):

    def test_10_render(self):
        tmpl = os.path.join(self.workdir, "a.t")
        tmpl_s = "$getVar('greeting', 'hello!')"
        ctx = dict(greeting="hello, Cheetah!", )
        open(tmpl, 'w').write(tmpl_s)

        if TT.Template is not None:
            egn = TT.Engine()
            res = egn.render(tmpl, ctx, at_paths=[self.workdir])
            self.assertEqual(res, ctx["greeting"])

    def test_12_render__no_context(self):
        tmpl = os.path.join(self.workdir, "a.t")
        tmpl_s = "$getVar('greeting', 'hello!')"
        open(tmpl, 'w').write(tmpl_s)

        if TT.Template is not None:
            egn = TT.Engine()
            res = egn.render(tmpl)
            self.assertEqual(res, "hello!")

    def test_26_render_impl__w_source(self):
        tmpl = os.path.join(self.workdir, "a.t")
        tmpl_s = "$getVar('greeting', 'hello!')"
        ctx = dict(greeting="hello, Cheetah!", )
        open(tmpl, 'w').write(tmpl_s)

        if TT.Template is not None:
            egn = TT.Engine()
            res = egn.render_impl(tmpl, ctx, at_paths=[self.workdir],
                                  source="aaa")
            self.assertEqual(res, ctx["greeting"])

# vim:sw=4:ts=4:et:
