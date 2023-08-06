# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import typing
from cegalprizm.pythontool.experimental import experimental_method
from cegalprizm.pythontool.petrelobject import PetrelObject
from cegalprizm.pythontool import gridproperty
from cegalprizm.pythontool import primitives
from cegalprizm.pythontool.exceptions import PythonToolException

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.grid_grpc import GridGrpc

class Grid(PetrelObject):
    def __init__(self, petrel_object_link: "GridGrpc"):
        super(Grid, self).__init__(petrel_object_link)

        self._grid_object_link = petrel_object_link
        self.__extent: typing.Optional[primitives.Extent] = None

    @property
    def extent(self) -> primitives.Extent:        
        """The number of cells in the i, j and k directions

        Returns:
            cegalprizm.pythontool.Extent: The number of cells in each direction
        """
        if self.__extent is None:
            i = self._grid_object_link.NumI()
            j = self._grid_object_link.NumJ()
            k = self._grid_object_link.NumK()
            self.__extent = primitives.Extent(i=i, j=j, k=k)

        return self.__extent

    def __str__(self) -> str:
        """A readable representation of the Grid"""
        return "Grid(petrel_name=\"{0}\")".format(self.petrel_name)

    def indices(self, x: float, y: float, z: float) -> primitives.Indices:
        """The indices of a cell containing the specified point

        Note that due to rounding errors and the way a pillar grid is
        defined, more than one cell might contain a given point; only
        one set of indices is ever returned.

        Args:
            x: the x-coordinate
            y: the y-coordinate
            z: the z-coordinate

        Returns:
            cegalprizm.pythontool.Indices: object representing the indices of the cell 
                containing the xyz coordinates

        Raises:
            ValueError: if no cell contains the specified point        
        """       

        index3 = self._grid_object_link.GetCellAtPoint(x, y, z)
        if index3 is None:
            raise ValueError("position not in grid")
        return primitives.Indices(index3.GetValue().I, index3.GetValue().J, index3.GetValue().K)

    def position(self, i: int, j: int, k: int) -> primitives.Point:
        """The XYZ position of the cell center in the Petrel coordinate system 

        Args:
            i: the i-index
            j: the j-index
            k: the k-index

        Returns:
            cegalprizm.pythontool.Point: The XYZ position of the cell center 
                in the Petrel coordinate system 

        Raises:
            ValueError: if the indices are invalid for the grid
        """
        point3 = self._grid_object_link.GetCellCenter(i, j, k)
        if point3 is None:
            raise ValueError("indices not in grid")
        return primitives.Point(point3.GetValue().X, point3.GetValue().Y, point3.GetValue().Z)

    def vertices(self, i: int, j: int, k: int) -> typing.List[primitives.Point]:
        """The positions of the vertices of the cell.

        Use :func:`vertices_unchecked` if you do not wish to spend
        time checking if the cell is defined.  In that case, the
        method will return an list of undefined points.

        See :class:`cegalprizm.pythontool.vertices` for how to query
        the returned list for specific vertices.

        Args:
            i: the i-index
            j: the j-index
            k: the k-index

        

        Returns:
            A list of :class:`cegalprizm.pythontool.Point` objects.
        
        Raises:
            ValueError: if the cell is undefined or outside of the grid
        """        

        points = self._grid_object_link.GetCellCorners(i, j, k)
        if points is None:
            raise ValueError("indices not in grid")
        if self.is_undef_cell(i, j, k):
            raise ValueError("cell is undefined")
        return [primitives.Point(pt.X, pt.Y, pt.Z) for pt in points.GetValue()]

    def vertices_unchecked(self, i: int, j: int, k: int) -> typing.List[primitives.Point]:
        """The positions of the vertices of the cell

        See :class:`cegalprizm.pythontool.vertices` for how to query
        the returned list for specific vertices.

        If the cell is not defined, a list of undefined points (where
        x, y and z are equal to NaN) will be returned.  (Use
        :func:`vertices` to check for undefined cells).

        Args:
            i: the i-index
            j: the j-index
            k: the k-index

        Returns:
            A list of :class:`cegalprizm.pythontool.Point` objects.
        
        Raises:
            ValueError: if the cell outside of the grid
        """        

        points = self._grid_object_link.GetCellCorners(i, j, k)
        if points is None:
            raise ValueError("indices not in grid")
        return [primitives.Point(pt.X, pt.Y, pt.Z) for pt in points.GetValue()]

    def is_undef_cell(self, i: int, j: int, k: int) -> bool:
        """Checks if the cell with given i,j and k index is undefined

        Args:
            i: the i-index
            j: the j-index
            k: the k-index

        Returns:
            bool: ``True`` if the cell is undefined at the indices specified
        """        

        return not self._grid_object_link.IsCellDefined(i, j, k)

    @property
    def coords_extent(self) -> primitives.CoordinatesExtent:
        """The extent of the object in world-coordinates

        Returns:

            cegalprizm.pythontool.CoordinatesExtent: the extent of the object in world-coordinate
        """
        return primitives.CoordinatesExtent(self._grid_object_link.AxesRange())

    @experimental_method
    def positions_to_ijks(self, 
            positions: typing.Tuple[typing.List[float], typing.List[float], typing.List[float]])\
            -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:            
        """Converts a tuple with xyzs to ijk

        Args:
            positions: A tuple([x], [y], [z]), where [x] is a list of x coordinates, 
                [y] is a list of y positions and [z] is a list of z (time/depth) coordinates.
            

        Returns:
            A tuple([i],[j],[k]) where [i] is a list of i indices, [j] is a list of j indices
                and [k] is a list of k indices.
        """         
        [x, y, z] = positions
        lst_is = []
        lst_js = []
        lst_ks = []
        n = 1000
        for i in range(0, len(x), n):
            data = self._grid_object_link.GetIjk(x[i:i+n], y[i:i+n], z[i:i+n])
            lst_is.append(data[0])
            lst_js.append(data[1])
            lst_ks.append(data[2])
        d = ([i for i_s in lst_is for i in i_s ], 
            [j for js in lst_js for j in js ], 
            [k for ks in lst_ks for k in ks ])
        return d

    @experimental_method
    def ijks_to_positions(self, 
            indices: typing.Tuple[typing.List[float], typing.List[float], typing.List[float]])\
            -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        """Converts a tuple with ijk indices to xyz.


        Args:
            indices: A tuple([i],[j],[k]) where [i] is a list of i indices, [j] is a list of j indices
                and [k] is a list of k indices.
                
            

        Returns:
            A tuple([x], [y], [z]), where [x] is a list of x coordinates, 
                [y] is a list of y positions and [z] is a list of z (time/depth) coordinates.
        """
        extent = self.extent
        for i_, j_, k_ in zip(*indices):
            if i_ < 0 or j_ < 0 or k_ < 0:
                raise PythonToolException("Index cannot be less than zero")
            if i_ >= extent.i or j_ >= extent.j or k_ >= extent.k:
                raise PythonToolException("Index cannot be greater than object extent")

        [i, j, k] = indices
        lst_x = []
        lst_y = []
        lst_z = []
        n = 1000
        for i_ in range(0, len(i), n):
            data = self._grid_object_link.GetPositions(i[i_:i_+n], j[i_:i_+n], k[i_:i_+n])
            lst_x.append(data[0])
            lst_y.append(data[1])
            lst_z.append(data[2])

        d = ([i for i_s in lst_x for i in i_s ], 
            [j for js in lst_y for j in js ], 
            [k for ks in lst_z for k in ks ])
        return d

    @property
    def properties(self) -> "gridproperty.GridProperties":        
        """A readonly iterable collection of the grid properties for the grid
        
        Returns: 
            a list of the grid properties (continuous and discrete)
        """
        return gridproperty.GridProperties(self)

    def _get_number_of_grid_properties(self) -> int:
        return self._grid_object_link.GetNumberOfGridProperties()

    def _get_grid_properties(self) -> typing.Iterable[typing.Union["gridproperty.GridProperty", "gridproperty.GridDiscreteProperty"]]:
        props = [gridproperty.GridProperty(p) for p in self._grid_object_link.GetProperties()]
        d_props = [gridproperty.GridDiscreteProperty(dp) for dp in self._grid_object_link.GetDictionaryProperties()]
        return props + d_props

