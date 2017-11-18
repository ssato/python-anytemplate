#
# Copyright (C) 2015 Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
import unittest
import anytemplate.engines.base as TT  # stands for test target


class Test(unittest.TestCase):

    def test_10_class_methods(self):
        self.assertEqual(TT.Engine.name(), "base")
        self.assertEqual(TT.Engine.file_extensions(), [])
        self.assertFalse(TT.Engine.supports("foo.tmpl"))

    def test_20_instance_methods(self):
        engine = TT.Engine()
        self.assertTrue(isinstance(engine, TT.Engine))
        engine.renders_impl("aaa", {})  # Template string must be given.
        engine.render_impl(__file__, {})

        engine.renders("aaa")
        engine.render(__file__)

# vim:sw=4:ts=4:et:
