# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class HorizonHub(BaseHub):
    def GetHorizonGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetHorizonGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetHorizonProperty3d(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetHorizonProperty3d", PetrelObjectRef, msg) # type: ignore
    
    def HorizonProperty3d_DisplayUnitSymbol(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.HorizonProperty3d_DisplayUnitSymbol", ProtoString, msg) # type: ignore
    
    def HorizonProperty3d_IndexAtPosition(self, msg) -> Primitives.ExtIndices2:
        return self._unary_wrapper("cegal.pythontool.HorizonProperty3d_IndexAtPosition", Primitives.ExtIndices2, msg) # type: ignore
    
    def HorizonProperty3d_PositionAtIndex(self, msg) -> Primitives.ExtDouble3:
        return self._unary_wrapper("cegal.pythontool.HorizonProperty3d_PositionAtIndex", Primitives.ExtDouble3, msg) # type: ignore
    
    def HorizonProperty3d_Extent(self, msg) -> Primitives.Indices2:
        return self._unary_wrapper("cegal.pythontool.HorizonProperty3d_Extent", Primitives.Indices2, msg) # type: ignore
    
    def HorizonProperty3d_GetChunk(self, msg) -> typing.Iterable[Subchunk]:
        return self._server_streaming_wrapper("cegal.pythontool.HorizonProperty3d_GetChunk", Subchunk, msg) # type: ignore
    
    def HorizonProperty3d_StreamSetChunk(self, iterable_requests) -> Report:
        return self._client_streaming_wrapper("cegal.pythontool.HorizonProperty3d_StreamSetChunk", Report, iterable_requests) # type: ignore
    
    def GetHorizonInterpretation3d(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetHorizonInterpretation3d", PetrelObjectRef, msg) # type: ignore
    
    def HorizonInterpretation3d_SampleCount(self, msg) -> ProtoInt:
        return self._unary_wrapper("cegal.pythontool.HorizonInterpretation3d_SampleCount", ProtoInt, msg) # type: ignore
    
    def HorizonInterpretation3d_DisplayUnitSymbol(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.HorizonInterpretation3d_DisplayUnitSymbol", ProtoString, msg) # type: ignore
    
    def HorizonInterpretation3d_IndexAtPosition(self, msg) -> Primitives.ExtIndices2:
        return self._unary_wrapper("cegal.pythontool.HorizonInterpretation3d_IndexAtPosition", Primitives.ExtIndices2, msg) # type: ignore
    
    def HorizonInterpretation3d_PositionAtIndex(self, msg) -> Primitives.ExtDouble3:
        return self._unary_wrapper("cegal.pythontool.HorizonInterpretation3d_PositionAtIndex", Primitives.ExtDouble3, msg) # type: ignore
    
    def HorizonInterpretation3d_Extent(self, msg) -> Primitives.Indices2:
        return self._unary_wrapper("cegal.pythontool.HorizonInterpretation3d_Extent", Primitives.Indices2, msg) # type: ignore
    
    def HorizonInterpretation3d_GetChunk(self, msg) -> typing.Iterable[Subchunk]:
        return self._server_streaming_wrapper("cegal.pythontool.HorizonInterpretation3d_GetChunk", Subchunk, msg) # type: ignore
    
    def HorizonInterpretation3d_StreamSetChunk(self, iterable_requests) -> Report:
        return self._client_streaming_wrapper("cegal.pythontool.HorizonInterpretation3d_StreamSetChunk", Report, iterable_requests) # type: ignore
    
    def HorizonInterpretation3d_GetAllHorizonPropertyValues(self, msg) -> PetrelObjectGuids:
        return self._unary_wrapper("cegal.pythontool.HorizonInterpretation3d_GetAllHorizonPropertyValues", PetrelObjectGuids, msg) # type: ignore
    
    def HorizonInterpretation3d_GetParent(self, msg) -> HorizonInterpretation3d_GetParent_Response:
        return self._unary_wrapper("cegal.pythontool.HorizonInterpretation3d_GetParent", HorizonInterpretation3d_GetParent_Response, msg) # type: ignore
    
    def HorizonInterpretation3d_GetIjk(self, msg) -> HorizonInterpretation3d_GetIjk_Response:
        return self._unary_wrapper("cegal.pythontool.HorizonInterpretation3d_GetIjk", HorizonInterpretation3d_GetIjk_Response, msg) # type: ignore
    
    def HorizonInterpretation3d_GetPositions(self, msg) -> HorizonInterpretation3d_GetPositions_Response:
        return self._unary_wrapper("cegal.pythontool.HorizonInterpretation3d_GetPositions", HorizonInterpretation3d_GetPositions_Response, msg) # type: ignore
    
    def HorizonProperty3d_GetIjk(self, msg) -> HorizonProperty3d_GetIjk_Response:
        return self._unary_wrapper("cegal.pythontool.HorizonProperty3d_GetIjk", HorizonProperty3d_GetIjk_Response, msg) # type: ignore
    
    def HorizonProperty3d_GetPositions(self, msg) -> HorizonProperty3d_GetPositions_Response:
        return self._unary_wrapper("cegal.pythontool.HorizonProperty3d_GetPositions", HorizonProperty3d_GetPositions_Response, msg) # type: ignore

    def HorizonProperty3d_GetParentHorizonInterpretation3d(self, msg) -> HorizonProperty3d_GetParentHorizonInterpretation3d_Response:
        return self._unary_wrapper("cegal.pythontool.HorizonProperty3d_GetParentHorizonInterpretation3d", HorizonProperty3d_GetParentHorizonInterpretation3d_Response, msg) # type: ignore
    
    
class HorizonInterpretationHub(BaseHub):
    def GetHorizonInterpretationGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetHorizonInterpretationGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetHorizonInterpretation(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetHorizonInterpretation", PetrelObjectRef, msg) # type: ignore
    
    def HorizonInterpretation_GetHorizonInterpretation3dObjects(self, msg) -> typing.Iterable[HorizonInterpretation_GetHorizonInterpretation3dObjects_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.HorizonInterpretation_GetHorizonInterpretation3dObjects", HorizonInterpretation_GetHorizonInterpretation3dObjects_Response, msg) # type: ignore
    