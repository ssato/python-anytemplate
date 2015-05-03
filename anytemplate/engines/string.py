#
# Author: Satoru SATOH <ssato redhat.com>
# License: BSD3
#
"""
Standard string module based template engine in python dist.
"""
from __future__ import absolute_import

import logging
import string
import anytemplate.engines.base
import anytemplate.compat


LOGGER = logging.getLogger(__name__)


class StringTemplateEngine(anytemplate.engines.base.BaseEngine):

    _name = "string"
    _supported = True

    def renders_impl(self, template_content, context=None, at_safe=False,
                     **kwargs):
        """
        Inherited class must implement this!

        :param template_content: Template content
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_safe: Try to render template[s] safely, that is,
            it will not raise any exceptions and returns the content of
            template file itself if any error occurs
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: To be rendered string in inherited classes
        """
        if at_safe:
            return string.Template(template_content).safe_substitute(context)
        else:
            try:
                return string.Template(template_content).substitute(context)
            except KeyError as exc:
                raise anytemplate.engines.base.CompileErrorException(str(exc))

    def render_impl(self, template, context=None, at_safe=False,
                    at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        Inherited class must implement this!

        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_safe: Try to render template[s] safely, that is,
            it will not raise any exceptions and returns the content of
            template file itself if any error occurs
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: To be rendered string in inherited classes
        """
        with anytemplate.compat.copen(template, encoding=at_encoding) as tmpl:
            return self.renders_impl(tmpl.read(), context, at_safe)

# vim:sw=4:ts=4:et:
