#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import pytest

import anytemplate.engines.strtemplate as TT
from anytemplate.globals import CompileError


@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "opts", "exp"),
    (("aaa", None, {}, "aaa"),
     ("$a", {'a': "aaa"}, {}, "aaa"),
     ("$a", {}, {"safe": True}, "$a"),
     ),
)
def test_renders_impl(tmpl_s, ctx, opts, exp):
    engine = TT.Engine()

    assert engine.renders_impl(tmpl_s, ctx, **opts) == exp


def test_renders_impl__error():
    engine = TT.Engine()
    try:
        engine.renders_impl("$a", {})
        engine = None
    except CompileError:
        pass
    assert engine is not None


@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "exp"),
    (("aaa", None, "aaa"),
     ("$a", {'a': "aaa"}, "aaa"),
     ),
)
def test_render_impl(tmpl_s, ctx, exp, tmp_path):
    engine = TT.Engine()

    tmpl = tmp_path / "test.tmpl"
    tmpl.write_text(tmpl_s)

    assert engine.render_impl(tmpl, ctx) == exp
