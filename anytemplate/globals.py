#
# Copyright (C) 2012 - 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""anytemplate globals.
"""
import logging

try:
    from logging import NullHandler
except ImportError:  # python < 2.7 don't have it.
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

PACKAGE = "anytemplate"
VERSION = "0.0.1"
AUTHOR = "Satoru SATOH <ssat@redhat.com>"

# See: "Configuring Logging for a Library" in python standard logging howto,
# e.g. https://docs.python.org/2/howto/logging.html#library-config.
LOGGER = logging.getLogger(PACKAGE)
LOGGER.addHandler(NullHandler())

# vim:sw=4:ts=4:et:
