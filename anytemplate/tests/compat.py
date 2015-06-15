#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os.path
import unittest

import anytemplate.compat as TT
import anytemplate.tests.common


class Test(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_20_json_load(self):
        fpath = os.path.join(self.workdir, "a.json")
        obj = {"a": "aaa", "b": [1, 2, 3]}

        TT.json.dump(obj, open(fpath, 'w'))

        self.assertEquals(TT.json_load(fpath, "dummy_arg0"), obj)

# vim:sw=4:ts=4:et:
