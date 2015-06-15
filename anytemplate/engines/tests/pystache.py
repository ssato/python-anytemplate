#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os
import unittest

import anytemplate.tests.common

try:
    import anytemplate.engines.pystache as TT
except ImportError:
    TT = None


class Test10(unittest.TestCase):

    def test_20_renders(self):
        tmpl_s = "Hello, {{name}}!"
        exp = "Hello, John!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s, {"name": "John", }), exp)

    def test_22_renders__no_context(self):
        tmpl_s = "Hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s), tmpl_s)

    def test_24_renders__no_context__w_at_path(self):
        tmpl_s = "Hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s, at_paths=['.']), tmpl_s)

    def test_26_renders__no_context__w_custom_options(self):
        tmpl_s = "Hello world!"

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s, missing_tags="strict"),
                              tmpl_s)

    def test_28_renders__with_special_option(self):
        tmpl_s = "{{ a }}"

        if TT is not None:
            egn = TT.Engine(missing_tags='ignore')
            self.assertEquals(egn.renders(tmpl_s), '')


class Test20(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_10_render__abspath(self):
        tmpl = os.path.join(self.workdir, "a.mustache")
        open(tmpl, 'w').write("a = {{a}}")

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.render(tmpl, {'a': "aaa", }), "a = aaa")

    def test_12_render__abspath__no_context(self):
        tmpl = os.path.join(self.workdir, "a.mustache")
        tmpl_s = "Hello!"
        open(tmpl, 'w').write(tmpl_s)

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.render(tmpl), tmpl_s)

    def test_14_render__basename(self):
        tmpl = os.path.join(self.workdir, "a.mustache")
        open(tmpl, 'w').write("a = {{a}}")

        if TT is not None:
            egn = TT.Engine()
            res = egn.render(os.path.basename(tmpl), {'a': "aaa", },
                             at_paths=[self.workdir])
            self.assertEquals(res, "a = aaa")

# vim:sw=4:ts=4:et:
