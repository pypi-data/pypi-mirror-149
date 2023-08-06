# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import Primitives as ProtobufPrimitives
from cegalprizm.pythontool.ooponly.ip_oop_transition import Range
from cegalprizm.pythontool.ooponly.ip_oop_transition import Ranges
from cegalprizm.pythontool.ooponly.ip_oop_transition import Value3
from cegalprizm.pythontool.ooponly.ip_oop_transition import ValuePoint
from cegalprizm.pythontool.ooponly.ip_oop_transition import Tuple2
from cegalprizm.pythontool.ooponly.ptutils import Utils

from .petrelobject_grpc import PetrelObjectGrpc
import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.surface_hub import SurfaceHub

class SurfaceGrpc(PetrelObjectGrpc):

    """
    Methods with C# style names share their signature with methods of Surface._petrel_object_link
    """

    def __init__(self, guid: str, petrel_connection: "PetrelConnection", sub_type: str = 'surface'):
        super(SurfaceGrpc, self).__init__(sub_type, guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content = {}
        self._channel = typing.cast("SurfaceHub", petrel_connection._service_surface)

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

    def _request_extent(self):
        self._invariant_content['extent'] = self._surface_extent(self._guid)

    def IndexAtPosition(self, x, y):
        self._plink._opened_test()
        position = ProtobufPrimitives.Double3(x = x, y = y, z = 0)
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.IndexAtPosition_Request(guid = po_guid, position = position)
        inds = self._channel.Surface_IndexAtPosition(request)
        return ValuePoint(Value3(inds.i, inds.j, None)) if inds.exist else None

    def PositionAtIndex(self, i, j):
        self._plink._opened_test()
        indices = ProtobufPrimitives.Indices3(i = i, j = j, k = 0)
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PositionAtIndex_Request(guid = po_guid, cell_indices = indices)
        pos = self._channel.Surface_PositionAtIndex(request)        
        return ValuePoint(Value3(pos.x, pos.y, pos.z)) if pos.exist else None

    def AxesRange(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        axes = self._channel.Surface_AxesRange(request)
        ranges = Ranges(Range(axes.range_x.value1, axes.range_x.value2), \
                 Range(axes.range_y.value1, axes.range_y.value2), \
                 Range(axes.range_z.value1, axes.range_z.value2))
        return ranges

    # The Surfaces of the parent, which are the siblings of self._surface including itself
    def ParentSurfaceCollection(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)        
        po_guid = self._channel.Surface_ParentSurfaceCollection(request)
        return SurfaceCollectionGrpc(po_guid.guid, self._plink)

    def GetSurfaceProperties(self):
        self._plink._opened_test()
        return self._getSurfaceProperties(False)
    
    def GetDictionarySurfaceProperties(self):
        self._plink._opened_test()
        return self._getSurfaceProperties(True)

    def _getSurfaceProperties(self, is_discrete):
        obj_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.Properties_Request(guid = obj_guid, discrete = is_discrete)
        po_guids = self._channel.Surface_Properties(request).guids
        guids = [po_guid.guid for po_guid in po_guids]
        properties_collection = []  #PropertyCollection()
        for guid in guids:
            if is_discrete:
                properties_collection.append(SurfaceDiscretePropertyGrpc(guid, self._plink))
            #    surface_attribute = self._plink.get_surface_discrete_attribute(guid.guid)
            else:
                properties_collection.append(SurfacePropertyGrpc(guid, self._plink))
            #    surface_attribute = self._plink.get_surface_attribute(guid.guid)

            #properties_collection.append(SurfacePropertyGrpc(surface_attribute.guid.guid, self._plink))

        return tuple(properties_collection)
        
    def _surface_extent(self, guid):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = guid)
        return self._channel.Surface_Extent(request)
        
    def GetIjk(self, x, y):
        self._plink._opened_test()

        request = petrelinterface_pb2.Surface_GetIjk_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , x = [v for v in x]
            , y = [v for v in y]
        )

        response = self._channel.Surface_GetIjk(request)
             
        return [[i for i in response.i], [j for j in response.j]]
    
    def GetPositions(self, i, j) -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        self._plink._opened_test()

        request = petrelinterface_pb2.Surface_GetPositions_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , i = [v for v in i]
            , j = [v for v in j]
        )

        response = self._channel.Surface_GetPositions(request)
             
        return ([x for x in response.x], [y for y in response.y], [z for z in response.z])
    



class SurfaceCollectionGrpc(PetrelObjectGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection", sub_type = 'surface collection'):
        super(SurfaceCollectionGrpc, self).__init__(sub_type, guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = petrel_connection._service_surface_collection
        
    def GetRegularHeightFieldObjects(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        surface_po_guids = self._channel.SurfaceCollection_GetRegularHeightFieldObjects(request).guids
        guids = [po_guid.guid for po_guid in surface_po_guids]
        return _SurfaceGrpcCollectionIterator(guids, self._plink)

class _SurfaceGrpcCollectionIterator():

    def __init__(self, guids, plink):
        self._guids = iter(guids)
        self._plink = plink
    
    def __iter__(self):
        return self

    def __next__(self):
        return SurfaceGrpc(self._guids.__next__(), self._plink)


class PropertyCollection():
    def __init__(self):
        self._collection = []
        self._ind = -1

    def __iter__(self):
        return self

    def __next__(self):
        self._ind += 1
        if self._ind < len(self._collection):
            return self._ind
        raise StopIteration

    def append(self, surface):
        self._collection.append(surface)

    def get_values(self):
        return self._collection


class SurfacePropertyGrpc(PetrelObjectGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection", sub_type: str = 'surface property'):
        super(SurfacePropertyGrpc, self).__init__(sub_type, guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content = {}
        self._channel = petrel_connection._service_surface_property

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
        return self._channel.SurfaceProperty_Extent(request)
    
    def _request_extent(self):
        self._invariant_content['extent'] = self._extent()  

    def GetDisplayUnitSymbol(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._channel.SurfaceProperty_DisplayUnitSymbol(request).value

    def GetParentSurface(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        parent_guid = self._channel.SurfaceProperty_ParentSurface(request).value
        if not parent_guid:
            return None        
        return SurfaceGrpc(parent_guid, self._plink)

    def GetAllValues(self):
        sub_chunks = self.GetChunk(None, None)
        return sub_chunks

    def GetChunk(self, range_i, range_j):
        self._plink._opened_test()
        return Utils.grpc_get_subchunk(
            self, 
            self._channel.SurfaceProperty_GetChunk,
            self._plink, 
            petrelinterface_pb2.SPANNING_IJ, 
            range_i, 
            range_j, 
            None
        )

    def SetAllValues(self, sub_chunks):
        return self.SetChunk(None, None, sub_chunks)

    def SetChunk(self, range_i, range_j, np_array):
        self._plink._opened_test()
        shift_start_i = range_i[0] if range_i else 0
        shift_start_j = range_j[0] if range_j else 0
        Utils.grpc_set_subchunk(
            self._guid, 
            self._plink, 
            np_array, 
            self._channel.SurfaceProperty_StreamSetChunk,
            shift_start_i, 
            shift_start_j, 
            0)

    def GetIjk(self, x, y):
        self._plink._opened_test()

        request = petrelinterface_pb2.SurfaceProperty_GetIjk_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , x = [v for v in x]
            , y = [v for v in y]
        )

        response = self._channel.SurfaceProperty_GetIjk(request)

        return [[i for i in response.i], [j for j in response.j]]
    
    def GetPositions(self, i, j) -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        self._plink._opened_test()

        request = petrelinterface_pb2.SurfaceProperty_GetPositions_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , i = [v for v in i]
            , j = [v for v in j]
        )

        response = self._channel.SurfaceProperty_GetPositions(request)

        return ([x for x in response.x], [y for y in response.y], [z for z in response.z])
    

class SurfaceDiscretePropertyGrpc(SurfacePropertyGrpc):
       
    def __init__(self, surface_property:str, petrel_connection: "PetrelConnection", sub_type = 'surface discrete property'):
        super(SurfaceDiscretePropertyGrpc, self).__init__(surface_property, petrel_connection, sub_type = sub_type)
        
    def GetAllDictionaryCodes(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        values = self._channel.SurfaceProperty_GetAllDictionaryCodes(request).values
        collection = []
        for pair in values:
            collection.append(Tuple2(pair.item1, pair.item2))

        return tuple(collection)

