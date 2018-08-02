#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import unittest
import anytemplate.globals as TT


class Test(unittest.TestCase):

    def test_10_null_handler(self):
        logger = TT.logging.getLogger(__name__)
        handler = TT.MyNullHandler()
        self.assertTrue(handler is not None)
        logger.addHandler(handler)
        logger.debug("aaa")

    def test_20_logger(self):
        TT.LOGGER.info("test log")
        self.assertTrue(TT.NullHandler is not None)

# vim:sw=4:ts=4:et:
