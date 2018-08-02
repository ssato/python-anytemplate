#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import os
import unittest

import tests.common
try:
    import anytemplate.engines.jinja2 as TT
except ImportError:
    TT = None


class Test00(tests.common.TestsWithWorkdir):

    def test_ex_loader(self):
        if TT is not None:
            for i in range(0, 3):
                open(os.path.join(self.workdir, "%d.j2" % i),
                     'w').write("%d" % i)

            loader = TT.FileSystemExLoader([self.workdir], enable_glob=True)
            env = TT.jinja2.Environment(loader=loader)
            tmpl = env.get_template("*.j2")
            res = tmpl.render()

            self.assertEqual(res, ''.join('%d' % i for i in range(0, 3)))


class Test10(unittest.TestCase):

    def test_20_renders(self):
        tmpl_s = 'a = {{ a }}, b = "{{ b }}"'

        if TT is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders(tmpl_s, {'a': 1, 'b': 'bbb'}),
                             'a = 1, b = "bbb"')

    def test_22_renders__no_context(self):
        if TT is not None:
            egn = TT.Engine()
            self.assertEqual(egn.renders("{{ a|default('aaa') }}"),
                             "aaa")


class Test20(tests.common.TestsWithWorkdir):

    def test_10_render(self):
        tmpl = "a.j2"
        open(os.path.join(self.workdir, tmpl), 'w').write("a = {{ a }}")

        if TT is not None:
            egn = TT.Engine()
            res = egn.render(tmpl, {'a': "aaa", }, [self.workdir])
            self.assertEqual(res, "a = aaa")

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
            self.assertEqual(res, "1,2,3,4")

# vim:sw=4:ts=4:et:
