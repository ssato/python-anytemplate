#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""
CLI frontend for various template engines.
"""
from __future__ import absolute_import
from __future__ import print_function

import argparse
import logging
import sys

import anytemplate.api
import anytemplate.globals
import anytemplate.utils


LOGGER = anytemplate.globals.LOGGER


def option_parser():
    """
    :return: Option parsing object :: optparse.OptionParser
    """
    defaults = dict(template_paths=[], contexts=[], schema=None, output='-',
                    engine=None, list_engines=False, verbose=1)

    psr = argparse.ArgumentParser()
    psr.set_defaults(**defaults)

    psr.add_argument("template", type=str, nargs="?",
                     help="Template file path")
    psr.add_argument("-T", "--template-path", action="append",
                     dest="template_paths",
                     help="Template search path can be specified multiple "
                          "times. Note: Dir in which given template exists is "
                          "always included in the search paths (at the end of "
                          "the path list) regardless of this option. ")
    psr.add_argument("-C", "--context", action="append", dest="contexts",
                     help="Specify file path and optionally its filetype, to "
                          "provides context data to instantiate templates. "
                          " The option argument's format is "
                          " [type:]<file_name_or_path_or_glob_pattern>"
                          " ex. -C json:common.json -C ./specific.yaml -C "
                          "yaml:test.dat, -C yaml:/etc/foo.d/*.conf")
    psr.add_argument("-s", "--schema",
                     help="JSON schema file in any formats anyconfig "
                          "supports, to validate context files")
    psr.add_argument("-E", "--engine",
                     help="Specify template engine name such as 'jinja2'")
    psr.add_argument("-L", "--list-engines", action="store_true",
                     help="List supported template engines in your "
                          "environment")
    psr.add_argument("-o", "--output", help="Output filename [stdout]")
    psr.add_argument("-v", "--verbose", action="store_const", const=0,
                     help="Verbose mode")
    psr.add_argument("-q", "--quiet", action="store_const", const=2,
                     dest="verbose", help="Quiet mode")
    return psr


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


def main(argv=None):
    """
    Entrypoint.
    """
    if argv is None:
        argv = sys.argv

    psr = option_parser()
    args = psr.parse_args(argv[1:])

    if not args.template:
        if args.list_engines:
            ecs = anytemplate.api.list_engines()
            print(", ".join("%s (%s)" % (e.name(), e.priority()) for e in ecs))
            sys.exit(0)
        else:
            psr.print_usage()
            sys.exit(1)

    LOGGER.setLevel(get_loglevel(args.verbose))

    ctx = {}

    if args.contexts:
        LOGGER.info("Loading contexts: %r ...", args.contexts[:3])
        ctx = anytemplate.utils.parse_and_load_contexts(args.contexts,
                                                        args.schema)
    anytemplate.api.render_to(args.template, ctx, args.output,
                              at_paths=args.template_paths,
                              at_engine=args.engine, at_ask_missing=True)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
