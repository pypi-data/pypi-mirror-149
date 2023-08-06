# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import typing

import requests
from cegalprizm.pythontool.ooponly.ptutils import Utils

from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.exceptions import PythonToolException

import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.petrelobject import PetrelObject
    from cegalprizm.pythontool.oophub.petrelobject_hub import PetrelObjectHub
class PetrelObjectGrpc:

    def __init__(self, sub_type: str, guid: str, petrel_connection: "PetrelConnection"):
        self._sub_type = sub_type
        self._guid = guid
        self._plink = petrel_connection
        self._invariant_content: typing.Dict[str, typing.Any] = {}
        self._base_channel = typing.cast("PetrelObjectHub", petrel_connection._service_petrel_object)
        self._domain_object: typing.Optional["PetrelObject"] = None
        
    @property
    def domain_object(self):
        return self._domain_object # Is set by constructor of associated PetrelObject

    @property
    def readonly(self):
        return self.domain_object.readonly

    def IsAlwaysReadonly(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObject_IsAlwaysReadonly_Request(guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid))
        return self._base_channel.PetrelObject_IsAlwaysReadonly(request).IsAlwaysReadonly

    def write_test(self):
        if self.domain_object.readonly:
            raise PythonToolException(f"{self.domain_object.path} is readonly")
    

    def GetPetrelName(self) -> str:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._base_channel.PetrelObject_GetPetrelName(request).value 
    
    def GetPath(self) -> str:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._base_channel.PetrelObject_GetPath(request).value 
    
    def GetDroidString(self) -> str:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._base_channel.PetrelObject_GetDroidString(request).value

    def RetrieveStats(self) -> typing.Dict[str, str]:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        reply = self._base_channel.PetrelObject_RetrieveStats(request)
        return Utils.protobuf_map_to_dict(reply.string_to_string_map, {})

    def GetOceanType(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        return self._base_channel.PetrelObject_GetOceanType(request).value  

    def ClonePetrelObject(self, path_of_clone, copy_values):
        already_exist = self._plink._get(self._sub_type, path_of_clone) is not None
        if already_exist:
            raise Exception(f'{self._sub_type.capitalize()} Petrel object with path "{path_of_clone}" already exist.')

        name = path_of_clone.split('/')[-1]
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.Clone_Request(
            guid = po_guid,
            name = name,
            sub_type = self._sub_type,
            copy_values = copy_values
        )
        reply = self._base_channel.PetrelObject_Clone(request)
        clone_guid = reply.guid
        if not clone_guid:
            return None

        clone = self._plink._get(self._sub_type, clone_guid)
        clone.readonly = False
        return clone
        
    def RetrieveHistory(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.PetrelObject_RetrieveHistory_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._base_channel.PetrelObject_RetrieveHistory(request)
        
        merged_list = [item for sublist in responses for item in sublist.RetrieveHistory]
        n = len(merged_list) // 4
        if n > 0:
            return [merged_list[i:i + n] for i in range(0, len(merged_list), n)]
        else:
            return 4*[[]]

    def GetTemplate(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObject_GetTemplate_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        return self._base_channel.PetrelObject_GetTemplate(request).GetTemplate