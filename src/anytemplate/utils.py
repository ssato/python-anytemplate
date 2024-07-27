# -*- coding: utf-8 -*-
"""
:copyright: (c) 2012 - 2018 by Satoru SATOH <ssato@redhat.com>
:license: MIT
"""
# unicode_literals ?
from __future__ import absolute_import, print_function, annotations

import codecs
import glob
import itertools
import logging
import os.path
import os
import sys
import typing

import anytemplate.compat

if typing.TYPE_CHECKING:
    import collections.abc


LOGGER = logging.getLogger(__name__)


def get_output_stream(
    encoding: str = anytemplate.compat.ENCODING,
    ostream: typing.IO = sys.stdout
) -> codecs.StreamWriter:
    """
    Get output stream take care of characters encoding correctly.

    :param ostream: Output stream (file-like object); sys.stdout by default
    :param encoding: Characters set encoding, e.g. UTF-8
    :return: sys.stdout can output encoded strings

    >>> get_output_stream("UTF-8")  # doctest: +ELLIPSIS
    <encodings.utf_8.StreamWriter ... at 0x...>
    """
    return codecs.getwriter(encoding)(ostream)


def uniq(items: list) -> list:
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


def chaincalls(
    callables: collections.abc.Iterable[collections.abc.Callable],
    obj: typing.Any
) -> typing.Any:
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
            raise ValueError(f"Not callable: {fun!r}")
        obj = fun(obj)

    return obj


def normpath(path: str) -> str:
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


def concat(
    xss: collections.abc.Iterable[collections.abc.Iterable]
) -> collections.abc.Iterable:
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
    return list(itertools.chain.from_iterable(xs for xs in xss))


def parse_filespec(
    fspec: str, sep: str = ':', gpat: str = '*'
) -> list[tuple[str, typing.Optional[str]]]:
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
        (ftype, fpath) = tuple(fspec.split(sep))
    else:
        (ftype, fpath) = (None, fspec)

    if gpat in fspec:
        return [
            (fs, ftype) for fs in sorted(glob.glob(fpath))
        ]

    return [(fpath, ftype)]


def load_context(
    ctx_path: str, ctx_type: str, scm: typing.Optional[str] = None
) -> dict:
    """
    :param ctx_path: context file path or '-' (read from stdin)
    :param ctx_type: context file type
    :param scm: JSON schema file in any formats anyconfig supports, to
        validate given context files
    """
    if ctx_path == '-':
        return anytemplate.compat.json_loads(
            sys.stdin.read(), ac_parser=ctx_type, ac_schema=scm
        )

    return anytemplate.compat.json_load(
        ctx_path, ac_parser=ctx_type, ac_schema=scm
    )


def parse_and_load_contexts(
    contexts: list[str], schema: typing.Optional[str] = None,
    werr: bool = False
) -> dict:
    """
    :param contexts: list of context file specs
    :param schema: JSON schema file in any formats anyconfig supports, to
        validate given context files
    :param werr: Exit immediately if True and any errors occurrs
        while loading context files
    """
    ctx: dict = {}
    diff = None

    if contexts:
        for ctx_path, ctx_type in concat(parse_filespec(c) for c in contexts):
            if ctx_type is None or not ctx_type:
                ctx_type = "json"  # default file type.
            try:
                diff = load_context(ctx_path, ctx_type, scm=schema)
                if diff is not None:
                    anytemplate.compat.merge(ctx, diff)
            except (IOError, OSError, AttributeError):
                if werr:
                    raise
    return ctx


def _write_to_filepath(content: str, output: str) -> None:
    """
    :param content: Content string to write to
    :param output: Output file path
    """
    outdir = os.path.dirname(output)
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir)

    with anytemplate.compat.copen(output, 'w') as out:
        out.write(content)


def write_to_output(
    content: str,
    output: typing.Optional[str] = None,
    encoding: str = anytemplate.compat.ENCODING
) -> None:
    """
    :param content: Content string to write to
    :param output: Output destination
    :param encoding: Character set encoding of outputs
    """
    if not isinstance(content, str):
        content = str(content, encoding)

    if output and not output == '-':
        _write_to_filepath(content, output)
    else:
        print(content)


def mk_template_paths(
    filepath: typing.Optional[str],
    paths: typing.Optional[list[str]] = None
) -> list[str]:
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


def find_template_from_path(
    filepath: str, paths: typing.Optional[list[str]] = None
) -> typing.Optional[str]:
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
