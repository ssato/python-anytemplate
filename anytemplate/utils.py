# -*- coding: utf-8 -*-
"""
:copyright: (c) 2012 - 2015 by Satoru SATOH <ssato@redhat.com>
:license: BSD-3
"""
# TODO: unicode_literals
from __future__ import absolute_import, print_function

import codecs
import glob
import logging
import os.path
import os
import sys

import anytemplate.compat

try:
    from anyconfig.api import container, load
except ImportError:
    container = dict

    try:
        import json
    except ImportError:
        try:
            import simplejson as json
        except ImportError:
            raise ("Could not import any json module to load contexts!"
                   " Aborting...")

    def load(filepath, *args):
        return json.load(open(filepath))

try:
    from anyconfig.utils import get_file_extension  # flake8: noqa
except ImportError:
    def _get_file_extension(filepath):
        """
        >>> get_file_extension("/a/b/c")
        ''
        >>> get_file_extension("/a/b.txt")
        'txt'
        >>> get_file_extension("/a/b/c.tar.xz")
        'xz'
        """
        _ext = os.path.splitext(filepath)[-1]
        if _ext:
            return _ext[1:] if _ext.startswith('.') else _ext
        else:
            return ''


LOGGER = logging.getLogger(__name__)


def get_output_stream(encoding=anytemplate.compat.ENCODING,
                      ostream=sys.stdout):
    """
    Get output stream take care of characters encoding correctly.

    :param ostream: Output stream (file-like object); sys.stdout by default
    :param encoding: Characters set encoding, e.g. UTF-8
    :return: sys.stdout can output encoded strings

    >>> _out = get_output_stream("UTF-8")
    """
    return codecs.getwriter(encoding)(ostream)


def get_input_stream(encoding=anytemplate.compat.ENCODING):
    """
    :param encoding: Chart sets encoding
    :return: sys.stdout can output encoded strings

    >>> _t = get_input_stream("UTF-8")
    """
    return codecs.getreader(encoding)(sys.stdin)


def uniq(xs):
    """Remove duplicates in given list with its order kept.

    >>> uniq([])
    []
    >>> uniq([1, 4, 5, 1, 2, 3, 5, 10])
    [1, 4, 5, 2, 3, 10]
    """
    acc = xs[:1]
    for x in xs[1:]:
        if x not in acc:
            acc += [x]

    return acc


def chaincalls(callables, x):
    """
    :param callables: callable objects to apply to x in this order
    :param x: Object to apply callables

    >>> chaincalls([lambda a: a + 1, lambda b: b + 2], 0)
    3
    """
    for c in callables:
        assert callable(c), "%s is not callable object!" % str(c)
        x = c(x)

    return x


def normpath(path):
    """Normalize given path in various different forms.

    >>> normpath("/tmp/../etc/hosts")
    '/etc/hosts'
    >>> normpath("~root/t")
    '/root/t'
    """
    if "~" in path:
        fs = [os.path.expanduser, os.path.normpath, os.path.abspath]
    else:
        fs = [os.path.normpath, os.path.abspath]

    return chaincalls(fs, path)


def flip(xy):
    """
    :param xy: A tuple of pair items

    >>> flip((1, 2))
    (2, 1)
    """
    (x, y) = xy
    return (y, x)


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

    Because anyconfig.api.load should find correct file's type to load by the
    file extension, this function will not try guessing file's type if not file
    type is specified explicitly.

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

    # FIXME: How to test this?
    # >>> parse_filespec("yaml:bar/*.conf")
    # [('bar/a.conf', 'yaml'), ('bar/b.conf', 'yaml')]

    TODO: Allow '*' (glob pattern) in filepath when escaped with '\\', etc.
    """
    tp = (ft, fp) = tuple(fspec.split(sep)) if sep in fspec else (None, fspec)

    return [(fs, ft) for fs in sorted(glob.glob(fp))] \
        if gpat in fspec else [flip(tp)]


def parse_and_load_contexts(contexts, werr=False,
                            enc=anytemplate.compat.ENCODING):
    """
    :param contexts: list of context file specs
    :param werr: Exit immediately if True and any errors occurrs
        while loading context files
    :param enc: Input encoding of context files (dummy param)
    """
    ctx = container()

    if contexts:
        for fpath, ftype in concat(parse_filespec(f) for f in contexts):
            diff = load(fpath, ftype)
            ctx.update(diff)

    return ctx


def write_to_output(content, output=None,
                    encoding=anytemplate.compat.ENCODING):
    """
    :param content: Content string to write to
    :param output: Output destination
    :param encoding: Character set encoding of outputs
    """
    if anytemplate.compat.IS_PYTHON_3:
        if isinstance(content, bytes):
            content = str(content, encoding)

    if output and not output == '-':
        outdir = os.path.dirname(output)
        if outdir and not os.path.exists(outdir):
            os.makedirs(outdir)

        anytemplate.compat.copen(output, 'w').write(content)
    else:
        if anytemplate.compat.IS_PYTHON_3:
            print(content)
        else:
            print(content.encode("utf-8"), file=get_output_stream())


def mk_template_paths(filepath=None, template_paths=None):
    """
    Make template paths from given filepath and paths list.

    :param filepath: (Base) filepath of template file
    :param template_paths: Template search paths

    >>> fn = __file__
    >>> fdir = os.path.abspath(os.path.dirname(fn))
    >>> assert mk_template_paths(fn, []) == ['.', fdir]
    >>> assert mk_template_paths(fn, ["/etc", ]) == ["/etc", fdir]
    >>> assert mk_template_paths(None, ["/etc", ]) == [os.curdir]
    """
    if filepath is None or not filepath:
        return [os.curdir]

    tmpldir = os.path.dirname(os.path.abspath(filepath))
    if template_paths is None or not template_paths:
        return [os.curdir, tmpldir]  # default:
    else:
        return uniq(template_paths + [tmpldir])


def find_template_from_path(filepath, paths=None):
    """
    Return resolved path of given template file

    :param filepath: (Base) filepath of template file
    :param paths: A list of template search paths
    """
    if paths is None or not paths:
        paths = [os.path.dirname(filepath), os.curdir]

    for p in paths:
        candidate = os.path.join(p, filepath)
        if os.path.exists(candidate):
            return candidate

    LOGGER.warn("Could not find template=%s in paths=%s", filepath, paths)
    return None

# vim:sw=4:ts=4:et:
