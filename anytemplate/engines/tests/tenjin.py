#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import os
import unittest

import anytemplate.tests.common
try:
    import anytemplate.engines.tenjin as TT
except ImportError:
    TT = None


class Test00(unittest.TestCase):

    def test_10_render(self):
        if TT is not None:
            tmpl_c = "${a} {=b=}"
            egn = TT.Engine()
            self.assertEquals(egn.renders(tmpl_c), tmpl_c)


class Test10(unittest.TestCase):

    def setUp(self):
        self.workdir = anytemplate.tests.common.setup_workdir()

    def tearDown(self):
        anytemplate.tests.common.cleanup_workdir(self.workdir)

    def test_10_render(self):
        tmpl = "a.t"
        tmpl_c = ("${a} {=b=}\n"
                  "<?py for c in cs: ?>\n"
                  "#{c}\n"
                  "<?py #endfor ?>")
        exp = "aaa bbb\nc\nd\n"

        open(os.path.join(self.workdir, tmpl), 'w').write(tmpl_c)

        if TT is not None:
            egn = TT.Engine()
            res = egn.render(tmpl, dict(a="aaa", b="bbb", cs=["c", "d"]),
                             at_paths=[self.workdir, os.curdir])
            self.assertEquals(res, exp,
                              anytemplate.tests.common.diff(res, exp))

# vim:sw=4:ts=4:et:
