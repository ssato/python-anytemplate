#
# Copyright (c) 2015 by Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Mako support.
"""
from __future__ import absolute_import

import logging
import mako.template  # :throw: ImportError
import mako.lookup

import anytemplate.compat
import anytemplate.engines.base
import anytemplate.utils


LOGGER = logging.getLogger(__name__)


def _render(tmpl, ctx):
    """
    :param tmpl: mako.template.Template object
    :param ctx: A dict or dict-like object to instantiate given
    """
    is_py3k = anytemplate.compat.IS_PYTHON_3
    return tmpl.render_unicode(**ctx) if is_py3k else tmpl.render(**ctx)


class Engine(anytemplate.engines.base.Engine):
    """
    Template Engine class to support `Mako <http://www.makotemplates.org/>`_ .

    - Limitations: None obvious
    - Supported template engine specific option parameters:

      - Engine._engine_valid_opts for mako.lookup.TemplateLookup:

        - Supported: directories, collection_size, filesystem_checks,
          modulename_callable

        - Notes: The sum value of keyword parameters both at_paths and
          directories will be passed to mako.lookup.TemplateLookup.__init__()
          as the keyword parameter "directories" which represents template
          search paths.

      - Engine._render_valid_opts for mako.template.Template:

        - Supported: text, filename, uri, format_exceptions, error_handler,
          output_encoding, encoding_errors, module_directory, cache_args,
          cache_impl, cache_enabled, cache_type, cache_dir, cache_url,
          module_filename, input_encoding, disable_unicode, module_writer,
          bytestring_passthrough, default_filters, buffer_filters,
          strict_undefined, imports, future_imports, enable_loop, preprocessor,
          lexer_cls

        - Notes: 'text' parameter passed to Engine.render() and 'filename'
          parameter passed to Engine.renders() will be ignored because it's
          meaningless.

     - References:

       - http://docs.makotemplates.org/en/latest/
     """

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
        see `help(mako.lookup.TemplateLookup)` for options.
        """
        super(Engine, self).__init__(**kwargs)
        self.lookup_options = self.filter_options(kwargs,
                                                  self.engine_valid_options())

    def renders_impl(self, template_content, context, at_paths=None,
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
        return _render(tmpl, context)

    def render_impl(self, template, context, at_paths=None,
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
        return _render(tmpl, context)

# vim:sw=4:ts=4:et:
