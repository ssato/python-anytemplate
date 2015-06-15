#
# Copyright (c) 2015 by Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-import
"""Tenjin support.
"""
from __future__ import absolute_import

import logging
import tenjin  # :throw: ImportError
tenjin.set_template_encoding('utf-8')  # FIXME

# TODO: It seems that tenjin forces this to make it work factually.
from tenjin.helpers import CaptureContext, cache_as, capture_as, \
    captured_as, echo, echo_cached, escape, fragment_cache, \
    generate_tostrfunc, html, new_cycle, not_cached, start_capture, \
    stop_capture, to_str, unquote  # flake8: noqa

import anytemplate.compat
import anytemplate.engines.base
import anytemplate.utils


LOGGER = logging.getLogger(__name__)


class Engine(anytemplate.engines.base.Engine):
    """
    Template Engine class to support
    `Tenjin <http://www.kuwata-lab.com/tenjin/>`_ .

    - Limitations:

      - Rendering template content string is not supported. That is,
        Engine.renders() does nothing but return given template content string
        itself because Tenjin does not look supporting that.

      - It seems that Tenjin can process templates written in various character
        encoding sets other than UTF-8 but tenjin.set_template_encoding() is
        called at the head of this module so that its capability is not
        available, I think.

    - Supported option parameters specific to Tenjin:

      - Option parameters passed to tenjin.Engine.__init__:

        - Supported: prefix, postfix, layout, path, cache, preprocess,
          templateclass, preprocessorclass, lang, loader, pp
        - The sum value of keyword parameters both at_paths and path will be
          passed to tenjin.Template.__init__() as the keyword parameter "path"
          which represents template search paths.

      - Option parameters passed to tenjin.Engine.render{s,}: globals and
        layout

    - References:

      - http://www.kuwata-lab.com/tenjin/pytenjin-users-guide.html
    """

    _name = "tenjin"
    _priority = 30

    # TODO: Template '.pyhtml' appear in its example doc.
    _file_extensions = ["pythml"]

    # see `help(tenjin.Engine.__init__)` and `help(tenjin.Engine.render)`.
    _engine_valid_opts = ("prefix", "postfix", "layout", "path", "cache",
                          "preprocess", "templateclass", "preprocessorclass",
                          "lang", "loader", "pp")
    _render_valid_opts = ("globals", "layout")

    def __init__(self, **kwargs):
        """
        see `help(tenjin.Engine.__init__)` for options.
        """
        super(Engine, self).__init__(**kwargs)
        self.engine_options = self.filter_options(kwargs,
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
        LOGGER.warn("Just return given template content as tenjin does not "
                    "support render template content directly !")
        return template_content

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
        # Override the path to pass it to tenjin.Engine.
        if at_paths is not None:
            paths = at_paths + self.engine_options.get("path", [])
            self.engine_options["path"] = paths

        engine = tenjin.Engine(**self.engine_options)
        LOGGER.warn("engine_options=%s", str(self.engine_options))

        return engine.render(template, context, **kwargs)

# vim:sw=4:ts=4:et:
