#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os.path
import unittest

import anytemplate.api as TT
import anytemplate.compat
import anytemplate.engine
import anytemplate.engines.stringTemplate
import anytemplate.tests.common

from anytemplate.engine import find_by_name
from anytemplate.globals import TemplateNotFound


class Test00(unittest.TestCase):

    def test_00_list_engines(self):
        clss = TT.list_engines()
        self.assertTrue(clss)
        self.assertTrue(anytemplate.engines.stringTemplate.Engine in clss)

    def test_10_find_engine__wo_any_info(self):
        cls = TT.find_engine()
        self.assertFalse(cls is None)

    def test_12_find_engine__by_filepath(self):
        if find_by_name("jinja2"):
            import anytemplate.engines.jinja2

            cls = TT.find_engine("foo.j2")
            self.assertEquals(cls, anytemplate.engines.jinja2.Engine)

    def test_14_find_engine__by_filepath__not_found(self):
        try:
            TT.find_engine("foo.not_existing_tmpl_ext")
            assert False, "Not reached here"
        except TT.TemplateEngineNotFound:
            pass

    def test_16_find_engine__by_name(self):
        cls = TT.find_engine("foo.t", "string.Template")
        self.assertEquals(cls, anytemplate.engines.stringTemplate.Engine)

    def test_18_find_engine__by_name__not_found(self):
        try:
            TT.find_engine(None, "not_existing_tmpl_name")
            assert False, "Not reached here"
        except TT.TemplateEngineNotFound:
            pass

    def test_20_renders__stringTemplate(self):
        self.assertEquals(TT.renders("$a", dict(a="aaa", ),
                                     at_engine="string.Template"),
                          "aaa")

    def test_22_renders__jinja2(self):
        if find_by_name("jinja2"):
            self.assertEquals(TT.renders("{{ a }}", dict(a="aaa", ),
                                         at_engine="jinja2"),
                              "aaa")

    def test_22_renders__jinja2__template_not_found(self):
        if find_by_name("jinja2"):
            try:
                TT.renders("{% include 'not_existing.j2' %}",
                           at_engine="jinja2", at_ask_missing=False)
                assert False, "Not reached here"
            except TemplateNotFound:
                pass


class Test10(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_10__render__usr_tmpl_given_by_kwargs(self):
        tmpl = os.path.join(self.workdir, "a.t")
        open(tmpl, 'w').write("$a")

        self.assertEquals(TT._render(None, os.path.basename(tmpl),
                                     dict(a="aaa", ),
                                     at_engine="string.Template",
                                     at_ask_missing=True,
                                     _at_usr_tmpl=tmpl),
                          "aaa")

    def test_12__render__usr_tmpl_given_by_kwargs__altname(self):
        tmpl = os.path.join(self.workdir, "a.t")
        open(tmpl, 'w').write("$a")

        self.assertEquals(TT._render(None, "b.t",
                                     dict(a="aaa", ),
                                     at_engine="string.Template",
                                     at_ask_missing=True,
                                     _at_usr_tmpl=tmpl),
                          "aaa")

    def test_14__render__usr_tmpl_given(self):
        """
        TODO: Test cases if given template file is missing but its path will be
        given by users on demand.
        """
        pass

    def test_20_render__no_at_paths(self):
        tmpl = os.path.join(self.workdir, "a.t")
        open(tmpl, 'w').write("$a")

        self.assertEquals(TT.render(tmpl, dict(a="aaa", ),
                                    at_engine="string.Template"),
                          "aaa")

    def test_22_render__template_missing(self):
        try:
            TT.render("not_exisiting_tmpl", at_engine="string.Template")
            assert False, "Not reached here"
        except TemplateNotFound:
            pass

    def test_24__render__with_engine_specific_options(self):
        tmpl = os.path.join(self.workdir, "a.t")
        open(tmpl, 'w').write("""\
{% set xs = [1, 2, 3] -%}
{% do xs.append(4) -%}
{{ xs|join(',') }}
""")
        if find_by_name("jinja2"):
            self.assertEquals(TT.render(tmpl, at_engine="jinja2",
                                        extensions=["jinja2.ext.do"]),
                              "1,2,3,4")

    def test_30_render_to(self):
        tmpl = os.path.join(self.workdir, "a.t")
        output = os.path.join(self.workdir, "a.txt")
        open(tmpl, 'w').write("$a")

        TT.render_to(tmpl, dict(a="aaa", ), output,
                     at_engine="string.Template")
        self.assertTrue(os.path.exists(output))
        self.assertEquals(open(output).read(), "aaa")

# vim:sw=4:ts=4:et:
