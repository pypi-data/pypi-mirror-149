# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from . import petrelobject_grpc
from . import gridproperty_grpc

from cegalprizm.pythontool.grpc import petrelinterface_pb2

from cegalprizm.pythontool.grpc.petrelinterface_pb2 import Primitives as ProtobufPrimitives
from cegalprizm.pythontool.ooponly.ip_oop_transition import Range
from cegalprizm.pythontool.ooponly.ip_oop_transition import Ranges
from cegalprizm.pythontool.ooponly.ip_oop_transition import Value3
from cegalprizm.pythontool.ooponly.ip_oop_transition import ValuePoint
from cegalprizm.pythontool.ooponly.ip_oop_transition import ValuePoints

import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.grid_hub import GridHub

class GridGrpc(petrelobject_grpc.PetrelObjectGrpc):

    """
    Methods with C# style names share their signature with methods of Grid._petrel_object_link
    """

    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(GridGrpc, self).__init__('grid', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content = {}
        self._channel = typing.cast("GridHub", petrel_connection._service_grid)
        
    def NumI(self):
        if not 'extent' in self._invariant_content:
            self._request_extent()
        return self._invariant_content['extent'].i

    def NumJ(self):
        if not 'extent' in self._invariant_content:
            self._request_extent()
        return self._invariant_content['extent'].j

    def NumK(self):
        if not 'extent' in self._invariant_content:
            self._request_extent()
        return self._invariant_content['extent'].k

    def _request_extent(self):
        self._invariant_content['extent'] = self._grid_extent(self._guid)
    
    def GetCellAtPoint(self, x, y, z):
        self._plink._opened_test()
        position = ProtobufPrimitives.Double3(x = x, y = y, z = z)
        request = petrelinterface_pb2.Grid_IndicesOfCell_Request(guid = self._guid, position = position)
        indices = self._channel.Grid_IndicesOfCell(request)
        return ValuePoint(Value3(indices.i, indices.j, indices.k)) if indices.exist else None
        
    def GetCellCenter(self, i, j, k):
        self._plink._opened_test()
        indices = ProtobufPrimitives.Indices3(i = i, j = j, k = k)
        request = petrelinterface_pb2.Grid_PositionOfCellCenter_Request(guid = self._guid, indices = indices)
        pos = self._channel.Grid_PositionOfCellCenter(request)
        return ValuePoint(Value3(pos.x, pos.y, pos.z)) if pos.exist else None
        
    def GetCellCorners(self, i, j, k):
        self._plink._opened_test()
        indices = ProtobufPrimitives.Indices3(i = i, j = j, k = k)
        request = petrelinterface_pb2.Grid_VerticesPositions_Request(guid = self._guid, indices = indices)
        reply = self._channel.Grid_VerticesPositions(request)
        if len(reply.point_list) == 0:
            return None

        valuePoints = ValuePoints()
        [valuePoints.append(Value3(point.x, point.y, point.z)) for point in reply.point_list]
        return valuePoints
        
    def AxesRange(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        axes = self._channel.Grid_AxesRange(request)
        ranges = Ranges(Range(axes.range_x.value1, axes.range_x.value2), \
                 Range(axes.range_y.value1, axes.range_y.value2), \
                 Range(axes.range_z.value1, axes.range_z.value2))
        return ranges

    def IsCellDefined(self, i, j, k):
        self._plink._opened_test()
        if i < 0 or j < 0 or k < 0:
            return False

        indices = ProtobufPrimitives.Indices3(i = i, j = j, k = k)
        request = petrelinterface_pb2.Grid_IsCellDefined_Request(guid = self._guid, indices = indices)
        reply = self._channel.Grid_IsCellDefined(request)
        return reply.value

    def _grid_extent(self, guid):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = guid)
        return self._channel.Grid_Extent(request)

    def GetIjk(self, x: typing.List[float], y: typing.List[float], z: typing.List[float]) -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        self._plink._opened_test()

        request = petrelinterface_pb2.Grid_GetIjk_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , x = [v for v in x]
            , y = [v for v in y]
            , z = [v for v in z]
        )

        response = self._channel.Grid_GetIjk(request)
             
        return ([i for i in response.i], [j for j in response.j], [k for k in response.k])

    
    def GetPositions(self, i: typing.List[float], j: typing.List[float], k: typing.List[float]) -> \
            typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        self._plink._opened_test()

        request = petrelinterface_pb2.Grid_GetPositions_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , i = [v for v in i]
            , j = [v for v in j]
            , k = [v for v in k]
        )

        response = self._channel.Grid_GetPositions(request)
             
        return ([x for x in response.x], [y for y in response.y], [z for z in response.z])

    def GetProperties(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.Grid_GetProperties_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.Grid_GetProperties(request)
        return [gridproperty_grpc.GridPropertyGrpc(item.GetProperty.guid, self._plink) for item in responses]

    def GetDictionaryProperties(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.Grid_GetDictionaryProperties_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        responses = self._channel.Grid_GetDictionaryProperties(request)
        return [gridproperty_grpc.GridDiscretePropertyGrpc(item.GetDictionaryProperty.guid, self._plink) for item in responses]

    def GetNumberOfGridProperties(self) -> int:
        self._plink._opened_test()
        request = petrelinterface_pb2.Grid_GetNumberOfGridProperties_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._channel.Grid_GetNumberOfGridProperties(request)
        return response.GetNumberOfGridProperties