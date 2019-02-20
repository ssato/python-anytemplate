#
# Copyright (C) 2015 - 2018 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name
"""Tests of anytempalte.cli
"""
from __future__ import absolute_import

import os.path
import os
import subprocess
import unittest

import anytemplate.cli as TT
import tests.common

from anytemplate.engine import find_by_name


_CWD = os.path.abspath(os.path.join(tests.common.selfdir(), ".."))
_RUN_CLI = "PYTHONPATH=./src/ python ./src/anytemplate/cli.py"


def run_and_check_exit_code(args=None, code=0):
    """
    Run main() and check its exit code.
    """
    try:
        TT.main(["dummy"] + ([] if args is None else args))
    except SystemExit as exc:
        return exc.code == code

    return True


class Test00(unittest.TestCase):

    def run_and_check_exit_code(self, args=None, code=0, _not=False):
        if args is None:
            args = []
        if _not:
            self.assertFalse(run_and_check_exit_code(args, code))
        else:
            self.assertTrue(run_and_check_exit_code(args, code))

    def test_10_main__wo_args(self):
        self.run_and_check_exit_code(code=1)

    def test_12__show_usage(self):
        self.run_and_check_exit_code(["--help"])

    def test_14__wrong_option(self):
        self.run_and_check_exit_code(["--wrong-option-xyz"], _not=True)

    def test_20_main__wo_args(self):
        self.assertRaises(SystemExit, TT.main, [])

    def test_22_main__show_usage(self):
        self.assertRaises(SystemExit, TT.main, ["dummy", "--help"])

    def test_24_main__show_usage(self):
        self.assertRaises(SystemExit, TT.main, ["dummy", "--wrong-option"])

    def test_26_main__list_engines(self):
        self.assertRaises(SystemExit, TT.main, ["dummy", "--list-engines"])


class Test10(tests.common.TestsWithWorkdir):

    def run_and_check_exit_code(self, args=None, code=0, _not=False):
        if args is None:
            args = []
        if _not:
            self.assertFalse(run_and_check_exit_code(args, code))
        else:
            self.assertTrue(run_and_check_exit_code(args, code))

    def test_10_main__strtemplate(self):
        tmpl = os.path.join(self.workdir, "test.tmpl")
        ctx = os.path.join(self.workdir, "ctx.yml")
        output = os.path.join(self.workdir, "output.txt")
        open(tmpl, 'w').write("$a\n")
        open(ctx, 'w').write("a: aaa\n")

        self.run_and_check_exit_code(["-E", "string.Template", "-C", ctx,
                                      "-o", output, tmpl])
        self.assertEqual(open(output).read(), "aaa\n")

    def test_20_main__jinja2(self):
        if find_by_name("jinja2"):
            tmpl = os.path.join(self.workdir, "test.j2")
            output = os.path.join(self.workdir, "output.txt")
            open(tmpl, 'w').write("{{ hello|default('hello') }}")

            self.run_and_check_exit_code(["-o", output, tmpl])
            self.assertEqual(open(output).read(), "hello")


class Test20(tests.common.TestsWithWorkdir):

    def test_10_strtemplate_read_ctx_from_stdin(self):
        tmpl = os.path.join(self.workdir, "test.tmpl")
        open(tmpl, 'w').write("$a\n")

        out = subprocess.check_output("echo 'a: aaa' | "
                                      "%s -E string.Template -C yaml:- "
                                      "-o - %s" % (_RUN_CLI, tmpl),
                                      cwd=_CWD, shell=True)
        self.assertEqual(out.rstrip(), tests.common.to_bytes("aaa"))

    def test_20_strtemplate_read_tmpl_from_stdin(self):
        ctx = os.path.join(self.workdir, "ctx.yml")
        open(ctx, 'w').write("a: aaa\n")

        out = subprocess.check_output("echo '$a' | "
                                      "%s -E string.Template -C yaml:%s "
                                      "-o - -" % (_RUN_CLI, ctx),
                                      cwd=_CWD, shell=True)
        self.assertEqual(out.rstrip(), tests.common.to_bytes("aaa"))

# vim:sw=4:ts=4:et:
