# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import typing
from cegalprizm.pythontool.exceptions import PythonToolException
from cegalprizm.pythontool.experimental import experimental_method
import math
from cegalprizm.pythontool import chunk
from cegalprizm.pythontool.petrelobject import PetrelObject
from cegalprizm.pythontool.primitives import Extent
from cegalprizm.pythontool import primitives
from cegalprizm.pythontool.chunktype import ChunkType
from cegalprizm.pythontool import _utils
import cegalprizm.pythontool

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.horizoninterpretation_grpc import HorizonInterpretationGrpc, HorizonProperty3dGrpc, HorizonInterpretation3dGrpc


class HorizonInterpretation(PetrelObject):
    """A class holding information about a Horizon Interpretation"""
    def __init__(self, python_petrel_property: "HorizonInterpretationGrpc"):
        super(HorizonInterpretation, self).__init__(python_petrel_property)
        self._extent = None
        self._horizoninterpretation_object_link = typing.cast("HorizonInterpretationGrpc", python_petrel_property)

    @property
    def horizon_interpretation_3ds(self) -> typing.List["HorizonInterpretation3d"]:
        return [HorizonInterpretation3d(po) for po in self._horizoninterpretation_object_link.GetHorizonInterpretation3dObjects()]

    def __str__(self) -> str:
        """A readable representation of the HorizonInterpretation3D"""
        return 'HorizonInterpretation(petrel_name="{0}")'.format(self.petrel_name)

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "HorizonInterpretation":
        return typing.cast("HorizonInterpretation", self._clone(name_of_clone, copy_values = copy_values))

class HorizonProperty3d(PetrelObject):
    def __init__(self, python_petrel_property: "HorizonProperty3dGrpc"):
        super(HorizonProperty3d, self).__init__(python_petrel_property)
        self._extent: typing.Optional[Extent] = None
        self._horizonproperty3d_object_link = python_petrel_property
        
    @property
    def extent(self) -> Extent:
        """The number of nodes in the i and j directions

        Returns:
            A :class:`cegalprizm.pythontool.Extent` object
        """
        if self._extent is None:
            i = self._horizonproperty3d_object_link.NumI()
            j = self._horizonproperty3d_object_link.NumJ()
            self._extent = Extent(i=i, j=j, k=1)

        return self._extent

    def indices(self, x: float, y: float) -> primitives.Indices:
        """The indices of the node nearest the specified point

        Please note: the node indices are 0-based, but in the Petrel
        UI they are 1-based.

        Args:
            x: the x-coordinate
            y: the y-coordinate

        Returns: A :class:`cegalprizm.pythontool.primitives.Indices` object
            representing the indices of the node nearest the point.
            `K` will always be `None`.

        Raises:

            ValueError: if the point is outside the beyond the extent
                        of the surface

        """
        index2 = self._horizonproperty3d_object_link.IndexAtPosition(x, y)
        if index2 is None:
            raise ValueError("position not in surface")
        if (
            index2 is None
            or index2.GetValue().I < 0
            or index2.GetValue().J < 0
            or index2.GetValue().I >= self.extent.i
            or index2.GetValue().J >= self.extent.j
        ):
            raise ValueError("position not in surface")
        return primitives.Indices(index2.GetValue().I, index2.GetValue().J, None)

    def position(self, i: int, j: int) -> primitives.Point:
        """The position of the node

        Args:
            i: the i-index of the node
            j: the j -index of the node

        Returns: A :class:`cegalprizm.pythontool.Point` object
            representing the position of the node.

        Raises:
            ValueError: if the indices are outside the surface
        """
        point3 = self._horizonproperty3d_object_link.PositionAtIndex(i, j)
        if point3 is None:
            raise ValueError("index not valid for surface")
        return primitives.Point(
            point3.GetValue().X, point3.GetValue().Y, point3.GetValue().Z
        )

    def is_undef_value(self, value: typing.Union[float, int]) -> bool:
        """Whether the value is the 'undefined value' for the attribute

        Petrel represents some undefined values by ``MAX_INT``, others
        by ``NaN``.  A comparison with ``NaN`` will always return
        ``False`` (e.g. ``float.nan != float.nan``) so it is
        preferable to always use this method to test for undefined
        values.

        Args:
            value: the value to test

        Returns:
            bool: True if value is 'undefined' for this surface
            attribute

        """
        return self._is_undef_value(value)

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "HorizonProperty3d":
        """ Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.

        This is a Python Tool Pro function and is not available when running scripts in the editor integrated in Python Tool or in a workflow.
        
        Args:
            path_of_clone: Petrel name of the clone
            copy_values: Set to True if values shall be copied into the clone. Defaults to False.

        Returns:
            cegalprizm.pythontool.HorizonProperty3d: the cloned HorizonProperty3d object
           
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("HorizonProperty3d",self._clone(name_of_clone, copy_values = copy_values))
   

    def _is_undef_value(self, value: typing.Union[float, int]) -> bool:
        return math.isnan(value)

    @property
    def undef_value(self) -> float:
        """The 'undefined value' for this attribute

        Use this value when setting a slice's value to 'undefined'.
        Do not attempt to test for undefinedness by comparing with
        this value, use :meth:`is_undef_value` instead.

        Returns:
           The 'undefined value' for this attribute
        """
        return self._undef_value()

    def _undef_value(self) -> float:
        return float("nan")

    @property
    def unit_symbol(self) -> typing.Optional[str]:
        """The symbol for the unit which the values are measured in

        Returns:

            string: The symbol for the unit, or None if no unit is used
        """
        return self._unit_symbol()

    def _unit_symbol(self) -> typing.Optional[str]:
        return _utils.str_or_none(self._horizonproperty3d_object_link.GetDisplayUnitSymbol())

    def all(self) -> chunk.Chunk:
        """Creates a :class:`cegalprizm.pythontool.Chunk` with the values for the attribute

        Returns:
            cegalprizm.pythontool.Chunk:  A `Slice` containing the values for the attribute
        """
        return self._make_chunk(i=None, j=None)

    def chunk(self, i: typing.Optional[typing.Tuple[int, int]] = None, j: typing.Optional[typing.Tuple[int, int]] = None) -> chunk.Chunk:
        """Creates a :class:`cegalprizm.pythontool.Chunk` with the values for the attribute

        Args:
            i: A tuple(i1,i2) where i1 is the start index and i2 is the end index. 
                The start and end value in this range is inclusive. If None include all i values.
            j: A tuple(j1,j2) where j1 is the start index and j2 is the end index. 
                The start and end value in this range is inclusive. If None include all j values.

        Returns:
            cegalprizm.pythontool.Chunk:  A `Slice` containing the values for the attribute
        """
        return self._make_chunk(i=i, j=j)

    def _make_chunk(self, i=None, j=None) -> "cegalprizm.pythontool.Chunk":
        value_getters = {
            ChunkType.k: lambda i, j, k: _utils.from_backing_arraytype(
                self._horizonproperty3d_object_link.GetChunk(i, j)
            )
        }
        value_setters = {
            ChunkType.k: lambda i, j, k, values: self._horizonproperty3d_object_link.SetChunk(
                i, j, _utils.to_backing_arraytype(values)
            )
        }
        value_shapers = {
            ChunkType.k: lambda i, j, k, values: _utils.ensure_2d_float_array(
                values, i, j
            )
        }
        value_accessors = {ChunkType.k: lambda i, j, k: _utils.native_accessor((i, j))}

        return cegalprizm.pythontool.Chunk(
            i,
            j,
            None,
            self,
            self.extent,
            value_getters,
            value_setters,
            value_shapers,
            value_accessors,
            (True, True, False),
            ChunkType.k,
            readonly=self.readonly,
        )

    def __str__(self) -> str:
        """A readable representation of the HorizonInterpretation3D"""
        return 'HorizonProperty3D(petrel_name="{0}")'.format(self.petrel_name)

    @experimental_method
    def positions_to_ijks(self, positions: typing.Union[typing.Tuple[typing.List[float], typing.List[float]], typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]])\
            -> typing.Tuple[typing.List[float], typing.List[float]]:
        """Converts a list of xyzs to ijk

        Args:
            positions: A tuple([x],[y]) where [x] is a list of x coordinates 
              and [y] is a list of y coordinates.

        Returns:
            A tuple([i],[j]) where [i] is a list of i indices
              and [j] is a list of j indices.
        """ 
        if len(positions) == 2:
            positions = typing.cast(typing.Tuple[typing.List[float], typing.List[float]], positions)
            [x, y] = positions
        elif len(positions) == 3:
            positions = typing.cast(typing.Tuple[typing.List[float], typing.List[float], typing.List[float]], positions)
            [x, y, _] = positions
        lst_is = []
        lst_js = []
        n = 1000
        for i in range(0, len(x), n):
            data = self._horizonproperty3d_object_link.GetIjk(x[i:i+n], y[i:i+n])
            lst_is.append(data[0])
            lst_js.append(data[1])
        d = ([i for i_s in lst_is for i in i_s ], 
            [j for js in lst_js for j in js ])
        return d

    @experimental_method
    def ijks_to_positions(self, indices: typing.Tuple[typing.List[float], typing.List[float]])\
            -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        """Converts a list with i and j indices to xyz.


        Args:
            indices: A tuple([i],[j]) where [i] is a list of i indices
              and [j] is a list of j indices.

        Returns:
            A tuple([x],[y],[z]) where [x] is a list of x coordinates, 
             [y] is a list of y coordinates and [z] is a list of z coordinates.
        """       
        extent = self.extent
        for i_, j_ in zip(*indices[:2]):
            if i_ < 0 or j_ < 0 :
                raise PythonToolException("Index cannot be less than zero")
            if i_ >= extent.i or j_ >= extent.j:
                raise PythonToolException("Index cannot be greater than object extent")
        
        [i, j] = indices[:2]
        lst_x = []
        lst_y = []
        lst_z = []
        n = 1000
        for i_ in range(0, len(i), n):
            data = self._horizonproperty3d_object_link.GetPositions(i[i_:i_+n], j[i_:i_+n])
            lst_x.append(data[0])
            lst_y.append(data[1])
            lst_z.append(data[2])

        d = ([i for i_s in lst_x for i in i_s ], 
            [j for js in lst_y for j in js ], 
            [k for ks in lst_z for k in ks ])
        return d

    @property
    def horizon_interpretation_3d(self) -> "HorizonInterpretation3d":
        """The parent 3d horizon interpretation of the horizon property.

        Returns:
            cegalprizm.pythontool.HorizonInterpretation3d: The parent grid of the property
        """   
        return HorizonInterpretation3d(self._horizonproperty3d_object_link.GetParentHorizonInterpretation3d())

class HorizonInterpretation3d(HorizonProperty3d):
    def __init__(self, python_petrel_property: "HorizonInterpretation3dGrpc"):
        super(HorizonInterpretation3d, self).__init__(python_petrel_property)
        self._extent = None
        self._horizoninterpretation3d_object_link = python_petrel_property
        
    def __str__(self) -> str:
        """A readable representation of the HorizonInterpretation3d"""
        return 'HorizonInterpretation3D(petrel_name="{0}")'.format(self.petrel_name)

    @property
    def sample_count(self) -> int:
        """The number of samples contained in the Horizon Interpretation 3d object.

        Returns:
            int: The number of points in the interpretation.
        """        
        return self._horizoninterpretation3d_object_link.SampleCount()

    @property
    def horizon_interpretation(self) -> HorizonInterpretation:
        """Returns the parent Horizon interpretation of the 3d horizon interpretation grid."""            
        return HorizonInterpretation(self._horizoninterpretation3d_object_link.GetParent())

    @property
    def horizon_property_3ds(self) -> typing.List[HorizonProperty3d]:
        """A readonly iterable collection of the 3d horizon interpretation properties for the 3d horizon interpretation grid 
        
        Returns:
            cegalprizm.pythontool.HorizonProperties:the 3d horizon interpretation properties
              for the 3d horizon interpretation grid"""
        return [
            HorizonProperty3d(po)
            for po in self._horizoninterpretation3d_object_link.GetAllHorizonPropertyValues()
        ]
