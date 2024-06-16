#
# Copyright (C) 2011 - 2015 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import pytest

try:
    import anytemplate.engines.jinja2 as TT
except ImportError:
    pytest.skip("jinja2 is not available.", allow_module_level=True)


def test_ex_loader(tmp_path):
    imax = 5

    for i in range(0, imax):
        (tmp_path / f"{i}.j2").write_text(str(i))

    loader = TT.FileSystemExLoader([str(tmp_path)], enable_glob=True)
    env = TT.jinja2.Environment(loader=loader)
    tmpl = env.get_template("*.j2")
    res = tmpl.render()

    assert res == ''.join(str(i) for i in range(0, imax))


@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "exp"),
    (
     ("{{ a | d('aaa') }}", {}, "aaa"),
     ('a = {{ a }}, b = "{{ b }}"', {'a': 1, 'b': 'bbb'}, 'a = 1, b = "bbb"'),
     ),
)
def test_renders(tmpl_s, ctx, exp):
    assert TT.Engine().renders(tmpl_s, ctx) == exp


@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "opts", "exp"),
    (
     ("a = {{ a }}", {'a': "aaa"}, {}, "a = aaa"),
     ("""\
{% set xs = [1, 2, 3] -%}
{% do xs.append(4) -%}
{{ xs|join(',') }}
""", {}, dict(extensions=["jinja2.ext.do"], ), "1,2,3,4"),
     ),
)
def test_render(tmpl_s, ctx, opts, exp, tmp_path):
    tmpl = tmp_path / "a.j2"
    tmpl.write_text(tmpl_s)

    assert TT.Engine().render(
        str(tmpl), ctx, at_paths=[str(tmp_path)], **opts
    ) == exp

# vim:sw=4:ts=4:et:
