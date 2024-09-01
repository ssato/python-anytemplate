#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import, with_statement

import io
import json
import os
import pathlib

import pytest

import anytemplate.utils as TT


@pytest.mark.parametrize(
    ("input", "exp_out"),
    (([], []),
     ([1, 4, 5, 1, 2, 3, 5, 10, 13, 2], [1, 4, 5, 2, 3, 10, 13]),
     ),
)
def test_uniq(input, exp_out):
    assert TT.uniq(input) == exp_out


def test_chaincalls():
    assert TT.chaincalls([lambda x: x + 1, lambda x: x - 1], 1) == 1


@pytest.mark.parametrize(
    ("input", "exp_out"),
    (("/tmp/../etc/hosts", "/etc/hosts"),
     ("~root/t", "/root/t"),
     ("./a/b/c.txt",
      TT.normpath(str(pathlib.Path.cwd() / "./a/b/c.txt"))),
     ),
)
def test_normpath(input, exp_out):
    assert TT.normpath(input) == exp_out


@pytest.mark.parametrize(
    ("input", "exp_out"),
    (([], []),
     ((), []),
     ([[1, 2, 3], [4, 5]], [1, 2, 3, 4, 5]),
     ([[1, 2, 3], [4, 5, [6, 7]]], [1, 2, 3, 4, 5, [6, 7]]),
     (((1, 2, 3), (4, 5, [6, 7])), [1, 2, 3, 4, 5, [6, 7]]),
     (((i, i * 2) for i in range(3)), [0, 0, 1, 2, 2, 4]),
     ),
)
def test_concat(input, exp_out):
    assert TT.concat(input) == exp_out


@pytest.mark.parametrize(
    ("input", "exp_out"),
    (("json:a.json", [("a.json", "json")]),
     ("a.json", [("a.json", None)]),
     ),
)
def test_parse_filespec__w_type(input, exp_out):
    assert TT.parse_filespec(input) == exp_out


@pytest.mark.parametrize(
    ("cpath", "ctype", "exp"),
    (("-", "json", {}),
     ("c.json", "json", {}),
     ("c.json", "json", {"a": "A"}),
     )
)
def test_load_context(cpath, ctype, exp, monkeypatch, tmp_path):
    ctx_s = json.dumps(exp)

    if cpath == "-":
        monkeypatch.setattr("sys.stdin", io.StringIO(ctx_s))
    else:
        cpath = tmp_path / cpath
        cpath.write_text(ctx_s)

    TT.load_context(cpath, ctype) == exp


@pytest.mark.parametrize(
    ("input", ),
    (("/a/b/c.json", ),  # invalid input.
     ("/root/c.json", ),  # os error (can't be written).
     ),
)
def test_parse_and_load_contexts__invalid_input(input):
    assert isinstance(TT.parse_and_load_contexts([input]), dict)


def test_find_template_from_path__wo_paths(request):
    fpath = request.path.absolute()

    assert TT.find_template_from_path(str(fpath)) == str(fpath)
    assert TT.find_template_from_path(
        fpath.name, [str(fpath.parent)]
    ) == str(fpath)


def test_find_template_from_path__none():
    assert TT.find_template_from_path("not_existing") is None


def test_mk_template_paths():
    this_path = pathlib.Path(__name__)
    fname = this_path.name
    fdir = str(this_path.absolute().parent)

    assert TT.mk_template_paths(fname, []) == [fdir]
    assert TT.mk_template_paths(fname, ["/etc"]) == ["/etc", fdir]
    assert TT.mk_template_paths(None, ["/etc"]) == ["/etc"]
    assert TT.mk_template_paths(None, None) == [os.curdir]


@pytest.mark.parametrize(
    ("ctx", ),
    (({}, ),
     ({"a": "A"}, ),
     ({"a": "A", "b": [1, 2]}, ),
     )
)
def test_parse_and_load_contexts(ctx, tmp_path):
    cpath = tmp_path / "c.json"
    with cpath.open(mode="w", encoding="utf-8") as cio:
        json.dump(ctx, cio)

    assert TT.parse_and_load_contexts([str(cpath)]) == ctx
    assert TT.parse_and_load_contexts(
        [f"json:{p}" for p in [cpath]]
    ) == ctx


def test_parse_and_load_contexts_multi(tmp_path):
    jsns = [
        tmp_path / "a.json", tmp_path / "b.json", tmp_path / "c.json"
    ]
    jsns[0].write_text('{"a": "aaa"}\n')
    jsns[1].write_text('{"b": "bbb"}\n')
    jsns[2].write_text('{"c": "ccc"}\n')
    paths = [str(j) for j in jsns]

    assert TT.parse_and_load_contexts(paths) == dict(a="aaa", b="bbb", c="ccc")


def test_write_to_output__create_dir(tmp_path):
    out = tmp_path / "a" / "out.txt"
    TT.write_to_output("hello", str(out))

    assert out.exists()
    assert out.read_text() == "hello"


def test_write_to_output__stdout(tmp_path):
    out = tmp_path / "test.out"
    TT.write_to_output("hello", output=out)

    assert out.exists()
    assert out.read_text() == "hello"
