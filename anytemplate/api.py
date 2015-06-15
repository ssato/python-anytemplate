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

from anytemplate.globals import LOGGER, TemplateNotFound, \
    TemplateEngineNotFound, CompileError  # flake8: noqa


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
        LOGGER.warn("** Missing template[s]: paths=%s",
                    ','.join(at_paths))
        if not at_ask_missing:
            raise TemplateNotFound(str(exc))

        if _at_usr_tmpl is None:
            _at_usr_tmpl = anytemplate.compat.raw_input(
                "\nPlease enter an absolute or relative path starting "
                "from '.' of missing template file"
                "%s : " % (", " + filepath if template is None else '')
            ).strip()

        usr_tmpl = anytemplate.utils.normpath(_at_usr_tmpl)
        usr_tmpldir = os.path.dirname(usr_tmpl)

        if template is None:
            LOGGER.debug("Render %s instead of %s", usr_tmpl, filepath)
            target = usr_tmpl

        return render_fn(target, context=context,
                         at_paths=(at_paths + [usr_tmpldir]),
                         at_encoding=at_encoding, **kwargs)
    except Exception as exc:
        raise CompileError(str(exc))


def renders(template, context=None, at_paths=None,
            at_encoding=anytemplate.compat.ENCODING, at_engine=None,
            at_ask_missing=False, at_cls_args=None, **kwargs):
    """
    Compile and render given template string and return the result string.

    :param template: Template content string
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
    return _render(template, context=context, at_paths=at_paths,
                   at_encoding=at_encoding, at_engine=at_engine,
                   at_ask_missing=at_ask_missing, at_cls_args=at_cls_args,
                   **kwargs)


def render(filepath, context=None, at_paths=None,
           at_encoding=anytemplate.compat.ENCODING,
           at_engine=None, at_ask_missing=False,
           at_cls_args=None, **kwargs):
    """
    Compile and render given template file and return the result string.

    :param filepath: Template file path
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
    return _render(filepath=filepath, context=context, at_paths=at_paths,
                   at_encoding=at_encoding, at_engine=at_engine,
                   at_ask_missing=at_ask_missing, at_cls_args=at_cls_args,
                   **kwargs)


def render_to(filepath, context=None, output=None, at_paths=None,
              at_encoding=anytemplate.compat.ENCODING,
              at_engine=None, at_ask_missing=False,
              at_cls_args=None, **kwargs):
    """
    Render given template file and write the result string to given `output`.
    The result string will be printed to sys.stdout if output is None or '-'.

    :param filepath: Template file path
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
