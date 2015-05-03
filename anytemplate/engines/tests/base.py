#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
import unittest
import anytemplate.engines.base as TT  # stands for test target


class Test_00(unittest.TestCase):

    def test_10__class_methods(self):
        self.assertEquals(TT.BaseEngine.name(), "base")
        self.assertEquals(TT.BaseEngine.file_extensions(), [])
        self.assertFalse(TT.BaseEngine.supports())

    def test_20__instance_methods(self):
        engine = TT.BaseEngine()
        try:
            engine.renders_impl("aaa")  # Template string must be given.
            engine.render_impl(__file__)

            engine.renders("aaa")
            engine.render(__file__)
        except NotImplementedError:
            pass

# vim:sw=4:ts=4:et:
