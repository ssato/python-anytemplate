#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import

import pytest

try:
    import anytemplate.engines.pystache as TT
except ImportError:
    pytest.skip("pystache is not available.", allow_module_level=True)


@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "opts", "exp"),
    (
     ("Hello world!", {}, {}, "Hello world!"),
     ("Hello world!", {}, dict(at_paths=['.']), "Hello world!"),
     ("Hello, {{name}}!", {"name": "John"}, {}, "Hello, John!"),
     ("Hello world!", {}, dict(missing_tags="strict"), "Hello world!"),
     ("{{ a }}", {}, dict(missing_tags="ignore"), ""),
     ),
)
def test_renders(tmpl_s, ctx, opts, exp):
    assert TT.Engine().renders(tmpl_s, ctx) == exp


@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "opts", "exp"),
    (
     ("Hello!", {}, {}, "Hello!"),
     ("a = {{a}}", {'a': "aaa"}, {}, "a = aaa"),
     ),
)
def test_render(tmpl_s, ctx, opts, exp, tmp_path):
    tmpl = tmp_path / "a.mustache"
    tmpl.write_text(tmpl_s)

    assert TT.Engine().render(str(tmpl), ctx, **opts) == exp
    assert TT.Engine().render(
        tmpl.name, ctx, at_paths=[str(tmp_path)], **opts
    ) == exp

# vim:sw=4:ts=4:et:
