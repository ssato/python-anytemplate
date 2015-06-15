#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""A module to consolidate access to template engine backends.
"""
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
    LOGGER.info("jinja2 support was disable as needed module looks missing")

try:
    import anytemplate.engines.mako
    ENGINES.append(anytemplate.engines.mako.Engine)
except ImportError:
    LOGGER.info("mako support was disable as needed module looks missing")

try:
    import anytemplate.engines.tenjin
    ENGINES.append(anytemplate.engines.tenjin.Engine)
except ImportError:
    LOGGER.info("tenjin support was disable as needed module looks missing")

try:
    import anytemplate.engines.cheetah
    import Cheetah.Template  # flake8: noqa

    ENGINES.append(anytemplate.engines.cheetah.Engine)
except ImportError:
    LOGGER.info("Cheetah support was disable as needed module looks missing")

try:
    import anytemplate.engines.pystache
    ENGINES.append(anytemplate.engines.pystache.Engine)
except ImportError:
    LOGGER.info("Pystache (mustache) support was disable as needed module "
                "looks missing")


def list_engines_by_priority(engines=None):
    """
    Return a list of engines supported sorted by each priority.
    """
    if engines is None:
        engines = ENGINES

    return sorted(engines, key=operator.methodcaller("priority"))


def find_by_filename(filename, engines=None):
    """
    Find a list of template engine classes to render template `filename`.

    :param filename: Template file name (may be a absolute/relative path)
    :param engines: Template engines

    :return: A list of engines support given template file
    """
    if engines is None:
        engines = ENGINES

    return sorted((e for e in engines if e.supports(filename)),
                  key=operator.methodcaller("priority"))


def find_by_name(name, engines=None):
    """
    Find a template engine class specified by its name `name`.

    :param name: Template name
    :param engines: Template engines

    :return: A template engine or None if no any template engine of given name
        were found.
    """
    if engines is None:
        engines = ENGINES

    for egn in engines:
        if egn.name() == name:
            return egn

    return None

# vim:sw=4:ts=4:et:
