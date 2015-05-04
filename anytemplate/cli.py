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
import optparse  # argparse is not available in python 2.6 dist.
import sys

import anytemplate.api
import anytemplate.utils


LOGGER = logging.getLogger(__name__)


def option_parser(argv=sys.argv):
    defaults = dict(template_paths=[], contexts=[], output='-',
                    engine_name=None, verbose=1)

    p = optparse.OptionParser("%prog [OPTION ...] TEMPLATE_FILE", prog=argv[0])
    p.set_defaults(**defaults)

    p.add_option("-T", "--template-paths", action="append",
                 help="Template search path can be specified multiple times. "
                      "Note: Dir in which given template exists is always "
                      "included in the search paths (at the end of "
                      "the path list) regardless of this option. ")
    p.add_option("-C", "--contexts", action="append",
                 help="Specify file path and optionally its filetype, to "
                      "provides context data to instantiate templates. "
                      " The option argument's format is "
                      " [type:]<file_name_or_path_or_glob_pattern>"
                      " ex. -C json:common.json -C ./specific.yaml -C "
                      "yaml:test.dat, -C yaml:/etc/foo.d/*.conf")
    p.add_option("-E", "--engine_name", help="Specify engine name")
    p.add_option("-o", "--output", help="Output filename [stdout]")
    p.add_option("-v", "--verbose", action="store_const", const=0,
                 help="Verbose")
    p.add_option("-q", "--quiet", action="store_const", const=2,
                 dest="verbose", help="Quiet mode")
    return p


def set_loglevel(level, logger=LOGGER):
    """
    Set log level.
    """
    try:
        lvl = [logging.DEBUG, logging.INFO, logging.WARN][level]
    except IndexError:
        lvl = logging.INFO

    logger.setLevel(lvl)


def main(argv):
    p = option_parser(argv)
    (options, args) = p.parse_args(argv[1:])

    if not args:
        p.print_help()
        sys.exit(0)

    set_loglevel(options.verbose)

    tmpl = args[0]
    ctx = anytemplate.utils.parse_and_load_contexts(options.contexts,
                                                    options.werror)
    res = anytemplate.api.render(tmpl, ctx, at_paths=options.paths,
                                 at_engine=options.engine_name,
                                 at_ask_missing=True)
    anytemplate.utils.write_to_output(res, options.output)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:
