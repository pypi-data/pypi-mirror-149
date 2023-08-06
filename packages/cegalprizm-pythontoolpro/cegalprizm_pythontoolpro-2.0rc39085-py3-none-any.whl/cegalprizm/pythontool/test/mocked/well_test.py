# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import cegalprizm.pythontool
import unittest
from cegalprizm.pythontool import WellLog, DiscreteWellLog
from cegalprizm.pythontool import _utils
from .inprocesstestcase import InprocessTestCase


class WellLogTest(InprocessTestCase):
    def test_mock_exists(self):
        wl = self.bridge.well_logs['gamma']
        self.assertIsNotNone(wl)

    def test_mock_borehole(self):
        bh = self.bridge.well_logs['gamma'].well
        self.assertIsNotNone(bh)
        self.assertEqual('borehole1', bh.petrel_name)

    @unittest.skipUnless(_utils.python_env() == _utils.CPY3, "Can only run on CPython")
    def test_dataframe(self):
        wl = self.bridge.well_logs['gamma']
        df = wl.as_dataframe()
        self.assertIsNotNone(df)

        
class DiscreteWellLogTest(InprocessTestCase):
    @unittest.skipUnless(_utils.python_env() == _utils.CPY3, "Can only run on CPython")
    def test_as_dataframe(self):
        wl = self.bridge.discrete_well_logs['facies']
        df = wl.as_dataframe()
        self.assertIsNotNone(df)

    @unittest.skipUnless(_utils.python_env() == _utils.CPY3, "Can only run on CPython")
    def test_as_dataframe_missing_value(self):
        wl = self.bridge.discrete_well_logs['facies_missing']
        df = wl.as_dataframe()
        self.assertIsNotNone(df)


class GlobalWellLogTest(InprocessTestCase):
    def test_x(self):
        self.assertEqual(2, 1 + 1)

    def test_mock_exists(self):
        gwl = self.bridge.global_well_logs['gamma']
        self.assertIsNotNone(gwl)

    def test_can_get_log(self):
        gwl = self.bridge.global_well_logs['gamma']
        borehole_name = 'borehole1'
        wl = gwl.log(borehole_name)
        self.assertIsInstance(wl, cegalprizm.pythontool.WellLog)
        self.assertEqual(wl.well.petrel_name, 'borehole1')
        # so we need to have a mock well log 'gamma' with a mock borehole borehole1

    def test_can_get_logs_with_different_boreholes(self):
        gwl = self.bridge.global_well_logs['gamma']
        self.assertEqual(2, len(gwl.logs))
        self.assertEqual('borehole1', gwl.logs['borehole1'].well.petrel_name)
        self.assertEqual('borehole2', gwl.logs['borehole2'].well.petrel_name)

    def test_can_get_logs_with_different_boreholes_discrete(self):
        gwl = self.bridge.discrete_global_well_logs['facies']
        self.assertEqual(2, len(gwl.logs))
        self.assertEqual('borehole1', gwl.logs['borehole1'].well.petrel_name)
        self.assertEqual('borehole2', gwl.logs['borehole2'].well.petrel_name)


class BoreholeTest(InprocessTestCase):
    @unittest.skipUnless(_utils.python_env() == _utils.CPY3, "Can only run on CPython")
    def test_logs_dataframe_takes_list(self):
        gwl = self.bridge.global_well_logs['gamma']
        bh = self.bridge.wells['borehole1']

        df = bh.logs_dataframe([gwl])
        self.assertEqual(len(df), 2) # 2 samples
        self.assertEqual(df.columns[0], 'gamma')
        self.assertEqual(df.columns[1], 'MD')
        self.assertEqual(df.columns[2], 'TWT')
        self.assertEqual(df.columns[3], 'TVD')

    @unittest.skipUnless(_utils.python_env() == _utils.CPY3, "Can only run on CPython")
    def test_logs_dataframe_takes_single(self):
        gwl = self.bridge.global_well_logs['gamma']
        bh = self.bridge.wells['borehole1']

        df = bh.logs_dataframe(gwl)
        self.assertEqual(len(df), 2) # 2 samples
        self.assertEqual(df.columns[0], 'gamma')
        self.assertEqual(df.columns[1], 'MD')
        self.assertEqual(df.columns[2], 'TWT')
        self.assertEqual(df.columns[3], 'TVD')

    @unittest.skipUnless(_utils.python_env() == _utils.CPY3, "Can only run on CPython")
    def test_logs_dataframe_takes_list_of_logs(self):
        wl = self.bridge.well_logs['gamma']
        bh = self.bridge.wells['borehole1']

        df = bh.logs_dataframe([wl])
        self.assertEqual(len(df), 2) # 2 samples
        self.assertEqual(df.columns[0], 'gamma')
        self.assertEqual(df.columns[1], 'MD')
        self.assertEqual(df.columns[2], 'TWT')
        self.assertEqual(df.columns[3], 'TVD')

    @unittest.skipUnless(_utils.python_env() == _utils.CPY3, "Can only run on CPython")
    def test_logs_dataframe_takes_single_log(self):
        wl = self.bridge.well_logs['gamma']
        bh = self.bridge.wells['borehole1']

        df = bh.logs_dataframe(wl)
        self.assertEqual(len(df), 2) # 2 samples
        self.assertEqual(df.columns[0], 'gamma')
        self.assertEqual(df.columns[1], 'MD')
        self.assertEqual(df.columns[2], 'TWT')
        self.assertEqual(df.columns[3], 'TVD')

    def test_logs(self):
        bh = self.bridge.wells['borehole2']
        logs = bh.logs
        self.assertEqual(5, len(logs))

    def test_logs_getter(self):
        bh = self.bridge.wells['borehole2']
        log = bh.logs['log2']
        self.assertTrue(isinstance(log, WellLog))
        self.assertEqual('log2', log.petrel_name)

    def test_logs_getter_fail(self):
        bh = self.bridge.wells['borehole2']
        with self.assertRaises(KeyError):
            bh.logs['doesnotexist']

    def test_types_of_logs(self):
        bh = self.bridge.wells['borehole2']
        log1 = bh.logs['log1']
        self.assertTrue(isinstance(log1, WellLog))
        dloga = bh.logs['dloga']
        self.assertTrue(isinstance(dloga, DiscreteWellLog))
