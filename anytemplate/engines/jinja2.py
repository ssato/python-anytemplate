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

from anytemplate.globals import TemplateNotFound


LOGGER = logging.getLogger(__name__)
ENCODING = anytemplate.compat.ENCODING


class Engine(anytemplate.engines.base.Engine):
    """
    Template Engine class to support `Jinja2 <http://jinja.pocoo.org>`_ .

    - Limitations: None obvious except for only FileSystemLoader is supported
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

    def __init__(self, **kwargs):
        """
        see `help(jinja2.Environment)` for options.
        """
        super(Engine, self).__init__(**kwargs)
        self._env_options = self.filter_options(kwargs,
                                                self.engine_valid_options())

    def __render(self, template, context, is_file=True, at_paths=None,
                 at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        Render given template string and return the result.

        :param template: Template content
        :param context: A dict or dict-like object to instantiate given
            template file
        :param is_file: True if given `template` is a filename
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to jinja2.Envrionment. Please
            note that 'loader' option is not supported because anytemplate does
            not support to load template except for files

        :return: Rendered string

        """
        eopts = self.filter_options(kwargs, self.engine_valid_options())
        self._env_options.update(eopts)

        loader = jinja2.FileSystemLoader(at_paths, at_encoding.lower())
        env = jinja2.Environment(loader=loader, **self._env_options)
        if kwargs:
            context.update(kwargs)
        try:
            tmpl = (env.get_template if is_file else env.from_string)(template)
            return tmpl.render(**context)
        except jinja2.exceptions.TemplateNotFound as exc:
            raise TemplateNotFound(str(exc))

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
        ...                         {'a': 1, 'b': 'bbb'}, ['.'])
        >>> assert s == 'a = 1, b = "bbb"'
        """
        return self.__render(template_content, context, is_file=False,
                             at_paths=at_paths, at_encoding=at_encoding,
                             **kwargs)

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
        return self.__render(os.path.basename(template), context, is_file=True,
                             at_paths=at_paths, at_encoding=at_encoding,
                             **kwargs)

# vim:sw=4:ts=4:et:
