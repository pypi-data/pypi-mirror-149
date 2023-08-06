# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.ooponly.ptutils import Utils
from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import Primitives as ProtobufPrimitives
from cegalprizm.pythontool.ooponly.ip_oop_transition import Range
from cegalprizm.pythontool.ooponly.ip_oop_transition import Ranges
from cegalprizm.pythontool.ooponly.ip_oop_transition import Value2
from cegalprizm.pythontool.ooponly.ip_oop_transition import Value3
from cegalprizm.pythontool.ooponly.ip_oop_transition import ValuePoint
import numpy as np

import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.seismic_hub import SeismicHub
    from cegalprizm.pythontool.oophub.seismic2d_hub import Seismic2DHub

class SeismicCubeGrpc(PetrelObjectGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(SeismicCubeGrpc, self).__init__('seismic cube', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content = {}
        self._channel = typing.cast("SeismicHub", petrel_connection._service_seismic)

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
        self._invariant_content['extent'] = self._extent()  

    def _extent(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.SeismicCube_Extent(request)

    def GetDisplayUnitSymbol(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.SeismicCube_DisplayUnitSymbol(request).value

    def IndexAtPosition(self, x, y, z):
        self._plink._opened_test()
        position = ProtobufPrimitives.Double3(x = x, y = y, z = z)
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.IndexAtPosition_Request(guid = po_guid, position = position)
        inds = self._channel.SeismicCube_IndexAtPosition(request)
        return ValuePoint(Value3(inds.i, inds.j, inds.k)) if inds.exist else None

    def PositionAtIndex(self, i, j, k):
        self._plink._opened_test()
        indices = ProtobufPrimitives.Indices3(i = i, j = j, k = k)
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PositionAtIndex_Request(guid = po_guid, cell_indices = indices)
        pos = self._channel.SeismicCube_PositionAtIndex(request)        
        return ValuePoint(Value3(pos.x, pos.y, pos.z)) if pos.exist else None

    def IndexToAnnotation(self, i, j, k):
        self._plink._opened_test()
        indices = ProtobufPrimitives.Indices3(i = i, j = j, k = k)
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.IndexToAnnotation_Request(guid = po_guid, indices = indices)
        inds = self._channel.SeismicCube_IndexToAnnotation(request)        
        return ValuePoint(Value3(inds.i, inds.j, inds.k)) if inds.exist else None

    def AnnotationToIndex(self, inline, crossline, samplenumber):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.AnnotationToIndex_Request(guid = po_guid, inline = inline, crossline = crossline, samplenumber = samplenumber)
        inds = self._channel.SeismicCube_AnnotationToIndex(request)
        return ValuePoint(Value3(inds.i, inds.j, inds.k)) if inds.exist else None

    def AxesRange(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        axes = self._channel.SeismicCube_AxesRange(request)
        ranges = Ranges( 
            Range(axes.range_x.value1, axes.range_x.value2), 
            Range(axes.range_y.value1, axes.range_y.value2), 
            Range(axes.range_z.value1, axes.range_z.value2)
        )
        return ranges

    def GetColumn(self, i, j):
        return self.GetChunk((i,i), (j,j), None, spanning_dims = petrelinterface_pb2.SPANNING_K)
    
    def GetLayer(self, k):
        return self.GetChunk(None, None, (k,k), spanning_dims = petrelinterface_pb2.SPANNING_IJ)
    
    def GetChunk(self, range_i, range_j, range_k, spanning_dims = petrelinterface_pb2.SPANNING_IJK):
        self._plink._opened_test()
        return Utils.grpc_get_subchunk(
            self, 
            self._channel.SeismicCube_GetChunk,
            self._plink, 
            spanning_dims, 
            range_i, 
            range_j, 
            range_k
        )

    def SetColumn(self, i, j, sub_chunks):
        self.SetChunk((i,i), (j,j), None, sub_chunks)

    def SetLayer(self, k, sub_chunks):
        self.SetChunk(None, None, (k,k), sub_chunks)

    def SetChunk(self, range_i, range_j, range_k, np_array):
        self.write_test()
        self._plink._opened_test()

        shift_start_i = range_i[0] if range_i else 0
        shift_start_j = range_j[0] if range_j else 0
        shift_start_k = range_k[0] if range_k else 0
        Utils.grpc_set_subchunk(
            self._guid, 
            self._plink, 
            np_array,
            self._channel.SeismicCube_StreamSetChunk,
            shift_start_i, 
            shift_start_j, 
            shift_start_k
        )

    def GetParentCollectionDroidString(self) -> str:
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        petrel_object_ref = self._channel.SeismicCube_GetParentCollection(po_guid)
        return petrel_object_ref.guid 

    def SetConstantValue(self, val) -> bool:
        self._plink._opened_test()

        request = petrelinterface_pb2.SeismicCube_SetConstantValue_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , val = val
        )

        response = self._channel.SeismicCube_SetConstantValue(request)
             
        return response.SetConstantValue 
    
    def GetIjk(self, x, y, z):
        self._plink._opened_test()

        request = petrelinterface_pb2.SeismicCube_GetIjk_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , x = [v for v in x]
            , y = [v for v in y]
            , z = [v for v in z]
        )

        response = self._channel.SeismicCube_GetIjk(request)

        return [[i for i in response.i], [j for j in response.j], [k for k in response.k]]
    

    def GetPositions(self, i, j, k):
        self._plink._opened_test()

        request = petrelinterface_pb2.SeismicCube_GetPositions_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , i = [v for v in i]
            , j = [v for v in j]
            , k = [v for v in k]
        )

        response = self._channel.SeismicCube_GetPositions(request)
             
        return [[x for x in response.x], [y for y in response.y], [z for z in response.z]]
    

   
    
class Seismic2DGrpc(PetrelObjectGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(Seismic2DGrpc, self).__init__('seismic 2d', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content = {}
        self._channel = typing.cast("Seismic2DHub", petrel_connection._service_seismic_2d)

    def GetDisplayUnitSymbol(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.Seismic2D_DisplayUnitSymbol(request).value

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
        self._invariant_content['extent'] = self._extent()

    def _extent(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.Seismic2D_Extent(request)

    def SetColumn(self, j, chunk):
        self.write_test()
        self._plink._opened_test()           
        Utils.grpc_set_subchunk(
            self._guid, 
            self._plink, 
            chunk, 
            self._channel.Seismic2D_StreamSetChunk, # for grpc streaming upload
            0, 
            j, 
            0
        )

    def GetColumn(self, j):
        self._plink._opened_test()
        chunk = Utils.grpc_get_subchunk(
            self, 
            self._channel.Seismic2D_GetChunk, # stream sub chunks
            self._plink, 
            petrelinterface_pb2.SPANNING_K, 
            None, 
            (j, j), 
            None
        )
        return chunk

    def IndexAtPosition(self, x, y, z):
        self._plink._opened_test()
        position = ProtobufPrimitives.Double3(x = x, y = y, z = z)
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.IndexAtPosition_Request(guid = po_guid, position = position)
        inds = self._channel.Seismic2D_IndexAtPosition(request)
        return ValuePoint(Value2(inds.j, inds.k)) if inds.exist else None

    def PositionAtIndex(self, j, k):
        self._plink._opened_test()
        pair = ProtobufPrimitives.PairInt(value1 = j, value2 = k)
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.Seismic2D_PositionAtIndex_Request(guid = po_guid, indices = pair)
        pos = self._channel.Seismic2D_PositionAtIndex(request)        
        return ValuePoint(Value3(pos.x, pos.y, pos.z)) if pos.exist else None

    def AxesRange(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        axes = self._channel.Seismic2D_AxesRange(request)
        ranges = Ranges( \
                 Range(axes.range_x.value1, axes.range_x.value2), \
                 Range(axes.range_y.value1, axes.range_y.value2), \
                 Range(axes.range_z.value1, axes.range_z.value2))
        return ranges

    def GetParentCollectionDroidString(self) -> str:
        self._plink._opened_test()
        guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        petrel_object_ref = self._channel.Seismic2D_GetParentCollection(guid)
        return petrel_object_ref.guid 


