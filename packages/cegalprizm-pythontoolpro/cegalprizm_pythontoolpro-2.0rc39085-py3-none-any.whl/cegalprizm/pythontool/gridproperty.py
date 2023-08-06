# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import typing
from warnings import warn
from cegalprizm.pythontool.petrelobject import PetrelObject
from cegalprizm.pythontool._toolmode import _ToolMode

import math

from cegalprizm.pythontool.chunk import Chunk
from cegalprizm.pythontool import grid
from cegalprizm.pythontool import _utils
from cegalprizm.pythontool import exceptions
from cegalprizm.pythontool import primitives
from datetime import datetime
from cegalprizm.pythontool.chunktype import ChunkType

from cegalprizm.pythontool._system import _system

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.gridproperty_grpc import GridDiscretePropertyGrpc, GridPropertyGrpc, PropertyCollectionGrpc
    from cegalprizm.pythontool.grid import Grid

class GridProperty(PetrelObject):
    def __init__(self, petrel_object_link: "GridPropertyGrpc"):
        super(GridProperty, self).__init__(petrel_object_link)
        self._gridproperty_object_link = petrel_object_link
        

    @property
    def parent_grid(self) -> None:
        """DeprecationWarning: 'parent_grid' has been removed. Use 'grid' instead
        """
        warn("'parent_grid' has been removed. Use 'grid' instead", 
             DeprecationWarning, stacklevel=2)
        raise RuntimeError("'parent_grid' has been removed. Use 'grid' instead")

    @property
    def grid(self) -> grid.Grid:
        """The parent grid of the property

        Returns:
            cegalprizm.pythontool.Grid: The parent grid of the property
        """
        return grid.Grid(self._gridproperty_object_link.GetParentPythonGridObject())

    @property
    def date(self) -> typing.Optional[datetime]:
        """The date and time recorded for the property

        Returns:
            datetime: The datetime recorded, or `None` if not used"""
        raw_date = self._gridproperty_object_link.GetDate()
        if _ToolMode.is_oop():
            return raw_date

        if raw_date is None:
            return None       
        return _utils.to_python_datetime(raw_date)

    def is_undef_value(self, value: typing.Union[float, int]) -> bool:
        """Whether the value is the 'undefined' value for the property

        Petrel represents some undefined values by ``MAX_INT``, others
        by ``NaN``.  A comparison with ``NaN`` will always return
        ``False`` (e.g. ``float.nan != float.nan``) so it is
        preferable to always use this method to test for undefined
        values.

        Args:
            value: The value to test if it is 'undefined' in Petrel

        Returns:
            bool: True if the value is 'undefined' for this property
        """        
        return self._is_undef_value(value)

    @property
    def undef_value(self) -> float:
        """The 'undefined value' for this property

        Use this value when setting a slice's value to 'undefined'.
        Do not attempt to test for undefined value by comparing with
        this value, use :meth:`is_undef_value` instead.

        Returns:
           The 'undefined value' for this property
        """
        return self._undef_value()

    @property
    def unit_symbol(self) -> typing.Optional[str]:
        """Returns the symbol of the object unit, None if template of object is unitless."""
        return self._unit_symbol()

    @property
    def upscaled_cells(self) -> typing.List[primitives.Indices]:
        """Get/set the cell indices of values which have been upscaled

        **Example:**

        .. code-block:: Python

            myproperty.upscaled_cells = [Indices(20, 24, 5), Indices(20, 24, 6)]
            print(len(myproperty.upscaled_cells))
            # outputs '2'

        Returns:
            List: a list of `cegalprizm.pythontool.Indices` of the upscaled cells
        """
        tuples = self._gridproperty_object_link.GetUpscaledCells()
        return [primitives.Indices(tup.Item1, tup.Item2, tup.Item3) for tup in tuples]

    @upscaled_cells.setter
    def upscaled_cells(self, cells: typing.List[primitives.Indices]):
        if self.readonly:
            raise exceptions.PythonToolException("GridProperty is readonly")
        if cells is None:
            cells = []
        num = len(cells)
        if _ToolMode.is_oop():
            ii = [int(0)] * num
            jj = [int(0)] * num
            kk = [int(0)] * num
        else:
            ii = _system().Array.CreateInstance(int, num)
            jj = _system().Array.CreateInstance(int, num)
            kk = _system().Array.CreateInstance(int, num)
        
        for i, cell in enumerate(cells):
            ii[i] = cell.i
            jj[i] = cell.j
            kk[i] = cell.k
        self._gridproperty_object_link.SetUpscaledCells(ii, jj, kk)

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "GridProperty":
        """Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.

        This is a Python Tool Pro function and is not available when running scripts in the editor integrated in Python Tool or in a workflow.

        Args:
            name_of_clone: Petrel name of the clone
            copy_values: Set to True if values shall be copied into the clone. Defaults to False.
        
        Returns:
            cegalprizm.pythontool.GridProperty: the cloned GridProperty object
        
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """        
        return typing.cast("GridProperty", self._clone(name_of_clone, copy_values = copy_values))

    def _unit_symbol(self) -> typing.Optional[str]:
        return _utils.str_or_none(self._gridproperty_object_link.GetDisplayUnitSymbol())

    def _undef_value(self) -> float:
        return float('nan')

    def _is_undef_value(self, value) -> bool:
        return math.isnan(value)

    def _make_chunk(self, i=None, j=None, k=None) -> "Chunk":
        value_getters = {ChunkType.ij:
                         lambda i, j, k: _utils.from_backing_arraytype(self._gridproperty_object_link.GetColumn(i, j)),
                         ChunkType.k:
                         lambda i, j, k: _utils.from_backing_arraytype(self._gridproperty_object_link.GetLayer(k)),
                         ChunkType.none:
                         lambda i, j, k: _utils.from_backing_arraytype(self._gridproperty_object_link.GetAll()),
                         ChunkType.chunk:
                         lambda i, j, k: _utils.from_backing_arraytype(self._gridproperty_object_link.GetChunk(i, j, k))}
        value_setters = {ChunkType.ij:
                         lambda i, j, k, values: self._gridproperty_object_link.SetColumn(i, j, _utils.to_backing_arraytype(values)),
                         ChunkType.k:
                         lambda i, j, k, values: self._gridproperty_object_link.SetLayer(k, _utils.to_backing_arraytype(values)),
                         ChunkType.none:
                         lambda i, j, k, values: self._gridproperty_object_link.SetAll(_utils.to_backing_arraytype(values)),
                         ChunkType.chunk:
                         lambda i, j, k, values: self._gridproperty_object_link.SetChunk(i, j, k, _utils.to_backing_arraytype(values))}
        value_shapers = {ChunkType.ij:
                         lambda i, j, k, values: _utils.ensure_1d_float_array(values, k),
                         ChunkType.k:
                         lambda i, j, k, values: _utils.ensure_2d_float_array(values, i, j),
                         ChunkType.none:
                         lambda i, j, k, values: _utils.ensure_3d_float_array(values, i, j, k),
                         ChunkType.chunk:
                         lambda i, j, k, values: _utils.ensure_3d_float_array(values, i, j, k)}
        value_accessors = {ChunkType.ij:
                           lambda i, j, k: k,
                           ChunkType.k:
                           lambda i, j, k:  _utils.native_accessor((i, j)),
                           ChunkType.none:
                           lambda i, j, k: _utils.native_accessor((i, j, k)),
                           ChunkType.chunk:
                           lambda i, j, k: _utils.native_accessor((i, j, k))}
        return Chunk(i, j, k,
                           self,
                           self.grid.extent,
                           value_getters,
                           value_setters,
                           value_shapers,
                           value_accessors,
                           (True, True, True),
                           readonly=self.readonly)

    def all(self) -> Chunk:
        """Creates a :class:`cegalprizm.pythontool.Chunk` with the values for the property

        Returns:
            cegalprizm.pythontool.Chunk:  A `Chunk` containing the values for the property
        """
        return self._make_chunk(i=None, j=None, k=None)

    def chunk(self,
            irange: typing.Tuple[int, int],
            jrange: typing.Tuple[int, int],
            krange: typing.Tuple[int, int])\
            -> Chunk:
        """Creates a :class:`cegalprizm.pythontool.Chunk` with the values for the specified ranges

        Args:
            i: inclusive range in the i-direction
            j: inclusive range in the j-direction
            k: inclusive range in the k-direction

        Returns:
            cegalprizm.pythontool.Chunk: A `Chunk` containing the values for all layers

        Raises:
            ValueError: if the ranges specify volumes outside the property's extent
        """
        return self._make_chunk(i=irange, j=jrange, k=krange)

    def column(self, i: int, j: int) -> Chunk:
        """Creates a :class:`cegalprizm.pythontool.Chunk` with the values for the specified column

        Args:
            i: the index in the i-direction
            j: the index in the j-direction

        Returns:
            cegalprizm.pythontool.Chunk: A `Chunk` containing the values for all layers

        Raises:
            ValueError: if the property does not have the column specified
        """
        return self._make_chunk(i=i, j=j)

    def layer(self, k: int) -> Chunk:
        """Creates a :class:`cegalprizm.pythontool.Chunk` with the values for the specified layer

        Args:
            k: the index in the k-direction (the layer)

        Returns:
            cegalprizm.pythontool.Chunk: A `Chunk` containing the values for the layer

        Raises:
            ValueError: if the property does not have the layer specified
        """
        return self._make_chunk(k=k)

    def __str__(self) -> str:
        """A readable representation of the GridProperty"""
        if self.date is None:
            return "GridProperty(petrel_name=\"{0}\")".format(self.petrel_name)
        else:
            return "GridProperty(petrel_name=\"{0}\", date=\"{1}\")".format(self.petrel_name, self.date)

    def columns(self,
            irange: typing.Tuple[int, int] = None,
            jrange: typing.Tuple[int, int] = None)\
            -> typing.Iterator[Chunk]:
        """Returns a generator of column slices
        
        Args:
            irange: an iterable (e.g list) of i-values to
                generate columns for.  If `None`,
                generate for all i-values
            jrange: an iterable (e.g. list) of j-values to
                generate columns for.  If `None`,
                generate for all j-values.
        
        Yields:
            A generator of column :class:`cegalprizm.pythontool.Chunk` objects covering the
                `irange` and `jrange` passed.

        Raises:
            ValueError: if the indices are invalid.

        **Example**:

        .. code-block:: python

          # sets to 0 all values in the i-slices i=10 through to i=19,
          for col in my_prop.columns(irange=range(10, 20), jrange=None):
              col.set(0)

          # sets to 0 all values in the property
          for col in my_prop.columns():
              col.set(0)        
        """        

        irange_used = irange if irange is not None else range(self.grid.extent.i)
        jrange_used = jrange if jrange is not None else range(self.grid.extent.j)
        for i in irange_used:
            for j in jrange_used:
                yield self.column(i, j)

    def layers(self, krange: typing.Tuple[int, int] = None)\
            -> typing.Iterator[Chunk]:
        """Returns a generator of layer slices
        
        Args:

          krange: an iterable (e.g.) of k-values to
                             generate layers for.  If `None`, generate
                             for all k-values

        Yields:
            A generator of layer :class:`cegalprizm.pythontool.Chunk` objects covering the
            `krange` passed
        
        **Example**:

        .. code-block:: python

          # sets to 0 all values in the k-slices k=10 through to k=19,
          for layer in my_prop.layers(range(10, 20)):
              layer.set(0)

          # sets to 0 all values in the property
          for layer in my_prop.layers():
              layer.set(0)
        """   
        krange_used = krange if krange is not None else range(self.grid.extent.k)
        for k in krange_used:
            yield self.layer(k)


    def has_same_parent(self, other: "GridProperty") -> bool:
        """Tests whether the grid property has the same parent grid

        Args:
            other: the other grid property

        Returns:
            bool: ``True`` if the ``other`` object has the same grid

        Raises:
            ValueError: if ``other`` is not a GridProperty
        """
        if not isinstance(other, GridProperty):
            raise ValueError("can only compare parent with other GridProperty")
        return self.grid._grid_object_link.GetDroidString() == other.grid._grid_object_link.GetDroidString()

    @property
    def parent_collection(self) -> typing.Optional["PropertyCollection"]:
        """The parent collection for the grid property

        Returns:
            cegalprizm.pythontool.PropertyCollection: the parent collection, or `None`"""
        coll = self._gridproperty_object_link.GetParentPropertyCollection()
        if coll is None:
            return None

        return PropertyCollection(coll)


class PropertyCollection(PetrelObject):
    """A readonly collection of a set of grid properties, including both continuous and discrete.

    Although this object wraps a Petrel collection, it does not
    support any operations on it apart from iterating through its
    contents.  It does not support operations to navigate through hierarchies of collections."""
    def __init__(self, petrel_object_link: "PropertyCollectionGrpc"):
        super(PropertyCollection, self).__init__(petrel_object_link)
        self._propertycollection_object_link = petrel_object_link


    @property
    def _continuous_properties(self):
        return [GridProperty(prop) for prop in self._propertycollection_object_link.GetPropertyObjects()]

    @property
    def _discrete_properties(self):
        return [GridDiscreteProperty(prop) for prop in self._propertycollection_object_link.GetDictionaryPropertyObjects()]

    def __str__(self) -> str:
        """A readable representation of the PropertyCollection"""
        return "PropertyCollection(petrel_name=\"{0}\")".format(self.petrel_name)

    def __iter__(self) -> typing.Iterator[typing.Union[GridProperty, "GridDiscreteProperty"]]:
        for p in self._continuous_properties:
            yield p
        for p in self._discrete_properties:
            yield p

    def __len__(self) -> int:
        return len(self._continuous_properties) + len(self._discrete_properties)



class GridDiscreteProperty(GridProperty):

    def __init__(self, petrel_object_link: "GridDiscretePropertyGrpc"):
        super(GridDiscreteProperty, self).__init__(petrel_object_link)
        self._griddiscreeteproperty_object_link = petrel_object_link
        self._discrete_codes = self.__make_discrete_codes_dict()
    
    @property
    def discrete_codes(self) -> typing.Dict[int, str]:

        """A dictionary of discrete codes and values

        Changes to this dictionary will not be persisted or affect any Petrel objects.

        **Example:**

        .. code-block:: Python

            print(my_discreteprop.discrete_codes[1])
            # outputs 'Fine sand'
        """

        return self._discrete_codes

    def _undef_value(self):
        return _system().Int32.MaxValue

    def _is_undef_value(self, value):
        return value == _system().Int32.MaxValue

    def _unit_symbol(self):
        return None

    def __make_discrete_codes_dict(self) -> typing.Dict[int, str]:
        codes = {}
        for tup in self._griddiscreeteproperty_object_link.GetAllDictionaryCodes():
            k = tup.Item1
            v = tup.Item2
            codes[k] = v
        return codes

    def _make_chunk(self, i=None, j=None, k=None):
        value_getters = {ChunkType.ij:
                         lambda i, j, k: _utils.from_backing_arraytype(self._griddiscreeteproperty_object_link.GetColumn(i, j)),
                         ChunkType.k:
                         lambda i, j, k: _utils.from_backing_arraytype(self._griddiscreeteproperty_object_link.GetLayer(k)),
                         ChunkType.none:
                         lambda i, j, k: _utils.from_backing_arraytype(self._griddiscreeteproperty_object_link.GetAll()),
                         ChunkType.chunk:
                         lambda i, j, k: _utils.from_backing_arraytype(self._griddiscreeteproperty_object_link.GetChunk(i, j, k))}
        value_setters = {ChunkType.ij:
                         lambda i, j, k, values: self._griddiscreeteproperty_object_link.SetColumn(i, j, _utils.to_backing_arraytype(values)),
                         ChunkType.k:
                         lambda i, j, k, values: self._griddiscreeteproperty_object_link.SetLayer(k, _utils.to_backing_arraytype(values)),
                         ChunkType.none:
                         lambda i, j, k, values: self._griddiscreeteproperty_object_link.SetAll(_utils.to_backing_arraytype(values)),
                         ChunkType.chunk:
                         lambda i, j, k, values: self._griddiscreeteproperty_object_link.SetChunk(i, j, k, _utils.to_backing_arraytype(values))}
        value_shapers = {ChunkType.ij:
                         lambda i, j, k, values: _utils.ensure_1d_int_array(values, k),
                         ChunkType.k:
                         lambda i, j, k, values: _utils.ensure_2d_int_array(values, i, j),
                         ChunkType.none:
                         lambda i, j, k, values: _utils.ensure_3d_int_array(values, i, j, k),
                         ChunkType.chunk:
                         lambda i, j, k, values: _utils.ensure_3d_int_array(values, i, j, k)}
        value_accessors = {ChunkType.ij:
                           lambda i, j, k: k,
                           ChunkType.k:
                           lambda i, j, k:  _utils.native_accessor((i, j)),
                           ChunkType.none:
                           lambda i, j, k: _utils.native_accessor((i, j, k)),
                           ChunkType.chunk:
                           lambda i, j, k: _utils.native_accessor((i, j, k))}
        return Chunk(i, j, k,
                           self,
                           self.grid.extent,
                           value_getters,
                           value_setters,
                           value_shapers,
                           value_accessors,
                           (True, True, True),
                           readonly=self.readonly)

    def __str__(self) -> str:
        """A readable representation of the GridDiscreteProperty"""
        if self.date is None:
            return "GridDiscreteProperty(petrel_name=\"{0}\")".format(self.petrel_name)
        else:
            return "GridDiscreteProperty(petrel_name=\"{0}\", date=\"{1}\")".format(self.petrel_name, self.date)

class GridProperties(object):
    """An iterable collection of :class:`cegalprizm.pythontool.GridProperty` and :class:`cegalprizm.pythontool.GridDiscreteProperty`
    objects for the grid properties and discrete grid properties belonging to this grid."""

    def __init__(self, grid: "Grid"):
        self._grid = grid

    def __iter__(self) -> typing.Iterator[typing.Union[GridProperty, GridDiscreteProperty]]:
        for p in self._grid._get_grid_properties():
            yield p
    
    def __getitem__(self, idx) -> typing.Union[GridProperty, GridDiscreteProperty]:
        gp = [item for item in self._grid._get_grid_properties()]
        return gp[idx] # type: ignore

    def __len__(self) -> int:
        return self._grid._get_number_of_grid_properties()

    def __str__(self) -> str:
        return 'GridProperties(grid="{0}")'.format(self._grid)

    @property
    def readonly(self) -> bool:
        return self._grid.readonly

