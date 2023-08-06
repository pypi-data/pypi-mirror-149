# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc
from . import grid_grpc

import collections
from datetime import datetime

from cegalprizm.pythontool.ooponly.ptutils import Utils

from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.ooponly.ip_oop_transition import Tuple2

import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.gridproperty_hub import GridPropertyHub
class GridPropertyGrpc(PetrelObjectGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection", sub_type: str = 'grid property'):
        super(GridPropertyGrpc, self).__init__(sub_type, guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content = {}
        self._channel = typing.cast("GridPropertyHub", petrel_connection._service_grid_property)

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

    def _extent(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.GridProperty_Extent(request)

    def _request_extent(self):
        self._invariant_content['extent'] = self._extent()  

    def GetParentPythonGridObject(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        parent_guid = self._channel.GridProperty_ParentGrid(request).value
        if not parent_guid:
            return None
        return grid_grpc.GridGrpc(parent_guid, self._plink)      

    def GetDate(self) -> typing.Optional[datetime]:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        date = self._channel.GridProperty_GetDate(request).t
        if date == 0:
            return None
        return datetime.fromtimestamp(date)

    def GetUpscaledCells(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        reply = self._channel.GridProperty_GetUpscaledCells(request)
        indices_ar = reply.indices_array
        n = len(indices_ar)
        indices = [None] * n
        Indices = collections.namedtuple('Indices', 'Item1 Item2 Item3')
        for m in range(n):
            inds = indices_ar[m]
            indices[m] = Indices(Item1=inds.i, Item2=inds.j, Item3=inds.k)

        return indices

    def SetUpscaledCells(self, ii, jj, kk):
        self.write_test()
        self._plink._opened_test()
        n = len(ii)
        inds = [None] * n
        for m in range(n):
            inds[m] = petrelinterface_pb2.Primitives.Indices3(i = ii[m], j = jj[m], k = kk[m])
        
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.SetIndicesArray_Request(
            guid = po_guid,
            indices_array = inds)
        return self._channel.GridProperty_SetUpscaledCells(request)

    def GetDisplayUnitSymbol(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.GridProperty_DisplayUnitSymbol(request).value

    def GetColumn(self, i, j):
        return self.GetChunk((i,i), (j,j), None, spanning_dims = petrelinterface_pb2.SPANNING_K)

    def GetLayer(self, k):
        return self.GetChunk(None, None, (k,k), spanning_dims = petrelinterface_pb2.SPANNING_IJ)

    def GetAll(self):
        return self.GetChunk(None, None, None)
        
    def GetChunk(self, range_i, range_j, range_k, spanning_dims = petrelinterface_pb2.SPANNING_IJK):
        self._plink._opened_test()
        return Utils.grpc_get_subchunk(
            self, 
            self._channel.GridProperty_GetChunk,
            self._plink, 
            spanning_dims, 
            range_i, 
            range_j, 
            range_k
        )

    def SetAll(self, sub_chunks):
        self.SetChunk(None, None, None, sub_chunks)
    
    def SetLayer(self, k, sub_chunks):
        self.SetChunk(None, None, (k, k), sub_chunks)

    def SetColumn(self, i, j, sub_chunks):        
        self.SetChunk((i,i), (j,j), None, sub_chunks)
    
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
            self._channel.GridProperty_StreamSetChunk,
            shift_start_i, 
            shift_start_j, 
            shift_start_k
        )

    def GetParentPropertyCollection(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        parent_guid = self._channel.GridProperty_GetParentPropertyCollection(request).value
        return PropertyCollectionGrpc(parent_guid, self._plink)        


class GridDiscretePropertyGrpc(GridPropertyGrpc):

    def __init__(self, guid, petrel_connection):
        super(GridDiscretePropertyGrpc, self).__init__(guid, petrel_connection, sub_type = 'grid discrete property')

    def GetAllDictionaryCodes(self) -> typing.List[Tuple2]:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        values = self._channel.GridDictionaryProperty_GetAllDictionaryCodes(request).values
        collection = []
        for pair in values:
            collection.append(Tuple2(pair.item1, pair.item2))

        return collection


class PropertyCollectionGrpc(PetrelObjectGrpc):

    def __init__(self, guid, petrel_connection):
        super(PropertyCollectionGrpc, self).__init__('property collection', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = petrel_connection._service_grid_property

    def GetPropertyObjects(self):
        return self._get_property_opbjects(False)    
    
    def GetDictionaryPropertyObjects(self):
        return self._get_property_opbjects(True)    

    def _get_property_opbjects(self, discrete):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.Properties_Request(
            guid = po_guid,
            discrete = discrete
        )
        reply_properties = self._channel.PropertyCollection_GetPropertyObjects(request)
        property_guids = [guid.guid for guid in reply_properties.guids]
        
        properties = []
        for guid in property_guids:
            if discrete:
                properties.append(GridDiscretePropertyGrpc(guid, self._plink))
            else:
                properties.append(GridPropertyGrpc(guid, self._plink))
            
        return properties
