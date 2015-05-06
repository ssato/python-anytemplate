#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: BSD3
#
from __future__ import absolute_import

import operator

from anytemplate.globals import LOGGER

import anytemplate.engines.base
import anytemplate.engines.stringTemplate

ENGINES = [anytemplate.engines.stringTemplate.Engine, ]

try:
    import anytemplate.engines.jinja2
    ENGINES.append(anytemplate.engines.jinja2.Engine)
except ImportError:
    LOGGER.info("jinja2 support was disable as necessary module looks missing")

try:
    import anytemplate.engines.tenjin
    ENGINES.append(anytemplate.engines.tenjin.Engine)
except ImportError:
    LOGGER.info("tenjin support was disable as necessary module looks missing")


TemplateNotFound = anytemplate.engines.base.TemplateNotFound


def list_engines_by_priority(engines=ENGINES):
    """
    Return a list of engines supported sorted by each priority.
    """
    return sorted(engines, key=operator.methodcaller("priority"))


def find_by_filename(filename, engines=ENGINES):
    """
    Find a list of template engine classes to render template `filename`.

    :param filename: Template file name (may be a absolute/relative path)
    :param engines: Template engines

    :return: A list of engines support given template file
    """
    return sorted((e for e in engines if e.supports(filename)),
                  key=operator.methodcaller("priority"))


def find_by_name(name, engines=ENGINES):
    """
    Find a template engine class specified by its name `name`.

    :param name: Template name
    :param engines: Template engines

    :return: A template engine or None if no any template engine of given name
        were found.
    """
    for egn in engines:
        if egn.name() == name:
            return egn

    return None

# vim:sw=4:ts=4:et:
