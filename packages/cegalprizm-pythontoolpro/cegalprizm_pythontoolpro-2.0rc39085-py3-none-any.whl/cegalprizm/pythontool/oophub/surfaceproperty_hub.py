# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class SurfacePropertyHub(BaseHub):
    def GetSurfacePropertyGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetSurfacePropertyGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetSurfaceProperty(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetSurfaceProperty", PetrelObjectRef, msg) # type: ignore
    
    def SurfaceProperty_DisplayUnitSymbol(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.SurfaceProperty_DisplayUnitSymbol", ProtoString, msg) # type: ignore
    
    def SurfaceProperty_ParentSurface(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.SurfaceProperty_ParentSurface", ProtoString, msg) # type: ignore
    
    def SurfaceProperty_TypeOfSurface(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.SurfaceProperty_TypeOfSurface", ProtoString, msg) # type: ignore
    
    def SurfaceProperty_GetAllDictionaryCodes(self, msg) -> IntStringTuples:
        return self._unary_wrapper("cegal.pythontool.SurfaceProperty_GetAllDictionaryCodes", IntStringTuples, msg) # type: ignore
    
    def SurfaceProperty_Extent(self, msg) -> Primitives.Indices3:
        return self._unary_wrapper("cegal.pythontool.SurfaceProperty_Extent", Primitives.Indices3, msg) # type: ignore
    
    def SurfaceProperty_GetChunk(self, msg) -> typing.Iterable[Subchunk]:
        return self._server_streaming_wrapper("cegal.pythontool.SurfaceProperty_GetChunk", Subchunk, msg) # type: ignore
    
    def SurfaceProperty_StreamSetChunk(self, iterable_requests) -> Report:
        return self._client_streaming_wrapper("cegal.pythontool.SurfaceProperty_StreamSetChunk", Report, iterable_requests) # type: ignore
    
    def SurfaceProperty_GetIjk(self, msg) -> SurfaceProperty_GetIjk_Response:
        return self._unary_wrapper("cegal.pythontool.SurfaceProperty_GetIjk", SurfaceProperty_GetIjk_Response, msg) # type: ignore
    
    def SurfaceProperty_GetPositions(self, msg) -> SurfaceProperty_GetPositions_Response:
        return self._unary_wrapper("cegal.pythontool.SurfaceProperty_GetPositions", SurfaceProperty_GetPositions_Response, msg)  # type: ignore