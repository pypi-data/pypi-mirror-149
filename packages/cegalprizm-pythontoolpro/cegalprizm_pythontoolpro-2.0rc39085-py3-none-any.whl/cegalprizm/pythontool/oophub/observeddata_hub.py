# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub
import typing

class ObservedDataHub(BaseHub):
    def GetObservedDataGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetObservedDataGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetObservedData(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetObservedData", PetrelObjectRef, msg) # type: ignore
    
    def ObservedData_SetValues(self, iterable_requests) -> ObservedData_SetValues_Response:
        return self._client_streaming_wrapper("cegal.pythontool.ObservedData_SetValues", ObservedData_SetValues_Response, iterable_requests) # type: ignore
    
    def ObservedData_GetValues(self, msg) -> typing.Iterable[ObservedData_GetValues_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.ObservedData_GetValues", ObservedData_GetValues_Response, msg) # type: ignore

    def ObservedData_DisplayUnitSymbol(self, msg) -> ProtoString:
        return self._unary_wrapper("cegal.pythontool.ObservedData_DisplayUnitSymbol", ProtoString, msg) # type: ignore

    def ObservedData_GetParentObservedDataSet(self, msg) -> ObservedData_GetParent_Response:
        return self._unary_wrapper("cegal.pythontool.ObservedData_GetParentObservedDataSet", ObservedData_GetParent_Response, msg) # type: ignore

class ObservedDataSetHub(BaseHub):
    def GetObservedDataSetGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetObservedDataSetGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetObservedDataSet(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetObservedDataSet", PetrelObjectRef, msg) # type: ignore
    
    def ObservedDataSet_GetObservedDataObjects(self, msg) -> typing.Iterable[ObservedDataSet_GetObservedDataObjects_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.ObservedDataSet_GetObservedDataObjects", ObservedDataSet_GetObservedDataObjects_Response, msg) # type: ignore

    def ObservedDataSet_GetNumberOfObservedDataObjects(self, msg) -> ObservedDataSet_GetNumberOfObservedDataObjects_Response:
        return self._unary_wrapper("cegal.pythontool.ObservedDataSet_GetNumberOfObservedDataObjects", ObservedDataSet_GetNumberOfObservedDataObjects_Response, msg) # type: ignore
    
    def ObservedDataSet_GetDates(self, msg) -> typing.Iterable[ObservedDataSet_GetDates_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.ObservedDataSet_GetDates", ObservedDataSet_GetDates_Response, msg) # type: ignore
    
    def ObservedDataSet_Append(self, iterable_requests) -> ObservedDataSet_Append_Response:
        return self._client_streaming_wrapper("cegal.pythontool.ObservedDataSet_Append", ObservedDataSet_Append_Response, iterable_requests) # type: ignore
    
    def ObservedDataSet_CreateObservedData(self, iterable_requests) -> ObservedDataSet_CreateObservedData_Response:
        return self._client_streaming_wrapper("cegal.pythontool.ObservedDataSet_CreateObservedData", ObservedDataSet_CreateObservedData_Response, iterable_requests) # type: ignore

    def ObservedDataSet_GetParentPythonBoreholeObject(self, msg) -> ObservedDataSet_GetParentPythonBoreholeObject_Response:
        return self._unary_wrapper("cegal.pythontool.ObservedDataSet_GetParentPythonBoreholeObject", ObservedDataSet_GetParentPythonBoreholeObject_Response, msg) # type: ignore
        