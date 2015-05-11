#
# Author: Satoru SATOH <ssto at redhat.com>
# License: MIT
#
"""jinja2 support
"""
from __future__ import absolute_import

import jinja2.exceptions   # :throw: ImportError if missing
import jinja2
import logging
import os.path
import os

import anytemplate.compat
import anytemplate.engines.base


LOGGER = logging.getLogger(__name__)
ENCODING = anytemplate.compat.ENCODING


class Engine(anytemplate.engines.base.Engine):
    """
    Template Engine class to support `Jinja2 <http://jinja.pocoo.org>`_ .

    - Limitations: None obvious
    - Supported option parameters specific to Jinja2:

      - Option parameters are passed to jinja2.Environment.__init__().

      - The parameter 'loader' is not supported because anytemplate only
        support to load tempaltes by jinja2.loaders.FileSystemLoader.

      - Supported: block_start_string, block_end_string, variable_start_string,
        variable_end_string, comment_start_string, comment_end_string,
        line_statement_prefix, line_comment_prefix, trim_blocks, lstrip_blocks,
        newline_sequence, keep_trailing_newline, extensions, optimized,
        undefined, finalize, autoescape, cache_size, auto_reload,
        bytecode_cache

    - References:

      - http://jinja.pocoo.org/docs/dev/api/
      - http://jinja.pocoo.org/docs/dev/templates/
    """

    _name = "jinja2"
    _file_extensions = ["j2", "jinja2", "jinja"]
    _priority = 10
    _engine_valid_opts = ("block_start_string", "block_end_string",
                          "variable_start_string", "variable_end_string",
                          "comment_start_string", "comment_end_string",
                          "line_statement_prefix", "line_comment_prefix",
                          "trim_blocks", "lstrip_blocks", "newline_sequence",
                          "keep_trailing_newline", "extensions", "optimized",
                          "undefined", "finalize", "autoescape", "cache_size",
                          "auto_reload", "bytecode_cache")
    _render_valid_opts = _engine_valid_opts

    def get_env(self, paths=None, encoding=None):
        """
        :param paths: Template search paths
        :param encoding: Template charset encoding, e.g. utf-8
        """
        if paths is None:
            paths = ['.']

        if encoding is None:
            encoding = ENCODING.lower()

        return jinja2.Environment(loader=jinja2.FileSystemLoader(paths,
                                                                 encoding))

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
        :param kwargs: Keyword arguments passed to jinja2.Envrionment. Please
            note that 'loader' option is not supported because anytemplate does
            not support to load template except for files

        :return: Rendered string

        >>> engine = Engine()
        >>> s = engine.renders_impl('a = {{ a }}, b = "{{ b }}"',
        ...                         {'a': 1, 'b': 'bbb'})
        >>> assert s == 'a = 1, b = "bbb"'
        """
        try:
            env = self.get_env(at_paths, at_encoding.lower())
            tmpl = env.from_string(template_content)

            return tmpl.render(**context)

        except jinja2.exceptions.TemplateNotFound as e:
            raise anytemplate.engines.base.TemplateNotFound(str(e))

    def render_impl(self, template, context, at_paths=None,
                    at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        Render given template file and return the result.

        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to jinja2.Envrionment. Please
            note that 'loader' option is not supported because anytemplate does
            not support to load template except for files


        :return: Rendered string
        """
        try:
            env = self.get_env(at_paths, at_encoding.lower())
            tmpl = env.get_template(os.path.basename(template))

            return tmpl.render(**context)

        except jinja2.exceptions.TemplateNotFound as e:
            raise anytemplate.engines.base.TemplateNotFound(str(e))

# vim:sw=4:ts=4:et:
