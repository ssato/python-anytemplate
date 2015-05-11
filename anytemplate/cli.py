#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
"""
CLI frontend for various template engines.
"""
from __future__ import absolute_import
from __future__ import print_function

import logging
import optparse  # argparse is not available in python 2.6 standard lib.
import sys

import anytemplate.api
import anytemplate.globals
import anytemplate.utils


LOGGER = anytemplate.globals.LOGGER


def option_parser():
    """
    :return: Option parsing object :: optparse.OptionParser
    """
    defaults = dict(template_paths=[], contexts=[], output='-',
                    engine=None, list_engines=False, verbose=1)

    psr = optparse.OptionParser("%prog [OPTION ...] TEMPLATE_FILE")
    psr.set_defaults(**defaults)

    psr.add_option("-T", "--template-path", action="append",
                   dest="template_paths",
                   help="Template search path can be specified multiple "
                        "times. Note: Dir in which given template exists is "
                        "always included in the search paths (at the end of "
                        "the path list) regardless of this option. ")
    psr.add_option("-C", "--context", action="append", dest="contexts",
                   help="Specify file path and optionally its filetype, to "
                        "provides context data to instantiate templates. "
                        " The option argument's format is "
                        " [type:]<file_name_or_path_or_glob_pattern>"
                        " ex. -C json:common.json -C ./specific.yaml -C "
                        "yaml:test.dat, -C yaml:/etc/foo.d/*.conf")
    psr.add_option("-E", "--engine",
                   help="Specify template engine name such as 'jinja2'")
    psr.add_option("-L", "--list-engines", action="store_true",
                   help="List supported template engines in your environment")
    psr.add_option("-o", "--output", help="Output filename [stdout]")
    psr.add_option("-v", "--verbose", action="store_const", const=0,
                   help="Verbose mode")
    psr.add_option("-q", "--quiet", action="store_const", const=2,
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
    (options, args) = psr.parse_args(argv[1:])

    if not args and not options.list_engines:
        psr.print_help()
        sys.exit(0)

    LOGGER.setLevel(get_loglevel(options.verbose))

    if options.list_engines:
        ecs = anytemplate.api.list_engines()
        print(", ".join("%s (%s)" % (e.name(), e.priority()) for e in ecs))
        return

    tmpl = args[0]
    ctx = anytemplate.utils.parse_and_load_contexts(options.contexts)
    anytemplate.api.render_to(tmpl, ctx, options.output,
                              at_paths=options.template_paths,
                              at_engine=options.engine, at_ask_missing=True)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
