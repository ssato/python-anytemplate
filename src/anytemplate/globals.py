#
# Copyright (C) 2012 - 2024 Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""anytemplate globals."""
import logging
import typing


PACKAGE: typing.Final[str] = "anytemplate"
AUTHOR: typing.Final[str] = "Satoru SATOH <satoru.satoh gmail.com>"

# See: "Configuring Logging for a Library" in python standard logging howto,
# https://docs.python.org/3/howto/logging.html#library-config
LOGGER: logging.Logger = logging.getLogger(PACKAGE)
LOGGER.addHandler(logging.NullHandler())


class TemplateNotFound(Exception):
    """
    Exception during rendering template[s] and any of templates are missing.
    """


class TemplateEngineNotFound(Exception):
    """
    Raised if no any appropriate template engines were found.
    """


class CompileError(Exception):
    """
    Excepction indicates any errors during template compilation.
    """
