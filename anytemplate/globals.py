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
        """Handler does nothing.
        """
        def emit(self, record):
            pass

PACKAGE = "anytemplate"
VERSION = "0.0.5"
AUTHOR = "Satoru SATOH <ssat@redhat.com>"

# See: "Configuring Logging for a Library" in python standard logging howto,
# e.g. https://docs.python.org/2/howto/logging.html#library-config.
LOGGER = logging.getLogger(PACKAGE)
LOGGER.addHandler(NullHandler())


class TemplateNotFound(Exception):
    """
    Exception during rendering template[s] and any of templates are missing.
    """
    pass


class TemplateEngineNotFound(Exception):
    """
    Raised if no any appropriate template engines were found.
    """
    pass


class CompileError(Exception):
    """
    Excepction indicates any errors during template compilation.
    """
    pass

# vim:sw=4:ts=4:et:
