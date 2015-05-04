#
# Author: Satoru SATOH <ssato redhat.com>
# License: BSD3
#
"""
Standard string module based template engine in python dist.
"""
from __future__ import absolute_import

import logging

import anytemplate.compat
import anytemplate.utils


LOGGER = logging.getLogger(__name__)


class TemplateNotFound(Exception):
    """
    Exception during rendering template[s] and any of templates are missing.
    """
    pass


class CompileError(Exception):
    """
    Excepction indicates any errors during template compilation.
    """
    pass


class BaseEngine(object):

    _name = "base"
    _file_extensions = []
    _supported = False
    _priority = 99

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
        :return: Whether the engine is supported (able to work)?
        """
        if template_file is None:
            return cls._supported
        else:
            return cls._supported and \
                (anytemplate.utils.get_file_extension(template_file) in
                 cls.file_extensions())

    @classmethod
    def priority(cls):
        """
        :return: priority from 0 to 99, smaller gets highter priority.
        """
        return cls._priority

    def __init__(self, **kwargs):
        """
        Instantiate and initialize a template engine object.

        :param kwargs: Keyword arguments passed to the template engine to
            configure/setup its specific features.
        """
        LOGGER.debug("Intialize %s with kwargs: %s", self.name(),
                     ", ".join("%s=%s" % (k, v) for k, v in kwargs.items()))

    def renders_impl(self, template_content, context=None, at_paths=None,
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

        :return: To be rendered string in inherited classes
        """
        raise NotImplementedError("Inherited class must implement this!")

    def render_impl(self, template, context=None, at_paths=None,
                    at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: To be rendered string in inherited classes
        """
        raise NotImplementedError("Inherited class must implement this!")

    def renders(self, template_content, context=None, at_paths=None,
                at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        :param template_content: Template content
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: Rendered string
        """
        LOGGER.debug("Render template %s... %s context",
                     template_content[:10],
                     "without" if context is None else "with a")
        return self.renders_impl(template_content, context, at_paths=at_paths,
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
        LOGGER.debug("Render template %s %s context" %
                     template, "without" if context is None else "with a")
        return self.render_impl(template, context, at_paths=at_paths,
                                at_encoding=at_encoding, **kwargs)

# vim:sw=4:ts=4:et:
