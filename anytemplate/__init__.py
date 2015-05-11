"""
.. module:: anytemplate
   :synopsis: A thin interface library for various Python template engines.

Overview
---------

There are many template language and engine libraries in python and each
template engine library provide own way to render templates (template
strings or template files).

For example, jinja2 provides the way to compile template file with given
context such like::

    import jinja2
    import os.path

    def render(tmpl_file, ctx, tmpl_paths):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(tmpl_paths))
        tmpl = env.get_template(os.path.basename(tmpl_file))

        return tmpl.render(**ctx)

    result = render("/path/to/a_jinja2_tmpl.tmpl", {'a': 1, }, ['.'])

and mako does such like::

    import mako.lookup
    import mako.template

    def render(tmpl_file, ctx, tmpl_paths):
        lookup = mako.lookup.TemplateLookup(directories=tmpl_paths)
        tmpl = mako.template.Template(filename=tmpl_file, lookup=lookup)

        return tmpl.render(**ctx)

    result = render("/path/to/a_jinja2_tmpl.tmpl", {'a': 1, }, ['.'])

Sometimes we have to use and/or switch different template engines for each
demands and use cases and then we need to remember how to use them in the ways
that each template engine library provides. I'm too lazy to remember each
template engine's way so that made this library provides a thin abstraction and
interface layer to some template engine libraries.

By using this library, you can simplify the above code like this::

    import anytemplate

    # If the given template file is a jinja2 template file.
    # (replace 'jinja2' with 'mako' for mako template files):
    result = anytemplate.render("/path/to/a_jinja2_tmpl.tmpl", {'a': 1, },
                                at_engine="jinja2")

Usage examples
---------------

To render given template string, you can call :function:`anytemplate.renders`.
Here is an example::

    result = anytemplate.renders("{{ x|default('aaa') }}", {'x': 'bbb'},
                                 at_engine="jinja2")

For details such as option parameters list of :function:`anytemplate.renders`,
see its help; see the output of 'help(anytemplate.renders)', etc.

And to render given template file, you can call :function:`anytemplate.render`.
Here is an example::

    result = anytemplate.render("/path/to/a_template.tmpl", {'x': 'bbb'},
                                at_engine="mako")

Some interface libraries of template engines in anytemplate supports automatic
detection by file extensions. For example, Jinja2 template files of which
expected file extensions are '.j2' or '.jinja2' are automatically detected and
you don't need to specify the engine by 'at_engine' parameter like this::

    result = anytemplate.render("/path/to/a_template.j2", {'x': 'bbb'})

For details such as option parameters list of :function:`anytemplate.render`,
see its help; see the output of 'help(anytemplate.render)', etc.
"""
from __future__ import absolute_import
from .globals import AUTHOR, VERSION, LOGGER
from .api import list_engines, find_engine, renders, render, render_to, \
    TemplateEngineNotFound, TemplateNotFound

__author__ = AUTHOR
__version__ = VERSION

__all__ = [
    "LOGGER",
    "list_engines", "find_engine", "renders", "render", "render_to",
    "TemplateEngineNotFound", "TemplateNotFound",
]

# vim:sw=4:ts=4:et:
