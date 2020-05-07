#
# Copyright (C) 2015 - 2018 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# Suppress warning of list_engines
# pylint: disable=unused-import
"""anytemplate.api - API of anytemplate module
"""
from __future__ import absolute_import

import logging
import os.path
import sys

import anytemplate.compat
import anytemplate.engine
import anytemplate.globals
import anytemplate.utils

from anytemplate.globals import (
    TemplateNotFound, TemplateEngineNotFound, CompileError  # noqa: F401
)
from anytemplate.engine import find_by_filename as list_engines  # noqa: F401


LOGGER = logging.getLogger(__name__)


def find_engine(filepath=None, name=None):
    """
    :param filepath: Template file path
    :param name: Specify the name of template engine to use explicitly or
        None; it will be selected automatically anyhow.

    :return: Template engine class found
    """
    if name is None:
        engines = anytemplate.engine.find_by_filename(filepath)
        if not engines:
            raise TemplateEngineNotFound("filename=%s" % str(filepath))

        return engines[0]  # It should have highest priority.
    else:
        engine = anytemplate.engine.find_by_name(name)
        if engine is None:
            raise TemplateEngineNotFound("(template) name=%s" % name)

        return engine


def _render(template=None, filepath=None, context=None, at_paths=None,
            at_encoding=anytemplate.compat.ENCODING, at_engine=None,
            at_ask_missing=False, at_cls_args=None, _at_usr_tmpl=None,
            **kwargs):
    """
    Compile and render given template string and return the result string.

    :param template: Template content string or None
    :param filepath: Template file path or None
    :param context: A dict or dict-like object to instantiate given
        template file
    :param at_paths: Template search paths
    :param at_encoding: Template encoding
    :param at_engine: Specify the name of template engine to use explicitly or
        None to find it automatically anyhow.
    :param at_cls_args: Arguments passed to instantiate template engine class
    :param _at_usr_tmpl: Template file of path will be given by user later;
        this file will be used just for testing purpose.
    :param kwargs: Keyword arguments passed to the template engine to
        render templates with specific features enabled.

    :return: Rendered string
    """
    ecls = find_engine(filepath, at_engine)
    LOGGER.debug("Use the template engine: %s", ecls.name())
    engine = ecls() if at_cls_args is None else ecls(**at_cls_args)
    at_paths = anytemplate.utils.mk_template_paths(filepath, at_paths)

    if filepath is None:
        (render_fn, target) = (engine.renders, template)
    else:
        (render_fn, target) = (engine.render, filepath)

    try:
        return render_fn(target, context=context, at_paths=at_paths,
                         at_encoding=at_encoding, **kwargs)
    except TemplateNotFound as exc:
        LOGGER.warning("** Missing template[s]: paths=%r", at_paths)
        if not at_ask_missing:
            raise TemplateNotFound(str(exc))

        if _at_usr_tmpl is None:
            _at_usr_tmpl = anytemplate.compat.raw_input(
                "\nPlease enter an absolute or relative path starting "
                "from '.' of missing template file"
                "%s : " % (", " + filepath if template is None else '')
            ).strip()

        usr_tmpl = anytemplate.utils.normpath(_at_usr_tmpl)
        if template is None:
            LOGGER.debug("Render %s instead of %s", usr_tmpl, filepath)
            target = usr_tmpl

        return render_fn(target, context=context,
                         at_paths=(at_paths + [os.path.dirname(usr_tmpl)]),
                         at_encoding=at_encoding, **kwargs)
    except Exception as exc:
        raise CompileError("exc=%r, template=%s" % (exc, target[:200]))


def renders(template, context=None, **options):
    """
    Compile and render given template string and return the result string.

    :param template: Template content string
    :param context: A dict or dict-like object to instantiate given
        template file
    :param options: Optional keyword arguments such as:

        - at_paths: Template search paths
        - at_encoding: Template encoding
        - at_engine: Specify the name of template engine to use explicitly or
          None to find it automatically anyhow.
        - at_cls_args: Arguments passed to instantiate template engine class
        - other keyword arguments passed to the template engine to render
          templates with specific features enabled.

    :return: Rendered string
    """
    return _render(template, context=context, **options)


def render(filepath, context=None, **options):
    """
    Compile and render given template file and return the result string.

    :param filepath: Template file path or '-'
    :param context: A dict or dict-like object to instantiate given
        template file
    :param options: Optional keyword arguments such as:

        - at_paths: Template search paths
        - at_encoding: Template encoding
        - at_engine: Specify the name of template engine to use explicitly or
          None to find it automatically anyhow.
        - at_cls_args: Arguments passed to instantiate template engine class
        - other keyword arguments passed to the template engine to render
          templates with specific features enabled.

    :return: Rendered string
    """
    if filepath == '-':
        return _render(sys.stdin.read(), context=context, **options)

    return _render(filepath=filepath, context=context, **options)


def render_to(filepath, context=None, output=None,
              at_encoding=anytemplate.compat.ENCODING, **options):
    """
    Render given template file and write the result string to given `output`.
    The result string will be printed to sys.stdout if output is None or '-'.

    :param filepath: Template file path
    :param context: A dict or dict-like object to instantiate given
        template file
    :param output: File path to write the rendered result string to or None/'-'
        to print it to stdout
    :param at_encoding: Template encoding
    :param options: Optional keyword arguments such as:

        - at_paths: Template search paths
        - at_engine: Specify the name of template engine to use explicitly or
          None to find it automatically anyhow.
        - at_cls_args: Arguments passed to instantiate template engine class
        - other keyword arguments passed to the template engine to render
          templates with specific features enabled.
    """
    res = render(filepath, context=context, **options)
    anytemplate.utils.write_to_output(res, output, at_encoding)

# vim:sw=4:ts=4:et:
