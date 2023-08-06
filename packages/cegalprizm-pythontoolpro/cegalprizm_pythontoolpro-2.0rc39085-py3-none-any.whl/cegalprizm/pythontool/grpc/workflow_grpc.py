# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.grpc import utils as grpc_utils    

from .grid_grpc import GridGrpc
from .gridproperty_grpc import GridPropertyGrpc, GridDiscretePropertyGrpc, PropertyCollectionGrpc
from .surface_grpc import SurfaceGrpc, SurfacePropertyGrpc, SurfaceDiscretePropertyGrpc
from .seismic_grpc import Seismic2DGrpc, SeismicCubeGrpc 
from .borehole_grpc import BoreholeGrpc, WellLogGrpc, DiscreteWellLogGrpc, GlobalWellLogGrpc, DiscreteGlobalWellLogGrpc
from .points_grpc import PointSetGrpc
from .polylines_grpc import PolylineSetGrpc
from .wavelet_grpc import WaveletGrpc
from .wellsurvey_grpc import XyzWellSurveyGrpc, XytvdWellSurveyGrpc, DxdytvdWellSurveyGrpc, MdinclazimWellSurveyGrpc, ExplicitWellSurveyGrpc
from .horizoninterpretation_grpc import HorizonInterpretation3dGrpc, HorizonProperty3dGrpc, HorizonInterpretationGrpc

from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.grpc import petrelinterface_pb2_grpc

from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.grpc import petrelinterface_pb2_grpc


import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.workflow_hub import WorkflowHub, ReferenceVariableHub
    
class ReferenceVariableGrpc(PetrelObjectGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(ReferenceVariableGrpc, self).__init__('referencevariable', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = typing.cast("ReferenceVariableHub", petrel_connection._service_referencevariable)

    def __str__(self):
        return 'ReferenceVariable(petrel_name="{}")'.format(self.GetPetrelName())

    def IsGood(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.ReferenceVariable_IsGood_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.ReferenceVariable_IsGood(request)
             
        return response.IsGood



class WorkflowGrpc(PetrelObjectGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(WorkflowGrpc, self).__init__('workflow', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = typing.cast("WorkflowHub", petrel_connection._service_workflow)

    def __str__(self):
        return 'Workflow(petrel_name="{}")'.format(self.GetPetrelName())

    def GetWorkflowInputReferences(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.Workflow_GetWorkflowInputReferences_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._channel.Workflow_GetWorkflowInputReferences(request)
        
        return [ReferenceVariableGrpc(item.guid, self._plink) if item.guid else None for sublist in responses for item in sublist.GetWorkflowInputReferences] 
    
    def GetWorkflowOutputReferences(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.Workflow_GetWorkflowOutputReferences_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._channel.Workflow_GetWorkflowOutputReferences(request)
        
        return [ReferenceVariableGrpc(item.guid, self._plink) if item.guid else None for sublist in responses for item in sublist.GetWorkflowOutputReferences]
    
    def RunSingle(
                    self, 
                    referenceVars, 
                    referenceTargets, 
                    doubleNames, 
                    doubleVals, 
                    intNames, 
                    intVals, 
                    boolNames, 
                    boolVals, 
                    dateNames, 
                    dateVals, 
                    stringNames, 
                    stringVals
                ):
        self._plink._opened_test()

        request = petrelinterface_pb2.Workflow_RunSingle_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , referenceVars = [petrelinterface_pb2.PetrelObjectGuid(guid = v._guid, sub_type = v._sub_type) for v in referenceVars]
            , referenceTargets = [petrelinterface_pb2.PetrelObjectGuid(guid = v._guid, sub_type = v._sub_type) for v in referenceTargets]
            , doubleNames = [v for v in doubleNames]
            , doubleVals = [v for v in doubleVals]
            , intNames = [v for v in intNames]
            , intVals = [v for v in intVals]
            , boolNames = [v for v in boolNames]
            , boolVals = [v for v in boolVals]
            , dateNames = [v for v in dateNames]
            , dateVals = [v for v in dateVals]
            , stringNames = [v for v in stringNames]
            , stringVals = [v for v in stringVals]
        )

        response = self._channel.Workflow_RunSingle(request)
        return [grpc_utils.pb_PetrelObjectRef_to_grpcobj(val, self._plink) for val in response.RunSingle] 
