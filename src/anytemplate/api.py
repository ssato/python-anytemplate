#
# Copyright (C) 2015 - 2024 Satoru SATOH <ssato redhat.com>
# License: MIT
#
# Suppress warning of list_engines
# pylint: disable=unused-import
"""anytemplate.api - API of anytemplate module."""
from __future__ import annotations

import logging
import os.path
import sys
import typing

import anytemplate.compat
import anytemplate.engine
import anytemplate.globals
import anytemplate.utils

from anytemplate.globals import (
    TemplateNotFound, TemplateEngineNotFound, CompileError  # noqa: F401
)
from anytemplate.engine import find_by_filename as list_engines  # noqa: F401

if typing.TYPE_CHECKING:
    from .engines.base import Engine
    from .datatypes import (
        PathType, MaybePath, MaybeCtx
    )


LOGGER: logging.Logger = logging.getLogger(__name__)


def find_engine(
    filepath: MaybePath = None, name: MaybePath = None
) -> typing.Type[Engine]:
    """
    :param filepath: Template file path
    :param name: Specify the name of template engine to use explicitly or
        None; it will be selected automatically anyhow.

    :return: Template engine class found
    """
    if name is None:
        engines = anytemplate.engine.find_by_filename(filepath)
        if not engines:
            raise TemplateEngineNotFound(f"filename={filepath!s}")

        return engines[0]  # It should have highest priority.

    engine = anytemplate.engine.find_by_name(name)
    if engine is None:
        raise TemplateEngineNotFound(f"(template) name={name!s}")

    return engine


def ask_user_tmpl(
    template: typing.Optional[str] = None,
    filepath: MaybePath = None
) -> str:
    _tpath = (filepath or "") if template is None else ""
    return input(
        "\nPlease enter an absolute or relative path starting "
        f"from '.' of missing template file {_tpath}"
    ).strip()


def _render(
    template: typing.Optional[str] = None, filepath: MaybePath = None,
    context: MaybeCtx = None,
    at_paths: typing.Optional[list[str]] = None,
    at_encoding: str = anytemplate.compat.ENCODING,
    at_engine: typing.Optional[str] = None,
    at_ask_missing: bool = False,
    at_cls_args: typing.Optional[dict] = None,
    _at_usr_tmpl: MaybePath = None,
    **kwargs
) -> str:
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
    if filepath is None and template is None:
        raise ValueError(
            "filepath or template must be something other than None."
        )

    ecls = find_engine(filepath, at_engine)
    LOGGER.debug("Use the template engine: %s", ecls.name())
    engine = ecls() if at_cls_args is None else ecls(**at_cls_args)
    tpaths: list[str] = anytemplate.utils.mk_template_paths(filepath, at_paths)

    if filepath is None:
        (render_fn, target) = (engine.renders, template)
    else:
        (render_fn, target) = (engine.render, filepath)

    try:
        return render_fn(
            target, context=context, at_paths=tpaths,
            at_encoding=at_encoding, **kwargs
        )
    except TemplateNotFound as exc:
        LOGGER.warning("** Missing template[s]: paths=%r", tpaths)
        if not at_ask_missing:
            raise TemplateNotFound(str(exc)) from exc

        if _at_usr_tmpl is None:
            _at_usr_tmpl = ask_user_tmpl(template, filepath)

        usr_tmpl = anytemplate.utils.normpath(_at_usr_tmpl)
        if template is None:
            LOGGER.debug("Render %s instead of %s", usr_tmpl, filepath)
            target = usr_tmpl

        return render_fn(
            target, context=context,
            at_paths=(tpaths + [os.path.dirname(usr_tmpl)]),
            at_encoding=at_encoding, **kwargs
        )
    except Exception as exc:
        raise CompileError(f"exc={exc!r}, template={target[:200]}") from exc


def renders(template: str, context: MaybeCtx = None, **options) -> str:
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


def render(filepath: PathType, context: MaybeCtx = None, **options) -> str:
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


def render_to(
    filepath: PathType, context: MaybeCtx = None, output: MaybePath = None,
    at_encoding: str = anytemplate.compat.ENCODING, **options
) -> None:
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
