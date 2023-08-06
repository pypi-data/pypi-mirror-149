# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import typing
import numpy as np
import pandas as pd
from warnings import warn
from cegalprizm.pythontool._toolmode import _ToolMode

import math
from cegalprizm.pythontool import exceptions
import contextlib

from cegalprizm.pythontool.chunktype import ChunkType
from cegalprizm.pythontool.primitives import Extent
from cegalprizm.pythontool import _utils


class Chunk(object):
    """An object allowing manipulation of the data in a Petrel object.
    """

    def _ensure_tuple(self, v: typing.Any) -> typing.Optional[typing.Tuple[int, int]]:
        if v is None:
            return None
        if type(v) is tuple and len(v) == 2 and type(v[0])==int and type(v[1])==int:
            return typing.cast(typing.Tuple[int, int], v)
        if type(v) is int:
            return (v, v)
        raise ValueError(f"Neither tuple nor int? {v}")

    def __init__(
        self,
        i,
        j,
        k,
        backing_object,
        extent,
        value_getters,
        value_setters,
        value_shapers,
        value_accessors,
        value_enumerations,
        chunk_type: typing.Optional[int] = None,
        readonly: bool = False,
        disconnected: bool = False,
    ):
        """Create a Chunk

        Args:
            i: The specific i-index, or `None` to range over all i-values
            j: The specific j-index, or `None` to range over all j-values
            k: The specific k-index, or `None` to range over all k-values
            extent (petrellink.primitives.Extent): The extent of the backing object
            value_getters: a dict indexed by ChunkType storing value-getting functions (see later)
            value_setters: a dict indexed by ChunkType storing value-setting functions (see later)
            value_shapers: a dict indexed by ChunkType storing value-shaping functions (see later)
            value_accessors: a dict indexed by ChunkType storing value-accessor-creating functions (see later)
            value_enumerations: a 3-Tuple of booleans indicating which indices this chunk can range over.
            readonly: is the chunk readonly
            disconnected: if disconnected, the chunk does not try and send values to its backing object

        `value_getters`
        --------------

        The functions provided by `value_getters` are called with with
        3 indices (i, j, k) provided by the constructor.  Different
        chunk types can and will ignore some or all of these indices,
        e.g. a 3d grid generating a k-slice will ignore i and j.  Use
        a lambda to create a function which ignores some of its
        arguments.

        `value_setters`
        ---------------

        These functions are called with 3 indices and a values objects.  See `values_getters`.

        `value_shapers`
        ---------------

        The functions are called with 3 indices and a values object.
        Different chunk types and backing objects (e.g a
        DictionaryProperty k-slice) will need to shape the values
        (which may be a System.Array, a Python list or a
        numpy.ndarray) etc into the correct data structure to pass to
        the backing object.

        `value_accessors`
        -----------------

        Backing objects storing .NET System.Arrays or numpy.ndarrays
        demand an indexing object specialized per chunk-type (i.e
        dimensionality of array).  See `Chunk.__make_accessor` for
        details.

        `value_enumerations`
        --------------------

        Different backing objects will enumerate over different
        indices.  For instance, all 3d backing object's chunks will
        enumerate over i, j and k (even if one or more of them are
        constant.  Surfaces will only enumerate over i and j, so pass
        (True, True, False) so the user is not provided a meaningless
        k-index by the enumerate() method.  A 2D Seismic object might
        only enumerate over i and k, so pass (True, False, True) in
        this case.

        """

        # empty tuple is equivalent to None
        if i == ():
            i = None
        if j == ():
            j = None
        if k == ():
            k = None

        if i is not None:
            if type(i) == tuple:
                if(i[0] > i[1] or i[0] < 0 or i[0] > extent.i-1 or i[1] < 0 or i[1] > extent.i-1):
                    raise ValueError("i-index range of chunk " + str(i) + " is not valid index range for object: " + str(extent))
            elif i < 0 or i >= extent.i:
                raise ValueError("i-index of chunk (%d) is not a valid index for object" % i)
        if j is not None:
            if type(j) == tuple:
                if(j[0] > j[1] or j[0] < 0 or j[0] > extent.j-1 or j[1] < 0 or j[1] > extent.j-1):
                    raise ValueError("j-index range of chunk " + str(j) + " is not valid index range for object: " + str(extent))
            elif j < 0 or j >= extent.j:
                raise ValueError("j-index of chunk (%d) is not a valid index for object" % j)
        if k is not None:
            if type(k) == tuple:
                if(k[0] > k[1] or k[0] < 0 or k[0] > extent.k-1 or k[1] < 0 or k[1] > extent.k-1):
                    raise ValueError("k-index range of chunk " + str(k) + " is not valid index range for object: " + str(extent))
            elif k < 0 or k >= extent.k:
                raise ValueError("k-index of chunk (%d) is not a valid index for object" % k)

        if chunk_type is None:
            self._type = ChunkType.make(i, j, k)
        else:
            self._type = chunk_type

        self.__i: typing.Union[typing.Optional[typing.Tuple[int, int]], int] = i if self._type != ChunkType.chunk else self._ensure_tuple(i)
        self.__j: typing.Union[typing.Optional[typing.Tuple[int, int]], int] = j if self._type != ChunkType.chunk else self._ensure_tuple(j)
        self.__k: typing.Union[typing.Optional[typing.Tuple[int, int]], int] = k if self._type != ChunkType.chunk else self._ensure_tuple(k)
        self.__extent = extent
        self.__slice_extent: typing.Union[Extent, None] = None  # will be calculated on_demand
        self.__backing_object = backing_object
        self.__value_getters = value_getters
        self.__value_setters = value_setters
        self.__value_shapers = value_shapers
        self.__value_accessors = value_accessors
        self.__value_enumerations = value_enumerations
        self.__cached = None
        self.__readonly = readonly
        self.__disconnected: bool = disconnected

        if (
            self.slice_extent.i > self.object_extent.i
            or self.slice_extent.j > self.object_extent.j
            or self.slice_extent.k > self.object_extent.k
        ):
            raise ValueError("Chunk too big")

    def __disconnected_clone(self):
        """Produces a disconnected slice"""
        return Chunk(
            self.__i,
            self.__j,
            self.__k,
            self.__backing_object,  # TODO none?
            self.object_extent,
            self.__value_getters,
            self.__value_setters,  # TODO remove this?
            self.__value_shapers,
            self.__value_accessors,
            self.__value_enumerations,
            self._type,
            False,  # no point if it is readonly - and it is disconnected!
            True,
        )

    def clone(self) -> "Chunk":
        """Returns a disconnected clone of the chunk

        The returned object has the same values as the original chunk,
        but it is not connected to any Petrel object.  Use the
        :meth:`set` method of another compatible chunk to set the
        values of a Petrel object.

        Returns:
            cegalprizm.pythontool.Chunk: a disconnected clone of the chunk

        """
        slc = self.__disconnected_clone()
        slc.set(_utils.clone_array(self.as_array()))
        return slc # type: ignore

    @property
    def disconnected(self) -> bool:
        """Is the chunk disconnected?

        Returns:
            bool: ``True`` if the chunk is disconnected
        """
        return self.__disconnected

    @property
    def readonly(self) -> bool:
        """The readonly status of this chunk

        Read-only chunks will not allow you to set the ``rawvalues``
        property.  A ``PythonToolException`` will be raised upon
        setting the ``rawvalues`` property or upon exit of a
        ``values()`` with-block.  However, note that the API does not
        detect changes to the existing values - it is only upon
        finally setting them that an error will be raised

        **Example::**

        .. code-block:: Python

          print(my_prop.readonly)
          # outputs 'True'
          my_prop.column(2, 3).as_array() = [2, 3, 4]
          # error is raised
          my_prop.column(2, 3).as_array()[88] = 1.33
          # no error is raised, but values have not been saved anyway
          with my_prop.column(2, 3).values() as vals:
              vals[88] = 1.33 # no error
          # error raised here

        """
        is_readonly = self.__readonly
        return is_readonly

    @contextlib.contextmanager
    def values(self) -> typing.Iterator[np.ndarray]:
        """A context-manager object which saves values automatically

        Use a with-statement to create this object, and then you can
        set the chunk's values directly.  At the end of the with-statement,
        the values are sent back to Petrel automatically.

        **Example:**

        .. code-block:: Python

            my_layer = my_property.layer(2)
            with my_layer.values() as vals:
                vals[1, 3] = 42
            # here, values are saved automatically to Petrel

        """
        try:
            yield self.as_array()
        finally:
            self.__set_values(self.__values())

    def get_rawvalues(self) -> None:
        """DeprecationWarning: 'get_rawvalues' has been removed. Use 'as_array' instead
        """
        warn("'get_rawvalues' has been removed. Use 'as_array' instead", 
             DeprecationWarning, stacklevel=2)
        raise RuntimeError("'get_rawvalues' has been removed. Use 'as_array' instead")

    def as_array(self) -> np.ndarray:
        """The raw values for the chunk.

        Gets the values covered by the chunk as an array, which will
        be of different dimensionality depending on whether it is a
        1d, 2d or 3d chunk.  If you change the values in this array,
        they will not be persisted in the Petrel project immediately.
        Use the :meth:`set` method to set the values in a Petrel
        object.

        You can treat a ``System.Array`` or ``numpy.ndarray`` as an
        ordinary Python list/iterable, but avoid doing this for
        maximum performance.

        Returns:
        
            numpy.ndarray (CPython): the raw values for the chunk

        **Example:**

        .. code-block:: Python

          # change one cell in a property
          vals = my_property.layer(2).as_array()
          vals[2, 5] = 1.23
          # my_property is unchanged at this point
          my_property.layer(2).set(vals)
          # my_property has now been changed.

          # assign layer 10's values to layer 11 if they are above 0.5, else set 0
          layer10_vals = my_property.layer(10).as_array()
          new_vals = [v if v > 0.5 else 0 for v in layer10_vals]
          my_property.layer(11).set(new_vals)
          # layer 11 has new values.  layer 10 is untouched

        """

        return self.__values()

    def _enumerate_ipy(self):
        for i in self.__irange():
            for j in self.__jrange():
                for k in self.__krange():
                    accessor = self.__make_accessor(i, j, k)
                    val = self.__values()[accessor]
                    yield (i, j, k, val)

    def _enumeratable_arrays_cpy(self) -> typing.Tuple[typing.List[int], typing.List[int], typing.List[int], typing.List[typing.Any]]:
        import numpy as np

        i_idxs = list(self.__irange())
        j_idxs = list(self.__jrange())
        k_idxs = list(self.__krange())

        all_is = np.repeat(i_idxs, len(j_idxs) * len(k_idxs))
        all_js = np.repeat(np.tile(j_idxs, len(i_idxs)), len(k_idxs))
        all_ks = np.tile(k_idxs, len(i_idxs) * len(j_idxs))

        vals = self.__values().ravel()

        return (all_is, all_js, all_ks, vals)

    def _enumerate_cpy(self) -> typing.Iterator[typing.Tuple[int, int, int, typing.Any]]:
        (all_is, all_js, all_ks, vals) = self._enumeratable_arrays_cpy()
        for a in range(0, len(vals)):
            yield (all_is[a], all_js[a], all_ks[a], vals[a])

    def enumerate(self) -> typing.Iterator[typing.Tuple[int, int, int, typing.Any]]:
        """Returns a generator yielding a tuple of the indices and values

        When the generator is evaluated, it will return tuples of the
        form (i, j, k, val) where i, j and k are the indices and val
        is the value at that index.

        This method of enumeration is slower than accessing the value
        array directly (via `as_array`) but gives the user more
        information about the order of indexing

        Returns:
            A generator yielding (i, j, k, value) tuples

        """
        return self._enumerate_cpy()     

    @property
    def i(self) -> typing.Union[typing.Optional[typing.Tuple[int, int]], int]:
        """The `i`-index of this chunk, or `None` if chunk ranges over `i`"""
        return self.__i

    @property
    def j(self) -> typing.Union[typing.Optional[typing.Tuple[int, int]], int]:
        """The `j`-index of this chunk, or `None` if chunk ranges over `j`"""
        return self.__j

    @property
    def k(self) -> typing.Union[typing.Optional[typing.Tuple[int, int]], int]:
        """The `k`-index of this chunk, or `None` if chunk ranges over `k`"""
        return self.__k

    @property
    def object_extent(self):
        """The extent of the object from which the chunk was created

        Returns:
            cegalprizm.pythontool.Extent: the extent of the object 
                from which the chunk was created"""
        return self.__extent

    @property
    def slice_extent(self) -> Extent:
        """The extent of this chunk in the i, j and k directions

        Returns:
            cegalprizm.pythontool.Extent: the extent of this chunk"""
        if self.__slice_extent is None:
            self.__slice_extent = Extent(
                len(self.__irange()), len(self.__jrange()), len(self.__krange())
            )

        return self.__slice_extent

    def set(self, value, value_column_name: str = "Value") -> None:
        """Sets the values of the chunk

        Use this to immediately set the values of the chunk.  If you
        supply a single value then all the values in the chunk will be
        set to this value.  If you supply another Chunk, then as long
        as it is compatible (i.e it has has same size and the same
        'undefined value') this chunk's values will be set to the
        other's.  Alternatively, you can supply a ``list`` (either
        flat or nested) or a ``numpy.ndarray`` (CPython) of the correct dimensions for the
        chunk.  Alternatively 2, you can supply a ``Pandas.DataFrame`` of 
        the correct value count for the chunk (number of rows in input 
        dataframe is same as in the original chunk dataframe). IJK indices in 
        the input dataframe must match IJK indices in the chunk.
        Optionally specify the value_column_name of the column to be set as chunk values
        

        Args:
          value: the value[s] or another Chunk instance or Pandas.DataFrame

        **Example**:

        .. code-block:: python

          # copy column i=8, j=10 to column i=1, j=2
          colA = my_prop.column(1, 2)
          colB = my_prop.column(8, 10)
          colA.set(colB)

          # set column i=3, j=4 to all 1s
          my_prop.column(3, 4).set(1)

        """


        if _utils.python_env() == _utils.CPY3 or _ToolMode.is_oop():
            import numpy as np
            import pandas as pd

            if isinstance(value, pd.DataFrame):
                self.__set_dataframe(value, value_column_name)
                return None
            if isinstance(value, np.int64) or isinstance(value, np.int32):
                self.set(int(value))
            if isinstance(value, np.float64) or isinstance(value, np.float32):
                self.set(float(value))
                
        if isinstance(value, int) or isinstance(value, float):
            self.__set_single_value(value)
        elif isinstance(value, Chunk):
            self.__set_slice(value)
        else:
            self.__set_values(value)

    def as_dataframe(self) -> pd.DataFrame:
        """The values of the chunk as a Pandas dataframe."""
        import pandas as pd

        # Use direct array construction instead of slower enumerate()
        (all_is, all_js, all_ks, vals) = self._enumeratable_arrays_cpy()
        df = pd.DataFrame(
            {"I": all_is, "J": all_js, "K": all_ks, "Value": vals},
            columns=["I", "J", "K", "Value"],
        )
        return df

    def __map_single_val_or_slice(self, other, fn):
        if _utils.python_env() == _utils.CPY3 or _ToolMode.is_oop():
            import numpy as np

            if isinstance(other, np.int32) or isinstance(other, np.int64):
                self.__map_single_val_or_slice(int(other), fn)
            if isinstance(other, np.float64):
                self.__map_single_val_or_slice(float(other), fn)
        clone = self.__disconnected_clone()
        if isinstance(other, int) or isinstance(other, float):
            clone.set(
                [fn(v, other) for v in _utils.iterable_values(self.as_array())]
            )
        elif isinstance(other, Chunk):
            if not self.__compatible(other):
                raise ValueError(
                    "Chunk must be the same orientation, size and have the same undef_value to set other chunk"
                )
            clone.set(
                [
                    fn(a, b)
                    for (a, b) in zip(
                        _utils.iterable_values(self.as_array()),
                        _utils.iterable_values(other.as_array()),
                    )
                ]
            )
        return clone

    def __assert_arithmetic_allowed(self):
        if not self.__arithmetic_ops_allowed():
            raise ValueError(
                "Arithmetic operations are not allowed for chunks of discrete values"
            )

    def __add__(self, other):
        """The add operator: add a scalar value or a Chunk to this chunk, returning a new Chunk

        Use the ordinary Python operator `+` to add a scalar value or
        a whole other Chunk to this chunk, returning a new Chunk.
        This new Chunk is 'disconnected' - it is not attached to a
        Petrel object.  You can change the values in a Petrel object
        by using this returned Chunk in the :meth:`set` method

        This method can be slow: for performance, choose to work
        directly with :obj:`rawvalues` instead.


        Raises:

            ValueError: if the chunk is of discrete values

        **Example**:

        .. code-block:: python

          # set colB to be colA's values + 10
          colA = myprop.column(1, 2)
          colB = myprop.column(10, 12)
          colB.set(colA + 10)

          # set a layer to be the average of two other layers
          myprop.layer(50).set((myprop.layer(48) + myprop.layer(49)) / 2)

        """
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: a + b)

    def __radd__(self, other):
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: a + b)

    def __sub__(self, other):
        """The sub operator: subtract a scalar value or a Chunk from this chunk, returning a new Chunk

        See :func:`__add__` for more details
        """
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: a - b)

    def __rsub__(self, other):
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: b - a)

    def __mul__(self, other):
        """The multiply operator: multiply a scalar value or a Chunk to this chunk, returning a new Chunk

        See :func:`__add__` for more details
        """
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: a * b)

    def __rmul__(self, other):
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: b * a)

    def __truediv__(self, other):
        """The divide operator: divicde a scalar value or a Chunk into this chunk, returning a new Chunk

        See :func:`__add__` for more details
        """
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: float(a) / float(b))

    def __rtruediv__(self, other):
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: float(b) / float(a))

    def __div__(self, other):
        """The divide operator: divicde a scalar value or a Chunk into this chunk, returning a new Chunk

        See :func:`__add__` for more details
        """
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: float(a) / float(b))

    def __rdiv__(self, other):
        self.__assert_arithmetic_allowed()
        return self.__map_single_val_or_slice(other, lambda a, b: float(b) / float(a))

    def _undef_value(self):
        """Inspects the backing object to figure out its undef value"""
        if not self.__backing_object:
            return None
        try:
            undef_value = self.__backing_object.undef_value
        except AttributeError:
            return None
        return undef_value

    def __undef_values_compatible(self, val_a, val_b):
        """Check the undef values are compatible.  NaNs are not equal, so we need a specific check"""
        # if the other doesn't have an undef_value, then it is compatible regardless of what ours is
        if val_b is None:
            return True
        if math.isnan(val_a) and math.isnan(val_b):
            return True
        if val_a == val_b:
            return True
        return False

    def __arithmetic_ops_allowed(self):
        # TODO refactor to use __is_backing_discrete
        """Arithmetic operations are only allowed on continuous chunks, not discrete.

        The heuristic for this is checking if the undef_value is None or NaN"""
        v = self._undef_value()
        return v is None or math.isnan(v)

    def __is_backing_discrete(self):
        """Is the backing object discrete data?"""
        # TODO refactor to query the backing object directly, and not rely on undef_value heuristics
        return not self.__arithmetic_ops_allowed()

    def __compatible(self, other):
        slice_type_equal = self._type == other._type
        extent_equal = self.slice_extent == other.slice_extent
        undefs_equal = self.__undef_values_compatible(
            self._undef_value(), other._undef_value()
        )

        return slice_type_equal and extent_equal and undefs_equal
        # return self._type == other._type and self.slice_extent == other.slice_extent and \
        #    self.__undef_values_compatible(self._undef_value(), other._undef_value())

    def __data_size(self):
        """The length of the data array as determined by the chunktype and the extent"""
        (can_i, can_j, can_k) = self.__value_enumerations

        i_extent = self.slice_extent.i if can_i else 1
        j_extent = self.slice_extent.j if can_j else 1
        k_extent = self.slice_extent.k if can_k else 1

        if self._type == ChunkType.none or self._type == ChunkType.chunk:
            return i_extent * j_extent * k_extent
        elif self._type == ChunkType.i:
            return j_extent * k_extent
        elif self._type == ChunkType.j:
            return i_extent * k_extent
        elif self._type == ChunkType.k:
            return i_extent * j_extent
        elif self._type == ChunkType.ij:
            return k_extent
        elif self._type == ChunkType.jk:
            return i_extent
        elif self._type == ChunkType.ik:
            return j_extent

    def __str__(self) -> str:
        """A readable representation of the Chunk"""
        return "Chunk(backing_object={3}, i={0}, j={1}, k={2})".format(
            self.__i, self.__j, self.__k, self.__backing_object
        )

    def __checked(self, values):
        """The values checked for dimensions and converted if necessary
        to a (multi-dimensional) System.Array"""

        i = self.slice_extent.i
        j = self.slice_extent.j
        k = self.slice_extent.k

        try:
            func = self.__value_shapers[self._type]
        except KeyError:
            raise NotImplementedError(
                "Cannot shape values for chunk " + "type " + str(self._type)
            )

        return func(i, j, k, values)

    def __set_single_value(self, value):
        # TODO instantiate an array, should be much quicker.  Fiddly to get correct dims though
        if self.__is_backing_discrete() and not isinstance(value, int):
            raise ValueError("Must supply an integer to a chunk of a discrete property")
        self.set([value] * self.__data_size())

    def __set_slice(self, other):
        # check slice is compatible
        if not self.__compatible(other):
            raise ValueError(
                "Chunk must be the same orientation and size and have the same undef_value to set other chunk"
            )
        self.set(other.as_array())

    def __set_dataframe(self, value_df, value_column_name="Value"):
        if (value_column_name not in value_df.columns):
            raise ValueError("Dataframe must include column named 'Value' or the named column specified when setting chunk (e.g. chunk.set(df,'Value_new')")
        if (self.__is_backing_discrete() and not (value_df[value_column_name].fillna(-9999) % 1  == 0).all()):
            raise ValueError("Must supply integers to a chunk of a discrete property")

        value_col_index = value_df.columns.get_loc(value_column_name)
        array = self.as_array()
        if (self._type is ChunkType.chunk):
            i_exist = "I" in value_df.columns or "i" in value_df.columns
            j_exist = "J" in value_df.columns or "j" in value_df.columns
            k_exist = "K" in value_df.columns or "k" in value_df.columns
            if not (i_exist and j_exist and k_exist):
                raise exceptions.PythonToolException("Can only set chunk column values with dataframe containing a 'I'/'i','J'/'j' and 'K'/'k' column")
            i_col_index = value_df.columns.get_loc("I" if "I" in value_df.columns else "i")
            j_col_index = value_df.columns.get_loc("J" if "J" in value_df.columns else "j")
            k_col_index = value_df.columns.get_loc("K" if "K" in value_df.columns else "k")
            for row in value_df.values:
                i_verified, new_row_i = self.__verify_row_index_and_shift_to_array(row[i_col_index], self.__i, self.object_extent.i)
                j_verified, new_row_j = self.__verify_row_index_and_shift_to_array(row[j_col_index], self.__j, self.object_extent.j)
                k_verified, new_row_k = self.__verify_row_index_and_shift_to_array(row[k_col_index], self.__k, self.object_extent.k)       
                if i_verified and j_verified and k_verified:
                    array[int(new_row_i), int(new_row_j), int(new_row_k)] = row[value_col_index]

        elif (self._type is ChunkType.none):
            i_exist = "I" in value_df.columns or "i" in value_df.columns
            j_exist = "J" in value_df.columns or "j" in value_df.columns
            k_exist = "K" in value_df.columns or "k" in value_df.columns
            if not (i_exist and j_exist and k_exist):
                raise exceptions.PythonToolException("Can only set chunk column values with dataframe containing a 'I'/'i','J'/'j' and 'K'/'k' column")
            i_col_index = value_df.columns.get_loc("I" if "I" in value_df.columns else "i")
            j_col_index = value_df.columns.get_loc("J" if "J" in value_df.columns else "j")
            k_col_index = value_df.columns.get_loc("K" if "K" in value_df.columns else "k")
            for row in value_df.values:
                i_verified, new_row_i = self.__verify_row_index_and_shift_to_array(row[i_col_index], self.__i, self.object_extent.i)
                j_verified, new_row_j = self.__verify_row_index_and_shift_to_array(row[j_col_index], self.__j, self.object_extent.j)
                k_verified, new_row_k = self.__verify_row_index_and_shift_to_array(row[k_col_index], self.__k, self.object_extent.k)       
                if i_verified and j_verified and k_verified: 
                    array[int(new_row_i), int(new_row_j), int(new_row_k)] = row[value_col_index]

        elif (self._type is ChunkType.i):
            j_exist = "J" in value_df.columns or "j" in value_df.columns
            k_exist = "K" in value_df.columns or "k" in value_df.columns
            if not (j_exist and k_exist):
                raise exceptions.PythonToolException("Can only set chunk column values with dataframe containing a 'J'/'j' and 'K'/'k' column")
            j_col_index = value_df.columns.get_loc("J" if "J" in value_df.columns else "j")
            k_col_index = value_df.columns.get_loc("K" if "K" in value_df.columns else "k")
            for row in value_df.values:
                j_verified, new_row_j = self.__verify_row_index_and_shift_to_array(row[j_col_index], self.__j, self.object_extent.j)
                k_verified, new_row_k = self.__verify_row_index_and_shift_to_array(row[k_col_index], self.__k, self.object_extent.k)
                if j_verified and k_verified:
                    array[int(new_row_j), int(new_row_k)] = row[value_col_index]

        elif (self._type is ChunkType.j):
            i_exist = "I" in value_df.columns or "i" in value_df.columns
            k_exist = "K" in value_df.columns or "k" in value_df.columns
            if not (i_exist and k_exist):
                raise exceptions.PythonToolException("Can only set chunk column values with dataframe containing a 'I'/'i' and 'K'/'k' column")
            i_col_index = value_df.columns.get_loc("I" if "I" in value_df.columns else "i")
            k_col_index = value_df.columns.get_loc("K" if "K" in value_df.columns else "k")
            for row in value_df.values:
                i_verified, new_row_i = self.__verify_row_index_and_shift_to_array(row[i_col_index], self.__i, self.object_extent.i)
                k_verified, new_row_k = self.__verify_row_index_and_shift_to_array(row[k_col_index], self.__k, self.object_extent.k)
                if i_verified and k_verified:
                    array[int(new_row_i), int(new_row_k)] = row[value_col_index]

        elif (self._type is ChunkType.k):
            i_exist = "I" in value_df.columns or "i" in value_df.columns
            j_exist = "J" in value_df.columns or "j" in value_df.columns
            if not (i_exist and j_exist):
                raise exceptions.PythonToolException("Can only set chunk column values with dataframe containing a 'I'/'i' and 'J'/'j' column")
            i_col_index = value_df.columns.get_loc("I" if "I" in value_df.columns else "i")
            j_col_index = value_df.columns.get_loc("J" if "J" in value_df.columns else "j")
            for row in value_df.values:
                i_verified, new_row_i = self.__verify_row_index_and_shift_to_array(row[i_col_index], self.__i, self.object_extent.i)
                j_verified, new_row_j = self.__verify_row_index_and_shift_to_array(row[j_col_index], self.__j, self.object_extent.j)
                if i_verified and j_verified:
                    array[int(new_row_i), int(new_row_j)] = row[value_col_index]

        elif (self._type is ChunkType.ij):
            if (not ("K" in value_df.columns or "k" in value_df.columns)):
                raise exceptions.PythonToolException("Can only set chunk column values with dataframe containing a 'K' or 'k' column")
            k_col_index = value_df.columns.get_loc("K" if "K" in value_df.columns else "k")
            for row in value_df.values:
                k_verified, new_row_k = self.__verify_row_index_and_shift_to_array(row[k_col_index], self.__k, self.object_extent.k)
                if k_verified:
                    array[int(new_row_k)] = row[value_col_index]

        elif (self._type is ChunkType.jk):
            if (not ("I" in value_df.columns or "i" in value_df.columns)):
                raise exceptions.PythonToolException("Can only set chunk column values with dataframe containing a 'I' or 'i' column")
            i_col_index = value_df.columns.get_loc("I" if "I" in value_df.columns else "i")
            for row in value_df.values:
                i_verified, new_row_i = self.__verify_row_index_and_shift_to_array(row[i_col_index], self.__i, self.object_extent.i)
                if i_verified:
                    array[int(new_row_i)] = row[value_col_index]

        elif (self._type is ChunkType.ik):
            if (not ("J" in value_df.columns or "j" in value_df.columns)):
                raise exceptions.PythonToolException("Can only set chunk column values with dataframe containing a 'J' or 'j' column")
            j_col_index = value_df.columns.get_loc("J" if "J" in value_df.columns else "j")
            for row in value_df.values:
                j_verified, new_row_j = self.__verify_row_index_and_shift_to_array(row[j_col_index], self.__j, self.object_extent.j)
                if j_verified:
                    array[int(new_row_j)] = row[value_col_index]
        
        elif (self._type is ChunkType.ijk):
            i_exist = "I" in value_df.columns or "i" in value_df.columns
            j_exist = "J" in value_df.columns or "j" in value_df.columns
            k_exist = "K" in value_df.columns or "k" in value_df.columns
            if not (i_exist and j_exist and k_exist):
                raise exceptions.PythonToolException("Can only set chunk column values with dataframe containing a 'I'/'i','J'/'j' and 'K'/'k' column")
            i_col_index = value_df.columns.get_loc("I" if "I" in value_df.columns else "i")
            j_col_index = value_df.columns.get_loc("J" if "J" in value_df.columns else "j")
            k_col_index = value_df.columns.get_loc("K" if "K" in value_df.columns else "k")
            for row in value_df.values:
                i_verified, new_row_i = self.__verify_row_index_and_shift_to_array(row[i_col_index], self.__i, self.object_extent.i)
                j_verified, new_row_j = self.__verify_row_index_and_shift_to_array(row[j_col_index], self.__j, self.object_extent.j)
                k_verified, new_row_k = self.__verify_row_index_and_shift_to_array(row[k_col_index], self.__k, self.object_extent.k)
                if i_verified and j_verified and k_verified:
                    array[0] = row[value_col_index]

        else:
            raise exceptions.PythonToolException("Not implemented error")

        self.set(array)

    def __verify_row_index_and_shift_to_array(self, row_value, dim, object_extent):
        if dim is None:
            if row_value < 0 or row_value >= object_extent:
                return False, row_value
        if isinstance(dim, int):
            if row_value != dim:
                return False, row_value
        if isinstance(dim, tuple):
            if row_value < dim[0] or row_value > dim[1]:  
                return False, row_value
            else:
                return True, row_value - dim[0]
        return True, row_value

    def __set_values(self, values):
        if self.__readonly:
            raise exceptions.PythonToolException("Chunk is readonly")

        if self.__is_backing_discrete():
            import numpy as np
            values_np = np.array(values)
            if not (values_np % 1 == 0).all():
                raise ValueError("Must supply integers to a chunk of a discrete property")

        try:
            func = self.__value_setters[self._type]
        except KeyError:
            raise NotImplementedError(
                "cannot access backing data " + "for type of chunk"
            )

        i = self.__i
        j = self.__j
        k = self.__k

        if not self.__disconnected:
            func(i, j, k, self.__checked(values))
            self.__cached = None
        else:
            vals = self.__checked(values)
            self.__cached = vals

    def __irange(self):
        if self.__value_enumerations[0] is False:
            return [None]

        if type(self.__i) is tuple:
            return range(self.__i[0], self.__i[1] + 1)

        if self.__i is None:
            return range(0, self.object_extent.i)
        else:
            return range(self.__i, self.__i + 1)

    def __jrange(self):
        if self.__value_enumerations[1] is False:
            return [None]

        if type(self.__j) is tuple:
            return range(self.__j[0], self.__j[1] + 1)

        if self.__j is None:
            return range(0, self.object_extent.j)
        else:
            return range(self.__j, self.__j + 1)

    def __krange(self):
        if self.__value_enumerations[2] is False:
            return [None]

        if type(self.__k) is tuple:
            return range(self.__k[0], self.__k[1] + 1)

        if self.__k is None:
            return range(0, self.object_extent.k)
        else:
            return range(self.__k, self.__k + 1)

    def __is_chunk(self):
        return (
            self._type == ChunkType.chunk
        )  # TODO maybe check for tuple-ness in __i, __j, __k?

    def __start_idx(self, axis_prop):
        if axis_prop is None:
            return 0
        if type(axis_prop) is not tuple:
            raise ValueError("Expects None or tuple")
        return axis_prop[0]

    def __make_accessor(self, i, j, k):
        """Returns an accessor object suitable for passing to a
        C# multidimensional array accessor __getitem__"""
        # IronPython multi-dimensional arrays have a strange
        # __getitems__ behaviour: whereas CPython accepts tuples (and
        # the IronPython source code indicates that it should too), it
        # actually demands a C# object[].  To whit, [i, j, k] syntax
        # desugars successfully but not __getitem__((i, j, k)).

        try:
            func = self.__value_accessors[self._type]
        except KeyError:
            raise NotImplementedError(
                "cannot get value accessors " + "for type of chunk"
            )

        if not self.__is_chunk():
            return func(i, j, k)
        else:
            return func(
                i - self.__start_idx(self.__i),
                j - self.__start_idx(self.__j),
                k - self.__start_idx(self.__k),
            )

    def __values(self):
        # returns the value array for this chunk lazily.
        if self.__cached is None:
            try:
                func = self.__value_getters[self._type]
            except KeyError:
                raise NotImplementedError(
                    "cannot access backing data " + "for type of chunk"
                )

            i = self.__i
            j = self.__j
            k = self.__k

            self.__cached = func(i, j, k)

        return self.__cached

# for backwards compatability
Slice = Chunk
