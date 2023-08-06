# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .inprocesstestcase import InprocessTestCase


class GridTest(InprocessTestCase):
    def test_vertices(self):
        grid = self.bridge.grids['FourGrid']
        self.assertTrue(grid is not None)

        vs = grid.vertices(1, 1, 1)

    def test_prop_columns(self):
        prop = self.bridge.grid_properties['ThreeProp']
        self.assertEqual(9, len([col for col in prop.columns()]))
