#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest

import anytemplate.engine as TT
import anytemplate.engines.stringTemplate as stringTemplate


class Test(unittest.TestCase):

    def test_10_find_by_filename(self):
        stringTemplate.Engine._file_extensions.append("t")
        clss = TT.find_by_filename("foo.t")
        self.assertTrue(stringTemplate.Engine in clss)

    def test_20_find_by_name__found(self):
        self.assertEquals(TT.find_by_name("string.Template"),
                          stringTemplate.Engine)

    def test_20_find_by_name__not_found(self):
        self.assertTrue(TT.find_by_name("not_existing_engine") is None)

# vim:sw=4:ts=4:et:
