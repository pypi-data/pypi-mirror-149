# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import cegalprizm.pythontool.gridproperty as gridproperty
import cegalprizm.pythontool.exceptions as exceptions
from .inprocesstestcase import InprocessTestCase

class PetrelLinkTest(InprocessTestCase):
    def test_property(self):
        prop = self.bridge.grid_properties['MyProp']
        self.assertEqual('MockProperty', prop.petrel_name)
        self.assertEqual(prop.grid.extent.i, 10)
        self.assertEqual(prop.grid.extent.j, 10)
        self.assertEqual(prop.grid.extent.k, 10)

    def test_properties_getitem(self):
        self.assertEqual(10, self.bridge.grid_properties["MyProp"].grid.extent.i)
        self.assertEqual(3, self.bridge.grid_properties["ThreeProp"].grid.extent.i)

    def test_properties_setitem(self):
        with self.assertRaises(exceptions.PythonToolException):
            self.bridge.grid_properties["new"] = "nope!"

    def test_propeties_len(self):
        self.assertEqual(3, len(self.bridge.grid_properties))

    def test_properties_iter(self):
        props = [prop for prop in self.bridge.grid_properties]
        for p in props:
            self.assertTrue(isinstance(p, gridproperty.GridProperty))

    def test_properties_items(self):
        for (k, v) in self.bridge.grid_properties.items():
            self.assertTrue(isinstance(k, str))
            self.assertTrue(isinstance(v, gridproperty.GridProperty))

    def test_grids_getitem(self):
        self.assertEqual(4, self.bridge.grids["FourGrid"].extent.i)
        self.assertEqual(5, self.bridge.grids["FiveGrid"].extent.i)

    def test_seismics_getitem(self):
        self.assertEqual(10, self.bridge.seismic_cubes["TenSeismic"].extent.i)
        self.assertEqual(12, self.bridge.seismic_cubes["TwelveSeismic"].extent.i)

    def test_decorated_welllogversion(self):
        global_well_log = self.bridge.global_well_logs['gamma']

    def test_all_boreholes(self):
        bs = list(self.bridge.wells)
        self.assertEqual(2, len(bs))

