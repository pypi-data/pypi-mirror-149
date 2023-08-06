# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import cegalprizm.pythontool.test.mocked.mocks as mocks
import cegalprizm.pythontool.primitives as primitives
import cegalprizm.pythontool.polylines as polylines
from .inprocesstestcase import InprocessTestCase

class PolylineSetTest(InprocessTestCase):
    def test_count(self):
        polys = self.bridge.polylinesets['MyPolylineSet']
        self.assertEqual(5, len(polys))

    def test_add(self):
        polys = polylines.PolylineSet(mocks.MockPolylineSetObject(5))
        polys.add_line([primitives.Point(11,11,11), primitives.Point(11,11,11), primitives.Point(11,11,11)])
        self.assertEqual(6, len(polys))
        self.assertTrue(all(pt.x == 11 and pt.y == 11 and pt.z == 11 for pt in polys[5]))

    def test_get(self):
        # the mock has lines with the xyzs just the index of the lines
        polys = polylines.PolylineSet(mocks.MockPolylineSetObject(5))
        for idx, line in enumerate(polys):
            self.assertTrue(len(line) > 0)
            self.assertTrue(all(pt.x == idx for pt in line))
            self.assertTrue(all(pt.y == idx for pt in line))
            self.assertTrue(all(pt.z == idx for pt in line))

    def test_delete_last(self):
        polys = polylines.PolylineSet(mocks.MockPolylineSetObject(5))
        line = polys[4]
        polys.delete_line(line)
        self.assertEqual(len(polys), 4)
        for idx, line in enumerate(polys):
            self.assertTrue(len(line) > 0)
            self.assertTrue(all(pt.x == idx for pt in line))
            self.assertTrue(all(pt.y == idx for pt in line))
            self.assertTrue(all(pt.z == idx for pt in line))

    def test_delete_first(self):
        polys = polylines.PolylineSet(mocks.MockPolylineSetObject(5))
        line = polys[0]
        polys.delete_line(line)
        self.assertEqual(len(polys), 4)

        for idx, line in enumerate(polys):
            self.assertTrue(len(line) > 0)
            self.assertTrue(all(pt.x == idx + 1 for pt in line))
            self.assertTrue(all(pt.y == idx + 1 for pt in line))
            self.assertTrue(all(pt.z == idx + 1 for pt in line))

    def test_delete_first_twice(self):
        polys = polylines.PolylineSet(mocks.MockPolylineSetObject(5))
        line = polys[0]
        polys.delete_line(polys[0])
        self.assertEqual(len(polys), 4)
        polys.delete_line(polys[0])
        self.assertEqual(len(polys), 3)

        for idx, line in enumerate(polys):
            self.assertTrue(len(line) > 0)
            self.assertTrue(all(pt.x == idx + 2 for pt in line))
            self.assertTrue(all(pt.y == idx + 2 for pt in line))
            self.assertTrue(all(pt.z == idx + 2 for pt in line))

    def test_delete_all(self):
        polys = polylines.PolylineSet(mocks.MockPolylineSetObject(5))
        polys.clear()
        self.assertEqual(len(polys), 0)
