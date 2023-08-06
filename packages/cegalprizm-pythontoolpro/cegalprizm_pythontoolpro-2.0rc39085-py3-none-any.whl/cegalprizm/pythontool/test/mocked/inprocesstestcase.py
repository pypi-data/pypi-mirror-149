# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import unittest
from cegalprizm.pythontool._toolmode import _ToolMode
import cegalprizm.pythontool
import cegalprizm.pythontool.test.mocked.mocks as mocks

class InprocessTestCase(unittest.TestCase):
    def setUp(self) -> None:
        _ToolMode._is_oop = False
        self.bridge = cegalprizm.pythontool.PetrelLink(mocks.MockObjectFactory())
        return super().setUp()

    def tearDown(self) -> None:
        _ToolMode._is_oop = None
        return super().tearDown()