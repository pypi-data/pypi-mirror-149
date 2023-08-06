# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import numpy as np
from cegalprizm.pythontool import _utils
from cegalprizm.pythontool._system import _system
from .inprocesstestcase import InprocessTestCase


class UtilsTest(InprocessTestCase):

    # our API to test is
    # ensure_1d_float_array
    # ensure_1d_int_array
    # ensure_2d_float_array
    # ensure_2d_int_array
    # ensure_3d_float_array
    # ensure_3d_int_array

    # each should be called with
    #  - a flat list
    #  - a list-of-lists
    #  - a System.Array
    #  - a ndarray
    #  - a ndarray of type f32 (for float)

    def test_new_ensure_1d_float_array(self):

        def populate_1d_float_array(arr, dim_len):
            for i in range(dim_len):
                arr[i] = i + 0.1
            return arr

        dim_len = 3
        
        nd_array = populate_1d_float_array(np.empty(dim_len, dtype=np.float64), dim_len)
        nd32_array = populate_1d_float_array(np.empty(dim_len, dtype=np.float32), dim_len)

        f_net_array = populate_1d_float_array(_system().Array.CreateInstance(_system().Double, 3), dim_len)

        f_list = [float(x + 0.1) for x in range(0, dim_len)]
        f64_list = [np.float64(x + 0.1) for x in range(0, dim_len)]

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_1d_float_array(nd_array, dim_len)))
        np.testing.assert_array_almost_equal(nd_array, _utils.ensure_1d_float_array(nd32_array, dim_len)) # expect conversion difference from np.float32 to float -> almost_equal

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_1d_float_array(f_net_array, dim_len)))

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_1d_float_array(f_list, dim_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_1d_float_array(f64_list, dim_len)))

    def test_new_ensure_1d_int_array(self):

        def populate_1d_int_array(arr, dim_len):
            for i in range(dim_len):
                arr[i] = i
            return arr

        dim_len = 3
        i_list = [int(x) for x in range(0, dim_len)]
        i_net_array = populate_1d_int_array(_system().Array.CreateInstance(_system().Int32, 3), dim_len)
        i_nd_array = populate_1d_int_array(np.empty(dim_len, dtype=np.int), dim_len)

        self.assertTrue(np.array_equal(i_nd_array, _utils.ensure_1d_int_array(i_list, dim_len)))
        self.assertTrue(np.array_equal(i_nd_array, _utils.ensure_1d_int_array(i_net_array, dim_len)))
        self.assertTrue(np.array_equal(i_nd_array, _utils.ensure_1d_int_array(i_nd_array, dim_len)))

    def test_new_ensure_2d_float_array(self):

        def populate_array(arr, i_len, j_len):
            for i in range(0, i_len):
                for j in range(0, j_len):
                    arr[i, j] = i + 10 * j + 0.1
            return arr

        i_len = 2
        j_len = 3

        nd_array = populate_array(np.empty((i_len, j_len), dtype=np.float64), i_len, j_len)
        nd32_array = populate_array(np.empty((i_len, j_len), dtype=np.float32), i_len, j_len)

        f_net_array = populate_array(_system().Array.CreateInstance(_system().Double, i_len, j_len), i_len, j_len)

        flat_list = [0.1, 10.1, 20.1, 1.1, 11.1, 21.1]

        list_of_lists = [[0.1, 10.1, 20.1],
                         [1.1, 11.1, 21.1]]

        f64_flat_list = [np.float64(0.1), np.float64(10.1), np.float64(20.1), np.float64(1.1), np.float64(11.1), np.float64(21.1)]

        f64_list_of_lists = [[np.float64(0.1), np.float64(10.1), np.float64(20.1)],
                         [np.float64(1.1), np.float64(11.1), np.float64(21.1)]]

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_float_array(nd_array, i_len, j_len)))
        np.testing.assert_array_almost_equal(nd_array, _utils.ensure_2d_float_array(nd32_array, i_len, j_len)) # expect conversion difference from np.float32 to float -> almost_equal

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_float_array(f_net_array, i_len, j_len)))

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_float_array(flat_list, i_len, j_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_float_array(list_of_lists, i_len, j_len)))

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_float_array(f64_flat_list, i_len, j_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_float_array(f64_list_of_lists, i_len, j_len)))

    def test_new_ensure_2d_int_array(self):

        def populate_array(arr, i_len, j_len):
            for i in range(0, i_len):
                for j in range(0, j_len):
                    arr[i, j] = i + 10 * j
            return arr

        i_len = 2
        j_len = 3

        flat_list = [0, 10, 20, 1, 11, 21]
        list_of_lists = [[0, 10, 20],
                         [1, 11, 21]]

        net_array = populate_array(_system().Array.CreateInstance(_system().Int32, i_len, j_len), i_len, j_len)
        nd_array = populate_array(np.empty((i_len, j_len), dtype=np.int32), i_len, j_len)

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_int_array(flat_list, i_len, j_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_int_array(list_of_lists, i_len, j_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_int_array(net_array, i_len, j_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_2d_int_array(nd_array, i_len, j_len)))

    def test_new_ensure_3d_int_array(self):

        def populate_array(arr, i_len, j_len, k_len):
            for i in range(0, i_len):
                for j in range(0, j_len):
                    for k in range(0, k_len):
                        arr[i, j, k] = i + 10 * j + 100 * k
            return arr

        i_len = 2
        j_len = 3
        k_len = 4

        flat_list = [0, 100, 200, 300, 10, 110, 210, 310, 20, 120, 220, 320, 1, 101, 201, 301, 11, 111, 211, 311, 21, 121, 221, 321]
        list_of_lists = [[[0, 100, 200, 300],
                          [10, 110, 210, 310],
                          [20, 120, 220, 320]],

                         [[1, 101, 201, 301],
                          [11, 111, 211, 311],
                          [21, 121, 221, 321]]]

        net_array = populate_array(_system().Array.CreateInstance(_system().Int32, i_len, j_len, k_len), i_len, j_len, k_len)
        nd_array = populate_array(np.empty((i_len, j_len, k_len), dtype=np.int32), i_len, j_len, k_len)

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_int_array(flat_list, i_len, j_len, k_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_int_array(list_of_lists, i_len, j_len, k_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_int_array(net_array, i_len, j_len, k_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_int_array(nd_array, i_len, j_len, k_len)))

    def test_new_ensure_3d_float_array(self):

        def populate_array(arr, i_len, j_len, k_len):
            for i in range(0, i_len):
                for j in range(0, j_len):
                    for k in range(0, k_len):
                        arr[i, j, k] = i + 10 * j + 100 * k + 0.1
            return arr

        i_len = 2
        j_len = 3
        k_len = 4

        nd_array = populate_array(np.empty((i_len, j_len, k_len), dtype=np.float64), i_len, j_len, k_len)
        nd32_array = populate_array(np.empty((i_len, j_len, k_len), dtype=np.float32), i_len, j_len, k_len)

        net_array = populate_array(_system().Array.CreateInstance(_system().Double, i_len, j_len, k_len), i_len, j_len, k_len)

        flat_list = [0.1, 100.1, 200.1, 300.1, 10.1, 110.1, 210.1, 310.1, 20.1, 120.1, 220.1, 320.1, 1.1, 101.1, 201.1, 301.1, 11.1, 111.1, 211.1, 311.1, 21.1, 121.1, 221.1, 321.1]
        list_of_lists = [[[0.1, 100.1, 200.1, 300.1],
                          [10.1, 110.1, 210.1, 310.1],
                          [20.1, 120.1, 220.1, 320.1]],

                         [[1.1, 101.1, 201.1, 301.1],
                          [11.1, 111.1, 211.1, 311.1],
                          [21.1, 121.1, 221.1, 321.1]]]

        f64_flat_list = [np.float64(0.1), np.float64(100.1), np.float64(200.1), np.float64(300.1), \
                         np.float64(10.1), np.float64(110.1), np.float64(210.1), np.float64(310.1), \
                         np.float64(20.1), np.float64(120.1), np.float64(220.1), np.float64(320.1), \
                         np.float64(1.1), np.float64(101.1), np.float64(201.1), np.float64(301.1), \
                         np.float64(11.1), np.float64(111.1), np.float64(211.1), np.float64(311.1), \
                         np.float64(21.1), np.float64(121.1), np.float64(221.1), np.float64(321.1)]

        f64_list_of_lists = [[[np.float64(0.1), np.float64(100.1), np.float64(200.1), np.float64(300.1)],
                          [np.float64(10.1), np.float64(110.1), np.float64(210.1), np.float64(310.1)],
                          [np.float64(20.1), np.float64(120.1), np.float64(220.1), np.float64(320.1)]],

                         [[np.float64(1.1), np.float64(101.1), np.float64(201.1), np.float64(301.1)],
                          [np.float64(11.1), np.float64(111.1), np.float64(211.1), np.float64(311.1)],
                          [np.float64(21.1), np.float64(121.1), np.float64(221.1), np.float64(321.1)]]]

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_float_array(nd_array, i_len, j_len, k_len)))
        np.testing.assert_array_almost_equal(nd_array, _utils.ensure_3d_float_array(nd32_array, i_len, j_len, k_len), 5) # expect conversion difference from np.float32 to float -> almost_equal

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_float_array(net_array, i_len, j_len, k_len)))

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_float_array(flat_list, i_len, j_len, k_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_float_array(list_of_lists, i_len, j_len, k_len)))

        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_float_array(f64_flat_list, i_len, j_len, k_len)))
        self.assertTrue(np.array_equal(nd_array, _utils.ensure_3d_float_array(f64_list_of_lists, i_len, j_len, k_len)))

    def test_str_or_none(self):
        self.assertEqual(None, _utils.str_or_none(None))
        self.assertEqual(None, _utils.str_or_none(" "))
        self.assertEqual(" m ", _utils.str_or_none(" m "))

    def test_to_python_datetime(self):
        system_datetime = _system().DateTime
        netdt = system_datetime(2017, 7, 20, 13, 12, 42) # 13:12:42 on the 20th July 2017
        pydt = _utils.to_python_datetime(netdt)
        self.assertEqual(2017, pydt.year)
        self.assertEqual(7, pydt.month)
        self.assertEqual(20, pydt.day)
        self.assertEqual(13, pydt.hour)
        self.assertEqual(12, pydt.minute)
        self.assertEqual(42, pydt.second)

    def test_to_backing_arraytype_float_3dim(self):
        n = np.ndarray((3, 3, 3), dtype=np.float64)
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    val = i + 10 * j + 100 * k
                    n[i, j, k] = val

        s = _utils.to_backing_arraytype(n)
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    val = i + 10 * j + 100 * k
                    self.assertEqual(val, s[i, j, k])

    def test_to_backing_arraytype_int_3dim(self):
        n = np.ndarray((3, 3, 3), dtype=np.int32)
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    val = i + 10 * j + 100 * k
                    n[i, j, k] = val

        s = _utils.to_backing_arraytype(n)
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    val = i + 10 * j + 100 * k
                    self.assertEqual(val, s[i, j, k])

    def test_to_backing_arraytype_float_2dim(self):
        n = np.ndarray((3, 3), dtype=np.float64)
        for i in range(0, 3):
            for j in range(0, 3):
                val = i + 10 * j
                n[i, j] = val

        s = _utils.to_backing_arraytype(n)
        for i in range(0, 3):
            for j in range(0, 3):
                val = i + 10 * j
                self.assertEqual(val, s[i, j])

    def test_to_backing_arraytype_int_2dim(self):
        n = np.ndarray((3, 3), dtype=np.int32)
        for i in range(0, 3):
            for j in range(0, 3):
                val = i + 10 * j
                n[i, j] = val

        s = _utils.to_backing_arraytype(n)
        for i in range(0, 3):
            for j in range(0, 3):
                val = i + 10 * j
                self.assertEqual(val, s[i, j])

    def test_to_backing_arraytype_float_1dim(self):
        n = np.ndarray((3,), dtype=np.float64)
        for i in range(0, 3):
            val = i
            n[i] = val

        s = _utils.to_backing_arraytype(n)
        for i in range(0, 3):
            val = i
            self.assertEqual(val, s[i])

    def test_to_backing_arraytype_int_1dim(self):
        n = np.ndarray((3,), dtype=np.int32)
        for i in range(0, 3):
            val = i
            n[i] = val

        s = _utils.to_backing_arraytype(n)
        for i in range(0, 3):
            val = i
            self.assertEqual(val, s[i])
