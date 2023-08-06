# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool import gridproperty
from cegalprizm.pythontool import grid
from cegalprizm.pythontool import seismic
from cegalprizm.pythontool import surface
from cegalprizm.pythontool import welllog
from cegalprizm.pythontool import borehole
from cegalprizm.pythontool import points
from cegalprizm.pythontool import polylines
from cegalprizm.pythontool import wavelet
from cegalprizm.pythontool import _utils
from cegalprizm.pythontool import exceptions
from cegalprizm.pythontool import horizoninterpretation
from cegalprizm.pythontool import wellsurvey
from cegalprizm.pythontool import observeddata
from cegalprizm.pythontool._system import _system
import datetime
import contextlib

class PetrelLink(object):
    """Supplies pre-existing Petrel objects to Python code"""

    def __init__(
        self, factory, message_helper=None, workflow_vars_helper=None, progress=None
    ):
        # take a reference to the injected factory
        # in case we change the mechanism
        self._factory = factory
        self._message_helper = message_helper
        self._vars = PetrelWorkflowVars(workflow_vars_helper)
        self._progress = progress
        self._properties = Properties(factory)
        self._discrete_properties = DiscreteProperties(factory)
        self._grids = Grids(factory)
        self._seismic_cubes = SeismicCubes(factory)
        self._seismic_lines = SeismicLines(factory)
        self._surfaces = Surfaces(factory)
        self._surface_attributes = SurfaceAttributes(factory)
        self._surface_discrete_attributes = SurfaceDiscreteAttributes(factory)
        self._wavelets = Wavelets(factory)
        self._well_logs = WellLogs(factory)
        self._global_well_logs = GlobalWellLogs(factory)
        self._discrete_global_well_logs = DiscreteGlobalWellLogs(factory)
        self._discrete_well_logs = DiscreteWellLogs(factory)
        self._pointsets = PointSets(factory)
        self._polylinesets = PolylineSets(factory)
        self._wells = Wells(factory)
        self._horizon_interpretation_3ds = HorizonInterpretation3ds(factory)
        self._well_surveys = WellSurveys(factory)
        self._horizon_interpretations = HorizonInterpretations(factory)
        self._observed_data = ObservedData(factory)
        self._observed_data_sets = ObservedDataSets(factory)

    @property
    def grid_properties(self):
        """Access to the Petrel Property objects via a :class:`cegalprizm.pythontool.petrellink.Properties` object"""
        return self._properties

    @property
    def grids(self):
        """Access to the Petrel Grid Model objects via a :class:`cegalprizm.pythontool.petrellink.Grids` object"""
        return self._grids

    @property
    def seismic_cubes(self):
        """Access to the Petrel Seismic 3D objects via a :class:`cegalprizm.pythontool.petrellink.SeismicCubes` object"""
        return self._seismic_cubes

    @property
    def seismic_lines(self):
        """Access to the Petrel Seismic 2D objects via a :class:`cegalprizm.pythontool.petrellink.SeismicsLines` object"""
        return self._seismic_lines

    @property
    def surfaces(self):
        """Access to the Petrel Surface objects via a :class:`cegalprizm.pythontool.petrellink.Surfaces` object"""
        return self._surfaces

    @property
    def surface_attributes(self):
        """Access to the Petrel Surface Attribute objects via a :class:`cegalprizm.pythontool.petrellink.SurfaceAttributes` object"""
        return self._surface_attributes

    @property
    def discrete_grid_properties(self):
        """Access to the Petrel Dictionary Property objects via a :class:`cegalprizm.pythontool.petrellink.DictionaryProperties` object"""
        return self._discrete_properties

    @property
    def surface_discrete_attributes(self):
        """Access to the Petrel Discrete Surface Attribute objects via a :class:`cegalprizm.pythontool.petrellink.DiscreteSurfaceAttributes` object"""
        return self._surface_discrete_attributes

    @property
    def wavelets(self):
        """Access to the Petrel wavelets objects via a :class:`cegalprizm.pythontool.petrellink.Wavelets` object"""
        return self._wavelets

    @property
    def well_logs(self):
        """Access to the Petrel Well Logs objects via a :class:`cegalprizm.pythontool.petrellink.WellLogs` object"""
        return self._well_logs

    @property
    def global_well_logs(self):
        """Access to the Petrel Global Well Logs objects via a :class:`cegalprizm.pythontool.petrellink.GlobalWellLogs` object"""
        return self._global_well_logs

    @property
    def discrete_global_well_logs(self):
        """Access to the Petrel Discrete Global Well Logs objects via a :class:`cegalprizm.pythontool.petrellink.DiscreteGlobalWellLogs` object"""
        return self._discrete_global_well_logs

    @property
    def discrete_well_logs(self):
        """Access to the Petrel Well Logs objects via a :class:`cegalprizm.pythontool.petrellink.DiscreteWellLogs` object"""
        return self._discrete_well_logs

    @property
    def well_surveys(self):
        """Access to the Petrel Well Logs objects via a :class:`cegalprizm.pythontool.petrellink.WellSurveys` object"""
        return self._well_surveys

    @property
    def pointsets(self):
        """Access to the Petrel PointSet objects via a :class:`cegalprizm.pythontool.petrellink.PointSets` object"""
        return self._pointsets

    @property
    def polylinesets(self):
        """Access to the Petrel PolylineSet objects via a :class:`cegalprizm.pythontool.petrellink.PolylineSets` object"""
        return self._polylinesets

    @property
    def wells(self):
        """Access to the Petrel Well objects via a :class:`cegalprizm.pythontool.petrellink.Wells` object"""
        return self._wells

    @property
    def horizon_interpretation_3ds(self):
        """Access to Petrel 3d grid interpretation objects via a :class:'cegalprizm.pythontool.petrellink.HorizonInterpretation3d' object"""
        return self._horizon_interpretation_3ds

    @property
    def horizon_interpretations(self):
        """Access to Petrel seismic horizon objects via a :class:'cegalprizm.pythontool.petrellink.HorizonInterpretation' object"""
        return self._horizon_interpretations

    @property
    def workflow_vars(self):
        """Read- and write-access to the Petrel workflow variables via a :class:`cegalprizm.pythontool.petrellink.PetrelWorkflowVars` object

        Returns:
            A `WorkflowVars` object which allows read and write access
            to the Petrel workflow variables (the 'dollar variables')
        """
        return self._vars
    
    @property
    def observed_data_sets(self):
        """Access to Petrel observed data set objects via a :class:'cegalprizm.pythontool.petrellink.ObservedDataSet' object"""
        return self._observed_data_sets
    
    @property
    def predefined_global_observed_data(self):
        """Returns a dictionary with the predefined global observed data in the petrel project

        keys: the name of the predefined global observed data
        values: the ID used to identify the predefined global observed data
        """
        predef_dict = self._factory.GetPredefinedGlobalObservedData()
        py_dict = {}
        for k in predef_dict.Keys:
            py_dict[k] = predef_dict[k]
        return py_dict

    def message_dialog(self, msg, show_in_msg_log=True):
        """Shows a message dialog

        Shows a message dialog and log the message in the
        OceanPetrel.log file.  If `show_in_msg_log` is `True`, the
        message is also shown in the Message Log window - in this
        case, the message will appear twice in OceanPetrel.log.

        Execution of the script will pause until the dialog is
        cleared.

        Args:

            show_in_msg_log (bool): Also write the message to the
                                        Message Log.

        """
        self._message_helper.MessageDialog(msg, show_in_msg_log)

    def warning_dialog(self, msg, show_in_msg_log=True):
        """Shows a warning dialog

        Shows a warning dialog and log the warning in the
        OceanPetrel.log file.  If `show_in_msg_log` is `True`, the
        message is also shown in the Message Log window - in this
        case, the message will appear twice in OceanPetrel.log.

        Execution of the script will pause until the dialog is
        cleared.

        Args:

            show_in_msg_log (bool): Also write the message to the
                                        Message Log.
        """
        self._message_helper.WarningDialog(msg, show_in_msg_log)

    def error_dialog(self, msg, show_in_msg_log=True):
        """Shows a warning dialog

        Shows a warning dialog and log the warning in the
        OceanPetrel.log file.  If `show_in_msg_log` is `True`, the
        message is also shown in the Message Log window - in this
        case, the message will appear twice in OceanPetrel.log.
        Execution of the script will pause until the dialog is
        cleared.

        Args:

            show_in_msg_log (bool): Also write the message to the
                                        Message Log.
        """
        self._message_helper.ErrorDialog(msg, show_in_msg_log)

    def set_progress(self, value):
        """Sets Petrel progress bar's value

        The Petrel progress bar displays values from 0 to 100%
        inclusive.  Petrel will update the bar on its own schedule -
        the visible value may not reflect this method's argument
        immediately.

        Args:
            value (int): a number between 0 and 100

        Raises:
            ValueError: if the value is not between 0 and 100

        """
        if value < 0 or value > 100:
            raise ValueError("value must be between 0 and 100")

        self._progress.SetStatus(value + 1)

    def set_statusbar_text(self, msg):
        """Sets the text of Petrel's status bar

        Args:
           msg (str):  the text of the status bar
        """
        self._progress.SetText(msg)

    @contextlib.contextmanager
    def create_transaction(self, obj, *objs):
        """Creates a context-manager which wraps the operation in a transaction

        Within a transaction, writing to disk is batched leading to
        considerable speed-ups.  Use this context-manager in a
        standard `with` block and the transaction will be
        automatically committed at the end of the block.  Petrel
        sometimes will decide to write to disk earlier if that is the
        most efficient way.  Unlike database transactions, you cannot roll-back
        any changes.

        Args:
           objs: a variable number of Petrel objects to hold in a transaction


        **Example**:

        .. code-block:: Python

            # assumes my_cube1 and my_cube2 are the same size...
            with petrellink.create_transaction(my_cube1, my_cube2):
                for i in range(0, my_cube1.extent.i):
                    for j in range(0, my_cube1.extent.j):
                        my_cube1.column(i, j).set(0.5) # writing deferred!
                        my_cube2.column(i, j).set(0.8) # writing deferred!
        """
        tx = self._factory.CreateTxProvider()
        try:
            tx.Add(obj._petrel_object_link.PetrelObject)
            if objs is not None:
                for o in objs:
                    tx.Add(o._petrel_object_link.PetrelObject)
            tx.StartTxs()
            yield
        finally:
            tx.CommitTxs()

    def _get_grid(self, name):

        """Returns a Petrel grid object"""
        return grid.Grid(self._factory.GetGridObject(name))

    def _get_property(self, name):
        """Returns a Petrel grid property object"""
        return gridproperty.GridProperty(self._factory.GetPropertyObject(name))

    def _get_seismic(self, name):
        """Returns a Petrel seismic 3d cube"""
        return seismic.Seismic(self._factory.GetSeismicObject(name))

class PetrelObjectStore(object):
    """A read-only collection storing Petrel objects by name.  When iterated over,
    the objects are returned, not their names (unlike a standard Python dictionary)"""

    def __init__(self, factory):
        self._objects = self._query_objects(factory)

    def __getitem__(self, key):
        return self._objects[key]

    def __setitem__(self, key, value):
        raise exceptions.PythonToolException("Cannot add to Petrel objects")

    def __len__(self):
        return len(self._objects)

    def __iter__(self):
        # This is not dict-like behaviour!
        return iter(self._objects.values())

    def keys(self):
        """The names of the Petrel objects

        Returns:
            A list of the names Petrel objects as set by the Tool user-interface
        """
        return self._objects.keys()

    def values(self):
        """The Petrel objects

        Returns:
            A list of the Petrel objects"""
        return self._objects.values()

    def items(self):
        """The (`name`, `Petrel object`) pairs available

        Returns:
            A list of (`name`, `objects`) tuples (pairs) available
        """
        return self._objects.items()

    def __str__(self) -> str:
        contents = ["'{}' : {}".format(k, v) for (k, v) in self.items()]
        return ', '.join(contents)

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, str(self))

class Properties(PetrelObjectStore):
    """A read-only collection storing GridProperty objects

    **Example**:

    .. code-block:: Python

        my_prop = petrellink.grid_properties["var1"]
        # my_prop now references the 'var1' property
        print(my_prop.petrel_name)
    """

    def _query_objects(self, factory):
        properties = {}
        for prop_name in factory.GetPropertyObjectNames():
            properties[prop_name] = gridproperty.GridProperty(
                factory.GetPropertyObject(prop_name)
            )
        return properties

class DiscreteProperties(PetrelObjectStore):
    """A read-only collection storing GridDiscreteProperty objects

    **Example**:

    .. code-block:: Python

        my_prop = petrellink.discrete_grid_properties["var1"]
        # my_prop now references the 'var1' property
        print(my_prop.petrel_name)
        # outputs (for example) 'Facies'
    """

    def _query_objects(self, factory):
        properties = {}
        for prop_name in factory.GetDictionaryPropertyObjectNames():
            properties[prop_name] = gridproperty.GridDiscreteProperty(
                factory.GetDictionaryPropertyObject(prop_name)
            )
        return properties

class Grids(PetrelObjectStore):
    """A read-only collection storing Grid objects"""

    def _query_objects(self, factory):
        grids = {}
        for grid_name in factory.GetGridObjectNames():
            grids[grid_name] = grid.Grid(factory.GetGridObject(grid_name))
        return grids

class HorizonInterpretation3ds(PetrelObjectStore):
    def _query_objects(self, factory):
        his = {}
        for name in factory.GetHorizonInterpretation3dObjectNames():
            his[name] = horizoninterpretation.HorizonInterpretation3d(
                factory.GetHorizonInterpretation3dObject(name)
            )
        return his

class HorizonInterpretations(PetrelObjectStore):
    def _query_objects(self, factory):
        his = {}
        for name in factory.GetHorizonInterpretationObjectNames():
            his[name] = horizoninterpretation.HorizonInterpretation(
                factory.GetHorizonInterpretationObject(name)
            )
        return his

class SeismicCubes(PetrelObjectStore):
    def _query_objects(self, factory):
        seismics = {}
        for name in factory.GetSeismicObjectNames():
            seismics[name] = seismic.SeismicCube(factory.GetSeismicObject(name))
        return seismics

class SeismicLines(PetrelObjectStore):
    def _query_objects(self, factory):
        seismic2ds = {}
        for name in factory.GetSeismic2dObjectNames():
            seismic2ds[name] = seismic.SeismicLine(factory.GetSeismic2dObject(name))
        return seismic2ds

class Surfaces(PetrelObjectStore):
    """A read-only collection storing Surface objects"""

    def _query_objects(self, factory):
        surfaces = {}
        for surface_name in factory.GetSurfaceObjectNames():
            surfaces[surface_name] = surface.Surface(
                factory.GetSurfaceObject(surface_name)
            )
        return surfaces

class SurfaceAttributes(PetrelObjectStore):
    """A read-only collection storing SurfaceaAttribute objects"""

    def _query_objects(self, factory):
        surface_attributes = {}
        for name in factory.GetSurfacePropertyObjectNames():
            surface_attributes[name] = surface.SurfaceAttribute(
                factory.GetSurfacePropertyObject(name)
            )
        return surface_attributes

class SurfaceDiscreteAttributes(PetrelObjectStore):
    """A read-only collection storing SurfaceaDiscreteAttribute objects"""

    def _query_objects(self, factory):
        surface_attributes = {}
        for name in factory.GetDictionarySurfacePropertyObjectNames():
            surface_attributes[name] = surface.SurfaceDiscreteAttribute(
                factory.GetDictionarySurfacePropertyObject(name)
            )
        return surface_attributes

class WellLogs(PetrelObjectStore):
    """A read-only collection storing WelllLog objects"""

    def _query_objects(self, factory):
        well_logs = {}
        for name in factory.GetWellLogObjectNames():
            well_logs[name] = welllog.WellLog(factory.GetWellLogObject(name))
        return well_logs

class Wavelets(PetrelObjectStore):
    """A read-only collection storing Wavelet objects"""
    def _query_objects(self, factory):
        ns = {}
        for name in factory.GetWaveletObjectNames():
            ns[name] = wavelet.Wavelet(
                factory.GetWaveletObject(name)
            )
        return ns

class DiscreteWellLogs(PetrelObjectStore):
    """A read-only collection storing DiscreteWelllLog objects"""

    def _query_objects(self, factory):
        well_logs = {}
        for name in factory.GetDictionaryWellLogObjectNames():
            well_logs[name] = welllog.DiscreteWellLog(
                factory.GetDictionaryWellLogObject(name)
            )
        return well_logs

class GlobalWellLogs(PetrelObjectStore):
    """A read-only collection storing WelllLog objects"""

    def _query_objects(self, factory):
        global_well_logs = {}
        for name in factory.GetGlobalWellLogObjectNames():
            global_well_logs[name] = welllog.GlobalWellLog(
                factory.GetGlobalWellLogObject(name)
            )
        return global_well_logs

class Wells(PetrelObjectStore):
    """A read-only collection for storing Well objects"""

    def _query_objects(self, factory):
        boreholes = {}
        for name in factory.GetBoreholeObjectNames():
            boreholes[name] = borehole.Well(factory.GetBoreholeObject(name))
        return boreholes

class DiscreteGlobalWellLogs(PetrelObjectStore):
    """A read-only collection storing WelllLog objects"""

    def _query_objects(self, factory):
        discrete_global_well_logs = {}
        for name in factory.GetDictionaryGlobalWellLogObjectNames():
            discrete_global_well_logs[name] = welllog.DiscreteGlobalWellLog(
                factory.GetDictionaryGlobalWellLogObject(name)
            )
        return discrete_global_well_logs

class WellSurveys(PetrelObjectStore):
    """A read-only collection storing WellSurvey objects"""
    def _query_objects(self, factory):
        well_surveys = {}
        for name in factory.GetXyzWellSurveyObjectNames():
            well_surveys[name] = wellsurvey.WellSurvey(factory.GetXyzWellSurveyObject(name))
        for name in factory.GetXytvdWellSurveyObjectNames():
            well_surveys[name] = wellsurvey.WellSurvey(factory.GetXytvdWellSurveyObject(name))
        for name in factory.GetDxdytvdWellSurveyObjectNames():
            well_surveys[name] = wellsurvey.WellSurvey(factory.GetDxdytvdWellSurveyObject(name))
        for name in factory.GetMdinclazimWellSurveyObjectNames():
            well_surveys[name] = wellsurvey.WellSurvey(factory.GetMdinclazimWellSurveyObject(name))
        for name in factory.GetExplicitWellSurveyObjectNames():
            well_surveys[name] = wellsurvey.WellSurvey(factory.GetExplicitWellSurveyObject(name))
        return well_surveys

class PointSets(PetrelObjectStore):
    """A read-only collection storing PointSet objects.
    
    ** The implementation of point sets is in a preliminary state. Handling large point sets may
    fail or be slow. We are working on improving this.
    """

    def _query_objects(self, factory):
        point_sets = {}
        for name in factory.GetPointSetObjectNames():
            point_sets[name] = points.PointSet(factory.GetPointSetObject(name))
        return point_sets

class PolylineSets(PetrelObjectStore):
    """A read-only collection storing PolylineSets objects.
    
    ** The implementation of polyline sets is in a preliminary state. Handling large point sets may
    fail or be slow. We are working on improving this.
    """

    def _query_objects(self, factory):
        polyline_sets = {}
        for name in factory.GetPolylineSetObjectNames():
            polyline_sets[name] = polylines.PolylineSet(factory.GetPolylineSetObject(name))
        return polyline_sets

class ObservedData(PetrelObjectStore):
    """A read-only collection storing ObservedData objects"""
    def _query_objects(self, factory):
        observed_data = {}
        for name in factory.GetObservedDataObjectNames():
            observed_data[name] = observeddata.ObservedData(factory.GetObservedDataObject(name))
        return observed_data

class ObservedDataSets(PetrelObjectStore):
    """A read-only collection storing ObservedDataSet objects"""
    def _query_objects(self, factory):
        observed_data_sets = {}
        for name in factory.GetObservedDataSetObjectNames():
            observed_data_sets[name] = observeddata.ObservedDataSet(factory.GetObservedDataSetObject(name))
        return observed_data_sets

class PetrelWorkflowVars(object):

    """Read and write access to the Petrel workflow variables

    Use this class to read and write Petrel workflow variables (the
    'dollar variables'.  These can be of numeric, string or date type,
    and if they are being created, their type is inferred by their new
    value. Once set their type cannot be changed.

    **Example**:

    .. code-block:: Python

        print(petrellink.workflow_vars["$i"])
        # outputs the contents of the $i variable

        petrellink.workflow_vars["$i"] = 42
        # sets $i to 42

        petrellink.workflow_vars["$s"] = "hello"
        # sets $s to "hello"

        petrellink.workflow_vars["$s"] = 10.1
        # error! $s has been set as a string variable and cannot be changed

    """

    def __init__(self, workflow_vars):
        self.__workflow_vars = workflow_vars

    def __getitem__(self, key):
        if self.__workflow_vars is None:
            raise exceptions.PythonToolException(
                "Workflow variables are not available - script must be run as part of workflow"
            )
        try:
            if not self.__workflow_vars.VarExists(key):
                raise exceptions.PythonToolException("Unknown variable name " + key)

            varType = self.__workflow_vars.VarType(key)
            if varType == self.__workflow_vars.WorkflowVariableType.NumericType:
                return self.__workflow_vars.GetVarDouble(key)
            elif varType == self.__workflow_vars.WorkflowVariableType.StringType:
                return self.__workflow_vars.GetVarString(key)
            elif varType == self.__workflow_vars.WorkflowVariableType.DateType:
                return _utils.to_python_datetime(self.__workflow_vars.GetVarDateTime(key).Date)
        except AttributeError:
            raise exceptions.PythonToolException(
                "Workflow variables are not available - script must be run as part of workflow"
            )

        raise exceptions.PythonToolException("Unhandled workflow variable type")

    def __setitem__(self, key, value):
        # n.b. we could chooose to coerce unknown types (using __str__ or __repr__)
        # but that's likely to confuse users more than help
        if self.__workflow_vars is None:
            raise exceptions.PythonToolException("Workflow variables are not available")

        try:
            if isinstance(value, str):
                self.__workflow_vars.SetVarString(key, value)
            elif isinstance(value, int) or isinstance(value, float):
                self.__workflow_vars.SetVarDouble(key, value)
            elif isinstance(value, _system().DateTime):
                self.__workflow_vars.SetVarDateTime(key, value)
            elif isinstance(value, datetime.date):
                self.__workflow_vars.SetVarDateTime(
                    key, _system().DateTime(value.year, value.month, value.day)
                )
            elif isinstance(value, datetime.datetime):
                self.__workflow_vars.SetVarDateTime(
                    key,
                    _system().DateTime(
                        value.year,
                        value.month,
                        value.day,
                        value.hour,
                        value.minute,
                        value.second,
                    ),
                )
            else:
                raise exceptions.PythonToolException("Unhandled workflow variable type")
        except SystemError as e:
            # one of the few occassions we let exceptions propagate from Petrel
            # - convert error to Pythonic one
            raise ValueError(e)