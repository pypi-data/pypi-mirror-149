# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import functools
import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.points import _PointsProvider
class _ChunkingArrayProvider:
    """Backing data provider - would be a GRPC call to Petrel"""

    _hits = 0
    # purposely not a cache_width
    _len = 104

    def get_range(self, start_incl, end_excl):
        self._hits += 1
        if (
            start_incl >= self._len
            or start_incl < 0
            or end_excl > self._len
            or end_excl <= 0
        ):
            raise Exception("Provider get_range oob: %d, %d" % (start_incl, end_excl))
        return list(range(start_incl, end_excl))

    def get_len(self):
        return self._len

    def reset(self):
        self._hits = 0

    # for checking cache hits in tests
    @property
    def hits(self):
        return self._hits


class _ChunkingArray:
    
    def __init__(self, provider: "_PointsProvider", chunk_size: int = 10):
        """An indexable data-structure which fetches chunks of data from
        `provider` transparently

        provider: datasource with `get_range` and `get_len` methods
        cache_width: size of chunks to fetch
        """
        self.provider = provider
        self._chunk_size = chunk_size

    # since people will usually iterate forwards, it's not really necessary to
    # cache much at all in this lru
    @functools.lru_cache(maxsize=128)
    def _get_range(self, start_incl, end_excl):
        if start_incl > len(self):
            return []
        if end_excl >= len(self):
            end_excl = len(self)
        return self.provider.get_range(start_incl, end_excl)

    def __getitem__(self, key):
        # always get ranges in multiples of window size so they can be cached
        if isinstance(key, int):
            if key >= len(self):
                raise IndexError("Index out-of-range [{key}]")

            d, m = divmod(key, self._chunk_size)
            return self._get_range(
                d * self._chunk_size, (d * self._chunk_size) + self._chunk_size
            )[m]
        if isinstance(key, slice):
            if (
                key.start >= len(self)
                or key.stop > len(self)
                or key.start < 0
                or key.stop <= 0
            ):
                raise IndexError("Slice out-of-range [" + key + "]")
            # assemble the chunks implied by the slice linearly
            d = key.start // self._chunk_size
            assembled = []
            idx = d * self._chunk_size
            while idx < key.stop:
                d = idx // self._chunk_size
                chunk = self._get_range(
                    d * self._chunk_size, (d * self._chunk_size) + self._chunk_size
                )
                assembled = assembled + chunk
                idx = idx + self._chunk_size

            # adjust the slice so it is offset to the chunk-assembly
            new_start = key.start % self._chunk_size
            new_stop = new_start + (key.stop - key.start)
            # return the applied slice
            return assembled[slice(new_start, new_stop, key.step)]
        raise ValueError("Must supply an int or slice")

    def __len__(self):
        return self.provider.get_len()

# @pytest.fixture
# def provider():
#     return Provider()


# @pytest.fixture
# def carray(provider):
#     return ChunkingArray(provider)


# def test_simple(carray):
#     assert carray[3] == 3
#     assert carray.provider.hits == 1


# def test_int_cache_miss(carray):
#     idx = 0
#     assert carray[idx] == idx
#     idx += carray._chunk_size
#     assert carray[idx] == idx
#     assert carray.provider.hits == 2


# def test_int_cache_hit(carray):
#     idx = 0
#     assert carray[idx] == idx
#     idx += carray._chunk_size - 1
#     assert carray[idx] == idx
#     assert carray.provider.hits == 1


# def test_slice_within_cache_width(carray):
#     assert carray[0:3] == [0, 1, 2]


# def test_slice_within_cache_width_hits(carray):
#     carray.provider.reset()
#     assert carray[0:3] == [0, 1, 2]
#     assert carray.provider.hits == 1


# def test_slice_across_1_cache_width(carray):
#     carray.provider.reset()
#     assert carray[8:12] == [8, 9, 10, 11]
#     assert carray.provider.hits == 2


# def test_can_convert_to_numpy_explicitly(carray):
#     a = np.array(carray[0 : len(carray)])
#     assert_array_equal(a, np.arange(0, len(carray)))


# def test_can_convert_to_numpy_implicitly(carray):
#     a = np.array(carray)
#     assert_array_equal(a, np.arange(0, len(carray)))


# def test_len(carray):
#     assert len(carray) == carray.provider.get_len()


# def test_iter(carray):
#     lst = []
#     for i in carray:
#         lst.append(i)
#     assert lst == list(range(0, carray.provider.get_len()))


# def test_int_out_of_range(carray):
#     oob_idx = carray.provider.get_len() + 1
#     with pytest.raises(IndexError):
#         carray[oob_idx]


# def test_slice_out_of_range_partial(carray):
#     idx = carray.provider.get_len() - 10
#     oob_idx = carray.provider.get_len() + 1
#     with pytest.raises(IndexError):
#         carray[idx:oob_idx]


# def test_slice_out_of_range_total(carray):
#     oob_idx = carray.provider.get_len() + 1
#     with pytest.raises(IndexError):
#         carray[oob_idx : oob_idx + 5]
