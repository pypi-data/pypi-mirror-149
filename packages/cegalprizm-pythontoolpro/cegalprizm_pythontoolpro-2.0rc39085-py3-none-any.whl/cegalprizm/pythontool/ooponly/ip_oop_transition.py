# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import collections

Tuple2 = collections.namedtuple('Tuple2', 'Item1 Item2')
Range = collections.namedtuple('Range', 'Min Max')

class Ranges:
    
    def __init__(self, range_x:Range, range_y:Range, range_z:Range):
        self._range_x = range_x
        self._range_y = range_y
        self._range_z = range_z
        
    @property
    def X(self):
        return self._range_x

    @property
    def Y(self):
        return self._range_y

    @property
    def Z(self):
        return self._range_z

class Value2:

    def __init__(self, v1, v2):
        self._v1 = v1
        self._v2 = v2

    @property
    def X(self):
        return self._v1
    
    @property
    def Y(self):
        return self._v2
    
    @property
    def I(self):
        return self._v1
    
    @property
    def J(self):
        return self._v2
    
class Value3:

    def __init__(self, v1, v2, v3):
        self._v1 = v1
        self._v2 = v2
        self._v3 = v3

    @property
    def X(self):
        return self._v1
    
    @property
    def Y(self):
        return self._v2
    
    @property
    def Z(self):
        return self._v3
    
    @property
    def I(self):
        return self._v1
    
    @property
    def J(self):
        return self._v2
    
    @property
    def K(self):
        return self._v3
    
class ValuePoint:

    def __init__(self, value:Value3):
        self._value = value

    def GetValue(self):
        return self._value

class ValuePoints:

    def __init__(self):
        self._points = []

    def append(self, value3:Value3):
        self._points.append(value3)

    def GetValue(self):
        return self._points

class Point:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

