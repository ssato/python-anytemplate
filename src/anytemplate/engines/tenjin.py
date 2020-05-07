#
# Copyright (c) 2015 - 2018 by Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=unused-import
"""Template engine to add support of
`Tenjin <http://www.kuwata-lab.com/tenjin/>`_ .

- Limitations:

  - Rendering template content string is not supported. That is,
    Engine.renders() does nothing but return given template content string
    itself because Tenjin does not look supporting that.

  - It seems that Tenjin can process templates written in various character
    encoding sets other than UTF-8 but tenjin.set_template_encoding() is called
    at the head of this module so that its capability is not available, I
    think.

- Supported option parameters specific to Tenjin:

  - Option parameters passed to tenjin.Engine.__init__:

    - Supported: prefix, postfix, layout, path, cache, preprocess,
      templateclass, preprocessorclass, lang, loader, pp
    - The sum value of keyword parameters both at_paths and path will be passed
      to tenjin.Template.__init__() as the keyword parameter "path" which
      represents template search paths.

  - Option parameters passed to tenjin.Engine.render{s,}: globals and layout

- References:

  - http://www.kuwata-lab.com/tenjin/pytenjin-users-guide.html
"""
from __future__ import absolute_import

import logging
import os.path
import os
import tempfile
import tenjin  # :throw: ImportError

import anytemplate.compat
import anytemplate.engines.base
import anytemplate.utils

# TODO: It seems that tenjin forces this to make it work factually.
from tenjin.helpers import (  # noqa: F401
    CaptureContext, cache_as, capture_as,
    captured_as, echo, echo_cached, escape, fragment_cache,
    generate_tostrfunc, html, new_cycle, not_cached, start_capture,
    stop_capture, to_str, unquote
)

tenjin.set_template_encoding('utf-8')  # FIXME


LOGGER = logging.getLogger(__name__)


class Engine(anytemplate.engines.base.Engine):
    """
    Template engine class to support Tenjin.
    """
    _name = "tenjin"
    _priority = 30

    # .. note:: Template '.pyhtml' appear in its example doc.
    _file_extensions = ["pythml"]

    # see `help(tenjin.Engine.__init__)` and `help(tenjin.Engine.render)`.
    _engine_valid_opts = ("prefix", "postfix", "layout", "path", "cache",
                          "preprocess", "templateclass", "preprocessorclass",
                          "lang", "loader", "pp")
    _render_valid_opts = ("globals", "layout")

    def __init__(self, **kwargs):
        """
        see `help(tenjin.Engine.__init__)` for options.
        """
        super(Engine, self).__init__(**kwargs)
        self.engine_options = self.filter_options(kwargs,
                                                  self.engine_valid_options())

    def renders_impl(self, template_content, context,
                     at_encoding=anytemplate.compat.ENCODING, **kwargs):
        """
        Render given template string and return the result.

        :param template_content: Template content
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_encoding: Template encoding
        :param kwargs: Keyword arguments such as:
            - at_paths: Template search paths
            - Other keyword arguments passed to the template engine to render
              templates with specific features enabled.

        :return: Rendered string
        """
        tmpdir = os.environ.get("TMPDIR", "/tmp")
        res = template_content
        try:
            (ofd, opath) = tempfile.mkstemp(prefix="at-tenjin-tmpl-",
                                            dir=tmpdir)
            os.write(ofd, template_content.encode(at_encoding))
            os.close(ofd)

            res = self.render_impl(opath, context, **kwargs)
        except (IOError, OSError) as exc:
            LOGGER.error("Failed to render from tempral template: %s"
                         " [exc=%r]", opath, exc)
            raise
        finally:
            try:
                os.remove(opath)
                os.removedirs(os.path.dirname(opath))
            except (IOError, OSError):
                pass

        return res

    def render_impl(self, template, context, at_paths=None, **kwargs):
        """
        Render given template file and return the result.

        :param template: Template file path
        :param context: A dict or dict-like object to instantiate given
            template file
        :param at_paths: Template search paths
        :param kwargs: Keyword arguments passed to the template engine to
            render templates with specific features enabled.

        :return: Rendered string
        """
        # Override the path to pass it to tenjin.Engine.
        if at_paths is not None:
            paths = at_paths + self.engine_options.get("path", [])
            self.engine_options["path"] = paths

        engine = tenjin.Engine(**self.engine_options)
        LOGGER.warning("engine_options=%s", str(self.engine_options))

        kwargs = self.filter_options(kwargs, self.render_valid_options())
        return engine.render(template, context, **kwargs)

# vim:sw=4:ts=4:et:
