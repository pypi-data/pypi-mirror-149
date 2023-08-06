# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class SeismicHub(BaseHub):
    def GetSeismicGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetSeismicGrpc", PetrelObjectRef, msg) # type: ignore
    
    def DebugConnectionTest(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.DebugConnectionTest", ProtoBool, msg) # type: ignore
    
    def GetSeismicCube(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetSeismicCube", PetrelObjectRef, msg) # type: ignore
    
    def SeismicCube_Extent(self, msg) -> Primitives.Indices3:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_Extent", Primitives.Indices3, msg) # type: ignore
    
    def SeismicCube_AxesRange(self, msg) -> AxesRange:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_AxesRange", AxesRange, msg) # type: ignore
    
    def SeismicCube_IndexAtPosition(self, msg) -> Primitives.ExtIndices3:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_IndexAtPosition", Primitives.ExtIndices3, msg) # type: ignore
    
    def SeismicCube_PositionAtIndex(self, msg) -> Primitives.ExtDouble3:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_PositionAtIndex", Primitives.ExtDouble3, msg) # type: ignore
    
    def SeismicCube_DisplayUnitSymbol(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_DisplayUnitSymbol", ProtoString, msg) # type: ignore
    
    def SeismicCube_GetChunk(self, msg) -> typing.Iterable[Subchunk]:
        return self._server_streaming_wrapper("cegal.pythontool.SeismicCube_GetChunk", Subchunk, msg) # type: ignore
    
    def SeismicCube_StreamSetChunk(self, iterable_requests) -> Report:
        return self._client_streaming_wrapper("cegal.pythontool.SeismicCube_StreamSetChunk", Report, iterable_requests) # type: ignore
    
    def SeismicCube_AnnotationToIndex(self, msg) -> Primitives.ExtIndices3:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_AnnotationToIndex", Primitives.ExtIndices3, msg) # type: ignore
    
    def SeismicCube_IndexToAnnotation(self, msg) -> Primitives.ExtIndices3:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_IndexToAnnotation", Primitives.ExtIndices3, msg) # type: ignore
    
    def SeismicCube_GetParentCollection(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_GetParentCollection", PetrelObjectRef, msg) # type: ignore
    
    def SeismicCube_SetConstantValue(self, msg) -> SeismicCube_SetConstantValue_Response:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_SetConstantValue", SeismicCube_SetConstantValue_Response, msg) # type: ignore
    
    def SeismicCube_GetIjk(self, msg) -> SeismicCube_GetIjk_Response:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_GetIjk", SeismicCube_GetIjk_Response, msg) # type: ignore
    
    def SeismicCube_GetPositions(self, msg) -> SeismicCube_GetPositions_Response:
        return self._unary_wrapper("cegal.pythontool.SeismicCube_GetPositions", SeismicCube_GetPositions_Response, msg) # type: ignore
    