# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.ooponly.ptutils import Utils
from cegalprizm.pythontool.grpc import utils as grpc_utils

from cegalprizm.pythontool.grpc.petrelinterface_pb2 import Primitives as ProtobufPrimitives
from cegalprizm.pythontool.ooponly.ip_oop_transition import Value3
from cegalprizm.pythontool.ooponly.ip_oop_transition import ValuePoint

from .petrelobject_grpc import PetrelObjectGrpc

import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.horizon_hub import HorizonHub, HorizonInterpretationHub

class HorizonProperty3dGrpc(PetrelObjectGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection", sub_type:str = 'horizon property 3d'):
        super(HorizonProperty3dGrpc, self).__init__(sub_type, guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content = {}
        self._channel = typing.cast("HorizonHub", petrel_connection._service_horizon)

    @property
    def ReadOnly(self):
        return False

    def NumI(self):
        if not 'extent' in self._invariant_content:
            self._request_extent()
        return self._invariant_content['extent'].i

    def NumJ(self):
        if not 'extent' in self._invariant_content:
            self._request_extent()
        return self._invariant_content['extent'].j

    def NumK(self):
        return 1

    def _request_extent(self):
        self._invariant_content['extent'] = self._extent(self._channel.HorizonProperty3d_Extent)

    def _extent(self, rpc_func):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return rpc_func(request)

    def IndexAtPosition(self, x, y):
        return self._IndexAtPosition(self._channel.HorizonProperty3d_IndexAtPosition, x, y)
        
    def _IndexAtPosition(self, rpc_func, x, y):
        self._plink._opened_test()
        position = ProtobufPrimitives.Double3(x = x, y = y, z = 0)
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.IndexAtPosition_Request(guid = po_guid, position = position)
        inds = rpc_func(request)
        return ValuePoint(Value3(inds.i, inds.j, None)) if inds.exist else None

    def PositionAtIndex(self, i, j):
        return self._PositionAtIndex(self._channel.HorizonProperty3d_PositionAtIndex, i, j)

    def _PositionAtIndex(self, rpc_func, i, j):
        self._plink._opened_test()
        indices = ProtobufPrimitives.Indices3(i = i, j = j, k = 0)
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PositionAtIndex_Request(guid = po_guid, cell_indices = indices)
        pos = rpc_func(request)        
        return ValuePoint(Value3(pos.x, pos.y, pos.z)) if pos.exist else None

    def GetDisplayUnitSymbol(self):
        return self._GetDisplayUnitSymbol(self._channel.HorizonProperty3d_DisplayUnitSymbol)

    def _GetDisplayUnitSymbol(self, rpc_func):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return rpc_func(request).value

    def GetChunk(self, range_i, range_j):
        return self._GetChunk(
            self._channel.HorizonProperty3d_GetChunk,
            range_i,
            range_j)

    def _GetChunk(self, rpc_get_chunk, range_i, range_j):
        self._plink._opened_test()
        return Utils.grpc_get_subchunk(
            self, 
            rpc_get_chunk,
            self._plink, 
            petrelinterface_pb2.SPANNING_IJ, 
            range_i, 
            range_j, 
            None
        )

    def SetChunk(self, range_i, range_j, np_array):
        return self._SetChunk(
            self._channel.HorizonProperty3d_StreamSetChunk,
            range_i,
            range_j,
            np_array)

    def _SetChunk(self, rpc_stream_set_chunk, range_i, range_j, np_array):
        self.write_test()
        self._plink._opened_test()
        shift_start_i = range_i[0] if range_i else 0
        shift_start_j = range_j[0] if range_j else 0
        Utils.grpc_set_subchunk(
            self._guid, 
            self._plink, 
            np_array,
            rpc_stream_set_chunk, 
            shift_start_i, 
            shift_start_j, 
            0)

    def GetIjk(self, x, y):
        self._plink._opened_test()

        request = petrelinterface_pb2.HorizonProperty3d_GetIjk_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , x = [v for v in x]
            , y = [v for v in y]
        )

        response = self._channel.HorizonProperty3d_GetIjk(request)
             
        return [[i for i in response.i], [j for j in response.j]]
    

    def GetPositions(self, i, j):
        self._plink._opened_test()

        request = petrelinterface_pb2.HorizonProperty3d_GetPositions_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , i = [v for v in i]
            , j = [v for v in j]
        )

        response = self._channel.HorizonProperty3d_GetPositions(request)
             
        return [[x for x in response.x], [y for y in response.y], [z for z in response.z]]

    def GetParentHorizonInterpretation3d(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.HorizonProperty3d_GetParentHorizonInterpretation3d_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.HorizonProperty3d_GetParentHorizonInterpretation3d(request)
             
        return grpc_utils.pb_PetrelObjectRef_to_grpcobj(response.GetParentHorizonInterpretation3d, self._plink) if response.GetParentHorizonInterpretation3d.guid else None
    


class HorizonInterpretation3dGrpc(HorizonProperty3dGrpc):
    
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(HorizonInterpretation3dGrpc, self).__init__(guid, petrel_connection, sub_type = 'horizon interpretation 3d')
        self._guid = guid
        self._plink = petrel_connection
        self._channel = typing.cast("HorizonHub", petrel_connection._service_horizon)

    @property
    def ReadOnly(self):
        return False

    def SampleCount(self) -> int:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.HorizonInterpretation3d_SampleCount(request).value 

    def _request_extent(self):
        self._invariant_content['extent'] = self._extent(self._channel.HorizonInterpretation3d_Extent)

    def IndexAtPosition(self, x, y):
        return self._IndexAtPosition(self._channel.HorizonInterpretation3d_IndexAtPosition, x, y)
        
    def PositionAtIndex(self, i, j):
        return self._PositionAtIndex(self._channel.HorizonInterpretation3d_PositionAtIndex, i, j)

    def GetDisplayUnitSymbol(self):
        return self._GetDisplayUnitSymbol(self._channel.HorizonInterpretation3d_DisplayUnitSymbol)

    def GetChunk(self, range_i, range_j):
        return self._GetChunk(
            self._channel.HorizonInterpretation3d_GetChunk,
            range_i,
            range_j)

    def SetChunk(self, range_i, range_j, np_array):
        return self._SetChunk(
            self._channel.HorizonInterpretation3d_StreamSetChunk,
            range_i,
            range_j,
            np_array)

    def GetAllHorizonPropertyValues(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        response = self._channel.HorizonInterpretation3d_GetAllHorizonPropertyValues(request)
        return [HorizonProperty3dGrpc(
            petrel_object.guid,
            petrel_connection = self._plink)
            for petrel_object in response.guids]

    def GetParent(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.HorizonInterpretation3d_GetParent_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.HorizonInterpretation3d_GetParent(request)
             
        return HorizonInterpretationGrpc(response.GetParent.guid, self._plink) if response.GetParent.guid else None 


    def GetIjk(self, x, y):
        self._plink._opened_test()

        request = petrelinterface_pb2.HorizonInterpretation3d_GetIjk_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , x = [v for v in x]
            , y = [v for v in y]
        )

        response = self._channel.HorizonInterpretation3d_GetIjk(request)
             
        return [[i for i in response.i], [j for j in response.j]]
    
    def GetPositions(self, i, j):
        self._plink._opened_test()

        request = petrelinterface_pb2.HorizonInterpretation3d_GetPositions_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , i = [v for v in i]
            , j = [v for v in j]
        )

        response = self._channel.HorizonInterpretation3d_GetPositions(request)
             
        return [[x for x in response.x], [y for y in response.y], [z for z in response.z]]
    


class HorizonInterpretationGrpc(PetrelObjectGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(HorizonInterpretationGrpc, self).__init__('horizon interpretation', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = typing.cast("HorizonInterpretationHub", petrel_connection._service_horizon_interpretation)

    def __str__(self):
        return 'HorizonInterpretation(petrel_name="{}")'.format(self.GetPetrelName())

    def GetHorizonInterpretation3dObjects(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.HorizonInterpretation_GetHorizonInterpretation3dObjects_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._channel.HorizonInterpretation_GetHorizonInterpretation3dObjects(request)
        
        return [HorizonInterpretation3dGrpc(item.guid, self._plink) if item.guid else None for sublist in responses for item in sublist.GetHorizonInterpretation3dObjects]

