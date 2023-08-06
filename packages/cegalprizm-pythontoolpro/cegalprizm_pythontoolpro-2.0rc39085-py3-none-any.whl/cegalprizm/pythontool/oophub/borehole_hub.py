# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class BoreholeHub(BaseHub):
    def GetBoreholeGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetBoreholeGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetBorehole(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetBorehole", PetrelObjectRef, msg) # type: ignore
    
    def Borehole_GetElevationTimePosition(self, msg) -> Borehole_GetElevationTimePosition_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetElevationTimePosition", Borehole_GetElevationTimePosition_Response, msg) # type: ignore
    
    def Borehole_GetTvdPosition(self, msg) -> Borehole_GetTvdPosition_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetTvdPosition", Borehole_GetTvdPosition_Response, msg) # type: ignore
    
    def Borehole_GetAllLogs(self, msg) -> PetrelObjectGuids:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetAllLogs", PetrelObjectGuids, msg) # type: ignore
    
    def Borehole_GetLogsValues(self, msg) -> typing.Iterable[LogValues]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetLogsValues", LogValues, msg) # type: ignore
 
    def Borehole_GetObservedDataSets(self, msg) -> typing.Iterable[Borehole_GetObservedDataSets_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetObservedDataSets", Borehole_GetObservedDataSets_Response, msg) # type: ignore
 
    def Borehole_GetNumberOfObservedDataSets(self, msg) -> Borehole_GetNumberOfObservedDataSets_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetNumberOfObservedDataSets", Borehole_GetNumberOfObservedDataSets_Response, msg) # type: ignore

    def Borehole_GetXyzWellSurveys(self, msg) -> typing.Iterable[Borehole_GetWellSurveys_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetXyzWellSurveys", Borehole_GetWellSurveys_Response, msg) # type: ignore
 
    def Borehole_GetXytvdWellSurveys(self, msg) -> typing.Iterable[Borehole_GetWellSurveys_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetXytvdWellSurveys", Borehole_GetWellSurveys_Response, msg) # type: ignore

    def Borehole_GetDxdytvdWellSurveys(self, msg) -> typing.Iterable[Borehole_GetWellSurveys_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetDxdytvdWellSurveys", Borehole_GetWellSurveys_Response, msg) # type: ignore

    def Borehole_GetMdinclazimWellSurveys(self, msg) -> typing.Iterable[Borehole_GetWellSurveys_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetMdinclazimWellSurveys", Borehole_GetWellSurveys_Response, msg) # type: ignore

    def Borehole_GetExplicitWellSurveys(self, msg) -> typing.Iterable[Borehole_GetWellSurveys_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetExplicitWellSurveys", Borehole_GetWellSurveys_Response, msg) # type: ignore

    def Borehole_GetNumberOfWellSurveys(self, msg) -> Borehole_GetNumberOfWellSurveys_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetNumberOfWellSurveys", Borehole_GetNumberOfWellSurveys_Response, msg) # type: ignore
 