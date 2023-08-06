# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



__version__ = '2.0.0'
__git_hash__ = 'c81667b1'

from cegalprizm.pythontool._toolmode import _ToolMode

if not _ToolMode.is_oop():
    try:
        import PythonPetrelObjectFactory # type: ignore
    except ImportError:
        # will fail when running unittests from outside Petrel environment
        pass

import sys

if _ToolMode.is_oop():
    from cegalprizm.pythontool.ooponly.ip_oop_transition import Point

from cegalprizm.pythontool import _utils

from cegalprizm.pythontool.petrelobject import PetrelObject

from cegalprizm.pythontool.petrellink import PetrelLink
from cegalprizm.pythontool.grid import Grid
from cegalprizm.pythontool.gridproperty import GridProperty, GridDiscreteProperty
from cegalprizm.pythontool.seismic import SeismicCube, SeismicLine
from cegalprizm.pythontool.surface import Surface, SurfaceAttribute, SurfaceDiscreteAttribute, Surfaces, SurfaceAttributes
from cegalprizm.pythontool.welllog import WellLog, DiscreteWellLog, LogSamples, LogSample, GlobalWellLog, DiscreteGlobalWellLog, Logs
from cegalprizm.pythontool.borehole import Well
from cegalprizm.pythontool.points import PointSet
from cegalprizm.pythontool.polylines import PolylineSet, Polyline
from cegalprizm.pythontool.horizoninterpretation import HorizonInterpretation, HorizonInterpretation3d, HorizonProperty3d
from cegalprizm.pythontool.wellsurvey import WellSurvey
from cegalprizm.pythontool.wavelet import Wavelet
from cegalprizm.pythontool.workflow import Workflow
from cegalprizm.pythontool.observeddata import ObservedData, ObservedDataSet
from cegalprizm.pythontool.primitives import Extent, Indices, Annotation, CoordinatesExtent, AxisExtent
from cegalprizm.pythontool.chunk import Chunk, Slice # Slice for backwards compatability
from cegalprizm.pythontool.chunktype import ChunkType
from cegalprizm.pythontool.exceptions import PythonToolException
from cegalprizm.pythontool.observeddata import ObservedDataSet, ObservedDataSets
from cegalprizm.pythontool.petrellink import DiscreteGlobalWellLogs, GlobalWellLogs
from cegalprizm.pythontool._toolmode import _ToolMode
from cegalprizm.pythontool.welllog import DiscreteWellLog, GlobalWellLog, WellLog
if _ToolMode.is_oop():
    from cegalprizm.pythontool.petrelconnection import PetrelConnection, make_connection
else:
    PetrelConnection = None
    make_connection = None

import cegalprizm.pythontool.transactions




    
