#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
import os
import unittest

import anytemplate.tests.common
try:
    import anytemplate.engines.jinja2 as TT
except ImportError:
    TT = None


class Test_00_pure_functions(unittest.TestCase):

    def test_20_renders(self):
        tmpl_s = 'a = {{ a }}, b = "{{ b }}"'

        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_s, {'a': 1, 'b': 'bbb'}),
                              'a = 1, b = "bbb"')

    def test_22_renders__no_context(self):
        if TT is not None:
            egn = TT.Engine()
            self.assertEquals(egn.renders("{{ a|default('aaa') }}"),
                              "aaa")


class Test_10_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_10_render(self):
        tmpl = "a.j2"
        open(os.path.join(self.workdir, tmpl), 'w').write("a = {{ a }}")

        if TT is not None:
            egn = TT.Engine()
            r = egn.render(tmpl, {'a': "aaa", }, [self.workdir])
            self.assertEquals(r, "a = aaa")

    def test_20_render(self):
        tmpl = "a.j2"
        open(os.path.join(self.workdir, tmpl), 'w').write("a = {{ a }}")

        if TT is not None:
            egn = TT.Engine()
            r = egn.render(tmpl, {'a': "aaa", }, [self.workdir])
            self.assertEquals(r, "a = aaa")

# vim:sw=4:ts=4:et:
