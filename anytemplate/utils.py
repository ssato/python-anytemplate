# -*- coding: utf-8 -*-
"""
:copyright: (c) 2012 - 2018 by Satoru SATOH <ssato@redhat.com>
:license: MIT
"""
# unicode_literals ?
from __future__ import absolute_import, print_function

import codecs
import glob
import logging
import os.path
import os
import sys

import anytemplate.compat

try:
    from anyconfig.api import loads, load, merge
except ImportError:
    from anytemplate.compat import (
        json_loads as loads, json_load as load, merge
    )


LOGGER = logging.getLogger(__name__)


def get_output_stream(encoding=anytemplate.compat.ENCODING,
                      ostream=sys.stdout):
    """
    Get output stream take care of characters encoding correctly.

    :param ostream: Output stream (file-like object); sys.stdout by default
    :param encoding: Characters set encoding, e.g. UTF-8
    :return: sys.stdout can output encoded strings

    >>> get_output_stream("UTF-8")  # doctest: +ELLIPSIS
    <encodings.utf_8.StreamWriter ... at 0x...>
    """
    return codecs.getwriter(encoding)(ostream)


def uniq(items):
    """Remove duplicates in given list with its order kept.

    >>> uniq([])
    []
    >>> uniq([1, 4, 5, 1, 2, 3, 5, 10])
    [1, 4, 5, 2, 3, 10]
    """
    acc = items[:1]
    for item in items[1:]:
        if item not in acc:
            acc += [item]

    return acc


def chaincalls(callables, obj):
    """
    :param callables: callable objects to apply to obj in this order
    :param obj: Object to apply callables

    >>> chaincalls([lambda a: a + 1, lambda b: b + 2], 0)
    3
    >>> chaincalls([[]], 0)
    Traceback (most recent call last):
    ValueError: Not callable: '[]'
    """
    for fun in callables:
        if not callable(fun):
            raise ValueError("Not callable: %r" % repr(fun))
        obj = fun(obj)

    return obj


def normpath(path):
    """Normalize given path in various different forms.

    >>> normpath("/tmp/../etc/hosts")
    '/etc/hosts'
    >>> normpath("~root/t")
    '/root/t'
    """
    funcs = [os.path.normpath, os.path.abspath]
    if "~" in path:
        funcs = [os.path.expanduser] + funcs

    return chaincalls(funcs, path)


def flip(pair):
    """
    :param pair: A tuple of pair items

    >>> flip((1, 2))
    (2, 1)
    """
    (fst, snd) = pair
    return (snd, fst)


def concat(xss):
    """
    >>> concat([[]])
    []
    >>> concat((()))
    []
    >>> concat([[1,2,3],[4,5]])
    [1, 2, 3, 4, 5]
    >>> concat([[1,2,3],[4,5,[6,7]]])
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat(((1,2,3),(4,5,[6,7])))
    [1, 2, 3, 4, 5, [6, 7]]
    >>> concat((i, i*2) for i in range(3))
    [0, 0, 1, 2, 2, 4]
    """
    return list(anytemplate.compat.from_iterable(xs for xs in xss))


def parse_filespec(fspec, sep=':', gpat='*'):
    """
    Parse given filespec `fspec` and return [(filetype, filepath)].

    Because anyconfig.load should find correct file's type to load by the file
    extension, this function will not try guessing file's type if not file type
    is specified explicitly.

    :param fspec: filespec
    :param sep: a char separating filetype and filepath in filespec
    :param gpat: a char for glob pattern

    >>> parse_filespec("base.json")
    [('base.json', None)]
    >>> parse_filespec("json:base.json")
    [('base.json', 'json')]
    >>> parse_filespec("yaml:foo.yaml")
    [('foo.yaml', 'yaml')]
    >>> parse_filespec("yaml:foo.dat")
    [('foo.dat', 'yaml')]

    TODO: Allow '*' (glob pattern) in filepath when escaped with '\\', etc.
    # >>> parse_filespec("yaml:bar/*.conf")
    # [('bar/a.conf', 'yaml'), ('bar/b.conf', 'yaml')]
    """
    if sep in fspec:
        tpl = (ftype, fpath) = tuple(fspec.split(sep))
    else:
        tpl = (ftype, fpath) = (None, fspec)

    return [(fs, ftype) for fs in sorted(glob.glob(fpath))] \
        if gpat in fspec else [flip(tpl)]


def load_context(ctx_path, ctx_type, scm=None):
    """
    :param ctx_path: context file path or '-' (read from stdin)
    :param ctx_type: context file type
    :param scm: JSON schema file in any formats anyconfig supports, to
        validate given context files
    """
    if ctx_path == '-':
        return loads(sys.stdin.read(), ac_parser=ctx_type, ac_schema=scm)

    return load(ctx_path, ac_parser=ctx_type, ac_schema=scm)


def parse_and_load_contexts(contexts, schema=None, werr=False):
    """
    :param contexts: list of context file specs
    :param schema: JSON schema file in any formats anyconfig supports, to
        validate given context files
    :param werr: Exit immediately if True and any errors occurrs
        while loading context files
    """
    ctx = dict()
    diff = None

    if contexts:
        for ctx_path, ctx_type in concat(parse_filespec(c) for c in contexts):
            try:
                diff = load_context(ctx_path, ctx_type, scm=schema)
                if diff is not None:
                    merge(ctx, diff)
            except (IOError, OSError, AttributeError):
                if werr:
                    raise
    return ctx


def _write_to_filepath(content, output):
    """
    :param content: Content string to write to
    :param output: Output file path
    """
    outdir = os.path.dirname(output)
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir)

    with anytemplate.compat.copen(output, 'w') as out:
        out.write(content)


def write_to_output(content, output=None,
                    encoding=anytemplate.compat.ENCODING):
    """
    :param content: Content string to write to
    :param output: Output destination
    :param encoding: Character set encoding of outputs
    """
    if anytemplate.compat.IS_PYTHON_3 and isinstance(content, bytes):
        content = str(content, encoding)

    if output and not output == '-':
        _write_to_filepath(content, output)
    elif anytemplate.compat.IS_PYTHON_3:
        print(content)
    else:
        print(content.encode(encoding.lower()), file=get_output_stream())


def mk_template_paths(filepath, paths=None):
    """
    Make template paths from given filepath and paths list.

    :param filepath: (Base) filepath of template file or None
    :param paths: A list of template search paths or None

    >>> mk_template_paths("/tmp/t.j2", [])
    ['/tmp']
    >>> mk_template_paths("/tmp/t.j2", ["/etc"])
    ['/etc', '/tmp']
    >>> mk_template_paths(None, ["/etc"])
    ['/etc']
    """
    if filepath is None:
        return [os.curdir] if paths is None else paths

    tmpldir = os.path.dirname(os.path.abspath(filepath))
    return [tmpldir] if paths is None else paths + [tmpldir]


def find_template_from_path(filepath, paths=None):
    """
    Return resolved path of given template file

    :param filepath: (Base) filepath of template file
    :param paths: A list of template search paths
    """
    if paths is None or not paths:
        paths = [os.path.dirname(filepath), os.curdir]

    for path in paths:
        candidate = os.path.join(path, filepath)
        if os.path.exists(candidate):
            return candidate

    LOGGER.warning("Could not find template=%s in paths=%s", filepath, paths)
    return None

# vim:sw=4:ts=4:et:
