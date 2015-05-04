#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: BSD3
#
from __future__ import absolute_import

import operator

import anytemplate.engines.jinja2
import anytemplate.engines.string


ENGINES = [e for e in
           [anytemplate.engines.string.StringTemplateEngine,
            anytemplate.engines.jinja2.Jjnja2Engine] if e.supports()]


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
