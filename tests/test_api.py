#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name, protected-access
from __future__ import absolute_import

import pytest

import anytemplate.api as TT
import anytemplate.engines.strtemplate

from anytemplate.globals import TemplateNotFound


ENGINES = TT.list_engines()
J2_ENGINE_IS_AVAIL = any(e.name() == "jinja2" for e in ENGINES)


def test_list_engines():
    assert ENGINES
    assert anytemplate.engines.strtemplate.Engine in ENGINES


def test_find_engine__wo_any_args():
    assert TT.find_engine() is not None


@pytest.mark.parametrize(
    ("filepath", "name"),
    (("foo.not_existing_tmpl_ext", None),
     (None, "not_existing_tmpl_name"),
     ),
)
def test_find_engine__exceptions(filepath, name):
    with pytest.raises(TT.TemplateEngineNotFound):
        TT.find_engine(filepath=filepath, name=name)


ENGINES_TEST_CASES = [
    ("foo.t", "string.Template", anytemplate.engines.strtemplate.Engine),
]

RENDERS_TEST_CASES = [
    # template string, context, engine, expected result
    ("$a", dict(a="aaa", ), "string.Template", "aaa"),
]

if "jinja2" in ENGINES:
    ENGINES_TEST_CASES.append(
        ("foo.j2", None, anytemplate.engines.jinja2.Engine)
    )
    RENDERS_TEST_CASES.append(
        ("{{ a }}", dict(a="aaa", ), "jinja2", "aaa")
    )


@pytest.mark.parametrize(
    ("filepath", "name", "exp_engine"),
    ENGINES_TEST_CASES,
)
def test_find_engine__ok(filepath, name, exp_engine):
    engine = TT.find_engine(filepath=filepath, name=name)
    assert engine == exp_engine


J2_NOT_AVAIL_MSG = "jinja2 is not available"


@pytest.mark.skipif(not J2_ENGINE_IS_AVAIL, reason=J2_NOT_AVAIL_MSG)
def test_renders__exceptions():
    with pytest.raises(TemplateNotFound):
        TT.renders(
            "{% include 'not_existing.j2' %}", at_engine="jinja2",
            at_ask_missing=False
        )


@pytest.mark.parametrize(
    ("tmpl_str", "ctx", "engine", "expected"),
    RENDERS_TEST_CASES,
)
def test_renders(tmpl_str, ctx, engine, expected):
    assert TT.renders(tmpl_str, ctx, at_engine=engine) == expected


def test_render__usr_tmpl_given_by_kwargs_or_altname(tmp_path):
    tmpl = tmp_path / "a.t"
    tmpl.write_text("$a")

    opts = dict(
        at_engine="string.Template", at_ask_missing=True,
        _at_usr_tmpl=str(tmpl)
    )

    for tname in (tmpl.name, "b.t"):
        assert TT._render(None, tname, dict(a="aaa", ), **opts) == "aaa"


def test__render__usr_tmpl_given_but_missing():
    """
    TODO: Test cases if given template file is missing but its path will be
    given by users on demand.
    """
    pass


def test_render__no_at_paths(tmp_path):
    tmpl = tmp_path / "a.t"
    tmpl.write_text("$a")

    assert TT.render(
        str(tmpl), dict(a="aaa", ), at_engine="string.Template"
    ) == "aaa"


def test_render__template_missing():
    with pytest.raises(TemplateNotFound):
        TT.render("not_exisiting_tmpl", at_engine="string.Template")


@pytest.mark.skipif(not J2_ENGINE_IS_AVAIL, reason=J2_NOT_AVAIL_MSG)
def test_render__with_engine_specific_options(tmp_path):
    tmpl = tmp_path / "a.t"
    tmpl.write_text("""\
{% set xs = [1, 2, 3] -%}
{% do xs.append(4) -%}
{{ xs|join(',') }}
""")
    assert TT.render(
        str(tmpl), at_engine="jinja2",
        extensions=["jinja2.ext.do"]
    ) == "1,2,3,4"


def test_render_to(tmp_path):
    tmpl = tmp_path / "a.t"
    tmpl.write_text("$a")
    output = tmp_path / "a.txt"

    TT.render_to(
        str(tmpl), dict(a="aaa", ), str(output), at_engine="string.Template"
    )
    assert output.exists()
    assert output.read_text() == "aaa"

# vim:sw=4:ts=4:et:
