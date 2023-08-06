# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class WaveletHub(BaseHub):
    def GetWaveletGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetWaveletGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetWavelet(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetWavelet", PetrelObjectRef, msg) # type: ignore
    
    def Wavelet_Amplitudes(self, msg) -> typing.Iterable[Wavelet_Amplitudes_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Wavelet_Amplitudes", Wavelet_Amplitudes_Response, msg) # type: ignore
    
    def Wavelet_SampleCount(self, msg) -> Wavelet_SampleCount_Response:
        return self._unary_wrapper("cegal.pythontool.Wavelet_SampleCount", Wavelet_SampleCount_Response, msg) # type: ignore
    
    def Wavelet_SamplingInterval(self, msg) -> Wavelet_SamplingInterval_Response:
        return self._unary_wrapper("cegal.pythontool.Wavelet_SamplingInterval", Wavelet_SamplingInterval_Response, msg) # type: ignore
    
    def Wavelet_SamplingStart(self, msg) -> Wavelet_SamplingStart_Response:
        return self._unary_wrapper("cegal.pythontool.Wavelet_SamplingStart", Wavelet_SamplingStart_Response, msg) # type: ignore
    
    def Wavelet_SamplePoints(self, msg) -> typing.Iterable[Wavelet_SamplePoints_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Wavelet_SamplePoints", Wavelet_SamplePoints_Response, msg) # type: ignore
    
    def Wavelet_TimeUnitSymbol(self, msg) -> Wavelet_TimeUnitSymbol_Response:
        return self._unary_wrapper("cegal.pythontool.Wavelet_TimeUnitSymbol", Wavelet_TimeUnitSymbol_Response, msg) # type: ignore
    
    def Wavelet_SetAmplitudes(self, iterable_requests) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.Wavelet_SetAmplitudes", ProtoBool, iterable_requests) # type: ignore
    
    def Wavelet_SetSamplingStart(self, msg) -> Wavelet_SetSamplingStart_Response:
        return self._unary_wrapper("cegal.pythontool.Wavelet_SetSamplingStart", Wavelet_SetSamplingStart_Response, msg) # type: ignore
    
    def Wavelet_SetSamplingInterval(self, msg) -> Wavelet_SetSamplingInterval_Response:
        return self._unary_wrapper("cegal.pythontool.Wavelet_SetSamplingInterval", Wavelet_SetSamplingInterval_Response, msg) # type: ignore
    