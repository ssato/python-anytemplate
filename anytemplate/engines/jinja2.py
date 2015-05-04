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

import logging
import os.path
import os

import anytemplate.compat
import anytemplate.engines.base
import anytemplate.utils

try:
    import jinja2.exceptions
    import jinja2

    SUPPORTED = True
except ImportError:
    SUPPORTED = False

LOGGER = logging.getLogger(__name__)


# Fallbacks:
def fallback_renders(template_content, ctx=None, paths=None):
    """
    Just returns tmpl_s as jinja2 is not available.

    :param tmpl_s: Template string
    :param ctx: Context dict needed to instantiate templates
    :param paths: Template search paths

    >>> fallback_renders("{{ a }}")
    '{{ a }}'
    """
    LOGGER.warn("Jinja2 is missing and not supported in your system")
    return template_content


def fallback_render(filepath, ctx, paths=None):
    """
    Just returns the content of filepath as jinja2 is not available.

    :param filepath: (Base) filepath of template file
    :param ctx: Context dict needed to instantiate templates
    :param paths: Template search paths

    # TODO:
    # >>>> assert fallback_render(__file__) == open(__file__).read()
    """
    tmpl = anytemplate.utils.find_template_from_path(filepath, paths)
    if tmpl is None:
        raise anytemplate.engines.base.TemplateNotFound(filepath)

    return anytemplate.compat.copen(filepath).read()


if SUPPORTED:
    def get_env(paths):
        """
        :param paths: Template search paths
        """
        return jinja2.Environment(loader=jinja2.FileSystemLoader(paths))

    # pylint: disable=no-value-for-parameter
    def renders(tmpl_s, ctx, paths=[os.curdir]):
        """
        Compile and render given template string `tmpl_s` with context
        `context`.

        :param tmpl_s: Template string
        :param ctx: Context dict needed to instantiate templates
        :param paths: Template search paths

        >>> s = renders('a = {{ a }}, b = "{{ b }}"', {'a': 1, 'b': 'bbb'})
        >>> assert s == 'a = 1, b = "bbb"'
        """
        try:
            return get_env(paths).from_string(tmpl_s).render(**ctx)
        except jinja2.exceptions.TemplateNotFound as e:
            raise anytemplate.engines.base.TemplateNotFound(str(e))

    def render(filepath, ctx, paths=None):
        """
        Compile and render template, and return the result.

        :param filepath: (Base) filepath of template file
        :param ctx: Context dict needed to instantiate templates
        :param paths: Template search paths
        """
        try:
            paths = anytemplate.utils.mk_template_paths(filepath, paths)
            tmpl = get_env(paths).get_template(os.path.basename(filepath))

            return tmpl.render(**ctx)
        except jinja2.exceptions.TemplateNotFound as e:
            raise anytemplate.engines.base.TemplateNotFound(str(e))

    # pylint: enable=no-value-for-parameter
else:
    renders = fallback_renders
    render = fallback_render


class Jjnja2Engine(anytemplate.engines.base.BaseEngine):

    _name = "jinja2"
    _file_extensions = ["j2", "jinja2"]
    _supported = SUPPORTED
    _priority = 10

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
        return renders(template_content, context, paths=at_paths)

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
        return render(template, context, paths=at_paths)

# vim:sw=4:ts=4:et:
