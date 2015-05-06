#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
#
import os
import unittest

import anytemplate.tests.common
try:
    import anytemplate.engines.tenjin as TT
except ImportError:
    TT = None


class Test_10(unittest.TestCase):

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
            r = egn.render(tmpl, dict(a="aaa", b="bbb", cs=["c", "d"]),
                           at_paths=[self.workdir, os.curdir])
            self.assertEquals(r, exp,
                              anytemplate.tests.common.diff(r, exp))

# vim:sw=4:ts=4:et:
