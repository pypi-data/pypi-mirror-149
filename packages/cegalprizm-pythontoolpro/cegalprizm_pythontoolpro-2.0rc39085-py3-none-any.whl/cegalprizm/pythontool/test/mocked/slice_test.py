# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import unittest
from cegalprizm.pythontool import _utils
from .inprocesstestcase import InprocessTestCase

def value_correct(i, j, k, val):
    return (i + 10 * j + 100 * k) == val


def all_monotonic_pairs_incl(min, max):
    return [(a, b) for a in range(min, max + 1) for b in range(min, max + 1) if b >= a]


class SliceTest(InprocessTestCase):

    def test_all_monotonic_pairs(self):
        pairs = all_monotonic_pairs_incl(0, 0)
        self.assertSequenceEqual(pairs, [(0, 0)])

        pairs = all_monotonic_pairs_incl(0, 1)
        self.assertSequenceEqual(pairs, [(0, 0), (0, 1), (1, 1)])

        pairs = all_monotonic_pairs_incl(1, 3)
        self.assertSequenceEqual(
            pairs, [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
        )

    def assertEqual(self, seqA, seqB):
        try:
            import numpy as np

            if isinstance(seqA, np.ndarray):
                seqA = list(seqA.flat)
                return self.assertEqual(seqA, seqB)
            if isinstance(seqB, np.ndarray):
                seqB = list(seqB.flat)
                return self.assertEqual(seqA, seqB)
        except ImportError:
            pass

        return super(SliceTest, self).assertEqual(seqA, seqB)

    def assertSequenceEqual(self, seqA, seqB):
        try:
            import numpy as np

            if isinstance(seqA, np.ndarray):
                seqA = list(seqA.flat)
                return self.assertSequenceEqual(seqA, seqB)
            if isinstance(seqB, np.ndarray):
                seqB = list(seqB.flat)
                return self.assertSequenceEqual(seqA, seqB)
        except ImportError:
            pass
        return super(SliceTest, self).assertSequenceEqual(seqA, seqB)

    def assertSequenceAlmostEqual(self, seqA, seqB):
        try:
            import numpy as np

            if isinstance(seqA, np.ndarray):
                seqA = list(seqA.flat)
                return self.assertSequenceAlmostEqual(seqA, seqB)
            if isinstance(seqB, np.ndarray):
                seqB = list(seqB.flat)
                return self.assertSequenceAlmostEqual(seqA, seqB)
        except ImportError:
            pass

        for (i, (a, b)) in enumerate(zip(seqA, seqB)):
            try:
                self.assertAlmostEqual(a, b)
            except AssertionError:
                text = "First differing element \
                {0}:\n{1}\n{2}\n\n- {3}\n+ {4}".format(
                    i, a, b, repr(seqA), repr(seqB)
                )
                raise AssertionError(text)

    def test_slice_values(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        self.assertEqual(prop.grid.extent.i, 3)
        #   self.assertEqual(27 ,len(prop.slice().values))
        self.assertEqual(
            3, len(_utils.iterable_values(prop.column(i=1, j=2).as_array()))
        )
        self.assertEqual(9, len(_utils.iterable_values(prop.layer(k=1).as_array())))

    def test_slice_enumerate(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        self.assert_chunk_consistent(prop.column(i=1, j=2))
        self.assert_chunk_consistent(prop.layer(k=2))

    def assert_chunk_consistent(self, chunk):
        for (i, j, k, v) in chunk.enumerate():
            self.assertTrue(value_correct(i, j, k, v))

    def test_chunk_enumerate(self):
        # test all possible 3d chunks
        prop = self.bridge.grid_properties["ThreeProp"]

        # genereate all possible 3d chunks for the property.
        # (this can get very slow very quickly)
        iranges = all_monotonic_pairs_incl(0, prop.grid.extent.i - 1)
        jranges = all_monotonic_pairs_incl(0, prop.grid.extent.j - 1)
        kranges = all_monotonic_pairs_incl(0, prop.grid.extent.k - 1)

        for ir in iranges:
            for jr in jranges:
                for kr in kranges:
                    chunk = prop.chunk(ir, jr, kr)
                    self.assert_chunk_consistent(chunk)

    @unittest.skipUnless(_utils.python_env() == _utils.CPY3, "Can only run on CPython")
    def test_dataframe_time(self):
        prop = self.bridge.grid_properties["LargeProp"]

        chunk = prop.chunk(
            (0, prop.grid.extent.i - 1),
            (0, prop.grid.extent.j - 1),
            (0, prop.grid.extent.k - 1),
        )

        import timeit

        print(
            "Time to dataframe", timeit.timeit(lambda: chunk.as_dataframe(), number=10)
        )
        print()

    def test_enumerate_time(self):
        prop = self.bridge.grid_properties["LargeProp"]

        chunk = prop.chunk(
            (0, prop.grid.extent.i - 1),
            (0, prop.grid.extent.j - 1),
            (0, prop.grid.extent.k - 1),
        )

        import timeit


    def test_slice_set_values_col(self):
        prop = self.bridge.grid_properties["ThreeProp"]

        col = prop.column(i=2, j=1)
        col.set([0, 0.1, 0.2])

        col2 = prop.column(i=2, j=1)
        self.assertSequenceAlmostEqual(col2.as_array(), [0, 0.1, 0.2])

    def test_slice_set_values_layer(self):
        prop = self.bridge.grid_properties["ThreeProp"]

        layer = prop.layer(k=1)
        layer.set([v * 2 for v in layer.as_array()])
        self.assertSequenceEqual(
            [v for v in _utils.iterable_values(layer.as_array())],
            [200, 220, 240, 202, 222, 242, 204, 224, 244],
        )

    def test_slice_checks_length(self):
        prop = self.bridge.grid_properties["ThreeProp"]

        with self.assertRaises(ValueError):
            col = prop.column(i=2, j=1)
            too_long = [v for v in col.as_array()] + [0]
            col.set(too_long)

        with self.assertRaises(ValueError):
            layer = prop.layer(k=1)
            too_long = [v for v in layer.as_array()] + [0]
            layer.set(too_long)

    def test_slice_converts_2d_arrays(self):
        prop = self.bridge.grid_properties["ThreeProp"]

        layer = prop.layer(k=1)
        newvals = [9 * v for v in layer.as_array()]
        layer.set(newvals)
        for (i, j, k, v) in prop.layer(k=1).enumerate():
            self.assertEqual(9 * (i + 10 * j + 100 * k), v)

    def test_slice_context(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        layer = prop.layer(1)

        with layer.values() as vals:
            vals[1, 2] = 42

        self.assertEqual(42, prop.layer(1).as_array()[1, 2])

        # example code using values() and rawvalues
        for k in range(0, prop.grid.extent.k):
            layer = prop.layer(k)
            with layer.values() as vals:
                for (i, j, k, _) in layer.enumerate():
                    vals[i, j] = k

        for k in range(0, prop.grid.extent.k):
            vals = prop.layer(k).as_array()
            for v in _utils.iterable_values(vals):
                self.assertEqual(k, v)

    def test_slice_surface_attribute(self):
        surfaceprop = self.bridge.surface_attributes["ThreeSurfaceProp"]
        slice = surfaceprop.all()
        self.assertEqual(9, len(_utils.iterable_values(slice.as_array())))
        self.assertSequenceEqual(
            [v for v in _utils.iterable_values(slice.as_array())],
            [0, 10, 20, 1, 11, 21, 2, 12, 22],
        )

    def test_slice_surface_attribute_write(self):
        surfaceprop = self.bridge.surface_attributes["ThreeSurfaceProp"]
        slice = surfaceprop.all()
        self.assertSequenceEqual(
            [v for v in _utils.iterable_values(slice.as_array())],
            [0, 10, 20, 1, 11, 21, 2, 12, 22],
        )
        slice.set([2 * v for v in slice.as_array()])
        self.assertSequenceEqual(
            [v for v in _utils.iterable_values(slice.as_array())],
            [0, 20, 40, 2, 22, 42, 4, 24, 44],
        )

    def test_chunk_surface_property(self):
        sp = self.bridge.surface_attributes["ThreeSurfaceProp"]
        chunk = sp.chunk((0, 1), (0, 1))
        data = _utils.iterable_values(chunk.as_array())
        data_vec = [v for v in data]
        self.assertEqual(4, len(data_vec))
        self.assertSequenceEqual(data_vec, [0, 10, 1, 11])
        chunk_1 = sp.chunk((0, 0), (0, 0))
        chunk_1.set(42)
        chunk_2 = sp.chunk((0, 1), (0, 1))
        new_data_vec = [v for v in _utils.iterable_values(chunk_2.as_array())]
        self.assertSequenceEqual(new_data_vec, [42, 10, 1, 11])

    def test_chunk_dictionary_surface_property(self):
        dsp = self.bridge.surface_discrete_attributes["ThreeDictSurfaceProp"]
        chunk = dsp.chunk((0, 1), (0, 1))
        data = _utils.iterable_values(chunk.as_array())
        data_vec = [v for v in data]
        self.assertEqual(4, len(data_vec))
        self.assertSequenceEqual(data_vec, [0, 10, 1, 11])
        chunk_1 = dsp.chunk((0, 0), (0, 0))
        chunk_1.set(42)
        chunk_2 = dsp.chunk((0, 1), (0, 1))
        new_data_vec = [v for v in _utils.iterable_values(chunk_2.as_array())]
        self.assertSequenceEqual(new_data_vec, [42, 10, 1, 11])

    def test_slice_surface_attribute_enumerate(self):
        surfaceprop = self.bridge.surface_attributes["ThreeSurfaceProp"]
        for (i, j, _, val) in surfaceprop.all().enumerate():
            self.assertEqual(10 * j + i, val)

    def test_slice_horizon_interpretation_3d(self):
        hi3d = self.bridge.horizon_interpretation_3ds["hi3d"]
        slice = hi3d.all()
        self.assertEqual(9, len(_utils.iterable_values(slice.as_array())))
        self.assertSequenceEqual(
            [v for v in _utils.iterable_values(slice.as_array())],
            [0, 10, 20, 1, 11, 21, 2, 12, 22],
        )

    def test_chunk_horizon_property_3d(self):
        hp3d = self.bridge.horizon_interpretation_3ds["hi3d"].horizon_property_3ds[0]
        chunk = hp3d.chunk((0, 1), (0, 1))
        data = _utils.iterable_values(chunk.as_array())
        data_vec = [v for v in data]
        self.assertEqual(4, len(data_vec))
        self.assertSequenceEqual(data_vec, [0, 10, 1, 11])
        chunk_1 = hp3d.chunk((0, 0), (0, 0))
        chunk_1.set(42)
        chunk_2 = hp3d.chunk((0, 1), (0, 1))
        new_data_vec = [v for v in _utils.iterable_values(chunk_2.as_array())]
        self.assertSequenceEqual(new_data_vec, [42, 10, 1, 11])

    def test_chunk_horizon_interpretation_3d(self):
        hi3d = self.bridge.horizon_interpretation_3ds["hi3d"]
        chunk = hi3d.chunk((0, 1), (0, 1))
        data = _utils.iterable_values(chunk.as_array())
        data_vec = [v for v in data]
        self.assertEqual(4, len(data_vec))
        self.assertSequenceEqual(data_vec, [0, 10, 1, 11])
        chunk_1 = hi3d.chunk((0, 0), (0, 0))
        chunk_1.set(42)
        chunk_2 = hi3d.chunk((0, 1), (0, 1))
        new_data_vec = [v for v in _utils.iterable_values(chunk_2.as_array())]
        self.assertSequenceEqual(new_data_vec, [42, 10, 1, 11])

    def test_slice_horizon_interpretation_3d_write(self):
        hi3d = self.bridge.horizon_interpretation_3ds["hi3d"]
        slice = hi3d.all()
        self.assertSequenceEqual(
            [v for v in _utils.iterable_values(slice.as_array())],
            [0, 10, 20, 1, 11, 21, 2, 12, 22],
        )
        slice.set([2 * v for v in slice.as_array()])
        self.assertSequenceEqual(
            [v for v in _utils.iterable_values(slice.as_array())],
            [0, 20, 40, 2, 22, 42, 4, 24, 44],
        )

    def test_slice_horizon_interpretation_3d_enumerate(self):
        hi3d = self.bridge.horizon_interpretation_3ds["hi3d"]
        slice = hi3d.all()
        for (i, j, _, val) in slice.enumerate():
            self.assertEqual(10 * j + i, val)

    def test_slice_set_slice_layer(self):
        prop = self.bridge.grid_properties["ThreeProp"]

        layer0 = prop.layer(0)
        layer1 = prop.layer(1)

        layer0.set(layer1)
        self.assertSequenceEqual(
            [v for v in _utils.iterable_values(prop.layer(0).as_array())],
            [v for v in _utils.iterable_values(prop.layer(1).as_array())],
        )

    def test_slice_set_slice_col(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        col0 = prop.column(0, 0)
        col1 = prop.column(1, 1)
        col0.set(col1)
        self.assertSequenceEqual(
            [v for v in prop.column(0, 0).as_array()],
            [v for v in prop.column(1, 1).as_array()],
        )

    def test_slice_set_slice_fails(self):
        prop = self.bridge.grid_properties["ThreeProp"]

        layer0 = prop.layer(0)
        col = prop.column(1, 2)
        with self.assertRaises(ValueError):
            layer0.set(col)

    def test_slice_set_val(self):
        prop = self.bridge.grid_properties["ThreeProp"]

        layer0 = prop.layer(0)
        layer0.set(0)
        self.assertSequenceEqual(
            [v for v in _utils.iterable_values(prop.layer(0).as_array())], [0] * 9
        )

    def test_slice_set_value_rawvalues(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])
        colA.set([42.0, 42.0, 42.0])
        self.assertSequenceEqual(
            [v for v in prop.column(0, 0).as_array()], [42.0] * 3
        )

    def test_slice_simple_add(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

        colB = prop.column(1, 1)
        colB.set(colA + 1)
        self.assertSequenceEqual([v for v in colB.as_array()], [1.0, 101.0, 201.0])

    def test_slice_simple_radd(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

        colB = prop.column(1, 1)
        colB.set(1 + colA)
        self.assertSequenceEqual([v for v in colB.as_array()], [1.0, 101.0, 201.0])

    def test_slice_simple_sub(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

        colB = prop.column(1, 1)
        colB.set(colA - 1)
        self.assertSequenceEqual([v for v in colB.as_array()], [-1.0, 99.0, 199.0])

    def test_slice_simple_rsub(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

        colB = prop.column(1, 1)
        colB.set(1 - colA)
        self.assertSequenceEqual(
            [v for v in colB.as_array()], [1.0, -99.0, -199.0]
        )

    def test_slice_simple_mul(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

        colB = prop.column(1, 1)
        colB.set(colA * 2)
        self.assertSequenceEqual([v for v in colB.as_array()], [0.0, 200.0, 400.0])

    def test_slice_simple_rmul(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

        colB = prop.column(1, 1)
        colB.set(2 * colA)
        self.assertSequenceEqual([v for v in colB.as_array()], [0.0, 200.0, 400.0])

    def test_slice_simple_div(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

        colB = prop.column(1, 1)
        colB.set(colA / 2)
        self.assertSequenceEqual([v for v in colB.as_array()], [0.0, 50.0, 100.0])

    def test_slice_simple_rdiv(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(1, 0)
        self.assertSequenceAlmostEqual(
            [v for v in colA.as_array()], [1.0, 101.0, 201.0]
        )

        colB = prop.column(1, 1)
        colB.set(100 / colA)
        self.assertSequenceAlmostEqual(
            [v for v in colB.as_array()], [100.0, 100.0 / 101.0, 100 / 201.0]
        )

    def test_slice_simple_add_slice(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

        colB = prop.column(1, 1)
        self.assertSequenceEqual(
            [v for v in colB.as_array()], [11.0, 111.0, 211.0]
        )

        prop.column(2, 2).set(colA + colB)

        self.assertSequenceEqual(
            [v for v in prop.column(2, 2).as_array()], [11.0, 211.0, 411.0]
        )

    def test_slice_average(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

        colB = prop.column(1, 1)
        self.assertSequenceEqual(
            [v for v in colB.as_array()], [11.0, 111.0, 211.0]
        )

        prop.column(2, 2).set((colA + colB) / 2)
        self.assertSequenceEqual(
            [v for v in prop.column(2, 2).as_array()], [5.5, 105.5, 205.5]
        )

    def test_slice_disconnected(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertFalse(colA.disconnected)
        colB = colA + 0
        self.assertTrue(colB.disconnected)

    def test_slice_clone(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        colA = prop.column(0, 0)
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])
        colClone = colA.clone()
        self.assertSequenceEqual(
            [v for v in colClone.as_array()], [0.0, 100.0, 200.0]
        )
        # test the original column's values aren't affected
        colClone.as_array()[0] = 42.0
        self.assertSequenceEqual(
            [v for v in colClone.as_array()], [42.0, 100.0, 200.0]
        )
        self.assertSequenceEqual([v for v in colA.as_array()], [0.0, 100.0, 200.0])

    def test_slice_compatability(self):
        threeProp = self.bridge.grid_properties["ThreeProp"]
        threeDiscProp = self.bridge.discrete_grid_properties["ThreeDiscProp"]
        fourDiscProp = self.bridge.discrete_grid_properties["FourDiscProp"]
        threeProp.column(0, 0).set(threeProp.column(1, 1))
        with self.assertRaises(ValueError):
            threeProp.column(0, 0).set(threeDiscProp.column(0, 0))
        with self.assertRaises(ValueError):
            threeDiscProp.column(0, 0).set(fourDiscProp.column(0, 0))
        with self.assertRaises(ValueError):
            threeProp.column(0, 0).set(threeProp.layer(0))

    def test_slice_compatability_with_arithmetic(self):
        threeProp = self.bridge.grid_properties["ThreeProp"]
        threeDiscProp = self.bridge.discrete_grid_properties["ThreeDiscProp"]
        fourDiscProp = self.bridge.discrete_grid_properties["FourDiscProp"]
        threeProp.column(0, 0) + threeProp.column(1, 1)
        with self.assertRaises(ValueError):
            threeProp.column(0, 0) + threeDiscProp.column(0, 0)
        with self.assertRaises(ValueError):
            threeDiscProp.column(0, 0) + fourDiscProp.column(0, 0)
        with self.assertRaises(ValueError):
            threeProp.column(0, 0) + threeProp.layer(0)

    def test_slice_arithmetic_disallowed(self):
        threeDiscProp = self.bridge.discrete_grid_properties["ThreeDiscProp"]
        col = threeDiscProp.column(1, 1)
        with self.assertRaises(ValueError):
            col + 1
        with self.assertRaises(ValueError):
            col - 1
        with self.assertRaises(ValueError):
            col * 1
        with self.assertRaises(ValueError):
            col / 1
        with self.assertRaises(ValueError):
            1 + col
        with self.assertRaises(ValueError):
            1 - col
        with self.assertRaises(ValueError):
            1 * col
        with self.assertRaises(ValueError):
            1 / col

    def test_3d_slice(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        self.assertEqual(
            27, len([v for v in _utils.iterable_values(prop.all().as_array())])
        )

        for (i, j, k, v) in prop.all().enumerate():
            self.assertTrue(value_correct(i, j, k, v))
        self.assertEqual(27, len([v for v in prop.all().enumerate()]))

    def test_3d_slice_set_single_val(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        prop.all().set(0.1)
        self.assertSequenceAlmostEqual([0.1] * 27, prop.all().as_array())

    def test_3d_slice_set_list(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        prop.all().set([0.1] * 27)
        self.assertSequenceAlmostEqual([0.1] * 27, prop.all().as_array())

    def test_3d_slice_set_list_of_lists_of_lists(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        prop.all().set([[[0.1] * 3] * 3] * 3)
        self.assertSequenceAlmostEqual([0.1] * 27, prop.all().as_array())

    def test_3d_slice_arithmetic(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        prop.all().set(1.0)
        prop.all().set(prop.all() * 2)
        self.assertSequenceAlmostEqual([2.0] * 27, prop.all().as_array())

    def test_3d_chunk(self):        
        prop = self.bridge.grid_properties["MyProp"]
        vals = [
            v
            for v in _utils.iterable_values(
                prop.chunk((1, 2), (2, 3), (3, 4)).as_array()
            )
        ]
        self.assertSequenceAlmostEqual(
            vals, [321.0, 421.0, 331.0, 431.0, 322.0, 422.0, 332.0, 432.0]
        )

    def test_3d_chunk_enumerate(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk = prop.chunk((1, 2), (2, 3), (3, 4))
        for (i, j, k, val) in chunk.enumerate():
            self.assertAlmostEqual(k * 100 + j * 10 + i, val)

    def test_3d_chunk_object_extent(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk = prop.chunk((1, 2), (2, 3), (3, 4))
        oe = chunk.object_extent
        self.assertEqual(oe.i, 10)
        self.assertEqual(oe.j, 10)
        self.assertEqual(oe.k, 10)

    def test_3d_chunk_slice_extent(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk = prop.chunk((1, 2), (2, 4), (3, 6))
        se = chunk.slice_extent
        self.assertEqual(se.i, 2)
        self.assertEqual(se.j, 3)
        self.assertEqual(se.k, 4)

    def test_3d_chunk_slice_extent_span_i(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk = prop.chunk((), (2, 3), (3, 4))
        se = chunk.slice_extent
        self.assertEqual(se.i, 10)
        self.assertEqual(se.j, 2)
        self.assertEqual(se.k, 2)

    def test_3d_chunk_slice_extent_span_i_as_none(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk = prop.chunk(None, (2, 3), (3, 4))
        se = chunk.slice_extent
        self.assertEqual(se.i, 10)
        self.assertEqual(se.j, 2)
        self.assertEqual(se.k, 2)

    def test_3d_chunk_slice_extent_span_j(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk = prop.chunk((1, 2), (), (3, 4))
        se = chunk.slice_extent
        self.assertEqual(se.i, 2)
        self.assertEqual(se.j, 10)
        self.assertEqual(se.k, 2)

    def test_3d_chunk_slice_extent_span_j_as_none(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk = prop.chunk((1, 2), None, (3, 4))
        se = chunk.slice_extent
        self.assertEqual(se.i, 2)
        self.assertEqual(se.j, 10)
        self.assertEqual(se.k, 2)

    def test_3d_chunk_slice_extent_span_k(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk = prop.chunk((1, 2), (2, 3), ())
        se = chunk.slice_extent
        self.assertEqual(se.i, 2)
        self.assertEqual(se.j, 2)
        self.assertEqual(se.k, 10)

    def test_3d_chunk_slice_extent_span_k_as_none(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk = prop.chunk((1, 2), (2, 3), None)
        se = chunk.slice_extent
        self.assertEqual(se.i, 2)
        self.assertEqual(se.j, 2)
        self.assertEqual(se.k, 10)

    def test_3d_chunk_enumerate_spannning_i(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        chunk = prop.chunk((), (0, 1), (1, 2))
        for (i, j, k, val) in chunk.enumerate():
            self.assertEqual(val, k * 100 + j * 10 + i)

    def test_3d_chunk_enumerate_spannning_j(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        chunk = prop.chunk((0, 1), (), (1, 2))
        for (i, j, k, val) in chunk.enumerate():
            self.assertEqual(val, k * 100 + j * 10 + i)

    def test_3d_chunk_enumerate_spannning_k(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        chunk = prop.chunk((0, 1), (1, 2), ())
        for (i, j, k, val) in chunk.enumerate():
            self.assertEqual(val, k * 100 + j * 10 + i)

    def expect_exception(exception):
        """Marks test to expect the specified exception. Call assertRaises internally"""

        def test_decorator(fn):
            def test_decorated(self, *args, **kwargs):
                self.assertRaises(exception, fn, self, *args, **kwargs)

            return test_decorated

        return test_decorator

    # test out-of-bounds in all ijk-range chunk args
    @expect_exception(ValueError) # type: ignore
    def test_3d_chunk_outofbounds_i(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        chunk = prop.chunk((0, 1000), (), ())

    # test out-of-order bounsd in all ijk-range chunk args

    # test chunk value random access

    # test chunk writing
    def test_3d_chunk_write_array(self):
        prop = self.bridge.grid_properties["ThreeProp"]
        chunk = prop.chunk((0, 1), (1, 2), 2)
        vs = chunk.as_array()
        self.assertSequenceEqual(
            list(_utils.iterable_values(vs)), [210.0, 220.0, 211.0, 221.0]
        )
        vs[0, 0, 0] = 999.9
        chunk.set(vs)
        self.assertSequenceEqual(
            list(_utils.iterable_values(vs)), [999.9, 220.0, 211.0, 221.0]
        )
        vs[1, 1, 0] = 888.8
        chunk.set(vs)
        self.assertSequenceEqual(
            list(_utils.iterable_values(vs)), [999.9, 220.0, 211.0, 888.8]
        )

    # test chunk assiging to another property in same place

    # test chunk assiging to another property in different place
    def test_3d_chunk_write_array_different_property_different_place(self):
        prop_large = self.bridge.grid_properties["MyProp"]
        prop_small = self.bridge.grid_properties["ThreeProp"]
        chunk_source = prop_small.chunk((), (), ())
        chunk_target = prop_large.chunk((0, 2), (1, 3), (2, 4))
        chunk_source.set(chunk_target)

    # test chunk assigning to same property, different place
    def test_3d_chunk_write_array_different_place(self):
        prop = self.bridge.grid_properties["MyProp"]
        chunk_a = prop.chunk((0, 1), (0, 1), (0, 1))
        self.assertSequenceEqual(
            list(_utils.iterable_values(chunk_a.as_array())),
            [0.0, 100.0, 10.0, 110.0, 1.0, 101.0, 11.0, 111.0],
        )

        chunk_b = prop.chunk((5, 6), (6, 7), (7, 8))
        chunk_b.set(chunk_a)

        chunk_c = prop.chunk((5, 6), (6, 7), (7, 8))
        self.assertSequenceEqual(
            list(_utils.iterable_values(chunk_c.as_array())),
            [0.0, 100.0, 10.0, 110.0, 1.0, 101.0, 11.0, 111.0],
        )

    @unittest.skipUnless(_utils.python_env() == _utils.CPY3, "Can only run on CPython")
    def test_dataframe(self):
        prop = self.bridge.grid_properties["MyProp"]
        df = prop.chunk((), (), ()).as_dataframe()
        for (_, i, j, k, v) in df.itertuples():
            self.assertEqual(i + 10 * j + 100 * k, v)
