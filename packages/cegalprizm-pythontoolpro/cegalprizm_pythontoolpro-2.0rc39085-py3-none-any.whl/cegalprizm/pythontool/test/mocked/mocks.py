# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import collections
from cegalprizm.pythontool._system import _system

import sys

class PropertyRangeData:
    def __init__(self):
        self.PropertyIndex = 0
        self.Name = ''
        self.Indices = None
        self.DataType = None
        self.Values = None

class MockReference(object):
    def __init__(self, v):
        self._v = v

    @property
    def Value(self):
        return self._v

    def GetValue(self):
        return self._v


class MockPoint(object):
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def X(self):
        return self._x

    @property
    def Y(self):
        return self._y

    @property
    def Z(self):
        return self._z


class MockObjectFactory(object):
    """Emulates the injected PythonPetrelObjectFactory"""

    def __init__(self):
        self._properties = {
            "MyProp": MockPropertyObject(10, 10, 10),
            "ThreeProp": MockPropertyObject(3, 3, 3),
            "LargeProp": largeProp(),
        }
        self._dictionary_properties = {
            "ThreeDiscProp": MockDictionaryPropertyObject(3, 3, 3),
            "FourDiscProp": MockDictionaryPropertyObject(4, 4, 4),
        }
        self._grids = {
            "FourGrid": MockGridObject(4, 4, 4),
            "FiveGrid": MockGridObject(5, 5, 5),
        }
        self._seismics = {
            "FiveCube": MockSeismicObject(5, 5, 5),
            "TenSeismic": MockSeismicObject(10, 10, 10),
            "TwelveSeismic": MockSeismicObject(12, 12, 12),
        }
        self._surface_properties = {"ThreeSurfaceProp": MockSurfacePropertyObject(3, 3)}
        self._seismic2ds = {}
        self._dictionary_surface_properties = {"ThreeDictSurfaceProp": MockDictionarySurfacePropertyObject(3,3)}
        self._well_logs = {
            "gamma": MockWellLog("gamma", "borehole1"),
            "MyLog": MockWellLog("MyLog", "borehole1"),
            "gamma_missing": MockWellLog(
                "gamma_missing", "borehole1", missing_value=True
            ),
        }
        self._dictionary_well_logs = {
            "facies": MockDictionaryWellLog("facies", "borehole1"),
            "facies_missing": MockDictionaryWellLog(
                "facies", "borehole1", first_value_missing=True
            ),
        }
        self._pointsets = {"MyMockPointSets": MockPointSet([[1.0], [2.0], [914.40]], [[-914.40], [None]], ["Twt", "Vp"])}
        self._polylinesets = {"MyPolylineSet": MockPolylineSetObject(5)}
        self._global_well_logs = {
            "gamma": MockGlobalWellLog("gamma", ["borehole1", "borehole2"])
        }
        self._discrete_global_well_logs = {
            "facies": MockDictionaryGlobalWellLog("facies", ["borehole1", "borehole2"])
        }
        self._wells = {
            "borehole1": MockBorehole("borehole1", ["gamma"], ["facies"]),
            "borehole2": MockBorehole(
                "borehole2", ["log1", "log2", "log3"], ["dloga", "dlogb"]
            ),
        }
        self._horizon_interpretation_3ds = {
            "hi3d": MockHorizonInterpretation3DObject("hi3d", 3, 3)
        }

        self._wavelets = {}

        self._xyz_well_surveys = {}
        self._xytvd_well_surveys = {}
        self._dxdytvd_well_surveys = {}
        self._mdinclazim_well_surveys = {}
        self._explicit_well_surveys = {}
        self._horizon_interpretations = {}

        self._observed_data = {}
        self._observed_data_sets = {}

    def GetWaveletObjectNames(self):
        return self._wavelets.keys()

    def GetWaveletObject(self, name):
        return self._wavelets[name]

    def GetGridObject(self, name):
        return self._grids[name]

    def GetGridObjectNames(self):
        return self._grids.keys()

    def GetPropertyObject(self, name):
        return self._properties[name]

    def GetPropertyObjectNames(self):
        return self._properties.keys()

    def GetDictionaryPropertyObject(self, name):
        return self._dictionary_properties[name]

    def GetDictionaryPropertyObjectNames(self):
        return self._dictionary_properties.keys()

    def GetSeismicObject(self, name):
        return self._seismics[name]

    def GetPolylineSetObject(self, name):
        return self._polylinesets[name]

    def GetWellLogObject(self, name):
        return self._well_logs[name]

    def GetDictionaryWellLogObject(self, name):
        return self._dictionary_well_logs[name]

    def GetGlobalWellLogObject(self, name):
        return self._global_well_logs[name]

    def GetBoreholeObject(self, name):
        return self._wells[name]

    def GetSeismicObjectNames(self):
        return self._seismics.keys()

    def GetSeismic2dObjectNames(self):
        return self._seismic2ds.keys()

    def GetSurfaceObjectNames(self):
        return []

    def GetSurfacePropertyObjectNames(self):
        return self._surface_properties.keys()

    def GetSurfacePropertyObject(self, name):
        return self._surface_properties[name]

    def GetHorizonInterpretation3dObject(self, name):
        return self._horizon_interpretation_3ds[name]

    def GetHorizonInterpretationObject(self, name):
        return self._horizon_interpretations[name]

    def GetDictionarySurfacePropertyObject(self, name):
        return self._dictionary_surface_properties[name]

    def GetDictionarySurfacePropertyObjectNames(self):
        return self._dictionary_surface_properties.keys()
    
    def GetWellLogObjectNames(self):
        return self._well_logs.keys()

    def GetDictionaryWellLogObjectNames(self):
        return self._dictionary_well_logs.keys()

    def GetPointSetObjectNames(self):
        return self._pointsets.keys()

    def GetPolylineSetObjectNames(self):
        return self._polylinesets.keys()

    def GetGlobalWellLogObjectNames(self):
        return self._global_well_logs.keys()

    def GetHorizonInterpretation3dObjectNames(self):
        return self._horizon_interpretation_3ds.keys()

    def GetHorizonInterpretationObjectNames(self):
        return self._horizon_interpretations.keys()

    def GetDecoratedWellLogVersion(self):
        return None

    def GetDictionaryGlobalWellLogObjectNames(self):
        return self._discrete_global_well_logs.keys()

    def GetDictionaryGlobalWellLogObject(self, name):
        return self._discrete_global_well_logs[name]

    def GetBoreholeObjectNames(self):
        return self._wells.keys()

    def GetPointSetObject(self, name):
        return self._pointsets[name]

    def GetXyzWellSurveyObjectNames(self):
        return self._xyz_well_surveys.keys()

    def GetXyzWellSurveyObject(self, name):
        return self._xyz_well_surveys[name]

    def GetXytvdWellSurveyObjectNames(self):
        return self._xytvd_well_surveys.keys()

    def GetXytvdWellSurveyObject(self, name):
        return self._xytvd_well_surveys[name]

    def GetDxdytvdWellSurveyObjectNames(self):
        return self._dxdytvd_well_surveys.keys()

    def GetDxdytvdWellSurveyObject(self, name):
        return self._dxdytvd_well_surveys[name]

    def GetMdinclazimWellSurveyObjectNames(self):
        return self._mdinclazim_well_surveys.keys()

    def GetMdinclazimWellSurveyObject(self, name):
        return self._mdinclazim_well_surveys[name]

    def GetExplicitWellSurveyObjectNames(self):
        return self._explicit_well_surveys.keys()

    def GetExplicitWellSurveyObject(self, name):
        return self._explicit_well_surveys[name]
        
    def GetObservedDataObjectNames(self):
        return self._observed_data.keys()

    def GetObservedDataObject(self, name):
        return self._observed_data[name]
        
    def GetObservedDataSetObjectNames(self):
        return self._observed_data_sets.keys()

    def GetObservedDataSetObject(self, name):
        return self._observed_data_sets[name]

class MockGridObject(object):
    def __init__(self, i, j, k):
        self.__i = i
        self.__j = j
        self.__k = k

    def NumI(self):
        return self.__i

    def NumJ(self):
        return self.__j

    def NumK(self):
        return self.__k

    @property
    def ReadOnly(self):
        return False

    def IsCellDefined(self, i, j, k):
        return True

    def GetCellCorners(self, i, j, k):
        return MockReference([MockPoint(0, 0, 0)] * 8)


class MockSeismicObject(object):
    def __init__(self, i, j, k):
        self.__i = i
        self.__j = j
        self.__k = k
        self._values = _system().Array.CreateInstance(_system().Double, i, j, k)

    def NumI(self):
        return self.__i

    def NumJ(self):
        return self.__j

    def NumK(self):
        return self.__k

    @property
    def ReadOnly(self):
        return False

    def Reset(self):
        for i in range(0, self.NumI()):
            for j in range(0, self.NumJ()):
                for k in range(0, self.NumK()):
                    self._values[i, j, k] = i + 10 * j + 100 * k

    def GetColumn(self, i, j):
        col = _system().Array.CreateInstance(_system().Double, self.NumK())
        for k in range(0, self.NumK()):
            col[k] = self._values[i, j, k]
        return col

    def SetColumn(self, i, j, values):
        for k in range(0, self.NumK()):
            self._values[i, j, k] = values[k]

    def GetLayer(self, k):
        layer = _system().Array.CreateInstance(_system().Double, self.NumI(), self.NumJ())
        for i in range(0, self.NumI()):
            for j in range(0, self.NumJ()):
                layer[i, j] = self._values[i, j, k]
        return layer

    def SetLayer(self, k, values):
        layer = _system().Array.CreateInstance(_system().Double, self.NumI(), self.NumJ())
        for i in range(0, self.NumI()):
            for j in range(0, self.NumJ()):
                self._values[i, j, k] = values[i, j]

    def GetChunk(self, i, j, k):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)
        if k is None:
            k = (0, self.NumK() - 1)

        if type(i) is not tuple and i is not None:
            raise ValueError("i arg incorrect")
        if type(j) is not tuple and j is not None:
            raise ValueError("j arg incorrect")
        if type(k) is not tuple and k is not None:
            raise ValueError("k arg incorrect")

        irange = range(i[0], i[1] + 1)
        jrange = range(j[0], j[1] + 1)
        krange = range(k[0], k[1] + 1)

        arr = _system().Array.CreateInstance(float, len(irange), len(jrange), len(krange))
        for i in irange:
            for j in jrange:
                for k in krange:
                    arr[i - irange[0], j - jrange[0], k - krange[0]] = self._values[
                        i, j, k
                    ]
        return arr

    def SetChunk(self, i, j, k, values):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)
        if k is None:
            k = (0, self.NumK() - 1)

        irange = list(range(i[0], i[1] + 1))
        jrange = list(range(j[0], j[1] + 1))
        krange = list(range(k[0], k[1] + 1))

        i = irange[0]
        j = jrange[0]
        k = krange[0]

        for v in values:
            self._values[i, j, k] = v
            k = k + 1
            if k > krange[-1]:
                k = krange[0]
                j = j + 1
            if j > jrange[-1]:
                j = jrange[0]
                i = i + 1
            if i > irange[-1]:
                break


class MockSurfaceObject(object):
    def __init__(self, i, j):
        self._i = i
        self._j = j

    def NumI(self):
        return self._i

    def NumJ(self):
        return self._j

    @property
    def ReadOnly(self):
        return False


class MockSurfacePropertyObject(object):
    """Emulates a PythonSurfacePropertyObject"""

    def __init__(self, i, j):
        self._i = i
        self._j = j
        self._array = _system().Array.CreateInstance(_system().Double, i, j)
        self._populate_array()

    def GetPetrelName(self):
        return "MockSurfaceProperty"

    def NumI(self):
        return self._i

    def NumJ(self):
        return self._j

    def GetParentSurface(self):
        return MockSurfaceObject(self._i, self._j)

    def GetAllValues(self):
        return self.GetChunk(None, None)

    def SetAllValues(self, values):
        if not isinstance(values, _system().Array):
            raise ValueError("values not of System.Array type")
        self.SetChunk(None, None, values)

    def GetChunk(self, i, j):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)

        if type(i) is not tuple and i is not None:
            raise ValueError("i arg incorrect")
        if type(j) is not tuple and j is not None:
            raise ValueError("j arg incorrect")

        irange = range(i[0], i[1] + 1)
        jrange = range(j[0], j[1] + 1)

        arr = _system().Array.CreateInstance(_system().Double,  len(irange), len(jrange))
        for i in irange:
            for j in jrange:
                arr[i - irange[0], j - jrange[0]] = self._array[i, j]
        return arr

    def SetChunk(self, i, j, values):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)

        irange = list(range(i[0], i[1] + 1))
        jrange = list(range(j[0], j[1] + 1))

        i = irange[0]
        j = jrange[0]

        for i in irange:
            for j in jrange:
                self._array[i - irange[0], j - jrange[0]] = values[i, j]

    def _populate_array(self):
        for i in range(0, self._i):
            for j in range(0, self._j):
                self._array[i, j] = i + 10 * j

    @property
    def ReadOnly(self):
        return False

class MockDictionarySurfacePropertyObject(MockSurfacePropertyObject):
    def __init__(self, i, j):
        self._i = i
        self._j = j
        self._array = _system().Array.CreateInstance(_system().Int32, i, j)
        self._populate_array()

    def GetPetrelName(self):
        return "MockSurfaceProperty"

    def NumI(self):
        return self._i

    def NumJ(self):
        return self._j

    def GetParentSurface(self):
        return MockSurfaceObject(self._i, self._j)

    def GetAllValues(self):
        return self.GetChunk(None, None)

    def SetAllValues(self, values):
        if not isinstance(values, _system().Array):
            raise ValueError("values not of System.Array type")
        self.SetChunk(None, None, values)

    def GetChunk(self, i, j):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)

        if type(i) is not tuple and i is not None:
            raise ValueError("i arg incorrect")
        if type(j) is not tuple and j is not None:
            raise ValueError("j arg incorrect")

        irange = range(i[0], i[1] + 1)
        jrange = range(j[0], j[1] + 1)

        arr = _system().Array.CreateInstance(_system().Int32,  len(irange), len(jrange))
        for i in irange:
            for j in jrange:
                arr[i - irange[0], j - jrange[0]] = self._array[i, j]
        return arr

    def SetChunk(self, i, j, values):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)

        irange = list(range(i[0], i[1] + 1))
        jrange = list(range(j[0], j[1] + 1))

        i = irange[0]
        j = jrange[0]

        for i in irange:
            for j in jrange:
                self._array[i - irange[0], j - jrange[0]] = values[i, j]

    def _populate_array(self):
        for i in range(0, self._i):
            for j in range(0, self._j):
                self._array[i, j] = i + 10 * j

    @property
    def ReadOnly(self):
        return False

    def GetAllDictionaryCodes(self):
        return []

class EmptyObject(object):
    pass


class MockHorizonProperty3DObject(object):
    def __init__(self, name, i, j):
        self._name = name
        self._i = i
        self._j = j
        self._array = _system().Array.CreateInstance(_system().Double, i, j)
        self._populate_array()

    def GetDisplayUnitSymbol(self):
        # TODO
        raise NotImplementedError

    def GetPetrelName(self):
        return self._name

    def IndexAtPosition(self, x, y):
        Index2 = collections.namedtuple("Index2", "I J")
        container = EmptyObject()
        container.GetValue = lambda: Index2(0, 1)
        return container

    def PositionAtIndex(self, i, j):
        Point3 = collections.namedtuple("Point3", "X Y Z")
        container = EmptyObject()
        container.GetValue = lambda: Point3(0.1, 1.2, -3)
        return container

    # The rest is basically copy paste from MockSurfacePropertyObject
    def NumI(self):
        return self._i

    def NumJ(self):
        return self._j

    def GetAllValues(self):
        self.GetChunk(None, None)

    def GetChunk(self, i, j):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)

        if type(i) is not tuple and i is not None:
            raise ValueError("i arg incorrect")
        if type(j) is not tuple and j is not None:
            raise ValueError("j arg incorrect")

        irange = range(i[0], i[1] + 1)
        jrange = range(j[0], j[1] + 1)

        arr = _system().Array.CreateInstance(_system().Double, len(irange), len(jrange))
        for i in irange:
            for j in jrange:
                arr[i - irange[0], j - jrange[0]] = self._array[i, j]
        return arr

    def SetChunk(self, i, j, values):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)

        irange = list(range(i[0], i[1] + 1))
        jrange = list(range(j[0], j[1] + 1))

        i = irange[0]
        j = jrange[0]

        for i in irange:
            for j in jrange:
                self._array[i - irange[0], j - jrange[0]] = values[i, j]

    def SetAllValues(self, values):
        if not isinstance(values, _system().Array):
            raise ValueError("values not of System.Array type")
        self.SetChunk(None, None, values)

    def _populate_array(self):
        for i in range(0, self._i):
            for j in range(0, self._j):
                self._array[i, j] = i + 10 * j

    @property
    def ReadOnly(self):
        return False


class MockHorizonInterpretation3DObject(MockHorizonProperty3DObject):
    def __init__(self, name, i, j):
        self._name = name
        self._i = i
        self._j = j
        self._array = _system().Array.CreateInstance(_system().Double, i, j)
        self._populate_array()

    def GetAllHorizonPropertyValues(self):
        return [MockHorizonProperty3DObject("TWT", 3, 3)]

    def SampleCount(self):
        return self._i * self._j


class MockPropertyObject(object):
    """Emulates a PetrelPropertyObject"""

    def __init__(self, i, j, k):
        self._i = i
        self._j = j
        self._k = k
        self._array = _system().Array.CreateInstance(float, self._i, self._j, self._k)
        self._populate_array()

    def GetParentPythonGridObject(self):
        return MockGridObject(self._i, self._j, self._k)

    def GetPetrelName(self):
        return "MockProperty"

    def NumI(self):
        return self._i

    def NumJ(self):
        return self._j

    def NumK(self):
        return self._k

    def GetAll(self):
        arr = _system().Array.CreateInstance(float, self.NumI(), self.NumJ(), self.NumK())
        for i in range(0, self.NumI()):
            for j in range(0, self.NumJ()):
                for k in range(0, self.NumK()):
                    arr[i, j, k] = self._array[i, j, k]
        return arr

    def GetChunk(self, i, j, k):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)
        if k is None:
            k = (0, self.NumK() - 1)

        if type(i) is not tuple and i is not None:
            raise ValueError("i arg incorrect")
        if type(j) is not tuple and j is not None:
            raise ValueError("j arg incorrect")
        if type(k) is not tuple and k is not None:
            raise ValueError("k arg incorrect")

        irange = range(i[0], i[1] + 1)
        jrange = range(j[0], j[1] + 1)
        krange = range(k[0], k[1] + 1)

        arr = _system().Array.CreateInstance(float, len(irange), len(jrange), len(krange))
        for i in irange:
            for j in jrange:
                for k in krange:
                    arr[i - irange[0], j - jrange[0], k - krange[0]] = self._array[
                        i, j, k
                    ]
        return arr

    def SetChunk(self, i, j, k, values):
        # if tuples are passed, they are *inclusive*, so subtract one from the extent as we add one later in the method
        if i is None:
            i = (0, self.NumI() - 1)
        if j is None:
            j = (0, self.NumJ() - 1)
        if k is None:
            k = (0, self.NumK() - 1)

        irange = list(range(i[0], i[1] + 1))
        jrange = list(range(j[0], j[1] + 1))
        krange = list(range(k[0], k[1] + 1))

        i = irange[0]
        j = jrange[0]
        k = krange[0]

        for v in values:
            self._array[i, j, k] = v
            k = k + 1
            if k > krange[-1]:
                k = krange[0]
                j = j + 1
            if j > jrange[-1]:
                j = jrange[0]
                i = i + 1
            if i > irange[-1]:
                break

    def GetColumn(self, i, j):
        arr = _system().Array.CreateInstance(float, self.NumK())
        for k in range(0, self.NumK()):
            arr[k] = self._array[i, j, k]
        return arr

    def GetLayer(self, k):
        arr = _system().Array.CreateInstance(float, self.NumI(), self.NumJ())
        for i in range(0, self.NumI()):
            for j in range(0, self.NumJ()):
                arr[i, j] = self._array[i, j, k]
        return arr

    def SetColumn(self, i, j, values):
        if not isinstance(values, _system().Array):
            raise ValueError("values not of System.Array type")
        for k, v in enumerate(values):
            self._array[i, j, k] = v

    def SetLayer(self, k, values):
        if not isinstance(values, _system().Array):
            raise ValueError("values not of System.Array type")
        i = 0
        j = 0
        for v in values:
            self._array[i, j, k] = v
            j = j + 1
            if j >= self.NumJ():
                j = 0
                i = i + 1

    def SetAll(self, values):
        if not isinstance(values, _system().Array):
            raise ValueError("values not of System.Array type")
        i = 0
        j = 0
        k = 0
        for v in values:
            self._array[i, j, k] = v
            k = k + 1
            if k >= self.NumK():
                k = 0
                j = j + 1
            if j >= self.NumJ():
                j = 0
                i = i + 1

    def _value(self, i, j, k):
        assert i < self.NumI()
        assert j < self.NumJ()
        assert k < self.NumK()
        return i + 10 * j + 100 * k

    def _populate_array(self):
        for i in range(0, self._i):
            for j in range(0, self._j):
                for k in range(0, self._k):
                    self._array[i, j, k] = self._value(i, j, k)

    @property
    def ReadOnly(self):
        return False

    def GetDate(self):
        return None





class MockDictionaryPropertyObject(object):
    """Emulates a PetrelDictionaryPropertyObject"""

    def __init__(self, i, j, k):
        self._i = i
        self._j = j
        self._k = k
        self._array = _system().Array.CreateInstance(int, self._i, self._j, self._k)
        self._populate_array()

    def GetParentPythonGridObject(self):
        return MockGridObject(self._i, self._j, self._k)

    def GetPetrelName(self):
        return "MockProperty"

    def NumI(self):
        return self._i

    def NumJ(self):
        return self._j

    def NumK(self):
        return self._k

    def GetColumn(self, i, j):
        arr = _system().Array.CreateInstance(int, self.NumK())
        for k in range(0, self.NumK()):
            arr[k] = self._array[i, j, k]
        return arr

    def GetLayer(self, k):
        arr = _system().Array.CreateInstance(int, self.NumI(), self.NumJ())
        for i in range(0, self.NumI()):
            for j in range(0, self.NumJ()):
                arr[i, j] = self._array[i, j, k]
        return arr

    def SetColumn(self, i, j, values):
        if not isinstance(values, _system().Array):
            raise ValueError("values not of System.Array type")
        for k, v in enumerate(values):
            self._array[i, j, k] = v

    def SetLayer(self, k, values):
        if not isinstance(values, _system().Array):
            raise ValueError("values not of System.Array type")
        i = 0
        j = 0
        for v in values:
            self._array[i, j, k] = v
            j = j + 1
            if j >= self.NumJ():
                j = 0
                i = i + 1

    def _value(self, i, j, k):
        assert i < self.NumI()
        assert j < self.NumJ()
        assert k < self.NumK()
        return i + 10 * j + 100 * k

    def _populate_array(self):
        for i in range(0, self._i):
            for j in range(0, self._j):
                for k in range(0, self._k):
                    self._array[i, j, k] = self._value(i, j, k)

    @property
    def ReadOnly(self):
        return False

    def GetAllDictionaryCodes(self):
        return []



class MockPolylineSetObject(object):
    def __init__(self, num_lines):
        self._num_lines = num_lines
        self._lines = []
        self._names = ["Twt"]
        self._properties = [[i for i in range(num_lines)]]
        for i in range(num_lines):
            rpts = 3
            self._lines.append([[i]*3, [i]*3, [i]*3])

    def GetPoints(self, idx):
        return self._lines[idx]

    def GetProperties(self):
        return self._properties

    def GetPropertyCount(self):
        return len(self._properties)

    def SetProperty(self,  propertyIdx, polylineIdx, val):
        self._properties[propertyIdx][polylineIdx] = val
        
    def SetProperties(self, propertyIdx, vals):
        for polylineIdx in range(len(self._properties[propertyIdx])):
            self._properties[propertyIdx][polylineIdx] = vals[polylineIdx]

    def SetPropertiesTable(self, valsTable):
        for propertyIdx in range(len(self._properties)):
            for polylineIdx in range(len(self._properties[propertyIdx])):
                self._properties[propertyIdx][polylineIdx] = valsTable[propertyIdx][polylineIdx]

    def GetPropertyNames(self):
        return self._names

    def GetNumPolylines(self):
        return len(self._lines)

    def AddPolyline(self, xs, ys, zs, isClosed):
        self._lines.append([xs, ys, zs])

    def DeletePolyline(self, idx):
        self._lines = [val for i, val in enumerate(self._lines) if not i == idx]

    @property
    def ReadOnly(self):
        return False

    def DeleteAll(self):
        self._lines = []
class MockBorehole:
    def __init__(self, name, continousLogNames, dictionaryLogNames):
        self._name = name
        self._continousLogNames = continousLogNames
        self._dictionaryLogNames = dictionaryLogNames

    def GetPetrelName(self):
        return self._name

    @property
    def ReadOnly(self):
        return False

    def GetLogs(self, global_well_logs, discrete_global_well_logs):
        mockWellLogs = [MockWellLog(gwl.GetPetrelName(), self._name) for gwl in global_well_logs]
        mockWellLogs.extend([MockWellLog(gwl.GetPetrelName(), self._name) for gwl in discrete_global_well_logs])
        num_samples = len(mockWellLogs[0].Samples())
        import numpy as np

        global_well_logs = [mockWellLog for mockWellLog in mockWellLogs if mockWellLog.GetPetrelName() in self._continousLogNames]
        discrete_global_well_logs = [mockWellLog for mockWellLog in mockWellLogs if mockWellLog.GetPetrelName() in self._dictionaryLogNames]
        logdata = np.zeros((num_samples, len(global_well_logs) + len(discrete_global_well_logs) + 3))

        for mockWellLog in mockWellLogs:
            samples = mockWellLog.Samples()
            values = [sample.Value for sample in samples]
            mds = [sample.Md for sample in samples]
            twts = [sample.ZTwt for sample in samples]
            tvds = [sample.ZTvd for sample in samples]
            logdata[:, 0] = values
            logdata[:, 1] = mds
            logdata[:, 2] = twts
            logdata[:, 3] = tvds

        return logdata

    def GetAllContinuousLogs(self):
        return [MockWellLog(ln, self._name) for ln in self._continousLogNames]

    def GetAllDictionaryLogs(self):
        return [MockWellLog(ln, self._name) for ln in self._dictionaryLogNames]

    # return [MockWellLog(gwl.GetPetrelName()) for gwl in global_well_logs]


MockWellLogSample = collections.namedtuple(
    "MockWellLogSample", ["Md", "X", "Y", "ZMd", "ZTwt", "ZTvd", "Value"]
)


class MockWellLog(object):
    def __init__(self, name, borehole_name, missing_value=False):
        self._name = name
        self._borehole_name = borehole_name
        self._missing_value = missing_value
        self._samples = self._make_samples()

    def _make_samples(self):
        return [
            MockWellLogSample(
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1 if not self._missing_value else None
            ),
            MockWellLogSample(
                1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9 if not self._missing_value else None
            ),
        ]

    def Samples(self):
        return self._samples

    def SetSamples(self, mds, values):
        tups = zip(mds, values)
        self._samples = [
            MockWellLogSample(tup[0], 0.0, 0.0, 0.0, 0.0, 0.0, tup[1]) for tup in tups
        ]

    def GetParentPythonBoreholeObject(self):
        return MockBorehole(self._borehole_name, [self._name], [])

    def GetPetrelName(self):
        return self._name

    def GetAllDictionaryCodes(self):
        return {}

    def GetGlobalWellLog(self):
        return MockGlobalWellLog(self._name, [self._borehole_name])

    @property
    def ReadOnly(self):
        return False


class MockTuple(object):
    def __init__(self, item1, item2):
        self._item1 = item1
        self._item2 = item2

    @property
    def Item1(self):
        return self._item1

    @property
    def Item2(self):
        return self._item2


class MockDictionaryWellLog(object):
    def __init__(self, name, borehole_name, first_value_missing=False):
        self._name = name
        self._borehole_name = borehole_name
        self._first_value_missing = first_value_missing
        self._samples = self._make_samples()

    def _make_samples(self):
        if not self._first_value_missing:
            return [
                MockWellLogSample(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1),
                MockWellLogSample(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2),
            ]
        else:
            return [
                MockWellLogSample(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None),
                MockWellLogSample(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2),
            ]

    def SetSamples(self, mds, values):
        tups = zip(mds, values)
        self._samples = [
            MockWellLogSample(tup[0], 0.0, 0.0, 0.0, 0.0, 0.0, tup[1]) for tup in tups
        ]

    def Samples(self):
        return self._samples

    def GetParentPythonBoreholeObject(self):
        return MockBorehole(self._borehole_name, [self._name], [])

    def GetPetrelName(self):
        return self._name

    def GetAllDictionaryCodes(self):
        return [MockTuple(1, "one"), MockTuple(2, "two")]

    def GetGlobalWellLog(self):
        return MockDictionaryGlobalWellLog(self._name, [self._borehole_name])

    @property
    def ReadOnly(self):
        return False


class MockGlobalWellLog(object):
    def __init__(self, name, boreholes=[]):
        self._name = name
        self._boreholes = boreholes

    def GetWellLogByBoreholeName(self, borehole_name):
        if borehole_name in self._boreholes:
            return MockWellLog(self._name, borehole_name)

    def GetAllWellLogs(self):
        return [
            MockWellLog(self._name, borehole_name) for borehole_name in self._boreholes
        ]

    def GetPetrelName(self):
        return self._name

    def GetDroidString(self):
        return self._name


class MockDictionaryGlobalWellLog(object):
    def __init__(self, name, boreholes=[]):
        self._name = name
        self._boreholes = boreholes

    def GetWellLogByBoreholeName(self, borehole_name):
        if borehole_name in self._boreholes:
            return MockWellLog(self._name, borehole_name)

    def GetAllWellLogs(self):
        return [
            MockWellLog(self._name, borehole_name) for borehole_name in self._boreholes
        ]

    def GetPetrelName(self):
        return self._name
        
    def GetDroidString(self):
        return self._name


class MockPointSet(object):
    def __init__(self, points, properties, names):
        self._points = points
        self._properties = properties
        self._names = names

    def GetPoints(self): 
        # List of point3s
        return self._points

    def SetPoints(self, xs, ys, zs):
        self._points = [xs, ys, zs]

    def GetPointProperties(self):
        # List of Point properties
        return self._properties

    def OrderedUniquePropertyNames(self):
        return ['x', 'y', 'z'] + self._names

    def GetPropertiesValuesByInds(self, indices):
        all_data = []
        for propertyIdx, name in enumerate(self._names):
            data = PropertyRangeData()
            data.Name = name
            data.Indices = range(0, len(self._points[0]))
            data.Values = [property for property in self._properties[propertyIdx][:]]
            data.DataType = "System.Double"
            all_data.append(data)
        
        return all_data

    # def GetPropertiesValuesByRange(self, start, end, step):
    #     return self.GetPropertiesValuesByInds(range(start, end + 1, step))

    def GetPositionValuesByInds(self, indices, x_range, y_range, z_range, max_points):
        all_data = []
        for i, name in enumerate(['x', 'y', 'z']):
            data = PropertyRangeData()
            data.Name = name
            data.Indices = range(0, len(self._points[0]))
            data.Values = self._points[i]
            data.DataType = "System.Double"
            all_data.append(data)

        return all_data

    def GetPositionValuesByRange(self, start, end, step, x_range, y_range, z_range, max_points):
        return self.GetPositionValuesByInds(range(start, end + 1, step), x_range, y_range, z_range, max_points)
        
    def SetPropertyValues(self, uniquePropertyName, indexes, vals):
        if uniquePropertyName in ['x', 'y', 'z']:
            return

        property_names = self.OrderedUniquePropertyNames()
        property_idx = property_names.index(uniquePropertyName) - 3
        try:
            for point_index in indexes:
                self._properties[property_idx][point_index] = vals[point_index]
        except:
            pass
    
    def GetPointPropertyNames(self):
        return self._names

    def SetPointProperty(self, propertyIdx, pointIdx, value):
        self._properties[propertyIdx][pointIdx] = value

    def GetDisplayUnitSymbol(self, row):
        return "Ms"

    def GetPointCount(self):
        return len(self._points[0])

    def GetPropertyCount(self):
        return len(self._properties)

    def SetPointProperties(self, property_index, values):
        self._properties[property_index] = values

    def SetPointPropertiesTable(self, values):
        self._properties = values


        
# only construct this once as it's so expensive.  Don't mutate!
# largeProp = MockPropertyObject(100, 100, 100)
_largeProp = None
def largeProp():
    global _largeProp
    if not _largeProp:
        _largeProp = MockPropertyObject(10, 10, 10)
    return _largeProp
