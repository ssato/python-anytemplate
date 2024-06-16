#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import pytest

try:
    import anytemplate.engines.mako as TT
    pytest.skip(
        "skipping mako tests as it looks having some issues.",
        allow_module_level=True
    )
except ImportError:
    pytest.skip("Mako is not available.", allow_module_level=True)


@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "opts", "exp"),
    (
     ("hello world!", {}, {}, "hello world!"),
     ("hello, ${name}!", {"name": "John"}, {}, "hello, John!"),
     ("hello world!", {}, dict(at_paths=['.']), "hello world!"),
     ("hello world!", {}, dict(filename="x.t"), "hello world!"),
     ("hello world!", {},
      dict(preprocessor=lambda *args, **kwargs: ""),
      ""),
     ),
)
def test_renders(tmpl_s, ctx, opts, exp):
    assert TT.Engine().renders(tmpl_s, ctx, **opts) == exp


@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "exp"),
    (
     ("a = ${a}", {'a': "aaa"}, "a = aaa"),
     ("hello", {}, "hello"),
     ),
)
def test_render(tmpl_s, ctx, exp, tmp_path):
    tmpl = tmp_path / "a.t"
    tmpl.write_text(tmpl_s)

    assert TT.Engine().render(
        str(tmpl), ctx, at_paths=[str(tmp_path)]
    ) == exp
