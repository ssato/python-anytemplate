#
# Copyright (C) 2015 - 2018 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import tests.common
import os.path


class TestsWithWorkdir(unittest.TestCase):

    def setUp(self):
        self.workdir = tests.common.setup_workdir()

    def tearDown(self):
        tests.common.cleanup_workdir(self.workdir)

    def test_00_workdir_exists(self):
        os.path.exists(self.workdir)

# vim:sw=4:ts=4:et:
