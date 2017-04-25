#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import os.path
import os
import difflib
import tempfile
import unittest


def selfdir():
    """
    :return: module path itself
    """
    return os.path.dirname(__file__)


def setup_workdir():
    """
    :return: Path of the created working dir
    """
    return tempfile.mkdtemp(dir="/tmp", prefix="python-tests-")


def cleanup_workdir(workdir):
    """
    FIXME: Danger!
    """
    os.system("rm -rf " + workdir)


class TestsWithWorkdir(unittest.TestCase):

    def setUp(self):
        self.workdir = setup_workdir()

    def tearDown(self):
        cleanup_workdir(self.workdir)

    def test_00_workdir_exists(self):
        os.path.exists(self.workdir)


class TempDir(object):

    def __init__(self):
        self._dir = None

    def __enter__(self):
        self._dir = setup_workdir()
        return self._dir

    def __exit__(self, _type, _value, _traceback):
        os.removedirs(self._dir)


def diff(result, exp):
    """
    Print unified diff.

    :param result: Result string
    :param exp: Expected result string
    """
    diff_ = difflib.unified_diff(result.splitlines(), exp.splitlines(),
                                 'Result', 'Expected')
    return "\n'" + "\n".join(diff_) + "'"

# vim:sw=4:ts=4:et:
