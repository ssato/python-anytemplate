#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""string.Template support.
"""
from __future__ import absolute_import

import logging
import string
import anytemplate.engines.base
import anytemplate.compat

from anytemplate.globals import CompileError


LOGGER = logging.getLogger(__name__)


class Engine(anytemplate.engines.base.Engine):
    """
    Template Engine class to support string.Template included in the standard
    'string' library of python distributions.

    - Limitations: None obvious
    - Supported option parameters specific to string.Template:

      - 'safe' to use string.Template.safe_substitute instead of
        string.Template.substitute to render templates

    - References:

      - Standard library doc, ex.
        https://docs.python.org/2/library/string.html#template-strings
    """

    _name = "string.Template"
    _priority = 50

    def renders_impl(self, template_content, context, at_paths=False,
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
                raise CompileError(str(exc))

    def render_impl(self, template, context, at_paths=None,
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
        read_content = anytemplate.engines.base.fallback_render
        tmpl = read_content(template, {}, at_paths=at_paths,
                            at_encoding=at_encoding)
        return self.renders_impl(tmpl, context, safe=safe)

# vim:sw=4:ts=4:et:
