# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .inprocesstestcase import InprocessTestCase

class HorizonInterpretationTest(InprocessTestCase):
    def test_horizoninterpretation3d(self):
        hi3d = self.bridge.horizon_interpretation_3ds['hi3d']
        self.assertTrue(hi3d is not None)
        self.assertTrue(hi3d.sample_count == 9)
        self.assertTrue(str(hi3d) == "HorizonInterpretation3D(petrel_name=\"hi3d\")")
        self.assertTrue(hi3d.indices(0.0, 1.0).i == 0)
        self.assertTrue(hi3d.position(0, 1).x == 0.1)

    def test_horizonproperty3d(self):
        hi3d = self.bridge.horizon_interpretation_3ds['hi3d']
        hp3d = hi3d.horizon_property_3ds[0]
        self.assertTrue(hp3d is not None)
        self.assertTrue(str(hp3d) == "HorizonProperty3D(petrel_name=\"TWT\")")
        self.assertTrue(hp3d.indices(0.0, 1.0).i == 0)
        self.assertTrue(hp3d.position(0, 1).x == 0.1)
