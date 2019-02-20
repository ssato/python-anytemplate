#
# Copyright (c) 2015 by Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""
Template engine to add support of `Cheetah <http://www.cheetahtemplate.org>`_ .

- Limitation: Cheetah does not support python 3 so it's not work in python 3
  environment at all.

- Supported option parameters specific to Cheetah:

  - source, namespaces, searchList, file: Supported but 'source' passed to
    render() and 'file' passed to renders() will be ignored.
  - filter, filtersLib, errorCatcher, compilerSettings, etc.

- References:

  - http://www.cheetahtemplate.org/docs/users_guide_html/
  - help(Cheetah.Template.Template)
  - help(Cheetah.Template.Template.compile)
"""
from __future__ import absolute_import

try:
    from Cheetah.Template import Template  # :throw: ImportError
except ImportError:
    Template = None

import anytemplate.compat
import anytemplate.engines.base


def render_impl(**kwargs):
    """
    :param tmpl: Template content string or file
    :param at_paths: Template search paths
    """
    if Template is None:
        tmpl = kwargs.get("file", None)
        if tmpl is None:
            tmpl = kwargs.get("source", None)
            return anytemplate.engines.base.fallback_renders(tmpl)

        return anytemplate.engines.base.fallback_render(tmpl, None, **kwargs)

    return Template(**kwargs).respond()


class Engine(anytemplate.engines.base.Engine):
    """
    Template Engine class to support Cheetah.
    """
    _name = "cheetah"
    _priority = 30

    # _engine_valid_opts: parameters for Cheetah.Template.Template
    # _render_valid_opts: same as the above currently
    #
    # TODO: Process parameters for Cheetah.Template.Template.{compile,respond}
    _engine_valid_opts = ("source", "namespaces", "searchList",
                          "file", "filter", "filtersLib", "errorCatcher",
                          "compilerSettings", "_globalSetVars",
                          "_preBuiltSearchList")
    _render_valid_opts = _engine_valid_opts

    @classmethod
    def supports(cls, template_file=None):
        """
        :return: Whether the engine can process given template file or not.
        """
        if anytemplate.compat.IS_PYTHON_3:
            cls._priority = 99
            return False  # Always as it's not ported to python 3.

        return super(Engine, cls).supports(template_file=template_file)

    def __init__(self, **kwargs):
        """
        see `help(Cheetah.Template.Template)` for options.
        """
        super(Engine, self).__init__(**kwargs)
        self.engine_options = self.filter_options(kwargs,
                                                  self.engine_valid_options())

    def __render(self, context, **kwargs):
        """
        Render template.

        :param context: A dict or dict-like object to instantiate given
            template file
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: Rendered string
        """
        # Not pass both searchList and namespaces.
        kwargs["namespaces"] = [context, ] + kwargs.get("namespaces", []) \
                                           + kwargs.get("searchList", [])
        kwargs["searchList"] = None

        # TODO:
        # if at_paths is not None:
        #    paths = at_paths + self._engine_valid_opts.get(..., [])
        #    ...
        kwargs = self.filter_options(kwargs, self.engine_valid_options())
        self.engine_options.update(kwargs)

        return render_impl(**self.engine_options)

    def renders_impl(self, template_content, context, **kwargs):
        """
        Render given template string and return the result.

        :param template_content: Template content
        :param context: A dict or dict-like object to instantiate given
            template file
        :param kwargs: Keyword arguments such as:
            - at_paths: Template search paths but it is not actually processed
              in this module (TODO)
            - at_encoding: Template encoding but it is not actually prcoessed
              in this module (TODO)
            - Other keyword arguments passed to the template engine to render
              templates with specific features enabled.

        :return: Rendered string
        """
        if "file" in kwargs:
            kwargs["file"] = None

        kwargs["source"] = template_content

        return self.__render(context, **kwargs)

    def render_impl(self, template, context, **kwargs):
        """
        Render given template file and return the result.

        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param kwargs: Keyword arguments such as:
            - at_paths: Template search paths but it is not actually processed
              in this module (TODO)
            - at_encoding: Template encoding but it is not actually prcoessed
              in this module (TODO)
            - Other keyword arguments passed to the template engine to render
              templates with specific features enabled.

        :return: Rendered string
        """
        if "source" in kwargs:
            kwargs["source"] = None

        kwargs["file"] = template

        return self.__render(context, **kwargs)

# vim:sw=4:ts=4:et:
