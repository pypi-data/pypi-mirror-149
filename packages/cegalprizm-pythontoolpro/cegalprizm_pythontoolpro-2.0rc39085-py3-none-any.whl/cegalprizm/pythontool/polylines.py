# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import typing
from warnings import warn

from contextlib import contextmanager
from cegalprizm.pythontool.petrelobject import PetrelObject
from cegalprizm.pythontool import primitives
from cegalprizm.pythontool import exceptions
from cegalprizm.pythontool._toolmode import _ToolMode
from cegalprizm.pythontool._system import _system

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.polylines_grpc import PolylineSetGrpc

class PolylinePoint(object):
    def __init__(self, polyline: "Polyline", index: int):
        self._polyline = polyline
        self._index = index

    def __eq__(self, other) -> bool:
        try:
            return other.x == self.x and other.y == self.y and other.z == self.z # type: ignore
        except:
            return False

    @property
    def x(self) -> float:
        """Returns the x coordinate of the point as a float.
        """
        return self._polyline.positions()[0][self._index]

    @property
    def y(self) -> float:
        """Returns the y coordinate of the point as a float.
        """
        return self._polyline.positions()[1][self._index]

    @property
    def z(self) -> float:
        """Returns the z coordinate of the point as a float.
        """
        return self._polyline.positions()[2][self._index]

class Polyline(object):
    """Represents a single polyline in a
    :class:`cegalprizm.pythontool.PolylineSet` object.

    It is an iterable, returning :class:`cegalprizm.pythontool.PolylinePoint` objects.
    """

    def __init__(self, polyline_set: "PolylineSet", polyline_index: int):
        self._polyline_set = polyline_set
        self._polyline_index = polyline_index

        self._position_array: typing.Optional[typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]] = None
        self._point_count: typing.Optional[int] = None
        self._points_cache: typing.Optional[typing.List[typing.Union[primitives.Point, PolylinePoint]]] = None

    def _load_points_cache(self) -> typing.List[typing.Union[PolylinePoint, primitives.Point]]:
        self._position_array = self._polyline_set.get_positions(self._polyline_index)
        self._point_count = len(self._position_array[0])
        self._points_cache = [PolylinePoint(self, i) for i in range(self._point_count)]
        return self._points_cache

    def _set_points(self, xs, ys, zs):
        self._polyline_set.set_positions(self._polyline_index, xs, ys, zs)

    @property
    def closed(self) -> bool:
        """A property to check if the polyline closed or open?

        Returns:
            `True` if the polyline is closed, `False` if open"""
        return self._polyline_set.is_closed(self._polyline_index)

    @property
    def parent_polylineset(self) -> None:
        """DeprecationWarning: 'parent_polylineset' has been removed. Use 'polylineset' instead
        """
        warn("'parent_polylineset' has been removed. Use 'polylineset' instead", 
             DeprecationWarning, stacklevel=2)
        raise RuntimeError("'parent_polylineset' has been removed. Use 'polylineset' instead")

    @property
    def polylineset(self) -> "PolylineSet":
        """Returns the parent 'PolylineSet' of the 'Polyline'"""
        return self._polyline_set

    @property
    def readonly(self) -> bool:
        """The readonly status of the parent `PolylineSet`

        Returns:
            bool: True if the parent `PolylineSet` is readonly"""
        return self._polyline_set.readonly

    def __str__(self) -> str:
        return "Polyline(parent_polylineset={0})".format(self.polylineset)

    def positions(self) -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        """Returns a tuple([x], [y], [z]), where x is a list of x positions, y is a list of y positions and z is a list of z positions"""        
        if self._position_array is None:
            self._load_points_cache()
        return typing.cast(typing.Tuple[typing.List[float], typing.List[float], typing.List[float]], self._position_array)

    @property
    def points(self) -> typing.List[typing.Union[PolylinePoint, primitives.Point]]:
        """A list of the :class:`cegalprizm.pythontool.PolylinePoint` objects making up the polyline"""
        if self._points_cache is None:
            self._load_points_cache()
        return typing.cast(typing.List[typing.Union[PolylinePoint, primitives.Point]], self._points_cache)

    @points.setter
    def points(self, lst: typing.List[typing.Union[PolylinePoint, primitives.Point]]) -> None:
        if self.readonly:
            raise exceptions.PythonToolException("Object is readonly")

        try:
            if _ToolMode.is_oop():
                arrayx = [float(0)] * len(lst)
                arrayy = [float(0)] * len(lst)
                arrayz = [float(0)] * len(lst)
            else:
                arrayx = _system().Array.CreateInstance(float, len(lst))
                arrayy = _system().Array.CreateInstance(float, len(lst))
                arrayz = _system().Array.CreateInstance(float, len(lst))
                
            for i, p in enumerate(lst):
                arrayx[i] = p.x
                arrayy[i] = p.y
                arrayz[i] = p.z
            self._set_points(arrayx, arrayy, arrayz)
            self._load_points_cache()
        except TypeError:
            raise TypeError("You must pass an iterable (list) of PolylinePoints")

    def add_point(self, point: primitives.Point) -> None:
        """Adds a point

        Adds a single point in displayed world co-ordinates to the polyline.  
        Using this method multiple times will
        be slower than building up a list of
        :class:`primitives.Point` objects and assigning it to
        the :func:`points` property in one go.

        **Example**:

        .. code-block:: python

          # slower
          mypolyline.add_point(primitives.Point(100.0, 123.0, 50.3))
          mypolyline.add_point(primitives.Point(102.0, 125.3, 50.2))

          # faster
          new_polylinepoints = [primitives.Point(100.0, 123.0, 50.3), primitives.Point(102.0, 125.3, 50.2)]
          mypolyline.points = new_polylinepoints

        Args:
            point (primitives.Point): the point to add

        """
        if self.readonly:
            raise exceptions.PythonToolException("Object is readonly")
        if self._points_cache is None:
            self._load_points_cache()
        self._points_cache = typing.cast(typing.List[typing.Union[PolylinePoint, primitives.Point]], self._points_cache)
        self._points_cache.append(point)
        self.points = self._points_cache
        self._load_points_cache()

    def delete_point(self, point: PolylinePoint) -> None:
        """Deletes a point

        Deletes one point from the polyline. Using this
        method multiple times will be slower than manipulating a list
        of :class:`cegalprizm.pythontool.PolylinePoint` objects and assigning it
        to the :func:`points` property in one go.

        Note that :class:`cegalprizm.pythontool.PolylinePoint` objects are compared by
        reference, not value.   In order to delete a point you must refer to
        the actual `PolylinePoint` object you wish to delete:

        **Example**:

        .. code-block:: python

          # set up the PointSet
          new_polylinepoints = [PolylinePoint(100.0, 123.0, 50.3), PolylinePoint(102.0, 125.3, 50.2)]
          mypolyline.points = new_polylinepoints

          # delete the second point in a Polyline
          # mypolyline.delete_point(PolylinePoint(102.0, 125.3, 50.2)) will not work
          p = mypolyline.points[1]  # the 2nd point
          mypolyline.delete_point(p)

        Args:
            point (cegalprizm.pythontool.PolylinePoint): the point to delete

        """
        if self.readonly:
            raise exceptions.PythonToolException("Object is readonly")
        if self._points_cache is None:
            self._points_cache = self._load_points_cache()
        try:
            self._points_cache.remove(point)
        except ValueError:
            raise ValueError("Point is not in the polyline")
        self.points = self._points_cache
        self._load_points_cache()

    def __getitem__(self, idx):
        if self._points_cache is None:
            self._load_points_cache()
        return self._points_cache[idx]

    def __len__(self):
        if self._points_cache is None:
            self._load_points_cache()
        return self._point_count

class PolylineSet(PetrelObject):
    """A class holding many :class:`cegalprizm.pythontool.Polyline` objects.

    ** The implementation of polyline sets is in a preliminary state. Handling large sets may
        fail or be slow. We are working on improving this.

    This is an iterable, returning  :class:`cegalprizm.pythontool.Polyline` objects.
    When iterating over this, do not modify the collection by adding or deleting lines
    - like many other Python iterators, undefined behaviour may result.
    """

    def __init__(self, python_petrel_polylineset: "PolylineSetGrpc"):
        super(PolylineSet, self).__init__(python_petrel_polylineset)
        self._polylines: typing.Dict[int, Polyline] = {}
        self._polylineset_object_link = python_petrel_polylineset

    def __str__(self) -> str:
        return 'PolylineSet(petrel_name="{0}")'.format(self.petrel_name)

    def __getitem__(self, idx: int) -> Polyline:
        if idx >= len(self) or idx < 0:
            raise ValueError("index out of range")

        if idx not in self._polylines:
            self._polylines[idx] = Polyline(self, idx)
        return self._polylines[idx]

    def __iter__(self) -> typing.Iterator[Polyline]:
        for i in range(0, len(self)):
            yield self[i]

    def __len__(self) -> int:
        """The number of lines in this `PolylineSet`"""
        return self._polylineset_object_link.GetNumPolylines()

    def is_closed(self, idx: int) -> bool:
        """Information if polygon is closed or open. 
                
        Args:
            idx (int): Index of the polygon in the PolylineSet

        Note: Index in Python starts at 0. Index in Petrel starts at 1.

        Returns:
            bool: True if closed, False otherwise.
        """        
        return self._polylineset_object_link.IsClosed(idx)

    @property
    def polylines(self) -> typing.Iterable[Polyline]:
        """Python iterator returning the polylines in a polyline set

        Use to retrieve the polylines :class:`cegalprizm.pythontool.Polyline` from the polyline set
        """
        return (val for val in self)

    def get_positions(self, idx: int) -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        """Gets the xyz positions of the polygons in a PolylineSet. 

        Args:
            idx: Index of the polygon in the PolylineSet

        Note: Index in Python starts at 0. Index in Petrel starts at 1.

        Raises:
            ValueError: If provided index is outside the range of indexes

        Returns:
            A tuple([x], [y], [z]), where [x] is a list of x positions, 
              [y] is a list of y positions and [z] is a list of z positions
        """ 
        if idx >= len(self) or idx < 0:
            raise ValueError("index out of range")
        pts = self._polylineset_object_link.GetPoints(idx)
        if type(pts) != type([]):
            pts = [[value for value in ls] for ls in pts]
        return (*pts,) # type: ignore

    def set_positions(self, idx: int, xs: typing.List[float], ys: typing.List[float], zs: typing.List[float]) -> None:
        """Replaces all xyz positions of the polygons in a PolylineSet.
             
        Note: Index in Python starts at 0. Index in Petrel starts at 1.

        Args:
            idx: Index of the polygon in the PolylineSet
            xs: A list with x-coordinates
            ys: A list with y-coordinates
            zs: A list with z-coordinates

        Raises:
            PythonToolException: if the polylineset is readonly
            ValueError: if the number of x-coordinates is lower than 1
        """        
        if self.readonly:
            raise exceptions.PythonToolException("PolylineSet is readonly")
        if len(xs) < 2:
            raise ValueError("You must supply at least 2 points")

        if _ToolMode.is_oop():
            arrayx = [float(0)] * len(xs)
            arrayy = [float(0)] * len(xs)
            arrayz = [float(0)] * len(xs)
        else:
            arrayx = _system().Array.CreateInstance(float, len(xs))
            arrayy = _system().Array.CreateInstance(float, len(xs))
            arrayz = _system().Array.CreateInstance(float, len(xs))

            
        for i, (x, y, z) in enumerate(zip(xs, ys, zs)):
            arrayx[i] = x
            arrayy[i] = y
            arrayz[i] = z
        self._polylineset_object_link.SetPolylinePoints(idx, arrayx, arrayy, arrayz)

    def add_line(self, points: typing.List[primitives.Point], closed: bool = True) -> None:
        """Adds a line to the set

        You must supply at least two points, or three if the polyline is closed.

        Args:
            points: a list of :class:`cegalprizm.pythontool.PolylinePoint` objects.
            closed: `True` if the polyline is closed, `False` if open. Defaults to True.

        Raises:
            exceptions.PythonToolException: If PolylineSet is readonly
            ValueError: if fewer than 2 points are given, or fewer than 3 if closed=True
        """        
        if self.readonly:
            raise exceptions.PythonToolException("PolylineSet is readonly")
        if len(points) < 2:
            raise ValueError("You must supply at least 2 points")
        if closed and (len(points) < 3):
            raise ValueError(
                "You must supply at least 3 points to create a closed polyline"
            )
      
        if _ToolMode.is_oop():
            arrayx = [float(0)] * len(points)
            arrayy = [float(0)] * len(points)
            arrayz = [float(0)] * len(points)
        else:
            arrayx = _system().Array.CreateInstance(float, len(points))
            arrayy = _system().Array.CreateInstance(float, len(points))
            arrayz = _system().Array.CreateInstance(float, len(points))
            
        for i, p in enumerate(points):
            arrayx[i] = p.x
            arrayy[i] = p.y
            arrayz[i] = p.z
        self._polylineset_object_link.AddPolyline(arrayx, arrayy, arrayz, closed)

    def delete_line(self, line: Polyline) -> None:
        """Deletes a polyline from the polyline set

        Args:
            line: the line to delete"""
        if self.readonly:
            raise exceptions.PythonToolException("PolylineSet is readonly")

        self._polylineset_object_link.DeletePolyline(line._polyline_index)

        # it's too tricky to maintain the cache so blow it away
        self._polylines = {}

    def clear(self) -> None:
        """Deletes all the lines from the polyline set"""
        if self.readonly:
            raise exceptions.PythonToolException("PolylineSet is readonly")

        self._polylineset_object_link.DeleteAll()
        self._polylines = {}

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "PolylineSet":
        """ Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.

        This is a Python Tool Pro function and is not available when running scripts in the editor integrated in Python Tool or in a workflow.
        
        Parameters:
            path_of_clone (str): Petrel name of the clone
            copy_values (bool): Set to True if values shall be copied into the clone. Defaults to False.

        Returns:
            PolylineSet: The clone
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("PolylineSet", self._clone(name_of_clone, copy_values = copy_values))
   
