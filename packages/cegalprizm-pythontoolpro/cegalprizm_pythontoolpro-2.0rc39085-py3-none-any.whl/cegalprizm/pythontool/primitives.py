# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import collections

# TODO rename extent to Indices or somesuch
Extent = collections.namedtuple('Extent', 'i j k')
"""The number of indices in each direction.  Valid indices will be
from 0 to `i-1`, 0 to `j-1` and 0 to `k-1`.  If an object does not
have an extent in a certain direction, the value will be ``None``."""

Indices = collections.namedtuple('Indices', 'i j k')
"""Represents a set of indices.  For 3D objects, all indices are
valid, but for 2D objects one will be ``None``.  Currently for a
:class:`cegalprizm.pythontool.SeismicLine` only `j` and `k` are valid;
for a :class:`cegalprizm.pythontool.Surface` only `i` and `j` are valid.
"""

Annotation = collections.namedtuple('Annotation', 'inline xline sample')
"""Represents a set of annotations for seismic objects.  These are
commonly not 0-based and possibly irregularly spaced, so it is not
advisable to iterate over annotations directly but to use methods to
convert them to :class:`cegalprizm.pythontool.Indices` and back again.
"""

class Point(collections.namedtuple('Point', 'x y z')):
    """Represents a point in space, according to the coordinate system in use (no coordinate transforms are attempted or considered)."""
    __slots__ = ()
    def __str__(self) -> str:
        return "Point(x={:.2f}, y={:.2f}, z={:.2f})".format(self.x, self.y, self.z)


class AxisExtent(object):
    """The minimum and maximum positions of an axis of an object in world-coordinates"""
    def __init__(self, min, max):
        self.__min = min
        self.__max = max

    @property
    def min(self):
        """The minimum value"""
        return self.__min

    @property
    def max(self):
        """The maximum value"""
        return self.__max

    def __str__(self):
        return "AxisExtent(min=%f, max=%f)" % (self.min, self.max)

class CoordinatesExtent(object):
    """Stores the minimum and maximum extent of an object in world-coordinates"""

    def __init__(self, cs_range):
        self.__x_axis_extent = AxisExtent(cs_range.X.Min, cs_range.X.Max)
        self.__y_axis_extent = AxisExtent(cs_range.Y.Min, cs_range.Y.Max)
        self.__z_axis_extent = AxisExtent(cs_range.Z.Min, cs_range.Z.Max)

    @property
    def x_axis(self):
        """The extent of the x-axis of the object in world-coordinates

        Returns:

          cegalprizm.pythontool.AxisExtent: the extent of the axis"""
        return self.__x_axis_extent

    @property
    def y_axis(self):
        """The extent of the y-axis of the object in world-coordinates

        Returns:

          cegalprizm.pythontool.AxisExtent: the extent of the axis"""
        return self.__y_axis_extent

    @property
    def z_axis(self):
        """The extent of the z-axis of the object in world-coordinates

         Returns:

          cegalprizm.pythontool.AxisExtent: the extent of the axis"""
        return self.__z_axis_extent

    def __str__(self):
        return "CoordinatesExtent(x_axis=%s, y_axis=%s, z_axis=%s)" % (self.x_axis,
                                                                       self.y_axis,
                                                                       self.z_axis)
