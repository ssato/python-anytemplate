#
# Copyright (C). 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring, invalid-name
from __future__ import absolute_import, with_statement

import os.path
import os
import unittest

import anytemplate.utils as TT
import tests.common


class Test00(unittest.TestCase):

    def test_02_uniq(self):
        self.assertEqual(TT.uniq([]), [])
        self.assertEqual(TT.uniq([1, 4, 5, 1, 2, 3, 5, 10, 13, 2]),
                         [1, 4, 5, 2, 3, 10, 13])

    def test_03_chaincalls(self):
        self.assertEqual(TT.chaincalls([lambda x: x + 1, lambda x: x - 1], 1),
                         1)

    def test_04_normpath(self):
        self.assertEqual(TT.normpath("/tmp/../etc/hosts"), "/etc/hosts")
        self.assertEqual(TT.normpath("~root/t"), "/root/t")

    def test_04_normpath__relative(self):
        curdir = os.curdir
        relpath = "./a/b/c.txt"

        self.assertEqual(TT.normpath(relpath),
                         TT.normpath(os.path.join(curdir, relpath)))

    def test_05_flip(self):
        self.assertEqual(TT.flip((1, 3)), (3, 1))

    def test_06_concat(self):
        self.assertEqual(TT.concat([]), [])
        self.assertEqual(TT.concat(()), [])
        self.assertEqual(TT.concat([[1, 2, 3], [4, 5]]), [1, 2, 3, 4, 5])
        self.assertEqual(TT.concat([[1, 2, 3], [4, 5, [6, 7]]]),
                         [1, 2, 3, 4, 5, [6, 7]])
        self.assertEqual(TT.concat(((1, 2, 3), (4, 5, [6, 7]))),
                         [1, 2, 3, 4, 5, [6, 7]])
        self.assertEqual(TT.concat((i, i * 2) for i in range(3)),
                         [0, 0, 1, 2, 2, 4])

    def test_40_parse_filespec__w_type(self):
        self.assertEqual(TT.parse_filespec("json:a.json"),
                         [("a.json", "json")])

    def test_41_parse_filespec__wo_type(self):
        self.assertEqual(TT.parse_filespec("a.json"), [("a.json", None)])

    def test_50_parse_and_load_contexts__invalid_input(self):
        self.assertTrue(isinstance(TT.parse_and_load_contexts(["/a/b/c.json"]),
                                   dict))

    def test_52_parse_and_load_contexts__werr(self):
        ret = TT.parse_and_load_contexts(["/root/c.json"])
        self.assertTrue(isinstance(ret, dict))

    def test_60_find_template_from_path__wo_paths(self):
        self.assertEqual(TT.find_template_from_path(__file__), __file__)

    def test_62_find_template_from_path__w_paths(self):
        fname = os.path.basename(__file__)
        fdir = os.path.dirname(__file__)

        self.assertEqual(TT.find_template_from_path(fname, [fdir]), __file__)

    def test_64_find_template_from_path__none(self):
        self.assertTrue(TT.find_template_from_path("not_existing") is None)

    def test_70_mk_template_paths(self):
        fname = __file__
        fdir = os.path.abspath(os.path.dirname(fname))

        self.assertEqual(TT.mk_template_paths(fname, []), [fdir])
        self.assertEqual(TT.mk_template_paths(fname, ["/etc"]), ["/etc", fdir])
        self.assertEqual(TT.mk_template_paths(None, ["/etc"]), ["/etc"])
        self.assertEqual(TT.mk_template_paths(None, None), [os.curdir])


class Test10(tests.common.TestsWithWorkdir):

    def test_40_parse_and_load_contexts(self):
        jsns = [os.path.join(self.workdir, "a.json"),
                os.path.join(self.workdir, "b.json"),
                os.path.join(self.workdir, "c.json")]
        open(jsns[0], 'w').write('{"a": "aaa"}\n')
        open(jsns[1], 'w').write('{"b": "bbb"}\n')
        open(jsns[2], 'w').write('{"c": "ccc"}\n')
        jsns[2] = "json:%s" % jsns[2]

        self.assertEqual(TT.parse_and_load_contexts(jsns),
                         dict(a="aaa", b="bbb", c="ccc"))

    def test_50_write_to_output__create_dir(self):
        output = os.path.join(self.workdir, "a", "out.txt")
        TT.write_to_output("hello", output)

        self.assertEqual(open(output).read(), "hello")

    def test_52_write_to_output__stdout(self):
        with tests.common.TempDir() as dir_:
            outpath = os.path.join(dir_, "test.out")
            TT.write_to_output("hello", output=outpath)
            self.assertTrue(os.path.exists(outpath))

            os.remove(outpath)

# vim:sw=4:ts=4:et:
