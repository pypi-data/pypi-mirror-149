# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import cegalprizm.pythontool
import cegalprizm.pythontool.test.mocked.mocks as mocks
import unittest
from .inprocesstestcase import InprocessTestCase
import sys

class PointSetTest(InprocessTestCase):
    def test_mock_exists(self):
        ps = self.bridge.pointsets['MyMockPointSets']
        self.assertIsNotNone(ps)

    def test_mock_petrel_like(self):
        var = self.bridge.pointsets['MyMockPointSets']
        def is_almost(val, target):
            return True if abs(val-target) < 0.001 else False
        ok = True

        if sys.version_info.major > 2:
            df = var.as_dataframe()
            old_value1 = df['Twt'][0]
            old_value2 = df['Vp'][0]
            df['Twt'][0] = 14.37
            df['Vp'][0] = 15.37
            var.set_values(df)

            if not is_almost(df['Twt'][0], 14.37):
                ok = False
                print("not is_almost(df['Twt'][0], 14.37)\n")
                print(df['Twt'][0])

            if not is_almost(df['Vp'][0], 15.37):
                ok = False
                print("not is_almost(df['Vp'][0], 15.37)\n")
                print(df['Vp'][0])

            with var.values() as df:
                df['Twt'][0] = 1.24
                df['Vp'][0] = 3.45

            if not is_almost(df['Twt'][0], 1.24):
                ok = False
                print("not is_almost(df['Twt'][0], 1.24)\n")
                print(df['Twt'][0])

            if not is_almost(df['Vp'][0], 3.45):
                ok = False
                print("not is_almost(df['Vp'][0], 3.45)\n")
                print(df['Vp'][0])

            with var.values() as df:
                df['Twt'][0] = old_value1
                df['Vp'][0] = old_value2
        self.assertTrue(ok)


