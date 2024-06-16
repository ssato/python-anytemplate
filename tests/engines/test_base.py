#
# Copyright (C) 2015 - 2024 Satoru SATOH <ssato redhat.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
from __future__ import absolute_import

import anytemplate.engines.base as TT  # stands for test target


def test_class_methods():
    assert TT.Engine.name() == "base"
    assert TT.Engine.file_extensions() == []
    assert not TT.Engine.supports("foo.tmpl")


def test_instance_methods():
    engine = TT.Engine()
    assert isinstance(engine, TT.Engine)

    engine.renders_impl("aaa", {})  # Template string must be given.
    engine.render_impl(__file__, {})

    engine.renders("aaa")
    engine.render(__file__)

# vim:sw=4:ts=4:et:
