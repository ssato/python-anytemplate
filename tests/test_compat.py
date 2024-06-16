#
# Copyright (C). 2015 - 2018 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import anytemplate.compat as TT


_OBJ = {"a": "aaa", "b": [1, 2, 3]}


def test_json_loads():
    content = TT.json.dumps(_OBJ)
    assert TT.json_loads(content, "arg0", arg1="aaa") == _OBJ


def test_json_load(tmp_path):
    fpath = tmp_path / "a.json"

    TT.json.dump(_OBJ, open(str(fpath), 'w'))

    assert TT.json_load(fpath, "dummy_arg0") == _OBJ

# vim:sw=4:ts=4:et:
