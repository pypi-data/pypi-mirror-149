# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class PetrelObjectHub(BaseHub):
    def GetPetrelObjectGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetPetrelObjectGrpc", PetrelObjectRef, msg) # type: ignore
    
    def PetrelObject_GetPetrelName(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.PetrelObject_GetPetrelName", ProtoString, msg) # type: ignore
    
    def PetrelObject_GetPath(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.PetrelObject_GetPath", ProtoString, msg) # type: ignore
    
    def PetrelObject_GetDroidString(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.PetrelObject_GetDroidString", ProtoString, msg) # type: ignore
    
    def PetrelObject_RetrieveStats(self, msg) -> StringsMap:
        return self._unary_wrapper("cegal.pythontool.PetrelObject_RetrieveStats", StringsMap, msg) # type: ignore
    
    def PetrelObject_GetReadOnly(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.PetrelObject_GetReadOnly", ProtoBool, msg) # type: ignore
    
    def PetrelObject_Clone(self, msg) -> PetrelObjectGuid:
        return self._unary_wrapper("cegal.pythontool.PetrelObject_Clone", PetrelObjectGuid, msg) # type: ignore
    
    def PetrelObject_IsAlwaysReadonly(self, msg) -> PetrelObject_IsAlwaysReadonly_Response:
        return self._unary_wrapper("cegal.pythontool.PetrelObject_IsAlwaysReadonly", PetrelObject_IsAlwaysReadonly_Response, msg) # type: ignore
    
    def PetrelObject_GetOceanType(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.PetrelObject_GetOceanType", ProtoString, msg) # type: ignore
    
    def PetrelObject_RetrieveHistory(self, msg) -> typing.Iterable[PetrelObject_RetrieveHistory_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.PetrelObject_RetrieveHistory", PetrelObject_RetrieveHistory_Response, msg) # type: ignore
    
    def PetrelObject_GetTemplate(self, msg) -> PetrelObject_GetTemplate_Response:
        return self._unary_wrapper("cegal.pythontool.PetrelObject_GetTemplate", PetrelObject_GetTemplate_Response, msg) # type: ignore