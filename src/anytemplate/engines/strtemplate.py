#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
"""Template engine to add support of string.Template included in the standard
'string' library of python distributions.

- Limitations: None obvious
- Supported option parameters specific to string.Template:

  - 'safe' to use string.Template.safe_substitute instead of
    string.Template.substitute to render templates

- References:

  - Standard library doc, ex.
    https://docs.python.org/2/library/string.html#template-strings
"""
from __future__ import absolute_import

import string

import anytemplate.compat
import anytemplate.engines.base
import anytemplate.globals


def renders(template_content, context, **options):
    """
    :param template_content: Template content
    :param context:
        A dict or dict-like object to instantiate given template file
    :param options: Options such as:

        - at_paths: Template search paths (common option)
        - at_encoding: Template encoding (common option)
        - safe: Safely substitute parameters in templates, that is,
          original template content will be returned if some of template
          parameters are not found in given context

    :return: Rendered string
    """
    if options.get("safe", False):
        return string.Template(template_content).safe_substitute(context)
    else:
        try:
            return string.Template(template_content).substitute(context)
        except KeyError as exc:
            raise anytemplate.globals.CompileError(str(exc))


class Engine(anytemplate.engines.base.Engine):
    """
    Template engine class to support string.Template.
    """
    _name = "string.Template"
    _priority = 50

    renders_impl = anytemplate.engines.base.to_method(renders)

    def render_impl(self, template, context, **options):
        """
        Inherited class must implement this!

        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param options: Same options as :meth:`renders_impl`

            - at_paths: Template search paths (common option)
            - at_encoding: Template encoding (common option)
            - safe: Safely substitute parameters in templates, that is,
              original template content will be returned if some of template
              parameters are not found in given context

        :return: To be rendered string in inherited classes
        """
        ropts = dict((k, v) for k, v in options.items() if k != "safe")
        tmpl = anytemplate.engines.base.fallback_render(template, {}, **ropts)
        return self.renders_impl(tmpl, context, **options)

# vim:sw=4:ts=4:et:
