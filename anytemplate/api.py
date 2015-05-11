#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""anytemplate.api - API of anytemplate module
"""
from __future__ import absolute_import

import os.path

import anytemplate.compat
import anytemplate.engine
import anytemplate.globals
import anytemplate.utils


# Aliases:
LOGGER = anytemplate.globals.LOGGER
TemplateNotFound = anytemplate.engine.TemplateNotFound


class TemplateEngineNotFound(Exception):
    """
    Raised if no any appropriate template engines were found.
    """
    pass


def list_engines():
    """
    List available template engines sorted by each priority.

    :return: A list of child classes of the class
        :class:`anytemplate.engines.base.Engine`
    """
    return anytemplate.engine.list_engines_by_priority()


def find_engine(filepath=None, name=None):
    """
    :param filepath: Template file path
    :param name: Specify the name of template engine to use explicitly or
        None; it will be selected automatically anyhow.

    :return: Template engine class found
    """
    if name is None:
        if filepath is None:
            engines = list_engines()
        else:
            engines = anytemplate.engine.find_by_filename(filepath)

        if not engines:
            raise TemplateEngineNotFound("filename=%s" % str(filepath))

        return engines[0]  # It should have highest priority.
    else:
        engine = anytemplate.engine.find_by_name(name)
        if engine is None:
            raise TemplateEngineNotFound("(template) name=%s" % name)

        return engine


def renders(template_content, context=None, at_paths=None,
            at_encoding=anytemplate.compat.ENCODING,
            at_engine=None, at_ask_missing=False,
            at_cls_args=None, **kwargs):
    """
    Compile and render given template string and return the result string.

    :param template_content: Template content string
    :param context: A dict or dict-like object to instantiate given
        template file
    :param at_paths: Template search paths
    :param at_encoding: Template encoding
    :param at_engine: Specify the name of template engine to use explicitly or
        None to find it automatically anyhow.
    :param at_cls_args: Arguments passed to instantiate template engine class
    :param kwargs: Keyword arguments passed to the template engine to
        render templates with specific features enabled.

    :return: Rendered string
    """
    ecls = find_engine(None, at_engine)
    LOGGER.info("Use the template engine: %s", ecls.name())
    engine = ecls() if at_cls_args is None else ecls(**at_cls_args)
    at_paths = anytemplate.utils.mk_template_paths(None, at_paths)

    try:
        return engine.renders(template_content, context=context,
                              at_paths=at_paths, at_encoding=at_encoding,
                              **kwargs)
    except anytemplate.engine.TemplateNotFound:
        if not at_ask_missing:
            raise

        usr_tmpl = anytemplate.compat.raw_input(
            "\n*** Missing template included. Please enter absolute or "
            "relative path starting from '.' to the template file: "
        )
        usr_tmpl = anytemplate.utils.normpath(usr_tmpl.strip())
        usr_tmpldir = os.path.dirname(usr_tmpl)

        return engine.renders(template_content, context=context,
                              at_paths=(at_paths + [usr_tmpldir]),
                              at_encoding=at_encoding, **kwargs)


def render(filepath, context=None, at_paths=None,
           at_encoding=anytemplate.compat.ENCODING,
           at_engine=None, at_ask_missing=False,
           at_cls_args=None, **kwargs):
    """
    Compile and render given template file and return the result string.

    :param template: Template file path
    :param context: A dict or dict-like object to instantiate given
        template file
    :param at_paths: Template search paths
    :param at_encoding: Template encoding
    :param at_engine: Specify the name of template engine to use explicitly or
        None to find it automatically anyhow.
    :param at_cls_args: Arguments passed to instantiate template engine class
    :param kwargs: Keyword arguments passed to the template engine to
        render templates with specific features enabled.

    :return: Rendered string
    """
    ecls = find_engine(filepath, at_engine)
    LOGGER.info("Use the template engine: %s", ecls.name())
    engine = ecls() if at_cls_args is None else ecls(**at_cls_args)

    if at_paths is None:
        at_paths = anytemplate.utils.mk_template_paths(filepath, at_paths)
    try:
        return engine.render(filepath, context=context, at_paths=at_paths,
                             at_encoding=at_encoding, **kwargs)
    except anytemplate.engine.TemplateNotFound:
        if not at_ask_missing:
            raise

        usr_tmpl = anytemplate.compat.raw_input(
            "\n*** Missing template '%s' or any/one of templates included "
            "from %s. Please enter absolute or relative path starting "
            "from '.' to the template file: " % (filepath, filepath)
        )
        usr_tmpl = anytemplate.utils.normpath(usr_tmpl.strip())
        usr_tmpldir = os.path.dirname(usr_tmpl)

        if os.path.basename(filepath) == os.path.basename(usr_tmpl):
            tmpl = usr_tmpl
        else:
            tmpl = filepath

        return engine.render(tmpl, context=context,
                             at_paths=(at_paths + [usr_tmpldir]),
                             at_encoding=at_encoding, **kwargs)


def render_to(filepath, context=None, output=None, at_paths=None,
              at_encoding=anytemplate.compat.ENCODING,
              at_engine=None, at_ask_missing=False,
              at_cls_args=None, **kwargs):
    """
    Render given template file and write the result string to given `output`.
    The result string will be printed to sys.stdout if output is None or '-'.

    :param template: Template file path
    :param context: A dict or dict-like object to instantiate given
        template file
    :param output: File path to write the rendered result string to or None/'-'
        to print it to stdout
    :param at_paths: Template search paths
    :param at_encoding: Template encoding
    :param at_engine: Specify the name of template engine to use explicitly or
        None to find it automatically anyhow.
    :param at_cls_args: Arguments passed to instantiate template engine class
    :param kwargs: Keyword arguments passed to the template engine to
        render templates with specific features enabled.
    """
    res = render(filepath, context=context, at_paths=at_paths,
                 at_encoding=at_encoding, at_engine=at_engine,
                 at_ask_missing=at_ask_missing, at_cls_args=at_cls_args,
                 **kwargs)
    anytemplate.utils.write_to_output(res, output, at_encoding)

# vim:sw=4:ts=4:et:
