#
# Copyright (c) 2015 by Satoru SATOH <ssato @ redhat.com>
# License: BSD-3
#
"""Render Mako-based template files.
"""
from __future__ import absolute_import

import logging
import mako.template  # :throw: ImportError
import mako.lookup

import anytemplate.compat
import anytemplate.engines.base
import anytemplate.utils


LOGGER = logging.getLogger(__name__)


class Engine(anytemplate.engines.base.Engine):

    _name = "mako"
    _priority = 30

    # _engine_valid_opts: parameters for mako.lookup.TemplateLookup
    # _render_valid_opts: parameters for mako.template.Template
    #
    # :see: http://docs.makotemplates.org/en/latest/usage.html
    _engine_valid_opts = ("directories", "collection_size",
                          "filesystem_checks", "modulename_callable")
    _render_valid_opts = ("uri", "format_exceptions", "error_handler",
                          "output_encoding", "encoding_errors",
                          "module_directory",
                          "cache_args", "cache_impl", "cache_enabled",
                          "cache_type", "cache_dir", "cache_url",
                          "module_filename", "input_encoding",
                          "disable_unicode", "module_writer",
                          "bytestring_passthrough", "default_filters",
                          "buffer_filters", "strict_undefined",
                          "imports", "future_imports", "enable_loop",
                          "preprocessor", "lexer_cls")

    def __init__(self, **kwargs):
        """
        see `help(tenjin.Engine.__init__)` for options.
        """
        self.lookup_options = self.filter_options(kwargs,
                                                  self.engine_valid_options())

    def renders_impl(self, template_content, context=None, at_paths=None,
                     at_encoding=anytemplate.compat.ENCODING,
                     **kwargs):
        """
        Render given template string and return the result.

        :param template_content: Template content
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: Rendered string
        """
        if context is None:
            context = {}

        if "filename" in kwargs:
            kwargs["filename"] = None

        kwargs["text"] = template_content

        if "input_encoding" not in kwargs:
            kwargs["input_encoding"] = at_encoding.lower()

        if "output_encoding" not in kwargs:
            kwargs["output_encoding"] = at_encoding.lower()

        if at_paths is not None:
            paths = at_paths + self.lookup_options.get("directories", [])
            self.lookup_options["directories"] = paths

            lookup = mako.lookup.TemplateLookup(**self.lookup_options)
            kwargs["lookup"] = lookup

        tmpl = mako.template.Template(**kwargs)
        return tmpl.render(**context)

    def render_impl(self, template, context=None, at_paths=None,
                    at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        Render given template file and return the result.

        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: Rendered string
        """
        if context is None:
            context = {}

        if "text" in kwargs:
            kwargs["text"] = None

        if "input_encoding" not in kwargs:
            kwargs["input_encoding"] = at_encoding.lower()

        if "output_encoding" not in kwargs:
            kwargs["output_encoding"] = at_encoding.lower()

        if at_paths is not None:
            paths = at_paths + self.lookup_options.get("directories", [])
            self.lookup_options["directories"] = paths

            lookup = mako.lookup.TemplateLookup(**self.lookup_options)
            kwargs["lookup"] = lookup

            template = anytemplate.utils.find_template_from_path(template,
                                                                 paths)
        # else:
        #     template = anytemplate.utils.find_template_from_path(template)

        kwargs["filename"] = template

        tmpl = mako.template.Template(**kwargs)
        return tmpl.render(**context)

# vim:sw=4:ts=4:et:
