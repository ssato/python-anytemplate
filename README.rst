=============
anytemplate
=============

About
======

.. image:: https://api.travis-ci.org/ssato/python-anytemplate.png?branch=master
   :target: https://travis-ci.org/ssato/python-anytemplate
   :alt: Test status

.. image:: https://coveralls.io/repos/ssato/python-anytemplate/badge.png
   :target: https://coveralls.io/r/ssato/python-anytemplate
   :alt: Coverage Status

.. image:: https://landscape.io/github/ssato/python-anytemplate/master/landscape.png
   :target: https://landscape.io/github/ssato/python-anytemplate/master
   :alt: Code Health

Anytemplate, a successor of jinja2-cli [#]_ , is a python library to provide an
abstraction layer for various python template engines and rendering libraries.
It works as a thin layer for these templates and also provide a simple CLI
tool.

- Author: Satoru SATOH <ssato@redhat.com>
- License: Same as python-jinja2, that is, BSD3.

Anytemplate supports the following template engines currently:

- standard string template (string.Template)
- jinja2: http://jinja.pocoo.org
- mako: http://www.makotemplates.org
- tenjin: http://www.kuwata-lab.com/tenjin/

.. [#] https://github.com/ssato/python-jinja2-cli

Features
=========

Multiple configuration files support
-------------------------------------

Anytemplate supports multiple configuration files in YAML or JSON or others to
set parameters w/ -C|--contexts option, ex. -C a.yaml -C b.yaml -C c.json.

Loading and composition of config files are handled by another python library
called anyconfig (python-anyconfig) if installed and available on your system.

- anyconfig on PyPI: http://pypi.python.org/pypi/anyconfig/
- python-anyconfig on github: https://github.com/ssato/python-anyconfig

Template search paths
-----------------------

It supports setting template search paths w/ -T|--template-paths. This is
useful when using 'include' directive in templates; ex. -T .:templates/.

NOTE: The default search path will be [., templatedir] where templatedir is the
directory in which the given template file exists if -T option is not given.
And even if -T option is used, templatedir will be appended to that search
paths at the end.

Usage
=======

Help
-------

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
    -o OUTPUT, --output=OUTPUT
                          Output filename [stdout]
    -v, --verbose         Verbose
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

Examples
---------

TBD

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

Hacks
=======

How to test
-------------

Try to run '[WITH_COVERAGE=1] ./pkg/runtest.sh [path_to_python_code]'.

Alternatives
================

There are few libraries works like this:

- TemplateAlchemy: https://pypi.python.org/pypi/TemplateAlchemy/
- collective.templateengines: https://pypi.python.org/pypi/collective.templateengines

These look more feature-rich and comprehensive, but I prefer a lot more
lightweight and thin wrapper library along with CLI tool (template renderer) so
that I made this.

.. vim:sw=2:ts=2:et:
