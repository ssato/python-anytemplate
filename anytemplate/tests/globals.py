#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
import unittest
import anytemplate.globals as TT


class Test_00(unittest.TestCase):

    def test_20_LOGGER(self):
        TT.LOGGER.info("test log")

# vim:sw=4:ts=4:et:
