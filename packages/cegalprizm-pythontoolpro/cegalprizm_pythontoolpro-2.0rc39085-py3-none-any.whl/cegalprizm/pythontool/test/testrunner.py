# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import unittest
from cegalprizm.pythontool.test.mocked.petrellink_test import PetrelLinkTest
from cegalprizm.pythontool.test.mocked.slice_test import SliceTest
from cegalprizm.pythontool.test.mocked.utils_test import UtilsTest
from cegalprizm.pythontool.test.mocked.grid_test import GridTest
from cegalprizm.pythontool.test.mocked.polylineset_test import PolylineSetTest
from cegalprizm.pythontool.test.mocked.prop_test import PropTest
from cegalprizm.pythontool.test.mocked.welllog_test import WellLogTest
from cegalprizm.pythontool.test.mocked.well_test import GlobalWellLogTest, BoreholeTest,  DiscreteWellLogTest
from cegalprizm.pythontool.test.mocked.seismic_test import SeismicTest
from cegalprizm.pythontool.test.mocked.pointset_test import PointSetTest
from cegalprizm.pythontool.test.mocked.horizoninterpretation_test import HorizonInterpretationTest


suite = unittest.TestSuite()
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(PetrelLinkTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(SliceTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(UtilsTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(GridTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(PropTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(PolylineSetTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(WellLogTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(DiscreteWellLogTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(GlobalWellLogTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(BoreholeTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(SeismicTest))
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(PointSetTest))              
suite.addTest(unittest.TestLoader().
              loadTestsFromTestCase(HorizonInterpretationTest))

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite)
