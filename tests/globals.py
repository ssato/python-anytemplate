#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest
import anytemplate.globals as TT


class Test(unittest.TestCase):

    def test_10_null_handler(self):
        logger = TT.logging.getLogger(__name__)
        logger.addHandler(TT.NullHandler_())
        logger.debug("aaa")

    def test_20_logger(self):
        TT.LOGGER.info("test log")
        self.assertTrue(TT.NullHandler is not None)

# vim:sw=4:ts=4:et:
