# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool._toolmode import _ToolMode
_ToolMode._is_oop = False
from  cegalprizm.pythontool import _utils
from .inprocesstestcase import InprocessTestCase

class PropTest(InprocessTestCase):
    def test_prop_columns(self):
        prop = self.bridge.grid_properties['ThreeProp']
        self.assertEqual(9, len([col for col in prop.columns()]))

        for col in prop.columns():
            for v in col.as_array():
                self.assertEqual(col.i, v % 10)
                self.assertEqual(col.j, (v % 100) // 10)

        self.assertEqual(3, len([col for col in prop.columns(irange=[1], jrange=None)]))

        self.assertEqual(4, len([col for col in prop.columns(irange=[1, 2], jrange=[0, 1])]))

    def test_prop_layers(self):
        prop = self.bridge.grid_properties['ThreeProp']
        self.assertEqual(3, len([layer for layer in prop.layers()]))

        for layer in prop.layers():
            for v in _utils.iterable_values(layer.as_array()):
                self.assertEqual(layer.k, v // 100)

    def test_all(self):
        prop = self.bridge.grid_properties['ThreeProp']
        all_slice = prop.all()
        self.assertEqual(27, len([v for v in _utils.iterable_values(all_slice.as_array())]))
