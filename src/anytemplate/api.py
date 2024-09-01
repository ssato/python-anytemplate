#
# Copyright (C) 2015 - 2024 Satoru SATOH <ssato redhat.com>
# License: MIT
#
# Suppress warning of list_engines
# pylint: disable=unused-import
"""anytemplate.api - API of anytemplate module."""
from __future__ import annotations

import logging
import pathlib
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
    import collections.abc

    from .engines.base import Engine
    from .datatypes import (
        PathType, MaybePath, MaybeCtx
    )


LOGGER: logging.Logger = logging.getLogger(__name__)


def find_engine(
    filepath: MaybePath = None, name: MaybePath = None,
    at_cls_args: typing.Optional[dict] = None,
) -> Engine:
    """
    :param filepath: Template file path
    :param name: Specify the name of template engine to use explicitly or
        None; it will be selected automatically anyhow.
    :param at_cls_args: Arguments passed to instantiate template engine class

    :return: Template engine class found
    """
    eopts = at_cls_args or {}

    if name:
        engine = anytemplate.engine.find_by_name(name)
        if engine is None:
            raise TemplateEngineNotFound(f"(template) name={name!s}")
        return engine(**eopts)

    engines = anytemplate.engine.find_by_filename(filepath)
    if not engines:
        raise TemplateEngineNotFound(f"filename={filepath!s}")

    return engines[0](**eopts)  # It should have highest priority.


def ask_user_tmpl(tpaths: list[str]) -> typing.Optional[pathlib.Path]:
    """Ask users a template path to use."""
    maybe_path: pathlib.Path = pathlib.Path(
        input(
            "\nPlease enter an absolute or relative path to "
            "your template file."
        ).strip()
    )
    maybe_path.resolve()

    if maybe_path.exists():
        return maybe_path

    # Try to find the tempalte from searching paths.
    for tpath in tpaths:
        candidate = pathlib.Path(tpath) / maybe_path
        if candidate.exists():
            candidate.resolve()
            return candidate

    return None


def _render(
    template: str,  # content or file path
    render_fn: collections.abc.Callable,
    context: MaybeCtx = None,
    at_ask_missing: bool = False,
    is_str_template: bool = False,
    **options
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
    :param options: Keyword arguments passed to the template engine to
        render templates with specific features enabled.

    :return: Rendered string
    """
    tpaths: list[str] = anytemplate.utils.mk_template_paths(
        None if is_str_template else template, options.get("at_paths", None)
    )
    if "at_paths" in options:
        del options["at_paths"]

    try:
        return render_fn(
            template, context=context, at_paths=tpaths, **options
        )
    except TemplateNotFound as exc:
        LOGGER.warning("Missing template[s]: paths=%r", tpaths)
        if at_ask_missing:
            tmpl = ask_user_tmpl(tpaths)  # :: pathlib.Path
        else:
            raise TemplateNotFound(str(exc)) from exc

        if tmpl is None:
            tpaths_s: str = ", ".join(tpaths)
            msg = f"Missing Template: {template!s}, paths={tpaths_s}"
            raise TemplateNotFound(msg) from exc

        tpaths = tpaths + [str(tmpl.parent)]
        return render_fn(
            str(tmpl), context=context, at_paths=tpaths, **options
        )
    except Exception as exc:
        msg = f"exc={exc!r}, template={template[:200]}, context={context!r}"
        raise CompileError(msg) from exc


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
    engine = find_engine(
        None, options.get("at_engine", None),
        options.get("at_cls_args", None)
    )
    return _render(
        template, engine.renders, context=context, **options
    )


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
        return renders(sys.stdin.read(), context=context, **options)

    engine = find_engine(
        filepath, options.get("at_engine", None),
        options.get("at_cls_args", None)
    )
    return _render(
        filepath, engine.render, context=context, **options
    )


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
