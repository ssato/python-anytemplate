#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
# pylint: disable=unused-argument, no-self-use
"""
Base class for template engine implementations.
"""
from __future__ import absolute_import

import logging

import anytemplate.compat
import anytemplate.utils

from anytemplate.globals import TemplateNotFound


LOGGER = logging.getLogger(__name__)


def fallback_renders(template_content, *args, **kwargs):
    """
    Render given template string `template_content`.

    This is a basic implementation actually does nothing and just returns
    original template content `template_content`.

    :param template_content: Template content
    :return: Rendered result string
    """
    return template_content


def fallback_render(template, context, at_paths=None,
                    at_encoding=anytemplate.compat.ENCODING,
                    **kwargs):
    """
    Render from given template and context.

    This is a basic implementation actually does nothing and just returns
    the content of given template file `template`.

    :param template: Template file path
    :param context: A dict or dict-like object to instantiate given
        template file
    :param at_paths: Template search paths
    :param at_encoding: Template encoding
    :param kwargs: Keyword arguments passed to the template engine to
        render templates with specific features enabled.

    :return: Rendered result string
    """
    tmpl = anytemplate.utils.find_template_from_path(template, at_paths)
    if tmpl is None:
        raise TemplateNotFound("template: %s" % template)

    try:
        return anytemplate.compat.copen(tmpl).read()
    except UnicodeDecodeError:
        return open(tmpl).read()


def filter_kwargs(keys, kwargs):
    """
    :param keys: A iterable key names to select items
    :param kwargs: A dict or dict-like object reprensents keyword args

    >>> list(filter_kwargs(("a", "b"), dict(a=1, b=2, c=3, d=4)))
    [('a', 1), ('b', 2)]
    """
    for k in keys:
        if k in kwargs:
            yield (k, kwargs[k])


class Engine(object):
    """
    Abstract class implementation of Template Engines.
    """

    _name = "base"
    _file_extensions = []
    _priority = 99  # Lowest priority
    _engine_valid_opts = []
    _render_valid_opts = []

    @classmethod
    def name(cls):
        """
        :return: Template Engine name (! class name)
        """
        return cls._name

    @classmethod
    def file_extensions(cls):
        """
        :return: File extensions this engine can process
        """
        return cls._file_extensions

    @classmethod
    def supports(cls, template_file=None):
        """
        :return: Whether the engine can process given template file or not.
        """
        return (anytemplate.utils.get_file_extension(template_file) in
                cls.file_extensions())

    @classmethod
    def priority(cls):
        """
        :return: priority from 0 to 99, smaller gets highter priority.
        """
        return cls._priority

    @classmethod
    def engine_valid_options(cls):
        """
        :return: A list of template engine specific initialization options
        """
        return cls._engine_valid_opts

    @classmethod
    def render_valid_options(cls):
        """
        :return: A list of template engine specific rendering options
        """
        return cls._render_valid_opts

    @classmethod
    def filter_options(cls, kwargs, keys):
        """
        Make optional kwargs valid and optimized for each template engines.

        :param kwargs: keyword arguements to process
        :param keys: optional argument names

        >>> Engine.filter_options(dict(aaa=1, bbb=2), ("aaa", ))
        {'aaa': 1}
        >>> Engine.filter_options(dict(bbb=2), ("aaa", ))
        {}
        """
        return dict((k, v) for k, v in filter_kwargs(keys, kwargs))

    def __init__(self, **kwargs):
        """
        Instantiate and initialize a template engine object.

        :param kwargs: Keyword arguments passed to the template engine to
            configure/setup its specific features.
        """
        LOGGER.debug("Intialize %s with kwargs: %s", self.name(),
                     ", ".join("%s=%s" % (k, v) for k, v in kwargs.items()))

    def renders_impl(self, template_content, context, at_paths=None,
                     at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        Render from given template content and context.

        :param template_content: Template content
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: Rendered string
        """
        # LOGGER.warn("Inherited class must implement this!")
        return fallback_renders(template_content, context, at_paths=at_paths,
                                at_encoding=at_encoding, **kwargs)

    def render_impl(self, template, context, at_paths=None,
                    at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: Rendered string
        """
        # LOGGER.warn("Inherited class must implement this!")
        return fallback_render(template, context, at_paths=at_paths,
                               at_encoding=at_encoding, **kwargs)

    def renders(self, template_content, context=None, at_paths=None,
                at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        :param template_content: Template content
        :param context: A dict or dict-like object to instantiate given
            template file or None
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: Rendered string
        """
        kwargs = self.filter_options(kwargs, self.render_valid_options())
        paths = anytemplate.utils.mk_template_paths(None, at_paths)
        if context is None:
            context = {}

        LOGGER.debug("Render template %s... %s context, options=%s",
                     template_content[:10],
                     "without" if context is None else "with a",
                     str(kwargs))
        return self.renders_impl(template_content, context, at_paths=paths,
                                 at_encoding=at_encoding, **kwargs)

    def render(self, template, context=None, at_paths=None,
               at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: Rendered string
        """
        kwargs = self.filter_options(kwargs, self.render_valid_options())
        paths = anytemplate.utils.mk_template_paths(template, at_paths)
        if context is None:
            context = {}

        LOGGER.debug("Render template %s %s context, options=%s",
                     template, "without" if context is None else "with a",
                     str(kwargs))
        return self.render_impl(template, context, at_paths=paths,
                                at_encoding=at_encoding, **kwargs)

# vim:sw=4:ts=4:et:
