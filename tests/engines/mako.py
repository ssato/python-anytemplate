#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
import os
import unittest

import tests.common

try:
    import anytemplate.engines.mako as TT
except ImportError:
    TT = None


class Test00(unittest.TestCase):

    def test_20_renders(self):
        tmpl_s = "hello, ${name}!"
        exp = "hello, John!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s, {"name": "John", }), exp)

    def test_22_renders__no_context(self):
        tmpl_s = "hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s), tmpl_s)

    def test_24_renders__no_context__w_at_path(self):
        tmpl_s = "hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s, at_paths=['.']), tmpl_s)

    def test_26_renders__no_context__w_filename(self):
        tmpl_s = "hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s, filename="x"), tmpl_s)

    def test_28_renders__with_special_option(self):
        tmpl_s = "hello world!"

        if TT is not None:
            def null_preproc(*args, **kwargs):
                return ''

            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s, preprocessor=null_preproc),
                             '')


class Test10(tests.common.TestsWithWorkdir):

    def test_10_render(self):
        tmpl = "a.t"
        open(os.path.join(self.workdir, tmpl), 'w').write("a = ${a}")

        if TT is not None:
            egn = TT.Engine()
            res = egn.render(tmpl, {'a': "aaa", }, at_paths=[self.workdir])
            self.assertEqual(res, "a = aaa")

    def test_12_render__no_context(self):
        tmpl = os.path.join(self.workdir, "a.t")
        open(tmpl, 'w').write("hello!")

        if TT is not None:
            egn = TT.Engine()
            res = egn.render(tmpl, text="x")
            self.assertEqual(res, "hello!")

# vim:sw=4:ts=4:et:
