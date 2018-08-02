#
# Copyright (C). 2015 - 2018 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import os.path
import unittest

import anytemplate.compat as TT
import tests.common


_OBJ = {"a": "aaa", "b": [1, 2, 3]}


class Test(unittest.TestCase):

    def test_10_json_loads(self):
        content = TT.json.dumps(_OBJ)

        self.assertEqual(TT.json_loads(content, "arg0", arg1="aaa"), _OBJ)


class TestWithIO(unittest.TestCase):

    def setUp(self):
        self.workdir = tests.common.setup_workdir()

    def tearDown(self):
        tests.common.cleanup_workdir(self.workdir)

    def test_20_json_load(self):
        fpath = os.path.join(self.workdir, "a.json")

        TT.json.dump(_OBJ, open(fpath, 'w'))

        self.assertEqual(TT.json_load(fpath, "dummy_arg0"), _OBJ)

# vim:sw=4:ts=4:et:
