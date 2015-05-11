#
# Copyright (c) 2015 by Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""Pystache (python implementation of mustache) support.
"""
from __future__ import absolute_import

import logging
import os.path
import pystache.renderer  # :throw: ImportError
import pystache.defaults

import anytemplate.compat
import anytemplate.engines.base


LOGGER = logging.getLogger(__name__)


class Engine(anytemplate.engines.base.Engine):
    """
    Template Engine class to support
    `Pystache <https://github.com/defunkt/pystache>`_ , python implementation
    of `Mustache <https://mustache.github.io>`_ .

    - Limitations: None obvious except for pystache's custom function loading
          feature at present
    - Supported template engine specific option parameters:

      - Supported: file_encoding, string_encoding, decode_errors, search_dirs,
        file_extension, escape, partials, missing_tags

      - Notes: The sum value of keyword parameters both at_paths and
        search_dirs will be passed to pystache.render.Renderer.__init__() as
        the keyword parameter "search_dirs" which represents template search
        paths.

     - References:

       - https://mustache.github.io
       - https://github.com/defunkt/pystache
     """

    _name = "pystache"
    _priority = 30
    _file_extensions = ["mustache"]

    # _engine_valid_opts: parameters for pystache.render.Renderer.__init__()
    # _render_valid_opts: same as the above at present
    #
    # :see:
    # https://github.com/defunkt/pystache/blob/master/pystache/renderer.py#L50
    _engine_valid_opts = ("file_encoding", "string_encoding", "decode_errors",
                          "search_dirs", "file_extension", "escape",
                          "partials", "missing_tags")
    _render_valid_opts = _engine_valid_opts

    def __init__(self, **kwargs):
        """
        see `help(pystache.render.Renderer)` for options.
        """
        super(Engine, self).__init__(**kwargs)
        self._roptions = self.filter_options(kwargs,
                                             self.engine_valid_options())

    def _make_renderer(self, at_paths, at_encoding, **kwargs):
        """
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.
        """
        for eopt in ("file_encoding", "string_encoding"):
            default = self._roptions.get(eopt, at_encoding.lower())
            self._roptions[eopt] = kwargs.get(eopt, default)

        pkey = "search_dirs"
        paths = kwargs.get(pkey, []) + self._roptions.get(pkey, [])
        if at_paths is not None:
            paths = at_paths + paths
        self._roptions[pkey] = paths

        return pystache.renderer.Renderer(**self._roptions)

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
        renderer = self._make_renderer(at_paths, at_encoding, **kwargs)
        ctxs = [] if context is None else [context]

        return renderer.render(template_content, *ctxs)

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
        renderer = self._make_renderer(at_paths, at_encoding, **kwargs)
        ctxs = [] if context is None else [context]

        if os.path.sep in template:  # `template` is in abs/rel-path.
            return renderer.render_path(template, *ctxs)
        else:
            if template.endswith(renderer.file_extension):
                template = os.path.splitext(template)[0]

            return renderer.render_name(template, *ctxs)

# vim:sw=4:ts=4:et:
