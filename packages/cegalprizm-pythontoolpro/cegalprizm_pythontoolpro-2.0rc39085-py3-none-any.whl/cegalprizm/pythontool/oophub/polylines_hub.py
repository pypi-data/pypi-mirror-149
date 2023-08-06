# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class PolylinesHub(BaseHub):
    def GetPolylinesGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetPolylinesGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetPolylineSet(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetPolylineSet", PetrelObjectRef, msg) # type: ignore
    
    def PolylineSet_GetNumPolylines(self, msg) -> ProtoInt:
        return self._unary_wrapper("cegal.pythontool.PolylineSet_GetNumPolylines", ProtoInt, msg) # type: ignore
    
    def PolylineSet_DisplayUnitSymbol(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.PolylineSet_DisplayUnitSymbol", ProtoString, msg) # type: ignore
    
    def PolylineSet_IsClosed(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.PolylineSet_IsClosed", ProtoBool, msg) # type: ignore
    
    def PolylineSet_GetPoints(self, msg) -> typing.Iterable[Primitives.Double3]:
        return self._server_streaming_wrapper("cegal.pythontool.PolylineSet_GetPoints", Primitives.Double3, msg) # type: ignore
    
    def PolylineSet_SetPolylinePoints(self, iterable_requests) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.PolylineSet_SetPolylinePoints", ProtoBool, iterable_requests) # type: ignore
    
    def PolylineSet_AddPolyline(self, iterable_requests) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.PolylineSet_AddPolyline", ProtoBool, iterable_requests) # type: ignore
    
    def PolylineSet_DeletePolyline(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.PolylineSet_DeletePolyline", ProtoBool, msg) # type: ignore
    
    def PolylineSet_DeleteAll(self, msg) -> PolylineSet_DeleteAll_Response:
        return self._unary_wrapper("cegal.pythontool.PolylineSet_DeleteAll", PolylineSet_DeleteAll_Response, msg) # type: ignore
    