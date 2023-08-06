# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import grpc
import os
import typing
import pkg_resources
import contextlib
from packaging import version

from warnings import warn
from enum import Enum
from cegalprizm.hub import BaseContext

from cegalprizm.pythontool.grpc import utils, petrelinterface_pb2, petrelinterface_pb2_grpc
from cegalprizm.pythontool.ooponly.ptutils import Utils

from cegalprizm.pythontool.grpc.workflow_grpc import ReferenceVariableGrpc, WorkflowGrpc
from cegalprizm.pythontool.grpc.grid_grpc import GridGrpc
from cegalprizm.pythontool.grpc.gridproperty_grpc import GridPropertyGrpc, GridDiscretePropertyGrpc, PropertyCollectionGrpc
from cegalprizm.pythontool.grpc.surface_grpc import SurfaceGrpc, SurfacePropertyGrpc, SurfaceDiscretePropertyGrpc
from cegalprizm.pythontool.grpc.seismic_grpc import Seismic2DGrpc, SeismicCubeGrpc 
from cegalprizm.pythontool.grpc.borehole_grpc import BoreholeGrpc, WellLogGrpc, DiscreteWellLogGrpc, GlobalWellLogGrpc, DiscreteGlobalWellLogGrpc
from cegalprizm.pythontool.grpc.points_grpc import PointSetGrpc
from cegalprizm.pythontool.grpc.polylines_grpc import PolylineSetGrpc
from cegalprizm.pythontool.grpc.wavelet_grpc import WaveletGrpc
from cegalprizm.pythontool.grpc.wellsurvey_grpc import XyzWellSurveyGrpc, XytvdWellSurveyGrpc, DxdytvdWellSurveyGrpc, MdinclazimWellSurveyGrpc, ExplicitWellSurveyGrpc
from cegalprizm.pythontool.grpc.horizoninterpretation_grpc import HorizonInterpretation3dGrpc, HorizonProperty3dGrpc, HorizonInterpretationGrpc
from cegalprizm.pythontool.grpc.observeddata_grpc import ObservedDataGrpc, ObservedDataSetGrpc
from cegalprizm.pythontool.grpc._logo import _logo_data_uri
from cegalprizm.pythontool.grpc.petrelobjects import Properties as PO_Properties
from cegalprizm.pythontool.grpc.petrelobjects import Grids as PO_Grids
from cegalprizm.pythontool.grpc.petrelobjects import SeismicCubes as PO_SeismicCubes
from cegalprizm.pythontool.grpc.petrelobjects import Seismic2Ds as PO_Seismic2Ds
from cegalprizm.pythontool.grpc.petrelobjects import Surfaces as PO_Surfaces
from cegalprizm.pythontool.grpc.petrelobjects import SurfaceAttributes as PO_SurfaceAttributes
from cegalprizm.pythontool.grpc.petrelobjects import DiscreteProperties as PO_DiscreteProperties
from cegalprizm.pythontool.grpc.petrelobjects import SurfaceDiscreteAttributes as PO_SurfaceDiscreteAttributes
from cegalprizm.pythontool.grpc.petrelobjects import WellLogs as PO_WellLogs
from cegalprizm.pythontool.grpc.petrelobjects import GlobalWellLogs as PO_GlobalWellLogs
from cegalprizm.pythontool.grpc.petrelobjects import DiscreteGlobalWellLogs as PO_DiscreteGlobalWellLogs
from cegalprizm.pythontool.grpc.petrelobjects import DiscreteWellLogs as PO_DiscreteWellLogs
from cegalprizm.pythontool.grpc.petrelobjects import PointSets as PO_PointSets
from cegalprizm.pythontool.grpc.petrelobjects import PolylineSets as PO_PolylineSets
from cegalprizm.pythontool.grpc.petrelobjects import Wells as PO_Wells
from cegalprizm.pythontool.grpc.petrelobjects import HorizonInterpretation3Ds as PO_HorizonInterpretation3Ds
from cegalprizm.pythontool.grpc.petrelobjects import HorizonInterpretations as  PO_HorizonInterpretations
from cegalprizm.pythontool.grpc.petrelobjects import HorizonProperties as PO_HorizonProperties
from cegalprizm.pythontool.grpc.petrelobjects import PropertyCollections as PO_PropertyCollections
from cegalprizm.pythontool.grpc.petrelobjects import Wavelets as PO_Wavelets
from cegalprizm.pythontool.grpc.petrelobjects import Workflows as PO_Workflows
from cegalprizm.pythontool.grpc.petrelobjects import WellSurveys as PO_WellSurveys
from cegalprizm.pythontool.grpc.petrelobjects import ObservedDataSets as PO_ObservedDataSets

from cegalprizm.pythontool.oophub.borehole_hub import BoreholeHub
from cegalprizm.pythontool.oophub.grid_hub import GridHub
from cegalprizm.pythontool.oophub.horizon_hub import HorizonHub, HorizonInterpretationHub
from cegalprizm.pythontool.oophub.gridproperty_hub import GridPropertyHub
from cegalprizm.pythontool.oophub.globalwelllog_hub import GlobalWellLogHub
from cegalprizm.pythontool.oophub.petrelobject_hub import PetrelObjectHub
from cegalprizm.pythontool.oophub.project_hub import ProjectHub
from cegalprizm.pythontool.oophub.points_hub import PointsHub
from cegalprizm.pythontool.oophub.polylines_hub import PolylinesHub
from cegalprizm.pythontool.oophub.observeddata_hub import ObservedDataHub, ObservedDataSetHub
from cegalprizm.pythontool.oophub.workflow_hub import ReferenceVariableHub, WorkflowHub
from cegalprizm.pythontool.oophub.seismic_hub import SeismicHub
from cegalprizm.pythontool.oophub.seismic2d_hub import Seismic2DHub
from cegalprizm.pythontool.oophub.surface_hub import SurfaceHub
from cegalprizm.pythontool.oophub.surfacecollection_hub import SurfaceCollectionHub
from cegalprizm.pythontool.oophub.surfaceproperty_hub import SurfacePropertyHub
from cegalprizm.pythontool.oophub.wavelet_hub import WaveletHub
from cegalprizm.pythontool.oophub.welllog_hub import WellLogHub
from cegalprizm.pythontool.oophub.wellsurvey_hub import XyzWellSurveyHub, XytvdWellSurveyHub, DxdytvdWellSurveyHub, MdinclazimWellSurveyHub, ExplicitWellSurveyHub 
from cegalprizm.pythontool.oophub.ptphubcontext import PtpHubContext

from cegalprizm.pythontool.grid import Grid
from cegalprizm.pythontool.gridproperty import GridProperty, GridDiscreteProperty, PropertyCollection
from cegalprizm.pythontool.surface import Surface, SurfaceAttribute, SurfaceDiscreteAttribute
from cegalprizm.pythontool.borehole import Well
from cegalprizm.pythontool.welllog import WellLog, DiscreteWellLog, GlobalWellLog, DiscreteGlobalWellLog
from cegalprizm.pythontool.points import PointSet
from cegalprizm.pythontool.polylines import PolylineSet
from cegalprizm.pythontool.horizoninterpretation import HorizonInterpretation3d, HorizonProperty3d, HorizonInterpretation
from cegalprizm.pythontool.seismic import SeismicCube, SeismicLine
from cegalprizm.pythontool.wavelet import Wavelet
from cegalprizm.pythontool.wellsurvey import WellSurvey
from cegalprizm.pythontool.workflow import ReferenceVariable, Workflow, _pb_PetrelObjectGuid_to_pyobj
from cegalprizm.pythontool.observeddata import ObservedData, ObservedDataSet
from cegalprizm.pythontool.experimental import set_experimental_ok, experimental_method
from cegalprizm.pythontool.exceptions import PythonToolException

@contextlib.contextmanager
def make_connection(
         allow_experimental: typing.Optional[bool] = None, 
         enable_history: typing.Optional[bool] = True, 
         petrel_ctx: typing.Optional[BaseContext] = None)\
        -> typing.Iterator["PetrelConnection"]:
    """A context-manager that provides a connection to Petrel.  A typical usage is 

    with make_connection() as p:
        p.wells
        ...
    
    The connection is closed automatically when the `with` context is exited.  

    See `cegalprizm.pythontool.petrelconnection.PetrelConnection` for more details.
    """
    c =  PetrelConnection(allow_experimental, enable_history, petrel_ctx)
    try:
        c.open()
        yield c
    finally:
        c.close()

def _get_version():
    return pkg_resources.get_distribution('cegalprizm-pythontoolpro').version

class PetrelConnectionState(Enum):
    UNOPENED = 1
    OPENED = 2
    CLOSED = 3

class PetrelConnection:
    """Creates a connection to Petrel. A typical usage is

    .. code-block:: Python

        ptp = PetrelConnection()
        '''write some code accessing Petrel here'''
        ptp.close()

    Python Tool Pro will try to connect to a running Hub server and will create a default Petrel context (petrel_ctx). This will work if 1 Petrel connector (1 Petrel instace) is connected to the Hub server. If multiple Petrel connectors are available you need to define the Petrel context to ensure you connect to the correct Petrel instance.

    Args:
        petrel_ctx: A context or handle to a Cegal Hub Petrel Connector
        allow_experimental: Enable experimental methods to be called. Defaults to False
        enable_history: Petrel data object history is updated when changed from Python Tool Pro. Defaults to True.
    """
    _keystone = None
    _no_keystone = None
    _keystone_url = None

    def __init__(self, allow_experimental: typing.Optional[bool] = None, enable_history: typing.Optional[bool] = True, petrel_ctx: typing.Optional[BaseContext] = None):
        self._preferred_streamed_unit_bytes: int = 2 * 1024 * 1024
        self._ptp_hub_ctx = PtpHubContext(petrel_ctx)
        from cegalprizm.hub import server_service_pb2

        try:
            self._ptp_hub_ctx.channel.server_request_stub.VerifyHealth(server_service_pb2.HealthQuery())
        except grpc._channel._InactiveRpcError as ine:
            message = "\n\n" + ine.details()
            if (ine.code() is grpc.StatusCode.UNAVAILABLE):
                message += """\n\nPlease check if a Hub Server is running and available for connections. \
This information can be found in the Hub Connection Settings tool under Hub in Marina in Petrel. 
For local connections; start a local Hub Server. For remote connections; please contact the Hub admin in your organisation.""" 
            if (ine.code() is grpc.StatusCode.UNKNOWN):
                message += """\n\nPlease check that you have the correct access rights."""
            raise PythonToolException(message)
        except Exception as e:
            message = "Please check if you have the correct access rights and that Petrel is opened with a Hub Server running available for connections."
            raise PythonToolException(message)
        
        self._service_project: ProjectHub = ProjectHub(self._ptp_hub_ctx)

        # Find if client version is accepted by server
        client_version_accepted, client_version, server_version = self._verify_version()
        if not client_version_accepted:
            raise PythonToolException(f'Client version {client_version} is not accepted by server. Server version is {server_version}')

        # Common settings
        self._opened = PetrelConnectionState.UNOPENED
        self._array_transfer_mode = petrelinterface_pb2.STREAM
        self._report = ''
        self._was_success = None
        self._enable_history = enable_history
        if not allow_experimental is None:
            set_experimental_ok(allow_experimental)
        self._set_enable_history(self._enable_history)

        # Test connection
        try:
            self.ping()
            self._opened = PetrelConnectionState.OPENED
        except Exception as e:
            message = str(e)
            # if connection failed it could be because auth failed so delete possibly-invalid cached refresh_token
            raise PythonToolException(e)

        self._service_petrel_object = PetrelObjectHub(self._ptp_hub_ctx) # type: ignore
        self._service_grid = GridHub(self._ptp_hub_ctx) # type: ignore
        self._service_grid_property = GridPropertyHub(self._ptp_hub_ctx) # type: ignore
        self._service_surface = SurfaceHub(self._ptp_hub_ctx) # type: ignore
        self._service_surface_property = SurfacePropertyHub(self._ptp_hub_ctx) # type: ignore
        self._service_surface_collection = SurfaceCollectionHub(self._ptp_hub_ctx) # type: ignore
        self._service_borehole = BoreholeHub(self._ptp_hub_ctx) # type: ignore
        self._service_globalwelllog = GlobalWellLogHub(self._ptp_hub_ctx) # type: ignore
        self._service_welllog = WellLogHub(self._ptp_hub_ctx) # type: ignore
        self._service_seismic = SeismicHub(self._ptp_hub_ctx) # type: ignore
        self._service_seismic_2d = Seismic2DHub(self._ptp_hub_ctx) # type: ignore
        self._service_points = PointsHub(self._ptp_hub_ctx) # type: ignore
        self._service_polylines = PolylinesHub(self._ptp_hub_ctx) # type: ignore
        self._service_horizon = HorizonHub(self._ptp_hub_ctx) # type: ignore
        self._service_wavelet = WaveletHub(self._ptp_hub_ctx) # type: ignore
        self._service_xyz_well_survey = XyzWellSurveyHub(self._ptp_hub_ctx) # type: ignore
        self._service_xytvd_well_survey = XytvdWellSurveyHub(self._ptp_hub_ctx) # type: ignore
        self._service_dxdytvd_well_survey = DxdytvdWellSurveyHub(self._ptp_hub_ctx) # type: ignore
        self._service_mdinclazim_well_survey = MdinclazimWellSurveyHub(self._ptp_hub_ctx) # type: ignore
        self._service_explicit_well_survey = ExplicitWellSurveyHub(self._ptp_hub_ctx) # type: ignore
        self._service_horizon_interpretation = HorizonInterpretationHub(self._ptp_hub_ctx) # type: ignore
        self._service_workflow = WorkflowHub(self._ptp_hub_ctx) # type: ignore
        self._service_referencevariable = ReferenceVariableHub(self._ptp_hub_ctx) # type: ignore
        self._service_observeddata = ObservedDataHub(self._ptp_hub_ctx) # type: ignore
        self._service_observeddataset = ObservedDataSetHub(self._ptp_hub_ctx) # type: ignore

    def open(self) -> None:
        """DeprecationWarning: "petrelconnection.open() is deprecated and will 
           be removed in Python Tool Pro in 3.0. open() is no longer necessary
           after creating a new PetrelConnection object.
        """
        warn("petrelconnection.open() is deprecated and will be removed for Python \
             Tool Pro in 3.0. open() is no longer necessary after creating a new \
             PetrelConnection object.", 
             DeprecationWarning, stacklevel=2)
        pass

    def close(self) -> None:
        """Close the connection to Petrel.
        """
        self._opened = PetrelConnectionState.CLOSED
        self._ptp_hub_ctx.close()


    def __repr__(self) -> str:
        try:
            package_version = self._package_version
        except Exception:
            package_version = None

        try:
            opened = self._opened == PetrelConnectionState.OPENED
        except Exception:
            opened = None
        
        return 'version: {0}\nis open: {1}'.format(package_version, opened)

    def __str__(self) -> str:
        return self.__repr__()

    def _get_server_version_from_localappdata(self):
        loc = os.environ["LOCALAPPDATA"]
        fp = os.path.join(loc,".blueback.pythontoolpro", "version")

        if not os.path.exists(fp) or not os.path.isfile(fp):
            return

        try:
            with open(fp) as f:
                data = f.readline()
            return data.strip()
        except:
            return None

    def _get_port_from_localappdata(self, default):
        loc = os.environ["LOCALAPPDATA"]
        fp = os.path.join(loc,".blueback.pythontoolpro", "version")

        if not os.path.exists(fp) or not os.path.isfile(fp):
            return default

        try:
            with open(fp) as f:
                data = f.readline()
            return int(data)
        except:
            return default
    
    def _set_report(self, report):
        self._report = report.message
        self._was_success = report.value

    def _can_connect_without_hub(self):
        appdata = os.environ.get("LOCALAPPDATA")
        if (appdata is None):
            return False
        return True

    def _check_session_version(self):
        server_version = self._get_server_version_from_localappdata()
        if not server_version:
            raise PythonToolException("This version of the Python Tool Pro client library does not work with Python Tool Pro plugin version < 1.3.0.")
        if len(server_version.split(".")) < 2:
            raise PythonToolException("Failed to determine Python Tool Pro plugin version.")
        client_version = self._package_version
        if len(client_version.split(".")) < 3:
            raise PythonToolException("Failed to determine Python Tool Pro client library version.")
        for c_v, l_v in zip(server_version.split(".")[:2], client_version.split(".")[:2]):
            if int(c_v) != int(l_v):
                raise PythonToolException(f"This version of the Python Tool Pro client library ({client_version}) does not work with Python Tool Pro plugin ({server_version})")

    def _verify_version(self):
        # parse the version to a Version object to avoid using client_version with a possible 'rc' string in it. 
        client_version = version.parse(self._package_version)
        reply = self._service_project.GetServerVersion(petrelinterface_pb2.EmptyRequest())
        server_version = version.parse(reply.value)
        version_ok = client_version.major == server_version.major and client_version.minor == server_version.minor
        client_version_str = "{0}.{1}.{2}".format(client_version.major, client_version.minor, client_version.micro)
        server_version_str = "{0}.{1}.{2}".format(server_version.major, server_version.minor, server_version.micro)
        return version_ok, client_version_str, server_version_str

    def _set_enable_history(self, enable):
        request = petrelinterface_pb2.ProtoBool(value=enable)
        reply = self._service_project.EnableHistory(request)
        return reply.value

    @experimental_method
    def import_workflows(self, projectPath: str, workflowNames: typing.List[str]) -> typing.List[Workflow]:
        """Import a Petrel workflow from a different Petrel project.

        Args:
           projectPath: the file path to the Petrel project
           workflowNames: the Petrel name[s] of the workflow[s] to be imported
        """
        request = petrelinterface_pb2.Project_ImportWorkflow_Request(
            projectPath = projectPath
            , workflowNames = [v for v in workflowNames]
        )

        response = self._service_project.Project_ImportWorkflow(request)
             
        return [Workflow(WorkflowGrpc(item.guid, self)) for item in response.ImportWorkflow]

    @property
    def _package_version(self):
        return _get_version()
    
    def ping(self) -> int:
        """Typically used to verify connection to the server.

        Returns:
            int: A counter returned by the server
        """
        request = petrelinterface_pb2.EmptyRequest()
        reply = self._service_project.Ping(request)
        return reply.value 

    def a_project_is_active(self) -> bool:
        """Verify that a project is active on the server. A project must be active.

        Returns:
            bool: True if and only if a project is active
        """
        self._opened_test()
        request = petrelinterface_pb2.EmptyRequest()
        reply = self._service_project.AProjectIsActive(request)
        return reply.value 

    def get_current_project_name(self) -> str:
        """Returns the name of the Petrel project of the established connection."""
        self._opened_test()
        request = petrelinterface_pb2.EmptyRequest()
        reply = self._service_project.GetCurrentProjectName(request)
        return reply.value

    def get_petrelobjects_by_guids(self, guids: typing.List[str]) -> typing.List[object]:
        """Get the Petrel objects with the given GUIDs

        Note:
            The format of the GUIDs need to be the same as the droids of the Petrel objects which is 32-character hexadecimal string including dashes, e.g '12345678-1234-5678-1234-567812345678'
            When using GUIDs from Studio for Petrel the GUIDs do not include the dashes, e.g '12345678123456781234567812345678'
            To convert GUIDs from Studio format to Petrel droid format use library uuid https://docs.python.org/3/library/uuid.html

        .. code-block:: Python

            import uuid
            str(uuid.UUID('12345678123456781234567812345678'))
        
        Args:
            guids: A list of GUIDs as strings of the objects to be returned

        Returns: 
            A list with the objects for the given GUIDs. 
              If GUID  does not exist in Petrel project 'None' is returned.
        """
        self._opened_test()
        if (not isinstance(guids, list) or not all(isinstance(item, str) for item in guids)):
            raise PythonToolException("Input argument 'GUIDs' must be a list and all items must be string")
        proto_guids = [g for g in guids]
        request = petrelinterface_pb2.Project_GetPetrelObjectsByGuids_Request(guids=proto_guids)
        responses = self._service_project.Project_GetPetrelObjectsByGuids(request)
        return [_pb_PetrelObjectGuid_to_pyobj(utils.pb_PetrelObjectRef_to_grpcobj(item.GetPetrelObjectsByGuids, self)) for item in responses]

    def get_petrel_project_units(self) -> typing.Dict[str, str]:
        """Get the Petrel project units of the established PetrelConnection.

        Returns: 
            A dictionary with the storage units and their unit symbols
        """
        self._opened_test()
        request = petrelinterface_pb2.EmptyRequest()
        response = self._service_project.Project_GetPetrelProjectUnits(request)
        return Utils.protobuf_map_to_dict(response.string_to_string_map)

    @experimental_method
    def append_scriptname_to_history(self, path_to_append: str) -> str:
        """Define path that will be appended to the history entries when objects are modified. 
        
        Args:
            path_to_append: The string of the path to append. 
        
        Example:

        from cegalprizm.pythontool.petrelconnection import PetrelConnection, make_connection
        petrel = PetrelConnection(allow_experimental=True)
        petrel.append_script_name_to_history('c:\\notebooks\mergeworkbook.ipynb')
        #Modify
        petrel.close()

        """
        self._opened_test()
        request = petrelinterface_pb2.ProtoString(value=path_to_append)
        reply = self._service_project.SetScriptName(request)
        return reply.value 

    def _find_global_well_logs(self, discrete = False):
        """A dictionary of GUIDs and paths to all global well logs in the current Petrel project.
        Use method get_global_well_log to select one of them. 
        
        Args:
            discrete (bool, optional): Discrete (True) or continous (False) global well logs. Defaults to False.
        Returns:
            Dictionary: All global well logs with GUID as key and path as value.
        """
        if discrete:
            request_string = 'find global discrete well logs'
        else:
            request_string = 'find global well logs'
        return self._find_paths_by_guids(request_string)
    
    def _find_grid_properties(self, discrete = False):
        """A dictionary of GUIDs and paths to all grid properties in the current Petrel project.
        Use method get_grid_property to select one of them. 

        Args:
            discrete (bool, optional): Discrete (True) or continous (False) grid properties. Defaults to False.

        Returns:
            Dictionary: All grid properties with GUID as key and path as value.
        """
        if discrete:
            request_string = 'find discrete grid properties'
        else:
            request_string = 'find grid properties'

        return self._find_paths_by_guids(request_string)

    def _find_grids(self):
        """A dictionary of GUIDs and paths to all grids in the current Petrel project.
        Use method get_grid to select one of them. 
        
        Returns:
            Dictionary: All grids with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find grids')

    def _find_horizon_properties(self):
        """A dictionary of GUIDs and paths to all horizon properties in the current Petrel project.
        Use method get_horizon_property to select one of them. 

        Returns:
            Dictionary: All horizon properties with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find horizon properties 3d')

    def _find_horizon_interpretation_3ds(self):
        """A dictionary of GUIDs and paths to all horizon interpretations in the current Petrel project.
        Use method get_horizon_interpretation to select one of them. 

        Returns:
            Dictionary: All horizon interpretations with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find horizon interpretations 3d')

    def _find_horizon_interpretations(self):
        """A dictionary of GUIDs and paths to all horizon interpretations in the current Petrel project.
        Use method get_horizon_interpretation to select one of them. 

        Returns:
            Dictionary: All horizon interpretations with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find horizon interpretations')

    def _find_pointsets(self):
        """A dictionary of GUIDs and paths to all pointsets in the current Petrel project.
        Use method get_pointset to select one of them. 

        ** The implementation of point sets is in a preliminary state. Handling large point sets may
        fail or be slow. We are working on improving this.

        Args:
            discrete (bool, optional): Discrete (True) or continous (False) pointsets. Defaults to False.

        Returns:
            Dictionary: All pointsets with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find pointsets')

    def _find_polylinesets(self):
        """A dictionary of GUIDs and paths to all polylinesets in the current Petrel project.
        Use method get_polylineset to select one of them. 

        ** The implementation of polyline sets is in a preliminary state. Handling large sets may
        fail or be slow. We are working on improving this.

        Returns:
            Dictionary: All polylinesets with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find polylinesets')

    def _find_wavelets(self):
        return self._find_paths_by_guids('find wavelets')

    def _find_workflows(self):
        return self._find_paths_by_guids('find workflows')

    def _find_reference_variables(self):
        return self._find_paths_by_guids('find reference variables')

    def _find_properties(self, discrete = False):
        """ Alias for method find_grid_properties().
        """
        return self._find_grid_properties(discrete = discrete)

    def _find_property_collections(self):
        """A dictionary of GUIDs and paths to all grid property collections in the current Petrel project.
        Use method get_property_collection to select one of them. 

        Returns:
            Dictionary: All grid property collections with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find property collections')

    def _find_surfaces(self):
        """A dictionary of GUIDs and paths to all surfaces in the current Petrel project.
        Use method get_surface to select one of them. 

        Returns:
            Dictionary: All surfaces with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find surfaces')

    def _find_surface_attributes(self, discrete = False):
        """A dictionary of GUIDs and paths to all surface attributes in the current Petrel project.
        Use method get_surface_attribute to select one of them. 
        
        Args:
            discrete (bool, optional): Discrete (True) or continous (False) surface attributes. Defaults to False.
        
        Returns:
            Dictionary: All surface attributes with GUID as key and path as value.
        """
        if discrete:
            request_string = 'find discrete surface properties'
        else:
            request_string = 'find surface properties'
        return self._find_paths_by_guids(request_string)

    def _find_seismic_2ds(self):
        """ Alias for method find_seismic_lines().
        """
        return self._find_seismic_lines()

    def _find_seismic_cubes(self):
        """A dictionary of GUIDs and paths to all seismic cubes in the current Petrel project.
        Use method get_seismic_cube to select one of them. 

        Returns:
            Dictionary: All seismic cubes with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find seismic cubes')

    def _find_seismic_lines(self):
        """A dictionary of GUIDs and paths to all seismic line objects in the current Petrel project.
        Use method get_seismic_line to select one of them.

        Returns:
            Dictionary: All seismic line objects with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find seismic 2ds')

    def _find_well_logs(self, discrete = False):
        """A dictionary of GUIDs and paths to all well logs in the current Petrel project.
        Use method get_well_log to select one of them. 

        Args:
            discrete (bool, optional): Discrete (True) or continous (False) global well logs. Defaults to False.

        Returns:
            Dictionary: All well logs with GUID as key and path as value.
        """
        if discrete:
            request_string = 'find discrete well logs'
        else:
            request_string = 'find well logs'
         
        return self._find_paths_by_guids(request_string)

    def _find_wells(self):
        """A dictionary of GUIDs and paths to all wells in the current Petrel project.
        Use method get_well to select one of them. 

        Returns:
            Dictionary: All wells with GUID as key and path as value.
        """
        return self._find_paths_by_guids('find boreholes')
    
    def _find_xyz_well_surveys(self):
        """A dictionary of _______ xyz well surveys"""
        return self._find_paths_by_guids('find xyz well surveys')

    def _find_xytvd_well_surveys(self):
        """A dictionary of _______ xytvd well surveys"""
        return self._find_paths_by_guids('find xytvd well surveys')

    def _find_dxdytvd_well_surveys(self):
        """A dictionary of _______ dxdytvd well surveys"""
        return self._find_paths_by_guids('find dxdytvd well surveys')

    def _find_mdinclazim_well_surveys(self):
        """A dictionary of _______ mdinclazim well surveys"""
        return self._find_paths_by_guids('find mdinclazim well surveys')

    def _find_explicit_well_surveys(self):
        """A dictionary of _______ explicit well surveys"""
        return self._find_paths_by_guids('find explicit well surveys')      

    def _find_observed_data(self):
        """A dictionary of observed data"""
        return self._find_paths_by_guids('find observed data')

    def _find_observed_data_sets(self):
        """A dictionary of observed data set"""
        return self._find_paths_by_guids('find observed data set')

    def _find_paths_by_guids(self, request_string):
        self._opened_test()
        request = petrelinterface_pb2.GetStringsMapRequest(request = request_string)
        responses = self._service_project.GetStringsMap(request)
        result = {}
        for response in responses:
            Utils.protobuf_map_to_dict(response.string_to_string_map, result)
        return result

    def _get_global_well_log(self, path, discrete = False):
        """Get a global well log in Petrel as a GlobalWellLog or DiscreteGlobalWellLog by its path or GUID as printed by method show_global_well_logs.

        Args:
            path (string): Either the path or GUID of the global well log.
            discrete (bool, optional): Get a discrete (True) or continous (False) global well log. Defaults to False.

        Returns:
            GlobalWellLog or DiscreteGlobalWellLog: Reference to a global well log object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.GetGlobalWellLog_Request(node_path = path, discrete_logs = discrete)
        reply = self._service_globalwelllog.GetGlobalWellLog(request)
        if not reply.guid:
            return None
        if discrete:
            return DiscreteGlobalWellLog(DiscreteGlobalWellLogGrpc(reply.guid, self))
        return GlobalWellLog(GlobalWellLogGrpc(reply.guid, self))
    
    def _get_grid(self, path):
        """Get a grid in Petrel as a Grid object by its path or GUID as printed by method show_grids.

        Args:
            path (string): Either the path or GUID of the grid.

        Returns:
            Grid: Reference to a grid object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_grid.GetGrid(request)
        if reply.guid:
            petrel_object_link = GridGrpc(reply.guid, self)
            return Grid(petrel_object_link)
        else:
            return None

    def _get_grid_property(self, path, discrete = False):
        """Get a grid property in Petrel as a GridProperty object by its path or GUID as printed by method show_grid_properties.

        Args:
            path (string): Either the path or GUID of the grid property.

        Args:
            path (string): Either the path or GUID of the grid.
            discrete (bool, optional): Get a discrete (True) or continous (False) grid property. Defaults to False.

        Returns:
            GridProperty: Reference to a grid property object in the current Petrel project.
        """
        request = petrelinterface_pb2.Property_Request(node_path = path, discrete = discrete)
        reply = self._service_grid_property.GetGridProperty(request)
            
        if not reply.guid:
            return None
        if discrete:
            return GridDiscreteProperty(GridDiscretePropertyGrpc(reply.guid, self))
    
        return GridProperty(GridPropertyGrpc(reply.guid, self))

    def _get_horizon_property(self, path):
        """Get a horizon property in Petrel as a HorizonProperty3d object by its path or GUID as printed by method show_horizon_properties.

        Args:
            path (string): Either the path or GUID of the horizon property object.

        Returns:
            HorizonPropery3d: Reference to a horizon property object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_horizon.GetHorizonProperty3d(request)
        if reply.guid:
            petrel_object_link = HorizonProperty3dGrpc(reply.guid, self)
            return HorizonProperty3d(petrel_object_link)
        else:
            return None

    def _get_horizon_interpretation_3d(self, path):
        """Get a horizon interpretation in Petrel as a HorizonInterpretation3d object by its path or GUID as printed by method show_horizon_interpretation.

        Args:
            path (string): Either the path or GUID of the horizon interpretation.

        Returns:
            HorizonInterpretation3d: Reference to a horizon interpretation object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_horizon.GetHorizonInterpretation3d(request)
        if reply.guid:
            petrel_object_link = HorizonInterpretation3dGrpc(reply.guid, self)
            return HorizonInterpretation3d(petrel_object_link)
        else:
            return None

    def _get_horizon_interpretation(self, path):
        """Get a horizon interpretation in Petrel as a HorizonInterpretation3d object by its path or GUID as printed by method show_horizon_interpretation.

        Args:
            path (string): Either the path or GUID of the horizon interpretation.

        Returns:
            HorizonInterpretation3d: Reference to a horizon interpretation object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_horizon_interpretation.GetHorizonInterpretation(request)
        if reply.guid:
            petrel_object_link = HorizonInterpretationGrpc(reply.guid, self)
            return HorizonInterpretation(petrel_object_link)
        else:
            return None

    def _get_wavelet(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_wavelet.GetWavelet(request)
        if reply.guid:
            petrel_object_link = WaveletGrpc(reply.guid, self)
            return Wavelet(petrel_object_link)
        else:
            return None

    def _get_workflow(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_workflow.GetWorkflow(request)
        if reply.guid:
            petrel_object_link = WorkflowGrpc(reply.guid, self)
            return Workflow(petrel_object_link)
        else:
            return None

    def _get_reference_variable(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_referencevariable.GetReferenceVariable(request)
        if reply.guid:
            petrel_object_link = ReferenceVariableGrpc(reply.guid, self)
            return ReferenceVariable(petrel_object_link)
        else:
            return None

    def _get_pointset(self, path):
        """Get a point set in Petrel as a PointSet object by its path or GUID as printed by method show_pointsets.

        ** The implementation of point sets is in a preliminary state. Handling large point sets may
        fail or be slow. We are working on improving this.

        Args:
            path (string): Either the path or GUID of the pointset.

        Returns:
            PointSet: Reference to a pointset object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_points.GetPointSet(request)
        if reply.guid:
            petrel_object_link = PointSetGrpc(reply.guid, self)
            return PointSet(petrel_object_link)
        else:
            return None

    def _get_polylineset(self, path):
        """Get a polyline set in Petrel as a PolylineSet by its path or GUID as printed by method show_polylinesets.

        ** The implementation of polyline sets is in a preliminary state. Handling large sets may
        fail or be slow. We are working on improving this.

        Args:
            path (string): Either the path or GUID of the polylineset.

        Returns:
            PolylineSet: Reference to a polylineset object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_polylines.GetPolylineSet(request)
        if reply.guid:
            petrel_object_link = PolylineSetGrpc(reply.guid, self)
            return PolylineSet(petrel_object_link)
        else:
            return None

    def _get_property(self, path, discrete = False):
        """Alias for method _get_grid_property().
        """
        return self._get_grid_property(path, discrete = discrete)    

    def _get_property_collection(self, path):
        """Get a property collection in Petrel as a PropertyCollection object by its path or GUID as printed by method show_property_collections.

        Args:
            path (string): Either the path or GUID of the grid property collection.

        Returns:
            PropertyCollection: Reference to a property collection object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.Property_Request(node_path = path)
        reply = self._service_grid_property.GetPropertyCollection(request)
        if reply.guid:
            petrel_object_link = PropertyCollectionGrpc(reply.guid, self)
            return PropertyCollection(petrel_object_link)
            
        else:
            return None

    def _get_seismic_2d(self, path):
        """Get a seismic line object in Petrel as a SeismicLine object by its path or GUID as printed by method show_seismic2ds.

        This is an alias for method _get_seismic_line.

        Args:
            path (string): Either the path or GUID of the seismic line object.

        Returns:
            SeismicLine: Reference to a seismic line object in the current Petrel project.
        """
        return self._get_seismic_line(path)

    def _get_seismic_cube(self, path):
        """Get a seismic cube in Petrel as a SeismicCube object by its path or GUID as printed by method show_seismic_cubes.

        Args:
            path (string): Either the path or GUID of the seismic cube.

        Returns:
            SeismicCube: Reference to a seismic cube object in the current Petrel project.
        """
        self._opened_test()

        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)        
        reply = self._service_seismic.GetSeismicCube(request)
        
        if reply.guid:
            petrel_object_link = SeismicCubeGrpc(reply.guid, self)
            return SeismicCube(petrel_object_link)
        else:
            return None

    def _get_seismic_line(self, path):
        """Get a seismic line object in Petrel as a SeismicLine object by its path or GUID as printed by method show_seismic2ds.

        Args:
            path (string): Either the path or GUID of the seismic line object.

        Returns:
            SeismicLine: Reference to a seismic line object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_seismic_2d.GetSeismic2D(request)
        if reply.guid:
            petrel_object_link = Seismic2DGrpc(reply.guid, self)
            return SeismicLine(petrel_object_link)
        else:
            return None

    def _get_surface(self, path):
        """Get a surface in Petrel as a Surface object by its path or GUID as printed by method show_surfaces.

        Args:
            path (string): Either the path or GUID of the surface.

        Returns:
            Surface: Reference to a surface object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_surface.GetSurface(request)
        if reply.guid:
            petrel_object_link = SurfaceGrpc(reply.guid, self)
            return Surface(petrel_object_link)
        return None
        
    def _get_surface_attribute(self, path, discrete = False):
        """Get a surface attribute in Petrel as a SurfaceAttribute or SurfaceDiscreteAttribute by its path or GUID as printed by method show_surface_attributes.

        Args:
            path (string): Either the path or GUID of the surface attribute.
            discrete (bool, optional): Get a discrete (True) or continous (False) surface attribute. Defaults to False.

        Returns:
            SurfaceAttribute or SurfaceDiscreteAttribute: Reference to a surface attribute object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.Property_Request(node_path = path, discrete = discrete)
        reply = self._service_surface_property.GetSurfaceProperty(request)
        if not reply.guid:
            return None
        if discrete:
            return SurfaceDiscreteAttribute(SurfaceDiscretePropertyGrpc(reply.guid, self))
        
        return SurfaceAttribute(SurfacePropertyGrpc(reply.guid, self))
    
    def _get_well(self, path):
        """Get a well in Petrel as a Well by its path or GUID as printed by method show_wells.

        Args:
            path (string): Either the path or GUID of the well.

        Returns:
            Well: Reference to a well object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_borehole.GetBorehole(request)
        if reply.guid:
            petrel_object_link = BoreholeGrpc(reply.guid, self)
            return Well(petrel_object_link)
        else:
            return None

    def _get_well_log(self, path, discrete = False):
        """Get a well log in Petrel as a WellLog or DiscreteWellLog by its path or GUID as printed by method show_well_logs.

        Args:
            path (string): Either the path or GUID of the well log.
            discrete (bool, optional): Get a discrete (True) or continous (False) well log. Defaults to False.

        Returns:
            WellLog or DiscreteWellLog: Reference to a well log object in the current Petrel project.
        """
        self._opened_test()
        request = petrelinterface_pb2.GetWellLog_Request(node_path = path, discrete_logs = discrete)
        reply = self._service_welllog.GetWellLog(request)
        if not reply.guid:
            return None
        if discrete:
            return DiscreteWellLog(DiscreteWellLogGrpc(reply.guid, self))
        return WellLog(WellLogGrpc(reply.guid, self))

    def _get_xyz_well_survey(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_xyz_well_survey.GetXyzWellSurvey(request)
        if reply.guid:
            petrel_object_link = XyzWellSurveyGrpc(reply.guid, self)
            return WellSurvey(petrel_object_link)
        else:
            return None

    def _get_xytvd_well_survey(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_xytvd_well_survey.GetXytvdWellSurvey(request)
        if reply.guid:
            petrel_object_link = XytvdWellSurveyGrpc(reply.guid, self)
            return WellSurvey(petrel_object_link)
        else:
            return None

    def _get_dxdytvd_well_survey(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_dxdytvd_well_survey.GetDxdytvdWellSurvey(request)
        if reply.guid:
            petrel_object_link = DxdytvdWellSurveyGrpc(reply.guid, self)
            return WellSurvey(petrel_object_link)
        else:
            return None

    def _get_mdinclazim_well_survey(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_mdinclazim_well_survey.GetMdinclazimWellSurvey(request)
        if reply.guid:
            petrel_object_link = MdinclazimWellSurveyGrpc(reply.guid, self)
            return WellSurvey(petrel_object_link)
        else:
            return None

    def _get_explicit_well_survey(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_explicit_well_survey.GetExplicitWellSurvey(request)
        if reply.guid:
            petrel_object_link = ExplicitWellSurveyGrpc(reply.guid, self)
            return WellSurvey(petrel_object_link)
        else:
            return None

    def _get_observed_data(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_observeddata.GetObservedData(request)
        if reply.guid:
            petrel_object_link = ObservedDataGrpc(reply.guid, self)
            return ObservedData(petrel_object_link)
        else:
            return None

    def _get_observed_data_set(self, path):
        self._opened_test()
        request = petrelinterface_pb2.PetrelObjectRequest(node_path = path)
        reply = self._service_observeddataset.GetObservedDataSet(request)
        if reply.guid:
            petrel_object_link = ObservedDataSetGrpc(reply.guid, self)
            return ObservedDataSet(petrel_object_link)
        else:
            return None

    def _get(self, obj_type, path):
        if obj_type == 'grid':
            return self._get_grid(path)

        if obj_type == 'grid property':
            return self._get_grid_property(path, discrete = False)

        if obj_type == 'grid discrete property':
            return self._get_grid_property(path, discrete = True)

        if obj_type == 'seismic cube':
            return self._get_seismic_cube(path)

        if obj_type == 'seismic 2d':
            return self._get_seismic_2d(path)

        if obj_type == 'surface':
            return self._get_surface(path)

        if obj_type == 'surface property':
            return self._get_surface_attribute(path)

        if obj_type == 'horizon interpretation 3d':
            return self._get_horizon_interpretation_3d(path)

        if obj_type == 'horizon interpretation':
            return self._get_horizon_interpretation(path)

        if obj_type == 'horizon property 3d':
            return self._get_horizon_property(path)

        if obj_type == 'surface discrete property':
            return self._get_surface_attribute(path, discrete = True)

        if obj_type == 'well':
            return self._get_well(path)

        if obj_type == 'well log':
            return self._get_well_log(path, discrete = False)

        if obj_type == 'discrete well log':
            return self._get_well_log(path, discrete = True)

        if obj_type == 'global well log':
            return self._get_global_well_log(path, discrete = False)

        if obj_type == 'global discrete well log':
            return self._get_global_well_log(path, discrete = True)

        if obj_type == 'pointset':
            return self._get_pointset(path)

        if obj_type == 'polylineset':
            return self._get_polylineset(path)

        if obj_type == 'wavelet':
            return self._get_wavelet(path)

        if obj_type == 'workflow':
            return self._get_workflow(path)

        if obj_type == 'referencevariable':
            return self._get_reference_variable(path)
        
        if obj_type == 'xyz well survey':
            return self._get_xyz_well_survey(path)

        if obj_type == 'xytvd well survey':
            return self._get_xytvd_well_survey(path)

        if obj_type == 'dxdytvd well survey':
            return self._get_dxdytvd_well_survey(path)

        if obj_type == 'mdinclazim well survey':
            return self._get_mdinclazim_well_survey(path)

        if obj_type == 'explicit well survey':
            return self._get_explicit_well_survey(path)

        if obj_type == "observed data":
            return self._get_observed_data(path)
        
        if obj_type == "observed data set":
            return self._get_observed_data_set(path)

        return None
        
    def _opened_test(self):
        if self._opened == PetrelConnectionState.UNOPENED:
            raise Exception('The connection is not opened. Call the open() method')
        if self._opened == PetrelConnectionState.CLOSED:
            raise Exception('The connection is closed. Make a new PetrelConnection instance')

    @property
    def discrete_global_well_logs(self) -> PO_DiscreteGlobalWellLogs:
        """Retrieve all discrete well logs in Petrel as DiscreteGlobalWellLog objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).  

        If multiple objects have the same path, a list of them is returned.

        Returns:
            DiscreteGlobalWellLogs: A dictionary of DiscreteGlobalWellLog objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.discrete_global_well_logs['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_DiscreteGlobalWellLogs(self)

    @property
    def discrete_grid_properties(self) -> PO_DiscreteProperties:
        """Retrieve all discrete grid properties in Petrel as GridDiscreteProperty objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            DiscreteProperties: A dictionary of GridDiscreteProperty objects by their path.
        
        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.discrete_grid_properties['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_DiscreteProperties(self)
    
    @property
    def discrete_properties(self) -> PO_DiscreteProperties:
        """DeprecationWarning: 'discrete_properties' has been removed. Use 'discrete_grid_properties' instead
        """
        warn("'discrete_properties' has been removed. Use 'discrete_grid_properties' instead", 
             DeprecationWarning, stacklevel=2)
        raise RuntimeError("'discrete_properties' has been removed. Use 'discrete_grid_properties' instead")     

    @property
    def discrete_well_logs(self) -> PO_DiscreteWellLogs:
        """Retrieve all discrete well logs in Petrel as DiscreteWellLog objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            DiscreteWellLogs: A dictionary of DiscreteWellLog objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.discrete_well_logs['Petrel path']

        With 'petrel' as your defined PetrelConnection. 
        """
        return PO_DiscreteWellLogs(self)

    @property
    def global_well_logs(self) -> PO_GlobalWellLogs:
        """Retrieve all global well logs in Petrel as GlobalWellLog objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).

        If multiple objects have the same path, a list of them is returned.
        
        Returns:
            GlobalWellLogs: A dictionary of GlobalWellLog objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.global_well_logs['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_GlobalWellLogs(self)

    @property
    def grid_properties(self) -> PO_Properties:
        """Retrieve all grid properties in Petrel as GridProperty objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            Properties: A dictionary of GridProperty objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.grid_properties['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_Properties(self)

    @property
    def grids(self) -> PO_Grids:
        """Retrieve all grids in Petrel as Grid objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            Grids: A dictionary of Grid objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.grids['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_Grids(self)

    @property
    def horizon_interpretation_3ds(self) -> PO_HorizonInterpretation3Ds:
        """Retrieve all 3D horizon interpretation objects in Petrel as HorizonInterpretation3d objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            HorizonInterpretation3Ds: A dictionary of HorizonInterpretation3d objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.horizon_interpretation_3ds['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_HorizonInterpretation3Ds(self)

    @property
    def horizon_interpretations(self) -> PO_HorizonInterpretations:
        """Retrieve all seismic horizon in Petrel as HorizonInterpretation objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).

        If multiple objects have the same path, a list of them is returned.
        
        Returns:
            HorizonInterpretation: A dictionary of HorizonInterpretation objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.horizon_interpretations['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """          
        return PO_HorizonInterpretations(self)

    @property
    def horizon_properties(self) -> PO_HorizonProperties:
        """Retrieve all horizon properties in Petrel as HorizonProperty objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).

        If multiple objects have the same path, a list of them is returned.
        
        Returns:
            HorizonProperties: A dictionary of HorizonProperty objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.horizon_properties['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """        
        return PO_HorizonProperties(self)

    @property
    def pointsets(self) -> PO_PointSets:
        """Retrieve all point sets in Petrel as PointSet objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            PointSets: A dictionary of PointSet objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.pointsets['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_PointSets(self)

    @property
    def polylinesets(self) -> PO_PolylineSets:
        """Retrieve all polyline sets in Petrel as PolylineSet objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            PolylineSets: A dictionary of PolylineSet objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.polylinesets['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_PolylineSets(self)

    @property
    def wavelets(self) -> PO_Wavelets:
        """Retrieve all wavelets in Petrel as Wavelet objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            Wavelets: A dictionary of Wavelet objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.wavelets['Petrel path']

        With 'petrel' as your defined PetrelConnection. 
        """
        return PO_Wavelets(self)

    @property # type: ignore
    @experimental_method
    def workflows(self) -> PO_Workflows:
        """Retrieve all workflows in Petrel as Workflows objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            Workflows: A dictionary of Workflow objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.workflows['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """         
        return PO_Workflows(self)

    @property
    def well_surveys(self) -> PO_WellSurveys:
        """Retrieve all well surveys in Petrel as WellSurvey objects
        and collect them in a dictionary with their paths as keys.
        All 5 types of well surveys in Petrel are treated as one object in Python Tool Pro
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).

        If multiple objects have the same path, a list of them is returned.
        
        Returns:
            Properties: A dictionary of WellSurveys objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.well_surveys['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_WellSurveys(self)

    @property
    def properties(self) -> PO_Properties:
        """DeprecationWarning: 'properties' has been removed. Use 'grid_properties' instead
        """
        warn("'properties' has been removed. Use 'grid_properties' instead", 
             DeprecationWarning, stacklevel=2)
        raise RuntimeError("'properties' has been removed. Use 'grid_properties' instead")

    @property
    def property_collections(self) -> PO_PropertyCollections:
        """Retrieve all property collections in Petrel as PropertyCollection objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            PropertyCollections: A dictionary of PropertyCollection objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.property_collections['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_PropertyCollections(self)

    @property
    def seismic_2ds(self) -> PO_Seismic2Ds:
        """Retrieve all seismic lines in Petrel as SeismicLine objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            Seismic2Ds: A dictionary of SeismicLine objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.seismic_2ds['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_Seismic2Ds(self)

    @property
    def seismic_cubes(self) -> PO_SeismicCubes:
        """Retrieve all seismic cubes in Petrel as SeismicCube objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Seismic cubes of format SEG-Y are read-only.

        Returns:
            SeismicCubes: A dictionary of SeismicCubes objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.seismic_cubes['Petrel path']

        With 'petrel' as your defined PetrelConnection.     
        """
        return PO_SeismicCubes(self)

    @property
    def seismic_lines(self) -> PO_Seismic2Ds:
        """Retrieve all seismic lines in Petrel as SeismicLine objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        This is an alias for the member named seismic_2ds of this class.

        Returns:
            Seismic2Ds: A dictionary of SeismicLine objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.seismic_lines['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_Seismic2Ds(self)

    @property
    def surface_attributes(self) -> PO_SurfaceAttributes:
        """Retrieve all surface attributes in Petrel as SurfaceAttribute objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).

        If multiple objects have the same path, a list of them is returned.
        
        Returns:
            SurfacesAttributes: A dictionary of SurfaceAttribute objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.surface_attributes['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_SurfaceAttributes(self)

    @property
    def surface_discrete_attributes(self) -> PO_SurfaceDiscreteAttributes:
        """Retrieve all discrete surface attributes in Petrel as SurfaceDiscreteAttribute objects
        and collect them in a dictionary with their paths as keys.

        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            SurfaceDiscreteAttributes: A dictionary of SurfaceDiscreteAttribute objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.surface_discrete_attributes['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_SurfaceDiscreteAttributes(self)
    
    # To maintain naming patterns, create this synonym
    discrete_surface_attributes = surface_discrete_attributes
    
    @property
    def surfaces(self) -> PO_Surfaces:
        """Retrieve all surfaces in Petrel as Surface objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).

        If multiple objects have the same path, a list of them is returned.
        
        Returns:
            Surfaces: A dictionary of Surface objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.surfaces['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_Surfaces(self)

    @property
    def well_logs(self) -> PO_WellLogs:
        """Retrieve all well logs in Petrel as WellLog objects
        and collect them in a dictionary with their paths as keys.

        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            WellLogs: A dictionary of WellLog objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.well_logs['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_WellLogs(self)

    @property
    def wells(self) -> PO_Wells:
        """Retrieve all wells in Petrel as Well objects
        and collect them in a dictionary with their paths as keys.
        
        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            Wells: A dictionary of Well objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.wells['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_Wells(self)

    @property
    def predefined_global_observed_data(self) -> typing.Dict[str, str]:
        """Returns a dictionary with the predefined global observed data in the petrel project

        keys: the name of the predefined global observed data
        values: the ID used to identify the predefined global observed data
        """
        self._opened_test()
        request = petrelinterface_pb2.EmptyRequest()
        response = self._service_project.Project_GetRegisteredObservedDataVersions(request)
        return Utils.protobuf_map_to_dict(response.string_to_string_map)

    @property
    def observed_data_sets(self) -> PO_ObservedDataSets:
        """Retrieve all observed data sets in Petrel as ObservedDataSet objects
        and collect them in a dictionary with their paths as keys.

        When iterated over, the objects are returned, not their paths (unlike a standard
        Python dictionary which returns the keys).
        
        If multiple objects have the same path, a list of them is returned.

        Returns:
            ObservedDataSets: A dictionary of ObservedDataSet objects by their path.

        Examples
        --------
        To retrieve a specific Petrel object use:
         
        my_var=petrel.observed_data_sets['Petrel path']

        With 'petrel' as your defined PetrelConnection.
        """
        return PO_ObservedDataSets(self)

    def _get_global_well_log_by_guid(self, guid: str, discrete: bool = False) -> typing.Union[DiscreteGlobalWellLog, GlobalWellLog]:
        if discrete:
            return DiscreteGlobalWellLog(DiscreteGlobalWellLogGrpc(guid, self))
        return GlobalWellLog(GlobalWellLogGrpc(guid, self))
    
    def _get_grid_by_guid(self, guid: str) -> Grid:
        petrel_object_link = GridGrpc(guid, self)
        return Grid(petrel_object_link)

    def _get_grid_property_by_guid(self, guid: str, discrete: bool = False) -> typing.Union[GridDiscreteProperty, GridProperty]:
        if discrete:
            return GridDiscreteProperty(GridDiscretePropertyGrpc(guid, self))
        return GridProperty(GridPropertyGrpc(guid, self))

    def _get_horizon_property_by_guid(self, guid: str) -> HorizonProperty3d:
        petrel_object_link = HorizonProperty3dGrpc(guid, self)
        return HorizonProperty3d(petrel_object_link)

    def _get_horizon_interpretation_3d_by_guid(self, guid: str) -> HorizonInterpretation3d:
        petrel_object_link = HorizonInterpretation3dGrpc(guid, self)
        return HorizonInterpretation3d(petrel_object_link)

    def _get_horizon_interpretation_by_guid(self, guid: str) -> HorizonInterpretation:
        petrel_object_link = HorizonInterpretationGrpc(guid, self)
        return HorizonInterpretation(petrel_object_link)

    def _get_wavelet_by_guid(self, guid: str) -> Wavelet:
        petrel_object_link = WaveletGrpc(guid, self)
        return Wavelet(petrel_object_link)

    def _get_workflow_by_guid(self, guid: str) -> Workflow:
        petrel_object_link = WorkflowGrpc(guid, self)
        return Workflow(petrel_object_link)

    def _get_reference_variable_by_guid(self, guid: str) -> ReferenceVariable:
        petrel_object_link = ReferenceVariableGrpc(guid, self)
        return ReferenceVariable(petrel_object_link)

    def _get_pointset_by_guid(self, guid: str) -> PointSet:
        petrel_object_link = PointSetGrpc(guid, self)
        return PointSet(petrel_object_link)

    def _get_polylineset_by_guid(self, guid: str) -> PolylineSet:
        petrel_object_link = PolylineSetGrpc(guid, self)
        return PolylineSet(petrel_object_link)

    def _get_property_by_guid(self, guid: str, discrete: bool = False):
        return self._get_grid_property_by_guid(guid, discrete = discrete)    

    def _get_property_collection_by_guid(self, guid: str) -> PropertyCollection:
        petrel_object_link = PropertyCollectionGrpc(guid, self)
        return PropertyCollection(petrel_object_link)

    def _get_seismic_2d_by_guid(self, guid: str):
        return self._get_seismic_line_by_guid(guid)

    def _get_seismic_cube_by_guid(self, guid: str) -> SeismicCube:
        petrel_object_link = SeismicCubeGrpc(guid, self)
        return SeismicCube(petrel_object_link)

    def _get_seismic_line_by_guid(self, guid: str) -> SeismicLine:
        petrel_object_link = Seismic2DGrpc(guid, self)
        return SeismicLine(petrel_object_link)

    def _get_surface_by_guid(self, guid: str) -> Surface:
        petrel_object_link = SurfaceGrpc(guid, self)
        return Surface(petrel_object_link)
        
    def _get_surface_attribute_by_guid(self, guid: str, discrete: bool = False) -> typing.Union[SurfaceDiscreteAttribute, SurfaceAttribute]:
        if discrete:
            return SurfaceDiscreteAttribute(SurfaceDiscretePropertyGrpc(guid, self))
        return SurfaceAttribute(SurfacePropertyGrpc(guid, self))
    
    def _get_well_by_guid(self, guid: str) -> Well:
        petrel_object_link = BoreholeGrpc(guid, self)
        return Well(petrel_object_link)

    def _get_well_log_by_guid(self, guid: str, discrete: bool = False) -> typing.Union[DiscreteWellLog, WellLog]:
        if discrete:
            return DiscreteWellLog(DiscreteWellLogGrpc(guid, self))
        return WellLog(WellLogGrpc(guid, self))

    def _get_xyz_well_survey_by_guid(self, guid: str) -> WellSurvey:
        petrel_object_link = XyzWellSurveyGrpc(guid, self)
        return WellSurvey(petrel_object_link)

    def _get_xytvd_well_survey_by_guid(self, guid: str) -> WellSurvey:
        petrel_object_link = XytvdWellSurveyGrpc(guid, self)
        return WellSurvey(petrel_object_link)

    def _get_dxdytvd_well_survey_by_guid(self, guid: str) -> WellSurvey:
        petrel_object_link = DxdytvdWellSurveyGrpc(guid, self)
        return WellSurvey(petrel_object_link)

    def _get_mdinclazim_well_survey_by_guid(self, guid: str) -> WellSurvey:
        petrel_object_link = MdinclazimWellSurveyGrpc(guid, self)
        return WellSurvey(petrel_object_link)

    def _get_explicit_well_survey_by_guid(self, guid: str) -> WellSurvey:
        petrel_object_link = ExplicitWellSurveyGrpc(guid, self)
        return WellSurvey(petrel_object_link)

    def _get_observed_data_by_guid(self, guid: str) -> ObservedData:
        petrel_object_link = ObservedDataGrpc(guid, self)
        return ObservedData(petrel_object_link)

    def _get_observed_data_set_by_guid(self, guid: str) -> ObservedDataSet:
        petrel_object_link = ObservedDataSetGrpc(guid, self)
        return ObservedDataSet(petrel_object_link)
