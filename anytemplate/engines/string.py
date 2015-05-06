#
# Author: Satoru SATOH <ssato redhat.com>
# License: BSD3
#
"""
Template engine based on string.Template which in standard library.
"""
from __future__ import absolute_import

import logging
import string
import anytemplate.engines.base
import anytemplate.compat


LOGGER = logging.getLogger(__name__)


class Engine(anytemplate.engines.base.Engine):

    _name = "string.Template"
    _priority = 50

    def renders_impl(self, template_content, context=None, at_paths=False,
                     at_encoding=anytemplate.compat.ENCODING,
                     safe=False, **kwargs):
        """
        Inherited class must implement this!

        :param template_content: Template content
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param safe: Safely substitute parameters in templates, that is,
            original template content will be returned if some of template
            parameters are not found in given context
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: To be rendered string in inherited classes
        """
        if safe:
            return string.Template(template_content).safe_substitute(context)
        else:
            try:
                return string.Template(template_content).substitute(context)
            except KeyError as exc:
                raise anytemplate.engines.base.CompileError(str(exc))

    def render_impl(self, template, context=None, at_paths=None,
                    at_encoding=anytemplate.compat.ENCODING,
                    safe=False, **kwargs):
        """
        Inherited class must implement this!

        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param at_encoding: Template encoding
        :param safe: Safely substitute parameters in templates, that is,
            original template content will be returned if some of template
            parameters are not found in given context
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: To be rendered string in inherited classes
        """
        with anytemplate.compat.copen(template, encoding=at_encoding) as tmpl:
            return self.renders_impl(tmpl.read(), context, safe=safe)

# vim:sw=4:ts=4:et:
