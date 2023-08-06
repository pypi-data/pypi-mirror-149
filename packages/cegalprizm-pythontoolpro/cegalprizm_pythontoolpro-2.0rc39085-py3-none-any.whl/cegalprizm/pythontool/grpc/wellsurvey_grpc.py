# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc
from cegalprizm.pythontool.grpc import petrelinterface_pb2
from cegalprizm.pythontool.grpc import borehole_grpc
import sys
import math

import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.wellsurvey_hub import XyzWellSurveyHub, XytvdWellSurveyHub, DxdytvdWellSurveyHub, ExplicitWellSurveyHub, MdinclazimWellSurveyHub

class BaseWellSurveyGrpc(PetrelObjectGrpc):
        def __init__(self, sub_type: str, guid: str, petrel_connection: "PetrelConnection"):
            super(BaseWellSurveyGrpc, self).__init__(sub_type, guid, petrel_connection)
            self._guid = guid
            self._plink = petrel_connection
            self._channel = petrel_connection._service_explicit_well_survey

        def ClonePetrelObject(self, path_of_clone, copy_values):
            already_exist = self._plink._get("xyz well survey", path_of_clone) is not None
            if already_exist:
                raise Exception(f'Well survey Petrel object with path "{path_of_clone}" already exist.')

            already_exist = self._plink._get("xytvd well survey", path_of_clone) is not None
            if already_exist:
                raise Exception(f'Well survey Petrel object with path "{path_of_clone}" already exist.')

            already_exist = self._plink._get("dxdytvd well survey", path_of_clone) is not None
            if already_exist:
                raise Exception(f'Well survey Petrel object with path "{path_of_clone}" already exist.')

            already_exist = self._plink._get("mdinclazim well survey", path_of_clone) is not None
            if already_exist:
                raise Exception(f'Well survey Petrel object with path "{path_of_clone}" already exist.')

            already_exist = self._plink._get("explicit well survey", path_of_clone) is not None
            if already_exist:
                raise Exception(f'Well survey Petrel object with path "{path_of_clone}" already exist.')
            
            return super(BaseWellSurveyGrpc, self).ClonePetrelObject(path_of_clone, copy_values)
    
class XyzWellSurveyGrpc(BaseWellSurveyGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(XyzWellSurveyGrpc, self).__init__('xyz well survey', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._xyzwellsurvey_channel = typing.cast("XyzWellSurveyHub", petrel_connection._service_xyz_well_survey) # type: ignore

    def __str__(self):
        return 'XyzWellSurvey(petrel_name="{}")'.format(self.GetPetrelName())

    def RecordCount(self) -> int:
        self._plink._opened_test()

        request = petrelinterface_pb2.XyzWellSurvey_RecordCount_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._xyzwellsurvey_channel.XyzWellSurvey_RecordCount(request) 
             
        return response.RecordCount 
    
    def GetXs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XyzWellSurvey_GetXs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xyzwellsurvey_channel.XyzWellSurvey_GetXs(request)
        
        return [item for sublist in responses for item in sublist.GetXs]
    
    def GetYs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XyzWellSurvey_GetYs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xyzwellsurvey_channel.XyzWellSurvey_GetYs(request)
        
        return [item for sublist in responses for item in sublist.GetYs]
    
    def GetZs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XyzWellSurvey_GetZs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xyzwellsurvey_channel.XyzWellSurvey_GetZs(request)
        
        return [item for sublist in responses for item in sublist.GetZs]
    
    def GetMds(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XyzWellSurvey_GetMds_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xyzwellsurvey_channel.XyzWellSurvey_GetMds(request)
        
        return [item for sublist in responses for item in sublist.GetMds]
    
    def GetIncls(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XyzWellSurvey_GetIncls_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xyzwellsurvey_channel.XyzWellSurvey_GetIncls(request)
        
        return [item for sublist in responses for item in sublist.GetIncls]
    
    def GetAzims(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XyzWellSurvey_GetAzims_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xyzwellsurvey_channel.XyzWellSurvey_GetAzims(request)
        
        return [item for sublist in responses for item in sublist.GetAzims]

    def SetRecords(self, xs, ys, zs):
        self._plink._opened_test()

        well_survey_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)

        if (len(xs) == 0):
            iterable_requests = [petrelinterface_pb2.XyzWellSurvey_SetRecords_Request(guid = well_survey_guid, xs = xs, ys = ys, zs = zs)]
        else:
            byte_size_one_record = sys.getsizeof(xs[0]) + sys.getsizeof(ys[0]) + sys.getsizeof(zs[0])
            num_records_per_request = math.floor(self._plink._preferred_streamed_unit_bytes / byte_size_one_record)
            iterable_requests = list(map(
                lambda start_index : petrelinterface_pb2.XyzWellSurvey_SetRecords_Request(
                            guid = well_survey_guid, 
                            xs = xs[start_index:(start_index + num_records_per_request)], 
                            ys = ys[start_index:(start_index + num_records_per_request)], 
                            zs = zs[start_index:(start_index + num_records_per_request)]
                            ),
                range(0, len(xs), num_records_per_request)
            ))

        ok = self._xyzwellsurvey_channel.XyzWellSurvey_SetRecords((v for v in iterable_requests))
        return ok.value

    def SetSurveyAsDefinitive(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.XyzWellSurvey_SetSurveyAsDefinitive_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._xyzwellsurvey_channel.XyzWellSurvey_SetSurveyAsDefinitive(request)
             
        return response.SetSurveyAsDefinitive

    def TieInMd(self) -> float:
        self._plink._opened_test()

        request = petrelinterface_pb2.XyzWellSurvey_TieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._xyzwellsurvey_channel.XyzWellSurvey_TieInMd(request) 
             
        return response.TieInMd 
    
    def SetTieInMd(self, tieInMd):
        self._plink._opened_test()

        request = petrelinterface_pb2.XyzWellSurvey_SetTieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , tieInMd = tieInMd
        )

        response = self._xyzwellsurvey_channel.XyzWellSurvey_SetTieInMd(request)
             
        return response.SetTieInMd
    
    def IsLateral(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.XyzWellSurvey_IsLateral_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._xyzwellsurvey_channel.XyzWellSurvey_IsLateral(request)
             
        return response.IsLateral

    def GetParentPythonBoreholeObject(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.XyzWellSurvey_GetParentPythonBoreholeObject_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._xyzwellsurvey_channel.XyzWellSurvey_GetParentPythonBoreholeObject(request)
        return borehole_grpc.BoreholeGrpc(response.guid.guid, self._plink)

class XytvdWellSurveyGrpc(BaseWellSurveyGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(XytvdWellSurveyGrpc, self).__init__('xytvd well survey', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._xytvdwellsurvey_channel = typing.cast("XytvdWellSurveyHub", petrel_connection._service_xytvd_well_survey) # type: ignore

    def __str__(self):
        return 'XytvdWellSurvey(petrel_name="{}")'.format(self.GetPetrelName())


    def RecordCount(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.XytvdWellSurvey_RecordCount_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._xytvdwellsurvey_channel.XytvdWellSurvey_RecordCount(request)
             
        return response.RecordCount
    
    def GetXs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XytvdWellSurvey_GetXs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xytvdwellsurvey_channel.XytvdWellSurvey_GetXs(request)
        
        return [item for sublist in responses for item in sublist.GetXs]
    
    def GetYs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XytvdWellSurvey_GetYs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xytvdwellsurvey_channel.XytvdWellSurvey_GetYs(request)
        
        return [item for sublist in responses for item in sublist.GetYs]
    
    def GetTvds(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XytvdWellSurvey_GetTvds_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xytvdwellsurvey_channel.XytvdWellSurvey_GetTvds(request)
        
        return [item for sublist in responses for item in sublist.GetTvds]

    def GetZs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XytvdWellSurvey_GetZs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xytvdwellsurvey_channel.XytvdWellSurvey_GetZs(request)
        
        return [item for sublist in responses for item in sublist.GetZs]

    def GetMds(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XytvdWellSurvey_GetMds_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xytvdwellsurvey_channel.XytvdWellSurvey_GetMds(request)
        
        return [item for sublist in responses for item in sublist.GetMds]
    
    def GetIncls(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XytvdWellSurvey_GetIncls_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xytvdwellsurvey_channel.XytvdWellSurvey_GetIncls(request)
        
        return [item for sublist in responses for item in sublist.GetIncls]
    
    def GetAzims(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.XytvdWellSurvey_GetAzims_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._xytvdwellsurvey_channel.XytvdWellSurvey_GetAzims(request)
        
        return [item for sublist in responses for item in sublist.GetAzims]
    
    def SetRecords(self, xs, ys, tvds):
        self._plink._opened_test()

        well_survey_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)

        if(len(xs) == 0):
            iterable_requests = [petrelinterface_pb2.XytvdWellSurvey_SetRecords_Request(guid = well_survey_guid, xs = xs, ys = ys, tvds = tvds)]
        else:
            byte_size_one_record = sys.getsizeof(xs[0]) + sys.getsizeof(ys[0]) + sys.getsizeof(tvds[0])
            num_records_per_request = math.floor(self._plink._preferred_streamed_unit_bytes / byte_size_one_record)
            iterable_requests = list(map(
                lambda start_index : petrelinterface_pb2.XytvdWellSurvey_SetRecords_Request(
                            guid = well_survey_guid, 
                            xs = xs[start_index:(start_index + num_records_per_request)], 
                            ys = ys[start_index:(start_index + num_records_per_request)], 
                            tvds = tvds[start_index:(start_index + num_records_per_request)]
                            ),
                range(0, len(xs), num_records_per_request)
            ))

        ok = self._xytvdwellsurvey_channel.XytvdWellSurvey_SetRecords((v for v in iterable_requests) )
        return ok.value

    def SetSurveyAsDefinitive(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.XytvdWellSurvey_SetSurveyAsDefinitive_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._xytvdwellsurvey_channel.XytvdWellSurvey_SetSurveyAsDefinitive(request)
             
        return response.SetSurveyAsDefinitive

    def TieInMd(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.XytvdWellSurvey_TieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._xytvdwellsurvey_channel.XytvdWellSurvey_TieInMd(request)
             
        return response.TieInMd
    
    def SetTieInMd(self, tieInMd):
        self._plink._opened_test()

        request = petrelinterface_pb2.XytvdWellSurvey_SetTieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , tieInMd = tieInMd
        )

        response = self._xytvdwellsurvey_channel.XytvdWellSurvey_SetTieInMd(request)
             
        return response.SetTieInMd
    
    def IsLateral(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.XytvdWellSurvey_IsLateral_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._xytvdwellsurvey_channel.XytvdWellSurvey_IsLateral(request)
             
        return response.IsLateral

    def GetParentPythonBoreholeObject(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.XytvdWellSurvey_GetParentPythonBoreholeObject_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._xytvdwellsurvey_channel.XytvdWellSurvey_GetParentPythonBoreholeObject(request)
        return borehole_grpc.BoreholeGrpc(response.guid.guid, self._plink)

class DxdytvdWellSurveyGrpc(BaseWellSurveyGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(DxdytvdWellSurveyGrpc, self).__init__('dxdytvd well survey', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._dxdytvdwellsurvey_channel = typing.cast("DxdytvdWellSurveyHub", petrel_connection._service_dxdytvd_well_survey) # type: ignore 

    
    def __str__(self):
        return 'DxdytvdWellSurvey(petrel_name="{}")'.format(self.GetPetrelName())


    def RecordCount(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.DxdytvdWellSurvey_RecordCount_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_RecordCount(request)
             
        return response.RecordCount

    def AzimuthReferenceIsGridNorth(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.DxdytvdWellSurvey_AzimuthReferenceIsGridNorth_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_AzimuthReferenceIsGridNorth(request)
             
        return response.AzimuthReferenceIsGridNorth
    
    def GetDxs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetDxs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetDxs(request)
        
        return [item for sublist in responses for item in sublist.GetDxs]
    
    def GetDys(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetDys_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetDys(request)
        
        return [item for sublist in responses for item in sublist.GetDys]
    
    def GetTvds(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetTvds_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetTvds(request)
        
        return [item for sublist in responses for item in sublist.GetTvds]

    def GetXs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetXs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetXs(request)
        
        return [item for sublist in responses for item in sublist.GetXs]
    
    def GetYs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetYs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetYs(request)
        
        return [item for sublist in responses for item in sublist.GetYs]
    
    def GetZs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetZs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetZs(request)
        
        return [item for sublist in responses for item in sublist.GetZs]

    def GetMds(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetMds_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetMds(request)
        
        return [item for sublist in responses for item in sublist.GetMds]
    
    def GetIncls(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetIncls_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetIncls(request)
        
        return [item for sublist in responses for item in sublist.GetIncls]
    
    def GetAzims(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetAzims_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetAzims(request)
        
        return [item for sublist in responses for item in sublist.GetAzims]
    
    def SetRecords(self, dxs, dys, tvds):
        self._plink._opened_test()

        well_survey_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)

        if(len(dxs) == 0):
            iterable_requests = [petrelinterface_pb2.DxdytvdWellSurvey_SetRecords_Request(guid = well_survey_guid, dxs = dxs, dys = dys, tvds = tvds)]
        else:
            byte_size_one_record = sys.getsizeof(dxs[0]) + sys.getsizeof(dys[0]) + sys.getsizeof(tvds[0])
            num_records_per_request = math.floor(self._plink._preferred_streamed_unit_bytes / byte_size_one_record)
            
            well_survey_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            iterable_requests = list(map(
                lambda start_index : petrelinterface_pb2.DxdytvdWellSurvey_SetRecords_Request(
                            guid = well_survey_guid, 
                            dxs = dxs[start_index:(start_index + num_records_per_request)], 
                            dys = dys[start_index:(start_index + num_records_per_request)], 
                            tvds = tvds[start_index:(start_index + num_records_per_request)]
                            ),
                range(0, len(dxs), num_records_per_request)
            ))

        ok = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_SetRecords((v for v in iterable_requests) )
        return ok.value

    def SetSurveyAsDefinitive(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.DxdytvdWellSurvey_SetSurveyAsDefinitive_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_SetSurveyAsDefinitive(request)
             
        return response.SetSurveyAsDefinitive

    def TieInMd(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.DxdytvdWellSurvey_TieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_TieInMd(request)
             
        return response.TieInMd
    
    def SetTieInMd(self, tieInMd):
        self._plink._opened_test()

        request = petrelinterface_pb2.DxdytvdWellSurvey_SetTieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , tieInMd = tieInMd
        )

        response = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_SetTieInMd(request)
             
        return response.SetTieInMd
    
    def IsLateral(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.DxdytvdWellSurvey_IsLateral_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_IsLateral(request)
             
        return response.IsLateral

    def GetParentPythonBoreholeObject(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.DxdytvdWellSurvey_GetParentPythonBoreholeObject_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._dxdytvdwellsurvey_channel.DxdytvdWellSurvey_GetParentPythonBoreholeObject(request)
        return borehole_grpc.BoreholeGrpc(response.guid.guid, self._plink)

class MdinclazimWellSurveyGrpc(BaseWellSurveyGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(MdinclazimWellSurveyGrpc, self).__init__('mdinclazim well survey', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._mdinclazimwellsurvey_channel = typing.cast("MdinclazimWellSurveyHub", petrel_connection._service_mdinclazim_well_survey) # type: ignore

    def __str__(self):
        return 'MdinclazimWellSurvey(petrel_name="{}")'.format(self.GetPetrelName())


    def RecordCount(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.MdinclazimWellSurvey_RecordCount_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_RecordCount(request)
             
        return response.RecordCount

    def AzimuthReferenceIsGridNorth(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.MdinclazimWellSurvey_AzimuthReferenceIsGridNorth_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_AzimuthReferenceIsGridNorth(request)
             
        return response.AzimuthReferenceIsGridNorth

    def GetMds(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.MdinclazimWellSurvey_GetMds_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_GetMds(request)
        
        return [item for sublist in responses for item in sublist.GetMds]
    
    def GetIncls(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.MdinclazimWellSurvey_GetIncls_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_GetIncls(request)
        
        return [item for sublist in responses for item in sublist.GetIncls]
    
    def GetAzims(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.MdinclazimWellSurvey_GetAzims_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_GetAzims(request)
        
        return [item for sublist in responses for item in sublist.GetAzims]
        
    def GetXs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.MdinclazimWellSurvey_GetXs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_GetXs(request)
        
        return [item for sublist in responses for item in sublist.GetXs]
    
    def GetYs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.MdinclazimWellSurvey_GetYs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_GetYs(request)
        
        return [item for sublist in responses for item in sublist.GetYs]
    
    def GetZs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.MdinclazimWellSurvey_GetZs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_GetZs(request)
        
        return [item for sublist in responses for item in sublist.GetZs]

    def IsAzimuthReferenceGridNorth(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.MdinclazimWellSurvey_IsAzimuthReferenceGridNorth_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_IsAzimuthReferenceGridNorth(request)
             
        return response.IsAzimuthReferenceGridNorth

    def SetRecords(self, mds, incls, azims):
        self._plink._opened_test()

        well_survey_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)

        if(len(mds) == 0):
            iterable_requests = [petrelinterface_pb2.MdinclazimWellSurvey_SetRecords_Request(guid = well_survey_guid, mds = mds, incls = incls, azims = azims)]
        else:
            byte_size_one_record = sys.getsizeof(mds[0]) + sys.getsizeof(incls[0]) + sys.getsizeof(azims[0])
            num_records_per_request = math.floor(self._plink._preferred_streamed_unit_bytes / byte_size_one_record)
            
            well_survey_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            iterable_requests = list(map(
                lambda start_index : petrelinterface_pb2.MdinclazimWellSurvey_SetRecords_Request(
                            guid = well_survey_guid, 
                            mds = mds[start_index:(start_index + num_records_per_request)], 
                            incls = incls[start_index:(start_index + num_records_per_request)], 
                            azims = azims[start_index:(start_index + num_records_per_request)]
                            ),
                range(0, len(mds), num_records_per_request)
            ))

        ok = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_SetRecords((v for v in iterable_requests) )
        return ok.value

    def SetSurveyAsDefinitive(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.MdinclazimWellSurvey_SetSurveyAsDefinitive_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_SetSurveyAsDefinitive(request)
             
        return response.SetSurveyAsDefinitive

    def TieInMd(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.MdinclazimWellSurvey_TieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_TieInMd(request)
             
        return response.TieInMd
    
    def SetTieInMd(self, tieInMd):
        self._plink._opened_test()

        request = petrelinterface_pb2.MdinclazimWellSurvey_SetTieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , tieInMd = tieInMd
        )

        response = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_SetTieInMd(request)
             
        return response.SetTieInMd
    
    def IsLateral(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.MdinclazimWellSurvey_IsLateral_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_IsLateral(request)
             
        return response.IsLateral

    def GetParentPythonBoreholeObject(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.MdinclazimWellSurvey_GetParentPythonBoreholeObject_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._mdinclazimwellsurvey_channel.MdinclazimWellSurvey_GetParentPythonBoreholeObject(request)
        return borehole_grpc.BoreholeGrpc(response.guid.guid, self._plink)

class ExplicitWellSurveyGrpc(BaseWellSurveyGrpc):
    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(ExplicitWellSurveyGrpc, self).__init__('explicit well survey', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._explicittwellsurvey_channel = typing.cast("ExplicitWellSurveyHub", petrel_connection._service_explicit_well_survey) # type: ignore

    def __str__(self):
        return 'ExplicitWellSurvey(petrel_name="{}")'.format(self.GetPetrelName())

    def RecordCount(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.ExplicitWellSurvey_RecordCount_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._explicittwellsurvey_channel.ExplicitWellSurvey_RecordCount(request)
             
        return response.RecordCount
    
    def GetXs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.ExplicitWellSurvey_GetXs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._explicittwellsurvey_channel.ExplicitWellSurvey_GetXs(request)
        
        return [item for sublist in responses for item in sublist.GetXs]
    
    def GetYs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.ExplicitWellSurvey_GetYs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._explicittwellsurvey_channel.ExplicitWellSurvey_GetYs(request)
        
        return [item for sublist in responses for item in sublist.GetYs]
    
    def GetZs(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.ExplicitWellSurvey_GetZs_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._explicittwellsurvey_channel.ExplicitWellSurvey_GetZs(request)
        
        return [item for sublist in responses for item in sublist.GetZs]
    
    def GetMds(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.ExplicitWellSurvey_GetMds_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._explicittwellsurvey_channel.ExplicitWellSurvey_GetMds(request)
        
        return [item for sublist in responses for item in sublist.GetMds]
    
    def GetIncls(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.ExplicitWellSurvey_GetIncls_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._explicittwellsurvey_channel.ExplicitWellSurvey_GetIncls(request)
        
        return [item for sublist in responses for item in sublist.GetIncls]
    
    def GetAzims(self):
        self._plink._opened_test()
    
        request = petrelinterface_pb2.ExplicitWellSurvey_GetAzims_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        responses = self._explicittwellsurvey_channel.ExplicitWellSurvey_GetAzims(request)
        
        return [item for sublist in responses for item in sublist.GetAzims]

    def SetSurveyAsDefinitive(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.ExplicitWellSurvey_SetSurveyAsDefinitive_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._explicittwellsurvey_channel.ExplicitWellSurvey_SetSurveyAsDefinitive(request)
             
        return response.SetSurveyAsDefinitive

    def TieInMd(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.ExplicitWellSurvey_TieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._explicittwellsurvey_channel.ExplicitWellSurvey_TieInMd(request)
             
        return response.TieInMd
    
    def SetTieInMd(self, tieInMd):
        self._plink._opened_test()

        request = petrelinterface_pb2.ExplicitWellSurvey_SetTieInMd_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
            , tieInMd = tieInMd
        )

        response = self._explicittwellsurvey_channel.ExplicitWellSurvey_SetTieInMd(request)
             
        return response.SetTieInMd
    
    def IsLateral(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.ExplicitWellSurvey_IsLateral_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._explicittwellsurvey_channel.ExplicitWellSurvey_IsLateral(request)
             
        return response.IsLateral

    def GetParentPythonBoreholeObject(self):
        self._plink._opened_test()
        request = petrelinterface_pb2.ExplicitWellSurvey_GetParentPythonBoreholeObject_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )
        response = self._explicittwellsurvey_channel.ExplicitWellSurvey_GetParentPythonBoreholeObject(request)
        return borehole_grpc.BoreholeGrpc(response.guid.guid, self._plink)


