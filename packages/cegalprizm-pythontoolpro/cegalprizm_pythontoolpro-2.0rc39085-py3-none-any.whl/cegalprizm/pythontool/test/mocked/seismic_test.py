# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool import _utils
from .inprocesstestcase import InprocessTestCase

class SeismicTest(InprocessTestCase):

    def setUp(self):
        super().setUp()
        self.cube = self.bridge.seismic_cubes['FiveCube']
        self.reset()

    def reset(self):
        self.cube._petrel_object_link.Reset()

    def test_check(self):
        self.assertEqual(2, 1+1)

    def test_dims(self):
        self.assertEqual(5, self.cube.extent.i)
        self.assertEqual(5, self.cube.extent.j)
        self.assertEqual(5, self.cube.extent.k)

    # test all columns
    def test_all_column_values_get(self):
        for i in range(0, self.cube.extent.i):
            for j in range(0, self.cube.extent.j):
                col = self.cube.column(i, j)
                with col.values() as vals:
                    for k in range(0, self.cube.extent.k):
                        self.assertEqual(i + 10 * j + 100 * k, vals[k])

    def test_all_column_values_set(self):
        for i in range(0, self.cube.extent.i):
            for j in range(0, self.cube.extent.j):
                self.reset()
                col_a = self.cube.column(i, j)
                col_a.set(999.0)
                new_col_vals = self.cube.column(i, j).as_array()
                for val in new_col_vals:
                    self.assertEqual(999.0, val)

    # test all layers
    def test_all_layers_values_get(self):
        for k in range(0, self.cube.extent.k):
            layer = self.cube.layer(k)
            for (i, j, k, val) in layer.enumerate():
                self.assertEqual(i + 10 * j + 100 * k, val)

    def test_all_layers_values_set(self):
        for k in range(0, self.cube.extent.k):
            self.reset()
            layer_a = self.cube.layer(k)
            layer_a.set(999.0)
            new_layer_vals = list(_utils.iterable_values(self.cube.layer(k).as_array()))
            for val in new_layer_vals:
                self.assertEqual(999.0, val)

    def test_chunk_no_args(self):
        chunk = self.cube.chunk((), (), ())
        self.assertEqual(chunk.slice_extent.i, self.cube.extent.i)
        self.assertEqual(chunk.slice_extent.j, self.cube.extent.j)
        self.assertEqual(chunk.slice_extent.k, self.cube.extent.k)

    def test_all(self):
        chunk = self.cube.all()
        self.assertEqual(chunk.slice_extent.i, self.cube.extent.i)
        self.assertEqual(chunk.slice_extent.j, self.cube.extent.j)
        self.assertEqual(chunk.slice_extent.k, self.cube.extent.k)

    # test allchunks
    def test_all_possible_chunks(self):

        extent = self.cube.extent

        def is_in(idx, idx_tuple):
            if idx_tuple is not None:
                return idx >= idx_tuple[0] and idx <= idx_tuple[1]
            else:
                return True

        def check_chunk(irange, jrange, krange):
            self.reset()
            c = self.cube.chunk(irange, jrange, krange)
            self.assertIsNotNone(c.as_array())
    
            c.set(999.0)

            with self.cube.chunk((), (), ()).values() as vals:
                for i in range(0, extent.i):
                    for j in range(0, extent.j):
                        for k in range(0, extent.k):
                            if is_in(i, irange) and is_in(j, jrange) and is_in(k, krange):
                                self.assertEqual(vals[i, j, k], 999.0)
                            else:
                                self.assertEqual(vals[i, j, k], i + j * 10 + k * 100)
        # get a chunk
        # iterate over it
        # check values for each
        possible_is = [None] + list(range(0, 2))##extent.i))
        possible_js = [None] + list(range(0, 2))#extent.j))
        possible_ks = [None] + list(range(0, 2))##extent.k))

        import itertools as it

        i_s = [None] + [(f, t) for (f, t) in it.combinations(possible_is, 2) if f is not None]
        j_s = [None] + [(f, t) for (f, t) in it.combinations(possible_js, 2) if f is not None]
        k_s = [None] + [(f, t) for (f, t) in it.combinations(possible_ks, 2) if f is not None]

        for irange in i_s:
            for jrange in j_s:
                for krange in k_s:
                    check_chunk(irange, jrange, krange)
