#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import anytemplate.globals as TT


def test_null_handler():
    logger = TT.logging.getLogger(__name__)
    handler = TT.MyNullHandler()
    assert handler is not None
    logger.addHandler(handler)
    logger.debug("aaa")


def test_20_logger():
    TT.LOGGER.info("test log")
    assert TT.NullHandler is not None

# vim:sw=4:ts=4:et:
