#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
#
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


class Test_00(unittest.TestCase):

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

    def test_26_renders__no_context__w_filename(self):
        tmpl_s = "hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s, filename="x"), tmpl_s)


class Test_10(unittest.TestCase):

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
            r = egn.render(tmpl, ctx, at_paths=[self.workdir])
            self.assertEquals(r, ctx["greeting"])

    def test_12_render__no_context(self):
        tmpl = os.path.join(self.workdir, "a.t")
        tmpl_s = "$getVar('greeting', 'hello!')"
        open(tmpl, 'w').write(tmpl_s)

        if TT is not None:
            egn = TT.Engine()
            r = egn.render(tmpl)
            self.assertEquals(r, "hello!")

# vim:sw=4:ts=4:et:
