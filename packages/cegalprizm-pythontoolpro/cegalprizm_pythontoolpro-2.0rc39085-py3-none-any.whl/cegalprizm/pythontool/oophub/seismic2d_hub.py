# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class Seismic2DHub(BaseHub):
    def GetSeismic2DGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetSeismic2DGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetSeismic2D(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetSeismic2D", PetrelObjectRef, msg) # type: ignore
    
    def Seismic2D_Extent(self, msg) -> Primitives.Indices3:
        return self._unary_wrapper("cegal.pythontool.Seismic2D_Extent", Primitives.Indices3, msg) # type: ignore
    
    def Seismic2D_AxesRange(self, msg) -> AxesRange:
        return self._unary_wrapper("cegal.pythontool.Seismic2D_AxesRange", AxesRange, msg) # type: ignore
    
    def Seismic2D_DisplayUnitSymbol(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.Seismic2D_DisplayUnitSymbol", ProtoString, msg) # type: ignore
    
    def Seismic2D_IndexAtPosition(self, msg) -> Primitives.ExtIndices3:
        return self._unary_wrapper("cegal.pythontool.Seismic2D_IndexAtPosition", Primitives.ExtIndices3, msg) # type: ignore
    
    def Seismic2D_PositionAtIndex(self, msg) -> Primitives.ExtDouble3:
        return self._unary_wrapper("cegal.pythontool.Seismic2D_PositionAtIndex", Primitives.ExtDouble3, msg) # type: ignore
    
    def Seismic2D_GetParentCollection(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.Seismic2D_GetParentCollection", PetrelObjectRef, msg) # type: ignore
    
    def Seismic2D_GetChunk(self, msg) -> typing.Iterable[Subchunk]:
        return self._server_streaming_wrapper("cegal.pythontool.Seismic2D_GetChunk", Subchunk, msg) # type: ignore
    
    def Seismic2D_StreamSetChunk(self, iterable_requests) -> Report:
        return self._client_streaming_wrapper("cegal.pythontool.Seismic2D_StreamSetChunk", Report, iterable_requests) # type: ignore
    