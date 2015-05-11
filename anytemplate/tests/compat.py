#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
import os.path
import unittest

import anytemplate.compat as TT
import anytemplate.tests.common


class Test_10_with_workdir(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_20_json_load(self):
        f = os.path.join(self.workdir, "a.json")
        obj = {"a": "aaa", "b": [1, 2, 3]}

        TT.json.dump(obj, open(f, 'w'))

        self.assertEquals(TT.json_load(f, "dummy_arg0"), obj)

# vim:sw=4:ts=4:et:
