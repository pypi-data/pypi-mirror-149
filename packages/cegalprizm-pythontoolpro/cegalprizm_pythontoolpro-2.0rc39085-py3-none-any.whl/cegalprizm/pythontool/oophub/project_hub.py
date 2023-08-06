# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class ProjectHub(BaseHub):
    def GetProjectGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetProjectGrpc", PetrelObjectRef, msg) # type: ignore
    
    def VerifyClientVersion(self, msg) -> VersionAccepted:
        return self._unary_wrapper("cegal.pythontool.VerifyClientVersion", VersionAccepted, msg) # type: ignore
    
    def Ping(self, msg) -> ProtoInt:
        return self._unary_wrapper("cegal.pythontool.Ping", ProtoInt, msg) # type: ignore
    
    def GetCurrentProjectName(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.GetCurrentProjectName", ProtoString, msg) # type: ignore
    
    def AProjectIsActive(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.AProjectIsActive", ProtoBool, msg) # type: ignore
    
    def EnableHistory(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.EnableHistory", ProtoBool, msg) # type: ignore
    
    def SetScriptName(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.SetScriptName", ProtoString, msg) # type: ignore
    
    def GetStringsMap(self, msg) -> typing.Iterable[StringsMap]:
        return self._server_streaming_wrapper("cegal.pythontool.GetStringsMap", StringsMap, msg) # type: ignore
    
    def Project_ImportWorkflow(self, msg) -> Project_ImportWorkflow_Response:
        return self._unary_wrapper("cegal.pythontool.Project_ImportWorkflow", Project_ImportWorkflow_Response, msg) # type: ignore
    
    def Project_GetRegisteredObservedDataVersions(self, msg) -> StringsMap:
        return self._unary_wrapper("cegal.pythontool.Project_GetRegisteredObservedDataVersions", StringsMap, msg)  # type: ignore
    
    def Project_GetPetrelObjectsByGuids(self, msg) -> Project_GetPetrelObjectsByGuids_Response:
        return self._server_streaming_wrapper("cegal.pythontool.Project_GetPetrelObjectsByGuids", Project_GetPetrelObjectsByGuids_Response, msg) # type: ignore

    def Project_GetPetrelProjectUnits(self, msg) -> StringsMap:
        return self._unary_wrapper("cegal.pythontool.Project_GetPetrelProjectUnits", StringsMap, msg) # type: ignore

    def GetServerVersion(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.GetServerVersion", ProtoString, msg) #type: ignore