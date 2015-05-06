#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
#
import os.path
import os
import subprocess
import unittest

import anytemplate.cli as TT
import anytemplate.tests.common

from anytemplate.engine import find_by_name


CLI_SCRIPT = os.path.join(anytemplate.tests.common.selfdir(), "..", "cli.py")


def run(args=[]):
    """
    :throw: subprocess.CalledProcessError if something goes wrong
    """
    args = ["python", CLI_SCRIPT] + args
    devnull = open("/dev/null", 'w')

    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(anytemplate.tests.common.selfdir(), "..")

    subprocess.check_call(args, stdout=devnull, stderr=devnull, env=env)


def run_and_check_exit_code(args=[], code=0):
    try:
        TT.main(["dummy"] + args)
    except SystemExit as e:
        return e.code == code

    return True


class Test_00(unittest.TestCase):

    def run_and_check_exit_code(self, args=[], code=0, _not=False):
        if _not:
            self.assertFalse(run_and_check_exit_code(args, code))
        else:
            self.assertTrue(run_and_check_exit_code(args, code))

    def test_50_main__wo_args(self):
        self.run_and_check_exit_code()

    def test_10__show_usage(self):
        self.run_and_check_exit_code(["--help"])

    def test_12__wrong_option(self):
        self.run_and_check_exit_code(["--wrong-option-xyz"], _not=True)


class Test_10_with_workdir(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        anytemplate.tests.common.cleanup_workdir(self.workdir)

    def run_and_check_exit_code(self, args=[], code=0, _not=False):
        if _not:
            self.assertFalse(run_and_check_exit_code(args, code))
        else:
            self.assertTrue(run_and_check_exit_code(args, code))

    def test_10_main__stringTemplate(self):
        tmpl = os.path.join(self.workdir, "test.tmpl")
        ctx = os.path.join(self.workdir, "ctx.yml")
        output = os.path.join(self.workdir, "output.txt")
        open(tmpl, 'w').write("$a\n")
        open(ctx, 'w').write("a: aaa\n")

        self.run_and_check_exit_code(["-E", "string.Template", "-C", ctx,
                                      "-o", output, tmpl])
        self.assertEquals(open(output).read(), "aaa\n")

    def test_20_main__jinja2(self):
        if find_by_name("jinja2"):
            tmpl = os.path.join(self.workdir, "test.j2")
            output = os.path.join(self.workdir, "output.txt")
            open(tmpl, 'w').write("{{ hello|default('hello') }}")

            self.run_and_check_exit_code(["-o", output, tmpl])
            self.assertEquals(open(output).read(), "hello")

# vim:sw=4:ts=4:et:
