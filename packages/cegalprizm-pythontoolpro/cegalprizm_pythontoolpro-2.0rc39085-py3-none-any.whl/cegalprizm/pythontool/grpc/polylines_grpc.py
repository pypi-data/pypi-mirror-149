# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from .petrelobject_grpc import PetrelObjectGrpc

from cegalprizm.pythontool.grpc import petrelinterface_pb2
from .petrelinterface_pb2 import Primitives
from .points_grpc import PropertyTableHandler
from distutils.util import strtobool

from math import ceil

import typing
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.petrelconnection import PetrelConnection
    from cegalprizm.pythontool.oophub.polylines_hub import PolylinesHub

class PolylineSetGrpc(PetrelObjectGrpc):

    def __init__(self, guid: str, petrel_connection: "PetrelConnection"):
        super(PolylineSetGrpc, self).__init__('polylineset', guid, petrel_connection)
        self._guid = guid
        self._plink = petrel_connection
        self._channel = typing.cast("PolylinesHub", petrel_connection._service_polylines)
        self._table_handler = PropertyTableHandler(self._guid, self._plink, self._channel, 'polylineset')

    def GetNumPolylines(self) -> int:
        self._plink._opened_test()
        request = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)        
        return self._channel.PolylineSet_GetNumPolylines(request).value 

    def GetDisplayUnitSymbol(self, idx):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndex(
            guid = po_guid,
            index = idx
        )
        return self._channel.PolylineSet_DisplayUnitSymbol(request).value

    def IsClosed(self, idx) -> bool:
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndex(
            guid = po_guid,
            index = idx
        )
        return self._channel.PolylineSet_IsClosed(request).value 

    def GetPoints(self, idx):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndex(guid = po_guid, index = idx)        
        responses = self._channel.PolylineSet_GetPoints(request)
        points = []
        for response in responses:
            point = Primitives.Double3(x = response.x, y = response.y, z = response.z)
            points.append(point)

        point_array = [None] * 3
        point_array[0] = []
        point_array[1] = []
        point_array[2] = []
        
        for p in points:
            point_array[0].append(p.x) 
            point_array[1].append(p.y) 
            point_array[2].append(p.z) 
        
        return point_array

    def SetPolylinePoints(self, idx, xs, ys, zs):
        if not xs or len(xs) == 0:
            return

        self.write_test()
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        no_points_per_streamed_unit = self._table_handler.no_points_per_streamed_unit(len(xs), self._plink._preferred_streamed_unit_bytes)
        no_points = len(xs)
        start_inds = range(0, no_points, no_points_per_streamed_unit)
        
        iterable_requests = map(
            lambda start_ind : self._table_handler.setpoints_request(start_ind, po_guid, xs, ys, zs, no_points_per_streamed_unit, idx = idx),
            start_inds
        )

        ok = self._channel.PolylineSet_SetPolylinePoints(iterable_requests)
        return ok.value

    def AddPolyline(self, arrayx, arrayy, arrayz, closed):
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        point_inds = range(len(arrayx))
        iterable_requests = map(
            lambda point_ind : self._add_polyline_request(po_guid, arrayx[point_ind], arrayy[point_ind], arrayz[point_ind], closed),
            point_inds
        )

        return self._channel.PolylineSet_AddPolyline(iterable_requests).value

    def _add_polyline_request(self, po_guid, x, y, z, closed):
        point = petrelinterface_pb2.Primitives.Double3(x = x, y = y, z = z)
        return petrelinterface_pb2.AddPolyline_Request(
            guid = po_guid,
            point = point,
            closed = closed
        )

    def DeletePolyline(self, polyline_index):
        self.write_test()
        self._plink._opened_test()
        po_guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        request = petrelinterface_pb2.PetrelObjectGuidAndIndex(guid = po_guid, index = polyline_index)        
        return self._channel.PolylineSet_DeletePolyline(request).value

    def DeleteAll(self):
        self._plink._opened_test()

        request = petrelinterface_pb2.PolylineSet_DeleteAll_Request(
            guid = petrelinterface_pb2.PetrelObjectGuid(guid = self._guid, sub_type = self._sub_type)
        )

        response = self._channel.PolylineSet_DeleteAll(request)
             
        return response.DeleteAll

