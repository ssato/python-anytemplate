#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: BSD3
#
"""
CLI frontend for various template engines.
"""
from __future__ import absolute_import
from __future__ import print_function

import logging
import operator
import optparse  # argparse is not available in python 2.6 standard lib.
import sys

import anytemplate.api
import anytemplate.engine
import anytemplate.globals
import anytemplate.utils


LOGGER = anytemplate.globals.LOGGER


def option_parser():
    """
    :return: Option parsing object :: optparse.OptionParser
    """
    defaults = dict(template_paths=[], contexts=[], output='-',
                    engine=None, list_engines=False, verbose=1)

    p = optparse.OptionParser("%prog [OPTION ...] TEMPLATE_FILE")
    p.set_defaults(**defaults)

    p.add_option("-T", "--template-path", action="append",
                 dest="template_paths",
                 help="Template search path can be specified multiple times. "
                      "Note: Dir in which given template exists is always "
                      "included in the search paths (at the end of "
                      "the path list) regardless of this option. ")
    p.add_option("-C", "--context", action="append", dest="contexts",
                 help="Specify file path and optionally its filetype, to "
                      "provides context data to instantiate templates. "
                      " The option argument's format is "
                      " [type:]<file_name_or_path_or_glob_pattern>"
                      " ex. -C json:common.json -C ./specific.yaml -C "
                      "yaml:test.dat, -C yaml:/etc/foo.d/*.conf")
    p.add_option("-E", "--engine",
                 help="Specify template engine name such as 'jinja2'")
    p.add_option("-L", "--list-engines", action="store_true",
                 help="List supported template engines in your environment")
    p.add_option("-o", "--output", help="Output filename [stdout]")
    p.add_option("-v", "--verbose", action="store_const", const=0,
                 help="Verbose mode")
    p.add_option("-q", "--quiet", action="store_const", const=2,
                 dest="verbose", help="Quiet mode")
    return p


def get_loglevel(level):
    """
    Set log level.

    >>> assert get_loglevel(2) == logging.WARN
    >>> assert get_loglevel(10) == logging.INFO
    """
    try:
        return [logging.DEBUG, logging.INFO, logging.WARN][level]
    except IndexError:
        return logging.INFO


def main(argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    if not args and not options.list_engines:
        p.print_help()
        sys.exit(0)

    LOGGER.setLevel(get_loglevel(options.verbose))

    if options.list_engines:
        ecs = sorted((e for e in anytemplate.engine.ENGINES),
                      key=operator.methodcaller("priority"))
        print(", ".join("%s (%s)" % (e.name(), e.priority()) for e in ecs))
        return

    tmpl = args[0]
    ctx = anytemplate.utils.parse_and_load_contexts(options.contexts)
    res = anytemplate.api.render(tmpl, ctx, at_paths=options.template_paths,
                                 at_engine=options.engine, at_ask_missing=True)
    anytemplate.utils.write_to_output(res, options.output)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
