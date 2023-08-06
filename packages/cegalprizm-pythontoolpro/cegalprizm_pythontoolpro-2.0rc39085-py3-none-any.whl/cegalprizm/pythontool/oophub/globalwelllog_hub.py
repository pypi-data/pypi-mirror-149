# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import *
from .base_hub import BaseHub


class GlobalWellLogHub(BaseHub):
    def GetGlobalWellLogGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetGlobalWellLogGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetGlobalWellLog(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetGlobalWellLog", PetrelObjectRef, msg) # type: ignore
    
    def GlobalWellLog_GetAllLogs(self, msg) -> GlobalWellLog_GetAllLogs_Response:
        return self._unary_wrapper("cegal.pythontool.GlobalWellLog_GetAllLogs", GlobalWellLog_GetAllLogs_Response, msg) # type: ignore
    
    def GlobalWellLog_GetWellLogByBoreholeNameOrGuid(self, msg) -> GlobalWellLog_GetWellLogByBoreholeName_Response:
        return self._unary_wrapper("cegal.pythontool.GlobalWellLog_GetWellLogByBoreholeNameOrGuid", GlobalWellLog_GetWellLogByBoreholeName_Response, msg) # type: ignore

    def GlobalWellLog_DisplayUnitSymbol(self, msg) -> GlobalWellLog_DisplayUnitSymbol_Response:
        return self._unary_wrapper("cegal.pythontool.GlobalWellLog_DisplayUnitSymbol", GlobalWellLog_DisplayUnitSymbol_Response, msg) # type: ignore