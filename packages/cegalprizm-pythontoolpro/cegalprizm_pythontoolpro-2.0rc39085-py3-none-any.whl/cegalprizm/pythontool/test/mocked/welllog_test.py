# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import datetime
import math
from cegalprizm.pythontool import GlobalWellLog, DiscreteGlobalWellLog
from cegalprizm.pythontool._system import _system
from .inprocesstestcase import InprocessTestCase


class WellLogTest(InprocessTestCase):
    def assertSequencesAlmostEqual(self, a, b):
        z = zip(a, b)
        for (x, y) in z:
            self.assertAlmostEqual(x, y)

    def test_borehole(self):
        b = self._log.well
        self.assertIsNotNone(b)

    def test_global_well_log(self):
        gwl = self._log.global_well_log
        self.assertIsNotNone(gwl)
        self.assertIsInstance(gwl, GlobalWellLog)

    def test_global_well_log_petrel_name(self):
        gwl = self._log.global_well_log
        self.assertEqual("MyLog", gwl.petrel_name)

    def test_discrete_global_well_log_petrel_name(self):
        gwl = self.bridge.discrete_well_logs["facies"].global_well_log
        self.assertEqual("facies", gwl.petrel_name)

    def test_dictionary_global_well_log(self):
        facies = self.bridge.discrete_well_logs["facies"]
        self.assertIsInstance(facies.global_well_log, DiscreteGlobalWellLog)

    def setUp(self):
        super().setUp()
        self._log = self.bridge.well_logs["MyLog"]

    def test_log_sample_str(self):
        gamma = self.bridge.well_logs["gamma"]
        self.assertEqual(
            "LogSample(md=0.00, position=Point(x=0.00, y=0.00, z=0.00), TWT=0.00, TVD=0.00, value=0.10)",
            str(gamma.samples[0]),
        )

    def test_log_sample_missing_str(self):
        gamma = self.bridge.well_logs["gamma_missing"]
        self.assertEqual(
            "LogSample(md=0.00, position=Point(x=0.00, y=0.00, z=0.00), TWT=0.00, TVD=0.00, value=None)",
            str(gamma.samples[0]),
        )

    def test_discrete_log_samples_set_values(self):
        facies = self.bridge.discrete_well_logs["facies"]
        mds = [s.md for s in facies.samples]
        original_values = [s.value for s in facies.samples]
        self.assertEqual(original_values, [1, 2])
        facies.set_values(mds, [3, 4])
        self.assertEqual([s.value for s in facies.samples], [3, 4])
        facies.set_values(mds, original_values)

    def test_log_samples_set_values(self):
        gamma = self.bridge.well_logs["gamma"]
        mds = [s.md for s in gamma.samples]
        original_values = [s.value for s in gamma.samples]
        self.assertEqual(original_values, [0.1, 0.9])
        gamma.set_values(mds, [0.2, 0.8])
        self.assertSequencesAlmostEqual([s.value for s in gamma.samples], [0.2, 0.8])
        gamma.set_values(mds, original_values)

    def test_missing_value(self):
        gamma = self.bridge.well_logs["gamma"]
        self.assertTrue(math.isnan(gamma.missing_value))

    def test_discrete_missing_value(self):
        facies = self.bridge.discrete_well_logs["facies"]
        self.assertEqual(facies.missing_value, _system().Int32.MaxValue)

    def test_discrete_log_set_values_with_missing(self):
        facies = self.bridge.discrete_well_logs["facies"]
        mds = [s.md for s in facies.samples]
        original_values = [s.value for s in facies.samples]
        new_values = [1, None]
        facies.set_values(mds, new_values)
        self.assertEqual(facies.samples[0].value, 1)
        self.assertEqual(facies.samples[1].value, None)
        facies.set_values(mds, original_values)

    def test_log_set_values_with_missing(self):
        gamma = self.bridge.well_logs["gamma"]
        mds = [s.md for s in gamma.samples]
        original_values = [s.value for s in gamma.samples]
        new_values = [0.1, None]
        gamma.set_values(mds, new_values)
        self.assertAlmostEqual(gamma.samples[0].value, 0.1)
        self.assertAlmostEqual(gamma.samples[1].value, None)
        gamma.set_values(mds, original_values)
