#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import pytest

import anytemplate.engines.cheetah as TT


has_cheeatah = pytest.mark.skipif(
    TT.Template is None, reason="Cheetah is not available."
)

pytest.skip(
    "skipping cheetah tests as it looks having some issues.",
    allow_module_level=True
)


@has_cheeatah
def test__init__w_kwargs():
    assert isinstance(TT.Engine(errorCatcher=None), TT.Engine)


@has_cheeatah
@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "opts", "exp"),
    (
     ("hello world!", {}, {}, "hello world!"),
     ("hello, $name!", {"name": "John"}, {}, "hello, John!"),
     ("hello world!", {}, dict(at_paths=['.']), "hello world!"),
     ("hello world!", {}, dict(file="x.t"), "hello world!"),
     ),
)
def test_renders(tmpl_s, ctx, opts, exp):
    assert TT.Engine().renders(tmpl_s,  ctx, **opts) == exp


@has_cheeatah
def test_renders__with_engine_special_option():
    egn = TT.Engine(compilerSettings={'cheetahVarStartToken': '@'})
    assert egn.renders("@a", {'a': ""}) == ''


@has_cheeatah
def test_render_with_template_paths(tmp_path):
    tmpl_s = "$getVar('greeting', 'hello!')"
    ctx = dict(greeting="hello, Cheetah!")
    exp = ctx["greeting"]

    tmpl = tmp_path / "a.t"
    tmpl.write_text(tmpl_s)

    assert TT.Engine().render(str(tmpl), ctx, at_paths=[str(tmp_path)]) == exp


@has_cheeatah
def test_render_without_context(tmp_path):
    tmpl_s = "$getVar('greeting', 'hello!')"
    exp = "hello!"

    tmpl = tmp_path / "a.t"
    tmpl.write_text(tmpl_s)

    assert TT.Engine().render(str(tmpl), {}) == exp


@has_cheeatah
def test_render_impl__w_source(tmp_path):
    tmpl_s = "$getVar('greeting', 'hello!')"
    ctx = dict(greeting="hello, Cheetah!")
    exp = ctx["greeting"]

    tmpl = tmp_path / "a.t"
    tmpl.write_text(tmpl_s)

    assert TT.Engine().render(
        str(tmpl), ctx, at_paths=[str(tmp_path)], source="aaa"
    ) == exp

# vim:sw=4:ts=4:et:
