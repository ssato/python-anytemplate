#
# Copyright (C) 2015 - 2018 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name
"""Tests of anytempalte.cli
"""
from __future__ import absolute_import

import json
import subprocess

import pytest

import anytemplate.cli as TT

from anytemplate.globals import CompileError

try:
    import jinja2
    J2_IS_AVAIL = bool(jinja2)
except ImportError:
    J2_IS_AVAIL = False

try:
    import yaml
    YAML_IS_AVAIL = bool(yaml)
except ImportError:
    YAML_IS_AVAIL = False


def assert_run(args=None, exp_code=0, expect_fail=False):
    """Run main() and check its exit code.
    """
    if args is None:
        args = []

    with pytest.raises(SystemExit) as exc_info:
        TT.main(["dummy"] + ([] if args is None else args))

    code = exc_info.value.code
    assert code != exp_code if expect_fail else code == exp_code


@pytest.mark.parametrize(
    ("args", "code", "exp_fail"),
    (([], 1, False),
     (["--help"], 0, False),
     (["--wrong-option-abc"], 0, True),
     (["--list-engines"], 0, False),
     ),
)
def test_run_main_without_side_effects(args, code, exp_fail):
    assert_run(args, code, exp_fail)


def test_run_main__strtemplate(tmp_path):
    tmpl = tmp_path / "test.tmpl"
    ctx = tmp_path / "ctx.yml"
    out = tmp_path / "output.txt"

    tmpl.write_text("$a\n")
    ctx.write_text("a: aaa\n")

    assert_run(
        ["-E", "string.Template",
         "-C", f"yaml:{ctx!s}", "-o", str(out),
         str(tmpl)]
    )
    assert out.exists()
    assert out.read_text() == "aaa\n"


@pytest.mark.skipif(not J2_IS_AVAIL, reason="jinja2 is not available.")
def test_run_main__jinja2(tmp_path):
    tmpl = tmp_path / "test.j2"
    ctx = tmp_path / "ctx.yml"
    out = tmp_path / "output.txt"

    tmpl.write_text("{{ msg | d('none') }}")
    ctx.write_text("---\nmsg: hello\n")

    assert_run(
        ["-C", f"yaml:{ctx!s}", "-o", str(out), str(tmpl)]
    )
    assert out.exists()
    assert out.read_text() == "hello"


def _subproc_run(args, request):
    """Call subprocess.check_output with some keyword arguments.

    .. seealso::

       https://docs.pytest.org/en/latest/reference/reference.html#request
    """
    src_root = request.path.parent.parent.absolute()

    return subprocess.run(
        ["python3", "src/anytemplate/cli.py", *args],
        env={"PYTHONPATH": "src"},
        shell=True,
        cwd=str(src_root),
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.mark.parametrize(
    ("tmpl_s", "ctx", "exp"),
    (("a\n", {}, "a"),
     ("$a\n", {"a": "aaa"}, "aaa"),
     )
)
def test_strtemplate_with_ctx(
    tmpl_s, ctx, exp, tmp_path, request
):
    tmpl = tmp_path / "test.tmpl"
    tmpl.write_text(tmpl_s)

    cpath = tmp_path / "ctx.json"
    with cpath.open(mode="w", encoding="utf-8") as ctxf:
        json.dump(ctx, ctxf)

    try:
        res = _subproc_run(
            ["-E", "string.Template", "-C", f"json:{cpath!s}",
             "-o", "-", str(tmpl)],
            request
        )
    except (IOError, OSError, CompileError):
        print(f"tmpl: {tmpl.read_text()}")
        print(f"ctx: {cpath.read_text()}")
        raise

    assert not res.stderr
    assert res.stdout.rstrip() == exp
