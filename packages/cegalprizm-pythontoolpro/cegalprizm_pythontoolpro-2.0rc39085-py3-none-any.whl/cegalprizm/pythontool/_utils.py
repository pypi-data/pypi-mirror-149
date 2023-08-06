# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool import _ToolMode
import numpy as np
import datetime
from cegalprizm.pythontool._system import _system
import typing


IPY2 = 'ipy2'
CPY3 = 'cpy3'


def python_env():
    return CPY3


def iterable_values(arr):
    return arr.flat


def clone_array(arr: np.ndarray) -> np.ndarray:
    return arr.copy()


def to_backing_arraytype(nparray):
    ''' Creates and returns a .NET Array that mirrors the provided numpy array

    @nparray: numpy array

    @Returns: .NET Array with element type matching nparray.dtype and identical dimensions with content that matches the provided numpy array
    '''
    if not _ToolMode.is_oop():
        buffer = _system().Buffer
        gchandle = _system().Runtime.InteropServices.GCHandle
        gchandleType = _system().Runtime.InteropServices.GCHandleType
        marshal = _system().Runtime.InteropServices.Marshal
        nelements = nparray.size

        # get pointer to nparray data
        ptr64 = _system().Int64(nparray.ctypes.data)
        ptr = _system().IntPtr.op_Explicit(ptr64)

        if nparray.dtype == float or nparray.dtype == np.float64:
            net_type = _system().Double
        elif nparray.dtype == np.float32:
            net_type = _system().Single
        elif nparray.dtype == int or nparray.dtype == np.int32:
            net_type = _system().Int32
        elif nparray.dtype == np.int64:
            net_type = _system().Int64
        else:
            raise ValueError("to_backing_array does not handle nparrays of type " + str(nparray.dtype))

        # create pinned interim destination one-dimensional-array
        interim_array = _system().Array.CreateInstance(net_type, nelements)
        handle = gchandle.Alloc(interim_array, gchandleType.Pinned)
        try:
            marshal.Copy(ptr, interim_array, 0, nelements)

            # create properly-shaped array
            dims = nparray.shape
            n = len(dims)
            dims_dn = _system().Array.CreateInstance(_system().Int32, n)
            for i in range(n):
                dims_dn[i] = _system().Int32(dims[i])
            final_array = _system().Array.CreateInstance(net_type, dims)

            buffer.BlockCopy(interim_array, 0, final_array, 0, nelements * nparray.dtype.itemsize)

            return final_array
        finally:
            if handle.IsAllocated:
                handle.Free()
    else:
            return nparray

######################## Conversions from .NET ###########################

def ndarray_from_net_array(src):
    import ctypes
    gchandle = _system().Runtime.InteropServices.GCHandle
    gchandleType = _system().Runtime.InteropServices.GCHandleType

    src_hndl = gchandle.Alloc(src,  gchandleType.Pinned)
    try:
        src_ptr = src_hndl.AddrOfPinnedObject().ToInt64()

        type_dn = src.GetType().GetElementType().Name
        if type_dn == 'Double':
            dtype = np.float64
            ct = ctypes.c_double
        elif type_dn == 'Int32':
            dtype = np.int32
            ct = ctypes.c_int
        elif type_dn == 'Int64':
            dtype = np.int64
            ct = ctypes.c_long
        elif type_dn == 'Boolean':
            dtype = np.bool
            ct = ctypes.c_bool
        else:
            raise ValueError("Unknown dotnet array type")

        bufType = ct*len(src)
        cbuf = bufType.from_address(src_ptr)
        dest = np.frombuffer(cbuf, dtype=dtype)
        clone = np.copy(dest)
        clone.shape = tuple([src.GetLength(d) for d in range(0, src.Rank)])
        return clone
    finally:
        if src_hndl.IsAllocated:
            src_hndl.Free()


def from_backing_arraytype(src):
    ''' Creates and returns a numpy Array that mirrors the provided .NET array

    @src: .NET Array in in-process mode and a protobuf type in out-of-process mode

    @Returns: numpy Array with dtype matching src's element type, and identical dimensions with content that matches the provided .NET Array
    '''
    if not _ToolMode.is_oop():
        if isinstance(src, np.ndarray):
            raise TypeError("src is " + str(type(src)))
        return ndarray_from_net_array(src)
    else:
        return src

def _to_shaped_ndarray(val, size_i, size_j, size_k, np_type, spanning_dims = 'ijk'):
    if isinstance(val, list):
        val = np.array(val)

    if isinstance(val, np.ndarray) and val.shape == (size_i, size_j, size_k):
        val_ndarray = val
    elif not hasattr(val, "__len__"):
        val_ndarray = np.empty(size_k, dtype = np_type)
        val_ndarray.fill(val)        
    else:
        val_ndarray = val
    
    if spanning_dims == 'ij':
        val_ndarray.shape = (size_i, size_j)
    elif spanning_dims == 'k':
        val_ndarray.shape = (size_i*size_j*size_k,)
    else:
        val_ndarray.shape = (size_i, size_j, size_k)
            
    return val_ndarray.astype(np_type, copy = False, subok = True)

###################

def _ensure_1d_array(val, i, np_typ, net_typ, convert):
    if isinstance(val, np.ndarray):
        return val.astype(dtype=np_typ, copy=False)
    if isinstance(val, _system().Array):
        return from_backing_arraytype(val)
    elif isinstance(val, list):
        if len(val) > i:
            raise ValueError("too many values")
        array = np.empty((i), np_typ)
        for index in range(0, i):
            array[index] = convert(val[index])
        return array

    raise ValueError("Cannot convert %s into 1d array" % val)

def ensure_1d_float_array(val, i):
    """Converts a flat list into a Array[float] if necessary"""
    if not _ToolMode.is_oop():
        return _ensure_1d_array(val, i, np.float64, _system().Double, float)
    else: 
        return _to_shaped_ndarray(val, 1, 1, i, np.float32, spanning_dims = 'k')

def ensure_1d_int_array(val, i):
    """Converts a flat list into a Array[int] if necessary"""
    if not _ToolMode.is_oop():
        return _ensure_1d_array(val, i, np.int32, _system().Int32, int)
    else:
        return _to_shaped_ndarray(val, 1, 1, i, np.int32, spanning_dims = 'k')

def _ensure_2d_array(val, i, j, np_typ, net_typ, convert):
    if not _ToolMode.is_oop():
        if isinstance(val, np.ndarray):
            return val.astype(dtype=np_typ, copy=False)
        if isinstance(val, _system().Array):
            #return from_backing_arraytype(val)
            return ndarray_from_net_array(val)

        if isinstance(val, list):
            array = np.empty((i, j), np_typ)
            if len(val) == i * j:
                # flat list
                index_i = 0
                index_j = 0
                for v in val:
                    array[index_i, index_j] = convert(v)
                    index_j = index_j + 1
                    if index_j >= j:
                        index_j = 0
                        index_i = index_i + 1
                return array
            elif len(val) == i:
                # nested list j-major
                for (index_i, jlst) in enumerate(val):
                    for (index_j, v) in enumerate(jlst):
                        array[index_i, index_j] = convert(v)
                return array
            else: raise ValueError("List is of incorrect dimensions")

        raise ValueError("Cannot convert %s into 2d array" % val)

def ensure_2d_float_array(val, i, j):
    """Converts a flat or nested list into a Array[float]
    if necessary"""
    if not _ToolMode.is_oop():
        return _ensure_2d_array(val, i, j, np.float64, _system().Double, float)
    else:
        return _to_shaped_ndarray(val, i, j, 1, np.float32, spanning_dims = 'ij')

def ensure_2d_int_array(val, i, j):
    """Converts a flat or nested list into a Array[float]
    if necessary"""
    if not _ToolMode.is_oop():
        return _ensure_2d_array(val, i, j, np.int32, _system().Int32, int)
    else:
        return _to_shaped_ndarray(val, i, j, 1, np.int32, spanning_dims = 'ij')

def _ensure_3d_array(val, i, j, k, np_typ, net_typ, convert):
    if not _ToolMode.is_oop():
        if isinstance(val, np.ndarray):
            return val.astype(dtype=np_typ, copy=False)
        if isinstance(val, _system().Array):
            return from_backing_arraytype(val)
        elif isinstance(val, list):
            array = np.empty((i, j, k), np_typ) #Array.CreateInstance(typ, i, j, k)
            if len(val) == i * j * k:
                # flat list
                index_i = 0
                index_j = 0
                index_k = 0
                for v in val:
                    array[index_i, index_j, index_k] = convert(v)
                    index_k = index_k + 1
                    if index_k >= k:
                        index_k = 0
                        index_j = index_j + 1
                    if index_j >= j:
                        index_j = 0
                        index_i = index_i + 1
                return array
            elif len(val) == i:
                # nested list k-major
                for (index_i, jklst) in enumerate(val):
                    for (index_j, jlst) in enumerate(jklst):
                        for (index_k, v) in enumerate(jlst):
                            array[index_i, index_j, index_k] = convert(v)
                return array
            else: raise ValueError("List is of incorrect dimensions")

def ensure_3d_float_array(val, i, j, k):
    if not _ToolMode.is_oop():
        return _ensure_3d_array(val, i, j, k, np.float64, _system().Double, float)
    else:
        return _to_shaped_ndarray(val, i, j, k, np.float32)

def ensure_3d_int_array(val, i, j, k):
    if not _ToolMode.is_oop():
        return _ensure_3d_array(val, i, j, k, np.int32, _system().Int32, int)
    else:
        return _to_shaped_ndarray(val, i, j, k, np.int32)


def arrayof(lst):
    """A Array[object] populated with the contents of the list"""
    if not _ToolMode.is_oop():
        system_array = _system().Array
        system_object = _system().Object
        return system_array[system_object](lst)

def str_has_content(s: typing.Optional[str]) -> bool:
    """Returns False if the string is None, empty, or just whitespace"""
    if s is None:
        return False
    return bool(s.strip())

def str_or_none(s: typing.Optional[str]) -> typing.Optional[str]:
    if not str_has_content(s):
        return None
    return s

def about_equal(a, b):
    return abs(a-b) < 0.0000001

def floatarray(lst):
    return ensure_1d_float_array(lst, len(lst))

def intarray(lst):
    return ensure_1d_int_array(lst, len(lst))

def to_python_datetime(dt: typing.Union[typing.Any, datetime.datetime]) -> datetime.datetime:
    if not _ToolMode.is_oop():
        system_datetime = _system().DateTime
        if not isinstance(dt, system_datetime):
            raise TypeError("dt is not a System.DateTime")
        return datetime.datetime(year=dt.Year, month=dt.Month, day=dt.Day, hour=dt.Hour, minute=dt.Minute, second=dt.Second)
    elif isinstance(dt, datetime.datetime):
        return dt
    else:
        raise ValueError("Argument was expected to be a datetime.datetime object, got {}".format(dt))

def from_python_datetime(dt):
    if not _ToolMode.is_oop():
        system_datetime = _system().DateTime
        if not isinstance(dt, datetime.datetime):
            raise TypeError("dt is not datetime.datetime")
        return system_datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    else:
        return dt

def native_accessor(accessor):
    if not isinstance(accessor, tuple):
        raise TypeError("accessor is not tuple")
    return accessor
