#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
import os.path
import difflib
import tempfile


def selfdir():
    """
    :return: module path itself
    """
    return os.path.dirname(__file__)


def setup_workdir():
    """
    :return: Path of the created working dir
    """
    return tempfile.mkdtemp(dir="/tmp", prefix="python-anytemplate-tests-")


def cleanup_workdir(workdir):
    """
    FIXME: Danger!
    """
    os.system("rm -rf " + workdir)


def diff(result, exp):
    """
    Print unified diff.

    :param result: Result string
    :param exp: Expected result string
    """
    diff = difflib.unified_diff(result.splitlines(), exp.splitlines(),
                                'Result', 'Expected')
    return "\n'" + "\n".join(diff) + "'"

# vim:sw=4:ts=4:et:
