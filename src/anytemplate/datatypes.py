#
# Copyright (C) 2024 Satoru SATOH <satoru.satoh gmail.com>
# License: MIT
#
"""Data types used internally.

The module imports this should have the line like as follows.

.. code-block:: pytohn

   import typing

   if typing.TYPE_CHECKING:
       from .datatypes import (
           PathType, MaybePath, MaybeCtx
       )
"""
from __future__ import annotations

import typing


PathType = str  # It will be typing.Union[str, pathlib.Path].
MaybePath = typing.Optional[PathType]
MaybeCtx = typing.Optional[dict]
