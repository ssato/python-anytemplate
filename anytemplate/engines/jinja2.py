#
# Author: Satoru SATOH <ssto at redhat.com>
# License: MIT
#
"""Template engine to add support of `Jinja2 <http://jinja.pocoo.org>`_ .

- Limitations: None obvious except that only FileSystemLoader is supported.
- Supported option parameters specific to Jinja2:

  - Option parameters are passed to jinja2.Environment.__init__().

  - The parameter 'loader' is not supported because anytemplate only supports
    jinja2.loaders.FileSystemLoader.

  - Supported: block_start_string, block_end_string, variable_start_string,
    variable_end_string, comment_start_string, comment_end_string,
    line_statement_prefix, line_comment_prefix, trim_blocks, lstrip_blocks,
    newline_sequence, keep_trailing_newline, extensions, optimized, undefined,
    finalize, autoescape, cache_size, auto_reload, bytecode_cache

- References:

  - http://jinja.pocoo.org/docs/dev/api/
  - http://jinja.pocoo.org/docs/dev/templates/
"""
from __future__ import absolute_import

import os.path
import os

import jinja2.exceptions   # :throw: ImportError if missing
import jinja2

import anytemplate.compat
import anytemplate.engines.base

from anytemplate.globals import TemplateNotFound
from anytemplate.compat import ENCODING


class Engine(anytemplate.engines.base.Engine):
    """
    Template engine class to support Jinja2.
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

    def _render(self, template, context, is_file, at_paths=None,
                at_encoding=ENCODING, **kwargs):
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

    def renders_impl(self, template_content, context, **opts):
        """
        Render given template string and return the result.

        :param template_content: Template content
        :param context: A dict or dict-like object to instantiate given
            template file
        :param opts: Options such as:
            - at_paths: Template search paths
            - at_encoding: Template encoding
            - other keyword options passed to jinja2.Envrionment. Please note
              that 'loader' option is not supported because anytemplate does
              not support to load template except for files

        :return: Rendered string

        >>> egn = Engine()
        >>> tmpl_s = 'a = {{ a }}, b = "{{ b }}"'
        >>> ctx = {'a': 1, 'b': 'bbb'}
        >>> egn.renders_impl(tmpl_s, ctx, at_paths=['.']) == 'a = 1, b = "bbb"'
        True
        """
        return self._render(template_content, context, False, **opts)

    def render_impl(self, template, context, **opts):
        """
        Render given template file and return the result.

        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param opts: Options such as:
            - at_paths: Template search paths
            - at_encoding: Template encoding
            - other keyword options passed to jinja2.Envrionment. Please note
              that 'loader' option is not supported because anytemplate does
              not support to load template except for files

        :return: Rendered string
        """
        return self._render(os.path.basename(template), context, True, **opts)

# vim:sw=4:ts=4:et:
