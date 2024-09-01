#
# Copyright (C). 2015 - 2018 Satoru SATOH <ssato at redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import json

import anytemplate.compat as TT


_OBJ = {"a": "aaa", "b": [1, 2, 3]}


def test_json_load(tmp_path):
    fpath = tmp_path / "a.json"
    fpath.write_text(json.dumps(_OBJ))

    assert TT.load(fpath) == _OBJ
