=============
anytemplate
=============

About
======

.. image:: https://pypip.in/version/anytemplate/badge.svg
   :target: https://pypi.python.org/pypi/anytemplate/
   :alt: [Latest Version]

.. image:: https://pypip.in/py_versions/anytemplate/badge.svg
   :target: https://pypi.python.org/pypi/anytemplate/
   :alt: [Python versions]

.. .. image:: https://pypip.in/license/anytemplate/badge.png
   :target: https://pypi.python.org/pypi/anytemplate/
   :alt: [MIT License]

.. image:: https://api.travis-ci.org/ssato/python-anytemplate.png?branch=master
   :target: https://travis-ci.org/ssato/python-anytemplate
   :alt: [Test status]

.. image:: https://coveralls.io/repos/ssato/python-anytemplate/badge.png
   :target: https://coveralls.io/r/ssato/python-anytemplate
   :alt: [Coverage Status]

.. image:: https://landscape.io/github/ssato/python-anytemplate/master/landscape.png
   :target: https://landscape.io/github/ssato/python-anytemplate/master
   :alt: [Code Health]

This is a python library works as an abstraction layer for various python
template engines and rendering libraries, and provide a few very simple and
easily understandable APIs to render templates.

It also provide a CLI tool called anytemplate_cli to render templates written
in these various template languages.

- Author: Satoru SATOH <ssato@redhat.com>
- License: MIT

It supports the following template engines currently:

.. csv-table::
   :header: "Name", "Notes"
   :widths: 15, 65

   `string.Template <https://www.python.org>`_ , Always available as it's included in python standard lib.
   `jinja2 <http://jinja.pocoo.org>`_ , Highest priory will be given and becomes default if found
   `mako <http://www.makotemplates.org>`_ ,
   `tenjin <http://www.kuwata-lab.com/tenjin/>`_ , renders() API is not supported
   `Cheetah <http://www.cheetahtemplate.org>`_ , Only available for python 2.x as it does not look supporting python 3.x
   `pystache <https://github.com/defunkt/pystache>`_ ,

Features
==========

- Provides very simple and unified APIs for various template engines:

  - anytemplate.renders() to render given template string
  - anytemplate.render() to render given template file

- Can process template engine specific options:

  - anytemplate.render{s,} allow passing option parameters specific to each template rendering functions behind this library
  - anytemplate.find_engine() returns an 'engine' object to allow some more fine tunes of template engine specific customization by passing option parameters to them

- Provide a CLI tool called anytemplate_cli to process templates in command line

API Usage
============

API Examples
--------------

Call 'anytemplate.renders' to render given template strings like this:

.. code-block:: python

    result = anytemplate.renders("{{ x|default('aaa') }}", {'x': 'bbb'},
                                 at_engine="jinja2")

The first parameter is a template string itself. And the second one is a dict
or dict-like object which is generally called as 'context' object to
instantiate templates. The third one, keyword parameter 'at_engine' is needed
to find the appropriate template engine to render given template string. This
keyword parameter is necessary because it's very difficult and should be almost
impossible for any template languages to detect correct template engine only by
given template string itself.

If 'at_engine' is omitted, a template engine of highest priority is choosen.
Only available template engines and libraries are enabled automatically in
anytemplate, so that that engine will be vary in accordance with your
environment. For example, 'jinja2' is the engine of highest priority in my
development envrionment with all supported template engines and libraries
installed:

.. code-block:: python

   In [6]: import anytemplate

   In [7]: anytemplate.find_engine()   # It will return the highest priority one.
   Out[7]: anytemplate.engines.jinja2.Engine

   In [8]: anytemplate.find_engine().name()
   Out[8]: 'jinja2'

It's also possible to some option parameters specific to the template engine
choosen with keyword parameters like this:

.. code-block:: python

    # 'strict_undefined' is a parameter for mako.template.Template.__init__().
    result = anytemplate.renders("${x}", {'x': 'bbb'},
                                 at_engine="mako",
                                 strict_undefined=False)

For details such as generic option parameters list of 'anytemplate.renders',
see its help:

.. code-block:: python

  In [20]: help(anytemplate.renders)
  Help on function renders in module anytemplate.api:

  renders(template_content, context=None, at_paths=None, at_encoding='UTF-8', at_engine=None, at_ask_missing=False, at_cls_args=None, **kwargs)
      Compile and render given template content and return the result string.

      :param template_content: Template content
      :param context: A dict or dict-like object to instantiate given
          template file
      :param at_paths: Template search paths
      :param at_encoding: Template encoding
      :param at_engine: Specify the name of template engine to use explicitly or
          None to find it automatically anyhow.
      :param at_cls_args: Arguments passed to instantiate template engine class
      :param kwargs: Keyword arguments passed to the template engine to
          render templates with specific features enabled.

      :return: Rendered string

  In [21]:

Call 'anytemplate.render' to render given template file like this:

.. code-block:: python

    result1 = anytemplate.render("/path/to/a_template.tmpl", {'x': 'bbb'},
                                 at_engine="mako")

    result2 = anytemplate.render("another_template.t", {'y': 'ccc'},
                                 at_engine="tenjin",
                                 at_paths=['/path/to/templates/', '.'])

The parameters are similar to the previous example except for the first one.

The first parameter is not a template string but a path of template file, may
be relative or absolute path, or basename with template search paths
(at_paths=[PATH_0, PATH_1, ...]) given.

Some module wraps actual template engines in anytemplate supports automatic
detection of the engine by file extensions of template files. For example,
Jinja2 template files of which expected file extensions are '.j2' or '.jinja2'
typically. So I made that such files are automatically detected as jinja2
template file and you don't need to specify the engine by 'at_engine' parameter
like this:

.. code-block:: python

    # 'jinaj2' template engine is automatically choosen because the extension
    # of template file is '.j2'.
    result = anytemplate.render("/path/to/a_template.j2", {'x': 'bbb'})

For details such as option parameters list of 'anytemplate.render',
see its help:

.. code-block:: python

  In [21]: help(anytemplate.render)
  Help on function render in module anytemplate.api:

  render(filepath, context=None, at_paths=None, at_encoding='UTF-8', at_engine=None, at_ask_missing=False, at_cls_args=None, **kwargs)
      Compile and render given template file and return the result string.

      :param template: Template file path
      :param context: A dict or dict-like object to instantiate given
          template file
      :param at_paths: Template search paths
      :param at_encoding: Template encoding
      :param at_engine: Specify the name of template engine to use explicitly or
          None to find it automatically anyhow.
      :param at_cls_args: Arguments passed to instantiate template engine class
      :param kwargs: Keyword arguments passed to the template engine to
          render templates with specific features enabled.

      :return: Rendered string

  In [22]:

CLI Usage
============

CLI help
-----------

.. code-block:: console

  ssato@localhost% PYTHONPATH=. python anytemplate/cli.py -h
  Usage: anytemplate/cli.py [OPTION ...] TEMPLATE_FILE

  Options:
    -h, --help            show this help message and exit
    -T TEMPLATE_PATHS, --template-path=TEMPLATE_PATHS
                          Template search path can be specified multiple times.
                          Note: Dir in which given template exists is always
                          included in the search paths (at the end of the path
                          list) regardless of this option.
    -C CONTEXTS, --context=CONTEXTS
                          Specify file path and optionally its filetype, to
                          provides context data to instantiate templates.  The
                          option argument's format is
                          [type:]<file_name_or_path_or_glob_pattern> ex. -C
                          json:common.json -C ./specific.yaml -C yaml:test.dat,
                          -C yaml:/etc/foo.d/*.conf
    -E ENGINE, --engine=ENGINE
                          Specify template engine name such as 'jinja2'
    -L, --list-engines    List supported template engines in your environment
    -o OUTPUT, --output=OUTPUT
                          Output filename [stdout]
    -v, --verbose         Verbose mode
    -q, --quiet           Quiet mode
  ssato@localhost% cat examples/ctx.yml
  xs:
    - name: Alice
    - name: Bob
    - name: John

  ssato@localhost% cat examples/jinja2.j2
  {% include "jinja2-incl.j2" %}
  ssato@localhost% cat examples/jinja2-incl.j2
  {# jinja2 example: #}
  {% for x in xs if x.name -%}
  {{ x.name }}
  {% endfor %}
  ssato@localhost% PYTHONPATH=. python anytemplate/cli.py -E jinja2 \
  > -C examples/ctx.yml examples/jinja2.j2

  Alice
  Bob
  John

  ssato@localhost%

CLI Features
-----------------

Multiple context files support to define template parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The CLI tool (anytemplate_cli) supports to load multiple context files in YAML
or JSON or others to give template parameters with -C|--context option.

Loading and composing of context files are handled by my another python library
called anyconfig (python-anyconfig) if installed and available on your system.

- anyconfig on PyPI: http://pypi.python.org/pypi/anyconfig/
- python-anyconfig on github: https://github.com/ssato/python-anyconfig

If anyconfig is not found on your system, only JSON context files are supported
format of context files, by help of python standard json or simplejson library.

Template search paths
^^^^^^^^^^^^^^^^^^^^^^^

The CLI tool (anytemplate_cli) supports to specify the template search
paths with -T|--template-path option. This is useful when using 'include'
directive in templates; ex. -T .:templates/.

NOTE: The default search path will be [., dir_in_which_given_template_file_is]
where templatedir is the directory in which the given template file exists if
-T option is not given.  And even if -T option is used, templatedir will be
appended to that search paths at the end.

Build & Install
================

If you're Fedora or Red Hat Enterprise Linux user, you can build and install
[s]rpm by yourself:

.. code-block:: console

   $ python setup.py srpm && mock dist/python-anytemplate-<ver_dist>.src.rpm

or:

.. code-block:: console

   $ python setup.py rpm

Otherwise, try usual ways to build and/or install python modules such like 'pip
install git+https://github.com/ssato/python-anytemplate' and 'python setup.py
bdist', etc.

Hacking
===========

How to test
-------------

Try to run '[WITH_COVERAGE=1] ./pkg/runtest.sh [path_to_python_code]'.

TODO & Issues
===============

- Add descriptions (doctext) of template engine and library specific options: WIP
- Add descriptions (doctext) how anytemplate wraps each template engine and library: WIP
- Complete unit tests of each template engine and library including template engine specific options, etc.
- Stablize public and private (internal) APIs:

  - Private APIs still needs a lot of work especially. It's very vague how it should be as each template engine have its own concept and design and I'm not sure how to abstract them.
  - I don't think public APIs have large issues but these be affected by changes of private APIs more or less; I'm thinking to deprecate the keyword parameter 'at_cls_args' for example.

Misc
======

Alternatives
---------------

There are a few libraries works like this:

- TemplateAlchemy: https://pypi.python.org/pypi/TemplateAlchemy/
- collective.templateengines: https://pypi.python.org/pypi/collective.templateengines

These look more feature-rich and comprehensive, but I prefer a lot more
lightweight and thin wrapper library along with CLI tool (template renderer) so
that I made anytemplate.

And:

- python-jinja2-cli: https://github.com/ssato/python-jinja2-cli

Anytemplate is a successor of python-jinja2-cli.

.. vim:sw=2:ts=2:et:
