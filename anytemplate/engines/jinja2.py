"""
    Jinja2 based template renderer.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Compiles and render Jinja2-based template files.

    :copyright: (c) 2012 - 2015 Red Hat, Inc.
    :copyright: (c) 2012 by Satoru SATOH <ssato@redhat.com>
    :license: BSD-3

References: http://jinja.pocoo.org,
    especially http://jinja.pocoo.org/docs/api/#basics
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

    _name = "jinja2"
    _file_extensions = ["j2", "jinja2"]
    _priority = 10

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

        >>> engine = Engine()
        >>> s = engine.renders_impl('a = {{ a }}, b = "{{ b }}"',
        ...                         {'a': 1, 'b': 'bbb'})
        >>> assert s == 'a = 1, b = "bbb"'
        """
        try:
            env = self.get_env(at_paths, at_encoding.lower())
            tmpl = env.from_string(template_content)

            if context is None:
                context = {}

            return tmpl.render(**context)

        except jinja2.exceptions.TemplateNotFound as e:
            raise anytemplate.engines.base.TemplateNotFound(str(e))

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
        try:
            env = self.get_env(at_paths, at_encoding.lower())
            tmpl = env.get_template(os.path.basename(template))

            return tmpl.render(**context)

        except jinja2.exceptions.TemplateNotFound as e:
            raise anytemplate.engines.base.TemplateNotFound(str(e))

# vim:sw=4:ts=4:et:
