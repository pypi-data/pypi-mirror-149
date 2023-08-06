# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.grpc import petrelinterface_pb2
    
from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.grpc import petrelinterface_pb2

import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.wavelet_hub import WaveletHub

class WaveletGrpc(PetrelObjectGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(WaveletGrpc, self).__init__('wavelet', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = typing.cast("WaveletHub", petrel_connection._service_wavelet)

    def __str__(self):
        return 'Wavelet(petrel_name="{}")'.format(self.petrel_name)


    def Amplitudes(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.Wavelet_Amplitudes_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._channel.Wavelet_Amplitudes(request)
        
        return [item for sublist in responses for item in sublist.Amplitudes]
    
    def SampleCount(self) -> int:
        self._plink._opened_test()

        request = petrelinterface_pb2.Wavelet_SampleCount_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.Wavelet_SampleCount(request)
             
        return response.SampleCount 
    
    def SamplingInterval(self) -> float:
        self._plink._opened_test()

        request = petrelinterface_pb2.Wavelet_SamplingInterval_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.Wavelet_SamplingInterval(request)
             
        return response.SamplingInterval 
    
    def SamplingStart(self) -> float:
        self._plink._opened_test()

        request = petrelinterface_pb2.Wavelet_SamplingStart_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.Wavelet_SamplingStart(request)
             
        return response.SamplingStart 
    
    def SamplePoints(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.Wavelet_SamplePoints_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._channel.Wavelet_SamplePoints(request)
        
        return [item for sublist in responses for item in sublist.SamplePoints]
    
    def TimeUnitSymbol(self) -> str:
        self._plink._opened_test()

        request = petrelinterface_pb2.Wavelet_TimeUnitSymbol_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.Wavelet_TimeUnitSymbol(request)
             
        return response.TimeUnitSymbol 
    
    def SetAmplitudes(self, amplitudes):
        self._plink._opened_test()
    
        # TODO: Should be iterable of multiple petrelinterface_pb2.Wavelet_SetAmplitudes_Request
        iterable_requests = list((petrelinterface_pb2.Wavelet_SetAmplitudes_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , amplitudes = [v for v in amplitudes]
            ) for _ in range(1)
        ))

        ok = self._channel.Wavelet_SetAmplitudes((v for v in iterable_requests) )
        return ok.value
    
    def SetSamplingStart(self, samplingStart):
        self._plink._opened_test()

        request = petrelinterface_pb2.Wavelet_SetSamplingStart_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , samplingStart = samplingStart
        )

        response = self._channel.Wavelet_SetSamplingStart(request)
             
        return response.SetSamplingStart
    
    def SetSamplingInterval(self, samplingInterval):
        self._plink._opened_test()

        request = petrelinterface_pb2.Wavelet_SetSamplingInterval_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , samplingInterval = samplingInterval
        )

        response = self._channel.Wavelet_SetSamplingInterval(request)
             
        return response.SetSamplingInterval

