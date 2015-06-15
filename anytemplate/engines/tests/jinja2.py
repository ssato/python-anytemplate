#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os
import unittest

import anytemplate.tests.common
try:
    import anytemplate.engines.jinja2 as TT
except ImportError:
    TT = None


class Test00(unittest.TestCase):

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


class Test10(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_10_render(self):
        tmpl = "a.j2"
        open(os.path.join(self.workdir, tmpl), 'w').write("a = {{ a }}")

        if TT is not None:
            egn = TT.Engine()
            res = egn.render(tmpl, {'a': "aaa", }, [self.workdir])
            self.assertEquals(res, "a = aaa")

    def test_12_render__with_extension(self):
        tmpl = "b.j2"
        content = """\
{% set xs = [1, 2, 3] -%}
{% do xs.append(4) -%}
{{ xs|join(',') }}
"""
        open(os.path.join(self.workdir, tmpl), 'w').write(content)

        if TT is not None:
            egn = TT.Engine()
            res = egn.render(tmpl, at_paths=[self.workdir],
                             extensions=["jinja2.ext.do"])
            self.assertEquals(res, "1,2,3,4")

# vim:sw=4:ts=4:et:
