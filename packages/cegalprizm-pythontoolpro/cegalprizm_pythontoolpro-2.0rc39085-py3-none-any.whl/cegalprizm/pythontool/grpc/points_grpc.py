# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc

from cegalprizm.pythontool.grpc import petrelinterface_pb2
from datetime import datetime
from distutils.util import strtobool

from math import ceil
import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.points_hub import PointsHub

class PointSetGrpc(PetrelObjectGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(PointSetGrpc, self).__init__('pointset', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = typing.cast("PointsHub", petrel_connection._service_points)
        self._table_handler = PropertyTableHandler(self._guid, self._plink, self._channel, 'pointset')
        self._property_range_handler = PropertyRangeHandler()
    
    def GetPositionValuesByInds(self, indices):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndices(guid = po_guid, indices = indices)
        responses = self._channel.PointSet_GetPositionValuesByInds(request)
        return self._property_range_handler.get_dataframe(responses)
        
    def GetPropertiesValuesByInds(self, indices):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndices(guid = po_guid, indices = indices)
        responses = self._channel.PointSet_GetPropertiesValuesByInds(request)
        return self._property_range_handler.get_dataframe(responses)

    def GetPositionValuesByRange(self, start, end, step, xRange, yRange, zRange, maxNumberOfPoints):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuidAndRange(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type),
            start = start,
            end = end,
            step = step,
            max_number_of_points = maxNumberOfPoints
        )
        if not xRange is  None and len(xRange) == 2:
            request.x_range.x = xRange[0]
            request.x_range.y = xRange[1]
        if not yRange is  None and len(yRange) == 2:
            request.y_range.x = yRange[0]
            request.y_range.y = yRange[1]
        if not zRange is  None and len(zRange) == 2:
            request.z_range.x = zRange[0]
            request.z_range.y = zRange[1]

        responses = self._channel.PointSet_GetPositionValuesByRange(request)
        return self._property_range_handler.get_dataframe(responses)

    def AddProperty(self, name, dtype):
        self._plink._opened_test()

        if  dtype == "String":
            datatype = petrelinterface_pb2.PointPropertyType.STRING
        elif dtype == "DateTime":
            datatype = petrelinterface_pb2.PointPropertyType.DATETIME
        elif dtype == "Double" or dtype == "Single":
            datatype = petrelinterface_pb2.PointPropertyType.DOUBLE_FLOAT
        elif dtype == "Int32":
            datatype = petrelinterface_pb2.PointPropertyType.INT 
        elif dtype == "Boolean":
            datatype = prop_type = petrelinterface_pb2.PointPropertyType.BOOL

        request = petrelinterface_pb2.AddProperty_request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type),
            name = name,
            type = datatype
        )
        return self._channel.PointSet_AddProperty(request)
        
    def AttributesInfo(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.PointSet_AttributesInfo(request)

    def AddPoints(self, xs, ys, zs):
        self._plink._opened_test()
        request = petrelinterface_pb2.AddPoints_request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type),
            xs = xs,
            ys = ys,
            zs = zs
        )
        return self._channel.PointSet_AddPoints(request).value

    def DeletePoints(self, indices):
        self._plink._opened_test()
        request = petrelinterface_pb2.DeletePoints_request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type), 
            indices = indices
        )
        return self._channel.PointSet_DeletePoints(request).value

    def SetPropertyValues(self, uniquePropertyName, indexes, vals):
        self._plink._opened_test()
        import time
        t = self._property_range_handler.get_property_range_datas(uniquePropertyName, indexes, vals)
        iterable_requests = [
            petrelinterface_pb2.SetPropertiesValues_Request(
                    guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type), 
                    data = prd
                    )
            for prd in self._property_range_handler.get_property_range_datas(uniquePropertyName, indexes, vals)
        ]
        ok = self._channel.PointSet_SetPropertyValues((v for v in iterable_requests))
        return ok.value

    def OrderedUniquePropertyNames(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.PointSet_OrderedUniquePropertyNames(request).values

    def GetDisplayUnitSymbol(self, idx):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndex(
            guid = po_guid,
            index = idx
        )
        return self._channel.PointSet_DisplayUnitSymbol(request).value
        
    def GetPointCount(self) -> int:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)        
        return self._channel.PointSet_GetPointCount(request).value 

    def GetPropertyCount(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)        
        return self._channel.PointSet_GetPropertyCount(request).value

class PropertyRangeHandler(object):

    def __init__(self, number_of_streamed_elements = 1024):
        self.number_of_streamed_elements = number_of_streamed_elements

    def _point_property_type(self, value):
        import numpy as np
        if 'float' in str(type(value)).lower():
            prop_type = petrelinterface_pb2.PointPropertyType.DOUBLE_FLOAT
        elif type(value) is int or type(value) is np.int64 or type(value) is np.int32:
            prop_type = petrelinterface_pb2.PointPropertyType.INT
        elif type(value) is datetime or type(value) is np.datetime64:
            prop_type = petrelinterface_pb2.PointPropertyType.DATETIME
        elif type(value) is str: 
            prop_type = petrelinterface_pb2.PointPropertyType.STRING
        elif type(value) is bool or type(value) is np.bool_:
            prop_type = petrelinterface_pb2.PointPropertyType.BOOL
        else:
            raise Exception("Value is not recognized")
        return prop_type

    def get_dataframe(self, responses):
        import pandas as pd
        data = {}
        dtypes = {}
        for property_data in responses:
            indices = [int(v) for v in property_data.indices] #SLOW
            name = property_data.name
            string_values = property_data.values
            value_type = property_data.data_type
            converter = self.get_from_grpc_converter(value_type)
            values = [converter(v) for v in string_values] #slow
            if not name in data:
                data[name] = {
                    "index" : indices,
                    "values" : values
                }
                dtypes[name] = value_type
            else:
                data[name]["index"] += indices
                data[name]["values"] += values
        
        df = None
        for key, val in data.items():
            if not df is None :
                df = pd.merge(df, pd.DataFrame({key:val["values"]}, index=val["index"]), left_index = True, right_index=True)
            else: 
                df = pd.DataFrame({key:val["values"]}, index=val["index"])

        df = self.cast_dataframe(df, dtypes)
        return df

    def cast_dataframe(self, df, dtypes):
        if df is None:
            return
        import numpy as np
        import pandas as pd
        for name in list(df):
            if dtypes[name] == petrelinterface_pb2.STRING:
                df[name] = df[name].astype(str)
            if dtypes[name] == petrelinterface_pb2.SINGLE_FLOAT or dtypes[name] == petrelinterface_pb2.DOUBLE_FLOAT:
                df[name] = df[name].astype(np.float64)
            if dtypes[name] == petrelinterface_pb2.INT:
                df[name] = df[name].astype(np.int32)
            if dtypes[name] == petrelinterface_pb2.BOOL:
                df[name] = df[name].astype(bool)
            if dtypes[name] == petrelinterface_pb2.DATETIME:
                df[name] = pd.to_datetime(df[name])
        return df


    def _serialize_value_to_string(self, value):
        import numpy as np
        import pandas as pd
        if 'float' in str(type(value)).lower():
            float_string = str(value)
            if float_string == "nan":
                return "NaN"
            return float_string
        elif type(value) is int or type(value) is np.int64 or type(value) is np.int32:
            return str(value)
        elif type(value) is str: 
            return str(value)
        elif type(value) is bool or type(value) is np.bool_:
            return str(value)
        elif type(value) is np.datetime64:
            dt = pd.Timestamp(value)
            if pd.isnull(dt):
                ret = "1/1/1/0/0/0"
            else:
                ret = "{}/{}/{}/{}/{}/{}".format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            return ret
        else:
            raise Exception("Value is not recognized")

    def get_from_grpc_converter(self, value_type):
        if value_type == petrelinterface_pb2.STRING:
            return lambda x: x
        if value_type == petrelinterface_pb2.SINGLE_FLOAT or value_type == petrelinterface_pb2.DOUBLE_FLOAT:
            return  lambda x: float(x)
        if value_type == petrelinterface_pb2.INT:
            return lambda x: int(x)
        if value_type == petrelinterface_pb2.BOOL:
            return lambda x: bool(strtobool(x))
        if value_type == petrelinterface_pb2.DATETIME:
            def datetimeconverter(date_string):
                if date_string == "1/1/1/0/0/0":
                    return None
                date_ints = [int(v) for v in date_string.split("/")]
                year, month, day, hour, minute, second = date_ints
                return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
            return datetimeconverter

    def chunk(self, lst, n):
        result = []
        for i in range(0, len(lst), n):
            start = i
            end = min(start+n, len(lst))
            result.append(lst[start:end])
        return result

    def get_property_range_datas(self, uniquePropertyName, indexes, vals):
        result = []
        for _ind, _val in zip(self.chunk(indexes, self.number_of_streamed_elements), self.chunk(vals, self.number_of_streamed_elements)):
            result.append(petrelinterface_pb2.PropertyRangeData(
                name = uniquePropertyName,
                indices = _ind,
                values = [self._serialize_value_to_string(v) for v in _val],
                data_type = self._point_property_type(_val[0])
            )) 
        return result

    def _find_element_type(self, array):
        i = 0
        element_type = None
        n = len(array)
        while i < n and not element_type:
            if not array[i] is None:
                element_type = type(array[i])
            i += 1

class PropertyTableHandler:
    def __init__(self, guid, plink, channel, sub_type):
        self._guid = guid
        self._plink = plink
        self._channel = channel
        self._sub_type = sub_type

    def write_properties_table(self, values):
        self._plink._opened_test()
        no_rows = len(values)
        no_cols = len(values[0])

        no_columns_per_streamed_unit = self._no_columns_per_streamed_unit(no_rows, no_cols)

        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        start_inds = range(0, no_cols, no_columns_per_streamed_unit)
        iterable_requests = map(
            lambda start_ind : self._setproperties_request(no_rows, no_cols, start_ind, po_guid, values, no_columns_per_streamed_unit),
            start_inds
        )

        return self._channel.PointSetAndPolylineSet_SetPropertiesTable(iterable_requests).value

    def read_properties_table(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        responses = self._channel.PointSetAndPolylineSet_GetPropertiesTable(request)
        no_rows = None
        no_columns = None
        for sub_table in responses:
            
            if not no_rows:
                no_rows = sub_table.no_rows
                no_columns = sub_table.no_columns
                properties_table = [None] * no_rows
                for r in range(no_rows):
                    properties_table[r] = [None] * no_columns
                    
            sub_start_column = sub_table.sub_start_column
            values = sub_table.values_as_string
            value_types = sub_table.value_types
            flat_index = 0
            for r in range(no_rows):
                for c in range(sub_table.sub_no_columns):
                    properties_table[r][sub_start_column + c] = self._convert_from_string(values[flat_index], value_types[flat_index])
                    flat_index += 1
        
        return properties_table

    def _no_columns_per_streamed_unit(self, no_rows, no_cols):
        max_size_bytes = self._plink._preferred_streamed_unit_bytes
        max_no_columns_per_streamed_unit = ceil(max_size_bytes / no_rows / 10)
        no_parts = ceil(no_cols/max_no_columns_per_streamed_unit)
        return ceil(no_cols/no_parts)

    def _setproperties_request(self, no_rows, no_cols, start_column, po_guid, values, no_columns_per_streamed_unit):
        values_as_string_flat = [None] * no_rows * no_columns_per_streamed_unit
        values_type_flat = [None] * no_rows * no_columns_per_streamed_unit
        flat_index = 0
        for r in range(no_rows):
            for c in range(start_column, start_column + no_columns_per_streamed_unit):
                val = self._serialize_value_to_string(values[r][c])
                values_as_string_flat[flat_index] = val
                values_type_flat[flat_index] = self._point_property_type(values[r][c])
                flat_index += 1
            
        return petrelinterface_pb2.SetSubTable_Request(
                guid = po_guid,
                sub_table = petrelinterface_pb2.SubTable(                    
                    sub_start_column = start_column,
                    no_rows = no_rows,
                    no_columns = no_cols,
                    sub_no_columns = no_columns_per_streamed_unit,
                    values_as_string = values_as_string_flat,
                    value_types = values_type_flat
                    )
                )

    def _convert_from_string(self, value_as_string, value_type):
        if value_type == petrelinterface_pb2.STRING:
            return value_as_string
        if value_type == petrelinterface_pb2.SINGLE_FLOAT or value_type == petrelinterface_pb2.DOUBLE_FLOAT:
            return float(value_as_string)
        if value_type == petrelinterface_pb2.INT:
            return int(value_as_string)
        if value_type == petrelinterface_pb2.BOOL:
            return bool(strtobool(value_as_string))
        if value_type == petrelinterface_pb2.DATETIME:
            return datetime.fromtimestamp(int(value_as_string))
        return value_as_string
    
    def _point_property_type(self, value):
        if 'float' in str(type(value)).lower():
            prop_type = petrelinterface_pb2.PointPropertyType.DOUBLE_FLOAT
        elif type(value) is int:
            prop_type = petrelinterface_pb2.PointPropertyType.INT
        elif type(value) is datetime:
            prop_type = petrelinterface_pb2.PointPropertyType.DATETIME
        elif type(value) is str: 
            prop_type = petrelinterface_pb2.PointPropertyType.STRING
        elif type(value) is bool:
            prop_type = petrelinterface_pb2.PointPropertyType.BOOL
        else:
            raise Exception("Value is not recognized")
        return prop_type

    def setpoints_request(self, start_index, po_guid, xs, ys, zs, no_points_per_streamed_unit, idx = None):
        part_xs = xs[start_index:(start_index + no_points_per_streamed_unit)]
        part_ys = ys[start_index:(start_index + no_points_per_streamed_unit)]
        part_zs = zs[start_index:(start_index + no_points_per_streamed_unit)]
        points = petrelinterface_pb2.Points(start_point_index = start_index)
        points.xs[:] = part_xs # pylint: disable=no-member
        points.ys[:] = part_ys # pylint: disable=no-member
        points.zs[:] = part_zs # pylint: disable=no-member
        
        if idx != None:
            return petrelinterface_pb2.SetPolylinePoints_Request(
                guid = po_guid,
                points = points,
                index = idx
            )
        else:
            return petrelinterface_pb2.SetPoints_Request(
                guid = po_guid,
                points = points
            )
    
    def no_points_per_streamed_unit(self, no_points, max_size_bytes):
        max_no_points_per_streamed_unit = ceil(max_size_bytes / 100)
        no_parts = ceil(no_points/max_no_points_per_streamed_unit)
        return ceil(no_points/no_parts)
    
    def set_property(self, property_index, point_index, value):
        self._plink._opened_test()
        prop_type = self._point_property_type(value)
        # if prop_type is None:
        #     return False
        request = self.setproperty_request(property_index, point_index, value)
        return self._channel.PointSetAndPolylineSet_SetProperty(request).value

    def setproperty_request(self, property_index, point_index, value):
        point_property = self._point_property(property_index, point_index, value)
            
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return petrelinterface_pb2.SetPointProperty_Request(
            guid = po_guid,
            property = point_property
        )

    
    def make_setpropertiesvalues_request(self, start_ind, property_index,  po_guid, indices, values, no_points_per_streamed_unit):
        
        start = start_ind*no_points_per_streamed_unit
        end = min(start + no_points_per_streamed_unit, len(indices))

        current_indices = indices[start:end]
        current_values = values[start:end]
        
        propety_range_data = self._make_propertyrangedata(property_index, current_indices, current_values)

        request = petrelinterface_pb2.SetPropertiesValues_Request(
            guid = po_guid,
            data = propety_range_data
        )

        return request
        
    def _serialize_value_to_string(self, value):
        if 'float' in str(type(value)).lower():
            float_string = str(value)
            if float_string == "nan":
                return "NaN"
            return float_string
        elif type(value) is int:
            return str(value)
        elif type(value) is datetime:
            ret = str(int(value.timestamp()))
            return ret
        elif type(value) is str: 
            return str(value)
        elif type(value) is bool:
            return str(value)
        else:
            raise Exception("Value is not recognized")

    def _point_property(self, property_index, point_index, value):
        prop_type = self._point_property_type(value)

        point_property = petrelinterface_pb2.PointSet_Property(
            property_index = property_index,
            point_index = point_index,
            value_as_string = self._serialize_value_to_string(value),
            value_type = prop_type
        )
        return point_property

    def _make_propertyrangedata(self, property_index, indices, values):
        prop_type = self._point_property_type(values[0])

        propertyrangedata = petrelinterface_pb2.PropertyRangeData(
            property_index = property_index,
            indices = indices,
            data_type = prop_type,
            values = [self._serialize_value_to_string(value) for value in values]
        )
        return propertyrangedata

    def set_properties(self, property_index, values):
        self._plink._opened_test()
        no_points = len(values)
        iterable_requests = map(
            lambda point_index : self.setproperty_request(
                property_index,
                point_index,
                values[point_index]
            ),
            range(no_points)
        )

        ok = self._channel.PointSetAndPolylineSet_SetProperties(iterable_requests)
        return ok.value

