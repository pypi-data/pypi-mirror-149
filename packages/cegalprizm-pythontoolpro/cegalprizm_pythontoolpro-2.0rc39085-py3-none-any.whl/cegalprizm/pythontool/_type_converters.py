# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import datetime
from cegalprizm.pythontool.exceptions import PythonToolException
from cegalprizm.pythontool._system import _system

import numpy as np
import pandas as pd

class _TypeConverter:
    
    def __init__(self):
        self._net_to_np_map = {
            'System.String': (object, lambda s: str(s)),
            'System.DateTime': (datetime.datetime, lambda d: datetime.datetime(d.Year, d.Month, d.Day, d.Hour, d.Minute, d.Second)
                                if (d.Year, d.Month, d.Day, d.Hour, d.Minute, d.Second) != (1,1,1,0,0,0) else None ),
            'System.Single': (np.float64, lambda s: np.float64(s)),
            'System.Double': (np.float64, lambda d: np.float64(d)),
            'System.Int32': (np.int32, lambda i: np.int32(i)),
            'System.Boolean': (bool, lambda b: b)
        }

    def _np_to_net_map(self, dtype):
        import pandas as pd
        Sys = _system()
        if dtype == str:
            return (Sys.String, lambda s: Sys.String(s))
        if dtype == np.str_:
            return (Sys.String, lambda s: Sys.String(str(s)))
        elif dtype == datetime.datetime or dtype == pd.Timestamp:
            return (Sys.DateTime, lambda dt: Sys.DateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))
        elif dtype == np.datetime64:
            def converter(dt):
                dt = pd.Timestamp(dt)
                if pd.isnull(dt):
                    return Sys.DateTime(1, 1, 1, 0, 0, 0)
                else:
                    return Sys.DateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            return (Sys.DateTime, converter)
        elif dtype == np.float64 or dtype == float:
            return (Sys.Double, lambda d: Sys.Double(d))
        elif dtype == np.float32:
            return (Sys.Single, lambda s: Sys.Single(s))
        elif dtype == np.int32 or dtype == int or dtype == np.int64:
            return (Sys.Int32, lambda i: Sys.Int32(i))
        elif dtype == bool or dtype == np.bool_:
            return (Sys.Boolean, lambda b: Sys.Boolean(b))
        else:
            raise Exception(f"Python type not matching any dotnet type. Type was {type(dtype)}")

    def get_python_type(self, net_type):
        return self._net_to_np_map[net_type][0]

    def get_other_type(self, numpy_type):
        return self._np_to_net_map(numpy_type)[0]

    def convert_from_python_enumerable(self, np_array, object_array = False):
        np_type = self._find_element_type(np_array)
        net_type, convert_fun = self._np_to_net_map(np_type)          

        n = len(np_array)
        
        if object_array:
            net_array = _system().Array.CreateInstance(_system().Object, n)
        else:
            net_array = _system().Array.CreateInstance(net_type, n)
            
        for i, elm in enumerate(np_array):
            net_array[i] = convert_fun(elm)

        return net_array

    def convert_to_python_enumerable(self, net_type, net_array):
        str_net_type = str(net_type)
        if str_net_type in self._net_to_np_map or type(net_array[0]) in self._net_to_np_map:
            np_type, convert_fun = self._net_to_np_map[str_net_type]            
        else:
            raise PythonToolException('Unknown type ' + str_net_type)
        
        n = len(net_array)
        np_array = np.ndarray((n,), dtype = np_type)
        for i, elm in enumerate(net_array):
            np_array[i] = convert_fun(elm)

        return np_array

    def _find_element_type(self, array):
        i = 0
        element_type = None
        n = len(array)
        while i < n and not element_type:
            if not array[i] is None:
                element_type = type(array[i])
            i += 1

        return element_type

    def to_dataframe(self, properties_data):
        df_columns = {}
        dtypes = {}
        indices = None
        for property_data in properties_data:
            if property_data.Indices:
                indices = property_data.Indices

            name = property_data.Name
            values = property_data.Values
            net_type = property_data.DataType

            df_columns[name] = self.convert_to_python_enumerable(net_type, values)
            dtypes[name] = str(net_type)

        df = pd.DataFrame(df_columns)
        if indices: 
            df = df.set_index(pd.Index(indices))
        
        df = self.cast_dataframe(df, dtypes)
        return df

    def cast_dataframe(self, df, dtypes):
        import numpy as np
        for name in list(df):
            if dtypes[name] == 'System.String':
                df[name] = df[name].astype(str)
            if dtypes[name] == 'System.Single' or dtypes[name] == 'System.Double':
                df[name] = df[name].astype(np.float64)
            if dtypes[name] == 'System.Int32':
                df[name] = df[name].astype(np.int32)
            if dtypes[name] == 'System.Boolean':
                df[name] = df[name].astype(bool)
            if dtypes[name] == 'System.DateTime':
                df[name] = pd.to_datetime(df[name])
        return df